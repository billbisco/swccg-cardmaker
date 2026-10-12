"""SWCCG card renderer: card JSON + template → PNG (1632×2220 print master, 745×1039 Holotable/GEMP).

Layout numbers come from Bardez's 600 DPI GIMP templates (wiki.swccg.com/wiki/Making_Custom_SWCCG_Cards):
the card area is 1343×1931 at (144,144) on a 1632×2220 black bleed. A Holotable image (745×1039) is that
card area at half scale with a ~37 px black border, so one render serves both.
"""
from __future__ import annotations
import base64, json, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "out"
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
        "card_type": (621, 1508, 399, 61),
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
        "ls_text": (250, 1341, 1719, 120),
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
        "caption_y": 2082,
    },
}

ICON_FILES = {
    "pilot": "icons/pilot.png", "warrior": "icons/warrior.png", "pilot-light": "icons/pilot-light-745.png", "warrior-light": "icons/warrior-light-745.png",
    "alter": "icons/VS-icon-immune-alter.png", "control": "icons/VS-icon-immune-control.png",
    "sense": "icons/VS-icon-immune-sense.png", 
    "grabber": "icons/grabber-fist.png", "pilotpower": "icons/VS-icon-pilot-power-x.png",
    "lightsaber": "icons/inline-permanent-weapon.png", "permanent-weapon": "icons/inline-permanent-weapon.png",
    "republic": "icons/inline-maintenance.png", "maintenance": "icons/inline-maintenance.png", "nav": "icons/inline-nav.png",
    "astromech": "icons/astromech-bardez.png",
}


def data_uri(path: Path) -> str:
    mime = "font/otf" if path.suffix == ".otf" else "image/png" if path.suffix == ".png" else "image/gif"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def icon_img(name: str, h: int = 64) -> str:
    return f'<img class="gt-icon" src="{data_uri(ASSETS / ICON_FILES[name])}" style="height:{h}px">'


def game_text_html(text: str) -> str:
    """{pilot:2} → pilot-power icon + number; {alter} {control} {sense} {maintenance} {grabber} {lightsaber} → icons.
    ▲ / ▼ (PC shorthand triangles) pass through as text. *bold* → bold."""
    out = []
    pos = 0
    for m in re.finditer(r"\{([\w-]+)(?::([^}]*))?\}", text):
        out.append(esc(text[pos:m.start()]))
        name, arg = m.group(1), m.group(2)
        if name == "pilot":
            out.append(icon_img("pilotpower") + f" {esc(arg or '')}")
        elif name in ("alter", "control", "sense"):
            # the slips' red "no" circle with the letter: drawn (transparent), not a pasted raster
            out.append(f'<span class="noicon"><span class="nol">{name[0].upper()}</span></span>')
        elif name == "set":   # expansion-set symbol inline, e.g. {set:anh} = "the A New Hope R2-D2"
            out.append(f'<img class="gt-icon" src="{data_uri(ASSETS / f"icons/set-{arg}-grainy.png")}" style="height:56px">')
        else:
            out.append(icon_img(name))
        pos = m.end()
    out.append(esc(text[pos:]))
    html = "".join(out)
    html = html.replace("•", '<span class="dot">•</span>')
    html = re.sub(r"\*(.+?)\*", r"<b>\1</b>", html)
    html = re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"<i>\1</i>", html)
    html = html.replace("▲", "<span class=tri>▲</span>").replace("▼", "<span class=tri>▼</span>")
    return html.replace("\n", "<br>")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def art_crop(card: dict) -> str:
    """Crop the art window out of a Decipher scan (any size: the silver frame is located, then mapped)."""
    src = Path(card["art"]["src"])
    im = Image.open(src).convert("RGB")
    import numpy as np
    a = np.array(im).astype(int)
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
    ax, ay, aw, ah = TEMPLATES[card["template"]]["art"]
    box = (fx0 + (ax - 144) * sx, fy0 + (ay - 144) * sy, fx0 + (ax + aw - 144) * sx, fy0 + (ay + ah - 144) * sy)
    crop = im.crop(tuple(int(round(v)) for v in box))
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
    p = OUT / f"_art_{card['id']}.png"
    crop.save(p)
    return data_uri(p)


