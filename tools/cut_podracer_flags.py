"""Cut the Episode I Podracer pilot flags (Tatooine 11_47, 11_95-98) from the wiki's Decipher archive scans.

Source: wiki.swccg.com File:Tat-{L,D}-<name>-decipher-archive.jpg (497x692; card body 24..471 x 24..669, so
master px = 144 + (scan - 24) * 3). The flag sits in a recessed window right of the round podracer-engine icon:
inner window scan x 98..160, y 37..85 (62 x 48) on the Dark cards -> master 366..552 x 183..327; on the Light card
(Anakin's, silver bar) x 95..158, y 34..85 -> master 357..546 x 174..327.
(The Holotable faces the server uses are 350x490, lower resolution, so the wiki scans are the source.)
Each window is upscaled 6x (Lanczos + a light unsharp mask), i.e. ~2x the master size.
Run: python3 tools/cut_podracer_flags.py  -> assets/icons/podracer-flag-<slug>.png
"""
import io, json, sys, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
FLAGS = {   # slug: (wiki scan, inner window x0, y0, x1, y1 on the scan: the sky-blue picture inside the bevel)
    "anakin": ("Tat-L-anakinspodracer-decipher-archive.jpg", (95, 34, 158, 85)),   # Light bar: the window sits 3 px up-left
    "sebulba": ("Tat-D-sebulbaspodracer-decipher-archive.jpg", (99, 39, 159, 84)),
    "ben-quadinaros": ("Tat-D-benquadinarospodracer-decipher-archive.jpg", (98, 37, 160, 85)),
    "dud-bolt": ("Tat-D-dudboltspodracer-decipher-archive.jpg", (98, 37, 160, 85)),
    "teemto-pagalies": ("Tat-D-teemtopagaliespodracer-decipher-archive.jpg", (98, 37, 160, 85)),
}
UA = {"User-Agent": "swccg-cardmaker/1.0"}


def scan(name):
    q = urllib.parse.urlencode({"action": "query", "titles": "File:" + name, "prop": "imageinfo", "iiprop": "url", "format": "json"})
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://wiki.swccg.com/api.php?" + q, headers=UA), timeout=30))
    url = next(iter(d["query"]["pages"].values()))["imageinfo"][0]["url"]
    return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())).convert("RGB")


def cut(im, window):
    assert im.size == (497, 692), im.size
    w = im.crop(window)
    big = w.resize((w.width * 6, w.height * 6), Image.LANCZOS)
    return big.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2))


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else None   # optional folder holding the scans already
    for slug, (name, window) in FLAGS.items():
        im = Image.open(src / name).convert("RGB") if src and (src / name).exists() else scan(name)
        out = ROOT / "assets" / "icons" / f"podracer-flag-{slug}.png"
        cut(im, window).save(out, optimize=True); print("wrote", out)
