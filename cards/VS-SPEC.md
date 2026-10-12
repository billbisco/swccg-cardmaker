# VSN (Original) data run — transcription spec for helpers

Goal: one JSON per slip, `cards/vsN/NN.json` (NN = 01..50), plus the base-card scan(s) in `src/vsN/`.
Work from the slip crops in `src/slips/vsN/NN-Title.png` (300 DPI crops of the PC's Dec 2006 Remaster sheet) —
NOT from wiki transcriptions (those dropped the inline icons). View each crop with the Read tool.

Read `STANDARD.md` first (what a slip changes, what stays from the printed card).

## Fields

```json
{
  "id": "vsN-18-red-5",
  "number": "18",
  "virtual_set": 3,
  "side": "Light",                       // Light slips are 01–25, Dark 26–50
  "slip_type": "Starfighter",            // banner on the slip if any (EFFECT, LOST INTERRUPT, CHARACTER WEAPON, DEFENSIVE SHIELD, IMMEDIATE EFFECT, STARFIGHTER: X-WING, AUTOMATED WEAPON...) else the card type (Character)
  "card_type": "STARFIGHTER: X-WING",    // the banner text exactly as printed on the slip, "" if no banner (characters)
  "title": "•Red 5",                     // base card title WITH its uniqueness dots (•, ••, •••, or none), WITHOUT " (V)"
  "caption": "•Red 5 (V)",               // exactly as the slip's bottom-left strip prints it
  "stats": [["POWER","3"],["MANEUVER","4"],["HYPERSPEED","5"]],   // from the slip's stat boxes, in order; [] if none.
                                         // Characters: [["POWER","6"],["ABILITY","2"]] + a third box when printed:
                                         // ["FORCE-ATTUNED",""] / ["FORCE-SENSITIVE",""] / ["ASTROMECH DROID",""] / ["INTERROGATOR DROID",""] (label only, value "")
  "deploy": "3", "forfeit": "6",         // the two small boxes left of the game text (deploy above forfeit); null if the slip has none
  "game_text": "May add Luke as pilot and {set:anh} R2-D2 (may ▼ here.) During battle, …",
  "icons": ["pilot", "warrior"],         // the icon column right of the game text, top to bottom, NOT counting the gold/blue
                                         // virtual-set symbol at the bottom. Names: pilot, warrior, nav, scomp(not here — see below),
                                         // presence, permanent-weapon, astromech, independent, republic, episode1, or describe:"…"
  "scomp": false,                        // true if a scomp-link ring is printed at the top-left of the text box (starships/vehicles/sites)
  "affiliation": "Rebel",                // characters only: Rebel / Alien / Imperial / Droid / "Alien + Rebel" (from the printed base card's
                                         // frame & icons — check the base scan; multi-affiliation cards have two discs top-left)
  "lore": "Luke's Incom T-65 X-wing …",  // the PRINTED base card's lore (from the wiki base page `|lore=`), with _italics_ where printed
  "destiny": "2",                        // the printed base card's destiny (wiki base page `|destiny=`)
  "expansion": "A New Hope",             // the printed base card's set (wiki base page `|set=`)
  "copyright": "TM & © 1996 LUCASFILM LTD. TM, ® & © 1996 DECIPHER INC.",   // read the year off the base scan's vertical line
  "base_page": "Red 5",                  // wiki page title of the printed card you used
  "art": {"src": "src/vsN/ANH-L-red5.gif", "modern": "src/vsN/modern/V9-L-red5.gif"},   // files you downloaded (modern = null if none)
  "notes": "anything odd: text you could not read, icons you could not name, a slip that differs from the wiki stub"
}
```

## Game-text markup
- Keep the slip's wording and punctuation exactly (curly quotes ’ “ ”, en-dashes, "<" etc.). Line breaks: none (one paragraph) unless the
  slip prints USED:/LOST: lines — then `\n` between them.
- Inline icons as tokens: `{pilot:2}` = the yellow pilot-power icon followed by a number ("2." on Chewbacca); `{alter}` `{control}` `{sense}`
  = the circled A / C / S; `{maintenance}`, `{grabber}`; `{lightsaber}`; `{warrior}`; `{pilot}` (plain pilot icon, no number);
  `{set:anh}` `{set:premiere}` `{set:hoth}` … = an expansion symbol used inline (the Red 5 one is A New Hope's Death Star);
  `{nav}`, `{astromech}`, `{permanent-weapon}`, `{presence}`, `{dark-force}`, `{light-force}`. Anything else: `{icon:your description}`.
- ▲ and ▼ are typed as those characters. `*bold*` for bold, `_italic_` for italics (ship names like _Falcon_).
- Uniqueness dots in text stay as • (e.g. "a non-• Leia", "•••Rodian").

## Base card
Wiki API: `https://wiki.swccg.com/api.php?action=parse&page=<Title>&prop=wikitext&format=json` → `{{Card …}}` fields.
The base page is the slip's title without " (V)" (and without the dots); if several printings exist use the one the stub links
("Decipher base:" line on the `<Title> (V) (Virtual Set N)` page). Download the base image via
`action=query&titles=File:<image>&prop=imageinfo&iiprop=url` to `src/vsN/`. Also check whether a modern PC remake exists
(`<Title> (V) (Virtual Set N)` page whose `|set=` is "Virtual Set N" with no "(Original)", image `V<N>-…gif`): download it to
`src/vsN/modern/` — its art is usually better than the 350 px scan. Never invent a value: if the wiki lacks it, write null and say so in notes.

Write each JSON with ensure_ascii=False, indent 1. Don't touch render.py or other helpers' files. Report: list of NNs done + notes.

## Additions (from the VS1 run, 2026-10-12)
- Replace N with the set number you were given. Slip crops: `src/slips/vsN/NN-Title.png`. Base scans go to `src/vsN/NN-<file>`, modern/Block images to `src/vsN/modern/NN-<file>`.
- Prefer a 745 px scan. The wiki often has both `X-decipher-archive.gif` (350) and `X.gif` (745): query
  `api.php?action=query&list=allimages&aiprop=size&ailimit=200&aifrom=<Set>-<L|D>-<first letters>` and take the widest
  file whose name matches the card. Modern remakes: `V0-…`, `VB1-…-pre.gif` (Virtual Block = the same slip reissued in 2009), `V<N>-…`.
- Lore: copy it from the wiki base page, then READ the lore box on the scan and correct the wiki text where it differs
  (the wiki has typos: "Servant of Emperor's", "packagedProduct"). Curly quotes ’ “ ” as printed. Note every correction in `notes`.
- Stats: a third character box prints a label only (FORCE-SENSITIVE, DARK JEDI, FORCE-ATTUNED …) → `["DARK JEDI",""]`; "NO HYPERSPEED" likewise.
- Set page titles are now `Virtual Set N: <Subtitle>`; the stub page is `<Title> (V) (Virtual Set N: Subtitle)`.
- Icons in the column: name them (pilot, warrior, nav, astromech, permanent-weapon, independent, episode1, republic …);
  an orange/gold virtual-set sphere at the bottom of the column is NOT an icon. A ring at the top-left of the text box = scomp true.
- Copyright year = the base card's set: Premiere 1995, A New Hope 1996, Hoth 1996, Dagobah 1997, Cloud City 1997, Jabba's Palace 1998, Special Edition 1998, Endor 1999, Death Star II 2000, Reflections II 2001, Tatooine/Coruscant/Theed 2001 — but read it off the scan's vertical line when legible.

## Additions (VS4 run)
- Slip crops are named by the slip's printed number: `NN-Title.png`; an **Objective** has two slips, front `NN-` and
  back `NNb-`. Transcribe an Objective as ONE json `NN.json` with: `title` = front title, `title_back` = back title (as
  the back slip's heading prints it, e.g. "Liberation"), `game_text` = front text, `game_text_back` = back text, `slip_type`
  "Objective", `card_type` "". The bold lead words (**For**, **While**, **Flip**, **Place**) are `*bold*`; the italic
  first lines are `_italic_`. Keep the slips' line structure as sentences (one paragraph each).
- A **site** slip (landscape, e.g. Hoth: Echo Med Lab) has a Light text (left/top) and may have a Dark text; use the
  fields of `cards/hoth-echo-med-lab-v-vs4.json` as the model (add them to the normal json): `game_text` = Light side
  text, `dark_text` = Dark side text ("" if the slip has none — the printed card's Dark text then stays), `light_force` /
  `dark_force` = whether the slip shows a Force icon on that side, `light_icons` / `dark_icons` = the icon boxes on each
  side as printed (outermost first, e.g. ["scomp", "planet", "interior", "underground"]), `slip_type` "Site",
  `card_type` = the banner text (•HOTH: ECHO MED LAB). `stats` []; no deploy/forfeit. The base card's lore field
  does not exist for sites — set lore "".
- An **Admiral's Order** / **Epic Event** / **Defensive Shield** / **Immediate Effect** / **Vehicle Weapon** /
  **Automated Weapon**: `slip_type` = the banner as printed, `card_type` = the banner text.
- Character third box may read ASTROMECH DROID, MEDICAL DROID, FORCE-SENSITIVE … → `["MEDICAL DROID",""]`.
- Hoth base cards: expansion "Hoth", copyright 1996; Dagobah 1997; Special Edition 1998; Premiere 1995; A New Hope 1996.
