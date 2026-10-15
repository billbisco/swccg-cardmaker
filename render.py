"""SWCCG card renderer: card JSON + template → PNG (1632×2220 print master, 745×1039 Holotable/GEMP).

Layout numbers come from Bardez's 600 DPI GIMP templates (wiki.swccg.com/wiki/Making_Custom_SWCCG_Cards):
the card area is 1343×1931 at (144,144) on a 1632×2220 black bleed. A Holotable image (745×1039) is that
card area at half scale with a ~37 px black border, so one render serves both.
"""
from __future__ import annotations
import base64, json, os, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = Path(os.environ.get("CARDMAKER_OUT") or ROOT / "out")
W, H = 1632, 2220

# Template geometry (x, y, w, h) in 1632×2220 space.
TEMPLATES = {
    "ds-character-imperial": {
        "frame": ("frames/ds-character-imperial.png", 144, 144),
        "art": (256, 666, 1121, 770),
        "title": (374, 200, 884, 90),
        "destiny": (1312, 213, 100, 84),
        "lore": (321, 377, 989, 193),
        "stats_y": 1506,
        "stats": [(305, 251), (613, 256), (924, 396)],   # (x, width): the three black stat boxes
        "game_text": (341, 1663, 971, 333),
        "deploy": (205, 1821, 45, 83),
        "forfeit": (205, 1927, 47, 85),
        "icon_slots": [(1352, 1643), (1352, 1749), (1352, 1855)],
        "set_icon_abs": (1358, 1933),
        "expansion_ring": (1380, 402),
        "copyright_x": 1404,
    },
    "ds-effect": {
        "frame": ("frames/ds-effect.png", 141, 147),
        "art": (254, 663, 1118, 765),
        "title": (398, 200, 779, 100),
        "destiny": (1308, 204, 104, 104),
        "lore": (321, 378, 989, 190),
        "card_type": (271, 1508, 1109, 61),
        "game_text": (320, 1667, 1000, 328),
        "banner_icon": (1292, 1492),
        "set_icon_abs": (1391, 1940), "set_icon_size": 64,
        "expansion_ring": (1381, 405),
        "copyright_x": 1404,
    },
    "ls-interrupt": {
        "frame": ("frames/ls-interrupt.png", 146, 145),
        "art": (256, 663, 1122, 754),
        "title": (398, 200, 880, 90),
        "destiny": (1312, 206, 100, 104),
        "lore": (321, 380, 1010, 180),
        "card_type": (268, 1505, 1089, 61),
        "game_text": (320, 1668, 1000, 326),
        "set_icon_abs": (1397, 1942), "set_icon_size": 60,
        "expansion_ring": (1381, 405),
        "copyright_x": 1416,
        "dark_text": True,
        "lore_indent": 0,
    },
    "ls-character-alien-rebel": {   # Bardez's Multiple Affiliation frame with the Alien + Rebel discs (A New Hope Chewbacca)
        "frame": ("frames/ls-character-alien-rebel.png", 143, 143),
        "art": (259, 656, 1130, 763),
        "title": (545, 205, 780, 90),
        "destiny": (1318, 196, 108, 108),
        "lore": (300, 395, 1040, 170),
        "stats_y": 1504,
        "stats": [(300, 275), (605, 285), (930, 420)],
        "game_text": (340, 1668, 990, 326),
        "deploy": (205, 1827, 45, 78),
        "forfeit": (205, 1931, 45, 84),
        "icon_slots": [(1367, 1653), (1367, 1757)],
        "set_icon_abs": (1372, 1935),
        "expansion_ring": (1385, 404),
        "expansion_size": 68,
        "copyright_x": 1428,
        "dark_text": True,
    },
    "ls-character-alien": {
        "frame": ("frames/ls-character-alien.png", 69, 131),
        "art": (259, 656, 1130, 763),
        "title": (400, 200, 900, 90),
        "destiny": (1318, 196, 108, 108),
        "lore": (300, 380, 1040, 170),
        "stats_y": 1504,
        "stats": [(300, 275), (605, 285), (930, 420)],
        "game_text": (340, 1668, 990, 326),
        "deploy": (205, 1827, 45, 78),
        "forfeit": (205, 1931, 45, 84),
        "icon_slots": [(1367, 1653), (1367, 1757)],
        "set_icon_abs": (1372, 1935),
        "expansion_ring": (1360, 396),
        "copyright_x": 1428,
        "dark_text": True,
    },

    "ds-character-alien": {
        "frame": ("frames/ds-character-alien.png", 144, 147),
        "art": (246, 669, 1137, 770), "title": (402, 208, 884, 90), "destiny": (1311, 209, 100, 99),
        "lore": (321, 380, 989, 193), "stats_y": 1509, "stats": [(305, 252), (613, 257), (924, 397)],
        "stats_wide": (613, 708), "game_text": (341, 1666, 971, 333),
        "deploy": (205, 1824, 45, 83), "forfeit": (205, 1930, 47, 85),
        "icon_slots": [(1353, 1650), (1353, 1756), (1353, 1862)], "set_icon_abs": (1359, 1936),
        "expansion_ring": (1380, 405), "copyright_x": 1404,
    },
    "ds-character-droid": {
        "frame": ("frames/ds-character-droid.png", 144, 147),
        "art": (246, 669, 1137, 770), "title": (402, 208, 884, 90), "destiny": (1311, 209, 100, 99),
        "lore": (321, 380, 989, 193), "stats_y": 1509, "stats": [(305, 252), (613, 257), (924, 397)],
        "stats_wide": (613, 708), "game_text": (341, 1666, 971, 333),
        "deploy": (205, 1824, 45, 83), "forfeit": (205, 1930, 47, 85),
        "icon_slots": [(1353, 1650), (1353, 1756), (1353, 1862)], "set_icon_abs": (1359, 1936),
        "expansion_ring": (1380, 405), "copyright_x": 1404,
    },
    "ds-interrupt": {
        "frame": ("frames/ds-interrupt.png", 141, 147),
        "art": (247, 663, 1134, 765), "title": (397, 204, 779, 100), "destiny": (1310, 207, 102, 99),
        "lore": (316, 378, 989, 193), "card_type": (269, 1507, 1091, 61), "game_text": (316, 1666, 997, 328),
        "banner_icon": (1292, 1495), "set_icon_abs": (1391, 1940), "set_icon_size": 64, "expansion_ring": (1381, 405), "copyright_x": 1404,
    },
    "ds-weapon": {
        "frame": ("frames/ds-weapon.png", 150, 148),
        "art": (251, 662, 1133, 763), "title": (405, 210, 779, 100), "destiny": (1315, 208, 100, 99),
        "lore": (324, 380, 989, 193), "card_type": (267, 1505, 1105, 61), "game_text": (318, 1669, 997, 328),
        "set_icon_abs": (1391, 1940), "set_icon_size": 64, "expansion_ring": (1380, 405), "copyright_x": 1404,
    },
    "ds-shield": {
        "frame": ("frames/ds-shield-hybrid.png", 141, 147),
        "art": (254, 663, 1118, 765), "title": (398, 200, 779, 100), "destiny": (1308, 204, 104, 104),
        "lore": (321, 378, 989, 190), "card_type": (262, 1506, 1110, 61), "game_text": (314, 1665, 997, 328),
        "banner_icon": (1292, 1492), "set_icon_abs": (1391, 1940), "set_icon_size": 64, "expansion_ring": (1374, 405), "copyright_x": 1404,
    },
    "ls-character-rebel": {
        "frame": ("frames/ls-character-rebel.png", 135, 131),
        "art": (259, 656, 1130, 763), "title": (400, 200, 900, 90), "destiny": (1318, 196, 108, 108),
        "lore": (300, 380, 1040, 170), "stats_y": 1504, "stats": [(300, 275), (605, 285), (930, 420)],
        "stats_wide": (605, 745), "game_text": (340, 1668, 990, 326),
        "deploy": (205, 1827, 45, 78), "forfeit": (205, 1931, 45, 84),
        "icon_slots": [(1367, 1653), (1367, 1757)], "set_icon_abs": (1372, 1935),
        "expansion_ring": (1381, 405), "copyright_x": 1428, "dark_text": True,
    },
    "ls-character-droid": {
        "frame": ("frames/ls-character-droid.png", 144, 133),
        "art": (246, 659, 1139, 767), "title": (405, 193, 900, 92), "destiny": (1318, 197, 105, 105),
        "lore": (318, 367, 1047, 197), "stats_y": 1502, "stats": [(305, 260), (620, 260), (940, 400)],
        "stats_wide": (620, 720), "game_text": (354, 1660, 932, 326),
        "deploy": (201, 1832, 48, 80), "forfeit": (201, 1936, 48, 82),
        "icon_slots": [(1367, 1653), (1367, 1757)], "set_icon_abs": (1372, 1935),
        "expansion_ring": (1380, 397), "expansion_size": 70, "copyright_x": 1428, "dark_text": True, "stats_wide_fill": "#c9c9cb",
        "stats_row3": ("frames/ls-stats-row3.png", 285, 1488), "stats_row3_boxes": [(311, 269), (630, 263), (944, 403)],
    },
    "ls-shield": {
        "frame": ("frames/ls-shield-hybrid.png", 146, 141),
        "art": (244, 661, 1143, 755), "title": (401, 206, 779, 100), "destiny": (1313, 202, 104, 104),
        "lore": (320, 376, 1019, 193), "card_type": (268, 1505, 1109, 61), "game_text": (317, 1658, 997, 328),
        "set_icon_abs": (1397, 1942), "set_icon_size": 60, "expansion_ring": (1381, 405), "copyright_x": 1416, "dark_text": True, "lore_indent": 0,
    },
    "ls-effect": {
        "frame": ("frames/ls-effect.png", 146, 141),
        "art": (244, 661, 1143, 755), "title": (401, 206, 779, 100), "destiny": (1313, 202, 104, 104),
        "lore": (320, 376, 1019, 193), "card_type": (271, 1505, 1109, 61), "game_text": (320, 1658, 997, 328),
        "banner_icon": (1292, 1492), "set_icon_abs": (1397, 1942), "set_icon_size": 60, "expansion_ring": (1378, 410), "expansion_size": 70,
        "copyright_x": 1416, "dark_text": True, "lore_indent": 0,
    },
    "ls-weapon": {
        "frame": ("frames/ls-weapon.png", 146, 145),
        "art": (254, 664, 1138, 751), "title": (401, 206, 779, 100), "destiny": (1312, 205, 106, 106),
        "lore": (320, 376, 1019, 193), "card_type": (271, 1505, 1109, 61), "game_text": (320, 1658, 997, 328),
        "set_icon_abs": (1397, 1942), "set_icon_size": 60, "expansion_ring": (1381, 407), "copyright_x": 1416, "dark_text": True, "lore_indent": 0,
    },
    "ls-starship-starfighter": {   # Bardez "LS - Starship" with his starfighter type icon in the top-left ring
        "frame": ("frames/ls-starship-starfighter.png", 65, 73),
        "art": (255, 662, 1137, 709),
        "title": (398, 200, 880, 90),
        "destiny": (1321, 208, 99, 101),
        "lore": (321, 385, 1010, 185),
        "card_type": (270, 1462, 1114, 61),
        "stats_y": 1582,
        "stats": [(270, 270), (600, 340), (985, 385)],
        "game_text": (349, 1729, 982, 279),
        "deploy": (203, 1835, 59, 81),
        "forfeit": (208, 1929, 47, 85),
        "icon_slots": [(1357, 1722), (1357, 1821)],
        "set_icon_abs": (1363, 1926),
        "expansion_ring": (1381, 405),
        "copyright_x": 1416,
        "dark_text": True,
        "lore_indent": 0,
        "scomp": (184, 1694),
        "ctype_spacing": 3,
    },
    "ds-starship-starfighter": {   # Bardez "DS - Starship.xcf" frame layer + his TIE type icon; boxes measured from the frame PNG
        "frame": ("frames/ds-starship-starfighter.png", 139, 148),
        "art": (241, 667, 1134, 710),
        "title": (398, 200, 880, 90),
        "destiny": (1305, 210, 100, 100),
        "lore": (316, 390, 985, 178),
        "card_type": (262, 1462, 1100, 61),
        "stats_y": 1588,
        "stats": [(268, 262), (581, 330), (962, 381)],
        "game_text": (344, 1732, 925, 265),
        "deploy": (199, 1826, 45, 82),
        "forfeit": (199, 1932, 46, 84),
        "icon_slots": [(1356, 1722), (1356, 1822)],
        "set_icon_abs": (1363, 1926),
        "expansion_ring": (1382, 405),
        "copyright_x": 1416,
        "scomp": (170, 1694),
        "ctype_spacing": 3,
    },
    "ls-vehicle": {   # Bardez "LS - Vehicle.xcf" frame layer ("Vehicle PC"); boxes as the LS starship (same card geometry)
        "frame": ("frames/ls-vehicle.png", 145, 146),
        "art": (246, 660, 1141, 716), "title": (398, 200, 880, 90), "destiny": (1321, 208, 99, 101), "lore": (321, 385, 1010, 185),
        "card_type": (270, 1462, 1114, 61), "stats_y": 1582, "stats": [(270, 270), (600, 340), (985, 385)],
        "game_text": (349, 1729, 982, 279), "deploy": (203, 1835, 59, 81), "forfeit": (208, 1929, 47, 85),
        "icon_slots": [(1357, 1722), (1357, 1821)], "set_icon_abs": (1363, 1926), "expansion_ring": (1381, 405),
        "copyright_x": 1416, "dark_text": True, "lore_indent": 0, "scomp": (184, 1694), "ctype_spacing": 3,
    },
    "ds-vehicle": {   # Bardez "DS - Vehicle.xcf" frame layer; boxes measured from the frame PNG
        "frame": ("frames/ds-vehicle.png", 143, 147),
        "art": (245, 666, 1134, 710), "title": (398, 200, 880, 90), "destiny": (1309, 209, 100, 100), "lore": (320, 390, 985, 178),
        "card_type": (262, 1462, 1100, 61), "stats_y": 1587, "stats": [(272, 262), (585, 330), (966, 381)],
        "game_text": (348, 1731, 925, 265), "deploy": (203, 1825, 45, 82), "forfeit": (203, 1931, 46, 84),
        "icon_slots": [(1353, 1720), (1353, 1826)], "set_icon_abs": (1363, 1926), "expansion_ring": (1371, 404),
        "copyright_x": 1416, "scomp": (170, 1694), "ctype_spacing": 3,
    },
    "creature": {   # Bardez "Creature.xcf" frame layer (one frame for both sides); boxes measured from the frame PNG
        "frame": ("frames/creature.png", 145, 146),
        "art": (249, 694, 1139, 686), "title": (373, 215, 841, 80), "destiny": (1329, 215, 104, 104), "lore": (324, 420, 987, 178),
        "stats_y": 1583, "stats": [(305, 350), (706, 622)],
        "game_text": (352, 1727, 925, 270), "deploy": (208, 1827, 45, 79), "forfeit": (206, 1930, 46, 85),
        "icon_slots": [(1353, 1651), (1353, 1756)], "set_icon_abs": (1363, 1926), "expansion_ring": (1375, 400),
        "copyright_x": 1416
    },
    "objective": {   # Bardez "DS - Objective.xcf" template, recoloured to the PC two-tone purple (make_objective_frames.py); black text box, white text
        "frame": ("frames/objective.png", 67, 73),
        "art": (236, 380, 1150, 855), "title": (382, 204, 878, 95), "destiny": (1310, 204, 105, 107),
        # text box (black) 260..1377 × 1324..2003; the slip's text starts 60 px in and its longest lines run to within
        # ~10 px of the right edge (62 px AGCn, 64 px pitch), so the box reaches almost to the edge and the fitter grows to it
        "game_text": (300, 1350, 1070, 652), "gt_lh_add": 2,
        # set sphere in the purple margin at the text box's bottom-right corner, as the slip prints it (centre 39 px right
        # of the box's right edge, 7 px above its bottom; 66 px across)
        "set_icon_abs": (1384, 1964), "set_icon_size": 66,
        "copyright_x": 1416, "no_type": True, "gt_grow": True,
    },
    "objective-ls": {   # Bardez "LS - Epic Objective.xcf" frame + Objective icon, re-hued to the Endor-era purple (make_objective_frames.py)
        "frame": ("frames/objective-ls.png", 0, 0),
        "art": (246, 378, 1148, 886), "title": (382, 204, 878, 95), "destiny": (1330, 204, 111, 113),
        "game_text": (305, 1358, 1085, 646), "gt_lh_add": 2,   # text box (white) 267..1395 × 1332..2005
        "set_icon_abs": (1401, 1965), "set_icon_size": 66,
        "copyright_x": 1416, "dark_text": True, "no_type": True, "gt_grow": True,
    },
    "ls-admirals-order": {   # Bardez "LS - Admiral's Order.xcf" Template layer: title bar + black text box over full-bleed art
        "frame": ("frames/ls-admirals-order.png", 0, 0),
        "art": (146, 146, 1344, 1929), "title": (400, 206, 900, 100), "destiny": (1330, 204, 111, 110),
        "game_text": (292, 1528, 1064, 464), "gt_ink": "#fff", "gt_grow": True,
        "set_icon_abs": (1430, 1972), "set_icon_size": 60, "expansion_ring": (1379, 400), "expansion_size": 70,
        "dark_text": True, "no_type": True, "no_copyright": True,
    },
    # Decipher printed both sides' Admiral's Orders in the same frame (Nothing Can Get Through Our Shield = Taking Them With Us)
    "epic-event": {   # Bardez "DS - Epic Event.xcf" (Epic Event icon + Epic Objective frame + text box), recoloured to the
        # Reflections III purple the slips print (hue .773 / sat .66 / val .45; make via make_objective_frames.recolour)
        "frame": ("frames/epic-event.png", 0, 0),
        "art": (238, 372, 1146, 866), "title": (396, 206, 880, 100), "destiny": (1310, 203, 108, 108),
        "game_text": (290, 1340, 1060, 650), "gt_ink": "#fff", "gt_grow": True,
        "set_icon_abs": (1405, 1950), "set_icon_size": 62, "expansion_ring": (1390, 373), "expansion_size": 70,
        "copyright_x": 1404, "dark_text": False, "no_type": True, "credit_mx": (180, 1411), "credit_ink": "#000",
    },
    # printed cards with no lore box (Jedi Tests, Reflections II combo cards) carry a TALL slip (VS12 #13, #42): Bardez's
    # Epic Objective frame with the art window shortened, the slip's banner and a tall text box below it
    "ls-jeditest-tall": {
        "frame": ("frames/ls-jeditest-tall.png", 0, 0),
        "art": (240, 372, 1146, 716), "title": (396, 206, 880, 100), "destiny": (1310, 203, 108, 108),
        "card_type": (271, 1170, 1109, 61), "game_text": (300, 1318, 1040, 666), "gt_grow": True,
        "set_icon_abs": (1405, 1950), "set_icon_size": 62, "expansion_ring": (1390, 373), "expansion_size": 70,
        "copyright_x": 1404, "dark_text": True, "credit_mx": (180, 1411), "credit_ink": "#fff",
    },
    "ds-effect-tall": {
        "frame": ("frames/ds-effect-tall.png", 0, 0),
        "art": (240, 372, 1146, 716), "title": (396, 206, 880, 100), "destiny": (1310, 203, 108, 108),
        "card_type": (271, 1170, 1109, 61), "game_text": (292, 1340, 1056, 650), "gt_grow": True,
        "set_icon_abs": (1405, 1950), "set_icon_size": 62, "expansion_ring": (1390, 373), "expansion_size": 70,
        "copyright_x": 1404, "dark_text": False, "credit_mx": (180, 1411),
    },
    # Landscape location (site). Bardez "Location - Site.xcf": doc 2220×1632, frame layer 2073×1497 whose card
    # area (1931×1343) sits at (70,68) inside it → frame at (74,76) puts the card at (144,144) like the portraits.
    # The frame is assembled per card (force icons, packed icon boxes, scomp rings) by loc_frame().
    "loc-site": {
        "landscape": True,
        "frame_xcf": "site",
        "frame_off": (74, 76),
        "art": (262, 458, 1695, 713),              # frame hole (188,382)-(1883,1095) + offset
        "ls_bar": (527, 1224, 90),                 # x0 of the Light title bar text area, y, h (frame 453,1148)
        "ls_bar_x1": 1657,                         # bar end when no icon boxes (frame 1583)
        "ds_bar": (580, 313, 1112, 90),            # Dark title bar (black) x, y, w, h  (frame 506,237)
        "ls_text": (250, 1344, 1719, 86),           # the box interior (frame 1268-1352)
        "ds_text": (250, 195, 1719, 99),
        "ls_slot0": 1855, "ds_slot0": 216,          # frame x of the centre of the right-most Light / left-most Dark icon box
        "slot_y": 1155, "slot_pitch": 111,
        "ls_scomp": (1790, 1142), "ds_scomp": (181, 236),
        "ls_force": (140, 1105), "ds_force": None,  # frame coords of the light-saber glow crop (DS = rotated mirror)
        "set_icon_abs": (1984, 1363),
        "expansion_ring": (1991, 453), "expansion_size": 50,
        "copyright": (2002, 560, 36, 600),
        "caption_y": 1494,
    },
    # Portrait system. Bardez "Location - System.xcf": no silver frame; the scan fills the card area and the two
    # bar assemblies (layer at (235,189)) sit on top. Light half at the bottom, Dark half rotated at the top.
    "loc-system": {
        "system": True,
        "frame_png": "frames/loc-system.png", "frame_off": (235, 189),
        "art": (144, 144, 1343, 1931),
        "ls_bar": (520, 1752, 660, 86), "ds_bar": (473, 377, 638, 90),
        "ls_text": (261, 1889, 1116, 140), "ds_text": (261, 210, 1116, 139),
        "ls_icon": (1232, 1797), "ds_icon": (406, 421),          # centres of the black icon boxes
        "ls_parsec": (1298, 1752, 89, 86), "ds_parsec": (250, 380, 88, 86),
        "ls_force": (230, 1700), "ds_force": (1110, 330),
        "set_icon_abs": (1410, 1923), "set_icon_size": 72,
        "system_ring": (138, 186, 52),
        "copyright_split": ((176, 1686, 36, 420), (1424, 1686, 36, 420)),   # Lucasfilm left / Decipher right margin (Dagobah)   # the printed systems' expansion sphere, top-left margin (Hoth, Bespin scans)
        "caption_y": 2082,
    },
}


