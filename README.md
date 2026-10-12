# swccg-cardmaker

An open-source card maker for the **Star Wars Customizable Card Game**. Today it produces full-card remasters of the
Players Committee's **Original Virtual Sets** (2002–2008, 686 slips in 17 sets): the printed Decipher card's top half
plus the PC's slip, re-typeset at 600 DPI in the look of the PC's Holotable cards, output as print masters
(1632×2220) and rounded-corner GEMP/Holotable images (745×1039). The longer plan: a web card maker for fan-made
and translated cards that produces GEMP-ready images.

Review of the first set: [Original Virtual Set 3 remaster review](https://wiki.swccg.com/wiki/Original_Virtual_Set_3_remaster_review).

## Credits

- **Decipher Inc.** designed the Star Wars CCG and its card frames (1995–2001). **Lucasfilm Ltd.** owns Star Wars.
- The **Star Wars CCG Players Committee** created the virtual card sets (2002–), the December 2006 *Remaster*
  slip sheets this project works from, the Holotable card images whose typography is the standard here, and the
  Game Aid icon sheet.
- **Bardez** (u/Bardez) drew the 600 DPI GIMP card templates (2021) that every frame here is cut from, and
  identified the fonts and sizes. Free community work; please credit him when you use the frames.
- The PC's Virtual Set 3 graphic design team (Michael Erisman, Dennis Hes, Jerry Jensen, Henk Maul, John Millet) and
  proofing team, and the card concept authors credited on individual slips (e.g. Eric Hunter, Wokling (V)).
- The **SWCCG Wiki** (wiki.swccg.com) preserves the scans, slips, sheets and templates this project reads.
- Built by Bill Bisco with AI Assistance. Not endorsed by anyone else.

## Layout

- `render.py` — card JSON + template → HTML/CSS → Chromium screenshot → PNG master and Holotable image.
- `build_vs.py N` — turns helper transcriptions `cards/vsN/NN.json` (spec: `cards/VS3-SPEC.md`) into render cards.
- `STANDARD.md` — **the locked standard** (every design ruling, rev 1–5) and the QA procedure. Read it first.
- `assets/frames` — flattened frames cut from Bardez's XCFs; `assets/icons` — set symbols cut from scans, inline
  icons from the slips and cover keys, Game Aid icons; `assets/loc` — location parts; `assets/fonts` — see FONTS.md.
- `docs/` — Bardez's original font/dimension notes.

Not in the repo: Bardez's XCFs (wiki: *Making Custom SWCCG Cards*), card scans and slip sheets (wiki), renders.

## Run

```
pip install pillow numpy scipy playwright gimpformats && playwright install chromium
python3 build_vs.py 3          # all of VS3 → out/vs3-NN_1632.png + out/vs3-NN_745.png
python3 render.py cards/tarkin-v-vs3.json
```

## Licence

MIT for the code and docs (see LICENSE). Card art, text and designs belong to Lucasfilm and Decipher; frames derive
from Bardez's free templates
