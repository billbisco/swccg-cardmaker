"""Episode I Podracer frames (Tatooine 11_47, 11_95-98), built from our own Effect frames.

The printed Podracers differ from the Effect frame only at the top: the title bar runs straight across with a flat
bottom ridge (no notch), and the lore box is a plain rectangle, wider and lower than the Effect's notched box. Measured on
the wiki's 497x692 Decipher archive scans (card body 24..471 x 24..669, so master = 144 + (scan - 24) * 3):
  title-bar ridge master y 336..360, lore box 276..1350 x 402..603 (Dark: black hole; Light: silver box, rim 264..1359 x
  393..612). Everything below the lore box (art window, banner, text box) is the Effect frame unchanged.
Construction: the band between the title bar and the art window is refilled column by column with the clean frame rows
under the Effect's lore box (mirror-tiled), the header colour is carried down to the new ridge, the Effect's own centre
ridge profile is copied to the new height, and the new lore box is drawn with the Effect box's own rims.
Run: python3 make_podracer_frames.py  -> assets/frames/{ds,ls}-podracer.png
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent; A = ROOT / "assets"
sys.path[:0] = [str(ROOT)]
import render

RIDGE = 336            # new title-bar ridge top (printed 336..360)
LORE = (276, 402, 1350, 603)   # Dark hole (x0, y0, x1, y1), master px
DISCS = [((267, 250), 78), ((1363, 251), 68)]   # type disc and destiny circle (ring outer radius): kept as they are
EDGE = (172, 1458)     # the outer frame bevel left / right of the old notch: the Effect's own


def canvas(key):
    fr, fx, fy = render.TEMPLATES[key]["frame"]
    im = Image.open(A / fr).convert("RGBA")
    c = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0)); c.alpha_composite(im, (fx, fy))
    return np.array(c).astype(np.float32), (fx, fy, im.width, im.height)


def mirror_rows(src, n):
    """n rows tiled from src rows (h, w, 4), mirrored at each repeat so the seams don't show."""
    out, k = [], 0
    while sum(len(o) for o in out) < n:
        out.append(src if k % 2 == 0 else src[::-1]); k += 1
    return np.concatenate(out)[:n]


