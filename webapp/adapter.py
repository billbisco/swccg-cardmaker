"""Card maker: turn a card from the Players Committee's card JSON (swccg-card-json, as GEMP uses it) into an editable
card spec, and turn a spec into a render.py card dict.

A *spec* is the same shape as the remaster transcriptions (cards/vsN/NN.json, see cards/VS-SPEC.md): human-level
fields (title, side, slip_type, card_type, stats, game_text, icons, ...) plus an `art` choice. The web UI edits specs;
AIs and batch jobs can write them directly.
"""
from __future__ import annotations
import os, re

SETS = {   # GEMP set id -> expansion name as build_vs.SET_ICON knows it (ring sphere right of the lore box)
    "1": "Premiere", "2": "A New Hope", "3": "Hoth", "4": "Dagobah", "5": "Cloud City", "6": "Jabba's Palace",
    "7": "Special Edition", "8": "Endor", "9": "Death Star II", "10": "Reflections II", "11": "Tatooine",
    "12": "Coruscant", "13": "Reflections III", "14": "Theed Palace", "101": "Premiere", "102": "Jedi Pack",
    "103": "Jedi Pack", "104": "Premium", "106": "Official Tournament Sealed Deck", "108": "Premium",
    "109": "Enhanced Cloud City", "110": "Enhanced Jabba's Palace", "111": "Premium", "112": "Jabba's Palace Sealed Deck",
    "15": "Reflections Gold Remastered", "15o": "Reflections Gold",   # set 15 (swccg-guild/work#174): Remastered = 15_N, original playtest = 15_No
}

# GEMP sets Decipher printed only with a white outer border (rev 76). The Unlimited / Revised reprints (GEMP 5x_N,
# First / Second Anthology previews) are not separate cards in the data: open the card and pick Border: White.
WHITE_BORDER_SETS = {"104"}   # The Empire Strikes Back Introductory Two-Player Game (ESB2P-L-chewie-decipher-archive.gif)

EXPANSION_NAMES = {"A New Hope", "Hoth", "Dagobah", "Cloud City", "Jabba's Palace", "Special Edition", "Endor",
                   "Death Star II", "Reflections II", "Tatooine", "Coruscant", "Reflections III", "Theed Palace", "Premium",
                   "Reflections Gold", "Reflections Gold Remastered"}
YEAR = {"1": 1995, "2": 1996, "3": 1996, "4": 1997, "5": 1997, "6": 1998, "7": 1998, "8": 1998, "9": 2000, "10": 2000,
        "11": 2001, "12": 2001, "13": 2001, "14": 2001, "101": 1996, "102": 1996, "103": 1997, "104": 1997, "106": 1998,
        "108": 1998, "109": 1998, "110": 1998, "111": 1998, "112": 1999, "15o": 2001}   # Remastered (15) prints no copyright line, as its renders


DECIPHER_SETS = {str(i) for i in range(1, 15)} | {"101", "102", "103", "104", "106", "108", "109", "110", "111", "112"}
# rev 80: the line as each set printed it, read on the printed scans (wiki Decipher archive / Holotable 350 px faces, 4+ cards a
# set). 1995-98 (Premiere .. Jabba's Palace and their premium sets): "TM & © y LUCASFILM LTD.  TM, ® & © y DECIPHER INC.";
# Special Edition (Dec 1998) .. Death Star II and the 1999-2000 premium sets drop "TM &" and the first year:
# "© LUCASFILM LTD. & TM.  TM, ® & © y DECIPHER INC."; Reflections II .. Theed Palace (2000-01) bring the year back and
# print no final period ("… DECIPHER INC"); Coruscant alone sets a comma after the ® ("TM, ®, & ©"). Every printing sets
# two spaces before the Decipher half and a full-size ®.
# rev 81, read on sharp photos of printed cards (pricecharting.com card photos, 700-1600 px): Enhanced Cloud City prints the
# final period (Boba Fett In Slave I, Crush The Rebellion, Dengar In Punishing One, IG-88 With Riot Gun, Any Methods
# Necessary); Endor prints 1999 on every card (Chewbacca's Bowcaster, Chewie's AT-ST, Chief Chirpa, Corporal Beezer; the
# Decipher archive scans of 8_160-8_178 carry the same digits, Speeder Bike and Tempest Scout 6 included); Reflections II's
# own cards (the combos: Alter & Collateral Damage, Sense & Recoil In Fear) print the final period and "TM, ® &" (its foil
# reprints of older cards set "TM, ®, &", but those render as their first printing).
# rev 81 (geometry 3): Decipher's own two-disc character titles, per set: (title x offset, letter-spacing, extra bar width),
# master px. Measured against the frame (from the Imperial disc's right edge, 745 px faces): Ref2 / PC print the bullet
# 28-29 px from the disc (our default); Death Star II (Emperor Palpatine) 20 px, run 3 % tighter; Enhanced Jabba's Palace
# (Mara Jade, The Emperor's Hand, both wiki faces) 23-25 px, title running to 384 px from the disc (19 px past our bar).
# No other Decipher two-disc card exists (ECC, Enhanced Premiere and the other premium sets have none).
DISC2_DECIPHER = {"9": (-17, 0.1, 0), "110": (-8, None, 42)}
SE_ERA = {"7", "8", "9", "109", "110", "111", "112"}
PRINT_YEAR = {"8": 1999, "101": 1995, "104": 1996, "109": 1999, "110": 1999, "111": 2000, "112": 2000}   # the year the card prints
NO_FINAL_PERIOD = {"11"}
# Rev 81 (integration): only Tatooine has no final period. Reflections II, Coruscant, Reflections III and Theed Palace DO
# print it (8x re-read of 4-8 scans a set; Reflections III also on photos of Stormtrooper Garrison, The Ebb Of Battle,
# Qui-Gon's Lightsaber). Enhanced Cloud City: the 350 px scans read no period, but sharp 700-1600 px photos of five cards
# (Boba Fett In Slave I, Crush The Rebellion, Dengar, IG-88, Any Methods Necessary) show it, so the photos win.
# Tatooine sets the line in its own tighter face: the © against the year and the ® against the ampersand
# ("©2001 … TM, ®& ©2001 DECIPHER INC"); its Epic Events (Boonta Eve Podrace, I Did It!) print the final period.


