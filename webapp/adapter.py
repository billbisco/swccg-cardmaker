"""Card maker: turn a card from the Players Committee's card JSON (swccg-card-json, as GEMP uses it) into an editable
card spec, and turn a spec into a render.py card dict.

A *spec* is the same shape as the remaster transcriptions (cards/vsN/NN.json, see cards/VS-SPEC.md): human-level
fields (title, side, slip_type, card_type, stats, game_text, icons, ...) plus an `art` choice. The web UI edits specs;
AIs and batch jobs can write them directly.
"""
from __future__ import annotations
import re

SETS = {   # GEMP set id -> expansion name as build_vs.SET_ICON knows it (ring sphere right of the lore box)
    "1": "Premiere", "2": "A New Hope", "3": "Hoth", "4": "Dagobah", "5": "Cloud City", "6": "Jabba's Palace",
    "7": "Special Edition", "8": "Endor", "9": "Death Star II", "10": "Reflections II", "11": "Tatooine",
    "12": "Coruscant", "13": "Reflections III", "14": "Theed Palace", "101": "Premiere", "102": "Jedi Pack",
    "103": "Jedi Pack", "104": "Premium", "106": "Official Tournament Sealed Deck", "108": "Premium",
    "109": "Enhanced Cloud City", "110": "Enhanced Jabba's Palace", "111": "Premium", "112": "Jabba's Palace Sealed Deck",
}

EXPANSION_NAMES = {"A New Hope", "Hoth", "Dagobah", "Cloud City", "Jabba's Palace", "Special Edition", "Endor",
                   "Death Star II", "Reflections II", "Tatooine", "Coruscant", "Reflections III", "Theed Palace", "Premium"}
YEAR = {"1": 1995, "2": 1996, "3": 1996, "4": 1997, "5": 1997, "6": 1998, "7": 1998, "8": 1998, "9": 2000, "10": 2000,
        "11": 2001, "12": 2001, "13": 2001, "14": 2001, "101": 1996, "102": 1996, "103": 1997, "104": 1997, "106": 1998,
        "108": 1998, "109": 1998, "110": 1998, "111": 1998, "112": 1999}


def copyright_for(set_id) -> str:
    """The vertical Lucasfilm / Decipher line printed beside the art (format as on the scans, cf. VS specs)."""
    sid = str(set_id or "")
    if (sid.isdigit() and 200 <= int(sid) <= 299) or sid == "200d":
        return "ARTWORK NEITHER AFFILIATED WITH NOR ENDORSED BY LUCASFILM LTD."   # the modern PC cards (I Want That Map)
    y = YEAR.get(sid)
    if not y:
        return ""
    if y >= 2000:
        return f"© {y} LUCASFILM LTD. & TM. TM, ® & © {y} DECIPHER INC."
    return f"TM & © {y} LUCASFILM LTD. TM, ® & © {y} DECIPHER INC."


def set_mark_for(set_id) -> str | None:
    """The Players Committee's set mark in the lower icon slot: modern Virtual Sets 0-27 (ring + number) and the 2009
    Virtual Blocks 1-9 (diamond)."""
    s = str(set_id or "")
    if s == "301":      # Virtual Premium: gold "P" (Asajj Ventress With Lightsabers)
        return "pc:P"
    if s == "200d":     # Virtual Defensive Shields: the gold ring with D (A Close Race (V), Don't Do That Again (V))
        return "pc:D"
    if s == "1000d":    # Virtual Block shields: the diamond with D (Affect Mind (V))
        return "vb:D"
    if s.isdigit() and 200 <= int(s) <= 299:
        return f"pc:{int(s) - 200}"
    if s.isdigit() and 1001 <= int(s) <= 1009:
        return f"vb:{int(s) - 1000}"
    return None


