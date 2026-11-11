import json,collections,sys
d=json.load(open('pdf/pdf_cards.json'))
def lines_of(c, pred):
    chars=[]
    for s in c['spans']:
        if pred(s):
            for ch,ox,bx in s['chars']:
                chars.append((round(s['origin'][1],1),ox,bx,ch,s['size'],s['font']))
    rows=collections.defaultdict(list)
    for y,ox,bx,ch,sz,f in chars:
        k=None
        for yy in rows:
            if abs(yy-y)<1.2: k=yy;break
        rows[k if k is not None else y].append((ox,bx,ch,sz,f))
    out=[]
    for y in sorted(rows):
        r=sorted(rows[y])
        out.append(dict(y=y,chars=r,text=''.join(c[2] for c in r)))
    return out
def is_gt(s): return (s['font'].startswith('AkzidenzGroteskBE') and 6.9<=s['size']<=7.6 and not s['font'].endswith('BoldCn')) or (s['font'].startswith('Wingdings') ) or (s['font'].startswith('AkzidenzGroteskBE-BoldCn') and s['size']>7.05)
res=[]
for c in d:
    L=[l for l in lines_of(c,is_gt) if l['text'].strip()]
    # keep the main block: lines with pitch ~7.5 contiguous at the bottom
    if not L: continue
    x0=c['bbox'][0]; y0=c['bbox'][1]
    rec=dict(caption=c['caption'],page=c['page'],file=c['file'],h=round(c['h']),lines=[])
    for i,l in enumerate(L):
        ch=l['chars']
        left=ch[0][0]-x0
        nonsp=[x for x in ch if x[2].strip()]
        right=nonsp[-1][1]-x0
        rec['lines'].append(dict(y=round(l['y']-y0,2),left=round(left,2),right=round(right,2),text=l['text'],chars=[(round(a[0]-x0,3),round(a[1]-x0,3),a[2]) for a in ch],size=collections.Counter(x[3] for x in ch).most_common(1)[0][0]))
    res.append(rec)
json.dump(res,open('pdf/pdf_lines.json','w'),indent=0)
print(len(res))
