"""Gera disponiveis.html a partir de assets/brand/disponiveis-originais/final/_site.json.
Cabeçalho, menu e rodapé vêm do portfolio.html (mesmo site). Rodar da raiz do site: python tools/gera_disponiveis.py"""
import json, html, re

CAT = {"tribal": "Tribal", "personagens": "Personagens", "lettering": "Lettering", "colagem": "Colagem"}
L = json.load(open("assets/brand/disponiveis-originais/final/_site.json", encoding="utf8"))
base = open("portfolio.html", encoding="utf8").read()
topo = base[: base.index('<main id="conteudo">')]
rodape = base[base.index("<footer"):]

topo = (topo.replace("<title>Portfólio | Maronez</title>", "<title>Disponíveis | Maronez</title>")
        .replace('content="Peças freehand e ignorant feitas por Maronez em Porto Alegre e guest spots."',
                 'content="Desenhos prontos do Maronez: tribal, personagens, lettering e colagem. Escolhe um e pede o orçamento."')
        .replace('href="https://maronez.com.br/portfolio"', 'href="https://maronez.com.br/disponiveis"')
        .replace('content="Portfólio | Maronez"', 'content="Disponíveis | Maronez"')
        .replace('content="Peças freehand feitas direto na pele."', 'content="Desenhos prontos pra tatuar."')
        .replace('content="https://maronez.com.br/portfolio"', 'content="https://maronez.com.br/disponiveis"')
        .replace('<link rel="stylesheet" href="css/style.css?v=20261105b">',
                 '<link rel="stylesheet" href="css/style.css?v=20261124">\n  <link rel="stylesheet" href="css/disponiveis.css?v=20261124i">'))
rodape = rodape.replace('<script src="js/main.js?v=20261124h" defer></script>',
                        '<script src="js/main.js?v=20261124h" defer></script>\n  <script src="js/disponiveis.js?v=20261124i" defer></script>')

seta = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
cont = {k: sum(p["cat"] == k for p in L) for k in CAT}
filtros = f'<button class="filter" type="button" data-filter="all" aria-pressed="true">Tudo <span class="disp-qt">{len(L)}</span></button>\n' + "\n".join(
    f'          <button class="filter" type="button" data-filter="{k}" aria-pressed="false">{v} <span class="disp-qt">{cont[k]}</span></button>' for k, v in CAT.items())

cards = []
for p in L:
    n = f'{p["n"]:02d}'
    nome = html.escape(p["nome"])
    cards.append(f'''          <li class="disp{' disp--mock' if p.get('mockup') else ''}" data-cat="{p["cat"]}">
            <button type="button" class="disp__btn" data-id="{p["id"]}" data-n="{n}" data-nome="{nome}" data-cat="{CAT[p["cat"]]}" data-full="assets/img/disponiveis/{p["id"]}.webp">
              <span class="disp__papel"><img src="assets/img/disponiveis/{p["id"]}-p.webp" alt="{nome}, desenho disponível ({CAT[p["cat"]].lower()})" width="{p["w"]}" height="{p["h"]}" decoding="async"></span>
            </button>
          </li>''')

main = f'''<main id="conteudo">
    <section class="page-head">
      <div class="wrap">
        <h1 class="display display--xl">Disponíveis</h1>
        <p class="lead">Desenhos prontos pra tatuar. Escolhe um e pede pelo WhatsApp.</p>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        <ul class="disp-grade" id="grade">
{chr(10).join(cards)}
        </ul>
      </div>
    </section>

    <section class="section cta-band" style="padding-top:0">
      <div class="wrap cta-band__in">
        <h2 class="display display--l">Gostou de algum?</h2>
        <div class="cta-band__actions">
          <a class="btn btn--wide" href="https://wa.me/555191248594" data-wa="Fala Maronez! Vi os teus disponíveis e quero fazer um.">Pedir pelo WhatsApp
            {seta}
          </a>
        </div>
      </div>
    </section>
  </main>

  <dialog class="disp-zoom" aria-label="Desenho disponível">
    <div class="disp-zoom__in">
      <div class="disp-zoom__papel"><img src="" alt=""></div>
      <div class="disp-zoom__info">
        <div class="disp-zoom__acoes">
          <a class="btn" href="https://wa.me/555191248594" target="_blank" rel="noopener" data-z-pedir>Pedir esse desenho {seta}</a>
          <div class="disp-zoom__nav">
            <button type="button" data-z-ant aria-label="Desenho anterior"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
            <button type="button" data-z-prox aria-label="Próximo desenho">{seta}</button>
          </div>
        </div>
      </div>
      <button class="disp-zoom__fechar" type="button" aria-label="Fechar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg></button>
    </div>
  </dialog>

  '''
