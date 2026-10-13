"""TEST (Bill 2026-10-13): Defensive Shield frames with the Remaster slip's colour transition — the Effect's colour
fades into the shield's cyan from just above the banner to the middle of the text box, instead of the hybrid
frames' hard cut at the banner. Writes assets/frames/{ds,ls}-shield-fade.png; the live hybrid frames are untouched.

Fade curve measured on VirtualCards6.pdf slips 24 (LS Weapons Display) and 34 (DS Firepower): coloured margin
pixels, red channel against the Effect red, mapped to the card at the slip's scale (slip width 750 px = card 1343 px,
slip bottom = card bottom 2075): ≈ 6 % cyan at card y 1445, 55 % at 1649, fully cyan by ≈ 1790.

    python3 make_shield_fade.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
F = ROOT / "assets/frames"

# (card y, fraction of shield colour) — from the slips' margin profile
CURVE = [(1380, 0.0), (1445, 0.06), (1520, 0.20), (1585, 0.36), (1649, 0.55), (1700, 0.74), (1745, 0.90), (1790, 1.0)]


def weights(H: int, off_y: int) -> np.ndarray:
    ys = np.arange(H) + off_y
    xs, ws = zip(*CURVE)
    return np.interp(ys, xs, ws)


def canvas(png: str, off) -> np.ndarray:
    c = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0))
    c.alpha_composite(Image.open(F / png).convert("RGBA"), off)
    return np.array(c).astype(float)


def build(effect: str, effect_off, hybrid: str, hybrid_off, banner, out: str):
    e = canvas(effect, effect_off)
    h = canvas(hybrid, hybrid_off)
    w = weights(2220, 0)[:, None, None]
    m = e * (1 - w) + h * w
    # the banner keeps the shield's own banner colour (cyan on Dark, silver on Light), as the slips print it
    bx, by, bw, bh = banner
    pad = 22
    m[by - pad:by + bh + pad, bx - pad:bx + bw + pad] = h[by - pad:by + bh + pad, bx - pad:bx + bw + pad]
    # text box (inside the bevel) from the hybrid as well: the slip fades only the frame margins
    img = Image.fromarray(np.clip(m, 0, 255).astype(np.uint8), "RGBA")
    img.save(F / out, optimize=True)
    print(out)


def main():
    build("ds-effect.png", (141, 147), "ds-shield-hybrid.png", (141, 147), (262, 1506, 1110, 61), "ds-shield-fade.png")
    build("ls-effect.png", (146, 141), "ls-shield-hybrid.png", (146, 141), (268, 1505, 1109, 61), "ls-shield-fade.png")


if __name__ == "__main__":
    main()
