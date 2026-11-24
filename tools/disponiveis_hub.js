/* orcamento.maronez.com.br: disponíveis + provador 3D (LRGZ Manequim, ?vitrine=1).
   "Provar no corpo" leva o desenho pro provador; "Pedir no WhatsApp" abre a conversa com o desenho na mensagem.
   Gerado por tools/gera_disponiveis.py (site do Maronez). Não editar o raiz.html à mão. */
(() => {
  const SITE = "https://maronez.com.br/";
  // no ar o provador é /provador/ deste domínio; no teste local (repo do Manequim) é /maronez/provador/
  const PROV = location.origin + (location.pathname.startsWith("/maronez/") ? "/maronez/provador/" : "/provador/") + "?vitrine=1";
  const suave = () => (matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth");
  const wa = (b) => {
    const num = (window.MARONEZ && window.MARONEZ.whatsappNumber) || "555191248594";
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

  /* ---------- provador ---------- */
  const f = document.getElementById("pv-janela");
  let pronto = false;
  if (f) {
    f.addEventListener("load", () => { pronto = true; });
    f.src = PROV;
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
    const alvo = document.getElementById("provador").getBoundingClientRect().top + scrollY;
    scrollTo({ top: Math.max(0, alvo), behavior: "instant" });
    if (pronto) f.contentWindow.postMessage({ manequim: 1, provar: id }, "*");
    else f.src = `${PROV}&d=${encodeURIComponent(id)}`;
  }

  /* ---------- zoom ---------- */
  const z = document.querySelector(".disp-zoom");
  if (!z) return;
  const img = z.querySelector(".disp-zoom__papel img");
  const zProvar = z.querySelector("[data-z-provar]"), zPedir = z.querySelector("[data-z-pedir]");
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
    b.addEventListener("pointerenter", () => { const i = new Image(); i.src = b.dataset.full; }, { once: true });
  });
  z.querySelector("[data-z-ant]").addEventListener("click", () => passa(-1));
  z.querySelector("[data-z-prox]").addEventListener("click", () => passa(1));
  z.querySelector(".disp-zoom__fechar").addEventListener("click", () => z.close());
  z.addEventListener("click", (e) => { if (e.target === z) z.close(); });
  z.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") passa(-1); if (e.key === "ArrowRight") passa(1); });
  // o <base> aponta pro site: o link "#provador" sairia daqui, então o clique é sempre tratado aqui
  zProvar.addEventListener("click", (e) => {
    e.preventDefault();
    const id = botoes[atual].dataset.id;
    z.addEventListener("close", () => setTimeout(() => prova(id), 0), { once: true });
    z.close();
  });
})();
