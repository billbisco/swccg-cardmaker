"""Rev 81 (frames): the wide Dark capital starship frames (Executor, Flagship Executor; Finalizer (AI)) carried
Bardez's "Type Icon" layer as a square crop of the starship icon art over the title bar's left end. Decipher printed
the round starship type disc in a ring, as on the portrait starships: measured on Executor (4_167) and Flagship Executor
(9_157) printed faces (745 x 532, registered at 2x + 70 master px): picture centre (305, 280), picture radius ~65,
blue ring to ~88. This tool replaces the square: the bar under it is inpainted from its surroundings, then the portrait
DS starship frame's disc (picture + ring + bevel, ds-starship-starfighter.png, centre (263, 263)) is set in at the
printed centre with a feathered edge. Runs on assets/frames/ds-starship-wide.png and ds-starship-wide-nolore.png
(idempotent: keeps the untouched originals as *.orig.png beside them under out/).
Usage: python3 tools/fix_starship_wide_disc.py"""
from pathlib import Path
import shutil
import numpy as np
from PIL import Image
import cv2

ROOT = Path(__file__).resolve().parents[1]
FR = ROOT / "assets/frames"
SQ = (212, 185, 443, 400)          # the square type-icon layer (master px, inclusive margins)


def portrait():
    P = Image.open(FR / "ds-starship-starfighter.png").convert("RGBA")
    c = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0)); c.alpha_composite(P, (139, 148))
    return np.array(c).astype(np.float32)


def fix(name):
    src = ROOT / "out" / f"{name}.orig.png"
    src.parent.mkdir(exist_ok=True)
    if not src.exists():
        shutil.copy(FR / f"{name}.png", src)
    F = np.array(Image.open(src).convert("RGBA"))
    x0, y0, x1, y1 = SQ
    mask = np.zeros(F.shape[:2], np.uint8); mask[y0:y1, x0:x1] = 1
    rgb = cv2.inpaint(np.ascontiguousarray(F[..., :3]), mask, 18, cv2.INPAINT_NS)
    G = F.copy(); G[..., :3] = rgb; G[y0:y1, x0:x1, 3] = 255
    # a light smoothing of the inpainted area (no streaks), keeping the frame round it
    sm = cv2.GaussianBlur(G[..., :3].astype(np.float32), (0, 0), 6)
    G[y0:y1, x0:x1, :3] = sm[y0:y1, x0:x1].round().astype(np.uint8)
    # the whole corner (disc in its ring, the bar's lower bevel bending into the V under the disc) from the portrait
    # frame, aligned on the V's tip (portrait (263, 397), wide (317, 413)): the disc lands at (317, 279), 12 px from
    # the printed estimate (the faces are 745 px upscales)
    P = portrait()
    sx, sy = 263 - 317, 397 - 413
    cx0 = x0 + 10                                              # the portrait's own left bevel stays out
    patch = P[y0 + sy:y1 + sy, cx0 + sx:x1 + sx, :3]
    G = G.astype(np.float32)
    w = np.ones(patch.shape[:2], np.float32)
    ramp = np.linspace(0, 1, 12, dtype=np.float32)
    w[:, :12] *= ramp[None, :]; w[:, -12:] *= ramp[::-1][None, :]
    w[:12, :] *= ramp[:, None]; w[-12:, :] *= ramp[::-1][:, None]
    G[y0:y1, cx0:x1, :3] = patch * w[..., None] + G[y0:y1, cx0:x1, :3] * (1 - w[..., None])
    Image.fromarray(G.round().astype(np.uint8), "RGBA").save(FR / f"{name}.png", optimize=True)
    print("wrote", FR / f"{name}.png")


if __name__ == "__main__":
    for n in ("ds-starship-wide", "ds-starship-wide-nolore"):
        fix(n)
