"""Rev 81 (frames): Decipher's printed Jedi Test frame (Dagobah Jedi Tests #1-#5, Death Star II's #6 and the PC's
It Is The Future You See (V) print the same frame) rebuilt from the printed faces -> assets/frames/ls-jeditest-olive.png.

The six printed faces (GEMP hires, 745 x 1039: 4_75-4_79, 9_55) are pixel-registered (card body 34..709 x 36..1003 on
every one); each card body is scaled to the master card area (144..1487 x 144..2075) and the per-pixel median taken:
the frame is identical on all six, art / title / text / destiny / sphere / copyright differ. Then:
  * art window = where the six faces differ (std) inside the window's bounds, holes filled, edge anti-aliased;
  * title bar, banner and text box interiors: the Light Effect frame's crisp silver (ls-effect.png) high-pass detail
    over the printed low-pass shading (taken from the per-pixel brightest face, residual ink inpainted) - no text;
  * margin: Decipher's olive paint over silver, the paint mask from the median (olive = saturated yellow-green),
    re-drawn crisp at master size with the printed olive (58, 61, 15) and a light grain; silver chips keep the scan;
  * destiny circle filled black (the number is drawn by the renderer), the expansion sphere and the copyright strip
    painted olive (both drawn by the renderer, DC_PRINT).
Usage: python3 tools/make_jeditest_frame.py [scan_cache_dir]"""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
import cv2

ROOT = Path(__file__).resolve().parents[1]
GIDS = ["4_75", "4_76", "4_77", "4_78", "4_79", "9_55"]
CACHE = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "out" / "jt-scans")
OLIVE = np.array([58.0, 61.0, 15.0])


