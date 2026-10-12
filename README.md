# cardmaker — Original Virtual Set full-card remasters

Claude's renderer for the Original Virtual Sets (VS1–17). Read `STANDARD.md` first: it is the locked standard
(Bill's rulings, rev 1–5) and the QA procedure. `cards/VS3-SPEC.md` is the helper transcription spec; `cards/vs3/`
the VS3 transcriptions (`NN.json`) and the derived render cards (`NN.card.json`).

Not in the repo (fetch per STANDARD.md § Sources): Bardez's fonts (`assets/fonts/`, commercial — his pack on the
wiki's Making Custom SWCCG Cards page), the Bardez XCFs (`bardez/`), scans and slips (`src/`), renders (`out/`).
Frames here are the flattened PNGs cut from the XCFs. Run: `python3 build_vs.py 3` (needs Playwright Chromium,
Pillow, numpy, scipy, gimpformats for new frames).
