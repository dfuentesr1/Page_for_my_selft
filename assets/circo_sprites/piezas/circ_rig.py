# Corta los personajes del circo en piezas para animarlos sin cambiar de dibujo
import cv2, numpy as np, json
from PIL import Image
SP='/tmp/claude-0/-home-user-Page-for-my-selft/b51c4c19-d7d6-586c-a09e-23edd5c32867/scratchpad/circ/'
OUT='/home/user/Page_for_my_selft/assets/circo_sprites/piezas/'
import os;os.makedirs(OUT,exist_ok=True)
def circle(cx,cy,r,n=40):import math;return [(cx+r*math.cos(i/n*6.283),cy+r*math.sin(i/n*6.283)) for i in range(n)]
V={
 'jefe':('an_jefe_escribe_0',[
   {'n':'cabeza','poly':[(72,30),(170,28),(178,80),(165,118),(140,126),(100,126),(80,115),(70,80)],'pv':(120,124),'fill':lambda x,y:True},
   {'n':'mano','poly':[(4,92),(40,98),(72,138),(92,148),(95,192),(50,195),(20,172),(12,140)],'pv':(60,182),'fill':lambda x,y:x>=34}]),
 'mono':('an_mono_0',[
   {'n':'cabeza','poly':[(8,8),(86,4),(94,40),(86,62),(72,74),(34,76),(10,60)],'pv':(52,72),'fill':lambda x,y:y>52},
   {'n':'brazoI','poly':[(38,72),(62,70),(70,96),(60,106),(40,106),(34,90)],'pv':(46,74),'fill':lambda x,y:True},
   {'n':'brazoD','poly':[(66,58),(84,52),(110,50),(118,60),(114,82),(100,88),(80,84),(68,80)],'pv':(72,72),'fill':lambda x,y:x<80}]),
 'elefante':('an_elefante_0',[
   {'n':'bola','poly':[(x,max(y,129)) for x,y in circle(75,157,39)],'pv':(75,157),'fill':None},
   {'n':'trompa','poly':[(120,46),(140,27),(150,21),(166,25),(169,40),(158,46),(150,60),(143,80),(124,80)],'pv':(128,72),'fill':lambda x,y:x<136}]),
}
meta={}
for name,(src,parts) in V.items():
  im=np.array(Image.open(SP+src+'.png').convert('RGBA'));H,W=im.shape[:2]
  if name=='elefante':im[150:,:42,3]=0   # rayitas de movimiento de la bola
  base=im.copy();out=[]
  for p in parts:
    m=np.zeros((H,W),np.uint8);cv2.fillPoly(m,[np.array(p['poly'],np.int32)],255);inside=m>0
    layer=im.copy();layer[...,3]=np.where(inside,im[...,3],0)
    if p['fill']:
      fm=np.zeros_like(inside)
      for y,x in zip(*np.nonzero(inside)):fm[y,x]=p['fill'](x,y)
      rgb=cv2.cvtColor(base[...,:3],cv2.COLOR_RGB2BGR);unk=((inside)|(base[...,3]<128)).astype(np.uint8)*255
      inp=cv2.cvtColor(cv2.inpaint(rgb,unk,5,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
      base[fm,:3]=inp[fm];base[...,3]=np.where(inside,np.where(fm,255,0),base[...,3])
    else:base[...,3]=np.where(inside,0,base[...,3])
    ys,xs=np.nonzero(layer[...,3]>0);x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
    Image.fromarray(layer[y0:y1,x0:x1]).save(OUT+f'{name}_{p["n"]}.png')
    out.append({'n':p['n'],'x':int(x0),'y':int(y0),'px':p['pv'][0],'py':p['pv'][1]})
  Image.fromarray(base).save(OUT+f'{name}_cuerpo.png')
  meta[name]={'w':W,'h':H,'parts':out}
for k in ['cut_forzudo','an_tigre_0']:Image.open(SP+k+'.png').save(OUT+{'cut_forzudo':'forzudo','an_tigre_0':'tigre'}[k]+'_cuerpo.png')
json.dump(meta,open(OUT+'piezas.json','w'),indent=1);print(json.dumps(meta,separators=(',',':')))
