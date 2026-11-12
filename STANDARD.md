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

## Remaster corrections
Published texts stay exactly as printed on the wiki and in GEMP. Corrections for a remaster (typos, unclear wording,
attributes to bold, icon/notation slips, image quality, inconsistent titles) are collected on the wiki's
[Remaster changes list](https://wiki.swccg.com/wiki/Remaster_changes_list) (swccg-guild/work#234). Read it before
building a remaster and apply the listed correction for the card; add any new finding there.

## Sources
- Frames, fonts, layout: Bardez's 600 DPI GIMP templates (wiki: Making Custom SWCCG Cards). Card area 1343×1931 at
  (144,144) on a 1632×2220 black bleed. Fonts from his pack (Fiorello CG Condensed, replaced in rev 62 by our own OFL Holotable Title; Akzidenz-Grotesk BQ Light/Medium/
  Bold Condensed, Medium Extended) — commercial fonts; fine for our renders, a licensing question for a public tool.
- Text: the slip image on the wiki (VSnO-NN-Title.png) and the PC's Dec 2006 Remaster sheets (VirtualCardsN.pdf,
  Wayback of swccgpc.com/Resources/). Wiki `{{Card}}` transcriptions dropped inline icons — re-transcribe from slips.
- Art: cropped automatically from the Decipher scan; when the PC's modern remake of the same card has better art,
  backport that (Tarkin). Wiki scan sizes: 350×490 (most), 745×1039, 1495×2032.
- Set symbol: the PDF's own 39×39 icon, Lanczos-upscaled with a round mask, as is. (Redraws rejected.)
- Game Aid Feb 2024 PDF (wiki) = clean copies of all 76 PC icons at template size.

## Type sizes (match the PC's Holotable cards; shrink only when a text won't fit)
Title Holotable Title 81.4 (rev 62: Fiorello CG's 80 × 1.017, the scale fitted on the PC interrupts; same cap height per px as CG) · destiny Akzidenz Medium Extended 80 · lore Light Condensed 58 (first line indented 60) ·
stat labels Bold Condensed 56 + value Medium Extended bold 60 right after the label (gap 26) · **game text Akzidenz-Grotesk BQ Condensed (regular weight) 62 / line 65** — the face and size of the PC's Holotable cards, verified against the modern Chewbacca (V) at equal scale (Bardez's spec named BE Medium Condensed, which is narrower and heavier than what the PC prints) · deploy & forfeit Fiorello 70 centered in their boxes · card-type banner Bold Condensed
60, letter-spacing 11 · bottom strip in the PC slip's faces and geometry: caption Arial Narrow Bold (Liberation Sans Narrow Bold) 61.7 px condensed to 90.6 %, bullet Holotable Title 61.9 px, number Akzidenz-Grotesk BE Bold Italic 58 px, one baseline 52 px under the frame (rev 53) · copyright line Bold Condensed 24.

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
  Light title centred in the grey bar between force slot and first box, Holotable Title 81.4; Dark title white on black.
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
- Rev 9b (Bill 2026-10-12): column icons are the PC's own Game Aid icons with their thin silver frame (g005 LS pilot,
  g068 DS pilot, g029 warrior), drawn at box size — the Bardez icon box + separate icon read fatter and heavier at
  the bottom. The inline DS pilot-power icon is g068 whole (the sheet's own inline icon is a 20 px raster, no better
  source). LS Objective frame = Bardez's LS Epic Objective re-hued to the Dark Objective's purple (hue 0.733): the
  Objective colour never changes between sides, only the scoring does. Maintenance ★ gets 6 px of air before "Lose"
  as on the slip. Base-page lore typos are fixed without asking (Bill).
- Rev 9c (Bill 2026-10-12): Dark Objectives have a BLACK text box with white text (printed SE cards and the PC's
  Virtual Block versions alike); only Light Objectives have the white box. No fill is drawn on the Dark frame.
- Rev 9d (Bill 2026-10-12): Objective frame purple measured on the printed SE scans and the PC's Virtual Block cards
  (HSV ≈ 0.70 / 0.63 / 0.48, rgb ≈ 70,46,123); Bardez's Objective frames (sat .47 / val .34) are re-saturated to
  that, both sides. Set sphere sits inside the text box's bottom-right corner (1282,1908, 72 px). Objective game
  text grows to fill the box width (`gt_grow`), since the slip's line breaks are fixed.
- Rev 9e (Bill 2026-10-12): Objective purple is taken from the PC's Virtual Block cards / the slip, not from Bardez.
  The Dark Objective frame is two-tone: blue-purple (hue .70 / sat .70 / val .45) above the art window's lower
  bevel, red-purple (hue .76 / sat .64 / val .44) below it, side borders included — rev 9d's single tone was the
  upper one, which is why the text-box half read too blue next to the slip. The Light Objective is one purple (hue
  .75, between the PC card's .735 and the slip's .763) over the Endor-era silver-frost frame. Both frames are built
  by `make_objective_frames.py` from the Bardez XCFs. The set sphere sits in the purple margin at the text box's
  bottom-right corner (centre 39 px right of the box edge, 7 px above its bottom, 66 px across) as the slip prints
  it — never inside the box. Objective game text is set like the slip: 62 px AGCn on a 64 px pitch, starting 60 px
  in from the box's left edge, the longest line reaching to within ~10 px of its right edge; the text box reaches
  almost to the frame's box edge so the fitter can grow to that size (capped at 63).
- Rev 9f (Bill 2026-10-13): the Dark Objective frame is ONE purple over the whole frame — the red-purple of the slip
  (hue .76 / sat .64 / val .44), art half included. The PC card's bluer upper half (rev 9e's two-tone) is not wanted.
