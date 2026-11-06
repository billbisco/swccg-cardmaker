"""Crop the art window of every Remastered card (families.json windows + masks), write orig/<gid>.png and manifest."""
import json,os
from pathlib import Path
import numpy as np, cv2
from PIL import Image
ROOT=Path('rg-work'); M=json.load(open(ROOT/'rg_cards.json'))
L=ROOT/'lib'/'remaster'; F=json.load(open(L/'families.json')); (L/'orig').mkdir(exist_ok=True)
MANUAL={'Dark|Starship|port':[88,296,655,650],'Dark|Vehicle|port':[88,296,655,650],'Light|Device|port':[87,296,649,672],'Dark|Device|port':[87,296,649,672],'Light|Location|land':[94,193,945,551]}
man={}
for fam,d in F.items():
    win=d['window'] or MANUAL[fam]
    wide=fam.endswith('|land') and ('Interrupt' in fam or 'Effect' in fam)
    if wide:   # wide vision: the art fills CardMaker's rg template art box (x,y,w,h = 134,138,1952,1356 on 2220x1632) = this box on the 1039 render
        win=[round(134*1039/2220),round(138*1039/2220),round((134+1952)*1039/2220),round((138+1356)*1039/2220)]
    sp=L/f"sd-{fam.replace('|','_')}.png"
    frame=None
    if d['window'] and sp.exists():
        sd=cv2.imread(str(sp),0)
        frame=(sd<60).astype(np.uint8)
        frame=cv2.morphologyEx(frame,cv2.MORPH_OPEN,np.ones((3,3),np.uint8)); frame=cv2.dilate(frame,np.ones((5,5),np.uint8))
    for g in d['members']:
        e=M[g]; im=Image.open(ROOT/'scans/remaster'/f'{g}.png').convert('RGB')
        x0,y0,x1,y1=(win if wide else [win[0]+3,win[1]+3,win[2]-3,win[3]-3])
        crop=im.crop((x0,y0,x1,y1))
        shaped='|combo' in fam; inpainted=0.0
        if wide:   # the remaster's own frame pieces (title bar, text box, set sphere, icons) are inpainted so only the picture
            # is left; CardMaker's template draws its own frame over the same places
            fr=(frame.copy() if frame is not None else np.zeros(im.size[::-1],np.uint8))
            fr[:153,:]=1; fr[503:,:]=1   # the title bar band and the text box band (their text differs per card, so variance misses it)
            for cy in (194,237): cv2.circle(fr,(961,cy),27,1,-1)
            fr=cv2.dilate(fr,np.ones((9,9),np.uint8))
            fm=fr[y0:y1,x0:x1]; inpainted=round(float(fm.mean()),4)
            crop=Image.fromarray(cv2.inpaint(np.array(crop),fm,5,cv2.INPAINT_TELEA))
        elif frame is not None:
            fr=frame.copy()
            if fam.endswith('|land'):   # set sphere and Episode I icon on the art's right edge (vary per card, so not caught by variance)
                for cy in (194,237): cv2.circle(fr,(961,cy),27,1,-1)
            fm=fr[y0:y1,x0:x1]
            if shaped:
                crop=crop.convert('RGBA'); crop.putalpha(Image.fromarray(((1-fm)*255).astype(np.uint8)))
            elif fm.mean()>0:
                inpainted=round(float(fm.mean()),4)
                crop=Image.fromarray(cv2.inpaint(np.array(crop),fm,5,cv2.INPAINT_TELEA))
        crop.save(L/'orig'/f'{g}.png')
        man[g]=dict(title=e['title'],side=e['side'],set='15',type=e['type'],subType=e['subType'],gempId=g,status='ok',
            scan_source=e['remaster_file'],scan_note='Reflections Gold Remastered render on the wiki (art chosen by Bill 2026-11-05)',
            scan_size=list(im.size),box=[x0,y0,x1,y1],box_space='remaster render 745x1039 (1039x745 landscape)',family=fam,
            inpainted_frame_fraction=inpainted,window_from=('CardMaker rg template art box' if wide else 'family variance') if d['window'] else 'measured by hand (one-card family)',shaped=shaped,
            original_page=e.get('original_page'),original_file=e.get('original_file'),remaster_page=e['remaster_page'],
            orig=f'orig/{g}.png',x4=f'x4/{g}.webp')
json.dump(dict(sorted(man.items(),key=lambda x:int(x[0].split('_')[1]))),open(L/'manifest.json','w'),indent=1,ensure_ascii=False)
print(len(man))
