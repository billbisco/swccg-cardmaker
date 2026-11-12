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
import base64, hashlib, io, json, os, queue, re, sys, threading, time, traceback, urllib.parse, urllib.request
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


def rg_art_urls(gid: str) -> dict:
    b, _, g = art_base(ART_CDN, gid, "orig"); o, _, _ = art_base(ART_CDN, gid, "original")
    return {"orig": f"{b}/orig/{g}.png", "original": f"{o}/orig/{g}.png"}


def art_base(base: str, gid: str, ver: str) -> tuple[str, str, str]:
    """Library folder for a card: Reflections Gold (set 15) lives in reflections-gold/; both versions use the art cut
    from the Remastered render (Bill 2026-11-05), version "original" = the window cut from the 2001 playtest photo."""
    m = re.fullmatch(r"15_(\d+)o?", gid or "")
    if not m:
        return base, ver, gid
    rg = base.rsplit("/decipher", 1)[0] + "/reflections-gold"
    if ver == "original":
        return rg + "/original", "orig", f"15_{m.group(1)}"
    return rg, ver, f"15_{m.group(1)}"
HOLOTABLE = Path(os.environ.get("HOLOTABLE", "/holotable/Images-HT/starwars"))   # swccg.com's mirror of the card faces
UA = {"User-Agent": "swccg-cardmaker/0.1"}

# ---------- card index ----------
CARDS: dict[str, dict] = {}
_SAME_ID: dict[str, list] = {}
for side in ("Light", "Dark"):
    for c in json.load(open(ROOT / f"gempdata/{side}.json", encoding="utf-8"))["cards"]:
        if c.get("gempId"):
            _SAME_ID.setdefault(c["gempId"], []).append(c)
for _g, _cs in _SAME_ID.items():
    # PC alternate-image printings share their card's gempId: the plain printing (shortest title) keeps the id, each
    # other printing is <gempId>^<its extra parenthetical>, as in card_labels.json (200_76^AI, 200_95^Tatooine)
    _base = min(_cs, key=lambda x: (len(x["front"].get("title") or ""), x["front"].get("title") or ""))
    _bp = set(re.findall(r"\(([^)]*)\)", _base["front"].get("title") or ""))
    for _c in _cs:
        if _c is _base:
            CARDS[_g] = _c; continue
        _extra = [p for p in re.findall(r"\(([^)]*)\)", _c["front"].get("title") or "") if p not in _bp]
        _k = f"{_g}^{' '.join(_extra) or _c['id']}"
        _c["gempId"] = _k if _k not in CARDS else f"{_g}^{_c['id']}"
        CARDS[_c["gempId"]] = _c
for side in ("Light", "Dark"):
    lp = ROOT / f"gempdata/{side}Legacy.json"   # the PC's 2009-2014 Virtual Blocks (legacy): no GEMP ids, keyed <set>_L<id>
    if lp.exists():
        for c in json.load(open(lp, encoding="utf-8"))["cards"]:
            c["gempId"] = f"{c['set']}_L{c['id']}"
            CARDS[c["gempId"]] = c
_rgp = ROOT / "gempdata/ReflectionsGold.json"   # set 15 (swccg-guild/work#174): Remastered 15_N, original playtest 15_No
if _rgp.exists():
    for c in json.load(open(_rgp, encoding="utf-8"))["cards"]:
        CARDS[c["gempId"]] = c
_RG_IDS = [g for g in CARDS if re.fullmatch(r"15_\d+o?", g)]
for _c in CARDS.values():   # one card spells the Force icon keys in lower case
    for _a, _b in (("lightsideIcons", "lightSideIcons"), ("darksideIcons", "darkSideIcons")):
        if _a in _c["front"]: _c["front"].setdefault(_b, _c["front"].pop(_a))
_CORR = json.load(open(ROOT / "gempdata/corrections.json", encoding="utf-8")) if (ROOT / "gempdata/corrections.json").exists() else {}
_FILL = json.load(open(ROOT / "gempdata/fill.json", encoding="utf-8")) if (ROOT / "gempdata/fill.json").exists() else {}
if (ROOT / "gempdata/card_labels.json").exists():   # PC extra labels, synced from billbisco/swccg-gemp (swccg-guild/work#100)
    adapter.PC_LABELS.update(json.load(open(ROOT / "gempdata/card_labels.json", encoding="utf-8")).get("cards", {}))
