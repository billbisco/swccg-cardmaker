"""Japanese printings (Takara 1997-98: Premiere, A New Hope, Hoth, the Japanese two-player games and the Japanese foils
in Reflections II / III) as a language layer over Decipher's templates (STANDARD rev 77, swccg-guild/work story
"Japanese card templates").

Spec `language: "ja"` (card `lang`). Same frame, art window, destiny, deploy / forfeit and icon column as the English
printing; what Takara changed is drawn here:

- title in a heavy gothic (Noto Sans JP Black for Morisawa-style 太ゴシック), uniqueness "＊" instead of "•";
- lore box taller (up 25 px, down 24 px at the master) with four lines of gothic set justified, the first line pulled in
  clear of the chamfered corners (centred, as Takara set it);
- one long black stat strip ("戦闘力６　能力値６　ダーク・ジェダイ") instead of Decipher's three boxes;
- game text in a medium gothic, justified, Japanese line breaking (no 。、」 at a line start);
- card-type banner in katakana / kanji without the English letter-spacing; copyright line in a light face.

Measured on Darth Vader (Japanese) (wiki File:Japanese-Premiere-Darth-Vader-Encyclopedia32-original.jpg) warped into the
1632x2220 master by its frame edges. Further types: JA_GEOM per template (measure, then add).

Language is a parameter: another language plugs in as its own module with the same three entry points (template, css,
stats_html / lore_html) and a `language` value; the English printing stays the default.
"""
from __future__ import annotations
import re

LANG = "ja"
FONT = '"Noto Sans JP"'   # assets/fonts/NotoSansJP (SIL OFL); installed into the container's fontconfig (webapp/Dockerfile)

# Labels as Takara printed them (read off the Japanese cards on wiki.swccg.com). Anything else is printed as typed, so a
# Japanese label can simply be typed in the editor.
LABELS = {
    "POWER": "戦闘力", "ABILITY": "能力値", "MANEUVER": "回避値", "HYPERSPEED": "航行速度", "ARMOR": "装甲値",
    "LANDSPEED": "移動速度", "FORCE-SENSITIVE": "フォース感知者", "DARK JEDI": "ダーク・ジェダイ",
    "NO HYPERDRIVE": "ハイパードライブ未装備", "FEROCITY": "凶暴性", "SLITHER": "粘膜",
}
CARD_TYPES = {
    "EFFECT": "エフェクト", "LOST INTERRUPT": "ロスト・インタラプト", "USED INTERRUPT": "ユーズド・インタラプト",
    "DEVICE": "アイテム", "AUTOMATED WEAPON": "自動化兵器", "SWAMP CREATURE": "沼沢地生物",
    "TRANSPORT VEHICLE": "運搬用ビークル", "STARFIGHTER: TIE/LN": "宇宙戦闘機：ＴＩＥ／ＬＮ",
    "STARFIGHTER: MODIFIED LIGHT FREIGHTER": "宇宙戦闘機：改造小型貨物船", "COMBAT VEHICLE: AT-AT": "戦闘用ビークル：ＡＴ－ＡＴ",
}
# Takara's copyright line (1997 for Premiere / A New Hope, 1998 for Hoth; the Reflections II foils say 2000)
COPYRIGHT = {"Premiere": 1997, "A New Hope": 1997, "Hoth": 1998}

# Per-template geometry at the master (1632x2220). Measured: ds-character-imperial (Darth Vader). Other templates use
# the same offsets from their own boxes until measured (DEFAULT).
DEFAULT = {
    "lore_box": (-37, -25, 31, 27),   # black box: (left, top, right, bottom) offsets from the English lore text box
    "lore_chamfer": 55,
    "lore_text": (-18, -31, 25, 28),   # text area offsets from the English lore text box (left, top, right, bottom)
    "lore_cut": 130,                  # first line pulled in on both sides (clear of the chamfers)
    "lore_size": 46.6, "lore_lh": 58,   # Vader: 22 characters a line (16 on the first; Takara broke line 2 at 21)
    "strip": (-29, -6, 42, 66),       # stat strip: (left of first well, top from stats_y, right of last well, bottom)
    "strip_items": (-5, -15),         # item x = well x + a + b * i (Vader: 300, 598, 889)
    "strip_items2": (-5, 90),         # two stats: the second sits mid-strip (Admiral Ozzel 703, Nalan Cheel ~690)
    "strip_size": 58,
    "title_left": 395, "title_dy": -27, "title_size": 67, "title_sx": 0.91,   # Takara's titles are condensed (長体)
    "gt": (-19, -6, 20, 11),          # game text offsets from the English box as rendered (left, top, width, height)
    "gt_size": 47.6, "gt_lh": 57.5,
}
JA_GEOM: dict[str, dict] = {
    "ds-character-imperial": {"gt_abs": (335, 1656, 962, 362)},
    "ls-character-rebel": {"strip": (-34, -6, 8, 66)},   # Luke Skywalker (Japanese)   # Darth Vader (Japanese): 20 characters of 47.6 px a line
}


