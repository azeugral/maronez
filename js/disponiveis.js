/* Disponíveis: filtros e zoom com anterior/próximo; "Pedir esse desenho" abre o WhatsApp do Maronez com o desenho na mensagem.
   (O provador 3D saiu do site por enquanto: volta quando a prova no corpo estiver 100%.) */
(() => {
  const SITE = "https://maronez.com.br/";
  // mensagem pronta: número, nome e link da imagem (ele vê qual é sem procurar)
  const wa = (b) => {
    const cfg = window.MARONEZ || {}, num = cfg.whatsappNumber || "555191248594";
    const msg = [
      "Fala Maronez! Curti um dos teus disponíveis:",
      `Nº ${b.dataset.n} · ${b.dataset.nome}`,
      SITE + b.dataset.full,
      "",
      "Quero saber valor e data pra fazer.",
    ].join("\n");
    return `https://wa.me/${num}?text=${encodeURIComponent(msg)}`;
  };

  /* ---------- filtros ---------- */
  const itens = [...document.querySelectorAll(".disp")];
  const filtros = document.querySelectorAll(".disp-filtros .filter");
  filtros.forEach((b) => b.addEventListener("click", () => {
    filtros.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    const c = b.dataset.filter;
    itens.forEach((it) => it.classList.toggle("is-hidden", c !== "all" && it.dataset.cat !== c));
  }));

  /* ---------- zoom ---------- */
  const z = document.querySelector(".disp-zoom");
  if (!z) return;
  const img = z.querySelector(".disp-zoom__papel img");
  const zPedir = z.querySelector("[data-z-pedir]");
  const botoes = [...document.querySelectorAll(".disp__btn")];
  let atual = -1;
  const visiveis = () => botoes.filter((b) => !b.closest(".disp").classList.contains("is-hidden"));
  function abre(b) {
    atual = botoes.indexOf(b);
    img.src = b.dataset.full; img.alt = b.querySelector("img").alt;
    zPedir.href = wa(b);
    if (!z.open) z.showModal();
  }
  const passa = (k) => { const v = visiveis(), i = v.indexOf(botoes[atual]); if (v.length) abre(v[(i + k + v.length) % v.length]); };
  botoes.forEach((b) => {
    b.addEventListener("click", () => abre(b));
    // pré-carrega a imagem grande quando o dedo/mouse chega no cartão
    b.addEventListener("pointerenter", () => { const i = new Image(); i.src = b.dataset.full; }, { once: true });
  });
  z.querySelector("[data-z-ant]").addEventListener("click", () => passa(-1));
  z.querySelector("[data-z-prox]").addEventListener("click", () => passa(1));
  z.querySelector(".disp-zoom__fechar").addEventListener("click", () => z.close());
  z.addEventListener("click", (e) => { if (e.target === z) z.close(); });
  z.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") passa(-1); if (e.key === "ArrowRight") passa(1); });
})();