- Rev 10 (VS5 run, 2026-10-13): `crop_slips.py` whites out only solid dark runs (> 200 px) above the heading — the
  old "35 % dark row" test erased long headings (•Location, Location, Location); 20 earlier crops were re-cut and
  re-uploaded. Icon column packing: two Warrior icons share Bardez's tall box (`col-warrior2.png`); when the stack
  (plus the set sphere) is taller than the column, everything shrinks uniformly from the first slot down to the
  sphere's bottom (IG-88: pilot, warrior×2, presence). Presence = Game Aid g013 (droid on red). Light Jedi Master
  (Yoda) = the Rebel frame with Bardez's Dark Jedi Master disc re-hued to the blue blade (`disc-jedi-light.png`,
  card `disc`). A grabber box on an EFFECT banner (#16) is `"grabber": true`; an Immediate Effect without one
  (#27) is `"grabber": false`. `qa_text.py N` compares every card's text with the sheet's text layer. The VS5 set
  sphere is the cover's own 46 px icon upscaled (`ovs-set-5.png`).
- Rev 10a (Bill 2026-10-13): the Presence icon is the Episode I one (Coruscant: red box, battle-droid figure) —
  `col-presence.png` is cut from the 745 px Theed-D-dfssquadronstarfighter.gif, not a Game Aid icon. Episode I
  base cards (Coruscant / Theed Palace / Tatooine) have their art window placed a little differently from the
  classic frame: `art_trim` cuts the mapped art box at the innermost silver line on each edge (Secure Route).
- Rev 11 (VS6 run, 2026-10-13): expansion ring icons for Cloud City, Jabba's Palace (also Jabba's Palace Sealed
  Deck), Reflections II, Death Star II, Reflections III and Coruscant, each cut from a 745 px Decipher scan by
  `cut_set_icon.py` (the ring is ~26 px across at 745 px, found by an annulus search right of the lore box).
  Inline icons: `{set:ds2}` / `{set:reflections3}` use the same files; `{light-force}` / `{dark-force}` = Game Aid
  g036 / g050 (Imperial Decree); `{episode1}` = g033 (Hopping Mad); `{icon:republic}` → `{republic-crest}` = g062,
  the Republic affiliation crest itself (The Emperor (V): "Gains [Republic] at opponent's Senate"). Two-disc
  characters (The Emperor: Dark Jedi Master + Imperial on the Reflections II frame): `disc` + `disc2` draw the second
  disc right of the first and shorten the title bar. Margin credits sit centred in the red margin between frame
  edge and text box (x 236 / 1404), never touching the box (Bill, Secure Route); on characters the left credit runs
  above the deploy/forfeit boxes, white on dark frames, shrunk to fit. A slip heading with extra words ("•Boba Fett
  ([sphere] persona only) (V)") goes in `heading`; title/caption stay as the bottom strip prints them.
  `crop_slips.py` also whites out any inked run above the heading (the number tail of the slip above).
- Rev 11a (Bill 2026-10-13): the inline Republic icon is the round silver Republic crest (Game Aid g007, "Character
  - Republic"), as The Emperor (V) slip prints it — not g062 (Clone Army). TEST, not adopted: Defensive Shield frames
  with the slip's red→cyan fade (`make_shield_fade.py` → `ds-/ls-shield-fade.png`, templates `ds-/ls-shield-fade`);
  fade curve measured on the VS6 slips (≈6 % cyan at card y 1445, 55 % at 1649, full by 1790), banner kept from the
  shield frame. Live shields still use the hybrid (hard-cut) frames until Bill decides.
- Rev 11b (Bill 2026-10-13, Rebel Planners (V)): never use a `decipher-archive` file that is a photo of the printed
  card on a white page (odd size, e.g. 367×506) as the art source — its silver-frame bbox and scale do not map, and
  the art window takes in the scan's own frame (frame-in-frame). Use the square-on 350/745 px scan of the same art
  for `art.src`; the archive photo may still be read for lore and copyright. Only VS6 #18 was affected in sets 1–6.
- Rev 12 (VS7 run + Bill 2026-10-13): Defensive Shields — the hybrid (hard cut at the banner) stays the PRIMARY
  shield template (`ds-shield` / `ls-shield`); the slips' red→cyan fade is an optional era template
  (`ds-shield-fade` / `ls-shield-fade`). `build_vs.py` uses the fade for the Original Virtual sets (it is the
  technique their Remaster slips used); a card can force the primary frame with `"shield_style": "hybrid"`.
  Label-only stat boxes (FORCE-SENSITIVE, MAINTENANCE DROID…) shrink to stay on one line. A droid printing three
  separate stat boxes (LE-BO2D9: POWER / ARMOR / MAINTENANCE DROID) gets the Rebel frame's three-box stat row laid
  over the droid frame's wide box (`ls-stats-row3.png`). Legal dates now from the swccgpc.com news archive:
  VS6 released 21 Nov 2003, final revision legal 12 Jan 2004; VS7 released 16 Jul 2004 (no separate legal date).
- Rev 13 (Bill 2026-10-13: "as indistinguishable from the original cards as possible, except where we clearly
  enhance"): stat boxes — the text sits in the wells as painted in the frame (`stat_boxes()` measures them per
  template), 16 px inset, labels AGBoldCnA 59 px tight-tracked with a 1.1 px stroke (Decipher's heavier caps), values
  AGMedExt 63 px with a 1.6 px stroke; a label-only box (MAINTENANCE DROID) keeps full height and is squeezed
  horizontally to the well. Lore — set from the printed text edges (Dark text from x 319, Light from 326) with the
  right limit, first-line indent, the Light window's bevelled corner and tracking fitted on 47 printed 745 px cards
  (`LORE_X`; 16/26 Dark and 17/21 Light cards break exactly as printed). Bold lore keywords are part of the lore:
  Decipher bolds characteristics (leader, spy, smuggler, gambler, bounty hunter, scout, thief, information broker,
  gangster, Enclosed, hologram, dejarik…) — checked on every 745 px scan / PC remake; low-res-only cards follow the
  same rule (noted per card). `fit_stats.py` fits stat typography to a scan.
- Rev 14 (VS8 run 2026-10-13): game-text fitting tightens tracking (to −1.2 px) and then leading (to 0.94 em) before
  it shrinks the size, as the slips set a long text (Thrown Back (V): 56 px instead of 50). Margin credits are
  centred in the coloured margin per side (Light x 185 / 1402, Dark 187 / 1391), measured with JS at 46 px and shrunk
  only to fit; below 34 px they wrap to two balanced lines ("Original concept / by Mike Gemme", The Emperor (V)).
  Enhanced Jabba's Palace ring icon (`set-ejp-grainy.png`). `make_upload.py` builds the wiki upload folder (745 px
  webp q90 remasters, slips under the stub names, set symbol); `--changed` keeps only remasters that differ. Wiki
  text: `{pilot:N}, M: <ship>.` → "Adds N to power of anything he pilots (M if <ship>)"; "▲ and/or ▼",
  "▲ or ▼ attempt", "▼ … ;" and "always {alter}" have their own expansions. VS8 released 24 Nov 2004 (swccgpc.com
  news; no separate legal date). Starting Interrupt article.
- Rev 15 (Bill 2026-10-13, Obi-Wan Kenobi (V) / Jabba's Space Cruiser (V)): stat values were too heavy — the
  synthetic bold on the single-weight Medium Extended face plus a 1.6 px stroke. Now no synthetic bold, 1.1 px stroke,
  scaleX 1.15 (Decipher's digits are wider and more open: easier 5s and 6s). Values sit at the RIGHT end of their box
  as Decipher prints them (ARMOR      5, LANDSPEED    2), except a character's wide third box, where the value
  follows the label (ARMOR 5 on Boba Fett). Lore keywords: bolding a character's characteristics (leader, spy,
  smuggler, gambler, scout, thief, bounty hunter, information broker, gangster, assassin) is a welcome enhancement even
  where Decipher printed them plain — `build_vs.bold_keywords()` does it on the remaster image only (not "Former
  scout", not the verb "spy on"); the wiki lore stays as printed.
- Rev 16 (VS9 run 2026-10-13): Admiral's Order template (`ls-admirals-order`, Bardez "LS - Admiral's Order.xcf"
  Template layer: silver title bar + black text box over full-bleed art, white game text, no copyright overlay —
  the scan keeps its own); the art maps the base scan by a measured `art.bbox` (text-box bevel ↔ scan). New:
  `stat_icon` (a round icon left of the stat row — Mon Mothma (V)'s Republic crest), two-line margin credits from a
  `\n` in the credit (both lines side by side in one margin), right credits run below the column icons and above the
  set sphere, `ds2` column icon (Death Star II sphere, Luke Skywalker, Rebel Scout (V)). Bill: "spy" in "to spy on"
  is bolded too. The VS8 #20 inline icon is the Death Star II icon (GEMP), not Independent. VS9 sheet from the
  starwarsccg.org CDN (the IA capture no longer opens); release date not found (2005 or later from the credits).
- Rev 17 (Bill 2026-10-13, Chewie's AT-ST (V)): right-set stat values stand in from the box's right end by the
  inset + 26 px (the slips' gap), not tight against the bevel. VS10 Fourth Anthology: slips found with a grey-outline
  threshold (`sheet.DARK_THR`), two-digit set numbers parsed by regex in crop_slips / make_upload / wiki_vs, "Out Of
  Play Interrupt" links to [[Interrupt]], "just ▲ or ▼" written out; release dates of VS9/VS10 not found.
- Rev 18 (VS11 run 2026-10-13): Epic Event template (`epic-event`, Bardez "DS - Epic Event.xcf" Epic Event icon +
  Epic Objective frame + text box, recoloured to the slips' Reflections III purple; white text on the black box, black
  margin credits); Republic affiliation disc (Bardez "LS - Character - Rebel.xcf" Republic layer, `disc-republic.png`);
  Reflections III art trimmed like the Episode I sets; `credit_bottom` (a credit under the text box, Lord Vader (V));
  accented letters in titles drawn over Fiorello (Padmé); wiki text "▲ or ▼" written out, "she pilots" for women.
- Rev 19 (VS12 run 2026-10-13): tall slips for printed cards without a lore box (Jedi Test #5 It Is The Future You
  See (V); Reflections II "There Is No Try & Oppressive Enforcement" (V)) — templates `ls-jeditest-tall` (olive top,
  the slip's purple foot, silver text box) and `ds-effect-tall`, built from Bardez's Epic Objective frame with the art
  window shortened to the printed art's proportion; the art is the scan's own art rectangle (`art.rect`) cover-fitted.
  Titles longer than their bar are condensed (scaleX). Republic disc on both sides (Daultay Dofine). Ring icons for
  Tatooine and Theed Palace from Bardez's Epic Event template; Enhanced Cloud City and Official Tournament Sealed Deck
  use the premium silver sphere. Sheets up to 530 px tall slips (`sheet.MAX_H`). Dark Jedi Lightsaber lore misprint
  "Mutlifaceted" corrected.
- Rev 20 (Bill 2026-10-13 evening): (1) stat values set right keep at least a 30 px gap after the label; when label +
  gap + value do not fit, the label is condensed (≥ 0.8) instead of the value crowding the R (Green Squadron 1 (V)).
  (2) Margin-credit ink follows the margin it sits on, as the slips print it: black on bright red/silver/blue
  margins (Dark Effects, Endor Shield (V)), white on the dark grey/black character frames (`margin_ink()`).
  (3) Two-line credits start at 42 px and run from above the stat row; `margin_right_at: "top"` puts a right credit
  above the column icons, level with the stats (Padmé Naberrie (V)). (4) Deep Hatred (V): art from the scan's own
  art rectangle (`art.rect`) — the mapped Reflections III purple frame had put a frame inside the frame.
- Rev 21 (Bill 2026-10-13, Lord Vader (V) / Mara Jade (V) / Stinger (V)): stat labels 55 px with 1.4 px tracking,
  widened ×1.1 (Decipher's stat caps are wider than AG Bold Condensed); in narrow boxes the value first closes up
  (gap ≥ 28 px, right inset ≥ 18 px), then the label narrows (≥ 0.8). Credit ink by hue: black on bright and on red
  margins, white on darker grey/blue/green Dark frames. Right credits can sit above the column icons
  (`margin_right_at: "top"`, Mara Jade, Stinger) or split around them (`margin_right_top` + `margin_right`, Aurra
  Sing). Left credit stays above the scomp ring. Stinger's column icons are Independent + Nav Computer (GEMP), not
  Nav + Astromech. Two-line credits on dark frames start at 48 px.
- Rev 22 (VS13 run 2026-10-13): full location overlays (both halves, renamed sites) render as landscape sites
  (`loc-site`) and a renamed system (`loc-system`, with parsec); the Dark Force icon on sites is now the red saber
  (`assets/loc/force-dark.png`, a red recolour of the Light glow), `dark_force_count: 2` prints two sabers. Site
  credits run across the bottom border between caption and number. `invert_text` turns title, lore, banner, text and
  destiny upside down in an upright frame (Dagobah's Through The Force Things You Will See). Wiki rows for renamed
  locations lead with the new name (and parsec) and give both halves ("Dark (printed)" only when the slip prints one
  half). Sheet crops: tall site slips (`sheet.MAX_H[13]`), the upside-down #12 turned upright by hand.
- Rev 23 (Bill 2026-10-14, VS13 locations): a renamed location is named by its bar title (Alderaan (Blown Away) (V),
  not "Asteroid Field (Light) (V)"): on these slips the caption only names the base card + (V); stubs move to the new
  title (`moves.txt`, redirects kept). Bar titles in the slip lettering: AG Bold Condensed caps, 74 px, condensed to
  the bar; the uniqueness dot/diamond is red on the bar of the card's own side and in the bar's text colour on the
  other (black on Light bar, white on Dark bar). Parsec in AG Medium Extended. The title bar runs right up to the
  first icon box (the end cap is slid over the frame's default boxes; no empty box). `light_force_count: 2` = two
  blue sabers on a system. Starship-site frames tinted as printed (`frame_tint`). Icons per slip (and GEMP where the
  slip is unclear: Carida = grabber). Site slips are published landscape (`landscape_slips.py`: heading on top, body
  turned 90°, the whole caption kept left and only the number moved to the right edge). Site credits run up the left
  margin. Republic disc re-cut light blue and brighter, as Decipher prints it.
- Rev 24 (Bill 2026-10-14): starship/vehicle sites take Decipher's blue frame (`frame_style`): `ls-starship` = Home One:
  War Room (blue paint worn through to silver, silver rim round the art), `ds-starship` = Executor: Comm Station
  (smooth deeper blue); title bars, Force slots and text boxes keep silver / black. Site text is set as the slips:
  the Light text box is the box interior (`ls_text` y 1344, h 86) so one line sits centred; `game_text_lines` /
  `dark_text_lines` carry the slip's line breaks (no re-wrapping); a two-line half gets the slip's taller text box
  (+28 px, bar and icons slide toward the art, `loc_grow`). Bar titles 57 px, 2 px tracking; text 56/58 px.
- Rev 25 (Bill 2026-10-14): Dark locations (remaster and V-slip) are shown from the Dark Side's seat, as Decipher
  prints them: the card is turned 180° (Dark half, icons, copyright and set sphere at the bottom/left), the picture
  stays upright and the caption strip stays in the bottom margin; landscape slips turn the body +90° for Dark cards.
- Rev 26 (VS14 run 2026-10-14): `ds-admirals-order` (same frame as Light; Decipher printed both sides alike); Episode I
  icon under the expansion ring (`ring_icons: ["episode1"]`, Bardez site layers, as the Coruscant/Theed/Tatooine/
  Reflections III printed cards carry it; set on earlier cards too); bottom credits left + right (`credit_bottom` as a
  list); long banners tighten then condense (HEAVILY-MODIFIED LIGHT FREIGHTER); GIF transparency (PC remakes mark
  their brightest highlight transparent) composited on white; combo slips renamed like locations (Obi-Wan In Radiant
  VII (V), GEMP agrees); wiki "non-[Immune to Sense]". sheet.py skips the stray "00" under VS14's numbers.
- Rev 27 (Bill 2026-10-14, Black 3 (V)): two Republic icons, as the PC Game Aid (Feb 2024) lists them: the ROUND crest
  = "Character - Republic" (affiliation disc; inline when the text means a character, The Emperor (V) "Gains
  [Republic]"), the SQUARE lavender tile = "Republic" under Other Features (starship icon column, Radiant VII; inline
  for starships: Black 3 (V), Diversionary Tactics (V)). `{icon:republic-square}` inline, column icon `republic` =
  col-republic.png (Game Aid g037). The column "republic" had been mapped to the maintenance icon by mistake.
- Rev 28 (VS15 run 2026-10-14): `text_grow` (tall slips whose banner and text box sit higher: the frame's art
  bottom, banner and text-box top slide up, the box stretches — Anger, Fear, Aggression (V), Knowledge And Defense
  (V), Uncharted Settlements (V), Abyssin Ornament (V)); no-lore-box base cards (Reflections II combos) take the scan's
  own art rectangle (`art.rect`) into the window above the raised banner; landscape site slip line breaks recorded
  (`game_text_lines`/`dark_text_lines`); stat values never wrap (Brainiac "X-Y"). Wiki: no stub moves when the stub
  already carries the slip's name (VS15 stubs were named by the slips); slip-printed lore that replaces the base
  card's lore (Shada, The Mandalorian) is never written onto the Decipher base page.
- Rev 29 (Bill 2026-10-14): tall slips are built like the PC's own reissue (V0 Knowledge And Defense): the art window
  gets shorter WITH its own corners (frame rows rebuilt top edge / stretched sides / bottom edge), banner and text box
  move up by `text_grow`, the art is centre-cropped into the window under the frame (no overlay over the frame); a
  no-lore-box base merges the lore window into the art window. Grows kept small (01: 160, 52: 170, 33: 110, 37: 230)
  to show more picture. ds-effect banner box spans the bar (STARTING EFFECT no longer condensed). Dagobah expansion
  icon = Decipher's Yoda-eye sphere (`set-dagobah-decipher.png`, from the wiki's Icon-set-Dagobah inner disc), not the
  dark-green redraw; 64 Dagobah-based remasters re-uploaded.
- Rev 30 (Bill 2026-10-14): merged window on no-lore-box base cards (Reflections II combos) starts just under the
  title bar (lore top + 5) and its top corners are chamfered (corner rows sheared, 100 px at 45°) as the printed
  card shows them.
- Rev 31 (Bill 2026-10-14, "start with the base card frame and build the taller card from the bottom"): tall slips
  over printed cards WITHOUT a lore box use `nolore_frame()`: the top is the no-lore frame of the base card's family
  (LS: Bardez's scratched LS Epic Objective frame recoloured to the LS Effect red → `ls-nolore-top.png`; DS:
  `ds-effect-tall.png`) — title bar and the chamfered window corners exactly as the printed Reflections II combos;
  the bottom (window bottom edge, banner, text box) is the template's own frame raised by `text_grow`; the window
  sides between are stretched and cross-faded (40 rows); the template's card-type disc and destiny hole are pasted
  back. Replaces the rev 30 corner shear.
- Rev 32 (Bill 2026-10-14, "they all really need to be the originals"): every expansion sphere (ring right of the
  lore box, inline `{set:…}`, margin `set:…`, column `ds2`) is Decipher's own: `set-<key>-decipher.png` = the inner
  disc of the wiki's Icon-set-* images (A New Hope, Cloud City, Death Star II, Endor, Hoth, Jabba's Palace, Special
  Edition, premium; Dagobah earlier), else cut from a 745 px Decipher scan at the ring (Coruscant, Reflections II,
  Reflections III, Theed Palace, Tatooine, Enhanced Jabba's Palace). Bardez/PC redraws (`-grainy`, `-bardez`,
  `set-theed.png`, `set-tatooine.png`) are no longer used. No-lore tall frames place the sphere in the frame's own
  ring position (1390, 373), clear of the art. 493 remasters re-uploaded.
- Rev 33 (Bill 2026-10-14 + VS16 run): expansion spheres cut from Decipher scans are centred on the sphere by fitting
  the black ring (circle fit, ring included, 2–3 scans averaged) — the earlier cut was off-centre (more black on one
  side) and looked darker; Reflections II now matches the scan's purple. VS16: maintenance flag glyph
  (`{icon:maintenance-flag}`, cut at 1200 DPI); `no_expansion_ring` (slips that drop the base card's ring); dual
  affiliations "Rebel + Republic" / "Alien + Republic" draw the Republic crest as a second disc; wiki banners split on
  ":" or "–"; slip-printed lore never written to base pages (`base_lore` used for the Decipher page's lore fix).
- Rev 34 (Bill 2026-10-14, Watto (V)): a credit the slip prints in the black caption strip stays there
  (`credit_strip`, right-aligned before the number). Art from the printed scan by its own window (`art.rect`) when the
  auto frame detection zooms (dark Episode I frames); never a Virtual Block reissue whose art is cropped differently.
- Rev 35 (Bill 2026-10-14, "zoom-in bug"): the Episode I-era edge trim (`art_trim`) cut bright picture edges as if they
  were silver frame and zoomed the art. Every Coruscant / Theed Palace / Tatooine / Reflections III base card now maps
  the printed scan by its measured window (`art.rect`): portraits ≈ [43,139,305,319–324] at 350 px (found by the
  per-pixel variance across scans of the same frame, i.e. where the picture differs), sites ≈ [45,91,447,260] at
  490 px; checked by template-matching the rendered art back into the scan (full window, ~263 px / ~400 px wide).
  58 remasters re-rendered (VS5, 8–16).
- Rev 36 (VS17 The Force Unleashed, 2026-10-14): VS17 prints no Virtual sphere — its set mark is the cover's
  diamond-17 (`ovs-set-17.png`, cut from the cover with transparency; shown in the lower icon slot as the slips do).
  Inline diamond marks with a number = that Virtual Set's card (`{vset:N}`, drawn as SVG; wiki text "[Virtual Set N]").
  Slips that print their own art (Force Unleashed photos) use the slip crop as the art source, mapped by its window
  (`art.src` = slip, `art.rect`, `slip_art`, base scan kept as `art.base_src`). AI (alternate image) slips are their
  own card file (`NNb.json`, `alt_image`, id `vsN-NNb`), with their own stub and hub row ("12 AI"). Sith affiliation
  disc (Darth Maul face) cut from the slip (`disc-sith.png`). Female characters (lore "Female.") get "she" in the
  wiki's pilot-icon expansion. Hub leads for VS12+ no longer claim a December 2006 Remaster reissue (that covered
  VS1–11 only); VS13+ leads say some slips cover the whole card.
- Rev 37 (card maker, Bill 2026-10-15): the bottom black caption strip is **blank by default** for every card
  (Decipher cards never print it; only some PC virtual cards do, sometimes with more than one item) — the editor
  offers strip-left (`caption`), strip-right (`credit_strip`) and number. An empty `caption` now means no strip text
  (it no longer falls back to the title). Systems: the expansion sphere sits in the top-left margin
  (`loc-system.system_ring`, measured on the Hoth / Bespin scans); drawn only when `draw_system_ring` (no scan art, or
  a different set than the scan's). Reflections Gold "wide vision" templates (`rg-{ls,ds}-{interrupt,effect}`,
  `wide: true` on a 2220×1632 canvas): Bardez's [Horizontal] XCFs (`make_rg_frames.py`), full-art window, banner
  type in the header, gold Reflections Gold sphere under the destiny lobe (`set-reflections-gold.png`, cut from Andy
  Talaga's reconstructions), 0–4 gold credit coins (`credits`) right of the text box.
- Rev 38 (card maker, Bill 2026-10-15): no Reflections Gold Weapon / Starship layouts; the wide **weapon** layout
  exists because Decipher printed one (Maul's Double-Bladed Lightsaber, Reflections III, 13_75): `ds-weapon-wide`
  from Bardez "DS - Weapon [Horizontal]" (Template layer, lore / text / destiny windows filled black), Dark Side only.
  13_75 opens wide automatically (`adapter.WIDE_PRINTED`).
- Rev 39 (card maker troubleshooting vs Holotable scans, 2026-10-15): printed-Decipher defaults in the card maker only
  (VS remasters unchanged, regression-checked): expansion sphere in its black hole; the vertical copyright line by set
  year (`adapter.copyright_for`, editable); character `extraText` (FORCE-ATTUNED …) in the third stat box; vehicles
  "COMBAT VEHICLE: AT-ST"; location icon boxes scomp outermost, then planet, then the rest (Docking Bay 94);
  Defensive Shields on Decipher's own frames (`ls-/ds-shield-dc`); creatures `creature-dc` (black title, banner such
  as GUARD CREATURE); Objectives: setup sentence italic, a paragraph per *For* / *While* / *Flip*; `¶` (= a typed
  line break in the editor) is a paragraph break that keeps normal wrapping. Library art is fetched from GitHub raw
  first, jsDelivr second, then the card's own scan.
- Rev 40 (Bill 2026-10-15: "re-create any card ever published by Decipher and the PC"): the card maker keeps every
  variant. **Frame style** per card: `decipher` (as printed) or `ovs` (Original Virtual remaster slips: shield fade,
  creature as remastered, virtual-set symbol, caption strip as the slip). The Original Virtual Sets 1–17 open in the
  editor straight from their transcriptions (`cards/vsN/NN.json`, GEMP ids `11NN_<slip>`, Browse group "Original
  Virtual Sets") with their published art (kind `ovs`) — pixel-identical to the wiki remasters (checked 6 cards).
  Systems from Holotable faces map the card area by fixed coordinates (starfield defeats edge detection); two Dark
  Force icons on systems (Dagobah); systems print the copyright split Lucasfilm left / Decipher right.
- Rev 41 (Bill 2026-10-15: modern and legacy virtual set symbols): the card maker draws the Players Committee set
  marks in the lower icon slot as vector (`render.set_mark_html`, card key `set_mark`): modern Virtual Sets 0–27
  `pc:N` = the number (condensed bold, white, blue edge) on a tilted blue ring — gold ring and orange edge for Set 0;
  2009–2014 Virtual Blocks `vb:N` = black diamond, white edge, number over the V chevron. Sizes and places measured on
  Holotable faces (Captain Lando Calrissian VS13, Admiral Raddus VS9, A Good Blaster At Your Side VS0, 2-1B (V)
  Virtual Block 2). The Virtual Block (legacy) cards are in the editor too (ids `<set>_L<id>`, Browse group).
  Editor: one "Set mark" choice — none / Original Virtual Set 1–17 / Virtual Block 1–9 / Virtual Set 0–27.
- Rev 42 (card maker, modern + legacy PC cards vs Holotable faces, 2026-10-15): titles print without "(V)"/"(AI)"
  (that names the printing); Virtual Block cards print "•Title (V)" in the strip; "Blank" lore = empty; Virtual
  Defensive Shields mark = gold ring + D (`pc:D`), Virtual Block shields = diamond + D (`vb:D`); Light Virtual Block
  shields default to the red→cyan fade (Affect Mind (V)) — every shield's frame is now a choice in the editor
  (Decipher / fade / hybrid); modern PC cards get "ARTWORK NEITHER AFFILIATED WITH NOR ENDORSED BY LUCASFILM LTD."
  beside the art; credit fields for both margins. Inline icons from the PC's Feb 2024 Game Aid sheet
  (`assets/icons/pc-gameaid-named/`, `{ga:<name>}`): Episode VII, Clone Army, Separatist, First Order, Resistance,
  Trade Federation, Independent Starship, Skywalker / Sidious themes, Selective Creature, Virtual; `[Virtual Block N]`
  → `{vb:N}` and `[Set N]` → `{pcset:N}` inline marks; `[Permanent Weapon]`, `[Presence]`, `[Nav Computer]`,
  `[Light Side]` / `[Dark Side]` mapped. Not yet drawn (no icon art): [Scoundrel], [Setup], [Vader].
- Rev 43 (Bill 2026-10-15, "get these"): PC icons placed as printed — column (framed): Selective Creature,
  Independent Starship, Trade Federation, Clone Army, Separatist, Resistance, First Order, Vader (starships: faction
  icon at the top of the column); discs under the expansion sphere (or in its place): Episode I, Episode VII,
  Sidious, Skywalker (`render.RING_DISCS`); Setup in the banner's right end (`banner_icon: setup`); Scoundrel as a
  portrait disc in the left margin at the text box (`margin_icon`). Inline: [Scoundrel] [Setup] [Vader]. Art: wiki
  180 px icons and the PC Game Aid sheet; Scoundrel / Setup / Vader cut from the only faces that carry them (350 px
  legacy scans: soft — replace when a sharper source turns up). Titles drop "(Holo AI)"-style printing names too. PC virtual cards take the base card's expansion sphere from their icon list (Blockade Support Ship: Coruscant); Sidious disc in the right margin at the text box top.
- Rev 44 (Bill 2026-10-15): set-mark coverage — Decipher spheres for every set (ESB 2-player, Enhanced Premiere,
  Third Anthology and Virtual Premium print the silver premium sphere, `SET_ICON["Premium"]`; Premiere and the
  Premiere 2-player print none); Original Virtual 1–17 (Remaster sheets); Virtual Blocks 1–9 + D (diamond); Virtual
  Sets 0–27 + D + P (ring) and future 28–40 in the editor; exported PNGs in `assets/set-marks/` for the PC. PC Game Aid
  icons Real-ESRGAN x4 (ONNX, `pc-gameaid-x4/`); Scoundrel / Setup / Vader x4 from 350 px legacy faces — still
  guesses at detail, replace with PC originals when available.
- Rev 45 (Bill 2026-10-15: "both standards"): expansion spheres come in two styles — `decipher` (as printed, also on
  the Original Virtual and Virtual Block slips) and `pc` (the Players Committee's redraws from their Game Aid sheet,
  Real-ESRGAN x4, as printed on the modern Virtual Sets: brighter Special Edition, orange-red Cloud City …):
  `assets/icons/set-<key>-pc.png`, card key `expansion_style`, picker in the editor; modern PC cards default to `pc`.
- Rev 46 (card maker, modern + legacy PC cards vs Holotable, 2026-10-15): printing tags stripped from titles ((V),
  (AI), (Premium), set names); PC-era game text in the PC's printed shorthand (pilot icon + N, ▼ / ▲ for
  deploy / take into hand from Reserve Deck, {alter} for "(Immune to Alter.)"); the PC JSON's single quotes back to
  printed “double” quotes; USED: / LOST: / STARTING: on their own lines; (V) cards take the original printing's
  expansion sphere; Mandalorian ARMOR stat; Virtual Block shields fade on both sides; Virtual Block lore without the
  remaster's bold characteristics; Virtual Block Dark shields `ds-shield-vb` (Decipher Dark shield frame, cyan → red foot, No Escape (V)); Devices on their own frames (`ds-/ls-device`, Bardez Device type icon).
- Rev 47 (Bill 2026-10-15: "544 deploy, 398 forfeit … not infinitely"): bounded fit for numbers — destiny up to 8
  characters (the pill widens left as R2-D2's "2 or 5", max +190 px, then condenses), deploy / forfeit up to 4 and
  stat values up to 5 characters (condense to ≥55 % width, then shrink, never leave their box). Limits enforced in the
  editor and in `adapter.spec_to_card` for API callers. 1–2 character values render exactly as before (VS1–17 regression identical).
- Rev 48 (Bill 2026-10-15: move / resize / hide / reset pieces): every drawn element belongs to a named piece (art,
  affiliation, title, destiny, lore, stats, banner, game_text, deploy, forfeit, scomp, icons, set_mark, expansion,
  coins, ring_icons, margin_icon, location_text, parsec, copyright, credits, caption, number), wrapped in a full-card
  layer. Card key `layout: {piece: {dx, dy (print px, ±2000), sx, sy (0.2–4), hidden}}` is applied after all fitting
  (CSS translate / scale about the piece's own centre, never changing the template); the render reports each piece's
  box (`X-Piece-Boxes`) so the editor can select, drag, resize and nudge on the preview. No layout = pixel-identical.
- Rev 49 (Bill 2026-10-15, Ahsoka Tano With Lightsabers): card maker pictures fill the frame's whole window
  (`render.frame_hole`, measured from the frame's alpha; `art_cover_hole` set by the adapter, VS remasters
  unchanged) — some frames' holes run past the template art box and left a black sliver. Editor: expansion symbol
  moved up into the Card section ("top, beside the lore"); the set mark is the "bottom corner".
- Rev 50 (Bill 2026-11-01: "create all of the Defensive Shields … so these Original Virtual Defensive Shields can
  continue to be easily created"): the Players Committee's 4 December 2006 sheet **Virtual Set: Defensive Shields**
  (18 slips, GEMP 1100) runs through the same pipeline as Virtual Sets 1–17 under the set key `DS`
  (`ovs_sets.py`: name, sheet PDF, GEMP set, file prefixes, slip titles). Folders `src/slips/vsDS/` (DefensiveShields.pdf
  from the Internet Archive + p300 pages + crops), `src/vsDS/` (base scans), `cards/vsDS/NN.json`, renders
  `out/vsDS-NN_*.png`; set sphere `assets/icons/ovs-set-DS.png` (the cover's red orb, 74 px → 312 px, round mask).
  `python3 crop_slips.py DS`, `slip_lines.py DS`, `qa_text.py DS`, `build_vs.py DS`, `make_upload.py DS <dir>`
  (remasters `PS1-NN-<Title>-remaster.webp`, slips under the wiki's `PS1-NN-<Title>.png`). All 18 bases are Decipher
  Effects, so every slip uses the shield-fade frame like VS6 #24 / #34. Light shields now carry the banner grabber box
  position (`ls-shield` `banner_icon`, A Tragedy Has Occurred (V)). Decipher's non-unique-location mark ◇ (Ounee Ta,
  No Escape: "opponent’s ◇ site") is typed as U+25C7 and drawn in DejaVu Sans (`.dia`), like ▲ / ▼. Where a base
  has only a Virtual Shields (VSh-) remake as its "modern" scan, art comes from the Decipher scan: the shield face's
  narrower art window left a cyan strip at the art box's right edge.
- Rev 51 (Bill 2026-11-01: "automatically … increase the size of the font of text fields to fill the space … the label
  on the card margin matches better"): on portrait cards the bottom-margin caption and collector number are sized to
  fill the strip, like the PC slips, instead of a fixed 48 / 44 px. Each sits in its own 96 px box (caption from x 110,
  number right-aligned 125 px from the edge) and `fit_js` picks the largest size up to `caption_max` (default 74) that
  fits; the caption also stays 40 px clear of the number. Measured against Aim High (V), Do They Have A Code
  Clearance? (V) and Come Here You Big Coward (V): caption height, start and number edge within a few px of the slip
  at 745 wide. The uniqueness dot in the caption is a full bullet (DejaVu Sans, 0.9 em) instead of the 40 px Fiorello
  dot. Cards that set `caption_y` (landscape) or `caption_fixed` keep the old fixed caption. Do, Or Do Not (V) is
  unique (the dot was missing from our caption: a PC slip error Bill confirmed).
- Rev 52 (Bill 2026-11-01: rev 51 cut "Aim High (V)" and "02" off at the bottom — "there has to be some space above and
  below the texts in the margin … not touching the bottom of the card nor the card image itself above it"): rev 51
  centred the text in a 96 px box measured on the 1632 master, but the Holotable/GEMP image keeps master rows only up
  to 2150 (`holotable_size`), so the lower half fell outside. Now the strip is explicit: `strip_top` 2076 (first black
  row under the frame; starship / Rebel Tech frames sit 1–2 px lower and still clear by 3 px) to `strip_bottom` 2150 (the visible card edge), inset by `strip_pad` 6 (3 px at 745) (template / card keys).
  `fit_js` reads the face's real ascent (capitals and parentheses) and descender from canvas `measureText`, takes the largest size whose cap
  + descender fit the padded strip (max `caption_max` 74), and puts the baseline at strip_top + pad + cap height, so every
  caption shares one baseline whatever its letters. The number's digits stand 0.86 of the caption's cap height on the
  same baseline (the slip's ratio); its −14° skew is on the digits themselves (skewing the zero-height box threw them
  ~500 px left). A caption too wide shrinks at the same baseline until it clears the number by 40 px. Horizontal, as
  the slip: caption ink starts just inside the frame's left edge (`caption_x` 140), the number ends ~20 px inside its
  right edge (`number_right` 185). Checked on all 18 Defensive Shields and VS3 interrupt, character, weapon, starship and Imperial frames at 745:
  ink at least 3 px under every frame and 3 px above the card edge, size within 1 px of the slip. Multiple uniqueness dots close up (each dot after the first −0.12 em).
- Rev 53 (Bill 2026-11-02, Aim High (V): "the V is a little thinner and the parenthesis are a different shape and the 02
  … is wider … much more closely emulate the margin text boxes to the original slips"): the faces now come from the
  PC's own PDF. `pdffonts` / PyMuPDF on DefensiveShields.pdf: the margin caption is **Arial Narrow Bold**, the bullet
  **ATFiorello-Condensed**, the number **AkzidenzGroteskBE-BoldIt**. The caption is drawn 7.54 pt tall and condensed
  to 90.6 % (glyph advances give a 6.83 pt em; the capitals stand 5.4 pt), the bullet 7.56 pt, the number 7.08 pt, all
  on one baseline 6.4 pt below the frame's bottom edge. The bullet starts 0.57 pt inside the frame's left edge, and the
  number ends 4.5 pt inside its right edge. Scaled by the frame width (163.2 pt = 1336 master px, 8.19 px/pt): caption
  `PCCap` (Liberation Sans Narrow Bold, Arial Narrow's metric twin) 61.7 px with scaleX 0.906, bullet Fiorello 1.003 em
  (counter-scaled so it stays round), number `PCNum` (the digit subset embedded in the PDF, no skew: it is a true italic)
  58 px, baseline 52 px below `strip_top` − 1, `caption_x` 153, `number_right` 185. Card keys `caption_size`,
  `caption_scale_x`, `number_size` and `caption_drop` override these. `fit_js` only shrinks a size that would bring the
  ink within 3 px (745 scale) of the frame or the card edge, or a caption that would run within 40 px of the number.
  Checked on Aim High (V) against the PDF rendered at master scale: bullet, caption and number ink boxes within 1 px.
  On all 18 Defensive Shields and the VS3 interrupt, character, weapon, starship and Imperial frames, the ink stays at
  least 2 px under the frame and 5 px above the card edge.
- Rev 54 (2026-11-02, re-rendering VS1–17 with rev 53): frames end at different rows (master 2071 for the LS
  Interrupt up to 2081 for the LS droid character), so a fixed `strip_top` left C-3PO (V) VS2 #3 and Imperial-Class
  Star Destroyer (V) touching their frames. `frame_bottom()` now reads each card's final frame image (after
  grown / no-lore / captive variants), taking the last row opaque across the bottom bar's middle third. The strip starts
  one row below it, and the baseline sits 52 px under that row. Frames that fill the card (Admiral's Orders, game aids)
  keep the template `strip_top`. When a low frame would bring the descenders within 3 px (745 scale) of the card edge,
  `fit_js` raises the baseline instead of shrinking the type. Checked on every VS3 card: ink at least 3 px under the
  frame and 4 px above the edge.
- Rev 55 (2026-11-02, VS1–17 re-render): locations and the wide templates use the PC margin caption too. The slips print
  Corellia (V) and Asteroid Field (Light) (V) exactly like every other card, but `caption_y` templates kept the old
  48 px caption. `capgrow` now applies to every template unless the card sets `caption_fixed`. `frame_bottom()` takes
  the canvas height, so a landscape frame's bottom bar is found (sanity window H−180 … H−125). Templates whose frame it
  cannot read fall back to `caption_y` − 6. The visible strip ends at master row 2150 on portrait cards and 1560 on
  landscape ones (`holotable_size` crops). Decipher's non-unique mark ◇ prints in the caption as the slip's Arial
  lozenge ◊ (◊◊◊ Asteroid Field (Light) (V), VS13 #1).

- Rev 56 (2026-11-03, swccg-guild/work#51): `compare_pc.py` — the Epic #48 comparison tool (README "Compare with a
  PC card"). It measures every element against the PC image with no tolerance. Self-check: a known +3/+2 px shift is
  reported exactly; against the PC slip PDF, the rev 53 margin caption's ink starts 2 px higher (same bottom row) and
  the number sits 1–2 px higher, so rev 53's "within 1 px" held for the baseline and left edge only — to fix in the
  margin-strip work. `deploy.sh` now makes assets world-readable first: the rev 53 deploy left fonts at mode 600
  (scp) and the live editor failed to render until fixed by hand on 2026-11-03.
- Rev 57 (2026-11-03, swccg-guild/work#73): margin baseline. Measured on all 18 slips in DefensiveShields.pdf (its text
  layer), the number's baseline sits 51.5–52.2 px (master) under the frame's bottom edge, but the PC placed each caption
  by hand, 49.5–56.3 px (6.05–6.875 pt). Rev 53 put both at `_st − 1 + 52`, 1 px high; both now default to `_st + 52`.
  The DS specs carry their own slip values (`caption_drop`, `number_drop`), and a card placed from its slip keeps the
  slip's type size: its gap above the ink drops from 6 px to the PC's own ~2 px (rev 52's 6 px still holds for every
  other card). Result against the PDF (registered on the frame edge, 0.1 px steps at 745): caption and number within
  0.8 px on all 18 (before: up to 1.8 px). The remainder is the registration itself (caption and number share it on
  14 of 18) and the face: Liberation Sans Narrow's capitals stand ~0.9 px lower than Arial Narrow's at 745 (fonts kept,
  #48 Q6). Slip 04's caption has no uniqueness dot; Bill ruled that a PC mistake on 2026-11-01, so the remaster keeps
  •Do, Or Do Not (V) and its caption sits ~9 px right of the slip's (the dot's width).
  Regression: all 18 DS cards and 692 of the 694 VS1–17 images changed in the margin strip only. The other two are the
  `ls-starship` landscape sites _Redemption_: Command Post (V) (VS13 #11) and Blockade Flagship: Prison (V) (VS16 #7).
  Their worn-paint pattern changed on every run because it was seeded with Python's per-process salted `hash()`; it is
  now seeded with CRC32 of the card id, so it is the same on every run.
- Rev 58 (2026-11-03, swccg-guild/work#72; Bill 2026-11-03 5:28 AM: "characteristics like spy, leader, smugger, etc.
  should generally be bolded going forward"): Rev 15 stands. Every characteristic in `KEYWORDS` is bold in a character
  remaster's lore even where the slip prints it plain. `bold_check.py` checks every transcription (`test`: 0 misses;
  `report`: card × characteristic, reference vs remaster, possible PC errors). Every word a slip sets bold was
  reviewed. Three character characteristics joined `KEYWORDS`: **Jedi Council member** (5 slips bold), **musician** (1)
  and **senator** (1). "then-Senator" is a new exception, next to "Former …" and possessives. Enclosed, hologram and
  dejarik are not added: they are vehicle, site and creature words, ordinary elsewhere in lore, and stay bold only where
  their slip prints them. Lore changes on three remasters only: Bail Organa (V) and Senator Padmé Amidala (V) (*Senator*)
  and Jedi Advisor (*Jedi Council Member*).
- Rev 59 (2026-11-03, swccg-guild/work#63, Interrupts; Bill 2026-11-03: "we should not automatically assume either
  bardez's template or the PC one is automatically correct!"). Each element was checked three ways: CardMaker against
  12 PC interrupts (one per side × subtype), against 10 printed Decipher interrupts (745-px scans), and Bardez against
  both. Where the PC and the printed cards agree and Bardez differs, Bardez was wrong:
  - **Frames:** Bardez's interrupt frames are 0.5 % small and sit 3 px (745) high-left of the printed card. A frame-only
    fit gives the same scale and offset against the PC and against the printed scans: Light 1.00512, −5.7/−6.2 master
    px; Dark 1.003/1.004, 0/−6. Both frames are rescaled (premultiplied Lanczos) to 1347×1939 at (140, 139) and
    1353×1936 at (141, 141); refit 1.0002 / 0, 0. Frame MAD against the printed scans 7.2 → 4.2.
  - **Dark interrupt icon:** the PC and every printed Dark interrupt show the same orange swirl as the Light one;
    Bardez's Dark frame had a darker red/black swirl. The disc is taken from the Light frame (MAD in the disc 42 → 26).
  - **Boxes, measured against both references:** title +12/−6 (Light), +9/−10 (Dark) master px; title 82 px (was 80),
    tracking 0.6 / 0.4 px, Dark titles a 2 px stroke (the PC's Dark titles are slightly heavier); destiny +4/−10 and
    +2/−10; type banner 62 px, tracking 11.3, moved to the PC's centre; lore 7 / 4 px up, Dark first-line indent 80;
    game text 7 / 2 px up (`GT_BOX_PC`); copyright 25.9 px, tracking 0.8, x 1421 / 1420; expansion ring +2 down,
    Dark 59 px. All within 1 px of the PC (most 0); title, destiny and banner 0 against the printed scans too.
  - **PC-only elements:** the set mark (Decipher printed a set icon there) follows the PC: 68 px slot, digits 160 (was
    142), ring moved and thickened (`set_ring`, `set_ring_w`); size and place now 0 px. Episode discs stay in the second
    slot under the expansion sphere even when a PC card has no sphere (`ring_fill` is now for printed cards only); the
    Skywalker disc sits at the text box top like Sidious, in a dark hole.
  - **Text, every card type:** the PC's ▲ shorthand was garbled when the object contained "deploy" or parentheses
    ("take Luke … printed ▼ < 4 into hand" → "▲ Luke … with printed deploy < 4", A New Hope; the bracketed "(reshuffle)" is
    dropped as the PC prints it; 27 PC cards change, six checked against their PC images). A hyphenated word and the icon after it stay on one line ("non-[icon]"). PC titles print
    typographic apostrophes (I’ve, It’s); the card data spells them straight.
  - **Left as found, explained in evidence/63/checklist.md:** the 1 px art offset (the build cuts art from the PC's
    350-px scan); game text and lore are ~1 % narrower than the PC's (the fitter's tracking, #49); PC-only labels
    ("Image courtesy of …", "Original concept by …", the original-title label) are not in the PC card data.
- Rev 60 (2026-11-03, #63 follow-up, Bill: "Sure. Try that please"): `compare_pc.py` now builds each card with art cut
  from the full-size reference itself, at the build's own art-window box (sub-pixel crop at master scale), instead of
  the server's 350-px scan; `--scan-art` keeps the old behaviour. The art row now measures the template: 0 px on the
  Dark interrupts, 0–1 px on the Light ones (half-pixel window edges at 745). `build_vs.convert` no longer fails on an
  API upload that carries a crop rectangle (the server resolves it; the convert step needs a `src`).
- Rev 61 (2026-11-03, swccg-guild/work#100): **PC printed labels from `gempdata/card_labels.json`.** The file is the
  copy of billbisco/swccg-gemp `card_labels.json` (2,544 PC faces: original title, errata mark, (AI)/(ALT) mark, concept
  credit, art credit, non-standard copyright line). `adapter.gemp_to_spec` applies it to every card: the original title
  as the `bottom-left` label (italic, or only its italic part, e.g. *Executor*: Control Station), the errata mark, the
  (AI)/(ALT) mark bottom right, the concept credit as the `concept` label, the art credit, and the copyright line when
  the card prints a Decipher line instead of the standard Lucasfilm one. Virtual Legacy cards take the original title
  as the slip caption.
  - **Art credit:** new `art_credit` section, the copyright line's mirror image about the art window; AGCn 51 px, white
    with a 1.6 px white stroke and a dark edge, as the PC prints it (Endless Legions: length and centre 0–1 px).
  - **Card data:** `gempdata/Light.json` and `Dark.json` refreshed from the PC's current card JSON (23 new VS27
    cards, including Do, Or Do Not & Wise Advice (V), 227_19; 28 updated).
  - **Left as found, explained in evidence/100/compare.md:** the PC sets its labels by hand, so they move a few px
    between sets: original-title label 0–1 px on VS26/27 but +7 px on VS0 (Master Qui-Gon); concept credit dx 6/−9;
    art credit 0–5 px. A Decipher copyright line copied from a scan (Do, Or Do Not & Wise Advice (V)) keeps the scan's
    smaller lettering, so CardMaker's standard copyright face runs longer.
- Rev 62 (2026-11-03, swccg-guild/work#118, Bill: "This is future proofing and important and avoids and legal issues"):
  card titles, deploy / forfeit numbers and the caption bullet are set in **Holotable Title**, our own font under the SIL
  Open Font License 1.1 (`assets/fonts/HolotableTitle/`: the OTF, OFL.txt, FONTLOG.txt, specimen and the sources and
  script that rebuild it byte for byte). It is traced from the PC's own Virtual card titles (each letter averaged over up
  to 1,166 printed instances), with spacing fitted to 689 measured letter pairs; no font file went into it. Fiorello CG
  is removed from the repository. Its cap height per px equals Fiorello CG's, so sizes carry over; titles scale 80 → 81.4
  (the interrupt fit) and the interrupts are re-fitted: 83.4 px, Light tracking 0.6, Dark 0.55 with a 0.6 px stroke (was
  2 px), Dark title box (404, 196). Accented letters and curly quotes are in the font, so `title_html` no longer draws
  accents over bare letters. Against the PC: title width within 1 px (median 1.0 px over 24 references, Fiorello CG
  2.0); the pixel difference is a few levels higher than Fiorello CG's on some long Light titles (deviation D2, Bill
  2026-11-03 7:08 PM: "if we fail, we just take what you have").
- Rev 63 (2026-11-03, swccg-guild/work#122, Bill: "how it approximates the other font but is still lacking"):
  documentation only. `assets/fonts/HolotableTitle/ACCURACY.md` records how close Holotable Title is to the PC's
  titles and where it falls short (per-card figures against Fiorello CG), and FONTLOG.txt points to it. No render change.
- Rev 62 (2026-11-03, swccg-guild/work#100 follow-up, Bill: "We need that to recreate the card exactly"):
  - **Every printing is its own card.** PC alternate-image printings share their card's gempId, so until now only one
    of them was reachable (the last one read, often the (AI) one). The plain printing keeps the gempId; each other
    printing is `<gempId>^<its extra parenthetical>` (`200_76^AI`, `200_95^Tatooine`), as in `card_labels.json`.
    145 more cards. Fills and typo corrections apply to every printing of the id.
  - **Labels match by printing.** `adapter.pc_labels_for` finds a card's labels by its PC image, so the (AI) printing
    gets its stamp and the Virtual Block cards (keyed `<set>_L<id>` here) get theirs for the first time.
  - **(AI)/(ALT) stamp** (`ai` label preset) with the Players Committee logo to its left
    (`assets/icons/pc-gameaid-named/pc-logo-stamp.png`). Measured on 105 PC AI faces: text right edge x 706, or 667
    when an errata mark follows; logo 52 × 30 px with an 8 px gap. Count Dooku (AI) and Imperial Decree (V) (AI)
    builds land within 1 px horizontally.
  - **Bottom-bar lines:** "In memory of …" dedications and other bar text use the `concept` preset, and so do the
    Virtual Block concept credits ("Original concept by James Booker, Worlds 2005": Master Qui-Gon (V) VB5 within
    2 px). Virtual Block errata marks are stamped at the strip's right end (E's left edge x 685).
  - **Copyright:** `card_labels.json` now records every card's copyright line, the standard one too; a card that
    prints none (Rescue In The Clouds (V)) gets none.
  - `compare_pc.py` accepts `<gempId>^<printing>` ids.
- Rev 64 (2026-11-03, swccg-guild/work#123, Bill: "let's work on tickets to replace Akzidenz-Grotesk and Craft Gothic"):
  lore, game text, stat labels, type banners, the © line and the "medium" labels are set in **Holotable Text** Light /
  Regular / Bold (`assets/fonts/HolotableText/`, SIL OFL 1.1), a modified Barlow Condensed (Light / Medium / SemiBold):
  narrowed (0.799 / 0.869 / 0.959), rescaled to the cap height per em and line metrics the templates assume, and
  widened or narrowed per character class so real card text sets to the same widths. Akzidenz-Grotesk BQ Light
  Condensed, BQ Condensed, BQ Bold Condensed and BE Medium Condensed leave the repository. No template setting changes:
  positions and line breaks match the Akzidenz-Grotesk build on the 24 reference cards (FONTLOG.txt has the figures).
  `data_uri` serves .ttf fonts as font/ttf.
- Rev 65 (2026-11-03, swccg-guild/work#124): destiny numbers, stat values and slip numbers are set in **Holotable Numbers
  Extended**, the bottom-strip card number in **Holotable Numbers Bold Italic** (`assets/fonts/HolotableNumbers/`, GUST Font
  License): TeX Gyre Heros Bold / Bold Italic widened and rescaled so flat-topped digits keep their height and
  baseline and digit spacing matches, with Extended digits 0-7 traced from the PC's own destiny numbers (6-240
  instances each, averaged) and 9 from the 6. Akzidenz-Grotesk Medium Extended and the PC's BE Bold Italic digit subset
  leave the repository. No template setting changes: destiny and stat positions match on the 24 reference cards.
- Rev 66 (2026-11-03, swccg-guild/work#125): Craft Gothic Heavy Extended leaves the repository. It had not been
  used since the VS13 location work (the parsec number is set in the stat-value face, now Holotable Numbers Extended);
  checked on 10 PC system cards covering parsecs 0-9: position, width and height within 0 px of the PC, pixel
  difference ~5. Every font in `assets/fonts` is now free software (FONTS.md).
- Rev 67 (2026-11-03, swccg-guild/work#124 follow-up): Holotable Numbers Extended keeps TeX Gyre Heros' own digits.
  The digits traced from the PC's destiny numbers (rev 65) matched a little better at 745 px but showed lumpy or
  rounded outlines at the 600-DPI master; Heros' drawn digits are crisp and closer to the PC's at render size
  (FONTLOG.txt). Positions are unchanged.
- Rev 68 (2026-11-04, swccg-guild/work#62, Effects; Bill 2026-11-03: neither Bardez's template nor the PC is assumed
  correct). Each element was checked against 13 PC Effects (Effect, Immediate, Political and Starting, both sides),
  12 printed Decipher Effects (745-px scans) and 10 PC no-lore Effects and Interrupt combos:
  - **Frames:** Bardez's Effect frames are 0.2-0.4 % small and sit 3 px (745) high-left of the printed card, the
    same error as the interrupts (Rev 59). A frame-only fit gives the same scale and offset against the PC and against
    the printed scans (to 0.5 master px): Light 1348×1938 at (140, 139), Dark 1352×1937 at (141, 141), rescaled with
    premultiplied Lanczos. Frame MAD against the PC 7-12 → 4-6, against the printed scans 8-12 → 4-6.
  - **Boxes and type:** title +6/−12 (Light), +5/−4 (Dark) master px, 83.4 px with the interrupts' tracking (Dark
    stroke 0.6); the title bar runs to x 1274 as the PC's does, and a title still too long starts at x 366 before it
    is condensed (`title_long_left`; PC two-name titles within 2 px at both ends, they were 15-45 px short); destiny
    −5 (Light) and +4/−8 (Dark); lore 4 px up, Dark first-line indent 80; banner 62 px, tracking 11.3, Light 4 px
    and Dark 6 px left, Dark 2 up; game text Light 2 up, Dark 4 down (line tops now equal the PC's on all 12 Dark
    references); set mark as the interrupts (68 px slot, digits 160, `set_ring`); expansion sphere Light 62 px at
    (1381, 406), Dark 59 px at (1382, 406); copyright 25.9 px, tracking 0.8, x 1420. All within 1 px of the PC (most 0)
    and the same against the printed scans where they print the element.
  - **Discs:** Episode discs under the sphere 6 px lower (Light, `ring_disc_dy`). New **Personal Force** disc
    (`disc-personal-force.png`, drawn by `make_personal_force.py`): the PC prints it on five Light Effects in the
    right margin at the text box top, stacked under a Skywalker disc 84 px apart; the margin discs on Light Effects sit
    in the PC's dark-red halo (`margin_disc_hole` may now be a colour, `margin_disc_hole_pad`).
  - **No-lore Effects and Interrupt combos (PC cards):** built from the template's own frame (`grown_frame`, lore
    window merged into the art window), banner and text box raised 276 px (was 290 and, for Dark Effects, the fixed
    `ds-effect-tall` frame whose banner sat 30 px (745) high; banner and first line now within 1 px). The Episode I
    disc sits in the left margin by the window top (`nolore_disc`), as the PC prints it. `ds-effect-tall` is now the
    Dark Effect template raised by `NOLORE_GROW` (VS12 #42 follows the PC's VB4 slip).
  - **Text:** the ▼ shorthand also applies when the object holds a bracketed aside and the Reserve Deck clause ends
    the sentence ("may ▼ an [Episode I] (or Coruscant) docking bay", never across "deploy phase"); 21 PC cards
    change, seven checked against their PC images.
  - **Unchanged on purpose:** `ls-jeditest-epic` and the Mission templates keep the pre-Rev-68 Effect boxes
    (`_LS_EFFECT_PRE62`, `_EFFECT_PRE62`) until their own Stories.
  - **Left as found, explained in evidence/62/checklist.md:** game text and lore widths (the fitter's tracking, #49);
    banner word widths ±5 px (letter widths of the banner face); the 1 px art cut; PC-only labels.
- Rev 69 (swccg-guild/work#174, Bill 2026-11-05: "Definitely the art from the remasters"; one Story for both Reflections Gold sets):
  set 15 opens in the card maker. `gempdata/ReflectionsGold.json` (from the wiki's RG pages): Remastered `15_N` (set
  `15`, expansion "Reflections Gold Remastered", gold sphere `set-reflections-gold-remaster.png`) and original playtest
  `15_No` (set `15o`, "Reflections Gold", original Decipher sphere `set-reflections-gold-decipher.png`, #50 R1). Art
  library: swccg-card-art `reflections-gold/` (cut from the Remastered renders; `original/` = the same windows cut from
  the 2001 playtest photos), used by both versions by default (`server.art_base`). Landscape cards set `wide` from the
  data; RG credits print as gold coins. Copyright year 2001. Tools: `tools/reflections_gold/`.
- Rev 70 (#174 render check, 620 cards against their RG-GEMP renders / straightened playtest photos): Remastered (set 15)
  prints no copyright line, as its renders; the original (15o) keeps 2001. Wide art recut at the full rg art box (the
  box's w,h had been read as x1,y1, so the picture was cut short and stretched). `rg-*` wide templates: title box
  (436,214,924,115), card type 64 px / spacing 3, game text 66 px, sphere and Episode I disc in red rings
  (`expansion_hole`), coins (1938,1386). Sites print the uniqueness dot and their Planet / Exterior / Episode I icons;
  Executor's subtype italicises _Imperial_.
- Rev 71 (Bill 2026-11-08: "anyone, human or AI, should be able to easily re-create any published version of any Star
  Wars CCG card from any Era … If you need to make updates to properly do this for Virtual Legacy … please do so"):
  **Virtual Legacy (2009-2014 Virtual Blocks 1-9 + shields) render from their own card, as printed.** Survey: 42 legacy
  cards across all blocks, sides and types against the PC's gifs (`res.starwarsccg.org/cards/legacy/…`, the printed
  layout). Systematic differences found and fixed:
  - **Art was zoomed/cropped** (art match r 0.14-0.99, median 0.61 on the 41-card sample): the scan path trimmed "silver" edges
    (`art_trim`/`legacy_scan`) and cover-fitted the rest. A Virtual Block slip keeps the top of the Decipher card it was
    pasted on, so its art *is* that card's library art. `tools/legacy/match_legacy_art.py` template-matches every
    library crop into every legacy gif → `gempdata/legacy_art.json` (1,040 of 1,203 cards; r ≥ 0.93, or ≥ 0.85 when the
    matched card has the card's title or original-title strip; cross-title hits follow the strip: There Is Another on
    The Way Of Things). Those cards open with `art: {kind: library, gempId: <Decipher card>}`. The rest (new PC art: AI
    printings, Clone Wars cards) use their own scan, mapped by the frame with **no trim** (trim kept behind
    `CM_LEGACY_TRIM=1` for comparison only). Sample after: median r 0.975 (27 of 41 ≥ 0.95, was 5), a second random 20: median 0.98, 19 ≥ 0.95; below 0.95 only full-art / no-frame cards
    whose window the metric cannot isolate (Admiral's Order, VB9 systems) and new-art Missions.
  - **No copyright line:** the slip keeps the Decipher card's line → `copyright_for(<set of the card it was printed
    on>)` (art match, else the original-title card, else the same-title card). `card_labels.json` lines (the PC's
    "Artwork not affiliated…") still win. Systems print none of ours: their picture is the whole scan, which carries
    its own line and side credits.
  - **No slip number:** `card_labels.json` `slip_mark` ("123", "85E", "2 • 26", "D60") → `number`.
  - **Expansion sphere** of renamed cards (Baktoid Armor Workshop): the printed-on card's set when no title match.
  - **Objective strip:** the original-title strip from the labels is kept ("Invasion (V)", it was overwritten by the
    front title), and a (V) title keeps its (V) ("Local Uprising (V)").
  - **Side credits** (`concept_credit_position` side/left side, `edge_text` right side) go into `margin_left` /
    `margin_right` like the OVS slips (Deep Hatred (V)); **"bottom bar" art credits** ("Image courtesy of …", VB AI
    cards) use the `concept` bottom-bar preset instead of the copyright's mirror.
  - **Episode I disc** on Virtual Block Objectives, Missions and Epic Events: left margin by the window top
    (`disc_left`, (200, 412) master), as printed (A Stunning Move, Hunt Down The Dark Acolyte, Deep Hatred (V)).
  - **Light Epic Events** keep the normal box (no `text_grow`) on Virtual Block cards: It Is The Future You See (V)
    prints the EPIC EVENT banner over a normal text box (r 0.29 → 0.97).
  - **"(Immune to Alter)" without the period** becomes the icon (Baktoid Armor Workshop; 7 cards).
  - **Virtual Block set mark** redrawn from the gifs: flat black face with a light edge over a white lower bevel, the
    number standing out of it, 92 % of the rev 41 size, ≈18 px higher and ≈8 px further left (745 px face) on the text
    box corner (6 cards checked, within ~2 px). Inline `{vb:N}` marks keep their place.
  - Renderer: a timed-out Chromium page is relaunched (it crashed the following jobs).
  **Recreating a version:** `GET /api/card/<id>` accepts the legacy id, the current GEMP card (12xx/601_x), a 22xx
  version card or `pc-legacy:<PC id>` (`gempdata/legacy_versions.json`, built by `tools/legacy/build_versions.py` from
  legacy-versions-v3.json: 2,783 aliases, 1,502 versions) and returns `versions`; `?version=<id|code|GEMP id>` puts
  that text on the card (`adapter.apply_version`); a `warning` flags the 143 sheet transcriptions whose inline icons
  were lost. The editor has a *Published version* picker. How-to: `docs/RECREATE-A-CARD.md`.
  **Left as found (open):** Virtual Block Mission banner (printed tan with the mission disc; ours silver); Dark
  Virtual Block shields printed with a red right edge (Death Star Sentry (V) and ~12 others) still use Decipher's cyan
  frame; Wampa (V) prints its art over the left frame; data-level differences (Galen Marek's blank lore, Padmé's
  FORCE-SENSITIVE, Kashyyyk "FORREST", Deep Hatred's uniqueness dot) are card-data/version questions, not template ones.
- Rev 72 (2026-11-08, batch agents' reports on the rev 71 version data): **Virtual Legacy versions follow
  legacy-versions-v4 and GEMP's version cards.**
  - `gempdata/legacy_versions.json` is rebuilt from **legacy-versions-v4.json** (v3 + the strict-audit card-list /
    Master List versions; 91 printings re-coded): 1,569 versions, listed in order (Original, PC-E1, PC-E2 …, v4
    `version_seq`), `label` = the code or "Original". Darth Vader, Betrayer Of The Jedi (1261_10): Original (2261_10),
    PC-E1 = the 2012 card-list text (2261_1010), PC-E2 = the Master List text (1261_10).
  - **22xx ids are read from swccg-gemp**, not computed: `build_versions.py --gemp <clone> --ref origin/master [--ref
    <open batch PR>]` reads every set22xx class's `LegacyVersion("<current id>", "<code>")` ("" = original); GEMP numbers
    versions in the order they were added (`n`, `n + 1000` …), so middle versions carry ids like 2261_1010, 2220_1036,
    2220_1156, 2261_1034, 2261_1065. 261 versions have a 22xx card; retired 22xx ids (blueprintMapping.txt) and back
    faces open the card. v4's own `gemp_22xx` is stale (it still names 2261_10 as PC-E1) and is used only without
    `--gemp`. This build: master `582181c1f` + PR #767 head.
  - **`is_version: null`** entries (82: capitals / punctuation only, waiting on Bill) are not selectable: the API returns
    them as `version_notes` (a 404 explains if one is asked for) and the editor names them under the picker.
  - **`[S]` / `[T]` in version texts are ▲ / ▼** (take into hand / deploy from Reserve Deck), as the slips print them;
    they had rendered as the Immune to Sense icon. The record always spells Immune to Sense out ("(Immune to Sense.)",
    "[Immune to Sense]", "[Immune To Sense]", the last now also an icon). GEMP / PC card data keep `[S]` as before.
    Checked against the slips: Rebel Leadership (V) original and PC-E1 (1230_109), Luke Skywalker (V) original (1210_105),
    •••Rodian (V) original (1210_20).
  - Version texts: two spaces after a sentence (the 2012-13 card list's style) become one and no longer count as lost
    icons (`icons_missing` 160 → 121; the warning stays for the real ones); a leading bare "3." on a Character (the pilot
    icon lost from a sheet / Master List text) is the pilot icon `{pilot:3}`. `?version=original` picks the original.
  - **"deploy phase" is never the ▼ verb:** the first Reserve Deck shorthand rule matched from "During your deploy
    phase, may deploy X from Reserve Deck" and printed "During your ▼ phase, may deploy X" (I'm Sorry (V) PC-E1, Boss
    Nass, every Operative). It now skips "deploy phase" and never runs across a second "deploy", like the #62 rule:
    116 card texts read "during your deploy phase, may ▼ X", Rebel Infantry "whenever you deploy a Rebel trooper, may
    immediately ▼ a Blaster Rifle"; Abyssin Ornament's STARTING clause keeps its words.
  - **Lore:** the PC Legacy JSON carries The Signal's Decipher lore on Jabba, This Is Your Last Chance! (1261_80); the slip,
    the PC image and the Master List print an empty lore box → `fill.json` `1006_L5619` lore "". Lore comes from the
    PC Legacy JSON plus `fill.json` (the recorded printed values), never from the Decipher card itself.
- Rev 73 (2026-11-09, batch agents' reports after B03–B34, swccg-gemp PRs #760–#788): **Virtual Block Missions,
  the [Vader] disc and the Setup icon as printed; version data rebuilt.** Measured on the PC gifs at 745 px (master
  px = 2 × (745 px + 35 / 36)), as rev 71 did.
  - **Mission / Critical Mission frames** (`tools/legacy/refit_mission_frames.py`, reads the rev 72 frames from git
    `240b511` so it can be re-run): the banner and the text box sat 17–33 px (745) too low and the banner was silver.
    Now as printed: Light (Hunt Down The Dark Acolyte, Assault On Muunilinst, Rescue On Geonosis, Kessel Run (V)) panel
    edge 1074, banner 1124–1218, text box from 1240; Dark (In The Hands Of The ISB, Galactic Domination, Spice Mine
    Operations, Defense Of Muunilinst) panel 1054, banner 1084–1190, text box from 1252 (the text box gains the rows,
    in mirrored tiles of its texture). Text box top vs the PC after: 0–10 px (745), was 35–45. Banner **cream**
    (Light 210,200,186) / **pale tan** (Dark 204,182,149) instead of silver, smoother on Dark as printed; panel tan
    darkened to the printed one (side margins: Light 189,151,112, Dark 164,129,88; ours were 210,177,139 / 204,170,130);
    MISSION ink grey (Light #322d33, Dark #504b49, measured). Dark: top corners cut at 45° with a lit edge, black text
    box 30 px wider to the right (the PC's runs to x 660 at 745, ours stopped at 645).
  - **Banner icon:** the Mission templates had no place for it. Setup (Rebel Aces, In The Hands Of The ISB, Kessel Run
    (V), the Critical Missions) or, on the Virtual Block 9 Missions, the faction icon (Clone Army: Hunt Down The Dark
    Acolyte, Assault On Muunilinst, Rescue On Geonosis; Separatist: Rally To Our Cause, Arena Execution, Defense Of Muunilinst),
    106 px at the banner's right end (Light (1274, 1118), Dark (1314, 1086)); template match on the gifs r 0.83–0.88.
  - **Left-margin disc:** Rebel Aces and Imperial Aces print the **Objective** icon left of the text box top (template
    match against the Game Aid icons: objective r 0.83 / 0.81, the next best 0.76); no other Mission does, so it is a
    per-card printed mark (`adapter.MISSION_DISC`, PC ids 5825, 6389), not derived from the card data (their
    Death Star II icon is the printed-on card's expansion; the DS2 Critical Missions print no disc).
  - **[Vader]:** Virtual Block 7 prints it as a round silver-rimmed disc, left of the text box top and inline; ours drew
    the PC's later square Game Aid icon inline and put it in the column of Darth Vader, More Machine Than Man. New
    `assets/icons/disc-vader.png` (`make_mission_frames.py --vader`: median of the six printed discs, aligned, from the
    gifs; no higher-resolution source), 82 px at (190, text box top + 34) (Vader's Bionic Limbs, Cape (V), Cybernetic
    Enhancements, Helmet, Mask; Darth Vader, More Machine Than Man), inline `{ga:disc-vader}` (legacy cards only; the
    column no longer carries it). Modern PC cards keep the square icon.
  - **Setup icon on an Epic Event:** Rise Of The Dark Lord prints it in the right margin at the text box top (47 px box
    at (664, 623), 745): `epic-event` template `banner_icon` (1398, 1318), 94 px. Only cards with a Setup icon draw it;
    no Decipher / OVS / modern Epic Event has one. The PC Legacy JSON drops its "Twisted And Evil:" paragraph (opened as
    1271_19 the API shows the recorded PC-E1 text with it).
  - **Versions** (`gempdata/legacy_versions.json`, rebuilt from legacy-versions-v4 at ai-team-skills `0ec9e00` and
    swccg-gemp master `823a035be`): 3,061 aliases, 1,565 versions, 312 with a 22xx card (was 261). Stat-only versions
    (`part: stats`, Bill B34) are versions: Jedi Survivor (V) Original destiny 1 → PC-E1 destiny 3; each version
    carries the stats it records and the API prints them. Version texts that lost icons are flagged more completely
    ("adds one and one .", "always A .", [W2-205]: 90 → 111); opened by the GEMP id alone such a version keeps the
    card's own text (`note`) instead of printing the lost-icon text on the current card. Straight double quotes in
    GEMP-copied version texts become curly ones (Rebel Aces' "May add 1 astromech.").
  - Unchanged: every one of the 4,467 Decipher, Reflections and modern cards builds the same render input as rev 72
    (card dicts compared one by one); the `epic-event` template only gained an icon position they never use; Original
    Virtual Set remasters render from their own transcriptions (untouched). Production renders before / after the
    deploy compared on 11 such cards (HANDOFF).
  - **Left as found (open):** the PC prints three Missions with a lower panel (Rebel Aces +77 px, Imperial Aces +86,
    Restore Freedom To The Galaxy +36 at 745: more art, shorter text box); ours keep the common layout. Vader's Mask /
    Helmet print a raised text box (other Effects' layout question, not the disc). Dark Mission panel bevel is drawn
    flat apart from the cut corners.
- Rev 74 (2026-11-10, Bill: "You need to apply more scrutiny to your CardMaker Creations" — Han Solo, Innocent
  Scoundrel (V) PC-E1: the Cloud City sphere sat on the lore box's edge, "otherwise" wrapped to line 2): **Virtual
  Legacy cards typeset and laid out as the PC's own cards.** Measured on the PC's vector master lists
  (`Virtual_Legacy_Final_Master_LS.pdf` / `_DS.pdf`, wiki; 1,050 cards, 337 full cards), not on the 350 px gifs.
  Tools, numbers and the build: `tools/legacy/typeset/` (README). Applies only to Virtual Legacy cards (`10NN_L…`,
  `1000d_L…`); Decipher, OVS, Reflections and modern PC cards render exactly as rev 73.
  - **Type:** the PC set game text and lore in Akzidenz-Grotesk BE Condensed: game text 7.14-7.4 pt on 7.42-7.5 pt
    lines with -5..+10 / 1000 em tracking, chosen per card; lore 6.2-6.4 pt. Our Holotable Text was fitted to the
    modern PC's narrower BQ Condensed, so Virtual Legacy lines held fewer words. New face **Holotable Text PC**
    (Regular / Bold, `assets/fonts/HolotableText/source/build_pc.py`): Holotable Text's own outlines with the PC
    face's advance widths and kerning pairs read from the PDFs (numbers only; FONTS.md). PC size N pt = N x 8.3333 px.
  - **Frames:** `gempdata/legacy_typeset.json` = per card (1,021 cards) the text frame's left edge, line width and
    first baseline, size, tracking, pitch, and the PC's own line breaks; per template defaults for the rest. Line
    width = the middle of the widths with which a first-fit line breaker reproduces the PC's breaks (841 of 999
    cards are reproducible that way; a Knuth-Plass composer matched fewer). Long text: size down in 0.05 pt steps
    and tracking to -6, as the PC did.
  - **Same words, same lines:** a card whose text has the master list's words breaks where the PC broke (the PC's
    composer sometimes broke early or kept "Yavin 4 site" together); any other text (a later version) is set by the
    rules. Check (`check_typeset.py`, game text of the 756 master-list cards whose text we hold, 2026-11-11): rev 73
    renderer 326 exact (43 %); rev 74 rules alone 540 (71 %), the rest mostly one word off on one line where our
    widths differ by 0.1-0.2 pt; with the PC's breaks 692 (92 %; most of the rest are check artefacts: the digit
    inside an inline set mark counts as a word). Lore of the PC-set full cards: 203 / 203 with the PC's breaks.
  - **Printed lore breaks (`lore_lines`):** the top half of a slip card is the Decipher card as printed, so its lore
    keeps Decipher's typesetting; a spec may carry the printed card's own lore lines (`lore_lines`, read off the PC
    image), which then decide the breaks (106 of the 242 uploaded recreations, 2026-11-11).
  - **Inline icons** take the PC's slot (6.6 pt = 55.5 px, an icon set over a run of spaces), whatever their width
    (Han Solo's pilot icon took 70 px and pushed "otherwise" to line 2).
  - **Raised text box:** a sixth line of game text on an Effect / Interrupt / Weapon / Device / shield raises banner
    and text box one line (first baseline 181.4 pt instead of 189.5 pt) as the PC did (Protocol Failure (V), Imperial
    Atrocity (V), Cane Adiss (V)), and so does every card the master list prints raised whatever its text (Return Of The
    Jedi (V) PC-E1 has five lines on the raised card); characters never were (the PC kept them to five lines). The art keeps its top and
    loses its foot (the slip was pasted over it), so a scan of the PC card no longer shows its own IMMEDIATE EFFECT
    banner inside the art window (batch B38 had painted two such files by hand).
  - **Pieces where the PC's card has them** (`render.PC_PIECE_FIX`, template match of each piece of our render into
    the master list's full cards, median per template, 745 px): expansion sphere (ls-character-alien +11,+10 — Han
    Solo; Light characters, effects, interrupts, weapons +7..+14 down), icon column (Light characters -4,+6 at 106 %,
    Dark +4,+6 at 108 %), Virtual Block set mark (effects / interrupts 6-8 px up), destiny and deploy numbers (Dark
    templates and starships 4-10 px up). After: every measured piece within 3 px (was up to 14).
- Rev 75 (2026-11-12, Bill: "update CardMaker to be able to create cards utilizing those old (bad) slips"): **Early
  Virtual slip** (`style: "early-slip"`, `early_slip.py`). The Players Committee's first sheet, Virtual Set #1
  (decipher.com/starwars/cardlists/virtual/VirtualCards1.pdf, 6 March 2002, Adobe Illustrator 9; VirtualCards1a.pdf
  the same 12 cards), was not drawn on Decipher's templates: flat vector strips cut out below their title label and
  laid over the bottom of the printed card. Measured on the vector PDF (all 12 slips): a black U as wide as the card
  (bar 8.95 pt, legs 8.66 pt, corners 3.8 x 4.5 pt), a flat band — characters a grey panel 55 pt high notched on the
  right at 32.9 pt (icons stay visible; Light 211/210/210, Dark 94/91/92) with the new deploy (white box) over forfeit
  (black box), Haettenschweiler 9 pt; starships a 12 pt band under the box (Light 35/140/212, Dark 45/86/174); weapons
  and devices (93/196/102, 14/131/54) and effects (201/52/93, 161/35/36) a 12 pt band across — a white text box with a
  0.5 pt rule (124.5 x 44.5 pt; starships 41.6 pt and 2.2 pt lower), game text Akzidenz-Grotesk BE Condensed 8/8 pt
  ragged right (our HolotableTextPC, the same advance widths), and the set mark "(1)•N" (Wingdings negative circled
  digit, Bold Italic number, 7 pt, white) in the bottom bar. The card under it is the Decipher printing (title without
  "(V)"); the slip is cut to its outline by default (`early_slip.paper: true` = the whole printed rectangle with its
  white paper, as on the sheet). Spec: `early_slip` = {kind, colour, deploy, forfeit, text, lines (printed breaks),
  set, number, under_text (the original card's own text where it shows), keep_v_title, paper}; a version record with
  `early_slip` opens on it (`adapter.apply_version`). Not on the VS1 sheet, so not measured: interrupts, locations,
  vehicles, creatures, objectives (band kind, Effect colours) — and later early sets were not found on Wayback
  (decipher.com hosted only VS1); every other card, template and style renders exactly as rev 74.
- Rev 76 (2026-11-12, template survey, ai-team-skills `shared/swccg-cardmaker/TEMPLATE-DIFFERENCES.md`): **White
  border** for the white-bordered printings (Premiere Unlimited, Revised A New Hope / Hoth / Dagobah, First and Second
  Anthology previews, the two-player sets). Compared on the wiki scans (Premiere Limited vs Unlimited Luke Skywalker,
  Raithal vs Raithal (Revised), ESB2P Chewie, Hoth / ANH Revised): only the outer border changes, black → white; frame,
  boxes, icons, sphere and copyright line are unchanged and stay where they are. Spec `border: "white"` (editor: Border →
  White; default black; GEMP set 104, ESB Two-Player, opens white): the bleed is white and a black card body (144,144,
  1343×1931, or 1931×1343 landscape) with corner radius `WHITE_BORDER_RADIUS` = 14 master px (measured on
  Premiere-U-L-lukeskywalker.png) sits under the frame, so locations keep their black starfield; text printed in the
  border (caption, number, labels) turns black. Black-border renders are byte-identical to rev 75 (checked on
  Luke Skywalker, Dejarik Hologameboard, Captain Yorr, Jabba's Palace: Audience Chamber, a Dark interrupt).
