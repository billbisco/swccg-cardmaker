import json,collections,statistics as st
T=json.load(open('legacy_typeset_raw.json'));L=json.load(open('legacy_index.json'))
def med(v): return round(st.median(v),2)
def bestW(iv):
    best=None
    for W in [x/20 for x in range(2000,3200)]:
        ok=sum(1 for lo,hi in iv if lo<=W<(hi or 999))
        if not best or ok>best[1]: best=(W,ok)
    return best[0]
by=collections.defaultdict(lambda: collections.defaultdict(list))
for g,rs in T.items():
    t=L[g]['template']
    for r in rs:
        for b in ('gt','lore'):
            if b in r and r[b]['n']>=2:
                x=r[b]; d=by[t]
                d[b+'.x'].append(x['x']); d[b+'.size'].append(x['size']); d[b+'.track'].append(x['track']); d[b+'.pitch'].append(x['pitch'])
                d[b+'.iv'].append((x['w_lo'],x['w_hi']))
                if b=='lore': d['lore.indent'].append(x['lines'][0]['indent']); d['lore.y'].append(x['y'])
                if b=='gt' and r['card_h']>200: d['gt.y'].append(x['y'])
tpl={}
for t,d in by.items():
    e={}
    for b in ('gt','lore'):
        if not d.get(b+'.x'): continue
        e[b]=dict(x=med(d[b+'.x']),size=collections.Counter(d[b+'.size']).most_common(1)[0][0],track=med(d[b+'.track']),pitch=med(d[b+'.pitch']),w=bestW(d[b+'.iv']),n=len(d[b+'.x']))
        if b=='lore': e[b]['indent']=med(d['lore.indent']); e[b]['y']=med(d['lore.y'])
        if b=='gt' and d.get('gt.y'): e[b]['y']=med(d['gt.y'])
    tpl[t]=e
def pickW(lo,hi,tw):
    if hi is None: hi=lo+4
    if lo< tw < hi: return tw
    return round(lo+0.2,2) if tw<=lo else round(max(lo+0.05,hi-0.2),2)
cards={}
import difflib,re
def _w(t): return [w for w in (re.sub(r'[^a-z0-9]','',x.lower()) for x in re.sub(r'\{[^}]*\}',' ',t or '').split()) if w]
def same_card(g,r):
    a=_w(' '.join(r['gt']['lines'] if isinstance(r['gt']['lines'][0],str) else [l['text'] for l in r['gt']['lines']])) if 'gt' in r else []
    b=_w(L[g]['game_text'])
    return not a or difflib.SequenceMatcher(None,a,b).ratio()>=0.5
DROP=[]
GIV=json.load(open('greedy_iv.json'))
def pickW2(a,b,tw):
    # the middle of the widths that reproduce the PC's breaks (most robust to our 0.1-0.2 pt width differences),
    # at most 1.5 pt from either end
    return round(min((a+b)/2, a+1.5),2)
for g,rs in T.items():
    t=L[g]['template']; e={}
    rs=[r for r in rs if same_card(g,r)] or []
    if not rs: DROP.append(g); continue
    rs=sorted(rs,key=lambda r:-r['card_h'])   # a full card first
    for b in ('gt','lore'):
        r=next((r for r in rs if b in r and r[b]['n']>=1),None)
        if not r: continue
        x=r[b]; tw=(tpl.get(t,{}).get(b) or {}).get('w') or x['w_lo']+1
        e[b]=dict(x=x['x'],size=x['size'],track=x['track'],pitch=x['pitch'] if x['n']>1 else (tpl.get(t,{}).get(b) or {}).get('pitch',x['pitch']),
                  w=(pickW2(*GIV[g],tw) if b=='gt' and GIV.get(g) else pickW(x['w_lo'],x['w_hi'],tw)),w_lo=x['w_lo'],w_hi=x['w_hi'],
                  lines=[l['text'].strip() for l in x['lines']],src=f"{r['file']} p{r['page']+1}")
        if b=='lore': e[b]['indent']=x['lines'][0]['indent']; e[b]['y']=x['y']
        if b=='gt' and r['card_h']>200: e[b]['y']=x['y']
    cards[g]=e
out={"about":"Virtual Legacy typesetting read from the PC's own vector text in Virtual_Legacy_Final_Master_LS.pdf / _DS.pdf (wiki.swccg.com, 2014): game text and lore box left edge x, line width w, first baseline y (pt from the card's left / top edge), Akzidenz-Grotesk BE Condensed size (pt), tracking (1/1000 em) and line pitch (pt); lines = the PDF's line breaks. Built by tools/legacy/typeset/build_typeset.py. Master px = pt * 8.3333 + 70 (x) / + 136 (y).",
     "templates":tpl,"cards":cards}
json.dump(out,open('swccg-cardmaker/gempdata/legacy_typeset.json','w'),ensure_ascii=False,separators=(',',':'))
for t,e in sorted(tpl.items()): print(t,e)
print(len(cards),'dropped',len(DROP),DROP[:20])