LOC = ASSETS / "loc"
LOC_ICON_FILES = {k: f"icon-{k}.png" for k in
                  ("underground", "interior", "planet", "space", "exterior", "underwater", "creature", "mobile", "starship", "vehicle")}


def loc_frame(card: dict, t: dict) -> Path:
    """Assemble a landscape location frame for this card from Bardez's layers: light-saber glows under the
    frame's force-icon holes, the icon boxes packed from the outside in (as Decipher printed them), scomp-link
    rings. Icons are given per side, outermost first: e.g. ["scomp", "planet", "interior", "underground"]."""
    fx, fy = t["frame_off"]
    frame = Image.open(ASSETS / "frames/loc-site.png").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.open(LOC / "force-light.png").convert("RGBA")
    gx, gy = t["ls_force"]
    if card.get("light_force", True):
        canvas.alpha_composite(glow, (fx + gx, fy + gy))
    if card.get("dark_force", False):
        g = glow.rotate(180)
        # mirror of the light glow box about the card centre (frame coords: x' = 2071-x-w, y' = 1479-y-h)
        canvas.alpha_composite(g, (fx + 2071 - gx - glow.width, fy + 1479 - gy - glow.height))
    canvas.alpha_composite(frame, (fx, fy))
    # cover the two default icon boxes on each bar with a clean patch of the bar
    ly = t["slot_y"]
    patch = frame.crop((900, ly - 8, 1100, ly + 119))
    for x in (1583, 1691):
        canvas.alpha_composite(patch.crop((0, 0, 100, 127)), (fx + x - 6, fy + ly - 8))
    dy = 1479 - ly - 111
    dpatch = frame.crop((1000, dy - 8, 1200, dy + 119))
    for x in (288, 395):
        canvas.alpha_composite(dpatch.crop((0, 0, 100, 127)), (fx + x - 6, fy + dy - 8))
    box = Image.open(LOC / "box.png").convert("RGBA")
    ring = Image.open(LOC / "scomp.png").convert("RGBA")

    def place(icons, light):
        # Boxes are cut from the printed Hoth card (brighter than Bardez's), 100×94, sitting inside the title bar.
        by = ly - 7
        dby = 1479 - by - 94
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
            y = ly if light else dy
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
        canvas.alpha_composite(Image.open(LOC / "sysforce-light.png").convert("RGBA"), t["ls_force"])
    if card.get("dark_force", False):
        canvas.alpha_composite(Image.open(LOC / "sysforce-dark.png").convert("RGBA"), t["ds_force"])
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


