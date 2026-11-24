# Separa os disponiveis do Maronez das folhas: caixas em coordenadas 1600x2000 (folhas 1-7) ou nativas (8-11).
import json,sys,os
import numpy as np
from PIL import Image
from scipy import ndimage as nd
D=sys.argv[1]; OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
P=[ # folha, id, nome, caixa, colorido
 (1,'dedo-do-meio','Dedo do meio',(140,100,830,1110),1),
 (1,'sorriso-de-serra','Sorriso de serra',(730,80,1500,1010),1),
 (1,'mijando-na-bandeira','Mijando na bandeira',(190,1120,760,1930),1),
 (1,'chapado','Chapado',(860,1030,1515,1950),1),
 (2,'yo-dont-do-drugs','Yo dont do drugs',(60,110,1120,1250),1),
 (2,'gato-dj','Gato DJ',(520,950,1470,1995),0),
 (3,'penis','Penis™',(25,90,765,660),0),
 (3,'made-in-japan','Made in Japan',(770,30,1560,800),1,'zumbi'),
 (3,'polo-gang','Polo gang',(0,700,1600,1610),0,'polo'),
 (3,'fodase','Fodase',(0,1540,1600,1705),1),
 (3,'gato-deitado','Gato deitado',(0,1705,1600,2000),0),
 (4,'soundcloud','SoundCloud',(45,140,665,1070),0),
 (4,'canivete','Canivete',(505,50,1560,180),0),
 (4,'obrigado','Obrigado por mudar minha vida',(655,320,1065,830),0),
 (4,'ps2','PS2',(835,250,1560,1150),0),
 (4,'capuz','Capuz',(55,1090,475,1995),0),
 (4,'mad','MAD',(465,1140,935,1995),0),
 (4,'pastelina','Pastelina',(915,1110,1590,1995),1),
 (5,'mapa','Mapa',(35,30,705,670),0),
 (5,'please-be-patient','Please be patient',(715,20,1545,305),1),
 (5,'problem','Problem',(705,370,1545,660),1),
 (5,'tribal-monstro','Tribal monstro',(35,670,765,1995),1),
 (5,'shh','Shh...',(735,655,1585,1405),1),
 (5,'better-call-saul','Better call Saul',(775,1405,1565,1965),0),
 (6,'capivara','Capivara armada',(25,50,725,1045),0),
 (6,'stella','Stella',(725,230,1585,1065),0),
 (6,'gato-pensando','Gato pensando',(155,1000,1535,1995),0),
 (7,'leon','Leon',(45,80,475,1160),0),
 (7,'npc','NPC',(475,85,925,565),0),
 (7,'perfil-tribal','Perfil tribal',(965,70,1585,705),0),
 (7,'i-love-beijar-djs','I ♥ beijar DJs',(525,490,1245,995),1),
 (7,'carrot-cobain','Carrot Cobain',(0,1150,445,2000),0),
 (7,'coringa','Coringa e porco',(385,990,1095,2000),0),
 (7,'ponei','Pônei',(1055,840,1600,1430),0),
 (7,'calcinha-preta','Calcinha Preta',(975,1440,1590,2000),0),

 (8,'tribal-quadril','Tribal do quadril',(160,1040,570,1545),1,'mock'),
 (8,'tribal-perna','Tribal da perna',(935,620,1495,1790),0,'mock-linha'),
 (9,'tribal-coxa','Tribal da coxa',(95,495,310,935),0,'mock'),
 (9,'tribal-canela','Tribal da canela',(120,945,345,1528),0,'mock'),
 (9,'tribal-perna-longa','Tribal perna longa',(330,495,545,1518),0,'mock'),
 (9,'tribal-costela','Tribal da costela',(690,535,1170,1760),0,'mock'),   # vai até o meio da coxa
 (11,'peitoral-tribal','Peitoral tribal (par)',(55,195,425,445),0,'mock'),
]
def folha(n):
    f=[x for x in os.listdir(D) if x.startswith('folha-%02d'%n)][0]
    return np.asarray(Image.open(os.path.join(D,f)).convert('RGB'))
