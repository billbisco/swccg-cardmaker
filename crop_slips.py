"""Crop the slips (heading + slip, nothing else) from a Remaster sheet rendered at 300 DPI (src/slips/vsN/p300-*.png).

    python3 crop_slips.py N

Writes src/slips/vsN/NN-Title.png. The slip box is detected as a dark component 700–800 px wide; the crop is then
cleaned: columns outside the slip's own span (a neighbour's sliver) and every row above the heading that belongs to
the slip above (its black caption bar) are whited out. Titles come from gempdata/original-vs-stubs.json."""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = Path(__file__).resolve().parent
PAD_TOP, PAD_SIDE, MIN_H = 92, 6, 362


def slip_boxes(png: Path):
    a = np.array(Image.open(png).convert("RGB"))
    dark = a.max(axis=2) < 60
    lab, _ = ndimage.label(ndimage.binary_closing(dark, iterations=3))
    bb = []
    for o in ndimage.find_objects(lab):
        h = o[0].stop - o[0].start; w = o[1].stop - o[1].start
        if 700 < w < 800 and 300 < h < 420:
            bb.append((o[1].start, o[0].start, w, h))
    bb.sort(key=lambda b: (round(b[1] / 100), b[0]))
    return bb


def clean(crop: Image.Image, w: int) -> Image.Image:
    a = np.array(crop.convert("L"))
    H, W = a.shape
    body = a[PAD_TOP + 10:PAD_TOP + 200]                     # rows well inside the slip
    # the slip's own column span: the widest run of non-white columns (a neighbour is separated by page white)
    nonwhite = body.mean(axis=0) < 235
    runs, start = [], None
    for x, v in enumerate(list(nonwhite) + [False]):
        if v and start is None:
            start = x
        elif not v and start is not None:
            runs.append((start, x)); start = None
    x0, x1 = max(runs, key=lambda r: r[1] - r[0]) if runs else (PAD_SIDE, PAD_SIDE + w)
    d = ImageDraw.Draw(crop)
    d.rectangle((0, 0, x0 - 1, H), fill="white"); d.rectangle((x1, 0, W, H), fill="white")
    # rows above the heading: the previous slip's caption bar is a mostly-dark row; whiten from the top down to the
    # last such row (the heading itself is sparse black text on white)
    top = a[:PAD_TOP, x0:x1]
    dark_rows = [y for y in range(top.shape[0]) if (top[y] < 100).mean() > 0.35]
    if dark_rows:
        d.rectangle((0, 0, W, max(dark_rows) + 6), fill="white")
    return crop


def main():
    vs = int(sys.argv[1])
    stubs = json.load(open(ROOT / "gempdata/original-vs-stubs.json", encoding="utf-8"))
    names = {int(v["image"][5:7]): v["image"][8:-4] for v in stubs.values() if v["set"] == f"Virtual Set {vs} (Original)"}
    n = 0
    for png in sorted((ROOT / f"src/slips/vs{vs}").glob("p300-*.png")):
        im = Image.open(png).convert("RGB")
        for x, y, w, h in slip_boxes(png):
            n += 1
            crop = im.crop((x - PAD_SIDE, y - PAD_TOP, x + w + PAD_SIDE + 1, y + max(MIN_H, h + 4)))
            clean(crop, w).save(ROOT / f"src/slips/vs{vs}/{n:02d}-{names[n]}.png", optimize=True)
    print(vs, n, "slips")


if __name__ == "__main__":
    main()
