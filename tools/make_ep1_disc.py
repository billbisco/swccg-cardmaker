"""Rev 80: the Episode I disc as printed, one disc for every place it goes (under the expansion sphere, left margin of
Objectives / Epic Events, Podracers). Measured on two stacks of printed discs, each registered to a hundredth of a
pixel and median-averaged (tools/set_spheres/cut_set_spheres.py's registration): 40 PC Virtual faces at 745 px
(res.starwarsccg.org hires) and 30 Decipher Tatooine faces at 497 px (wiki decipher-archive scans); both agree:

  - black disc; a tall white serif "I": 0.79 of the disc high, centred; stem 0.085 wide; bracketed slab serifs 0.26
    wide, 0.045 thick
  - "EPISODE" behind it in a bold sans, light grey (dimmer than the I: ~200 against 255), cap height 0.125 of the disc,
    0.88 wide, centred on the disc's middle (0.495 down); the letters next to the stem are hidden by a black gap
    0.018 wide on each side of it (the stem runs through the middle of the S)

Run: python3 tools/make_ep1_disc.py  ->  assets/icons/ep1-disc.png (232 px, transparent outside the disc)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
S = 4; D = 232 * S
I_H, STEM, SERIF_W, SERIF_T, BRACKET = 0.79, 0.085, 0.26, 0.045, 0.055
CAP, EP_W, EP_CY, GAP = 0.125, 0.88, 0.495, 0.018
WHITE = (250, 250, 248, 255); GREY = (202, 202, 200, 255); BLACK = (0, 0, 0, 255)


def main():
    im = Image.new("RGBA", (D, D), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, D - 1, D - 1), fill=BLACK)
    font = ImageFont.truetype(str(ROOT / "assets/fonts/HolotableText/HolotableText-Bold.ttf"), 400)
    L = Image.new("L", (4000, 600), 0); ImageDraw.Draw(L).text((50, 50), "EPISODE", font=font, fill=255)
    L = L.crop(L.getbbox())
    tw, ch = EP_W * D, CAP * D; cy = EP_CY * D
    L = L.resize((int(tw), int(ch)), Image.LANCZOS)
    im.paste(Image.new("RGBA", L.size, GREY), (int((D - tw) / 2), int(cy - ch / 2)), L)
    cx = D / 2; h = I_H * D; y0 = (D - h) / 2; y1 = y0 + h
    sw, fw, ft, br, gap = STEM * D, SERIF_W * D, SERIF_T * D, BRACKET * D, GAP * D
    d.rectangle((cx - sw / 2 - gap, cy - ch, cx + sw / 2 + gap, cy + ch), fill=BLACK)   # the black gap round the stem
    d.rectangle((cx - sw / 2, y0, cx + sw / 2, y1), fill=WHITE)
    for ys, sgn in ((y0, 1), (y1, -1)):
        d.rectangle((cx - fw / 2, min(ys, ys + sgn * ft), cx + fw / 2, max(ys, ys + sgn * ft)), fill=WHITE)
        for sx in (-1, 1):   # bracketed serifs: fill the corner, carve it round with a black circle
            x0 = cx + sx * sw / 2; ye = ys + sgn * ft
            d.rectangle((min(x0, x0 + sx * br), min(ye, ye + sgn * br), max(x0, x0 + sx * br), max(ye, ye + sgn * br)), fill=WHITE)
            ccx, ccy = x0 + sx * br, ye + sgn * br
            d.ellipse((ccx - br, ccy - br, ccx + br, ccy + br), fill=BLACK)
    mask = Image.new("L", (D, D), 0); ImageDraw.Draw(mask).ellipse((0, 0, D - 1, D - 1), fill=255)
    im.putalpha(mask)
    out = im.resize((232, 232), Image.LANCZOS)
    out.save(ROOT / "assets/icons/ep1-disc.png")
    print("wrote", ROOT / "assets/icons/ep1-disc.png")


if __name__ == "__main__":
    main()
