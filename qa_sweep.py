"""Card maker QA sweep: render every card the editor offers (as it opens, default art) at Holotable size and compare
with the card's own scan. Writes metrics (CSV) and small side-by-side thumbs (scan | render) for review.

Run inside the swccg-cardmaker image:  CARDMAKER_NO_CACHE=1 python3 qa_sweep.py OUTDIR SHARD NSHARDS [gid ...]
"""
import csv, io, json, os, re, sys, time, traceback, urllib.request
from pathlib import Path
os.environ.setdefault("CARDMAKER_NO_CACHE", "1")
os.environ["CARDMAKER_OUT"] = f"/tmp/cm-out-{sys.argv[2]}"; os.makedirs(os.environ["CARDMAKER_OUT"], exist_ok=True)   # per shard
for _p in ("/app", "/app/webapp", str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent / "webapp")):
    sys.path.insert(0, _p)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import server, adapter

out = Path(sys.argv[1]); shard, nsh = int(sys.argv[2]), int(sys.argv[3]); only = sys.argv[4:]
(out / "thumbs").mkdir(parents=True, exist_ok=True)
ids = only or sorted(server.CARDS, key=lambda g: (str(server.CARDS[g].get("set")), g))
ids = [g for i, g in enumerate(ids) if i % nsh == shard]
done = set()
for mf in out.glob("metrics-*.csv"):          # resume: skip cards already rendered without error
    for row in csv.DictReader(open(mf)):
        if row.get("status") in ("ok", "noscan") and not only: done.add(row["gid"])
ids = [g for g in ids if g not in done]

def scan_of(g):
    u = server.CARDS[g]["front"].get("imageUrl") or ""
    m = re.search(r"/cards/(.+)$", u)
    if not m: return None
    p = server.HOLOTABLE / m.group(1)
    if p.exists(): return Image.open(p)
    try: return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=server.UA), timeout=30).read()))
    except Exception: return None

def metrics(r, s):
    r = np.array(r.convert("RGB")).astype(float); s = np.array(s.convert("RGB")).astype(float)
    small = lambda a: np.array(Image.fromarray(a.astype(np.uint8)).resize((60, 84), Image.BOX)).astype(float)
    coarse = np.abs(small(r) - small(s)).mean()                       # layout / colour / art placement
    rl, sl = r.mean(axis=2), s.mean(axis=2)
    inner = (slice(40, -40), slice(40, -40))
    black = ((rl < 28) & (sl > 110))[inner].mean() * 100               # render dark where the card is light (slivers, holes)
    white = ((rl > 200) & (sl < 60))[inner].mean() * 100               # render light where the card is dark
    hue = lambda a: np.array(Image.fromarray(a.astype(np.uint8)).resize((30, 42), Image.BOX).convert("HSV")).astype(float)
    hr, hs = hue(r), hue(s); sat = (hr[:, :, 1] > 60) & (hs[:, :, 1] > 60)
    dh = np.minimum(np.abs(hr[:, :, 0] - hs[:, :, 0]), 256 - np.abs(hr[:, :, 0] - hs[:, :, 0]))[sat].mean() if sat.any() else 0
    return round(coarse, 2), round(black, 3), round(white, 3), round(float(dh), 1)

rows = []; t0 = time.time()
mpath = out / (f"metrics-{shard}.csv" if not only else f"metrics-redo-{shard}.csv")
new = not mpath.exists(); fo = open(mpath, "a", newline=""); w = csv.writer(fo)
if new: w.writerow(["gid", "title", "type", "set", "status", "coarse", "black", "white", "hue", "secs", "error"])
for n, g in enumerate(ids):
    c = server.CARDS[g]; f = c["front"]; st = time.time(); err = ""; m = ("", "", "", "")
    try:
        spec = adapter.gemp_to_spec(c)
        lib = server.ART_MANIFEST.get(g, {}).get("status") == "ok"
        spec["art"] = {"kind": "library" if lib and spec.get("slip_type") != "System" else "scan", "gempId": g, "version": "orig"}
        data, _ = server.render_spec(spec, "holotable", "png")
        r = Image.open(io.BytesIO(data)).convert("RGB")
        s = scan_of(g)
        if s is None:
            status = "noscan"
        else:
            s = s.convert("RGB")
            if (s.width > s.height) != (r.width > r.height): s = s.rotate(90, expand=True)
            s = s.resize(r.size, Image.LANCZOS); m = metrics(r, s); status = "ok"
            th = Image.new("RGB", (2 * 240 + 6, int(240 * r.height / r.width)), "white")
            th.paste(s.resize((240, th.height)), (0, 0)); th.paste(r.resize((240, th.height)), (246, 0))
            th.save(out / "thumbs" / f"{g}.jpg", quality=82)
    except Exception as e:   # noqa: BLE001
        status = "error"; err = f"{type(e).__name__}: {e}"[:300]
    w.writerow([g, f.get("title"), f.get("type"), c.get("set"), status, *m, round(time.time() - st, 1), err]); fo.flush()
    if n % 50 == 0: print(f"[{shard}] {n}/{len(ids)} {time.time() - t0:.0f}s", flush=True)
print(f"[{shard}] done {len(ids)} in {time.time() - t0:.0f}s", flush=True)
