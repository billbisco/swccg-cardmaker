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
