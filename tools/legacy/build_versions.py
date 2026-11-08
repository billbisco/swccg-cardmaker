#!/usr/bin/env python3
"""Build gempdata/legacy_versions.json from the Virtual Legacy version record (STANDARD rev 71).

  python3 tools/legacy/build_versions.py <ai-team-skills>/shared/gemp-legacy-cards/versions/legacy-versions-v3.json

Writes {"aliases": {GEMP id -> legacy card id}, "versions": {legacy card id -> [version, ...]}}:
- aliases: the current GEMP card (12xx / 601_x / pc-legacy:<PC id>) and every 22xx version card -> `<set>_L<PC id>`
- versions: id, code (PC-E1 …), label, kind, date, part, gemp (the GEMP card that carries that text), latest, text, and
  icons_missing = true when the transcription dropped inline icons (printed-sheet texts read from the PDFs: "( ) , ,").
  Render those only with the icons put back (--text), never as they stand.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
rec = json.load(open(sys.argv[1], encoding="utf-8"))
leg = {}
for side in ("Light", "Dark"):
    for c in json.load(open(ROOT / f"gempdata/{side}Legacy.json", encoding="utf-8"))["cards"]:
        leg[c["id"]] = f"{c['set']}_L{c['id']}"
MISSING = re.compile(r"\(\s*\)|,\s*,|\(•\)\s*,|\s[A-Z]\s*$|\s{2,}|\[[A-Za-z]+-[A-Za-z-]+-\d+\]")
aliases, versions = {}, {}
for gid, f in rec.items():
    if gid.startswith("_") or not isinstance(f, dict) or not f.get("pc_id"):
        continue
    lid = leg.get(f["pc_id"])
    if not lid:
        continue
    aliases[gid] = lid
    aliases[f"pc-legacy:{f['pc_id']}"] = lid   # card_labels.json's key for cards not yet coded in GEMP
    if f.get("pc_gemp_id"):
        aliases[str(f["pc_gemp_id"])] = lid
    out = []
    for v in f.get("versions") or []:
        if not v.get("is_version") or not v.get("text_known") or not v.get("text"):
            continue
        g22 = [x["blueprint"] for x in (v.get("gemp_22xx") or []) if x.get("blueprint")]
        for b in g22:
            aliases[b] = lid
        out.append({"id": v["id"], "code": v.get("version_code"), "label": v.get("label"), "kind": v.get("kind"),
                    "date": v.get("date"), "part": v.get("part"), "latest": bool(v.get("is_latest")),
                    "gemp": g22[0] if g22 else (gid if v.get("in_gemp_now") else None),
                    "wiki": v.get("wiki_page"), "icons_missing": bool(MISSING.search(v["text"])), "text": v["text"]})
    versions[lid] = out
json.dump({"_meta": {"source": "swccg-guild legacy-versions-v3.json (" + rec.get("_about", {}).get("built", "") + ")",
                     "tool": "tools/legacy/build_versions.py"},
           "aliases": dict(sorted(aliases.items())), "versions": dict(sorted(versions.items()))},
          open(ROOT / "gempdata/legacy_versions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
n = sum(len(v) for v in versions.values())
print(len(aliases), "aliases,", n, "versions,", sum(x["icons_missing"] for v in versions.values() for x in v), "with icons missing")
