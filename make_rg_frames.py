"""Reflections Gold "wide vision" frames (Decipher's cancelled set: Effects / Interrupts printed landscape, full art,
gold credit coins) from Bardez's [Horizontal] XCFs (wiki.swccg.com/preserved/bardez/). 2220x1632 canvases.

    python3 make_rg_frames.py
"""
from pathlib import Path
from PIL import Image
from gimpformats.gimpXcfDocument import GimpDocument

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
