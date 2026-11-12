# Virtual Legacy typesetting (rev 74)

Bill 2026-11-10: CardMaker's Virtual Legacy recreations must put the same words on the same lines as the Players
Committee's card, and every icon where the PC's card has it. These scripts read the PC's own vector text out of the
Virtual Legacy master list PDFs and build `gempdata/legacy_typeset.json`; `check_typeset.py` is the regression check.

Sources (wiki.swccg.com): `Virtual_Legacy_Final_Master_LS.pdf`, `Virtual_Legacy_Final_Master_DS.pdf` (2014; 1,050
cards, 337 of them as full cards). The PC set game text and lore in Akzidenz-Grotesk BE Condensed (bold words in
BE Bold Condensed): game text 7.14-7.4 pt on a 7.42-7.5 pt pitch, tracking -5..+10 / 1000 em, chosen per card; lore
6.2-6.4 pt. A 745 px Holotable card is 178.8 pt wide (300 dpi); master px = pt x 8.3333 + 70 (x) / + 136 (y) (the
PDF's full-card image sits 32 px (745) lower in the Holotable crop).

Build (run from a work folder holding `pdf/` with both PDFs, and the cardmaker checkout as `swccg-cardmaker/`):

    python3 tools/legacy/typeset/pdf_extract.py pdf/Virtual_Legacy_Final_Master_LS.pdf pdf/Virtual_Legacy_Final_Master_DS.pdf   # -> pdf_cards.json (move into pdf/)
    (fonts' /Widths: assets/fonts/HolotableText/source/pc_widths.json, see build_pc.py)
    python3 tools/legacy/typeset/legacy_index.py      # legacy card -> template, text
    python3 tools/legacy/typeset/pdf_lines.py && python3 tools/legacy/typeset/match.py   # lines per card, matched to legacy ids
    python3 tools/legacy/typeset/typeset_table.py     # per-card frame, size, tracking, pitch, line breaks
    python3 tools/legacy/typeset/kp_test.py && python3 tools/legacy/typeset/greedy_iv.py   # frame widths that reproduce the breaks
    python3 tools/legacy/typeset/typeset_final.py     # -> gempdata/legacy_typeset.json

Icon positions: `render_full.py` renders the master list's full cards; `piece_scale.py` template-matches each piece of
our render (expansion sphere, icon column, set mark, destiny, deploy / forfeit) into them and prints the median offset
and scale per template; `render.PC_PIECE_FIX` holds the result.

Check: `PLAYWRIGHT_BROWSERS_PATH=... python3 tools/legacy/typeset/check_typeset.py --json out.json` (with
`CM_PC_HINTS=0` the stored PC line breaks are off, so it measures the rules a new version text gets).
