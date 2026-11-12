#!/usr/bin/env python3
"""Build a Japanese sample spec (STANDARD rev 80) from a wiki page "<Card> (Japanese)".

  python3 tools/japanese/make_sample.py "Astromech Shortage (Japanese)" [...] [--out tools/japanese/samples]

The English card (the page's Printing ID 13xx_n -> n_n) gives frame, icons, stats, destiny, deploy / forfeit; the page
gives the Japanese title, game text and lore and the printed face (`_scan`). Line breaks are not on the wiki: read them
off the scan and add `lore_lines` / `text_breaks` by hand (compare_ja.py shows the scan beside the render).
"""
import argparse, html, json, re, sys, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "webapp")]
UA = {"User-Agent": "swccg-cardmaker make_sample"}
JA_SETS = {"1301": "1", "1302": "2", "1303": "3"}


def wikitext(title: str) -> str:
    q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "wikitext", "format": "json"})
    return json.load(urllib.request.urlopen(urllib.request.Request("https://wiki.swccg.com/api.php?" + q, headers=UA), timeout=60))["parse"]["wikitext"]["*"]


def section(t: str, name: str) -> str | None:
    m = re.search(r"<h2>" + re.escape(name) + r"</h2>\s*(.*?)(?=<h2>|\Z)", t, re.S)
    if not m:
        return None
    s = re.findall(r'<span lang="ja">(.*?)</span>', m.group(1), re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", "".join(s))).strip() if s else None


def build(title: str) -> dict:
    import server, adapter
    t = wikitext(title)
    pid = re.search(r"(?:Printing|GEMP) ID</th><td><code>(\d+)_(\d+)", t)
    gid = f"{JA_SETS[pid.group(1)]}_{pid.group(2)}"
    spec = adapter.gemp_to_spec(server.CARDS[gid])
    spec["_en_title"] = spec.get("title", "")
    lib = server.ART_MANIFEST.get(gid, {}).get("status") == "ok"
    spec["art"] = {"kind": "library" if lib and spec.get("slip_type") != "System" else "scan", "gempId": gid, "version": "orig"}
    for key, sec in (("title", "Title"), ("game_text", "Card Text"), ("lore", "Lore")):
        v = section(t, sec)
        if v:
            spec[key] = v
    m = re.search(r"<h2>Card Text</h2>(.*?)(?=<h2>)", t, re.S)
    halves = dict(re.findall(r"'''(Light|Dark) Side:'''\s*<span lang=\"ja\">(.*?)</span>", m.group(1) if m else "", re.S))
    if not halves and spec.get("slip_type") in ("Site", "System") and re.match(r"^(ライトサイド|ダークサイド)：", spec.get("game_text") or ""):
        # rev 83: some pages give one Japanese block, "ライトサイド：…ダークサイド：…" (a half printed blank is left out)
        jm = re.match(r"^(?:ライトサイド：(.*?))?(?:ダークサイド：(.*))?$", spec.get("game_text") or "", re.S)
        if jm and (jm.group(1) is not None or jm.group(2) is not None):
            halves = {"Light": jm.group(1) or "", "Dark": jm.group(2) or ""}
    if halves:   # a location: the Light half is game_text, the Dark half dark_text (as in the English spec)
        spec["game_text"] = html.unescape(halves.get("Light", "")).strip()
        spec["dark_text"] = html.unescape(halves.get("Dark", "")).strip()
    dots = len(re.match(r"^[•●]*", server.CARDS[gid].get("front", server.CARDS[gid]).get("title", "") or "").group(0)) or \
        len(re.match(r"^[•●]*", spec.get("_en_title", "")).group(0))
    if dots and not re.match(r"^[＊•*]", spec.get("title", "")):
        spec["title"] = "＊" * dots + spec["title"]   # the wiki's Japanese title often leaves out the printed ＊
    spec["language"] = "ja"
    spec["_scan"] = re.search(r'card-portrait">\[\[File:([^|\]]+)', t).group(1)
    spec["_page"] = title
    return spec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="+")
    ap.add_argument("--out", default=str(Path(__file__).parent / "samples"))
    a = ap.parse_args()
    for p in a.pages:
        s = build(p)
        name = re.sub(r"[^a-z0-9]+", "_", p.replace("(Japanese)", "").lower()).strip("_")
        f = Path(a.out) / f"{name}.json"
        f.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f, s["_scan"], s.get("slip_type"), s.get("card_type"))


if __name__ == "__main__":
    main()
