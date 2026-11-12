"""Episode I Podracer frames (Tatooine 11_47, 11_95-98), built from our own Effect frames.

The printed Podracers differ from the Effect frame only at the top: the title bar runs straight across with a flat
bottom edge (no notch, no lobes round the discs), and the lore box is a plain rectangle, wider and lower than the
Effect's notched box. Measured on the wiki's 497x692 Decipher archive scans (master = 72 + 3 * scan px):
  Dark: header down to y 341, ridge 341..363 (lighter band, highlight), body, lore hole 276..1350 x 402..603.
  Light: silver bar down to y 342, bevel 342..360, red paint 360..393, silver lore box 255..1361 x 393..612.
Everything below the lore box (art window, banner, text box) is the Effect frame unchanged.

Rev 80 rebuild (no seams, Bill 2026-11-12): rev 78 carried mirrored header rows down and pasted a single-column ridge,
which left a light ridge line, streaks in the Light silver bar and a step under the engine icon.
  Dark: the band between the old notch and the new ridge is inpainted (Navier-Stokes) from the header round it, so the
    header's own sheen runs on smoothly; the ridge is the Effect's own straight ridge (its middle section, as a ratio to
    the header above it) stretched across and laid on the new header colour; the body under it is the clean band
    under the Effect's lore box.
  Light: the silver bar is warped down column by column (each column of bar above the Effect's bevel resampled to end
    at the new edge; columns whose lobe already reaches it are only cut), so the brushed silver keeps its texture with
    no repeated rows; the bevel is the Effect's own straight bevel stretched across; the paint strip is the clean paint
    under the Effect's lore box, feathered into the margins; the stamped marks under the destiny circle (cut in half
    by the new edge; the printed Podracer has none there) are inpainted away.
Run: python3 make_podracer_frames.py  -> assets/frames/{ds,ls}-podracer.png
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import cv2

ROOT = Path(__file__).resolve().parent; A = ROOT / "assets"
sys.path[:0] = [str(ROOT)]
import render

LORE = (276, 402, 1350, 603)   # Dark hole (x0, y0, x1, y1), master px
DISCS = [((267, 250), 78), ((1363, 251), 68)]   # type disc and destiny circle (ring outer radius) on the Effect frame
# rev 80: the printed Podracers' destiny circle sits lower (and on Light, further right) than the Effect's: black disc
# centre Dark (1360, 255.5) (4 scans), Light (1375, 266.5) vs the Effect's (1362.5, 250.5) / (1362.5, 251.5)
DESTINY_SHIFT = {"ds": (-2, 5), "ls": (12, 15)}
# ... and the type disc (the podracer engine) sits lower too: template-matched on the scans, Dark (-1, +11), Light (-8, +6)
TYPE_SHIFT = {"ds": (-1, 11), "ls": (-8, 6)}
INNER = {"ds": (171, 1460), "ls": (164, 1461)}   # inside the frame's outer side strips (the strips are vertical, kept)
DARK_RIDGE, DARK_RH, DARK_SRC = 341, 22, 310       # new ridge top, rows, the Effect's straight ridge top (x 420..1220)
LIGHT_EDGE, LIGHT_BH = 342, 18                     # new silver bar foot, bevel rows (paint from 360)
LOWER_SHIFT = 5                                    # art window + banner: 5 px lower than the Effect's (rev 80)


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


CUR = list(DISCS)   # the discs as they sit on the frame being built (destiny moved)


def relocate(G, side, i):
    """Move the Effect's type disc socket (i = 0) or destiny ring (i = 1) by TYPE_SHIFT / DESTINY_SHIFT; returns the mask
    of what it left uncovered."""
    (cx, cy), r = DISCS[i]; dx, dy = (TYPE_SHIFT if i == 0 else DESTINY_SHIFT)[side]
    R = r + (8 if side == "ls" else 3)   # Light: the ring's soft shadow on the silver moves with it
    ys, xs = np.mgrid[0:2220, 0:1632]
    old = (xs - cx) ** 2 + (ys - cy) ** 2 < R * R
    new = (xs - cx - dx) ** 2 + (ys - cy - dy) ** 2 < R * R
    src = G.copy()
    G[new] = src[ys[new] - dy, xs[new] - dx]
    CUR[i] = ((cx + dx, cy + dy), r)
    return old & ~new


def disc_mask(pad=0):
    ys, xs = np.mgrid[0:2220, 0:1632]
    keep = np.zeros((2220, 1632), bool)
    for (cx, cy), r in CUR:
        keep |= (xs - cx) ** 2 + (ys - cy) ** 2 < (r + pad) ** 2
    return keep


def disc_bottom(x):
    b = 0.0
    for (cx, cy), r in CUR:
        if abs(x - cx) < r + 4:
            b = max(b, cy + np.sqrt(max((r + 4) ** 2 - (x - cx) ** 2, 0)))
    return b


def stretch_x(block, w):
    """block (h, n, c) resampled horizontally to w columns (linear)."""
    h, n, c = block.shape
    xs = np.linspace(0, n - 1, w)
    i0 = np.floor(xs).astype(int); i1 = np.minimum(i0 + 1, n - 1); f = (xs - i0)[None, :, None]
    return block[:, i0] * (1 - f) + block[:, i1] * f


def smooth_x(v, k):
    """moving average along axis 1 (edge-padded), v (h, w, c)."""
    p = k // 2
    vp = np.pad(v, ((0, 0), (p, p), (0, 0)), mode="edge")
    cs = np.cumsum(np.pad(vp, ((0, 0), (1, 0), (0, 0))), axis=1)
    return (cs[:, k:] - cs[:, :-k]) / k


def inpaint(G, mask, radius=9):
    """Navier-Stokes inpaint of the RGB channels of G where mask (alpha kept)."""
    rgb = G[:, :, :3].clip(0, 255).astype(np.uint8)
    out = cv2.inpaint(rgb, mask.astype(np.uint8) * 255, radius, cv2.INPAINT_NS)
    G[mask, :3] = out[mask].astype(np.float32)


def laplace_fill(G, mask, iters=3000):
    """Harmonic fill of G's RGB where mask (Dirichlet boundary: every pixel round it), started from a column-wise
    straight blend of the nearest known rows above and below."""
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min() - 1, ys.max() + 2, xs.min() - 1, xs.max() + 2
    U = G[y0:y1, x0:x1, :3].copy(); M = mask[y0:y1, x0:x1]
    for j in range(U.shape[1]):          # initial guess
        col = M[:, j]
        if not col.any():
            continue
        known = np.where(~col)[0]
        U[col, j] = np.stack([np.interp(np.where(col)[0], known, U[known, j, c]) for c in range(3)], 1)
    for _ in range(iters):
        avg = (np.roll(U, 1, 0) + np.roll(U, -1, 0) + np.roll(U, 1, 1) + np.roll(U, -1, 1)) / 4
        U[M] = avg[M]
    G[y0:y1, x0:x1, :3][M] = U[M]


def build_dark(E):
    G = E.copy()
    xl, xr = INNER["ds"]
    Y, RH = DARK_RIDGE, DARK_RH
    vac = relocate(G, "ds", 1) | relocate(G, "ds", 0)
    # 1. body: the clean band under the Effect's lore hole, mirror-tiled, from the ridge foot down to the old hole's foot
    clean0, clean1 = 578, 626
    G[Y + RH:clean0, xl:xr] = mirror_rows(E[clean0:clean1, xl:xr], clean0 - Y - RH)
    # 2. the outer side strips (the Effect's V slopes run into them): column by column, a straight blend between the
    #    strip above the V and the strip below it, so the strip's own bevel lines run straight down
    top_r, bot_r = 288, Y + RH + 24
    for xa, xb in ((141, xl), (xr, 1493)):
        a_ = G[top_r, xa:xb]; b_ = G[bot_r, xa:xb]
        t = ((np.arange(top_r, bot_r) - top_r) / (bot_r - top_r))[:, None, None]
        G[top_r:bot_r, xa:xb] = a_[None] * (1 - t) + b_[None] * t
    # 3. header: from the old notch (ridge and V slopes) down to the ridge foot, a harmonic (Laplace) fill from the
    #    header above, the disc rims, the strips and the body below: smooth, no streaks, the header's sheen runs on
    m = np.zeros((2220, 1632), bool)
    m[290:Y + RH, xl:xr] = True
    m |= vac                                       # where the destiny ring and the type disc socket were
    ys, xs = np.mgrid[0:2220, 0:1632]
    for (cx, cy), r in CUR:                        # and the seam round the moved patches
        d2 = (xs - cx) ** 2 + (ys - cy) ** 2
        m |= (d2 >= (r + 1) ** 2) & (d2 < (r + 7) ** 2) & (xs >= xl) & (xs < xr)
    m[175:290, xl:205] = True; m[175:290, 1425:xr] = True   # the lit facets beside the discs, re-run smoothly
    m &= ~disc_mask(1)
    laplace_fill(G, m)
    # 4. the ridge: the Effect's straight ridge (middle section) as a ratio to the header just above it, stretched
    #    across and laid on the new header colour (its own sheen per column)
    sx0, sx1 = 420, 1220
    ref = E[DARK_SRC - 8:DARK_SRC - 2, sx0:sx1, :3].mean(0)                        # header above the Effect ridge
    rat = E[DARK_SRC:DARK_SRC + RH, sx0:sx1, :3] / np.maximum(ref[None], 1)
    rat = stretch_x(rat, xr - xl)
    hdr = smooth_x(G[Y - 8:Y - 2, xl:xr, :3].mean(0)[None], 31)[0]                  # new header just above
    G[Y:Y + RH, xl:xr, :3] = rat * hdr[None]
    G[Y:Y + RH, xl:xr, 3] = 255
    # 5. the lore hole, plain rectangle, drawn with the Effect hole's own rims
    x0, y0, x1, y1 = LORE
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
    return G


def build_light(E):
    G = E.copy()
    xl, xr = INNER["ls"]
    Y, BH = LIGHT_EDGE, LIGHT_BH
    # the destiny ring and type disc socket moved; the silver they uncover (a crescent up to ~20 px wide) inpainted from the silver round it
    vac = relocate(G, "ls", 1) | relocate(G, "ls", 0)
    inpaint(G, cv2.dilate(vac.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & ~disc_mask(), 6)
    # 0. stamped marks the new edge would cut or push out from under the flag badge (the printed card shows neither):
    #    the marks under the destiny circle and the arrows right of the engine disc, inpainted from the silver round them
    mk = np.zeros((2220, 1632), bool)
    for (x0, y0, x1, y1), th in (((1300, 300, 1440, 372), 7), ((340, 270, 430, 340), 10)):
        lum = G[y0:y1, x0:x1, :3].mean(2); loc = cv2.blur(lum, (25, 25))
        mk[y0:y1, x0:x1] = np.abs(lum - loc) > th
    mk = cv2.dilate(mk.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
    mk &= ~disc_mask(2)
    mk[Y:] = False
    inpaint(G, mk, 5)
    E2 = G.copy()
    # 1. the silver bar warped down: per column, the bar between T (below the discs) and the Effect's bevel top s is
    #    resampled to end at Y. s = first red-paint row minus the Effect bevel's height, a running minimum (flecks in
    #    the paint and the lobes' sloped bevels must not count as bar), smoothed; s >= Y: cut only.
    red = (E2[:, :, 0] - E2[:, :, 2]) > 45
    s = np.zeros(1632)
    for x in range(xl, xr):
        T = int(max(220, disc_bottom(x) + 4))
        ys = np.where(red[T + 4:430, x])[0]
        s[x] = (T + 4 + ys[0] - 17) if len(ys) else 430
    s[xl:xr] = cv2.medianBlur(s[xl:xr].astype(np.float32).reshape(1, -1), 5).ravel()
    ss = s.copy()
    for i in range(xl, xr):
        ss[i] = s[max(xl, i - 24):min(xr, i + 25)].min()
    sm = np.convolve(np.pad(ss[xl:xr], 12, mode="edge"), np.ones(25) / 25, mode="same")[12:-12]
    s = np.full(1632, 430.0); s[xl:xr] = sm
    for x in range(xl, xr):
        T = max(220.0, disc_bottom(x) + 4)
        src_end = min(s[x], Y)
        if src_end >= Y - 0.5:
            continue
        ty = np.arange(int(np.ceil(T)), Y)
        sy = T + (ty - T) * (src_end - T) / (Y - T)
        y0 = np.floor(sy).astype(int); f = (sy - y0)[:, None]
        G[ty, x] = E2[y0, x] * (1 - f) + E2[y0 + 1, x] * f
    # 2. the bevel: the Effect's straight bevel (x 420..1220, rows 313..331) stretched across
    n = 393 - (Y + BH)
    G[Y:Y + BH, xl:xr] = stretch_x(E2[313:313 + BH, 420:1220], xr - xl)
    # 3. the paint strip down to the new box: the clean paint under the Effect's lore box, its big silver flakes (the
    #    twins of the flakes on the art window's rim just below) painted out, feathered into the margins
    strip = E2[586:586 + n, xl:xr].copy()
    silver = ((strip[:, :, 0] - strip[:, :, 2]) < 45).astype(np.uint8)
    k_, lab, st, _ = cv2.connectedComponentsWithStats(silver, 8)
    big = np.zeros_like(silver, bool)
    for i in range(1, k_):
        if st[i, cv2.CC_STAT_AREA] > 350:
            big |= lab == i
    big = cv2.dilate(big.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
    # cloned from the same rows further along (the nearest offset whose patch has no big flake of its own), feathered
    out = strip.copy()
    k_, lab, st, _ = cv2.connectedComponentsWithStats(big.astype(np.uint8), 8)
    for i in range(1, k_):
        x0, w0 = st[i, cv2.CC_STAT_LEFT], st[i, cv2.CC_STAT_WIDTH]
        for dx in (w0 + 40, -(w0 + 40), 2 * w0 + 80, -(2 * w0 + 80), 3 * w0 + 120):
            if 0 <= x0 + dx and x0 + dx + w0 <= strip.shape[1] and not big[:, x0 + dx:x0 + dx + w0].any():
                break
        reg = (lab == i).astype(np.float32)
        al = cv2.GaussianBlur(cv2.dilate(reg, np.ones((7, 7), np.uint8)), (0, 0), 3)[:, :, None].clip(0, 1)
        shifted = np.roll(strip, -dx, axis=1)
        out = out * (1 - al) + shifted * al
    G[Y + BH:393, xl:xr] = out
    for k in range(12):                # below 393 the margins (x < 255, x > 1361) keep the Effect's own paint
        a = 1 - (k + 1) / 13
        for xa, xb in ((xl, 255), (1361, xr)):
            G[393 + k, xa:xb] = E2[586 + n + k, xa:xb] * a + E2[393 + k, xa:xb] * (1 - a)
    # 4. the lore box, plain rectangle: the Light Effect's silver box rescaled to the printed box
    sx0_, sx1_ = 255, 1361                       # old silver box outer edges (incl. rim) on the middle rows
    sy0, sy1 = 354, 581
    box = Image.fromarray(E[sy0:sy1, sx0_:sx1_].clip(0, 255).astype(np.uint8))
    mid = box.crop((0, 90, box.width, 170))
    brim = box.crop((0, box.height - 28, box.width, box.height))
    bx0, by0, bx1, by1 = 255, 393, 1361, 612   # printed: 264..1359 x 393..612 (scan, +-3)
    W, H = bx1 - bx0, by1 - by0
    nb = Image.new("RGBA", (W, H))
    nb.paste(mid.resize((W, H - 56), Image.LANCZOS), (0, 28))
    nb.paste(brim.resize((W, 28), Image.LANCZOS), (0, H - 28))
    nb.paste(brim.transpose(Image.FLIP_TOP_BOTTOM).resize((W, 28), Image.LANCZOS), (0, 0))
    G[by0:by1, bx0:bx1] = np.array(nb).astype(np.float32)
    return G


def build(side):
    E, (fx, fy, fw, fh) = canvas(f"{side}-effect")
    G = build_dark(E) if side == "ds" else build_light(E)
    # the Effect's green type icon under the podracer disc: darkened, so no green sliver shows round the disc
    ys, xs = np.mgrid[0:2220, 0:1632]
    (cx, cy), r = CUR[0]
    inner = (xs - cx) ** 2 + (ys - cy) ** 2 < 82 * 82
    green = inner & (G[:, :, 1] > G[:, :, 0] + 15)
    G[green, :3] = 24
    # the printed Podracers' art window and banner sit 5 px lower than the Effect's (the text box top does not move on
    # Dark, ~4 px on Light): the band from above the art window to above the text box (Light: through its top rim) moves
    # down 5 px; the 5 rows it opens above are the body rows just over it
    b0, b1 = 630, (1640 if side == "ls" else 1600)
    G[b0 + LOWER_SHIFT:b1 + LOWER_SHIFT] = G[b0:b1].copy()
    G[b0:b0 + LOWER_SHIFT] = G[b0 - LOWER_SHIFT:b0]
    # ... and the text box runs 6 px further down (printed box foot Dark 2011 / Light shadow 2003 vs 2004 / 1997), its
    # foot rim and the body under it moved down, the frame's bottom bevel pressed into the rows left (edge kept at 2078)
    src = G.copy()
    def remap(t0, t1, s0, s1):
        t = np.arange(t0, t1); sy = s0 + (t - t0) * (s1 - s0) / (t1 - t0)
        y0 = np.floor(sy).astype(int); f = (sy - y0)[:, None, None]
        G[t0:t1] = src[y0] * (1 - f) + src[np.minimum(y0 + 1, 2219)] * f
    remap(1975, 2003, 1975, 1997)
    G[2003:2060] = src[1997:2054]
    remap(2060, 2078, 2054, 2078)
    out = Image.fromarray(G.clip(0, 255).astype(np.uint8)).crop((fx, fy, fx + fw, fy + fh))
    out.save(A / "frames" / f"{side}-podracer.png", optimize=True)
    return out


if __name__ == "__main__":
    for s in sys.argv[1:] or ("ds", "ls"):
        build(s); print("wrote", A / "frames" / f"{s}-podracer.png")
