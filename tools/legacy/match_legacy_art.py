#!/usr/bin/env python3
"""Find each Virtual Legacy card's art in the Decipher art library (STANDARD rev 71).

The 2009-2014 Virtual Block cards were printed on the original Decipher card: the PC pasted a new slip over the text and
kept the top of the card, art included. So the art of most legacy cards *is* a Decipher card's library art, cut from a
better-registered scan by its measured window. This tool template-matches every library crop (swccg-card-art
decipher/orig, box from webapp/art-manifest.json, both in the 350x490 normalised card space) into each legacy PC gif
and writes gempdata/legacy_art.json:

  {"cards": {"1001_L5521": {"gempId": "106_3", "r": 0.991, "dx": 0, "dy": -1}, ...}}

Matches with r >= 0.93 are kept (>= 0.85 when the titles agree); the others (new PC art: AI printings, Clone Wars cards) render from the legacy
card's own scan, mapped by the frame (no trim).

  python3 tools/legacy/match_legacy_art.py <legacy gif dir: <id>.gif> <swccg-card-art/decipher/orig> [--out gempdata/legacy_art.json]
"""
import json, re, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
gifs, lib = Path(sys.argv[1]), Path(sys.argv[2])
out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "gempdata/legacy_art.json"
MAN = json.load(open(ROOT / "webapp/art-manifest.json", encoding="utf-8"))["cards"]
T = (40, 28)   # coarse thumbnail for the all-pairs search


def z(a):
    a = a - a.mean(); n = np.linalg.norm(a)
    return a / n if n else a


def gray(im):
    return np.asarray(im.convert("L"), float)


cands = []
for g, e in MAN.items():
    if e.get("status") != "ok" or not e.get("box") or e.get("system"):
        continue
    p = lib / f"{g}.png"
    if not p.exists():
        continue
    im = Image.open(p).convert("RGBA")
    cands.append((g, e["box"], im, e.get("side"), e.get("family") or ""))
print(len(cands), "library crops", file=sys.stderr)


def norm_card(path):
    im = Image.open(path).convert("RGB")
    return im.resize((350, 490) if im.height >= im.width else (490, 350))


def coarse(im, box):
    x0, y0, x1, y1 = box
    return z(gray(im.crop((x0, y0, x1, y1)).resize(T, Image.BILINEAR)).ravel())


libv = {}
for g, box, im, side, fam in cands:
    a = im.convert("RGB")
    libv[g] = z(gray(a.resize(T, Image.BILINEAR)).ravel())

bybox = {}
for g, box, im, side, fam in cands:   # coarse search: windows within 4 px share one crop (the refine step uses each card's own box)
    bybox.setdefault(tuple(4 * round(v / 4) for v in box), []).append(g)
BOX = {g: box for g, box, im, side, fam in cands}
libm = {b: (gs, np.stack([libv[g] for g in gs])) for b, gs in bybox.items()}
print(len(libm), "distinct windows", file=sys.stderr)
IM = {g: im for g, box, im, side, fam in cands}

res = {}
files = sorted(p for p in gifs.glob("*.gif") if not p.stem.endswith("_BACK"))
for i, p in enumerate(files):
    card = norm_card(p)
    W, H = card.size
    C = gray(card)
    scores = []
    for box, (gs, M) in libm.items():
        if box[2] > W or box[3] > H:
            continue
        best = None
        for dx, dy in ((0, 0), (-3, 0), (3, 0), (0, -3), (0, 3)):
            b = (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)
            s_ = M @ coarse(card, b)
            best = s_ if best is None else np.maximum(best, s_)
        scores += [(float(v), g, BOX[g]) for v, g in zip(best, gs)]
    if not scores:
        continue
    scores.sort(key=lambda s: -s[0])
    top = None
    for c0, g, box in scores[:4]:   # refine: full resolution, +-6 px
        w, h = box[2] - box[0], box[3] - box[1]
        A = gray(IM[g].convert("RGB").resize((w, h), Image.BILINEAR))
        a = z(A[4:-4, 4:-4].ravel())
        for dy in range(-6, 7):
            for dx in range(-6, 7):
                y0, x0 = box[1] + dy + 4, box[0] + dx + 4
                Q = C[y0:y0 + h - 8, x0:x0 + w - 8]
                if Q.shape != (h - 8, w - 8):
                    continue
                r = float(z(Q.ravel()) @ a)
                if top is None or r > top[0]:
                    top = (r, g, dx, dy)
    if top:
        res[p.stem] = {"gempId": top[1], "r": round(top[0], 3), "dx": top[2], "dy": top[3]}
    if i % 50 == 0:
        print(i, p.stem, res.get(p.stem), file=sys.stderr, flush=True)

# keep r >= 0.93, or r >= 0.85 when the matched card has the legacy card's title or its original-title strip (the
# lower scores are shield fades and dark scans of the same picture: Toryn Farr (V) 0.86, Leave Them To Me (V) 0.88)
TITLES = {}
for side in ("Light", "Dark"):
    for c in json.load(open(ROOT / f"gempdata/{side}.json", encoding="utf-8"))["cards"]:
        TITLES.setdefault(c.get("gempId"), c["front"].get("title"))
    for c in json.load(open(ROOT / f"gempdata/{side}Legacy.json", encoding="utf-8"))["cards"]:
        TITLES[f"{c['set']}_L{c['id']}"] = (c["front"].get("title"), c["front"].get("imageUrl"))
LAB = {v.get("image"): v for v in json.load(open(ROOT / "gempdata/card_labels.json", encoding="utf-8"))["cards"].values()}
tn = lambda t: re.sub(r"\((v|light|dark|premium|ai|ref iii|death star ii)\)|[^a-z0-9]", "", (t or "").lower())


def same_title(k, v):
    t, img = TITLES.get(k, (None, None))
    return tn(TITLES.get(v["gempId"])) in (tn(t), tn((LAB.get(img) or {}).get("original_title")))


keep = {k: v for k, v in res.items() if v["r"] >= 0.93 or (v["r"] >= 0.85 and same_title(k, v))}
json.dump({"_meta": {"tool": "tools/legacy/match_legacy_art.py", "threshold": "r >= 0.93, or >= 0.85 with the same title / original title",
                     "note": "legacy card -> Decipher library art it was printed with (template match into the PC gif)"},
           "cards": dict(sorted(keep.items()))}, open(out, "w", encoding="utf-8"), indent=0)
if "--all" in sys.argv:
    json.dump(res, open(sys.argv[sys.argv.index("--all") + 1], "w"), indent=0)
print(len(keep), "of", len(res), "matched", file=sys.stderr)
