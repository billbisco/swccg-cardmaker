"""#118 step 4-6: trace the averaged PC glyph images, fit spacing from the measured PC letter gaps, build the OTF.
In: glyphs/<cp>.png (white ink, 8 canonical px per PC px, cap top row 220, baseline row 476), pairs.json.
Out: HolotableTitle-Regular.otf, spacing.json (per-glyph side bearings and kerning, for the FONTLOG)."""
import json, collections, sys
import numpy as np, cv2, potrace
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

UPM, CAPU = 931, 700      # drawn at cap 700 / 931 em = 0.752 em (Fiorello CG's cap height, so CardMaker's sizes carry over); scaled to 1000 UPM on save
import os
BLUR = float(os.environ.get('BLUR', 4)); OPTT = float(os.environ.get('OPTT', 0.8)); THR = float(os.environ.get('THR', 0.5))
BASE_ROW, CAP_ROWS = 476, 256
K = CAPU / CAP_ROWS                     # font units per canonical px
CAP_PC = 32.0                           # PC px per cap height (scale.json)
meta = json.load(open('glyphs/meta.json'))
pairs = {tuple(k.split('|')): v for k, v in json.load(open('pairs.json')).items()}

NAMES = {' ': 'space', '!': 'exclam', '&': 'ampersand', '(': 'parenleft', ')': 'parenright', ',': 'comma', '-': 'hyphen',
         '.': 'period', '?': 'question', '’': 'quoteright', '•': 'bullet', ':': 'colon', ';': 'semicolon', '/': 'slash',
         "'": 'quotesingle', '‘': 'quoteleft', '#': 'numbersign', '“': 'quotedblleft', '”': 'quotedblright', 'é': 'eacute', 'è': 'egrave', 'á': 'aacute', 'à': 'agrave', 'í': 'iacute', 'ó': 'oacute', 'ú': 'uacute', 'É': 'Eacute', '◊': 'lozenge', '–': 'endash', '—': 'emdash'}
for d, n in zip('0123456789', 'zero one two three four five six seven eight nine'.split()):
    NAMES[d] = n


def gname(ch):
    return NAMES.get(ch, ch if ch.isascii() and ch.isalpha() else 'uni%04X' % ord(ch))


# ---------- tracing ----------
def trace(img):
    """potrace contours of one glyph image, in canonical px (x right, y down)."""
    m = cv2.GaussianBlur(img.astype(np.float32), (0, 0), BLUR) > 255 * THR
    return potrace.Bitmap(~m).trace(turdsize=40, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0,
                                   opticurve=True, opttolerance=OPTT), m


def draw(pen, curves, x0):
    """canonical px -> font units: x from the ink's left edge, y up from the baseline."""
    T = lambda p: ((p.x - x0) * K, (BASE_ROW - p.y) * K)
    for c in curves:
        pen.moveTo(T(c.start_point))
        for s in c.segments:
            if s.is_corner:
                pen.lineTo(T(s.c)); pen.lineTo(T(s.end_point))
            else:
                pen.curveTo(T(s.c1), T(s.c2), T(s.end_point))
        pen.closePath()


shapes = {}           # ch -> (curves, x0, ink width in units)
for ch in meta:
    img = cv2.imread('glyphs/%04x.png' % ord(ch), 0)
    curves, m = trace(img)
    xs = np.where(m.any(0))[0]
    shapes[ch] = ([c for c in curves], float(xs.min()), (xs.max() + 1 - xs.min()) * K)


# ---------- constructed glyphs (no PC instances) ----------
class Recorder:
    """a glyph made of other glyphs' outlines, each offset (dx, dy) in font units."""
    def __init__(self, parts, width):
        self.parts, self.width = parts, width


constructed = {}
pw = shapes['.'][2]
constructed[':'] = Recorder([('.', 0, 0), ('.', 0, 500 - pw * 0.95)], pw)
constructed[';'] = Recorder([(',', 0, 0), ('.', (shapes[','][2] - pw) / 2, 500 - pw * 0.95)], shapes[','][2])
constructed["'"] = Recorder([('’', 0, 0)], shapes['’'][2])
constructed['–'] = Recorder([('-', 0, 0), ('-', shapes['-'][2] * 0.6, 0)], shapes['-'][2] * 1.6)


def poly(pts):
    return pts


# slash, number sign and lozenge from the stem weight of l (measured on the PC glyph)
lw = shapes['l'][2]
SLASH = [[(0, -40), (lw * 0.95, -40), (lw * 0.95 + 300, 740), (300, 740)]]
LOZ = [[(0, 300), (230, 700), (460, 300), (230, -100)], [(230, 600), (400, 300), (230, 0), (60, 300)]][:1]
st = lw * 0.9
HASH = []
for x in (110, 290):
    HASH.append([(x, 0), (x + st, 0), (x + st + 60, 700), (x + 60, 700)])
for y in (200, 450):
    HASH.append([(20, y), (520, y), (520, y + st * 0.85), (20, y + st * 0.85)])
