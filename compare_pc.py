#!/usr/bin/env python3
"""compare_pc.py: rebuild a PC card in CardMaker and measure it against the PC's own image (swccg-guild/work#51).

    python3 compare_pc.py "A New Hope"                 # one card: title or gempId (227_4)
    python3 compare_pc.py --batch cards.txt --sheet    # one card per line, plus a contact sheet
    python3 compare_pc.py 1100_2 --ref slip.png        # compare against another reference image (745x1039)

CardMaker is driven through its own web API, the path the live editor uses:
  GET  /api/card/<gempId>   spec from the PC card JSON (+ corrections.json), art = the card's own PC scan
  POST /api/render          745x1039 build + every element's box (X-Piece-Boxes)
The reference is the PC's 745x1039 hires PNG (holotable copy, else res.starwarsccg.org).

Per card it writes <out>/<gempId>/: pc.png, build.png, overlay.png (50 %), diff.png (|build-pc|, x4), side.png,
report.md and report.json. For each element box the report gives the best integer offset (dx, dy) of the build
against the PC image within +-SEARCH px, the ink-box size change (dw, dh), the mean absolute difference after that
alignment (MAD, 0-255), the share of pixels that differ by more than 40 levels, and the mean colour difference
(CIE76 dE). Nothing is thresholded away: every element with any difference is reported, so each one can be fixed,
logged as an approved deviation (docs/design-log/48-deviations.md) or explained (Epic #48, Bill 2026-11-03).
"frame" is everything outside the element boxes and the art window.
"""
from __future__ import annotations
import argparse, io, json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

SEARCH = 10         # px, offset search radius for each element (a result at the limit is flagged)
INK_DELTA = 40      # levels: "differs" for the changed-pixel share
UA = {"User-Agent": "swccg-cardmaker-compare/1.0"}


def http(url, data=None, timeout=180):
    req = urllib.request.Request(url, json.dumps(data).encode() if data is not None else None,
                                 {**UA, "Content-Type": "application/json"} if data is not None else UA)
    return urllib.request.urlopen(req, timeout=timeout)


def resolve(api, q):
    if re.fullmatch(r"\d+[a-z]?_\w+", q):
        return q
    hits = json.load(http(f"{api}/api/search?q={urllib.parse.quote(q)}&limit=20"))
    exact = [h for h in hits if h["title"].replace("•", "").strip().lower() == q.replace("•", "").strip().lower()]
    if not (exact or hits):
        raise SystemExit(f"no card found for {q!r}")
    return (exact or hits)[0]["gempId"]


def ref_image(spec, holotable, ref):
    if ref:
        return Image.open(ref).convert("RGB"), str(ref)
    src = spec.get("source")
    u = src.get("imageUrl") if isinstance(src, dict) else (re.search(r"imageUrl.{0,4}'([^']+)'", str(src or "")) or [None, None])[1]
    if not u:
        raise ValueError("spec has no PC imageUrl; pass --ref")
    url = re.sub(r"/large/(.+)\.gif$", r"/hires/\1.png", u)
    rel = url.split("/cards/", 1)[1]
    p = Path(holotable) / rel if holotable else None
    if p and p.exists():
        return Image.open(p).convert("RGB"), str(p)
    return Image.open(io.BytesIO(http(url).read())).convert("RGB"), url


def lab(a):
    """sRGB uint8 (..., 3) -> CIE Lab (D65)."""
    c = a.astype(np.float64) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    xyz = c @ np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]).T
    xyz /= np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def ink_box(g, bg):
    m = np.abs(g - bg) > INK_DELTA
    ys, xs = np.where(m)
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else None


