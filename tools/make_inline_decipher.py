"""Rev 84 (inline icons): Decipher's own colours for the inline game-text icons it printed differently from the PC's
Game Aid icons we draw (render.game_text_html picks the "-decipher" file on Decipher's own printings, card
decipher_print). Measured on the wiki's 1497 px hires faces (median colour inside the icon):

  Independent (Wooof's [Independent], [Independent Starship]): a dark slate square, the wheel barely showing, light grey
  border. Printed inside median (60-69, 68-77, 70-75), 10th / 90th percentile (34-40, 40-47, 42-47) / (92-109,
  103-115, 103-113) on Gela Yeens 7_178, Outer Rim Scout 7_195, Thul Fain 6_125, My Favorite Decoration 7_296 (back);
  ours (the PC's icon) is bright blue (107, 134, 154). The low-resolution web faces (Local Defense, Black Sun
  Fleet) show it teal: they are Decipher's web images, not the print.
  Selective creature (Ithorian 6_20): the green is darker and duller on the print: (88, 135, 84) against (76, 193, 124).

Run: python3 tools/make_inline_decipher.py -> assets/icons/inline-independent-decipher.png,
     assets/icons/selective-creature-decipher.png
"""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IC = ROOT / "assets/icons"


def independent():
    im = Image.open(IC / "inline-independent.png").convert("RGBA")
    a = np.array(im).astype(float); n = a.shape[0]
    rgb, al = a[:, :, :3], a[:, :, 3]
    y, x = np.mgrid[0:n, 0:n]
    edge = np.minimum(np.minimum(x, y), np.minimum(n - 1 - x, n - 1 - y))
    border = edge < 0.085 * n                       # the icon's light frame
    lum = rgb.mean(2)
    inner = ~border
    lo, hi = np.percentile(lum[inner], 10), np.percentile(lum[inner], 90)
    t = np.clip((lum - lo) / max(1.0, hi - lo), 0, 1)[..., None]
    dark, light = np.array([40, 47, 48]), np.array([88, 97, 97])   # printed 10th / 90th percentile (the print's dot
    # screen spreads them; the wheel itself reads fainter than that)
    out = dark + t * (light - dark)
    out[border] = (np.clip((lum[border] - lum[border].min()) / max(1.0, np.ptp(lum[border])), 0, 1)[..., None]
                   * (np.array([178, 180, 176]) - np.array([110, 112, 110])) + np.array([110, 112, 110]))
    res = np.dstack([out, al]).clip(0, 255).astype(np.uint8)
    Image.fromarray(res, "RGBA").save(IC / "inline-independent-decipher.png")


def selective():
    im = Image.open(IC / "pc-gameaid-x4/selective-creature.png").convert("RGBA")
    a = np.array(im).astype(float)
    k = np.array([88 / 76, 135 / 193, 84 / 124])    # printed / ours, median of the green
    rgb = a[:, :, :3]
    green = (rgb[:, :, 1] > rgb[:, :, 0] + 15) & (rgb[:, :, 1] > rgb[:, :, 2] + 15)   # the field only, not the frame
    rgb[green] = (rgb[green] * k).clip(0, 255)
    Image.fromarray(a.astype(np.uint8), "RGBA").save(IC / "selective-creature-decipher.png")


if __name__ == "__main__":
    independent(); selective()
    print("wrote inline-independent-decipher.png, selective-creature-decipher.png")