def copyright_for(set_id, decipher: bool = True, card_type: str = "") -> str:
    """The vertical Lucasfilm / Decipher line printed beside the art, word for word as each set printed it (rev 80).
    decipher=False: the line as the Players Committee's slips reproduce it (the form before rev 80, kept for their cards)."""
    sid = str(set_id or "")
    if (sid.isdigit() and 200 <= int(sid) <= 299) or sid == "200d":
        return "ARTWORK NEITHER AFFILIATED WITH NOR ENDORSED BY LUCASFILM LTD."   # the modern PC cards (I Want That Map)
    if not decipher:
        y = YEAR.get(sid)
        if not y:
            return ""
        if y >= 2000:
            return f"© {y} LUCASFILM LTD. & TM. TM, ® & © {y} DECIPHER INC."
        return f"TM & © {y} LUCASFILM LTD. TM, ® & © {y} DECIPHER INC."
    y = PRINT_YEAR.get(sid) or YEAR.get(sid)
    if not y:
        return ""
    end = "" if sid in NO_FINAL_PERIOD and not (sid == "11" and card_type == "Epic Event") else "."
    reg = "®," if sid in ("12", "15o") else "®"   # rev 81: Reflections Gold's playtest prints set the comma too (Local Trouble)
    if sid == "11":
        return f"©{y} LUCASFILM LTD. & TM.  TM, ®& ©{y} DECIPHER INC{end}"
    if sid in SE_ERA:
        return f"© LUCASFILM LTD. & TM.  TM, {reg} & © {y} DECIPHER INC{end}"
    if y >= 2000:
        return f"© {y} LUCASFILM LTD. & TM.  TM, {reg} & © {y} DECIPHER INC{end}"
    return f"TM & © {y} LUCASFILM LTD.  TM, {reg} & © {y} DECIPHER INC{end}"


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
    "[Immune to Sense]": "{sense}", "[Immune To Sense]": "{sense}", "[Immune To Sense.]": "{sense}", "[Immune to Control.]": "{control}", "[Immune to Control]": "{control}",
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
# rev 73: a type disc printed left of the text box top of two Virtual Block 7 Missions (PC id -> icon), as printed:
# Rebel Aces / Imperial Aces carry the Objective icon there (template match on the PC gifs, r 0.83 / 0.81)
MISSION_DISC = {"5825": "objective", "6389": "objective"}
RING = {"Episode I": "episode1", "Episode VII": "episode7", "Sidious": "sidious", "Skywalker": "skywalker", "Personal Force": "personal-force"}
LOC_ICON = {"Planet": "planet", "Interior": "interior", "Exterior": "exterior", "Mobile": "mobile",
            "Underground": "underground", "Underwater": "underwater", "Starship": "starship", "Vehicle": "vehicle",
            "Scomp Link": "scomp", "Space": "space",
            # rev 81: GEMP's names for the printed vehicle / creature site icons (Sandcrawler: Loading Bay, Big One)
            "Vehicle Site": "vehicle", "Starship Site": "starship", "Creature Site": "creature"}


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
    t = re.sub(r"\[Set (\d{1,2})\]", r"{pcset:\1}", t)
    t = re.sub(r"\[V(\d{1,2})\]", r"{pcset:\1}", t)   # [V17] = Virtual Set 17
    t = t.replace("[Set D]", "{pcset:D}").replace("[S]", "{sense}").replace("[Sith]", "{ga:character-sith}")
    t = re.sub(r"(?i)\[download\]", "▼", t); t = re.sub(r"(?i)\[upload\]", "▲", t)     # the modern Virtual Set marks
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
LEGACY_NOLORE = {"1004_L5987"}   # Virtual Block cards printed without a lore box (Uncharted Settlements)
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
    # "take" first, and "deploy" only as the verb: "take Luke … with printed deploy < 4 into hand from Reserve Deck" is
    # ▲ (PC A New Hope, VS27); matching "deploy" first turned it into "take Luke … printed ▼ < 4 into hand" (#63)
    t = re.sub(r"(?i)\btake ((?:(?!\binto hand\b)[^.;])+?) into hand from (?:your )?Reserve Deck(?:; reshuffle| \(reshuffle\))?", r"▲ \1", t)
    t = re.sub(r"(?i)(?<!printed )(?<!total )\bdeploy (?![<>=≤≥])(?!phase\b)((?:(?!\bdeploy\b)[^.;()])+?) from (?:your )?Reserve Deck(?:; reshuffle| \(reshuffle\))?", r"▼ \1", t)   # rev 72: not from "deploy phase, may deploy …" (I'm Sorry (V) PC-E1)
    # #62: the object may hold a bracketed aside ("an [Episode I] (or Coruscant) docking bay"), when the Reserve Deck
    # clause ends the sentence; never across a second "deploy" or a "deploy phase"
    t = re.sub(r"(?i)(?<!printed )(?<!total )\bdeploy (?![<>=≤≥])(?!phase\b)((?:(?!\bdeploy\b)[^.;()]|\([^().;]*\))+?)(?<!,) from (?:your )?Reserve Deck(?:; reshuffle| \(reshuffle\)|(?=[.;]))", r"▼ \1", t)
    t = re.sub(r"\(Immune to \{alter\}\.?\)", "{alter}", t)
    t = re.sub(r"\(Immune to Alter\.?\)", "{alter}", t)   # also without the period (Baktoid Armor Workshop, VB7)
    t = re.sub(r"\(Immune to (Sense|Control)\.?\)", lambda m: "{%s}" % m.group(1).lower(), t).replace("(Immune to Alter.)", "{alter}")
    return t


def quotes(t: str) -> str:
    """The PC JSON writes printed double quotes as single ones: 'Vehicle with armor' -> “Vehicle with armor”. Lore
    (rev 80): every quoted run prints in double curly quotes, Premiere to the PC's Virtual Sets ("What was that?" …
    "affect mind", Affect Mind; "It’s a good bet …", Perimeter Scan (V))."""
    return re.sub(r"(?<![\w])'(.+?)'(?![\w])", "\u201c\\1\u201d", t)


# rev 80: a quoted run of game text that names words a card carries ("with 'Death Star' in title") prints in double
# curly quotes (Ominous Rumors, Something Special Planned For Them, Mara Jade (V) "Mara" in game text, Darth Maul,
# Young Apprentice (V) "Trade Federation" in lore); every other quoted game term in single curly ones ('insert',
# A Tremor In The Force; 'react', Admiral Ackbar (V); 'credits.', 'communing,', 'BEEP-BOOP'). Decipher printed a few
# "in title" runs single (Death Star II: Coolant Shaft 'Occupation', Invasion 'Trade Federation'): the data does not say
# which, the double form is the commoner one.
GT_DOUBLE = r"\s+in\s+(?:its\s+|their\s+)?(?:title|lore|game\s+text|name|persona)\b"


def gt_quotes(t: str) -> str:
    t = (t or "").replace("`", "'")   # a few PC texts open the quote with a backtick (`credits.', Credits Will Do Fine (V))
    return re.sub(r"(?<![\w])'(.+?)'(?![\w])(?=(" + GT_DOUBLE + r")?)",
                  lambda m: ("\u201c%s\u201d" if m.group(2) else "\u2018%s\u2019") % m.group(1), t)


def apostrophes(t: str) -> str:
    """Rev 80: Decipher and the PC print typographic apostrophes in titles, lore and game text (Han’s Heavy Blaster
    Pistol, Don’t Get Cocky, opponent’s, Let ’er go!, Twi’lek): any straight ' left after the quotes are paired."""
    return (t or "").replace("'", "\u2019") if isinstance(t, str) else t


BASE_ICONS: dict = {}   # title -> icons of the original Decipher printing (filled by the server)
BASE_LOC: dict = {}   # location title -> (Light, Dark) Force icons of the PC data's printing (filled by the server)
BASE_EXP: dict = {}   # title -> Decipher expansion of the original printing (filled by the server)
PC_LABELS: dict = {}  # gempId -> PC extra printed labels (gempdata/card_labels.json, filled by the server; swccg-guild/work#100)


