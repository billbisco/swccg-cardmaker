"""Turn the helpers' transcription JSON (cards/vsN/NN.json, spec in cards/VS3-SPEC.md) into render.py card dicts
and render them. Usage: python3 build_vs.py 3 [NN ...]"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
import render

ROOT = Path(__file__).resolve().parent

SET_ICON = {   # expansion name → ring icon file (None = no ring at all, as Premiere prints — checked on BoShek/Black 2 scans)
    "A New Hope": "icons/set-anh-grainy.png", "Premiere": None, "Premiere Limited": None, "Premiere Unlimited": None,
    "Jedi Pack": "icons/set-premium-grainy.png", "Hoth": "icons/set-hoth-bardez.png", "Dagobah": "icons/set-dagobah.png",
    "Special Edition": "icons/set-se-grainy.png", "Endor": "icons/set-endor-grainy.png",
    "Cloud City": "icons/set-cloudcity-grainy.png", "Jabba's Palace": "icons/set-jabbaspalace-grainy.png", "Jabba's Palace Sealed Deck": "icons/set-jabbaspalace-grainy.png", "Enhanced Jabba's Palace": "icons/set-ejp-grainy.png",
    "Reflections II": "icons/set-reflections2-grainy.png", "Coruscant": "icons/set-coruscant-grainy.png",
    "Tatooine": "icons/set-tatooine.png", "Theed Palace": "icons/set-theed.png",   # Bardez "DS - Epic Event.xcf" expansion layers
    "Enhanced Cloud City": "icons/set-premium-grainy.png", "Official Tournament Sealed Deck": "icons/set-premium-grainy.png",   # silver premium sphere
    "Death Star II": "icons/set-ds2-grainy.png", "Reflections III": "icons/set-reflections3-grainy.png",
}
TOKEN_FIX = {"{icon:immune-alter}": "{alter}", "{icon:immune-control}": "{control}", "{icon:immune-sense}": "{sense}",
             "{icon:virtual-set symbol}": "{ovs}", "{icon:republic}": "{republic-crest}", "{icon:republic-square}": "{republic-square}"}


KEYWORDS = r"bounty hunter|information broker|leader|spy|smuggler|gambler|scout|thief|gangster|assassin"


def bold_keywords(lore: str) -> str:
    """Remaster enhancement (Bill 2026-10-13): bold a character's lore characteristics everywhere, even where Decipher
    printed them plain. The wiki keeps the lore as printed; only the remaster image gets the bold."""
    parts = re.split(r"(\*[^*]+\*)", lore)   # leave already-bold runs alone
    def one(m):
        before, after = m.string[:m.start()], m.string[m.end():]
        if re.search(r"(?i)\bformer\s+$", before) or re.match(r"[’']s\b", after):
            return m.group(0)        # "Former scout", "smuggler's" — not a characteristic ("to spy on" IS bolded, Bill)
        return f"*{m.group(0)}*"
    return "".join(p if p.startswith("*") else re.sub(rf"(?i)(?<![A-Za-z])(?:{KEYWORDS})(?![A-Za-z])", one, p) for p in parts)


def template_for(c: dict) -> str:
    side = "ls" if c["side"] == "Light" else "ds"
    st = (c.get("slip_type") or "").lower()
    aff = (c.get("affiliation") or "").lower()
    if st == "objective" or c.get("game_text_back"):
        return "objective-ls" if side == "ls" else "objective"
    if "creature" in st and "vehicle" not in st:
        return "creature"
    if st == "site":
        return "loc-site"
    if st == "system":
        return "loc-system"
    if c.get("no_lore_box") and st in ("effect",) and side == "ds":
        return "ds-effect-tall"
    if st == "epic event":
        return "ls-jeditest-tall" if side == "ls" else "epic-event"
    if "admiral" in st:
        return f"{side}-admirals-order"
    if st == "character" or c.get("stats") and not c.get("card_type"):
        if side == "ls":
            if "alien" in aff and "rebel" in aff:
                return "ls-character-alien-rebel"
            if "droid" in aff:
                return "ls-character-droid"
            if "alien" in aff:
                return "ls-character-alien"
            return "ls-character-rebel"
        if "droid" in aff:
            return "ds-character-droid"
        if "alien" in aff:
            return "ds-character-alien"
        return "ds-character-imperial"
    if "weapon" in st or "device" in st:
        return f"{side}-weapon"
    if "vehicle" in st:
        return f"{side}-vehicle"
    if "starfighter" in st or "starship" in st or "capital" in st:
        return f"{side}-starship-starfighter"   # one starship icon for starfighters and capitals on the printed cards
    if "shield" in st:
        return f"{side}-shield"
    if "weapon" in st or "device" in st:
        return f"{side}-weapon"
    if "interrupt" in st:
        return f"{side}-interrupt"
    return f"{side}-effect"


def convert(c: dict, vs: int) -> dict:
    gt = c.get("game_text_lines") or c["game_text"]   # the slip's own line breaks when slip_lines.py has recorded them
    for k, v in TOKEN_FIX.items():
        gt = gt.replace(k, v)
    t = template_for(c)
    if t.endswith("-shield") and c.get("shield_style", "fade") == "fade":
        t += "-fade"      # Original Virtual era: the slips' red→cyan fade; "shield_style": "hybrid" keeps the primary frame
    art = c.get("art") or {}
    src = art.get("modern") or art.get("src")
    exp = c.get("expansion")
    card = {
        "id": f"vs{vs}-{int(c['number']):02d}", "template": t, "side": c["side"], "title": c["title"],
        "caption": c.get("caption") or f"{c['title']} (V)", "number": str(int(c["number"])), "virtual_set": vs,
        "destiny": c.get("destiny") or "", "lore": bold_keywords(c.get("lore") or "") if "character" in template_for(c) else c.get("lore") or "", "game_text": gt,
        "icons": c.get("icons") or [], "scomp": bool(c.get("scomp")),
        "copyright": c.get("copyright") or "", "expansion_icon": SET_ICON.get(exp, None) if exp else None,
        "expansion_icon_in_hole": False,
    }
    if c.get("card_type"):
        card["card_type"] = c["card_type"]
    if c.get("stats"):
        card["stats"] = [[a, b] for a, b in c["stats"]]
    if c.get("deploy") is not None:
        card["deploy"], card["forfeit"] = str(c["deploy"]), str(c.get("forfeit") or "")
    if c.get("grabber") or ("immediate" in (c.get("slip_type") or "").lower() and c.get("grabber") is not False):   # VS5 #27 prints none
        card["banner_icon"] = "grabber"
    if src:
        card["art"] = {"src": src}
    if art.get("rect"):   # the scan's own art rectangle (tall-slip cards)
        card["art"] = {"src": art["src"], "rect": art["rect"]}
    if art.get("bbox"):   # a hand-measured scan mapping belongs to the base scan (full-art Admiral's Orders)
        card["art"] = {"src": art["src"], "bbox": art["bbox"]}
    if (c.get("expansion") or "") in ("Coruscant", "Theed Palace", "Tatooine", "Reflections III"):
        card["art_trim"] = True          # Episode I frame: trim the silver edge the classic art box would include
    if "dark jedi" in (c.get("affiliation") or "").lower() and "imperial" in (c.get("affiliation") or "").lower():
        card["disc"], card["disc2"] = "dark-jedi", "ds-imperial-ring"   # Reflections II Emperor: two discs on the Imperial frame
    if "republic" in (c.get("affiliation") or "").lower():
        card["disc"] = "republic"        # Bardez "LS - Character - Rebel" Republic affiliation disc (Obi-Wan, Padmé (V))
    if "jedi" in (c.get("affiliation") or "").lower() and c["side"] == "Light":
        card["disc"] = "jedi-light"      # Yoda: Rebel frame with the Jedi Master blade disc (Bardez has no Light Jedi disc)
    for k in ("text_grow", "ring_icons", "frame_tint", "frame_style", "text_lines", "light_force_count", "dark_force_count", "invert_text", "margin_right_top", "margin_right_at", "no_lore_box", "stat_icon", "credit_bottom", "margin_left", "margin_right", "lore_align", "lore_indent", "dark_text", "light_icons", "dark_icons", "light_force", "dark_force"):
        if c.get(k) is not None and c.get(k) != "":
            card[k] = c[k]
    if t in ("loc-site", "loc-system"):
        if c.get("parsec") is not None:
            card["parsec"] = c["parsec"]
        card["light_force"] = bool(c.get("light_force")); card["dark_force"] = bool(c.get("dark_force"))
        card["dark_text"] = c.get("dark_text_lines") or c.get("dark_text") or ""
        for k, v in TOKEN_FIX.items():
            card["dark_text"] = card["dark_text"].replace(k, v)
        card["text_lines"] = bool(c.get("game_text_lines") or c.get("dark_text_lines"))   # slip line breaks: no re-wrapping
    if t.startswith("objective"):
        card["destiny"] = c.get("destiny") or "0"
        card["back"] = {"title": c.get("title_back") or "", "caption": c.get("caption_back") or f"{c.get('title_back','')} (V)",
                        "destiny": c.get("destiny_back") or "7", "game_text": (c.get("game_text_back_lines") or c.get("game_text_back") or ""),
                        "art": {"src": (c.get("art_back") or {}).get("modern") or (c.get("art_back") or {}).get("src")}}
    return card


if __name__ == "__main__":
    vs = int(sys.argv[1])
    nums = [f"{int(n):02d}" for n in sys.argv[2:]] or sorted(p.stem for p in (ROOT / f"cards/vs{vs}").glob("[0-9][0-9].json"))
    for n in nums:
        c = json.loads((ROOT / f"cards/vs{vs}/{n}.json").read_text(encoding="utf-8"))
        card = convert(c, vs)
        (ROOT / f"cards/vs{vs}/{n}.card.json").write_text(json.dumps(card, ensure_ascii=False, indent=1), encoding="utf-8")
        try:
            m, h = render.render(card)
            print(n, card["template"], "ok")
            if card.get("back"):   # Objective: second face
                b = dict(card); b.update(card["back"]); b["id"] = card["id"] + "b"; b.pop("back")
                render.render(b); print(n + "b", card["template"], "ok")
        except Exception as e:
            print(n, card["template"], "FAIL", e)
