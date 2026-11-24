# Acabamento final: separa as cores (preto, vermelho, magenta), alisa as bordas com supersample 2x,
# tira pontinhos de JPEG e furinhos, e grava PNG em fundo branco + PNG transparente.
import sys,os,json
import numpy as np
from PIL import Image
from scipy import ndimage as nd
SRC,OUT=sys.argv[1],sys.argv[2]; os.makedirs(OUT,exist_ok=True)
LADO=2400
L=json.load(open(SRC+'/_lista.json',encoding='utf8'))
def area_min(m,a):
    lab,n=nd.label(m); 
    if n==0: return m
    sz=nd.sum(m,lab,range(1,n+1)); return np.isin(lab,1+np.nonzero(sz>=a)[0])
for p in L:
    a=np.asarray(Image.open(f"{SRC}/{p['id']}.png").convert('RGB')).astype(np.float32)
    h,w=a.shape[:2]; k=LADO/max(h,w)            # escala final
    lum=a@np.array([.299,.587,.114],np.float32); sat=a.max(2)-a.min(2)
    cor=np.clip((sat-35)/80,0,1)
    preto=np.clip((205-lum)/140,0,1)*(1-cor)
    mag=(a[...,2]>a[...,1]+60)&(sat>60)
    camadas={'preto':preto}
    if p['colorido']:
        camadas['vermelho']=cor*(~mag)
        if mag.any(): camadas['magenta']=cor*mag
    ref={'preto':np.array([8,8,8])}
    for c in ('vermelho','magenta'):
        if c in camadas:
            sel=(camadas[c]>.8)
            ref[c]=np.median(a[sel],0) if sel.sum()>50 else np.array([170,0,10])
    W2,H2=int(w*k*2),int(h*k*2)
    sig=max(.6,1.1*k)          # alisa o serrilhado do original (em px da escala 2x)
    fim={}
    for c,m in camadas.items():
        up=np.asarray(Image.fromarray((m*255).astype(np.uint8)).resize((W2,H2),Image.BICUBIC),np.float32)/255
        up=nd.gaussian_filter(up,sig)
        b=up>(.36 if p['id']=='yo-dont-do-drugs' else .5)
        amin=((2 if p['id']=='yo-dont-do-drugs' else 6)*k*2)**2*.5     # pontinho de JPEG: < ~4 px no original
        b=area_min(b,amin); b=~area_min(~b,amin)   # tira pontos e fecha furinhos
        fim[c]=b
    # pontinhos soltos longe do desenho (sujeira do JPEG/recorte) somem
    uni=np.zeros((H2,W2),bool)
    for m in fim.values(): uni|=m
    lab,n=nd.label(uni,structure=np.ones((3,3)))
    if n>1 and p['id'] in ('yo-dont-do-drugs','coringa','peitoral-tribal'):
        sz=nd.sum(uni,lab,range(1,n+1)); px=(k*2)**2
        grande=np.isin(lab,1+np.nonzero(sz>=1500*px)[0])
        perto=nd.binary_dilation(grande[::4,::4],iterations=max(1,int(60*k*2/4)))
        perto=np.kron(perto,np.ones((4,4),bool))[:H2,:W2]
        pequenos=1+np.nonzero(sz<1500*px)[0]
        toca=np.zeros(n+1,bool); toca[np.unique(lab[perto&uni])]=True
        fora=np.isin(lab,[q for q in pequenos if not toca[q]])
        if p['id']=='yo-dont-do-drugs':   # o texto fino e solto fica; so a sujeira de baixo sai
            fora[:int(H2*.62)]=False; fora[:,:int(W2*.7)]=False
        for c in fim: fim[c]=fim[c]&~fora
    # ordem: cor por cima do preto (o vermelho foi pintado por cima no desenho)
    alfa2=np.zeros((H2,W2),np.float32); rgb2=np.zeros((H2,W2,3),np.float32)
    for c in ['preto','vermelho','magenta']:
        if c in fim:
            m=fim[c]; rgb2[m]=ref[c]; alfa2=np.maximum(alfa2,m)
    # supersample 2x -> 1x (borda antisserrilhada)
    al=alfa2.reshape(H2//2,2,W2//2,2).mean((1,3)) if H2%2==0 and W2%2==0 else None
    rgb2=rgb2[:H2//2*2,:W2//2*2]; alfa2=alfa2[:H2//2*2,:W2//2*2]
    al=alfa2.reshape(H2//2,2,W2//2,2).mean((1,3))
    pm=(rgb2*alfa2[...,None]).reshape(H2//2,2,W2//2,2,3).sum((1,3))
    rgb=np.where(al[...,None]>0,pm/np.maximum(al[...,None]*4,1e-6),0)
    ys,xs=np.nonzero(al>0); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    al,rgb=al[y0:y1,x0:x1],rgb[y0:y1,x0:x1]
    pad=int(max(al.shape)*.05)
    al=np.pad(al,pad); rgb=np.pad(rgb,((pad,pad),(pad,pad),(0,0)))
    Image.fromarray(np.dstack([rgb.clip(0,255).astype(np.uint8),(al*255).astype(np.uint8)]),'RGBA').save(f"{OUT}/{p['id']}.png",optimize=True)
    branco=rgb*al[...,None]+255*(1-al[...,None])
    Image.fromarray(branco.clip(0,255).astype(np.uint8)).save(f"{OUT}/{p['id']}-branco.png",optimize=True)
    print(p['id'],al.shape,list(fim))
json.dump(L,open(OUT+'/_lista.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