def _img_key(u) -> str:
    """The PC image a label entry was read from, as a key that also matches the card JSON's imageUrl (the labels were
    read from hires .png faces for Virtual Sets, the card JSON points at large .gif ones)."""
    u = str(u or "").strip().lower()
    return re.sub(r"\.(png|gif|jpe?g)$", "", u.replace("/hires/", "/large/"))


_LABELS_BY_IMAGE: dict = {}
_LABELS_INDEXED = [-1]   # len(PC_LABELS) when the image index was built


def pc_labels_for(c: dict) -> dict:
    """The label entry for this exact printing: matched by its PC image, because alternate-image printings share a
    gempId and Virtual Block cards have none in the PC data; falls back to the gempId."""
    if _LABELS_INDEXED[0] != len(PC_LABELS):
        _LABELS_BY_IMAGE.clear()
        for k, e in PC_LABELS.items():
            if not k.endswith("_BACK"):
                _LABELS_BY_IMAGE.setdefault(_img_key(e.get("image")), e)
        _LABELS_INDEXED[0] = len(PC_LABELS)
    hit = _LABELS_BY_IMAGE.get(_img_key((c.get("front") or {}).get("imageUrl")))
    return hit or PC_LABELS.get(str(c.get("gempId") or "")) or {}


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
            "copyright": copyright_for(c.get("set"), card_type=f.get("type") or ""), "set_mark": set_mark_for(c.get("set"))}
    if f.get("loreLines"):   # rev 80: the printed lore's own line breaks (gempdata/fill.json "loreLines"; Teemto Pagalies' Podracer)
        spec["lore_lines"] = list(f["loreLines"])
    if c.get("wide"):   # Reflections Gold "wide vision" cards (set 15): landscape per the card data
        spec["_wide"] = True
    if f.get("credits"):   # Reflections Gold credit value: gold coins
        spec["credits"] = f["credits"]
    lab = pc_labels_for(c)
    if lab:   # the PC's extra printed labels (billbisco/swccg-gemp card_labels.json, swccg-guild/work#100)
        _sid = str(c.get("set") or "")
        _modern = (_sid.isdigit() and 200 <= int(_sid) <= 399) or _sid == "200d"
        labels = []
        if lab.get("original_title"):
            if _modern:   # Virtual Sets 0-27 set it in the bottom-left label face the PC uses (preset measured on V21-27)
                it = lab.get("original_title_italic")
                labels.append(dict({"preset": "bottom-left", "text": lab["original_title"]},
                                   **({"italic": True, "skew": 10} if it is True else {"italic_part": it} if isinstance(it, str) else {})))
            else:
                spec["caption"] = lab["original_title"]
                if lab.get("original_title_italic"):
                    spec["caption_italic"] = True
        if lab.get("errata_mark"):
            if _modern:
                spec["errata_mark"] = lab["errata_mark"]
            else:   # Virtual Block slips stamp it at the strip's right end (E's left edge x 685 on the 745 px face)
                labels.append({"preset": "errata", "text": lab["errata_mark"], "e_x": -200})
        if lab.get("ai_mark"):   # "(AI)" / "(ALT)" with the PC logo to its left; it moves left of an errata mark
            labels.append(dict({"preset": "ai", "text": lab["ai_mark"] if isinstance(lab["ai_mark"], str) else "(AI)"},
                               **({"x": -228} if lab.get("errata_mark") else {})))
        for _f in ("concept_credit", "dedication", "bar_text", "edge_text"):   # the line in the frame's bottom bar ("Original concept by …",
            pos = lab.get(_f + "_position")                                      # "In memory of …"); edge-printed ones run up a side margin
            if lab.get(_f) and (not pos or pos == "bottom bar") and _f != "edge_text":
                labels.append({"preset": "concept", "text": lab[_f]})
            elif lab.get(_f) and pos in ("side", "left side", "right side") and c.get("legacy"):   # rev 71: up the side margins,
                spec["margin_right" if pos == "right side" else "margin_left"] = lab[_f]           # as the OVS slips (Deep Hatred (V))
        if labels:
            spec["labels"] = labels
        if lab.get("art_credit") and lab.get("art_credit_position") == "bottom bar":
            labels.append({"preset": "concept", "text": lab["art_credit"], "kind": "art_credit"})   # rev 71: "Image courtesy of …" in the bottom bar (VB AI cards)
            spec["labels"] = labels
        elif lab.get("art_credit"):
            spec["art_credit"] = lab["art_credit"]
        if lab.get("copyright"):
            spec["copyright"] = lab["copyright"]
        elif _modern and lab.get("original_title") is not None:   # checked on the PC image: no copyright line printed
            spec["copyright"] = ""
    if c.get("legacy"):
        # rev 71: the 2009-14 Virtual Block slips print their sheet number at the strip's right end ("123", "85E", "2 • 26",
        # "D60"), read off the PC gifs into card_labels.json slip_mark; and keep the copyright line of the Decipher card
        # they were printed on (the server finds that card: c["_print_base_set"])
        if lab.get("slip_mark"):
            spec["number"] = str(lab["slip_mark"])
        if not lab.get("copyright") and c.get("_print_base_set"):
            spec["copyright"] = copyright_for(c["_print_base_set"], decipher=False)   # rev 80: the PC slip's form
    if c.get("legacy") and not lab.get("original_title"):   # 2009-2014 Virtual Blocks print "•Title (V)" in the bottom strip (Holotable faces)
        spec["caption"] = (f.get("title") or "").replace("<>", "◊")
    if c.get("legacy"):
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
    if not spec.get("expansion") and c.get("legacy") and SETS.get(str(c.get("_print_base_set") or "")) in EXPANSION_NAMES:
        spec["expansion"] = SETS[str(c["_print_base_set"])]   # rev 71: the sphere of the Decipher card it was printed on (Baktoid Armor Workshop: Coruscant)
    if not spec.get("expansion") and pc_era:   # (V) cards keep the original card's sphere (Overseeing It Personally (V): DS2)
        spec["expansion"] = BASE_EXP.get(re.sub(r"[^a-z0-9]", "", title.lower().replace("•", "")))
    spec["lore"] = quotes(spec["lore"])
    if typ != "Objective" and "/" in (f.get("title") or "") and title != strip_printing(f.get("title") or ""):   # flip card text joined to the other side's: "…unpiloted).May not…"
        spec["game_text"] = re.split(r"(?<=[.)!])(?=[A-Z•])", spec["game_text"], maxsplit=1)[0]
    spec["game_text"] = ship_text(maintenance(gt_quotes(spec["game_text"])))
    spec["lore"] = ship_text(re.sub(r"\{([A-Za-z][A-Za-z' ]*)\}", r"*\1*", spec["lore"]))   # {leader} = bold in lore
    if c.get("gempId") in UNDERCOVER_FRAME:   # undercover spies print on the other side's frame (TK-422, Boushh, U-3PO)
        spec["side_frame"] = "Dark" if side == "Light" else "Light"
    if c.get("gempId") in CAPTIVE_NOART:
        spec["side_frame"] = "Light"; spec["captive_noart"] = True
    if c.get("gempId") in CAPTIVE_ART:   # carbonite captives (The Mythrol, Luke Skywalker, The Emperor's Prize): printed
        # on the Light character frame with no lore box; the art runs down to a raised stat bar over a tall text box
        spec["side_frame"] = "Light"
        spec["no_lore_box"] = True; spec["text_grow"] = 330; spec["text_grow_scan"] = True; spec["grow_keep_frame"] = True
    if not spec["lore"].strip() and (" & " in title or c.get("gempId") in LEGACY_NOLORE) and typ in ("Interrupt", "Effect", "Defensive Shield"):
        # Reflections II combo cards print no lore box: the art runs from the title bar to a raised banner and the text
        # box grows by the same amount (Evader & Monnok, Do, Or Do Not & Wise Advice)
        spec["no_lore_box"] = True; spec["text_grow_scan"] = True
        spec["text_grow"] = 290 if typ == "Defensive Shield" else 276   # #62: the PC raises banner and text box 276 px (138 at 745) on both sides
        if typ in ("Defensive Shield", "Effect", "Interrupt"):   # #62: Effect and Interrupt combos too (the PC keeps the Effect frame's own window edges)
            spec["grow_keep_frame"] = True   # shield combos keep the shield frame (A Useless Gesture & Death Star Sentry)
    if pc_era:
        spec["game_text"] = pc_shorthand(spec["game_text"])
        # the PC prints titles with typographic apostrophes (You Know What I’ve Come For, Ommni Box & It’s Worse, #63)
        spec["title"] = spec["title"].replace("'", "\u2019")
        spec["caption"] = (spec.get("caption") or "").replace("'", "\u2019")
    spec["game_text"] = re.sub(r"\s+(LOST|STARTING|USED):", r"\n\1:", spec["game_text"]) if re.match(r"\s*(USED|LOST|STARTING):", spec["game_text"]) else spec["game_text"]
    if c.get("legacy"):
        spec["game_text"] = spec["game_text"].replace("{ga:vader}", "{ga:disc-vader}")   # rev 73: the round VB7 disc inline
        spec["bold_lore"] = False
        if typ in ("Objective", "Mission", "Epic Event"):
            spec["disc_left"] = True   # rev 71: the Episode I disc in the left margin (A Stunning Move, Hunt Down The Dark Acolyte)   # Virtual Block lore prints characteristics plain (Chief Chirpa (V))
    if c.get("legacy") and typ == "Location" and sub in ("System", "Sector"):
        # rev 71: a system's picture is its whole PC scan, which already carries its copyright and side credits
        spec["copyright"] = ""; spec.pop("margin_left", None); spec.pop("margin_right", None)
    if typ in ("Device",):
        spec["device_frame"] = True
    # modern PC cards print the PC's own redrawn spheres; Decipher, OVS and Virtual Block cards print Decipher's
    # expansion sphere style: the PC's redraws by default (Bill 2026-11-01: the target look is the PC's); Decipher's own
    # as printed is the editor's / API's "decipher". The 2009-14 Virtual Blocks (sets 1000+) printed Decipher's spheres.
    spec["expansion_style"] = "decipher" if (sid.isdigit() and int(sid) >= 1000) or sid == "1000d" else "pc"
    spec["border"] = "white" if sid in WHITE_BORDER_SETS else "black"   # rev 76: Unlimited / Revised / Anthology printings
    rings = [RING[i] for i in icons if i in RING]
    if rings:
        spec["ring_icons"] = rings   # Episode I / VII, Sidious, Skywalker discs under the expansion sphere (A Close Race, Porg)
    if "Setup" in icons:
        spec["banner_icon"] = "setup"   # in the banner's right end (A Remote Planet (V))
    elif c.get("legacy") and typ == "Mission" and ("Clone Army" in icons or "Separatist" in icons):
        # rev 73: Virtual Block 9 Missions print their faction icon there (Hunt Down The Dark Acolyte, Rally To Our Cause)
        spec["banner_icon"] = "clone-army" if "Clone Army" in icons else "separatist"
    if c.get("legacy") and typ == "Mission" and str(c.get("id")) in MISSION_DISC:
        spec["mission_disc"] = MISSION_DISC[str(c.get("id"))]
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
    if c.get("legacy") and "Vader" in icons:
        # rev 73: Virtual Block 7 prints [Vader] as a round disc left of the text box, not in the column (Darth Vader,
        # More Machine Than Man; Vader's Mask) and as the same disc inline ("Deploy on [Vader] Vader")
        col = [c_ for c_ in col if c_ != "vader"]
        spec["margin_disc"] = "disc-vader"
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
        polish = lambda x: (pc_shorthand if pc_era else str)(ship_text(maintenance(gt_quotes(game_text(x)))))
        spec["game_text"], spec["dark_text"] = polish(light), polish(dark)
        # icon boxes are drawn right to left from the list: scomp outermost, then planet, then the rest (Docking Bay 94)
        li = [LOC_ICON[i] for i in reversed(icons) if i in LOC_ICON]
        li.sort(key=lambda k: {"scomp": 0, "planet": 1}.get(k, 2))
        if "mobile" in li and "starship" in li and str(c.get("gempId") or "").split("_")[0] in DECIPHER_SETS:
            # rev 81: Decipher prints the mobile icon outside the starship icon (Executor: Comm Station, Home One: War
            # Room, Star Destroyer: Launch Bay, Blockade Flagship: Bridge); GEMP lists them either way round
            li.remove("mobile"); li.insert(li.index("starship"), "mobile")
        if "exterior" in li and "interior" in li and str(c.get("gempId") or "").split("_")[0] in DECIPHER_SETS:
            # rev 81 (sites 2): Decipher prints the exterior icon outside the interior one (Hoth: Echo Docking Bay,
            # Death Star: Docking Bay 327, Executor: Docking Bay, Star Destroyer: Launch Bay); GEMP lists them either way
            li.remove("exterior"); li.insert(li.index("interior"), "exterior")
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
        # starship/vehicle sites print blue (Blockade Flagship: Bridge). rev 81: GEMP names the vehicle-site icon "Vehicle Site"
        # (Sandcrawler: Loading Bay / Droid Junkheap, Jabba's Sail Barge: Passenger Deck print blue too)
        if sub == "Site" and ("Starship" in icons or "Vehicle" in icons or "Vehicle Site" in icons or "Starship Site" in icons):
            spec["frame_style"] = "ls-starship" if side == "Light" else "ds-starship"
            # rev 81: Decipher italicised the named capital ship in its sites' title bars (EXECUTOR: COMM STATION,
            # HOME ONE: WAR ROOM); class names stay roman (STAR DESTROYER: LAUNCH BAY, BLOCKADE FLAGSHIP: BRIDGE)
            if str(c.get("gempId") or "").split("_")[0] in DECIPHER_SETS:
                spec["card_type"] = re.sub(r"^([•◊]*)(EXECUTOR|HOME ONE)(?=:)", r"\1_\2_", spec["card_type"])
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
            if spec["caption"] and not lab.get("original_title"):   # rev 71: "Local Uprising (V)", not "Local Uprising"; an
                cap = spec["caption"]                                # original title from the labels stays (A Stunning Move: "Invasion (V)")
                spec["caption"] = cap.split(" / ")[0] + (" (V)" if cap.rstrip().endswith("(V)") and not cap.split(" / ")[0].rstrip().endswith("(V)") else "")
            if i > 0:
                spec["game_text"] = gt_quotes(game_text(gt[:i].strip().removeprefix(ft.replace("•", "").strip() + ":").strip()))
                spec["game_text_back"] = gt_quotes(game_text(gt[i + len(bt.replace("•", "").strip()) + 1:].strip()))
            spec["title_back"] = bt
            spec["destiny_back"] = "7"
            return finish(spec)
        b = c.get("back") or {}
        spec["title_back"] = b.get("title") or ""
        spec["game_text_back"] = gt_quotes(game_text(b.get("gametext")))
        spec["destiny_back"] = b.get("destiny") or "7"
    elif typ.startswith("Jedi Test"):
        spec["slip_type"] = "Jedi Test"; spec["card_type"] = typ.upper()
        # the printed steps start with the Jedi Test icon and a bold verb: "[icon] Deploy … [icon] Target … [icon] Attempt"
        # rev 81: also after "test completed:" (Size Matters Not, Great Warrior: "[icon] Place"; You Must Confront Vader: "[icon] Leave")
        spec["game_text"] = re.sub(r"(^|(?<=[.):] ))(Deploy|Target|Attempt|Place|Leave|Required|Reward)\b", r"{ga:jedi-test}*\2*", spec["game_text"])
    elif typ == "Mission":   # Virtual Block Missions (Rebel Aces) / Critical Missions (Spice Mine Operations)
        spec["slip_type"] = "Critical Mission" if sub == "Critical" else "Mission"
        spec["card_type"] = spec["slip_type"].upper()
    elif typ == "Epic Event":
        spec["slip_type"] = "Epic Event"
        if side == "Light" and not c.get("legacy"):
            spec["text_grow"] = 230 if len(spec["game_text"]) > 600 else (110 if len(spec["game_text"]) > 480 else 0)   # Light Epic Events print a shorter art window over a tall text box (Attack Run, Communing)
        # the printed Epic Events set each step on its own line with a bold run-in label (Communing: "The Living Force:")
        spec["game_text"] = re.sub(r"(?<=[.):'”\"]) ((?:[A-Z][\w'’!-]*,? ){0,6}[A-Z][\w'’!-]*!?):(?= )", r"\n*\1:*", spec["game_text"])
    elif "Admiral" in typ:
        spec["slip_type"] = "Admiral's Order"
    else:
        spec["slip_type"] = typ or "Effect"; spec["card_type"] = typ.upper()
    if typ in ("Starship", "Vehicle") and (str(c.get("gempId") or "").split("_")[0] in DECIPHER_SETS or is_wide_printed(c.get("gempId"))):
        # rev 81: Decipher set the class name italic in the banner (CAPITAL: _IMPERIAL_-CLASS STAR DESTROYER,
        # _VICTORY_-CLASS, _SUPER_-CLASS: Devastator, Victory-Class Star Destroyer, Executor, Flagship Executor)
        spec["card_type"] = re.sub(r"(?<![_\w])([A-Z]{3,})(?=-CLASS\b)", r"_\1_", spec.get("card_type") or "")
    return finish(spec)


