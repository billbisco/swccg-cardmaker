"""Set/Thumbs wiki page from the art library (Bill 2026-10-14, after the LOTR TCG wiki's Thumbs tab): for every card
on the set page, the printed art crop next to its RealESRGAN x4plus upscale.

    python3 thumbs_page.py "Cloud City Limited" OUTDIR

Reads the set page's card list (rows "| [[File:CC-L-name.gif|…|link=Page]] || [[Page|Title]] || [[Type|Type]] || R || …"),
matches each row to the library by side + file name, and writes OUTDIR/page.wiki plus OUTDIR/up/ with
Art-<file stem>.png (original crop) and Art-<file stem>-x4.webp (upscale).
"""
from __future__ import annotations
import json, re, shutil, sys, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "library"
UA = {"User-Agent": "HolocronClaude/1.0 (thumbs)"}


def main():
    title, out = sys.argv[1], Path(sys.argv[2])
    (out / "up").mkdir(parents=True, exist_ok=True)
    raw = urllib.request.urlopen(urllib.request.Request(
        "https://wiki.swccg.com/index.php?" + urllib.parse.urlencode({"title": title, "action": "raw"}), headers=UA)).read().decode()
    man = json.loads((LIB / "manifest-all.json").read_text())
    by = {}
    for g, e in man.items():
        folder, name = re.search(r"/cards/([^/]+)/large/([^/.]+)\.", e["imageUrl"]).groups()
        by.setdefault((e["side"][0], name), []).append(g)
    rows = {"L": [], "D": []}; missing = []
    side = "L"
    for line in raw.splitlines():
        if line.startswith("=== ") and "Dark" in line: side = "D"
        m = re.match(r"\| \[\[File:([^|\]]+)\|[^\]]*link=([^\]]+)\]\] \|\| (\[\[[^\]]+\]\]) \|\| (\[\[[^\]]+\]\]) \|\| ([^|]*)\|\|", line)
        if not m:
            continue
        fn, page, cardlink, typelink, rarity = m.groups()
        stem = fn.rsplit(".", 1)[0]
        sd, name = stem.split("-")[-2], stem.split("-")[-1]
        gs = by.get((sd, name), [])
        g = next((x for x in gs if (LIB / "orig" / f"{x}.png").exists()), None)
        if not g:
            missing.append(stem); rows[sd].append(f"|-\n| [[File:{fn}|120px|link={page}]] || colspan=\"2\" | ''art not cut yet'' || {cardlink} || {typelink}"); continue
        o = f"Art-{stem}.png"; x = f"Art-{stem}-x4.webp"
        shutil.copy(LIB / "orig" / f"{g}.png", out / "up" / o)
        has_x4 = (LIB / "x4" / f"{g}.webp").exists()
        if has_x4:
            shutil.copy(LIB / "x4" / f"{g}.webp", out / "up" / x)
        cell_x = f"[[File:{x}|300px|link=File:{x}]]" if has_x4 else "''upscale pending''"
        rows[sd].append(f"|-\n| [[File:{fn}|120px|link={page}]] || [[File:{o}|300px|link=File:{o}]] || {cell_x} || {cardlink} || {typelink}")
    head = ("{| class=\"wikitable\" style=\"width:auto\"\n! Card !! Original art (printed scan) !! Upscaled (RealESRGAN ×4) !! Name !! Type\n")
    page = f"""{{{{Set tabs|{title}}}}}
'''Thumbs''' shows the artwork of every [[{title}]] card, cut from the printed card's scan, next to an AI-upscaled
copy (RealESRGAN x4plus, 4× the scan's resolution). The original crop is the reference: the upscale invents fine
detail the scan does not hold and can smooth faces. Click an image for the full-size file.

== [[Light|Light Side]] ==
{head}{chr(10).join(rows['L'])}
|}}

== [[Dark|Dark Side]] ==
{head}{chr(10).join(rows['D'])}
|}}

[[Category:Card art thumbs]]
"""
    (out / "page.wiki").write_text(page, encoding="utf-8")
    print(len(rows["L"]) + len(rows["D"]), "rows;", len(missing), "without art:", missing[:10])


if __name__ == "__main__":
    main()
