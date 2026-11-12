# Japanese printings — checks (STANDARD rev 77, 80)

`compare_ja.py` renders each spec in `samples/` (`language: "ja"`) and sets it beside the wiki's Japanese scan, warped
into the 1632×2220 master by the frame edges: `<name>-sheet.png` (scan | render), `<name>-top.png` / `-bottom.png`
(lore, stat strip and game text, scan above render).

Samples: Darth Vader (Dark imperial character, Premiere), Luke Skywalker (Light rebel character, Premiere; its Japanese
text was read off the scan, the wiki page has none yet), Admiral Ozzel (two stats, Hoth © 1998). Result 12 Nov 2026:
same line breaks as printed in lore and game text, strip / boxes / title within a few px; art differs (Takara's crop
shows ~4 % more picture).

Rev 80 (Effects, Interrupts, Devices; titles on every type): `make_sample.py "<Card> (Japanese)"` builds a sample from
the wiki page (English card's frame and stats, Japanese title / text / lore, the printed face as `_scan`); add the
printed line breaks (`lore_lines`, `text_breaks`) read off the scan. `compare_ja.py --full` also writes the warped scan
and the render at full size (`-scanw.png`, `-ours.png`) for measuring. Samples: astromech_shortage, affect_mind
(Effects), charming_to_the_last, emergency_deployment, we_re_doomed, warrior_s_courage, blue_milk (Interrupts),
electrobinoculars, droid_detector (Devices), help_me_obi_wan_kenobi (Takara's Effect-frame misprint). Result: same
printed lines in lore and game text; text edges within ~3 px of the scans; titles within ~5 px.

Comparison sheets (scan | CardMaker, half size): `sheets/<sample>.jpg`.
