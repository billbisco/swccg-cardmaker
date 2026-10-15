"""SWCCG Card Maker web service (prototype).

    python3 webapp/server.py [--port 8790]

Endpoints (all JSON unless noted):
  GET  /api/health
  GET  /api/search?q=luke&limit=30        cards from the PC card JSON (Decipher + PC virtual), title search
  GET  /api/card/<gempId>                  editable spec for that card (+ which art sources exist)
  GET  /api/options                        templates, sides, icons, expansions the editor offers
  POST /api/render   {"spec": {...}, "size": "preview"|"holotable"|"master", "format": "webp"|"png"}
                     -> image bytes. spec.art = {"kind": "library", "gempId": "5_75", "version": "orig"|"x4"}
                                              | {"kind": "upload", "data": "data:image/...;base64,..."}
                                              | {"kind": "scan"}   (the card's own scan, frame-mapped)
                                              | {"kind": "none"}
                        spec.set_symbol = "data:image/png;base64,..." (optional, lower icon slot)

Rendering runs render.py in one long-lived headless Chromium on a worker thread (Playwright's sync API is not
thread-safe), so requests are served one at a time. Previews are cached by spec hash.
"""
from __future__ import annotations
import base64, hashlib, io, json, os, queue, re, sys, threading, time, traceback, urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(HERE))
import render, build_vs, adapter   # noqa: E402
from PIL import Image   # noqa: E402

DATA = Path(os.environ.get("CARDMAKER_DATA", "/tmp/cardmaker-data")); DATA.mkdir(parents=True, exist_ok=True)
CACHE = DATA / "cache"; CACHE.mkdir(exist_ok=True)
ART_RAW = os.environ.get("ART_RAW", "https://raw.githubusercontent.com/billbisco/swccg-card-art/main/decipher")
ART_CDN = os.environ.get("ART_CDN", "https://cdn.jsdelivr.net/gh/billbisco/swccg-card-art@main/decipher")
HOLOTABLE = Path(os.environ.get("HOLOTABLE", "/holotable/Images-HT/starwars"))   # swccg.com's mirror of the card faces
UA = {"User-Agent": "swccg-cardmaker/0.1"}

# ---------- card index ----------
CARDS: dict[str, dict] = {}
for side in ("Light", "Dark"):
    for c in json.load(open(ROOT / f"gempdata/{side}.json", encoding="utf-8"))["cards"]:
        if c.get("gempId"):
            CARDS[c["gempId"]] = c
_CORR = json.load(open(ROOT / "gempdata/corrections.json", encoding="utf-8")) if (ROOT / "gempdata/corrections.json").exists() else {}
for _g, _fix in _CORR.items():   # printed-card typo fixes over the PC JSON
    if _g in CARDS:
        for _k, (_wrong, _right) in _fix.items():
            _f = CARDS[_g]["front"]
            if isinstance(_f.get(_k), str):
                _f[_k] = _f[_k].replace(_wrong, _right)
ART_MANIFEST = {}
mp = ROOT / "webapp/art-manifest.json"
if mp.exists():
    ART_MANIFEST = json.load(open(mp, encoding="utf-8")).get("cards", {})
SETS = {s["id"]: s["name"] for s in json.load(open(ROOT / "gempdata/sets.json", encoding="utf-8"))}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower().replace("•", ""))


INDEX = [(norm(c["front"].get("title")), g) for g, c in CARDS.items()]


def search(q: str, limit: int = 30) -> list[dict]:
    nq = norm(q)
    if not nq:
        return []
    hits = [g for t, g in INDEX if nq in t]
    hits.sort(key=lambda g: (not norm(CARDS[g]["front"].get("title")).startswith(nq), len(CARDS[g]["front"].get("title") or ""), g))
    return [row(g) for g in hits[:limit]]


def row(g: str) -> dict:
    c = CARDS[g]; f = c["front"]
    return {"gempId": g, "title": f.get("title"), "side": c["side"], "type": f.get("type"),
            "subType": f.get("subType"), "set": SETS.get(c.get("set"), c.get("set")),
            "art": "library" if ART_MANIFEST.get(g, {}).get("status") == "ok" else "scan"}


def set_group(sid: str) -> str:
    n = int(re.match(r"\d+", sid).group()) if re.match(r"\d+", sid) else 0
    return "Decipher" if n < 200 else ("Players Committee virtual" if n < 300 else "Players Committee other")


