# Holotable Numbers: sources

    pip install fonttools potracer opencv-python-headless numpy
    python3 build.py ..      # writes ../HolotableNumbers-Extended.otf and ../HolotableNumbers-BoldItalic.otf

| File | What it is |
|---|---|
| `texgyreheros-bold.otf`, `texgyreheros-bolditalic.otf`, `GUST-FONT-LICENSE.txt`, `README-TeX-Gyre-Heros.txt` | TeX Gyre Heros, unmodified (GUST Font License) |
| `targets.json` | per style: flat-top digit height and line metrics per em, and the fitted width / spacing parameters |
| `build.py` | builds both styles |