# Reflections Gold "wide vision" (Decipher's cancelled last set; Bill 2026-10-15): Effects / Interrupts printed landscape,
# full art, gold credit coins right of the text box, the set's gold sphere under the destiny lobe. Frames from Bardez's
# [Horizontal] XCFs (make_rg_frames.py); text positions from Andy Talaga's reconstructions (wiki "Reflections Gold").
_RG = {"wide": True, "art": (134, 138, 1952, 1356), "title": (500, 222, 860, 100), "destiny": (1850, 216, 108, 108),
       "card_type": (1180, 246, 580, 56), "ctype_size": 44, "ctype_spacing": 5, "game_text": (330, 1162, 1585, 214),
       "gt_size": 56, "expansion_ring": (1902, 403), "expansion_size": 68, "no_copyright": True,
       "coins": (1952, 1370, 39), "caption_y": 1532}
for _side, _ink in (("ls", True), ("ds", False)):
    for _kind in ("interrupt", "effect"):
        TEMPLATES[f"rg-{_side}-{_kind}"] = dict(_RG, frame=(f"frames/rg-{_side}-{_kind}.png", 0, 0), dark_text=_ink)


# Dark Side wide weapon (Bill 2026-10-15: precedent = Maul's Double-Bladed Lightsaber, Reflections III, printed landscape)
TEMPLATES["ds-weapon-wide"] = {
    "wide": True, "frame": ("frames/ds-weapon-wide.png", 0, 0), "art": (134, 138, 1952, 1356),
    "title": (430, 222, 820, 110), "card_type": (1230, 244, 560, 64), "ctype_size": 52, "ctype_spacing": 4,
    "destiny": (1859, 225, 110, 110), "lore": (360, 404, 1480, 140), "lore_x": (360, 1840, 60, 0, 0.0),
    "game_text": (350, 1172, 1550, 196), "gt_size": 58, "expansion_ring": (1932, 418), "expansion_size": 66,
    "no_copyright": True, "caption_y": 1532, "dark_text": False,
}


# Decipher's printed creatures (Worrt, Bog-wing): black title and the banner (GUARD CREATURE) — card maker; the VS
# remasters keep "creature" as approved (white title, empty banner)
TEMPLATES["creature-dc"] = dict(TEMPLATES["creature"], card_type=(271, 1466, 1109, 61), title_ink="#000", ctype_ink="#000")


def is_wide(t: dict) -> bool:
    """Landscape canvas (2220x1632): locations (site) and the Reflections Gold wide cards."""
    return bool(t.get("landscape") or t.get("wide"))


# Optional era templates (Bill 2026-10-13): the red→cyan fade the Original Virtual Remaster slips used for Defensive
# Shields (make_shield_fade.py). The hybrid (hard cut) above stays the primary shield template; a card opts in with
# "shield_style": "fade" (build_vs.py sets it for the Original Virtual sets).
TEMPLATES["ls-jeditest-epic"] = dict(TEMPLATES["ls-effect"], frame=("frames/ls-jeditest-epic.png", 0, 0))   # Jedi Test frame (olive) with the slip's purple Epic Event foot
TEMPLATES["ds-admirals-order"] = dict(TEMPLATES["ls-admirals-order"])   # Decipher printed both sides' Admiral's Orders in one frame
# Decipher's own Defensive Shield frames (all-cyan Light / its Dark twin, shield icon) for the card maker's printed cards
TEMPLATES["ls-shield-dc"] = dict(TEMPLATES["ls-shield"], frame=("frames/ls-shield.png", 148, 142))
TEMPLATES["ds-shield-dc"] = dict(TEMPLATES["ds-shield"], frame=("frames/ds-shield.png", 144, 146))
# Devices (card maker): the weapon frames with Bardez's Device type icon (DS / LS - Device.xcf) — Deflector Shield Generators
TEMPLATES["ds-device"] = dict(TEMPLATES["ds-weapon"], frame=("frames/ds-device.png",) + TEMPLATES["ds-weapon"]["frame"][1:])
TEMPLATES["ls-device"] = dict(TEMPLATES["ls-weapon"], frame=("frames/ls-device.png",) + TEMPLATES["ls-weapon"]["frame"][1:])
TEMPLATES["ds-shield-fade"] = dict(TEMPLATES["ds-shield"], frame=("frames/ds-shield-fade.png", 0, 0))
TEMPLATES["ls-shield-fade"] = dict(TEMPLATES["ls-shield"], frame=("frames/ls-shield-fade.png", 0, 0))
# Virtual Block Dark shields (No Escape (V)): Decipher's Dark shield frame, cyan fading to red at the foot
TEMPLATES["ds-shield-vb"] = dict(TEMPLATES["ds-shield-dc"], frame=("frames/ds-shield-vb.png",) + TEMPLATES["ds-shield-dc"]["frame"][1:])

ICON_FILES = {
    # column icons: the PC's own Game Aid icons, frame included (COL_ prefix = drawn without the Bardez icon box)
    "pilot": "icons/col-pilot-dark.png", "warrior": "icons/col-warrior.png", "pilot-light": "icons/col-pilot-light.png", "warrior-light": "icons/col-warrior.png",
    "alter": "icons/VS-icon-immune-alter.png", "control": "icons/VS-icon-immune-control.png",
    "sense": "icons/VS-icon-immune-sense.png", 
    "grabber": "icons/grabber-fist.png", "pilotpower": "icons/VS-icon-pilot-power-x.png", "pilotpower-dark": "icons/VS-icon-pilot-power-x-dark.png",
    "lightsaber": "icons/inline-permanent-weapon.png", "permanent-weapon": "icons/inline-permanent-weapon.png",
    "republic": "icons/col-republic.png", "republic-square": "icons/inline-republic-square.png", "maintenance": "icons/inline-maintenance.png", "nav": "icons/inline-nav.png",
    "astromech": "icons/astromech-bardez.png",
    "independent": "icons/inline-independent.png", "presence": "icons/col-presence.png",
    "republic-crest": "icons/inline-republic-crest.png",
    "ds2": "icons/set-ds2-decipher.png",   # Death Star II icon in the column (Luke Skywalker, Rebel Scout (V))
    "light-force": "icons/inline-force-light.png", "dark-force": "icons/inline-force-dark.png",   # Game Aid g036 / g050 (Imperial Decree (V))
    "episode1": "icons/inline-episode1.png",   # Game Aid g033 (Hopping Mad (V): "non-[Episode I] C-3PO")   # the Republic affiliation icon itself (The Emperor (V): "Gains [Republic] at opponent's Senate")   # Presence = Game Aid g013 (droid on red), as on IG-88
    "permanent-pilot": "icons/col-pilot-dark.png", "permanent-pilot-light": "icons/col-pilot-light.png",   # same helmet icon as Pilot on the printed cards
    # Players Committee column icons (framed): wiki 180 px / PC Game Aid sheet (Feb 2024) / cut from PC scans (Bill 2026-10-15)
    "selective-creature": "icons/col-selective-creature.png", "independent-starship": "icons/col-independent-starship.png",
    "trade-federation": "icons/col-trade-federation.png", "clone-army": "icons/col-clone-army.png",
    "separatist": "icons/col-separatist.png", "resistance": "icons/col-resistance.png", "first-order": "icons/col-first-order.png",
    "vader": "icons/col-vader.png", "setup": "icons/col-setup.png",
}
RING_DISCS = {   # discs printed under the expansion sphere (or in its place when the card has none)
    "episode1": "icons/ep1-disc.png", "episode7": "icons/ep7-disc.png",
    "sidious": "icons/disc-sidious.png", "skywalker": "icons/disc-skywalker.png",
}


# lore typography (Bill 2026-10-13: lore must break and weigh as on the printed card) — tuned on printed 745 px scans
LORE_CSS = {"ff": "AGLightCn", "fs": 58, "ls": 0.25, "lh": 60, "pt": 4, "ind": 60}
# where the printed lore text starts and how far right it may run (card px), measured on 46 printed 745 px scans:
# Dark frames' lore window runs to x≈1349, Light ones' to ≈1366–1378; text starts at x≈319 (Dark) / 326 (Light)
# fitted (fit on 26 Dark / 21 Light printed cards: line counts and line ends): (text left, right limit, first-line
# indent, first-line cut for the window's bevelled corner, tracking)
LORE_X = {"Dark": (319, 1270, 90, 0, 0.0), "Light": (326, 1290, 75, 40, 0.0)}   # 16/26 Dark, 17/21 Light exact

