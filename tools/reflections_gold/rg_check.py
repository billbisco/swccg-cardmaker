"""Render check for Reflections Gold (swccg-guild/work#174): render every set-15 card in CardMaker (holotable size) and
compare with its source: Remastered (15_N) with its RG-GEMP render, original (15_No) with its playtest photo straightened
onto the Remastered layout. Writes metrics.csv and side-by-side sheets (render | source), worst first."""
import csv,json,os,sys,urllib.request,math
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT='rg-work'; OUT=sys.argv[1]; os.makedirs(OUT+'/r',exist_ok=True)
API='http://localhost:8790/api'
M=json.load(open(ROOT+'/rg_cards.json'))
ids=[g for g in M]+[g+'o' for g in M]
if len(sys.argv)>2: ids=sys.argv[2:]
def render(g):
    p=f'{OUT}/r/{g}.png'
    if os.path.exists(p): return p
    d=json.load(urllib.request.urlopen(f'{API}/card/{g}',timeout=120))
    r=urllib.request.Request(f'{API}/render',data=json.dumps({"spec":d['spec'],"size":"holotable","format":"png"}).encode(),headers={"Content-Type":"application/json"})
    open(p,'wb').write(urllib.request.urlopen(r,timeout=300).read()); return p
def src(g):
    if g.endswith('o'):
        return ROOT+'/lib/original/warped/'+g[:-1]+'.jpg'
    return ROOT+'/scans/remaster/'+g+'.png'
rows=[]
for i,g in enumerate(ids):
    try:
        rp=render(g)
        a=Image.open(rp).convert('L'); b=Image.open(src(g)).convert('L')
        S=(260,186) if a.size[0]>a.size[1] else (186,260)
        A=np.array(a.resize(S,Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))).astype(float)
        B=np.array(b.resize(S,Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))).astype(float)
        d=np.abs(A-B); H=S[1]
        rows.append(dict(gid=g,title=M[g.rstrip('o')]['title'],version='original' if g.endswith('o') else 'remastered',orient='land' if S[0]>S[1] else 'port',
            mad=round(d.mean(),1),top=round(d[:int(H*.15)].mean(),1),middle=round(d[int(H*.15):int(H*.65)].mean(),1),bottom=round(d[int(H*.65):].mean(),1),status='ok'))
    except Exception as e:
        rows.append(dict(gid=g,title=M[g.rstrip('o')]['title'],status='error: '+str(e)[:120]))
    if (i+1)%20==0: print(i+1,flush=True)
with open(OUT+'/metrics.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['gid','title','version','orient','mad','top','middle','bottom','status']); w.writeheader(); w.writerows(rows)
for ver in ('remastered','original'):
    R=sorted([r for r in rows if r.get('version')==ver and r['status']=='ok'],key=lambda r:-r['mad'])
    for s in range(math.ceil(len(R)/24)):
        sh=Image.new('RGB',(6*420,4*330),'white'); dr=ImageDraw.Draw(sh)
        for k,r in enumerate(R[s*24:(s+1)*24]):
            a=Image.open(f"{OUT}/r/{r['gid']}.png").convert('RGB'); b=Image.open(src(r['gid'])).convert('RGB')
            h=300; a=a.resize((int(a.size[0]*h/a.size[1]),h)); b=b.resize((int(b.size[0]*h/b.size[1]),h))
            x=(k%6)*420; y=(k//6)*330
            if a.size[0]>200:   # landscape: stack
                a=a.resize((200,int(200*a.size[1]/a.size[0]))); b=b.resize((200,int(200*b.size[1]/b.size[0])))
            sh.paste(a,(x+2,y+2)); sh.paste(b,(x+4+a.size[0],y+2)); dr.text((x+2,y+305),f"{r['gid']} mad {r['mad']} {r['title'][:30]}",fill='black')
        sh.save(f'{OUT}/sheet-{ver}-{s+1:02d}.png')
print('done',len(rows),sum(1 for r in rows if r['status']!='ok'),'errors')
