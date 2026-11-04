"""Holotable Numbers: build from the files in this folder (byte-for-byte reproducible).

    pip install fonttools potracer opencv-python-headless numpy
    python3 build.py ..

1. Extended (destiny, stat values, slip numbers) and Bold Italic (bottom-strip number) start from TeX Gyre Heros
   Bold / Bold Italic (GUST Font License): widened, scaled so flat-topped digits (1 4 7) are as tall as on the
   PC's cards and sit on the baseline, digit spacing fitted (targets.json: per style, the flat-top height, line
   metrics and the fitted parameters).
"""
import os, sys, json, copy

from fontTools.ttLib import TTFont
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

def height(f, ch='8'):
    gs = f.getGlyphSet(); bp = BoundsPen(gs); gs[f.getBestCmap()[ord(ch)]].draw(bp); return (bp.bounds[3] - bp.bounds[1]) / f['head'].unitsPerEm

def digit_span(f):
    import numpy as np
    gs = f.getGlyphSet(); cm = f.getBestCmap(); u = f['head'].unitsPerEm; B = []
    for c in '0123456789':
        bp = BoundsPen(gs); gs[cm[ord(c)]].draw(bp); B.append(bp.bounds)
    B = np.array(B) / u; return float(B[:, 1].mean()), float(B[:, 3].mean())

def flat_top(f):
    gs = f.getGlyphSet(); cm = f.getBestCmap(); u = f['head'].unitsPerEm; t = []
    for c in '147':
        bp = BoundsPen(gs); gs[cm[ord(c)]].draw(bp); t.append(bp.bounds[3])
    return sum(t) / len(t) / u

def derive(src, out, sx, target, line, family, style, weight, italic=False, cls=None, digit_adv=1.0, star=1.0, caps_y=1.0):
    f = TTFont(src); upm = f['head'].unitsPerEm
    k = target / flat_top(f)                   # flat-topped digits (1 4 7) as tall as the replaced face's; on the baseline
    ty = 0.0
    rev = {}
    for cp, g in f.getBestCmap().items(): rev.setdefault(g, chr(cp))
    def cf(g):
        c = rev.get(g)
        if not cls or c is None: return 1.0
        return cls.get('digits', 1.0) if c.isdigit() else cls.get('other', 1.0)
    order = f.getGlyphOrder(); gs = f.getGlyphSet(); cs = {}; hm = {}
    for g in order:
        c = rev.get(g); s = star if c == '*' else 1.0
        ax = sx * k * cf(g) * s; ay = k * s * (caps_y if (c or '').isupper() else 1.0)
        adv, lsb = f['hmtx'][g]
        extra = adv * ax * (digit_adv - 1) if (c or '').isdigit() else 0.0     # digit spacing: half each side
        pen = T2CharStringPen(0, gs); gs[g].draw(TransformPen(pen, (ax, 0, 0, ay, extra / 2, ty))); cs[g] = pen.getCharString()
        hm[g] = (round(adv * ax + extra), round(lsb * ax + extra / 2))
    fb = FontBuilder(upm, isTTF=False); fb.setupGlyphOrder(order); fb.setupCharacterMap(f.getBestCmap())
    ps = family.replace(' ', '') + '-' + style.replace(' ', '')
    fb.setupCFF(ps, {'FullName': f'{family} {style}', 'FamilyName': family, 'Weight': style}, cs, {})
    fb.setupHorizontalMetrics(hm)
    L = {a: round(v * upm) for a, v in line.items()}
    fb.setupHorizontalHeader(ascent=L['hhea.ascent'], descent=L['hhea.descent'], lineGap=L['hhea.lineGap'])
    o = f['OS/2']
    fb.setupOS2(sTypoAscender=L['OS/2.sTypoAscender'], sTypoDescender=L['OS/2.sTypoDescender'], sTypoLineGap=L['OS/2.sTypoLineGap'],
                usWinAscent=L['OS/2.usWinAscent'], usWinDescent=L['OS/2.usWinDescent'], sxHeight=round(o.sxHeight * k),
                sCapHeight=round(o.sCapHeight * k), usWeightClass=weight, fsSelection=(0x01 if italic else 0x40) | (0x20 if weight >= 700 else 0), achVendID='HOLO')
    cr = f['name'].getDebugName(0) or ''
    fb.setupNameTable({'familyName': family, 'styleName': style, 'uniqueFontIdentifier': f'{ps} 1.000', 'fullName': f'{family} {style}',
                       'psName': ps, 'version': 'Version 1.000',
                       'copyright': cr + ' Holotable Numbers modifications copyright 2026 The swccg-cardmaker contributors.',
                       'description': 'Holotable Numbers is a modified version of TeX Gyre Heros (widened and rescaled for swccg-cardmaker), distributed under the GUST Font License.',
                       'licenseDescription': 'GUST Font License (LaTeX Project Public License 1.3c); see GUST-FONT-LICENSE.txt.'})
    fb.setupPost(italicAngle=f['post'].italicAngle)
    if 'GPOS' in f:
        gp = copy.deepcopy(f['GPOS'])
        scale_gpos(gp.table, sx * k)
        fb.font['GPOS'] = gp
    fb.font['head'].created = fb.font['head'].modified = 3845232000; fb.font['head'].macStyle = (2 if italic else 0) | (1 if weight >= 700 else 0)
    fb.font.recalcTimestamp = False
    fb.save(out)

def scale_gpos(table, ax):
    """scale horizontal values (XAdvance, XPlacement) in every pair/single positioning subtable."""
    def sv(v):
        if v is None: return
        for a in ('XAdvance', 'XPlacement'):
            if hasattr(v, a) and getattr(v, a): setattr(v, a, round(getattr(v, a) * ax))
    for lk in table.LookupList.Lookup:
        for st in lk.SubTable:
            if lk.LookupType == 9: st = st.ExtSubTable
            if getattr(st, 'Format', None) is None: continue
            if hasattr(st, 'PairSet'):
                for ps in st.PairSet:
                    for pv in ps.PairValueRecord: sv(pv.Value1); sv(pv.Value2)
            if hasattr(st, 'Class1Record'):
                for c1 in st.Class1Record:
                    for c2 in c1.Class2Record: sv(c2.Value1); sv(c2.Value2)
            if hasattr(st, 'Value'):
                v = st.Value
                if isinstance(v, list): [sv(x) for x in v]
                else: sv(v)



if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '..'
    T = json.load(open('targets.json'))
    for st, src, name in (('Extended', 'texgyreheros-bold.otf', 'Extended'), ('BoldItalic', 'texgyreheros-bolditalic.otf', 'Bold Italic')):
        p = T[st]['params']
        dst = os.path.join(out, f'HolotableNumbers-{st}.otf')
        derive(src, dst, p['sx'], T[st]['flat_top'], T[st]['line'], 'Holotable Numbers', name, p['weight'], italic=p['italic'],
               digit_adv=p['digit_adv'], star=p['star'], caps_y=p['caps_y'])
        print('HolotableNumbers-' + st)
