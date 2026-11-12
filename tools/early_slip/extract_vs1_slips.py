import pymupdf, json, sys
d=pymupdf.open(sys.argv[2] if len(sys.argv) > 2 else 'VirtualCards1.pdf'); p=d[0]
frames0=sorted([dr['rect'] for dr in p.get_drawings() if dr.get('fill') and dr['fill'][0]<0.2 and dr['rect'].width>175 and dr['rect'].width<200], key=lambda r:(r.x0>300, r.y0))
frames=[pymupdf.Rect(r.x0,r.y1-64,r.x1,r.y1) for r in frames0]
spans=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
out=[]
for r in frames:
  lines=[s for s in spans if 'Cn' in s['font'] and r.x0<s['origin'][0]<r.x1 and r.y0-5<s['origin'][1]<r.y1]
  stats=[s['text'] for s in sorted([s for s in spans if 'Haett' in s['font'] and r.x0<s['origin'][0]<r.x1 and r.y0-5<s['origin'][1]<r.y1], key=lambda s:s['origin'][1])]
  num=''.join(s['text'] for s in spans if 'BoldIt' in s['font'] and r.x0<s['origin'][0]<r.x1 and r.y1-8<s['origin'][1]<r.y1+2)
  ttl=[s['text'] for s in spans if 'Regular' in s['font'] and s['size']>9 and r.x0-20<s['origin'][0]<r.x1 and r.y0-30<s['origin'][1]<r.y1-50]
  out.append({'rect':[r.x0,r.y0,r.x1,r.y1],'title':' '.join(ttl).strip(),'lines':[s['text'].rstrip() for s in sorted(lines,key=lambda s:s['origin'][1])],'stats':stats,'number':num})
json.dump(out,open(sys.argv[1],'w'),indent=1)
for o in out: print(o['number'],o['title'],o['stats'],len(o['lines']),[round(v,1) for v in o['rect']])