INLINE = {   # GEMP's bracketed icon names in game text -> renderer tokens
    "[Immune to Alter.]": "{alter}", "[Immune to Alter]": "{alter}", "[Immune to Sense.]": "{sense}",
    "[Immune to Sense]": "{sense}", "[Immune to Control.]": "{control}", "[Immune to Control]": "{control}",
    "[Episode I]": "{episode1}", "[Light Side Force]": "{light-force}", "[Dark Side Force]": "{dark-force}",
    "[Maintenance]": "{maintenance}", "[Independent]": "{independent}", "[Grabber]": "{grabber}",
    "[Republic]": "{icon:republic}", "[Pilot]": "{icon:pilot}", "[Warrior]": "{icon:warrior}",
    "[Permanent Weapon]": "{permanent-weapon}", "[Permanent weapon]": "{permanent-weapon}", "[permanent weapon]": "{permanent-weapon}",
    "[maintenance]": "{maintenance}", "[Presence]": "{presence}", "[Nav Computer]": "{nav}",
    "[Light Side]": "{light-force}", "[Dark Side]": "{dark-force}",
    # Players Committee Game Aid icons (assets/icons/pc-gameaid-named, from their Feb 2024 reference sheet)
    "[Episode VII]": "{ga:episode-vii-sequel-era}", "[Clone Army]": "{ga:clone-army}", "[Separatist]": "{ga:separatist}",
    "[Independent Starship]": "{ga:independent-starship}", "[First Order]": "{ga:first-order}",
    "[Resistance]": "{ga:resistance}", "[Trade Federation]": "{ga:trade-federation}", "[Skywalker]": "{ga:skywalker-theme}",
    "[Sidious]": "{ga:sidious-theme}", "[Selective Creature]": "{ga:selective-creature}", "[Virtual]": "{ga:virtual}",
    "[Scoundrel]": "{ga:scoundrel}", "[Setup]": "{ga:setup}", "[Vader]": "{ga:vader}",
    # spellings (and typos) found in the PC data by the QA sweep (2026-10-15)
    "[Presence Droid]": "{presence}", "[Droid with Presence]": "{presence}", "[Light side]": "{light-force}",
    "[Light Side Icon]": "{light-force}", "[Dark Side Force icon]": "{dark-force}", "[Dark Side Icon]": "{dark-force}",
    "[Restistance]": "{ga:resistance}", "[Clone Army Icon]": "{ga:clone-army}", "[Permenant Weapon]": "{permanent-weapon}",
    "[Pemanent Weapon]": "{permanent-weapon}", "[Seperatists icon]": "{ga:separatist}", "[Seperatist]": "{ga:separatist}",
    "[Selective]": "{ga:selective-creature}", "[Defensive Shield]": "{ga:defensive-shield}",
    "[Endor icon]": "{set:endor}", "[Coruscant Icon]": "{set:coruscant}", "[Jabba's Place]": "{set:jabbaspalace}",
    "[Ref 3]": "{set:reflections3}", "[Reflection 3]": "{set:reflections3}", "[Virtural Block 7]": "{vb:7}",
}
SET_TOKENS = {"A New Hope": "anh", "Hoth": "hoth", "Dagobah": "dagobah", "Cloud City": "cloudcity",
              "Jabba's Palace": "jabbaspalace", "Special Edition": "se", "Endor": "endor", "Death Star II": "ds2",
              "Reflections II": "reflections2", "Reflections 2": "reflections2", "Reflections III": "reflections3",
              "Reflections 3": "reflections3", "Coruscant": "coruscant", "Theed Palace": "theed", "Tatooine": "tatooine",
              "Death Star 2": "ds2", "Endor Icon": "endor", "JP": "jabbaspalace", "Premium": "premium"}

ICON_COL = {"Pilot": "pilot", "Warrior": "warrior", "Nav Computer": "nav", "Permanent Weapon": "permanent-weapon",
            "Permanent weapon": "permanent-weapon", "Independent": "independent", "Presence": "presence",
            "Astromech": "astromech", "Permanent Pilot": "permanent-pilot", "Episode I": "episode1",
            "Selective Creature": "selective-creature", "Selective": "selective-creature", "Independent Starship": "independent-starship",
            "Trade Federation": "trade-federation", "Clone Army": "clone-army", "Separatist": "separatist",
            "Resistance": "resistance", "First Order": "first-order", "Vader": "vader", "Republic": "republic"}
FACTION = {"independent", "independent-starship", "trade-federation", "clone-army", "separatist", "resistance",
           "first-order", "republic", "vader"}
RING = {"Episode I": "episode1", "Episode VII": "episode7", "Sidious": "sidious", "Skywalker": "skywalker"}
LOC_ICON = {"Planet": "planet", "Interior": "interior", "Exterior": "exterior", "Mobile": "mobile",
            "Underground": "underground", "Underwater": "underwater", "Starship": "starship", "Vehicle": "vehicle",
            "Scomp Link": "scomp", "Space": "space"}


def dedupe(label: str) -> str:
    """PC data typos repeat the class word: "Jedi Knight Knight", "Assassin Droid Droid"."""
    return re.sub(r"\b(\w+)(\s+\1)+$", r"\1", str(label or ""), flags=re.I)


def game_text(t: str) -> str:
    t = t or ""
    t = t.replace("/\\", "▲").replace("\\/", "▼")
    t = t.replace("<>", "◊")
    t = t.replace("(*)", "(•)").replace("*", "✶")   # the PC data marks bold with {…}: a raw asterisk is the printed star (Attack Run's footnote)   # the PC data's ASCII diamond (<>Spaceport City)   # ASCII arrows in a few PC texts (Don't Do That Again (V))
    t = re.sub(r"\{([A-Za-z][A-Za-z' ]*)\}", r"*\1*", t)   # GEMP marks bold words {Flip}; the renderer bolds *...*
    t = re.sub(r"\{([^{}]*\s[^{}]*)\}", lambda m: "_" + m.group(1).strip() + "_", t)   # long {…} runs = italic (Jabba's Prize)
    for k, v in INLINE.items():
        t = t.replace(k, v)
    for name, key in SET_TOKENS.items():
        t = t.replace(f"[{name}]", f"{{set:{key}}}")
    t = re.sub(r"[\[(]Virtual Block (\d)[\])]", r"{vb:\1}", t)   # also "(Virtual Block 8)" in a few legacy texts
    t = re.sub(r"\(Reflections? (3|III)\)", "{set:reflections3}", t)   # the 2009 Virtual Block diamonds
    t = re.sub(r"\[Set (\d{1,2})\]", r"{pcset:\1}", t)     # the modern Virtual Set marks
    return t