# rev 81 (sites 2): label placements that differ from the preset on a printing's face (master px; for landscape cards
# with labels_rotated the portrait x runs up the right margin). Finalizer (AI): the art credit 46.5 px (745) higher
# than on Finalizer (printed 210..440 against 256..486), so the redraw lies over the scan's own credit
LABEL_PLACE = {"204_54^AI": {"concept": {"x": 95}}}
WIDE_PRINTED = {"13_75", "4_167", "9_157", "204_54", "204_54^AI", "200_41^ALT", "204_47^ALT"}   # QA 2026-10-15: every non-location scan printed landscape (rev 81 sites 2: by printing id)   # Decipher cards printed landscape: Maul's Double-Bladed Lightsaber (Reflections III)



def is_wide_printed(gid) -> bool:
    """rev 81 (sites 2): is this printing landscape? By the printing's own id: the PC's alternate-image printings carry the
    card's id with a ^ suffix and are not always printed like their card. Checked on the PC gifs: Finalizer and
    Finalizer (AI) both 1039 x 745; I Must Be Allowed To Speak (V) and Bow To The First Order 745 x 1039 (portrait),
    their (ALT) printings 1039 x 745 (the old entries 200_41 / 204_47 turned the portrait cards landscape)."""
    return str(gid or "") in WIDE_PRINTED