def build_html(card: dict) -> str:
    t = TEMPLATES[card["template"]]
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
    W, H = (2220, 1632) if t.get("landscape") else (1632, 2220)
    if t.get("landscape"):
        fr, fx, fy = loc_frame(card, t), 0, 0
    elif t.get("system"):
        fr, fx, fy = sys_frame(card, t), 0, 0
    else:
        fr, fx, fy = t["frame"]
        fr = ASSETS / fr
    ax, ay, aw, ah = t["art"]
    art = art_crop(card) if card.get("art") else ""

    def box(key, style=""):
        x, y, w, h = t[key]
        return f"left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}"

    parts = [f'<div id="card" style="position:relative;width:{W}px;height:{H}px;background:#000;overflow:hidden">']
    if art:
        parts.append(f'<img src="{art}" style="position:absolute;left:{ax}px;top:{ay}px;width:{aw}px;height:{ah}px">')
    parts.append(f'<img src="{data_uri(fr)}" style="position:absolute;left:{fx}px;top:{fy}px">')
    # title + destiny
    if t.get("landscape"):
        # Light title centred in the grey bar between the force slot and the first icon box; Dark mirrored, rotated.
        nbox = len([i for i in card.get("light_icons", []) if i != "scomp"])
        x0, y, h = t["ls_bar"]
        x1 = t["ls_bar_x1"] if nbox == 0 else fx + t["ls_slot0"] - (nbox - 1) * t["slot_pitch"] - 55 + t["frame_off"][0]
        parts.append(f'<div class="title ltitle" style="position:absolute;left:{x0}px;top:{y}px;width:{x1 - x0}px;height:{h}px">{esc(card["title"])}</div>')
        nbox = len([i for i in card.get("dark_icons", []) if i != "scomp"])
        dx, dy_, dw, dh = t["ds_bar"]
        dx0 = dx if nbox == 0 else t["frame_off"][0] + t["ds_slot0"] + (nbox - 1) * t["slot_pitch"] + 55
        parts.append(f'<div class="title dtitle" style="position:absolute;left:{dx0}px;top:{dy_}px;width:{dx + dw - dx0}px;height:{dh}px">{esc(card["title"])}</div>')
        lx, ly_, lw, lh = t["ls_text"]
        parts.append(f'<div class="ltext fit" style="position:absolute;left:{lx}px;top:{ly_}px;width:{lw}px;height:{lh}px"><span>{game_text_html(card["game_text"])}</span></div>')
        tx, ty, tw, th = t["ds_text"]
        parts.append(f'<div class="dtext fit" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px"><span>{game_text_html(card["dark_text"])}</span></div>')
    elif t.get("system"):
        x, y, w, h = t["ls_bar"]
        parts.append(f'<div class="title ltitle" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{esc(card["title"])}</div>')
        x, y, w, h = t["ds_bar"]
        parts.append(f'<div class="title dtitle" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{esc(card["title"])}</div>')
        x, y, w, h = t["ls_text"]
        parts.append(f'<div class="ltext fit" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span>{game_text_html(card["game_text"])}</span></div>')
        x, y, w, h = t["ds_text"]
        parts.append(f'<div class="dtext fit" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span>{game_text_html(card["dark_text"])}</span></div>')
        if card.get("parsec") is not None:
            x, y, w, h = t["ls_parsec"]
            parts.append(f'<div class="parsec" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{esc(str(card["parsec"]))}</div>')
            x, y, w, h = t["ds_parsec"]
            parts.append(f'<div class="parsec" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate(180deg)">{esc(str(card["parsec"]))}</div>')
    else:
        parts.append(f'<div class="title" style="position:absolute;{box("title")}">{esc(card["title"])}</div>')
    if card.get("destiny"):
        dv = esc(card["destiny"])
        if " or " in dv:   # multi-value destiny (R2-D2 "2 or 5"): the printed pill is widened to the left
            x, y, w, h = t["destiny"]
            ext = 150
            parts.append(f'<div style="position:absolute;left:{x - ext - 6}px;top:{y - 6}px;width:{w + ext + 12}px;height:{h + 12}px;background:#000;border:6px solid #d0d0d2;border-radius:{h // 2 + 6}px;box-sizing:border-box"></div>')
            parts.append(f'<div class="destiny" style="position:absolute;left:{x - ext}px;top:{y}px;width:{w + ext}px;height:{h}px;font-size:80px;white-space:nowrap;padding-top:4px">{dv.replace(" or ", "<span style=\"font-size:46px\">&nbsp;or&nbsp;</span>")}</div>')
        else:
            parts.append(f'<div class="destiny" style="position:absolute;{box("destiny")}">{dv}</div>')
    # lore
    if card.get("lore"):
        parts.append(f'<div class="lore fit" style="position:absolute;{box("lore")}">{game_text_html(card["lore"])}</div>')
    # stats (character)
    if "stats" in t and card.get("stats"):
        y = t["stats_y"]
        stats = list(card["stats"])
        if len(stats) == 2 and stats[1][0] not in ("ABILITY", "ARMOR", "MANEUVER") and "stats_wide" in t:
            # droids: one wide box (e.g. ASTROMECH DROID) spans the ability + third slots
            wx, ww = t["stats_wide"]
            parts.append(f'<div style="position:absolute;left:{wx}px;top:{y}px;width:{ww}px;height:69px;background:{t.get("stats_wide_fill", "#000")};border-radius:6px"></div>')
            boxes = [t["stats"][0], (wx, ww)]
        else:
            boxes = t["stats"]
        for (x, w), (label, value) in zip(boxes, stats):
            parts.append(f'<div class="stat" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:68px">'
                         f'<span class="lab">{esc(label)}</span>{"<span class=val>" + esc(value) + "</span>" if value else ""}</div>')
    if "card_type" in t and card.get("card_type"):
        parts.append(f'<div class="ctype" style="position:absolute;{box("card_type")}">{esc(card["card_type"])}</div>')
    if card.get("banner_icon") and "banner_icon" in t:
        bx, by = t["banner_icon"]
        parts.append(f'<img src="{data_uri(ASSETS / "icons/icon-box-effect.png")}" style="position:absolute;left:{bx}px;top:{by}px">')
        parts.append(f'<img src="{data_uri(ASSETS / ICON_FILES[card["banner_icon"]])}" style="position:absolute;left:{bx + 8}px;top:{by + 8}px;width:73px;height:73px">')
    # game text
    if "game_text" in t:
        parts.append(f'<div class="gt fit" style="position:absolute;{box("game_text")}">{game_text_html(card["game_text"])}</div>')
    # deploy / forfeit
    if card.get("deploy") is not None and "deploy" in t:
        parts.append(f'<div class="deploy" style="position:absolute;{box("deploy")}">{esc(str(card["deploy"]))}</div>')
        parts.append(f'<div class="forfeit" style="position:absolute;{box("forfeit")}">{esc(str(card["forfeit"]))}</div>')
    if card.get("scomp") and "scomp" in t:
        sx, sy = t["scomp"]
        parts.append(f'<img src="{data_uri(ASSETS / "icons/scomp-ship.png")}" style="position:absolute;left:{sx}px;top:{sy}px">')
    # icon slots
    light = card.get("side") == "Light"
    for (x, y), name in zip(t.get("icon_slots", []), card.get("icons", [])):
        key = f"{name}-light" if light and f"{name}-light" in ICON_FILES else name   # Light and Dark pilot icons differ
        parts.append(f'<img src="{data_uri(ASSETS / "icons/icon-box.png")}" style="position:absolute;left:{x}px;top:{y}px">')
        parts.append(f'<img src="{data_uri(ASSETS / ICON_FILES[key])}" style="position:absolute;left:{x + 6}px;top:{y + 7}px;width:75px;height:75px">')
    # original-era virtual marker: the slips print the gold virtual-set symbol in the lower icon slot
    if card.get("virtual_set") is not None and "set_icon_abs" in t:
        x, y = t["set_icon_abs"]
        sym = ASSETS / f"icons/ovs-set-{card['virtual_set']}.png"   # each original set has its own symbol (from its Remaster PDF)
        ss = t.get("set_icon_size", 76)
        parts.append(f'<img src="{data_uri(sym)}" style="position:absolute;left:{x}px;top:{y}px;width:{ss}px;height:{ss}px">')
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
    # vertical Lucasfilm / Decipher line on the right margin of the art, as on the printed card
    if card.get("copyright"):
        cx, cy, cw, ch = t.get("copyright", (t.get("copyright_x", 1404), ay, 36, ah))
        parts.append(f'<div class="copy" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px">'
                     f'<div class="copyin">{esc(card["copyright"])}</div></div>')
    # slip credit lines in the side margins (Wokling (V): "Original concept by …" left, "GenCon 2002 Winner" right),
    # italic, reading bottom-to-top, spanning the banner + text box
    for key, x in (("margin_left", 222), ("margin_right", 1388)):
        if card.get(key):
            gx, gy, gw, gh = t["game_text"]
            cx_, cy_, cw_, ch_ = t.get("card_type", (gx, gy - 160, gw, 61))
            top, bot = cy_, gy + gh
            parts.append(f'<div class="copy" style="position:absolute;left:{x}px;top:{top}px;width:40px;height:{bot - top}px">'
                         f'<div class="credit">{esc(card[key])}</div></div>')
    # bottom strip in the black border: title (as the slip prints it) left, card number right
    cap = card.get("caption") or card["title"]
    cy = t.get("caption_y", 2082)
    parts.append(f'<div class="cap" style="position:absolute;left:160px;top:{cy}px;width:900px;height:52px">{game_text_html(cap)}</div>')
    if card.get("number"):
        parts.append(f'<div class="num" style="position:absolute;right:230px;top:{cy}px;width:300px;height:52px">{esc(str(card["number"]).zfill(2) if str(card["number"]).isdigit() else str(card["number"]))}</div>')
    parts.append("</div>")
    ink = "#000" if t.get("dark_text") else "#fff"
    css = f"""
    {font_css}
    body{{margin:0;background:#000}}
    .title{{font-family:Fiorello;font-size:80px;color:{ink};letter-spacing:1px;line-height:90px;white-space:nowrap}}
    .destiny{{font-family:AGMedExt;font-size:80px;color:#fff;display:flex;align-items:center;justify-content:center;padding-top:2px;box-sizing:border-box}}
    .lore{{font-family:AGLightCn;font-size:58px;color:{ink};letter-spacing:0.8px;line-height:60px;padding:4px 110px 0 10px;box-sizing:border-box;text-align:{card.get("lore_align", "left")};text-indent:{card.get("lore_indent", 60)}px}}
    .lore b{{font-family:AGCn;font-weight:bold}}
    .gt{{font-family:AGCn;font-size:62px;color:{ink};letter-spacing:0.5px;line-height:65px;box-sizing:border-box;padding:6px 0 0 0;letter-spacing:0px}}
    .tri{{font-family:"DejaVu Sans",sans-serif;font-size:0.88em;vertical-align:0.14em;line-height:0}}
    .gt b{{font-family:AGBoldCnA}}
    .gt-icon{{vertical-align:-9px;margin:0 3px}}
    .noicon{{display:inline-block;position:relative;width:62px;height:62px;border:6px solid #e3000f;border-radius:50%;box-sizing:border-box;vertical-align:-16px;margin:0 0 0 4px;overflow:hidden}}
    .noicon::after{{content:"";position:absolute;left:-8px;top:22px;width:70px;height:6px;background:#e3000f;transform:rotate(-45deg)}}
    .nol{{position:absolute;left:0;top:0;width:50px;height:50px;line-height:52px;text-align:center;font-family:AGBoldCnA;font-size:46px;color:{ink}}}
    .stat{{display:flex;align-items:center;padding-left:22px;box-sizing:border-box}}
    .stat .lab{{font-family:AGBoldCnA;font-size:56px;color:{t.get("stats_ink", ink)};letter-spacing:1.8px}}
    .stat .val{{font-family:AGMedExt;font-weight:bold;font-size:60px;color:{t.get("stats_ink", ink)};margin-left:26px}}
    .ctype{{font-family:AGBoldCnA;font-size:60px;color:{ink};letter-spacing:{t.get("ctype_spacing", 11)}px;text-align:center;line-height:61px;white-space:nowrap}}
    .deploy{{font-family:Fiorello;font-size:70px;color:#000;display:flex;align-items:center;justify-content:center;padding-top:14px;box-sizing:border-box}}
    .forfeit{{font-family:Fiorello;font-size:70px;color:#fff;display:flex;align-items:center;justify-content:center;padding-top:14px;box-sizing:border-box}}
    .cap{{font-family:AGBoldCnA;font-size:48px;color:#fff;line-height:52px;white-space:nowrap}}
    .cap .dot{{font-size:40px}}
    .dot{{font-family:Fiorello}}
    .num{{font-family:AGMedExt;font-weight:bold;font-size:44px;color:#fff;line-height:52px;text-align:right;transform:skewX(-14deg)}}
    .ltitle{{color:#000;display:flex;align-items:center;justify-content:center;padding-top:6px;box-sizing:border-box}}
    .dtitle{{color:#fff;display:flex;align-items:center;justify-content:center;padding-top:6px;box-sizing:border-box;transform:rotate(180deg)}}
    .ltext{{font-family:AGCn;font-size:62px;color:#000;letter-spacing:0.5px;line-height:65px;display:flex;align-items:center;justify-content:center;text-align:center;box-sizing:border-box;padding:0 20px}}
    .dtext{{font-family:AGCn;font-size:62px;color:#fff;letter-spacing:0.5px;line-height:65px;display:flex;align-items:center;justify-content:center;text-align:center;box-sizing:border-box;padding:0 20px;transform:rotate(180deg)}}
    .parsec{{font-family:Craft;font-size:65px;color:#fff;display:flex;align-items:center;justify-content:center;padding-top:4px;box-sizing:border-box}}
    .copy{{display:flex;align-items:center;justify-content:center}}
    .credit{{font-family:AGCn;font-style:italic;font-size:40px;color:#000;white-space:nowrap;transform:rotate(-90deg)}}
    .copyin{{font-family:AGBoldCnA;font-size:24px;color:{ink};letter-spacing:1px;white-space:nowrap;transform:rotate(-90deg)}}
    """
    fit_js = """
    document.fonts.ready.then(()=>{
      for (const el of document.querySelectorAll('.fit')) {
        let size = parseFloat(getComputedStyle(el).fontSize);
        let lh = parseFloat(getComputedStyle(el).lineHeight);
        while (el.scrollHeight > el.clientHeight + 1 && size > 20) {
          size -= 1; lh -= 1; el.style.fontSize = size + 'px'; el.style.lineHeight = lh + 'px';
        }
      }
      document.body.dataset.ready = '1';
    });
    """
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(parts)}<script>{fit_js}</script></body></html>"


