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
            "Scomp Link": "scomp"}


def game_text(t: str) -> str:
    t = t or ""
    t = re.sub(r"\{([A-Za-z][A-Za-z' ]*)\}", r"*\1*", t)   # GEMP marks bold words {Flip}; the renderer bolds *...*
    for k, v in INLINE.items():
        t = t.replace(k, v)
    for name, key in SET_TOKENS.items():
        t = t.replace(f"[{name}]", f"{{set:{key}}}")
    t = re.sub(r"\[Virtual Block (\d)\]", r"{vb:\1}", t)   # the 2009 Virtual Block diamonds
    t = re.sub(r"\[Set (\d{1,2})\]", r"{pcset:\1}", t)     # the modern Virtual Set marks
    return t


PRINTING_TAGS = r"V|AI|[^()]*\bAI|Premium|Light|Dark|Tatooine|Coruscant|Reflections I{1,3}|Death Star II|Cloud City|Endor|Hoth|Dagobah|Special Edition|Jabba's Palace|A New Hope|Theed Palace|Premiere|Errata|ALT"


def strip_printing(t: str) -> str:
    prev = None
    while prev != t:
        prev = t
        t = re.sub(rf"\s*\((?:{PRINTING_TAGS})\)(?=\s*(?:/|&|$))", "", t)
    return t


def pc_shorthand(t: str) -> str:
    """The Players Committee prints its own shorthand (Game Aid sheet): the card JSON spells it out."""
    t = re.sub(r"Adds (\d) to power of anything (?:he|she|it) pilots\.", r"{pilot:\1}.", t)
    t = re.sub(r"(?i)\bdeploy ([^.;()]+?) from (?:your )?Reserve Deck(?:; reshuffle)?", r"▼ \1", t)
    t = re.sub(r"(?i)\btake ([^.;()]+?) into hand from (?:your )?Reserve Deck(?:; reshuffle)?", r"▲ \1", t)
    t = t.replace("(Immune to {alter}.)", "{alter}").replace("(Immune to Alter.)", "{alter}")
    return t


def quotes(t: str) -> str:
    """The PC JSON writes printed double quotes as single ones: 'Vehicle with armor' -> “Vehicle with armor”."""
    return re.sub(r"(?<![\w])'(.+?)'(?![\w])", "\u201c\\1\u201d", t)


BASE_EXP: dict = {}   # title -> Decipher expansion of the original printing (filled by the server)


