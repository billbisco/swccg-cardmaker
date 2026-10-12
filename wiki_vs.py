"""Build the wiki hub page + the 50 card stubs for an Original Virtual Set from cards/vsN/NN.json.
Usage: python3 wiki_vs.py 3 out/vs3-wiki   → page.wiki, stubs/*.wiki, y-*.tsv"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VS = int(sys.argv[1]); YEAR = {1: 2002, 2: 2002, 3: 2002, 4: 2003, 5: 2003, 6: 2003, 7: 2004, 8: 2004}.get(VS, "2002–2008"); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True); (OUT / "stubs").mkdir(exist_ok=True)
SUBTITLES = {1: "Legacy", 2: "Our Most Desperate Hour", 3: "Revolution", 4: "Battle Of Hoth", 5: "A Dark Time", 6: "City In The Clouds",
             7: "Shadows Of The Empire", 8: "Jabba's Court", 9: "Sanctuary Moon", 10: "Fourth Anthology", 11: "Gathering Storm",
             12: "Martyrs & Magistrates", 13: "Remote Outpost", 14: "Armed & Operational", 15: "Galactic Frontier",
             16: "Revenge Of The Sith", 17: "The Force Unleashed"}
SETNAME = SUBTITLES[VS]
OLDSET = f"Virtual Set {VS} (Original)"            # pre-2026-10-12 wiki name (stub data is keyed on it)
SET = f"Virtual Set {VS}: {SETNAME}"                 # shared/swccg-card-identity
SUFFIX = f" (Virtual Set {VS}: {SETNAME})"
GEMPSET = f"11{VS:02d}"


def newtitle(old: str) -> str:
    return old.replace(f" (Virtual Set {VS})", SUFFIX) if old.endswith(f" (Virtual Set {VS})") else old
SHEET = {3: ("https://web.archive.org/web/20071024153955/http://www.swccgpc.com/Resources/VirtualCards3.pdf", "VirtualCards3.pdf", "24 October 2007", "4 December 2006")}[VS]
stubs = {int(v["image"][5:7]): (k, v) for k, v in json.load(open(ROOT / "gempdata/original-vs-stubs.json", encoding="utf-8")).items() if v["set"] == OLDSET}

TYPE_PAGE = {"EFFECT": ("Effect", None), "IMMEDIATE EFFECT": ("Effect", "Immediate Effect"), "USED INTERRUPT": ("Interrupt", "Used Interrupt"),
             "LOST INTERRUPT": ("Interrupt", "Lost Interrupt"), "USED OR LOST INTERRUPT": ("Interrupt", "Used or Lost Interrupt"),
             "DEFENSIVE SHIELD": ("Defensive Shield", None), "CHARACTER WEAPON": ("Weapon", "Character Weapon"), "AUTOMATED WEAPON": ("Weapon", "Automated Weapon")}
ICON_WORD = {"permanent-weapon": "[[Permanent Weapon]]", "lightsaber": "[[Permanent Weapon]]", "maintenance": "[Maintenance]", "republic": "[Maintenance]",
             "nav": "[[Nav Computer]]", "set": None}
COL_ICON = {"pilot": "[[Pilot]]", "warrior": "[[Warrior]]", "astromech": "Astromech"}


def pronoun(c):
    return "she" if any(w in c["title"] for w in ("Leia",)) else "he"


def expand(c: dict) -> str:
    """Slip shorthand → prose, following the sheet's ICON KEY (what GEMP's legacy texts do too)."""
    t = c["game_text"]
    for a, b in {"{icon:immune-alter}": "{alter}", "{icon:immune-control}": "{control}", "{icon:immune-sense}": "{sense}"}.items():
        t = t.replace(a, b)
    t = re.sub(r"\{pilot:(\d)\}, (\d): _Falcon_\.", lambda m: f"Adds {m.group(1)} to power of anything he pilots ({m.group(2)} if ''Falcon'').", t)
    t = re.sub(r"\{pilot:(\d)\}\.?", lambda m: f"Adds {m.group(1)} to power of anything {pronoun(c)} pilots.", t)
    t = t.replace(" is {alter}.", " is immune to Alter.")
    t = t.replace("{alter}", "(Immune to Alter.)").replace("{control}", "(Immune to Control.)").replace("{sense}", "(Immune to Sense.)")
    t = re.sub(r"\{set:anh\}", "[A New Hope]", t)
    t = re.sub(r"\{([\w-]+)\}", lambda m: ICON_WORD.get(m.group(1), f"[{m.group(1).title()}]"), t)
    # ▲ X / ▼ X — object runs to the next sentence end
    def tri(m):
        verb = "take" if m.group(1) == "▲" else "deploy"
        obj = m.group(2).strip()
        tail = " into hand from Reserve Deck; reshuffle" if verb == "take" else " from Reserve Deck; reshuffle"
        return f"{verb} {obj}{tail}{m.group(3)}"
    t = re.sub(r"([▲▼])\s*([^.?!\n]*?)([.?!])", tri, t)
    t = t.replace("(may deploy here from Reserve Deck; reshuffle.)", "(may deploy here from Reserve Deck; reshuffle).")
    t = re.sub(r"\*(.+?)\*", r"'''\1'''", t)
    t = re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"''\1''", t)
    t = re.sub(r"\s+\.", ".", t).replace("  ", " ")
    return t.replace("\n", "<br />")


def lore_wiki(l: str) -> str:
    l = re.sub(r"\*(.+?)\*", r"'''\1'''", l or "")
    return re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"''\1''", l)


rows = {"Light": [], "Dark": []}
tsv = []
for n in range(1, 51):
    c = json.loads((ROOT / f"cards/vs{VS}/{n:02d}.json").read_text(encoding="utf-8"))
    page, s = stubs[n]
    page = newtitle(page)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", c["title"].replace("•", "")).strip("_")
    rem = f"OVS{VS}-{n:02d}-{safe}-remaster.webp"
    banner = (c.get("card_type") or "").upper()
    if banner.startswith("STARFIGHTER"):
        typ, sub, model = "Starship", "Starfighter", banner.split(":", 1)[1].strip().title().replace("X-Wing", "X-wing")
    elif banner:
        typ, sub = TYPE_PAGE[banner]; model = ""
    else:
        typ, sub, model = "Character", (c.get("affiliation") or "").replace(" + ", "/"), ""
    sub_link = {"Alien/Rebel": "Alien"}.get(sub, sub)
    type_cell = f"[[{typ}]]" if not sub else f"[[{sub_link}|{sub}]]" if typ == "Character" else f"[[{sub_link}|{sub}]]"
    gt = expand(c)
    stats = dict(c.get("stats") or [])
    icons = " ".join(COL_ICON.get(i, i.title()) for i in c.get("icons") or [])
    if c.get("scomp"):
        icons = (icons + " [[Scomp Link]]").strip()
    base = c.get("base_page") or ""
    base_link = f"[[{base}]]" if base else ""
    uniq = s.get("uniqueness") or "Unrestricted"
    stub = f"""{{{{Card
|title={s['title']}
|card_uid={GEMPSET}_{n}
|image={rem}
|image2={s['image']}
|side={c['side']}
|type={typ}
|subtype={sub}
|subtype_link={sub_link}
|model={model}
|set={SET}
|rarity=
|uniqueness={uniq}
|destiny={c.get('destiny') or ''}
|power={stats.get('POWER', '')}
|ability={stats.get('ABILITY', '')}
|maneuver={stats.get('MANEUVER', '')}
|hyperspeed={stats.get('HYPERSPEED', '')}
|deploy={c.get('deploy') or ''}
|forfeit={c.get('forfeit') or ''}
|icons={icons}
|version_label=virtual
|set_band=Virtual
|prev={newtitle(s.get('prev') or '')}
|next={newtitle(s.get('next') or '')}
|lore={lore_wiki(c.get('lore'))}
|game_text={gt}
|printings='''{SET}''' (slip {n:02d}) — this page
|sources=* [{SHEET[0]} {SHEET[1]}] (Players Committee Remaster sheet, Internet Archive {SHEET[2]}) — official text as of {SHEET[3]}; slip {n:02d}. Slip image and game text from this sheet.
* Lore and art: the printed Decipher card, {base_link or 'see hatnote'}.
* Full-card remaster: [[{SET}#Cards|{SET}]] (fan reconstruction, 2026).
|hatnote=For the Decipher card this slip modifies, see {base_link or 'the set page'}. Code OVS{VS} · GEMP id {GEMPSET}_{n}.
}}}}

[[Category:Virtual Original sets]]
"""
    fn = OUT / "stubs" / (re.sub(r"[^A-Za-z0-9]+", "_", page) + ".wiki")
    fn.write_text(stub, encoding="utf-8"); tsv.append(f"{page}\t{OUT.name}/stubs/{fn.name}")
    rows[c["side"]].append(f"|-\n| {n:02d} || [[File:{s['image']}|320px|link={page}]] || [[File:{rem}|200px|link={page}]] || style=\"white-space:nowrap\" | [[{page}|{s['title']}]] || style=\"white-space:nowrap\" | {type_cell} || {gt}")


def table(side):
    return "{| class=\"wikitable\" style=\"width:auto\"\n! # !! Slip !! Remaster !! Card !! Type !! Game text\n" + "\n".join(rows[side]) + "\n|}"


page = f"""{{{{Hatnote|1=The {YEAR} Players Committee set, numbered before the 2009 reorganisation (code OVS{VS}). For the post-2014 set numbered {VS} see [[Virtual Set {VS}]].}}}}
{{| class="wikitable expansion-infobox"
! colspan="2" | {SET}
|-
| colspan="2" style="text-align:center;" | [[File:VS{VS}O-pack.png|200px]]<br />[[File:VS{VS}O-set-symbol.png|48px]]
|-
! Code
|| OVS{VS} · GEMP set {GEMPSET}
|-
! Publisher
|| [[Players Committee|Star Wars CCG Players Committee]]
|-
! Era
|| [[:Category:Virtual Original sets|Virtual Original]] (2002–2009)
|-
! Legal
|| 20 September 2002<ref name="cdn">[https://res.starwarsccg.org/legacyblocks/VirtualCards{VS}.pdf VirtualCards{VS}.pdf] (starwarsccg.org CDN) — 2002 slip sheet with the legal date.</ref>
|-
! Remaster sheet
|| Official text as of {SHEET[3]}; errata to #39 on 28 July 2007<ref name="ia">[{SHEET[0]} {SHEET[1]}] (swccgpc.com, Internet Archive {SHEET[2]}) — the December 2006 Remaster sheet: cover, set symbol and the slips shown below.</ref>
|-
! Cards
|| 50 (25 Light, 25 Dark)
|}}

'''Virtual Set {VS}: {SETNAME}''' is the third of the [[Virtual Sets (2002-2009)|numbered Virtual Sets]] the [[Players Committee]] released between 2002 and 2009. Each of its 50 cards is a printed slip that replaces the bottom half of a [[Decipher]] card (new game text, stats and icons) while the card's title, lore and art stay as printed. The set became tournament-legal on 20 September 2002.<ref name="cdn" /> In December 2006 the Committee reissued it as a ''Remaster'' sheet with new pack art, a set symbol and the final text; that sheet is the source for the slips shown here.<ref name="ia" /> Icons used on the slips are explained at [[Virtual card icons]].

The second image in each row is a full-card remaster: the printed Decipher card with the slip re-typeset at 600 DPI in the style of the Committee's later Holotable cards, made for the wiki in 2026 (see [[Typography of Star Wars CCG cards]]). These are fan reconstructions, not Committee products. Game text is written out the way the sheet's icon key defines its shorthand.

== Cards ==
=== [[Light|Light Side]] ===
{table('Light')}

=== [[Dark|Dark Side]] ===
{table('Dark')}

== See also ==
* [[Virtual Sets (2002-2009)]] · [[History of the Players Committee]]
* [[Virtual card icons]] · [[Defensive Shields]] · [[Virtual Shields]]

== References ==
<references />

[[Category:Virtual Original sets]]
[[Category:Sets]]
"""
(OUT / "page.wiki").write_text(page, encoding="utf-8")
tsv.insert(0, f"{SET}\t{OUT.name}/page.wiki")
moves = [f"{OLDSET}|{SET}", f"Talk:{OLDSET}|Talk:{SET}"] + [f"{k}|{newtitle(k)}" for k, v in stubs.values()]
(OUT / "moves.txt").write_text("\n".join(moves) + "\n", encoding="utf-8")
(OUT / f"y-vs{VS}wiki.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")
print(len(tsv), "pages")
