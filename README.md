# Maronez | Seja Nask

Site do tatuador Maronez (cyber freehand, Porto Alegre). HTML, CSS e JS puros, sem build.

## Estrutura

```
index.html            home: hero, portfólio, artista, localização, CTA
portfolio.html        grade com filtros (cyber / freehand / curada) e lightbox
cyber-freehand.html   página do estilo cyber freehand
freehand.html         página do estilo freehand
loja.html             camiseta e bandeira, checkout na loja parceira
sala.html             sala de espera: Kick Buttowski na TV, playlist, vlogs
orcamento.html        formulário que monta a mensagem e abre o WhatsApp
css/style.css         tokens, componentes, animações, responsivo
js/main.js            menu, reveal, filtros, lightbox, embeds, FAQ, orçamento
assets/img/           logo, favicon, og; loja/ e portfolio/ com as fotos otimizadas (1200 e 640 px)
assets/fonts/         StreetTech (soltar o arquivo aqui)
assets/brand/         arquivos de origem (logo, PNG dos produtos, zip das fotos)
```

## Rodar local

```
python -m http.server 8765
```

Abrir http://localhost:8765. O embed do YouTube não funciona abrindo o HTML direto do disco.

## Antes de publicar

Buscar `CONFIRMAR` nos arquivos: fonte StreetTech, número do WhatsApp (`js/main.js`), fotos,
links e preços da loja, endereço e horário, agenda de guest spots, sinal, domínio.
