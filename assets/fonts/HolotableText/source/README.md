# Holotable Text: sources

    pip install fonttools
    python3 build.py ..        # writes ../HolotableText-Light.ttf, -Regular.ttf, -Bold.ttf (byte-identical rebuild)

| File | What it is |
|---|---|
| `BarlowCondensed-Light.ttf`, `-Medium.ttf`, `-SemiBold.ttf` | Barlow Condensed (SIL OFL 1.1, The Barlow Project Authors), the base of Light, Regular and Bold; licence in `Barlow-OFL.txt` |
| `targets.json` | per style: the cap height and line metrics per em that CardMaker's sizes and baselines assume |
| `classes.json` | per style: width factors for capitals, lowercase, digits, punctuation and the word space |
| `build.py` | narrows, rescales and renames each style |

See `../FONTLOG.txt` for the method and `../OFL.txt` for the licence.