cache={}
lista=[]
claim={}
SO=set(sys.argv[3].split(',')) if len(sys.argv)>3 else None   # refaz só esses ids
for item in P:
    if SO and item[1] not in SO: continue
    n,i,nome,b,col=item[:5]; modo=item[5] if len(item)>5 else ''
    if modo.startswith('mock'):
        a=folha(n); nat=n in (9,10,11)
        s=1 if nat else a.shape[1]/1600
        x0,y0,x1,y1=[int(v*s) for v in b]
        c=a[y0:y1,x0:x1].astype(int)
        lum=c@np.array([.299,.587,.114])
        red=(c[...,0]>110)&(c[...,0]-c[...,1]>60)
        m=(lum<95)|(red if col else False)
        if modo=='mock-linha':
            op=nd.binary_opening(m,iterations=4); m=m&nd.binary_dilation(op,iterations=6)
        lab,_=nd.label(m,structure=np.ones((3,3))); sz=nd.sum(m,lab,range(1,lab.max()+1))
        borda=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
        maior=1+int(np.argmax(sz))
        ok=[k+1 for k in range(len(sz)) if sz[k]>40 and (k+1==maior or k+1 not in borda)]
        m=np.isin(lab,ok)
        out=np.full(c.shape,255,np.uint8); out[m]=np.clip(c[m],0,255)
        if not col: out[m]=0
        ys,xs=np.nonzero(m); out=out[ys.min():ys.max()+1,xs.min():xs.max()+1]
        pad=int(max(out.shape[:2])*.04); out=np.pad(out,((pad,pad),(pad,pad),(0,0)),constant_values=255)
        im=Image.fromarray(out)
        if max(im.size)<1000: im=im.resize((im.width*1000//max(im.size),im.height*1000//max(im.size)),Image.LANCZOS)
        im.save(f'{OUT}/{i}.png'); lista.append(dict(id=i,nome=nome,folha=n,colorido=bool(col))); continue
    if n not in cache:
        a=folha(n); ai=a.astype(int)
        ink=(ai.min(2)<215)|((ai.max(2)-ai.min(2))>50)
        lab,_=nd.label(nd.binary_dilation(ink,iterations=3))
        cache[n]=(a,ink,lab,nd.center_of_mass(ink,lab,range(1,lab.max()+1)))
    a,ink,lab,cm=cache[n]
    s=a.shape[1]/1600
    x0,y0,x1,y1=[int(v*s) for v in b]
    cl=claim.setdefault(n,set())
    keep=np.zeros(lab.max()+1,bool)
    for k,(cy,cx) in enumerate(cm,1):
        if x0<=cx<x1 and y0<=cy<y1 and k not in cl: keep[k]=True; cl.add(k)
    m=keep[lab]
    if modo in('zumbi','polo'):
        H,W=lab.shape; yy,xx=np.mgrid[0:H,0:W]
        lim=np.where(xx<1500,1000,np.where(xx<1775,1049,1017))
        z=ink&(yy<lim)&(xx>=int(770*s))
        if modo=='zumbi': m=z
        else: m=ink&~z&(yy>=int(700*s))&(yy<int(1610*s))&(keep[lab]|(yy<int(800*s)))
        m[:y0]=0;m[y1:]=0;m[:,:x0]=0;m[:,x1:]=0
        from skimage.morphology import convex_hull_image,disk
        R=(slice(960,1160),slice(1650,2000))       # zona onde o pe do zumbi encosta na cabeca
        sub=m[R].copy()
        if modo=='zumbi':
            sub=nd.binary_opening(sub,structure=disk(9))|(sub&(np.mgrid[0:200,0:350][0]<40))
        else:
            lab2,n2=nd.label(sub); sz=nd.sum(sub,lab2,range(1,n2+1))
            sub=lab2==(1+np.argmax(sz))            # so a cabeca, sem lasca do pe
            sub=nd.binary_opening(sub,structure=disk(4))
            hull=convex_hull_image(sub)
            buraco=nd.binary_fill_holes(sub)&~sub
            yy2=np.mgrid[0:200,0:350][0]
            topo=np.nonzero(sub.any(1))[0][0]
            sub=sub|(hull&~buraco&(yy2<topo+70))
        m[R]=sub
        lab3,n3=nd.label(m); sz3=nd.sum(m,lab3,range(1,n3+1))
        m=np.isin(lab3,1+np.nonzero(sz3>=150)[0])
    if modo=='corta': m=keep[lab]|(lab>0)&False
    m[:y0]=0;m[y1:]=0;m[:,:x0]=0;m[:,x1:]=0
    ys,xs=np.nonzero(m&ink)
    yy0,yy1,xx0,xx1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    c=a[yy0:yy1,xx0:xx1].copy(); c[~m[yy0:yy1,xx0:xx1]]=255
    pad=int(max(c.shape[:2])*.04)
    c=np.pad(c,((pad,pad),(pad,pad),(0,0)),constant_values=255)
    Image.fromarray(c).save(f'{OUT}/{i}.png')
    lista.append(dict(id=i,nome=nome,folha=n,colorido=bool(col)))
json.dump(lista,open(OUT+('/_lista_so.json' if SO else '/_lista.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
print(len(lista))
