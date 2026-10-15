"""Art library: the printed art of every base card, cut once from its scan by the measured window, kept twice:
the original crop (master, untouched pixels) and a RealESRGAN x4plus upscale (Bill 2026-10-14). A manifest records
where each crop came from, so a better scan can replace it later and be re-upscaled.

    python3 art_library.py collect            # VS1-17 base cards → library/manifest.json + masters
    python3 art_library.py upscale [N]        # upscale masters that have no @4x yet (N at most)
    python3 art_library.py sheet OUT.png [ids…]   # review sheet: original | upscale

Window = the one the remasters use (template art window mapped onto the scan, or the card's measured art.rect /
art.bbox, with the Episode I edge trim), so the library matches what Bill already approved on the wiki.
"""
from __future__ import annotations
import json, re, sys, glob, hashlib
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "library"
MODEL = Path("/tmp/claude-0/models/x4plus128.onnx")   # RealESRGAN x4plus (ONNX, 128 px tiles)


def load_scan(src: Path) -> Image.Image:
    im = Image.open(src)
    if im.mode == "P" and "transparency" in im.info:
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im.convert("RGBA")); im = bg
    return im.convert("RGB")


def art_box(card: dict, T: dict, im: Image.Image) -> list[int]:
    """Same mapping as render.art_crop, returning the scan-space window instead of cropping (no aspect cover-fit)."""
    a = np.array(im).astype(int)
    if card["art"].get("rect"):
        return [int(v) for v in card["art"]["rect"]]
    tpl = T[card["template"]]
    if card["art"].get("bbox"):
        fx0, fy0, fx1, fy1 = card["art"]["bbox"]
    elif tpl.get("system"):
        m = a.max(axis=2) > 40
        rows = np.where(m.mean(axis=1) > 0.05)[0]; cols = np.where(m.mean(axis=0) > 0.05)[0]
        return [int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())]   # full-art system card
    else:
        bright = a.sum(axis=2) > 120
        rows = np.where(bright.mean(axis=1) > 0.5)[0]; cols = np.where(bright.mean(axis=0) > 0.5)[0]
        fx0, fy0, fx1, fy1 = cols.min(), rows.min(), cols.max(), rows.max()
    cw, ch = (1931, 1343) if tpl.get("landscape") else (1343, 1931)
    sx = (fx1 - fx0) / cw; sy = (fy1 - fy0) / ch
    if not card["art"].get("bbox") and abs(sy / sx - 1) > 0.015:
        sy = sx
        if fy0 <= 1: fy0 = fy1 - ch * sx
        else: fy1 = fy0 + ch * sx
    ax, ay, aw, ah = tpl["art"]
    box = [int(round(v)) for v in (fx0 + (ax - 144) * sx, fy0 + (ay - 144) * sy, fx0 + (ax + aw - 144) * sx, fy0 + (ay + ah - 144) * sy)]
    if card.get("art_trim"):
        x0, y0, x1, y1 = box
        sub = a[max(y0, 0):y1, max(x0, 0):x1]
        def silver(line):
            mx, mn = line.max(axis=1), line.min(axis=1)
            return line.mean() > 100 and (mx - mn).mean() < 45
        h, w = sub.shape[:2]
        def innermost(lines, n):
            cut = 0
            for i in range(n):
                if silver(lines(i)): cut = i + 1
            return cut
        box = [x0 + innermost(lambda i: sub[:, i], int(w * .15)), y0 + innermost(lambda i: sub[i], int(h * .15)),
               x1 - innermost(lambda i: sub[:, w - 1 - i], int(w * .15)), y1 - innermost(lambda i: sub[h - 1 - i], int(h * .15))]
    W, H = im.size
    box = [max(box[0], 0), max(box[1], 0), min(box[2], W), min(box[3], H)]
    return box


