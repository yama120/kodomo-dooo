import sys,json
from PIL import Image
base=sys.argv[1]; dpr=float(sys.argv[2]); vh=int(sys.argv[3])
parts=json.load(open(base+'.json'))
ims=[Image.open(base.replace('.png','')+f'_part{i}.png') for i in range(len(parts))]
w=ims[0].width; H=int((parts[-1]['y']+vh)*dpr)
out=Image.new('RGB',(w,H),'white')
for p,im in zip(parts,ims): out.paste(im,(0,int(p['y']*dpr)))
out.save(base); print('stitched',out.size)
