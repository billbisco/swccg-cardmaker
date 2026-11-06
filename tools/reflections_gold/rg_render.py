import json,sys,urllib.request
API='http://localhost:8790/api'
def card(g): return json.load(urllib.request.urlopen(f'{API}/card/{g}',timeout=120))
def render(spec,out,size='holotable'):
    r=urllib.request.Request(f'{API}/render',data=json.dumps({"spec":spec,"size":size,"format":"png"}).encode(),headers={"Content-Type":"application/json"})
    open(out,'wb').write(urllib.request.urlopen(r,timeout=300).read())
for g in sys.argv[1:]:
    d=card(g); 
    try: render(d['spec'],f'rg-work/render/{g}.png'); print(g,'ok',d['spec'].get('wide'),d['spec'].get('expansion'))
    except Exception as e: print(g,'ERR',e, e.read()[:500] if hasattr(e,'read') else '')
