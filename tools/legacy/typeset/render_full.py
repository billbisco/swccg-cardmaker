import json,pymupdf as fitz,os
C=json.load(open('pdf/pdf_cards.json')); P=json.load(open('pdf/pdf_lines.json'))
gidmap={}
for r in P:
    if r.get('gid'): gidmap[(r['file'],r['page'],r['caption'])]=r['gid']
docs={}
out=[]
for c in C:
    if c['h']<200: continue
    g=gidmap.get((c['file'],c['page'],c['caption']))
    if not g: continue
    f='pdf/'+c['file'].split('/')[-1]
    d=docs.setdefault(f,fitz.open(f))
    x0,y0,x1,y1=c['bbox']
    pix=d[c['page']].get_pixmap(dpi=300,clip=fitz.Rect(x0,y0,x0+178.8,y1))
    fn=f"pcfull/{g[0]}.png"; pix.save(fn); out.append((g[0],fn))
json.dump(out,open('pcfull/index.json','w'))
print(len(out))
