"""Rev 84 (Decipher printed text): gempdata/decipher_printed.json from a dump of wiki.swccg.com.

GEMP carries each card's current text, which for a card that got errata (Decipher's Glossary Version 2.0 / Glossary
Supplement, or the Players Committee's Advanced Rulebook Appendix A) is the errata, not what Decipher printed. The wiki
keeps the printed face on its own page:

  * the printed page's card_uid is the GEMP id + "o" (Jek Porkins 1_13o, Sandcrawler: Loading Bay 2_66o); the errata
    page carries the GEMP id itself: "<Title> (Errata)" (Decipher errata, version_label "errata (Decipher Glossary
    ...)") or "<Title> (PC Errata)" (version_label "PC Errata ..."); "<Title> (Original)" is a redirect to the printed
    page, or (version_label "printed (Decipher archive)") a second printed page, which wins when they disagree;
  * a card with no errata has one page, card_uid = the GEMP id, version_label "printed": nothing to do.
  * uniqueness: the wiki's uniqueness field on the printed pages is copied from the errata page (equal on all 491), so
    printed bullets come from the errata documents instead: Errata.wiki rows "Errata face (• unique)" / "(•••
    restricted)" and Appendix A notes "print: (non-unique)" / "print: no uniqueness" (Decipher printed no bullet), plus
    UNIQUENESS_SEEN (read off the printed faces).

Only fields whose words differ from GEMP's are written (markup, quote style, ellipsis spacing and the wiki's own field
gaps are not differences), in GEMP's own raw conventions (straight quotes, "Light: … Dark: …", "Front: … Back: …"), so
webapp/adapter.py runs them through the same text pipeline as every other card.

    python3 tools/make_decipher_printed.py [/path/to/swccg-wiki/pages]
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/swccg-wiki/pages"
OUT = os.path.join(ROOT, "gempdata", "decipher_printed.json")
sys.path.insert(0, os.path.join(ROOT, "webapp"))
from adapter import DECIPHER_SETS  # noqa: E402

# printed bullets read off the printed faces (wiki Decipher-archive scans), where no errata document names the change
UNIQUENESS_SEEN = {
    "Sandcrawler: Loading Bay": "•",    # ANH-L-sandcrawlerloadingbay-decipher-archive.gif: one bullet; PC errata •••
    "Sandcrawler: Droid Junkheap": "•",  # ANH-D-sandcrawlerdroidjunkheap-decipher-archive.gif: one bullet; PC errata •••
    # rev 84 (2): title strips of all 512 faces compared with ours: these print no bullet (Glossary made them unique /
    # restricted: "•Legendary Starfighter", "••Floating Refinery")
    "Do, Or Do Not": "",
    "Legendary Starfighter": "",
    "Floating Refinery": "",
}
# read off the printed faces (Decipher archive scans on the wiki) where the wiki's printed page has no separate text:
# (wrong, right) replacements over GEMP's raw text, on Decipher printings only
PRINTED_SEEN = {
    # Dantooine Base Operations / More Dangerous Than You Realize: “blown away.” in double quotes on both faces, "site"
    # set italic on the front (SE-L-dantooinebaseoperations / -moredangerousthanyourealize-decipher-archive.gif)
    "7_135": {"gametext": [("is 'blown away.'", "is “blown away.”"), ("is 'blown away.'", "is “blown away.”"), ("one site or", "one _site_ or")]},
    # Plead My Case To The Senate: the front prints "at least one with with a peace agenda" (Cor-L-pleadmycasetothesenate)
    "12_88": {"gametext": [("at least one with a peace agenda", "at least one with with a peace agenda")]},
    # errata'd cards the wiki keeps no printed page for: the printed text read off the wiki's Decipher-archive faces
    # (<set>-<side>-<name>-decipher-archive.gif/.jpg, ANH-L-sorryaboutthemess-hires.webp); a string replaces the whole
    # text, pairs replace the first occurrence (an Objective's front comes before its back)
    "101_3": "At any time, move Luke (for free) to a battle just initiated at an adjacent site. Luke is power +2 during that battle, unless Vader is present or adjacent to the battle site. OR You may cancel Vader's Obsession.",
    "106_1": "When deployed, you may immediately search your Reserve Deck, take one non-unique alien into hand and reshuffle. Adds 2 to power of any starship he pilots. Your aliens deploy -1 to same or adjacent Tatooine site.",
    "106_11": "When deployed, you may immediately search your Reserve Deck, take one non-unique alien into hand and reshuffle. Adds 2 to power of any starship he pilots. Your aliens deploy -1 to same or adjacent Tatooine site.",
    "106_10": "Deploy -2 to same location as Darth Vader or at Death Star. Permanent pilot aboard provides ability of 2 and adds 2 to power. Adds 1 to its weapon destiny draws.",
    "106_15": "Deploy -1 at any cloud sector. Permanent pilot aboard provides ability of 2 and adds 2 to power. Power +2 at non-unique cloud sectors. Boosted TIE Cannon may deploy here and fires free here.",
    "106_13": "May add 3 pilots, 6 passengers and 4 TIEs. Has ship-docking capability. Permanent pilots aboard provide total ability of 2. Turbolaser Battery may deploy here. Your TIEs present are each power +1.",
    "106_7": "Deploy -2 at Yavin 4 or to same location as Red Leader. Permanent pilot aboard provides ability of 2 and adds 2 to power. Proton Torpedoes deploy and fire free here.",
    "1_117": "Sacrifice (forfeit) a droid to cancel all attrition against you at same site this turn. OR Re-target an opponent's weapon to one of your droids at same site. If droid is lost, use original target's forfeit number.",
    "1_123": {"gametext": [("all imprisoned characters", "all captured characters")]},
    "1_142": "May add 2 pilots or passengers, and 1 astromech. Must have pilot aboard to use power, maneuver or hyperspeed.",
    "1_288": "Dark: Your starships deploy -1 here, -2 if Tarkin is present. If you control, Kessel Run is prevented (canceled). Light: Total ability of 6 or more required for you to draw battle destiny here.",
    "1_312": "Use 2 Force to deploy on any warrior. May target using 2 Force. Draw destiny. Character hit if destiny +1 > ability. Vehicle hit if destiny +1 > maneuver or armor.",
    "2_23": "Adds 3 to power of any starship he pilots. On Red 2, also adds 2 to maneuver and draws one battle destiny if not able to otherwise. May use 1 Force to search your Reserve Deck and take one Corellian Slip into hand. Shuffle, cut and replace.",
    "2_57": "During your control phase, fire one of your weapons (at normal use of the Force). If Han firing, may add 1 to destiny draw. (A seeker may be targeted by a character weapon as if it has maneuver of 4.) Hit target is immediately lost.",
    "2_58": "If Chewbacca is defending a battle alone at a site, add two battle destiny. OR Use 3 Force to search through your Reserve Deck and take Chewbacca into your hand. Shuffle deck, cut and replace. OR Scare off (lose) one 'mouse' droid on table.",
    "2_139": "During your control phase, fire one of your weapons (at normal use of the Force). If URoRRuR'R'R firing, add 2 to destiny draw. (A seeker may be targeted by a character weapon as if it has maneuver of 4.) Hit target is immediately lost.",
    "2_156": "May carry 3 passengers. Permanent pilot aboard provides ability of 1. May move as a 'react.' *Landspeed = 3. OR Up to 3 characters may shuttle to or from same site for free.",
    "3_20": {"gametext": [("Adds 2 to power of anything he pilots.", "Adds 2 to power of any starship he pilots.")]},
    "3_25": "If aboard a starship as a passenger, adds 1 to starship's weapon destiny draws (adds 3 if aboard Rogue 3 or with Wedge or Jek).",
    "3_27": "Adds 2 to power of any starship he pilots. On Rogue 2, also adds 3 to maneuver and may draw one battle destiny if not able to otherwise.",
    "3_50": "During your control phase, target a vehicle with armor at same site as one of your warriors. Draw destiny. If warrior has a Concussion Grenade or a lightsaber, add 3 to destiny draw (7 if both). Vehicle (and grenade) lost if total destiny > armor.",
    "3_64": "Light: If you control, opponent's bounty hunters are forfeit -2. Dark: Your bounty hunter pilots add an additional 1 to power of starships they pilot here.",
    "3_81": "Deploy at same exterior site as one of your mining droids. 'Explodes' if starfighter or non-creature vehicle deploys or moves to or across same site. Draw destiny. Vehicle lost if destiny +2 > armor or maneuver. Starfighter lost if destiny > 3. Vehicle Mine is also lost.",
    "4_7": "Habitat: planet sites (except Hoth). Attacks by attaching to character. X = 0. Every move phase, draw destiny; each time destiny > ability, add 1 to X. Character is power -X (eaten if power = 0).",
    "4_74": "During a battle, before any cards have been forfeited, cause all attrition for both sides to be reduced to zero.",
    "5_91": "Adds 3 to power of any starship he pilots. On Slave I, also adds 2 to maneuver and draws one battle destiny if not able to otherwise. When escorting a captive, captive is forfeit +5. May 'fly' (landspeed = 3). Immune to attrition < 3.",
    "7_110": "Light: Your spies deploy -1 here and at related sites. If you control, Undercover is immune to Hutt Smooch. Dark: Force drain -X here, where X = number of spies opponent has on table.",
    "7_123": {"gametext": [("Neither player may Force drain here.", "Opponent's Force drains here are canceled. You may not Force drain here.")]},
    # Hidden Base / Systems Will Slip Through Your Fingers: both faces (SE-L-hiddenbase / -systemswillslipthroughyourfingers
    # -decipher-archive.gif); "system(s)" set italic throughout
    "7_136": "Hidden Base: Deploy Rendezvous Point. Place a planet _system_ (with a parsec number from 1 to 8) from Reserve Deck face down on your side of table (not in play); that card indicates the planet where your “Hidden Base” is located. {While} this side up, once during each of your deploy phases, may deploy one _system_ from Reserve Deck; reshuffle. Opponent loses no more than 1 Force from each of your Force drains at _systems_ and sectors. {Flip} this card any time after the _system_ matching your “Hidden Base” indicator has been deployed. Systems Will Slip Through Your Fingers: {While} this side up, to draw a card from Force Pile, opponent must first use 1 Force. For each battleground _system_ you control, you may cancel one opponent's Force drain (limit twice per turn). You may not deploy any _systems_. At each _system_ opponent occupies during any draw phase, opponent may 'probe' there by placing one card from hand face down beneath that _system_. {Place} out of play if “Hidden Base” _system_ is 'probed;' Dark Side places 'probe' cards in Used Pile (and may retrieve 1 Force for each Probe Droid used to 'probe').",
    "8_78": {"gametext": [("into hand from Reserve Deck; reshuffle", "into hand; reshuffle"), ("if Bunker 'blown away'", "if Bunker “blown away”"),
                          ("if Endor 'blown away.'", "if Endor “blown away.”"),
                          # back (Endor-L-garrisondestroyed-decipher-archive.gif)
                          ("except by a 'react'.", "except by a 'react.'"), ("(unless Bunker 'blown away')", "(unless Bunker “blown away”)"),
                          ("during an opponent's move phase", "during opponent's move phase"), ("if Endor is 'blown away'.", "if Endor is “blown away.”")]},
    "9_61": {"gametext": [("Alter, Strangle, or Captive Fury", "Alter, Strangle or Captive Fury"),
                          ("transfer Luke to Vader, if present with Vader.", "transfer Luke to Vader, if present.")]},   # back: DS2-L-icansavehim
    # Hindsight: the printed (mirrored) face, pricecharting.com/game/star-wars-ccg-cloud-city/hindsight
    "5_26": {"gametext": [("Also, during each draw phase,", "Also, at the end of every turn,")]},
    # Rebel Guard prints POWER * (GEMP 0); DFS Squadron Starfighter (below) ARMOR 2 (GEMP: maneuver 2)
    "1_26": {"power": "*"},
    "10_27": "USED: During opponent's turn, take up to four cards from your hand and place them on top of your Force Pile. LOST: During a battle, before any cards have been forfeited, cause all attrition for both sides to be reduced to zero.",
    "10_46": "USED: Target your highest-ability character and one just-played Interrupt. Draw destiny. If destiny < ability of target character, cancel target Interrupt. LOST: Use 3 Force. Each player counts cards in hand, then places entire hand and Used Pile onto Reserve Deck; reshuffle. Each player then draws from Reserve Deck the counted number of cards to create a new hand.",
    "11_18": "Deploy on table. If Death Star “blown away”: once during each of your turns you may deploy (for free) a starship from hand or Reserve Deck and reshuffle; if you just deployed a unique (*) starship to a system location, retrieve 3 Force. (Immune to Alter.)",
    "11_25": {"gametext": [("may reveal the bottom card", "may take the bottom card")]},
    "11_88": {"gametext": [("stacked on I Feel The Conflict", "stacked on I Can Feel The Conflict")]},
    "12_79": {"gametext": [("Your AATs deploy +1 here.", "Your tanks deploy +1 here.")]},
    "12_136": "Use 3 Force to deploy on table. If you just forfeited all your cards that participated in a battle opponent initiated, you may place this Effect out of play to cancel all remaining battle damage. (Immune to Alter.)",
    "12_170": {"gametext": [("your AATs are each power +2 here", "your tanks are each power +2 here")]},
    "13_29": {"gametext": [("non-alien character here,", "non-alien character present,")]},
    "13_62": "Deploy on table. Once per turn, you may take a non-Interrupt card with “door” in title into hand from Reserve Deck; reshuffle. At Endor sites where you have a scout, Rebel scouts are power -1 and forfeit -3. (Immune to Alter.)",
    "13_74": {"gametext": [("Immune to Clash Of Sabers and attrition < 5 (or < 6 if armed with a lightsaber). May not be Disarmed.",
                            "Immune to Disarmed, Clash Of Sabers, and attrition < 5 (or < 6 if armed with a lightsaber).")]},
    # lore "to weld properly": Decipher's 497 px face (Ref3-D-maulsdoublebladedlightsaber-decipher-archive.jpg, rev 84
    # text setting 3); the PC's D-E1 re-render prints "to wield"
    "13_75": {"gametext": [("While on Maul, may not be stolen.", "May not be stolen.")],
              "lore": [("years of training to wield properly", "years of training to weld properly")]},
    "13_77": "Dark: Characters of ability < 5 'hit' here are placed (with all cards on them) in owner's Used Pile. Light: Characters of ability < 5 'hit' here are placed (with all cards on them) in owner's Used Pile.",
    "14_115": {"gametext": [("Laser Cannons aboard from Reserve Deck", "Laser Cannons here from Reserve Deck")], "armor": "2", "maneuver": None},
    "110_7": {"gametext": [("Adds 2 to the power of anything he pilots.", "Adds 2 to power of anything he pilots.")]},
    # Desperate Times: printed with the Episode I disc under its Reflections III sphere (Glossary Supplement struck it)
    "7_224": {"title": "Come Here You Big Coward!"},  # SE-D-comehereyoubigcoward: no bullet, "!" (GEMP •Come Here You Big Coward)
    # the wiki's printed page holds another printing's / the list's words (read on ANH-D-dssixtyonefour… archive faces)
    "2_88": "Adds 3 to power of any starship he pilots. On Black 4, also draws one battle destiny if not able to otherwise. May use 1 Force to search through your Reserve Deck and take one Lone Pilot into your hand. Shuffle, cut and replace.",
    "2_45": "After a battle at an interior _site_ is initiated, use 1 Force to cause all leaders and all characters with ability > 2 (on both sides) to be completely excluded from that battle.",
    # rev 84 (3): Reflections II combos whose GEMP text is not what Decipher printed and the wiki keeps no printed page
    # (Ref2-<side>-<name>-decipher-archive.gif): Sense & Recoil In Fear carries Sense & Uncertain's printed LOST text
    "10_21": "USED: Target your highest-ability character and one just-played Interrupt. Draw destiny. If destiny < ability of target character, cancel target Interrupt. LOST: Use 3 Force. Each player counts cards in hand, then places entire hand and Used Pile onto Reserve Deck; reshuffle. Each player then draws from Reserve Deck the counted number of cards to create a new hand.",
    "10_13": {"gametext": [("(Immune to Sense)", "(immune to Sense)"), ("may immediately deploy as", "may deploy as")]},
    "10_16": "USED: Use 1 Force to randomly select one card from opponent's Lost Pile and place out of play. LOST: Cancel one hologram. OR Use 4 Force. Draw destiny. Add 1 to destiny for each asteroid sector on table. If total destiny > 3, Imperial Holotable site is “blown away.”",
    "10_19": {"gametext": [("OR If opponent has no presence or Force icons,", "OR If opponent just deployed a spy to a site where opponent has no presence or Force icons,")]},
    "10_28": {"gametext": [("game text of one Rebel for remainder", "game text of one Rebel present for remainder")]},
    "10_8": {"gametext": [("battle damage. (Immune to Sense.)", "battle damage (immune to Sense).")]},
    "13_13": {"icons": ["Reflections 3", "Episode I"]},
    "112_9": {"gametext": [("Your characters here aboard vehicles are each power +1.", "Your characters aboard vehicles here are each power +1.")]},
}
# fields whose wiki "printed" text the printed face contradicts (OCR of the wiki's Decipher-archive scan, see STANDARD
# rev 84 Decipher printed text): GEMP's text is kept for these
REJECT = {}
# corrections to the wiki's printed text where the printed face differs (checked by eye)
WIKI_FIX = {
    "3_124": {"gametext": [("or Missing)", "or missing)")]},          # Exposure: lower case on the print
    "1_65": {"gametext": [("Millenium Falcon", "_Millenium Falcon_")]},  # Special Modifications: misspelt, italic
    # Decipher's double quotes where the faces show them (the GEMP convention would set them single)
    "2_66": {"gametext": [("'Nighttime conditions'", "“Nighttime conditions”"), ("'Nighttime conditions'", "“Nighttime conditions”")]},
    "2_149": {"gametext": [("'Nighttime conditions'", "“Nighttime conditions”"), ("'Nighttime conditions'", "“Nighttime conditions”")]},
    "1_212": {"gametext": [("'nighttime conditions.'", "“nighttime conditions.”"), ("'game text'", "“game text”")]},
    "1_13": {"gametext": [("On Red 6 also", "On Red 6, also")]},                 # Jek Porkins: comma on the print
    "5_45": {"lore": [("to prevent their", "to _prevent_ their")]},       # Dodge: "prevent" italic on the print
    "4_121": {"gametext": [("gains leader skill", "gains {leader} skill")]},  # Field Promotion: "leader" bold
}
# lore: the wiki's printed pages copy lore from Decipher's card lists, which differ from the print (Dark Hours prints
# "Interrogator droid", the list "Interceptor"; Imperial Blaster "power packs", the page "packagedProduct"); only lore
# the printed face confirms is taken (read on the wiki's hires / archive faces)
LORE_OK = {"1_112", "1_168", "1_309", "2_16", "2_32", "3_16", "4_15", "4_110", "5_122", "6_75",
           # rev 84 (2): read on the hires / archive faces (the wiki's lore was right)
           "1_22", "1_150", "1_155", "1_164", "1_211", "1_256", "2_25", "2_116", "2_129", "2_136", "2_161", "3_4", "4_39",
           "4_108", "5_15", "5_45", "5_65", "6_10", "6_124", "6_125", "6_173", "7_12", "13_53"}
# lore the faces contradict (GEMP kept): 1_18 LIN-V8K (the wiki has another card's lore), 1_26 "heroes", 1_149 "open-air",
# 1_173 "missions", 1_174 "Pilot DS-61-3.", 1_212 "Interrogator", 1_261 "as laborer", 1_317 "power packs"
STATS = ("destiny", "power", "ability", "deploy", "forfeit", "maneuver", "armor", "hyperspeed", "landspeed", "politics", "parsec")


def field(t, k):
    m = re.search(r"^\|%s=(.*?)(?=^\||^\}\})" % k, t, re.M | re.S)
    return m.group(1).strip() if m else None


def wiki_to_raw(v, lore=False):
    """wikitext of a card field -> GEMP's raw text conventions."""
    v = v or ""
    v = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", v)
    v = re.sub(r"</?nowiki>", "", v)
    v = re.sub(r"<br\s*/?>", "\n", v)
    v = re.sub(r"'''((?:Light|Dark) Side:|\d side\s*[—-][^']*)'''", r"\1", v)   # the wiki's half / face headings
    # bold: game text keeps it as GEMP's {word} (Field Promotion "{leader} skill", Retractable Arm "{thief}"); lore drops
    # it (GEMP's lore carries none; the renderer bolds characteristics itself)
    v = re.sub(r"'''(.+?)'''", r"\1" if lore else r"{\1}", v)
    v = re.sub(r"''([^'\n]+?)''", r"\1", v)              # italic ship names (the adapter's ship_text re-italicises)
    v = html.unescape(v)
    v = re.sub(r"[“”\"]", "'", v)                        # GEMP writes printed double quotes as single ones
    v = re.sub(r"[‘’`]", "'", v)
    v = v.replace("…", "...").replace("–", "-").replace("—", "-").replace("✻", "*").replace("✶", "*")
    v = re.sub(r"[ \t]+", " ", v)
    v = re.sub(r" *\n *", "\n", v)
    return v.strip()


