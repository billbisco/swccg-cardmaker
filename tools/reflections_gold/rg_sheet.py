from PIL import Image,ImageDraw
import json,math,sys
L=sys.argv[1]; man=json.load(open(L+'/manifest.json')); g=[k for k in man if man[k].get('status')=='ok']
for s in range(math.ceil(len(g)/48)):
    sh=Image.new('RGB',(8*220,6*190),'white'); d=ImageDraw.Draw(sh)
    for i,k in enumerate(g[s*48:(s+1)*48]):
        im=Image.open(f'{L}/orig/{k}.png')
        if im.mode=='RGBA':
            bg=Image.new('RGB',im.size,(255,0,255)); bg.paste(im,mask=im.split()[3])
        else: bg=im.convert('RGB')
        bg.thumbnail((210,160)); x=(i%8)*220+5; y=(i//8)*190+5; sh.paste(bg,(x,y)); d.text((x,y+165),f"{k} {man[k]['title'][:26]}",fill='black')
    sh.save(f'{L}/sheet-{s+1}.png')
