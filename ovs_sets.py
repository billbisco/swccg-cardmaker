"""Set keys for the Original Virtual pipeline (crop_slips, sheet, slip_lines, build_vs, make_upload).

A set is either a number (Virtual Set 1–17, folder vsN) or a short key for a sheet that is not a numbered set:
  DS = Virtual Set: Defensive Shields (4 December 2006 sheet, 18 slips, GEMP 1100) — folder vsDS.
Everything keyed by the set uses f"vs{key}" for folders and ids, so a key is used exactly like a number."""
from __future__ import annotations

SPECIAL = {
    "DS": dict(name="Virtual Set: Defensive Shields", pdf="DefensiveShields.pdf", gemp="1100",
               slip_prefix="PS1", remaster_prefix="PS1", official_text="4 December 2006",
               sheet_url="https://web.archive.org/web/20071028141121/http://www.swccgpc.com/Resources/DefensiveShields.pdf",
               # slip number → file-name title, as the wiki's PS1-NN-<Title>.png slip files name them
               titles={1: "A_Tragedy_Has_Occurred", 2: "Aim_High", 3: "Battle_Plan", 4: "Do_Or_Do_Not", 5: "Dont_Do_That_Again",
                       6: "Ounee_Ta", 7: "Wise_Advice", 8: "Your_Insight_Serves_You_Well", 9: "Allegations_Of_Corruption",
                       10: "Battle_Order", 11: "Come_Here_You_Big_Coward", 12: "Do_They_Have_A_Code_Clearance", 13: "Fanfare",
                       14: "No_Escape", 15: "Oppressive_Enforcement", 16: "Secret_Plans", 17: "There_Is_No_Try",
                       18: "You_Cannot_Hide_Forever"}),
}


def parse(arg) -> int | str:
    """'6' → 6, 'ds'/'DS' → 'DS'."""
    s = str(arg).strip()
    if s.isdigit():
        return int(s)
    k = s.upper()
    if k not in SPECIAL:
        raise SystemExit(f"unknown set {arg!r}: use 1–17 or one of {sorted(SPECIAL)}")
    return k


def is_special(vs) -> bool:
    return isinstance(vs, str)


def set_name(vs) -> str:
    return SPECIAL[vs]["name"] if is_special(vs) else f"Virtual Set {vs}"
