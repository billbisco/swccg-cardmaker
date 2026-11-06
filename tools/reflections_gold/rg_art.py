"""Reflections Gold art library: cut the art window from each card image by frame family (variance between aligned
cards = picture; identical = frame). Usage: python3 rg_art.py measure remaster|original"""
import json,sys,os
from collections import defaultdict
from pathlib import Path
import numpy as np, cv2
from PIL import Image
ROOT=Path('rg-work'); MAN=json.load(open(ROOT/'rg_cards.json'))
def fam(e,land):
    t=e['type']; st=(e['subType'] or '')
    combo='|combo' if ' & ' in e['title'] and t in ('Interrupt','Effect') else ''
    if t=='Character': t='Character'
    return f"{e['side']}|{t}{combo}|{'land' if land else 'port'}"
def load(p):
    im=Image.open(p).convert('RGB'); return im
def measure(kind):
    out=ROOT/'lib'/kind; (out/'orig').mkdir(parents=True,exist_ok=True)
    fams=defaultdict(list); imgs={}
    for g,e in MAN.items():
        f=[x for x in os.listdir(ROOT/'scans'/kind) if x.split('.')[0]==g]
        if not f: continue
        im=load(ROOT/'scans'/kind/f[0]); land=im.size[0]>im.size[1]
        S=(1039,745) if land else (745,1039)
        if im.size!=S: im=im.resize(S,Image.LANCZOS)
        imgs[g]=im; fams[fam(e,land)].append(g)
    res={}; rep={}
    for F,mem in sorted(fams.items(),key=lambda x:-len(x[1])):
        S=imgs[mem[0]].size
        G={g:np.array(imgs[g].convert('L')).astype(np.float32) for g in mem}
        if len(mem)>=4:
            med=np.median(np.stack(list(G.values())),axis=0)
            ref=min(mem,key=lambda g:np.abs(G[g]-med).mean())
            W={}
            for g in mem:
                w=np.eye(2,3,dtype=np.float32)
                try:
                    cc,w=cv2.findTransformECC(G[ref],G[g],w,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,100,1e-5),None,5)
                    if cc<0.3 or abs(w[0,0]-1)>.05 or abs(w[1,1]-1)>.05: w=np.eye(2,3,dtype=np.float32)
                except cv2.error: w=np.eye(2,3,dtype=np.float32)
                W[g]=w
            st=[cv2.warpAffine(G[g],W[g],S,flags=cv2.INTER_LINEAR+cv2.WARP_INVERSE_MAP) for g in mem]
            sd=np.std(np.stack(st),axis=0)
            v8=np.clip(sd*255/max(sd.max(),1),0,255).astype(np.uint8)
            _,bw=cv2.threshold(v8,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            bw=cv2.morphologyEx(bw,cv2.MORPH_OPEN,np.ones((31,31),np.uint8))
            n,lab,stats,_=cv2.connectedComponentsWithStats(bw)
            big=stats[1:,cv2.CC_STAT_AREA].max()
            keep=[k for k in range(1,n) if stats[k,cv2.CC_STAT_AREA]>0.15*big and stats[k,cv2.CC_STAT_HEIGHT]>100]
            m=np.isin(lab,keep).astype(np.uint8)*255
            ys,xs=np.where(m>0); win=[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1]
            cv2.imwrite(str(out/f"mask-{F.replace('|','_')}.png"),m)
            Image.fromarray(np.clip(sd*3,0,255).astype(np.uint8)).save(out/f"sd-{F.replace('|','_')}.png")
        else:
            win=None; W={g:np.eye(2,3,dtype=np.float32) for g in mem}
        rep[F]=(len(mem),win); print(F,len(mem),win,flush=True)
        res[F]=dict(members=mem,window=win)
    json.dump(res,open(out/'families.json','w'),indent=1)
if __name__=='__main__': measure(sys.argv[2])
