"""Per-card checks on the art library crops, plus full contact sheets.

    python3 art_qa.py check            # writes qa fields into library/manifest-all.json, prints a summary
    python3 art_qa.py sheets OUTDIR    # every ok crop, 60 per sheet, flagged cards outlined in red

Checks (each crop, at scan resolution):
  edge_line   a uniform line along an edge that differs from the picture just inside it (frame keyline left in)
  align       ECC alignment score to the family reference below 0.80 (frame did not line up well)
  aspect      crop aspect more than 4 % off its family's median (window slid or clipped)
  size        crop smaller than 85 % of its family's median width or height
"""
from __future__ import annotations
import json, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "library"; MAN = LIB / "manifest-all.json"


def edge_lines(a: np.ndarray) -> list[str]:
    out = []
    for name in ("top", "bottom", "left", "right"):
        for k in range(2):
            line, inner = {"top": (a[k], a[k + 3]), "bottom": (a[-1 - k], a[-4 - k]),
                           "left": (a[:, k], a[:, k + 3]), "right": (a[:, -1 - k], a[:, -4 - k])}[name]
            med = np.median(line, 0)
            uniform = np.median(np.abs(line - med).sum(1)) < 30
            differs = np.abs(med - np.median(inner, 0)).sum() > 45
            if uniform and differs:
                out.append(name); break
    return out


def check():
    man = json.loads(MAN.read_text())
    fam_dims = defaultdict(list)
    for g, e in man.items():
        if e.get("status") == "ok":
            fam_dims[e["family"]].append(e["size"])
    med = {f: np.median(np.array(v), axis=0) for f, v in fam_dims.items()}
    counts = defaultdict(int)
    for g, e in man.items():
        if e.get("status") != "ok":
            continue
        a = np.array(Image.open(LIB / "orig" / f"{g}.png").convert("RGB")).astype(int)
        flags = []
        el = edge_lines(a)
        if el: flags.append("edge_line:" + ",".join(el))
        if not e.get("system") and e.get("align_cc") is not None and e["align_cc"] < 0.80: flags.append(f"align:{e['align_cc']}")
        mw, mh = med[e["family"]]; w, h = e["size"]
        if abs((w / h) / (mw / mh) - 1) > 0.04: flags.append(f"aspect:{w}x{h}")
        if w < 0.85 * mw or h < 0.85 * mh: flags.append(f"size:{w}x{h}")
        e["qa"] = flags
        for f in flags: counts[f.split(":")[0]] += 1
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1))
    n_ok = sum(1 for e in man.values() if e.get("status") == "ok")
    n_flag = sum(1 for e in man.values() if e.get("status") == "ok" and e.get("qa"))
    print(f"{n_ok} ok crops, {n_flag} flagged:", dict(counts))


def sheets(outdir: str, per: int = 60):
    man = json.loads(MAN.read_text()); out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    try: F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except Exception: F = None
    def key(g):
        s, n = g.split("_"); return (int("".join(c for c in s if c.isdigit()) or 0), int("".join(c for c in n if c.isdigit()) or 0))
    gs = sorted([g for g, e in man.items() if e.get("status") == "ok"], key=key)
    W, H, cols = 200, 140, 10
    for i in range(0, len(gs), per):
        part = gs[i:i + per]; rows = (len(part) + cols - 1) // cols
        S = Image.new("RGB", (cols * (W + 6), rows * (H + 30)), "white"); d = ImageDraw.Draw(S)
        for j, g in enumerate(part):
            e = man[g]; src = Image.open(LIB / "orig" / f"{g}.png").convert("RGBA")
            im = Image.new("RGB", src.size, (255, 0, 255)); im.paste(src, (0, 0), src); im.thumbnail((W, H))   # magenta = transparent
            x = (j % cols) * (W + 6); y = (j // cols) * (H + 30)
            S.paste(im, (x, y + 28))
            if e.get("qa"): d.rectangle((x - 2, y + 26, x + im.width + 1, y + 29 + im.height), outline="red", width=3)
            d.text((x, y), f"{g} {(e['title'] or '')[:22]}", fill="black", font=F)
            d.text((x, y + 13), ", ".join(e.get("qa") or [])[:34], fill="red", font=F)
        S.save(out / f"sheet-{i // per + 1:02d}.png")
    print((len(gs) + per - 1) // per, "sheets in", out)


if __name__ == "__main__":
    {"check": lambda: check(), "sheets": lambda: sheets(sys.argv[2])}[sys.argv[1]]()