def scans():
    CACHE.mkdir(parents=True, exist_ok=True)
    cards = {c["gempId"]: c for f in ("Light", "Dark") for c in json.load(open(ROOT / f"gempdata/{f}.json"))["cards"]}
    out = []
    for g in GIDS:
        p = CACHE / f"{g}.png"
        if not p.exists() or p.stat().st_size < 1000:
            u = cards[g]["front"]["imageUrl"].replace("/large/", "/hires/").replace(".gif", ".png")
            subprocess.run(["curl", "-sS", "-m", "60", "-o", str(p), u], check=True)
        a = Image.open(p).convert("RGB")
        assert a.size == (745, 1039), (g, a.size)
        a = a.crop((34, 36, 710, 1004)).resize((1344, 1932), Image.LANCZOS)
        c = Image.new("RGB", (1632, 2220), (0, 0, 0)); c.paste(a, (144, 144))
        out.append(np.array(c).astype(np.float32))
    return np.stack(out)


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def main():
    S = scans()
    med = np.median(S, 0)
    sd = S.std(0).mean(-1)
    H, W = med.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    out = med.copy()
    alpha = np.zeros((H, W), np.float32)
    alpha[144:2076, 144:1488] = 1.0
    # card's outer edge: the scans' own anti-aliased silhouette (cut corners)
    lum = med.mean(-1)
    alpha[(lum < 18) & ((xx < 170) | (xx > 1460) | (yy < 170) | (yy > 2050))] = 0.0

    # --- art window: the faces differ there
    win = np.zeros((H, W), np.uint8)
    win[380:1108, 240:1402] = (sd[380:1108, 240:1402] > 14).astype(np.uint8)
    win = cv2.morphologyEx(win, cv2.MORPH_OPEN, disk(3))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(win)
    big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    win = (lab == big).astype(np.uint8)
    ff = win.copy(); m = np.zeros((H + 2, W + 2), np.uint8); cv2.floodFill(ff, m, (0, 0), 1)
    win = win | (1 - ff)                                   # holes filled
    # the opening is one run per row and per column: take each row's / column's extent, median-filter the four
    # boundary profiles (dark art at the edge on all six faces made notches), fill
    from scipy.ndimage import median_filter
    def prof(mask, axis):
        idx = np.arange(mask.shape[1 - axis])
        lo = np.full(mask.shape[axis], -1.0); hi = np.full(mask.shape[axis], -1.0)
        for i in range(mask.shape[axis]):
            r = np.nonzero(mask[i] if axis == 0 else mask[:, i])[0]
            if len(r) > 40:
                lo[i], hi[i] = r.min(), r.max()
        ok = lo >= 0
        k = np.nonzero(ok)[0]
        lo[k] = median_filter(lo[k], 101, mode="nearest"); hi[k] = median_filter(hi[k], 101, mode="nearest")
        return ok, lo, hi
    okr, l, r = prof(win, 0)
    rowfill = np.zeros_like(win)
    for y in np.nonzero(okr)[0]:
        rowfill[y, int(l[y]):int(r[y]) + 1] = 1
    okc, t, b = prof(rowfill, 1)
    win = np.zeros_like(win)
    for x in np.nonzero(okc)[0]:
        win[int(t[x]):int(b[x]) + 1, x] = rowfill[int(t[x]):int(b[x]) + 1, x]
    win = cv2.morphologyEx(win, cv2.MORPH_OPEN, disk(5))
    win = cv2.morphologyEx(win, cv2.MORPH_CLOSE, disk(15))
    # lower half: straight sides and bottom with the printed 18 px rounded corners (dark art at the corner on all six
    # faces hides the edge there)
    xL = int(np.median(l[600:1000])); xR = int(np.median(r[600:1000])); yB = int(np.median(b[500:1200]))
    rr = np.zeros_like(win); rc = 18
    rr[600:yB + 1, xL:xR + 1] = 1
    for cx in (xL + rc, xR - rc):
        q = (yy > yB - rc) & (np.abs(xx - cx) <= rc) & ((xx < xL + rc) | (xx > xR - rc))
        rr[q & ((xx - cx) ** 2 + (yy - (yB - rc)) ** 2 > rc * rc)] = 0
    win[600:] = rr[600:]
    print("window sides", xL, xR, "bottom", yB)
    wa = cv2.GaussianBlur(win.astype(np.float32), (0, 0), 1.0)
    alpha = alpha * (1 - wa)
    ys, xs = np.nonzero(win)
    print("art window", xs.min(), ys.min(), xs.max(), ys.max())

    # --- text-free shading: per pixel the brightest face, residual ink inpainted
    L = S.mean(-1)
    idx = np.argsort(L, 0)[-2]                             # 2nd brightest (the brightest can be a highlight)
    bright = np.take_along_axis(S, idx[None, :, :, None].repeat(3, -1), 0)[0]
    bl = bright.mean(-1)
    ink = (bl < cv2.GaussianBlur(bl, (0, 0), 12) - 12).astype(np.uint8)
    ink = cv2.dilate(ink, disk(4))
    clean = cv2.inpaint(np.clip(bright, 0, 255).astype(np.uint8), ink, 6, cv2.INPAINT_TELEA).astype(np.float32)

    # --- crisp silver from the Light Effect frame, on the printed shading
    E = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0))
    E.alpha_composite(Image.open(ROOT / "assets/frames/ls-effect.png").convert("RGBA"), (140, 139))
    E = np.array(E)[..., :3].astype(np.float32)

    def plate(src_box, dst_box, mask):
        sx0, sy0, sx1, sy1 = src_box; dx0, dy0, dx1, dy1 = dst_box
        tex = cv2.resize(E[sy0:sy1, sx0:sx1], (dx1 - dx0, dy1 - dy0), interpolation=cv2.INTER_LANCZOS4)
        det = tex - cv2.GaussianBlur(tex, (0, 0), 10)
        low = cv2.GaussianBlur(cv2.dilate(clean, disk(9)), (0, 0), 14)[dy0:dy1, dx0:dx1]   # grey-level max: no ink left
        new = low + det
        mk = cv2.GaussianBlur(mask[dy0:dy1, dx0:dx1].astype(np.float32), (0, 0), 3)[..., None]
        plates[dy0:dy1, dx0:dx1] |= mask[dy0:dy1, dx0:dx1] > 0
        out[dy0:dy1, dx0:dx1] = out[dy0:dy1, dx0:dx1] * (1 - mk) + new * mk

    zone = np.zeros((H, W), np.uint8)
    plates = np.zeros((H, W), bool)
    # title bar (between the disc ring and the destiny ring, above the bar's lower bevel)
    zone[:] = 0; zone[166:312, 372:1272] = 1
    zone[(xx - 265) ** 2 + (yy - 233) ** 2 < 100 ** 2] = 0
    zone[(xx - 1360) ** 2 + (yy - 253) ** 2 < 104 ** 2] = 0
    plate((420, 165, 1250, 300), (360, 160, 1290, 316), zone.copy())
    zone[:] = 0; zone[1170:1248, 262:1372] = 1
    plate((280, 1500, 1330, 1572), (256, 1166, 1378, 1252), zone.copy())   # banner
    zone[:] = 0; zone[1306:1988, 278:1356] = 1
    plate((300, 1680, 1330, 1960), (272, 1300, 1362, 1994), zone.copy())   # text box

    # --- margin paint: olive over silver, re-drawn crisp
    mx, mn = med.max(-1), med.min(-1)
    sat = (mx - mn) / (mx + 1)
    p = np.clip((sat - 0.22) / 0.25, 0, 1) * (med[..., 2] < med[..., 1] - 10)
    p = p.astype(np.float32)
    # the sphere and the copyright strip (drawn by the renderer): paint
    p[(xx - 1437) ** 2 + (yy - 419) ** 2 < 36 ** 2] = 1
    p[440:1110, 1418:1468] = 1
    field = cv2.dilate((p > 0.5).astype(np.uint8), disk(5)).astype(bool)
    field &= wa < 0.01
    field &= ~cv2.dilate(plates.astype(np.uint8), disk(6)).astype(bool)   # the plates' own interiors (ink fringes)
    field &= (xx - 265) ** 2 + (yy - 233) ** 2 > 100 ** 2                  # the type disc (the Jedi Test stone)
    ps = cv2.GaussianBlur(p, (0, 0), 1.6)
    a = np.clip((ps - 0.5) / 0.18 + 0.5, 0, 1)            # crisp, anti-aliased paint edge
    rng = np.random.default_rng(81)
    grain = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 1.2) * 9
    olive = OLIVE[None, None, :] + grain[..., None] * np.array([1.0, 1.0, 0.5])
    silver_lp = cv2.GaussianBlur(np.where((p < 0.1)[..., None], med, 0), (0, 0), 3) / \
        np.maximum(cv2.GaussianBlur((p < 0.1).astype(np.float32), (0, 0), 3), 1e-3)[..., None]
    silver = np.where((p < 0.15)[..., None], med, silver_lp)
    mixed = olive * a[..., None] + silver * (1 - a[..., None])
    out[field] = mixed[field]

    # --- destiny circle: black (the renderer draws the number)
    dz = (xx - 1360) ** 2 + (yy - 253) ** 2
    da = np.clip(53.5 - np.sqrt(dz), 0, 1)[..., None]
    out = out * (1 - da)

    rgba = np.dstack([np.clip(out, 0, 255), alpha * 255]).round().astype(np.uint8)
    dst = ROOT / "assets/frames/ls-jeditest-olive.png"
    Image.fromarray(rgba, "RGBA").save(dst, optimize=True)
    print("wrote", dst)


if __name__ == "__main__":
    main()