def measure(B, P, box, W, H):
    """B, P: float RGB arrays. box: x, y, w, h (745 px). Returns the element's row."""
    x, y, w, h = [int(round(v)) for v in box]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return None
    gB, gP = B.mean(2), P.mean(2)
    best = None
    for dy in range(-SEARCH, SEARCH + 1):
        for dx in range(-SEARCH, SEARCH + 1):
            sx0, sy0, sx1, sy1 = x0 + dx, y0 + dy, x1 + dx, y1 + dy
            if sx0 < 0 or sy0 < 0 or sx1 > W or sy1 > H:
                continue
            mad = float(np.abs(gB[y0:y1, x0:x1] - gP[sy0:sy1, sx0:sx1]).mean())
            if best is None or mad < best[0] - 1e-9 or (abs(mad - best[0]) <= 1e-9 and abs(dx) + abs(dy) < abs(best[1]) + abs(best[2])):
                best = (mad, dx, dy)
    mad, dx, dy = best
    b = B[y0:y1, x0:x1]; p = P[y0 + dy:y1 + dy, x0 + dx:x1 + dx]
    bgB = np.median(gB[y0:y1, x0:x1]); bgP = np.median(gP[y0 + dy:y1 + dy, x0 + dx:x1 + dx])
    ib, ip = ink_box(gB[y0:y1, x0:x1], bgB), ink_box(gP[y0 + dy:y1 + dy, x0 + dx:x1 + dx], bgP)
    dw = dh = None
    if ib and ip:
        dw, dh = int((ib[2] - ib[0]) - (ip[2] - ip[0])), int((ib[3] - ib[1]) - (ip[3] - ip[1]))
    z0 = np.abs(gB[y0:y1, x0:x1] - gP[y0:y1, x0:x1])
    de = float(np.linalg.norm(lab(b) - lab(p), axis=-1).mean())
    return dict(box=[x0, y0, x1 - x0, y1 - y0], dx=-dx, dy=-dy, dw=dw, dh=dh, mad=round(mad, 2),
                changed_pct=round(float((z0 > INK_DELTA).mean() * 100), 2), dE=round(de, 2))


def frame_row(B, P, boxes, W, H):
    mask = np.ones((H, W), bool)
    for x, y, w, h in boxes:
        mask[max(0, int(y)):int(y + h), max(0, int(x)):int(x + w)] = False
    d = np.abs(B.mean(2) - P.mean(2))
    de = np.linalg.norm(lab(B[mask]) - lab(P[mask]), axis=-1)
    return dict(box=None, dx=None, dy=None, dw=None, dh=None, mad=round(float(d[mask].mean()), 2),
                changed_pct=round(float((d[mask] > INK_DELTA).mean() * 100), 2), dE=round(float(de.mean()), 2))


