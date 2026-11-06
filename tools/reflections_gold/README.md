# Reflections Gold (set 15) tools — swccg-guild/work#174

Run from the folder that holds the work tree `rg-work/` (the scripts use that relative path).

| Step | Script | What |
|---|---|---|
| 1 | (download) | `rg-work/scans/remaster/15_N.png` = wiki `File:RG-GEMP-*.png`; `rg-work/scans/original/15_N.jpg` = `File:RG-C1-*.jpg`; `rg-work/rg_cards.json` pairs them |
| 2 | `rg_art.py measure remaster` | frame families, art window by variance (OpenCV ECC affine) |
| 3 | `rg_crop.py` | crops + manifest (`lib/remaster/`); wide cards cut at the rg template art box, frame bands inpainted |
| 4 | `rg_orig.py` | original playtest photos straightened onto the Remastered render (ECC homography), same windows |
| 5 | `rg_up.py lib/remaster` | RealESRGAN x4plus (ONNX) copies, optional (CardMaker's default is `orig/`) |
| 6 | `rg_data.py gempdata/ReflectionsGold.json` | CardMaker card data for 15_N (Remastered) and 15_No (original) from the wiki pages |
| 7 | `rg_check.py OUTDIR` | render all 620 in a running CardMaker, compare with the sources, metrics + sheets |

The art is published in [billbisco/swccg-card-art](https://github.com/billbisco/swccg-card-art) `reflections-gold/`.
