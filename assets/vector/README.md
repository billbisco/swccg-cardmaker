# Set symbol and icon assets

## ovs-set-symbol-upscaled.png — Original Virtual Set symbol (STANDARD, Bill 2026-10-11)
The Players Committee's Dec 2006 Remaster slip sheets (VirtualCards1.pdf … VirtualCards17.pdf, archived from
swccgpc.com/Resources/) print a gold banded sphere with a silver rim in the lower icon slot of every slip. The
PDFs embed it as a 39×39 px raster (extract with `pdfimages -png`). Decision: use that original as it is,
upscaled with plain Lanczos (×8, then scaled to the slot) and given a round alpha mask — grain and all. No
sharpening, no redraw, no recolor (both were tried and rejected: `ovs-set-symbol.svg`, `ovs-set-symbol-flat*.png`
are kept only as a record).

Placement on the Dark Character frame: 76×76 px at (slot-3 x + 6, slot-3 y + 78), i.e. the bottom of the
game-text box in the right icon column, matching the slip.

To do for other sets: extract each sheet's 39×39 icon and confirm it is the same symbol before reusing this file.
