/* Páginas de teste: manda tudo para outro número de WhatsApp.
   Use ?wa=5551999999999 na URL, ou troque o valor de PADRAO abaixo. */
(() => {
  const PADRAO = ""; // ex.: "5551999999999"
  const url = new URLSearchParams(location.search).get("wa") || "";
  const num = (url || PADRAO).replace(/\D/g, "");
  if (num) {
    window.MARONEZ_WA = num;
    try { sessionStorage.setItem("maronez_wa_teste", num); } catch (e) {}
  } else {
    try { window.MARONEZ_WA = sessionStorage.getItem("maronez_wa_teste") || ""; } catch (e) {}
  }
  addEventListener("DOMContentLoaded", () => {
    const bar = document.createElement("div");
    bar.className = "teste-bar";
    bar.innerHTML = window.MARONEZ_WA
      ? `Modo teste. Mensagens vão para <strong>+${window.MARONEZ_WA}</strong>. <a href="index.html">trocar número</a>`
      : `Modo teste sem número. <a href="index.html">definir número</a>`;
    document.body.prepend(bar);
    // mantém o ?wa entre as páginas de teste
    if (window.MARONEZ_WA) {
      document.querySelectorAll('a[href$="loja.html"], a[href$="orcamento.html"], a[href="index.html"]').forEach((a) => {
        if (a.getAttribute("href").startsWith("../")) return;
        a.href = a.getAttribute("href").split("?")[0] + "?wa=" + window.MARONEZ_WA;
      });
    }
  });
})();