def objective_text(t: str, front: bool) -> str:
    """Decipher's Objective layout: the setup sentence(s) in italics, then a paragraph per *For* / *While* / *Flip*."""
    # the PC JSON marks the keywords {For} (-> *For*) or not at all: "For remainder of game", "While this side up",
    # "Flip this card" always open a paragraph on the printed Objectives
    # rev 77: "Place out of play" and "Immediately retrieve" open their own paragraph too (In The Hands Of The Empire,
    # Systems Will Slip Through Your Fingers, Save You It Can, Or Be Destroyed); the 2010s PC text leaves them unmarked
    t = re.sub(r"(?<![*\w])(For remainder of game|While this side up|Flip this card|Place out of play|Immediately retrieve)", lambda m: "*" + m.group(1).split()[0] + "*" + m.group(1)[len(m.group(1).split()[0]):], t)
    t = re.sub(r"\s+(\*(?:For|While|Flip|Place|Immediately)\*)", r"\n\1", t).strip()
    if front:
        first, sep, rest = t.partition("\n")
        if sep and not first.startswith("*"):
            t = f"_{first.replace('_', '')}_\n{rest}"   # ship names inside the italic setup line stay italic
    return t


# rev 77: the five printed Podracers' pilot flags (assets/icons/podracer-flag-<slug>.png, tools/cut_podracer_flags.py)
PODRACER_FLAGS = {"Anakin's Podracer": "anakin", "Sebulba's Podracer": "sebulba", "Ben Quadinaros' Podracer": "ben-quadinaros",
                  "Dud Bolt's Podracer": "dud-bolt", "Teemto Pagalies' Podracer": "teemto-pagalies"}


