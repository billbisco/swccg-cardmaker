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
META = {   # per set: Remaster sheet (IA url, file, IA capture date, "official text as of"), legal date + its source, ordinal, remaster note
    1: dict(sheet=("https://web.archive.org/web/20071024153847/http://www.swccgpc.com/Resources/VirtualCards1.pdf", "VirtualCards1.pdf", "24 October 2007", "4 December 2006"),
            legal="9 March 2002", legal_ref="[https://web.archive.org/web/20020611031545/http://decipher.com/starwars/cardlists/index.html Decipher Star Wars CCG cardlists index] (Internet Archive, 11 June 2002) — \"Virtual Card Set #1 – 12 cards. Tournament-legal 03-09-02.\"",
            ordinal="first", remaster="the December 2006 ''Legacy'' sheet: cover, set symbol and the slips shown below", pack="VS1-Legacy-pack.png", symbol="VS1-Legacy-set-symbol.png",
            title_fix={1: "BoShek (V)"}, already_renamed=True,
            carry_fix={"|| Later redesign || Later PC packaging proxies || Gap flagged: virtual-slips CDN Cloudflare-blocked; Legacy Block 1 <code>-pre.gif</code> proxies (not 2002 Premium).": "|| Virtual Block 1 || The same twelve slips reissued as [[Virtual Block 1]] cards after the 2009 reorganisation || <code>VB1-…-pre.gif</code> card images",
                       "Premium+Decipher composites (File:VS1O-*-composite.png) exist separately; composite QA is paused. This gallery is hub-only slip comparison across printable styles.": "",
                       "Same twelve titles appear in multiple printable packaging styles. ": "The same twelve titles appear in several printable packaging styles.",
                       "Premium slip sheet (PC 2002 branding; PDF distill Feb 2005 on local copy)": "Premium slip sheet (PC 2002 branding)",
                       "! Card !! 1A / early !! Premium !! Later (Block-era proxy)": "! Card !! 1A / early !! Premium !! Virtual Block 1",
                       "(composite overlays; card-page thumbs now use Legacy slip crops)": ""}),
    2: dict(sheet=("https://web.archive.org/web/20071024153738/http://www.swccgpc.com/Resources/VirtualCards2.pdf", "VirtualCards2.pdf", "24 October 2007", "4 December 2006"),
            legal="1 June 2002", legal_ref="[https://res.starwarsccg.org/legacyblocks/VirtualCards2.pdf VirtualCards2.pdf] (starwarsccg.org CDN) — 2002 slip sheet with the legal banner: tournament-legal 1 June 2002, Regional 8 June 2002.",
            ordinal="second", remaster="the December 2006 Remaster sheet: cover, set symbol and the slips shown below; errata to #34 on 28 July 2007", pack="VS2O-pack.png", symbol="VS2O-set-symbol.png",
            title_fix={}, already_renamed=True,
            carry_fix={"Do not invent card text on this stub.": "", "Light/Dark same-name slips (Sandcrawler, Utinni!) are disambiguated in page titles.": ""}),
    4: dict(sheet=("https://web.archive.org/web/20071024153629/http://www.swccgpc.com/Resources/VirtualCards4.pdf", "VirtualCards4.pdf", "24 October 2007", "4 December 2006"),
            legal="5 February 2003", legal_ref="[https://res.starwarsccg.org/legacyblocks/VirtualCards4.pdf VirtualCards4.pdf] (starwarsccg.org CDN) — 2003 slip sheet with the legal banner.",
            ordinal="fourth", remaster="the December 2006 Remaster sheet: cover, set symbol and the slips shown below", pack="VS4O-pack.png", symbol="VS4O-set-symbol.png",
            title_fix={}, already_renamed=True,
            carry_fix={"Do not invent card text on this stub.": "", "Do not collapse launch packaging and the Remaster sheet into one unverified gloss: keep launch (or earliest documented presence) separate from the Remaster cover used here for pack and set-symbol art.": ""}),
    3: dict(sheet=("https://web.archive.org/web/20071024153955/http://www.swccgpc.com/Resources/VirtualCards3.pdf", "VirtualCards3.pdf", "24 October 2007", "4 December 2006"),
            legal="20 September 2002", legal_ref="[https://res.starwarsccg.org/legacyblocks/VirtualCards3.pdf VirtualCards3.pdf] (starwarsccg.org CDN) — 2002 slip sheet with the legal date.",
            ordinal="third", remaster="the December 2006 Remaster sheet: cover, set symbol and the slips shown below; errata to #39 on 28 July 2007", pack="VS3O-pack.png", symbol="VS3O-set-symbol.png",
            title_fix={}, already_renamed=True),
}[VS]
SHEET = META["sheet"]
NCARDS = len(list((ROOT / f"cards/vs{VS}").glob("[0-9][0-9].json")))
stubs = {int(v["image"][5:7]): (k, v) for k, v in json.load(open(ROOT / "gempdata/original-vs-stubs.json", encoding="utf-8")).items() if v["set"] == OLDSET}
CARRY = Path(sys.argv[3]).read_text(encoding="utf-8") if len(sys.argv) > 3 else ""   # current hub page: its history sections are carried over

