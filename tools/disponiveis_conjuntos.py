# Conjuntos: desenhos que são UMA arte espalhada pelo corpo (vêm dos mockups).
#   pernas-tribais  = tribal-coxa + tribal-canela + tribal-perna-longa (folha 9, pernas)
#   corpo-inteiro   = 7 partes recortadas do manequim da porta (folha 10)
# 1) recorta as partes do manequim (a tinta encosta no fundo escuro da porta: erosão + watershed separam)
# 2) limpa as partes com o mesmo acabamento dos outros (disponiveis_limpa.py)
# 3) monta a imagem única de cada conjunto com as partes limpas no lugar do mockup
# Rodar da raiz do site: python tools/disponiveis_conjuntos.py
import json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from skimage.morphology import disk
from skimage.segmentation import watershed

D = "assets/brand/disponiveis-originais"
REC, FIN = f"{D}/recortes", f"{D}/final"

# ---------- folha 10: manequim na porta ----------
X0, Y0 = 740, 100
a = np.asarray(Image.open(f"{D}/folha-10.jpeg").convert("RGB")).astype(int)
c = a[Y0:1500, X0:1120]; H, W = c.shape[:2]
lum = c @ np.array([.299, .587, .114])
dark = lum < 90
dark[370:620, :38] = False        # ponta do braço encosta no fundo
dark[380:480, :44] = False
dark[850:950, 274:] = False       # ponta da coxa encosta no vão entre as pernas
dark[380:600, 81:83] = False      # meio do braço encosta no vão entre braço e cintura
er = nd.binary_erosion(dark, structure=disk(3), border_value=1)
lab, _ = nd.label(er)
fundo = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
for x, y in [(100, 490)]:         # vão escuro entre o braço e a cintura
    if lab[y, x]: fundo.add(lab[y, x])
mk = np.zeros((H, W), int)
mk[np.isin(lab, list(fundo))] = 1
mk[(lab > 0) & ~np.isin(lab, list(fundo))] = 2
mk[lum > 150] = 1
ws = watershed(lum.astype(float), markers=mk, mask=dark | (lum > 150))
ink = (ws == 2) & dark
ink[380:480, 44:81] |= dark[380:480, 44:81]; ink[480:556, 39:81] |= dark[480:556, 39:81]   # meio do braço: ali só tem tinta (fundo e vão ficam fora)
L, n = nd.label(ink, structure=np.ones((3, 3)))
objs = nd.find_objects(L)

# partes: caixa (x0, y0, x1, y1) no recorte; entra o componente cujo centro cai na caixa
PARTES = [
    ("corpo-cabeca", (80, 40, 210, 200)),
    ("corpo-braco", (25, 200, 160, 710)),
    ("corpo-peito", (140, 255, 310, 395)),
    ("corpo-coxa", (105, 700, 250, 990)),
    ("corpo-tronco", (95, 380, 300, 960)),
    ("corpo-canela-d", (215, 1130, 250, 1345)),
    ("corpo-canela-e", (185, 950, 335, 1335)),
]
cm = nd.center_of_mass(ink, L, range(1, n + 1))
sz = nd.sum(ink, L, range(1, n + 1))
caixas = {}
usado = set()
lista = []
for pid, (x0, y0, x1, y1) in PARTES:
    ks = [k + 1 for k, (cy, cx) in enumerate(cm) if sz[k] >= 150 and x0 <= cx < x1 and y0 <= cy < y1 and k + 1 not in usado
          and objs[k][0].stop < 1345 and not (objs[k][0].start > 1170 and objs[k][1].start > 245)]
    usado.update(ks)
    m = np.isin(L, ks)
    ys, xs = np.nonzero(m)
    by0, by1, bx0, bx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    caixas[pid] = (int(bx0), int(by0), int(bx1), int(by1))
    # tom original da tinta (borda já suavizada pela foto); fora da parte, papel branco
    mm = nd.binary_dilation(m, iterations=1)[by0:by1, bx0:bx1]
    g = np.clip(lum[by0:by1, bx0:bx1], 0, 255).astype(np.uint8)
    out = np.where(mm, g, 255).astype(np.uint8)
    out = np.dstack([out] * 3)
    pad = int(max(out.shape[:2]) * .04)
    out = np.pad(out, ((pad, pad), (pad, pad), (0, 0)), constant_values=255)
    im = Image.fromarray(out)
    im.save(f"{REC}/{pid}.png")
    lista.append(dict(id=pid, nome=pid, folha=10, colorido=False))
    print(pid, ks, caixas[pid])
json.dump(lista, open(f"{REC}/_lista_corpo.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, "tools/disponiveis_limpa.py", REC, FIN, f"{REC}/_lista_corpo.json"], check=True)

# ---------- folha 9: caixas das três partes das pernas (mesmo recorte "mock" do disponiveis_cortes.py) ----------
a9 = np.asarray(Image.open(f"{D}/folha-09.jpeg").convert("RGB")).astype(int)
def caixa_mock(b):
    x0, y0, x1, y1 = b
    cc = a9[y0:y1, x0:x1]
    l9 = cc @ np.array([.299, .587, .114]); m = l9 < 95
    lb, _ = nd.label(m, structure=np.ones((3, 3))); s = nd.sum(m, lb, range(1, lb.max() + 1))
    borda = set(np.unique(np.r_[lb[0], lb[-1], lb[:, 0], lb[:, -1]])) - {0}
    maior = 1 + int(np.argmax(s))
    ok = [k + 1 for k in range(len(s)) if s[k] > 40 and (k + 1 == maior or k + 1 not in borda)]
    ys, xs = np.nonzero(np.isin(lb, ok))
    return (x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()) + 1, y0 + int(ys.max()) + 1)
pernas = {"tribal-coxa": caixa_mock((95, 495, 310, 935)), "tribal-canela": caixa_mock((120, 945, 345, 1528)),
          "tribal-perna-longa": caixa_mock((330, 495, 545, 1518))}

# ---------- monta a arte única de cada conjunto ----------
def monta(nome, partes, K):
    xs0 = min(b[0] for b in partes.values()); ys0 = min(b[1] for b in partes.values())
    xs1 = max(b[2] for b in partes.values()); ys1 = max(b[3] for b in partes.values())
    tela = Image.new("RGBA", ((xs1 - xs0) * K, (ys1 - ys0) * K), (0, 0, 0, 0))
    for pid, (x0, y0, x1, y1) in partes.items():
        p = Image.open(f"{FIN}/{pid}.png")
        p = p.crop(p.getchannel("A").getbbox())
        p = p.resize(((x1 - x0) * K, (y1 - y0) * K), Image.LANCZOS)
        tela.alpha_composite(p, ((x0 - xs0) * K, (y0 - ys0) * K))
    pad = int(max(tela.size) * .05)
    t = Image.new("RGBA", (tela.width + 2 * pad, tela.height + 2 * pad), (0, 0, 0, 0)); t.alpha_composite(tela, (pad, pad))
    t.save(f"{FIN}/{nome}.png", optimize=True)
    b = Image.new("RGB", t.size, (255, 255, 255)); b.paste(t, mask=t.getchannel("A")); b.save(f"{FIN}/{nome}-branco.png", optimize=True)
    print(nome, t.size)

monta("pernas-tribais", pernas, 4)
monta("corpo-inteiro", caixas, 4)
json.dump({"corpo": caixas, "pernas": pernas}, open(f"{REC}/_conjuntos.json", "w"), indent=1)