_EDGE_CACHE: dict = {}


def stat_boxes(t: dict, n: int):
    """The stat boxes' interiors (x, width) as painted in the template's frame, measured on a row through their middle
    (Bill 2026-10-13: the text must sit in the printed boxes as on the Decipher cards). Dark frames: black wells;
    Light frames: grey wells right of a dark bevel. Falls back to the template's own numbers."""
    key = (t["frame"], t["stats_y"])
    if key not in _EDGE_CACHE:
        fr, fx, fy = t["frame"]
        c = Image.new("RGBA", (1632, 2220), (0, 0, 0, 255)); c.alpha_composite(Image.open(ASSETS / fr).convert("RGBA"), (fx, fy))
        import numpy as np
        a = np.array(c.convert("L")).astype(int)
        y = t["stats_y"] + 34
        row = a[y - 4:y + 5].mean(0)
        boxes = []
        if row[t["stats"][0][0] + 40] < 40:          # dark wells
            run = None
            for x in range(200, 1450):
                if row[x] < 30 and run is None: run = x
                if row[x] >= 30 and run is not None:
                    if x - run > 120: boxes.append((run, x - run))
                    run = None
        else:                                        # light wells: grey run (150–215) after a dark bevel (< 150)
            x = 200
            while x < 1430:
                if row[x] < 150:
                    j = x
                    while j < 1430 and row[j] < 160: j += 1
                    k = j
                    while k < 1450 and (150 <= row[k] <= 215 or (k + 6 < 1450 and (150 <= row[k + 6] <= 215))): k += 1
                    if k - j > 120:
                        boxes.append((j, k - j)); x = k; continue
                    x = j
                x += 1
        _EDGE_CACHE[key] = boxes if len(boxes) >= 2 else None
    b = _EDGE_CACHE[key]
    return b[:n] if b and len(b) >= n else None


def data_uri(path: Path) -> str:
    mime = "font/otf" if path.suffix == ".otf" else "image/png" if path.suffix == ".png" else "image/gif"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def icon_img(name: str, h: int = 64) -> str:
    return f'<img class="gt-icon" src="{data_uri(ASSETS / ICON_FILES[name])}" style="height:{h}px">'


card_ctx: dict = {}   # set by render() so tokens can see the card (virtual_set for {ovs})


def game_text_html(text: str) -> str:
    """{pilot:2} → pilot-power icon + number; {alter} {control} {sense} {maintenance} {grabber} {lightsaber} → icons.
    ▲ / ▼ (PC shorthand triangles) pass through as text. *bold* → bold."""
    out = []
    pos = 0
    for m in re.finditer(r"\{([\w-]+)(?::([^}]*))?\}", text):
        out.append(esc(text[pos:m.start()]))
        name, arg = m.group(1), m.group(2)
        if name == "pilot":   # Dark Side cards print the DS (TIE pilot) icon, Light Side the Rebel one (Bill 2026-10-12)
            out.append(icon_img("pilotpower-dark" if card_ctx.get("side") == "Dark" else "pilotpower") + f" {esc(arg or '')}")
        elif name in ("alter", "control", "sense"):
            # the slips' red "no" circle with the letter: drawn (transparent), not a pasted raster
            out.append(f'<span class="noicon"><span class="nol">{name[0].upper()}</span></span>')
        elif name == "icon" and arg in ("maintenance-star", "maintenance-skull", "maintenance-flag"):
            # Decipher's maintenance-cost glyphs, cut from the Remaster sheet at 1200 DPI (black on transparent)
            g = {"maintenance-star": "glyph-star", "maintenance-skull": "glyph-skull", "maintenance-flag": "glyph-flag"}[arg]
            hpx = {"glyph-star": 46, "glyph-skull": 60, "glyph-flag": 48}[g]   # the flag (VS16 Jedi Survivor) cut at 1200 DPI   # the star is cap-height, the skull a little taller than the x-height+descender
            out.append(f'<img class="gt-icon" src="{data_uri(ASSETS / f"icons/{g}.png")}" style="height:{hpx}px;vertical-align:{-4 if g == "glyph-star" else -10}px;margin-right:{6 if g == "glyph-star" else 0}px{";filter:invert(1)" if not card_ctx.get("_dark_text") else ""}">')
        elif name == "ovs":   # the slip prints its own Original Virtual set sphere inline (= "the (V) version of")
            out.append(f'<img class="gt-icon" src="{data_uri(ASSETS / f"icons/ovs-set-{arg or card_ctx.get('virtual_set', 3)}.png")}" style="height:56px">')
        elif name == "vset":   # VS17 slips: the Committee's diamond set mark with a number = "Virtual Set N's" (e.g. {vset:9})
            svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 86">'
                   '<polygon points="50,3 97,43 50,83 3,43" fill="#111" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>'
                   '<polyline points="12,47 50,76 88,47" fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="miter"/>'
                   f'<text x="50" y="53" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-weight="700" font-size="{40 if len(arg or "") < 2 else 36}" fill="#fff">{esc(arg or "")}</text></svg>')
            out.append(f'<img class="gt-icon" src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}" style="height:60px;vertical-align:-12px">')
        elif name == "ga":   # a Players Committee Game Aid icon (Feb 2024 reference sheet), e.g. {ga:separatist}
            gf = ASSETS / f"icons/pc-gameaid-x4/{arg}.png"
            out.append(f'<img class="gt-icon" src="{data_uri(gf)}" style="height:56px">' if gf.exists() else esc(f"[{arg}]"))
        elif name in ("vb", "pcset"):   # inline set marks: [Virtual Block 4] -> {vb:4}, [Set 13] -> {pcset:13}
            out.append(inline_set_mark(("vb:" if name == "vb" else "pc:") + (arg or "")))
        elif name == "set":   # expansion-set symbol inline, e.g. {set:anh} = "the A New Hope R2-D2"
            sf = ASSETS / f"icons/set-{arg}-decipher.png"   # Decipher's own sphere (Bill 2026-10-14)
            if not sf.exists():
                sf = ASSETS / f"icons/set-{arg}-grainy.png"
            out.append(f'<img class="gt-icon" src="{data_uri(sf)}" style="height:56px;border-radius:50%;box-shadow:0 0 0 3px #000">')
        elif name == "icon" and arg in ICON_FILES:   # {icon:pilot}, {icon:warrior} …
            out.append(icon_img(arg))
        elif name == "icon" and (ASSETS / f"icons/pc-gameaid-x4/{arg}.png").exists():
            out.append(f'<img class="gt-icon" src="{data_uri(ASSETS / f"icons/pc-gameaid-x4/{arg}.png")}" style="height:56px">')
        elif name in ICON_FILES:
            out.append(icon_img(name))
        else:   # unknown code: print it as typed rather than fail the card
            out.append(esc(m.group(0)))
        pos = m.end()
    out.append(esc(text[pos:]))
    html = "".join(out)
    html = html.replace("•", '<span class="dot">•</span>')
    html = re.sub(r"\*(.+?)\*", r"<b>\1</b>", html, flags=re.S)
    html = re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"<i>\1</i>", html, flags=re.S)   # italics may span the slip's line breaks
    html = html.replace("▲", "<span class=tri>▲</span>").replace("▼", "<span class=tri>▼</span>")
    return html.replace("\n", "<br>").replace("¶", "<br>")   # ¶ = a paragraph break that keeps normal wrapping (card maker)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def margin_ink(frame_path, x: int, top: int, bot: int) -> str:
    """Credit ink by the margin it sits on, as the slips print it (Bill 2026-10-13: Endor Shield (V), Mara Jade (V),
    Stinger (V)): black on the bright margins and on red ones (Light frames, Dark Effects / Interrupts), white on the
    darker grey, blue and green Dark frames (characters, starships)."""
    try:
        import numpy as np
        im = Image.open(frame_path).convert("RGBA").crop((x - 10, top, x + 50, bot))
        al = np.array(im)[:, :, 3] > 200
        if not al.any():
            return "#fff"
        h, s_, v = np.median(np.array(im.convert("RGB").convert("HSV")).astype(float)[al] / 255, axis=0)
        red = (h < 0.08 or h > 0.92) and s_ > 0.3
        return "#000" if v > 0.7 or red else "#fff"
    except Exception:
        return "#fff"


def loc_title(card: dict, bar: str = "Light") -> str:
    """Location bar title as the Remaster slips letter it (Bill 2026-10-14): AG Bold Condensed caps. The uniqueness
    dot / diamond is red on the bar of the card's own side and in the bar's text colour on the other (VS13 slips:
    Light cards print a white dot on the Dark bar, Dark cards a black dot on the Light bar)."""
    t = card.get("card_type") or card["title"]
    h = esc_i(t)
    cls = "dot" if bar == card.get("side", "Light") else "dot plain"
    return '<span class="lt">' + re.sub(r"^([•◊]+)", lambda m: f'<span class="{cls}">{m.group(1)}</span>', h) + '</span>'


def title_html(s: str) -> str:
    """esc_i() for card titles: Fiorello has no accented letters, so é/è/á are an e/a with the accent drawn above it
    (Padmé Naberrie (V))."""
    out = esc_i(s)
    for ch, base, acc in (("é", "e", "´"), ("è", "e", "`"), ("á", "a", "´")):
        out = out.replace(ch, f'<span style="position:relative;display:inline-block">{base}<span style="position:absolute;left:0.02em;top:-0.22em;font-family:AGBoldCnA;font-size:0.85em">{acc}</span></span>')
    return out


def esc_i(s: str) -> str:
    """esc() plus _italic_ markup (the slips italicise ship names in titles/banners: _Imperial_-Class Star Destroyer)."""
    return re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"<i>\1</i>", esc(s))


def art_crop(card: dict, win=None, tag: str = "") -> str:
    """Crop the art window out of a Decipher scan (any size: the silver frame is located, then mapped)."""
    src = Path(card["art"]["src"])
    im = Image.open(src)
    if im.mode == "P" and "transparency" in im.info:   # Virtual Block "-pre" GIFs mark their brightest highlight transparent
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im.convert("RGBA")); im = bg
    im = im.convert("RGB")
    import numpy as np
    a = np.array(im).astype(int)
    if card["art"].get("rect") and (not win or tag == "-rect"):
        # the scan's own art rectangle, cover-fitted to the window (tall-slip cards whose window shape differs)
        x0, y0, x1, y1 = card["art"]["rect"]
        aw_, ah_ = TEMPLATES[card["template"]]["art"][2:] if not win else win[2:]
        if (x1 - x0) / (y1 - y0) > aw_ / ah_:
            cw_ = (y1 - y0) * aw_ / ah_; x0, x1 = (x0 + x1 - cw_) / 2, (x0 + x1 + cw_) / 2
        else:
            ch_ = (x1 - x0) * ah_ / aw_; y0, y1 = (y0 + y1 - ch_) / 2, (y0 + y1 + ch_) / 2
        crop = im.crop(tuple(int(round(v)) for v in (x0, y0, x1, y1))).resize((aw_, ah_), Image.LANCZOS)
        p = OUT / f"_art_{card['id']}{tag}.png"; crop.save(p); return data_uri(p)
    if card["art"].get("bbox"):
        fx0, fy0, fx1, fy1 = card["art"]["bbox"]
    elif TEMPLATES[card["template"]].get("system"):
        # no silver frame on a system: the card is everything that is not the black border
        m = a.max(axis=2) > 40
        rows = np.where(m.mean(axis=1) > 0.05)[0]
        cols = np.where(m.mean(axis=0) > 0.05)[0]
        fx0, fy0, fx1, fy1 = cols.min(), rows.min(), cols.max(), rows.max()
        # archive scans are often cut short on one edge: keep the card's true proportions (uniform scale from
        # the taller axis) and let the missing strip be filled with starfield below
        sc = max((fy1 - fy0) / 1931, (fx1 - fx0) / 1343)
        missing = (int(1343 - (fx1 - fx0) / sc), int(1931 - (fy1 - fy0) / sc))   # strip lost at right / bottom
        fx1, fy1 = fx0 + 1343 * sc, fy0 + 1931 * sc
    else:
        bright = a.sum(axis=2) > 120
        rows = np.where(bright.mean(axis=1) > 0.5)[0]
        cols = np.where(bright.mean(axis=0) > 0.5)[0]
        fx0, fy0, fx1, fy1 = cols.min(), rows.min(), cols.max(), rows.max()   # silver frame bbox in the scan
    cw, ch = (1931, 1343) if TEMPLATES[card["template"]].get("landscape") else (1343, 1931)
    sx = (fx1 - fx0) / cw
    sy = (fy1 - fy0) / ch
    if not card["art"].get("bbox") and abs(sy / sx - 1) > 0.015:
        # the scan is cut short on one edge: trust the width, anchor on the edge that is inside the image
        sy = sx
        if fy0 <= 1:
            fy0 = fy1 - ch * sx
        else:
            fy1 = fy0 + ch * sx
    ax, ay, aw, ah = win or TEMPLATES[card["template"]]["art"]
    box = (fx0 + (ax - 144) * sx, fy0 + (ay - 144) * sy, fx0 + (ax + aw - 144) * sx, fy0 + (ay + ah - 144) * sy)
    box = [int(round(v)) for v in box]
    if card.get("art_trim"):
        # Episode I frames (Coruscant/Theed/Tatooine) put the art window a little differently from the classic frame:
        # trim silver-frame rows/columns (bright, unsaturated) off the mapped box's edges, up to 12 % per edge
        x0, y0, x1, y1 = box
        sub = a[max(y0, 0):y1, max(x0, 0):x1]
        def silver(line):   # mean brightness high, mean saturation low
            mx, mn = line.max(axis=1), line.min(axis=1)
            return line.mean() > 100 and (mx - mn).mean() < 45
        h, w = sub.shape[:2]
        # cut at the innermost silver line found in each edge zone (the frame's black inner line may sit between
        # the silver band and the mapped edge)
        def innermost(lines, n):
            cut = 0
            for i in range(n):
                if silver(lines(i)): cut = i + 1
            return cut
        t = innermost(lambda i: sub[i], int(h * 0.15))
        b = innermost(lambda i: sub[h - 1 - i], int(h * 0.15))
        l = innermost(lambda i: sub[:, i], int(w * 0.15))
        r = innermost(lambda i: sub[:, w - 1 - i], int(w * 0.15))
        box = [x0 + l, y0 + t, x1 - r, y1 - b]
    crop = im.crop(tuple(box))
    crop = crop.resize((aw, ah), Image.LANCZOS)
    if TEMPLATES[card["template"]].get("system"):
        # the scan's own printed bars sit a little off the template's: hide them under a starfield band cloned
        # from the middle of the scan (margins are left alone so the scan's set icon and TM lines stay)
        mw, mh = missing if not card["art"].get("bbox") else (0, 0)
        if mw > 0:
            x0 = 1343 - mw - 2
            crop.paste(crop.crop((x0 - mw - 2 - 20, 0, x0 - 20, 1931)).transpose(Image.FLIP_LEFT_RIGHT), (x0, 0))
        if mh > 0:
            y0 = 1931 - mh - 2
            crop.paste(crop.crop((0, y0 - mh - 2 - 20, 1343, y0 - 20)).transpose(Image.FLIP_TOP_BOTTOM), (0, y0))
        # the slip replaces the whole Light half, margins included: its TM lines go too (starfield from the
        # same margins higher up)
        for x0, x1 in ((0, 95), (1248, 1343)):
            mb = crop.crop((x0, 700, x1, 1100))
            for y in range(1560, 1931, mb.height):
                crop.paste(mb.crop((0, 0, mb.width, min(mb.height, 1931 - y))), (x0, y))
        band = crop.crop((80, 365, 1265, 560))
        for y0, y1 in ((40, 360), (1420, 1931)):
            y = y0
            while y < y1:
                h = min(band.height, y1 - y)
                crop.paste(band.crop((0, 0, band.width, h)), (80, y))
                y += h
    p = OUT / f"_art_{card['id']}{tag}.png"
    crop.save(p)
    return data_uri(p)


