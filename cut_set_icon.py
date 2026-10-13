"""Cut an expansion-set icon out of a 745 px Decipher scan (STANDARD: the icon in the frame's ring right of the lore
box, found from its dark ring (~26 px across at 745 px), Lanczos-upscaled to 232 px with a round mask at its own dark edge).

    python3 cut_set_icon.py src/vs6/01-CC-L-accessdenied.gif assets/icons/set-cloudcity-grainy.png
"""
from __future__ import annotations
import sys
import numpy as np
from PIL import Image, ImageDraw


def find_ring(a: np.ndarray, x0=640, x1=720, y0=150, y1=235, radii=range(10, 17)):
    """Best (cx, cy, r) of a dark annulus in the search window: score = mean darkness on the ring minus inside."""
    g = a.mean(axis=2)
    dark = (255 - g) / 255
    best = None
    ys, xs = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    for r in radii:
        for cy in range(y0 + r, y1 - r, 2):
            for cx in range(x0 + r, min(x1, a.shape[1]) - r, 2):
                d2 = (xs[cy - r - 3:cy + r + 4, cx - r - 3:cx + r + 4] - cx) ** 2 + (ys[cy - r - 3:cy + r + 4, cx - r - 3:cx + r + 4] - cy) ** 2
                win = dark[cy - r - 3:cy + r + 4, cx - r - 3:cx + r + 4]
                ring = win[(d2 >= (r - 1.5) ** 2) & (d2 <= (r + 1.5) ** 2)].mean()
                inner = win[d2 <= (r - 4) ** 2].mean()
                outer = win[(d2 >= (r + 3) ** 2) & (d2 <= (r + 6) ** 2)].mean()
                score = ring - 0.5 * inner - 0.5 * outer
                if best is None or score > best[0]:
                    best = (score, cx, cy, r)
    return best


def main():
    src, dst = sys.argv[1], sys.argv[2]
    im = Image.open(src).convert("RGB")
    if im.width != 745:
        im = im.resize((745, round(im.height * 745 / im.width)), Image.LANCZOS)
    a = np.array(im).astype(float)
    score, cx, cy, r = find_ring(a)
    print("ring", cx, cy, r, round(score, 3))
    rr = r - 1                                   # inside the dark ring edge
    crop = im.crop((cx - rr, cy - rr, cx + rr + 1, cy + rr + 1)).resize((232, 232), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (232, 232), 0); ImageDraw.Draw(mask).ellipse((0, 0, 231, 231), fill=255)
    crop.putalpha(mask); crop.save(dst)


if __name__ == "__main__":
    main()
