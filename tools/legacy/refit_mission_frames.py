#!/usr/bin/env python3
"""Refit the Virtual Block Mission / Critical Mission frames to the PC's printed layout (STANDARD rev 73).

  python3 tools/legacy/refit_mission_frames.py      # rewrites assets/frames/{ls,ds}-mission.png

Reads the rev 72 frames from git (commit 240b511, so the script can be run again and gives the same result) and moves
their rows to where the PC images print them, measured on the 745 px PC gifs (master px = 2 * (745 px + 35/36)):

  Light (Hunt Down The Dark Acolyte, Assault On Muunilinst, Rescue On Geonosis, Kessel Run (V)):
      panel edge 1074, banner 1124-1218 (was 1155-1267), text box from 1240 (was 1309)
  Dark (In The Hands Of The ISB, Galactic Domination, Spice Mine Operations, Defense Of Muunilinst):
      panel 1054, banner 1084-1190 (was 1155-1267), text box from 1252 (was 1322)

The text box grows by the rows the banner gave up (mirrored tiles of its own texture, as make_mission_frames.py
stretches it). The banner is the PC's cream (Light 210,200,186) / pale tan (Dark 204,182,149) instead of silver, and
the tan of the panel is darkened to the PC's (side margins: Light 189,151,112, Dark 164,129,88).
"""
import io, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
BASE = "240b511"

# (source rows in the rev 72 frame) -> (target rows), per side; the last entry is the text box top
LAYOUT = {
    "ls": {"src": [1093, 1112, 1155, 1267, 1309], "dst": [1074, 1093, 1124, 1218, 1240],
           "banner": (210, 200, 186), "texture": 0.6, "tan": (189 / 210, 151 / 177, 112 / 139)},
    "ds": {"src": [1093, 1155, 1267, 1322], "dst": [1054, 1084, 1190, 1252],
           "banner": (204, 182, 149), "texture": 0.3, "tan": (164 / 204, 129 / 170, 88 / 130),
           # the black text box runs to x 660 (745 px) on the PC cards, ours to 645: move its right edge 30 px out
           "widen": (1196, 2074, 1340, 1430, 1485, 30)},
}


def rows(a, h):
    """Resize a block of rows to h rows (vertical only)."""
    if a.shape[0] == h:
        return a
    return np.array(Image.fromarray(a).resize((a.shape[1], h), Image.LANCZOS))


def refit(side):
    L = LAYOUT[side]
    G = np.array(Image.open(io.BytesIO(subprocess.run(["git", "-C", str(ROOT), "show", f"{BASE}:assets/frames/{side}-mission.png"],
                                                      capture_output=True, check=True).stdout)).convert("RGBA"))
    src, dst = L["src"], L["dst"]
    out = np.zeros_like(G)
    out[:dst[0]] = G[:dst[0]]
    for i in range(len(src) - 1):
        out[dst[i]:dst[i + 1]] = rows(G[src[i]:src[i + 1]], dst[i + 1] - dst[i])
    # text box: its top edge as printed, then the rows it gains (mirrored tiles of its texture), then the rest unchanged
    t0, s0 = dst[-1], src[-1]
    gain = s0 - t0
    edge = 40
    out[t0:t0 + edge] = G[s0:s0 + edge]
    band = G[s0 + edge:s0 + edge + 70]
    tiles, n = [], 0
    while n < gain:
        tiles.append(band if len(tiles) % 2 == 0 else band[::-1]); n += len(band)
    out[t0 + edge:t0 + edge + gain] = np.concatenate(tiles)[:gain]
    out[s0 + edge:] = G[s0 + edge:]
    if L.get("widen"):
        y0_, y1_, xa, xb, xe, dx = L["widen"]
        blk = out[y0_:y1_].copy()
        out[y0_:y1_, xa + dx:xb + dx] = blk[:, xa:xb]
        out[y0_:y1_, xb + dx:xe] = np.array(Image.fromarray(blk[:, xb:xe]).resize((xe - xb - dx, y1_ - y0_), Image.LANCZOS))
        out[y0_:y1_, xa:xa + dx] = np.where((blk[:, xa - 1:xa, 3:4] < 50), 0, blk[:, xa - dx:xa])   # the hole (or margin) continues
    # colours: the panel's tan as printed, the banner cream / pale tan (luminance kept, so its brushed texture stays)
    rgb = out[:, :, :3].astype(float)
    hsv = np.array(Image.fromarray(out[:, :, :3]).convert("HSV")).astype(float)
    y0 = dst[0]
    tan = np.zeros(out.shape[:2], bool)
    tan[y0:] = (hsv[y0:, :, 1] > 55) & (hsv[y0:, :, 0] > 10) & (hsv[y0:, :, 0] < 40) & (out[y0:, :, 3] > 0)
    b0, b1 = (dst[2], dst[3]) if side == "ls" else (dst[1], dst[2])
    ban = np.zeros(out.shape[:2], bool)
    cols = np.where(~tan[(b0 + b1) // 2] & (out[(b0 + b1) // 2, :, 3] > 0))[0]
    cols = cols[(cols > 200) & (cols < 1450)]
    bx0, bx1 = cols.min() - 2, cols.max() + 3
    ban[b0 + 2:b1 - 2, bx0:bx1] = True
    tan &= ~ban
    rgb[tan] *= np.array(L["tan"])
    lum = rgb[ban].mean(1); lum = lum.mean() + (lum - lum.mean()) * L["texture"]   # the PC banner is smoother (Dark: almost flat)
    rgb[ban] = np.clip(lum[:, None] / lum.mean() * np.array(L["banner"]), 0, 255)
    out[:, :, :3] = rgb.round().astype(np.uint8)
    if side == "ds":   # the Dark panel's top corners are cut at 45 degrees with a lit edge, as printed (ISB, Galactic Domination)
        op = np.where(out[y0 + 20, :, 3] > 0)[0]; xl, xr = op.min(), op.max()
        c = 36
        for y in range(y0, y0 + c):
            k = c - (y - y0)
            out[y, xl:xl + k] = 0; out[y, xr - k + 1:xr + 1] = 0
            for x in (xl + k, xl + k + 1, xr - k, xr - k - 1):
                out[y, x, :3] = np.clip(out[y, x, :3].astype(float) * 1.25, 0, 255).astype(np.uint8)
        out[y0:y0 + 3, :, :3] = np.clip(out[y0:y0 + 3, :, :3].astype(float) * 1.2, 0, 255).astype(np.uint8)
    Image.fromarray(out).save(ROOT / f"assets/frames/{side}-mission.png", optimize=True)
    print(side, "banner rows", b0, b1, "cols", bx0, bx1, "text box from", t0, "(+%d)" % gain)


if __name__ == "__main__":
    for s in ("ls", "ds"):
        refit(s)
