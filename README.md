# swccg-cardmaker

An open-source card maker for the **Star Wars Customizable Card Game**. Today it produces full-card remasters of the
Players Committee's **Original Virtual Sets** (2002–2008, 686 slips in 17 sets): the printed Decipher card's top half
plus the PC's slip, re-typeset at 600 DPI in the look of the PC's Holotable cards, output as print masters
(1632×2220) and rounded-corner GEMP/Holotable images (745×1039). The longer plan: a web card maker for fan-made
and translated cards that produces GEMP-ready images.

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
- `compare_pc.py` — rebuilds a PC Virtual card in CardMaker and measures it against the PC's own image (Epic
  swccg-guild/work#48, see "Compare with a PC card" below).
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

## Recreate a published card version

Any printed card (Decipher, Reflections Gold, Original Virtual Sets, Virtual Legacy blocks, Virtual Sets 0–27) opens in
the browser editor (<https://swccg.com/cardmaker/>) or the API; Virtual Legacy cards also open by GEMP id and list every
published game-text version. Step by step for people and scripts: [docs/RECREATE-A-CARD.md](docs/RECREATE-A-CARD.md).

## Compare with a PC card

`compare_pc.py` builds a PC Virtual card through the CardMaker API (`/api/card`, `/api/render`) and compares it with the
PC's 745×1039 image, element by element (boxes from the render's `X-Piece-Boxes`).

```
python3 compare_pc.py "A New Hope"                 # title or gempId (227_4); API: --api or $CARDMAKER_API
python3 compare_pc.py --batch cards.txt --sheet    # one card per line + contact sheet
python3 compare_pc.py X --build b.png --boxes b.json --ref pc.png   # offline: compare two images
```

On the VPS (no numpy on the host), run it in the CardMaker image:
`docker run --rm --user 0 --network host -v $PWD:/w -v /opt/swccg-holotable:/opt/swccg-holotable:ro -w /w
--entrypoint python3 swccg-cardmaker:latest compare_pc.py "A New Hope"`.

Each card gets `out/compare/<gempId>/`: `pc.png`, `build.png`, `overlay.png` (50 %), `diff.png` (×4), `side.png`,
`report.json` and `report.md`. The table gives, per element, dx/dy (build relative to PC, best integer alignment within
±10 px, flagged at the limit), dw/dh (ink-box size), MAD, changed % (>40 levels at zero offset) and ΔE (CIE76). There is
no tolerance: anything not exactly 0 is `DIFF` and must be fixed, logged as an approved deviation or explained (#48 Q2).

## Licence

MIT for the code and docs (see LICENSE). Card art, text and designs belong to Lucasfilm and Decipher; frames derive
from Bardez's free templates