PRINTING_TAGS = r"V|AI|[^()\[\]]*\bAI\b[^()\[\]]*|Premium|Light|Dark|Tatooine|Coruscant|Reflections I{1,3}|Death Star II|Cloud City|Endor|Hoth|Dagobah|Special Edition|Jabba's Palace|A New Hope|Theed Palace|Premiere|Errata|ALT"


def strip_printing(t: str) -> str:
    prev = None
    while prev != t:
        prev = t
        t = re.sub(rf"\s*[(\[](?:{PRINTING_TAGS})[)\]](?=\s*(?:/|&|$))", "", t, flags=re.I)   # "(V)", "(v)", "[v]"
    return t


def ship_italics(title: str) -> str:
    """Decipher italicises a starship's proper name in its title (•_Mist Hunter_, •_Home One_, Han, Chewie, And The
    _Falcon_, Boba Fett In _Slave I_) but not call signs, squadrons or possessives (•Gold 4, •Luke's T-16 Skyhopper)."""
    m = re.match(r"^(•*)(.*)$", title); bul, name = m.group(1), m.group(2)
    if "_" in name or len(bul) > 1:
        return title
    plain = lambda s: not re.search(r"\d|'s\b|\b(Garrison|Squadron|Shuttle|Escort|Fighter|Leader|Flagship)\b", s)
    if " In " in name:
        a, b = name.rsplit(" In ", 1)
        return f"{bul}{a} In _{b}_" if plain(b) else title
    if " And The " in name:
        a, b = name.rsplit(" And The ", 1)
        return f"{bul}{a} And The _{b}_" if plain(b) else title
    if name.startswith("Flagship ") and plain(name[9:]):   # •Flagship _Executor_
        return f"{bul}Flagship _{name[9:]}_"
    if not bul or "," in name or " & " in name or not plain(name):
        return title
    return f"{bul}_{name}_"


LEGACY_SHIELD_FADE = {'1000d_L6077', '1000d_L6595', '1000d_L6369', '1000d_L5981', '1000d_L6008', '1000d_L5319', '1000d_L6047', '1000d_L6299'}
UNDERCOVER_FRAME = {"7_48", "215_20", "110_1", "1009_L5394", "223_32", "206_4", "2_107"}   # printed on the opponent's frame
CAPTIVE_ART = {"200_16", "205_14"}
CAPTIVE_NOART = {"10_42", "1006_L5620"}   # Jabba's Prize: no art window
SHIP_NAMES: set = set()   # unique starship/vehicle proper names (from the italic titles; filled by the server)
SHIP_EXTRA = {"Rand Ecliptic", "Ecliptic", "Falcon", "Hound's Tooth", "Tantive IV", "Slave I"}
SHIP_AMBIGUOUS = {"Victory", "Liberty", "Independence", "Infinity", "Phantom", "Conquest", "Endurance", "Redemption",
                  "Defiance", "Resolute", "Ghost", "Luminous", "Spiral", "Profundity", "Steadfast", "Supremacy", "Overseer",
                  "Rogue One", "Blockade Support Ship"}
_SHIP_RE = None


def ship_text(t: str) -> str:
    """Decipher italicises starship names in lore and game text too (Han Solo: "When piloting _Falcon_")."""
    global _SHIP_RE
    if not t or not SHIP_NAMES:
        return t
    if _SHIP_RE is None:
        names = sorted((SHIP_NAMES | SHIP_EXTRA) - SHIP_AMBIGUOUS, key=len, reverse=True)
        _SHIP_RE = re.compile(r"(?<![\w_•-])(" + "|".join(re.escape(n) for n in names) + r")(?![\w_-])(?! \d| Squadron)")
    parts = re.split(r"((?<![A-Za-z0-9])_.+?_(?![A-Za-z0-9]))", t)   # leave already-italic runs alone
    return "".join(p if i % 2 else _SHIP_RE.sub(r"_\1_", p) for i, p in enumerate(parts))


def maintenance(t: str) -> str:
    """Reflections III maintenance costs, as printed: ✱ Use 2 or [flag] Lose 1 or [skull]."""
    t = re.sub(r"Use (\d+)(?: Force)? to maintain", r"{icon:maintenance-star}Use \1", t)
    t = re.sub(r" OR Lose (\d+)(?: Force)? to place in Used Pile", r" or {icon:maintenance-flag} Lose \1", t)
    t = re.sub(r" OR Place out of play", r" or {icon:maintenance-skull}", t)
    return t


def pc_shorthand(t: str) -> str:
    """The Players Committee prints its own shorthand (Game Aid sheet): the card JSON spells it out."""
    t = re.sub(r"Adds (\d|one|two|three) to (?:the )?power of anything (?:he|she|it) pilots\.", lambda m: "{pilot:%s}." % {"one": "1", "two": "2", "three": "3"}.get(m.group(1), m.group(1)), t)
    t = re.sub(r"(?i)\bdeploy ([^.;()]+?) from (?:your )?Reserve Deck(?:; reshuffle)?", r"▼ \1", t)
    t = re.sub(r"(?i)\btake ([^.;()]+?) into hand from (?:your )?Reserve Deck(?:; reshuffle)?", r"▲ \1", t)
    t = t.replace("(Immune to {alter}.)", "{alter}")
    t = re.sub(r"\(Immune to (Sense|Control)\.?\)", lambda m: "{%s}" % m.group(1).lower(), t).replace("(Immune to Alter.)", "{alter}")
    return t


