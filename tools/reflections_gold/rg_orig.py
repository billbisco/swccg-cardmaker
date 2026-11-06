"""Original playtest art: straighten each RG-C1 photo onto its own Remastered render (same card, same layout) with an
ECC homography, then cut the same art window as the Remastered crop."""
import json,os
from pathlib import Path
import numpy as np, cv2
from PIL import Image
ROOT=Path('rg-work'); RM=json.load(open(ROOT/'lib/remaster/manifest.json')); M=json.load(open(ROOT/'rg_cards.json'))
L=ROOT/'lib/original'; (L/'orig').mkdir(parents=True,exist_ok=True); (L/'warped').mkdir(exist_ok=True)
def card_only(a):
    g=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY)
    # photos sit on white/black backgrounds: keep the largest non-background blob
    m=((g>20)&(g<245)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m)
    if n<2: return a
    i=1+int(np.argmax(st[1:,cv2.CC_STAT_AREA])); x,y,w,h=st[i,:4]
    return a[y:y+h,x:x+w] if w*h>0.6*a.shape[0]*a.shape[1] else a
man={}
VIS={'15_31','15_33','15_205','15_236','15_274','15_177','15_156'}   # border left in, seen on the contact sheets
for g,e in RM.items():
    f=[x for x in os.listdir(ROOT/'scans/original') if x.split('.')[0]==g]
    if not f: man[g]=dict(e,status='no-source'); continue
    P=np.array(Image.open(ROOT/'scans/original'/f[0]).convert('RGB')); P=card_only(P)
    R=np.array(Image.open(ROOT/'scans/remaster'/f'{g}.png').convert('RGB'))
    land=R.shape[1]>R.shape[0]; S=(490,350) if land else (350,490); k=S[0]/R.shape[1]
    Rs=cv2.resize(R,S,interpolation=cv2.INTER_AREA)
    # crop the remaster's black outer border: card body is ~ inset 38px at 745 scale
    Ps=cv2.resize(P,S,interpolation=cv2.INTER_AREA)
    gr=lambda a: cv2.GaussianBlur(cv2.cvtColor(a,cv2.COLOR_RGB2GRAY).astype(np.float32),(5,5),0)
    # initial guess: photo card fills the remaster's card body (black border ~5% each side)
    bx=int(38*k); W0=np.array([[ (S[0]-2*bx)/S[0],0,bx],[0,(S[1]-2*bx)/S[1],bx],[0,0,1]],np.float32)
    H=np.linalg.inv(W0).astype(np.float32)
    try:
        cc,H=cv2.findTransformECC(gr(Rs),gr(Ps),H,cv2.MOTION_HOMOGRAPHY,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,300,1e-6),None,5)
    except cv2.error: cc=0
    Wp=cv2.warpPerspective(Ps,H,S,flags=cv2.INTER_LINEAR+cv2.WARP_INVERSE_MAP)
    # warp at full photo resolution for the crop: scale the homography up
    sx=P.shape[1]/S[0]; sy=P.shape[0]/S[1]; up=np.diag([1/k,1/k,1]).astype(np.float32)
    Hfull=np.diag([sx,sy,1]).astype(np.float32)@H@np.diag([k,k,1]).astype(np.float32)   # remaster(745) -> photo
    Rsz=(R.shape[1],R.shape[0])
    Wfull=cv2.warpPerspective(P,Hfull,Rsz,flags=cv2.INTER_CUBIC+cv2.WARP_INVERSE_MAP)
    Image.fromarray(cv2.resize(Wfull,(S[0],S[1]))).save(L/'warped'/f'{g}.jpg',quality=85)
    if land and e['family'].endswith('|land') and e['type'] in ('Interrupt','Effect'):
        fr=np.zeros(Wfull.shape[:2],np.uint8)
        for cy in (194,237): cv2.circle(fr,(961,cy),27,1,-1)
        Wfull=cv2.inpaint(Wfull,fr,5,cv2.INPAINT_TELEA)
    x0,y0,x1,y1=e['box']; crop=Image.fromarray(Wfull[y0:y1,x0:x1])
    a=np.array(crop.convert('RGB')).astype(int); band=np.concatenate([a[:6].reshape(-1,3),a[-6:].reshape(-1,3),a[:,:6].reshape(-1,3),a[:,-6:].reshape(-1,3)])
    flat=((band.max(1)<25)|(band.min(1)>235)).mean()
    if e['shaped']:
        al=Image.open(ROOT/'lib/remaster/orig'/f'{g}.png').split()[3]; crop=crop.convert('RGBA'); crop.putalpha(al)
    crop.save(L/'orig'/f'{g}.png')
    st='ok' if cc>=0.45 and g not in VIS else 'needs-review'
    man[g]=dict(e,status=st,align_cc=round(float(cc),3),edge_flat=round(float(flat),3),scan_source=e['original_file'],scan_note='Reflections Gold original playtest photo on the wiki (forum Photobucket / Category One buylist); straightened onto the Remastered layout',scan_size=list(P.shape[1::-1]),box_space='Remastered render space after straightening',x4=None,inpainted_frame_fraction=None)
json.dump(man,open(L/'manifest.json','w'),indent=1,ensure_ascii=False)
import collections; print(collections.Counter(v['status'] for v in man.values()))
cs=sorted(v.get('align_cc',0) for v in man.values()); print(cs[:10], cs[len(cs)//2])
