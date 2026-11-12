"""Reflections Gold "wide vision" frames (Decipher's cancelled set: Effects / Interrupts printed landscape, full art,
gold credit coins) from Bardez's [Horizontal] XCFs (wiki.swccg.com/preserved/bardez/). 2220x1632 canvases.

    python3 make_rg_frames.py
"""
from pathlib import Path
from PIL import Image
try:
    from gimpformats.gimpXcfDocument import GimpDocument
except ImportError:   # only the XCF builds need it (round_ds_interrupt_disc works on the PNG)
    GimpDocument = None

ROOT = Path(__file__).resolve().parent
B = ROOT / "bardez"
OUT = ROOT / "assets/frames"


def comp(doc, idx, size=(2220, 1632)):
    c = Image.new("RGBA", size, (0, 0, 0, 0))
    for i in idx:   # bottom first
        l = doc.raw_layers[i]
        im = l.image.convert("RGBA")
        x, y = l.xOffset, l.yOffset
        if x < 0 or y < 0:
            im = im.crop((max(-x, 0), max(-y, 0), im.width, im.height)); x, y = max(x, 0), max(y, 0)
        im = im.crop((0, 0, min(im.width, size[0] - x), min(im.height, size[1] - y)))
        c.alpha_composite(im, (x, y))
    return c


SPEC = {   # frame name: (xcf, layer indices bottom→top; the black border with its window comes last)
    "rg-ls-interrupt": ("LS - Interrupt [Horizontal].xcf", [6, 27]),
    "rg-ls-effect": ("LS - Effect [Horizontal].xcf", [22, 23, 47]),
    "rg-ds-interrupt": ("DS - Interrupt [Horizontal].xcf", [16, 18, 21]),
    "rg-ds-effect": ("DS - Effect [Horizontal].xcf", [16, 20]),
}
if __name__ == "__main__" and "weapon" in __import__("sys").argv:
    pass
elif __name__ == "__main__" and "round-disc" in __import__("sys").argv:
    pass   # handled at the end of the file (round_ds_interrupt_disc is defined below)
elif __name__ == "__main__":
    for name, (f, idx) in SPEC.items():
        d = GimpDocument(str(B / f))
        comp(d, idx).save(OUT / f"{name}.png", optimize=True)
        print(name)
    d = GimpDocument(str(B / "LS - Interrupt [Horizontal].xcf"))
    d.raw_layers[3].image.convert("RGBA").save(ROOT / "assets/icons/rg-coin.png")   # one gold credit coin (57x56)


def weapon_wide():
    """Dark Side wide (landscape) weapon, as Decipher printed Maul's Double-Bladed Lightsaber (Reflections III):
    Bardez "DS - Weapon [Horizontal]" Template layer (doc 2073x1497 placed at 73,68), its lore and game-text windows
    filled black, the black card border from the Reflections Gold XCF on top."""
    from PIL import ImageDraw
    d = GimpDocument(str(B / "DS - Weapon [Horizontal].xcf"))
    fr = comp(d, [48], size=(d.width, d.height))
    a = fr.split()[3].point(lambda v: 255 if v > 0 else 0)
    for seed in ((1000, 440), (1000, 1200), (1841, 212)):   # inside the lore / game-text windows and the destiny ring
        ImageDraw.floodfill(a, seed, 128)
    black = Image.new("RGBA", fr.size, (0, 0, 0, 255))
    fr = Image.composite(black, fr, a.point(lambda v: 255 if v == 128 else 0))
    c = Image.new("RGBA", (2220, 1632), (0, 0, 0, 0))
    c.alpha_composite(fr, (73, 68))
    border = GimpDocument(str(B / "LS - Interrupt [Horizontal].xcf"))
    c.alpha_composite(comp(border, [27]))
    c.save(OUT / "ds-weapon-wide.png", optimize=True)
    print("ds-weapon-wide")


if __name__ == "__main__" and "weapon" in __import__("sys").argv:
    weapon_wide()


def starship_wide():
    """Dark Side wide (landscape) capital starship, as Decipher printed Executor (Dagobah) and Flagship Executor (Death
    Star II): Bardez "DS - Sharship [Horizontal]" Blackground + Template + Type Icon (doc 2073x1497 at 73,68), the black
    card border from the Reflections Gold XCF on top."""
    d = GimpDocument(str(B / "DS - Sharship [Horizontal].xcf"))
    fr = comp(d, [17, 15, 16], size=(d.width, d.height))
    c = Image.new("RGBA", (2220, 1632), (0, 0, 0, 0))
    c.alpha_composite(fr, (73, 68))
    border = GimpDocument(str(B / "LS - Interrupt [Horizontal].xcf"))
    c.alpha_composite(comp(border, [27]))
    c.save(OUT / "ds-starship-wide.png", optimize=True)
    print("ds-starship-wide")


if __name__ == "__main__" and "starship" in __import__("sys").argv:
    starship_wide()


def round_ds_interrupt_disc(cx=318.5, cy=288.0, r=82.0, ring=5.0):
    """Rev 84: the Dark Interrupt type disc round, as the 2001 playtest prints show it (Atmospheric Assault, Blow
    Parried: a round swirl disc with a thin dark rim in the red lobe). Bardez's DS layer clips the swirl to a chamfered
    square (227-410 x 200-375 px): the swirl inside the circle is kept, a dark rim drawn, and the square's corners
    filled with the lobe round them (OpenCV inpainting)."""
    import numpy as np, cv2
    p = OUT / "rg-ds-interrupt.png"
    a = np.asarray(Image.open(p).convert("RGBA")).copy()
    yy, xx = np.mgrid[:a.shape[0], :a.shape[1]]
    d = np.hypot(xx - cx, yy - cy)
    sq = np.zeros(a.shape[:2], np.uint8); sq[196:380, 222:415] = 1
    swirl = (a[..., 1] < 30) & (a[..., 2] < 30) & (a[..., 3] > 200)   # the disc's black / pure-red pixels
    hole = ((sq == 1) & (d > r - 1) & (swirl | (d < r + ring + 3))).astype(np.uint8) * 255
    hole = cv2.dilate(hole, np.ones((3, 3), np.uint8))
    hole[d <= r - 1] = 0
    rgb = cv2.inpaint(np.ascontiguousarray(a[..., :3]), hole, 9, cv2.INPAINT_TELEA)
    a[..., :3] = np.where(hole[..., None] > 0, rgb, a[..., :3])
    glint = (d <= r + 1) & (a[..., 1] > 60) & (a[..., 3] > 200)   # Bardez's cyan / yellow glint at the square's corner
    a[glint, :3] = 0
    rim = np.clip(ring + 0.5 - np.abs(d - (r + ring / 2)), 0, 1)[..., None]   # anti-aliased dark rim round the disc
    a[..., :3] = (a[..., :3] * (1 - rim) + np.array([38, 6, 10]) * rim).astype(np.uint8)
    Image.fromarray(a, "RGBA").save(p, optimize=True)


if __name__ == "__main__" and "weapon" not in __import__("sys").argv:
    round_ds_interrupt_disc()   # rev 84: after a full build too (python3 make_rg_frames.py [round-disc])