polys = {'/': (SLASH, lw * 0.95 + 300), '#': (HASH, 540), '◊': (LOZ, 460)}
# accented letters and curly quotes: parts are ('g', glyph, (a, b, c, d, dx, dy)) or ('p', polygon, offset)
qw = shapes['’'][2]
ACUTE = [(0, 570), (st, 570), (st + 110, 760), (110, 760)]
GRAVE = [(110, 570), (110 + st, 570), (st, 760), (0, 760)]
aw = st + 110
comp = {}
for ch, base, acc in (('é', 'e', ACUTE), ('è', 'e', GRAVE), ('á', 'a', ACUTE), ('à', 'a', GRAVE), ('í', 'i', ACUTE),
                      ('ó', 'o', ACUTE), ('ú', 'u', ACUTE), ('É', 'E', [(x, y + 230) for x, y in ACUTE])):
    bw = shapes[base][2]
    comp[ch] = ([('g', base, (1, 0, 0, 1, 0, 0)), ('p', acc, ((bw - aw) / 2, 0))], bw, base)
flip = lambda dx: (-1, 0, 0, -1, dx + qw, 544 + 700)          # ’ turned half round = ‘
comp['‘'] = ([('g', '’', flip(0))], qw, '’')
comp['“'] = ([('g', '’', flip(0)), ('g', '’', flip(qw * 1.7))], qw * 2.7, '’')
comp['”'] = ([('g', '’', (1, 0, 0, 1, 0, 0)), ('g', '’', (1, 0, 0, 1, qw * 1.7, 0))], qw * 2.7, '’')

# ---------- spacing: least squares over the measured PC gaps ----------
# gap(a, b) = R[a] + L[b] (cap-height units, ink edge to ink edge), regularised towards L = R
glyphs = list(meta)
idx = {c: i for i, c in enumerate(glyphs)}
n = len(glyphs)
rows, rhs, wts = [], [], []
tight = collections.defaultdict(list)
for (a, sp, b), v in pairs.items():
    if sp or a not in idx or b not in idx or len(v) < 1:
        continue
    g = float(np.median(v))
    r = np.zeros(2 * n); r[n + idx[a]] = 1; r[idx[b]] = 1
    rows.append(r); rhs.append(g); wts.append(min(len(v), 20) ** 0.5)
    tight[(a, b)] = (g, len(v), float(np.std(v)) if len(v) > 1 else 0)
for i in range(n):
    r = np.zeros(2 * n); r[i] = 1; r[n + i] = -1
    rows.append(r); rhs.append(0); wts.append(0.3)
A = np.array(rows) * np.array(wts)[:, None]; bvec = np.array(rhs) * np.array(wts)
sol = np.linalg.lstsq(A, bvec, rcond=None)[0]
L = {c: sol[idx[c]] * CAPU for c in glyphs}; R = {c: sol[n + idx[c]] * CAPU for c in glyphs}
spaces = [float(np.median(v)) * CAPU - R[a] - L[b] for (a, sp, b), v in pairs.items() if sp and a in idx and b in idx for _ in v]
SPACE = float(np.median(spaces))
kern = {}
for (a, b), (g, cnt, sd) in tight.items():
    v = np.array(pairs[(a, '', b)]) * CAPU - (R[a] + L[b])        # each measured gap minus the spaced gap
    res = float(np.median(v))
    # gaps are measured to 1 PC px (22 u): kern only where >= 8 instances agree, 70 % of them beyond half a pixel
    # on the same side (bimodal pairs are letters mis-assigned by the cluster alignment, not kerning)
    if cnt >= 8 and abs(res) >= 11 and np.mean(np.sign(v) * np.sign(res) * (np.abs(v) >= 11)) >= 0.7:
        kern[(a, b)] = int(np.clip(round(res), -90, 90))
print(f'{len(tight)} measured pairs, space {SPACE:.0f} u, {len(kern)} kerning pairs')
resid = [abs(g * CAPU - R[a] - L[b]) / CAPU * CAP_PC for (a, b), (g, c, _) in tight.items() if (a, b) not in kern]
print('residual after spacing+kerning (PC px): median %.2f, 90%% %.2f' % (np.median(resid), np.percentile(resid, 90)))

# side bearings for constructed glyphs
for ch, src in ((':', '.'), (';', ','), ("'", '’'), ('–', '-'), ('/', 'l'), ('#', 'H'), ('◊', 'o')):
    L[ch] = L[src]; R[ch] = R[src]

# ---------- build ----------
for ch, (_, _, src) in comp.items():
    L[ch] = L[src]; R[ch] = R[src]
order = ['.notdef', 'space'] + [gname(c) for c in glyphs] + [gname(c) for c in constructed] + [gname(c) for c in polys] + [gname(c) for c in comp]
cmap = {32: 'space', 0xA0: 'space'}
charstrings, metrics = {}, {}


def finish(name, pen_fn, inkw, ch):
    pen = T2CharStringPen(0, None)
    pen_fn(pen)
    lsb = round(L[ch]); adv = round(L[ch] + inkw + R[ch])
    charstrings[name] = pen.getCharString()
    metrics[name] = (adv, lsb)


def shifted(pen, dx, dy=0):
    return TransformPen(pen, (1, 0, 0, 1, dx, dy))