LOC = ASSETS / "loc"
LOC_ICON_FILES = {k: f"icon-{k}.png" for k in
                  ("grabber", "underground", "interior", "planet", "space", "exterior", "underwater", "creature", "mobile", "starship", "vehicle")}


def nolore_frame(card: dict, t: dict, fr: Path, fx: int, fy: int):
    """Tall slip over a printed card WITHOUT a lore box (Reflections II combos: Abyssin Ornament & Wounded Wookiee (V),
    Uncharted Settlements (V)). Bill 2026-10-14: start from the base card's frame and build the taller card from the
    bottom. Top = the no-lore frame of the base card's family (title bar, chamfered window corners under it):
    Bardez's scratched LS Epic Objective frame recoloured to the LS Effect red (ls-nolore-top.png) or the Dark
    no-lore red frame (ds-effect-tall.png); bottom = this template's own frame (window bottom edge, banner, text box),
    raised by `text_grow`; window sides stretched between; the card-type disc and destiny hole are this template's."""
    import numpy as np
    D = int(card.get("text_grow") or 0)
    ax, ay, aw, ah = t["art"]; gx, gy, gw, gh = t["game_text"]
    c = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0)); c.alpha_composite(Image.open(fr).convert("RGBA"), (fx, fy))
    F = np.array(c)
    light = card.get("side") == "Light"
    T = np.array(Image.open(ASSETS / ("frames/ls-nolore-top.png" if light else "frames/ds-effect-tall.png")).convert("RGBA"))
    Wt, Wtb = (377, 1265) if light else (379, 1085)
    Wb = ay + ah
    G = np.zeros_like(F)
    k = Wt + 170
    G[:k] = T[:k]
    b0 = Wb - 40
    G[b0 - D:gy + 30 - D] = F[b0:gy + 30]
    if D:
        G[gy + 30 - D:gy + 30] = np.array(Image.fromarray(F[gy + 40:gy + gh - 40]).resize((F.shape[1], D), Image.LANCZOS))
    G[gy + 30:] = F[gy + 30:]
    X = 40   # cross-fade the stretched top frame into the bottom frame over X rows (no seam)
    mid = np.array(Image.fromarray(T[k:Wtb - 60]).resize((F.shape[1], b0 - D - k + X), Image.LANCZOS)).astype(float)
    G[k:b0 - D] = mid[:b0 - D - k].astype(np.uint8)
    w = np.linspace(1, 0, X)[:, None, None]
    G[b0 - D:b0 - D + X] = (mid[b0 - D - k:] * w + G[b0 - D:b0 - D + X].astype(float) * (1 - w)).round().astype(np.uint8)
    # the template's own disc and destiny hole, with their bevels, over the top frame's
    yy, xx = np.mgrid[0:G.shape[0], 0:G.shape[1]]
    for cx, cy, r in t.get("nolore_holes", [(258, 230, 80), (t["destiny"][0] + t["destiny"][2] // 2, t["destiny"][1] + t["destiny"][3] // 2, 80)]):
        m = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
        G[m] = F[m]
    p = OUT / f"_frame_{card['id']}.png"; Image.fromarray(G).save(p)
    t = dict(t, card_type=(t["card_type"][0], t["card_type"][1] - D, t["card_type"][2], t["card_type"][3]),
             game_text=(gx, gy - D, gw, gh + D), _artwin=(ax, Wt - 10, aw, Wb - D + 6 - (Wt - 10)),
             expansion_ring=(1390, 373), expansion_size=70)   # the no-lore frame's own ring, clear of the art (Bill)
    if "banner_icon" in t:
        t["banner_icon"] = (t["banner_icon"][0], t["banner_icon"][1] - D)
    return p, t, 0, 0


def grown_frame(card: dict, t: dict, fr: Path, fx: int, fy: int):
    """A tall slip (VS15 Anger, Fear, Aggression (V), Knowledge And Defense (V)): the slip's banner sits higher and its
    text box is taller, as the PC's own reissues print it (V0 Knowledge And Defense): the art window gets shorter with
    its own corners, banner and text-box top move up by `text_grow` px, the text box stretches. A base card with no
    lore box (Reflections II combos) also merges the lore window into the art window (Uncharted Settlements (V)).
    Works on a full-card canvas; returns (frame path, template, 0, 0) and t["_artwin"] = the new art window."""
    import numpy as np
    D = int(card.get("text_grow") or 0)
    ax, ay, aw, ah = t["art"]
    gx, gy, gw, gh = t["game_text"]
    c = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0)); c.alpha_composite(Image.open(fr).convert("RGBA"), (fx, fy))
    F = np.array(c); G = np.zeros_like(F)
    top = (t["lore"][1] + 5) if card.get("no_lore_box") and t.get("lore") else ay
    bot = ay + ah - D
    T0, T1 = ay - 25, ay + 70                  # art window top edge with its corners
    B0, B1 = ay + ah - 95, gy + 30             # art window bottom edge with its corners, banner, text-box top
    G[:top - 25] = F[:top - 25]
    G[top - 25:top - 25 + (T1 - T0)] = F[T0:T1]
    m0 = top - 25 + (T1 - T0)
    m1 = bot - 95    # straight window sides: the frame's own, stretched to fit
    G[m0:m1] = np.array(Image.fromarray(F[T1:B0]).resize((F.shape[1], m1 - m0), Image.LANCZOS))
    G[m1:m1 + (B1 - B0)] = F[B0:B1]
    e = m1 + (B1 - B0)                         # = gy + 30 - D
    if D:
        G[e:gy + 30] = np.array(Image.fromarray(F[gy + 40:gy + gh - 40]).resize((F.shape[1], gy + 30 - e), Image.LANCZOS))
    G[gy + 30:] = F[gy + 30:]
    if card.get("no_lore_box") and t.get("lore"):
        # the printed no-lore cards chamfer the window's top corners under the title bar (Bill 2026-10-14,
        # Abyssin Ornament (V)): shear the corner rows so the window edge runs in diagonally, bevel included
        def run(row, c):
            a = c; b = c
            while a > 0 and row[a - 1]: a -= 1
            while b < len(row) - 1 and row[b + 1]: b += 1
            return a, b
        cx = ax + aw // 2
        A0, A1 = run(F[ay + ah // 2, :, 3] < 20, cx)
        op = np.nonzero(F[ay + ah // 2, :, 3] > 200)[0]; E0, E1 = op.min() + 30, op.max() - 30
        Hc = 100
        y_top = top - 25
        X = np.arange(G.shape[1])
        for y in range(y_top, y_top + Hc + 30):
            sh = int(np.clip(Hc - (y - y_top - 10), 0, Hc))
            if not sh:
                continue
            src = np.interp(X, [0, E0, A0 + sh, cx, A1 - sh, E1, X[-1]], [0, E0, A0, cx, A1, E1, X[-1]]).round().astype(int)
            G[y] = G[y][src]
    p = OUT / f"_frame_{card['id']}.png"; Image.fromarray(G).save(p)
    t = dict(t, card_type=(t["card_type"][0], t["card_type"][1] - D, t["card_type"][2], t["card_type"][3]),
             game_text=(gx, gy - D, gw, gh + D), _artwin=(ax, top, aw, bot - top))
    if "banner_icon" in t:
        t["banner_icon"] = (t["banner_icon"][0], t["banner_icon"][1] - D)
    return p, t, 0, 0


def loc_grow(card: dict) -> tuple[int, int]:
    """Two-line site texts: the slips print a taller text box (by ~14 slip px = 28 px here) and move that half's title
    bar and icons toward the art (VS13: Outpost, AT-AT: Deployment Platform, Dungeon, ISB Sector Office)."""
    if not card.get("text_lines"):
        return 0, 0
    return (28 if "\n" in card.get("game_text", "") else 0), (28 if "\n" in card.get("dark_text", "") else 0)


def starship_frame(frame: Image.Image, card: dict, t: dict, DL: int, DD: int) -> Image.Image:
    """Starship / vehicle site frames as Decipher prints them (Bill 2026-10-14): the frame field is painted blue while
    the title bars, Force slots and text boxes keep their silver (Light) and black (Dark) with silver bevels.
    ls-starship = Home One: War Room (Death Star II): blue paint worn through to the silver in chips and scuffs;
    ds-starship = Executor: Comm Station (Dagobah): smooth deeper blue. Colours sampled from those scans."""
    import numpy as np
    fa = np.array(frame).astype(float)
    H, Wd = fa.shape[:2]
    keep = np.zeros((H, Wd), bool)
    def E(n, slot0):
        return (slot0 - (n - 1) * t["slot_pitch"] - 55 - 4) if n else 1790
    lb = max(1574, E(len(card.get("light_icons", [])), t["ls_slot0"]))
    db = 2072 - max(1581, E(len(card.get("dark_icons", [])), t["ls_slot0"]))
    m = 4   # bevels stay silver
    for x0, y0, x1, y1 in ((163, 1135 - DL, 444, 1252 - DL), (440, 1135 - DL, lb + 2, 1252 - DL),   # Light slot, bar
                           (163, 1252 - DL, 1900, 1370),                                              # Light text box
                           (163, 106, 1900, 225 + DD),                                                # Dark text box
                           (db - 2, 225 + DD, 1634, 336 + DD), (1630, 225 + DD, 1900, 336 + DD)):     # Dark bar, slot
        keep[max(0, y0 - m):y1 + m, max(0, x0 - m):x1 + m] = True
    if card["frame_style"] == "ls-starship":   # Home One keeps a silver rim round the art window
        ax0, ay0, ax1, ay1 = 188, 382 + DD, 1883, 1095 - DL
        ring = np.zeros_like(keep); ring[ay0 - 12:ay1 + 12, ax0 - 12:ax1 + 12] = True; ring[ay0:ay1, ax0:ax1] = False
        keep |= ring
    rgb = fa[:, :, :3]
    silver = (np.abs(rgb[:, :, 0] - rgb[:, :, 2]) < 30) & (rgb.mean(axis=2) > 80) & (fa[:, :, 3] > 0)
    paint = silver & ~keep
    lum = rgb.mean(axis=2, keepdims=True) / 172.0
    if card["frame_style"] == "ls-starship":
        col = np.array([38, 118, 162], float)
        rng = np.random.default_rng(abs(hash(card["id"])) % 2**32)
        from PIL import ImageFilter
        chips = np.zeros((H, Wd))
        for sc, wgt in ((24, 1.0), (9, 0.6), (4, 0.35)):   # worn paint: multi-scale blotches, more of them near the rim
            n = rng.random((H // sc + 2, Wd // sc + 2))
            chips += wgt * np.array(Image.fromarray((n * 255).astype(np.uint8)).resize((Wd + 2 * sc, H + 2 * sc), Image.BICUBIC))[sc:sc + H, sc:sc + Wd] / 255.0
        yy, xx = np.mgrid[0:H, 0:Wd]
        edge = np.minimum.reduce([xx - 70, Wd - 74 - xx, yy - 70, H - 90 - yy]).clip(0, 400) / 400.0
        worn = chips > (1.47 + 0.18 * edge)
        worn = np.array(Image.fromarray((worn * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
        paint &= ~worn
    else:
        col = np.array([18, 95, 160], float)
    tint = np.clip(lum * col * 1.08, 0, 255)
    rgb[paint] = tint[paint]
    fa[:, :, :3] = rgb
    return Image.fromarray(fa.astype(np.uint8), "RGBA")


def loc_frame(card: dict, t: dict) -> Path:
    """Assemble a landscape location frame for this card from Bardez's layers: light-saber glows under the
    frame's force-icon holes, the icon boxes packed from the outside in (as Decipher printed them), scomp-link
    rings. Icons are given per side, outermost first: e.g. ["scomp", "planet", "interior", "underground"]."""
    fx, fy = t["frame_off"]
    frame = Image.open(ASSETS / "frames/loc-site.png").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.open(LOC / "force-light.png").convert("RGBA")
    gx, gy = t["ls_force"]
    DL, DD = loc_grow(card)
    if card.get("light_force", True):
        canvas.alpha_composite(glow, (fx + gx, fy + gy - DL))
    if card.get("dark_force", False):
        g = Image.open(LOC / "force-dark.png").convert("RGBA").rotate(180)   # the Dark Force icon is the red saber
        # mirror of the light glow box about the card centre (frame coords: x' = 2071-x-w, y' = 1479-y-h)
        n = int(card.get("dark_force_count") or 1)
        for k in range(n):   # two Dark Force icons print two sabers in the slot (VS13 #19, #21, #22)
            off = (-40 - k * 64) if n > 1 else 0
            pos = (fx + 2071 - gx - glow.width + off, fy + 1479 - gy - glow.height + DD)
            if k == 0:
                canvas.alpha_composite(g, pos)
            else:   # the glow bitmaps are opaque black around the saber: lighten, not cover
                from PIL import ImageChops
                reg = canvas.crop((pos[0], pos[1], pos[0] + g.width, pos[1] + g.height))
                canvas.paste(ImageChops.lighter(reg.convert("RGB"), g.convert("RGB")).convert("RGBA"), pos)
    if card.get("frame_tint"):   # starship-site frames the slips print in blue (Executor / Redemption, VS13)
        import numpy as np
        fa = np.array(frame).astype(float)
        lum = fa[:, :, :3].mean(axis=2, keepdims=True) / 172.0   # silver ≈ 172 → the slip's colour
        silver = (np.abs(fa[:, :, 0] - fa[:, :, 2]) < 25) & (fa[:, :, :3].mean(axis=2) > 90)
        tint = np.clip(lum * np.array(card["frame_tint"], dtype=float), 0, 255)
        fa[:, :, :3] = np.where(silver[:, :, None], tint, fa[:, :, :3])
        frame = Image.fromarray(fa.astype(np.uint8), "RGBA")
    # The slips run the title bar right up to the first icon box: slide the bar's end cap over the frame's two
    # default boxes and fill the rest with plain silver (light bar, then the dark bar in the 180°-turned frame).
    def extend_bar(img, n, y0, y1, cap1):
        E = (t["ls_slot0"] - (n - 1) * t["slot_pitch"] - 55 - 4) if n else 1790
        S = E - cap1
        if S <= 0:
            return img
        img = img.copy()
        img.alpha_composite(img.crop((1795, y0, 1795 + 1790 - E, y1)), (E, y0)) if E < 1790 else None
        img.alpha_composite(img.crop((1300, y0, cap1, y1)), (1300 + S, y0))
        return img
    frame = extend_bar(frame, len(card.get("light_icons", [])), 1134, 1252, 1574)
    frame = extend_bar(frame.rotate(180), len(card.get("dark_icons", [])), 1155, 1270, 1581).rotate(180)
    if DL or DD:   # taller text box: slide the title band toward the art, stretch the box interior
        import numpy as np
        fa = np.array(frame); old = fa.copy()
        if DL:
            fa[1096 - DL:1320 - DL] = old[1096:1320]; fa[1320 - DL:1320] = old[1272:1272 + DL]
        if DD:
            fa[160 + DD:381 + DD] = old[160:381]; fa[160:160 + DD] = old[122:122 + DD]
        frame = Image.fromarray(fa, "RGBA")
    if card.get("frame_style") in ("ls-starship", "ds-starship"):
        frame = starship_frame(frame, card, t, DL, DD)
    canvas.alpha_composite(frame, (fx, fy))
    ly = t["slot_y"]
    dy = 1479 - ly - 111
    box = Image.open(LOC / "box.png").convert("RGBA")
    ring = Image.open(LOC / "scomp.png").convert("RGBA")

    def place(icons, light):
        # Boxes are cut from the printed Hoth card (brighter than Bardez's), 100×94, sitting inside the title bar.
        by = ly - 7 - DL
        dby = 1479 - (ly - 7) - 94 + DD
        for k, name in enumerate(icons):
            cx = (t["ls_slot0"] - k * t["slot_pitch"]) if light else (t["ds_slot0"] + k * t["slot_pitch"])
            if name == "scomp":
                r = Image.open(LOC / "scanring.png").convert("RGBA")
                y = by - 5 if light else dby - 5
                canvas.alpha_composite(r if light else r.rotate(180), (fx + cx - 52, fy + y))
                continue
            sb = LOC / f"scanbox-{name}.png"
            if sb.exists():
                b = Image.open(sb).convert("RGBA")
                if not light:
                    b = b.rotate(180)
                canvas.alpha_composite(b, (fx + cx - 50, fy + (by if light else dby)))
                continue
            y = (ly - DL) if light else (dy + DD)
            b = box if light else box.rotate(180)
            canvas.alpha_composite(b, (fx + cx - 55, fy + y))
            ic = Image.open(LOC / LOC_ICON_FILES[name]).convert("RGBA")
            if not light:
                ic = ic.rotate(180)
            canvas.alpha_composite(ic, (fx + cx - ic.width // 2, fy + y + 55 - ic.height // 2))

    place(card.get("light_icons", []), True)
    place(card.get("dark_icons", []), False)
    p = OUT / f"_frame_{card['id']}.png"
    canvas.save(p)
    return p


def sys_frame(card: dict, t: dict) -> Path:
    """Portrait system: force glows under the bar assembly's force holes, planet icon(s), parsec boxes."""
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if card.get("light_force", True):
        g = Image.open(LOC / "sysforce-light.png").convert("RGBA")
        n = int(card.get("light_force_count") or 1)
        canvas.alpha_composite(g, t["ls_force"])
        if n > 1:   # two Light Force icons = a second saber beside the first (Alderaan (Blown Away) (V))
            import numpy as np
            ga = np.array(g).astype(float); lum = ga[:, :, :3].max(axis=2)
            ga[:, :, 3] = np.clip(lum * 1.4, 0, 255) * (ga[:, :, 3] > 250); ga[:48] = 0
            sab = Image.fromarray(ga.astype(np.uint8), "RGBA")
            for k in range(1, n):
                canvas.alpha_composite(sab, (t["ls_force"][0] + 82 * k, t["ls_force"][1]))
    if card.get("dark_force", False):
        g = Image.open(LOC / "sysforce-dark.png").convert("RGBA")
        canvas.alpha_composite(g, t["ds_force"])
        n = int(card.get("dark_force_count") or 1)
        if n > 1:   # two Dark Force icons (Dagobah): the Light rule mirrored — second saber left of the first
            import numpy as np
            ga = np.array(g).astype(float); lum = ga[:, :, :3].max(axis=2)
            ga[:, :, 3] = np.clip(lum * 1.4, 0, 255) * (ga[:, :, 3] > 250); ga[-48:] = 0
            sab = Image.fromarray(ga.astype(np.uint8), "RGBA")
            for k in range(1, n):
                canvas.alpha_composite(sab, (t["ds_force"][0] - 82 * k, t["ds_force"][1]))
    fx, fy = t["frame_off"]
    canvas.alpha_composite(Image.open(ASSETS / t["frame_png"]).convert("RGBA"), (fx, fy))
    for key, light in (("light_icons", True), ("dark_icons", False)):
        for name in card.get(key, [])[:1]:
            cx, cy = t["ls_icon"] if light else t["ds_icon"]
            sb = LOC / f"scanbox-{name}.png"
            if sb.exists():   # printed-card box + icon (brighter than Bardez's), scaled into the frame's black box
                ic = Image.open(sb).convert("RGBA").resize((89, 86), Image.LANCZOS)
            else:
                ic = Image.open(LOC / LOC_ICON_FILES[name]).convert("RGBA")
            if not light:
                ic = ic.rotate(180)
            canvas.alpha_composite(ic, (cx - ic.width // 2, cy - ic.height // 2))
    p = OUT / f"_frame_{card['id']}.png"
    canvas.save(p)
    return p


def inline_set_mark(mark: str) -> str:
    """A set mark sized for a line of game text (wrapped so it sits on the baseline like the other inline icons)."""
    html = set_mark_html(mark, 0, 0, 40).replace("position:absolute;", "position:relative;display:inline-block;vertical-align:-14px;")
    return re.sub(r"left:-?\d+px;top:-?\d+px;", "", html)


def set_mark_html(mark: str, cx: float, cy: float, ss: float) -> str:
    """Inline SVG (uses the page's fonts) centred on the template's set-icon slot. mark = "pc:<n>" or "vb:<n>".
    Sizes/placement measured on Holotable faces (Captain Lando Calrissian VS13, Admiral Raddus VS9, A Good Blaster
    At Your Side VS0, 2-1B (Too-Onebee) (V) Virtual Block 2)."""
    kind, _, num = str(mark).partition(":")
    if kind == "vb":   # Virtual Block diamond: black, white edge, number over a V chevron
        w = ss * 1.55; h = w * .86
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 86" width="{w:.0f}" height="{h:.0f}">'
               '<polygon points="50,3 97,43 50,83 3,43" fill="#111" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>'
               '<polyline points="12,47 50,76 88,47" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="miter"/>'
               f'<text x="50" y="53" text-anchor="middle" font-family="AGMedExt" font-size="{38 if len(num) < 2 else 32}" fill="#fff">{esc(num)}</text></svg>')
        return f'<div style="position:absolute;left:{cx - w / 2 + ss * .25:.0f}px;top:{cy - h / 2 + ss * .85:.0f}px;line-height:0">{svg}</div>'
    gold = num in ("0", "D", "P")   # Set 0 and the Virtual Defensive Shields: gold ring (PC Game Aid sheet)
    ring_a, ring_b = ("#8a6a1c", "#e6c766") if gold else ("#0b3a74", "#5a9bd2")
    edge = "#c97a12" if gold else "#1d4aa0"
    w, h = ss * 2.0, ss * 1.5
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 150" width="{w:.0f}" height="{h:.0f}">'
           f'<defs><linearGradient id="rg{num}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ring_b}"/>'
           f'<stop offset=".55" stop-color="{ring_a}"/><stop offset="1" stop-color="{ring_b}"/></linearGradient></defs>'
           f'<ellipse cx="100" cy="80" rx="74" ry="30" transform="rotate(-28 100 80)" fill="none" stroke="url(#rg{num})" stroke-width="16"/>'
           f'<text x="100" y="124" text-anchor="middle" font-family="AGBoldCnA" font-size="142" letter-spacing="-3" '
           f'fill="#fff" stroke="{edge}" stroke-width="9" paint-order="stroke" stroke-linejoin="round">{esc(num)}</text></svg>')
    return f'<div style="position:absolute;left:{cx - w / 2 - ss * .1:.0f}px;top:{cy - h / 2 + ss * .2:.0f}px;line-height:0">{svg}</div>'


_HOLE: dict = {}


def frame_hole(t: dict) -> tuple:
    """The transparent window of the template's frame around its art box (card px), measured once per frame."""
    fr, fx, fy = t["frame"]
    key = (fr, fx, fy, t["art"])
    if key not in _HOLE:
        import numpy as np
        a = np.array(Image.open(ASSETS / fr).convert("RGBA"))[:, :, 3] < 128
        ax, ay, aw, ah = t["art"]
        cx, cy = ax + aw // 2 - fx, ay + ah // 2 - fy
        def run(line, i, step):
            while 0 <= i + step < len(line) and line[i + step]:
                i += step
            return i
        rows = [run(a[cy + d], cx, -1) for d in (-ah // 3, 0, ah // 3)], [run(a[cy + d], cx, 1) for d in (-ah // 3, 0, ah // 3)]
        cols = [run(a[:, cx + d], cy, -1) for d in (-aw // 3, 0, aw // 3)], [run(a[:, cx + d], cy, 1) for d in (-aw // 3, 0, aw // 3)]
        _HOLE[key] = (min(rows[0]) + fx, min(cols[0]) + fy, max(rows[1]) + fx + 1, max(cols[1]) + fy + 1)
    return _HOLE[key]


def build_html(card: dict) -> str:
    t = TEMPLATES[card["template"]]
    card_ctx.clear(); card_ctx.update(card); card_ctx["_dark_text"] = bool(t.get("dark_text"))
    fonts = {
        "Fiorello": "fonts/Fiorello CG Condensed Regular.otf",
        "AGLightCn": "fonts/Akzidenz-Grotesk BQ Light Conde.otf",
        "AGMedCn": "fonts/AkzidenzGroteskBE-MdCn.otf",
        "AGBoldCnA": "fonts/Akzidenz-Grotesk BQ Condensed A.otf",
        "AGCn": "fonts/Akzidenz-Grotesk BQ Condensed.otf",
        "AGMedExt": "fonts/AkzidenzGrotesk-MediumExtended.otf",
        "Craft": "fonts/CraftGothic-HeavyExtended.otf",
    }
    font_css = "\n".join(f'@font-face{{font-family:"{k}";src:url("{data_uri(ASSETS / v)}");}}' for k, v in fonts.items())
    global W, H
    W, H = (2220, 1632) if is_wide(t) else (1632, 2220)
    if t.get("landscape"):
        fr, fx, fy = loc_frame(card, t), 0, 0
    elif t.get("system"):
        fr, fx, fy = sys_frame(card, t), 0, 0
    else:
        fr, fx, fy = t["frame"]
        fr = ASSETS / fr
        if card.get("text_grow") and card.get("no_lore_box"):
            fr, t, fx, fy = nolore_frame(card, t, fr, fx, fy)
        elif card.get("text_grow"):
            fr, t, fx, fy = grown_frame(card, t, fr, fx, fy)
    ax, ay, aw, ah = t["art"]
    art = art_crop(card) if card.get("art") else ""

    def box(key, style=""):
        x, y, w, h = t[key]
        return f"left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}"

    parts = [f'<div id="card"{' class="inv"' if card.get("invert_text") else ''} style="position:relative;width:{W}px;height:{H}px;background:#000;overflow:hidden">']
    marks = []   # (piece, index into parts): card maker layers — each piece is wrapped so it can be moved / resized / hidden

    def sec(name):
        marks.append((name, len(parts)))
    sec('art')
    if art and t.get("_artwin"):   # reshaped window (tall slips): the art fills it, under the frame
        wx, wy, ww, wh = t["_artwin"]
        if card.get("no_lore_box") and card["art"].get("rect"):
            parts.append(f'<img src="{art_crop(card, t["_artwin"], "-rect")}" style="position:absolute;left:{wx}px;top:{wy}px;width:{ww}px;height:{wh}px">')
        else:
            parts.append(f'<div style="position:absolute;left:{wx}px;top:{wy}px;width:{ww}px;height:{wh}px;overflow:hidden">'
                         f'<img src="{art}" style="position:absolute;left:0;top:{(wh - ah) // 2}px;width:{aw}px;height:{ah}px"></div>')
    elif art and card.get("art_cover_hole") and not t.get("landscape") and not t.get("system") and not t.get("wide"):
        # card maker: the picture fills the frame's whole window (some frames' holes run a few px past the template's
        # art box — a black sliver showed on Ahsoka Tano With Lightsabers, Bill 2026-10-15)
        hx0, hy0, hx1, hy1 = frame_hole(t)
        win = (min(ax, hx0), min(ay, hy0), max(ax + aw, hx1) - min(ax, hx0), max(ay + ah, hy1) - min(ay, hy0))
        parts.append(f'<img src="{art_crop(card, win, "-rect" if card["art"].get("rect") else "-hole")}" style="position:absolute;left:{win[0]}px;top:{win[1]}px;width:{win[2]}px;height:{win[3]}px">')
    elif art:
        parts.append(f'<img src="{art}" style="position:absolute;left:{ax}px;top:{ay}px;width:{aw}px;height:{ah}px">')
    sec(None)
    parts.append(f'<img src="{data_uri(fr)}" style="position:absolute;left:{fx}px;top:{fy}px">')
    sec('art')
    if card.get("no_lore_box") and card.get("art") and t.get("lore") and not t.get("_artwin"):
        # the printed card has no lore box (Jedi Tests, Reflections II combo cards): its art runs from the title bar to the
        # banner — lay the mapped scan over the frame's lore window too
        lx, ly, lw, lh = t["lore"]
        win = (ax, ly - 34, aw, ay + ah - (ly - 34) - int(card.get("text_grow") or 0))
        parts.append(f'<img src="{art_crop(card, win, "-rect" if card["art"].get("rect") else "-full")}" style="position:absolute;left:{win[0]}px;top:{win[1]}px;width:{win[2]}px;height:{win[3]}px">')
    sec('affiliation')
    if card.get("disc"):   # affiliation disc swapped over the frame's own (Yoda: the Light Jedi Master blade on the Rebel frame)
        dx_, dy__ = t.get("disc_at", (193, 176))
        parts.append(f'<img src="{data_uri(ASSETS / f"icons/disc-{card["disc"]}.png")}" style="position:absolute;left:{dx_}px;top:{dy__}px">')
    if card.get("disc2"):   # second affiliation disc right of the first, title bar shortened (The Emperor: Dark Jedi Master + Imperial)
        parts.append(f'<img src="{data_uri(ASSETS / f"icons/disc-{card["disc2"]}.png")}" style="position:absolute;left:{359}px;top:{174}px">')
        t = dict(t, title=(t["title"][0] + 170, t["title"][1], t["title"][2] - 170, t["title"][3]))
    sec('title')
    # title + destiny
    pre = " pre" if card.get("text_lines") else ""
    if t.get("landscape"):
        # Light title centred in the grey bar between the force slot and the first icon box; Dark mirrored, rotated.
        DL, DD = loc_grow(card)
        nbox = len(card.get("light_icons", []))
        x0, y, h = t["ls_bar"]; y -= DL
        x1 = fx + 1790 - 15 + t["frame_off"][0] - fx if nbox == 0 else fx + t["ls_slot0"] - (nbox - 1) * t["slot_pitch"] - 55 + t["frame_off"][0]
        parts.append(f'<div class="title ltitle" style="position:absolute;left:{x0}px;top:{y}px;width:{x1 - x0}px;height:{h}px">{loc_title(card, "Light")}</div>')
        nbox = len(card.get("dark_icons", []))
        dx, dy_, dw, dh = t["ds_bar"]; dy_ += DD
        dx0 = dx if nbox == 0 else t["frame_off"][0] + t["ds_slot0"] + (nbox - 1) * t["slot_pitch"] + 55
        parts.append(f'<div class="title dtitle" style="position:absolute;left:{dx0}px;top:{dy_}px;width:{dx + dw - dx0}px;height:{dh}px">{loc_title(card, "Dark")}</div>')
        sec('location_text')
        lx, ly_, lw, lh = t["ls_text"]; ly_ -= DL; lh += DL
        parts.append(f'<div class="ltext fit{pre}" style="position:absolute;left:{lx}px;top:{ly_}px;width:{lw}px;height:{lh}px"><span>{game_text_html(card["game_text"])}</span></div>')
        tx, ty, tw, th = t["ds_text"]; th += DD
        parts.append(f'<div class="dtext fit{pre}" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px"><span>{game_text_html(card["dark_text"])}</span></div>')
    elif t.get("system"):
        x, y, w, h = t["ls_bar"]
        parts.append(f'<div class="title ltitle" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{loc_title(card, "Light")}</div>')
        x, y, w, h = t["ds_bar"]
        parts.append(f'<div class="title dtitle" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{loc_title(card, "Dark")}</div>')
        sec('location_text')
        x, y, w, h = t["ls_text"]
        parts.append(f'<div class="ltext fit{pre}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span>{game_text_html(card["game_text"])}</span></div>')
        x, y, w, h = t["ds_text"]
        parts.append(f'<div class="dtext fit{pre}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span>{game_text_html(card["dark_text"])}</span></div>')
        sec('parsec')
        if card.get("parsec") is not None:
            x, y, w, h = t["ls_parsec"]
            parts.append(f'<div class="parsec" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{esc(str(card["parsec"]))}</div>')
            x, y, w, h = t["ds_parsec"]
            parts.append(f'<div class="parsec" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate(180deg)">{esc(str(card["parsec"]))}</div>')
    else:
        parts.append(f'<div class="title" style="position:absolute;{box("title")}">{title_html(card["title"])}</div>')
    sec('destiny')
    if card.get("destiny") and "destiny" in t:
        dv = esc(card["destiny"])
        plain = re.sub(r"<[^>]+>", "", dv)
        if " or " in dv or len(plain) > 2:   # multi-value destiny (R2-D2 "2 or 5"), or a long value: the pill widens left (card maker: capped, then condensed)
            x, y, w, h = t["destiny"]
            ext = 150 if " or " in dv else min(190, 52 * (len(plain) - 2))
            parts.append(f'<div style="position:absolute;left:{x - ext - 6}px;top:{y - 6}px;width:{w + ext + 12}px;height:{h + 12}px;background:#000;border:6px solid #d0d0d2;border-radius:{h // 2 + 6}px;box-sizing:border-box"></div>')
            parts.append(f'<div class="destiny" style="position:absolute;left:{x - ext}px;top:{y}px;width:{w + ext}px;height:{h}px;font-size:80px;white-space:nowrap;padding-top:4px"><span class="fitnum" data-avail="{w + ext - 20}">{dv.replace(" or ", "<span style=\"font-size:46px\">&nbsp;or&nbsp;</span>")}</span></div>')
        else:
            parts.append(f'<div class="destiny" style="position:absolute;{box("destiny")}"><span class="fitnum" data-avail="{t["destiny"][2] - 8}">{dv}</span></div>')
    sec(None)
    for fx, fy, fw, fh, col in t.get("fill_boxes", []):
        parts.append(f'<div style="position:absolute;left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px;background:{col}"></div>')
    sec('lore')
    # lore
    if card.get("lore"):
        lx_, ly_, lw_, lh_ = t["lore"]
        tx0, rgt, ind, cut, lsp = t.get("lore_x") or LORE_X["Light" if t.get("dark_text") else "Dark"]
        parts.append(f'<div class="lore fit" style="position:absolute;left:{tx0}px;top:{ly_}px;width:{rgt - tx0}px;height:{lh_}px;'
                     f'text-indent:{card.get("lore_indent", ind)}px;letter-spacing:{lsp}px">'
                     f'<span style="float:right;width:{cut}px;height:58px"></span>{game_text_html(card["lore"])}</div>')
    sec('stats')
    # stats (character)
    if "stats" in t and card.get("stats"):
        y = t["stats_y"]
        stats = list(card["stats"])
        if len(stats) == 3 and "stats_row3" in t:
            # a droid printing three separate boxes (LE-BO2D9 (V): POWER / ARMOR / MAINTENANCE DROID): the droid frame
            # has one wide box, so the Rebel frame's three-box stat row (same white silver) is laid over it
            png, sx, sy = t["stats_row3"]
            parts.append(f'<img src="{data_uri(ASSETS / png)}" style="position:absolute;left:{sx}px;top:{sy}px">')
            boxes = t["stats_row3_boxes"]
        elif len(stats) == 2 and stats[1][0] not in ("ABILITY", "ARMOR", "MANEUVER") and "stats_wide" in t:
            # droids: one wide box (e.g. ASTROMECH DROID) spans the ability + third slots
            wx, ww = t["stats_wide"]
            parts.append(f'<div style="position:absolute;left:{wx}px;top:{y}px;width:{ww}px;height:69px;background:{t.get("stats_wide_fill", "#000")};border-radius:6px"></div>')
            boxes = [t["stats"][0], (wx, ww)]
        else:
            boxes = t["stats"]
        if boxes is t["stats"]:
            boxes = stat_boxes(t, len(boxes)) or boxes   # the wells as painted in the frame
        is_char = "character" in card["template"]
        for i, ((x, w), (label, value)) in enumerate(zip(boxes, stats)):
            # Decipher sets the value at the right end of its box (ARMOR      5, LANDSPEED    2 on starships and
            # vehicles; POWER 5 / ABILITY 6 fill theirs) — except a character's wide third box (ARMOR 5 follows the
            # label, Boba Fett). Bill 2026-10-13 (Jabba's Space Cruiser (V)).
            vcls = "val" if (is_char and i >= 2) else "val r"
            # a label-only box (FORCE-SENSITIVE, MAINTENANCE DROID) stays on one line: shrink it to the box as the
            # slips do (LE-BO2D9 (V), 2026-10-13); AGBoldCnA caps ≈ 0.50 em + 1.8 px tracking per character
            lab_style = ""
            if not value:
                # full height, squeezed horizontally to the well (as the slips print MAINTENANCE DROID) — fitlab JS
                lab_style = f' class="lab fitlab" data-avail="{w - 2 * t.get("stat_pl", 16)}" style="white-space:nowrap;display:inline-block;transform-origin:left center"'
            parts.append(f'<div class="stat" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:68px">'
                         f'<span{lab_style if lab_style else " class=lab"}>{esc(label)}</span>{f'<span class="{vcls}">' + esc(value) + "</span>" if value else ""}</div>')
    if card.get("stat_icon") and t.get("stats_y"):   # a round icon left of the stat row (Mon Mothma (V): the Republic crest)
        sx0 = (stat_boxes(t, 3) or t["stats"])[0][0]
        parts.append(f'<img src="{data_uri(ASSETS / ICON_FILES[card["stat_icon"]])}" style="position:absolute;left:{sx0 - 100}px;top:{t["stats_y"] - 14}px;width:96px;height:96px">')
    sec('banner')
    if "card_type" in t and card.get("card_type"):
        parts.append(f'<div class="ctype" style="position:absolute;{box("card_type")}"><span class="ct">{esc_i(card["card_type"])}</span></div>')
    if card.get("banner_icon") and "banner_icon" in t:
        bx, by = t["banner_icon"]
        if ICON_FILES[card["banner_icon"]].startswith("icons/col-"):   # framed icon (Setup): drawn at box size
            parts.append(f'<img src="{data_uri(ASSETS / ICON_FILES[card["banner_icon"]])}" style="position:absolute;left:{bx}px;top:{by}px;width:89px;height:90px">')
        else:
            parts.append(f'<img src="{data_uri(ASSETS / "icons/icon-box-effect.png")}" style="position:absolute;left:{bx}px;top:{by}px">')
            parts.append(f'<img src="{data_uri(ASSETS / ICON_FILES[card["banner_icon"]])}" style="position:absolute;left:{bx + 8}px;top:{by + 8}px;width:73px;height:73px">')
    sec('game_text')
    # game text
    if "game_text" in t:
        parts.append(f'<div class="gt fit{" grow" if t.get("gt_grow") else ""}" style="position:absolute;{box("game_text")}">{game_text_html(card["game_text"])}</div>')
    # deploy / forfeit
    if card.get("deploy") is not None and "deploy" in t:
        for k_ in ("deploy", "forfeit"):   # long values (544) condense into the printed box, then shrink — never overflow it
            sec(k_)
            parts.append(f'<div class="{k_}" style="position:absolute;{box(k_)}"><span class="fitnum" data-avail="{t[k_][2] + 6}" data-h="{t[k_][3]}">{esc(str(card[k_]))}</span></div>')
    sec(None)
    sec('scomp')
    if card.get("scomp") and "scomp" in t:
        sx, sy = t["scomp"]
        parts.append(f'<img src="{data_uri(ASSETS / "icons/scomp-ship.png")}" style="position:absolute;left:{sx}px;top:{sy}px">')
    sec('icons')
    # icon slots
    light = card.get("side") == "Light"
    icons = list(card.get("icons", []))
    # two Warrior icons share one tall box on the printed cards (IG-88): "warrior","warrior" → "warrior2" (89×158);
    # Premiere (no expansion symbol) printed them as two separate boxes (Tonnika Sisters)
    packed = []
    for nm in icons:
        if nm == "warrior" and packed and packed[-1] == "warrior" and card.get("expansion_icon"):
            packed[-1] = "warrior2"
        else:
            packed.append(nm)
    slots = list(t.get("icon_slots", []))
    if packed and slots and ("warrior2" in packed or len(packed) > len(slots)) and "set_icon_abs" in t:
        # more than the frame's slots: stack from the first slot down to the set sphere, shrinking uniformly to fit
        x0, y0 = slots[0]
        sy = t["set_icon_abs"][1]; ss = t.get("set_icon_size", 76)
        heights = [158 if nm == "warrior2" else 90 for nm in packed]
        gap = 8
        total = sum(heights) + gap * len(heights) + ss
        avail = sy + ss - y0
        k = min(1.0, avail / total)
        y = y0; slots = []; sizes = []
        for h in heights:
            slots.append((x0 + int((89 - 89 * k) / 2), int(y))); sizes.append(k); y += (h + gap) * k
        card["_set_icon_override"] = (t["set_icon_abs"][0] + int((ss - ss * k) / 2), int(y), int(ss * k))
    else:
        sizes = [1.0] * len(packed)
    for (x, y), name, k in zip(slots, packed, sizes):
        if name == "warrior2":
            parts.append(f'<img src="{data_uri(ASSETS / "icons/col-warrior2.png")}" style="position:absolute;left:{x}px;top:{y}px;width:{int(89 * k)}px;height:{int(158 * k)}px">')
            continue
        key = f"{name}-light" if light and f"{name}-light" in ICON_FILES else name   # Light and Dark pilot icons differ
        if ICON_FILES[key].startswith("icons/col-"):   # Game Aid icon with its own silver frame, box size
            parts.append(f'<img src="{data_uri(ASSETS / ICON_FILES[key])}" style="position:absolute;left:{x}px;top:{y}px;width:{int(89 * k)}px;height:{int(90 * k)}px">')
        else:
            parts.append(f'<img src="{data_uri(ASSETS / "icons/icon-box.png")}" style="position:absolute;left:{x}px;top:{y}px;width:{int(89 * k)}px;height:{int(90 * k)}px">')
            parts.append(f'<img src="{data_uri(ASSETS / ICON_FILES[key])}" style="position:absolute;left:{x + int(6 * k)}px;top:{y + int(7 * k)}px;width:{int(75 * k)}px;height:{int(75 * k)}px">')
    sec('set_mark')
    # original-era virtual marker: the slips print the gold virtual-set symbol in the lower icon slot
    if card.get("set_mark") and "set_icon_abs" in t and not card.get("set_icon_file"):
        # Players Committee set marks, drawn as vector: modern Virtual Sets = the number on a tilted ring (blue; gold
        # for Set 0), 2009 Virtual Blocks = the black diamond with its chevron (Bill 2026-10-15, from Holotable scans)
        x, y = t["set_icon_abs"]; ss = t.get("set_icon_size", 76)
        parts.append(set_mark_html(card["set_mark"], x + ss / 2, y + ss / 2, ss))
    elif (card.get("virtual_set") is not None or card.get("set_icon_file")) and "set_icon_abs" in t:
        x, y = t["set_icon_abs"]
        sym = Path(card["set_icon_file"]) if card.get("set_icon_file") else ASSETS / f"icons/ovs-set-{card['virtual_set']}.png"   # each original set has its own symbol (from its Remaster PDF); card maker: the user's own
        ss = t.get("set_icon_size", 76)
        if card.get("_set_icon_override"):
            x, y, ss = card["_set_icon_override"]
        parts.append(f'<img src="{data_uri(sym)}" style="position:absolute;left:{x}px;top:{y}px;width:{ss}px;height:{ss}px">')
    sec('expansion')
    # expansion-set icon of the base Decipher card, in the ring right of the lore box (a slip never changes the top half)
    if card.get("expansion_icon") and "expansion_ring" in t:
        x, y = t["expansion_ring"]
        sz = t.get("expansion_size", 62)
        if card.get("expansion_icon_in_hole", True):
            # printed cards: the set icon is a sphere sitting in a black hole of the frame
            parts.append(f'<div style="position:absolute;left:{x - 1}px;top:{y - 1}px;width:{sz + 2}px;height:{sz + 2}px;border-radius:50%;background:#000"></div>')
            isz = sz - 4
            parts.append(f'<img src="{data_uri(ASSETS / card["expansion_icon"])}" style="position:absolute;left:{x + (sz - isz) // 2}px;top:{y + (sz - isz) // 2}px;width:{isz}px;height:{isz}px">')
        else:
            parts.append(f'<img src="{data_uri(ASSETS / card["expansion_icon"])}" style="position:absolute;left:{x}px;top:{y}px;width:{sz}px;height:{sz}px">')
    sec('coins')
    if t.get("coins") and card.get("credits"):   # Reflections Gold credit value: gold coins stacked up from the box foot
        cx_, cy_, step_ = t["coins"]
        for k in range(min(int(card["credits"]), 4)):
            parts.append(f'<img src="{data_uri(ASSETS / "icons/rg-coin.png")}" style="position:absolute;left:{cx_}px;top:{cy_ - k * step_}px">')
    sec('expansion')
    if card.get("expansion_icon") and t.get("system_ring") and card.get("draw_system_ring"):
        # systems keep the scan whole (its own sphere included): drawn only when asked (card maker: no scan, or a new set)
        x, y, sz = t["system_ring"]
        parts.append(f'<img src="{data_uri(ASSETS / card["expansion_icon"])}" style="position:absolute;left:{x}px;top:{y}px;width:{sz}px;height:{sz}px">')
    sec('ring_icons')
    # Episode I icon below the ring, as the Episode I-era printed cards carry it (Radiant VII, Wesa Ready To Do Our-sa Part)
    if card.get("ring_icons") and "expansion_ring" in t:
        x, y = t["expansion_ring"]
        sz = t.get("expansion_size", 62)
        k = 0 if (card.get("ring_fill") and not card.get("expansion_icon")) else 1   # card maker: no sphere -> the first disc takes its place (Aayla Secura)
        for nm in card["ring_icons"]:
            if nm == "sidious" and "game_text" in t:   # printed in the right margin at the text box top (Unlimited Power!)
                parts.append(f'<img src="{data_uri(ASSETS / RING_DISCS[nm])}" style="position:absolute;left:{x + 3}px;top:{t["game_text"][1] - 70}px;width:{sz - 6}px;height:{sz - 6}px;border-radius:50%">')
                continue
            if nm in RING_DISCS:
                parts.append(f'<img src="{data_uri(ASSETS / RING_DISCS[nm])}" style="position:absolute;left:{x + 3}px;top:{y + k * (sz + 30)}px;width:{sz - 6}px;height:{sz - 6}px;border-radius:50%">')
                k += 1
    sec('margin_icon')
    if card.get("margin_icon") and "game_text" in t:   # Scoundrel: a portrait disc in the left margin at the text box top
        gx, gy, gw, gh = t["game_text"]
        parts.append(f'<img src="{data_uri(ASSETS / "icons/pc-gameaid-named" / (card["margin_icon"] + ".png"))}" style="position:absolute;left:{t.get("margin_icon_x", 190)}px;top:{gy + 8}px;width:84px;height:84px;border-radius:50%">')
    sec('copyright')
    # vertical Lucasfilm / Decipher line on the right margin of the art, as on the printed card
    if card.get("copyright") and t.get("copyright_split") and card.get("copyright_split"):   # systems (card maker): split over the two bottom margins
        txt = card["copyright"]
        cut = txt.find("TM, ®")
        halves = (txt[:cut].strip(), txt[cut:].strip()) if cut > 0 else (txt, "")
        for (cx, cy, cw, ch), part in zip(t["copyright_split"], halves):
            if part:
                parts.append(f'<div class="copy" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px">'
                             f'<div class="copyin" style="color:#fff">{esc(part)}</div></div>')
    elif card.get("copyright") and not t.get("no_copyright"):   # full-art Admiral's Orders keep the scan's own line
        cx, cy, cw, ch = t.get("copyright", (t.get("copyright_x", 1404), ay, 36, ah))
        parts.append(f'<div class="copy" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px">'
                     f'<div class="copyin">{esc(card["copyright"])}</div></div>')
    sec('credits')
    # slip credit lines in the side margins (Wokling (V): "Original concept by …" left, "GenCon 2002 Winner" right),
    # italic, reading bottom-to-top, spanning the banner + text box
    # centred in the coloured margin between frame edge and text box, as the slips print them (Bill 2026-10-13);
    # margins measured on the frames: Light ≈169–246 / 1389–1433, Dark ≈145–264 / 1361–1483 (div is 40 px wide)
    mx = t.get("credit_mx") or ((187, 1391) if t.get("dark_text") else (185, 1402))
    for key, x in (("margin_left", mx[0]), ("margin_right", mx[1]), ("margin_right_top", mx[1])):
        if card.get(key) and "game_text" in t:
            gx, gy, gw, gh = t["game_text"]
            cx_, cy_, cw_, ch_ = t.get("card_type", (gx, gy - 160, gw, 61))
            top, bot = cy_, gy + gh
            ink = t.get("credit_ink") or margin_ink(fr, x - fx, top - fy, bot - fy)
            if (key == "margin_right_top" or key == "margin_right" and card.get("margin_right_at") == "top") and t.get("icon_slots"):
                # the slip prints the credit above the column icons, level with the stat row (Padmé Naberrie (V))
                top, bot = t.get("stats_y", top) - 60, t["icon_slots"][0][1] - 8
            elif key == "margin_right" and card.get("icons") and t.get("icon_slots"):
                # the column icons sit in the right margin: the credit runs below them (Mace Windu (V))
                top = max(top, t["icon_slots"][min(len(card["icons"]), len(t["icon_slots"])) - 1][1] + 100)
                if t.get("set_icon_abs"):
                    bot = min(bot, t["set_icon_abs"][1] - 8)   # and above the set sphere
            if key == "margin_left" and card.get("scomp") and t.get("scomp"):
                bot = min(bot, t["scomp"][1] - 12)   # above the scomp ring (Stinger (V))
                if "deploy" in t and card.get("deploy") is not None:
                    top = t.get("stats_y", top) - 60
            elif key == "margin_left" and "deploy" in t and card.get("deploy") is not None:
                # characters: the deploy/forfeit boxes sit in the left margin — the credit runs above them (as The
                # Emperor (V) prints it), white on the dark frames
                top, bot = t.get("stats_y", top) - (60 if "\n" in card[key] else 10), t["deploy"][1] - 10
            # the rotated line is as long as the text; shrink the font so it fits the span (AGCn italic ≈ 0.40 em/char)
            # the slips run the credit nearly the whole span at ~46 px; the fitcredit JS shrinks it only if it would overflow
            parts.append(f'<div class="copy" style="position:absolute;left:{x}px;top:{top}px;width:40px;height:{bot - top}px">'
                         f'<div class="credit fitcredit" data-avail="{bot - top - 10}"{(' data-lines="2" data-fs="' + ('48' if ink == '#fff' and not t.get('dark_text') else '42') + '"') if chr(10) in card[key] else ''} style="color:{ink};font-size:46px">{esc(card[key]).replace(chr(10), "<br>")}</div></div>')
    sec('credits')
    if card.get("credit_bottom") and "game_text" in t:   # a credit set under the text box (Lord Vader (V))
        gx, gy, gw, gh = t["game_text"]
        cink = "#000" if t.get("dark_text") else "#ddd"
        cb = card["credit_bottom"]
        if isinstance(cb, list):   # left + right under the text box (Yoda, Dominator, Thrawn (V), VS14)
            inner = "".join(f"<span>{esc(x)}</span>" for x in cb)
            parts.append(f'<div style="position:absolute;left:{gx - 20}px;top:{t.get("credit_bottom_y", 2024)}px;width:{gw + 40}px;height:44px;display:flex;justify-content:space-between;'
                         f'font-family:AGCn;font-style:italic;font-size:38px;line-height:44px;color:{cink};white-space:nowrap">{inner}</div>')
        else:
            parts.append(f'<div style="position:absolute;left:{gx - 60}px;top:{t.get("credit_bottom_y", 2024)}px;width:{gw + 120}px;height:44px;text-align:center;'
                         f'font-family:AGCn;font-style:italic;font-size:36px;line-height:44px;color:{cink};white-space:nowrap">{esc(cb)}</div>')
    sec('icons')
    if (t.get("landscape") or t.get("system")) and card.get("icons") and t.get("set_icon_abs"):
        sx_, sy_ = t["set_icon_abs"]; sz_ = t.get("set_icon_size", 60)
        for k, ic in enumerate(card["icons"]):   # margin discs the slip prints beside the set sphere (Episode I)
            f_ = ICON_FILES.get(ic) or ((f"icons/set-{ic[4:]}-decipher.png" if (ASSETS / f"icons/set-{ic[4:]}-decipher.png").exists() else f"icons/set-{ic[4:]}-grainy.png") if ic.startswith("set:") else None)
            if f_:
                parts.append(f'<img src="{data_uri(ASSETS / f_)}" style="position:absolute;left:{sx_}px;top:{sy_ - (k + 1) * (sz_ + 14)}px;width:{sz_}px;height:{sz_}px">')
    sec('caption')
    # bottom strip in the black border: title (as the slip prints it) left, card number right
    cap = card["caption"] if card.get("caption") is not None else card["title"]   # "" = no strip text (Decipher cards)
    cy = t.get("caption_y", 2082)
    if cap: parts.append(f'<div class="cap" style="position:absolute;left:160px;top:{cy}px;width:900px;height:52px">{game_text_html(cap)}</div>')
    sec('credits')
    if "game_text" not in t and (card.get("margin_left") or card.get("margin_right")) and t.get("landscape"):
        # locations: the slips print the credits up the left margin between the two bars (Carida (V)), reading top-down
        a_, b_ = (card.get("margin_left") or "").replace("\n", " "), (card.get("margin_right") or "").replace("\n", " ")
        parts.append(f'<div style="position:absolute;left:{t.get("credit_x", 186)}px;top:430px;width:44px;height:760px;display:flex;align-items:center;justify-content:center">'
                     f'<div style="flex-shrink:0;width:760px;transform:rotate(90deg);display:flex;justify-content:space-between;font-family:AGCn;font-style:italic;font-size:36px;color:#000;white-space:nowrap">'
                     f'<span>{esc(a_)}</span><span>{esc(b_)}</span></div></div>')
    sec('caption')
    if card.get("credit_strip"):   # a credit printed in the black caption strip, right, before the number (Watto (V), VS16)
        parts.append(f'<div style="position:absolute;right:{1632 - 1240}px;top:{cy + 4}px;height:48px;line-height:48px;font-family:AGCn;font-style:italic;'
                     f'font-size:38px;color:#fff;white-space:nowrap">{esc(card["credit_strip"])}</div>')
    sec('number')
    if card.get("number"):
        parts.append(f'<div class="num" style="position:absolute;right:230px;top:{cy}px;width:300px;height:52px">{esc(str(card["number"]).zfill(2) if str(card["number"]).isdigit() else str(card["number"]))}</div>')
    # wrap each piece's elements in a full-card layer (children keep their coordinates)
    ends = [i for _, i in marks[1:]] + [len(parts)]
    for (name, i), j in reversed(list(zip(marks, ends))):
        if name and j > i:
            parts[i:j] = [f'<div class="piece" data-piece="{name}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px">'] + parts[i:j] + ["</div>"]
    parts.append("</div>")
    ink = "#000" if t.get("dark_text") else "#fff"
    LP = dict(LORE_CSS, **card.get("_lore_css", {}))
    css = f"""
    {font_css}
    body{{margin:0;background:#000}}
    .inv .title, .inv .lore, .inv .ctype, .inv .gt, .inv .destiny {{rotate:180deg}}   /* Dagobah's upside-down cards (Through The Force Things You Will See) */
    .title{{font-family:Fiorello;font-size:80px;color:{t.get("title_ink", ink)};letter-spacing:1px;line-height:90px;white-space:nowrap}}
    .destiny{{font-family:AGMedExt;font-size:80px;color:#fff;display:flex;align-items:center;justify-content:center;padding-top:2px;box-sizing:border-box}}
    .lore{{font-family:{LP["ff"]};font-size:{LP["fs"]}px;color:{ink};letter-spacing:{LP["ls"]}px;line-height:{LP["lh"]}px;padding:{LP["pt"]}px 0 0 0;box-sizing:border-box;text-align:{card.get("lore_align", "left")};text-indent:{card.get("lore_indent", LP["ind"])}px}}
    .lore b{{font-family:AGCn;font-weight:bold}}
    .gt{{font-family:AGCn;font-size:{t.get("gt_size", 62)}px;color:{t.get("gt_ink", ink)};letter-spacing:0.5px;line-height:{t.get("gt_size", 62) + t.get("gt_lh_add", 3)}px;box-sizing:border-box;padding:6px 0 0 0;letter-spacing:0px;white-space:{"pre" if "\n" in card.get("game_text", "") else "normal"}}}
    .glyph{{font-family:"DejaVu Sans",sans-serif;font-size:1.0em;line-height:0;vertical-align:0.02em}}
    .tri{{font-family:"DejaVu Sans",sans-serif;font-size:0.88em;vertical-align:0.14em;line-height:0}}
    .gt b{{font-family:AGBoldCnA}}
    .gt-icon{{vertical-align:-9px;margin:0 3px}}
    .noicon{{display:inline-block;position:relative;width:62px;height:62px;border:6px solid #e3000f;border-radius:50%;box-sizing:border-box;vertical-align:-16px;margin:0 0 0 4px;overflow:hidden}}
    .noicon::after{{content:"";position:absolute;left:-8px;top:22px;width:70px;height:6px;background:#e3000f;transform:rotate(-45deg)}}
    .nol{{position:absolute;left:0;top:0;width:50px;height:50px;line-height:52px;text-align:center;font-family:AGBoldCnA;font-size:46px;color:{ink}}}
    .stat{{display:flex;align-items:center;padding-left:{t.get("stat_pl", 16)}px;padding-bottom:6px;box-sizing:border-box}}
    .stat .lab{{font-family:AGBoldCnA;font-size:55px;color:{t.get("stats_ink", ink)};letter-spacing:1.4px;-webkit-text-stroke:1.1px {t.get("stats_ink", ink)}}}
    .stat .val{{white-space:nowrap;font-family:AGMedExt;font-size:63px;color:{t.get("stats_ink", ink)};margin-left:30px;-webkit-text-stroke:1.1px {t.get("stats_ink", ink)};display:inline-block;transform:scaleX(1.15);transform-origin:left center}}
    .stat .val.r{{margin-left:auto;padding-left:30px;margin-right:{t.get("stat_pl", 16) + 26}px;transform-origin:right center}}
    .ctype{{font-family:AGBoldCnA;font-size:{t.get("ctype_size", 60)}px;color:{t.get("ctype_ink", ink)};letter-spacing:{t.get("ctype_spacing", 11)}px;text-align:center;line-height:{t.get("ctype_size", 60) + 1}px;white-space:nowrap}}
    .deploy{{font-family:Fiorello;font-size:70px;color:#000;display:flex;align-items:center;justify-content:center;padding-top:14px;box-sizing:border-box}}
    .forfeit{{font-family:Fiorello;font-size:70px;color:#fff;display:flex;align-items:center;justify-content:center;padding-top:14px;box-sizing:border-box}}
    .cap{{font-family:AGBoldCnA;font-size:48px;color:#fff;line-height:52px;white-space:nowrap}}
    .cap .dot{{font-size:40px}}
    .dot{{font-family:Fiorello}}
    .num{{font-family:AGMedExt;font-weight:bold;font-size:44px;color:#fff;line-height:52px;text-align:right;transform:skewX(-14deg)}}
    .ltitle, .dtitle{{font-family:AGBoldCnA;font-size:57px;letter-spacing:2px;text-transform:uppercase}}
    .ltext.pre span, .dtext.pre span{{white-space:pre}}
    .ltitle .dot, .dtitle .dot{{font-family:"DejaVu Sans",sans-serif;color:#d4141c;font-size:0.8em;margin-right:6px;vertical-align:0.05em}}
    .ltitle .dot.plain, .dtitle .dot.plain{{color:inherit}}
    .ltitle span.lt, .dtitle span.lt{{display:inline-block;white-space:nowrap;transform-origin:center center}}
    .ltitle{{color:#000;display:flex;align-items:center;justify-content:center;padding-top:6px;box-sizing:border-box}}
    .dtitle{{color:#fff;display:flex;align-items:center;justify-content:center;padding-top:6px;box-sizing:border-box;transform:rotate(180deg)}}
    .ltext{{font-family:AGCn;font-size:56px;color:#000;letter-spacing:1.5px;line-height:58px;display:flex;align-items:center;justify-content:center;text-align:center;box-sizing:border-box;padding:0 20px}}
    .dtext{{font-family:AGCn;font-size:56px;color:#fff;letter-spacing:1.5px;line-height:58px;display:flex;align-items:center;justify-content:center;text-align:center;box-sizing:border-box;padding:0 20px;transform:rotate(180deg)}}
    .parsec{{font-family:AGMedExt;font-size:72px;color:#fff;display:flex;align-items:center;justify-content:center;padding-top:4px;box-sizing:border-box}}
    .copy{{display:flex;align-items:center;justify-content:center}}
    .credit{{font-family:AGCn;font-style:italic;font-size:40px;color:#000;white-space:nowrap;transform:rotate(-90deg)}}
    .copyin{{font-family:AGBoldCnA;font-size:24px;color:{ink};letter-spacing:1px;white-space:nowrap;transform:rotate(-90deg)}}
    """
    fit_js = """
    document.fonts.ready.then(()=>{
      for (const el of document.querySelectorAll('.ctype')) {   // a long banner (HEAVILY-MODIFIED LIGHT FREIGHTER): tighten, then condense as the slip does
        const sp = el.querySelector('.ct'); if (!sp) continue;
        sp.style.display = 'inline-block';
        let ls = parseFloat(getComputedStyle(el).letterSpacing) || 0;
        while (sp.offsetWidth > el.clientWidth - 24 && ls > 0) { ls -= 0.5; el.style.letterSpacing = ls + 'px'; }
        if (sp.offsetWidth > el.clientWidth - 24) { sp.style.transform = 'scaleX(' + ((el.clientWidth - 24) / sp.offsetWidth) + ')'; }
      }
      for (const el of document.querySelectorAll('.fit')) {
        let size = parseFloat(getComputedStyle(el).fontSize);
        let lh = parseFloat(getComputedStyle(el).lineHeight);
        if (el.classList.contains('grow')) {   // Objectives: the slip's lines fill the box width — grow until a line would overflow
          while (el.scrollWidth <= el.clientWidth + 1 && el.scrollHeight <= el.clientHeight + 1 && size < 63) {   // the slips set Objectives in 62 px
            size += 1; lh += 1; el.style.fontSize = size + 'px'; el.style.lineHeight = lh + 'px';
          }
        }
        // too wide: tighten the tracking a little first (to -1.2 px), as the slips set a long line
        let ls = parseFloat(getComputedStyle(el).letterSpacing) || 0;
        while (el.scrollWidth > el.clientWidth + 1 && ls > -1.2) { ls -= 0.2; el.style.letterSpacing = ls + 'px'; }
        // too tall: tighten the line spacing first (to 0.94 em, as the slips do with a sixth line), then the size
        while (el.scrollHeight > el.clientHeight + 1 && lh > size * 0.94 && el.scrollWidth <= el.clientWidth + 1) {
          lh -= 1; el.style.lineHeight = lh + 'px';
        }
        while ((el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1) && size > 20) {
          size -= 1; lh -= 1; el.style.fontSize = size + 'px'; el.style.lineHeight = lh + 'px';
        }
      }
      let creditFs = 46;   // rotated credits: unrotated width = run length; both share one size, as the slips print them
      for (const el of document.querySelectorAll('.fitcredit')) {
        let fs = 46; const avail = parseFloat(el.dataset.avail);
        if (el.dataset.lines == '2') {   // the slip prints both credit lines side by side in one margin (Mon Mothma (V))
          fs = parseFloat(el.dataset.fs || 42); el.style.fontSize = fs + 'px'; el.style.lineHeight = '0.92'; el.style.flexShrink = '0'; el.style.textAlign = 'center';
          while (el.offsetWidth > avail && fs > 20) { fs -= 1; el.style.fontSize = fs + 'px'; }
          el.dataset.solo = '1'; continue;
        }
        while (el.offsetWidth > avail && fs > 20) { fs -= 1; el.style.fontSize = fs + 'px'; }
        if (fs < 34) {   // too small on one line: two lines, as The Emperor (V) slip prints "Original concept / by Mike Gemme"
          el.style.whiteSpace = 'normal'; el.style.flexShrink = '0'; el.style.textWrap = 'balance'; el.style.width = avail + 'px'; el.style.textAlign = 'center';
          fs = 34; el.style.fontSize = fs + 'px'; el.style.lineHeight = '1.0';
          while (el.offsetHeight > 2.05 * fs && fs > 20) { fs -= 1; el.style.fontSize = fs + 'px'; }
        }
        creditFs = Math.min(creditFs, fs);
      }
      const cr = [...document.querySelectorAll('.fitcredit')].filter(e => !e.dataset.solo);
      if (cr.length == 2 && cr[0].dataset.avail == cr[1].dataset.avail) for (const el of cr) el.style.fontSize = creditFs + 'px';
      for (const el of document.querySelectorAll('.ltitle .lt, .dtitle .lt')) {   // location bar titles: condense to the bar
        const avail = el.parentElement.clientWidth - 30, w = el.offsetWidth;
        if (w > avail) el.style.transform = 'scaleX(' + (avail / w).toFixed(3) + ')';
      }
      for (const el of document.querySelectorAll('.title')) {   // a title longer than its bar is condensed, as Decipher did
        const w = el.scrollWidth, avail = el.clientWidth;
        if (w > avail + 1) { el.style.transformOrigin = 'left center'; el.style.transform = 'scaleX(' + (avail / w).toFixed(3) + ')'; el.style.width = w + 'px'; }
      }
      for (const st of document.querySelectorAll('.stat')) {   // label + gap + value too wide for the box: condense the label (Bill: Green Squadron 1 (V))
        const lab = st.querySelector('.lab'), val = st.querySelector('.val');
        if (!lab || !val || lab.classList.contains('fitlab')) continue;
        const cs = getComputedStyle(st), inner = st.clientWidth - parseFloat(cs.paddingLeft);
        const vp = parseFloat(getComputedStyle(val).paddingLeft) || 0; let need = lab.offsetWidth + (val.offsetWidth - vp) * 1.15 + vp + (parseFloat(getComputedStyle(val).marginRight) || 0);
        if (val.classList.contains('r')) {   // narrow (character) boxes: the value closes up to the label and the box end first
          const mr = parseFloat(getComputedStyle(val).marginRight) || 0, w0 = lab.offsetWidth * 1.1 + (val.offsetWidth - vp) * 1.15;
          const slack = inner - w0 - vp - mr;
          if (slack < 0) { const cut = Math.min(-slack, (vp - 28) + (mr - 18)); const a = Math.min(vp - 28, cut / 2 + Math.max(0, cut / 2 - (mr - 18)));
            val.style.paddingLeft = (vp - a) + 'px'; val.style.marginRight = (mr - (cut - a)) + 'px'; }
        }
        { const vp2 = parseFloat(getComputedStyle(val).paddingLeft) || 0;
          need = lab.offsetWidth + (val.offsetWidth - vp2) * 1.15 + vp2 + (parseFloat(getComputedStyle(val).marginRight) || 0); }
        // Decipher's stat caps are wider than AG Bold Condensed: widen the label ×1.1 (Bill: Lord Vader (V)), less if the box is tight
        const k = Math.max(0.8, Math.min(1.1, (inner - (need - lab.offsetWidth)) / lab.offsetWidth));
        { lab.style.display = 'inline-block'; lab.style.transformOrigin = 'left center'; lab.style.transform = 'scaleX(' + k.toFixed(3) + ')'; lab.style.marginRight = (-(1 - k) * lab.offsetWidth) + 'px'; }
      }
      for (const st of document.querySelectorAll('.stat')) {   // a value still too wide for its box (3333): condense it, then shrink it
        const val = st.querySelector('.val'); if (!val) continue;
        const sr = st.getBoundingClientRect(), vr = val.getBoundingClientRect();
        const over = vr.right - (sr.right - 8);
        if (over > 0) {
          const k = Math.max(0.5, (vr.width - over) / vr.width) * 1.15;
          val.style.transform = 'scaleX(' + k.toFixed(3) + ')';
          const vr2 = val.getBoundingClientRect(); const over2 = vr2.right - (sr.right - 8);
          if (over2 > 0) val.style.fontSize = Math.max(28, 63 * (vr2.width - over2) / vr2.width).toFixed(1) + 'px';
        }
      }
      for (const el of document.querySelectorAll('.fitnum')) {   // destiny / deploy / forfeit: condense to the box (≥55 %), then shrink
        el.style.display = 'inline-block'; el.style.whiteSpace = 'nowrap'; el.style.transformOrigin = 'center center';
        const avail = parseFloat(el.dataset.avail), w = el.getBoundingClientRect().width;
        if (w > avail) {
          const k = Math.max(0.55, avail / w); el.style.transform = 'scaleX(' + k.toFixed(3) + ')';
          if (w * k > avail) { const fs = parseFloat(getComputedStyle(el).fontSize); el.style.fontSize = (fs * avail / (w * k)).toFixed(1) + 'px'; }
        }
      }
      for (const el of document.querySelectorAll('.fitlab')) {   // label-only stat: squeeze to the well, keep the height
        const avail = parseFloat(el.dataset.avail), w = el.getBoundingClientRect().width;
        if (w > avail) el.style.transform = 'scaleX(' + (avail / w).toFixed(3) + ')';
      }
      { // card maker layers: per-piece offset / scale / hide (applied after all fitting), then report each piece's box
        const LAYOUT = __LAYOUT__, boxes = {};
        const union = (el) => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
          for (const c of el.querySelectorAll('*')) { const r = c.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
            x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); }
          return x1 > x0 ? [x0, y0, x1 - x0, y1 - y0] : null; };
        const card = document.getElementById('card').getBoundingClientRect();
        for (const el of document.querySelectorAll('.piece')) {
          const L = LAYOUT[el.dataset.piece]; if (!L) continue;
          const u = union(el); if (u) el.style.transformOrigin = (u[0] - card.left + u[2] / 2) + 'px ' + (u[1] - card.top + u[3] / 2) + 'px';
          el.style.translate = (L.dx || 0) + 'px ' + (L.dy || 0) + 'px';
          el.style.scale = (L.sx || 1) + ' ' + (L.sy || 1);
          if (L.hidden) el.style.visibility = 'hidden';
        }
        for (const el of document.querySelectorAll('.piece')) {
          const u = union(el); if (!u) continue; const n = el.dataset.piece, b = [u[0] - card.left, u[1] - card.top, u[2], u[3]];
          if (boxes[n]) { const a = boxes[n]; const x0 = Math.min(a[0], b[0]), y0 = Math.min(a[1], b[1]);
            boxes[n] = [x0, y0, Math.max(a[0] + a[2], b[0] + b[2]) - x0, Math.max(a[1] + a[3], b[1] + b[3]) - y0]; } else boxes[n] = b;
        }
        document.body.dataset.boxes = JSON.stringify(boxes);
      }
      document.body.dataset.ready = '1';
    });
    """
    lay = {re.sub(r"[^a-z_]", "", str(k)): {kk: (bool(v.get(kk)) if kk == "hidden" else max(-2000.0, min(2000.0, float(v.get(kk))))
                                               if kk in ("dx", "dy") else max(0.2, min(4.0, float(v.get(kk)))))
                                          for kk in ("dx", "dy", "sx", "sy", "hidden") if v.get(kk) is not None}
           for k, v in (card.get("layout") or {}).items() if isinstance(v, dict)}
    fit_js = fit_js.replace("__LAYOUT__", json.dumps(lay))
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(parts)}<script>{fit_js}</script></body></html>"


def rounded(img: Image.Image, radius: int) -> Image.Image:
    """Rounded corners (real cards and GEMP's images): transparent outside a rounded rectangle."""
    from PIL import ImageDraw
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=radius, fill=255)
    out = img.convert("RGBA")
    out.putalpha(m)
    return out


def screenshot_card(card: dict, page) -> Image.Image:
    """Render one card with an open Playwright page: the 600 DPI master (1632x2220 / 2220x1632), Dark locations turned
    to the Dark Side's seat, rounded corners. Shared by render() and the card maker web service."""
    import io
    html = build_html(card)
    page.set_content(html, wait_until="load")
    page.wait_for_function("document.body.dataset.ready==='1'")
    im = Image.open(io.BytesIO(page.locator("#card").screenshot())).convert("RGBA")
    try:
        card["_boxes"] = json.loads(page.evaluate("document.body.dataset.boxes || '{}'"))
    except Exception:   # noqa: BLE001
        card["_boxes"] = {}
    if card.get("side") == "Dark" and card["template"] in ("loc-site", "loc-system"):
        # Dark locations are shown from the Dark Side's seat, as Decipher prints them (Executor: Comm Station): the
        # whole card turned 180° (Dark half, its icons and credits at the bottom); the caption strip stays upright
        # in the bottom margin (Bill 2026-10-14).
        card["_boxes"] = {k: [im.width - b[0] - b[2], im.height - b[1] - b[3], b[2], b[3]] for k, b in card.get("_boxes", {}).items()}
        rot = im.rotate(180)
        rot.paste(im.crop((0, 0, im.width, 144)), (0, 0))
        rot.paste(im.crop((0, im.height - 145, im.width, im.height)), (0, im.height - 145))
        ax, ay, aw, ah = TEMPLATES[card["template"]]["art"]   # the picture itself stays upright
        DL, DD = loc_grow(card) if card["template"] == "loc-site" else (0, 0)
        y0, y1 = ay + DD, ay + ah - DL
        box = (im.width - 1 - (ax + aw - 1), im.height - 1 - (y1 - 1), im.width - (ax), im.height - y0)
        rot.paste(rot.crop(box).rotate(180), box[:2])
        im = rot
    return rounded(im, 80)


def holotable_size(master: Image.Image, land: bool) -> Image.Image:
    """Holotable size: the whole master at half scale (816×1110), cropped to 745×1039 so the card area lands at
    (37,36) like the PC's images, keeping the bottom caption strip in the border."""
    if land:
        im = master.convert("RGB").resize((1110, 816), Image.LANCZOS)
        return rounded(im.crop((36, 35, 1075, 780)), 34)
    im = master.convert("RGB").resize((816, 1110), Image.LANCZOS)
    return rounded(im.crop((35, 36, 780, 1075)), 34)


def render(card: dict) -> tuple[Path, Path]:
    from playwright.sync_api import sync_playwright
    OUT.mkdir(exist_ok=True)
    land = is_wide(TEMPLATES[card["template"]])
    (OUT / f"{card['id']}.html").write_text(build_html(card), encoding="utf-8")
    master = OUT / f"{card['id']}_{'2220' if land else '1632'}.png"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        im = screenshot_card(card, pg)
        b.close()
    im.save(master)
    htp = OUT / f"{card['id']}_{'1039' if land else '745'}.png"
    holotable_size(im, land).save(htp, optimize=True)
    return master, htp


if __name__ == "__main__":
    for f in sys.argv[1:]:
        card = json.loads(Path(f).read_text(encoding="utf-8"))
        m, h = render(card)
        print(card["id"], m.stat().st_size // 1024, "KB", h.stat().st_size // 1024, "KB")