_PRINTINGS = {g: [g] + [k for k in CARDS if k.startswith(g + "^")] for g in _SAME_ID}   # fills / fixes cover every printing
for _g, _vals in _FILL.items():   # values the PC JSON lacks, transcribed from the printed cards (Force icons, INFLUENCE, …)
    for _gg in _PRINTINGS.get(_g, [_g]):
        if _gg in CARDS and isinstance(_vals, dict):
            for _k, _v in _vals.items():
                if not _k.startswith("_"):
                    CARDS[_gg]["front"][_k] = _v
for _g, _fix in _CORR.items():   # printed-card typo fixes over the PC JSON
    for _gg in [x for x in _PRINTINGS.get(_g, [_g]) if x in CARDS]:
        for _k, _pairs in _fix.items():
            _side, _, _kk = _k.rpartition(".")   # "gametext" (front) or "back.gametext"
            _f = CARDS[_gg].get(_side or "front") or {}
            for _wrong, _right in ([_pairs] if isinstance(_pairs[0], str) else _pairs):
                if isinstance(_f.get(_kk), str):
                    _f[_kk] = _f[_kk].replace(_wrong, _right)
for _g, _c in CARDS.items():   # title -> Decipher expansion (sets 1-14, 101-112), for the PC (V) cards' spheres
    _sid = str(_c.get("set"))
    if _sid.isdigit() and int(_sid) < 200 and adapter.SETS.get(_sid):
        adapter.BASE_ICONS.setdefault(re.sub(r"[^a-z0-9]", "", adapter.strip_printing(_c["front"].get("title") or "").lower().replace("•", "")), _c["front"].get("icons") or [])
        adapter.BASE_EXP.setdefault(re.sub(r"[^a-z0-9]", "", adapter.strip_printing(_c["front"].get("title") or "").lower().replace("•", "")), adapter.SETS[_sid])
for _c in CARDS.values():   # Force icons per location title, for Virtual Block printings that lack them
    _f = _c["front"]
    if _f.get("type") == "Location" and not _c.get("legacy") and (_f.get("lightSideIcons") is not None or _f.get("darkSideIcons") is not None):
        adapter.BASE_LOC.setdefault(re.sub(r"[^a-z0-9]", "", adapter.strip_printing(_f.get("title") or "").lower()), (_f.get("lightSideIcons") or 0, _f.get("darkSideIcons") or 0))
for _c in CARDS.values():   # starship names Decipher prints in italics (titles, lore, game text)
    if (_c["front"].get("type") in ("Starship", "Vehicle")):
        _t = adapter.ship_italics(adapter.strip_printing(_c["front"].get("title") or "").split(" / ")[0])
        adapter.SHIP_NAMES.update(re.findall(r"_(.+?)_", _t))
ART_MANIFEST = {}
mp = ROOT / "webapp/art-manifest.json"
if mp.exists():
    ART_MANIFEST = json.load(open(mp, encoding="utf-8")).get("cards", {})
for _g in _RG_IDS:   # every Reflections Gold card has its art cut from the Remastered render (swccg-card-art reflections-gold/)
    ART_MANIFEST.setdefault(_g, {"status": "ok", "library": "reflections-gold"})
SETS = {s["id"]: s["name"] for s in json.load(open(ROOT / "gempdata/sets.json", encoding="utf-8"))}



def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower().replace("•", ""))


# ---------- Virtual Legacy (2009-2014 Virtual Blocks): the Decipher card each was printed on (STANDARD rev 71) ----------
# legacy_art.json: the library art found in each legacy PC gif (tools/legacy/match_legacy_art.py, r >= 0.93)
LEGACY_ART = json.load(open(ROOT / "gempdata/legacy_art.json", encoding="utf-8")).get("cards", {}) if (ROOT / "gempdata/legacy_art.json").exists() else {}
_DECIPHER_BY_TITLE: dict = {}
for _g, _c in CARDS.items():
    _sid = str(_c.get("set"))
    if _sid.isdigit() and int(_sid) < 200 and "^" not in _g:
        _DECIPHER_BY_TITLE.setdefault(norm(adapter.strip_printing(_c["front"].get("title") or "")), _g)


