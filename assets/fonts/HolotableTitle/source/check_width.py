"""Ink width of each PC title vs the same title set in a font at the title's measured cap height (PC px)."""
import json, sys, numpy as np, re
from PIL import Image, ImageDraw, ImageFont
import importlib.util
src = open('extract.py').read().split("inst = collections.defaultdict")[0]
g = {}; exec(src, g)
fontfile = sys.argv[1]; capfrac = float(sys.argv[2])   # cap height / em of that font
rows = [r for r in json.load(open('cards.json')) if r['type'] != 'Location']
res = []
for r in rows[::3]:
    try: ink = g['title_mask'](f"crops/{r['key']}.png", r['side'] == 'Dark')
    except Exception: continue
    cl, lab = g['clusters'](ink)
    cl = [c for c in cl if c['x0'] > 1 and c['x1'] < ink.shape[1] - 2]
    text = g['clean'](r['title'])
    if text.startswith('•'):
        bl = [k for k, c in enumerate(cl) if (c['x1']-c['x0']) < 16 and (c['y1']-c['y0']) < 16]
        if bl: cl = cl[bl[0]:]
    while len(cl) > 1 and (cl[-1]['x0'] - cl[-2]['x1']) > 25: cl = cl[:-1]
    if len(cl) < 3: continue
    base = float(np.median([c['y1'] for c in cl])) + 1; capH = base - float(np.percentile([c['y0'] for c in cl], 10))
    if not 28 < capH < 36: continue
    pcw = cl[-1]['x1'] - cl[0]['x0'] + 1
    F = ImageFont.truetype(fontfile, 400)
    im = Image.new('L', (8000, 700), 0); ImageDraw.Draw(im).text((10, 10), text, font=F, fill=255)
    bb = im.getbbox(); w = (bb[2] - bb[0]) * capH / (400 * capfrac)
    if pcw > 380: continue   # likely squeezed to fit the bar
    if 0.8 < w / pcw < 1.2: res.append((w - pcw, w / pcw, text))
d = np.array([x[0] for x in res]); q = np.array([x[1] for x in res])
print(f'{len(res)} titles: width diff px median {np.median(d):+.2f}, |diff| median {np.median(abs(d)):.2f}, 90% {np.percentile(abs(d),90):.2f}; ratio median {np.median(q):.4f}')
for x in sorted(res, key=lambda x: -abs(x[0]))[:6]: print('  %+.1f %s' % (x[0], x[2]))