TYPE_PAGE = {"EFFECT": ("Effect", None), "IMMEDIATE EFFECT": ("Effect", "Immediate Effect"), "USED INTERRUPT": ("Interrupt", "Used Interrupt"),
             "LOST INTERRUPT": ("Interrupt", "Lost Interrupt"), "USED OR LOST INTERRUPT": ("Interrupt", "Used or Lost Interrupt"),
             "DEFENSIVE SHIELD": ("Defensive Shield", None), "CHARACTER WEAPON": ("Weapon", "Character Weapon"), "AUTOMATED WEAPON": ("Weapon", "Automated Weapon"),
             "DEVICE": ("Device", None), "UTINNI EFFECT": ("Effect", "Utinni Effect"), "TRANSPORT VEHICLE": ("Vehicle", "Transport"),
             "COMBAT VEHICLE": ("Vehicle", "Combat"), "CREATURE VEHICLE": ("Vehicle", "Creature"), "SHUTTLE VEHICLE": ("Vehicle", "Shuttle"),
             "POLITICAL EFFECT": ("Effect", "Political Effect"), "MOBILE EFFECT": ("Effect", "Mobile Effect"), "EPIC EVENT": ("Epic Event", None),
             "STARTING INTERRUPT": ("Interrupt", "Starting Interrupt"), "OBJECTIVE": ("Objective", None), "ADMIRAL'S ORDER": ("Admiral's Order", None),
             "VEHICLE WEAPON": ("Weapon", "Vehicle Weapon"), "STARSHIP WEAPON": ("Weapon", "Starship Weapon"), "SNOW CREATURE": ("Creature", None),
             "CREATURE": ("Creature", None)}
ICON_WORD = {"permanent-weapon": "[[Permanent Weapon]]", "lightsaber": "[[Permanent Weapon]]", "maintenance": "[Maintenance]", "republic": "[Maintenance]",
             "nav": "[[Nav Computer]]", "set": None, "independent": "[Independent]", "presence": "[Presence]", "ovs": "[Virtual]"}
COL_ICON = {"pilot": "[[Pilot]]", "warrior": "[[Warrior]]", "astromech": "Astromech", "permanent-pilot": "[[Permanent Pilot]]", "nav": "[[Nav Computer]]"}


def pronoun(c):
    return "she" if any(w in c["title"] for w in ("Leia",)) else "he"