def norm(v):
    """for the comparison only: what counts as the same words."""
    v = str(v or "")
    v = re.sub(r"[“”‘’`\"]", "'", v).replace("(•)", "(*)").replace("…", "...").replace("–", "-").replace("✻", "*").replace("✶", "*")
    v = re.sub(r"\{([^{}]*)\}", r"\1", v)                # GEMP's {bold} marks
    v = re.sub(r"\s*\.\s*\.\s*\.\s*", "...", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v


def halves(gt):
    """'Light: a Dark: b' (either order, wiki '''Light Side:''' paragraphs too) -> (light, dark) or None."""
    gt = gt or ""
    m = re.match(r"\s*(?:Light(?: Side)?)\s*:?\s*(.*?)\s*(?:Dark(?: Side)?)\s*:\s*(.*)$", gt, re.S)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r"\s*(?:Dark(?: Side)?)\s*:?\s*(.*?)\s*(?:Light(?: Side)?)\s*:\s*(.*)$", gt, re.S)
    if m:
        return m.group(2), m.group(1)
    return None


def empty(x):
    return re.fullmatch(r"\s*(\((?:empty|none)\)\.?|Blank\.?|-)?\s*", x or "", re.I) is not None


def location_text(w, g):
    """wiki halves in GEMP's order (the card's own side first, as GEMP lists them)."""
    hw, hg = halves(w), halves(g)
    if not hw or not hg:
        return None, None
    same = all(norm("" if empty(a) else a) == norm("" if empty(b) else b) for a, b in zip(hw, hg))
    lw, dw = ("(none)" if empty(x) else x.strip() for x in hw)
    dark_first = re.match(r"\s*Dark", g or "") is not None
    return same, (f"Dark: {dw} Light: {lw}" if dark_first else f"Light: {lw} Dark: {dw}")


