import json,collections,sys
C=json.load(open('pdf/pdf_cards.json'));U=json.load(open('pdf/akz_uni.json'))['AkzidenzGroteskBE-Cn']
TS=json.load(open('swccg-cardmaker/gempdata/legacy_typeset.json'));L=json.load(open('legacy_index.json'))
P=json.load(open('pdf/pdf_lines.json'))
items={}
for r in P:
    if not r.get('gid'): continue
    g=r['gid'][0]
    gt=TS['cards'].get(g,{}).get('gt')
    if not gt or len(gt['lines'])<2: continue
    # rebuild word items from pdf_lines chars that belong to gt lines (match by text)
    lines=[l for l in r['lines'] if l['text'].strip()]
    seq=[]; brk=[]
    for l in lines:
        ch=l['chars']; words=[]; cur=None; gap=0; lastend=None
        for ox,bx,c in ch:
            if c.strip():
                if cur is None: cur=[ox,bx,lastend]
                else: cur[1]=bx
            else:
                if cur: words.append(cur); cur=None
            if c.strip(): lastend=bx
        if cur: words.append(cur)
        for i,(a,b,prev) in enumerate(words):
            gp = (a-prev) if (i>0 and prev is not None) else None
            seq.append([b-a,gp])
        brk.append(len(seq))
    items[g]=dict(seq=seq,brk=brk,size=gt['size'],track=gt['track'],w=gt['w'],lo=gt['w_lo'],tpl=L[g]['template'],x=gt['x'],first_indent=lines[0]['chars'][0][0], lead=[c for c in lines[0]['chars'] if c[2].strip()][0][0]-min(l['left'] for l in lines), starts=[([c for c in l['chars'] if c[2].strip()][0][0]-min(ll['left'] for ll in lines)) for l in lines])
json.dump(items,open('kp_items.json','w'))
print(len(items))
