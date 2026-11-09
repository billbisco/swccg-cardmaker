# How to recreate a published card version

The card maker can rebuild any printed Star Wars CCG card — Decipher (1995–2001), Reflections Gold, the Players
Committee's Original Virtual Sets (2002–2008), the Virtual Legacy blocks (2009–2014, "Virtual Block 1–9" and the
Virtual Block shields) and the modern Virtual Sets 0–27 — and then show it with any published text. Everything but
what you change stays as printed: frame, art, title, lore, icons, set mark, slip number, copyright line and the
Players Committee's labels (original-title strip, errata mark, AI stamp, "Original concept by …").

Editor: <https://swccg.com/cardmaker/> · API: `https://swccg.com/cardmaker/api` (no key needed).

## In the browser

1. **Find the card.** Type part of its title in *Start from an existing card*, or use **Browse** (set → side → type).
   Each printing is its own entry: the Decipher card, the Original Virtual Set card (`11NN_…`, "Virtual Set N
   (Original)") and the Virtual Legacy card (`10NN_L…`, "Virtual Block N"). Pick the printing you want to recreate.
   You can also open a card by its GEMP id in the address bar: `https://swccg.com/cardmaker/#card=1210_124`
   (Virtual Legacy cards also open by their 22xx version-card id or `pc-legacy:<PC id>`).
2. **Pick the version (Virtual Legacy).** Under the search box, *Published version* lists every recorded text of the
   card in order (Original, then PC-E1, PC-E2 … as the wiki and GEMP number them, card-list rewordings included), with
   its date and the GEMP card that carries it (the current 12xx card for the latest; 22xx version cards such as
   `2261_10` for an original and `2261_1010` for a middle version). Choosing one puts that text on the card. Texts that
   differ only in capitals or punctuation are not listed (Bill has not ruled on them); the note under the picker names them. A version marked "icons to add" was read from the printed sheet without
   its inline icons: put them back in the game text (see the token table under the form).
3. **Change what differs.** Game text, title, lore, destiny, stats, card number, errata mark and copyright line are all
   form fields. Icons are typed as codes (`{alter}`, `{set:hoth}`, `▼`, `{pilot:2}`, `*bold*`, `_italic_`), never as words.
4. **Check against the printed card** (the PC image or the release-sheet slip): everything except the text you changed
   should match. Lore and game text are re-typeset, so line breaks may differ; words may not.
5. **Download** the PNG (745 × 1039, the Holotable / GEMP size, or print size) and **Export JSON** to keep the exact
   recipe.

## For scripts and AIs (API)

```
GET  /api/search?q=faithful service              -> the printings and their ids
GET  /api/card/1001_L5521                        -> editable spec + "versions" (Virtual Legacy) + art source
GET  /api/card/1210_124?version=PC-E1            -> the same card with that version's text (id, code, "original" or GEMP id)
GET  /api/card/2261_1010                         -> a 22xx version card opens with its own version's text
POST /api/render {"spec": {...}, "size": "holotable", "format": "png"}   -> the image
```

Change any field of `spec` before rendering (`game_text`, `title`, `lore`, `destiny`, `stats`, `number`,
`labels` …). A `warning` in the card response means the version text lost its icons: fix `game_text` first.
Opened by the GEMP id alone (no `?version`), such a version keeps the card's own text and says so in `note`; its
recorded stats still apply. A version can change only stats (`stats`, e.g. Jedi Survivor (V) PC-E1: destiny 1 → 3);
the API puts them on the card (rev 73).
`version_notes` lists held texts (capitals / punctuation only, waiting on Bill): shown, not selectable. In version
texts the record's `[S]` / `[T]` are the slips' ▲ / ▼ (take into hand / deploy from Reserve Deck); Immune to Sense is
always written out there.
The helper `legacy_version_image.py` in billbisco/ai-team-skills (`shared/swccg-cardmaker/`) does the whole round trip
and checks the art against the printed card:

```
python3 legacy_version_image.py --card 1210_124 --version PC-E1 --out VB1-123-Faithful_Service-PC-E1-cardmaker.png
```

## Where the pieces come from (Virtual Legacy)

- **Art:** the Decipher card the slip was printed on, from the art library (`gempdata/legacy_art.json`, found by
  template-matching every library crop into the PC's card image). Cards with new art (AI printings, Clone Wars cards)
  use their own PC image, mapped by the frame.
- **Copyright line:** that Decipher card's line (its year), or the PC's "Artwork not affiliated…" disclaimer where the
  card prints it.
- **Slip number, original-title strip, errata mark, credits:** `gempdata/card_labels.json` (read off the PC images).
- **Versions:** `gempdata/legacy_versions.json`, built from the version record (legacy-versions-v4.json) and the
  22xx version classes in billbisco/swccg-gemp by `tools/legacy/build_versions.py` (rerun it when either changes).

Rules behind all of this: `STANDARD.md` (rev 71-72 for Virtual Legacy).
