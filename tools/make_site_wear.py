"""Rev 84 (site wear and PC wide starships): the paint of Decipher's blue starship / vehicle site frames, rebuilt from
the printed faces -> assets/frames/site-wear-light.png (frame coordinates, 2073 x 1497, the size of
assets/frames/loc-site.png).

Decipher printed the Light starship / vehicle sites (Sandcrawler: Loading Bay, Home One: War Room / Docking Bay,
Blockade Flagship: Docking Bay) with the blue paint worn through to the silver in large scratched patches - heaviest on
the strips between the title bars and the picture and along the outer rim - and the Dark ones (Executor sites,
Sandcrawler: Droid Junkheap, Star Destroyer: Launch Bay, ...) in smooth unworn blue (checked on the six hi-res Dark
faces below: no wear to rebuild; the renderer paints them plain, as before). Each Light card has its own
patches, in the same places on every copy (the wiki's hi-res scan and Decipher's archive image of Loading Bay agree).

  * Every printed face is registered to the site frame (loc-site.png on the master card, 2220 x 1632, its paint zone
    tinted blue as printed) by ECC (affine, coarse to fine; a sheared fit is rejected) over the card body and its
    edge on the black border, the picture masked out. Each scan is saved as out/site-wear-scans/registered-*.png.
  * Each registered face is classified inside the frame's paint zone: blue paint 1, silver 0, anything else (the
    black copyright line, the sphere, icons) unknown.
  * Light wear = the per-pixel median of the four Light faces (unknown left out): worn where most of them show silver.
    No smoothing, no hand retouching; site-wear-light.png: 255 = worn to the silver.
    Under the copyright line (the same place on all four) no face shows the paint: left unworn.

Faces (wiki.swccg.com): Light: ANH-L-sandcrawlerloadingbay-hires.webp (2073 px), DS2-L-homeonewarroom /
DS2-L-homeonedockingbay / Theed-L-blockadeflagshipdockingbay -decipher-archive (Decipher's own images, ~500 px);
Dark (checked, not used): the six -hires.webp faces (Droid Junkheap, Executor: Comm Station / Control Station /
Holotheatre / Main Corridor / Meditation Chamber).
Usage: python3 tools/make_site_wear.py [scan_cache_dir]"""
from __future__ import annotations
import json, sys, urllib.parse, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
import cv2

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "out" / "site-wear-scans")
API = "https://wiki.swccg.com/api.php"
LIGHT = ["ANH-L-sandcrawlerloadingbay-hires.webp", "DS2-L-homeonewarroom-decipher-archive.gif",
         "DS2-L-homeonedockingbay-decipher-archive.gif", "Theed-L-blockadeflagshipdockingbay-decipher-archive.jpg"]
MW, MH = 2220, 1632          # master card (landscape)
FX, FY = 74, 76              # loc-site frame offset on the master (render.TEMPLATES["loc-site"]["frame_off"])


def fetch(name: str) -> Path:
    p = CACHE / name
    if not p.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        q = urllib.parse.urlencode({"action": "query", "titles": "File:" + name, "prop": "imageinfo",
                                    "iiprop": "url", "format": "json"})
        req = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "cardmaker-tools/1.0"}), timeout=60)
        d = json.load(req(API + "?" + q))
        url = next(iter(d["query"]["pages"].values()))["imageinfo"][0]["url"]
        p.write_bytes(req(url).read())
    return p


def frame_zone(painted: bool = True):
    """The bare frame on the master, and the zone render.starship_frame paints (no icon boxes, no grown text)."""
    fa = np.array(Image.open(ROOT / "assets/frames/loc-site.png").convert("RGBA")).astype(float)
    H, W = fa.shape[:2]
    keep = np.zeros((H, W), bool)
    m = 4
    for x0, y0, x1, y1 in ((163, 1135, 444, 1252), (440, 1135, 1576, 1252), (163, 1252, 1900, 1370),
                           (163, 106, 1900, 225), (489, 225, 1634, 336), (1630, 225, 1900, 336)):
        keep[max(0, y0 - m):y1 + m, max(0, x0 - m):x1 + m] = True
    rgb = fa[:, :, :3]
    silver = (np.abs(rgb[:, :, 0] - rgb[:, :, 2]) < 30) & (rgb.mean(2) > 80) & (fa[:, :, 3] > 0)
    zone = silver & ~keep
    ref = np.zeros((MH, MW, 3), np.uint8)
    a = fa[:, :, 3:] / 255.0
    paint = rgb * a
    if painted:   # the blue sites: the zone painted, as printed (make_site_scanboxes.py also registers silver sites)
        paint[zone] = rgb[zone].mean(-1, keepdims=True) / 172.0 * np.array([33.0, 95.0, 140.0])
    ref[FY:FY + H, FX:FX + W] = np.clip(paint, 0, 255).astype(np.uint8)
    # registration mask: the whole card body and its edge on the black border, but not the picture
    msk = np.zeros((MH, MW), np.uint8)
    msk[FY + 68 - 40:FY + 1410 + 40, FX + 70 - 40:FX + 2000 + 40] = 1
    msk[FY + 382 + 12:FY + 1095 - 12, FX + 188 + 12:FX + 1883 - 12] = 0
    return ref, msk, zone