def geom(template: str) -> dict:
    return dict(DEFAULT, **JA_GEOM.get(template, {}))


def title(s: str) -> str:
    """•Darth Vader -> ＊ダース・ベイダー: Takara printed the uniqueness dots as asterisks (•••Blizzard Walker -> ＊＊＊)."""
    return re.sub(r"^[•●]+", lambda m: "＊" * len(m.group(0)), s or "")


def label(s: str) -> str:
    return LABELS.get((s or "").strip().upper(), s or "")


def wide_digits(s: str) -> str:
    """Stat values print in full-width figures (戦闘力６)."""
    return s.translate({ord(c): 0xFF10 + i for i, c in enumerate("0123456789")})


def card_type(s: str) -> str:
    return CARD_TYPES.get((s or "").strip().upper(), s or "")


def copyright_for(expansion: str | None) -> str | None:
    y = COPYRIGHT.get(expansion or "")
    return f"TM & © {y} LUCASFILM LTD.  TM, ® & © {y} DECIPHER INC." if y else None


def template(card: dict, t: dict) -> dict:
    """The English template with the boxes Takara moved."""
    g = geom(card["template"])
    t = dict(t)
    if "game_text" in t:
        x, y, w, h = t["game_text"]; a, b, c, d = g["gt"]
        t["game_text"] = tuple(g["gt_abs"]) if g.get("gt_abs") else (x + a, y + b, w + c, h + d)
    if "title" in t and not t.get("landscape"):
        x, y, w, h = t["title"]
        left = max(x, g["title_left"]) if "character" in card["template"] else x
        t["title"] = (left, y + g["title_dy"], w + (x - left), h)
    return t


def lines_html(lines: list, text_html) -> str:
    """The printed lines, each justified to the box and never re-wrapped: a line-end 。 or 、 that Takara let hang past
    the measure (ぶら下げ) hangs here too."""
    return "".join(f'<span class="jal{" jalast" if i == len(lines) - 1 else ""}">{text_html(l)}</span>' for i, l in enumerate(lines))


def gt_html(card: dict, t: dict, text_html, fit_attrs: str = "") -> str:
    x, y, w, h = t["game_text"]
    lines = printed_lines(card.get("game_text"), card.get("text_breaks"))
    if lines:   # printed breaks: no fitting (a hanging 。 is meant to cross the measure)
        return f'<div class="gt jagt" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{lines_html(lines, text_html)}</div>'
    return f'<div class="gt jagt fit"{fit_attrs} style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{text_html(card["game_text"])}</div>'


def frame_color(t: dict, x: int, y: int, lighten: float = 0.0) -> str:
    """Median colour of the template's frame around (x, y) (master px)."""
    from PIL import Image
    import numpy as np
    from pathlib import Path
    fr, fx, fy = t["frame"]
    p = Path(__file__).resolve().parent / "assets" / fr
    a = np.array(Image.open(p).convert("RGB")).astype(float)[y - fy - 6:y - fy + 7, x - fx - 6:x - fx + 7].reshape(-1, 3)
    r, g, b = (np.median(a, axis=0) if len(a) else np.array([200, 200, 200])) * (1 - lighten) + 255 * lighten
    return f"rgb({r:.0f},{g:.0f},{b:.0f})"


def printed_lines(text: str | None, lines) -> list | None:
    """The printed card's own line breaks (spec lore_lines), used when they hold exactly the same characters."""
    if not text or not isinstance(lines, list) or len(lines) < 2:
        return None
    strip = lambda s: re.sub(r"\s+", "", s or "")
    return [l.strip() for l in lines] if strip("".join(lines)) == strip(text) else None


