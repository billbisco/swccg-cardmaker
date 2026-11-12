"""Rev 80: the Episode I disc as Decipher printed it on the Tatooine Podracers (wiki 497x692 scans, 58 master px across):
a tall heavy serif "I" (~80 % of the disc, stem ~13 %, serifs ~34 %) in front of a dimmer "EPISODE" (cap height ~19 %,
~92 % wide, centred ~53 % down), the letters next to the I hidden behind its black edge. The VS14 disc (icons/ep1-disc.png, 67 px,
from the PC's Episode I icon) sets a short I (60 %) over large letters. Drawn at 4x and reduced.
Run: python3 tools/make_ep1_disc_decipher.py -> assets/icons/ep1-disc-decipher.png"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"   # its Latin is Noto Serif (a Times-like old style)
FONT_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
N = 480; OUT = 120


def text_layer(txt, size, cap_h, width, cy, fill, font=FONT):
    f = ImageFont.truetype(font, size, index=0)
    bb = f.getbbox(txt)
    im = Image.new("L", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), 0)
    ImageDraw.Draw(im).text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=255)
    im = im.resize((int(width), int(cap_h)), Image.LANCZOS)
    lay = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    col = Image.new("RGBA", im.size, fill); col.putalpha(im)
    lay.alpha_composite(col, (int((N - im.width) / 2), int(cy - im.height / 2)))
    return lay, im


def main():
    disc = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, N - 1, N - 1), fill=(0, 0, 0, 255))
    ep, _ = text_layer("EPISODE", 400, 0.19 * N, 0.92 * N, 0.53 * N, (205, 205, 205, 255), FONT_B)
    i_lay, i_m = text_layer("I", 900, 0.80 * N, 0.33 * N, 0.50 * N, (255, 255, 255, 255), FONT_B)
    # the I's black edge hides the letters next to it
    halo = Image.new("L", (N, N), 0); halo.paste(i_m, (int((N - i_m.width) / 2), int(0.50 * N - i_m.height / 2)))
    halo = halo.filter(ImageFilter.MaxFilter(13))
    blk = Image.new("RGBA", (N, N), (0, 0, 0, 255)); blk.putalpha(halo)
    disc.alpha_composite(ep); disc.alpha_composite(blk); disc.alpha_composite(i_lay)
    mask = Image.new("L", (N, N), 0); ImageDraw.Draw(mask).ellipse((0, 0, N - 1, N - 1), fill=255)
    disc.putalpha(Image.composite(disc.getchannel("A"), Image.new("L", (N, N), 0), mask))
    out = disc.resize((OUT, OUT), Image.LANCZOS)
    p = ROOT / "assets/icons/ep1-disc-decipher.png"; out.save(p, optimize=True); print("wrote", p)


if __name__ == "__main__":
    main()
