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
- Rev 77 (2026-11-12, swccg-guild/work#283, Bill: "We also need to be able to re-create Japanese cards in Cardmaker"):
  **Japanese printings** (Takara 1997-98) as a language layer, `lang_ja.py`. Spec `language: "ja"` (editor: Printing
  language), default `en`; English renders are byte-identical to rev 76. Compared on the wiki's Japanese scans warped into
  the master by the frame edges (Darth Vader, Luke Skywalker, Admiral Ozzel; `tools/japanese/compare_ja.py`): Takara kept
  Decipher's frames, art window, destiny, icons, deploy / forfeit and sphere, and changed: uniqueness `＊` for `•`; title
  in a heavy gothic condensed to 91 % (Noto Sans JP 800, 67 px, x 395, 27 px higher); the character lore box taller
  (25 px up, 27 px down, chamfered, English side bevels blended away) with gothic lore 46.6 px / 58 px, justified, the
  first line pulled in 130 px a side; **one stat strip** instead of three boxes (black on Dark frames, the frame's light
  well on Light frames, black text), items at the English wells (two stats: the second mid-strip), labels translated
  (`LABELS`), figures full width; game text Noto Sans JP 500, 47.6 px / 57.5 px, justified, Japanese line breaking, Dark
  imperial box (335, 1656, 962); banners in katakana / kanji (`CARD_TYPES`) without the English tracking; copyright
  © 1997 (Premiere, ANH) / 1998 (Hoth) in the light face. Takara broke lines by hand and its leading varies card to
  card: `lore_lines` / `text_breaks` (editor: Line breaks as printed = each typed line is a printed line) set each line
  justified and unwrapped, so a line-end 。 hangs as printed. `{u:…}` underlines (Blizzard Walker, Admiral Ozzel).
  Font: Noto Sans JP (SIL OFL) in `assets/fonts/NotoSansJP`, installed in the container's fontconfig. Not yet: Takara's
  art shows ~4 % more picture (scale 0.95-0.97; our library art is the English window), types other than characters
  (they get the same text layer, unmeasured), Japanese location halves.
- Rev 78 (2026-11-12, template survey fixes; numbered 78 because the Japanese printings layer took rev 77 the same day; code comments say "rev 77"):
- Rev 78 two-sided Objectives (2026-11-12): the editor and `/api/render` render an Objective's **back face** with spec
  `face: "back"` (default front; a spec without it renders exactly as before). The back is built exactly as build_vs's
  batch path builds it (front card dict + `card["back"]`: back title, destiny 7, back game text, id + "b"); its picture
  is spec `art_back` — default (and `{"kind": "scan"}`) the card's own printed back from the GEMP data's `back.imageUrl`
  (every GEMP / Legacy Objective has one; the art library holds front windows only), `{"kind": "front"}` the front's
  picture, `{"kind": "none"}`, `{"kind": "upload", …}` / `library` as for `art`; `art.kind: "ovs"` keeps the remaster's
  own back art. The back's margin caption follows the front's (Decipher printings: none) instead of build_vs's slip
  default "<back title> (V)"; spec `caption_back` overrides. Editor (Objectives only): Face Front / Back and Back art
  (back scan / same as front / none); exports of the back are named `…_back.png`. Compared with the wiki Decipher-archive
  scans — I Shall Enjoy Watching You Die (EJP 110_6), Systems Will Slip Through Your Fingers (SE 7_136), In The Hands
  Of The Empire (7_300), Save You It Can (7_138): title, destiny 7, art window and text box sit where the front's do.
  Found and fixed: `*Place* out of play` and `*Immediately* retrieve` open their own paragraph on the printed Objectives
  (both faces, 23 cards), as *For* / *While* / *Flip* do (`adapter.objective_text`; unmarked 2010s PC text is marked
  too), and the back text now gets build_vs's TOKEN_FIX. Fronts without those words are byte-identical to rev 76
  (md5 checked on Hidden Base, Court Of The Vile Gangster, a character, a Dark site, a system, an interrupt). Not
  changed: the Light Objective frame (`objective-ls`) draws the expansion sphere lower and further right than the
  scans (it touches the destiny circle) — front and back alike.
- Rev 78 printing variants (2026-11-12): three misprint / finish variants, all off by default.
  **Uniqueness dot colour** — Eriadu (Jedi Pack, GEMP 102_7): first runs printed the Dark bar's uniqueness dot white
  instead of red (Collecting Encyclopedia 3.2 p.46, both printings side by side; wiki Jedi-D-eriadu-decipher-archive.gif
  is the corrected red one). Spec `bullet_colour`: `red` / absent = as printed; `white` (or `black`, or a #hex) recolours
  the location dot on the card's own-side bar (the other bar's plain dot is unchanged) and the leading dots of a card
  title. Editor: Uniqueness dot → Red / White (Eriadu misprint).
  **Forfeit box border** — Lando In Millennium Falcon (Enhanced Cloud City, GEMP 109_2): 1 in 20 per sheet printed a
  thicker black border round the forfeit value (Encyclopedia p.47 photo, normal and variant cards side by side, pdf
  image 1152×2048). Measured with a 3 px blur on the halftone: the black box is 1.79× the white deploy box's width on
  the variant against 1.27× on the normal card, i.e. ~12 master px more black each side (photo ≈ 1 master px per px by
  the game-text pitch); vertically the box grows up to meet the deploy box (~6-8 px, the photo is too soft to separate
  it). Spec `forfeit_box_border` (extra master px, default 0, max 40) draws a black rectangle that much larger than the
  frame's forfeit box under the value; use 12 for this variant. Editor: Forfeit box border (extra px).
  **Foil** — Reflections I-III foils (and any other card): spec `foil: true`, editor checkbox Foil. No wiki scan shows
  the foil; matched to collector photos of Reflections II foils (PriceCharting: Admiral Ackbar, Chewie With Blaster
  Rifle, Jodo Kast, Lord Vader, Home One): the silver frame's white splatter and bevels shimmer pastel rainbow (magenta,
  violet, cyan, green, gold) in broad diagonal bands; dark frames keep their tone with a faint violet / blue cast; the
  outer black border, the art and the text boxes stay as on a normal card. Drawn (`foil_html`) as three layers over the
  frame image, each masked by the frame PNG's own alpha (so art windows and location starfields are untouched) and
  clipped (even-odd path) round the lore / game text / location text boxes: a 118° repeating rainbow (1080 px period)
  multiplied at 50 %, the same screened at 16 %, and two soft-light gloss streaks at 70 %.
  Checks: renders without the keys (and with `bullet_colour: red`, `forfeit_box_border: 0`, `foil: false`) are
  byte-identical to rev 76 (md5 on Luke Skywalker 1_19, Death Star: Central Core 1_283, Alderaan system 1_121, Charming
  To The Last 1_236, an objective 7_135, Eriadu 102_7, Lando In Millennium Falcon 109_2).
- Rev 78 Split art (2026-11-12): **two-picture windows** of the Reflections II combo cards (Do, Or Do Not & Wise
  Advice, Ghhhk & Those Rebels Won't Escape Us, Sunsdown & Too Cold For Speeders …), for new cards and remasters.
  Measured on 24 printed combo scans (res.starwarsccg.org ReflectionsII-Light/-Dark large faces: 12 Light, 12 Dark;
  Ghhhk 745 px true colour, the rest 354 px GIFs): one straight stripe rising from lower left to upper right at 60.0°
  from horizontal (dx/dy −0.577 on every scan, centre ±1 px at 745 across all 24), its centre line crossing the window's
  mid-height 0.508 of the window width from the left (master x 821 in the scan window 240..1384 × 372..1150; it meets the
  top edge at ~0.70 and the bottom edge at ~0.31 of the width); width across the stripe Light 36 master px (20.5 px
  horizontally at 745), Dark 38 (22 px); two bevel facets split along its middle, soft ~1 px edges, no outline: Light
  silver, lower-left facet 226/225/222, upper-right 200/200/198 (median of 12); Dark red, lower-left 176/28/45, upper-right
  214/31/53 (Ghhhk; the GIFs show the same split darker, 138/25/37 and 167/14/40). Each printed picture is at the scale of
  the whole window and pushed against the stripe (Ghhhk's right edge at the stripe's top end, the TIE picture's left edge at
  its bottom end). Spec: `art2` = the second picture, same forms as `art` (`{kind: library, gempId, version}`,
  `{kind: scan, gempId}`, `{kind: upload, data}`; `none` or absent = one picture, rendering unchanged); `split` (optional)
  = `{angle: 60, x: 0.508, width: 36 Light / 38 Dark, color: "silver" | "red" | "#rrggbb" (two facets ±6/8 %) | "none"
  (default silver for Light, red for Dark templates), texture: "bevel" | "flat", fit1 / fit2: {zoom ≥ 1, fx, fy}}` — fx 1
  for picture 1 and 0 for picture 2 by default (pushed against the stripe), fy 0.5. `render.split_art()` composes the
  window (picture 1 left / lower, picture 2 right / upper, analytic anti-aliasing, stripe over the seam) and places it in
  whatever window the card has: the raised no-lore window (`_artwin`), the lore-merged window, the frame hole, or a lore
  card's normal window (Owen Lars & Beru Lars); landscape and system cards ignore `art2`. A scan picture is cut by the
  template's normal art box (a lore-box card's window). Server: `resolve_art(spec, split=True)` returns uploads whole
  (framed by fit1 / fit2, not by the upload's own zoom). Editor (Art): "Split art" checkbox (ticked on cards with no lore
  box or with art2), first / second picture from any card (title or GEMP id, library art, 4× or scan) or uploaded, zoom /
  left-right / up-down sliders for each picture, stripe angle, position, width, colour (auto / silver / red / own colour /
  none), finish (bevelled / flat), reset. Checks: md5 of 9 renders identical before / after (Beru Lars 1_2, Death Star:
  Central Core 1_283, Alderaan system 1_121, Alter 1_234, objective 9_151, and the combos 10_7, 10_39, 10_50, 10_18 with
  their own scans), and `art2: {kind: none}` = no art2; composed from library art and compared with the scans: 10_7 = 4_21
  + 7_81, 10_39 = 2_132 + 4_150, 10_50 = 1_230 + 3_113, 10_22 = 5_68 + 2_49 — stripe position, angle, width and colour
  within ~1 px (745) of the printed cards; Decipher's own crops of each picture differ a little (adjust with fx / zoom).
