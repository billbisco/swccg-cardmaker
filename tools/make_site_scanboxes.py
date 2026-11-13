"""Rev 84 (sites 2): the Mobile, Starship and Vehicle icon boxes of Decipher's location cards, cut from printed faces ->
assets/loc/scanbox-{mobile,starship,vehicle}.png (100 x 94, as scanbox-interior / -exterior / -planet / -underground,
which were cut from the printed Hoth cards).

These three were drawn as the Holotable icon (icon-*.png, its own brown speckled border) on box.png: a brown-speckled
box, 10 px too large and 3-8 px off, unlike the print's thin dark line inside the silver rim. Each printed hi-res face
(wiki, 2073 px) is registered to the site frame as in make_site_wear.py; every box of the wanted kinds is located from
where the renderer puts it (frame x 1805 - 111 k, y 1148 for the half at the bottom; the top half turned): the square
boxes of the row are matched by scanbox-interior.png's rim (+-24 px) and the row fitted (x0 - pitch k, y), which places the
round mobile disc too (the rim match alone mistakes it); the boxes of one kind are averaged by per-pixel median.
Faces: Executor: Comm Station / Control Station / Holotheatre / Main Corridor / Meditation Chamber (mobile, starship),
Death Star: Docking Bay 327, Death Star: Central Core, Death Star: War Room (mobile), Sandcrawler: Loading Bay /
Droid Junkheap (vehicle). Usage: python3 tools/make_site_scanboxes.py [scan_dir]"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import make_site_wear as W   # noqa: E402  (fetch, frame_zone, register; its CACHE follows argv[1] too)

# face file -> (painted frame, the card's location icons outermost first: the same list for both halves)
FACES = {
    "Dagobah-D-executorcommstation-hires.webp": (True, ["scomp", "mobile", "starship", "interior"]),
    "Dagobah-D-executorcontrolstation-hires.webp": (True, ["scomp", "mobile", "starship", "interior"]),
    "Dagobah-D-executorholotheatre-hires.webp": (True, ["scomp", "mobile", "starship", "interior"]),
    "Dagobah-D-executormaincorridor-hires.webp": (True, ["scomp", "mobile", "starship", "interior"]),
    "Dagobah-D-executormeditationchamber-hires.webp": (True, ["scomp", "mobile", "starship", "interior"]),
    "Premiere-D-deathstardockingbay327-hires.webp": (False, ["scomp", "mobile", "exterior", "interior"]),
    "Premiere-D-deathstarcentralcore-hires.webp": (False, ["scomp", "mobile", "interior"]),
    "Premiere-D-deathstarwarroom-hires.webp": (False, ["scomp", "mobile", "interior"]),
    "ANH-L-sandcrawlerloadingbay-hires.webp": (True, ["vehicle", "interior"]),
    "ANH-D-sandcrawlerdroidjunkheap-hires.webp": (True, ["vehicle", "interior"]),
}
WANT = ("mobile", "starship", "vehicle")
S = 24   # search radius (px) round the renderer's box position


def main():
    tpl = np.array(Image.open(ROOT / "assets/loc/scanbox-interior.png").convert("L")).astype(np.float32)
    rim = np.ones_like(tpl, np.uint8); rim[12:-12, 12:-12] = 0     # match on the silver rim and the dark line only
    got = {k: [] for k in WANT}
    refs = {p: W.frame_zone(p) for p in (True, False)}
    for name, (painted, icons) in FACES.items():
        ref, msk, zone = refs[painted]
        f = W.register(W.fetch(name), ref, msk, zone, (0, 180)).clip(0, 255).astype(np.uint8)   # frame orientation
        for half in ("bottom", "top"):
            img = f if half == "bottom" else np.ascontiguousarray(f[::-1, ::-1])   # the top half turned upright
            g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
            # the box positions in the print: match the rim of every box of the row, keep the reliable ones (the square
            # pictures; the round mobile disc and the scomp ring fool the rim match), and fit the row (x0 + pitch k, y)
            pos = {}
            for k, nm in enumerate(icons):
                if nm == "scomp":
                    continue
                x, y = 1805 - 111 * k, 1148
                win = g[y - S:y + 94 + S, x - S:x + 100 + S]
                r = cv2.matchTemplate(win, tpl, cv2.TM_CCORR_NORMED, mask=rim)
                _, sc, _, (dx, dy) = cv2.minMaxLoc(r)
                if nm != "mobile" and abs(dx - S) < S and abs(dy - S) < S:
                    pos[k] = (x - S + dx, y - S + dy)
            if not pos:
                continue
            ks = sorted(pos)
            pitch = (pos[ks[0]][0] - pos[ks[-1]][0]) / (ks[-1] - ks[0]) if len(ks) > 1 else 111.0
            k0 = ks[0]; X0, Y0 = pos[k0][0] + pitch * k0, float(np.mean([p[1] for p in pos.values()]))
            for k, nm in enumerate(icons):
                if nm not in WANT:
                    continue
                bx, by = int(round(X0 - pitch * k)), int(round(Y0))
                print(f"  {name} {half} {nm}: box at ({bx - (1805 - 111 * k):+d}, {by - 1148:+d}) from ours, row pitch {pitch:.1f}")
                got[nm].append(img[by:by + 94, bx:bx + 100].astype(np.float32))
    ring = np.zeros((94, 100), bool); ring[:5] = ring[-5:] = True; ring[:, :5] = ring[:, -5:] = True
    ref_rim = np.median(np.array(Image.open(ROOT / "assets/loc/scanbox-interior.png").convert("RGB")).astype(np.float32)[ring], 0)
    for nm, lst in got.items():
        # the hi-res scans are duller than the faces the other scanboxes came from: each crop's channels scaled so its
        # silver rim (outer 5 px) matches scanbox-interior's; then every crop aligned (ECC, translation) on the first
        # median and the median taken again
        lst = [np.clip(c * (ref_rim / np.maximum(np.median(c[ring], 0), 1)), 0, 255) for c in lst]
        med = np.median(np.stack(lst), 0)
        al = []
        for c in lst:
            w = np.eye(2, 3, dtype=np.float32)
            try:
                _, w = cv2.findTransformECC(cv2.cvtColor(med.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32),
                                            cv2.cvtColor(c.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32), w,
                                            cv2.MOTION_TRANSLATION, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-5), None, 3)
            except cv2.error:
                pass
            if abs(w[0, 2]) < 12 and abs(w[1, 2]) < 12:
                al.append(np.clip(cv2.warpAffine(c, w, (100, 94), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE), 0, 255))
        med = np.median(np.stack(al), 0)
        Image.fromarray(np.dstack([med, np.full(med.shape[:2], 255.0)]).round().clip(0, 255).astype(np.uint8), "RGBA").save(
            ROOT / f"assets/loc/scanbox-{nm}.png", optimize=True)
        print(nm, len(al), "of", len(lst), "boxes aligned")


if __name__ == "__main__":
    main()
