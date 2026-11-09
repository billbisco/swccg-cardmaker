#!/usr/bin/env python3
"""Build gempdata/legacy_versions.json from the Virtual Legacy version record (STANDARD rev 71, rev 72).

  python3 tools/legacy/build_versions.py <ai-team-skills>/shared/gemp-legacy-cards/versions/legacy-versions-v4.json \
      [--gemp <swccg-gemp clone> [--ref origin/master] [--ref <open PR head> …]]

Writes {"aliases": {GEMP id -> legacy card id}, "versions": {legacy card id -> [version, ...]},
        "notes": {legacy card id -> [held text, ...]}}:
- aliases: the current GEMP card (12xx / 601_x / pc-legacy:<PC id>), every 22xx version card and every retired 22xx id
  (blueprintMapping.txt) -> `<set>_L<PC id>`
- versions (only entries with `is_version: true`), in order (original, PC-E1, PC-E2 …, v4 `version_seq`): id, code,
  label, kind, date, part, seq, gemp (the GEMP card that carries that text), latest, wiki, text, and icons_missing = true
  when the transcription dropped inline icons (printed-sheet texts read from the PDFs: "( ) , ,"). Render those only
  with the icons put back (--text), never as they stand.
- rev 73: stat-only versions (`part: stats`, e.g. Jedi Survivor (V) PC-E1 destiny 1 -> 3) are versions too, and every
  version carries the stats it records (`stats`: destiny, power …) for the API to print.
- notes: v4 entries with `is_version: null` (capitals / punctuation only, waiting on Bill): shown, never selectable.

The 22xx id of a version comes from swccg-gemp itself (`--gemp`): each set22xx class's
`setLegacyVersion(new LegacyVersion("<current id>", "<label>", …))` names the current card and the version code
("" = original). GEMP picks the number by the order versions were added (`n`, `n + 1000`, … docs/legacy-versions.md),
so it is read, never computed. Later `--ref`s override earlier ones (an open batch PR over master). Without `--gemp`
the record's own `gemp_22xx` is used (it can be stale: v4 still lists 2261_10 as PC-E1).
"""
import argparse, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument("record")
ap.add_argument("--gemp", help="swccg-gemp clone")
ap.add_argument("--ref", action="append", help="git ref(s) to read, later wins (default origin/master)")
a = ap.parse_args()
rec = json.load(open(a.record, encoding="utf-8"))

CARDS_DIR = "src/gemp-swccg-cards/src/main/java/com/gempukku/swccgo/cards/"
MAPPING = "src/gemp-swccg-cards/src/main/resources/blueprintMapping.txt"
gemp_ver: dict = {}      # (current id, code or "") -> 22xx id
retired: dict = {}       # retired 22xx id -> current id
gemp_refs = []
if a.gemp:
    git = lambda *x: subprocess.run(["git", "-C", a.gemp, *x], capture_output=True, text=True, check=True).stdout
    for ref in a.ref or ["origin/master"]:
        sha = git("rev-parse", ref).strip()
        gemp_refs.append(f"{ref} {sha[:9]}")
        files = [p for p in git("ls-tree", "-r", "--name-only", ref, CARDS_DIR).splitlines()
                 if re.search(r"/set22\d\d/\w+/Card22\d\d_\d+\w*\.java$", p)]
        batch = subprocess.run(["git", "-C", a.gemp, "cat-file", "--batch"], input="".join(f"{ref}:{p}\n" for p in files).encode(),
                               capture_output=True, check=True).stdout
        pos = 0
        for p in files:
            head_end = batch.index(b"\n", pos)
            size = int(batch[pos:head_end].split()[2])
            src = batch[head_end + 1: head_end + 1 + size].decode("utf-8", "replace")
            pos = head_end + 1 + size + 1
            m = re.search(r"Card(22\d\d)_(\d+)(\w*)\.java$", p)
            bid = f"{m.group(1)}_{int(m.group(2))}{m.group(3)}"
            lv = re.search(r'new\s+LegacyVersion\(\s*"([^"]+)"\s*,\s*"([^"]*)"', src)
            if lv:
                gemp_ver[(lv.group(1), lv.group(2))] = bid
        for line in git("show", f"{ref}:{MAPPING}").splitlines():
            x = line.strip().split(",")
            if len(x) == 2 and re.fullmatch(r"22\d\d_\d+\w*", x[0]):
                retired[x[0]] = x[1]
    # a 22xx id retired on a later ref beats a class still present on an earlier one
    gemp_ver = {k: v for k, v in gemp_ver.items() if v not in retired}

