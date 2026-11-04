#!/usr/bin/env python3
"""Draw the Personal Force icon disc (assets/icons/disc-personal-force.png, 160x160) for swccg-guild/work#62.

The Players Committee prints this disc in the right margin of five Light Effects (Commando Training (V), The Greatest Of
All The Jedi, Seeking An Audience (V), Wokling (V), Twilight Is Upon Me (V)): a green lightsaber blade with a white core
across a black disc, rising to the right at about 67 degrees. No Game Aid or vector copy of it exists, so it is drawn here
from measurements of the PC's 745 px card images (blade angle and widths as fractions of the disc). Our own drawing."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

N, SS = 160, 4                      # output size, supersampling
W = N * SS; c = W / 2; r = W / 2 - SS
ang = math.radians(67)              # blade angle from the horizontal, rising to the right
dx, dy = math.cos(ang) * r * 1.2, -math.sin(ang) * r * 1.2


def blade(width, fill, blur):
    im = Image.new("L", (W, W), 0)
    ImageDraw.Draw(im).line([(c - dx, c - dy), (c + dx, c + dy)], fill=255, width=int(width * W))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(blur * W)) if blur else im).astype(np.float32)[..., None] / 255, np.array(fill, np.float32)


rgb = np.zeros((W, W, 3), np.float32); rgb[:] = (4, 14, 6)          # the disc: black with a faint green cast
for width, fill, blur in ((0.40, (0, 60, 8), 0.03), (0.30, (20, 215, 35), 0.008), (0.20, (150, 255, 150), 0.004), (0.15, (255, 255, 255), 0.003)):
    a, col = blade(width, fill, blur)
    rgb = rgb * (1 - a) + col * a
disc = Image.new("L", (W, W), 0); ImageDraw.Draw(disc).ellipse([c - r, c - r, c + r, c + r], fill=255)
out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA"); out.putalpha(disc)
out.resize((N, N), Image.LANCZOS).save("assets/icons/disc-personal-force.png", optimize=True)
print("assets/icons/disc-personal-force.png")
