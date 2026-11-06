import json,sys,time
from pathlib import Path
import numpy as np, onnxruntime as ort
from PIL import Image
L=Path(sys.argv[1]); (L/'x4').mkdir(exist_ok=True)
so=ort.SessionOptions(); so.intra_op_num_threads=2
sess=ort.InferenceSession('/tmp/claude-0/models/x4plus128.onnx',so)
man=json.load(open(L/'manifest.json'))
todo=[g for g,e in man.items() if e['status']=='ok' and not (L/'x4'/f'{g}.webp').exists()]
if len(sys.argv)>2: todo=todo[:int(sys.argv[2])]
print(len(todo),'to do',flush=True)
for i,g in enumerate(todo):
    t0=time.time(); im=Image.open(L/'orig'/f'{g}.png'); alpha=im.split()[3] if im.mode=='RGBA' else None
    a=np.array(im.convert('RGB')).astype(np.float32)/255
    T,pad=128,12; step=T-2*pad; H,W=a.shape[:2]; outp=np.zeros((H*4,W*4,3),np.float32)
    for y in range(0,H,step):
        for x in range(0,W,step):
            y0=max(min(y-pad,H-T),0); x0=max(min(x-pad,W-T),0)
            tile=np.zeros((T,T,3),np.float32); sub=a[y0:y0+T,x0:x0+T]; tile[:sub.shape[0],:sub.shape[1]]=sub
            r=sess.run(None,{'image':tile.transpose(2,0,1)[None]})[0][0].transpose(1,2,0)
            ye,xe=min(y+step,H),min(x+step,W)
            outp[y*4:ye*4,x*4:xe*4]=r[(y-y0)*4:(ye-y0)*4,(x-x0)*4:(xe-x0)*4]
    o=Image.fromarray((np.clip(outp,0,1)*255).round().astype(np.uint8))
    if alpha is not None: o=o.convert('RGBA'); o.putalpha(alpha.resize(o.size,Image.LANCZOS))
    o.save(L/'x4'/f'{g}.webp',quality=92,method=6)
    print(i+1,g,round(time.time()-t0,1),flush=True)