def expand(c: dict) -> str:
    """Slip shorthand → prose, following the sheet's ICON KEY (what GEMP's legacy texts do too)."""
    t = c["game_text"]
    for a, b in {"{icon:immune-alter}": "{alter}", "{icon:immune-control}": "{control}", "{icon:immune-sense}": "{sense}", "{icon:virtual-set symbol}": "{ovs}"}.items():
        t = t.replace(a, b)
    t = re.sub(r"\{pilot:(\d)\}, (\d): _Falcon_\.", lambda m: f"Adds {m.group(1)} to power of anything he pilots ({m.group(2)} if ''Falcon'').", t)
    t = re.sub(r"\{pilot:(\d)\}\.?", lambda m: f"Adds {m.group(1)} to power of anything {pronoun(c)} pilots.", t)
    t = t.replace(" is {alter}.", " is immune to Alter.").replace("non-{alter}", "non-[Immune to Alter]").replace("{ovs} ", "[Virtual] ")
    t = t.replace("{alter}", "(Immune to Alter.)").replace("{control}", "(Immune to Control.)").replace("{sense}", "(Immune to Sense.)")
    t = re.sub(r"\{set:anh\}", "[A New Hope]", t)
    t = t.replace("{icon:maintenance-star}", "★").replace("{icon:maintenance-skull}", "☠")
    t = re.sub(r"\{([\w-]+)\}", lambda m: ICON_WORD.get(m.group(1), f"[{m.group(1).title()}]"), t)
    # ▲ X / ▼ X — object runs to the next sentence end
    def tri(m):
        verb = "take" if m.group(1) == "▲" else "deploy"
        obj = m.group(2).strip()
        tail = " into hand from Reserve Deck; reshuffle" if verb == "take" else " from Reserve Deck; reshuffle"
        return f"{verb} {obj}{tail}{m.group(3)}"
    t = re.sub(r"([▲▼])\s*([^.?!\n]*?)([.?!])", tri, t)
    t = re.sub(r"(^|[.?!]\s+|\bOR\s+|\n)(take|deploy)\b", lambda m: m.group(1) + m.group(2).capitalize(), t)
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
extra_gallery = {}
moves = [] if META["already_renamed"] else [f"{OLDSET}|{SET}", f"Talk:{OLDSET}|Talk:{SET}"] + [f"{k}|{newtitle(k)}" for k, v in stubs.values()]
def page_of(n):
    pg = newtitle(stubs[n][0])
    return META["title_fix"][n] + pg[pg.index(" (V)") + 4:] if n in META["title_fix"] else pg


