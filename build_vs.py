"""Turn the helpers' transcription JSON (cards/vsN/NN.json, spec in cards/VS3-SPEC.md) into render.py card dicts
and render them. Usage: python3 build_vs.py 3 [NN ...]"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
import render

ROOT = Path(__file__).resolve().parent

SET_ICON = {   # expansion name → ring icon file (None = empty ring, as Premiere prints)
    "A New Hope": "icons/set-anh-grainy.png", "Premiere": None, "Premiere Limited": None, "Premiere Unlimited": None,
    "Jedi Pack": "icons/set-premium-grainy.png", "Hoth": "icons/set-hoth-bardez.png", "Dagobah": "icons/set-dagobah.png",
    "Special Edition": "icons/set-se-grainy.png", "Endor": "icons/set-endor-grainy.png",
}
TOKEN_FIX = {"{icon:immune-alter}": "{alter}", "{icon:immune-control}": "{control}", "{icon:immune-sense}": "{sense}"}


def template_for(c: dict) -> str:
    side = "ls" if c["side"] == "Light" else "ds"
    st = (c.get("slip_type") or "").lower()
    aff = (c.get("affiliation") or "").lower()
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
    if "starfighter" in st or "starship" in st:
        return "ls-starship-starfighter"
    if "shield" in st:
        return f"{side}-shield"
    if "weapon" in st or "device" in st:
        return f"{side}-weapon"
    if "interrupt" in st:
        return f"{side}-interrupt"
    return f"{side}-effect"


def convert(c: dict, vs: int) -> dict:
    gt = c["game_text"]
    for k, v in TOKEN_FIX.items():
        gt = gt.replace(k, v)
    t = template_for(c)
    art = c.get("art") or {}
    src = art.get("modern") or art.get("src")
    exp = c.get("expansion")
    card = {
        "id": f"vs{vs}-{int(c['number']):02d}", "template": t, "side": c["side"], "title": c["title"],
        "caption": c.get("caption") or f"{c['title']} (V)", "number": str(int(c["number"])), "virtual_set": vs,
        "destiny": c.get("destiny") or "", "lore": c.get("lore") or "", "game_text": gt,
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
    if "immediate" in (c.get("slip_type") or "").lower():
        card["banner_icon"] = "grabber"
    if src:
        card["art"] = {"src": src}
    for k in ("margin_left", "margin_right", "lore_align", "lore_indent"):
        if c.get(k):
            card[k] = c[k]
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
        except Exception as e:
            print(n, card["template"], "FAIL", e)