def snap_edges(a: np.ndarray, box: list[int], r: int = 12) -> list[int]:
    """Move each side of the mapped window to the strongest straight edge within ±r px: the printed window's keyline
    is a crisp line running the whole side, picture edges rarely are. Inset 1 px so the keyline itself stays out."""
    g = a.astype(float).mean(axis=2)
    gy = np.abs(np.diff(g, axis=0)); gx = np.abs(np.diff(g, axis=1))
    x0, y0, x1, y1 = box; H, W = g.shape
    def best(prof_fn, c, lo, hi):
        sc = [(prof_fn(v), v) for v in range(max(c - r, lo), min(c + r, hi))]
        return max(sc)[1] if sc else c
    mx0, mx1 = x0 + (x1 - x0) // 10, x1 - (x1 - x0) // 10; my0, my1 = y0 + (y1 - y0) // 10, y1 - (y1 - y0) // 10
    # row edge strength: fraction of the span with a strong step (robust to picture content)
    rowp = lambda v: (gy[v, mx0:mx1] > 18).mean()
    colp = lambda v: (gx[my0:my1, v] > 18).mean()
    t = best(rowp, y0, 1, H - 2); b = best(rowp, y1, 1, H - 2)
    l = best(colp, x0, 1, W - 2); rr = best(colp, x1, 1, W - 2)
    # the step at row v is between v and v+1: inside starts at v+1 for the top, ends at v for the bottom
    nb = [l + 2, t + 2, rr - 1, b - 1]
    if (nb[2] - nb[0]) < 0.8 * (x1 - x0) or (nb[3] - nb[1]) < 0.8 * (y1 - y0):
        return box   # implausible: keep the mapped window
    return nb


def trim_frame(a: np.ndarray, box: list[int], frac: float = 0.09) -> list[int]:
    """Trim frame colour and the window's dark keyline off each edge: a line is frame when its median colour is
    close to the frame band just outside the window (or near-black keyline) and it is fairly uniform."""
    x0, y0, x1, y1 = box; H, W = a.shape[:2]
    def frame_col(side):
        if side == "t": band = a[max(y0 - 6, 0):max(y0 - 1, 1), x0:x1]
        elif side == "b": band = a[min(y1 + 1, H - 1):min(y1 + 6, H), x0:x1]
        elif side == "l": band = a[y0:y1, max(x0 - 6, 0):max(x0 - 1, 1)]
        else: band = a[y0:y1, min(x1 + 1, W - 1):min(x1 + 6, W)]
        return np.median(band.reshape(-1, 3), axis=0) if band.size else None
    def is_frame(line, fc):
        med = np.median(line, axis=0); spread = np.percentile(np.abs(line - med).sum(axis=1), 75)
        dark = med.max() < 45
        near = fc is not None and np.abs(med - fc).sum() < 70
        return (near or dark) and spread < 90
    out = list(box)
    for side in "tblr":
        fc = frame_col(side); n = int((y1 - y0 if side in "tb" else x1 - x0) * frac); cut = 0
        for i in range(n):
            if side == "t": line = a[y0 + i, x0:x1]
            elif side == "b": line = a[y1 - 1 - i, x0:x1]
            elif side == "l": line = a[y0:y1, x0 + i]
            else: line = a[y0:y1, x1 - 1 - i]
            if is_frame(line.astype(int), fc): cut = i + 1
            elif i > cut + 2: break
        if side == "t": out[1] = y0 + cut
        elif side == "b": out[3] = y1 - cut
        elif side == "l": out[0] = x0 + cut
        else: out[2] = x1 - cut
    return out


def key_for(src: str, c: dict) -> str:
    stem = Path(src).stem.replace("-decipher-archive", "")
    stem = re.sub(r"^\d+b?-", "", stem)                       # cards' local copies are prefixed "NN-"
    if "src/slips/" in src:                                    # art printed on the slip itself (VS17)
        return f"OVS{c['virtual_set']}-{int(c['number']):02d}-slip"
    return stem