def print_base(gid: str) -> str | None:
    """The Decipher card a Virtual Block card was printed on: the one whose art is in its gif, else the card named by its
    original-title strip, else the card of the same title."""
    if gid in LEGACY_ART:
        return LEGACY_ART[gid]["gempId"]
    c = CARDS[gid]
    lab = adapter.pc_labels_for(c)
    for t in (lab.get("original_title"), c["front"].get("title")):
        t = re.sub(r"\s*\((?:Light|Dark|V|Premium|Ref III|Death Star II)\)", "", str(t or ""))
        g = _DECIPHER_BY_TITLE.get(norm(adapter.strip_printing(t)))
        if g:
            return g
    return None


# legacy_versions.json (tools/legacy/build_versions.py): GEMP ids (12xx current cards, 22xx version cards, pc-legacy:<id>)
# -> legacy card ids, and each published game-text version (swccg-guild legacy-versions-v4), so /api/card/<GEMP id> and
# ?version=<id> open a Virtual Legacy card with that version's text on its own Virtual Block template
_LV = json.load(open(ROOT / "gempdata/legacy_versions.json", encoding="utf-8")) if (ROOT / "gempdata/legacy_versions.json").exists() else {}
LEGACY_ALIAS: dict = _LV.get("aliases", {})
LEGACY_VERSIONS: dict = _LV.get("versions", {})
LEGACY_NOTES: dict = _LV.get("notes", {})   # v4 is_version null (capitals / punctuation only, waiting on Bill): shown, not selectable
for _g, _c in CARDS.items():
    if _c.get("legacy"):
        _b = print_base(_g)
        if _b:
            _c["_print_base_set"] = str(CARDS[_b].get("set"))


# ---------- Original Virtual Sets 1-17 (2002-2008): the remaster transcriptions, GEMP ids 11NN_<slip> ----------
OVS_NAMES = {1: "Legacy", 2: "Our Most Desperate Hour", 3: "Revolution", 4: "Battle Of Hoth", 5: "A Dark Time",
             6: "City In The Clouds", 7: "Shadows Of The Empire", 8: "Jabba's Court", 9: "Sanctuary Moon",
             10: "Fourth Anthology", 11: "Gathering Storm", 12: "Martyrs & Magistrates", 13: "Remote Outpost",
             14: "Armed & Operational", 15: "Galactic Frontier", 16: "Revenge Of The Sith", 17: "The Force Unleashed"}
OVS: dict[str, dict] = {}
for _n in OVS_NAMES:
    for _f in sorted((ROOT / f"cards/vs{_n}").glob("*.json")) if (ROOT / f"cards/vs{_n}").exists() else []:
        if not re.fullmatch(r"\d\d[a-z]?", _f.stem):
            continue
        _d = json.load(open(_f, encoding="utf-8"))
        _g = f"{1100 + _n}_{_f.stem.lstrip('0') or '0'}"
        _d.update(gempId=_g, virtual_set=_n, style="ovs", number=str(_d.get("number") or _f.stem))
        OVS[_g] = _d


def ovs_type(st: str) -> str:
    st = st or ""
    for k, v in (("Interrupt", "Interrupt"), ("Effect", "Effect"), ("Weapon", "Weapon"), ("Device", "Device"),
                 ("Starfighter", "Starship"), ("Starship", "Starship"), ("Vehicle", "Vehicle"), ("Creature", "Creature"),
                 ("Shield", "Defensive Shield"), ("Site", "Location"), ("System", "Location"), ("Objective", "Objective"),
                 ("Epic", "Epic Event"), ("Admiral", "Admiral's Order"), ("Character", "Character")):
        if k in st:
            return v
    return st


INDEX = [(norm(c["front"].get("title")), g) for g, c in CARDS.items()] + [(norm(d.get("title")), g) for g, d in OVS.items()]


def search(q: str, limit: int = 30) -> list[dict]:
    nq = norm(q)
    if not nq:
        return []
    hits = [g for t, g in INDEX if nq in t]
    ttl = lambda g: OVS[g].get("title") if g in OVS else CARDS[g]["front"].get("title")
    hits.sort(key=lambda g: (not norm(ttl(g)).startswith(nq), len(ttl(g) or ""), g))
    return [row(g) for g in hits[:limit]]


