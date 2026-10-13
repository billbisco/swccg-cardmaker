"""Fit the stat-box typography (label size / width / tracking / inset, value size / gap, baseline) to a printed
Decipher scan by pixel comparison (Bill 2026-10-13: Kebyc / Boba Fett stat boxes did not match the printed cards).

    python3 fit_stats.py src/vs6/12-CC-L-kebyc.gif ls-character-alien POWER=1 ABILITY=2
    python3 fit_stats.py src/vs6/29-CC-D-bobafett.gif ds-character-alien POWER=4 ABILITY=3 ARMOR=5

The scan is mapped onto the 1632×2220 card by its silver frame (as art_crop does); ink = black on Light frames,
white on Dark. Prints the best parameters (coordinate descent on IoU of the ink masks inside the stat boxes).
"""
from __future__ import annotations
import base64, io, json, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import render

FONTS = {"AGBoldCnA": "fonts/Akzidenz-Grotesk BQ Condensed A.otf", "AGMedExt": "fonts/AkzidenzGrotesk-MediumExtended.otf"}


def mapped_scan(path: str) -> np.ndarray:
    s = Image.open(path).convert("RGB")
    a = np.array(s).astype(int)
    bright = a.sum(2) > 120
    rows = np.where(bright.mean(1) > 0.5)[0]; cols = np.where(bright.mean(0) > 0.5)[0]
    fx0, fy0, fx1, fy1 = cols.min(), rows.min(), cols.max(), rows.max()
    sc = 1343 / (fx1 - fx0)
    S = s.resize((round(s.width * sc), round(s.height * sc)), Image.LANCZOS)
    card = Image.new("RGB", (1632, 2220), "black"); card.paste(S, (144 - round(fx0 * sc), 144 - round(fy0 * sc)))
    return np.array(card).astype(int)


def page_html(t, stats, p, dark_ink):
    ink = "#000" if dark_ink else "#fff"
    css = "\n".join(f'@font-face{{font-family:"{k}";src:url("{render.data_uri(render.ASSETS / v)}");}}' for k, v in FONTS.items())
    y = t["stats_y"]
    parts = []
    for (x, w), (lab, val) in zip(t["stats"], stats):
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y + p["dy"]}px;width:{w}px;height:68px;display:flex;align-items:center;padding-left:{p["pl"]}px;box-sizing:border-box">'
                     f'<span class="lab" style="font-family:AGBoldCnA;font-size:{p["fs"]}px;letter-spacing:{p["ls"]}px;color:{ink};display:inline-block;transform:scaleX({p["sx"]});transform-origin:left center;white-space:nowrap">{lab}</span>'
                     f'<span class="val" style="font-family:AGMedExt;font-weight:bold;font-size:{p["vs"]}px;color:{ink};white-space:nowrap">{val}</span></div>')
    js = """document.fonts.ready.then(()=>{for(const l of document.querySelectorAll('.lab')){const w=l.getBoundingClientRect().width;
      l.nextElementSibling.style.marginLeft=(w-l.offsetWidth+%s)+'px';} document.body.dataset.ready='1';});""" % p["vm"]
    return f"<!doctype html><html><head><style>{css} body{{margin:0;background:transparent}}</style></head><body><div style='position:relative;width:1632px;height:2220px'>{''.join(parts)}</div><script>{js}</script></body></html>"


def main():
    scan, tname = sys.argv[1], sys.argv[2]
    stats = [a.split("=") for a in sys.argv[3:]]
    t = render.TEMPLATES[tname]
    dark_ink = bool(t.get("dark_text"))
    orig = mapped_scan(scan)
    y = t["stats_y"]
    boxes = [(x, w) for (x, w), _ in zip(t["stats"], stats)]
    y0, y1 = y + 4, y + 64
    def mask_orig():
        g = orig[y0:y1].mean(2)
        return (g < 80) if dark_ink else (g > 190)
    om = mask_orig()
    region = np.zeros_like(om)
    for x, w in boxes:
        region[:, x + 12:x + w - 12] = True
    p = {"fs": 56, "ls": 1.8, "sx": 1.0, "pl": 22, "dy": 0, "vs": 60, "vm": 26}
    steps = {"fs": [2, 1], "ls": [0.6, 0.3], "sx": [0.04, 0.02], "pl": [4, 2, 1], "dy": [3, 1], "vs": [3, 1], "vm": [4, 2, 1]}
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1632, "height": 2220})
        def score(pp):
            pg.set_content(page_html(t, stats, pp, dark_ink)); pg.wait_for_function("document.body.dataset.ready=='1'")
            png = pg.screenshot(clip={"x": 0, "y": y0, "width": 1632, "height": y1 - y0}, omit_background=True)
            a = np.array(Image.open(io.BytesIO(png)).convert("RGBA")).astype(int)
            m = a[:, :, 3] > 120
            inter = (m & om & region).sum(); uni = ((m | om) & region).sum()
            return inter / max(uni, 1)
        best = score(p)
        for rnd in range(3):
            for k, st in steps.items():
                for d in st:
                    improved = True
                    while improved:
                        improved = False
                        for sgn in (1, -1):
                            q = dict(p); q[k] = round(q[k] + sgn * d, 3)
                            s_ = score(q)
                            if s_ > best + 1e-4:
                                best, p, improved = s_, q, True
                                break
            print("round", rnd, round(best, 4), json.dumps(p))
        b.close()
    print("BEST", round(best, 4), json.dumps(p))


if __name__ == "__main__":
    main()
