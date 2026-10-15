"""Virtual Block Mission / Critical Mission frames (VB7-9, e.g. Rebel Aces, Rally To Our Cause): full-art card under the
Admiral's Order title bar, a tan panel at the foot with the silver MISSION banner and the text box (Light: speckled
silver box like the Light Effect; Dark: black box like the Dark Effect). Built from our own frames: the Effect frame's
banner + text box, recoloured red -> tan, raised to the panel top with the text box stretched by mirrored tiles.
The type disc (teal hologram) is cut from the Holotable scans (no higher-resolution source yet)."""
import io, sys, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
ROOT = Path(__file__).resolve().parent; A = ROOT / "assets"
sys.path[:0] = [str(ROOT), str(ROOT / "webapp")]
import render

P = 1080   # panel top (printed ~0.47-0.53 of the card height)


def canvas(key):
    fr, fx, fy = render.TEMPLATES[key]["frame"]
    c = Image.new("RGBA", (1632, 2220), (0, 0, 0, 0)); c.alpha_composite(Image.open(A / fr).convert("RGBA"), (fx, fy))
    return np.array(c)


def tan(a, light):
    hsv = np.array(Image.fromarray(a[:, :, :3]).convert("HSV")).astype(float)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    red = ((h < 25) | (h > 235)) & (s > 70)
    h[red] = 33 * 255 / 360          # tan hue (Rally To Our Cause: ~#c8a878)
    s[red] = np.clip(s[red] * 0.55, 70, 125)
    v[red] = np.clip(v[red] * 0.95 + 25, 0, 215)
    out = np.array(Image.fromarray(np.dstack([h, s, v]).astype(np.uint8), "HSV").convert("RGB"))
    b = a.copy(); b[:, :, :3] = out; return b


def build(side):
    eff = f"{side}-effect"; t = render.TEMPLATES[eff]
    E = canvas(eff); Ad = canvas("ls-admirals-order")
    ax, ay, aw, ah = t["art"]; gx, gy, gw, gh = t["game_text"]
    src0 = ay + ah - 12; D = src0 - P
    G = np.zeros_like(E)
    G[:P] = Ad[:P]
    G[P:gy + 30 - D] = E[src0:gy + 30]
    band = E[gy + 40:gy + 120]; rows = []
    while sum(len(r) for r in rows) < D:
        rows.append(band if len(rows) % 2 == 0 else band[::-1])
    G[gy + 30 - D:gy + 30] = np.concatenate(rows)[:D]
    G[gy + 30:] = E[gy + 30:]
    G[P - 20:] = tan(G[P - 20:], side == "ls")
    if side == "ds":   # the Dark Mission prints the silver banner too (Rally To Our Cause): take the Light Effect's
        L = canvas("ls-effect"); lt = render.TEMPLATES["ls-effect"]
        lsrc0 = lt["art"][1] + lt["art"][3] - 12
        cx, cy, cw, ch = lt["card_type"]; y0, y1 = cy - 28, cy + ch + 28
        dst = y0 - (lsrc0 - P)
        G[dst:dst + (y1 - y0), cx - 20:cx + cw + 20] = L[y0:y1, cx - 20:cx + cw + 20]
    Image.fromarray(G).save(A / f"frames/{side}-mission.png")
    return D


def disc():
    UA = {"User-Agent": "Mozilla/5.0"}
    urls = ["https://res.starwarsccg.org/cards/legacy/VirtualBlock7-Light/large/rebelaces.gif"]
    import server
    acc = []
    for g in ("1007_L5825", "1009_L5356", "1009_L6593", "1007_L6657"):
        u = server.CARDS[g]["front"]["imageUrl"]
        im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())).convert("RGB").resize((350, 490), Image.LANCZOS)
        a = np.array(im).astype(float)
        # locate the disc: darkest-teal blob in the top-left corner
        sub = a[10:70, 10:70]; m = (sub[:, :, 1] > sub[:, :, 0] + 25) & (sub[:, :, 2] > sub[:, :, 0] + 25)
        ys, xs = np.nonzero(m); cy, cx = 10 + ys.mean(), 10 + xs.mean()
        acc.append(np.array(im.crop((int(cx - 17), int(cy - 17), int(cx + 17), int(cy + 17))).resize((136, 136), Image.LANCZOS)).astype(float))
    d = np.median(np.stack(acc), axis=0).astype(np.uint8)
    im = Image.fromarray(d).convert("RGBA")
    yy, xx = np.mgrid[0:136, 0:136]; al = np.clip((66 - np.hypot(xx - 67.5, yy - 67.5)) * 60, 0, 255).astype(np.uint8)
    im.putalpha(Image.fromarray(al)); im.save(A / "icons/disc-mission.png")


if __name__ == "__main__":
    print(build("ls"), build("ds")); disc()