leg = {}
for side in ("Light", "Dark"):
    for c in json.load(open(ROOT / f"gempdata/{side}Legacy.json", encoding="utf-8"))["cards"]:
        leg[c["id"]] = f"{c['set']}_L{c['id']}"
# two spaces after a sentence end are the 2012-13 card list's style, not a lost icon
MISSING = re.compile(r"\(\s*\)|,\s*,|\(•\)\s*,|\s[A-Z]\s*$|(?<![.!?:)\"'”’])\s{2,}|\[[A-Za-z]+-[A-Za-z-]+-\d+\]"
                     r"|\s[.,;:](?=\s|$)|\[W\d*-\d+\]")   # rev 73: "adds one and one ." / "always A ." / [W2-205] (an icon read as a word)
STAT_KEYS = ("destiny", "power", "ability", "deploy", "forfeit", "armor", "maneuver", "hyperspeed", "landspeed", "politics")
aliases, versions, notes, unused = {}, {}, {}, set(gemp_ver.values())
by_current = {}
for gid, f in rec.items():
    if gid.startswith("_") or not isinstance(f, dict) or not f.get("pc_id"):
        continue
    lid = leg.get(f["pc_id"])
    if not lid:
        continue
    by_current[gid] = lid
    aliases[gid] = lid
    aliases[f"pc-legacy:{f['pc_id']}"] = lid   # card_labels.json's key for cards not yet coded in GEMP
    if f.get("pc_gemp_id"):
        aliases[str(f["pc_gemp_id"])] = lid
    out, held = [], []
    for v in f.get("versions") or []:
        stat_only = (v.get("part") == "stats")   # rev 73: a stat-only change (Jedi Survivor (V) destiny 1 -> 3) is a version (Bill, B34)
        if not v.get("text") or not (v.get("text_known") or stat_only):
            continue
        if v.get("is_version") is None:   # capitals / punctuation only: Bill has not ruled; a note, not a version
            held.append({"id": v["id"], "date": v.get("date"), "part": v.get("part"), "change": v.get("change"),
                         "reason": v.get("needs_bill_reason") or "waiting on Bill", "text": v["text"]})
            continue
        if not v.get("is_version"):
            continue
        code = v.get("version_code")
        if a.gemp:
            g22 = [gemp_ver[(gid, code or "")]] if (gid, code or "") in gemp_ver else []   # is_latest is per part: match by code
        else:
            g22 = [x["blueprint"] for x in (v.get("gemp_22xx") or []) if x.get("blueprint")]
        for b in g22:
            aliases[b] = lid
            unused.discard(b)
        seq = v.get("version_seq")
        out.append({"id": v["id"], "code": code, "label": "Original" if not code else code, "kind": v.get("kind"),
                    "date": v.get("date"), "part": v.get("part"), "seq": seq, "latest": bool(v.get("is_latest")),
                    "gemp": g22[0] if g22 else (gid if v.get("is_latest") else None),
                    "wiki": v.get("wiki_page"), "icons_missing": bool(MISSING.search(v["text"])), "text": v["text"]})
        st = {k: v[k] for k in STAT_KEYS if v.get(k) is not None}   # printed stats the version records (destiny …)
        if st:
            out[-1]["stats"] = st
    out.sort(key=lambda x: (x["seq"] if x["seq"] is not None else 99, x["part"] or ""))
    versions[lid] = out
    if held:
        notes[lid] = held
for b, cur in retired.items():   # retired version ids: old decks still load them as the current card
    if cur in by_current:
        aliases.setdefault(b, by_current[cur])
if unused:
    print("GEMP version classes with no matching record version:", sorted(unused))
    for (cur, code), b in gemp_ver.items():
        if b in unused and cur in by_current:
            aliases.setdefault(b, by_current[cur])
json.dump({"_meta": {"source": "swccg-guild legacy-versions-v%s.json (%s)" % (rec.get("_about", {}).get("version", "?"),
                                                                             rec.get("_about", {}).get("built", "")),
                     "gemp": gemp_refs or "record gemp_22xx", "tool": "tools/legacy/build_versions.py"},
           "aliases": dict(sorted(aliases.items())), "versions": dict(sorted(versions.items())),
           "notes": dict(sorted(notes.items()))},
          open(ROOT / "gempdata/legacy_versions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
n = sum(len(v) for v in versions.values())
print(len(aliases), "aliases,", n, "versions,", sum(x["icons_missing"] for v in versions.values() for x in v),
      "with icons missing,", sum(len(v) for v in notes.values()), "held notes,",
      sum(1 for v in versions.values() for x in v if x["gemp"] and x["gemp"].startswith("22")), "with a 22xx card")