def bbox_blue(a):
    a = a.astype(int)
    blue = (a[:, :, 2] - a[:, :, 0]) > 25
    if (blue.mean(1) > 0.25).sum() < 50:   # a silver site: the card body (neither the black border nor the white scan ground)
        m = a.mean(-1); blue = (m > 55) & (m < 238)
    r = np.where(blue.mean(1) > 0.25)[0]; c = np.where(blue.mean(0) > 0.25)[0]
    return c[0], r[0], c[-1] + 1, r[-1] + 1


def gray(a, s):
    return cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255, (0, 0), s)


def register(path: Path, ref, msk, zone, rots):
    """The printed face warped onto the master, in the frame's orientation (best of the given turns)."""
    im = Image.open(path).convert("RGB")
    if im.height > im.width:
        im = im.rotate(-90, expand=True)
    bo = (FX + 70, FY + 68, FX + 2000, FY + 1410)   # the frame's body (alpha bounds) = where the printed blue starts
    best = None
    for rot in rots:
        p = np.array(im.rotate(rot)) if rot else np.array(im)
        pr = cv2.resize(p, (MW, MH), interpolation=cv2.INTER_AREA if p.shape[1] > MW else cv2.INTER_CUBIC)
        bp = bbox_blue(pr)
        sx = (bp[2] - bp[0]) / (bo[2] - bo[0]); sy = (bp[3] - bp[1]) / (bo[3] - bo[1])
        M0 = np.array([[sx, 0, bp[0] - sx * bo[0]], [0, sy, bp[1] - sy * bo[1]]], np.float32)
        # two schedules (affine from the start / translation first); a sheared result is a failed fit
        for sched in (((0.25, 3.0, cv2.MOTION_AFFINE), (0.5, 1.5, cv2.MOTION_AFFINE)),
                      ((0.25, 3.0, cv2.MOTION_TRANSLATION), (0.5, 1.5, cv2.MOTION_TRANSLATION), (0.5, 1.5, cv2.MOTION_AFFINE))):
            M, cc = M0.copy(), -1.0
            for S, sig, mot in sched:
                o = cv2.resize(ref, None, fx=S, fy=S, interpolation=cv2.INTER_AREA)
                q = cv2.resize(pr, (o.shape[1], o.shape[0]), interpolation=cv2.INTER_AREA)
                mm = cv2.resize(msk, (o.shape[1], o.shape[0]), interpolation=cv2.INTER_NEAREST)
                w = M.copy(); w[:, 2] *= S
                try:
                    cc, w = cv2.findTransformECC(gray(o, sig), gray(q, sig), w, mot,
                                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 500, 1e-7), mm, 1)
                    M = w.copy(); M[:, 2] /= S
                except cv2.error:
                    cc = -1.0
            if abs(M[0, 1]) > 0.02 or abs(M[1, 0]) > 0.02 or abs(M[0, 0] / M[1, 1] - sx / sy) > 0.05:
                cc = -1.0
            if best is None or cc > best[0]:
                best = (cc, rot, M, pr)
    cc, rot, M, pr = best
    reg = cv2.warpAffine(pr, M, (MW, MH), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    print(f"  {path.name}: ECC {cc:.3f}, turned {rot}, scale {M[0, 0]:.3f} x {M[1, 1]:.3f}")
    Image.fromarray(reg).save(CACHE / f"registered-{path.stem}.png")   # for checking against the frame
    return reg[FY:FY + zone.shape[0], FX:FX + zone.shape[1]].astype(np.float32)


def classify(face, zone):
    """1 = blue paint, 0 = silver, nan = neither (ink: copyright line, sphere, icons). Thresholds from the face's own
    zone (Otsu on blue - red), as the scans' colour differs (archive images are more saturated than the hi-res)."""
    r, b = face[:, :, 0], face[:, :, 2]
    lum = face.mean(-1)
    bl = np.clip(b - r, 0, 255).astype(np.uint8)
    t, _ = cv2.threshold(bl[zone & (lum > 50)].reshape(-1, 1), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    paint = bl > t
    silver_lum = np.median(lum[zone & ~paint & (lum > 60)])
    silver = ~paint & (lum > 0.6 * silver_lum)
    ink = cv2.dilate((~paint & ~silver).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    out = np.where(paint, 1.0, 0.0).astype(np.float32)
    out[ink & ~paint] = np.nan
    out[~zone] = np.nan
    return out, paint


def main():
    ref, msk, zone = frame_zone()
    print("Light faces:")
    L = [classify(register(fetch(n), ref, msk, zone, (0, 180)), zone)[0] for n in LIGHT]
    med = np.nanmedian(np.stack(L), 0)
    wear = zone & (np.nan_to_num(med, nan=1.0) < 0.5)
    Image.fromarray((wear * 255).astype(np.uint8), "L").save(ROOT / "assets/frames/site-wear-light.png", optimize=True)
    print(f"  worn: {wear.sum() / zone.sum():.3f} of the paint zone")


if __name__ == "__main__":
    main()
