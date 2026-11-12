"""Regression check (rev 74): Virtual Legacy line breaks against the PC's own.

For every card in gempdata/legacy_typeset.json whose current text has the same words as the PC master-list text,
render it (no art) and compare the words on each line of game text and lore with the PC's lines.

    PLAYWRIGHT_BROWSERS_PATH=... python3 tools/legacy/typeset/check_typeset.py [--cards 1008_L5562,...] [--limit N] [--json out.json]

CM_PC_HINTS=0 turns off the stored PC line breaks, so the check measures the typesetting rules alone (what a new
version text gets); with them on, every card whose text is the master list's must match exactly.
"""
import json, os, re, sys, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "webapp")); os.chdir(ROOT)
os.environ.setdefault("CARDMAKER_DATA", "/tmp/cardmaker-data")
import server, adapter, build_vs, render   # noqa: E402

def words(s):
    s = s.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    out = []
    for w in s.split():
        w = re.sub(r"[^A-Za-z0-9]", "", w).lower()
        if w and not re.fullmatch(r"[stu]", w):   # Wingdings3 ▲ ▼ glyphs read as S / T / U
            out.append(w)
    return out

def strip_codes(s):
    s = re.sub(r"\{pilot:([^}]*)\}", r" \1", s or "")
    return re.sub(r"\{[^}]*\}", " ", s).replace("*", "").replace("_", " ")

JS = """(sel) => { const el = document.querySelector(sel); if (!el) return null;
  const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const rows = []; let n;
  while ((n = tw.nextNode())) { const t = n.textContent; const re = /\\S+/g; let m;
    while ((m = re.exec(t))) { const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
      const b = r.getClientRects()[0]; if (!b) continue; rows.push([Math.round(b.top + b.height / 2), m[0]]); } }
  rows.sort((a, b) => a[0] - b[0]); const lines = [];
  for (const [y, w] of rows) { if (lines.length && Math.abs(lines[lines.length - 1][0] - y) < 20) lines[lines.length - 1][1].push(w); else lines.push([y, [w]]); }
  return {lines: lines.map(l => l[1].join(' ')), fit: el.dataset.fit}; }"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cards"); ap.add_argument("--limit", type=int); ap.add_argument("--json"); ap.add_argument("--off", action="store_true", help="the renderer without the PC typesetting (baseline)")
    a = ap.parse_args()
    TS = json.load(open("gempdata/legacy_typeset.json", encoding="utf-8"))["cards"]
    ids = a.cards.split(",") if a.cards else sorted(TS)
    if a.limit: ids = ids[:a.limit]
    from playwright.sync_api import sync_playwright
    res = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1632, "height": 2220})
        for gid in ids:
            if gid not in server.CARDS: continue
            spec = adapter.gemp_to_spec(server.CARDS[gid])
            if a.off: spec["pc_typeset"] = False
            card = adapter.spec_to_card(dict(spec, _art=None, _art_kind=None, _set_icon_file=None), build_vs)
            card.pop("art", None)
            rec = {"gid": gid, "title": spec.get("title"), "template": card["template"]}
            todo = []
            # the master list prints one of the card's recorded texts: use the one with the PDF's words
            pdfw = words(" ".join((TS[gid].get("gt") or {}).get("lines") or []))
            if pdfw and words(strip_codes(spec.get("game_text"))) != pdfw:
                for v in server.LEGACY_VERSIONS.get(gid, []):
                    s2 = dict(spec); adapter.apply_version(s2, v)
                    if a.off: s2["pc_typeset"] = False
                    if words(strip_codes(s2.get("game_text"))) == pdfw:
                        spec = s2; rec["version"] = v.get("code") or v.get("label"); break
                card = adapter.spec_to_card(dict(spec, _art=None, _art_kind=None, _set_icon_file=None), build_vs); card.pop("art", None)
            for blk, sel, field in (("gt", ".gt", "game_text"), ("lore", ".lore", "lore")):
                pdf = (TS[gid].get(blk) or {}).get("lines")
                if not pdf or not spec.get(field): continue
                if words(" ".join(pdf)) != words(strip_codes(spec[field])):
                    rec[blk] = "text differs"; continue
                todo.append((blk, sel, pdf))
            if todo:
                html = render.build_html(card)
                for attempt in range(3):
                    try:
                        pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(60); break
                    except Exception:   # Chromium in a small sandbox crashes now and then: new page, try again
                        try: pg.close()
                        except Exception: pass
                        pg = b.new_page(viewport={"width": 1632, "height": 2220})
                for blk, sel, pdf in todo:
                    got = pg.evaluate(JS, sel)
                    ours = [words(l) for l in (got or {}).get("lines", [])]
                    theirs = [words(l) for l in pdf]
                    ours = [l for l in ours if l]; theirs = [l for l in theirs if l]
                    rec[blk] = "ok" if ours == theirs else "breaks differ"
                    if ours != theirs:
                        rec[blk + "_ours"] = [" ".join(l) for l in ours]; rec[blk + "_pc"] = [" ".join(l) for l in theirs]
                    rec[blk + "_fit"] = (got or {}).get("fit")
            res.append(rec)
        b.close()
    for blk in ("gt", "lore"):
        c = {}
        for r in res:
            if blk in r: c[r[blk]] = c.get(r[blk], 0) + 1
        print(blk, c)
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