for n in range(1, NCARDS + 1):
    c = json.loads((ROOT / f"cards/vs{VS}/{n:02d}.json").read_text(encoding="utf-8"))
    page, s = stubs[n]
    page = newtitle(page)
    if n in META["title_fix"]:   # stub titled differently from the printed card (e.g. "Bo Shek" → "BoShek")
        s = dict(s, title=META["title_fix"][n])
        old_page, page = page, META["title_fix"][n] + page[page.index(" (V)") + 4:]
        moves.append(f"{old_page}|{page}")
    safe = re.sub(r"[^A-Za-z0-9]+", "_", c["title"].replace("•", "")).strip("_")
    rem = f"OVS{VS}-{n:02d}-{safe}-remaster.webp"
    banner = (c.get("card_type") or "").upper()
    banner = banner.replace("_", "")
    st = (c.get("slip_type") or "").lower()
    if st == "objective" or c.get("game_text_back"):
        typ, sub, model, banner = "Objective", "", "", "OBJECTIVE"
    elif st == "site":
        typ, sub, model, banner = "Location", "Site", "", "SITE"
    elif "creature" in st and "vehicle" not in st:
        typ, sub, model = "Creature", "", ""
    elif banner.startswith("STARFIGHTER") or banner.startswith("CAPITAL") or banner.startswith("SQUADRON"):
        typ, sub, model = "Starship", banner.split(":", 1)[0].strip().title(), banner.split(":", 1)[1].strip().title().replace("X-Wing", "X-wing").replace("Tie/Ln", "TIE/ln")
    elif "VEHICLE" in banner and "WEAPON" not in banner:
        typ, sub = "Vehicle", banner.split(":", 1)[0].replace("VEHICLE", "").strip().title()
        model = banner.split(":", 1)[1].strip().title().replace("At-At", "AT-AT").replace("At-St", "AT-ST") if ":" in banner else ""
    elif banner:
        typ, sub = TYPE_PAGE[banner]; model = ""
    else:
        typ, sub, model = "Character", (c.get("affiliation") or "").replace(" + ", "/"), ""
    sub_link = {"Alien/Rebel": "Alien"}.get(sub, sub)
    if typ == "Vehicle":
        sub_link = "Vehicle"
    if typ == "Creature" and banner:
        sub, sub_link, model = "", "", banner.title()
    type_cell = f"[[{typ}]]" if not sub else f"[[{sub_link}|{sub}]]" if typ == "Character" else f"[[{sub_link}|{sub}]]"
    gt = expand(c)
    rem2, slip2 = "", ""
    if c.get("game_text_back"):
        safe_b = re.sub(r"[^A-Za-z0-9]+", "_", (c.get("title_back") or "").replace("•", "")).strip("_")
        rem2 = f"OVS{VS}-{n:02d}b-{safe_b}-remaster.webp"
        slip2 = s.get("image2") or f"VS{VS}O-{n:02d}-{safe_b}.png"
        gt = f"'''{c.get('destiny') or '0'} side – {c['title'].replace('•', '')} (V)'''<br />{gt}<br /><br />'''{c.get('destiny_back') or '7'} side – {c.get('title_back')} (V)'''<br />{expand(dict(c, game_text=c['game_text_back']))}"
    if c.get("dark_text") and (c.get("slip_type") or "").lower() == "site":
        gt = f"'''Light:''' {gt}<br />'''Dark (printed):''' {expand(dict(c, game_text=c['dark_text']))}"
    extra_gallery[page] = f"<gallery mode=\"packed\" heights=\"180\">\nFile:{s['image']}|{c['title'].replace('•', '')} (V) slip\nFile:{slip2}|{c.get('title_back')} (V) slip\n</gallery>\n" if rem2 else ""
    stats = dict(c.get("stats") or [])
    icons = " ".join(COL_ICON.get(i, i.title()) for i in c.get("icons") or [])
    if c.get("scomp"):
        icons = (icons + " [[Scomp Link]]").strip()
    base = c.get("base_page") or ""
    base_link = f"[[{base}]]" if base else ""
    uniq = c.get("uniqueness") or s.get("uniqueness") or "Unrestricted"
    stub = f"""{{{{Card
|title={s['title']}
|card_uid={GEMPSET}_{n}
|image={rem}
|image2={rem2 or s['image']}{chr(10) + '|image2_layout=responsive' if rem2 else ''}
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
|armor={stats.get('ARMOR', '')}
|hyperspeed={stats.get('HYPERSPEED', '')}
|landspeed={stats.get('LANDSPEED', '')}
|deploy={c.get('deploy') or ''}
|forfeit={c.get('forfeit') or ''}
|icons={icons}
|light_icons={' '.join(i.title() for i in c.get('light_icons') or [])}
|dark_icons={' '.join(i.title() for i in c.get('dark_icons') or [])}
|version_label=virtual
|set_band=Virtual
|prev={page_of(n - 1) if n > 1 else ''}
|next={page_of(n + 1) if n < NCARDS else ''}
|lore={lore_wiki(c.get('lore'))}
|game_text={gt}
|printings='''{SET}''' (slip {n:02d}) — this page
|sources=* [{SHEET[0]} {SHEET[1]}] (Players Committee Remaster sheet, Internet Archive {SHEET[2]}) — official text as of {SHEET[3]}; slip {n:02d}. Slip image and game text from this sheet.
* Lore and art: the printed Decipher card, {base_link or 'see hatnote'}.
* Full-card remaster: [[{SET}#Cards|{SET}]] (fan reconstruction, 2026).
|hatnote=For the Decipher card this slip modifies, see {base_link or 'the set page'}. Code OVS{VS} · GEMP id {GEMPSET}_{n}.
}}}}

{extra_gallery.get(page, '')}[[Category:Virtual Original sets]]
"""
    fn = OUT / "stubs" / (re.sub(r"[^A-Za-z0-9]+", "_", page) + ".wiki")
    fn.write_text(stub, encoding="utf-8"); tsv.append(f"{page}\t{OUT.name}/stubs/{fn.name}")
    slip_cell = f"[[File:{s['image']}|320px|link={page}]]" + (f"<br />[[File:{slip2}|320px|link={page}]]" if slip2 else "")
    rem_cell = f"[[File:{rem}|200px|link={page}]]" + (f" [[File:{rem2}|200px|link={page}]]" if rem2 else "")
    rows[c["side"]].append(f"|-\n| {n:02d} || {slip_cell} || {rem_cell} || style=\"white-space:nowrap\" | [[{page}|{s['title']}]] || style=\"white-space:nowrap\" | {type_cell} || {gt}")
    # the slips of an Objective's back go on the stub as a gallery below the Card template