def quotes(t: str) -> str:
    """The PC JSON writes printed double quotes as single ones: 'Vehicle with armor' -> “Vehicle with armor”."""
    return re.sub(r"(?<![\w])'(.+?)'(?![\w])", "\u201c\\1\u201d", t)


BASE_ICONS: dict = {}   # title -> icons of the original Decipher printing (filled by the server)
BASE_LOC: dict = {}   # location title -> (Light, Dark) Force icons of the PC data's printing (filled by the server)
BASE_EXP: dict = {}   # title -> Decipher expansion of the original printing (filled by the server)


def gemp_to_spec(c: dict) -> dict:
    f = c["front"]
    side = c["side"]
    typ = f.get("type") or ""
    sub = f.get("subType") or ""
    icons = []
    if c.get("legacy") and f.get("icons") is None and f.get("type") not in ("Location",):
        # Virtual Block data often omits the icons: the original card's expansion / Episode I icons still print (He Always Wins!)
        f = dict(f, icons=[i for i in BASE_ICONS.get(re.sub(r"[^a-z0-9]", "", strip_printing(f.get("title") or "").lower().replace("•", "")), []) if i in RING or i in EXPANSION_NAMES or i in ("Reflections 2", "Reflections 3")])
    for i in f.get("icons") or []:   # "Warrior x2" = two icons (Tonnika Sisters)
        mm = re.match(r"(.+?)\s+x(\d)$", i)
        icons += [mm.group(1)] * int(mm.group(2)) if mm else [i]
    title = strip_printing(f.get("title") or "").replace("<>", "◊")   # "(V)", "(AI)", "(Premium)", "(Tatooine)" … name the printing, not the card
    if typ != "Objective" and "/" in title:   # flip cards (Jabba's Prize, The Falcon, Junkyard Garbage): this side's title
        a, _, b = title.partition(" / ") if " / " in title else title.partition("/")
        if " / " in title or a.replace("•", "").strip().lower() == b.replace("•", "").strip().lower():
            title = a.strip()
    if typ in ("Starship", "Vehicle"):
        title = ship_italics(title)
    exp = SETS.get(str(c.get("set")))
    # the black caption strip is blank by default (Bill 2026-10-15): only some PC virtual cards print text there
    spec = {"_printed_stats": f.get("printedStats"), "side": side, "title": title, "caption": "", "number": "", "destiny": f.get("destiny") or "",
            "lore": "" if (f.get("lore") or "").strip().rstrip(".") == "Blank" else (f.get("lore") or ""), "game_text": game_text(f.get("gametext")), "icons": [], "stats": [],
            "deploy": f.get("deploy"), "forfeit": f.get("forfeit"), "scomp": "Scomp Link" in icons,
            "affiliation": None, "expansion": exp, "card_type": "", "gempId": c.get("gempId"),
            "source": {"gempId": c.get("gempId"), "imageUrl": f.get("imageUrl"), "set": c.get("set")},
            "copyright": copyright_for(c.get("set")), "set_mark": set_mark_for(c.get("set"))}
    if c.get("legacy"):   # 2009-2014 Virtual Blocks print "•Title (V)" in the bottom strip (Holotable faces)
        spec["caption"] = (f.get("title") or "").replace("<>", "◊")
        if typ == "Defensive Shield":
            # the Virtual Defensive Shields reuse their original card's frame (QA vs the Holotable scans, 2026-10-15):
            # Episode I-style red→cyan with the green swirl (Affect Mind (V), After Her! (V)), else Decipher's cyan
            spec["shield_style"] = "fade" if c.get("gempId") in LEGACY_SHIELD_FADE else "decipher"
    if not spec.get("expansion"):   # PC virtual cards print the base card's expansion sphere (Blockade Support Ship: Coruscant)
        for i in icons:
            nm = {"Reflections 2": "Reflections II", "Reflections 3": "Reflections III", "Premium": "Premium"}.get(i, i)
            if nm in EXPANSION_NAMES:
                spec["expansion"] = nm; break
    sid = str(c.get("set") or "")
    pc_era = (sid.isdigit() and (200 <= int(sid) <= 399 or int(sid) >= 1000)) or sid in ("200d", "1000d")
    if not spec.get("expansion") and pc_era:   # (V) cards keep the original card's sphere (Overseeing It Personally (V): DS2)
        spec["expansion"] = BASE_EXP.get(re.sub(r"[^a-z0-9]", "", title.lower().replace("•", "")))
    spec["lore"] = quotes(spec["lore"])
    if typ != "Objective" and "/" in (f.get("title") or "") and title != strip_printing(f.get("title") or ""):   # flip card text joined to the other side's: "…unpiloted).May not…"
        spec["game_text"] = re.split(r"(?<=[.)!])(?=[A-Z•])", spec["game_text"], maxsplit=1)[0]
    spec["game_text"] = ship_text(maintenance(quotes(spec["game_text"])))
    spec["lore"] = ship_text(re.sub(r"\{([A-Za-z][A-Za-z' ]*)\}", r"*\1*", spec["lore"]))   # {leader} = bold in lore
    if c.get("gempId") in UNDERCOVER_FRAME:   # undercover spies print on the other side's frame (TK-422, Boushh, U-3PO)
        spec["side_frame"] = "Dark" if side == "Light" else "Light"
    if c.get("gempId") in CAPTIVE_NOART:
        spec["side_frame"] = "Light"; spec["captive_noart"] = True
    if c.get("gempId") in CAPTIVE_ART:   # carbonite captives (The Mythrol, Luke Skywalker, The Emperor's Prize): printed
        # on the Light character frame with no lore box; the art runs down to a raised stat bar over a tall text box
        spec["side_frame"] = "Light"
        spec["no_lore_box"] = True; spec["text_grow"] = 330; spec["text_grow_scan"] = True; spec["grow_keep_frame"] = True
    if not spec["lore"].strip() and (" & " in title or c.get("legacy")) and typ in ("Interrupt", "Effect", "Defensive Shield"):
        # Reflections II combo cards print no lore box: the art runs from the title bar to a raised banner and the text
        # box grows by the same amount (Evader & Monnok, Do, Or Do Not & Wise Advice)
        spec["no_lore_box"] = True; spec["text_grow_scan"] = True
        spec["text_grow"] = 0 if (side == "Dark" and typ == "Effect") else 290   # the Dark Effect combo frame is already tall
        if typ == "Defensive Shield":
            spec["grow_keep_frame"] = True   # shield combos keep the shield frame (A Useless Gesture & Death Star Sentry)
    if pc_era:
        spec["game_text"] = pc_shorthand(spec["game_text"])
    spec["game_text"] = re.sub(r"\s+(LOST|STARTING|USED):", r"\n\1:", spec["game_text"]) if re.match(r"\s*(USED|LOST|STARTING):", spec["game_text"]) else spec["game_text"]
    if c.get("legacy"):
        spec["bold_lore"] = False   # Virtual Block lore prints characteristics plain (Chief Chirpa (V))
    if typ in ("Device",):
        spec["device_frame"] = True
    # modern PC cards print the PC's own redrawn spheres; Decipher, OVS and Virtual Block cards print Decipher's
    spec["expansion_style"] = "pc" if ((sid.isdigit() and 200 <= int(sid) <= 399) or sid == "200d") else "decipher"
    rings = [RING[i] for i in icons if i in RING]
    if rings:
        spec["ring_icons"] = rings   # Episode I / VII, Sidious, Skywalker discs under the expansion sphere (A Close Race, Porg)
    if "Setup" in icons:
        spec["banner_icon"] = "setup"   # in the banner's right end (A Remote Planet (V))
    if "Scoundrel" in icons:
        spec["margin_icon"] = "scoundrel"   # left margin at the text box (Scoundrel's Bravado)
    col = [ICON_COL[i] for i in icons if i in ICON_COL and i != "Episode I"]
    sid_ = str(c.get("set") or "")
    if typ == "Character" and sid_.isdigit() and int(sid_) < 200:   # Decipher droids print no Nav Computer column icon (R2-D2)
        col = [x for x in col if x != "nav"]
    if str(c.get("set")) == "1":   # Premiere printed no astromech icon (R2-X2, R1-G4)
        col = [x for x in col if x != "astromech"]
    if exp in ("Reflections II", "Reflections III") and "Death Star II" in icons and typ == "Character":
        col.append("ds2")   # Reflections reprints print the original set's DS2 icon in the column (Luke, Rebel Scout; The Emperor)
    if typ in ("Starship", "Vehicle"):   # starships print their faction icon at the top of the column (Blockade Support Ship)
        col = [c_ for c_ in col if c_ in FACTION] + [c_ for c_ in col if c_ not in FACTION]
    rings = [RING[i] for i in icons if i in RING]
    if "Republic" in icons and typ == "Character":
        col = [c_ for c_ in col if c_ != "republic"]   # characters show Republic as the affiliation disc
    if typ == "Character":
        spec["slip_type"] = "Character"
        spec["affiliation"] = sub
        third = dedupe((f.get("extraText") or [""])[0]) if sub == "Droid" else ""
        if sub == "Droid":
            spec["stats"] = [["POWER", f.get("power") or "0"]]
            if f.get("armor"): spec["stats"].append(["ARMOR", f["armor"]])   # armored droids
            elif f.get("maneuver"): spec["stats"].append(["MANEUVER", f["maneuver"]])   # Sith Probe Droid (IG-88: POWER, ARMOR, ASSASSIN DROID)
            spec["stats"].append([third.upper() or "DROID", ""])
        else:
            ab = f.get("ability") or ""
            spec["stats"] = [["POWER", f.get("power") or "0"], ["ABILITY", ab]]
            if f.get("politics"):
                spec["stats"].append(["POLITICS", f["politics"]])
            elif f.get("maneuver"):   # pilot-droids / Gungan riders (Dams Denna): MANEUVER in the third box
                spec["stats"].append(["MANEUVER", f["maneuver"]])
            elif f.get("armor"):   # Mandalorians (Fenn Rau): ARMOR in the third box
                plus = "".join(x.replace(" ", "") for x in f.get("extraText") or [] if re.fullmatch(r"\s*[+-]\s*\w\s*", str(x)))
                spec["stats"].append(["ARMOR", f["armor"] + plus])   # Chewie, Enraged: ARMOR 4+X
            elif f.get("extraText"):   # third box label: FORCE-ATTUNED, FORCE-SENSITIVE … (Lando)
                spec["stats"].append([dedupe(f["extraText"][0]).upper(), ""])
        spec["icons"] = col
    elif typ in ("Starship", "Vehicle"):
        spec["slip_type"] = "Starfighter" if "starfighter" in sub.lower() else ("Vehicle" if typ == "Vehicle" else "Starship")
        if typ == "Vehicle":   # printed "COMBAT VEHICLE: AT-ST", "SHUTTLE VEHICLE" (Chewie's AT-ST)
            kind, _, model = sub.partition(":")
            spec["card_type"] = (f"{kind.strip()} VEHICLE: {model.strip()}" if model else f"{kind.strip()} VEHICLE").upper()
        else:
            spec["card_type"] = sub.upper()
        st = [["POWER", f.get("power") or "0"]]
        if f.get("maneuver"): st.append(["MANEUVER", f["maneuver"]])
        if f.get("armor"): st.append(["ARMOR", f["armor"]])
        if typ == "Starship" and not f.get("hyperspeed") and any(str(x).lower() == "no hyperdrive" for x in f.get("extraText") or []):
            st.append(["NO HYPERDRIVE", ""])   # TIEs
        elif typ == "Starship": st.append(["HYPERSPEED", f.get("hyperspeed") or "0"])
        else: st.append(["LANDSPEED", f.get("landspeed") or "0"])
        spec["stats"] = st[:3]
        spec["icons"] = col
        if sub.startswith("Squadron") and len(col) > 3:   # X-wing Assault Squadron: the icon row under the stats
            spec["squadron_row"] = True; spec["squadron_scomp"] = icons.count("Scomp Link"); spec["scomp"] = False
    elif typ == "Location":
        spec["slip_type"] = "System" if sub in ("System", "Sector") else "Site"
        spec["card_type"] = title.upper()
        gt = f.get("gametext") or ""
        m = re.match(r"\s*(?:Light|LIGHT)\s*:?\s*(.*?)\s*(?:Dark|DARK)\s*:\s*(.*)$", gt, re.S)
        light, dark = (m.group(1), m.group(2)) if m else (gt, "")
        if not m:
            m2 = re.match(r"\s*(?:Dark|DARK)\s*:?\s*(.*?)\s*(?:Light|LIGHT)\s*:\s*(.*)$", gt, re.S)
            if m2: dark, light = m2.group(1), m2.group(2)
        polish = lambda x: (pc_shorthand if pc_era else str)(ship_text(maintenance(quotes(game_text(x)))))
        spec["game_text"], spec["dark_text"] = polish(light), polish(dark)
        # icon boxes are drawn right to left from the list: scomp outermost, then planet, then the rest (Docking Bay 94)
        li = [LOC_ICON[i] for i in reversed(icons) if i in LOC_ICON]
        li.sort(key=lambda k: {"scomp": 0, "planet": 1}.get(k, 2))
        spec["light_icons"] = spec["dark_icons"] = li
        if c.get("legacy") and f.get("lightSideIcons") is None and f.get("darkSideIcons") is None:
            # the Virtual Block data carries no Force icons: take the original printing's (Lars' Moisture Farm (V))
            b = BASE_LOC.get(re.sub(r"[^a-z0-9]", "", strip_printing(f.get("title") or "").lower()))
            if b: f = dict(f, lightSideIcons=b[0], darkSideIcons=b[1])
        spec["light_force"] = bool(f.get("lightSideIcons")); spec["dark_force"] = bool(f.get("darkSideIcons"))
        spec["light_force_count"] = int(f.get("lightSideIcons") or 0); spec["dark_force_count"] = int(f.get("darkSideIcons") or 0)
        if f.get("parsec"): spec["parsec"] = f["parsec"]
        elif re.match(r"\s*(?:Dark:|Light:)?\s*X = parsec", f.get("gametext") or ""): spec["parsec"] = "X"   # Death Star
        if spec["slip_type"] == "System" or re.search(r"\((AI|ALT)\)", f.get("title") or ""):
            # one-sided systems (Death Star) and full-art AI / ALT sites: no opponent icons, Force or text
            for half, txt, frc in (("light", "game_text", "light_force_count"), ("dark", "dark_text", "dark_force_count")):
                if half != side.lower() and not (spec.get(txt) or "").strip().strip("-") and not spec.get(frc):
                    spec[f"{half}_half_absent"] = True
        if sub == "Site" and ("Starship" in icons or "Vehicle" in icons):   # starship/vehicle sites print blue (Blockade Flagship: Bridge)
            spec["frame_style"] = "ls-starship" if side == "Light" else "ds-starship"
        spec["deploy"] = spec["forfeit"] = None
    elif typ == "Interrupt":
        spec["slip_type"] = f"{sub} Interrupt".strip()
        spec["card_type"] = f"{sub} INTERRUPT".upper().strip()
    elif typ == "Effect":
        spec["slip_type"] = "Effect" if not sub else f"{sub} Effect"
        spec["card_type"] = ("EFFECT" if not sub else f"{sub} EFFECT").upper()
        spec["grabber"] = "Grabber" in icons
    elif typ == "Defensive Shield":
        spec["slip_type"] = "Defensive Shield"; spec["card_type"] = "DEFENSIVE SHIELD"
        spec["grabber"] = "Grabber" in icons   # the banner's grabber fist (A Tragedy Has Occurred)
    elif typ in ("Weapon", "Device"):
        spec["slip_type"] = f"{sub} {typ}".strip()
        spec["card_type"] = f"{sub} {typ}".upper().strip()
    elif typ == "Creature":
        spec["slip_type"] = "Creature"
        spec["card_type"] = (f"CREATURE - {sub.upper()}" if sub.lower() == "force eater" else f"{sub.upper()} CREATURE") if sub else "CREATURE"
        fer = str(f.get("ferocity") or "").strip()
        if not fer and f.get("power"):   # the Virtual Block data keeps ferocity in "power" (One-Arm (V), Gundark)
            fer = "✶" if str(f["power"]).strip() == "*" else str(f["power"]).strip()
        st = []
        if fer:
            if re.fullmatch(r"[0-9.½✶]+", fer):
                st.append(["FEROCITY", fer])
            else:   # "destiny -1", "two destiny": the printed cards show ✶ and explain it in the game text (VS4 Wampa)
                st.append(["FEROCITY", "✶"])
                if "ferocity" not in spec["game_text"].lower()[:60]:
                    spec["game_text"] = f"✶ Ferocity = {fer}. " + spec["game_text"]
                else:
                    spec["game_text"] = re.sub(r"^\s*[*✶]\s*Ferocity", "✶ Ferocity", spec["game_text"])
        for x in f.get("extraText") or []:
            if ":" in x:
                k, v = x.split(":", 1); st.append([k.strip().upper(), v.strip()])
        spec["stats"] = st[:2]
        spec["icons"] = col   # Selective Creature (Porg, Bog-wing)
    elif typ == "Objective":
        spec["slip_type"] = "Objective"
        if " / " in title:   # GEMP keeps both sides on the front: "Front / Back", text "Front: ... Back: ..."
            ft, bt = title.split(" / ", 1)
            gt = f.get("gametext") or ""
            i = gt.find(bt.replace("•", "").strip() + ":")
            spec["title"] = ft
            if spec["caption"]: spec["caption"] = ft
            if i > 0:
                spec["game_text"] = game_text(gt[:i].strip().removeprefix(ft.replace("•", "").strip() + ":").strip())
                spec["game_text_back"] = game_text(gt[i + len(bt.replace("•", "").strip()) + 1:].strip())
            spec["title_back"] = bt
            spec["destiny_back"] = "7"
            return finish(spec)
        b = c.get("back") or {}
        spec["title_back"] = b.get("title") or ""
        spec["game_text_back"] = game_text(b.get("gametext"))
        spec["destiny_back"] = b.get("destiny") or "7"
    elif typ.startswith("Jedi Test"):
        spec["slip_type"] = "Jedi Test"; spec["card_type"] = typ.upper()
        # the printed steps start with the Jedi Test icon and a bold verb: "[icon] Deploy … [icon] Target … [icon] Attempt"
        spec["game_text"] = re.sub(r"(^|(?<=[.)] ))(Deploy|Target|Attempt|Place|Required|Reward)\b", r"{ga:jedi-test}*\2*", spec["game_text"])
    elif typ == "Mission":   # Virtual Block Missions (Rebel Aces) / Critical Missions (Spice Mine Operations)
        spec["slip_type"] = "Critical Mission" if sub == "Critical" else "Mission"
        spec["card_type"] = spec["slip_type"].upper()
    elif typ == "Epic Event":
        spec["slip_type"] = "Epic Event"
        if side == "Light":
            spec["text_grow"] = 230 if len(spec["game_text"]) > 600 else (110 if len(spec["game_text"]) > 480 else 0)   # Light Epic Events print a shorter art window over a tall text box (Attack Run, Communing)
        # the printed Epic Events set each step on its own line with a bold run-in label (Communing: "The Living Force:")
        spec["game_text"] = re.sub(r"(?<=[.):'”\"]) ((?:[A-Z][\w'’!-]*,? ){0,6}[A-Z][\w'’!-]*!?):(?= )", r"\n*\1:*", spec["game_text"])
    elif "Admiral" in typ:
        spec["slip_type"] = "Admiral's Order"
    else:
        spec["slip_type"] = typ or "Effect"; spec["card_type"] = typ.upper()
    return finish(spec)


