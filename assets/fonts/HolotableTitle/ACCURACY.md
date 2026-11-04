# Holotable Title: how close it is to the PC's titles

Measured 2026-11-03 (swccg-cardmaker rev 62) with `compare_pc.py`. Each card is rebuilt in CardMaker and compared
with the Players Committee's own 745 × 1039 image of the same card. The title is compared in two ways:
- **Position and size:** dx, dy, dw and dh, in 745-px pixels (+ = right, down, wider, taller).
- **Pixel difference (MAD):** the mean absolute difference inside the title box, after aligning, on a 0–255 scale.

Holotable Title is compared with **Fiorello CG Condensed**, the commercial copy of the PC's face that CardMaker used before. The PC itself set its titles in AT (PL) Fiorello Condensed; its slip PDFs embed `ATFiorello-Condensed`.

## Summary

| | Fiorello CG | Holotable Title |
|---|---|---|
| Title width vs the PC, 180 PC titles at each title's own size (`source/check_width.py`), median \|difference\| | 2.70 px (median +2.04, wider) | 1.11 px (median −0.87) |
| 24 reference cards in CardMaker, median \|dw\| | 2.0 px | 1.0 px |
| 12 interrupt references (templates fitted to the PC): largest \|dx\|, \|dw\| | 2 px | 1 px |
| Pixel difference, sum over the 12 interrupts | 136.0 | 132.7 |
| Pixel difference, median over the 6 Dark (white) interrupt titles | 12.1 | 9.3 |
| Stem thickness, Light (black) interrupt titles (PC 4.70 px) | 4.40 px | 4.78 px |
| Stem thickness, Dark (white) interrupt titles (PC 4.94 px) | 5.54 px | 4.91 px |
| Cards where the pixel difference is higher than Fiorello CG's | — | 10 of 24 |

## Where it falls short

- **Long Light titles.** On black-on-silver titles, Fiorello CG puts every letter within 0–1 px of the PC's. That is expected, because it is a digital copy of the PC's own typeface. Holotable Title gets each title's total width and height right, but individual letters drift by up to 1–2 px in the middle of the title. Its edges are also a little softer, because each letter is an average of many printed copies. The pixel difference on the longest Light titles is up to 4.4 levels higher than Fiorello CG's (for example "The Destiny Of A Jedi", 10.8 → 15.2).
- **Resolution.** The PC's images are 745 px wide, so a title capital is about 32 px tall. No larger source of these titles exists. Averaging up to 1,166 copies of a letter recovers detail finer than one pixel, but not every fine corner.
- **Characters the PC never printed in a title** were constructed from traced parts or drawn from the measured stroke weight: `: ; ' ‘ “ ” – / # ◊` and the accented letters. The curly quotes are built from the PC's apostrophe, a slanted tick, so they are not comma-shaped.
- A final per-letter fit against 340 PC titles, scored on 60 held-out titles, improved the match by only 0.2 %. The spacing is at the limit these images support.

## Per-card figures

| Card (gempId) | Fiorello CG dx / dy / dw / dh · MAD | Holotable Title dx / dy / dw / dh · MAD |
|---|---|---|
| •A New Hope (227_4) | 0 / 0 / 0 / 0 · 8.74 | 0 / 0 / 0 / 0 · 9.27 |
| •Endless Legions (226_3) | 0 / 0 / 0 / 0 · 7.96 | 0 / 0 / 0 / −1 · 6.43 |
| •Honoring What They Fight For (225_46) | 0 / 0 / 0 / 0 · 13.87 | −1 / 0 / −1 / 0 · 17.08 |
| •Welcome Home, Lord Tyranus (226_13) | −1 / 0 / −2 / 0 · 15.04 | 0 / 0 / +1 / −1 · 9.96 |
| •My Sister Has It (225_9) | 0 / 0 / 0 / 0 · 9.91 | 0 / 0 / 0 / 0 · 10.24 |
| Ommni Box & It's Worse (226_9) | 0 / 0 / −2 / −10 · 15.02 | 0 / 0 / −1 / −10 · 12.89 |
| •Podrace Prep (227_1) | 0 / 0 / 0 / −2 · 8.97 | 0 / 0 / 0 / −2 · 8.71 |
| •Slip Sliding Away (212_4) | 0 / 0 / 0 / 0 · 8.45 | 0 / 0 / −1 / −1 · 8.22 |
| •Something About This Boy (226_27) | 0 / 0 / 0 / 0 · 13.17 | 0 / 0 / 0 / 0 · 15.39 |
| •No Civility, Only Politics (225_25) | 0 / 0 / 0 / 0 · 9.71 | 0 / 0 / 0 / −1 · 8.56 |
| The Destiny Of A Jedi (217_49) | 0 / 0 / 0 / −2 · 10.79 | +1 / 0 / +1 / −2 · 15.15 |
| •You Know What I've Come For (208_46) | −1 / 0 / −2 / −1 · 14.39 | −1 / 0 / −1 / −1 · 10.81 |

These are the 12 interrupt references (one Light and one Dark per interrupt subtype), whose templates are fitted to the PC. The dh of −10 on Ommni Box & It's Worse is that combo card's own layout, and the −2 on two cards is the same with both fonts. Twelve more cards of other types were measured too. Their title boxes are not fitted yet, so their dx and dy reflect the box rather than the font. There, Holotable Title's pixel difference is higher than Fiorello CG's on five cards (up to +2.7) and lower on the rest.