def finish(spec: dict) -> dict:
    for lb_ in spec.get("labels") or []:   # rev 81 (sites 2): per-printing label placement measured on the printed face
        if isinstance(lb_, dict):
            lb_.update(LABEL_PLACE.get(str(spec.get("gempId") or ""), {}).get(lb_.get("preset"), {}))
    if spec.get("slip_type") == "Podracer" and not spec.get("podracer_flag"):
        fl = PODRACER_FLAGS.get(re.sub(r"[•\u2022<>]", "", spec.get("title") or "").replace("(V)", "").strip())
        if fl:
            spec["podracer_flag"] = fl
    ps = spec.pop("_printed_stats", None)
    if ps:   # stat boxes transcribed from the printed card (gempdata/fill.json "printedStats")
        spec["stats"] = [list(x) for x in ps]
    for st in spec.get("stats") or []:   # printed cards show halves as ½ (Hunchback: ABILITY 1½)
        if len(st) > 1 and re.fullmatch(r"\d*\.5", str(st[1] or "")):
            st[1] = str(st[1]).split(".")[0].lstrip("0") + "½"
    for k in ("game_text", "dark_text"):   # PC placeholders for an empty text half: "(none).", "Blank.", "-"
        spec[k] = re.sub(r"^\s*Text:\s*", "", spec.get(k) or "")   # a stray "Text:" label (Boba Fett, Bounty Hunter)
        if re.fullmatch(r"\s*([(<]none[)>]\.?|Blank\.?|-|\.|none\.?)\s*", spec.get(k) or "", re.I):
            spec[k] = ""
    if spec.get("slip_type") == "Objective":
        spec["game_text"] = objective_text(spec.get("game_text") or "", True)
        spec["game_text_back"] = objective_text(spec.get("game_text_back") or "", False)
    if is_wide_printed(spec.get("gempId")) or spec.pop("_wide", False):
        spec["wide"] = True
    if spec.get("deploy") is None:
        spec.pop("deploy", None); spec.pop("forfeit", None)
    for k in ("title", "caption", "title_back", "lore", "game_text", "dark_text", "game_text_back"):   # rev 80: as printed
        if spec.get(k):
            spec[k] = apostrophes(spec[k])
    if decipher_print(spec):
        spec["decipher_print"] = True   # Rev 80: Decipher's own title setting and ink (editor: "As Decipher printed it")
        # rev 81: a creature's ferocity formula prints a spaced en dash ("Ferocity = destiny – 1": Bog-wing both sides,
        # Nudj, Sleen); modifiers keep the hyphen as printed ("destiny -1 > ability", "power -1", "deploy -1")
        if spec.get("game_text"):
            spec["game_text"] = re.sub(r"(Ferocity = destiny) ?- ?(\d)", "\\1 – \\2", spec["game_text"])
    return spec


def dc_ellipses(t: str) -> str:
    """Rev 81: lore ellipses as Decipher printed them: spaced ". . ." (31 of 33 printed lore ellipses checked, Premiere to
    Reflections III), no space before, one space before a following word ("Luke. . . She", "“. . . I know"). Already
    spaced ones (corrections.json) are left as they are."""
    t = re.sub(r"\s*(?:\.{3}|…)", ".\u00a0.\u00a0.", t)   # no-break spaces: the dots never split over a line end
    return re.sub(r"\.[ \u00a0]\.[ \u00a0]\.(?=[A-Za-z0-9])", lambda m: m.group(0) + " ", t)


def dc_bold(t: str, set_id) -> str:
    """Rev 81 (text data 2): keywords Decipher set bold in game text. "Agenda"/"Agendas" (not the colon) on every
    Coruscant / Reflections III senator (Horox Ryyder, Mas Amedda, Aks Moe, Tikkes, Sio Bibble). "cumulatively" in
    A New Hope to Special Edition (Rebel Tech, Death Star Gunner, Frozen Dinner, Mynock, Ortolan, Ugnaught, Aqualish,
    Nudj, Sleen, Something Hit Us!); Endor and Death Star II print it regular (AT-ST Pilot, Navy Trooper Shield
    Technician, Imperial Academy Training, Scimitar Squadron TIE)."""
    t = re.sub(r"(?<![*\w])(Agendas?)(?=:)", r"*\1*", t)
    if str(set_id or "").isdigit() and 1 <= int(set_id) <= 7:
        t = re.sub(r"(?<![*\w])([Cc]umulatively)(?![*\w])", r"*\1*", t)
    return t


