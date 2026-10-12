# Original Virtual card remaster standard (locked 2026-10-11, Bill)

Reference card: **Tarkin (V), Virtual Set 3 #47** (`cards/tarkin-v-vs3.json` → `out/tarkin-v-vs3_*.png`).

## What a slip changes and what it does not
A V-slip replaces the **bottom half** of the printed Decipher card only. The top half stays exactly as printed:
- title **without** "(V)" (e.g. "•Tarkin"), destiny, lore, art, the expansion-set icon in the ring beside the lore box
  (Premium for Jedi Pack Tarkin; Premiere prints no ring at all — verified on the BoShek and Black 2 scans, VS1 run), the vertical "TM & © <year> LUCASFILM LTD. TM, ® & © <year>
  DECIPHER INC." line on the right margin of the art (year = the base card's set).
- The slip supplies: stats row, game text (with the PC shorthand icons and ▲/▼ triangles kept), deploy/forfeit,
  the icon column, the Original Virtual set symbol at the bottom of the icon column, and the bottom strip:
  "•Title (V)" bottom-left and the slip number bottom-right in the black border.

## Sources
- Frames, fonts, layout: Bardez's 600 DPI GIMP templates (wiki: Making Custom SWCCG Cards). Card area 1343×1931 at
  (144,144) on a 1632×2220 black bleed. Fonts from his pack (Fiorello CG Condensed; Akzidenz-Grotesk BQ Light/Medium/
  Bold Condensed, Medium Extended) — commercial fonts; fine for our renders, a licensing question for a public tool.
- Text: the slip image on the wiki (VSnO-NN-Title.png) and the PC's Dec 2006 Remaster sheets (VirtualCardsN.pdf,
  Wayback of swccgpc.com/Resources/). Wiki `{{Card}}` transcriptions dropped inline icons — re-transcribe from slips.
- Art: cropped automatically from the Decipher scan; when the PC's modern remake of the same card has better art,
  backport that (Tarkin). Wiki scan sizes: 350×490 (most), 745×1039, 1495×2032.
- Set symbol: the PDF's own 39×39 icon, Lanczos-upscaled with a round mask, as is. (Redraws rejected.)
- Game Aid Feb 2024 PDF (wiki) = clean copies of all 76 PC icons at template size.

## Type sizes (match the PC's Holotable cards; shrink only when a text won't fit)
Title Fiorello 80 · destiny Akzidenz Medium Extended 80 · lore Light Condensed 58 (first line indented 60) ·
stat labels Bold Condensed 56 + value Medium Extended bold 60 right after the label (gap 26) · **game text Akzidenz-Grotesk BQ Condensed (regular weight) 62 / line 65** — the face and size of the PC's Holotable cards, verified against the modern Chewbacca (V) at equal scale (Bardez's spec named BE Medium Condensed, which is narrower and heavier than what the PC prints) · deploy & forfeit Fiorello 70 centered in their boxes · card-type banner Bold Condensed
60, letter-spacing 11 · bottom strip Bold Condensed 48 (number skewed −14°) · copyright line Bold Condensed 24.

## Geometry, Dark Character frame (1632×2220 space)
title (374,200,884×90) · destiny hole (1312,213,100×84) · lore (321,377,989×193) · art (256,666,1121×770) ·
stat boxes y 1506: x 305/613/924, w 251/256/396 · game text (341,1663,971×333) · deploy (204,1816,47×88) ·
forfeit (204,1926,47×85) · icon slots (1352,1643/1749/1855) · set symbol 76×76 at (1358,1933) · expansion ring
icon 77×75 at (1371,396) · copyright column x 1404 · bottom strip y 2082: caption x 160, number right edge 1402.

## Outputs
- Master 1632×2220 PNG (print master; square with bleed is the print convention) — plus rounded-corner version.
- Holotable/GEMP 745×1039: whole master at ½ scale cropped to (35,36)–(780,1075) so the card area sits at (37,36)
  like the PC's images and the bottom strip stays in the border; rounded corners r=34, transparent outside.
