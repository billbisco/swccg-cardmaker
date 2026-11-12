"""Rev 81 (site wear and PC wide starships): the Episode VII disc as the PC printed it on its blue landscape Finalizer
and Finalizer (AI): a broad blue ring (assets/icons/ep7-disc.png has a thin silver one) -> assets/icons/ep7-disc-blue.png.

The ring's radial colour profile is measured on the two printed faces (wiki V4-D-finalizer.gif, V4-D-finalizer_ai.gif,
745 px; disc centre (90, 203), outer radius 20.5 px: dark inside r 12, blue r 13-18 peaking (35, 84, 122) at r 16, dark
edge) and laid on the disc outside 0.6 of its radius; the VII, "EPISODE" and the black field inside stay as they are.
Usage: python3 tools/make_ep7_disc_blue.py [scan_dir]   (the two faces, default out/site-wear-scans; fetched if missing)"""
import json, sys, urllib.parse, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "out" / "site-wear-scans")
FACES = ["V4-D-finalizer.gif", "V4-D-finalizer_ai.gif"]
CX, CY, R = 90.0, 203.0, 20.5


def fetch(name):
    p = CACHE / name
    if not p.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        q = urllib.parse.urlencode({"action": "query", "titles": "File:" + name, "prop": "imageinfo", "iiprop": "url", "format": "json"})
        get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "cardmaker-tools/1.0"}), timeout=60)
        url = next(iter(json.load(get("https://wiki.swccg.com/api.php?" + q))["query"]["pages"].values()))["imageinfo"][0]["url"]
        p.write_bytes(get(url).read())
    return p


# printed radial profile, 0.25 px bins, averaged over the two faces (all angles)
rs = np.arange(0, R + 0.5, 0.25)
prof = np.zeros((len(rs), 3))
for f in FACES:
    a = np.array(Image.open(fetch(f)).convert("RGB")).astype(float)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    r = np.hypot(xx - CX, yy - CY)
    for i, r0 in enumerate(rs):
        m = (r >= r0 - 0.5) & (r < r0 + 0.5)
        prof[i] += a[m].mean(0) / len(FACES)
d = np.array(Image.open(ROOT / "assets/icons/ep7-disc.png").convert("RGBA")).astype(float)
h, w = d.shape[:2]
yy, xx = np.mgrid[0:h, 0:w]
rr = np.hypot(xx - (w - 1) / 2, yy - (h - 1) / 2) / (w / 2) * R      # the asset's radius in printed px
ring = rr >= 0.6 * R
col = np.stack([np.interp(rr, rs, prof[:, k]) for k in range(3)], -1)
d[:, :, :3] = np.where(ring[:, :, None], col, d[:, :, :3])
Image.fromarray(d.round().clip(0, 255).astype(np.uint8), "RGBA").save(ROOT / "assets/icons/ep7-disc-blue.png", optimize=True)
k = np.argmax(np.where(rs > 10, prof[:, 2], 0)); print("ring peak", prof[k].round(), "at r", rs[k])
