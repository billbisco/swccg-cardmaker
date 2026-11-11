import json,sys,os,re
R=os.path.abspath('swccg-cardmaker');sys.path.insert(0,R);sys.path.insert(0,R+'/webapp');os.chdir(R)
import server,adapter,build_vs
out={}
for gid,c in server.CARDS.items():
    if not c.get('legacy'): continue
    spec=adapter.gemp_to_spec(c)
    s=dict(spec,_art=None,_art_kind=None,_set_icon_file=None)
    try: card=adapter.spec_to_card(s,build_vs); tpl=card['template']
    except Exception as e: tpl='ERR '+str(e)
    out[gid]=dict(title=spec.get('title'),caption=spec.get('caption'),legacy_title=c['front']['title'],template=tpl,side=spec.get('side'),set=c.get('set'),game_text=spec.get('game_text'),lore=spec.get('lore'),gemp=[k for k,v in server.LEGACY_ALIAS.items() if v==gid][:3])
json.dump(out,open('../legacy_index.json','w'),indent=0)
print(len(out))
