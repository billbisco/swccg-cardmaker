# Holotable Title: sources

Rebuild the font from what is here (no download needed):

    pip install fonttools potracer opencv-python-headless numpy pillow
    python3 build.py ../HolotableTitle-Regular.otf

Re-derive the glyph images from the PC's card images (downloads ~1,200 title strips into `crops/`):

    python3 fetch.py && python3 extract.py && python3 build.py ../HolotableTitle-Regular.otf
    python3 check_width.py ../HolotableTitle-Regular.otf 0.752     # width check against the PC titles

| File | What it is |
|---|---|
| `cards.json` | the PC Virtual cards used (gempId, side, type, title, hires URL) |
| `glyphs/<hex>.png`, `glyphs/meta.json` | averaged glyph images: white ink, 8 px per card px, cap top row 220, baseline row 476 |
| `pairs.json` | measured ink-to-ink gaps per letter pair (`prev|space|next`, in cap heights) |
| `scale.json` | cap height of the canonical images in card px |
| `spacing.json` | written by build.py: fitted side bearings, word space and kerning |

See `../FONTLOG.txt` for the method and `../OFL.txt` for the licence.
