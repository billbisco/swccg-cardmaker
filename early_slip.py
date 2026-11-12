"""Early Virtual slips (STANDARD rev 75): the Players Committee's first Virtual Card sheets (Virtual Set #1, 6 March
2002, decipher.com/starwars/cardlists/virtual/VirtualCards1.pdf), printed before the PC drew its slips on Decipher's
templates. Each slip was cut out below its title label and laid in an opaque sleeve over the bottom of the original
card, cut to its outline ("being careful not to obscure any icons"), so a card "as played" is the printed Decipher
card with these pieces over its lower quarter: a black U (the card's border), a flat colour band, a white text box with a thin black rule, and on characters the new
deploy / forfeit in two small boxes (white / black) and a grey panel notched on the right to leave the icons showing.

Every number here is measured on the vector PDF (Adobe Illustrator 9, PyMuPDF drawings + spans): points, x from the
slip's left edge (179.13 pt wide = the card), y upward from the slip's bottom edge (= the card's bottom). The slip
is mapped onto the 1343x1931 card area at (144,144) of the 1632x2220 master, bottom on bottom, full width.

Kinds: "character" (Luke Skywalker (V), BoShek (V), Darth Vader (V), Prophetess (V)), "starship" (Gold 1 (V),
Black 2 (V)), "band" (weapons, devices, effects: Han's Heavy Blaster Pistol (V), Assault Rifle (V), Fusion Generator
Supply Tanks (V) x2, Sai'torr Kal Fas (V), Blaster Rack (V)). Interrupts, locations, vehicles, creatures and
objectives were not on the sheet: they take the band kind with the Effect colours unless the spec gives `colour`.
"""
from __future__ import annotations
import re

SLIP_W = 179.13          # pt, the printed slip = the card's width
BLACK = "rgb(35,31,32)"  # the sheet's process black (13.7 %, 12.2 %, 12.5 %)
BAR = 8.95               # bottom bar (the card's black border)
LEG = 8.66               # left / right legs
RIGHT_LEG_X = 169.90
CORNER = (3.78, 4.47)    # rounded outer corners (x, y radius)

COLOURS = {   # (kind, side) -> band colour, measured fills
    ("character", "Light"): "rgb(211,210,210)", ("character", "Dark"): "rgb(94,91,92)",
    ("starship", "Light"): "rgb(35,140,212)", ("starship", "Dark"): "rgb(45,86,174)",
    ("weapon", "Light"): "rgb(93,196,102)", ("weapon", "Dark"): "rgb(14,131,54)",    # weapons and devices
    ("effect", "Light"): "rgb(201,52,93)", ("effect", "Dark"): "rgb(161,35,36)",
}

# per kind: band (x0, x1, y0, y1); legs height (left, right); text box (x0, x1, y0, y1); notch (x from, top) for the
# character panel; slip top (where the cut-out starts)
GEOM = {
    # means over the sheet's slips (each was placed by hand: boxes vary +-0.7 pt)
    "character": {"band": (8.43, 170.10, 8.60, 63.84), "notch": (152.52, 32.85), "legs": (63.84, 32.85),
                  "box": (26.32, 150.82, 17.25, 61.78), "box_dark": (26.83, 151.34, 18.31, 62.84), "top": 63.84},
    "starship": {"band": (25.20, 170.10, 7.76, 19.81), "legs": (19.85, 19.85),
                 "box": (25.50, 150.00, 9.72, 51.33), "top": 51.33, "text_base": 7.18},
    "band": {"band": (8.51, 170.29, 7.76, 19.79), "legs": (19.85, 19.85),
             "box": (26.05, 150.55, 16.59, 61.12), "top": 61.12},
}
TEXT_PT, PITCH_PT = 8.0, 8.0          # Akzidenz-Grotesk BE Condensed 8 / 8
TEXT_DX, TEXT_BASE = 2.04, 8.18       # first baseline below the box top; text left inset
BOX_RULE = 0.5
STAT_X0, STAT_X1 = 15.90, 21.57       # deploy (white) above forfeit (black), Haettenschweiler 9 pt
DEPLOY_Y, FORFEIT_Y = (51.96, 61.88), (39.00, 48.92)
STAT_BASE = (53.71, 40.67)
MARK_X, MARK_BASE, MARK_PT = 151.50, 2.15, 7.0   # Wingdings negative circled digit + "•" + number (Bold Italic), white


