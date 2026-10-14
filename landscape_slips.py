"""Turn the portrait site slips of a Remaster sheet (full location overlays, VS13+) into landscape slips, the way a site
card is read (Bill 2026-10-14: "make the Vslips for sites horizontal as normal for a site"). The heading stays on
top, the slip body is turned 90° clockwise (Light half at the bottom), the caption strip (title + number) runs along
the bottom. The portrait crop is kept in src/slips/vsN/portrait/.

    python3 landscape_slips.py 13 03 04 09 …
"""
from __future__ import annotations
import glob, shutil, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
HEAD = 92


def caption_top(a: np.ndarray) -> int:
    """The caption strip: the last run of rows that are mostly black at the bottom of the box."""
    dark = (a.max(axis=2) < 50).mean(axis=1)
    y = a.shape[0] - 1
    while y > a.shape[0] - 80 and dark[y] < 0.5:   # white padding below the slip
        y -= 1
    while y > a.shape[0] - 120 and dark[y] > 0.45:
        y -= 1
    return y + 1


def number_left(a: np.ndarray) -> int:
    """Left edge of the slip number: the last cluster of bright (text) columns, after a gap of ≥24 empty columns."""
    lit = (a.max(axis=2) > 140).sum(axis=0) > 1
    x = len(lit) - 16                                   # skip the slip's right border
    while x > 0 and not lit[x]:
        x -= 1
    gap = 0
    while x > 0:
        x -= 1
        gap = gap + 1 if not lit[x] else 0
        if gap >= 14:
            return x + gap // 2
    return int(len(lit) * 0.85)


def main():
    vs = int(sys.argv[1])
    for n in sys.argv[2:]:
        src = Path(glob.glob(str(ROOT / f"src/slips/vs{vs}/{n}-*.png"))[0])
        port = src.parent / "portrait" / src.name
        if not port.exists():
            port.parent.mkdir(exist_ok=True); shutil.copy(src, port)
        im = Image.open(port).convert("RGB")
        a = np.array(im)
        head = im.crop((0, 0, im.width, HEAD))
        cy = caption_top(a[HEAD:]) + HEAD
        body = im.crop((0, HEAD, im.width, cy)).rotate(-90, expand=True)
        cap = im.crop((0, cy, im.width, im.height))
        W = body.width
        out = Image.new("RGB", (W, HEAD + body.height + cap.height), "white")
        out.paste(head, ((W - head.width) // 2, 0))
        out.paste(body, (0, HEAD))
        ca = np.array(cap).astype(int)
        mid = np.median(ca[:, 40:ca.shape[1] - 40].max(axis=2), axis=1)
        yb = max(y for y in range(ca.shape[0]) if mid[y] < 60 or y < ca.shape[0] // 2) + 1   # black strip, page white below
        cap = cap.crop((12, 0, cap.width - 12, yb))
        k = number_left(np.array(cap))                     # whole caption | the slip number (moved to the right edge)
        strip = Image.new("RGB", (W, yb), (14, 14, 14))
        strip.paste(cap.crop((0, 0, k, yb)), (12, 0))
        strip.paste(cap.crop((k, 0, cap.width, yb)), (W - 12 - (cap.width - k), 0))
        sa = np.array(strip); r = 12                       # the slip's rounded bottom corners
        for y in range(r):
            dx = r - int(round((r * r - (y + 1) ** 2) ** 0.5)) if y + 1 < r else r
            sa[yb - r + y, :dx] = 255; sa[yb - r + y, W - dx:] = 255
        strip = Image.fromarray(sa)
        out = out.crop((0, 0, W, HEAD + body.height + yb))
        out.paste(strip, (0, HEAD + body.height))
        oa = np.array(out); y0 = HEAD + body.height
        for y in range(y0 - 14, min(y0 + 8, oa.shape[0])):   # stray page-white seams at the junction
            if (oa[y].min(axis=1) > 150).mean() > 0.3:
                oa[y] = (14, 14, 14)
        out = Image.fromarray(oa)
        out.save(src)
        print(src.name, out.size)


if __name__ == "__main__":
    main()
