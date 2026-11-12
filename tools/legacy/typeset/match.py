import json,collections,re
L=json.load(open('legacy_index.json'));P=json.load(open('pdf/pdf_lines.json'))
def norm(s): return re.sub(r'[^a-z0-9]','',(s or '').replace('ﬁ ','fi').replace('ﬂ ','fl').replace('ﬁ','fi').replace('ﬂ','fl').lower().replace('’',"'"))
def nt(s): return re.sub(r'[^a-z]','',(s or '').replace('ﬁ ','fi').replace('ﬂ ','fl').replace('ﬁ','fi').replace('ﬂ','fl').lower())[:60]
by=collections.defaultdict(list)
for g,c in L.items():
    for k in (c['legacy_title'],c['caption']):
        by[norm(k)].append(g)
miss=[]
for r in P:
    side='Light' if '_LS' in r['file'] else 'Dark'
    cands=sorted(g for g in set(by.get(norm(r['caption']),[])) if L[g]['side']==side)
    if len(cands)>1:   # disambiguate by text start
        t=nt(''.join(l['text'] for l in r['lines']))
        best=[g for g in cands if nt(re.sub(r'\{[^}]*\}','',L[g]['game_text'] or ''))[:25]==t[:25]]
        if best: cands=best
    if cands: r['gid']=cands
    else: miss.append(r['caption'])
print(len(P),len(miss),miss[:30])
json.dump(P,open('pdf/pdf_lines.json','w'),indent=0)
print(collections.Counter(len(r.get('gid',[])) for r in P))
