"""Rev 80: re-cut every expansion sphere from the printed cards themselves, stacked.

Each sphere is about 13-28 px across on the best scans we have (Decipher's archive faces on the wiki: 350-500 px wide;
the A New Hope Holotable hires faces: 1497 px; the PC's own 745 px faces). One scan is soft, but every card of a set
carries the same sphere at a slightly different sub-pixel position, so the spheres of many cards, each centred on its
own black ring to a hundredth of a pixel and scaled by its ring radius, average into one sharp sphere (median per
pixel, so a frame's highlight or a speck on one card drops out). No AI upscaling, no retouching, no redrawing.

  decipher  set-<key>-decipher.png  from Decipher's printed faces of that set (wiki "...-decipher-archive" scans;
            A New Hope: the wiki's 1497 px "-hires.webp" faces)
  pc        set-<key>-pc.png        from the Players Committee's printed Virtual cards that carry that sphere
            (res.starwarsccg.org 745 px hires faces)

Output: 312 px RGBA, the sphere cut at 0.92 of its black ring's centre-line radius (the inner half of the ring stays,
as the earlier scan cuts, rev 32/33), anti-aliased round mask; render.py sets it in the frame's black hole.
Sources: tools/set_spheres/sources.json (urls; "decipher_kept" / "pc_kept" lists are not cut: those files stay, see
_note there). Also writes stack evidence to --evidence (per set: the stack and how
many cards went in).

    python3 tools/set_spheres/cut_set_spheres.py [--only anh,hoth] [--style decipher|pc|both] [--cache DIR]
"""
from __future__ import annotations
import argparse, hashlib, io, json, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw
from scipy import ndimage, optimize

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "swccg-cardmaker/1.0"}
OUT_PX = 312
CUT = 0.92          # cut radius / ring centre-line radius
GRID = 256          # stack grid (covers +-1.25 ring radii)
SPAN = 1.25


def fetch(url: str, cache: Path) -> Path | None:
    p = cache / (hashlib.sha1(url.encode()).hexdigest()[:16] + Path(url).suffix)
    if not p.exists():
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception:
            return None
        if data[:5] == b"<?xml":
            return None
        p.write_bytes(data)
    return p


def ring_template(d: int):
    """Black ring on a lighter rim, the inside masked out (any sphere picture), at 745 px scale."""
    n = d + 12; c = (n - 1) / 2; r = d / 2
    y, x = np.mgrid[0:n, 0:n]; rho = np.hypot(x - c, y - c)
    t = np.full((n, n), 128, np.float32); m = np.zeros((n, n), np.float32)
    ring = (rho > r - 2.2) & (rho < r + 0.8); rim = (rho > r + 2.2) & (rho < r + 5.5)
    t[ring] = 0; t[rim] = 200; m[ring | rim] = 1
    return t, m