- Rev 78 Podracers (2026-11-12): **Episode I Podracers** (Tatooine Anakin's 11_47, Ben Quadinaros' 11_95, Dud Bolt's
  11_96, Sebulba's 11_97, Teemto Pagalies' 11_98; GEMP has five, not six). Measured on the wiki's 497×692 Decipher
  archive scans (card body 24..471 × 24..669, master = 144 + (scan − 24) × 3) against our Effect renders: the printed
  Podracer top differs from the Effect frame — the title bar runs straight across (ridge master y 336..360, no notch) and
  the lore box is a plain rectangle 276..1350 × 402..603 (Light: silver box 255..1361 × 393..612), lore flush left with no
  first-line indent (text x 320..~1310); the type disc, destiny, art window, banner "PODRACER" and text box are the
  Effect's (within 5 px). New templates `ds-podracer` / `ls-podracer` (`build_vs.template_for`: slip type Podracer;
  frames from `make_podracer_frames.py`, built from our own Effect frames: band refilled from the clean rows under the
  old lore box, header carried down, the Effect's own ridge profile and box rims; the frame's green Effect icon under the
  podracer disc darkened). The **pilot flag badge**: the flag picture in a recessed window right of the disc — Dark
  master 366..552 × 183..327 (scan 98..160 × 37..85), Light 357..546 × 174..327 — drawn with a 14 px CSS bevel; the
  title then starts at x 611 (printed bullet 618) instead of 403. Flags cut from the wiki scans (the Holotable faces are
  350×490, lower) by `tools/cut_podracer_flags.py`, 6× Lanczos + unsharp mask → `assets/icons/podracer-flag-<slug>.png`
  (anakin, sebulba, ben-quadinaros, dud-bolt, teemto-pagalies; the window is ≈4:3, not square). Spec keys:
  `podracer_flag: "<slug>"` (set by `adapter.finish` from the title for the five cards; `"own"` with
  `podracer_flag_data`: a data-URI image, resolved by the server like the set symbol → card `podracer_flag_file`);
  no flag → no badge and the Effect title position. Editor: Card type "Podracer" is now in the list; a Podracer shows
  "Pilot flag" (the five, None, Your own) and an upload. Checks: before/after sheets of all five against the scans;
  non-Podracer renders byte-identical to rev 76 (Luke Skywalker 1_19, Death Star: Central Core 1_283, Alderaan System
  1_121, A Few Maneuvers 1_70, Carbon Chamber Testing 7_296, A Bright Center To The Universe 7_218, 1_47). Not changed:
  the printed Podracers set their game text a little larger/narrower than our Effect box (the shared Effect text box).
- Rev 78 objective sphere (2026-11-12): the expansion sphere on printed Objectives sits in the purple margin right of
  the art, clear below the destiny circle. Measured (ring fit on body-normalised 745 px scans) on 20 Light faces (Hidden
  Base / Systems Will Slip, Mind What You Have Learned / Save You It Can, Rescue The Princess, Rebel Strike Team, There Is
  Good In Him, Watch Your Step, Plead My Case, We'll Handle This, We Have A Plan, Quiet Mining Colony, You Can Either
  Profit, fronts and backs) and Light Epic Events (Attack Run, Deactivate The Shield Generator, Boonta Eve, Inner
  Strength): centre (678.5, 159.5) at 745 px = master (1427, 391); 10 Dark faces (Carbon Chamber Testing, Endor
  Operations, Bring Him Before Me, Coruscant, R3, Theed, Enhanced CC / JP): (676, 166) = master (1422, 404). The sphere
  with its black ring is ~29 px across at 745 = 58 master. `objective-ls` (and `ls-epic-event`, which copies it)
  expansion_ring (1412, 295) -> (1398, 362), `objective` -> (1393, 375); expansion_size 70 -> 58. No new spec keys; the
  Episode I disc under the sphere (Theed-era) follows it down. Every other template is md5-identical (character, Dark
  site, system, interrupt, effect, Admiral's Order, starship, Dark Epic Events Target The Main Generator / Boonta Eve,
  a Virtual Objective). Not changed: the Dark Epic Event template (`epic-event`) is in the right place but draws its
  sphere at 70 px vs ~58 printed; printed Theed Objectives carry the Episode I disc in the LEFT margin, not under the sphere.