def decipher_print(spec: dict, card: dict | None = None) -> bool:
    """Rev 80: is this spec a Decipher printing (spec "decipher_print", else inferred from its source set)?"""
    if spec.get("decipher_print") is not None:
        return bool(spec["decipher_print"])
    if spec.get("style") == "ovs" or (card or spec).get("set_mark") or spec.get("virtual_set") or (spec.get("language") or "en") != "en":
        return False   # PC / OVS cards, and Takara's Japanese printings (their own typesetting, lang_ja.py) unless asked
    sid = str((spec.get("source") or {}).get("set") or "").strip()
    # a Decipher set's own card, or a new card with no source set and no PC set mark (rev 80 sphere-copyright audit)
    return sid in DECIPHER_SETS or not sid


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
    if decipher_print(spec) and (spec.get("language") or "en") == "en":   # rev 81: Decipher's bold keywords (dc_bold)
        for k in ("game_text", "dark_text", "game_text_back"):
            if isinstance(c.get(k), str):
                c[k] = dc_bold(c[k], (spec.get("source") or {}).get("set"))
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
        # printed Decipher cards with no sphere: the first disc takes the sphere's place. PC Virtual cards keep the disc in
        # the second slot even with no sphere (Aayla Secura VS0, You Know What I've Come For, #63)
        card["ring_fill"] = not str(card.get("set_mark") or "").startswith("pc:")
        # Rev 80: the card as Decipher printed it (1995-2001): Decipher's title setting and ink on the Effect / Interrupt
        # frames. Default: a Decipher set's own card (GEMP set 1-199) without a PC set mark; the spec's decipher_print
        # (true / false) decides otherwise (custom cards keep the PC look)
        if decipher_print(spec, card):
            card["decipher_print"] = True
            card["dc_expansion"] = spec.get("expansion")   # rev 81: Decipher's text setting differs by set (render.DC_EARLY)
            if card.get("lore"):
                card["lore"] = dc_ellipses(card["lore"])   # rev 81: Decipher spaced its lore ellipses ". . ."
        card["copyright_split"] = True          # systems print Lucasfilm left / Decipher right (Dagobah)
        card["expansion_icon_in_hole"] = True   # printed Decipher cards: the sphere sits in a black hole of the frame (2-1B)
        # rev 80: a card of one of Decipher's own sets (or a new card with no Players Committee set mark) takes the sphere
        # and copyright line where Decipher printed them (render.DC_PRINT); PC and Virtual Block cards keep the PC's
        # (one definition for both: decipher_print() above; the editor's "As Decipher printed it" box overrides)
        card["art_scan"] = spec.get("_art_kind") == "scan"   # the printed face is the picture (full-art cards carry their own line)
        _d2 = DISC2_DECIPHER.get(str((spec.get("source") or {}).get("set")))
        if card.get("decipher_print") and card.get("disc2") and _d2:
            card["disc2_title_dx"], card["disc2_title_ls"], card["disc2_title_dw"] = _d2
        if card.get("decipher_print") and str((spec.get("source") or {}).get("set")) == "11" and card["template"] == "ls-epic-event":
            card["copyright_ink"] = "#fff"   # rev 81: Boonta Eve Podrace, I Did It! print the line white on the purple (other Light Epic Events black)
            # rev 81 (geometry 2): line measured against the card body on both printed faces (Boonta Eve Podrace 11_24,
            # I Did It! 11_25): 1.3 px (745) right and 2.6 px lower than ours
            card["copyright_dxy"] = (3, 6)
        if card["template"] == "ls-jeditest-tall" and (spec.get("slip_type") or "").startswith("Jedi Test"):
            card["template"] = "ls-jeditest-olive"   # printed Jedi Tests are olive throughout (Domain Of Evil)
        if spec.get("slip_type") == "Podracer":
            card["disc"] = "podracer"   # Episode I Podracers: the podracer type disc (Game Aid icon)
            if spec.get("_podracer_flag_file"):   # rev 77: the editor's own flag image (podracer_flag_data)
                card["podracer_flag_file"] = spec["_podracer_flag_file"]
            elif spec.get("podracer_flag"):
                card["podracer_flag"] = spec["podracer_flag"]
        if spec.get("gempId") in UNDERCOVER_FRAME and spec.get("side") == "Light" and "rebel" in (spec.get("affiliation") or "").lower():
            card["disc"] = "rebel"   # the Rebel disc on the Dark frame (TK-422, Boushh)
        if card["template"].endswith("-mission"):
            card["disc"] = "mission"   # the teal hologram type disc
        if card["template"] == "ds-starship-wide" and not (spec.get("lore") or "").strip():
            card["template"] = "ds-starship-wide-nolore"
        if (card["template"].startswith("ds-starship-wide") or card["template"].startswith("rg-")) and str(card.get("set_mark") or "").startswith("pc:"):
            card["template"] += "-pc"   # rev 81: the PC's landscape Finalizers and (ALT) Effects: their own banner, set mark, disc and labels
        if card["template"] in ("ls-character-droid", "ds-character-droid"):
            card["template"] += "-dc"   # brass droid disc as printed
        if card["template"] == "creature":
            card["template"] = "creature-dc" if card.get("decipher_print") else "creature-dc-pc"   # printed Decipher creature: banner + black title (rev 81: measured layout on Decipher's own)
    card["id"] = "cm-" + re.sub(r"[^A-Za-z0-9_-]+", "_", spec.get("title") or "card")[:40]
    card["caption"] = spec.get("caption") if spec.get("caption") is not None else spec.get("title", "")
    if card.get("back"):   # rev 77: the back face's margin caption follows the front's (Decipher printings: none), not
        bt = card["back"].get("title") or ""   # build_vs's slip default "<back title> (V)"
        if spec.get("caption_back") is not None:
            card["back"]["caption"] = spec["caption_back"]
        elif not (card["caption"] or "").strip():
            card["back"]["caption"] = ""
        else:
            card["back"]["caption"] = bt + (" (V)" if card["caption"].rstrip().endswith("(V)") and not bt.rstrip().endswith("(V)") else "")
    card["number"] = str(spec.get("number") or "")
    if spec.get("border") == "white":
        card["border"] = "white"
    # rev 77 printing variants: uniqueness dot colour (Eriadu's white dot), Lando In Millennium Falcon's thick forfeit
    # border, Reflections foil sheen. Absent / default values leave the card exactly as before.
    if str(spec.get("bullet_colour") or "red").lower() != "red":
        card["bullet_colour"] = spec["bullet_colour"]
    try:
        if float(spec.get("forfeit_box_border") or 0) > 0:
            card["forfeit_box_border"] = max(0.0, min(40.0, float(spec["forfeit_box_border"])))
    except (TypeError, ValueError):
        pass
    if spec.get("foil"):
        card["foil"] = True
    for k in ("labels", "errata_mark", "text_fit", "text_adjust", "lore_adjust", "art_credit", "caption_italic", "disc_left", "mission_disc", "margin_disc", "lore_lines", "text_breaks"):   # PC labels (D-E1 …) and text-fit limits (Bill 2026-11-01)
        if spec.get(k):
            card[k] = spec[k]
    if vs is None:
        card.pop("virtual_set", None)
    if spec.get("_set_icon_file"):
        card["set_icon_file"] = spec["_set_icon_file"]
    if spec.get("_art"):
        card["art"] = spec["_art"]
        card.pop("art_trim", None)
        if spec.get("_art_kind") == "scan" and str((spec.get("source") or {}).get("set") or "").startswith("100") and os.environ.get("CM_LEGACY_TRIM"):
            card["art_trim"] = True
            if any(k in (spec.get("slip_type") or "") for k in ("Interrupt", "Effect")):
                card["legacy_scan"] = True   # Virtual Block scans: the PC's slips sit their banner/stat bar a little higher (A Jedi's Patience (V))
    if spec.get("_art2"):   # rev 77: second picture of a split window (Reflections II combos): spec art2 + split
        card["art2"] = spec["_art2"]
        if isinstance(spec.get("split"), dict):
            card["split"] = spec["split"]
    if spec.get("slip_type") == "Game Aid" and spec.get("_art_kind") != "upload":
        card.pop("art", None)   # the chart's own starfield is drawn (the scan carries the printed chart)
    if not spec.get("expansion"):
        card["expansion_icon"] = None
    src_exp = SETS.get(str((spec.get("source") or {}).get("set")))
    if not ovs and spec.get("expansion"):
        card["draw_system_ring"] = True
    gid_ = (spec.get("source") or {}).get("gempId") or spec.get("gempId") or ""
    if (spec.get("language") or "en") != "en":
        apply_language(spec, card)
    if spec.get("style") == "early-slip" or spec.get("early_slip"):
        # rev 75: the original card as Decipher printed it, under the 2002 Virtual Set #1 paper slip (early_slip.py):
        # the printed title has no "(V)"; the slip carries the virtual deploy / forfeit / game text
        import early_slip
        card["early_slip"] = early_slip.resolve(spec, card)
        es_ = spec.get("early_slip") if isinstance(spec.get("early_slip"), dict) else {}
        if isinstance(es_.get("under_text"), str):   # the original card's own text, where it shows round the cut slip
            card["game_text"] = es_["under_text"][:1500]
        if not es_.get("keep_v_title"):
            card["title"] = re.sub(r"\s*\(V\)\s*$", "", card.get("title") or "")
        return card
    if spec.get("pc_typeset") is not False and re.fullmatch(r"10\d\d[a-z]?_L\d+", gid_ or "") and not ovs \
            and not card["template"].startswith(("loc-", "ls-jeditest", "objective", "epic-event")):
        card["pc_type"] = spec["pc_typeset"] if isinstance(spec.get("pc_typeset"), dict) else legacy_typeset(gid_, card["template"], spec.get("side"))   # systems: the scan carries its own sphere; draw ours when there's none or it changed
    return card


LANGUAGES = {"en": "English", "ja": "Japanese (Takara 1997-98)"}   # rev 77: printing language; a new one = a lang_<code>.py module


