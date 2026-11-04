"""#123: Holotable Text, narrowed derivatives of Barlow Condensed (OFL 1.1, The Barlow Project Authors).
Each style: outlines and advances scaled horizontally by SX and uniformly so the cap height per em equals the face
CardMaker used before (sizes carry over). Renamed (OFL: a modified version gets its own name)."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.boundsPen import BoundsPen

def cap_per_em(path):
    f = TTFont(path); gs = f.getGlyphSet(); bp = BoundsPen(gs); gs[f.getBestCmap()[ord('H')]].draw(bp)
    return (bp.bounds[3] - bp.bounds[1]) / f['head'].unitsPerEm

def derive(src, out, sx, target_cap, family, style, weight, LINE, CLS=None):
    f = TTFont(src); upm = f['head'].unitsPerEm
    k = target_cap / cap_per_em(src)              # uniform scale so cap/em matches
    ax, ay = sx * k, k
    gs = f.getGlyphSet(); glyf = f['glyf']; new = {}
    rev = {}
    for cp, g in f.getBestCmap().items(): rev.setdefault(g, chr(cp))
    def cf(g):
        c = rev.get(g)
        if not CLS or c is None: return 1.0
        if c.isupper(): return CLS['upper']
        if c.islower(): return CLS['lower']
        if c.isdigit(): return CLS['digits']
        if c == ' ': return CLS['space']
        return CLS['punct']
    FAC = {g: ax * cf(g) for g in f.getGlyphOrder()}
    for g in f.getGlyphOrder():
        pen = TTGlyphPen(gs); gs[g].draw(TransformPen(pen, (FAC[g], 0, 0, ay, 0, 0))); new[g] = pen.glyph()
    for g, gl in new.items(): glyf[g] = gl
    hm = f['hmtx'].metrics
    for g in hm:
        adv, lsb = hm[g]; hm[g] = (round(adv * FAC.get(g, ax)), round(lsb * FAC.get(g, ax)))
    for g in f.getGlyphOrder(): glyf[g].recalcBounds(glyf)
    for t in ('GPOS',):        # kerning values scale horizontally
        if t in f:
            from fontTools.otlLib import maxContextCalc
            pass
    if 'kern' in f: del f['kern']
    for tb, attrs in (('OS/2', ('sxHeight', 'sCapHeight')),):
        for a in attrs: setattr(f[tb], a, round(getattr(f[tb], a) * ay))
    # line metrics per em = the replaced face's, so text lands on the same baselines in CardMaker's line boxes
    for a, v in LINE.items():
        tb, at = a.split('.'); setattr(f[tb], at, round(v * upm))
    if 'GPOS' in f: scale_gpos(f['GPOS'].table, ax)
    if 'fvar' in f or 'gvar' in f: raise SystemExit('static fonts only')
    f['OS/2'].usWeightClass = weight
    f['OS/2'].fsSelection &= ~(1 << 7)        # USE_TYPO_METRICS off, as on the replaced faces: browsers place lines by hhea
    nm = f['name']
    ps = family.replace(' ', '') + '-' + style.replace(' ', '')
    for rec in list(nm.names):
        if rec.nameID in (1, 3, 4, 6, 16, 17, 21, 22): nm.removeNames(nameID=rec.nameID)
    full = f'{family} {style}'
    for nid, val in ((1, family if style in ('Regular', 'Bold') else full), (2, style if style in ('Regular', 'Bold') else 'Regular'),
                     (3, f'{ps} 1.000'), (4, full), (6, ps), (16, family), (17, style)):
        nm.setName(val, nid, 3, 1, 0x409)
    cr = nm.getDebugName(0) or ''
    nm.setName(cr + ' Holotable Text modifications copyright 2026 The swccg-cardmaker contributors.', 0, 3, 1, 0x409)
    nm.setName('Holotable Text is a modified version of Barlow Condensed (narrowed and rescaled for swccg-cardmaker).', 10, 3, 1, 0x409)
    f['head'].created = f['head'].modified = 3845232000   # fixed timestamp: reproducible build
    f.recalcTimestamp = False
    f.save(out)

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
    # Targets per style: cap height per em and line metrics per em of the face each style replaces in CardMaker
    # (recorded as numbers in targets.json, so CardMaker's sizes and baselines carry over), and the width factor
    # per character class (classes.json), fitted so text sets to the same widths and line breaks.
    import json, os
    T = json.load(open('targets.json')); CLSALL = json.load(open('classes.json'))
    SX = {'Light': 0.799, 'Regular': 0.869, 'Bold': 0.959}          # narrowing of Barlow Condensed per style
    jobs = [('BarlowCondensed-Light.ttf', 'Light', 300), ('BarlowCondensed-Medium.ttf', 'Regular', 400), ('BarlowCondensed-SemiBold.ttf', 'Bold', 700)]
    out = sys.argv[1] if len(sys.argv) > 1 else '..'
    for src, style, w in jobs:
        t = T[style]; LINE = {k: v for k, v in t.items() if k != 'cap'}
        derive(src, os.path.join(out, f'HolotableText-{style}.ttf'), SX[style], t['cap'], 'Holotable Text', style, w, LINE, CLSALL[style])
        print('HolotableText-' + style, 'from', src)
