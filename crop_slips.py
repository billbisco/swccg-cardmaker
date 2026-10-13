"""Crop the slips (heading + slip, nothing else) from a Remaster sheet rendered at 300 DPI (src/slips/vsN/p300-*.png).

    python3 crop_slips.py N

Writes src/slips/vsN/NN-Title.png. The slip box is detected as a dark component 700–800 px wide; the crop is then
cleaned: columns outside the slip's own span (a neighbour's sliver) and every row above the heading that belongs to
the slip above (its black caption bar) are whited out. Titles come from gempdata/original-vs-stubs.json."""
from __future__ import annotations
import json, re, sys
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
        if 700 < w < 800 and 300 < h < 460:      # Objectives print taller slips (432 px)
            bb.append((o[1].start, o[0].start, w, h))
    bb.sort(key=lambda b: (round(b[1] / 100), b[0]))
    return bb


def clean(crop: Image.Image, w: int) -> Image.Image:
    """Keep the heading and the slip (its own black outline included); white out the columns outside the detected
    slip box (a neighbour's sliver) and the rows above the heading that belong to the slip above (its caption bar)."""
    a = np.array(crop.convert("L"))
    H, W = a.shape
    x0, x1 = PAD_SIDE - 1, PAD_SIDE + w + 2          # the box edges = the slip's black outline
    d = ImageDraw.Draw(crop)
    d.rectangle((0, 0, x0 - 1, H), fill="white"); d.rectangle((x1, 0, W, H), fill="white")
    top = a[:PAD_TOP, x0:x1]
    # a caption bar (of the slip above) is a solid dark run; heading text never runs dark for 200 px without a gap
    def longest_run(row):
        d = np.concatenate(([0], (row < 100).astype(np.int8), [0]))
        edges = np.flatnonzero(np.diff(d))
        return int((edges[1::2] - edges[::2]).max()) if len(edges) else 0
    dark_rows = [y for y in range(top.shape[0]) if longest_run(top[y]) > 200]
    if dark_rows:
        d.rectangle((0, 0, W, max(dark_rows) + 6), fill="white")
    # the heading is the last run of inked rows above the slip; anything above it (a glyph tail of the slip above's
    # number — VS6 #20/#36) is whited out
    a = np.array(crop.convert("L"))[:PAD_TOP, x0:x1]
    inked = [(a[y] < 140).any() for y in range(a.shape[0])]
    runs, start = [], None
    for y, v in enumerate(inked + [False]):
        if v and start is None: start = y
        if not v and start is not None: runs.append((start, y - 1)); start = None
    runs = [r for r in runs if r[1] - r[0] >= 8]
    if len(runs) >= 2:
        d.rectangle((0, 0, W, runs[-1][0] - 3), fill="white")
    return crop


def main():
    vs = int(sys.argv[1])
    from sheet import slip_boxes as keyed_boxes
    stubs = json.load(open(ROOT / "gempdata/original-vs-stubs.json", encoding="utf-8"))
    names = {int(re.match(r"VS\d+O-(\d+)-", v["image"]).group(1)): v["image"].split("-", 2)[2][:-4] for v in stubs.values() if v["set"] == f"Virtual Set {vs} (Original)"}
    pages = {}
    n = 0
    for key, (pg, x, y, w, h) in sorted(keyed_boxes(vs).items()):
        im = pages.setdefault(pg, Image.open(ROOT / f"src/slips/vs{vs}/p300-{pg}.png").convert("RGB"))
        crop = im.crop((x - PAD_SIDE, y - PAD_TOP, x + w + PAD_SIDE + 1, y + max(MIN_H if h > 300 else h + 4, h + 4)))
        crop = clean(crop, w)
        num = int(key[:2])
        if h <= 300 and crop.height > PAD_TOP + h + 4:   # short site slips: no MIN_H padding below
            crop = crop.crop((0, 0, crop.width, PAD_TOP + h + 6))
        crop.save(ROOT / f"src/slips/vs{vs}/{num:02d}{key[2:]}-{names[num]}.png", optimize=True)
        n += 1
    print(vs, n, "slips")


if __name__ == "__main__":
    main()