def row(g: str) -> dict:
    if g in OVS:
        d = OVS[g]; n = d["virtual_set"]
        return {"gempId": g, "title": (d.get("title") or "") + " (V)" + (" AI" if g.endswith("b") else ""), "side": d["side"],
                "type": ovs_type(d.get("slip_type")), "subType": d.get("slip_type"),
                "set": f"Virtual Set {n}: {OVS_NAMES[n]} (Original)", "art": "ovs"}
    c = CARDS[g]; f = c["front"]
    return {"gempId": g, "title": f.get("title"), "side": c["side"], "type": f.get("type"),
            "subType": f.get("subType"), "set": SETS.get(c.get("set"), c.get("set")),
            "art": "library" if ART_MANIFEST.get(g, {}).get("status") == "ok" else "scan"}


def set_group(sid: str) -> str:
    n = int(re.match(r"\d+", sid).group()) if re.match(r"\d+", sid) else 0
    if 1000 <= n < 1100:
        return "Players Committee Virtual Blocks (2009–2014, legacy)"
    return "Decipher" if n < 200 else ("Players Committee virtual" if n < 300 else "Players Committee other")


SET_LIST = []   # browse: every set that has cards, Decipher first, in release order
_counts: dict[str, int] = {}
for _c in CARDS.values():
    _counts[str(_c.get("set"))] = _counts.get(str(_c.get("set")), 0) + 1
for _s in json.load(open(ROOT / "gempdata/sets.json", encoding="utf-8")):
    if _counts.get(_s["id"]):
        SET_LIST.append({"id": _s["id"], "name": _s["name"], "group": set_group(_s["id"]), "count": _counts[_s["id"]]})
for _n, _nm in OVS_NAMES.items():
    _c = sum(1 for d in OVS.values() if d["virtual_set"] == _n)
    if _c:
        SET_LIST.append({"id": f"{1100 + _n}", "name": f"Virtual Set {_n}: {_nm}", "group": "Players Committee Original Virtual Sets (2002–2008)", "count": _c})
GROUPS = ["Decipher", "Players Committee Original Virtual Sets (2002–2008)", "Players Committee Virtual Blocks (2009–2014, legacy)",
          "Players Committee virtual", "Players Committee other"]
SET_LIST.sort(key=lambda s: GROUPS.index(s["group"]))
TYPES = sorted({c["front"].get("type") or "" for c in CARDS.values()} - {""})


# expansion symbol (the ring right of the lore box) per card, as the card maker draws it: Decipher cards by their set,
# PC (V) cards by the original printing's sphere; no sphere (Premiere and its reprints) = "none"
EXP_OF: dict[str, str] = {}
for _g, _c in CARDS.items():
    try:
        _e = adapter.gemp_to_spec(_c).get("expansion")
    except Exception:   # noqa: BLE001
        _e = None
    EXP_OF[_g] = _e if (_e and build_vs.SET_ICON.get(_e)) else "none"
for _g, _d in OVS.items():
    _e = _d.get("expansion")
    EXP_OF[_g] = _e if (_e and build_vs.SET_ICON.get(_e)) else "none"
EXP_ORDER = ["none", "A New Hope", "Hoth", "Dagobah", "Cloud City", "Jabba's Palace", "Special Edition", "Endor",
             "Death Star II", "Reflections II", "Tatooine", "Coruscant", "Reflections III", "Theed Palace", "Premium",
             "Jedi Pack", "Enhanced Cloud City", "Enhanced Jabba's Palace", "Official Tournament Sealed Deck",
             "Jabba's Palace Sealed Deck", "Reflections Gold"]
_ec: dict[str, int] = {}
for _e in EXP_OF.values():
    _ec[_e] = _ec.get(_e, 0) + 1
EXP_LIST = [{"id": e, "name": "None (Premiere, new virtual cards)" if e == "none" else e, "count": _ec[e]}
            for e in sorted(_ec, key=lambda e: (EXP_ORDER.index(e) if e in EXP_ORDER else 99, e))]


