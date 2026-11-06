"""Build CardMaker card data for Reflections Gold (set 15): Remastered = 15_N (set "15"), original playtest = 15_No (set "15o"),
from the wiki's card pages. Writes gempdata/ReflectionsGold.json in the swccg-card-json shape CardMaker reads."""
import json,re,sys
from PIL import Image
T=json.load(open('rg-work/data/wikitext.json')); M=json.load(open('rg-work/rg_cards.json'))
def fields(t):
    m=re.search(r'\{\{Card(.*?)\n\}\}',t,re.S).group(1)
    out={}; cur=None
    for line in m.split('\n'):
        mm=re.match(r'\|\s*([a-z_0-9]+)\s*=(.*)',line)
        if mm: cur=mm.group(1); out[cur]=mm.group(2)
        elif cur: out[cur]+='\n'+line
    return {k:v.strip() for k,v in out.items()}
def clean(s):
    s=re.sub(r'</?nowiki>','',s or ''); s=re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]',r'\2',s); s=re.sub(r"'''?",'',s)
    s=re.sub(r'<ref[^>]*/>|<ref.*?</ref>','',s,flags=re.S); return s.strip()
def bullets(s): return [clean(x) for x in re.findall(r'^\*\s*(.+)$',s or '',re.M)]
DOTS={k:sorted(v) for k,v in json.load(open('rg-work/data/part_dots.json')).items()}
cards=[]
for g,e in M.items():
    n=int(g.split('_')[1])
    for page,gid,sid,expname in ((e['remaster_page'],g,'15','Reflections Gold Remastered'),(e['original_page'],g+'o','15o','Reflections Gold')):
        F=fields(T[page]); typ=F.get('type','')
        icons=[x for x in re.findall(r'\[\[([^\]|]+)',F.get('icons','')) if x not in ('Alien','Rebel','Imperial','Droid','Republic','Jedi Master','Sith','Device','Starship','Vehicle')]
        icons=icons+[expname]
        uniq=F.get('uniqueness','')
        title=clean(F['title']); dot='•' if uniq.lower().startswith('unique') else ''   # sites print the dot too (RG-GEMP Naboo: Ceremonial Chamber)
        if ' & ' in title and typ in ('Interrupt','Effect'):
            parts=[]
            for p in title.split(' & '):
                k=re.sub(r'[^a-z0-9]','',p.lower()); u=DOTS.get(k)
                parts.append(('•' if u==[True] else '')+p)
            title=' & '.join(parts)
        else: title=dot+title
        f={"title":title,"type":typ,"destiny":F.get('destiny',''),"gametext":clean(F.get('game_text','')),"lore":clean(F.get('lore','')),"icons":icons}
        st=F.get('subtype','')
        if typ in ('Interrupt','Effect') and st and st not in (typ,): f['subType']=st.replace(' Interrupt','').replace(' Effect','') if typ=='Interrupt' else st.replace(' Effect','')
        if typ=='Character': f['subType']=st
        if typ in ('Starship','Vehicle'): f['subType']={'Capital':'Capital: _Imperial_-Class Star Destroyer','Combat':'Combat Vehicle: AT-ST'}.get(st,st)
        if typ=='Location': f['subType']='Site'
        if typ=='Location':   # "0 Force icons; [[Planet]] [[Exterior Site|Exterior]] [[Episode I]]" per side
            for side_,key in (('light','lightSideIcons'),('dark','darkSideIcons')):
                v=F.get(side_+'_icons','')
                m_=re.match(r'\s*(\d+)',v); f[key]=int(m_.group(1)) if m_ else 0
            li=[re.split(r'\|',x)[-1] for x in re.findall(r'\[\[([^\]]+)\]\]',F.get('light_icons',''))]
            f['icons']=[x for x in ('Interior','Exterior','Planet','Episode I') if x in li]+[expname]
            f['destiny']=F.get('destiny','') or '0'
        for k in ('power','ability','deploy','forfeit','armor','maneuver','hyperspeed','landspeed','politics'):
            if F.get(k): f[k]=clean(F[k])
        ch=bullets(F.get('characteristics',''))
        ext=[c for c in ch if c in ('Force-Sensitive','Force-Attuned')]
        if ext: f['extraText']=ext
        ch=[c for c in ch if c not in ext and c!='Skywalker']
        if ch: f['characteristics']=ch
        if F.get('credits'): f['credits']=F['credits']
        if uniq.lower().startswith('unique'): f['uniqueness']='*'
        img='scans/remaster/'+g+'.png'
        land=Image.open('rg-work/'+img).size[0]>1000
        c={"gempId":gid,"id":150000+n*2+(1 if sid=='15o' else 0),"legacy":False,"set":sid,"side":F.get('side'),"front":f,
           "printings":[{"set":sid}],"rarity":"","wide":land,
           "source_page":page,"source_image":F.get('image')}
        cards.append(c)
json.dump({"generated":"2026-11-05","source":"wiki.swccg.com Reflections Gold card pages (Remastered: set 15 = GEMP 15_N; original playtest: 15_No, set 15o)","cards":cards},open(sys.argv[1],'w'),indent=1,ensure_ascii=False)
import collections; print(len(cards), collections.Counter((c['set'],c['front']['type']) for c in cards))
