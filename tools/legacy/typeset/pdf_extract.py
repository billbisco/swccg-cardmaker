"""Extract per-card text lines from the PC's Virtual Legacy master PDFs (vector Akzidenz text)."""
import pymupdf as fitz, json, sys, re, collections
out=[]
for fn in sys.argv[1:]:
    d=fitz.open(fn)
    for pn,p in enumerate(d):
        cards=[i['bbox'] for i in p.get_image_info() if i['width']==745 and i['height']>=200]
        spans=[]
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                for s in l['spans']:
                    spans.append(dict(font=s['font'].split('+')[-1],size=round(s['size'],2),bbox=s['bbox'],origin=s['origin'],text=s['text'],chars=None))
        # raw chars for widths
        raw=p.get_text('rawdict')
        rspans=[]
        for b in raw['blocks']:
            for l in b.get('lines',[]):
                for s in l['spans']:
                    rspans.append(dict(font=s['font'].split('+')[-1],size=round(s['size'],2),origin=s['origin'],chars=[(c['c'],c['origin'][0],c['bbox'][2]) for c in s['chars']]))
        for cb in cards:
            x0,y0,x1,y1=cb
            inside=[s for s in rspans if x0-1<=s['origin'][0]<=x1+1 and y0-1<=s['origin'][1]<=y1+1]
            if not inside: continue
            cap=[s for s in inside if s['font'].startswith('Arial') and abs(s['size']-6.71)<0.05]
            caption=''.join(c[0] for s in sorted(cap,key=lambda s:s['origin'][0]) for c in s['chars']).strip()
            out.append(dict(file=fn,page=pn,bbox=cb,h=cb[3]-cb[1],caption=caption,spans=inside))
json.dump(out,open('pdf_cards.json','w'))
print(len(out))
