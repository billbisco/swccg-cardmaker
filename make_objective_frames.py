"""Build assets/frames/objective.png (Dark Side) and objective-ls.png (Light Side) from Bardez's templates, recoloured
to the purple of the printed / PC Objective cards (Bill, 2026-10-12: "the purple tone has to match … Grab a Decipher
DS objective if you must and recreate").

Measured on the PC modern cards (src/vs4/modern/40-VB2-D-*.gif, 11-VB2-L-*.gif, median HSV of the frame's purple):
  DS: two-tone — above the art window's bottom edge hue .70 / sat .70 / val .45, below it hue .76 / sat .64 / val .44
      (the split is exactly at the art window's lower bevel; the side borders switch too).
  LS: one tone  — hue .733 / sat .68 / val .45, over the silver-frost speckles of the Endor-era LS frame
      (Bardez's "LS - Epic Objective" frame is that frame in Death Star II blue, hue .627 / sat .55 / val .50).

    python3 make_objective_frames.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image
from gimpformats.gimpXcfDocument import GimpDocument

ROOT = Path(__file__).resolve().parent


def recolour(img: Image.Image, dh: float, ks: float, kv: float, rows=None, flatten: tuple | None = None) -> Image.Image:
    """Shift hue by dh and scale sat/val of the coloured pixels (sat > .2); silver, white and black stay.
    flatten=(h0, k) first pulls every hue towards h0 (h0 + (h - h0) * k) so a frame painted in several blues becomes
    one purple."""
    rgba = np.array(img.convert("RGBA"))
    hsv = np.array(Image.fromarray(rgba[:, :, :3]).convert("HSV")).astype(float)
    sel = hsv[:, :, 1] > 0.2 * 255
    if rows is not None:
        rmask = np.zeros_like(sel); rmask[rows] = True; sel &= rmask
    h = hsv[:, :, 0]
    if flatten:
        h0 = flatten[0] * 255
        h = h0 + (h - h0) * flatten[1]
    h = (h + dh * 255) % 255
    s = np.clip(hsv[:, :, 1] * ks, 0, 255)
    v = np.clip(hsv[:, :, 2] * kv, 0, 255)
    hsv[sel, 0], hsv[sel, 1], hsv[sel, 2] = h[sel], s[sel], v[sel]
    rgb = np.array(Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB"))
    rgba[:, :, :3] = rgb
    return Image.fromarray(rgba)


def main():
    # Dark Side: Bardez "DS - Objective" Template layer (1497×2073 at 67,73): hue .725 / sat .47 / val .34
    ds = GimpDocument(str(ROOT / "bardez/DS - Objective.xcf")).raw_layers[4].image
    # Bill (2026-10-13): one purple over the whole frame — the red-purple of the text-box half / the slip; the PC
    # card's bluer upper half is not wanted
    ds2 = recolour(ds, 0.76 - 0.725, 0.64 / 0.47, 0.44 / 0.34)
    ds2.save(ROOT / "assets/frames/objective.png", optimize=True)

    # Light Side: Bardez "LS - Epic Objective" frame layer (6) + its Objective icon layer (8), both at 67,73
    doc = GimpDocument(str(ROOT / "bardez/LS - Epic Objective.xcf"))
    frame = doc.raw_layers[6].image.convert("RGBA")
    icon = doc.raw_layers[8].image.convert("RGBA")
    canvas = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0))
    canvas.alpha_composite(frame, (67, 72))
    canvas.alpha_composite(icon, (67, 73))
    # one purple between the PC card (.735) and the slip (.763): hue .75, with Bardez's blue-to-blue variation flattened
    ls = recolour(canvas, 0.75 - 0.627, 0.72 / 0.55, 0.45 / 0.50, flatten=(0.627, 0.3))
    ls.save(ROOT / "assets/frames/objective-ls.png", optimize=True)
    print("ok")


if __name__ == "__main__":
    main()
