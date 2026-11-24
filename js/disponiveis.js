/* Disponíveis: filtros, zoom com anterior/próximo e o provador 3D (LRGZ Manequim, ?vitrine=1).
   "Provar no corpo" leva o desenho escolhido direto pro provador (?d=<id> ou postMessage). */
(() => {
  const PROV = "https://orcamento.maronez.com.br/provador/?vitrine=1";
  const ORC = "https://orcamento.maronez.com.br/";
  const suave = () => (matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth");

  /* ---------- filtros ---------- */
  const itens = [...document.querySelectorAll(".disp")];
  const filtros = document.querySelectorAll(".disp-filtros .filter");
  filtros.forEach((b) => b.addEventListener("click", () => {
    filtros.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    const c = b.dataset.filter;
    itens.forEach((it) => it.classList.toggle("is-hidden", c !== "all" && it.dataset.cat !== c));
  }));

  /* ---------- provador ---------- */
  const f = document.getElementById("pv-janela");
  let pronto = false;
  if (f) {
    f.addEventListener("load", () => { pronto = true; });
    const topoLivre = () => { const n = document.querySelector(".header"); return (n ? Math.max(0, n.getBoundingClientRect().bottom) : 0) + 14; };
    addEventListener("message", (e) => {
      if (e.source !== f.contentWindow || !e.data || !e.data.manequim) return;
      const d = e.data;
      if (d.altura) f.style.height = Math.max(480, Math.min(4000, d.altura)) + "px";
      if (d.rolar) {
        const base = f.getBoundingClientRect().top + scrollY, t = base + d.rolar.t, b = base + d.rolar.b;
        const cima = scrollY + topoLivre(), baixo = scrollY + innerHeight - 16;
        let y = null;
        if (d.rolar.modo === "fim") { if (b > baixo) y = b - innerHeight + 24; }
        else if (t < cima || b > baixo) y = t - topoLivre();
        if (y !== null) scrollTo({ top: Math.max(0, y), behavior: suave() });
      }
    });
  }
  function prova(id) {
    if (!f) return;
    document.getElementById("provador").scrollIntoView({ behavior: suave() });
    if (pronto) f.contentWindow.postMessage({ manequim: 1, provar: id }, "*");
    else { f.loading = "eager"; f.src = `${PROV}&d=${encodeURIComponent(id)}`; }
  }

  /* ---------- zoom ---------- */
  const z = document.querySelector(".disp-zoom");
  if (!z) return;
  const img = z.querySelector(".disp-zoom__papel img");
  const zN = z.querySelector("[data-z-n]"), zNome = z.querySelector("[data-z-nome]"), zCat = z.querySelector("[data-z-cat]");
  const zProvar = z.querySelector("[data-z-provar]"), zPedir = z.querySelector("[data-z-pedir]");
  const botoes = [...document.querySelectorAll(".disp__btn")];
  let atual = -1;
  const visiveis = () => botoes.filter((b) => !b.closest(".disp").classList.contains("is-hidden"));
  function abre(b) {
    atual = botoes.indexOf(b);
    img.src = b.dataset.full; img.alt = b.querySelector("img").alt;
    zN.textContent = `Nº ${b.dataset.n}`; zNome.textContent = b.dataset.nome; zCat.textContent = b.dataset.cat;
    zPedir.href = `${ORC}?desenho=${encodeURIComponent(`${b.dataset.nome} (disponível Nº ${b.dataset.n})`)}`;
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
  zProvar.addEventListener("click", (e) => { e.preventDefault(); const id = botoes[atual].dataset.id; z.close(); prova(id); });
})();