def gemp_to_spec(c: dict) -> dict:
    f = c["front"]
    side = c["side"]
    typ = f.get("type") or ""
    sub = f.get("subType") or ""
    icons = f.get("icons") or []
    title = strip_printing(f.get("title") or "")   # "(V)", "(AI)", "(Premium)", "(Tatooine)" … name the printing, not the card
    exp = SETS.get(str(c.get("set")))
    # the black caption strip is blank by default (Bill 2026-10-15): only some PC virtual cards print text there
    spec = {"side": side, "title": title, "caption": "", "number": "", "destiny": f.get("destiny") or "",
            "lore": "" if (f.get("lore") or "").strip().rstrip(".") == "Blank" else (f.get("lore") or ""), "game_text": game_text(f.get("gametext")), "icons": [], "stats": [],
            "deploy": f.get("deploy"), "forfeit": f.get("forfeit"), "scomp": "Scomp Link" in icons,
            "affiliation": None, "expansion": exp, "card_type": "", "gempId": c.get("gempId"),
            "source": {"gempId": c.get("gempId"), "imageUrl": f.get("imageUrl"), "set": c.get("set")},
            "copyright": copyright_for(c.get("set")), "set_mark": set_mark_for(c.get("set"))}
    if c.get("legacy"):   # 2009-2014 Virtual Blocks print "•Title (V)" in the bottom strip (Holotable faces)
        spec["caption"] = f.get("title") or ""
        if typ == "Defensive Shield":
            spec["shield_style"] = "fade" if side == "Light" else "vb"   # Virtual Block shields: Light red→cyan (Affect Mind (V)), Dark cyan→red (No Escape (V))
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
    spec["game_text"] = quotes(spec["game_text"])
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
    if typ in ("Starship", "Vehicle"):   # starships print their faction icon at the top of the column (Blockade Support Ship)
        col = [c_ for c_ in col if c_ in FACTION] + [c_ for c_ in col if c_ not in FACTION]
    rings = [RING[i] for i in icons if i in RING]
    if "Republic" in icons and typ == "Character":
        col = [c_ for c_ in col if c_ != "republic"]   # characters show Republic as the affiliation disc
    if typ == "Character":
        spec["slip_type"] = "Character"
        spec["affiliation"] = sub
        third = (f.get("extraText") or [""])[0] if sub == "Droid" else ""
        if sub == "Droid":
            spec["stats"] = [["POWER", f.get("power") or "0"], [third.upper() or "DROID", ""]]
        else:
            ab = f.get("ability") or ""
            spec["stats"] = [["POWER", f.get("power") or "0"], ["ABILITY", ab]]
            if f.get("politics"):
                spec["stats"].append(["POLITICS", f["politics"]])
            elif f.get("armor"):   # Mandalorians (Fenn Rau): ARMOR in the third box
                spec["stats"].append(["ARMOR", f["armor"]])
            elif f.get("extraText"):   # third box label: FORCE-ATTUNED, FORCE-SENSITIVE … (Lando)
                spec["stats"].append([str(f["extraText"][0]).upper(), ""])
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
        if typ == "Starship": st.append(["HYPERSPEED", f.get("hyperspeed") or "0"])
        else: st.append(["LANDSPEED", f.get("landspeed") or "0"])
        spec["stats"] = st[:3]
        spec["icons"] = col
    elif typ == "Location":
        spec["slip_type"] = "System" if sub in ("System", "Sector") else "Site"
        spec["card_type"] = title.upper()
        gt = f.get("gametext") or ""
        m = re.match(r"\s*(?:Light|LIGHT)\s*:?\s*(.*?)\s*(?:Dark|DARK)\s*:\s*(.*)$", gt, re.S)
        light, dark = (m.group(1), m.group(2)) if m else (gt, "")
        if not m:
            m2 = re.match(r"\s*(?:Dark|DARK)\s*:?\s*(.*?)\s*(?:Light|LIGHT)\s*:\s*(.*)$", gt, re.S)
            if m2: dark, light = m2.group(1), m2.group(2)
        spec["game_text"], spec["dark_text"] = game_text(light), game_text(dark)
        # icon boxes are drawn right to left from the list: scomp outermost, then planet, then the rest (Docking Bay 94)
        li = [LOC_ICON[i] for i in reversed(icons) if i in LOC_ICON]
        li.sort(key=lambda k: {"scomp": 0, "planet": 1}.get(k, 2))
        spec["light_icons"] = spec["dark_icons"] = li
        spec["light_force"] = bool(f.get("lightSideIcons")); spec["dark_force"] = bool(f.get("darkSideIcons"))
        spec["light_force_count"] = int(f.get("lightSideIcons") or 0); spec["dark_force_count"] = int(f.get("darkSideIcons") or 0)
        if f.get("parsec"): spec["parsec"] = f["parsec"]
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
    elif typ in ("Weapon", "Device"):
        spec["slip_type"] = f"{sub} {typ}".strip()
        spec["card_type"] = f"{sub} {typ}".upper().strip()
    elif typ == "Creature":
        spec["slip_type"] = "Creature"; spec["card_type"] = f"{sub.upper()} CREATURE" if sub else "CREATURE"
        fer = str(f.get("ferocity") or "").strip()
        st = []
        if fer:
            if re.fullmatch(r"[0-9.½]+", fer):
                st.append(["FEROCITY", fer])
            else:   # "destiny -1", "two destiny": the printed cards show ✶ and explain it in the game text (VS4 Wampa)
                st.append(["FEROCITY", "✶"])
                if "ferocity" not in spec["game_text"].lower()[:60]:
                    spec["game_text"] = f"✶ Ferocity = {fer}. " + spec["game_text"]
                else:
                    spec["game_text"] = re.sub(r"^\s*\*\s*Ferocity", "✶ Ferocity", spec["game_text"])
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
    elif typ == "Epic Event":
        spec["slip_type"] = "Epic Event"
    elif "Admiral" in typ:
        spec["slip_type"] = "Admiral's Order"
    else:
        spec["slip_type"] = typ or "Effect"; spec["card_type"] = typ.upper()
    return finish(spec)


WIDE_PRINTED = {"13_75"}   # Decipher cards printed landscape: Maul's Double-Bladed Lightsaber (Reflections III)


def objective_text(t: str, front: bool) -> str:
    """Decipher's Objective layout: the setup sentence(s) in italics, then a paragraph per *For* / *While* / *Flip*."""
    # the PC JSON marks the keywords {For} (-> *For*) or not at all: "For remainder of game", "While this side up",
    # "Flip this card" always open a paragraph on the printed Objectives
    t = re.sub(r"(?<![*\w])(For remainder of game|While this side up|Flip this card)", lambda m: "*" + m.group(1).split()[0] + "*" + m.group(1)[len(m.group(1).split()[0]):], t)
    t = re.sub(r"\s+(\*(?:For|While|Flip)\*)", r"\n\1", t).strip()
    if front:
        first, sep, rest = t.partition("\n")
        if sep and not first.startswith("*"):
            t = f"_{first}_\n{rest}"
    return t


def finish(spec: dict) -> dict:
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
        card["ring_fill"] = True
        card["copyright_split"] = True          # systems print Lucasfilm left / Decipher right (Dagobah)
        card["expansion_icon_in_hole"] = True   # printed Decipher cards: the sphere sits in a black hole of the frame (2-1B)
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
    if not spec.get("expansion"):
        card["expansion_icon"] = None
    src_exp = SETS.get(str((spec.get("source") or {}).get("set")))
    if not ovs and spec.get("expansion") and (not spec.get("_art") or spec.get("_art_kind") != "scan" or spec["expansion"] != src_exp):
        card["draw_system_ring"] = True   # systems: the scan carries its own sphere; draw ours when there's none or it changed
    return card
