# Fonts

The renderer uses the typefaces of the printed Decipher cards and the Players Committee's Holotable remakes, as
identified and bundled by Bardez with his templates (`docs/bardez-card-fonts-and-dimensions.txt`):

| File | Face | Used for |
|------|------|----------|
| HolotableTitle/HolotableTitle-Regular.otf | Holotable Title (our own, SIL OFL 1.1) | card titles, deploy / forfeit numbers, caption bullet |
| HolotableText/HolotableText-Light.ttf | Holotable Text Light (OFL, from Barlow Condensed) | lore |
| HolotableText/HolotableText-Regular.ttf | Holotable Text Regular (OFL, from Barlow Condensed) | game text (the PC's Holotable size: 62 px / 65 line at 600 DPI), "medium" labels |
| HolotableText/HolotableText-Bold.ttf | Holotable Text Bold (OFL, from Barlow Condensed) | stat labels, type banners, © line (landscape bottom strips) |
| HolotableNumbers/HolotableNumbers-Extended.otf | Holotable Numbers Extended (GUST Font License, from TeX Gyre Heros; PC-traced digits) | destiny, stat values, slip numbers |
| CraftGothic-HeavyExtended.otf | Craft Gothic Heavy Extended | parsec numbers on systems |
| LiberationSansNarrow-Bold.ttf | Liberation Sans Narrow Bold (metric twin of Arial Narrow Bold) | bottom-strip caption on portrait cards (the PC slips use Arial Narrow Bold) |
| HolotableNumbers/HolotableNumbers-BoldItalic.otf | Holotable Numbers Bold Italic (GUST Font License, from TeX Gyre Heros) | bottom-strip card number (the PC's PDF sets it in Akzidenz-Grotesk BE Bold Italic) |

Craft Gothic is redistributed here as it came in Bardez's community template pack, for this free, non-commercial fan
project. It is a commercial design (being replaced: swccg-guild/work#125): they are not open-source fonts, and nothing in this repository's MIT licence applies to them. If you
redistribute or build a commercial product on this code, replace them (the renderer only needs the
`@font-face` names in `render.py`).

Liberation Sans Narrow (Liberation Fonts 1.07.4, from Debian's `fonts-liberation` package) is free software under the
GNU GPL v2 with the font exception; its licence is in `assets/fonts/LiberationSansNarrow-LICENSE.txt`. The PC printed
the slip captions in Arial Narrow Bold (a Monotype font). Liberation has identical advance widths, and at the slip
geometry (STANDARD rev 53) its ink lands within 1 px of the PDF's. The digits file is a subset of the Berthold face
that the PC's PDF embeds; it covers only what card numbers need.

**Holotable Title** (rev 62, swccg-guild/work#118) replaces Fiorello CG Condensed, the commercial face of the
title before. It is traced from the PC's own card titles (the PC set them in AT/PL Fiorello Condensed), shares no
file or name with any commercial font, and is free software under the SIL Open Font License 1.1: its licence,
FONTLOG and the sources and script that rebuild it are in `assets/fonts/HolotableTitle/`. It matches the PC's
title widths within 1 px (Fiorello CG: 2 px). Fiorello CG is no longer in the repository.

**Holotable Text** (rev 64, swccg-guild/work#123) replaces Akzidenz-Grotesk BQ Light Condensed, BQ Condensed and BQ Bold
Condensed (and Bardez's BE Medium Condensed). It is Barlow Condensed (SIL OFL 1.1, The Barlow Project Authors), narrowed
and rescaled so CardMaker's sizes, baselines and line breaks carry over; licence, FONTLOG and the script that rebuilds it
are in `assets/fonts/HolotableText/`. On 24 PC reference cards it breaks lines where Akzidenz-Grotesk did.

**Holotable Numbers** (rev 65, swccg-guild/work#124) replaces Akzidenz-Grotesk Medium Extended and the PC's Akzidenz-Grotesk
BE Bold Italic digits. It is TeX Gyre Heros Bold / Bold Italic (GUST Font License, a free licence: LPPL 1.3c) widened and
rescaled, with the Extended digits 0-7 and 9 redrawn from the PC's own destiny numbers (averaged from its card images).
Licence, FONTLOG and the script that rebuilds it are in `assets/fonts/HolotableNumbers/`.

The wiki page *Typography of Star Wars CCG cards* (wiki.swccg.com) documents what is known about the faces Decipher
and the PC used, measured sizes, and how this program maps to them.