SET_LIST = []   # browse: every set that has cards, Decipher first, in release order
_counts: dict[str, int] = {}
for _c in CARDS.values():
    _counts[str(_c.get("set"))] = _counts.get(str(_c.get("set")), 0) + 1
for _s in json.load(open(ROOT / "gempdata/sets.json", encoding="utf-8")):
    if _counts.get(_s["id"]):
        SET_LIST.append({"id": _s["id"], "name": _s["name"], "group": set_group(_s["id"]), "count": _counts[_s["id"]]})
SET_LIST.sort(key=lambda s: (["Decipher", "Players Committee virtual", "Players Committee other"].index(s["group"]), s.get("_pos", 0)))
TYPES = sorted({c["front"].get("type") or "" for c in CARDS.values()} - {""})


def browse(sid: str, side: str, typ: str) -> list[dict]:
    gs = [g for g, c in CARDS.items() if (not sid or str(c.get("set")) == sid) and (not side or c["side"] == side)
          and (not typ or (c["front"].get("type") or "") == typ)]
    gs.sort(key=lambda g: (norm(CARDS[g]["front"].get("title")), g))
    return [row(g) for g in gs[:2000]]


# ---------- art ----------
def fetch(url: str, dest: Path) -> Path:
    if not dest.exists():
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        tmp = dest.with_suffix(dest.suffix + ".part"); tmp.write_bytes(data); tmp.rename(dest)
    return dest


def scan_path(gid: str) -> Path | None:
    u = (CARDS.get(gid) or {}).get("front", {}).get("imageUrl") or ""
    m = re.search(r"/cards/(.+)$", u)
    if m:
        p = HOLOTABLE / m.group(1)
        if p.exists():
            return p
        return fetch(u, CACHE / ("scan-" + re.sub(r"[^A-Za-z0-9._-]", "_", m.group(1))))
    return None


def resolve_art(spec: dict) -> dict | None:
    a = spec.get("art") or {}
    kind = a.get("kind") or ("library" if ART_MANIFEST.get(spec.get("gempId") or "", {}).get("status") == "ok" else "scan")
    if kind == "none":
        return None
    if kind == "upload" and a.get("data"):
        raw = base64.b64decode(a["data"].split(",", 1)[1])
        h = hashlib.sha1(raw).hexdigest()[:16]; p = CACHE / f"up-{h}.img"
        if not p.exists(): p.write_bytes(raw)
        im = Image.open(p); w, hgt = im.size
        if a.get("rect"):
            return {"src": str(p), "rect": list(a["rect"])}
        # framing: zoom >= 1 and a focus point (fx, fy in 0..1) inside the cover-fitted crop of the art window
        tpl = render.TEMPLATES[build_vs.template_for(spec)]
        aw, ah = tpl["art"][2:]
        if w / hgt > aw / ah: cw, ch = hgt * aw / ah, hgt
        else: cw, ch = w, w * ah / aw
        z = min(max(float(a.get("zoom") or 1), 1.0), 6.0); cw, ch = cw / z, ch / z
        fx = min(max(float(a.get("fx", 0.5)), 0.0), 1.0); fy = min(max(float(a.get("fy", 0.5)), 0.0), 1.0)
        x0 = fx * (w - cw); y0 = fy * (hgt - ch)
        return {"src": str(p), "rect": [x0, y0, x0 + cw, y0 + ch]}
    gid = a.get("gempId") or spec.get("gempId")
    if kind == "library" and gid:
        ver = a.get("version", "orig"); ext = "png" if ver == "orig" else "webp"
        for base in (ART_RAW, ART_CDN):   # GitHub raw first (fast from the VPS), jsDelivr second (flaky from there)
            try:
                p = fetch(f"{base}/{ver}/{gid}.{ext}", CACHE / f"art-{ver}-{gid}.{ext}")
                w, h = Image.open(p).size
                return {"src": str(p), "rect": [0, 0, w, h]}
            except Exception as e:   # noqa: BLE001
                print("art source failed:", base, gid, e, file=sys.stderr)
        # neither reachable: the card's own scan, so the card still has its picture
    if gid:
        p = scan_path(gid)
        if p:
            if spec.get("wide") and "weapon" in (spec.get("slip_type") or "").lower():
                # landscape printed card (Maul's Double-Bladed Lightsaber): the whole card area of the 1039x745 face
                w, h = Image.open(p).size; k = w / 1039
                return {"src": str(p), "rect": [31 * k, 34 * k, 1007 * k, 712 * k]}
            if "admiral" in (spec.get("slip_type") or "").lower():
                # full-art slip: no silver frame to find, so map the frame box of a Holotable-size face directly
                # (master frame 144..1487 x 144..2075 -> 745x1039 face: x*0.5-35, y*0.5-36), scaled to this scan
                w, h = Image.open(p).size; k = w / 745
                return {"src": str(p), "bbox": [37 * k, 36 * k, 708.5 * k, 1001.5 * k]}
            return {"src": str(p)}   # the card's own scan: render.py maps the frame and cuts the window
    return None