def render(card: dict) -> tuple[Path, Path]:
    from playwright.sync_api import sync_playwright
    OUT.mkdir(exist_ok=True)
    html = build_html(card)
    land = TEMPLATES[card["template"]].get("landscape", False)
    hp = OUT / f"{card['id']}.html"
    hp.write_text(html, encoding="utf-8")
    master = OUT / f"{card['id']}_{'2220' if land else '1632'}.png"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(hp.as_uri())
        pg.wait_for_function("document.body.dataset.ready==='1'")
        pg.locator("#card").screenshot(path=str(master))
        b.close()
    # Rounded corners (real cards and GEMP's images): transparent outside a rounded rectangle.
    def rounded(img: Image.Image, radius: int) -> Image.Image:
        from PIL import ImageDraw
        m = Image.new("L", img.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=radius, fill=255)
        out = img.convert("RGBA")
        out.putalpha(m)
        return out
    rounded(Image.open(master), 80).save(master)
    # Holotable size: the whole master at half scale (816×1110), cropped to 745×1039 so the card area
    # lands at (37,36) like the PC's images, keeping the bottom caption strip in the border.
    if land:
        im = Image.open(master).convert("RGB").resize((1110, 816), Image.LANCZOS)
        ht = rounded(im.crop((36, 35, 1075, 780)), 34)
        htp = OUT / f"{card['id']}_1039.png"
    else:
        im = Image.open(master).convert("RGB").resize((816, 1110), Image.LANCZOS)
        ht = rounded(im.crop((35, 36, 780, 1075)), 34)
        htp = OUT / f"{card['id']}_745.png"
    ht.save(htp, optimize=True)
    return master, htp


if __name__ == "__main__":
    for f in sys.argv[1:]:
        card = json.loads(Path(f).read_text(encoding="utf-8"))
        m, h = render(card)
        print(card["id"], m.stat().st_size // 1024, "KB", h.stat().st_size // 1024, "KB")