def apply_language(spec: dict, card: dict) -> dict:
    """rev 77: a card printed in another language (spec "language"). The English printing's frame and pieces stay; the
    language module draws what that printing changed (lang_ja.py: Takara's Japanese cards). Title, lore and game text are
    typed in that language; English stat labels / banners are translated where the printed word is known."""
    lang = spec.get("language")
    if lang != "ja":
        return card
    import lang_ja
    card["lang"] = "ja"
    card["title"] = lang_ja.title(card.get("title") or "")
    if card.get("card_type"):
        card["card_type"] = lang_ja.card_type(card["card_type"])
    if spec.get("printed_breaks"):   # editor: each typed line is a printed line
        for key, dest in (("lore", "lore_lines"), ("game_text", "text_breaks")):
            parts = [x for x in (card.get(key) or "").split("¶") if x.strip()]
            if len(parts) > 1 and not card.get(dest):
                card[dest] = parts
                card[key] = "".join(parts)
    if not spec.get("halfwidth"):   # rev 80: Takara's figures and Latin letters are full width (３フォース, 能力値＞２)
        for key in ("lore", "game_text"):
            card[key] = lang_ja.fullwidth(card.get(key))
        for key in ("lore_lines", "text_breaks"):
            if isinstance(card.get(key), list):
                card[key] = [lang_ja.fullwidth(x) for x in card[key]]
    cr = card.get("copyright") or ""
    if not spec.get("keep_copyright") and re.search(r"19\d\d LUCASFILM", cr):
        card["copyright"] = lang_ja.copyright_for(spec.get("expansion")) or cr   # Takara's line: 1997 (Premiere, ANH), 1998 (Hoth)
    return card


def legacy_marks(t: str) -> str:
    """The Virtual Legacy version record (legacy-versions-v4) writes the printed Reserve Deck arrows as [S] (▲, take into
    hand) and [T] (▼, deploy), as the slips print them; Immune to Sense is always spelled out there ("(Immune to Sense.)",
    "[Immune to Sense]"). Only for version texts: in GEMP / PC card data [S] stays the Immune to Sense mark (rev 72)."""
    t = (t or "").replace("[S]", "▲").replace("[T]", "▼")
    return re.sub(r"(?<=[.!?:)\"'”’])[ \t]{2,}", " ", t)   # the 2012-13 card list puts two spaces after a sentence


def polish_text(t: str, pc_era: bool = True, legacy_version: bool = False) -> str:
    """GEMP / PC card-list game text -> CardMaker codes, the same steps gemp_to_spec applies to a card's own text."""
    if legacy_version:
        t = legacy_marks(t)
        t = re.sub(r'"([^"]+)"', "\u201c\\1\u201d", t)   # rev 73: GEMP-copied version texts write straight double quotes (Rebel Aces)
    t = ship_text(maintenance(gt_quotes(game_text(t))))
    if pc_era:
        t = pc_shorthand(t)
    t = apostrophes(t)
    if legacy_version:
        t = t.replace("{ga:vader}", "{ga:disc-vader}")
    if re.match(r"\s*(USED|LOST|STARTING):", t):
        t = re.sub(r"\s+(LOST|STARTING|USED):", r"\n\1:", t)
    return t


def apply_version(spec: dict, v: dict, text: bool = True) -> dict:
    """Put one published version's text (gempdata/legacy_versions.json, from legacy-versions-v4) on a Virtual Legacy spec
    (STANDARD rev 71). Everything else (art, frame, title, lore, icons, slip number) stays the printed card's.
    Rev 73: the version's recorded stats (`stats`: destiny …; stat-only versions such as Jedi Survivor (V) PC-E1) go on
    too; text=False keeps the card's own text (a recorded text that lost its icons, opened without ?version)."""
    if v.get("early_slip"):   # rev 75: a VO version whose image is a 2002 paper slip (early_slip.py)
        spec["style"] = "early-slip"
        spec["early_slip"] = v["early_slip"] if isinstance(v["early_slip"], dict) else {}
    for k, val in (v.get("stats") or {}).items():
        if k in ("destiny", "deploy", "forfeit"):
            spec[k] = str(val)
        else:
            lab = {"hyperspeed": "HYPERSPEED", "landspeed": "LANDSPEED"}.get(k, k.upper())
            for row in spec.get("stats") or []:
                if row and row[0] == lab:
                    row[1] = str(val)
    spec["version_id"] = v.get("id")
    if not text:
        return spec
    t = polish_text(v.get("text") or "", legacy_version=True)
    if spec.get("slip_type") == "Character":   # sheets / Master List print the pilot icon as "3." (icon lost): "[Pilot] 3"
        t = re.sub(r"^\s*\{icon:pilot\}\s*(\d)\.?\s+|^\s*(\d)\.\s+(?=[A-Z])", lambda m: "{pilot:%s}. " % (m.group(1) or m.group(2)), t)
    part = (v.get("part") or "game_text").lower()
    if spec.get("slip_type") == "Objective" and part in ("front", "back"):
        spec["game_text" if part == "front" else "game_text_back"] = objective_text(t, part == "front")
    elif part in ("ds", "dark"):
        spec["dark_text"] = t
    else:   # game_text, ls, and the rotated halves of the few 4-way cards
        spec["game_text"] = t
    spec.pop("game_text_lines", None)
    spec["version_id"] = v.get("id")
    return spec


# rev 74: Virtual Legacy typesetting read from the PC's master list PDFs (tools/legacy/typeset/): each card's text frame,
# Akzidenz size, tracking and pitch, so the same words land on the same lines as the PC's card (Bill 2026-11-10).
_TYPESET = None


def legacy_typeset(gid: str, template: str, side: str) -> dict | None:
    global _TYPESET
    if _TYPESET is None:
        import json
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gempdata", "legacy_typeset.json")
        try:
            _TYPESET = json.load(open(p, encoding="utf-8"))
        except OSError:
            _TYPESET = {"templates": {}, "cards": {}}
    T = _TYPESET["templates"]
    base = template.replace("-dc", "") if template not in T else template
    tp = T.get(template) or T.get(base) or {}
    side_tp = T.get("ls-character-rebel" if side == "Light" else "ds-character-imperial", {})
    fx = (T.get("ls-effect" if side == "Light" else "ds-effect") or {})
    card = _TYPESET["cards"].get(gid or "", {})
    out = {}
    for b in ("gt", "lore"):
        c = card.get(b) or {}
        if b == "lore" and not c:
            # a slip covers only the card's lower half: title and lore stay the Decipher card's as printed (Decipher's
            # typesetting). Only a card the PC reprinted whole (a full card in the master list) has PC-set lore.
            continue
        d = dict(tp.get(b) or {})
        if b == "lore" and not d:   # templates the master list shows no full card of: the same side's lore frame
            d = dict((fx if "character" not in template else side_tp).get("lore") or {})
        if b == "gt" and "y" not in d and d:
            d["y"] = (side_tp.get("gt") or {}).get("y", 189.5)
        for k in ("x", "w", "size", "track", "pitch", "indent", "y"):
            if c.get(k) is not None:
                if k == "y" and b == "gt" and d.get("y") is not None and abs(c[k] - d["y"]) > 3:
                    if 5 < d["y"] - c[k] < 12:
                        d["raised"] = round(d["y"] - c[k], 2)   # the PC printed this card with its text box one line up
                    continue   # a raised text box (six lines, no-lore combos): text_grow moves it, from the template's line
                d[k] = c[k]
        if d.get("x") is not None and d.get("w"):
            d.setdefault("y", 189.5 if b == "gt" else 34.3)
            out[b] = {k: d[k] for k in ("x", "y", "w", "size", "track", "pitch", "indent", "raised") if k in d}
            if c.get("lines"):
                out[b]["lines"] = c["lines"]   # the PC's own line breaks (kept when the text is the same words)
    return out or None
