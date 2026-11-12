"""Rev 81 (sites 2): the Nav Computer icon box as printed -> assets/icons/col-nav.png (89 x 90, the box size of the
other col-* icons, drawn in the icon slots without icon-box.png).

The renderer drew the in-text icon (inline-nav.png: R2-D2 small, inside a grey inner frame) inside icon-box.png, a
double frame no printing shows: Decipher (Executor) and the PC (Ghost, Azure Angel, Blue Squadron 1, Bright Hope,
Finalizer) print the red field to a thin silver rim, R2-D2's dome filling its lower half.
The box is cut from five PC faces (GEMP 745 px gifs, all the same art): the red field located (R > 190, R - G > 110),
the box = the field + 4.5 px left / 3.5 px up / 3.5 px right / 5 px down (43 x 41.5 px at 745, rim included), each crop
scaled to 89 x 90 and the per-pixel median taken.
Usage: python3 tools/make_col_nav.py [scan_dir]   (default out/site-wear-scans; fetched from the PC's image server)"""
import sys, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "out" / "site-wear-scans")
FACES = {"ghost.gif": "Virtual7-Light", "azureangel.gif": "Virtual2-Light", "bluesquadron1.gif": "Virtual10-Light",
         "brighthope.gif": "Virtual3-Light", "finalizer.gif": "Virtual4-Dark"}
crops = []
for name, d in FACES.items():
    p = CACHE / name
    if not p.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        p.write_bytes(urllib.request.urlopen(f"https://res.starwarsccg.org/cards/{d}/large/{name}", timeout=60).read())
    im = Image.open(p).convert("RGB"); a = np.array(im).astype(int)
    red = (a[:, :, 0] > 190) & (a[:, :, 0] - a[:, :, 1] > 110) & (a[:, :, 2] < 110)
    lab, _ = ndimage.label(ndimage.binary_closing(red, iterations=2))
    boxes = [s for s in ndimage.find_objects(lab) if 32 <= s[1].stop - s[1].start <= 38 and 31 <= s[0].stop - s[0].start <= 36]
    assert len(boxes) == 1, (name, boxes)
    y0, x0 = boxes[0][0].start, boxes[0][1].start
    crops.append(np.array(im.transform((89, 90), Image.EXTENT, (x0 - 4.5, y0 - 3.5, x0 + 38.5, y0 + 38), Image.BICUBIC)).astype(float))
med = np.median(np.stack(crops), 0)
out = np.dstack([med, np.full(med.shape[:2], 255.0)])
Image.fromarray(out.round().clip(0, 255).astype(np.uint8), "RGBA").save(ROOT / "assets/icons/col-nav.png", optimize=True)
print(len(crops), "faces")
