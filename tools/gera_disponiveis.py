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
                 'content="Desenhos prontos do Maronez: tribal, personagens, lettering e colagem. Prove no corpo 3D e peça o orçamento."')
        .replace('href="https://maronez.com.br/portfolio"', 'href="https://maronez.com.br/disponiveis"')
        .replace('content="Portfólio | Maronez"', 'content="Disponíveis | Maronez"')
        .replace('content="Peças freehand feitas direto na pele."', 'content="Desenhos prontos pra tatuar. Prove no corpo 3D."')
        .replace('content="https://maronez.com.br/portfolio"', 'content="https://maronez.com.br/disponiveis"')
        .replace('<link rel="stylesheet" href="css/style.css?v=20261105b">',
                 '<link rel="stylesheet" href="css/style.css?v=20261124">\n  <link rel="stylesheet" href="css/disponiveis.css?v=20261124c">'))
rodape = rodape.replace('<script src="js/main.js?v=20261105b" defer></script>',
                        '<script src="js/main.js?v=20261124" defer></script>\n  <script src="js/disponiveis.js?v=20261124c" defer></script>')

seta = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
cont = {k: sum(p["cat"] == k for p in L) for k in CAT}
filtros = f'<button class="filter" type="button" data-filter="all" aria-pressed="true">Tudo <span class="disp-qt">{len(L)}</span></button>\n' + "\n".join(
    f'          <button class="filter" type="button" data-filter="{k}" aria-pressed="false">{v} <span class="disp-qt">{cont[k]}</span></button>' for k, v in CAT.items())

cards = []
for p in L:
    n = f'{p["n"]:02d}'
    nome = html.escape(p["nome"])
    cards.append(f'''          <li class="disp" data-cat="{p["cat"]}">
            <button type="button" class="disp__btn" data-id="{p["id"]}" data-n="{n}" data-nome="{nome}" data-cat="{CAT[p["cat"]]}" data-full="assets/img/disponiveis/{p["id"]}.webp">
              <span class="disp__papel"><img src="assets/img/disponiveis/{p["id"]}-p.webp" alt="{nome}, desenho disponível ({CAT[p["cat"]].lower()})" width="{p["w"]}" height="{p["h"]}" decoding="async"></span>
            </button>
          </li>''')

main = f'''<main id="conteudo">
    <section class="page-head">
      <div class="wrap">
        <h1 class="display display--xl">Disponíveis</h1>
        <p class="lead">Desenhos prontos pra tatuar. Escolhe um, prova no corpo 3D e manda pro orçamento.</p>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        <ul class="disp-grade" id="grade">
{chr(10).join(cards)}
        </ul>
      </div>
    </section>

    <section class="section disp-corpo" aria-labelledby="t-corpo">
      <div class="wrap">
        <div class="section-head">
          <p class="label">No corpo</p>
          <h2 class="display display--l" id="t-corpo">Como fica na pele</h2>
        </div>
        <div class="disp-mock">
          <figure><img src="assets/img/disponiveis/mockup-2.webp" alt="Tribais nas pernas e na lateral do tronco" width="1022" height="1400" loading="lazy"></figure>
          <figure><img src="assets/img/disponiveis/mockup-4.webp" alt="Tribais no corpo inteiro de um manequim" width="1022" height="1400" loading="lazy"></figure>
          <figure><img src="assets/img/disponiveis/mockup-3.webp" alt="Tribal em preto e vermelho no quadril e tribal na perna" width="1120" height="1400" loading="lazy"></figure>
        </div>
      </div>
    </section>

    <section class="section disp-prov" id="provador" aria-labelledby="t-prov">
      <div class="wrap">
        <div class="section-head">
          <p class="label">Provador 3D</p>
          <h2 class="display display--l" id="t-prov">Prova no corpo</h2>
          <p class="lead">Põe um disponível na pele, ajusta tamanho e giro e vê de todos os lados. Depois é só mandar a montagem pro orçamento.</p>
        </div>
        <div class="pv-janela">
          <div class="pv-janela__barra">
            <span translate="no">Provador 3D · Maronez</span>
            <a href="https://orcamento.maronez.com.br/provador" target="_blank" rel="noopener">Abrir em tela cheia ↗</a>
          </div>
          <iframe id="pv-janela" src="https://orcamento.maronez.com.br/provador/?vitrine=1" title="Provador 3D dos disponíveis" loading="lazy" allow="clipboard-write; web-share"></iframe>
        </div>
      </div>
    </section>

    <section class="section cta-band" style="padding-top:0">
      <div class="wrap cta-band__in">
        <h2 class="display display--l">Gostou de algum?</h2>
        <div class="cta-band__actions">
          <a class="btn btn--wide" href="https://orcamento.maronez.com.br/">Pedir orçamento
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
          <a class="btn" href="#provador" data-z-provar>Provar no corpo {seta}</a>
          <a class="btn btn--ghost" href="https://orcamento.maronez.com.br/" data-z-pedir>Pedir esse desenho</a>
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