def compare(api, q, out, holotable=None, ref=None, build=None, boxes_file=None):
    if build and boxes_file and ref:   # offline: a finished CardMaker image, its element boxes and a reference
        gid, spec = re.sub(r"[^A-Za-z0-9_.-]", "_", q), {"title": q}
        bimg = Image.open(build).convert("RGB")
        boxes = json.load(open(boxes_file)).get("pieces", {})
    else:
        gid = resolve(api, q)
        spec = json.load(http(f"{api}/api/card/{gid}"))["spec"]
        resp = http(f"{api}/api/render", {"spec": spec, "size": "holotable", "format": "png"})
        bimg = Image.open(io.BytesIO(resp.read())).convert("RGB")
        boxes = json.loads(resp.headers.get("X-Piece-Boxes") or "{}").get("pieces", {})
        if boxes_file:
            boxes = json.load(open(boxes_file)).get("pieces", {})
        if build:
            bimg = Image.open(build).convert("RGB")
    pimg, ref_src = ref_image(spec, holotable, ref)
    W, H = bimg.size
    if pimg.size != (W, H):
        pimg = pimg.resize((W, H), Image.LANCZOS)
    d = Path(out) / gid; d.mkdir(parents=True, exist_ok=True)
    pimg.save(d / "pc.png"); bimg.save(d / "build.png")
    Image.blend(pimg, bimg, 0.5).save(d / "overlay.png")
    B, P = np.asarray(bimg).astype(np.float64), np.asarray(pimg).astype(np.float64)
    diff = np.clip(np.abs(B - P) * 4, 0, 255).astype(np.uint8); Image.fromarray(diff).save(d / "diff.png")
    side = Image.new("RGB", (W * 3 + 20, H), "white"); side.paste(pimg, (0, 0)); side.paste(bimg, (W + 10, 0)); side.paste(Image.fromarray(diff), (2 * W + 20, 0))
    side.save(d / "side.png")
    rows = {}
    for name, box in sorted(boxes.items()):
        r = measure(B, P, box, W, H)
        if r: rows[name] = r
    rows["frame"] = frame_row(B, P, [b for b in boxes.values()], W, H)
    rep = dict(gempId=gid, title=spec.get("title"), template=None, reference=ref_src, build_source=build or f"{api}/api/render",
               size=[W, H], search_px=SEARCH, elements=rows)
    (d / "report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    (d / "report.md").write_text(to_md(rep), encoding="utf-8")
    return rep, d


def to_md(rep):
    L = [f"### {rep['title']} ({rep['gempId']})", "", f"Reference: `{rep['reference']}` · build: `{rep['build_source']}` · {rep['size'][0]}×{rep['size'][1]}", "",
         "| Element | box (x, y, w, h) | dx | dy | dw | dh | MAD | changed % | ΔE | Result |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, r in rep["elements"].items():
        exact = (r["dx"] in (0, None) and r["dy"] in (0, None) and r["dw"] in (0, None) and r["dh"] in (0, None) and r["changed_pct"] == 0)
        L.append(f"| {k} | {r['box'] or '—'} | {r['dx'] if r['dx'] is not None else '—'} | {r['dy'] if r['dy'] is not None else '—'} | "
                 f"{r['dw'] if r['dw'] is not None else '—'} | {r['dh'] if r['dh'] is not None else '—'} | {r['mad']} | {r['changed_pct']} | {r['dE']} | "
                 f"{'MATCH' if exact else 'DIFF: fix, deviation or explain'}{' (offset at search limit: may be larger)' if SEARCH in (abs(r['dx'] or 0), abs(r['dy'] or 0)) else ''} |")
    L += ["", "dx/dy: where the build's element sits relative to the PC's (+ = right/down), best integer alignment within "
          f"±{rep['search_px']} px. dw/dh: ink-box size change in px. MAD: mean |build−PC| after alignment (0–255). "
          f"changed %: share of pixels that differ by >{INK_DELTA} levels without re-alignment. ΔE: mean CIE76 colour difference."]
    return "\n".join(L)


def sheet(results, path):
    th = []
    for rep, d in results:
        ims = [Image.open(d / n).convert("RGB").resize((248, 346), Image.LANCZOS) for n in ("pc.png", "build.png", "diff.png")]
        row = Image.new("RGB", (248 * 3 + 20, 346 + 22), "white")
        for i, im in enumerate(ims): row.paste(im, (i * 258, 22))
        label = (rep["title"] or "").replace("•", "").replace("_", "")   # the default bitmap font has no bullet
        ImageDraw.Draw(row).text((4, 4), f"{rep['gempId']}  {label}   (PC | CardMaker | diff x4)", fill="black")
        th.append(row)
    S = Image.new("RGB", (th[0].width, sum(t.height for t in th)), "white")
    y = 0
    for t in th: S.paste(t, (0, y)); y += t.height
    S.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cards", nargs="*", help="titles or gempIds")
    ap.add_argument("--batch", help="file with one title or gempId per line (# comments)")
    ap.add_argument("--api", default=os.environ.get("CARDMAKER_API", "http://127.0.0.1:17010"))
    ap.add_argument("--holotable", default=os.environ.get("HOLOTABLE_CARDS", "/opt/swccg-holotable/Images-HT/starwars"))
    ap.add_argument("--ref", help="reference image instead of the PC hires PNG (single card)")
    ap.add_argument("--build", help="CardMaker image to measure instead of a fresh API render (single card)")
    ap.add_argument("--boxes", help="element boxes JSON ({pieces: {name: [x, y, w, h]}} at the image's size); with --build and --ref no API is needed")
    ap.add_argument("--out", default="out/compare")
    ap.add_argument("--sheet", action="store_true", help="write <out>/sheet.png")
    a = ap.parse_args()
    qs = list(a.cards)
    if a.batch:
        qs += [l.split("#")[0].strip() for l in open(a.batch, encoding="utf-8") if l.split("#")[0].strip()]
    results, failed = [], []
    for q in qs:
        try:
            rep, d = compare(a.api, q, a.out, a.holotable, a.ref, a.build, a.boxes)
            results.append((rep, d)); print(f"ok   {rep['gempId']:>8}  {rep['title']}  -> {d}/report.md", flush=True)
        except Exception as e:   # noqa: BLE001
            failed.append((q, str(e))); print(f"FAIL {q}: {e}", flush=True)
    Path(a.out).mkdir(parents=True, exist_ok=True)
    if a.sheet and results:
        sheet(results, Path(a.out) / "sheet.png")
    (Path(a.out) / "summary.json").write_text(json.dumps({"ok": [r["gempId"] for r, _ in results], "failed": failed}, indent=1))
    sys.exit(1 if failed and not results else 0)


if __name__ == "__main__":
    main()