- Publish as WebP q85 (≈75 KB at 745, ≈180 KB at 1632); keep PNG masters.

## Expansion-set icon (locked 2026-10-11, after the ANH tries)
Cut the icon from a 745 px Decipher scan of a card of that set (centre found from its dark ring, ~29 px),
Lanczos-upscale to the ring size with a round mask at its own dark edge, and place it in the frame's ring with
nothing drawn under or around it — grain and all, exactly like the Original Virtual set symbols. Rejected:
Bardez's layer icons, the PC Game Aid icons (silver rim reads as "a circle in a circle"), any added black disc.
ANH = `icons/set-anh-grainy.png` (from ANH-D-astromechshortage.gif). Do the same per set as it first comes up.

## Locations (locked 2026-10-11: Hoth: Echo Med Lab (V) VS4 #10, Corellia (V) VS16 #27)
- A location slip replaces one side's **whole half** (force slot, title bar, icon boxes, game text, margins),
  not the bottom half. Data is per side: `light_icons` / `dark_icons` (outermost first, e.g.
  `["scomp","planet","interior","underground"]`), `light_force` / `dark_force`, `game_text` (slip side),
  `dark_text` (printed side), `parsec` for systems. The printed side is re-typeset from the scan.
- Site (landscape, master 2220×1632, Holotable 1039×745): Bardez "Location - Site" frame at (74,76).
  Icon boxes are cut from the printed Hoth card (brighter than Bardez's), 100×94 with their bevel, sitting in
  the title bar (frame y 1148), packed from the outside in: right-most centre frame x 1855, pitch 111; scomp ring
  (cut from the same card, 104 px) at frame (1790,1143). Dark half = the same mirrored and rotated 180°.
  Light title centred in the grey bar between force slot and first box, Fiorello 80; Dark title white on black.
  Text boxes: Light grey (250,1341,1719×120), Dark black (250,195,1719×99), centred, AGCn 62. Set symbol 76 px
  centred in the right margin on the text-box centre line; caption/number in the bottom border at y 1494.
- System (portrait): Bardez "Location - System" bar assembly at (235,189) over the full-card scan (prefer the
  PC's 745 scan with explicit `art.bbox` [37,37,708,1002]). The scan's own bars and the slip-side margins (its
  TM lines go with the slip) are hidden under starfield cloned from the same card. Parsec Craft Gothic Heavy
  Extended 65 white in the black box. Set symbol 72 px at (1410,1923): clear of the text-box bevel and the border.
- Almost no locations exist before VS12 (VS4 Med Lab is the only one in VS1–11); VS16/17 sheets also contain
  full new cards with lore (Bravo Fighter, BoShek's Freighter, Jedi Council Chamber) → full-card path later.
- Corner rounding is part of every render (master r=80, Holotable r=34, transparent outside) — nothing to do at
  the end; the square print master is kept too.

## Additions from the VS3 run (2026-10-11)
- Immune to Alter/Control/Sense icons are **drawn** (red circle + slash + letter, transparent), never a pasted raster:
  `{alter}` `{control}` `{sense}` in game text. The slips' other inline icons are cut from the 300 DPI sheet crops
  with their own square (permanent weapon / lightsaber, Republic wheel, nav computer) — `icons/inline-*.png`.
- Set icons cut so far (ANH method): A New Hope (from the PC's Corellia, on black), Special Edition (SE Dagobah
  system, on black), Endor (Wokling V0, red frame). Premiere = no ring icon. Jedi Pack = Premium.
- Slip credit lines in the side margins (Wokling (V)) stay: `margin_left` / `margin_right`, italic AGCn 40,
  reading bottom-to-top beside banner + text box. Bill: "annoying but part of the card's design".
- A slip whose heading differs from the printed card (sheet "Advanced Preparation" vs printed "Advance
  Preparation"): title = printed card, caption = as the slip prints it.
- Droids: one wide stat box (ASTROMECH DROID / INTERROGATOR DROID) spans the ability + third slots; LS droid stat
  boxes are black with white text. Two-value destiny ("2 or 5") stacks small in the destiny hole.
- Immediate Effects carry the grabber icon box at the right end of the banner.
- QA: every card's game text is checked as 4-grams against the Remaster sheet's text layer (pdftotext, reading
  order) — only the icon letters (A/C/S) and column interleaving show up as false positives.
- Pipeline: `cards/VS3-SPEC.md` (helper transcription spec) → `cards/vsN/NN.json` → `build_vs.py N` → `out/vsN-NN_745.png`
  → WebP → VPS importImages + review page "Original Virtual Set N remaster review".
- Rev 3 corrections (proofread of all 50 against printed card + slip): lore is **left-aligned with a 60 px first-line
  indent** (Decipher's setting on every card checked; Chewbacca ANH has no indent → `lore_indent: 0`), column
  narrowed (padding 110 right) so wraps follow the printed card; uniqueness dots in game text and captions are
  Fiorello's round • (Akzidenz's is square); slip numbers are zero-padded ("01") in bold extended italic; the drawn
  immune icon's letter takes the ink colour (was invisible on Dark boxes); Dark Interrupt type icon is masked to its
  ring; Defensive Shields keep the printed Effect top half with the shield bottom (hybrid frames, as the slips'
  blended top edge shows); the Immediate Effect grabber is Bardez's upright fist; LS droid wide stat box is silver;
  scans cut short on one edge are anchored on the edge that is inside the image.
- Rev 4 (Bill's review of rev 3): **every expansion-set icon is cut from a 745 px scan where the sphere sits on
  black** and centred by eye on the sphere, not by threshold (Premium now from the PC's Tarkin V4; the old Bardez
  `premium.png` was blurred and off-centre). Set symbol on Effect/Interrupt/Weapon/Shield frames sits **inside the
  coloured margin**, clear of both the text-box bevel and the card edge: Light frames margin x 1389–1465 → icon 60 px
  at (1397,1942); Dark frames 1361–1485 → 64 px at (1391,1940); characters unchanged. Multi-value destiny ("2 or 5")
  gets a black pill widened 150 px to the left, values at 60 px, "or" at 40 — the template must support it for every
  R2-D2. The gold spoked wheel inline icon is the **maintenance** icon per the VS3 cover ICON KEY (`{maintenance}`;
  the wiki stubs' "[Republic]" reading was wrong) — cut from the cover key's 27 px image, not from a slip. LS Rebel
  expansion ring is at (1381,405) like the other Bardez frames. Game text letter-spacing 0 so a trailing immune icon
  stays on the slip's line. Margin credits span banner top → text-box bottom.
- Before each batch goes up: three-way QA sheets (printed | slip | remaster) proofread by fresh reviewers with the
  checklist (title/dots, destiny, lore wording+breaks+alignment, ring icon, art crop, TM line, banner, stats, text +
  inline icons, D/F, icon column, scomp, set symbol clear of edges, caption/number, margins), then zoom crops of
  every ring icon and margin icon.
- Rev 5: Dark character deploy/forfeit boxes are measured from the frame image, not from Bardez's text-layer
  offsets (which sit 16 px low): DS Alien/Droid deploy (205,1824,45×83) forfeit (205,1930,47×85); Imperial
  (205,1821) / (205,1927). **Every box coordinate in a new template must be measured from the frame PNG
  (white/black component bbox), never copied from a text layer or a sibling template.** Multi-value destiny: values
  at the full 80 px, "or" at 46, in a black pill with a 6 px silver outline that replaces the ring.

- Rev 6 (2026-10-12, Bill on BoShek (V)): the ▲/▼ triangles sat too low and too small. Now 0.88em DejaVu Sans, raised 0.14em so the base sits on the baseline and the apex reaches cap height, as the slips print them. Re-rendered every VS1/VS3 card that uses them (23 files).
- Rev 7 (VS2 run, 2026-10-12): vehicle templates (`ls-vehicle`/`ds-vehicle` = the starship frames with the vehicle type
  icon cut from the PC's 745 px Blizzard 2 scan); capital ships use the starship frame — the printed cards use one
  starship icon for starfighters and capitals (checked on Black 2 / Blockade Support Ship). `permanent-pilot` column
  icon = the Pilot helmet icon, as printed. `{ovs}` = the slip's own set sphere printed inline ("the (V) version");
  `_italic_` works in titles, banners and captions (_Imperial_-Class Star Destroyer). Slip crops: heading + whole slip
  incl. the caption strip (per-box height). Wiki hubs keep the old page's history sections under "== History ==".
- Rev 8 (Bill 2026-10-12): game text breaks lines exactly where the slip does. `slip_lines.py N` reads the Remaster
  PDF's text layer (pdftotext -bbox-layout, lines grouped by slip box) and stores `game_text_lines` in each card JSON;
  the renderer uses those breaks (white-space:pre) and only shrinks the font if a line would not fit ("Trash Compactor,"
  stays on one line). Icons: the black square with a green lightsaber in game text is the Permanent Weapon icon, not
  Warrior (K'lor'slug, Han Seeker). Defensive Shields are unique even when the printed Effect is not (I Find Your Lack
  Of Faith Disturbing); Local Trouble is not unique. Expanded prose capitalises a sentence that starts with ▲/▼ ("Take…").
- Rev 8a (Bill 2026-10-12, Han's Dice): `_italic_`/`*bold*` spans may cross the slip's line breaks — the markup regex
  runs with re.S, otherwise the underscores print. Apply scripts: never `set -e` around `importImages --overwrite` —
  it exits non-zero when a file is unchanged and the page edits after it were silently skipped; check the log for
  the DONE line of every step. Every wiki change must be verified live after the batch (view the stub, not just the log).
- Rev 8b (Bill 2026-10-12): slip crops are made by `crop_slips.py N` (heading + slip only: columns outside the slip's
  own span and the previous slip's caption bar are whited out; stale crop files from earlier runs must be deleted —
  a `NN-*` glob otherwise picks the old one). `slip_lines.py` merges text runs split by an inline icon so a line like
  "opponent's [icon] weapon destiny" stays one line.
- Rev 9 (VS4 run, 2026-10-12): slips are keyed by their printed number (`sheet.py`; an Objective's back = `NNb`,
  site slips are wide and short). New frames from Bardez's wiki-preserved XCFs (wiki.swccg.com/preserved/bardez/):
  Objective (purple; the printed and PC Objectives have a white text box with black text — filled in; Light Side
  frame = the same frame lightened 32% to its lavender), Creature (two stat boxes FEROCITY / second trait), proper
  Vehicle frames (replacing the starship-frame hack). Objectives render two faces (`NN`, `NNb`), the stub shows both
  remasters (image/image2 responsive) and both slips in a gallery. Sites keep the printed Dark text (`dark_text`).
  Inline icons added: independent (g051), presence (g010); maintenance ★/☠ glyphs as text. Template order: weapon
  before vehicle ("VEHICLE WEAPON" is a weapon). Special Edition copyright line reads "© LUCASFILM LTD. & TM. TM, ® &
  © 1998 DECIPHER INC." (checked on scans) — not the Hoth-style line.
- Rev 9a (Bill 2026-10-12): slip crops keep the slip's full black outline (trim by the detected box, not by
  brightness). Dark Side cards print the DS (TIE pilot) icon for {pilot:N}, Light Side the Rebel one. The maintenance
  ★ / ☠ in game text are Decipher's own glyphs — cut from the sheet at 1200 DPI (`glyph-star.png`, `glyph-skull.png`),
  black on Light, white on Dark; a font glyph is not acceptable. Light Side Objectives use Bardez's "LS - Epic
  Objective" frame (blue-purple with Light scoring, textured white text box), not a lightened Dark frame.
