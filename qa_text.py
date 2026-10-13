"""Compare each card's game_text (and title/caption) with the Remaster sheet's own text layer inside its slip box.
    python3 qa_text.py 5          → per card: words of the JSON missing from the sheet, and sheet words missing from the JSON
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from collections import Counter
from sheet import slip_boxes, pdf_words
from slip_lines import norm, visible

ROOT = Path(__file__).resolve().parent
vs = int(sys.argv[1])
keyed = slip_boxes(vs); words = pdf_words(vs)
bad = 0
for n in sorted(k for k in keyed if k[2:] == ""):
    c = json.loads((ROOT / f"cards/vs{vs}/{n}.json").read_text(encoding="utf-8"))
    pg, bx, by, bw, bh = keyed[n]; bx, by, bw, bh = [v * 72 / 300 for v in (bx, by, bw, bh)]
    sheet = [norm(t) for p, x0, y0, x1, y1, t in words if p == pg and bx - 2 <= x0 <= bx + bw and by - 2 <= y0 <= by + bh]
    sheet = Counter(w for w in sheet if w)
    mine = Counter()
    text = c["game_text"] + ("\n" + c.get("game_text_back", "") if c.get("game_text_back") else "") + " " + c.get("caption", "")
    for u in text.split():
        v = visible(u)
        if v: mine[v] += 1
    # the layer splits italic ship names etc.; try joining neighbours
    miss = [w for w in (mine - sheet).elements()]
    extra = [w for w in (sheet - mine).elements() if not re.fullmatch(r"\d{1,2}|[a-z]|[a-z]{2,}:", w) and w not in ("•",)]
    joined = "".join(sheet.elements())
    miss = [w for w in miss if w not in joined]      # a split word is still a hit if the sheet has its pieces
    if miss or extra:
        bad += 1
        print(n, c["title"][:30], "| JSON-only:", miss, "| sheet-only:", extra)
print("cards with differences:", bad)
