import json,urllib.request,cv2,numpy as np,collections,statistics as st
API='http://localhost:8791/api'
idx=json.load(open('pcfull/index.json')); L=json.load(open('legacy_index.json'))
per=collections.defaultdict(list)
for g,f in idx: per[L[g]['template']].append((g,f))
res=collections.defaultdict(lambda: collections.defaultdict(list)); allb={}
for tpl,lst in per.items():
    for gid,fn in lst[:6]:
        try:
            spec=json.load(urllib.request.urlopen(f'{API}/card/{gid}'))['spec']; spec['art']={'kind':'none'}
            r=urllib.request.urlopen(urllib.request.Request(API+'/render',data=json.dumps({'spec':spec,'size':'holotable','format':'png'}).encode(),headers={'Content-Type':'application/json'}),timeout=120)
            boxes=json.loads(r.headers['X-Piece-Boxes'])['pieces']; img=cv2.imdecode(np.frombuffer(r.read(),np.uint8),1)
        except Exception as e: print('fail',gid,e); continue
        allb[gid]=boxes
        pc=cv2.imread(fn,1); pc2=np.zeros_like(img); h=min(pc.shape[0],1039-32); pc2[32:32+h,:745]=pc[:h,:745]
        for name in ('icons','set_mark','expansion','ring_icons','destiny','affiliation'):
            if name not in boxes: continue
            x,y,bw,bh=[int(round(v)) for v in boxes[name]]
            if bw<8 or bh<8 or x<0 or y<0 or x+bw>745 or y+bh>1039: continue
            t=img[y:y+bh,x:x+bw]; best=None
            for s in [0.84+0.02*k for k in range(17)]:
                ts=cv2.resize(t,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
                R=30; cx,cy=x+bw/2,y+bh/2
                sx0,sy0=int(max(0,cx-bw*s/2-R)),int(max(0,cy-bh*s/2-R)); sx1,sy1=int(min(745,cx+bw*s/2+R)),int(min(1039,cy+bh*s/2+R))
                S=pc2[sy0:sy1,sx0:sx1]
                if S.shape[0]<ts.shape[0] or S.shape[1]<ts.shape[1]: continue
                m=cv2.matchTemplate(S,ts,cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(m)
                if not best or mx>best[0]:
                    ncx=sx0+loc[0]+ts.shape[1]/2; ncy=sy0+loc[1]+ts.shape[0]/2
                    best=(mx,s,ncx-cx,ncy-cy)
            if best and best[0]>0.55: res[tpl][name].append(best[1:])
out={}
for tpl,d in sorted(res.items()):
    out[tpl]={k:(len(v),round(st.median(a for a,b,c in v),3),round(st.median(b for a,b,c in v),1),round(st.median(c for a,b,c in v),1)) for k,v in d.items()}
    print(tpl,out[tpl])
json.dump(dict(scale=out,boxes=allb),open('pcfull/scale.json','w'))