- Rev 79 (2026-11-12, swccg-guild/work#52, Characters: Rebel / Imperial plates with the Republic, First Order and
  Resistance discs; deployed 2026-11-12). Measured with `compare_pc.py` on 10 PC
  characters (VS24-27; Light: Chewbacca Of Kashyyyk (V), Obi-Wan Kenobi Jedi In Exile, Captain Han Solo (V), Finn
  Resistance Hero, Corporal Rushing (V); Dark: Sil Unch (V), Captain Moden Canady, Cardo, Warrant Officer
  Bachenkall, DS-61-3 (V)); every per-element offset was the same on all five cards of a side.
  - **Frames:** a frame-only affine fit (ECC, element boxes and art window masked; `tools/pc_characters/`) gives the
    same scale and shift on every reference of a side (to 0.01 px): Light `ls-character-rebel` 0.4 % too large and
    2.3 px (745) right / 2 px high → 1426×1972 at (133, 139); Dark `ds-character-imperial` 0.3 % too small, 1 px high
    → 1348×1938 at (142, 143), the same error as Bardez's Effect frames (Rev 68). Resampled with premultiplied
    Lanczos (`refit_frame.py`, sub-pixel rest baked in).
  - **Boxes** (master px; Light / Dark): title +10/−4 / +30/0 (Dark bar end kept at x 1276: width 872); destiny
    −8/+2 / +4/−4 (Light: the digit sat 3 px (745) low in the ring); stat row −4/−2 / +6/+4; icon column −14/−4 /
    +2/+6; set mark −5/+6 / +12/+12; deploy and forfeit 2 px left (Dark also 5-6 px down); copyright 13 / 16 px left;
    expansion sphere 4 down (Light) / 2 right, 8 down (Dark); swapped affiliation disc (`disc_at`) (189, 184) /
    (195, 183); Episode I disc under the sphere (`ring_disc_dy`) 8 / 6.
  - **Dark stat squeeze:** the Dark wells are tight, so the label-value squeeze (render JS) had shrunk the labels to
    about ×1.0 against the PC's ×1.1. New template key `stat_min` (smallest label-value gap, right margin) = (22, 14)
    on `ds-character-imperial` (default 28, 18 elsewhere): POWER / ABILITY labels and values now within 1 px of the PC.
  - **Result** (10 references, 745 px): every title, destiny, icon column, set mark, deploy, forfeit, copyright and
    swapped disc within 1 px (one set mark 2 px); frame MAD 11.6 → 4.4. Regression (13-card sample of the 115 VS1-17
    remasters on these two templates, art-less): every card changes, frame and boxes only (Light ≈10 % of pixels,
    Dark ≈4 %), as intended. Evidence: swccg-guild/work evidence/52/.
  - **Left as found** (evidence/52/checklist.md): lore and game text line widths and wraps (the fitter, #49), art
    credit and margin strip faces, the Dark third (wide) stat box 1-2 px; Bardez XCF and printed-scan cross-checks
    (R7, AC7) not yet done.
- Rev 80 (2026-11-12, swccg-guild/work#283, Japanese printings part 2): **Effects, Interrupts, Devices** measured against
  the wiki's Japanese scans (`tools/japanese/compare_ja.py`, which now also finds the frame inside PSA / SWCA slabs).
  Takara used the same lore box on every one of these types whatever Decipher's box (`lang_ja.TEXT`, templates
  `ls|ds-effect|interrupt|device|weapon`): box (281, 359)-(1348, 600), text 303-1336 from y 362, first line pulled in
  125 px a side; game text (284, 1652, 1054 × 360), the English box's side bevels blended away on Dark frames as on
  characters. Text weight 600 (was 500; Takara's gothic is heavier). Takara fitted each card: with printed lines
  (`lore_lines` / `text_breaks`) the size follows the longest line — lore shrinks (Astromech Shortage, 27 characters,
  ~37 px), game text is first condensed to 90 % (長体) and then shrinks (Droid Detector, 26 characters, leading 51 px).
  Figures, Latin letters and + － ＞ ＜ ＝ ／ print full width (３フォース, 能力値＞２, Ｒ２－Ｄ２); a number of two or
  more digits stays half width (ライフフォースが15より); spec `halfwidth: true` keeps text as typed (`lang_ja.fullwidth`).
  Titles on every Japanese card: glyphs 73 px tall (Noto Sans JP 800 at 79 px, condensed to 78 %; was 67 px / 91 %,
  ~11 px short on the rev 77 characters too), x 386, condensed further when wider than 790 px (Luke Skywalker 787,
  Charming To The Last 730; `.jatitle` JS). Banner condensed to 95 %. The character lore box is absolute too (Vader's rev 77
  box): Luke Skywalker's English box is 30 px wider, the Japanese one is not. After rev 79 (#52) moved the Dark
  character stat boxes, the Dark Japanese strip and game text were refit (Vader: strip within 2 px, same printed lines). **Help Me Obi-Wan Kenobi**: slip type
  Effect with the card type left as USED INTERRUPT draws Takara's misprint (Effect frame and icon, interrupt banner).
  Samples (same printed lines as the scans): Astromech Shortage, Affect Mind (Effects), Charming To The Last (Lost),
  Emergency Deployment (Used), We're Doomed (Used), Warrior's Courage (Lost), Blue Milk (Used Or Lost), Electrobinoculars,
  Droid Detector (Devices), Help Me Obi-Wan Kenobi. Starting Interrupts were never printed in Japanese. English renders
  byte-identical to rev 79. `tools/japanese/make_sample.py` builds a sample from a wiki page "<Card> (Japanese)".
- Rev 81 leftovers (2026-11-12): two fixes on Objectives / Epic Events, measured on printed scans (body-normalised to
  745 px; master = 2 × (x + 35), 2 × (y + 36)). **Dark Epic Event sphere** (`epic-event`): ring fit on 7 printed Dark
  Epic Events (Target The Main Generator, Commence Primary Ignition, Epic Duel, That Thing's Operational, Boonta Eve
  Podrace (Dark), If The Trace Was Correct, Deep Hatred; the PC's With Thunderous Applause agrees): centre (675, 166.4),
  ~29 px across incl. its black ring = master (1420, 405), 58 px; `expansion_ring` (1390, 373) -> (1391, 376),
  `expansion_size` 70 -> 58 (renders now fit (674.5–675, 166), r 14). **Episode I disc in the left margin**: printed
  Episode I-era Objectives (We Have A Plan, Invasion, Plead My Case, The Hyperdrive Generator's Gone, My Lord Is That
  Legal?, No Money No Parts No Deal!, We'll Handle This, Let Them Make The First Move, fronts and backs), Epic Events of
  both sides (Boonta Eve Podrace Light / Dark, I Did It!, Inner Strength, If The Trace Was Correct, Deep Hatred) and the
  PC's Virtual ones (Hunt For The Droid General, Twin Suns, Communing, How Liberty Dies, Revenge Of The Sith; the
  Episode VII disc too: Be With Me, Tracked Fleet) print the disc in the left margin under the card-type disc, not under
  the sphere. Half-level edge on 11 faces: centre x 67.2, Light y 163, Dark y 168.5, 27.5–29 px across = master
  (205, 397) Light / (204, 410) Dark, 56 px. New template key `ring_disc_left` = (cx, cy, size): `objective-ls` and
  `ls-epic-event` (205, 397, 56), `objective` and `epic-event` (204, 410, 56); an `episode1` / `episode7` ring icon
  goes there (one disc), other discs keep their places; legacy `disc_left` (Virtual Block, (200, 412) 58 px) and the
  no-lore `nolore_disc` are unchanged. No new spec keys or editor controls. Checks: before/after sheets against the
  scans; renders of every other template md5-identical (Luke Skywalker 1_19, Death Star: Central Core 1_283, Alderaan
  1_121, Charming To The Last 1_236, objectives 7_135 / 9_151 / 7_136 back, Light Epic Events Attack Run 2_42 and
  Deactivate The Shield Generator 8_43, effect 1_72, 4_19, combos 10_18 / 10_22). **Episode I disc picture**
  (second commit): the printed disc (left margin and under the sphere alike: We Have A Plan, Hunt For The Droid
  General, Communing, I Did It!, A Tragedy Has Occurred, Boss Nass, Captain Panaka, A Remote Planet) is a black disc with
  a tall serif "I" (0.80 of the disc, stem ~0.09, serifs ~0.29 wide) over bright white, heavy, wide "EPISODE" (cap height
  ~0.14, ~0.88 wide, centred at 0.48) that reads as a white bar at card size; our old `ep1-disc.png` had a short "I"
  (0.61) and thin grey serif lettering that vanished. Redrawn by `tools/make_ep1_disc.py` (232 px, Holotable Text Bold
  stretched to width, stem cut through the S with a thin black gap); one picture serves every place the disc prints.
  Cards without an Episode I disc render md5-identical (1_19, 1_283, 1_121, 1_236, 7_135, 9_151, 2_42, 3_115, 10_22).
- Rev 81 Combo template (2026-11-12, Bill: Do, Or Do Not & Wise Advice against its printed card — window corner,
  sphere, copyright line): the **no-lore combo cards** (Reflections II and Coruscant Effects / Interrupts, and the
  PC's reissues, which print the same corners) now follow the printed frame. Measured on the 745 px true-colour scans
  (Ghhhk & Those Rebels Won't Escape Us, Houjix & Out Of Nowhere) and checked on the 354 px GIFs of all 24 Reflections II
  combos, the four Coruscant combos and four PC reissues (master = 2 × (745 px + 35 / 36)):
  - **Window top corners** (`combo_corners()`, replacing the rev 30 45° shear on these templates): each corner column of
    the merged window is moved down by a drop profile from the top of the window's edge band, so the frame's own bevel
    bends into the corner with its shading; the opened rows are filled with the side margin's per-row median colour and
    grain, blended into the row above. Dark: straight 30° chamfers, left 82 px down × 144 wide, right 78 × 136 (printed
    (83,192)→(155,151) and (590,151)→(658,190) at 745). Light: a rounded step under each lobe, 74 / 70 px down, flat 12,
    S-curve over 118 (printed: rounded step at y 182, ~40° rise to the top edge at x 155).
  - **Light title-bar lobes** (`combo_lobes()`): the printed silver bar bulges round the type disc and the destiny circle
    (rim lower edge at 745 y 157 / 152; the Effect / Interrupt frame's bar runs flat at 141): circles (264, 216, R 170)
    and (1366, 228, R 148) painted below the bar, silver body from the bar above, 12 px white rim.
  - **Expansion sphere**: centre Dark (1420, 404), Light (1425, 411), 56 px with its own black ring and no extra hole
    (printed ring 28 px, purple 22 px at 745; it sat 15 px (745) low, 5 left and ~10 % heavy), with the frame's ring
    round it (Light red paint, Dark lighter rim) — template keys `expansion_bare`, `expansion_halo`.
  - **Copyright line**: centred at master y 798 (printed run 210..519 at 745; it ran 333..618), same face, size and x.
  - **Art**: the window art covers the frame's whole opening (no black sliver at the right edge), and the card's own
    combo scan (Holotable face, 745 × 1039 or scaled) is mapped by the Holotable card body (37, 36)..(708.5, 1001.5)
    instead of the detected silver bbox, which was 3-4 % small on the 354 px GIFs (the printed frame and copyright
    showed inside the window).
  No new spec keys: the templates `ls-effect`, `ls-interrupt`, `ds-effect`, `ds-interrupt`, `ds-effect-tall` carry
  `combo_corners` (light / dark), used only with `no_lore_box`; constants `COMBO_CORNERS`, `COMBO_LOBES`, `COMBO_SPHERE`,
  `COMBO_SPHERE_HALO`, `COMBO_COPYRIGHT_CY` in render.py. Checks: md5 of renders identical before / after for Luke
  Skywalker 1_19, Dark site 1_283, Alderaan system 1_121, Effects with lore 1_42 / 1_208, Interrupts 1_70 / 1_234,
  objective 7_135, starships 1_140 / 1_299, the lore combos Owen Lars & Beru Lars 10_18 / Artoo & Threepio 10_2 and the
  carbonite captive 200_16 (no-lore character, keeps the rev 30 shear). Left as found (shared with every card): the
  copyright's ® is set as a small superscript where Decipher prints it full size; the Dark Interrupt frame's type disc
  shows red streaks on its right edge; title widths 2-4 % wider than printed on long combo titles (the fitter).
- Rev 81 Podracers (2026-11-12): every remaining difference between our five Podracers (11_47, 11_95-98) and the wiki's
  497x692 Decipher archive scans fixed (master = 72 + 3 x scan px; checked by line boxes, column profiles and template
  matching on all five). **Frames** (`make_podracer_frames.py`, rebuilt, no seams at 4x): Dark header between the old
  notch and the new ridge (341..363) is a harmonic (Laplace) fill from the header, disc rims, strips and body (no mirrored
  rows), the side strips blended straight down, the ridge is the Effect's own straight ridge as a ratio to the header,
  stretched across; Light silver bar warped down column by column (bar above the Effect's bevel resampled to end at 342;
  lobe columns only cut), the Effect's straight bevel stretched across (342..360), paint 360..393 from under the old lore
  box with its big flakes cloned out, the stamped marks under the destiny circle and the arrows by the engine disc
  inpainted. Printed geometry: destiny circle Dark (-2, +5) / Light (+12, +15), type disc socket Dark (-1, +11) / Light
  (-8, +6), art window + banner 5 px lower, text box foot 6 px lower (bottom bevel pressed, edge kept). **Templates**
  (`ds-podracer` / `ls-podracer` only): lore 59.6 px (`lore_css`, new template key merged into LORE_CSS; the Effect's 58),
  lore x 317, y 406; game text 63.9 px / 63.75 px pitch in its own box Dark (312, 1666, 1006, 335), Light (312, 1664,
  1050, 330) (printed wrap limit Dark between 1002 and 1010 px of advance; every printed line break of all five now
  reproduced); title x 617 (bullet 621), y 200, tracking 0.15 / 0.3; destiny box (1312, 197) / (1325, 206) (the printed
  digit sits 4-6 px above the circle's centre); `disc_at` (192, 187) / (185, 182); expansion sphere 56 px at
  (1380, 407) / (1382, 417), `expansion_inset` 2 (thin outline; new key, default 4); Episode I disc 58 px centred (1408,
  536) (`ring_disc_size`, `ring_disc_dx`, `ring_disc_icons` new keys, defaults = before) drawn with
  `icons/ep1-disc.png` (the one measured disc of the text-and-icons pass; the pod2 `ep1-disc-decipher.png` was dropped);
  banner "PODRACER" 59.5 px, spacing 10.8, box (269, 1511/1512); art (254, 668) / (244, 666); copyright `copy_ls` 1.0 in
  box (1420, 661 / 666) (printed 735..1352). **Teemto Pagalies' Podracer** lore set by hand ("is designed" starts line
  2): `gempdata/fill.json` "11_98": "loreLines" -> spec `lore_lines` (adapter.gemp_to_spec: any card's fill.json
  loreLines now carry the printed lore breaks). Checks: non-Podracer renders md5-identical (Luke Skywalker 1_19, Death
  Star: Central Core 1_283, Alderaan 1_121, A Few Maneuvers 1_70, Carbon Chamber Testing 7_296, 7_218, 1_47, Tatooine
  Effect 11_68 and Interrupt 11_26 with the Episode I disc, 14_20). Not changed (outside these templates, for the lead):
  printed Tatooine copyright reads "... DECIPHER INC" with no period and a full-size circled R (ours "INC.", small R:
  adapter.copyright_for, all 2000+ sets); printed lore / game text use curly apostrophes (Anakin's, owner's, doesn't);
  the printed Tatooine sphere is octagonal (our tatooine sphere icon is round); the shared `icons/ep1-disc.png` (VS14,
  67 px) differs from Decipher's printed disc on every Episode I-era Decipher card.
- Rev 81 sphere and copyright audit (2026-11-12): the expansion sphere and the vertical copyright line of every
  Decipher-printed template other than the no-lore combos, Objectives and Epic Events, measured against the printed
  cards. 166 cards (2-6 a template, every era: Premiere, ANH-JP, SE-DSII and the premium sets, Reflections II-Theed)
  rendered and compared with their printed faces (Holotable 350 / 745 px faces and the wiki's Decipher archive scans),
  each scan registered to our render by an affine ECC fit of the whole card; sphere found by multi-scale template match
  of Decipher's own sphere, copyright line by its ink extent and by template-matching our line into the scan.
  - **Scope switch:** new card key `decipher_print` (set by `adapter.spec_to_card` for a card of a Decipher set, or a new
    card with no Players Committee set mark). Only those cards change: VS remasters, PC and Virtual Block cards keep
    the templates as fitted to the PC (md5-identical, 13 cards checked: VS0-27 characters / interrupts / sites /
    starships / effects, four Virtual Block legacy cards, Reflections Gold).
  - **Sphere** (`render.DC_PRINT[template]["dc_sphere"]` = centre x, y and diameter, master px): Decipher prints it
    56 px across with its own dark rim, in a hole only 1 px wider, the frame's bevel (`DC_SPHERE_BEVEL`, a 6 px ring
    pulling the frame to mid grey) round it; we drew 58-66 px inside a 3 px black ring. Positions moved by up to
    29 master px (Light alien characters: 14.7 px (745) right, 4 down); Light devices, weapons, vehicles, starships,
    shields, Dark vehicles and creatures 4-5 px (745) down; Dark starships 5.5 px left; Jedi Tests 6 / 5.5 px right /
    down; wide starships / weapon 8-10 px down; sites 3 px right and 50 → 56 px; systems 8 px left / 4 up, in a dark
    grey ring (`dc_system_ring`). Episode I discs under the sphere follow it (`dc_template`). Residual on the sample
    after the fix: ≤ 1 px (745) on every portrait template, ≤ 2 px on wide / site / system.
  - **Copyright line** (`DC_PRINT[...]["dc_copy"]` = centre x, y; `dc_copy_ink`, `dc_copy_size`, `dc_split` for
    systems, `dc_copy_unless_scan` for full-art Admiral's Orders): Decipher's line is taller and more condensed than
    ours and centred beside the art. New typesetting `DC_COPY` (applies to every Decipher-printed card, the combos,
    Objectives and Epic Events included, at their own positions): Holotable Text Bold 28 px condensed to 83 %,
    word-spacing +5, © and ® as full-size circles (25 px, 2.2 px ring, 18 px letter) where we printed a small superscript
    ®; run length now within 2-3 px (745) of the crisp scans (was 15-25 px short). Centres moved: Dark characters,
    devices, weapons 8-9 px (745) right (Imperial 16 px: rev 79 had fitted it to the PC), Dark shields 5.5, Light 1-4;
    Dark effects / interrupts / shields 4-5 px up; Jedi Tests white (was black) and 11 px right; creatures black (was
    white); sites black (was white), 20 px lower and slightly larger; systems' split halves 3 px lower. Residual ≤ 3 px.
  - **Wording** (`adapter.copyright_for`, read on ≥ 4 scans a set): 1995-98 `TM & © y LUCASFILM LTD.  TM, ® & © y
    DECIPHER INC.`; Special Edition, Endor, Death Star II, Enhanced Cloud City / Jabba's Palace, Third Anthology, JP
    Sealed Deck `© LUCASFILM LTD. & TM.  TM, ® & © y DECIPHER INC.` (we printed "TM & © 1998 LUCASFILM" on all of
    them); Reflections II-Theed `© y LUCASFILM LTD. & TM.  TM, ® & © y DECIPHER INC` with no final period; Coruscant
    `TM, ®, & ©`; Enhanced Cloud City no final period. Years corrected: Premiere Two-Player 1995, ESB Two-Player 1996,
    Enhanced Cloud City / Jabba's Palace 1999, Third Anthology and JP Sealed Deck 2000. Two spaces before the Decipher
    half on every printing. PC slips keep their own form (`copyright_for(set, decipher=False)`).
  - **Not changed here (other templates' owners / not near the elements):** Jedi Test frame (printed silver with olive
    speckle, art window and banner placement differ), creature frame, ANH site frames (printed blue), the wide
    starship's type icon. Evidence sheets: per template scan | before | after with x4 sphere and x3 copyright zooms.
- Rev 81 shared Effect / Interrupt frames and title fitter (2026-11-12): measured on 100 printed Decipher Effects and
  Interrupts (the PC's 2x .png faces / 350 px .gif faces, sets 1-14, both sides, registered to our renders by the card
  body) and 15 PC Virtual Effects / Interrupts as control.
  - **Dark Interrupt type disc** (`ds-interrupt.png`, all printings): the swirl was Bardez's Light disc shifted 5.5 px
    left, leaving red streaks in the disc's right edge. Replaced inside the ring (centre (125.75, 108.54), r 68.6 frame
    px) by the Light Interrupt disc, centred as the PC and the printed cards centre it. PC Dark Interrupts change only
    in that 75x75 px (745) square; nothing else in any PC render changes.
  - **Decipher printings** (card `decipher_print`; spec key `decipher_print` true / false; absent = a Decipher set's
    own card, GEMP set 1-199, no PC set mark, not OVS, English; the editor's "As Decipher printed it (1995–2001)"
    checkbox; custom cards and PC / VS / OVS cards keep the PC look and render pixel-identical):
    - *Title setting* (template key `decipher_title` = (dx, bar end, fit right, lead) on the four templates and
      `ds-effect-tall`): normal titles were already within ±1 % of the printed width; Light titles start 8 master px
      left of the PC's (printed ink 3.9 px (745) left on 32 Light cards, the PC 0.8); the bar runs to x 1274 on all four
      (`ds-interrupt` condensed at 1183: 7_266, 12_156 were 8 % short). A title longer than the bar is not moved left and
      condensed (the PC's rule) but set smaller with its baseline kept, scale k = (1248 − x + 140) / (w + 140), ending at
      x 1248 and starting further left the more it shrinks (JS `data-dfit`). 19 long printed titles (combos, 36-46
      characters): width within 2 % on 14 (There Is No Try & Oppressive Enforcement 436 → 430 px, You Cannot Hide
      Forever … 435 → 434), height now scales as printed; Decipher hand-set four combos smaller than needed
      (12_152, 12_135, 12_53, 12_51: 4-16 % narrower printed).
    - *Ink* (template key `decipher_tone` = (side, disc kind, disc circle)): our frames carry the PC's colours (within
      5 levels of the PC's cards); Decipher printed the Dark frames a deeper crimson (left margin 181,1,46 against our
      186,32,55; bright margin 204,64,77 against 214,85,86), silver not cyan chips on the Light red margins, and redder
      Interrupt / yellower Effect discs. `make_decipher_tone.py` fits `assets/frames/decipher-tone.npz` (a 3D colour
      offset table per side on frame pixels, blacks pinned; gain-gamma curves per disc) on half the cards;
      `render.decipher_toned()` recolours the frame once (cached in out/). Held-out half: Dark frame MAD 18.0 → 9.4,
      Light 19.2 → 17.7 (texture-limited), disc means within 2-4 levels. Podracers (Tatooine) get the frame tone.
      Note the PC's errata re-renders (Ghhhk & Those Rebels Won't Escape Us 10_39, Ghhhk 2_132) carry the PC's
      colours, not Decipher's: they are not printed references.
  - **Checked, unchanged:** left window bevel against the PC +0.4 px (745); against Decipher printings of sets 1-8 our
    bevel sits 1.4 px right (25 cards, 0.6-3.2), sets 9-14 −0.3 px; printed window and lore-box tops ~2 px lower than
    ours/the PC's. These are Decipher-only geometry differences of ≤ 1 scan pixel; not warped this rev.
  - **Regression:** md5 identical before/after for 25 cards of other templates (characters, sites, systems, starships,
    vehicles, weapons, devices, creatures, Objectives, Epic Events, Admiral's Orders, Jedi Test) and for PC Effects /
    Light Interrupts; PC Dark Interrupts differ only in the disc.
- Rev 81 text and icons (2026-11-12): three findings from the printed cards, fixed together.
  - **Quotes and apostrophes** (`webapp/adapter.py`; gempdata unchanged, converted when the spec is built). Checked on
    printed faces from Premiere to Theed Palace, the PC's Virtual Sets 1-27 and a Virtual Block 3 slip (Admiral Ackbar
    (V)): every era prints typographic marks, so the rule is the same for all cards that come from GEMP data
    (the Original Virtual remasters keep their own transcribed text). Titles, captions, lore and game text print ’
    for every apostrophe (Han’s Heavy Blaster Pistol, Don’t Get Cocky, opponent’s, Let ’er go!, Twi’lek). Lore quotes
    print double curly “…” (“What was that?” … “affect mind”, Affect Mind; “It’s a good bet …”, Perimeter Scan (V)).
    Game text: a quoted term prints single curly ‘…’ (‘insert’, A Tremor In The Force; ‘react’, Admiral Ackbar (V);
    ‘credits.’, Credits Will Do Fine (V); ‘BEEP-BOOP’), a quoted run naming words a card carries (“… with ‘X’ in
    title / lore / game text / name / persona”) double curly (“Death Star”, Put All Sections On Alert; “Bad Feeling”;
    “sabacc”; “Mara”, Mara Jade (V); “Trade Federation”, Darth Maul (V)). Decipher printed two such runs single (Death
    Star II: Coolant Shaft ‘Occupation’, Invasion ‘Trade Federation’) and one term double (Death Star “blown away.”);
    the data cannot tell those apart, the commoner form wins. New `gt_quotes()` / `apostrophes()`; `quotes()` stays
    for lore; Objective front/back texts and version texts (`polish_text`) get the same treatment; a leading backtick
    (`credits.') opens a single quote. All fonts in assets/fonts carry U+2018/2019/201C/201D.
  - **Expansion spheres re-cut from the printed cards** (`tools/set_spheres/cut_set_spheres.py`, sources in
    `tools/set_spheres/sources.json`; no AI, no retouching). Each `set-<key>-decipher.png` and `set-<key>-pc.png` is
    the per-pixel median of the sphere on many printed faces, each centred on its own black ring to sub-pixel and
    scaled by the ring radius, then registered to the PC stack by cross-correlation (the soft Decipher scans) and cut
    at 0.92 of the ring's centre line (312 px, as rev 32/33). Sources: `decipher` = Decipher's faces of that set
    (wiki 745 px Holotable gifs, topped up with wiki decipher-archive scans; A New Hope the wiki's 1497 px hires),
    `pc` = the PC's 745 px Virtual faces that carry that sphere. Audit result (scan | before | after sheets): the
    wiki Icon-set-* discs used since rev 32 for A New Hope, Hoth, Dagobah, Cloud City, Jabba's Palace, Special
    Edition, Endor, Death Star II and premium were NOT the printed spheres (zoomed-in inner crops, wrong colours; Cloud
    City was a different picture altogether, a yellow-red cloud car instead of the printed orange banded planet; Hoth
    a flat grey ball instead of the dark sphere lit white from below). The PC's printed Virtual cards (VS0-27) carry
    exactly the same sphere art as Decipher's cards, not the Game Aid redraws the `pc` files were made from in rev
    45 (those differed most on Endor: a white blob for the printed blue sky with the grey speeder), so `pc` is now
    cut from the PC's own printed faces too. Kept: the Decipher files of Coruscant, Reflections II, Reflections III,
    Theed Palace, Tatooine and Enhanced Jabba's Palace (the rev 32/33 scan cuts match the print and are sharper than
    their stacks); `set-reflections3-pc.png` = the Decipher file (only two PC faces carry it). Provenance table:
    assets/icons/SET-ICONS-PROVENANCE.md. Shape: every sphere is round with a black ring; the Tatooine sphere
    only looks octagonal at the ~20 px of the 497 px scans (staircase of a 9-px-radius ring): a circle fits the
    ring better than an octagon on every scan tried (3 Decipher, 1 printed scan, 1 PC face) and the PC's 745 px
    faces print it round. Rim: black on every set; Theed Palace's olive rim on res.starwarsccg.org's face of
    Panaka, Protector Of The Queen (14_24) is that one image only: Decipher's own face of the same card and five
    other Theed cards print it black. Coruscant's gold ring is inside the black ring (part of the picture) and kept.
  - **Episode I disc** (`assets/icons/ep1-disc.png`, `tools/make_ep1_disc.py`, 232 px): one disc for every place
    (under the sphere, left margin, Podracers). Measured on two median stacks of printed discs (40 PC faces at 745 px,
    30 Decipher Tatooine faces at 497 px), which agree: serif I 0.79 of the disc tall, stem 0.085, bracketed serifs
    0.26 wide; EPISODE behind it in a bold sans, light grey (dimmer than the I), cap 0.125, 0.88 wide, centred
    (0.495), a 0.018 black gap each side of the stem (it runs through the S). Replaces the 67 px VS14 disc; the two
    candidate discs from other branches were each wrong in part (cm-left: the closest, but EPISODE pure white, too heavy
    and a little high; cm-pod2 `ep1-disc-decipher.png`: EPISODE in a serif face, cap 0.19 and set low at 0.53).
  - Also fixed on the way: the ring finder took the Episode I disc for the sphere on Episode I-era faces (the tool
    now takes the uppermost good hit and skips black-inside hits).
  - **Checks:** md5-identical before/after (holotable PNG) on six cards with no apostrophe, no quote, no sphere and no
    Episode I disc: 1_3 Biggs Darklighter, 1_74 Collision!, 1_122 Dantooine, 1_140 Corellian Corvette, 1_49 Ellorrs
    Madak (Premiere: no sphere printed) and 223_40 Life Day (VS23). Changed as intended on 16 others (quotes, title
    apostrophes, spheres, Episode I disc), each looked at against its printed face.
  - **Left as found (other scopes):** GEMP text differs from the print in places (A Tremor In The Force: "When effect"
    for printed "When Effect", "Stand By..." for "Stand by . . ."); sphere placement / rim / bevel belong to the
    integration branch's DC_PRINT / DC_SPHERE_BEVEL work; Decipher's web (decipher-archive) images show Cloud City and
    Theed Palace spheres more saturated (red-yellow, yellow ship) than the printed-card scans and the PC's faces
    (orange): the files follow the printed scans.
- Rev 81 frames (2026-11-12): four printed-frame differences found by the rev 81 sphere / copyright audit, fixed against
  the printed faces (GEMP / Holotable 745 px, card body registered to the master), plus everything else seen on the same
  templates. No new spec keys; new template keys only where noted. Untouched templates md5-identical (see the check).
  - **Jedi Test** (`ls-jeditest-olive`, Dagobah #1-#5, Death Star II #6 You Must Confront Vader, the PC's It Is The Future
    You See (V)): the frame is **olive paint (58, 61, 15) chipped to silver** (silver ground with olive, not olive with
    silver speckle), with a silver title bar bulging round the stone disc and the destiny circle. Rebuilt from the
    per-pixel median of the six printed faces by `tools/make_jeditest_frame.py` (window from where the faces differ,
    plates re-textured with the Light Effect frame's crisp silver over the printed shading, paint mask re-drawn crisp).
    Measured: window 243..1386 x 387..1107 with 18 px rounded lower corners (ours 240..1386 x 372..1088), banner
    1160..1258 (was 1170), text box 1290..2015, text left 310, first line 1318, a fixed 57.3 px pitch on all six (the
    fitter no longer grows it: `gt_grow` False, 60 px on 57.3 lines). Title box (405, 196), destiny (1308, 201).
    The step keyword icon is the bare stone (no disc), 36 px, kept on the line with its word
    (`assets/icons/jedi-test-stone.png`, cut from the Game Aid icon); the adapter now also marks "test completed:
    Place" and You Must Confront Vader's "Leave". `ls-jeditest-tall` (VS slips) and `ls-jeditest-epic` unchanged.
  - **Creatures** (`creature-dc`, Decipher's sets only; PC creatures such as Porg keep the previous layout as
    `creature-dc-pc`): frame within 2 px of print; the text was off. Title box from x 402 (29 px right, 5 up); lore
    flush left 318..1300 (no first-line indent), box from 410; banner 8 px higher, 54.5 px heavy (`ctype_stroke` 1.4)
    and tight (`ctype_spacing` 3.2: AVIAN CREATURE 353 px, GIGANTIC PREDATOR CREATURE 653, within 10 px of print);
    second stat value 19 px after its label (`stat_val_gap`); FEROCITY ✶ and the "✶ Ferocity = ..." note print
    Decipher's eight-point star (`dc_star_img`); hyphenated names never break (Bog-wing); the creature icon box sits
    beside the text box top (icon slots (1357, 1715) / (1357, 1820), printed centre (1402, 1758)).
  - **Starship / vehicle sites**: GEMP names the vehicle-site icon "Vehicle Site", so Sandcrawler: Loading Bay /
    Droid Junkheap and Jabba's Sail Barge: Passenger Deck missed the blue frame and the vehicle icon box. Both mapped
    (also "Starship Site", "Creature Site": Big One's creature box). Decipher printings (`decipher_print`) take the
    printed blue sampled on nine site margins: Light (32, 98, 149) worn, Dark (33, 91, 131) (VS slips keep theirs);
    margin colour now within 3-6 levels of print (was 20-30 too bright / saturated). The ship's name in Executor and
    Home One site bars is italic as printed (_EXECUTOR_: COMM STATION); the mobile icon sits outside the starship icon
    (Executor, Home One, Star Destroyer, Blockade Flagship sites). Checked: Death Star, Death Star II, Cloud City and
    Big One sites print silver (unchanged); Blockade Flagship, Star Destroyer: Launch Bay, Executor: Docking Bay blue.
  - **Wide capital starships** (`ds-starship-wide`, `-nolore`: Executor, Flagship Executor, Finalizer (AI)): the
    frame carried Bardez's square type-icon crop; Decipher printed the round starship disc in its ring with the bar's
    bevel bending into a V under it, as on the portrait starships. `tools/fix_starship_wide_disc.py` inpaints the
    square and sets the portrait DS starship corner in, aligned on the V tip (disc centre (317, 279)). Banner 60 px
    tight (`ctype_spacing` 0.5), centred between the title's end and x 1845 (`ctype_centre_to`); game text at the
    printed 62 px in a box ending at 1992 (lines ended on the bevel); destiny number 12 px higher. Portrait capitals
    (Devastator, Home One, Corellian Corvette) checked: disc and ring as printed, unchanged.
  - **Banners of Decipher starships / vehicles**: the class name is italic (CAPITAL: _IMPERIAL_-CLASS STAR DESTROYER,
    STARFIGHTER: _LAMBDA_-CLASS SHUTTLE; YV-CLASS stays roman as printed).
  - Checks: md5 identical before / after for Luke Skywalker 1_19, Dark site 1_283, system 1_121, interrupt 1_70,
    objective 7_135, Corellian Corvette 1_140, effect 1_42, combo 10_7, Death Star: Docking Bay 327 1_124, Cloud City:
    Carbonite Chamber 5_78, Porg 223_43 (PC creature), Home One 9_74 and YV-class 7_144 (no italic class name);
    Devastator 1_301 changes only by its italic banner (intended). Evidence sheets (scan | before | after, zooms) in the batch report.
- Rev 81 verify (2026-11-12): the three points the rev 81 sphere / copyright audit could not settle, measured.
  - **Systems, Light and Dark** (`loc-system`): 33 printed systems (16 Light, 17 Dark, Premiere .. Coruscant, Jedi
    Pack, OTSD) registered to our render on the two bar assemblies (the picture differs from the library art; the
    350 px faces are cropped up to 2.5 % inside the card edge, so the card outline is no reference); Dark scans turned
    180° and measured in Light coordinates. The Dark system is the Light layout turned whole, as rendered, but rev 81's
    numbers were off on both sides: the sphere sits 8.7 / 6.1 px (745) right / down of rev 81's spot on Light systems
    and 9.8 / 7.8 on Dark ones (`dc_system_ring` (166, 200, 56); new key `dc_system_ring_dark` (169, 204, 56), pre-turn
    coordinates; median of 10 / 9 centroid fits, spread ±1.5 px); the copyright halves 9.5 px in (Lucasfilm) / 4 px in
    (Decipher) and 9-12 px higher (`dc_split` ((216, 1884), (1427, 1880)), 14-16 halves a side, sd ≤ 1.8 px across).
    The printed left half reads top to bottom (letters facing the card, like the right half; real Alderaan, Kessel,
    Fondor, Corellia printings): new key `dc_split_left_down` turns it (`rotate(90deg)`), Decipher-printed cards only.
    Coruscant-set systems (Coruscant, Naboo, Malastare, Tatooine, both sides) print the sphere bare on the starfield
    (no grey ring) and Decipher's Episode I disc under it, which we did not draw: centre 2 / 100 px (master) from the
    sphere's, 56 px in a 74 px ring 6 px wide, grey #5f6163 (new key `dc_system_ep1`, drawn when the card's `ring_icons`
    hold `episode1`; 8 printed systems, ≤ 1.5 px (745)).
    Dark sites (`loc-site`, the whole card turned): sphere and line where the Light measurement puts them (11 Dark sites,
    ≤ 2 px), no change, except Episode I-era sites.
  - **Episode I-era sites** (Tatooine .. Theed, Light and Dark, 13 printed sites): Decipher's Episode I disc
    (`icons/ep1-disc-decipher.png`) 56 px across, centred 99 px under the sphere (ours: the VS disc, 44 px, 77 px under,
    lying over the end of the copyright line); the sphere 4 px higher; the line 12 % smaller and centred 110 px further
    from the sphere, ending ~40 px (745) short of the disc. `DC_PRINT["loc-site"]["ep1"]` (applied when the card's
    `ring_icons` hold `episode1`): `dc_sphere` (2022, 476, 56), `dc_copy` (2017, 950), `dc_copy_size` 25.5,
    `ring_disc_size` 56, `ring_disc_dx` -2, `ring_disc_dy` 16, `ring_disc_icons`.
  - **Coruscant** (GEMP 12_*, 18 characters, effects, interrupts, weapons, starships, sites, systems): the template
    positions hold (centre within 1 px on every template); the weak rev 81 match came from the picture: our Coruscant
    spheres (the PC redraw `set-coruscant-pc.png`, the default, and Decipher's) carry a black rim outside the gold ring,
    the printed one has the gold ring at the disc's edge (radial profiles: gold peak r 12.5-13 px (745), no dark ring).
    `DC_SPHERE_ZOOM` (render.py) draws those pictures 1.23x / 1.16x inside a round clip (`dc_sphere_img`), on
    Decipher-printed cards, sites and systems.
  - **Wording** (`adapter.copyright_for`), settled on sharp photos of printed cards (pricecharting.com, 700-1600 px):
    Enhanced Cloud City prints the final period (5 cards); Endor prints "TM, ® & © 1999 DECIPHER INC." on every card
    (4 photos; Speeder Bike and Tempest Scout 6 carry the same digits as the rest of the set on the Decipher archive
    scans): `PRINT_YEAR["8"]` 1999; Reflections II's own cards print the final period ("… 2000 DECIPHER INC.", Alter &
    Collateral Damage, Sense & Recoil In Fear; its foil reprints set "TM, ®, &" but render as their first printing).
    `NO_FINAL_PERIOD` now 11-14.
  Checks: md5 identical before / after for Luke Skywalker 1_19, Death Star: Central Core 1_283, A Few Maneuvers 1_70,
  objective 7_135, starship 1_140, Hoth: Echo Command Center 3_56, Cloud City: Casino (Dark) 7_269, Tatooine Interrupt
  with the Episode I disc 11_26, effect 1_42, Coruscant objective 12_88, PC systems Ahch-To 211_48 and Coruscant (V)
  203_31. Evidence sheets: scan | before | after with x4 zooms of the sphere and each copyright half.
- Rev 81 (systems and discs) (2026-11-12): five points checked on printed systems / sites (wiki Decipher-archive scans,
  the wiki's 16 1497 px `-hires.webp` system faces, Decipher's 1039 px Episode I site files, pricecharting photos).
  - **System art scale** (`render.system_library_art`, `server.resolve_art`): the art library keeps a system's picture as
    the strip between its bars, cut from the whole card normalised to 350x490 (`art-manifest.json` `box`, e.g. Bespin
    [14, 96, 336, 395]). It came back as a plain `rect` and was cover-fitted to the whole 1343x1931 art area, so the
    planet printed 1.4-1.6x too large (Bespin, Fondor, Kessel). Library art of a system now carries `card350` (the box)
    and is placed where it sits on the printed card: card body = the 745 px face's 37..708.5 x 36..1001.5, i.e.
    17.38..332.85 x 16.98..472.33 of the 350x490 card (`SYS_BODY_350`); the rows under the bars / beside them are the
    strip mirrored outward. Checked by registering each render's art (745 px, x 120..625, y 250..790) inside the printed
    face over scale 0.80-1.25 and both turns: all 59 library systems with a wiki face (Light and Dark, Premiere ..
    Coruscant, Jedi Pack, OTSD) match at scale 0.97-1.00, median offset 0 / 0 px (745), worst 7 / 8.5 px; the 16
    independent 1497 px faces 0.97-0.98 (their card outline sits ~1 % differently); before: below 0.80 (search floor).
    Scans and uploads unchanged; PC systems (Ahch-To 211_48, Coruscant (V) 203_31) md5-identical.
  - **Location title dot** (Decipher printings only, `decipher_print`): sites and systems print the dot against the
    first letter (•BESPIN, •KESSEL, •DEATH STAR: CENTRAL CORE: 4-5 px gap at the master, dot ~15 px, centred on the cap
    height); ours stood 18 px off. `.ltitle/.dtitle .dot` get `font-size:0.88em; margin-right:-7px` (gap 4-6 px, dot
    14-16 px). Character titles already match print (Darth Vader hires: dot 118-139 / D at 146 vs ours 116.5-138.6 /
    144.7) and are unchanged. PC / VS slips unchanged.
  - **Episode I disc on systems and sites**: confirmed, no change. On the sharpest faces (Decipher's 1039 px Naboo:
    Battle Plains Light / Dark and Theed Palace Generator Core; the 745 px printed scan of Watto's Junkyard; Coruscant
    systems at 357 px) the disc is the same as everywhere else: tall serif I nearly the disc's height, EPISODE a light
    bold sans behind it, as `icons/ep1-disc.png` draws it. The "short heavy I over a strong EPISODE bar" was the blur of
    a ~12 px disc on the 350 px scans.
  - **Reflections III copyright**: prints the final period ("TM, ® & © 2001 DECIPHER INC."): sharp photos of
    Stormtrooper Garrison, The Ebb Of Battle, Qui-Gon's Lightsaber, and Decipher's own 1039 px Reflections III / Coruscant
    files. `NO_FINAL_PERIOD` now 11, 12, 14 (12 and 14 left as rev 81 verify set them: Decipher's Coruscant file also ends
    "INC.", but no sharp printed Coruscant / Theed photo was found to settle it).
  - **Tatooine sphere**: round with a round black ring on the sharpest photo found (Padmé Naberrie, 1200x1600); no change.
  - Checks: md5 identical before / after for Luke Skywalker 1_19, interrupt 1_70, objective 7_135, Darth Vader 1_168,
    Ahch-To 211_48, Coruscant (V) 203_31 and the three Japanese samples; Death Star: Central Core 1_283, Cloud City:
    Carbonite Chamber 5_166 and Bespin 5_76 from its scan change only inside the two title bars (the dot, intended);
    Allegations Of Corruption 13_52 ends "DECIPHER INC.".
- Rev 81 (Coruscant sphere) (2026-11-12): `DC_SPHERE_ZOOM` re-measured per picture and per place; the default
  `expansion_style` "pc" (Bill 2026-11-01) is unchanged. Ring fit (least-squares circle on the dark ring, 8x upsampled,
  then a radial yellowness / lightness profile) on Decipher's own 745 / 1039 px faces of Allegations Of Corruption, A
  Tragedy Has Occurred and Naboo: Battle Plains (Light and Dark): the gold ring peaks at r 11.0 px (745) of the 14 px seat
  and a black ring runs from r 12.5 to 14.5 (all four faces alike). The rev 81 zoom (PC 1.23, Decipher 1.16) pushed the
  gold out of the clip on cards and sites: no gold showed at all. The pictures: Decipher's has its gold peak at 0.80 of
  the radius and its own black ring 0.88-0.97; the PC redraw's gold peaks at 0.94 with no black ring. Cards and sites
  now draw Decipher's 1:1 and the PC's at 0.87 (gold at 0.82, the black hole behind it shows as the printed black ring);
  measured after: gold peak r 11.0 and black ring from r 12.0-12.5 on all three cards, both styles. Systems print the
  sphere larger on the bare starfield (Coruscant, Tatooine, Naboo, Malastare systems: gold peak r 13 px of the 14 px
  seat, its black ring lost in the starfield): systems keep Decipher's at 1.16 and draw the PC's 1:1 (gold r 13.0 after;
  was clipped at 1.23). Values are (cards and sites, systems); `dc_sphere_img(..., system=True)` takes the second. Only
  Coruscant's two pictures are in the table: every other set's sphere is drawn whole and unclipped, so none loses its rim.
  Checks: md5 identical before / after for 1_19, 1_70, 7_135, 3_56, 1_283, 5_76, Tatooine: City Outskirts 11_42, Naboo:
  Boss Nass' Chambers 14_49 (Theed sphere) and the Tatooine system 12_84 in Decipher style; Coruscant cards change only
  in the sphere.
- Rev 81 (geometry and copyright) (2026-11-12): measured on the printed faces on wiki.swccg.com (Decipher archive scans,
  hires 1497 px faces of sets 1-4, the PC's 745 px faces), each registered to our render.
  - **Two-disc title** (`render.DISC2_TITLE_SHIFT`): the title moved 170 px right of the one-disc title on every
    template; printed bullets start at x 235-238 (745) on Dark two-disc cards (The Emperor 10_51, Arica 10_31, The
    Emperor, Relentless, Palpatine, Galactic Emperor, Mara Jade (V), Arica (V)), 229-230 on the Light Rebel frame
    (Bail Organa, Mon Mothma, Cal Kestis, Kelleran Beq), 231 on the Light Alien frame (Chewie With Bowcaster, Solo,
    Chewbacca, Defender Of Kashyyyk, Grakchawwaa); we set them at 253-254 / 240 / 235. Now Dark 136, `ls-character-rebel`
    114, `ls-character-alien` 127 (all within 1 px). Decipher's 1999-2000 printings (Emperor Palpatine 9_109, Mara Jade,
    The Emperor's Hand 110_10) set it 10 px (745) further left again: card key `disc2_title_dx` = -22 (adapter, Decipher
    prints of the SE-era sets). The second disc on the Dark frames sits 4 px (745) left of ours on all six measured faces:
    x 350 (was 359). Tarfful's "original" face (243) is an outlier, not followed.
  - **Copyright wording** (`adapter.copyright_for`, re-read at 8x on 4-8 scans a set): Reflections II, Coruscant,
    Reflections III and Theed Palace print the final period ("… DECIPHER INC.", rev 81 had dropped it); only Tatooine
    and Enhanced Cloud City print none (`NO_FINAL_PERIOD` = 11, 109). Tatooine sets the line in its own tighter face:
    `©2001 LUCASFILM LTD. & TM.  TM, ®& ©2001 DECIPHER INC`; its Epic Events (Boonta Eve Podrace, I Did It!) print the
    period. `copyright_for(set, card_type=…)`. Render: a line containing "®&" takes `DC_COPY_TAT` (30 px, letter-spacing
    0.8, oval rings 29 x 24 px, 2.4 px rim, 20 px letter): print cap 11.2 px (745) against our 10.5, © / ® 12.8 x 11.2;
    run length now 310.0 / 309.5 against 309.5 / 308.5 printed (Sebulba's Podracer, Losing Track), centre within 2 px.
    Tatooine's Light Epic Events print the line white on the purple (`copyright_ink`, others black as before).
  - **Scan mapping** (`render._edge_trim`): Decipher's 350 x 490 Tatooine GIFs carry a white last column, so the frame
    bbox ran to the image edge and the Podracer scans mapped 5 % wide: their own red frame and copyright line showed
    inside the window (two copyright lines). A run of bright columns / rows touching the image edge, under 1 % of it and
    3+ px from the body is dropped. All five Podracers checked with library and scan art: one line, at the printed spot.
  - **Location bar titles on Decipher prints** (decipher_print sites and systems only): letter-spacing 1.4 px (was 2) and
    the black-on-grey title a 1 px stroke heavier. Death Star: Central Core (hires): printed caps 40 / 42 px (white on
    black / black on grey), widths 21.5 / 23, stem 6 / 7, run 586 / 588 px; ours now 40 / 41, 21 / 22, 6 / 7, 589 / 589
    (was 601 / 601, black caps 40 x 21, stem 6). Kessel's white title was already 40 px, as printed.
  - **Reflections Gold Dark Interrupt disc**: printed references exist (the 2001 playtest photos, e.g. Atmospheric
    Assault, Blow Parried): a round swirl disc with a thin dark rim in the red lobe. Bardez's layer clipped it to a
    chamfered square; `make_rg_frames.round_ds_interrupt_disc()` keeps the swirl inside r 82 round (318.5, 288), draws
    a 5 px dark rim and inpaints the square's corners from the lobe (`python3 make_rg_frames.py round-disc`).
  - **Text** (gempdata/corrections.json; the same fixes are listed for GEMP / wiki): A Tremor In The Force "When
    Effect", lore “Stand by . . .” (1_42 and its VB1 printing); A Disturbance In The Force "When Effect", lore "in the
    Force, “. . . as if" (1_208 and VB1, whose game text also had "Whever"); Presence Of The Force "“. . . binds";
    Out Of Commission lore "got that tractor beam"; Out of Commission & Transmission Terminated (title "of",
    "destiny > 3"); Domain Of Evil "test completed: Place" (the other Jedi Tests had it); Sleen "✶ Ferocity". Adapter,
    Decipher prints only: "Ferocity = destiny – N" with a spaced en dash (Bog-wing both sides, Nudj, Sleen print it so;
    modifiers such as "destiny -1 > ability", "power -1", "deploy -1" print a hyphen and stay).
  - **Checked, not changed — Decipher window / lore-box geometry (sets 1-8)**: 20 hires faces (sets 1-4, eight
    templates) warped into the 1632 x 2220 master by ECC affine fit and measured edge by edge against our master renders
    (gradient peaks): window top −2 px master on Light Effects / Interrupts / Rebels, +0.3 on Aliens / starships, ~0 on
    Dark; lore-box top within ±1 px (median −0.5); window left edge +1.3..+2.2 px master (print RIGHT of ours) on Light
    Effects / Interrupts and scattered elsewhere. No consistent offset of the size or direction reported in rev 81
    (bevel 1.4 px (745) right, tops 2 px) shows at master resolution; all are ≤ 1 px at 745 and differ in sign between
    templates, so nothing was warped. PC and Japanese renders are untouched by this revision: md5-identical before /
    after for the Japanese samples Darth Vader, Luke Skywalker, Admiral Ozzel, PC cards 223_40, 200_105, 205_14, 213_12,
    211_48, 211_47, and Decipher 1_3, 1_74, 1_140, 9_113, 9_55.
- Rev 81 (site wear and PC wide starships) (2026-11-12): two follow-ups to rev 81 frames, measured on printed faces.
  - **Light starship / vehicle site wear** (`ls-starship`, Decipher printings only, `decipher_print`): the procedural
    fine speckle is replaced by Decipher's worn paint as printed: large scratched patches, heaviest on the strips
    between the title bars and the picture, a silver outer rim and window rim. `tools/make_site_wear.py` registers
    four printed Light faces (wiki: Sandcrawler: Loading Bay hi-res 2073 px; Decipher archive images of Home One: War
    Room, Home One: Docking Bay, Blockade Flagship: Docking Bay) to the site frame by ECC (affine), classifies each
    pixel of the frame's paint zone as blue / silver / ink (Otsu on blue - red per face), and takes the per-pixel
    median (ink left out) -> `assets/frames/site-wear-light.png` (frame coordinates, 255 = worn; 44 % of the zone).
    No smoothing or retouching; under the copyright line (ink on all four) the paint stays. Rows move with a taller
    text box exactly as the frame does. The Light colour (32.4, 97.7, 149) is unchanged. Each Light card has its own
    patches on the print (the hi-res and archive Loading Bay agree, so the wear is printed, not handling damage); the
    median gives the shared character, not any one card's pattern. Dark blue sites: the six hi-res Dark faces (Droid
    Junkheap, five Executor sites) show smooth unworn paint, as we render it: unchanged. PC / non-Decipher Light
    starship sites (Profundity: Docking Bay) keep the previous speckle (unchanged).
  - **PC landscape starships** (Finalizer 204_54 and Finalizer (AI) 204_54^AI, both printed 1039 x 745): Finalizer
    (AI) was missing from WIDE_PRINTED (its printing id carries ^AI) and rendered on the portrait starfighter frame;
    now on the wide frame without lore box. The PC printed the round type disc too (no square icon): kept. Both take
    new templates `ds-starship-wide-pc` / `ds-starship-wide-nolore-pc` (adapter: wide starship with a `pc:` set mark),
    measured on wiki V4-D-finalizer.gif / V4-D-finalizer_ai.gif (745 px; x 2 + Holotable offset = master): banner
    left-set 108 px after the title's end (`ctype_after_title`, printed 345..837, ours 344..837), `ctype_spacing`
    0.95, y 233; title y 219 (printed cap top 76); class name italic (_RESURGENT_-CLASS) as printed; the Episode VII
    disc in the left margin (`ring_disc_left` (252, 476, 82), not under the destiny) with the PC's broad blue ring
    (`assets/icons/ep7-disc-blue.png`, ring profile measured on the two faces by `tools/make_ep7_disc_blue.py`); the
    Virtual Set 4 mark after the icon boxes (`set_icon_abs` (1916, 1104), size 70: digit 924..947 x 524..558 printed,
    926..946 x 524..557 ours); icon boxes 10 px lower and 6 px left (within 1 px of print); the PC labels turned a
    quarter left into the right margin (`labels_rotated`: caption "Executor", the (AI) stamp and logo, the art credit,
    within 2-3 px of print; the credit upright at 51 px, `label_presets`). Executor and Flagship Executor (Decipher)
    unchanged.
  - **Checks:** md5 identical before / after (holotable PNG): 1_19, 1_283, 1_121, 1_70, 7_135, Dark blue sites 4_159,
    2_149, 12_164, Executor 4_167, Flagship Executor 9_157, Profundity: Docking Bay 217_44, Death Star: Docking Bay 1_124
    and the Japanese samples darth_vader / luke_skywalker / admiral_ozzel (tools/japanese/samples). Changed as intended:
    2_66, 9_57, 9_58, 14_48 (wear), 204_54, 204_54^AI.
- Rev 81 (geometry 2) (2026-11-12): the three items left open by Rev 81 (geometry and copyright).
  - **Reflections Gold original playtest cards (set 15o), wide Effects / Interrupts**: the 2001 photos (Local Trouble
    1957 px, Strangle, Weapon Malfunction, Atmospheric Assault) print the copyright line split over the black border,
    white, in Decipher's typesetting: "© 2001 LUCASFILM LTD. & TM." down the left edge (reading top to bottom) and
    "TM, ®, & © 2001 DECIPHER INC." up the right edge (with the comma after ®, as Coruscant). Template key `rg_copy`
    (centres (112, 352) and (2116, 348) master, from the photos mapped to the card body) and `rg_copy_size` 31.5 (the
    printed run is 12 % longer than our 28 px Decipher line). Remastered set 15 keeps no line (md5-identical).
  - **Tatooine Light Epic Events** (Boonta Eve Podrace 11_24, I Did It! 11_25): third measurement, the line against the
    card body on the same face (the black border on both sides, the scan's stray white last column excluded): ours sat
    1.3 px (745) left and 2.6 px high. Card key `copyright_dxy` = (3, 6) master; now x 0.9596-0.9600 of the body width
    (print 0.9598) and centre 0.3410-0.3420 of its height (print 0.3421).
  - **Decipher 1999-2000 two-disc titles** (Emperor Palpatine 9_109, Mara Jade, The Emperor's Hand 110_10): glyph by
    glyph on the printed faces (card normalised to 745 x 1039) the caps are the same height (31 / 22 px) but the run is
    3 % narrower and starts further left: `disc2_title_dx` −32 (was −22) and new `disc2_title_ls` 0.1 (letter-spacing,
    was 1). 9_109 now bullet 221, E 234, end 428 against the print's 221 / 234 / 429. Mara Jade's long title still
    starts ~5 px right of the print's and is condensed 2 % more; the EJP archive scan sits 10 px off vertically, so its
    crop is not reliable enough to follow further. 9_109 keeps the PC sphere (Bill's default).
  - md5-identical before / after: Japanese samples (Darth Vader, Luke Skywalker, Admiral Ozzel), 223_40, 200_105,
    205_14, 213_12, 211_48, 1_3, 1_74, 1_140, 9_113, 9_55, 10_51, 219_19, 15_260, 15_220, 2_42, 11_97.
- Rev 81 (Decipher text setting) (2026-11-12): **game text and lore set the way Decipher set them** on its own printings
  (card `decipher_print`, i.e. the editor's "As Decipher printed it" box / adapter `decipher_print()`; PC, VS, OVS,
  Virtual Legacy and Japanese renders are untouched). Measured on 58 printed faces registered to our renders by the card
  body (the wiki's 1497 px hires scans of Premiere, A New Hope, Hoth and Dagobah; Decipher's 350-367 px archive / web
  faces for Cloud City to Theed Palace; the wiki's 745 px gifs of Decipher cards turned out to be the PC's errata
  re-renders, set in the PC's face, and were not used), lines read by OCR and aligned word-for-word with the card text.
  - *Face and size:* x-height equals ours (game text 32 px at 62, lore 30 px at 58), so the sizes stay; the printed glyphs
    are wider than Holotable Text (printed ink width / our advance at tracking 0: game text 1.026, lore 1.044). The box is
    laid out at width / k and stretched by k (`scaleX`), tracking 0 (was -0.4 / +0.25), inline icons counter-scaled.
  - *Leading:* game text pitch 63.5 (29 faces, 63.0-64.5; ours 64), first baseline 1 px lower; lore 60.5 (20 faces), and
    three-line lore keeps that pitch (the lore box grows to 187 px instead of the fitter tightening it to 54 px, as it did
    on every 3-line character lore). Fitter: fractional pitch (`data-fit-step`).
  - *Measure:* fitted on the printed line breaks of 56 blocks (layout simulated over the right edge): game text box width
    -18 px on characters, -33 on Premiere / A New Hope Effects and Interrupts (their lines run a word shorter than Hoth's
    onward), 0 elsewhere; lore starts at x 317 (ours 319 Dark / 326 Light) with a 75 px first-line indent and ends 6 px
    short (Dark) / 6 px past (Light) of the PC lore limits. Identical line breaks: 13 → 35 of 56 blocks, 65 → 169 of 224
    lines. The rest differ by one word at a line end; Decipher tightened tracking card by card (Vote Now!, Organized
    Attack, Our Only Hope print longer lines than any one measure allows), which no single setting reproduces.
  - *Ink weight:* printed black text is heavier and white text (reversed out of the Dark boxes) lighter than our faces
    (ink coverage printed / ours 1.04-1.08 and 1.15 lore on Light, 0.83-0.88 and 0.77-0.90 on Dark): a 0.2 / 0.3 px
    text-stroke in the text colour on Light, 0.5 / 0.35 px in black on Dark brings both to 0.96-1.06.
  - *Ellipses:* Decipher printed lore ellipses spaced ". . ." in 31 of 33 checked (Premiere to Reflections III; Boring
    Conversation Anyway and Jawa print "... "): lore "..." / "…" becomes ". . ." with no-break spaces, no space before,
    one space before a following word; texts already spaced (corrections.json) stay as they are.
  - Template data: `render.DC_TEXT` / `DC_EARLY` / `DC_TEXT_FAMILY` (characters, Effects, Interrupts, weapons, devices,
    starfighters / capital ships, vehicles, creatures); card key `dc_expansion` (adapter). Sites and systems were
    measured too (Premiere, A New Hope, Hoth): their centred, tracked text is within 1-2 % of the print and unchanged.
  - **Checks:** md5-identical holotable renders before/after: 223_40 Life Day (PC set mark), 200_1 Aayla Secura (VS0),
    the OVS spec 1101_1, the three Japanese samples, 2_13 / 1_241 / 3_126 with `decipher_print` false, and the Decipher
    sites / system 1_283, 2_67, 2_143.
- Rev 81 (Episode I spheres) (2026-11-12): two leftovers of the Coruscant sphere work, measured.
  - **Portrait cards (Effect, Interrupt, Character, Weapon, Shield, Starship) of Tatooine, Coruscant, Theed Palace and
    Reflections III: no change.** Each face registered to our render on the frame round the sphere (top-right corner,
    destiny area, right margin; NCC, sub-pixel), the sphere matched by its own picture and by a ring fit; print minus
    ours, px at 745. Decipher's 745 px files (25 faces): Dark Effects / Interrupts / Shields dx -0.1..+0.8, dy +2.1..+3.0;
    Light Effects / Interrupts dx -0.3..-1.0, dy -1.2..-2.2. The same files of classic sets (ANH .. DS II, 10 Effects /
    Interrupts) give the same: Dark dy +0.1..+3.2, Light dy -1.4..-2.2, dx within 0.7. Scans of printed cards (3
    printed-scan PNGs, 33 Decipher-archive scans at 357 / 497 px) give dx -1.5..-2.1, dy -0.8..+0.8, and the classic
    archive scans the same again. So the Episode I-era sphere sits where the classic one does (within 0.5 px per source);
    the 2-3 px spread is between sources (the same card differs that much: I Will Find Them Quickly, Master printed
    -1.95 / -0.09 vs Decipher's file +0.65 / +1.40; Booma -1.49 / +0.54 vs +0.29 / -2.62), and the rev 81 positions,
    fitted on all sources, stay. Tables: m745.txt, m357.txt, mclassic745.txt, mclassic-archive.txt in the batch sheets.
  - **Coruscant-set systems (Coruscant, Naboo, Tatooine, Malastare): no grey ring round the sphere; the sphere is larger.**
    Sharpest faces found: the PC's 742 px faces (2x of the printed scans; pricecharting and the wiki only have 350 px).
    Radial profiles: the Episode I disc's grey ring shows as a peak (L 50 at r 16 px, dip to 30 inside, 9 outside); round
    the sphere the profile falls smoothly from the gold (L 152 at r 12 to 8 at r 20) and stays below the disc ring's at
    r 17-18 (41 / 28 against 44 / 33) although the gold's blur adds to it: no ring. The sphere's bright edge (half level
    of a blurred-disc fit) is at r 15.0-15.3 on all four (ours 13.5 at 56 px): new key `dc_system_ep1_sphere` 62 draws
    it 62 px across on the same centre (after: r 15.0 both styles); the Episode I disc stays where it was.
  - Checks: md5 identical before / after for 1_19, 1_283, 1_70, 7_135, Alderaan 1_121, Bespin 5_76, Allegations Of
    Corruption 12_128 and Naboo: Battle Plains 12_79; only the Coruscant-set systems change (the sphere).
- Rev 81 (geometry 3) (2026-11-12): Decipher's two-disc character titles re-measured against the frame instead of the
  scan's crop. The geometry 2 figures normalised each archive scan by its own crop (white surround), which put the EJP
  and DS2 faces 6-12 px off; the title is now measured from the Imperial disc's right edge on the same face (745 px).
  Check of the method on Ref2 / PC faces (The Emperor, Arica, The Emperor, Relentless, Mara Jade (V)): print and ours
  both 28-29 px. Decipher's own sets: Death Star II, Emperor Palpatine 9_109: bullet 20, run 208 px (print) — ours now
  21 / 207; Enhanced Jabba's Palace, Mara Jade, The Emperor's Hand 110_10 (both wiki faces, 350 px Holotable gif and
  367 px archive scan): bullet 23-25, run 362-372 at full width, ending past our bar (the print is not condensed) —
  ours now 24 / 366 (was 12 px from the disc and condensed to 353). Per-set table `adapter.DISC2_DECIPHER`
  (x offset, letter-spacing, extra bar width; master px): set 9 (-17, 0.1, 0), set 110 (-8, default, 42); new card key
  `disc2_title_dw`. No other Decipher card prints two discs (Enhanced Premiere, ECC, the other premium sets have none;
  Reflections II's The Emperor and Arica keep the default, checked). Sheet: Mara Jade gif / archive / ours, Emperor
  Palpatine print / ours. md5-identical before / after: Japanese samples (Darth Vader, Luke Skywalker, Admiral Ozzel),
  223_40, 200_105, 205_14, 213_12, 211_48, 1_3, 1_74, 9_113, 10_51, 10_31, 219_19, 226_8, 15_260o, 11_24.
- Rev 81 (sites 2) (2026-11-12): the leftovers of rev 81 (site wear and PC wide starships), measured on printed faces.
  - **Site icon boxes** (Decipher sites, all): the Mobile, Starship and Vehicle boxes were the Holotable icon on box.png
    (a brown-speckled surround, ~10 px too large, which read as a dark shadow block on the blue sites). New
    `assets/loc/scanbox-{mobile,starship,vehicle}.png` (100 x 94, as the existing interior / exterior / planet /
    underground scanboxes) cut by `tools/make_site_scanboxes.py` from 10 wiki hi-res faces (five Executor sites, Death
    Star: Docking Bay 327 / Central Core / War Room, Sandcrawler: Loading Bay / Droid Junkheap): each face registered to
    the frame (make_site_wear.register; silver sites too), the row of square boxes matched by the scanbox rim and fitted,
    each kind's crops rim-colour matched, ECC-aligned and per-pixel median'd (mobile 15, starship 10, vehicle 4). The
    rows sit within 5 px of print. Decipher prints the exterior icon outside the interior one (Hoth: Echo Docking Bay,
    Death Star: Docking Bay 327): adapter now orders them so.
  - **Site title position** (Decipher printings, `dc_title_cx` 1110 on loc-site): Decipher centres the title on the
    card's centre line in both bars, moving it only to clear the boxes / Force slot; ours centred it in the free bar
    (Home One: War Room / Docking Bay, Executor: Comm Station, Hoth: Echo Docking Bay up to 70 px off). Now within a
    few px on the 9 faces checked (Home One x2, Sandcrawler x2, Executor: Comm Station, Cloud City: Lower Corridor,
    Death Star: Central Core, Hoth: Echo Docking Bay / Command Center).
  - **Nav Computer box** (`BOX_ICON_FILES`, `assets/icons/col-nav.png`, `tools/make_col_nav.py`): was the in-text icon
    (grey inner frame) inside icon-box.png; no printing shows the double frame (Executor, Ghost, Azure Angel, Blue
    Squadron 1, Bright Hope, Finalizer): red field to a thin silver rim, median of five PC faces. The in-text icon is
    unchanged.
  - **WIDE_PRINTED by printing id** (`adapter.is_wide_printed`): the PC's alternate-image printings carry ^ ids. The
    GEMP gifs show I Must Be Allowed To Speak (V) 200_41 and Bow To The First Order 204_47 are portrait and only their
    (ALT) printings landscape: the set now lists 204_54, 204_54^AI, 200_41^ALT, 204_47^ALT (the old 200_41 / 204_47
    entries turned the portrait cards landscape). The (ALT) Effects take `rg-{ls,ds}-{effect,interrupt}-pc`: banner
    55 px, 18 px left (printed 652..726 at 745); text 8 px lower; sphere in its red ring at the printed place (925..961 x
    183..219); Episode VII disc in the left margin in a red ring (`ep7-disc-red.png`, `tools/make_ep7_disc.py`, which
    also makes the blue one); the PC set mark at the text box's lower right; labels turned into the right margin;
    "Original concept by" 19 px (745) higher in the bottom bar.
  - **Finalizer (AI) credit doubled**: the (AI) face prints its art credit 46 px (745) higher than Finalizer's; the redraw
    sat beside the scan's own. `adapter.LABEL_PLACE` per printing ({"204_54^AI": concept x 95}); both now lie on the
    scan's credit. Label kinds: art credits are tagged `kind: art_credit` (template `label_presets` by kind or preset).
  - **PC set mark** (all PC cards): the ring was long and thin (57 x 39 px at 745 for a 35 px digit); printed 46.5 x 42,
    a rounder band tilted 38 degrees with a dark navy (gold: brown) edge; digit 18 % wider. Portrait PC starships
    (`ls-/ds-starship-starfighter`, `pc_set_icon_abs`, `pc_set_digit_size`, `pc_stack`): the mark 8 px lower (digit
    centre (664.5, 961) at 745), and 3-4 icon boxes stacked up from a fixed foot at the printed 43 px / 48 px pitch with
    the mark below (Azure Angel, Booster In Pulsar Skate, Bravo Fighter (V), Acclamator, Blockade Support Ship), not
    shrunk to fit above it.
  - **Sandcrawler text**: no transcription error. GEMP 2_66 / 2_149 is the PC errata printing ("Deploy on your
    sandcrawler. Each Jawa is forfeit +2 here.", •••), matching the PC face; Decipher printed "Deploy on your
    Sandcrawler. Jawas forfeit +2 here." with one dot (wiki 2_66o / 2_149o). corrections.json unchanged.
  - **Checks:** md5 identical before / after: 1_19, 1_121, 1_70, 7_135, effect 1_42, combo 10_7 and the three Japanese
    samples. Changed as intended: sites (1_283, 5_78, 4_159, 9_58, 2_66 ...: titles, boxes), Nav cards (4_167, 9_157,
    PC starships), every PC set mark, 200_41 (portrait again), the (ALT) Effects and the Finalizers.
- Rev 81 (Decipher text setting 2) (2026-11-12): the rest of the Decipher text setting, on `decipher_print` renders only.
  - **Printed line breaks per card** (`gempdata/decipher_lines.json`, keys `lore` / `game_text` / `game_text_back`;
    adapter `decipher_lines()` → card `dc_lines`; render `dc_hint()`): the 72 blocks read from the printed faces (the
    56 of the first part and 16 more below; Allegations Of Corruption's lore and I'll Try Spinning's text read by eye where OCR failed), each line as printed. A text whose words (and line-opening signs such as
    "+" or "=") no longer match its lines is set normally; with the lines the block does not re-wrap (`nowrap`), so a
    line Decipher tracked tighter than the measure makes the fitter tighten the tracking, as Decipher did. Paragraph
    marks follow the printed lines: Organized Attack (7_97) runs "LOST:" on, Our Only Hope (9_53) starts it on a new
    line. Result (layout check against the print): 72 of 72 blocks break as printed (two show a token split only:
    ". . .”" and italic "Executor ." — the same visible lines).
  - **More templates measured** (printed line width / ours, pitch, on 350-1497 px faces):
    Defensive Shields (6 faces, Reflections III) and Admiral's Orders (5, Death Star II / Theed): widths 1.03-1.04 of
    our PC setting, as the family → set like the family (`DC_TEXT_FAMILY`); Admiral's Orders print seven lines at pitch
    64.5 (5 faces 63.5-65), measure 36 px shorter and the box 45 px deeper than the PC's (`DC_TPL`). Objectives (4 fronts, 4 backs; Special Edition, Death Star II, Coruscant): width at 62 px ×1.026 matches,
    pitch 63.0-64.5 (ours 65 at 63 px, grow) → 62 px, pitch 63.5, no grow; the italic heading line ("Deploy Throne Room,
    Insignificant Rebellion and Your Destiny.") is condensed onto one line as printed (JS, `.objhead`). Jedi Tests (5,
    incl. the 1497 px A Jedi's Strength): x-height 30 (ours 31), widths as the family at 58.5 px, pitch 58.0-59.0 (mean
    58.4; the 57.3 of the rebuilt frame came from the PC's faces) → 58.5 px, pitch 58.4, measure -16. Podracers (5):
    widths already within 1 % (rev 81); pitch 63.0 (ours 63.75) and lore 60.5 → set for Decipher printings.
  - **Dark white text tone:** on 14 hires Dark faces the brightest point of each white glyph (median 194-213) equals the
    brightest paper on the same scan (99.5th percentile 194-213, R = G = B): the letters are unprinted paper, the scans
    are just exposed ~200. Our white (#fff, like our paper white) stays.
  - **Checks:** md5-identical before/after: 223_40, 200_1, OVS 1101_1, the three Japanese samples, and 2_13, 7_97,
    4_75, 9_151, 13_8, 9_3, 11_47 with `decipher_print` false, and the Decipher site / system 1_283, 2_143.
  - Left for the text-data agent (GEMP text differs from the print): Concentrate All Fire 9_3 ("for remainder", "Once
    per turn, you"), Plead My Case back 12_88b (bold "order agenda"), More Dangerous Than You Realize 7_135b (“blown away.”).
- Rev 81 (Decipher printed text) (2026-11-12): a card rendered as Decipher printed it (`decipher_print`, English) now
  carries the text, title / bullets, lore and icons Decipher printed where GEMP's text is an errata (Decipher Glossary
  Version 2.0 / Glossary Supplement, or the Players Committee's AR 2023 Appendix A). 514 cards.
  - *Source:* `gempdata/decipher_printed.json` (GEMP id -> the GEMP front fields that differ, raw GEMP conventions,
    `_page` / `_image` / `_label` provenance), made by `tools/make_decipher_printed.py` from a dump of wiki.swccg.com.
    Wiki conventions: the printed face's page has `card_uid` = GEMP id + "o" (Jek Porkins 1_13o, version_label "printed"
    or "Decipher final (Glossary …)"); the errata page carries the GEMP id, "<Title> (Errata)" (Decipher errata, label
    "errata (Decipher Glossary …)") or "<Title> (PC Errata)" (label "PC Errata (AR 2023 Appendix A)"); "<Title>
    (Original)" is a redirect to the printed page or a second printed page (label "printed (Decipher archive)", which
    wins). Cards without errata have one page (uid = GEMP id). The printed pages' uniqueness field is copied from the
    errata page (equal on all 491), so printed bullets come from Errata.wiki ("Errata face (• unique)", Appendix A
    "print: (non-unique)") and the faces: Beru Stew, Limited Resources, Spaceport Speeders, Innocent Scoundrel, Pride Of
    The Empire print none; Sandcrawler: Loading Bay / Droid Junkheap print one (GEMP •••). Only words count as a
    difference (quote style, ellipses, markup and the wiki's missing / spurious stat fields do not).
  - *Checked against the print:* every printed text was OCR'd (tesseract) on the wiki's Decipher-archive face of the card
    (hires 1497 px scan for lore) and scored against both texts; the 31 not clearly decided were read by eye: the wiki was
    right on all game text (OCR's three "GEMP" votes were misreads); fixes `WIKI_FIX` (Exposure "missing", Special
    Modifications _Millenium Falcon_, Field Promotion bold *leader*, Jek Porkins "On Red 6, also", Decipher's double quotes
    on the Sandcrawler sites and Dark Hours). Lore: the wiki's printed pages copy Decipher's card lists, not the print (Dark
    Hours prints "Interrogator", the page "Interceptor"; Imperial Blaster "packagedProduct"), so only the 10 lore texts a
    face confirms are taken (`LORE_OK`: Darth Vader "Servant of Emperor.", RA-7 "menial", Retractable Arm ".85", …).
    50 errata'd cards the wiki keeps no printed page for (or whose page copied the errata) were read off their faces
    (`PRINTED_SEEN`: Run Luke, Run!, the Jedi Pack / ECC cards, Wedge Antilles, Sense & Uncertain Is The Future, Kessel,
    Lord Maul, …; Desperate Times' Episode I disc), plus two non-errata printing details (Dantooine Base Operations
    “blown away.” / italic _site_, Plead My Case To The Senate "with with").
  - *Adapter:* `gemp_to_spec` builds the spec twice (GEMP card, and the card with the printed fields) and keeps the
    differing spec keys as `dc_printed` / `dc_errata`; `dc_printed_spec` (first thing in `spec_to_card`) puts the printed
    values on when `decipher_print` and English, for every field still equal to its errata value (an edited field is
    kept), before dc_bold / dc_ellipses run; the dc_* keys never reach the card. Editor: "As Decipher printed it" swaps the
    form between printed and errata text (`dcSwap`, app.js); a card opens with the printed text.
  - *Also:* dc_bold bolds a named agenda ("order agenda") on Political Effects and senate Objectives (Ascertaining The
    Truth, Plea To The Court, Plead My Case, My Lord, Is That Legal?; characters and Interrupts print it regular);
    corrections.json: Concentrate All Fire "for remainder of battle. Once per turn, you", Battle Deployment "present,
    that player's" / "from your Reserve Deck" (transcription, read on the DS2 archive faces); decipher_lines.json 4_17
    Asteroid Sanctuary holds the printed lines (the stored ones had GEMP's errata words).
  - **Checks:** card-dict md5 over all 8116 CARDS × en/ja: 528 change = the 514 cards (en) + 9 agenda cards + 9_3 / 9_92
    (corrections, en and ja) + 4_17 ja (dc_lines data); no PC / VS / OVS / Legacy card and no other Japanese card
    changes. Holotable renders md5-identical: 1_70, 1_283, 200_1, 223_40, 2_66 and 7_135 with the box off, Japanese
    2_66 / 1_13. decipher_lines hints: all 69 that applied before still apply (4_17 now too).