def resolve_set_symbol(spec: dict) -> str | None:
    d = spec.get("set_symbol")
    if not d or not str(d).startswith("data:"):
        return None
    raw = base64.b64decode(d.split(",", 1)[1]); h = hashlib.sha1(raw).hexdigest()[:16]
    p = CACHE / f"sym-{h}.png"
    if not p.exists():
        Image.open(io.BytesIO(raw)).convert("RGBA").save(p)
    return str(p)


# ---------- renderer thread ----------
JOBS: "queue.Queue[tuple]" = queue.Queue()


def worker():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width": render.W, "height": render.H}, device_scale_factor=1)
        while True:
            card, done = JOBS.get()
            try:
                land = render.is_wide(render.TEMPLATES[card["template"]])
                pg.set_viewport_size({"width": render.H, "height": render.W} if land else {"width": render.W, "height": render.H})
                done["img"] = render.screenshot_card(card, pg); done["land"] = land
            except Exception as e:   # noqa: BLE001
                done["err"] = f"{type(e).__name__}: {e}"; traceback.print_exc()
            finally:
                done["ev"].set()


threading.Thread(target=worker, daemon=True).start()


# render cache entries are only valid for the code that made them: a deploy changes this and old entries are ignored
CODE_VERSION = hashlib.sha1(b"".join((ROOT / f).read_bytes() for f in ("render.py", "build_vs.py", "webapp/adapter.py", "webapp/server.py"))).hexdigest()[:12]


def render_spec(spec: dict, size: str, fmt: str) -> tuple[bytes, str]:
    key = hashlib.sha1(json.dumps([CODE_VERSION, spec, size, fmt], sort_keys=True).encode()).hexdigest()
    cp = CACHE / f"r-{key}.{fmt}"
    if cp.exists():
        return cp.read_bytes(), fmt
    s = dict(spec)
    art_ok = True
    try:
        s["_art"] = resolve_art(spec); s["_art_kind"] = (spec.get("art") or {}).get("kind")
    except Exception as e:   # art source unreachable: still draw the card (blank window), don't cache it
        print("art failed:", spec.get("gempId"), e, file=sys.stderr); s["_art"] = None; art_ok = False
    s["_set_icon_file"] = resolve_set_symbol(spec)
    card = adapter.spec_to_card(s, build_vs)
    if s["_art"] is None:
        card.pop("art", None)
    done = {"ev": threading.Event()}
    JOBS.put((card, done))
    if not done["ev"].wait(120):
        raise RuntimeError("render timed out")
    if "err" in done:
        raise RuntimeError(done["err"])
    im, land = done["img"], done["land"]
    if size in ("holotable", "preview"):
        im = render.holotable_size(im, land)   # the card itself at Holotable / GEMP size (745 x 1039)
    buf = io.BytesIO()
    if fmt == "png":
        im.save(buf, "PNG", optimize=size != "master")
    else:
        im.save(buf, "WEBP", quality=88 if size == "preview" else 95)
    data = buf.getvalue()
    if art_ok:
        cp.write_bytes(data)
    return data, fmt


