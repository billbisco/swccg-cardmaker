# Fonts

The renderer uses the typefaces of the printed Decipher cards and the Players Committee's Holotable remakes, as
identified and bundled by Bardez with his templates (`docs/bardez-card-fonts-and-dimensions.txt`):

| File | Face | Used for |
|------|------|----------|
| Fiorello CG Condensed Regular.otf | Fiorello CG Condensed | card titles, deploy / forfeit numbers |
| Akzidenz-Grotesk BQ Light Conde.otf | Akzidenz-Grotesk BQ Light Condensed | lore |
| Akzidenz-Grotesk BQ Condensed.otf | Akzidenz-Grotesk BQ Condensed (regular) | game text (the PC's Holotable size: 62 px / 65 line at 600 DPI) |
| Akzidenz-Grotesk BQ Condensed A.otf | Akzidenz-Grotesk BQ Bold Condensed | stat labels, type banners, bottom-strip captions, © line |
| AkzidenzGroteskBE-MdCn.otf | Akzidenz-Grotesk BE Medium Condensed | Bardez's game-text face (kept for reference; not the PC's) |
| AkzidenzGrotesk-MediumExtended.otf | Akzidenz-Grotesk Medium Extended | destiny, stat values, slip numbers |
| CraftGothic-HeavyExtended.otf | Craft Gothic Heavy Extended | parsec numbers on systems |

These files are redistributed here as they came in Bardez's community template pack, for this free,
non-commercial fan project. Akzidenz-Grotesk is a Berthold typeface and Fiorello / Craft Gothic are commercial
designs too: they are not open-source fonts, and nothing in this repository's MIT licence applies to them. If you
redistribute or build a commercial product on this code, replace them (the renderer only needs the seven
`@font-face` names in `render.py`).

The wiki page *Typography of Star Wars CCG cards* (wiki.swccg.com) documents what is known about the faces Decipher
and the PC used, measured sizes, and how this program maps to them.
