# Helper brief — Original Virtual Set transcription (shared by all helpers; Claude 2026-10-13)

Working directory: /home/claude/cardmaker (paths relative). Read cards/VS-SPEC.md (field spec incl. all "Additions")
and STANDARD.md first.

Models for the exact JSON shape: cards/vs6/17.json (Light character with icons), cards/vs6/15.json (Light alien),
cards/vs6/29.json (Dark character, pilot icon, "heading" field), cards/vs6/31.json (Imperial), cards/vs7/06.json
(droid with three stat boxes), cards/vs6/46.json (two affiliations, margin credits), cards/vs6/16.json and
cards/vs6/30.json (character weapons), cards/vs6/04.json (device), cards/vs6/05.json / cards/vs6/19.json (capitals),
cards/vs5/46.json (starfighter), cards/vs6/01.json / cards/vs6/26.json (effects), cards/vs6/38.json (Force icons),
cards/vs6/11.json / cards/vs6/36.json (immediate effects; "grabber": false when the banner has no grabber box, true
when an EFFECT banner has one), cards/vs6/07.json / cards/vs6/28.json (interrupts), cards/vs6/24.json /
cards/vs6/34.json (defensive shields), cards/vs6/20.json (margin credits), cards/vs4/10.json (site), cards/vs4/11.json
/ cards/vs4/40.json (objectives, front NN + back NNb slips), cards/vs4/30.json (vehicle), cards/vs4/14.json (creature
if present). Starting Effects: "slip_type": "Starting Effect".

For each slip NN you are given:
1. View src/slips/vsN/NN-*.png with the Read tool. Transcribe EXACTLY: wording, curly quotes ’ “ ”, dashes, •, ▲ ▼,
   inline icon tokens, *bold*, _italic_, USED:/LOST: lines separated by \n, stat boxes, deploy/forfeit, icon column
   top-to-bottom, scomp ring, banner text. Tokens: black square + green blade = {lightsaber}; red circle-slash
   letters = {alter} {control} {sense}; gold spoked wheel = {maintenance}; yellow pilot icon + number = {pilot:N};
   blue wheel = {independent}; black "EPISODE I" circle = {episode1}; grabber hand = {grabber}; Light/Dark Force
   icons = {light-force}/{dark-force}; the slip's own Virtual sphere used inline = {ovs}; an expansion symbol inline
   = {set:<name>} (anh, hoth, dagobah, cloudcity, jabbaspalace, se, endor, ds2, reflections2, reflections3,
   coruscant, theed, tatooine); round silver Republic crest = {icon:republic}; anything else {icon:description}.
   Column icons: pilot, warrior, nav, astromech, permanent-weapon, permanent-pilot, independent, presence (red box,
   battle-droid figure), episode1… (the coloured sphere at the bottom of the column is the set symbol, not an icon).
   A heading with extra words → "heading"; title/caption as the bottom strip prints them. Margin credits →
   margin_left / margin_right. If a crop's heading is cut off, take the title from the bottom strip and say so.
2. Base card from the wiki (API https://wiki.swccg.com/api.php, User-Agent "HolocronClaude/1.0 (helper)"): stub page
   "<Title> (V) (Virtual Set N: <Subtitle>)" (title without dots) names the base page; else the title without " (V)"
   and dots (if that page is an errata/Glossary version, use the "(Original)" page). Take lore, destiny, set
   (expansion), uniqueness from the base {{Card}}. Download the widest base scan to src/vsN/NN-<file> and any modern
   PC remake (V0-/V<N>-…gif, or Virtual Block VB…-pre.gif) to src/vsN/modern/NN-<file>. A 745 px scan may be an
   errata face — art only, note it. NEVER set art.src to a "decipher-archive" photo of the card on a white page / odd
   size (367×506): use a square-on 350/745 px scan of the same art for art.src (read lore/copyright off the photo).
3. LORE must match the printed card exactly (Bill 2026-10-13: "indistinguishable from the original"). Read the lore
   box on the base scan (and on a 745 px PC remake if one exists — the PC remakes keep the printed lore and bold) and
   correct the wiki: wording, curly quotes, italic ship names _…_, and BOLD keywords *…* — Decipher bolds
   characteristics in lore (leader, spy, smuggler, gambler, bounty hunter, scout, thief, information broker,
   gangster, assassin when bold, Enclosed, hologram, dejarik…); mark bold only when you can see it (the remaster
   renderer bolds characters' keywords itself — Bill 2026-10-13 — so do not infer bold on low-res cards). Record every correction.
4. Write cards/vsN/NN.json (ensure_ascii=False, indent 1) with "id": "vsN-NN", "virtual_set": N, "side", all spec
   fields. Never invent a value — null + a note. Copyright by base set: Premiere 1995; A New Hope / Hoth 1996;
   Dagobah / Cloud City "TM & © 1997 LUCASFILM LTD. TM, ® & © 1997 DECIPHER INC."; Jabba's Palace 1998 (Hoth-style
   line); Special Edition "© LUCASFILM LTD. & TM. TM, ® & © 1998 DECIPHER INC."; Endor 1999; Death Star II 2000;
   Reflections II 2000; Coruscant/Theed/Tatooine 2001 (SE-style line) — read it off the scan when legible.

Do not edit any other file. Report: NNs written, slip_type/card_type each, and anything odd (unreadable text,
unknown icons, slip text differing from the wiki stub, lore corrections, cut-off headings). For every card you name
in the report, give its wiki stub URL (https://wiki.swccg.com/wiki/…).