def browse(sid: str, side: str, typ: str, exp: str = "") -> list[dict]:
    gs = [g for g, c in CARDS.items() if (not sid or str(c.get("set")) == sid) and (not side or c["side"] == side)
          and (not typ or (c["front"].get("type") or "") == typ)]
    gs += [g for g, d in OVS.items() if (not sid or g.split("_")[0] == sid) and (not side or d["side"] == side)
           and (not typ or ovs_type(d.get("slip_type")) == typ)]
    if exp:
        gs = [g for g in gs if EXP_OF.get(g) == exp]
    gs.sort(key=lambda g: (norm(OVS[g].get("title") if g in OVS else CARDS[g]["front"].get("title")), g))
    return [row(g) for g in gs[:2000]]


# ---------- art ----------
def fetch(url: str, dest: Path) -> Path:
    if not dest.exists():
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        tmp = dest.with_suffix(dest.suffix + ".part"); tmp.write_bytes(data); tmp.rename(dest)
    return dest


def scan_path(gid: str, face: str = "front") -> Path | None:
    """The card's printed face (Holotable mirror, else the PC image). face "back": an Objective's second side (rev 77)."""
    u = ((CARDS.get(gid) or {}).get(face) or {}).get("imageUrl") or ""
    m = re.search(r"/cards/(.+)$", u)
    if m:
        p = HOLOTABLE / m.group(1)
        if p.exists():
            return p
        return fetch(u, CACHE / ("scan-" + re.sub(r"[^A-Za-z0-9._-]", "_", m.group(1))))
    return None


def resolve_art(spec: dict, face: str = "front", split: bool = False) -> dict | None:
    """`split` (rev 77): a picture of a two-picture window: an upload comes whole (render.split_art frames it with
    spec split.fit1 / fit2 in its own side of the stripe)."""
    if face == "back":
        # rev 77: an Objective's back face has its own picture. spec art_back takes the art shapes (upload / scan / none);
        # the art library holds front windows only, so the default (and "library") is the scan of the printed back
        # ("front": the front's own picture; "library" / "upload" / "none" as for art)
        a = dict(spec.get("art_back") or {}) if isinstance(spec.get("art_back"), dict) and (spec.get("art_back") or {}).get("kind") else {}
        if a.get("kind") == "front":
            return resolve_art(spec)
        if a.get("kind") in (None, "ovs"):
            a["kind"] = "scan"
        gid = a.get("gempId") or spec.get("gempId")
        if a["kind"] == "scan":
            p = scan_path(gid, "back") if gid else None
            return {"src": str(p)} if p else None   # render.py maps the frame and cuts the window, as for a front scan
        return resolve_art(dict(spec, art=a))
    a = spec.get("art") or {}
    kind = a.get("kind") or ("library" if ART_MANIFEST.get(spec.get("gempId") or "", {}).get("status") == "ok" else "scan")
    if kind == "none":
        return None
    if kind == "upload" and a.get("data"):
        raw = base64.b64decode(a["data"].split(",", 1)[1])
        h = hashlib.sha1(raw).hexdigest()[:16]; p = CACHE / f"up-{h}.img"
        if not p.exists(): p.write_bytes(raw)
        im = Image.open(p); w, hgt = im.size
        if split and not a.get("rect"):
            return {"src": str(p), "rect": [0, 0, w, hgt]}
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
    if kind == "library" and gid and spec.get("wide") and scan_path(gid):
        kind = "scan"   # landscape printings: the library art is the portrait reprint's window; use the card's own face
    if kind == "library" and gid:
        ver = a.get("version", "orig"); ext = "png" if ver == "orig" else "webp"
        for base in (ART_RAW, ART_CDN):   # GitHub raw first (fast from the VPS), jsDelivr second (flaky from there)
            try:
                b_, v_, g_ = art_base(base, gid, ver); ext = "png" if v_ == "orig" else "webp"
                p = fetch(f"{b_}/{v_}/{g_}.{ext}", CACHE / f"art-{b_.rsplit('/', 1)[-1]}-{v_}-{g_}.{ext}")
                w, h = Image.open(p).size
                e_ = ART_MANIFEST.get(gid, {})
                if e_.get("system") and e_.get("box") and e_.get("box_space") in ("card350", "card normalised to 350x490 (490x350 landscape)"):
                    # rev 84: a system's strip between the bars, placed where it sits on the printed card (render.system_library_art)
                    return {"src": str(p), "rect": [0, 0, w, h], "card350": list(e_["box"])}
                return {"src": str(p), "rect": [0, 0, w, h]}
            except Exception as e:   # noqa: BLE001
                print("art source failed:", base, gid, e, file=sys.stderr)
        # neither reachable: the card's own scan, so the card still has its picture
    if gid:
        p = scan_path(gid)
        if p:
            if spec.get("wide"):
                # landscape printed card (Maul's Double-Bladed Lightsaber): the whole card area of the 1039x745 face
                w, h = Image.open(p).size; k = w / 1039
                return {"src": str(p), "rect": [31 * k, 34 * k, 1007 * k, 712 * k]}
            if spec.get("slip_type") == "System":
                w, h = Image.open(p).size
                if abs(h / w - 1039 / 745) < 0.01 and w >= 700:
                    # Holotable face: the card area sits at a fixed place (dark starfield defeats edge detection)
                    k = w / 745
                    return {"src": str(p), "bbox": [37 * k, 36 * k, 708.5 * k, 1001.5 * k]}
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
        b = pg = None
        n = 0
        while True:
            card, done = JOBS.get()
            for attempt in (1, 2):   # a crashed / closed browser is relaunched once, then the job is retried
                try:
                    if pg is None or n >= 400:   # fresh browser every 400 renders (Chromium memory grows)
                        try:
                            b and b.close()
                        except Exception:   # noqa: BLE001
                            pass
                        b = p.chromium.launch(args=["--disable-dev-shm-usage"])
                        pg = b.new_page(viewport={"width": render.W, "height": render.H}, device_scale_factor=1); n = 0
                    land = render.is_wide(render.TEMPLATES[card["template"]])
                    pg.set_viewport_size({"width": render.H, "height": render.W} if land else {"width": render.W, "height": render.H})
                    done["img"] = render.screenshot_card(card, pg); done["land"] = land; n += 1
                    done.pop("err", None)
                    break
                except Exception as e:   # noqa: BLE001
                    done["err"] = f"{type(e).__name__}: {e}"; traceback.print_exc()
                    if any(w in str(e).lower() for w in ("crash", "closed", "timeout")):   # a timed-out page is relaunched too (it crashed the next jobs)
                        pg = None; continue
                    break
            for tmp in render.OUT.glob(f"_*{card['id']}*"):   # per-card crops / frames: not kept (disk)
                tmp.unlink(missing_ok=True)
            done["ev"].set()