def frame(fr, fx: int, fy: int, card: dict, t: dict, wells) -> "Path":
    """The English frame with its stat wells' rims smoothed away where Takara's one strip replaces them (each column
    blended from the frame just above to just below the old wells). Cached next to the renders."""
    from pathlib import Path
    from PIL import Image
    import numpy as np, os, hashlib
    if not wells or "stats_y" not in t:
        return fr
    g = geom(card["template"])
    lx, ly, lw, lh = t["lore"]
    la, lb, lc, ld = g["lore_box"]
    LX0, LX1, LY0, LY1 = lx + la, lx + lw + lc, ly + 43, ly + lh + ld - 4   # the English lore box's side bevels
    y = t["stats_y"]; a, b, c, d = g["strip"]
    X0, X1 = wells[0][0] + a - 14, wells[-1][0] + wells[-1][1] + c + 14
    Y0, Y1 = y + b - 12, y + d + 22
    out = Path(os.environ.get("CARDMAKER_OUT") or Path(__file__).resolve().parent / "out")
    out.mkdir(exist_ok=True)
    key = hashlib.sha1(f"{fr}|{fx}|{fy}|{X0}|{X1}|{Y0}|{Y1}|{LX0}|{LX1}|{LY0}|{LY1}|5|{bool(t.get('dark_text'))}".encode()).hexdigest()[:12]
    dest = out / f"jaframe-{Path(fr).stem}-{key}.png"
    if dest.exists():
        return dest
    im = np.array(Image.open(fr).convert("RGBA")).astype(float)
    x0, x1, y0, y1 = X0 - fx, X1 - fx, Y0 - fy, Y1 - fy
    s0, s1 = y + b - fy, y + d - fy   # the strip itself covers these rows; mirror the frame into the bands above / below it
    for i in range(s0 - y0):
        im[s0 - 1 - i, x0:x1] = im[y0 - 1 - i, x0:x1] if i < y0 else im[s0 - 1 - i, x0:x1]
    for i in range(y1 - s1):
        im[s1 + i, x0:x1] = im[y1 + (y1 - s1) - 1 - i, x0:x1]
    for yy in (range(LY0 - fy, LY1 - fy) if not t.get("dark_text") else ()):   # lore box sides (Dark frames; Light frames are mottled)
        lft = im[yy, LX0 - 46 - fx:LX0 - 40 - fx].mean(0) * [.9, .9, .9, 1]; rgt = im[yy, LX1 + 30 - fx:LX1 + 36 - fx].mean(0) * [.9, .9, .9, 1]   # the box's shadow on the frame
        im[yy, LX0 - 40 - fx:LX0 + 4 - fx] = lft
        im[yy, LX1 - 4 - fx:LX1 + 30 - fx] = rgt
    Image.fromarray(im.clip(0, 255).astype("uint8"), "RGBA").save(dest)
    return dest