WIDE_PRINTED = {"13_75", "4_167", "9_157", "204_54", "200_41", "204_47"}   # QA 2026-10-15: every non-location scan printed landscape   # Decipher cards printed landscape: Maul's Double-Bladed Lightsaber (Reflections III)


def objective_text(t: str, front: bool) -> str:
    """Decipher's Objective layout: the setup sentence(s) in italics, then a paragraph per *For* / *While* / *Flip*."""
    # the PC JSON marks the keywords {For} (-> *For*) or not at all: "For remainder of game", "While this side up",
    # "Flip this card" always open a paragraph on the printed Objectives
    t = re.sub(r"(?<![*\w])(For remainder of game|While this side up|Flip this card)", lambda m: "*" + m.group(1).split()[0] + "*" + m.group(1)[len(m.group(1).split()[0]):], t)
    t = re.sub(r"\s+(\*(?:For|While|Flip)\*)", r"\n\1", t).strip()
    if front:
        first, sep, rest = t.partition("\n")
        if sep and not first.startswith("*"):
            t = f"_{first.replace('_', '')}_\n{rest}"   # ship names inside the italic setup line stay italic
    return t


def finish(spec: dict) -> dict:
    ps = spec.pop("_printed_stats", None)
    if ps:   # stat boxes transcribed from the printed card (gempdata/fill.json "printedStats")
        spec["stats"] = [list(x) for x in ps]
    for k in ("game_text", "dark_text"):   # PC placeholders for an empty text half: "(none).", "Blank.", "-"
        spec[k] = re.sub(r"^\s*Text:\s*", "", spec.get(k) or "")   # a stray "Text:" label (Boba Fett, Bounty Hunter)
        if re.fullmatch(r"\s*([(<]none[)>]\.?|Blank\.?|-|\.|none\.?)\s*", spec.get(k) or "", re.I):
            spec[k] = ""
    if spec.get("slip_type") == "Objective":
        spec["game_text"] = objective_text(spec.get("game_text") or "", True)
        spec["game_text_back"] = objective_text(spec.get("game_text_back") or "", False)
    if spec.get("gempId") in WIDE_PRINTED:
        spec["wide"] = True
    if spec.get("deploy") is None:
        spec.pop("deploy", None); spec.pop("forfeit", None)
    return spec


