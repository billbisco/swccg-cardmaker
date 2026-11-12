#!/usr/bin/env python3
"""Japanese printing vs CardMaker (STANDARD rev 77): render each sample spec and set it beside the wiki's Japanese scan.

  python3 tools/japanese/compare_ja.py [samples/*.json] --out <dir>

Each sample is an editor spec with `language: "ja"` plus `_scan` (the wiki File name of the printed face) and optional
`_scan_bounds` (x0,y0,x1,y1 of the frame's outer edge in the scan when the slab or a light frame defeats detection,
or "bars": a location is mapped by its two bars onto the render's).
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
    b = edge(colk, 0, w // 3, 1), edge(rowk, 0, h // 4, 1), edge(colk, w - 1, 2 * w // 3, -1), edge(rowk, h - 1, 3 * h // 4, -1)
    try:
        c = frame_bounds_inside(a)
        if None not in c and 1.40 < (c[3] - c[1]) / (c[2] - c[0]) < 1.48:
            return c
    except TypeError:
        pass
    return b


def frame_bounds_inside(a):
    """Slabbed / photographed scans (PSA, BGS holders): walk out from the card's middle to the first column / row that
    is black from end to end (the border inside the frame's outer edge). Columns are judged on the middle rows; rows on
    a narrow band just inside the frame's left side bar (the lore and text boxes are black across the middle)."""
    h, w = a.shape
    def walk(fr, start, stop, step):
        for i in range(start, stop, step):
            if fr[i] > 0.8 and fr[i + step] > 0.8:
                return i - step
        return None
    colk = (a[int(h * .35):int(h * .65)] < 50).mean(0)
    def side(start, stop, step):   # from inside the frame's side bar outward: first frame-coloured column, then the border
        seen = False
        for i in range(start, stop, step):
            if colk[i] < 0.15: seen = True
            elif seen and colk[i] > 0.85 and colk[i + step] > 0.85: return i - step
        return None
    x0, x1 = side(int(w * .2), 1, -1), side(int(w * .8), w - 2, 1)
    cw = x1 - x0
    rowk = (a[:, x0 + int(cw * .008):x0 + int(cw * .025)] < 50).mean(1)
    rowk2 = (a[:, x1 - int(cw * .025):x1 - int(cw * .008)] < 50).mean(1)
    rk = np.minimum(rowk, rowk2)
    return x0, walk(rk, h // 2, 1, -1), x1, walk(rk, h // 2, h - 2, 1)


def bars_box(im: Image.Image):
    """A location's two bars (light grey) bound the printed layout: (x0, y0, x1, y1) of the bright rows / columns in
    the top and bottom thirds. Used for systems, whose starfield runs into the black border (no frame edge to find)."""
    a = np.asarray(im.convert("L")).astype(float); h, w = a.shape
    br = a > 150
    rows = br.mean(1) > 0.3
    def longest(lo, hi):   # the longest run of bright rows (text box + bar), not a slab's edge
        best, cur = (0, 0), None
        for i in range(lo, hi):
            if rows[i] and cur is None: cur = i
            if (not rows[i] or i == hi - 1) and cur is not None:
                best = max(best, (i - cur, cur)); cur = None
        return best[1], best[1] + best[0]
    t0, t1 = longest(int(h * .02), int(h * .4)); b0, b1 = longest(int(h * .6), int(h * .98))
    cols = br[np.r_[t0:t1, b0:b1]].mean(0) > 0.5
    xs = np.where(cols)[0]
    return xs.min(), t0, xs.max(), b1


def warp(scan: Path, bounds=None, ref: Image.Image | None = None) -> Image.Image:
    if isinstance(bounds, dict) or (bounds == "bars" and ref is not None):   # map the scan's bars onto the render's bars
        im = Image.open(scan).convert("RGB")   # {"scan": [x0, y0, x1, y1], "ref": [...]}: the two text boxes' outer edges, read by hand
        sx0, sy0, sx1, sy1 = bounds["scan"] if isinstance(bounds, dict) else bars_box(im)
        rx0, ry0, rx1, ry1 = bounds["ref"] if isinstance(bounds, dict) else bars_box(ref)
        kx, ky = (rx1 - rx0) / (sx1 - sx0), (ry1 - ry0) / (sy1 - sy0)
        out = Image.new("RGB", (1632, 2220)); out.paste(im.resize((round(im.width * kx), round(im.height * ky)), Image.LANCZOS), (round(rx0 - sx0 * kx), round(ry0 - sy0 * ky)))
        return out
    im = Image.open(scan).convert("RGB"); x0, y0, x1, y1 = bounds or frame_bounds(im)
    X0, Y0, X1, Y1 = 146, 145, 1484, 2073   # the frame's outer edge in a portrait render
    sx, sy = (X1 - X0) / (x1 - x0), (Y1 - Y0) / (y1 - y0)
    out = Image.new("RGB", (1632, 2220)); out.paste(im.resize((round(im.width * sx), round(im.height * sy)), Image.LANCZOS), (round(X0 - x0 * sx), round(Y0 - y0 * sy)))
    return out


def render(spec: dict, cache: Path) -> Image.Image:
    import render as R, build_vs, adapter
    gid = (spec.get("art") or {}).get("gempId") or spec.get("gempId")
    s = {k: v for k, v in spec.items() if not k.startswith("_")}
    if (spec.get("art") or {}).get("kind", "library") != "library":   # a system's picture is the whole scan: the server's own route
        import server
        s.update(_art=server.resolve_art(s), _art_kind=spec["art"]["kind"], _set_icon_file=None)
    else:
        art = cache / f"art-{gid}.png"
        if not art.exists():
            art.write_bytes(urllib.request.urlopen(urllib.request.Request(f"https://raw.githubusercontent.com/billbisco/swccg-card-art/main/decipher/orig/{gid}.png", headers=UA), timeout=60).read())
        w, h = Image.open(art).size
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
    ap.add_argument("--full", action="store_true", help="also save the warped scan and the render at full size (measuring)")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True); os.environ.setdefault("CARDMAKER_OUT", str(out))
    for f in a.specs:
        spec = json.loads(Path(f).read_text(encoding="utf-8")); name = Path(f).stem
        ours = render(spec, out)
        try:
            scan = warp(wiki_file(spec["_scan"], out / spec["_scan"]), spec.get("_scan_bounds"), ours)
        except Exception as e:   # noqa: BLE001 - one bad scan (frame not found) must not stop the batch
            print(name, "-> scan not usable:", e, "(set _scan_bounds, or \"bars\" for a location)"); continue
        if a.full:
            scan.save(out / f"{name}-scanw.png"); ours.save(out / f"{name}-ours.png")
        sheet = Image.new("RGB", (1632 * 2 + 10, 2220), "white"); sheet.paste(scan, (0, 0)); sheet.paste(ours, (1642, 0))
        sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(out / f"{name}-sheet.png")
        for part, box in (("top", (140, 140, 1500, 640)), ("bottom", (140, 1440, 1500, 2090))):
            x, y = scan.crop(box), ours.crop(box); c = Image.new("RGB", (x.width, x.height * 2 + 6), "red")
            c.paste(x, (0, 0)); c.paste(y, (0, x.height + 6)); c.save(out / f"{name}-{part}.png")
        print(name, "->", out / f"{name}-sheet.png")


if __name__ == "__main__":
    main()