for ch in glyphs:
    curves, x0, w = shapes[ch]
    finish(gname(ch), lambda p, c=curves, x=x0, ch=ch: draw(shifted(p, round(L[ch])), c, x), w, ch)
    cmap[ord(ch)] = gname(ch)
for ch, rec in constructed.items():
    def f(p, rec=rec, ch=ch):
        for part, dx, dy in rec.parts:
            c, x0, _ = shapes[part]
            draw(shifted(p, round(L[ch]) + dx, dy), c, x0)
    finish(gname(ch), f, rec.width, ch)
    cmap[ord(ch)] = gname(ch)
for ch, (P, w) in polys.items():
    def f(p, P=P, ch=ch):
        q = shifted(p, round(L[ch]))
        for pts in P:
            q.moveTo(pts[0])
            for pt in pts[1:]:
                q.lineTo(pt)
            q.closePath()
    finish(gname(ch), f, w, ch)
    cmap[ord(ch)] = gname(ch)
for ch, (parts, w, src) in comp.items():
    def f(p, parts=parts, ch=ch):
        for kind, what, tr in parts:
            if kind == 'g':
                c, x0, _ = shapes[what]
                a, b, c2, d, dx, dy = tr
                draw(TransformPen(p, (a, b, c2, d, round(L[ch]) + dx, dy)), c, x0)
            else:
                q = shifted(p, round(L[ch]) + tr[0], tr[1])
                q.moveTo(what[0]); [q.lineTo(pt) for pt in what[1:]]; q.closePath()
    finish(gname(ch), f, w, ch)
    cmap[ord(ch)] = gname(ch)
pen = T2CharStringPen(0, None); pen.moveTo((50, 0)); pen.lineTo((450, 0)); pen.lineTo((450, 700)); pen.lineTo((50, 700)); pen.closePath()
pen.moveTo((100, 50)); pen.lineTo((100, 650)); pen.lineTo((400, 650)); pen.lineTo((400, 50)); pen.closePath()
charstrings['.notdef'] = pen.getCharString(); metrics['.notdef'] = (500, 50)
charstrings['space'] = T2CharStringPen(0, None).getCharString(); metrics['space'] = (round(SPACE), 0)

fb = FontBuilder(UPM, isTTF=False)
fb.setupGlyphOrder(order)
fb.setupCharacterMap(cmap)
fam = 'Holotable Title'
fb.setupCFF('HolotableTitle-Regular', {'FullName': fam, 'FamilyName': fam, 'Weight': 'Regular'}, charstrings, {})
# recompute lsb from the real outlines
fb.setupHorizontalMetrics(metrics)
gs = fb.font.getGlyphSet()
hm = {}
for g in order:
    bp = BoundsPen(gs); gs[g].draw(bp)
    hm[g] = (metrics[g][0], round(bp.bounds[0]) if bp.bounds else 0)
fb.setupHorizontalMetrics(hm)
fb.setupHorizontalHeader(ascent=700, descent=-209, lineGap=68)   # = Fiorello CG's 752 / -225 / 73 after the scale to 1000: same baseline in CardMaker's fixed line boxes
fb.setupNameTable({'familyName': fam, 'styleName': 'Regular', 'uniqueFontIdentifier': 'HolotableTitle-Regular 1.000',
                   'fullName': fam + ' Regular', 'psName': 'HolotableTitle-Regular', 'version': 'Version 1.000',
                   'copyright': 'Copyright 2026 The swccg-cardmaker contributors (github.com/billbisco/swccg-cardmaker)',
                   'licenseDescription': 'This Font Software is licensed under the SIL Open Font License, Version 1.1.',
                   'licenseInfoURL': 'https://openfontlicense.org',
                   'description': 'Drawn from the Star Wars CCG Players Committee card titles. Not affiliated with any commercial typeface.'})
fb.setupOS2(sTypoAscender=700, sTypoDescender=-209, sTypoLineGap=68, usWinAscent=866, usWinDescent=210,
            sxHeight=500, sCapHeight=700, achVendID='HOLO', fsType=0)
fb.setupPost()
if kern:
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    fea = 'feature kern {\n' + ''.join(f'  pos {gname(a)} {gname(b)} {v};\n' for (a, b), v in sorted(kern.items())) + '} kern;\n'
    addOpenTypeFeaturesFromString(fb.font, fea)
out = sys.argv[1] if len(sys.argv) > 1 else 'HolotableTitle-Regular.otf'
from fontTools.ttLib.scaleUpem import scale_upem
scale_upem(fb.font, 1000)
from fontTools.misc.timeTools import timestampFromString
fb.font['head'].created = fb.font['head'].modified = timestampFromString('Tue Nov  3 00:00:00 2026')   # fixed: the build is reproducible
fb.font.recalcTimestamp = False
fb.save(out)
json.dump({'space': SPACE, 'L': L, 'R': R, 'kern': {f'{a}|{b}': v for (a, b), v in kern.items()}}, open('spacing.json', 'w'), ensure_ascii=False, indent=0)
print('saved', out, len(order), 'glyphs')