def spec_to_card(spec: dict, build_vs) -> dict:
    """spec (+ resolved art/set-symbol files) -> render.py card dict, through build_vs.convert (the remaster path)."""
    c = dict(spec)
    # bounded inputs (the boxes condense, then shrink, but only so far): API callers get the same limits as the editor
    for k, n in (("destiny", 8), ("deploy", 4), ("forfeit", 4), ("destiny_back", 8)):
        if c.get(k) is not None:
            c[k] = str(c[k])[:n]
    c["stats"] = [[str(a)[:24], str(b)[:5]] for a, b in (c.get("stats") or [])][:4]
    for k in ("game_text", "dark_text", "game_text_back", "lore"):   # typed line breaks = paragraphs that still wrap
        if isinstance(c.get(k), str):
            c[k] = c[k].replace("\r\n", "\n").replace("\n", "¶")
    c.setdefault("number", "")
    ovs = spec.get("style") == "ovs"   # Original Virtual Set remaster look (2002-08 slips) instead of Decipher's printing
    if not ovs:
        c.setdefault("shield_style", "decipher")   # Decipher's own shield frames (cyan / red), not the VS-era fade
    else:
        c.pop("shield_style", None) if c.get("shield_style") == "decipher" else None
    c["number"] = str(c.get("number") or "0")
    vs = int(c.get("virtual_set") or 0) or None
    if not ovs:
        vs = None if not spec.get("virtual_set") else vs
    card = build_vs.convert(dict(c, number=c["number"] if c["number"].isdigit() else "0"), vs or 0)
    if not ovs:
        card["art_cover_hole"] = True
        card["ring_fill"] = True
        card["copyright_split"] = True          # systems print Lucasfilm left / Decipher right (Dagobah)
        card["expansion_icon_in_hole"] = True   # printed Decipher cards: the sphere sits in a black hole of the frame (2-1B)
        if card["template"] == "ls-jeditest-tall" and (spec.get("slip_type") or "").startswith("Jedi Test"):
            card["template"] = "ls-jeditest-olive"   # printed Jedi Tests are olive throughout (Domain Of Evil)
        if spec.get("slip_type") == "Podracer":
            card["disc"] = "podracer"   # Episode I Podracers: the podracer type disc (Game Aid icon)
        if spec.get("gempId") in UNDERCOVER_FRAME and spec.get("side") == "Light" and "rebel" in (spec.get("affiliation") or "").lower():
            card["disc"] = "rebel"   # the Rebel disc on the Dark frame (TK-422, Boushh)
        if card["template"].endswith("-mission"):
            card["disc"] = "mission"   # the teal hologram type disc
        if card["template"] in ("ls-character-droid", "ds-character-droid"):
            card["template"] += "-dc"   # brass droid disc as printed
        if card["template"] == "creature":
            card["template"] = "creature-dc"   # printed Decipher creature: banner + black title
    card["id"] = "cm-" + re.sub(r"[^A-Za-z0-9_-]+", "_", spec.get("title") or "card")[:40]
    card["caption"] = spec.get("caption") if spec.get("caption") is not None else spec.get("title", "")
    card["number"] = str(spec.get("number") or "")
    if vs is None:
        card.pop("virtual_set", None)
    if spec.get("_set_icon_file"):
        card["set_icon_file"] = spec["_set_icon_file"]
    if spec.get("_art"):
        card["art"] = spec["_art"]
        card.pop("art_trim", None)
        if spec.get("_art_kind") == "scan" and str((spec.get("source") or {}).get("set") or "").startswith("100"):
            card["art_trim"] = True; card["legacy_scan"] = True   # Virtual Block scans: the PC's slips sit their banner/stat bar a little higher (A Jedi's Patience (V))
    if not spec.get("expansion"):
        card["expansion_icon"] = None
    src_exp = SETS.get(str((spec.get("source") or {}).get("set")))
    if not ovs and spec.get("expansion"):
        card["draw_system_ring"] = True   # systems: the scan carries its own sphere; draw ours when there's none or it changed
    return card
