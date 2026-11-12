"""Rev 78: the Episode I disc as printed (Theed Palace / Coruscant / Tatooine / Reflections III Objectives, Epic Events,
characters and effects under the sphere; the PC's Virtual cards): a black disc, a tall serif "I" (0.80 of the disc, stem
0.09, serifs 0.29 wide) over bright white bold condensed "EPISODE" (cap height 0.14, 0.88 wide, centred at 0.48),
the stem cutting through the S with a thin black gap. Measured on the 745 px PC scans (Hunt For The Droid General,
Communing, How Liberty Dies, More Systems Will Rally, I Did It!). Writes assets/icons/ep1-disc.png (232 px)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
S = 4; D = 232 * S
im = Image.new("RGBA", (D, D), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.ellipse((0, 0, D - 1, D - 1), fill=(0, 0, 0, 255))
WHITE = (246, 246, 244, 255)
# EPISODE: bold sans set tight, stretched to 0.88 D wide at cap height 0.14 D (the printed letters are wide and heavy)
font = ImageFont.truetype(str(ROOT / "assets/fonts/HolotableText/HolotableText-Bold.ttf"), 400)
txt = "EPISODE"
L = Image.new("L", (4000, 600), 0); ImageDraw.Draw(L).text((50, 50), txt, font=font, fill=255, stroke_width=5, stroke_fill=255)
L = L.crop(L.getbbox())
cy = 0.48 * D; ch = 0.14 * D; tw = 0.88 * D
L = L.resize((int(tw), int(ch)), Image.LANCZOS)
im.paste(Image.new("RGBA", L.size, WHITE), (int((D - tw) / 2), int(cy - ch / 2)), L)
# the serif I over it, with a thin black gap round the stem
cx = D / 2; h = 0.80 * D; y0 = (D - h) / 2; y1 = y0 + h
sw = 0.09 * D; fw = 0.29 * D; ft = 0.05 * D; br = 0.07 * D   # stem, serif width, serif thickness, bracket
gap = 0.014 * D
d.rectangle((cx - sw / 2 - gap, cy - 0.10 * D, cx + sw / 2 + gap, cy + 0.10 * D), fill=(0, 0, 0, 255))
d.rectangle((cx - sw / 2, y0, cx + sw / 2, y1), fill=WHITE)
for ys, sgn in ((y0, 1), (y1, -1)):
    d.rectangle((cx - fw / 2, min(ys, ys + sgn * ft), cx + fw / 2, max(ys, ys + sgn * ft)), fill=WHITE)
    # bracketed serifs: fill the corner, carve with a black circle
    for sx in (-1, 1):
        x0 = cx + sx * sw / 2; ye = ys + sgn * ft
        d.rectangle((min(x0, x0 + sx * br), min(ye, ye + sgn * br), max(x0, x0 + sx * br), max(ye, ye + sgn * br)), fill=WHITE)
        ccx, ccy = x0 + sx * br, ye + sgn * br
        d.ellipse((ccx - br, ccy - br, ccx + br, ccy + br), fill=(0, 0, 0, 255))
out = im.resize((232, 232), Image.LANCZOS)
out.save(ROOT / "assets/icons/ep1-disc.png")
print("wrote", ROOT / "assets/icons/ep1-disc.png")