open("disponiveis.html", "w", encoding="utf8", newline="\n").write(topo + main + rodape)
print(len(L), "desenhos")

# ---------- orcamento.maronez.com.br: a mesma página + o provador 3D ----------
# Fica no repo do LRGZ Manequim (clientes/maronez/raiz.html → maronez/index.html). <base> aponta pro site:
# CSS, imagens, fontes e menu vêm de maronez.com.br; o provador é do próprio subdomínio (mesma origem).
HUB = r"C:/Users/dslru/Documents/L R G Z/Sistemas/lrgz-manequim/clientes/maronez/raiz.html"
prov = '''    <section class="section disp-prov" id="provador" aria-labelledby="t-prov">
      <div class="wrap">
        <div class="section-head">
          <p class="label">Provador 3D</p>
          <h2 class="display display--l" id="t-prov">Prova no corpo</h2>
          <p class="lead">Põe um disponível na pele, gira o corpo e vê de todos os lados. Gostou? Pede pelo WhatsApp.</p>
        </div>
        <div class="pv-janela">
          <iframe id="pv-janela" title="Provador 3D dos disponíveis" allow="clipboard-write; web-share"></iframe>
        </div>
      </div>
    </section>

'''
hub_main = (main
    .replace("Escolhe um e pede pelo WhatsApp.", "Escolhe um, prova no corpo 3D e pede pelo WhatsApp.")
    .replace('    <section class="section" style="padding-top:0">', prov + '    <section class="section disp-todos" aria-label="Todos os disponíveis">', 1)
    .replace('<a class="btn" href="https://wa.me/555191248594" target="_blank" rel="noopener" data-z-pedir>Pedir esse desenho',
             f'<a class="btn" href="#provador" data-z-provar>Provar no corpo {seta}</a>\n          <a class="btn btn--ghost" href="https://wa.me/555191248594" target="_blank" rel="noopener" data-z-pedir>Pedir no WhatsApp'))
hub_js = open("tools/disponiveis_hub.js", encoding="utf8").read()
hub_topo = (topo
    .replace("<head>", '<head>\n  <base href="https://maronez.com.br/">', 1)
    .replace('<link rel="canonical" href="https://maronez.com.br/disponiveis">', '<link rel="canonical" href="https://orcamento.maronez.com.br/">')
    .replace('content="https://maronez.com.br/disponiveis"', 'content="https://orcamento.maronez.com.br/"')
    .replace('<link rel="manifest" href="manifest.webmanifest">\n', '')
    .replace('class="nav__link" href="/disponiveis"', 'class="nav__link" href="/disponiveis" aria-current="page"')
    .replace('class="menu__link" href="/disponiveis"', 'class="menu__link" href="/disponiveis" aria-current="page"'))
hub_rod = rodape.replace('  <script src="js/disponiveis.js?v=20261124i" defer></script>', f'  <script>\n{hub_js}\n  </script>')
assert hub_rod != rodape and '<base href' in hub_topo and 'data-z-provar' in hub_main and 'id="provador"' in hub_main
open(HUB, "w", encoding="utf8", newline="\n").write(hub_topo + hub_main + hub_rod)
print("hub:", HUB)