threading.Thread(target=worker, daemon=True).start()


# render cache entries are only valid for the code that made them: a deploy changes this and old entries are ignored
CODE_VERSION = hashlib.sha1(b"".join((ROOT / f).read_bytes() for f in ("render.py", "build_vs.py", "lang_ja.py", "webapp/adapter.py", "webapp/server.py", "gempdata/legacy_typeset.json", "assets/fonts/HolotableText/HolotableTextPC-Regular.ttf", "assets/frames/decipher-tone.npz"))).hexdigest()[:12]


LAST_BOXES: dict = {}


def render_spec(spec: dict, size: str, fmt: str) -> tuple[bytes, str]:
    key = hashlib.sha1(json.dumps([CODE_VERSION, spec, size, fmt], sort_keys=True).encode()).hexdigest()
    cp = CACHE / f"r-{key}.{fmt}"; bp = CACHE / f"r-{key}.boxes.json"
    if cp.exists():
        LAST_BOXES[threading.get_ident()] = json.loads(bp.read_text()) if bp.exists() else {}
        return cp.read_bytes(), fmt
    s = dict(spec)
    art_ok = True
    keep_art = False
    if (spec.get("art") or {}).get("kind") == "ovs" and spec.get("gempId") in OVS:
        # the remaster's own picture (slip / scan mapping exactly as published)
        base = OVS[spec["gempId"]]
        s["art"], s["art_back"] = base.get("art"), base.get("art_back")
        s["_art"], s["_art_kind"], keep_art = None, "ovs", True
    else:
      try:
        two = bool((spec.get("art2") or {}).get("kind") not in (None, "none"))   # rev 77: second picture (split window)
        s["_art"] = resolve_art(spec, split=two); s["_art_kind"] = (spec.get("art") or {}).get("kind")
        s["_art2"] = resolve_art(dict(spec, art=spec["art2"]), split=True) if two else None
      except Exception as e:   # art source unreachable: still draw the card (blank window), don't cache it
        print("art failed:", spec.get("gempId"), e, file=sys.stderr); s["_art"] = None; s["_art2"] = None; art_ok = False
    s["_set_icon_file"] = resolve_set_symbol(spec)
    if spec.get("podracer_flag_data"):   # rev 77: a custom Podracer's own pilot flag (data URI, like the set symbol)
        s["_podracer_flag_file"] = resolve_set_symbol({"set_symbol": spec["podracer_flag_data"]})
    card = adapter.spec_to_card(s, build_vs)
    if s["_art"] is None and not keep_art:
        card.pop("art", None)
    if spec.get("face") == "back" and card.get("back"):
        # rev 77: an Objective's back face, exactly as build_vs's batch path renders it (front card + card["back"])
        art_b = (card["back"] or {}).get("art") or {}
        b = dict(card); b.update(card["back"]); b["id"] = card["id"] + "b"; b.pop("back")
        b.pop("art", None)
        if keep_art and art_b.get("src"):
            b["art"] = art_b   # the remaster's own back picture
        else:
            try:
                ab = resolve_art(spec, "back")
            except Exception as e:   # noqa: BLE001
                print("back art failed:", spec.get("gempId"), e, file=sys.stderr); ab = None; art_ok = False
            if ab:
                b["art"] = ab
        card = b
    done = {"ev": threading.Event()}
    JOBS.put((card, done))
    if not done["ev"].wait(120):
        raise RuntimeError("render timed out")
    if "err" in done:
        raise RuntimeError(done["err"])
    im, land = done["img"], done["land"]
    boxes = card.get("_boxes") or {}
    if size in ("holotable", "preview"):
        im = render.holotable_size(im, land)   # the card itself at Holotable / GEMP size (745 x 1039)
        ox, oy = (36, 35) if land else (35, 36)   # master -> half size, then the Holotable crop
        boxes = {k: [round(b[0] / 2 - ox, 1), round(b[1] / 2 - oy, 1), round(b[2] / 2, 1), round(b[3] / 2, 1)] for k, b in boxes.items()}
    boxes = {"w": im.width, "h": im.height, "pieces": boxes}
    LAST_BOXES[threading.get_ident()] = boxes
    buf = io.BytesIO()
    if fmt == "png":
        im.save(buf, "PNG", optimize=size != "master")
    else:
        im.save(buf, "WEBP", quality=88 if size == "preview" else 95)
    data = buf.getvalue()
    if art_ok and not os.environ.get("CARDMAKER_NO_CACHE"):   # QA sweeps render thousands of cards: no cache writes
        cp.write_bytes(data); bp.write_text(json.dumps(boxes))
    return data, fmt


