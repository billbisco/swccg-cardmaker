"""Art library for every Decipher card (sets 1–14 and the premium / enhanced products), keyed by GEMP id.

    python3 art_library_all.py fetch          # download each card's printed face (350 px scan) into library/scans/
    python3 art_library_all.py measure        # register each frame family, measure its art window, crop masters
    python3 art_library_all.py sheet FAMILY OUT.png

The printed face is the PC's 350 px GIF (= Decipher's scan). Cards the PC has re-rendered with errata (745 px,
regraded art) use the wiki's Decipher-archive copy of the printed face, else the PC's 2021 .png (a 2x enlargement of
the same scan, art untouched). Each frame family (side, card type, character class, era, orientation) is aligned to
one reference scan (OpenCV ECC, affine, frame-only mask); the art window is where the aligned scans differ (the art)
while the frame stays the same; that window is mapped back into every scan. Scans that do not align are listed, not
guessed (manifest status "unaligned").
"""
from __future__ import annotations
import json, os, re, sys, urllib.request, urllib.parse
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "library"; SCANS = LIB / "scans"; ORIG = LIB / "orig"
MAN = LIB / "manifest-all.json"
UA = {"User-Agent": "HolocronClaude/1.0 (art library)"}
EP1_SETS = {"11", "12", "13", "14"}            # Tatooine, Coruscant, Reflections III, Theed Palace: Episode I frames
LONG = {"Premiere": "Premiere", "ANewHope": "ANewHope", "Hoth": "Hoth", "Dagobah": "Dagobah", "CloudCity": "CloudCity",
        "JabbasPalace": "JabbasPalace", "SpecialEdition": "SpecialEdition", "Endor": "Endor", "DeathStarII": "DeathStarII"}


def cards():
    out = []
    for side in ("Light", "Dark"):
        for c in json.load(open(ROOT / f"gempdata/{side}.json"))["cards"]:
            s = re.sub(r"\D", "", c["set"]) or "0"
            if int(s) < 200:
                out.append(c)
    return out


def get(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def fetch():
    SCANS.mkdir(parents=True, exist_ok=True)
    man = json.loads(MAN.read_text()) if MAN.exists() else {}
    for c in cards():
        gid = c["gempId"]; f = c["front"]; u = f.get("imageUrl")
        if not u or (gid in man and (SCANS / man[gid]["scan"]).exists()):
            continue
        folder, name = re.search(r"/cards/([^/]+)/large/([^/.]+)\.", u).groups()
        e = {"gempId": gid, "title": f.get("title"), "side": c["side"], "set": c["set"], "type": f.get("type"),
             "subType": f.get("subType"), "imageUrl": u}
        try:
            data = get(u); im = Image.open(__import__("io").BytesIO(data))
            src, note = u, "PC 350 px GIF (Decipher's printed scan)"
            if im.size[0] > 600:                                    # PC errata re-render: find the printed face
                data = None
                arch = f"{folder.replace('-Light', '-L').replace('-Dark', '-D')}-{name}-decipher-archive.gif"
                try:
                    d2 = get("https://wiki.swccg.com/index.php?title=Special:FilePath/" + urllib.parse.quote(arch))
                    if d2[:3] == b"GIF": data, src, note = d2, arch, "wiki Decipher-archive copy of the printed face"
                except Exception:
                    pass
                if data is None:
                    try:
                        data = get(u.rsplit(".", 1)[0] + ".png"); src, note = u.rsplit(".", 1)[0] + ".png", "PC 2021 .png (2x of the printed scan)"
                    except Exception:
                        data = get(u); note = "ONLY the PC errata re-render (art regraded) — needs a printed scan"
                        e["status"] = "regraded-only"
            ext = "png" if data[:4] == b"\x89PNG" else "gif"; fn = f"{gid}.{ext}"
            (SCANS / fn).write_bytes(data)
            e.update(scan=fn, scan_source=src, scan_note=note)
            man[gid] = e
            print(gid, f.get("title"), note[:30], flush=True)
        except Exception as ex:
            print("FAIL", gid, u, ex, flush=True)
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(len(man), "cards")


def family(e: dict, size) -> str:
    t = e["type"] or ""
    if t == "Location":
        t = f"Location/{(e.get('subType') or '').split(':')[0].strip()}"
    if t == "Character":
        st = (e.get("subType") or "").split(":")[0].strip()
        t = f"Character/{st}"
    era = ("ep1" if e["set"] in EP1_SETS else "ref2" if e["set"] == "10"
           else "enhanced" if e["set"] in ("108", "109", "110") else "classic")   # reprints have their own frames
    orient = "land" if size[0] > size[1] else "port"
    combo = "|combo" if " & " in (e.get("title") or "") and t in ("Interrupt", "Effect") else ""   # no lore box: art sits higher
    return f"{e['side']}|{t}{combo}|{era}|{orient}"


def load(path: Path) -> Image.Image:
    im = Image.open(path)
    if im.mode == "P" and "transparency" in im.info:
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im.convert("RGBA")); im = bg
    return im.convert("RGB")


