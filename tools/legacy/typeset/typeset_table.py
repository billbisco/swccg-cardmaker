"""Per-card typesetting of the PC's Virtual Legacy master list (pdf_cards.json) -> legacy_typeset.json."""
import json,collections,statistics as st,re,sys
C=json.load(open('pdf/pdf_cards.json')); U=json.load(open('pdf/akz_uni.json'))
P=json.load(open('pdf/pdf_lines.json'))
gid_of={(r['file'],r['page'],round(r['lines'][0]['y'],1) if r['lines'] else 0,r['caption']):r.get('gid') for r in P}
def rows(spans):
    chars=[]
    for s in spans:
        for ch,ox,bx in s['chars']:
            chars.append((s['origin'][1],ox,bx,ch,s['size'],s['font']))
    R=[]
    for c in sorted(chars,key=lambda c:c[0]):
        if R and abs(R[-1][0]-c[0])<1.2: R[-1][1].append(c)
        else: R.append([c[0],[c]])
    return [(y,sorted(cs,key=lambda c:c[1])) for y,cs in R]
def block(spans,x0,y0):
    R=[(y,cs) for y,cs in rows(spans) if any(c[3].strip() for c in cs)]
    if not R: return None
    # main block: the longest run with pitch 6-9
    runs=[[R[0]]]
    for a,b in zip(R,R[1:]):
        if 5.5<b[0]-a[0]<9.5: runs[-1].append(b)
        else: runs.append([b])
    R=max(runs,key=len)
    sizes=collections.Counter(c[4] for y,cs in R for c in cs if c[5].endswith('BE-Cn'))
    if not sizes: return None
    size=sizes.most_common(1)[0][0]
    tr=[]
    for y,cs in R:
        for a,b in zip(cs,cs[1:]):
            if a[5].endswith('BE-Cn') and b[5]==a[5] and a[3] in U['AkzidenzGroteskBE-Cn'] and 0<b[1]-a[1]<6:
                tr.append(((b[1]-a[1])-U['AkzidenzGroteskBE-Cn'][a[3]]*a[4]/1000)/a[4]*1000)
    track=round(st.median(tr),1) if tr else 0
    ys=[y for y,_ in R]; pitch=round(st.median([b-a for a,b in zip(ys,ys[1:])]),2) if len(ys)>1 else round(size*1.03,2)
    left=min(cs[0][1] for y,cs in R)-x0
    lo=0; his=[]; lines=[]
    for i,(y,cs) in enumerate(R):
        nons=[c for c in cs if c[3].strip()]
        right=nons[-1][2]-x0
        lo=max(lo,right-left)
        lines.append(dict(text=''.join(({'S':'▲','T':'▼'}.get(c[3],' ') if c[5].startswith('Wingdings3') else ' ' if c[5].startswith('Wingdings') else c[3]) for c in cs).replace('ﬁ ','fi').replace('ﬂ ','fl').replace('ﬁ','fi').replace('ﬂ','fl'),right=round(right-left,2),indent=round(nons[0][1]-x0-left,2)))
        if i+1<len(R):
            nx=R[i+1][1]
            if nx[0][3]==' ': continue
            k=0
            while k<len(nx) and nx[k][3]!=' ': k+=1
            # where the next word would start: after this line's trailing space (or one space after the last glyph)
            end = cs[-1][2] if cs[-1][3]==' ' else nons[-1][2]+U['AkzidenzGroteskBE-Cn'][' ']*size/1000
            his.append(end-x0-left+(nx[k-1][2]-nx[0][1]))
    valid=[h for h in his if h>lo]
    hi=min(valid) if valid else None
    return dict(size=size,track=track,pitch=pitch,x=round(left,2),y=round(R[0][0]-y0,2),w_lo=round(lo,2),w_hi=round(hi,2) if hi else None,n=len(R),lines=lines)
out={}
for c in C:
    x0,y0,x1,y1=c['bbox']
    gt=[s for s in c['spans'] if (s['font'].startswith('AkzidenzGroteskBE-Cn') or s['font'].startswith('Wingdings') or (s['font'].startswith('AkzidenzGroteskBE-BoldCn') and s['size']>7.05)) and (s['size']>=6.9 or s['font'].startswith('Wingdings')) and (c['h']<200 or s['origin'][1]-y0>0.45*(y1-y0))]
    lo=[s for s in c['spans'] if (s['font'].startswith('AkzidenzGroteskBE-Cn') or s['font'].startswith('AkzidenzGroteskBE-BoldCn')) and 5.5<=s['size']<6.95 and s['origin'][1]-y0<0.45*(y1-y0)]
    rec={'caption':c['caption'],'file':c['file'].split('/')[-1],'page':c['page'],'card_h':round(y1-y0,1)}
    g=block(gt,x0,y0); l=block(lo,x0,y0) if c['h']>200 else None
    if g: rec['gt']=g
    if l: rec['lore']=l
    # match to gid by caption + first game text line
    key=None
    for r in P:
        if r['file']==c['file'] and r['page']==c['page'] and r['caption']==c['caption'] and r.get('gid'):
            key=r['gid'];break
    if key:
        for gidx in key: out.setdefault(gidx,[]).append(rec)
json.dump(out,open('legacy_typeset_raw.json','w'),indent=0,ensure_ascii=False)
print(len(out), sum(len(v) for v in out.values()))
