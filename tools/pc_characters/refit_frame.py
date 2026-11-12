#!/usr/bin/env python3
"""Refit a character frame plate to the PC (swccg-guild/work#52).

    python3 tools/pc_characters/refit_frame.py FRAME.png FX FY SX SY TX TY  -> rewrites FRAME.png, prints new (x, y)

SX/SY and TX/TY are the frame-only similarity fit of a CardMaker build onto the PC hires image (745 px space, scale
about the card centre (372.5, 519.5), shift in 745 px), from tools/pc_characters/frame_ecc.py. The plate is resampled
(premultiplied alpha, Lanczos) so that it lands at an integer master position with the sub-pixel rest baked in.
"""
import sys, numpy as np, cv2
from PIL import Image
f, fx, fy, sx, sy, tx, ty = sys.argv[1], *map(float, sys.argv[2:])
im = np.asarray(Image.open(f).convert("RGBA")).astype(np.float32)
h, w = im.shape[:2]
CX, CY = 815.0, 1111.0          # master coordinates of the 745 px card centre
nx = sx * (fx - CX) + CX + 2 * tx; ny = sy * (fy - CY) + CY + 2 * ty
ix, iy = int(np.floor(nx)), int(np.floor(ny))
nw, nh = int(np.ceil(nx + sx * w)) - ix, int(np.ceil(ny + sy * h)) - iy
M = np.float32([[sx, 0, nx - ix], [0, sy, ny - iy]])
a = im[..., 3:4] / 255.0
pm = np.concatenate([im[..., :3] * a, im[..., 3:4]], 2)
out = cv2.warpAffine(pm, M, (nw, nh), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
out = np.clip(out, 0, 255); A = out[..., 3:4]
rgb = np.where(A > 0, out[..., :3] / np.maximum(A / 255.0, 1e-6), 0)
Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), A], 2).round().astype(np.uint8), "RGBA").save(f)
print(f"{f}: {w}x{h} at ({fx:g},{fy:g}) -> {nw}x{nh} at ({ix},{iy})")