def kind_for(template: str, slip_type: str = "") -> tuple[str, str]:
    """(geometry kind, colour kind) from the render template / slip type."""
    s = f"{template} {slip_type}".lower()
    if "weapon" in s or "device" in s:   # before "character": Character Weapon (Han's Heavy Blaster Pistol)
        return "band", "weapon"
    if "character" in s:
        return "character", "character"
    if "starship" in s or "starfighter" in s:
        return "starship", "starship"
    return "band", "effect"


def resolve(spec: dict, card: dict) -> dict:
    """spec["early_slip"] (dict or true) + the spec -> the dict the renderer draws."""
    es = spec.get("early_slip")
    es = dict(es) if isinstance(es, dict) else {}
    g, ck = kind_for(card.get("template", ""), spec.get("slip_type") or "")
    g = es.get("kind") if es.get("kind") in GEOM else g
    if es.get("kind") in ("character", "starship"):
        ck = es["kind"]
    side = "Dark" if (spec.get("side") or card.get("side")) == "Dark" else "Light"
    colour = es.get("colour") or COLOURS[(es.get("colour_kind") or ck, side)]
    if not re.fullmatch(r"#[0-9a-fA-F]{3,8}|rgb\(\d{1,3},\d{1,3},\d{1,3}\)", str(colour)):
        colour = COLOURS[(ck, side)]
    text = es.get("text") if es.get("text") is not None else (spec.get("game_text") or "")
    return {
        "kind": g, "colour": colour, "side": side,
        "text": str(text).replace("\r\n", "\n").replace("¶", "\n")[:1200],
        "deploy": str(es.get("deploy", spec.get("deploy") or ""))[:3],
        "forfeit": str(es.get("forfeit", spec.get("forfeit") or ""))[:3],
        "set": str(es.get("set") or spec.get("virtual_set") or "1")[:2],
        "number": str(es.get("number") or spec.get("early_slip_number") or "")[:4],
        "paper": bool(es.get("paper")),
        "lines": es.get("lines") if isinstance(es.get("lines"), list) else None,   # printed line breaks, optional
    }