OPTIONS = {
    "sides": ["Light", "Dark"],
    "slip_types": ["Character", "Effect", "Immediate Effect", "Used Interrupt", "Lost Interrupt", "Used Or Lost Interrupt",
                   "Starting Interrupt", "Character Weapon", "Starship Weapon", "Device", "Starfighter", "Starship",
                   "Vehicle", "Creature", "Defensive Shield", "Site", "System", "Objective", "Epic Event", "Jedi Test", "Admiral's Order", "Podracer"],
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
                return self._json({"sets": SET_LIST, "types": TYPES, "expansions": EXP_LIST})
            if path == "/api/browse":
                g1 = lambda k: q.get(k, [""])[0]
                return self._json(browse(g1("set"), g1("side"), g1("type"), g1("exp")))
            if path.startswith("/api/card/") and path.rsplit("/", 1)[1] in OVS:
                gid = path.rsplit("/", 1)[1]
                spec = {k: v for k, v in OVS[gid].items() if k not in ("art", "art_back", "notes", "id")}
                spec["art"] = {"kind": "ovs", "gempId": gid}
                return self._json({"spec": spec, "art_sources": ["ovs", "upload", "none"], "art_urls": {}})
            if path.startswith("/api/card/"):
                gid = urllib.parse.unquote(path.rsplit("/", 1)[1])
                asked = gid
                if gid not in CARDS and gid in LEGACY_ALIAS:   # a GEMP id of a Virtual Legacy card (1210_124, 2210_110, pc-legacy:5521)
                    gid = LEGACY_ALIAS[gid]
                if gid not in CARDS:
                    return self._json({"error": "unknown card"}, 404)
                spec = adapter.gemp_to_spec(CARDS[gid])
                extra = {}
                lib_gid = gid
                if CARDS[gid].get("legacy") and gid in LEGACY_ART:
                    lib_gid = LEGACY_ART[gid]["gempId"]   # rev 71: the printed art = the Decipher card's library art
                    extra["art_match"] = LEGACY_ART[gid]
                lib = ART_MANIFEST.get(lib_gid, {}).get("status") == "ok"
                sys_card = spec.get("slip_type") == "System"   # a system's picture is the whole card: its own scan fits, a crop zooms
                spec["art"] = {"kind": "library" if lib and not sys_card else "scan", "gempId": lib_gid if lib and not sys_card else gid, "version": "orig"}
                if CARDS[gid].get("legacy"):
                    vers = LEGACY_VERSIONS.get(gid, [])
                    extra["versions"] = [{k: v for k, v in x.items() if k != "text"} for x in vers]
                    if LEGACY_NOTES.get(gid):
                        extra["version_notes"] = LEGACY_NOTES[gid]
                    # an Objective's back class (22xx_n_BACK) opens the same version as its front (gemp_back, V4-GAPS 2026-11-12)
                    want = q.get("version", [""])[0] or (asked if asked != gid and asked in {x.get(k) for x in vers for k in ("gemp", "gemp_back")} else "")
                    hit = next((x for x in vers if want and (want in (x["id"], x.get("code"), x.get("gemp"), x.get("gemp_back")) or want.lower() == (x.get("label") or "").lower())), None)
                    if want and not hit and any(want == x["id"] for x in LEGACY_NOTES.get(gid, [])):
                        return self._json({"error": f"{want!r} is not a version (capitals / punctuation only, waiting on Bill's ruling)",
                                           "versions": extra["versions"], "version_notes": LEGACY_NOTES[gid]}, 404)
                    if want and not hit:
                        return self._json({"error": f"unknown version {want!r}", "versions": extra["versions"]}, 404)
                    if hit:
                        implicit = not q.get("version", [""])[0]   # opened by the GEMP id that carries this version
                        adapter.apply_version(spec, hit, text=not (implicit and hit.get("icons_missing")))
                        extra["version"] = {k: v for k, v in hit.items() if k != "text"}
                        if implicit and hit.get("icons_missing"):
                            extra["note"] = ("the recorded text of this version lost its inline icons; the card's own text is shown "
                                             "(ask ?version=" + (hit.get("code") or "original") + " for the recorded text)")
                        elif hit.get("icons_missing"):
                            extra["warning"] = ("this version's recorded text lost its inline icons when it was read from the printed sheet: "
                                                "put them back (CardMaker codes such as {set:hoth} {alter}) in game_text before rendering")
                return self._json(dict({"spec": spec, "art_sources": (["library"] if lib else []) + ["scan", "upload", "none"],
                                   "art_urls": rg_art_urls(gid) if gid in _RG_IDS else ({"orig": f"{ART_CDN}/orig/{lib_gid}.png", "x4": f"{ART_CDN}/x4/{lib_gid}.webp"} if lib else {})}, **extra))
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
                bx = json.dumps(LAST_BOXES.pop(threading.get_ident(), {}))
                return self._send(200, data, f"image/{fmt}", {"Cache-Control": "no-store", "X-Piece-Boxes": bx,
                                                              "Access-Control-Expose-Headers": "X-Piece-Boxes"})
            return self._json({"error": "not found"}, 404)
        except Exception as e:   # noqa: BLE001
            traceback.print_exc(); return self._json({"error": str(e)}, 500)


if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8790
    print(f"cardmaker on :{port}, {len(CARDS)} cards, {len(ART_MANIFEST)} in art manifest", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