def collect():
    sys.path.insert(0, str(ROOT))
    import render, build_vs
    LIB.mkdir(exist_ok=True); (LIB / "orig").mkdir(exist_ok=True)
    man = json.loads((LIB / "manifest.json").read_text()) if (LIB / "manifest.json").exists() else {}
    for p in sorted(ROOT.glob("cards/vs*/[0-9][0-9]*.json")):
        if p.name.endswith(".card.json") or not re.fullmatch(r"\d\d[a-z]?", p.stem):
            continue
        vs = int(p.parent.name[2:]); c = json.loads(p.read_text(encoding="utf-8"))
        try:
            card = build_vs.convert(c, vs)
        except Exception as e:
            print("skip", p, e); continue
        if not card.get("art", {}).get("src"):
            continue
        printed = (c.get("art") or {}).get("src")
        if printed and not c.get("slip_art"):   # the library holds the PRINTED card's art, not a PC reissue's
            card["art"]["src"] = printed
        src = card["art"]["src"]
        k = key_for(src, c)
        if k in man:
            man[k].setdefault("used_by", []).append(card["id"]) if card["id"] not in man[k].get("used_by", []) else None
            continue
        im = load_scan(ROOT / src)
        box = art_box(card, render.TEMPLATES, im)
        crop = im.crop(box)
        out = LIB / "orig" / f"{k}.png"; crop.save(out)
        man[k] = {"key": k, "source_file": src, "source_size": list(im.size), "box": box, "size": list(crop.size),
                  "window": "rect" if card["art"].get("rect") else ("bbox" if card["art"].get("bbox") else "template"),
                  "template": card["template"], "title": c.get("base_title") or c.get("title"), "used_by": [card["id"]],
                  "sha1": hashlib.sha1(out.read_bytes()).hexdigest()[:12], "upscale": None}
        print(k, box, crop.size)
    (LIB / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(len(man), "entries")


def upscale(limit: int | None = None):
    import onnxruntime as ort
    sess = ort.InferenceSession(str(MODEL))
    man = json.loads((LIB / "manifest.json").read_text()); (LIB / "x4").mkdir(exist_ok=True)
    done = 0
    for k, e in man.items():
        if e.get("upscale"):
            continue
        a = np.array(Image.open(LIB / "orig" / f"{k}.png").convert("RGB")).astype(np.float32) / 255
        Tz, pad = 128, 12; step = Tz - 2 * pad; H, W = a.shape[:2]
        outp = np.zeros((H * 4, W * 4, 3), np.float32)
        for y in range(0, H, step):
            for x in range(0, W, step):
                y0 = max(min(y - pad, H - Tz), 0); x0 = max(min(x - pad, W - Tz), 0)
                tile = np.zeros((Tz, Tz, 3), np.float32); sub = a[y0:y0 + Tz, x0:x0 + Tz]; tile[:sub.shape[0], :sub.shape[1]] = sub
                r = sess.run(None, {"image": tile.transpose(2, 0, 1)[None]})[0][0].transpose(1, 2, 0)
                ye, xe = min(y + step, H), min(x + step, W)
                outp[y * 4:ye * 4, x * 4:xe * 4] = r[(y - y0) * 4:(ye - y0) * 4, (x - x0) * 4:(xe - x0) * 4]
        Image.fromarray((np.clip(outp, 0, 1) * 255).round().astype(np.uint8)).save(LIB / "x4" / f"{k}.webp", quality=92, method=6)
        e["upscale"] = {"model": "RealESRGAN_x4plus (ONNX)", "scale": 4}
        done += 1
        (LIB / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
        print(k, done, flush=True)
        if limit and done >= limit:
            break


def sheet(out: str, keys: list[str]):
    from PIL import ImageDraw
    man = json.loads((LIB / "manifest.json").read_text())
    keys = keys or [k for k, e in man.items() if e.get("upscale")][:12]
    rows = []
    for k in keys:
        o = Image.open(LIB / "orig" / f"{k}.png").convert("RGB"); u = Image.open(LIB / "x4" / f"{k}.webp").convert("RGB")
        w = 520; h = int(u.height * w / u.width)
        r = Image.new("RGB", (w * 2 + 10, h + 22), "white"); d = ImageDraw.Draw(r)
        r.paste(o.resize((w, h), Image.NEAREST), (0, 22)); r.paste(u.resize((w, h), Image.LANCZOS), (w + 10, 22))
        d.text((2, 4), f"{k}  original {o.size[0]}x{o.size[1]}", fill="black"); d.text((w + 12, 4), "RealESRGAN x4plus", fill="black")
        rows.append(r)
    S = Image.new("RGB", (rows[0].width * 2 + 20, sum(r.height + 10 for r in rows[::2]) + 10), "white")
    for i, r in enumerate(rows):
        S.paste(r, ((i % 2) * (r.width + 20), sum(x.height + 10 for x in rows[:i - i % 2:2])))
    S.save(out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "collect": collect()
    elif cmd == "upscale": upscale(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif cmd == "sheet": sheet(sys.argv[2], sys.argv[3:])