def html(es: dict, x0: float, bottom: float, sx: float, sy: float, esc, fonts: dict) -> str:
    """The slip as absolutely placed HTML on the card: x0 / bottom = card area's left / bottom edge in px."""
    G = GEOM[es["kind"]]
    X = lambda p: x0 + p * sx            # noqa: E731
    Y = lambda p: bottom - p * sy        # noqa: E731

    def rect(xa, xb, ya, yb, style):
        return (f'<div style="position:absolute;left:{X(xa):.1f}px;top:{Y(yb):.1f}px;width:{(xb - xa) * sx:.1f}px;'
                f'height:{(yb - ya) * sy:.1f}px;{style}"></div>')
    o = []
    top = G["top"]
    rx, ry = CORNER[0] * sx, CORNER[1] * sy
    # cut to its outline (the notch leaves the icons showing; starships / weapons keep the card's own deploy / forfeit
    # beside the short legs), unless `paper` asks for the whole printed rectangle with its white paper
    if es.get("paper"):
        o.append(f'<div style="position:absolute;left:{x0:.1f}px;top:{Y(top):.1f}px;width:{SLIP_W * sx:.1f}px;height:{top * sy:.1f}px;'
             f'background:#fff;border-radius:0 0 {rx:.1f}px {rx:.1f}px / 0 0 {ry:.1f}px {ry:.1f}px"></div>')
    bx0, bx1, by0, by1 = G["band"]
    if es["kind"] == "character":   # grey panel, notched on the right (the icon column stays visible above it)
        nx, ny = G["notch"]
        o.append(rect(bx0, nx, by0, by1, f"background:{es['colour']}"))
        o.append(rect(nx - 0.05, bx1, by0, ny, f"background:{es['colour']}"))
    else:
        o.append(rect(bx0, bx1, by0, by1, f"background:{es['colour']}"))
    # black U: bottom bar + legs
    o.append(f'<div style="position:absolute;left:{x0:.1f}px;top:{Y(BAR):.1f}px;width:{SLIP_W * sx:.1f}px;height:{BAR * sy:.1f}px;'
             f'background:{BLACK};border-radius:0 0 {rx:.1f}px {rx:.1f}px / 0 0 {ry:.1f}px {ry:.1f}px"></div>')
    o.append(rect(0, LEG, BAR - 0.5, G["legs"][0], f"background:{BLACK}"))
    o.append(rect(RIGHT_LEG_X, SLIP_W, BAR - 0.5, G["legs"][1], f"background:{BLACK}"))
    # text box
    tx0, tx1, ty0, ty1 = G["box_dark"] if es["side"] == "Dark" and "box_dark" in G else G["box"]
    rule = max(1.0, BOX_RULE * sx)
    o.append(rect(tx0, tx1, ty0, ty1, f"background:#fff;box-sizing:border-box;border:{rule:.1f}px solid {BLACK}"))
    fs, lh = TEXT_PT * sx, PITCH_PT * sy
    asc, desc = 0.908, 0.250   # HolotableTextPC hhea
    first_top = Y(ty1 - G.get("text_base", TEXT_BASE)) - ((lh - (asc + desc) * fs) / 2 + asc * fs)
    if es.get("lines"):
        body = "<br>".join(esc(str(s)) for s in es["lines"][:12])
        ws = "nowrap"
    else:
        body = "<br>".join(esc(p) for p in es["text"].split("\n"))
        ws = "normal"
    o.append(f'<div class="eslip-text" style="position:absolute;left:{X(tx0 + TEXT_DX):.1f}px;top:{first_top:.1f}px;'
             f'width:{(tx1 - tx0 - TEXT_DX - 1.2) * sx:.1f}px;font-family:{fonts["text"]};font-size:{fs:.2f}px;line-height:{lh:.2f}px;'
             f'color:{BLACK};white-space:{ws};text-align:left;letter-spacing:0">{body}</div>')
    if es["kind"] == "character":
        for (ya, yb), base, val, white in ((DEPLOY_Y, STAT_BASE[0], es["deploy"], True), (FORFEIT_Y, STAT_BASE[1], es["forfeit"], False)):
            o.append(rect(STAT_X0, STAT_X1, ya, yb, f"background:{'#fff' if white else BLACK};box-sizing:border-box;"
                                                     f"border:{max(1.0, 0.25 * sx):.1f}px solid {BLACK if white else '#fff'}"))
            if val:
                # Haettenschweiler 9 pt: digits 7.2 pt tall; drawn in the condensed bold text face, fitted to that height
                h = 6.3 * sy   # measured digit height on the sheet (Luke, BoShek)
                o.append(f'<div style="position:absolute;left:{X(STAT_X0):.1f}px;top:{Y(base + 0.5) - h:.1f}px;width:{(STAT_X1 - STAT_X0) * sx:.1f}px;'
                         f'height:{h:.1f}px;display:flex;justify-content:center;align-items:flex-end;overflow:visible">'
                         f'<span style="font-family:{fonts["stat"]};font-size:{h / 0.706:.1f}px;line-height:{h:.1f}px;height:{h:.1f}px;'
                         f'display:inline-block;transform:scaleX(1.04);-webkit-text-stroke:1.5px currentColor;color:{BLACK if white else "#fff"}">{esc(val)}</span></div>')
    # set mark in the bottom bar: (n)•number, white
    d = MARK_PT * sy * 0.709   # the Wingdings disc (4.96 pt)
    by = Y(MARK_BASE)
    num = esc(es["number"])
    o.append(f'<div style="position:absolute;left:{X(MARK_X + 0.64):.1f}px;top:{by - d - 5:.1f}px;width:{d:.1f}px;height:{d:.1f}px;border-radius:50%;'
             f'background:#fff;color:{BLACK};font-family:{fonts["stat"]};font-size:{d * 0.95:.1f}px;line-height:{d:.1f}px;text-align:center">'
             f'{esc(es["set"])}</div>')
    o.append(f'<div style="position:absolute;left:{X(MARK_X + 6.8):.1f}px;top:{by - MARK_PT * sy * 0.9 + 3:.1f}px;height:{MARK_PT * sy:.1f}px;'
             f'font-family:{fonts["mark"]};font-size:{MARK_PT * sx * 0.99:.1f}px;line-height:{MARK_PT * sy:.1f}px;color:#fff;white-space:nowrap">'
             f'•{num}</div>')
    return "".join(o)