def card_norm(im: Image.Image) -> Image.Image:
    """The card itself, without page margin, at the scan's native scale: 350x490 portrait / 490x350 landscape.
    2x enlargements (742 px) come back to 350 px (they hold no more detail); bordered archive copies (367x506)
    lose their white margin; slightly short scans (348x488) are stretched by a pixel or two."""
    a = np.array(im).astype(int)
    ink = a.min(axis=2) < 200                     # anything that is not page white
    rows = np.where(ink.mean(axis=1) > 0.5)[0]; cols = np.where(ink.mean(axis=0) > 0.5)[0]
    if len(rows) and len(cols):
        im = im.crop((int(cols.min()), int(rows.min()), int(cols.max()) + 1, int(rows.max()) + 1))
    land = im.size[0] > im.size[1]
    return im.resize((490, 350) if land else (350, 490), Image.LANCZOS)


def system_box(im: Image.Image) -> list[int]:
    """Systems are full-art: the picture runs between the two bars (top bar upside down). Each bar's inner edge is the
    strongest full-width horizontal edge near its usual place (bars sit a little differently per set)."""
    a = np.array(im).astype(float)
    d = np.abs(np.diff(a, axis=0)).sum(axis=2)[:, 30:320]          # RGB step between row y and y+1
    score = (d > 60).mean(axis=1)
    top = 70 + int(np.argmax(score[70:125])) + 3
    bot = 360 + int(np.argmax(score[360:415])) - 2
    return [14, top, 336, bot]


def snap_inward(a: np.ndarray, box: list[int], reach: int = 16) -> list[int]:
    """Move each side inward to a straight edge that spans nearly the whole side (a frame band, banner or bar the
    family window let in, e.g. the Sabacc interrupts' shorter window); only ever shrinks, and only within `reach`."""
    g = a.astype(float); x0, y0, x1, y1 = box
    def row_edge(y): return (np.abs(g[y, x0:x1] - g[y + 1, x0:x1]).sum(1) > 60).mean()
    def col_edge(x): return (np.abs(g[y0:y1, x] - g[y0:y1, x + 1]).sum(1) > 60).mean()
    for y in range(y0 + reach, y0 - 1, -1):
        if row_edge(y) > 0.75: y0 = y + 1; break
    for y in range(y1 - reach, y1 - 1):
        if row_edge(y) > 0.75: y1 = y + 1; break
    for x in range(x0 + reach, x0 - 1, -1):
        if col_edge(x) > 0.8: x0 = x + 1; break
    for x in range(x1 - reach, x1 - 1):
        if col_edge(x) > 0.8: x1 = x + 1; break
    return [x0, y0, x1, y1]


