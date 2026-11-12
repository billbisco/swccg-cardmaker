"""Holotable Text PC: Holotable Text Regular / Bold with the advance widths of the faces the Players Committee set its
Virtual Legacy slips in (2009-2014 release sheets and the 2014 Virtual Cards Master List PDFs: Akzidenz-Grotesk BE
Condensed for game text and lore, BE Bold Condensed for bold words). Only the width numbers are taken from the PDFs
(pc_widths.json, 1/1000 em, read from the PDFs' font dictionaries); every outline is Holotable Text's own, scaled
horizontally per glyph (factor clamped to 0.85-1.20, the rest goes into the side bearings) so words take the same
room as on the PC's slips and lines break at the same words. Kerning: Barlow's is dropped and the PC's
pairs are added (pc_widths.json kern_regular, median offsets of each letter pair in the PDFs). Cap height per em stays 0.706, the PC face's, so a PC size of N pt is N x 8.333 px on the 1632 px master.
    python3 build_pc.py [outdir]
"""
import sys, os, json
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

def derive(src, out, widths, family, style, kern=None):
    f = TTFont(src); upm = f['head'].unitsPerEm
    srcgs = TTFont(src).getGlyphSet()   # untouched outlines (composites are decomposed from these)
    cmap = f.getBestCmap(); glyf = f['glyf']; hm = f['hmtx'].metrics
    from fontTools.pens.recordingPen import DecomposingRecordingPen
    from fontTools.pens.boundsPen import BoundsPen
    ratios = sorted((widths[chr(cp)] / 1000 * upm) / hm[g][0] for cp, g in cmap.items() if chr(cp) in widths and hm[g][0] > 0)
    med = ratios[len(ratios) // 2]   # glyphs the PDFs never used keep their proportion to the rest of the face
    done = set()
    for cp, g in sorted(cmap.items()):
        if g in done: continue
        done.add(g)
        adv, lsb = hm[g]
        if adv <= 0: continue
        tgt = widths.get(chr(cp))
        new_adv = round(tgt / 1000 * upm) if tgt else round(adv * med)
        k = new_adv / adv
        ko = min(1.20, max(0.85, k))       # outline factor; the rest of the change goes into the side bearings
        rec = DecomposingRecordingPen(srcgs); srcgs[g].draw(rec)
        bp = BoundsPen(None); rec.replay(TransformPen(bp, (ko, 0, 0, 1, 0, 0)))
        if bp.bounds:
            x0, _, x1, _ = bp.bounds
            nlsb = round(lsb * ko) if ko == k else round((new_adv - (x1 - x0)) / 2)
            dx = nlsb - x0
        else:
            nlsb, dx = 0, 0
        pen = TTGlyphPen(None); rec.replay(TransformPen(pen, (ko, 0, 0, 1, dx, 0))); gl = pen.glyph(); gl.recalcBounds(glyf)
        glyf[g] = gl
        hm[g] = (new_adv, gl.xMin if gl.numberOfContours else 0)
    for t in ('GPOS', 'kern'):
        if t in f: del f[t]
    if kern:   # the PC's kerning pairs (read off the master list PDFs), as a plain GPOS kern feature
        from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
        rules = []
        for pair, v in sorted(kern.items()):
            ga, gb = cmap.get(ord(pair[0])), cmap.get(ord(pair[1]))
            if ga and gb:
                rules.append(f"    pos {ga} {gb} {round(v / 1000 * upm)};")
        addOpenTypeFeaturesFromString(f, "feature kern {\n" + "\n".join(rules) + "\n} kern;\n")
    nm = f['name']; ps = family.replace(' ', '') + '-' + style
    for rec in list(nm.names):
        if rec.nameID in (1, 3, 4, 6, 16, 17): nm.removeNames(nameID=rec.nameID)
    for nid, val in ((1, family), (3, f'{ps} 1.000'), (4, f'{family} {style}'), (6, ps), (16, family), (17, style)):
        nm.setName(val, nid, 3, 1, 0x409)
    nm.setName('Holotable Text PC: Holotable Text with the Players Committee slips\' advance widths (swccg-cardmaker).', 10, 3, 1, 0x409)
    f['head'].created = f['head'].modified = 3845232000; f.recalcTimestamp = False
    f.save(out)

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..')
    W = json.load(open(os.path.join(here, 'pc_widths.json'), encoding='utf-8'))
    derive(os.path.join(here, '..', 'HolotableText-Regular.ttf'), os.path.join(out, 'HolotableTextPC-Regular.ttf'), W['regular'], 'Holotable Text PC', 'Regular', W.get('kern_regular'))
    derive(os.path.join(here, '..', 'HolotableText-Bold.ttf'), os.path.join(out, 'HolotableTextPC-Bold.ttf'), W['bold'], 'Holotable Text PC', 'Bold')
    print('built HolotableTextPC-Regular.ttf, HolotableTextPC-Bold.ttf')
