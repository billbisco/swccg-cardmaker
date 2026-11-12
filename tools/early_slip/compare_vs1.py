"""Render the 12 Virtual Set #1 cards on the early-slip template through a running card maker (/api/card + /api/render)
and build side-by-side comparisons with the archived 2002 slips (VirtualCards1.pdf)."""
import json, sys, io, urllib.request, pymupdf
from PIL import Image, ImageDraw, ImageChops
API = sys.argv[1]; OUTD = sys.argv[2]; PDF = sys.argv[3]; MODE = sys.argv[4] if len(sys.argv) > 4 else "wrap"
IDS = {1: "1_19", 2: "1_4", 3: "1_141", 4: "1_154", 5: "1_36", 6: "1_64", 7: "1_168", 8: "1_191", 9: "1_299", 10: "1_311", 11: "1_203", 12: "1_211"}
slips = json.load(open(sys.argv[5] if len(sys.argv) > 5 else "slips.json"))
doc = pymupdf.open(PDF); pg = doc[0]
SX, SY = 1343 / 179.13, 1931 / 252
H = 66
res = []
for o in slips:
    n = int(o["number"]); gid = IDS[n]
    spec = json.load(urllib.request.urlopen(f"{API}/api/card/{gid}"))["spec"]
    spec["style"] = "early-slip"
    es = {"set": "1", "number": str(n), "text": " ".join(o["lines"])}
    if o["stats"]:
        es["deploy"], es["forfeit"] = o["stats"]
    if MODE == "lines":
        es["lines"] = o["lines"]
    def rend(e):
        spec["early_slip"] = e
        req = urllib.request.Request(f"{API}/api/render", json.dumps({"spec": spec, "size": "master", "format": "png"}).encode(), {"Content-Type": "application/json"})
        return Image.open(io.BytesIO(urllib.request.urlopen(req).read())).convert("RGB")
    rend(es).save(f"{OUTD}/vs1-{n:02d}-{gid}-early-slip.png")   # as played: cut to the outline
    im = rend(dict(es, paper=True))                                # as printed on the sheet (white paper), for the comparison
    ours = im.crop((144, int(2075 - H * SY), 1487, 2075))
    x0, y0, x1, y1 = o["rect"]
    clip = pymupdf.Rect(x0, y1 - H, x0 + 179.13, y1)
    pm = pg.get_pixmap(clip=clip, dpi=600)
    arch = Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB").resize(ours.size, Image.LANCZOS)
    # side by side: archive | ours | difference
    diff = ImageChops.difference(arch, ours).convert("L").point(lambda v: 255 - v)
    W_, H_ = ours.size
    sheet = Image.new("RGB", (W_, H_ * 3 + 120), "white")
    d = ImageDraw.Draw(sheet)
    for i, (lab, img) in enumerate((("archived 2002 slip (VirtualCards1.pdf)", arch), ("card maker early-slip", ours), ("difference (dark = differs)", diff.convert("RGB")))):
        d.text((10, i * (H_ + 40) + 5), lab, fill="black")
        sheet.paste(img, (0, i * (H_ + 40) + 30))
    sheet.save(f"{OUTD}/cmp-vs1-{n:02d}.png")
    import numpy as np
    a = np.asarray(arch).astype(int); b = np.asarray(ours).astype(int)
    score = float((np.abs(a - b).sum(2) > 120).mean())
    res.append((n, gid, o["title"], round(score * 100, 2)))
    print(n, gid, round(score * 100, 2), "% px differ")
json.dump(res, open(f"{OUTD}/scores-{MODE}.json", "w"))
