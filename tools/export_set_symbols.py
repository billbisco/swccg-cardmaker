"""Export existing CardMaker sphere masters; no redraw, background inference or palette change.

Run from a CardMaker checkout, or pass --root. Wiki images are lossless WebP
encodings of a deterministic96px display derivative. The PNG masters remain
authoritative and unmodified. Do not use an era/style label to infer AI rings.
"""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
def digest(data):return hashlib.sha256(data).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--output',type=Path);parser.add_argument('--source-commit');args=parser.parse_args()
    root=args.root;out=args.output or root/'assets/symbols';out.mkdir(parents=True,exist_ok=True)
    commit=args.source_commit
    if not commit:
        top=Path(subprocess.check_output(['git','-C',str(root),'rev-parse','--show-toplevel']).decode().strip())
        if top.resolve()!=root.resolve():parser.error('--source-commit is required outside the CardMaker checkout root')
        commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD']).decode().strip()
    if not re.fullmatch('[0-9a-f]{40}',commit):parser.error('--source-commit must be a full lowercase Git commit')
    names={'anh':'A New Hope','hoth':'Hoth','dagobah':'Dagobah','cloudcity':'Cloud City','jabbaspalace':"Jabba’s Palace",'se':'Special Edition','endor':'Endor','ds2':'Death Star II','premium':'Premium','reflections2':'Reflections II','reflections3':'Reflections III','tatooine':'Tatooine','coruscant':'Coruscant','theed':'Theed Palace','ejp':"Enhanced Jabba’s Palace",'reflections-gold':'Reflections Gold'}
    rows=[]
    for key,label in names.items():
        for style in ['decipher','pc']:
            src=root/'assets/icons'/f'set-{key}-{style}.png'
            if not src.exists():continue
            original=src.read_bytes();im=Image.open(src).convert('RGBA');assert all(im.getpixel(x)[3]==0 for x in [(0,0),(0,im.height-1),(im.width-1,0),(im.width-1,im.height-1)]),src
            display=im.resize((96,96),Image.Resampling.LANCZOS);dest=out/f'set-{key}-{style}.webp';display.save(dest,'WEBP',lossless=True,exact=True,method=6)
            decoded=Image.open(dest).convert('RGBA');assert decoded.tobytes()==display.tobytes(),dest
            assert decoded.getextrema()[3][0]==0 and decoded.getextrema()[3][1]==255
            rows.append(dict(key=key,label=label,style=style,source=src.relative_to(root).as_posix(),source_sha256=digest(original),source_dimensions=list(im.size),source_bytes=len(original),file=dest.name,sha256=digest(dest.read_bytes()),bytes=dest.stat().st_size,dimensions=[96,96],true_alpha=True,lossless_webp_round_trip=True,source_unchanged=src.read_bytes()==original,presentation='inner sphere; apply the existing CardMaker inline black-ring recipe when that printed variant requires it',printing_status='ring variant requires physical-card verification; do not use for regular Coruscant by default' if key=='coruscant' else 'reuse subject to per-printing verification; style is not a set-identity or AI-ring override'))
    manifest=dict(schema_version=1,master_repository='https://github.com/billbisco/swccg-cardmaker',master_commit=commit,master_policy='Existing CardMaker PNG masters and current superseding provenance remain authoritative. WebP files are reproducible display derivatives; do not maintain separate wiki artwork.',ring_recipe=dict(source='render.py DC_SPHERE_CSS',inner_height=42,black_ring_width=4,black_ring_color='#111',note='This completes the inline symbol, not the card frame. Preserve verified silver/gold/AI ring variants separately.'),symbols=rows)
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(len(rows),'transparent96px WebP exports; source PNGs unchanged; lossless derivative round trips verified;',sum(x['bytes'] for x in rows),'total bytes')
if __name__=='__main__':main()