OPTIONS = {
    "sides": ["Light", "Dark"],
    "slip_types": ["Character", "Effect", "Immediate Effect", "Used Interrupt", "Lost Interrupt", "Used Or Lost Interrupt",
                   "Starting Interrupt", "Character Weapon", "Starship Weapon", "Device", "Starfighter", "Starship",
                   "Vehicle", "Creature", "Defensive Shield", "Site", "System", "Objective", "Epic Event", "Jedi Test", "Admiral's Order"],
    "affiliations": ["Rebel", "Imperial", "Alien", "Droid", "Republic", "Jedi Master", "Dark Jedi Master", "Sith",
                     "Alien/Rebel", "Alien/Imperial"],
    "icons": ["pilot", "warrior", "nav", "astromech", "permanent-weapon", "permanent-pilot", "independent", "presence", "episode1"],
    "loc_icons": ["planet", "interior", "exterior", "mobile", "underground", "underwater", "starship", "vehicle", "scomp"],
    "expansions": [None] + sorted(k for k in build_vs.SET_ICON),
    "tokens": {"{alter}": "Immune to Alter icon", "{sense}": "Immune to Sense icon", "{control}": "Immune to Control icon",
               "{episode1}": "Episode I icon", "{light-force}": "Light Side Force icon", "{dark-force}": "Dark Side Force icon",
               "{maintenance}": "maintenance icon", "{pilot:N}": "pilot icon with N (adds N to power...)",
               "▼": "deploy-from-Reserve arrow", "▲": "take-into-hand arrow", "*bold*": "bold", "_italic_": "italic"},
}


class H(BaseHTTPRequestHandler):
    server_version = "swccg-cardmaker/0.1"

    def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None):
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    def do_GET(self):
        u = urlparse(self.path); path = re.sub(r"^/cardmaker", "", u.path); q = parse_qs(u.query)
        try:
            if path == "/api/health":
                return self._json({"ok": True, "cards": len(CARDS), "library": sum(1 for e in ART_MANIFEST.values() if e.get("status") == "ok"), "queue": JOBS.qsize(), "version": CODE_VERSION})
            if path == "/api/search":
                return self._json(search(q.get("q", [""])[0], int(q.get("limit", ["30"])[0])))
            if path == "/api/sets":
                return self._json({"sets": SET_LIST, "types": TYPES})
            if path == "/api/browse":
                g1 = lambda k: q.get(k, [""])[0]
                return self._json(browse(g1("set"), g1("side"), g1("type")))
            if path.startswith("/api/card/"):
                gid = path.rsplit("/", 1)[1]
                if gid not in CARDS:
                    return self._json({"error": "unknown card"}, 404)
                spec = adapter.gemp_to_spec(CARDS[gid])
                lib = ART_MANIFEST.get(gid, {}).get("status") == "ok"
                spec["art"] = {"kind": "library" if lib else "scan", "gempId": gid, "version": "orig"}
                return self._json({"spec": spec, "art_sources": (["library"] if lib else []) + ["scan", "upload", "none"],
                                   "art_urls": {"orig": f"{ART_CDN}/orig/{gid}.png", "x4": f"{ART_CDN}/x4/{gid}.webp"} if lib else {}})
            if path == "/api/options":
                return self._json(OPTIONS)
            # static UI (nginx serves it in production; this is for local runs)
            f = (HERE / "static" / (path.strip("/") or "index.html")).resolve()
            if str(f).startswith(str((HERE / "static").resolve())) and f.is_file():
                ct = {".html": "text/html", ".js": "application/javascript", ".css": "text/css", ".png": "image/png", ".svg": "image/svg+xml"}.get(f.suffix, "application/octet-stream")
                return self._send(200, f.read_bytes(), ct + ("; charset=utf-8" if ct.startswith(("text", "application/j")) else ""))
            return self._json({"error": "not found"}, 404)
        except Exception as e:   # noqa: BLE001
            traceback.print_exc(); return self._json({"error": str(e)}, 500)

    def do_POST(self):
        path = re.sub(r"^/cardmaker", "", urlparse(self.path).path)
        n = int(self.headers.get("Content-Length") or 0)
        if n > 25_000_000:
            return self._json({"error": "request too large (25 MB max)"}, 413)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            if path == "/api/render":
                size = body.get("size", "preview"); fmt = body.get("format", "webp")
                if size not in ("preview", "holotable", "master") or fmt not in ("webp", "png"):
                    return self._json({"error": "bad size/format"}, 400)
                data, fmt = render_spec(body["spec"], size, fmt)
                return self._send(200, data, f"image/{fmt}", {"Cache-Control": "no-store"})
            return self._json({"error": "not found"}, 404)
        except Exception as e:   # noqa: BLE001
            traceback.print_exc(); return self._json({"error": str(e)}, 500)


if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8790
    print(f"cardmaker on :{port}, {len(CARDS)} cards, {len(ART_MANIFEST)} in art manifest", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