def objective_text(w, g):
    """wiki "'''0 side — Front'''\\n\\ntext\\n\\n'''7 side — Back'''\\n\\ntext" -> GEMP "Front: text Back: text"."""
    parts = re.split(r"\n*\s*\d side\s*[—-]\s*([^\n]+?)\s*\n+", "\n" + w)
    if len(parts) < 5:
        return None
    return f"{parts[1].strip()}: {parts[2].strip()} {parts[3].strip()}: {parts[4].strip()}"


def uniqueness_errata(pages):
    """titles whose errata only added bullets (Decipher printed none), from Errata.wiki."""
    p = os.path.join(pages, "Errata.wiki")
    out = {}
    if not os.path.exists(p):
        return out
    t = open(p, encoding="utf-8").read()
    for row in t.split("\n|-"):
        m = re.search(r"^\|+ \[\[([^\]|]+)\]\]", row.strip(), re.M)
        if not m:
            continue
        if re.search(r"Errata face \((?:•+) (?:unique|restricted)\)", row) or re.search(r"print: (?:\(non-unique\)|no uniqueness)", row):
            out[m.group(1).strip()] = ""
    return out


def main():
    gem = {}
    for f in ("Light", "Dark"):
        for c in json.load(open(os.path.join(ROOT, "gempdata", f + ".json"), encoding="utf-8"))["cards"]:
            gem[c["gempId"]] = c
    corr = json.load(open(os.path.join(ROOT, "gempdata", "corrections.json"), encoding="utf-8"))
    for g, fix in corr.items():   # the printed-card typo fixes the server applies (webapp/server.py), so GEMP = served text
        if g not in gem:
            continue
        for k, pairs in fix.items():
            side, _, kk = k.rpartition(".")
            f = gem[g].get(side or "front") or {}
            for a, b in ([pairs] if isinstance(pairs[0], str) else pairs):
                if isinstance(f.get(kk), str):
                    f[kk] = f[kk].replace(a, b)
    printed = {}   # GEMP id -> [(rank, path, text)]
    for root, _, files in os.walk(PAGES):
        for fn in files:
            if not fn.endswith(".wiki"):
                continue
            p = os.path.join(root, fn)
            t = open(p, encoding="utf-8", errors="replace").read()
            if "{{Card" not in t:
                continue
            u = field(t, "card_uid") or ""
            if not u.endswith("o") or u[:-1] not in gem:
                continue
            lab = field(t, "version_label") or ""
            rank = 0 if lab.startswith("printed") else 1
            printed.setdefault(u[:-1], []).append((rank, root != PAGES, p, t))
    uniq = uniqueness_errata(PAGES)
    uniq.update(UNIQUENESS_SEEN)
    out = {}
    for gid in sorted(printed, key=lambda g: (g.split("_")[0].zfill(4), int(re.sub(r"\D", "", g.split("_")[1]) or 0))):
        c = gem[gid]
        if str(c.get("set")) not in DECIPHER_SETS:
            continue
        f = c["front"]
        rank, _, p, t = sorted(printed[gid], key=lambda x: (x[0], x[1], x[2]))[0]
        e = {}
        typ = f.get("type") or ""
        w_gt = wiki_to_raw(field(t, "game_text"))
        g_gt = f.get("gametext") or ""
        if typ == "Location" and halves(g_gt):
            same, txt = location_text(w_gt, g_gt)
            if same is False:
                e["gametext"] = txt
        elif typ == "Objective" and " / " in (f.get("title") or ""):
            txt = objective_text(w_gt, g_gt)
            if txt and norm(txt) != norm(g_gt):
                e["gametext"] = txt
        elif w_gt and norm(w_gt) != norm(g_gt):
            e["gametext"] = w_gt
        w_lore = wiki_to_raw(field(t, "lore"), lore=True)
        if w_lore and norm(w_lore) != norm(f.get("lore")) and not (empty(w_lore) and not f.get("lore")):
            e["lore"] = w_lore
        for k in STATS:   # the wiki leaves fields out (parsec) or fills ones a card does not print (landspeed 1 on
            w, g = (field(t, k) or "").strip(), str(f.get(k) or "").strip()   # characters, ability 0 on droids):
            if w and g and w != g:                                             # only a value both give, differing
                e[k] = w
        # title (wiki title has no bullets; uniqueness from the errata documents, see the module docstring)
        bul = re.match(r"^([•<>◊]*)", f.get("title") or "").group(1)
        name = (f.get("title") or "")[len(bul):]
        wt = re.sub(r"\s*\((?:Original|Dark|Light)\)$", "", field(t, "title") or "").strip()
        base = re.sub(r"\s*\((?:V|Dark|Light)\)$", "", name).strip()
        new_name = name
        if wt and norm(wt).lower() != norm(base).lower() and "/" not in name:
            new_name = name.replace(base, wt) if base in name else wt
        new_bul = uniq.get(base, uniq.get(wt, bul)) if (base in uniq or wt in uniq) else bul
        if new_name != name or new_bul != bul:
            e["title"] = new_bul + new_name
        for k, pairs in WIKI_FIX.get(gid, {}).items():
            for a, b in pairs:
                assert a in e.get(k, ""), (gid, a)
                e[k] = e[k].replace(a, b, 1)
        for k in (() if os.environ.get("DP_ALL") else REJECT.get(gid, ())):
            e.pop(k, None)
        if "lore" in e and gid not in LORE_OK and not os.environ.get("DP_ALL"):
            e.pop("lore")
        if e:
            e["_page"] = field(t, "title")
            e["_image"] = field(t, "image")
            e["_label"] = field(t, "version_label")
            out[gid] = e
    for gid, fix in PRINTED_SEEN.items():
        f = gem[gid]["front"]
        e = out.setdefault(gid, {})
        for k, pairs in ({"gametext": fix} if isinstance(fix, str) else fix).items():
            v = e.get(k, f.get(k))
            if isinstance(pairs, str) or pairs is None or k not in ("gametext", "lore", "title"):
                v = pairs
            else:
                for a, b in pairs:
                    assert a in v, (gid, a)
                    v = v.replace(a, b, 1)
            e[k] = v
        e["_label"] = "read off the printed face (PRINTED_SEEN)"
        e.setdefault("_page", re.sub(r"^[•<>]+", "", f.get("title") or ""))
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=False)
    print(f"{len(out)} cards with printed fields -> {OUT}")


if __name__ == "__main__":
    main()
