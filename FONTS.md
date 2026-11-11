# Fonts

Every font in this repository is free software: anyone may use, copy, modify and redistribute it, alone or with this
code. Each one is built to stand in for a face of the printed Decipher cards and the Players Committee's Holotable
remakes, as identified by Bardez (`docs/bardez-card-fonts-and-dimensions.txt`) and measured on the PC's own cards.
Each font's folder holds its licence, a FONTLOG (how it was made, how close it is, where it falls short) and the
sources and script that rebuild it.

| File | Face | Used for |
|------|------|----------|
| HolotableTitle/HolotableTitle-Regular.otf | Holotable Title (our own, SIL OFL 1.1) | card titles, deploy / forfeit numbers, caption bullet |
| HolotableText/HolotableText-Light.ttf | Holotable Text Light (OFL, from Barlow Condensed) | lore |
| HolotableText/HolotableText-Regular.ttf | Holotable Text Regular (OFL, from Barlow Condensed) | game text (the PC's Holotable size: 62 px / 65 line at 600 DPI), "medium" labels |
| HolotableText/HolotableTextPC-Regular.ttf, -Bold.ttf | Holotable Text PC (OFL, from Holotable Text) | Virtual Legacy game text and lore (rev 74): the PC slips' Akzidenz-Grotesk BE Condensed advance widths and kerning |
| HolotableText/HolotableText-Bold.ttf | Holotable Text Bold (OFL, from Barlow Condensed) | stat labels, type banners, © line (landscape bottom strips) |
| HolotableNumbers/HolotableNumbers-Extended.otf | Holotable Numbers Extended (GUST Font License, from TeX Gyre Heros) | destiny, stat values, slip numbers, parsec numbers on systems |
| LiberationSansNarrow-Bold.ttf | Liberation Sans Narrow Bold (metric twin of Arial Narrow Bold) | bottom-strip caption on portrait cards (the PC slips use Arial Narrow Bold) |
| HolotableNumbers/HolotableNumbers-BoldItalic.otf | Holotable Numbers Bold Italic (GUST Font License, from TeX Gyre Heros) | bottom-strip card number (the PC's PDF sets it in Akzidenz-Grotesk BE Bold Italic) |

Until rev 62-66 (3 November 2026) the repository carried commercial fonts from Bardez's community template pack
(Fiorello CG Condensed, five Akzidenz-Grotesk files, Craft Gothic Heavy Extended) and a digit subset of Akzidenz-Grotesk
BE Bold Italic from the PC's PDF. All have been replaced and removed (swccg-guild/work#118, #123, #124, #125); they remain
in the git history only. Craft Gothic had not been used since the VS13 location work moved the parsec number to the
stat-value face.

Liberation Sans Narrow (Liberation Fonts 1.07.4, from Debian's `fonts-liberation` package) is free software under the
GNU GPL v2 with the font exception; its licence is in `assets/fonts/LiberationSansNarrow-LICENSE.txt`. The PC printed
the slip captions in Arial Narrow Bold (a Monotype font). Liberation has identical advance widths, and at the slip
geometry (STANDARD rev 53) its ink lands within 1 px of the PDF's.

**Holotable Title** (rev 62, swccg-guild/work#118) replaces Fiorello CG Condensed, the commercial face of the
title before. It is traced from the PC's own card titles (the PC set them in AT/PL Fiorello Condensed), shares no
file or name with any commercial font, and is free software under the SIL Open Font License 1.1: its licence,
FONTLOG and the sources and script that rebuild it are in `assets/fonts/HolotableTitle/`. It matches the PC's
title widths within 1 px (Fiorello CG: 2 px). Fiorello CG is no longer in the repository.

**Holotable Text** (rev 64, swccg-guild/work#123) replaces Akzidenz-Grotesk BQ Light Condensed, BQ Condensed and BQ Bold
Condensed (and Bardez's BE Medium Condensed). It is Barlow Condensed (SIL OFL 1.1, The Barlow Project Authors), narrowed
and rescaled so CardMaker's sizes, baselines and line breaks carry over; licence, FONTLOG and the script that rebuilds it
are in `assets/fonts/HolotableText/`. On 24 PC reference cards it breaks lines where Akzidenz-Grotesk did.

**Holotable Text PC** (rev 74) is Holotable Text Regular / Bold with each glyph's advance width set to the
advance width of the face the PC set its 2009-2014 Virtual Legacy slips in (Akzidenz-Grotesk BE Condensed / Bold
Condensed) and the PC's kerning pairs, both read as numbers from the PDFs' font dictionaries and text positions
(`source/pc_widths.json`, built by `source/build_pc.py`). No outline, file or name of the commercial face is used, as
Liberation Sans carries Arial's metrics. Outlines are Holotable Text's, scaled horizontally per glyph (0.85-1.20).

**Holotable Numbers** (rev 65 / 67, swccg-guild/work#124) replaces Akzidenz-Grotesk Medium Extended and the PC's Akzidenz-Grotesk
BE Bold Italic digits. It is TeX Gyre Heros Bold / Bold Italic (GUST Font License, a free licence: LPPL 1.3c) widened and
rescaled to the digit height, baseline and spacing the templates assume.
Licence, FONTLOG and the script that rebuilds it are in `assets/fonts/HolotableNumbers/`.

The wiki page *Typography of Star Wars CCG cards* (wiki.swccg.com) documents what is known about the faces Decipher
and the PC used, measured sizes, and how this program maps to them.
