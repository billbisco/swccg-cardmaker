import json, io, urllib.request, concurrent.futures as cf, os
from PIL import Image
rows=[r for r in json.load(open('cards.json')) if r['type']!='Location']
def get(r):
    out=f"crops/{r['key']}.png"
    if os.path.exists(out): return 'have'
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(r['url'],timeout=40).read())).convert('RGB')
        if im.size!=(745,1039): return f"size {im.size}"
        im.crop((0,0,745,170)).save(out); return 'ok'
    except Exception as e: return f'err {e}'
res=list(cf.ThreadPoolExecutor(16).map(get,rows))
import collections; print(collections.Counter(x.split(' ')[0] for x in res)); print([x for x in res if not x in ('ok','have')][:5])
