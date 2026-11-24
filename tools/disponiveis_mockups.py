# Cartões dos disponíveis que já vêm num manequim: no site (grade e zoom) aparece o mockup, não só a arte.
# O fundo vira branco, então no cartão de papel (mix-blend multiply) o manequim fica no mesmo papel dos outros.
# O provador continua usando a arte limpa. Rodar da raiz do site: python tools/disponiveis_mockups.py
import json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

D = "assets/brand/disponiveis-originais"
OUT = "assets/img/disponiveis"
folha = lambda n: Image.open(f"{D}/folha-{n:02d}" + (".png" if n == 11 else ".jpeg")).convert("RGB")

# id: (folha, caixa)
CORTES = {
    "peitoral-tribal": (11, (0, 52, 474, 693)),
    "tribal-quadril": (8, (60, 200, 1270, 2580)),
    "tribal-perna": (8, (1240, 0, 2160, 2700)),
    "pernas-tribais": (9, (40, 0, 660, 1850)),
    "tribal-costela": (9, (630, 40, 1350, 1850)),
}


def branco(im, limiar=242):
    """papel quase branco vira branco puro (o multiply do cartão não deixa véu cinza)"""
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(2)
    k = np.clip((lum - limiar) / (255 - limiar), 0, 1)[..., None]
    return Image.fromarray((a * (1 - k) + 255 * k).clip(0, 255).astype(np.uint8))


def manequim_da_porta():
    """folha 10: o manequim sai da porta escura e vai para o branco"""
    X0, Y0, X1, Y1 = 740, 100, 1120, 1500
    a = np.asarray(folha(10))[Y0:Y1, X0:X1].astype(np.float32)
    lum = a @ np.array([.299, .587, .114])
    tinta = np.zeros(lum.shape, bool)
    from skimage.morphology import disk
    # a mesma separação tinta x fundo do disponiveis_conjuntos.py (refeita aqui de forma simples: a tinta fica dentro do corpo)
    claro = lum > 150
    corpo = nd.binary_closing(claro, structure=disk(9))
    lab, n = nd.label(corpo)
    corpo = lab == 1 + int(np.argmax(nd.sum(corpo, lab, range(1, n + 1))))
    # buracos pequenos (tinta) entram; o vão entre braço e cintura (grande) fica fora
    buracos = nd.binary_fill_holes(corpo) & ~corpo
    lb, nb = nd.label(buracos)
    for k in range(1, nb + 1):
        if (lb == k).sum() < 2600:
            corpo |= lb == k
    corpo = nd.binary_opening(corpo, structure=disk(1))
    # pés: abaixo do tornozelo só fica o que é pele clara (a calçada cinza sai)
    yy = np.mgrid[0:corpo.shape[0], 0:corpo.shape[1]][0]
    corpo &= ~((yy > 1215) & (lum < 175) & (lum > 70))   # a tinta (bem escura) fica
    corpo[1175:1255, 242:280] &= lum[1175:1255, 242:280] > 70   # vão escuro entre as canelas cruzadas
    lab, n = nd.label(corpo)
    corpo = np.isin(lab, 1 + np.nonzero(nd.sum(corpo, lab, range(1, n + 1)) > 400)[0])
    m = Image.fromarray((corpo * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8))
    al = np.asarray(m).astype(np.float32)[..., None] / 255
    out = a * al + 255 * (1 - al)
    im = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    return im.crop((40, 20, 380, 1395))


L = json.load(open(f"{D}/final/_site.json", encoding="utf8"))
ix = {x["id"]: x for x in L}
ims = {k: branco(folha(n).crop(b)) for k, (n, b) in CORTES.items()}
ims["corpo-inteiro"] = manequim_da_porta()
for pid, im in ims.items():
    k = 1600 / max(im.size)
    im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS).save(f"{OUT}/{pid}.webp", quality=90, method=6)
    k = 640 / max(im.size)
    p = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    p.save(f"{OUT}/{pid}-p.webp", quality=88, method=6)
    ix[pid].update(w=p.width, h=p.height, mockup=True)
    print(pid, im.size)
json.dump(L, open(f"{D}/final/_site.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
