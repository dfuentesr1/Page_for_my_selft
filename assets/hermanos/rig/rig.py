# Corta las poses de los hermanos en piezas (cuerpo, brazos, piernas) para animarlas por partes.
import cv2, numpy as np, json, os
from PIL import Image
SRC='/home/user/Page_for_my_selft/assets/hermanos/'
OUT=SRC+'rig/'
def mir(poly,W):return [(W-1-x,y) for x,y in poly]
FA=[(84,258),(108,258),(106,300),(104,340),(108,372),(128,378),(130,410),(100,420),(97,470),(95,506),(28,506),(24,420),(32,380),(56,368),(62,320),(72,278)]
BA=[(30,276),(66,282),(68,370),(80,378),(80,412),(64,420),(64,498),(6,498),(2,410),(6,376),(20,364)]
SA=[(160,258),(201,258),(201,380),(212,386),(214,420),(216,470),(208,507),(148,507),(138,450),(134,392),(158,376)]
PA=[(272,246),(302,236),(328,300),(338,410),(345,470),(341,538),(266,538),(258,470),(276,410),(270,330)]
def rect(x0,y0,x1,y1):return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
VIEWS={
 'bufon_frente':{'parts':[
   {'n':'legL','poly':[(110,533),(152,533),(152,712),(0,712),(0,556),(110,556)],'pv':(132,540),'z':-1,'pad':40},
   {'n':'legR','poly':[(152,533),(196,533),(196,556),(301,556),(301,712),(152,712)],'pv':(176,540),'z':-1,'pad':40},
   {'n':'armL','poly':FA,'pv':(88,272),'z':1,'fill':lambda x,y:x>=97},
   {'n':'armR','poly':[(205,262),(240,258),(252,280),(276,370),(298,378),(298,410),(296,496),(232,498),(228,420),(222,408),(220,386),(214,330),(206,290)],'pv':(228,274),'z':1,'fill':lambda x,y:x<=252 if y>=380 else x<=214+(y-290)*.12}]},
 'bufon_espalda':{'parts':[
   {'n':'legL','poly':[(88,546),(136,546),(136,712),(0,712),(0,560),(88,560)],'pv':(112,550),'z':-1,'pad':40},
   {'n':'legR','poly':[(136,546),(186,546),(186,560),(298,560),(298,712),(136,712)],'pv':(160,550),'z':-1,'pad':40},
   {'n':'armL','poly':BA,'pv':(48,290),'z':1,'fill':lambda x,y:x>=63},
   {'n':'armR','poly':[(170,268),(205,262),(222,300),(240,370),(262,374),(264,412),(262,503),(204,503),(204,420),(195,410),(192,380),(186,330),(172,290)],'pv':(190,280),'z':1,'fill':lambda x,y:x<=212 if y>=380 else x<=180+(y-280)*.2}]},
 'bufon_der':{'parts':[
   {'n':'leg','poly':[(140,538),(214,538),(214,600),(285,600),(285,713),(105,713),(105,600),(140,600)],'pv':(172,546),'z':-1,'pad':45},
   {'n':'arm','poly':SA,'pv':(180,276),'z':1,'fill':lambda x,y:True}]},
 'punk_quieto':{'parts':[
   {'n':'legL','poly':[(100,556),(172,556),(172,719),(0,719),(0,600),(100,600)],'pv':(134,560),'z':-1,'pad':40},
   {'n':'legR','poly':[(172,556),(260,556),(260,600),(341,600),(341,719),(172,719)],'pv':(222,560),'z':-1,'pad':40},
   {'n':'arm','poly':PA,'pv':(292,268),'z':-1,'pad':0}]},
}
meta={}
for v,cfg in VIEWS.items():
  im=np.array(Image.open(OUT+'src_'+v+'.png').convert('RGBA'));H,W=im.shape[:2]
  base=im.copy();parts=[]
  for p in cfg['parts']:
    m=np.zeros((H,W),np.uint8);cv2.fillPoly(m,[np.array(p['poly'],np.int32)],255)
    layer=im.copy();layer[...,3]=np.where(m>0,im[...,3],0)
    if p.get('pad'):  # alarga la pieza hacia arriba (queda escondida tras el cuerpo) para que no se vea el corte al girar
      ys=np.where(layer[...,3].max(1)>0)[0];top=ys.min()
      row=layer[top+2].copy();pad=p['pad']
      for k in range(1,pad+3):
        y=top+2-k
        if y<0:break
        layer[y]=np.where(layer[y,:,3:4]>0,layer[y],row)
    # quitar la pieza del cuerpo y rellenar lo que tapaba
    a=base[...,3].copy();inside=m>0
    fillm=np.zeros_like(m)
    if p.get('fill'):
      yy,xx=np.nonzero(inside)
      for y,x in zip(yy,xx):
        if p['fill'](x,y):fillm[y,x]=255
    rgb=cv2.cvtColor(base[...,:3],cv2.COLOR_RGB2BGR)
    unknown=((inside)|(a<128)).astype(np.uint8)*255
    if fillm.any():
      inp=cv2.inpaint(rgb,unknown,9,cv2.INPAINT_TELEA)
      inp=cv2.cvtColor(inp,cv2.COLOR_BGR2RGB)
      sel=fillm>0
      base[sel,:3]=inp[sel];base[...,3]=np.where(inside,np.where(sel,255,0),base[...,3])
    else:
      base[...,3]=np.where(inside,0,base[...,3])
    ys,xs=np.nonzero(layer[...,3]>0);x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
    Image.fromarray(layer[y0:y1,x0:x1]).save(OUT+f'{v}_{p["n"]}.png')
    parts.append({'n':p['n'],'x':int(x0),'y':int(y0),'px':p['pv'][0],'py':p['pv'][1],'z':p['z']})
  # suavizar el borde del relleno con un contorno de tinta donde corresponda: (lo deja la propia pieza)
  Image.fromarray(base).save(OUT+f'{v}_base.png')
  meta[v]={'w':W,'h':H,'parts':parts}
json.dump(meta,open(OUT+'rig.json','w'),indent=1)
print(json.dumps(meta))