def locate(g745: np.ndarray):
    """(score, cx, cy, d) of the sphere at 745 px: a dark ring with a lighter rim in the right margin. Episode I-era
    cards carry the black Episode I disc right under it, which matches the ring as well: of the good hits (within 85 %
    of the best score) the uppermost is the sphere."""
    H, W = g745.shape
    x0, y0, x1, y1 = 590, 90, W, min(H, 600)
    reg = g745[y0:y1, x0:x1].astype(np.float32)
    hits = []
    for d in range(22, 38):
        t, m = ring_template(d)
        r = cv2.matchTemplate(reg, t, cv2.TM_CCOEFF_NORMED, mask=m)
        r = np.nan_to_num(r, nan=-1, posinf=-1, neginf=-1)
        n = t.shape[0]
        for _ in range(3):   # the three best places at this size
            _, mx, _, loc = cv2.minMaxLoc(r)
            hits.append((mx, x0 + loc[0] + n / 2 - 0.5, y0 + loc[1] + n / 2 - 0.5, d))
            cv2.circle(r, loc, d // 2 + 2, -1, -1)
    def ep1_like(h):   # inside black once the I's stem and the EPISODE band are left out
        _, cx, cy, d = h; r = d / 2 - 2
        yy, xx = np.mgrid[0:H, 0:W]
        m = (np.hypot(xx - cx, yy - cy) < r * 0.85) & (abs(xx - cx) > 0.18 * r) & (abs(yy - cy) > 0.16 * r)
        return g745[m].mean() < 40 if m.any() else True
    hits = [h for h in hits if not ep1_like(h)] or hits
    best = max(h[0] for h in hits)
    good = [h for h in hits if h[0] >= 0.85 * best]
    top = min(h[2] for h in good)
    upper = [h for h in good if h[2] < top + 12]   # the uppermost object; its best-scoring size
    return max(upper)


def refine(g: np.ndarray, cx: float, cy: float, r: float):
    """Sub-pixel centre and radius of the black ring's centre line (native px): the circle along which the scan is
    darkest against the sphere just inside it and the frame's rim just outside (bounded near the coarse hit)."""
    pad = int(r * 2 + 6)
    ox, oy = max(0, int(cx) - pad), max(0, int(cy) - pad)
    sub = g[oy:int(cy) + pad, ox:int(cx) + pad].astype(float)
    th = np.linspace(0, 2 * np.pi, 160, endpoint=False)
    w = max(1.0, 0.2 * r)

    def ring(x, y, rr):
        return ndimage.map_coordinates(sub, [y - oy + rr * np.sin(th), x - ox + rr * np.cos(th)], order=1).mean()

    def f(p):
        x, y, rr = p
        return ring(x, y, rr) - 0.5 * ring(x, y, rr - w) - 0.5 * ring(x, y, rr + w)
    best = None
    b = [(cx - 0.3 * r, cx + 0.3 * r), (cy - 0.3 * r, cy + 0.3 * r), (0.8 * r, 1.2 * r)]
    for k in (0.92, 1.0, 1.08):
        res = optimize.minimize(f, [cx, cy, r * k], method="Powell", bounds=b, options=dict(xtol=0.003, ftol=1e-4))
        if best is None or res.fun < best.fun:
            best = res
    x, y, rr = best.x
    return best.x, ring(x, y, rr)


def sample(rgb: np.ndarray, cx: float, cy: float, r: float):
    u = np.linspace(-SPAN, SPAN, GRID)
    X, Y = np.meshgrid(cx + u * r, cy + u * r)
    return np.stack([ndimage.map_coordinates(rgb[:, :, i].astype(float), [Y, X], order=3, mode="nearest") for i in range(3)], 2)


def align(rgb: np.ndarray, x: float, y: float, r: float, ref: np.ndarray):
    """Centre and scale that best match the card's sphere to a reference stack (normalised cross-correlation over the
    sphere and its ring): registers soft scans whose thin ring alone is too broken to fit (Endor at 367 px)."""
    g = rgb.mean(2).astype(float)
    n = 72; u = np.linspace(-SPAN, SPAN, n)
    rf = np.array(Image.fromarray(ref).convert("L").resize((n, n), Image.LANCZOS)).astype(float)
    U, V = np.meshgrid(u, u); m = np.hypot(U, V) <= 1.12
    rf = rf[m]; rf = (rf - rf.mean()) / (rf.std() + 1e-6)

    def f(p):
        cx, cy, rr = p
        v = ndimage.map_coordinates(g, [cy + V * rr, cx + U * rr], order=1, mode="nearest")[m]
        return -np.mean(rf * (v - v.mean()) / (v.std() + 1e-6))
    b = [(x - 0.3 * r, x + 0.3 * r), (y - 0.3 * r, y + 0.3 * r), (0.85 * r, 1.15 * r)]
    res = optimize.minimize(f, [x, y, r], method="Powell", bounds=b, options=dict(xtol=0.003, ftol=1e-5))
    return res.x, -res.fun


def stack_set(paths, ref=None):
    """Median of the sphere crops: centred on the ring first, then (second pass) each card registered to the reference
    (the PC stack of the same sphere when there is one, else this set's own first stack)."""
    cards, info = [], []
    for p in paths:
        try:
            im = Image.open(p).convert("RGB")
        except Exception:
            continue
        if im.width > im.height:
            continue
        s = 745 / im.width
        g745 = np.array(im.resize((745, round(im.height * s)), Image.LANCZOS).convert("L"))
        sc, cx, cy, d = locate(g745)
        if sc < 0.55:
            continue
        rgb = np.array(im)
        (x, y, r), v = refine(rgb.mean(2), cx / s, cy / s, (d / 2 - 0.7) / s)
        info.append(dict(src=Path(p).name, score=round(float(sc), 3), cx=round(float(x), 2), cy=round(float(y), 2),
                         r=round(float(r), 2), ring=round(float(v), 1), w=im.width))
        cards.append((rgb, x, y, r))
    if not cards:
        return None, info
    # keep the cards whose ring radius (relative to the card width) agrees with the majority: drops wrong hits
    rel = np.array([i["r"] / i["w"] for i in info]); med = np.median(rel)
    keep = [k for k in range(len(cards)) if abs(rel[k] / med - 1) < 0.08]
    first = np.median(np.array([sample(*cards[k]) for k in keep]), 0)
    first = np.clip(first, 0, 255).astype(np.uint8)
    for attempt, rf in enumerate((ref, first) if ref is not None else (first,)):
        crops, keep2 = [], []
        for k in keep:
            rgb, x, y, r = cards[k]
            (x, y, r), ncc = align(rgb, x, y, r, rf)
            info[k].update(ax=round(float(x), 2), ay=round(float(y), 2), ar=round(float(r), 2), ncc=round(float(ncc), 3), ref="pc" if rf is ref and ref is not None else "self")
            if ncc > 0.5:
                crops.append(sample(rgb, x, y, r)); keep2.append(k)
        if len(keep2) >= max(2, len(keep) // 2):   # the PC stack did not fit these scans (too few PC faces): self-register
            break
    for k in range(len(info)):
        info[k]["used"] = k in keep2
    if not crops:
        return None, info
    st = np.median(np.array(crops), 0)
    return np.clip(st, 0, 255).astype(np.uint8), info


def cut(st: np.ndarray) -> Image.Image:
    """The sphere at CUT of the ring radius, OUT_PX across, round anti-aliased mask."""
    c = (GRID - 1) / 2; h = CUT / SPAN * (GRID - 1) / 2
    im = Image.fromarray(st).resize((OUT_PX, OUT_PX), Image.LANCZOS, box=(c - h + 0.5, c - h + 0.5, c + h + 0.5, c + h + 0.5))
    m = Image.new("L", (OUT_PX * 4, OUT_PX * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, OUT_PX * 4 - 1, OUT_PX * 4 - 1), fill=255)
    im = im.convert("RGBA"); im.putalpha(m.resize((OUT_PX, OUT_PX), Image.LANCZOS))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--style", default="both")
    ap.add_argument("--cache", default="/tmp/set-spheres-cache")
    ap.add_argument("--evidence", default="")
    ap.add_argument("--out", default=str(ROOT / "assets/icons"))
    a = ap.parse_args()
    src = json.loads((HERE / "sources.json").read_text())
    cache = Path(a.cache); cache.mkdir(parents=True, exist_ok=True)
    ev = Path(a.evidence) if a.evidence else None
    if ev:
        ev.mkdir(parents=True, exist_ok=True)
    report = {}
    for key, styles in src.items():
        if key.startswith("_"):
            continue
        if a.only and key not in a.only.split(","):
            continue
        ref = None
        for style in ("pc", "decipher"):   # the PC's sharp 745 px faces first: the Decipher scans register to them
            urls = styles.get(style)
            if not urls:
                continue
            with ThreadPoolExecutor(8) as ex:
                paths = [p for p in ex.map(lambda u: fetch(u, cache), urls) if p]
            st, info = stack_set(paths, ref)
            if style == "pc":
                ref = st
            if a.style != "both" and style != a.style:
                continue
            n = sum(1 for i in info if i.get("used"))
            report[f"{key}-{style}"] = dict(cards=n, of=len(urls), details=info)
            print(f"{key:14s} {style:8s} {n:3d} cards stacked of {len(urls)}", flush=True)
            if st is None or n < 2:
                continue
            cut(st).save(Path(a.out) / f"set-{key}-{style}.png")
            if ev:
                Image.fromarray(st).save(ev / f"stack-{key}-{style}.png")
    if ev:
        (ev / "report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
