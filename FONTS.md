# Fonts

The renderer uses the typefaces of the printed Decipher cards and the Players Committee's Holotable remakes, as
identified and bundled by Bardez with his templates (`docs/bardez-card-fonts-and-dimensions.txt`):

| File | Face | Used for |
|------|------|----------|
| HolotableTitle/HolotableTitle-Regular.otf | Holotable Title (our own, SIL OFL 1.1) | card titles, deploy / forfeit numbers, caption bullet |
| Akzidenz-Grotesk BQ Light Conde.otf | Akzidenz-Grotesk BQ Light Condensed | lore |
| Akzidenz-Grotesk BQ Condensed.otf | Akzidenz-Grotesk BQ Condensed (regular) | game text (the PC's Holotable size: 62 px / 65 line at 600 DPI) |
| Akzidenz-Grotesk BQ Condensed A.otf | Akzidenz-Grotesk BQ Bold Condensed | stat labels, type banners, © line (landscape bottom strips) |
| AkzidenzGroteskBE-MdCn.otf | Akzidenz-Grotesk BE Medium Condensed | Bardez's game-text face (kept for reference; not the PC's) |
| AkzidenzGrotesk-MediumExtended.otf | Akzidenz-Grotesk Medium Extended | destiny, stat values, slip numbers |
| CraftGothic-HeavyExtended.otf | Craft Gothic Heavy Extended | parsec numbers on systems |
| LiberationSansNarrow-Bold.ttf | Liberation Sans Narrow Bold (metric twin of Arial Narrow Bold) | bottom-strip caption on portrait cards (the PC slips use Arial Narrow Bold) |
| AkzidenzGroteskBE-BoldIt-PCdigits.otf | Akzidenz-Grotesk BE Bold Italic, digits 0–9 and space only | bottom-strip card number (taken from the font subset embedded in the PC's DefensiveShields.pdf) |

These files are redistributed here as they came in Bardez's community template pack, for this free,
non-commercial fan project. Akzidenz-Grotesk is a Berthold typeface and Craft Gothic is a commercial
design too: they are not open-source fonts, and nothing in this repository's MIT licence applies to them. If you
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

The wiki page *Typography of Star Wars CCG cards* (wiki.swccg.com) documents what is known about the faces Decipher
and the PC used, measured sizes, and how this program maps to them.