DROP_LINES = ("QA paused", "QA is paused", "Do not collapse", "normalized to the same display size", "Card-list thumbs use", "Individual card pages use")


def carried() -> str:
    """History/provenance sections of the current hub page, kept under == History == (everything except the card list,
    sources, set-symbol gallery and the old hub boilerplate)."""
    if not CARRY:
        return ""
    keep, out = False, []
    for line in CARRY.splitlines():
        m = re.match(r"^== (.+?) ==$", line)
        if m:
            keep = m.group(1).strip() not in ("Card list", "Sources", "See also", "References", "Set symbol and pack example", "Cards")
            if keep:
                out.append(f"=== {m.group(1).strip()} ===")
            continue
        if keep and not any(x in line for x in DROP_LINES):
            out.append(line)
    text = "\n".join(out).strip()
    for a, b in META.get("carry_fix", {}).items():
        text = text.replace(a, b)
    return f"== History ==\n{text}\n\n" if text else ""


def table(side):
    return "{| class=\"wikitable\" style=\"width:auto\"\n! # !! Slip !! Remaster !! Card !! Type !! Game text\n" + "\n".join(rows[side]) + "\n|}"


page = f"""{{{{Hatnote|1=The {YEAR} Players Committee set, numbered before the 2009 reorganisation (code OVS{VS}). For the post-2014 set numbered {VS} see [[Virtual Set {VS}]].}}}}
{{| class="wikitable expansion-infobox"
! colspan="2" | {SET}
|-
| colspan="2" style="text-align:center;" | [[File:{META['pack']}|200px]]<br />[[File:{META['symbol']}|48px]]
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
|| {META['legal']}<ref name="legal">{META['legal_ref']}</ref>
|-
! Remaster sheet
|| Official text as of {SHEET[3]}<ref name="ia">[{SHEET[0]} {SHEET[1]}] (swccgpc.com, Internet Archive {SHEET[2]}) — {META['remaster']}.</ref>
|-
! Cards
|| {NCARDS} ({len(rows['Light'])} Light, {len(rows['Dark'])} Dark)
|}}

'''Virtual Set {VS}: {SETNAME}''' is the {META['ordinal']} of the [[Virtual Sets (2002-2009)|numbered Virtual Sets]] the [[Players Committee]] released between 2002 and 2009. Each of its {NCARDS} cards is a printed slip that replaces the bottom half of a [[Decipher]] card (new game text, stats and icons) while the card's title, lore and art stay as printed. The set became tournament-legal on {META['legal']}.<ref name="legal" /> In December 2006 the Committee reissued it as a ''Remaster'' sheet with new pack art, a set symbol and the final text; that sheet is the source for the slips shown here.<ref name="ia" /> Icons used on the slips are explained at [[Virtual card icons]].

The second image in each row is a full-card remaster: the printed Decipher card with the slip re-typeset at 600 DPI in the style of the Committee's later Holotable cards, made for the wiki in 2026 (see [[Typography of Star Wars CCG cards]]). These are fan reconstructions, not Committee products. Game text is written out the way the sheet's icon key defines its shorthand.

== Cards ==
=== [[Light|Light Side]] ===
{table('Light')}

=== [[Dark|Dark Side]] ===
{table('Dark')}

{carried()}== See also ==
* [[Virtual Sets (2002-2009)]] · [[History of the Players Committee]]
* [[Virtual card icons]] · [[Defensive Shields]] · [[Virtual Shields]]

== References ==
<references />

[[Category:Virtual Original sets]]
[[Category:Sets]]
"""
(OUT / "page.wiki").write_text(page, encoding="utf-8")
tsv.insert(0, f"{SET}\t{OUT.name}/page.wiki")
(OUT / "moves.txt").write_text("\n".join(moves) + "\n", encoding="utf-8")
(OUT / f"y-vs{VS}wiki.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")
print(len(tsv), "pages")