def lore_html(card: dict, t: dict, text_html, fit_attrs: str = "") -> str:
    g = geom(card["template"])
    lx, ly, lw, lh = t["lore"]
    a, b, c, d = g["lore_box"]
    L, T, R, B = lx + a, ly + b, lx + lw + c, ly + lh + d
    k = g["lore_chamfer"]
    pts = f"{L + k},{T} {R - k},{T} {R},{T + k} {R},{B} {L},{B} {L},{T + k}"
    fill, stroke = "#000", "#4d5a5e"
    if t.get("dark_text"):   # Light frames: the lore box is the frame's own light grey with a dark bevel
        fill, stroke = frame_color(t, lx + lw // 2, ly + lh // 2, lighten=0.2), "#6e6e74"
    svg = (f'<svg style="position:absolute;left:0;top:0" width="1632" height="2220">'
           f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="3" stroke-linejoin="miter"/></svg>')
    a, b, c, d = g["lore_text"]
    x0, y0, x1, y1 = lx + a, ly + b, lx + lw + c, ly + lh + d
    cut = g["lore_cut"]
    lines = printed_lines(card.get("lore"), card.get("lore_lines"))
    body = lines_html(lines, text_html) if lines else text_html(card["lore"])
    return (svg + f'<div class="lore jalore fit"{fit_attrs} style="position:absolute;left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px">'
            f'<span class="jacut" style="float:left;width:{cut}px;height:{g["lore_lh"] - 2}px"></span>'
            f'<span class="jacut" style="float:right;width:{cut}px;height:{g["lore_lh"] - 2}px"></span>{body}</div>')


def stats_html(card: dict, t: dict, wells: list, esc) -> str:
    """One black strip over Decipher's wells; each stat set where its English box started (label + value run together)."""
    g = geom(card["template"])
    y = t["stats_y"]
    a, b, c, d = g["strip"]
    x0 = wells[0][0] + a; x1 = wells[-1][0] + wells[-1][1] + c
    fill = "#050505"
    if t.get("dark_text"):   # Light frames: Takara's strip is the frame's own light well colour, text black
        fill = frame_color(t, wells[0][0] + 30, y + 34, lighten=0.5)
    out = [f'<div class="jastrip{" light" if t.get("dark_text") else ""}" style="position:absolute;left:{x0}px;top:{y + b}px;width:{x1 - x0}px;height:{d - b}px;background:{fill}"></div>']
    stats = [s_ for s_ in (card.get("stats") or []) if (s_[0] or "").strip() or str(s_[1] or "").strip()]
    ia, ib = g["strip_items2"] if len(stats) == 2 else g["strip_items"]
    for i, (lab, val) in enumerate(stats[:len(wells)]):
        x = wells[i][0] + ia + ib * i
        right = x1 - 8 if i == len(stats) - 1 else wells[i + 1][0] + ia + ib * (i + 1) - 10
        out.append(f'<div class="jastat" style="position:absolute;left:{x}px;top:{y + b}px;height:{d - b}px;max-width:{right - x}px">'
                   f'<span class="fitlab" data-avail="{right - x}" style="display:inline-block;white-space:nowrap;transform-origin:left center">{esc(label(lab))}{esc(wide_digits(str(val or "")))}</span></div>')
    return "".join(out)


def css(card: dict, t: dict) -> str:
    g = geom(card["template"])
    ink = "#dcdcdc" if not t.get("dark_text") else "#111"
    return f"""
    .title{{font-family:{FONT}!important;font-weight:800;font-size:{g["title_size"]}px;letter-spacing:0!important;-webkit-text-stroke:0!important;color:{"#dedede" if not t.get("dark_text") else "#1a1a1a"}!important;}}
    .title:not(.ltitle):not(.dtitle){{transform:scaleX({g["title_sx"]});transform-origin:left center}}
    .title .dot{{font-family:{FONT}}}
    .lore.jalore{{font-family:{FONT}!important;font-weight:500;font-size:{g["lore_size"]}px;line-height:{g["lore_lh"]}px;letter-spacing:0!important;color:{ink};text-indent:0!important;padding:0;
      text-align:justify;text-align-last:left;line-break:strict;word-break:normal;overflow-wrap:anywhere}}
    .gt{{font-family:{FONT}!important;font-weight:500;font-size:{g["gt_size"]}px;line-height:{g["gt_lh"]}px;letter-spacing:0!important;color:{ink};padding:0!important;
      text-align:justify;text-align-last:left;line-break:strict;word-break:normal;overflow-wrap:anywhere}}
    .jal{{display:block;white-space:nowrap;text-align:justify;text-align-last:justify}}
    .jal.jalast{{text-align-last:left}}
    .gt b, .lore b{{font-family:{FONT};font-weight:800}}
    .gt u, .lore u{{text-underline-offset:6px;text-decoration-thickness:3px}}
    .jastrip{{box-shadow:inset 0 0 0 2px #151515, 2px 3px 0 0 #8c979a, -1px -1px 0 0 #2a3134}}
    .jastrip.light{{box-shadow:inset 3px 3px 0 0 #5c5c62, 2px 3px 0 0 #f4f4f6}}
    .jastat{{display:flex;align-items:center;font-family:{FONT};font-weight:800;font-size:{g["strip_size"]}px;color:{"#e8e8e8" if not t.get("dark_text") else "#1c1c1c"};padding-bottom:2px;box-sizing:border-box}}
    .ctype{{font-family:{FONT}!important;font-weight:800;letter-spacing:0!important}}
    .copyin{{font-family:AGCn!important;font-weight:normal;color:{"#c4c4c4" if not t.get("dark_text") else "#333"}!important;letter-spacing:0.6px!important}}
    """
