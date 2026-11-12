#!/usr/bin/env python3
"""Japanese printing vs CardMaker (STANDARD rev 77): render each sample spec and set it beside the wiki's Japanese scan.

  python3 tools/japanese/compare_ja.py [samples/*.json] --out <dir>

Each sample is an editor spec with `language: "ja"` plus `_scan` (the wiki File name of the printed face) and optional
`_scan_bounds` (x0,y0,x1,y1 of the frame's outer edge in the scan when the slab or a light frame defeats detection).
The scan is warped into the 1632x2220 master by the frame edges (the card's black border inside edge), so pieces line up
pixel for pixel with the render. Output per card: <name>-sheet.png (scan | render) and <name>-top.png / -bottom.png
(the lore / stat / text areas, scan above render). Art: the library art (English crop); Takara's shows ~4 % more.
"""
import argparse, json, os, sys, urllib.parse, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "webapp")]
UA = {"User-Agent": "swccg-cardmaker compare_ja"}


def wiki_file(name: str, dest: Path) -> Path:
    if dest.exists():
        return dest
    q = urllib.parse.urlencode({"action": "query", "titles": "File:" + name, "prop": "imageinfo", "iiprop": "url", "format": "json"})
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://wiki.swccg.com/api.php?" + q, headers=UA), timeout=60))
    url = list(d["query"]["pages"].values())[0]["imageinfo"][0]["url"]
    dest.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read())
    return dest


def frame_bounds(im: Image.Image):
    """Inner edge of the card's black border (the frame's outer edge)."""
    a = np.asarray(im.convert("L")).astype(float); h, w = a.shape
    colk = (a[int(h * .25):int(h * .75)] < 60).mean(0); rowk = (a[:, int(w * .3):int(w * .7)] < 60).mean(1)
    def edge(fr, lo, hi, step):
        best = None
        for i in range(lo, hi, step):
            if fr[i] > 0.8: best = i
            elif best is not None and fr[i] < 0.3: return best + step
        return best
    return edge(colk, 0, w // 3, 1), edge(rowk, 0, h // 4, 1), edge(colk, w - 1, 2 * w // 3, -1), edge(rowk, h - 1, 3 * h // 4, -1)


def warp(scan: Path, bounds=None) -> Image.Image:
    im = Image.open(scan).convert("RGB"); x0, y0, x1, y1 = bounds or frame_bounds(im)
    X0, Y0, X1, Y1 = 146, 145, 1484, 2073   # the frame's outer edge in a portrait render
    sx, sy = (X1 - X0) / (x1 - x0), (Y1 - Y0) / (y1 - y0)
    out = Image.new("RGB", (1632, 2220)); out.paste(im.resize((round(im.width * sx), round(im.height * sy)), Image.LANCZOS), (round(X0 - x0 * sx), round(Y0 - y0 * sy)))
    return out


def render(spec: dict, cache: Path) -> Image.Image:
    import render as R, build_vs, adapter
    gid = (spec.get("art") or {}).get("gempId") or spec.get("gempId")
    art = cache / f"art-{gid}.png"
    if not art.exists():
        art.write_bytes(urllib.request.urlopen(urllib.request.Request(f"https://raw.githubusercontent.com/billbisco/swccg-card-art/main/decipher/orig/{gid}.png", headers=UA), timeout=60).read())
    w, h = Image.open(art).size
    s = {k: v for k, v in spec.items() if not k.startswith("_")}
    s.update(_art={"src": str(art), "rect": [0, 0, w, h]}, _art_kind="library", _set_icon_file=None)
    card = adapter.spec_to_card(s, build_vs)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1632, "height": 2220})
        im = R.screenshot_card(card, pg); b.close()
    return im.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="*", default=sorted(str(p) for p in (Path(__file__).parent / "samples").glob("*.json")))
    ap.add_argument("--out", default="out/japanese")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True); os.environ.setdefault("CARDMAKER_OUT", str(out))
    for f in a.specs:
        spec = json.loads(Path(f).read_text(encoding="utf-8")); name = Path(f).stem
        scan = warp(wiki_file(spec["_scan"], out / spec["_scan"]), spec.get("_scan_bounds"))
        ours = render(spec, out)
        sheet = Image.new("RGB", (1632 * 2 + 10, 2220), "white"); sheet.paste(scan, (0, 0)); sheet.paste(ours, (1642, 0))
        sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(out / f"{name}-sheet.png")
        for part, box in (("top", (140, 140, 1500, 640)), ("bottom", (140, 1440, 1500, 2090))):
            x, y = scan.crop(box), ours.crop(box); c = Image.new("RGB", (x.width, x.height * 2 + 6), "red")
            c.paste(x, (0, 0)); c.paste(y, (0, x.height + 6)); c.save(out / f"{name}-{part}.png")
        print(name, "->", out / f"{name}-sheet.png")


if __name__ == "__main__":
    main()
