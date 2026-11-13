"""Rev 80: fit assets/frames/decipher-tone.npz, the colours Decipher printed the Effect / Interrupt frames in.

Our four Effect / Interrupt frames carry the PC's colours (within 5 levels of the PC's own Virtual cards). Decipher's
printed faces are a deeper crimson on the Dark frames, show silver (not cyan) chips on the Light red margins, and print
the type discs redder (Interrupt) / yellower (Effect). This script pairs printed scans with our renders of the same cards
(both 745x1039 Holotable size; the scans are registered to the render by their card body) and writes:

  light, dark            3D colour offset tables (17^3 nodes, step 16), fitted on frame pixels only (title, destiny,
                         lore / art / banner / text boxes, sphere + copyright column and the type disc left out, mask
                         eroded 3 px, compared after a 3x3 box blur: the scans are 2x upscales of ~350 px faces);
                         nodes <= 32 are pinned to 0 so blacks stay black
  disc_effect,           per-channel curves out = g * 255 * (x/255)^gamma for the type discs, fitted on quantiles 40-99
  disc_interrupt         (the scans' thin dark stripes are lifted by blur, so the low end is not matched)

render.decipher_toned() applies them to a frame when the card is a Decipher printing (card "decipher_print").

Usage: python3 make_decipher_tone.py SCANS RENDERS LIGHT_IDS DARK_IDS [OUT]
  SCANS/<gempId>.png    printed scans: the PC's .png 2x faces (res.starwarsccg.org .../large/<name>.png) or the 350 px
                        .gif faces; not the PC's errata re-renders (they carry the PC's colours)
  RENDERS/<gempId>.png  our holotable renders of the same cards (art may be off: the art window is not used)
  LIGHT_IDS, DARK_IDS   comma-separated GEMP ids of Decipher Effects / Interrupts (Rev 80 used every other card of 50
                        Light and 48 Dark printed faces, sets 1-14; the other half validated: Dark frame MAD 18.0 -> 9.4,
                        Light 19.2 -> 17.7, disc means within 2-4 levels)
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import render  # noqa: E402

TPL = {("Light", "Effect"): "ls-effect", ("Light", "Interrupt"): "ls-interrupt",
       ("Dark", "Effect"): "ds-effect", ("Dark", "Interrupt"): "ds-interrupt"}
N = 17


def body(im):
    """Card body box (x0, y0, x1, y1) of a 745-px face: median first / last bright pixel over the middle rows / columns."""
    m = np.asarray(im.convert("RGB")).astype(int).max(2) > 60
    def edges(mm):
        L, R = [], []
        for row in mm[int(len(mm) * 0.2):int(len(mm) * 0.8)]:
            w = np.where(row[2:-2])[0]
            if len(w):
                L.append(w[0] + 2); R.append(w[-1] + 3)
        return int(np.median(L)), int(np.median(R))
    x0, x1 = edges(m); y0, y1 = edges(m.T)
    return x0, y0, x1, y1


def registered(scan: Path, ref: Path):
    s = Image.open(scan).convert("RGB"); r = Image.open(ref).convert("RGB")
    bs, br = body(s), body(r)
    sx = (bs[2] - bs[0]) / (br[2] - br[0]); sy = (bs[3] - bs[1]) / (br[3] - br[1])
    return s.transform(r.size, Image.AFFINE, (sx, 0, bs[0] - br[0] * sx, 0, sy, bs[1] - br[1] * sy), Image.BICUBIC), r


def disc_745(tn: str):
    t = render.TEMPLATES[tn]; _, fx, fy = t["frame"]; cx, cy, r = t["decipher_tone"][2]
    return (cx + fx) / 2 - 35, (cy + fy) / 2 - 35, r / 2


def frame_mask(tn: str) -> np.ndarray:
    t = render.TEMPLATES[tn]; fr, fx, fy = t["frame"]
    a = np.asarray(Image.open(render.ASSETS / fr).convert("RGBA"))[..., 3]
    M = np.zeros((2220, 1632), bool); M[fy:fy + a.shape[0], fx:fx + a.shape[1]] = a > 250
    H = np.asarray(Image.fromarray(M).resize((816, 1110), Image.NEAREST))[35:35 + 1039, 35:35 + 745].copy()
    def rect(x, y, w, h, pad=8):
        H[max(0, int(y / 2 - 35) - pad):int((y + h) / 2 - 35) + pad, max(0, int(x / 2 - 35) - pad):int((x + w) / 2 - 35) + pad] = False
    for k in ("title", "destiny", "lore", "art", "card_type", "game_text"):
        if k in t:
            rect(*t[k])
    rect(1340, 330, 160, 1800, 0)   # expansion sphere, copyright line, set mark
    H[60:120, 600:650] = False      # destiny circle
    cx, cy, _ = disc_745(tn); yy, xx = np.mgrid[:1039, :745]
    H[np.hypot(xx - cx, yy - cy) < 44] = False
    return H


def pairs(ids, scans: Path, renders: Path, cards: dict):
    from scipy.ndimage import binary_erosion, uniform_filter
    S, O, D = [], [], []
    for g in ids:
        c = cards[g]; tn = TPL[(c["side"], c["front"]["type"])]
        s, o = registered(scans / f"{g}.png", renders / f"{g}.png")
        s = np.asarray(s).astype(float); o = np.asarray(o).astype(float)
        M = binary_erosion(frame_mask(tn), iterations=3)
        sb = np.stack([uniform_filter(s[..., i], 3) for i in range(3)], -1)
        ob = np.stack([uniform_filter(o[..., i], 3) for i in range(3)], -1)
        S.append(sb[M][::2]); O.append(ob[M][::2])
        cx, cy, _ = disc_745(tn); yy, xx = np.mgrid[:1039, :745]; dm = np.hypot(xx - cx, yy - cy) < 29
        D.append((tn.split("-")[1], s[dm], o[dm]))
    return np.concatenate(O), np.concatenate(S), D


def _nb(off):
    p = np.pad(off, ((1, 1), (1, 1), (1, 1), (0, 0)), mode="edge")
    return (p[2:, 1:-1, 1:-1] + p[:-2, 1:-1, 1:-1] + p[1:-1, 2:, 1:-1] + p[1:-1, :-2, 1:-1] + p[1:-1, 1:-1, 2:] + p[1:-1, 1:-1, :-2]) / 6


def fit_lut(src, dst):
    acc = np.zeros((N, N, N, 3)); w = np.zeros((N, N, N))
    f = src / 16.0; i0 = np.clip(np.floor(f).astype(int), 0, N - 2); t = f - i0; d = dst - src
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                ww = (t[:, 0] if dx else 1 - t[:, 0]) * (t[:, 1] if dy else 1 - t[:, 1]) * (t[:, 2] if dz else 1 - t[:, 2])
                idx = (i0[:, 0] + dx, i0[:, 1] + dy, i0[:, 2] + dz)
                np.add.at(w, idx, ww); np.add.at(acc, idx, ww[:, None] * d)
    known = w > 2
    off = np.zeros((N, N, N, 3)); off[known] = acc[known] / w[known][:, None]
    off[:3, :3, :3] = 0; known[:3, :3, :3] = True   # blacks stay black
    for _ in range(300):   # empty nodes: diffused from their neighbours
        off = np.where(known[..., None], off, _nb(off))
    return 0.6 * off + 0.4 * _nb(off)   # light smoothing (scan noise)


def disc_curves(src, dst):
    L = np.zeros((3, 256)); qs = np.arange(40, 100); x = np.arange(256) / 255
    for c in range(3):
        a = np.percentile(src[:, c], qs); b = np.percentile(dst[:, c], qs); ok = (a > 4) & (b > 4)
        gam, lg = np.polyfit(np.log(a[ok] / 255), np.log(b[ok] / 255), 1)
        L[c] = np.clip(np.exp(lg) * 255 * x ** gam, 0, 255)
    return L


def main():
    scans, renders = Path(sys.argv[1]), Path(sys.argv[2])
    light, dark = sys.argv[3].split(","), sys.argv[4].split(",")
    out = Path(sys.argv[5]) if len(sys.argv) > 5 else render.ASSETS / "frames/decipher-tone.npz"
    cards = {}
    for side in ("Light", "Dark"):
        for c in json.load(open(ROOT / f"gempdata/{side}.json"))["cards"]:
            cards[c["gempId"]] = c
    res, discs = {}, {"effect": [], "interrupt": []}
    for nm, ids in (("light", light), ("dark", dark)):
        o, s, D = pairs(ids, scans, renders, cards)
        res[nm] = fit_lut(o, s)
        print(nm, len(ids), "cards,", len(o), "pixel pairs; median ours", np.median(o, 0).round(), "printed", np.median(s, 0).round())
        for kind, a, b in D:
            discs[kind].append((b, a))
    for kind, L in discs.items():
        res[f"disc_{kind}"] = disc_curves(np.concatenate([a for a, _ in L]), np.concatenate([b for _, b in L]))
    np.savez_compressed(out, **{k: v.astype(np.float32) for k, v in res.items()})
    print("wrote", out)


if __name__ == "__main__":
    main()
