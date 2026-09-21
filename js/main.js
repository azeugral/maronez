/* MARONEZ  -  scripts compartilhados (sem dependências) */
(() => {
  "use strict";

  /* ---------- Config: tudo que o cliente pode trocar fica aqui ---------- */
  const CONFIG = {
    // CONFIRMAR: número com DDI para abrir o WhatsApp com mensagem pronta (ex.: "5551999999999").
    // Vazio = usa o link de mensagem do Instagram (sem texto pré-preenchido).
    whatsappNumber: "",
    whatsappMessageLink: "https://wa.me/message/BCC4OXL3C5G3M1",
    instagram: "https://www.instagram.com/maronezzzz/",
    tiktok: "https://www.tiktok.com/@maronezzz",
    youtube: "https://www.youtube.com/@maronezzzz",
    playlist: "63ik4dkmrl8umtK1OLSJS7",
    // CONFIRMAR: ID do vídeo do Kick Buttowski que ele quer na TV (hoje: 1h de episódios dublados).
    kickVideoId: "-5EEwggolgM",
  };
  window.MARONEZ = CONFIG;

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Links de WhatsApp: todos os [data-wa] apontam pro mesmo lugar ---------- */
  const waHref = (text) => {
    if (CONFIG.whatsappNumber) {
      const q = text ? `?text=${encodeURIComponent(text)}` : "";
      return `https://wa.me/${CONFIG.whatsappNumber}${q}`;
    }
    return CONFIG.whatsappMessageLink;
  };
  document.querySelectorAll("[data-wa]").forEach((a) => {
    a.href = waHref(a.dataset.wa || "");
    a.target = "_blank";
    a.rel = "noopener";
  });

  /* ---------- Logo: se a imagem não existir, cai no monograma ---------- */
  document.querySelectorAll("img[data-logo]").forEach((img) => {
    const swap = () => {
      const fb = document.createElement("span");
      const inBadge = img.closest(".hero__badge");
      fb.className = inBadge ? "hero__badge--text" : img.className + " brand__mark--fallback";
      fb.innerHTML = inBadge ? "Seja<br>Nask" : "M";
      fb.setAttribute("aria-hidden", "true");
      img.replaceWith(fb);
    };
    // O erro pode ter disparado antes do script (defer) rodar.
    if (img.complete && img.naturalWidth === 0) swap();
    else img.addEventListener("error", swap, { once: true });
  });

  /* ---------- Nav: página atual ---------- */
  const here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav__link, .menu__link").forEach((a) => {
    const target = a.getAttribute("href").split("/").pop();
    if (target === here) a.setAttribute("aria-current", "page");
  });

  /* ---------- Menu mobile ---------- */
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.querySelector(".nav-toggle__label").textContent = open ? "Fechar" : "Menu";
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && document.body.classList.contains("menu-open")) toggle.click();
    });
  }

  /* ---------- Reveal on scroll (IntersectionObserver, nunca scroll listener) ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length && !reduceMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- Portfólio: filtros ---------- */
  const filters = document.querySelectorAll(".filter");
  const items = document.querySelectorAll(".grid-port .work");
  if (filters.length && items.length) {
    filters.forEach((btn) => {
      btn.addEventListener("click", () => {
        filters.forEach((b) => b.setAttribute("aria-pressed", "false"));
        btn.setAttribute("aria-pressed", "true");
        const cat = btn.dataset.filter;
        items.forEach((it) => {
          const show = cat === "all" || (it.dataset.cat || "").split(" ").includes(cat);
          it.classList.toggle("is-hidden", !show);
        });
      });
    });
  }

  /* ---------- Portfólio: lightbox ---------- */
  const lb = document.querySelector(".lightbox");
  if (lb) {
    const img = lb.querySelector(".lightbox__img img");
    const title = lb.querySelector("[data-lb-title]");
    const style = lb.querySelector("[data-lb-style]");
    const region = lb.querySelector("[data-lb-region]");
    const state = lb.querySelector("[data-lb-state]");
    const quote = lb.querySelector("[data-lb-quote]");
    document.querySelectorAll(".grid-port .work").forEach((w) => {
      w.addEventListener("click", (e) => {
        e.preventDefault();
        const src = w.querySelector("img");
        img.src = src.dataset.full || src.src;
        img.alt = src.alt;
        title.textContent = w.dataset.title || "";
        style.textContent = w.dataset.style || "";
        region.textContent = w.dataset.region || "";
        state.textContent = w.dataset.state || "";
        quote.href = `orcamento.html?ref=${encodeURIComponent(w.dataset.title || "")}`;
        lb.showModal();
      });
    });
    lb.querySelector(".lightbox__close").addEventListener("click", () => lb.close());
    lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
  }

  /* ---------- FAQ: abre e fecha com animação de altura (WAAPI) ---------- */
  document.querySelectorAll(".faq details").forEach((d) => {
    const summary = d.querySelector("summary");
    const body = d.querySelector(".faq__a");
    if (!summary || !body) return;
    let running = null;

    const toggle = () => {
      if (reduceMotion) { d.open = !d.open; return; }
      if (running) running.cancel();
      const from = d.offsetHeight;
      d.style.overflow = "hidden";

      if (d.open) {
        // fechar: encolhe até a altura do summary, depois fecha de verdade
        const to = summary.offsetHeight;
        body.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(-6px)" }], { duration: 220, easing: "cubic-bezier(0.65, 0, 0.35, 1)", fill: "forwards" });
        running = d.animate([{ height: `${from}px` }, { height: `${to}px` }], { duration: 380, easing: "cubic-bezier(0.65, 0, 0.35, 1)" });
        running.onfinish = () => { d.open = false; d.style.height = ""; d.style.overflow = ""; running = null; body.getAnimations().forEach((a) => a.cancel()); };
      } else {
        // abrir: abre, mede, e anima da altura fechada até a aberta
        d.open = true;
        const to = d.offsetHeight;
        running = d.animate([{ height: `${from}px` }, { height: `${to}px` }], { duration: 480, easing: "cubic-bezier(0.16, 1, 0.3, 1)" });
        body.animate([{ opacity: 0, transform: "translateY(-6px)" }, { opacity: 1, transform: "none" }], { duration: 420, delay: 80, easing: "cubic-bezier(0.16, 1, 0.3, 1)", fill: "backwards" });
        running.onfinish = () => { d.style.height = ""; d.style.overflow = ""; running = null; };
      }
    };

    summary.addEventListener("click", (e) => { e.preventDefault(); toggle(); });
  });

  /* ---------- Loja: variante de cor troca foto e link de compra ---------- */
  document.querySelectorAll("[data-variants]").forEach((card) => {
    const img = card.querySelector("[data-variant-img]");
    const links = card.querySelectorAll("[data-variant-link]");
    card.querySelectorAll('input[type="radio"]').forEach((r) => {
      r.addEventListener("change", () => {
        if (!r.checked) return;
        img.src = r.dataset.img;
        img.srcset = r.dataset.srcset || "";
        img.alt = r.dataset.alt || img.alt;
        links.forEach((a) => { a.href = r.dataset.href; });
      });
    });
  });

  /* ---------- Embeds sob demanda (YouTube / Spotify só carregam no clique) ---------- */
  document.querySelectorAll("[data-embed]").forEach((box) => {
    const trigger = box.querySelector("[data-embed-load]");
    if (!trigger) return;
    trigger.addEventListener("click", () => {
      const kind = box.dataset.embed;
      const iframe = document.createElement("iframe");
      iframe.setAttribute("allowfullscreen", "");
      iframe.setAttribute("loading", "lazy");
      if (kind === "youtube") {
        const id = box.dataset.id || CONFIG.kickVideoId;
        iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.title = box.dataset.title || "Vídeo";
      } else if (kind === "spotify") {
        iframe.src = `https://open.spotify.com/embed/playlist/${CONFIG.playlist}?theme=0`;
        iframe.allow = "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture";
        iframe.title = "Playlist MARONASKS";
      }
      box.querySelectorAll("[data-embed-facade]").forEach((f) => f.remove());
      box.appendChild(iframe);
    });
  });

  /* ---------- Orçamento: monta a mensagem e abre o WhatsApp ---------- */
  const form = document.querySelector("#form-orcamento");
  if (form) {
    const ref = new URLSearchParams(location.search).get("ref");
    if (ref) {
      const refField = form.querySelector("#ref");
      if (refField) refField.value = `Referência do portfólio: ${ref}`;
    }
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      let ok = true;
      form.querySelectorAll("[required]").forEach((f) => {
        const wrap = f.closest(".field");
        const bad = !f.value.trim();
        wrap.classList.toggle("is-invalid", bad);
        if (bad) ok = false;
      });
      if (!ok) { form.querySelector(".is-invalid input, .is-invalid textarea")?.focus(); return; }

      const v = (id) => (form.querySelector(`#${id}`)?.value || "").trim();
      const cidade = form.querySelector('input[name="cidade"]:checked')?.value || "";
      const tamanho = form.querySelector('input[name="tamanho"]:checked')?.value || "";
      const msg = [
        "Fala Maronez! Quero fazer uma tattoo.",
        `Ideia: ${v("ideia")}`,
        `Região: ${v("regiao")}`,
        tamanho && `Tamanho: ${tamanho}`,
        cidade && `Onde: ${cidade}`,
        v("ref") && v("ref"),
        `Nome: ${v("nome")}`,
      ].filter(Boolean).join("\n");

      const url = waHref(msg);
      if (!CONFIG.whatsappNumber && navigator.clipboard) {
        // Sem número configurado: copia a mensagem para colar no chat.
        navigator.clipboard.writeText(msg).catch(() => {});
        const note = form.querySelector("[data-copied]");
        if (note) note.hidden = false;
      }
      window.open(url, "_blank", "noopener");
    });
  }
})();