def build(side):
    E, (fx, fy, fw, fh) = canvas(f"{side}-effect")
    G = E.copy()
    ys, xs = np.mgrid[0:2220, 0:1632]
    keep = np.zeros((2220, 1632), bool)
    for (cx, cy), r in DISCS:
        keep |= (xs - cx) ** 2 + (ys - cy) ** 2 < r * r
    el, er = EDGE
    # 1. the band between the old notch and the art window: the clean rows under the Effect's lore box, mirror-tiled
    if side == "ds":
        clean0, clean1, notch_top, ridge_src = 578, 626, 296, 309
    else:
        clean0, clean1, notch_top, ridge_src = 584, 632, 296, 326
    if side == "ds":   # smooth paint: the whole band, mirror-tiled
        band = mirror_rows(E[clean0:clean1], clean0 - RIDGE - 26)
        G[RIDGE + 26:clean0] = band[: clean0 - RIDGE - 26]
    else:              # scratched paint: only the strip above the new silver box (the margins are already clean)
        n0 = 393 - RIDGE - 26
        G[RIDGE + 26:393, el:er] = E[clean0:clean0 + n0, el:er]
    # 2. the title bar carried down to the ridge: the header rows just above the old notch, mirrored, discs kept
    n = RIDGE - notch_top
    hdr = E[notch_top - n:notch_top][::-1]
    m = ~keep[notch_top:RIDGE]
    m[:, :el] = False; m[:, er:] = False
    G[notch_top:RIDGE][m] = hdr[m]
    # under the discs the mirrored rows would repeat the disc: blend across them from the header either side
    for (cx, cy), r in DISCS:
        L, R = cx - r - 2, cx + r + 2
        # the header colour of the inner side (left disc: its right; destiny circle: its left), carried across
        src = G[notch_top:RIDGE, R:R + 1] if cx < 800 else G[notch_top:RIDGE, L - 1:L]
        blend = np.repeat(src, R - L, 1)
        mk = ~keep[notch_top:RIDGE, L:R]
        G[notch_top:RIDGE, L:R][mk] = blend[mk]
    if side == "ds":   # smooth paint: soften the carried header horizontally so the disc columns don't show as blocks
        k = 61; blk = G[notch_top:RIDGE, el - k:er + k].copy()
        cs = np.cumsum(np.pad(blk, ((0, 0), (1, 0), (0, 0))), axis=1)
        sm = (cs[:, k:] - cs[:, :-k]) / k
        off = (k - 1) // 2
        sm = sm[:, k - off:k - off + (er - el)]
        mk = ~keep[notch_top:RIDGE, el:er]
        G[notch_top:RIDGE, el:er][mk] = sm[mk]
    # 3. the ridge: the Effect's centre ridge profile (26 rows), copied column by column at the new height,
    #    scaled by the header's own brightness per column (the horizontal sheen)
    prof = E[ridge_src:ridge_src + 26, 800:801]
    ridge = np.repeat(prof, 1632, 1)
    hb = G[RIDGE - 3, :, :3].mean(1); hb = hb / max(hb[700:900].mean(), 1)
    ridge[:, :, :3] *= np.clip(hb, 0.75, 1.25)[None, :, None]
    G[RIDGE:RIDGE + 26, el:er] = ridge[:, el:er]
    # 4. the lore box, plain rectangle, drawn with the Effect box's own rims
    x0, y0, x1, y1 = LORE
    if side == "ds":
        # Effect hole rims (centre column / middle row of the old notched hole)
        top = E[358:374, 800:801]                    # rows above the hole: lighter rim
        bot = E[566:580, 800:801]                    # rows below the hole
        G[y0 - 16:y0, x0:x1] = np.repeat(top, x1 - x0, 1)
        G[y1:y1 + 14, x0:x1] = np.repeat(bot, x1 - x0, 1)
        holes = np.where(E[480, 250:1420, 3] < 128)[0] + 250
        lx, rx = int(holes.min()), int(holes.max()) + 1      # the old hole's left / right edge on a middle row
        lft = E[480:481, lx - 12:lx]; rgt = E[480:481, rx:rx + 12]
        G[y0 - 16:y1 + 14, x0 - 12:x0] = np.repeat(lft, y1 - y0 + 30, 0)
        G[y0 - 16:y1 + 14, x1:x1 + 12] = np.repeat(rgt, y1 - y0 + 30, 0)
        G[y0:y1, x0:x1] = 0                          # the hole (render.py draws the black box under the frame)
    else:
        # the Light Effect's silver lore box is part of the frame: rows 420..560 have no notch; rescale it to the new box
        sx0, sx1 = 255, 1361                         # old silver box outer edges (incl. rim) on the middle rows
        sy0, sy1 = 354, 581
        box = Image.fromarray(E[sy0:sy1, sx0:sx1].clip(0, 255).astype(np.uint8))
        # body: middle rows (no notch) stretched; top rim: the bottom rim flipped
        mid = box.crop((0, 90, box.width, 170))
        brim = box.crop((0, box.height - 28, box.width, box.height))
        bx0, by0, bx1, by1 = 255, 393, 1361, 612   # printed: 264..1359 x 393..612 (scan, +-3)
        W, H = bx1 - bx0, by1 - by0
        nb = Image.new("RGBA", (W, H))
        nb.paste(mid.resize((W, H - 56), Image.LANCZOS), (0, 28))
        nb.paste(brim.resize((W, 28), Image.LANCZOS), (0, H - 28))
        nb.paste(brim.transpose(Image.FLIP_TOP_BOTTOM).resize((W, 28), Image.LANCZOS), (0, 0))
        G[by0:by1, bx0:bx1] = np.array(nb).astype(np.float32)
    # 5. the Effect's green type icon under the podracer disc: darkened, so no green sliver shows round the disc
    (cx, cy), r = DISCS[0]
    inner = (xs - cx) ** 2 + (ys - cy) ** 2 < 82 * 82
    green = inner & (G[:, :, 1] > G[:, :, 0] + 15)
    G[green, :3] = 24
    out = Image.fromarray(G.clip(0, 255).astype(np.uint8)).crop((fx, fy, fx + fw, fy + fh))
    out.save(A / "frames" / f"{side}-podracer.png", optimize=True)
    return out


if __name__ == "__main__":
    for s in ("ds", "ls"):
        build(s); print("wrote", A / "frames" / f"{s}-podracer.png")