def trim_lines(a: np.ndarray, box: list[int], most: int = 5) -> list[int]:
    """Peel off up to `most` px per side while the outermost line is a uniform line that differs from the picture
    just inside it (a frame keyline the family window left in)."""
    x0, y0, x1, y1 = box
    def is_line(line, inner):
        med = np.median(line, 0)
        return np.median(np.abs(line - med).sum(1)) < 30 and np.abs(med - np.median(inner, 0)).sum() > 24
    for _ in range(most):
        if is_line(a[y0, x0:x1], a[y0 + 3, x0:x1]): y0 += 1
        else: break
    for _ in range(most):
        if is_line(a[y1 - 1, x0:x1], a[y1 - 4, x0:x1]): y1 -= 1
        else: break
    for _ in range(most):
        if is_line(a[y0:y1, x0], a[y0:y1, x0 + 3]): x0 += 1
        else: break
    for _ in range(most):
        if is_line(a[y0:y1, x1 - 1], a[y0:y1, x1 - 4]): x1 -= 1
        else: break
    return [x0, y0, x1, y1]


def measure(only: str | None = None):
    import cv2
    ORIG.mkdir(exist_ok=True)
    man = json.loads(MAN.read_text())
    fams = defaultdict(list)
    for gid, e in man.items():
        if not e.get("scan"):
            continue
        if not only:
            e.pop("status", None) if e.get("status") != "regraded-only" else None
        im = load(SCANS / e["scan"]); e["scan_size"] = list(im.size)
        fams[family(e, card_norm(im).size)].append(gid)
    # tiny reprint families give no usable variance: fold them into the parent frame family (same card frame)
    for fam in [f for f in fams if len(fams[f]) < 8 and ("|ref2|" in f or "|enhanced|" in f)]:
        parent = fam.replace("|ref2|", "|classic|").replace("|enhanced|", "|classic|")
        if parent in fams and len(fams[parent]) >= 8:
            fams[parent] += fams.pop(fam)
    report = {}
    for fam, mem in sorted(fams.items(), key=lambda x: -len(x[1])):
        if only and only != fam:
            continue
        land = fam.endswith("land"); S = (490, 350) if land else (350, 490)
        if ("|Location/System|" in fam or "|Location/Sector|" in fam) and fam.endswith("port"):
            for g in mem:
                im = card_norm(load(SCANS / man[g]["scan"])); SYS = system_box(im); im.crop(SYS).save(ORIG / f"{g}.png")
                man[g].update(status="ok", family=fam, box=SYS, box_space="card350", size=[SYS[2] - SYS[0], SYS[3] - SYS[1]], system=True)
                man[g].pop("full_art", None)
            report[fam] = (len(mem), f"system: between the bars {SYS}"); continue
        if len(mem) < 2 or ("|combo|" in fam and len(mem) < 4):
            for g in mem: man[g].update(status="family-too-small", family=fam)
            report[fam] = (len(mem), "too small"); continue
        data = {}
        for g in mem:
            im = card_norm(load(SCANS / man[g]["scan"])); sc = 1.0
            G = np.array(im.convert("L")).astype(np.float32)
            data[g] = (G, sc, im)
        # reference: the scan closest to the family's median image (the most typical one)
        medimg = np.median(np.stack([d[0] for d in data.values()]), axis=0)
        ref = min(mem, key=lambda g: np.abs(data[g][0] - medimg).mean())
        R = data[ref][0]
        # first pass mask: whole card; second pass: frame only (outside the measured art window)
        CC = {}
        def align(mask):
            W = {}
            for g, (G, sc, im) in data.items():
                w = np.eye(2, 3, dtype=np.float32)
                try:
                    cc, w = cv2.findTransformECC(R, G, w, cv2.MOTION_AFFINE,
                                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-5), mask, 5)
                    if cc < 0.6 or abs(w[0, 0] - 1) > .08 or abs(w[1, 1] - 1) > .08: w = None
                    else: CC[g] = cc
                except cv2.error:
                    w = None
                W[g] = w
            return W
        def window(W):
            st = [cv2.warpAffine(data[g][0], W[g], S, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP) for g in mem if W[g] is not None]
            sd = np.std(np.stack(st), axis=0)
            # the art window: the largest solid block of high variance (Otsu + opening removes the striped text
            # lines), then each edge refined to the strongest variance step within ±6 px
            v8 = np.clip(sd * 255 / max(sd.max(), 1), 0, 255).astype(np.uint8)
            _, bw = cv2.threshold(v8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
            n, lab, stats, _ = cv2.connectedComponentsWithStats(bw)
            if n < 2: return None, sd
            i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
            x, y, w, h = stats[i, :4]
            def edge(prof, c, rise):
                prof = np.convolve(prof, np.ones(3) / 3, "same"); d = np.diff(prof)
                lo, hi_ = max(c - 6, 1), min(c + 6, len(d) - 1)
                seg = d[lo:hi_] if rise else -d[lo:hi_]
                return lo + int(np.argmax(seg)) + (1 if rise else 0)
            cp = sd[y + h // 5:y + h - h // 5].mean(0); rp = sd[:, x + w // 5:x + w - w // 5].mean(1)
            win = [edge(cp, x, True), edge(rp, y, True), edge(cp, x + w - 1, False) + 1, edge(rp, y + h - 1, False) + 1]
            return [int(v) for v in win], sd
        full = np.ones((S[1], S[0]), np.uint8)
        W = align(full)
        win, sd = window(W)
        if win:
            mask = full.copy(); mask[win[1] + 4:win[3] - 4, win[0] + 4:win[2] - 4] = 0
            W = align(mask); win2, sd = window(W); win = win2 or win
        # second chance for scans that did not align to the reference: align to an already-aligned member and chain
        crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-5)
        aligned = [g for g in mem if W[g] is not None]
        for g in [g for g in mem if W[g] is None]:
            G = data[g][0]
            for r in sorted(aligned, key=lambda r: np.abs(data[r][0] - G).mean())[:6]:
                w = np.eye(2, 3, dtype=np.float32)
                try:
                    cc, w = cv2.findTransformECC(data[r][0], G, w, cv2.MOTION_AFFINE, crit, None, 5)
                except cv2.error:
                    continue
                if cc < 0.6 or abs(w[0, 0] - 1) > .08 or abs(w[1, 1] - 1) > .08:
                    continue
                A = np.vstack([W[r], [0, 0, 1]]); B = np.vstack([w, [0, 0, 1]])
                W[g] = (B @ A)[:2].astype(np.float32); break
        # a family window far from the frame's standard window is a detection failure: use the standard one
        era = "ep1" if "|ep1|" in fam else "classic"
        if "|Objective|" in fam and fam.endswith("port"):
            std_o = [43, 73, 306, 282] if era == "ep1" else [41, 73, 308, 282]
            if not win or any(abs(a - b) > 10 for a, b in zip(win, std_o)):
                win = std_o
        elif any(t in fam for t in ("|Admiral's Order|", "|Epic Event|", "|Jedi Test", "|Game Aid|")):
            win = None   # special layouts: reviewed by hand, not guessed
        elif fam.endswith("port") and win:
            std = [42, 140, 306] if era == "ep1" else [40, 138, 309]
            if "|combo" in fam or "|ref2|" in fam or "|enhanced|" in fam:
                pass   # own layouts: keep what was measured; the QA pass flags doubtful crops
            elif any(abs(a - b) > 10 for a, b in zip(win[:3], std)) or not 295 <= win[3] <= 335:
                bottom = 309 if any(t in fam for t in ("|Starship|", "|Vehicle|", "|Creature|", "|Podracer|")) else 322
                win = std + [bottom]; report_note = "standard window (detection failed)"
        Image.fromarray(np.clip(sd * 3, 0, 255).astype(np.uint8)).save(LIB / f"sd-{fam.replace('|', '_').replace('/', '-').replace(' ', '')}.png")
        if not win:
            report[fam] = (len(mem), "no window"); continue
        # window SHAPE (Bill 2026-10-14: Objective windows have cut top corners, Episode I windows rounded ones; keep
        # the full window and make the frame's corners transparent instead of cropping the picture): the convex hull of
        # the high-variance (= picture) area inside the window, shrunk 3 px like the rectangle inset
        v8 = np.clip(sd * 255 / max(sd.max(), 1), 0, 255).astype(np.uint8)
        _, bw = cv2.threshold(v8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        inner = np.zeros_like(bw); inner[win[1]:win[3], win[0]:win[2]] = bw[win[1]:win[3], win[0]:win[2]]
        inner = cv2.morphologyEx(inner, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
        pts = cv2.findNonZero(inner)
        shape = None
        if pts is not None:
            hull = cv2.convexHull(pts); hm = np.zeros_like(bw); cv2.fillConvexPoly(hm, hull, 255)
            hm = cv2.erode(hm, np.ones((7, 7), np.uint8))
            ys, xs = np.where(hm > 0)
            fill = (hm > 0).sum() / max((xs.max() - xs.min() + 1) * (ys.max() - ys.min() + 1), 1)
            pass
        if "|Objective|" in fam:
            # Light Objective windows have 45-degree cut top corners (16 px on the 350 px card)
            c = 16; x0, y0, x1, y1 = win; y1 -= 4   # the bottom keyline of the Objective window is a textured purple/silver band
            poly = np.array([[x0, y0 + c], [x0 + c, y0], [x1 - 1 - c, y0], [x1 - 1, y0 + c], [x1 - 1, y1 - 1], [x0, y1 - 1]], np.int32)
            hm = np.zeros_like(bw); cv2.fillPoly(hm, [poly], 255); hm = cv2.erode(hm, np.ones((7, 7), np.uint8))
            shape = hm.astype(np.float32) / 255; fill = 0.98
        if "|combo|ref2|" in fam:
            # Reflections II combo cards (two pictures, no lore box): window measured by hand on the scans, rounded top
            # corners (r 14 px on the 350 px card)
            win = [40, 76, 309, 255]; rr = 30
            hm = np.zeros_like(bw); cv2.rectangle(hm, (win[0], win[1] + rr), (win[2] - 1, win[3] - 1), 255, -1)
            cv2.rectangle(hm, (win[0] + rr, win[1]), (win[2] - 1 - rr, win[3] - 1), 255, -1)
            for cx in (win[0] + rr, win[2] - 1 - rr): cv2.circle(hm, (cx, win[1] + rr), rr, 255, -1)
            hm = cv2.erode(hm, np.ones((7, 7), np.uint8)); shape = hm.astype(np.float32) / 255; fill = 0.99
        report_shape = None if shape is None else round(float(fill), 3)
        ok = 0
        for g in mem:
            w = W[g]
            if w is None:
                man[g].update(status="unaligned", family=fam); continue
            G, sc, im = data[g]
            if shape is not None:
                cm = cv2.warpAffine(shape, w, im.size, flags=cv2.INTER_LINEAR)
                ys, xs = np.where(cm > 0.5)
                box = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
                box = trim_lines(np.array(im).astype(int), box)
                rgba = im.crop(box).convert("RGBA")
                rgba.putalpha(Image.fromarray((np.clip(cm[box[1]:box[3], box[0]:box[2]], 0, 1) * 255).astype(np.uint8)))
                rgba.save(ORIG / f"{g}.png")
                man[g].update(status="ok", family=fam, family_window=win, family_ref=ref, box=box, box_space="card350",
                              size=[box[2] - box[0], box[3] - box[1]], align_cc=round(float(CC.get(g, 0)), 3),
                              shaped=True, shape_fill=report_shape)
                ok += 1; continue
            man[g].pop("shaped", None)
            P = np.array([[win[0] + 3, win[1] + 3, 1], [win[2] - 3, win[3] - 3, 1]], np.float32) @ w.T / sc
            box = [int(round(P[0, 0])), int(round(P[0, 1])), int(round(P[1, 0])), int(round(P[1, 1]))]
            box = [max(box[0], 0), max(box[1], 0), min(box[2], im.size[0]), min(box[3], im.size[1])]
            arr = np.array(im).astype(int)
            box = trim_lines(arr, snap_inward(arr, box))
            im.crop(box).save(ORIG / f"{g}.png")
            man[g].update(status="ok", family=fam, family_window=win, family_ref=ref, box=box, box_space="card350",
                          size=[box[2] - box[0], box[3] - box[1]], align_cc=round(float(CC.get(g, 0)), 3))
            ok += 1
        report[fam] = (len(mem), f"window {win} ok {ok}" + (f" shaped (fill {report_shape})" if report_shape else ""))
        print(fam, report[fam], flush=True)
        MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1))
    (LIB / "families.json").write_text(json.dumps(report, indent=1))


def sheet(fam: str, out: str, n: int = 40):
    from PIL import ImageDraw
    import random
    man = json.loads(MAN.read_text())
    ks = [g for g, e in man.items() if e.get("family") == fam and e.get("status") == "ok"]
    random.seed(1); ks = random.sample(ks, min(n, len(ks)))
    W, H = 250, 175; o = Image.new("RGB", (8 * (W + 6), ((len(ks) + 7) // 8) * (H + 18)), "white"); d = ImageDraw.Draw(o)
    for i, g in enumerate(ks):
        im = Image.open(ORIG / f"{g}.png").convert("RGB"); im.thumbnail((W, H))
        x = (i % 8) * (W + 6); y = (i // 8) * (H + 18); o.paste(im, (x, y + 14)); d.text((x, y), f"{g} {man[g]['title']}"[:36], fill="black")
    o.save(out)


def upscale(shard: int = 0, nshards: int = 1, model: str = "/tmp/claude-0/models/x4plus128.onnx", lib: str | None = None):
    """RealESRGAN x4plus on every measured master (resumable; shard k of n so several machines can share the work)."""
    import onnxruntime as ort, zlib
    lib = Path(lib) if lib else LIB
    man = json.loads((lib / "manifest-all.json").read_text()); (lib / "x4").mkdir(exist_ok=True)
    so = ort.SessionOptions(); sess = ort.InferenceSession(model, so)
    todo = [g for g, e in man.items() if e.get("status") == "ok" and zlib.crc32(g.encode()) % nshards == shard
            and not (lib / "x4" / f"{g}.webp").exists() and (lib / "orig" / f"{g}.png").exists()]
    print(len(todo), "to do", flush=True)
    for i, g in enumerate(todo):
        a = np.array(Image.open(lib / "orig" / f"{g}.png").convert("RGB")).astype(np.float32) / 255
        T, pad = 128, 12; step = T - 2 * pad; H, W = a.shape[:2]; outp = np.zeros((H * 4, W * 4, 3), np.float32)
        for y in range(0, H, step):
            for x in range(0, W, step):
                y0 = max(min(y - pad, H - T), 0); x0 = max(min(x - pad, W - T), 0)
                tile = np.zeros((T, T, 3), np.float32); sub = a[y0:y0 + T, x0:x0 + T]; tile[:sub.shape[0], :sub.shape[1]] = sub
                r = sess.run(None, {"image": tile.transpose(2, 0, 1)[None]})[0][0].transpose(1, 2, 0)
                ye, xe = min(y + step, H), min(x + step, W)
                outp[y * 4:ye * 4, x * 4:xe * 4] = r[(y - y0) * 4:(ye - y0) * 4, (x - x0) * 4:(xe - x0) * 4]
        Image.fromarray((np.clip(outp, 0, 1) * 255).round().astype(np.uint8)).save(lib / "x4" / f"{g}.webp", quality=92, method=6)
        print(i + 1, g, flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch": fetch()
    elif cmd == "measure": measure(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "sheet": sheet(sys.argv[2], sys.argv[3])
    elif cmd == "upscale": upscale(int(sys.argv[2]), int(sys.argv[3]), *(sys.argv[4:6]))
