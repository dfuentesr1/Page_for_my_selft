# Caras nuevas: ojos abiertos (las pupilas se dibujan en el juego) y boca cerrada
from PIL import Image,ImageDraw
import numpy as np
SRC='/home/user/Page_for_my_selft/assets/hermanos/';OUT=SRC+'rig/'
SK=(248,214,182,255);INK=(30,18,14,255);WH=(250,246,236,255)
K=4
import cv2
ERASE={'bufon_frente':[(132,150,13,9),(184,150,15,9)],'bufon_der':[(211,147,13,9)]}
DARKBOX={'bufon_frente':((119,138,209,162),[(165,158,16)]),'bufon_der':((192,136,225,158),[])}
def edit(name,box,fn):
  im=Image.open(SRC+name+'.png').convert('RGBA')
  if name in ERASE:  # borra los ojos cerrados y las pestañas y rellena con la piel de alrededor
    a=np.array(im);m=np.zeros(a.shape[:2],np.uint8)
    for cx,cy,rx,ry in ERASE[name]:cv2.ellipse(m,(cx,cy),(rx,ry),0,0,360,255,-1)
    if name in DARKBOX:  # restos oscuros de pestañas y párpados cerrados
      lum=a[...,:3].astype(int).sum(2);x0,y0,x1,y1=DARKBOX[name][0];dk=np.zeros_like(m)
      dk[y0:y1,x0:x1]=(lum[y0:y1,x0:x1]<420).astype(np.uint8)*255
      for cx,cy,r in DARKBOX[name][1]:cv2.circle(dk,(cx,cy),r,0,-1)
      m=np.maximum(m,cv2.dilate(dk,np.ones((5,5),np.uint8)))
    bgr=cv2.cvtColor(a[...,:3],cv2.COLOR_RGB2BGR);a[...,:3]=cv2.cvtColor(cv2.inpaint(bgr,m,6,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB);im=Image.fromarray(a)
  x0,y0,x1,y1=box;cr=im.crop(box).resize(((x1-x0)*K,(y1-y0)*K),Image.LANCZOS)
  d=ImageDraw.Draw(cr);mk=Image.new('L',cr.size,0);er=Image.new('L',cr.size,0);global MD,ED;MD=ImageDraw.Draw(mk);ED=ImageDraw.Draw(er)
  P=lambda x,y:((x-x0)*K,(y-y0)*K)
  fn(d,P,cr)
  cr=cr.resize((x1-x0,y1-y0),Image.LANCZOS);mk=np.array(mk.resize((x1-x0,y1-y0),Image.LANCZOS))>100;er=np.array(er.resize((x1-x0,y1-y0),Image.LANCZOS)).astype(float)/255
  a=np.array(im);c=np.array(cr).astype(float)
  # grano de pintura para que el parche no quede plano
  rng=np.random.default_rng(3);n=rng.normal(0,5,c.shape[:2]);
  n=cv2.GaussianBlur(n,(0,0),1.2)*1.6
  orig=a[y0:y1,x0:x1].astype(float);chg=((np.abs(c[...,:3]-orig[...,:3]).sum(2)>12)&(orig[...,3]>200))|mk
  for k in range(3):c[...,k]=np.where(chg,c[...,k]+n,c[...,k])
  c=np.clip(c,0,255).astype(np.uint8)
  c[...,3]=(np.maximum(a[y0:y1,x0:x1,3],np.where(chg,255,0))*(1-er)).astype(np.uint8);a[y0:y1,x0:x1]=c
  Image.fromarray(a).save(OUT+'src_'+name+'.png')
def ell(d,P,cx,cy,rx,ry,fill,out=None,w=0):
  (a,b),(c,e)=P(cx-rx,cy-ry),P(cx+rx,cy+ry);d.ellipse([a,b,c,e],fill=fill,outline=out,width=int(w*K))
def curve(d,P,pts,w):
  q=[P(*p) for p in pts];d.line(q,fill=INK,width=int(w*K),joint='curve')
  for p in (q[0],q[-1]):r=w*K/2;d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=INK)
def bez(p0,p1,p2,n=16):return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in [i/n for i in range(n+1)]]
import math
def cartoonEye(d,P,cx,cy,rx,ry,side):
  ell(d,P,cx,cy,rx,ry,WH,INK,1.8)
  lid=[(cx+rx*math.cos(a),cy+ry*math.sin(a)) for a in [math.pi*(1+i/20) for i in range(21)]]
  curve(d,P,lid,3)                                     # párpado de tinta
  ox=cx+side*rx*.92;oy=cy-ry*.55                         # pestañas en el rabillo exterior
  for k in range(2):curve(d,P,bez((ox-side*k*3,oy-k*2.5),(ox+side*(4-k),oy-5-k*2),(ox+side*(6-k*1.5),oy-4-k*3)),1.6)
def front(d,P,cr):
  ell(d,P,166,193,41,31,SK)
  ell(d,P,136,176,11,6,(238,160,130,255));ell(d,P,197,176,11,6,(238,160,130,255))  # coloretes
  curve(d,P,bez((148,189),(167,203),(186,189)),3)          # sonrisa cerrada
  curve(d,P,bez((144,186),(146,190),(149,191)),2);curve(d,P,bez((189,186),(187,190),(184,191)),2)
  cartoonEye(d,P,131,149,9.5,13,-1);cartoonEye(d,P,181,149,9.5,13,1)
def side(d,P,cr):
  prof=bez((245,160),(257,188),(246,212))+bez((246,212),(236,222),(222,217))[1:]
  poly=[P(*p) for p in [(206,160),(238,153)]+prof+[(212,198),(207,176)]]
  ED.polygon([P(*p) for p in [p for p in prof if p[1]>=167]+[(270,224),(270,167)]],fill=255)
  d.polygon(poly,fill=SK);MD.polygon(poly,fill=255)
  curve(d,P,prof,3.4)           # perfil del mentón
  curve(d,P,bez((224,171),(236,180),(247,172)),3)           # sonrisa
  ell(d,P,224,178,8,5,(238,160,130,255))
  cartoonEye(d,P,212,147,7.5,12.5,-1)
edit('bufon_frente',(100,110,225,235),front)
edit('bufon_der',(180,110,280,230),side)
# punk: el ojo abierto queda en blanco, la pupila la pone el juego
im=Image.open(SRC+'punk_quieto.png').convert('RGBA');a=np.array(im).astype(int)
for y in range(146,172):
  for x in range(238,268):
    if ((x-253)/10.5)**2+((y-159)/7.5)**2<1 and a[y,x,:3].sum()<330:a[y,x,:3]=[245,242,232]
Image.fromarray(a.astype(np.uint8)).save(OUT+'src_punk_quieto.png')
for n in ['bufon_espalda']:Image.open(SRC+n+'.png').save(OUT+'src_'+n+'.png')
