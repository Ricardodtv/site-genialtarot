/* menu.js — 27/11/2026, pedido dele: «o site está desorganizado, não consigo navegar por todo o site». Medido: 614 das 659
   páginas só tinham o «‹ genialtarot.com». Este é o MENU ÚNICO de todas as páginas (aprovado pela maquete no Telegram):
   barra no topo (logótipo, temas no computador, Consulta, pesquisa, ☰), gaveta com os temas no telemóvel, e a linha
   «Início › Tema › Página». Carregado pelo vivo.js — em todas, a página inicial incluída (27/11, ele: «deveriam aparecer na página principal»;
   lá substitui a barra antiga); fora do consultório, da app e do pagamento. Para mudar o menu: só a lista TEMAS aqui em baixo. Para o tirar: a linha do menu.js no vivo.js. */
(function () {
  if (window.__gtm) return; window.__gtm = 1;
  var P = location.pathname.replace(/\.html$/, "").replace(/\/$/, "") || "/";
  if (/^\/(consultorio|o-teu-ceu|pagar|30-dias|gerar-pix)(\/|-sala|-autorizacao|$)/.test(P)) return;

  var TEMAS = [
    ["🔮", "Horóscopo", "/horoscopo", [["Do dia", "/horoscopo-do-dia"], ["De amanhã", "/horoscopo-de-amanha"], ["Semanal", "/horoscopo-semanal"], ["Fim de semana", "/fimdesemana"],
      ["Horóscopo 2027", "/horoscopo-2027"], ["Os 12 signos", "/signos-do-zodiaco"], ["Compatibilidade", "/compatibilidade"], ["Horóscopo chinês", "/horoscopo-chines"]], /^\/(horoscopo|signo\/|fimdesemana|signos-|compat|melhores-signos)/],
    ["🃏", "Tarot", "/tarot", [["Tarot grátis", "/tarot-gratis"], ["A carta do dia", "/tiragem-carta-do-dia"], ["Os Arcanos Maiores", "/arcanos"], ["Os Arcanos Menores", "/arcanos-menores"],
      ["Tarot do amor", "/tarot-do-amor"], ["Tarot por tema", "/tarot-por-tema"], ["Tarot terapêutico", "/tarot-terapeutico"], ["Tarot cigano", "/tarot-cigano"]], /^\/(tarot|tiragem|arcano|carta-(?!da-semana)|amor-do-dia|leia-o-tarot)/],
    ["🪐", "Astrologia", "/astrologia", [["Mapa astral", "/mapa-astral"], ["Ascendente", "/ascendente"], ["Calendário lunar", "/lua"], ["Notícias do céu", "/noticias-do-ceu"],
      ["Efemérides", "/efemerides"], ["Retrógrados 2027", "/retrogrados-2027"], ["Eclipses 2027", "/eclipses-2027"], ["Famosos com o seu céu", "/famosos-ceu"]], /^\/(mapa-astral|ascendente|lua|noticias|efemerides|retrogrados|eclipses|mercurio|famosos|astrolog|alinhamento|decanatos)/],
    ["🔢", "Numerologia", "/numerologia", [["Os números da sua vida", "/numerologia"], ["Calculadora 2027", "/numerologia-2027"]].concat([1, 2, 3, 4, 5, 6, 7, 8, 9].map(function (n) { return ["Ano Pessoal " + n, "/ano-pessoal-" + n + "-2027"]; })), /^\/(numerolog|ano-pessoal)/],
    ["🙏", "Fé e tradição", "/fe-e-tradicao", [["Rezas e orações", "/rezas-e-oracoes"], ["Benzimentos", "/benzimentos"], ["Rezas de proteção", "/rezas-de-protecao"], ["Salmos", "/salmos"],
      ["Anjo da guarda", "/anjo-da-guarda"], ["Sonhos", "/sonhos"], ["Pêndulo", "/pendulo"], ["Quiromancia", "/quiromancia"]], /^\/(fe-e-tradicao|reza|benz|salmo|anjo|sonho|pendulo|quiromancia|oracao|responso|talhar|sao-|santa-|santo|linha|montes-da-mao|tipos-de-mao|como-ler-a-mao)/],
    ["📜", "Histórias", "/historias", [["Parábolas", "/parabolas"], ["Parábolas de Jesus", "/parabolas-de-jesus"], ["Fábulas", "/fabulas-de-esopo"], ["Contos tradicionais", "/contos-tradicionais"],
      ["Lendas", "/historias-e-lendas"], ["Lendas de Lisboa", "/lendas-de-lisboa"], ["Lendas brasileiras", "/lendas-brasileiras"], ["Lendas urbanas", "/lendas-urbanas"]], /^\/(historias|parabola|fabula|conto|lenda|historia-)/],
    ["📖", "Revista", "/revista", [["A revista do mês", "/revista"], ["✉️ A Carta da Semana", "/carta-da-semana"]], /^\/(revista|carta-da-semana)/]
  ];
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var meu = -1; TEMAS.forEach(function (t, i) { if (meu < 0 && (t[4].test(P) || t[3].some(function (x) { return x[1] === P; }))) meu = i; });

  var css = ".gtm-barra{position:relative;z-index:9989;display:flex;align-items:center;gap:.6rem;padding:.55rem .9rem;background:#160b2bf2;border-bottom:1px solid #f2c96b73;box-shadow:0 6px 20px #0008;font-family:Inter,system-ui,sans-serif}" +
    ".gtm-logo{display:flex;align-items:center;gap:.5rem;text-decoration:none;color:#ffe2a0;font-family:Cinzel,Georgia,serif;font-weight:700;font-size:1.05rem;white-space:nowrap}.gtm-logo img{width:2rem;height:2rem;border-radius:.35rem}" +
    ".gtm-links{display:none;gap:1.05rem;margin-left:.8rem}.gtm-links a{color:#e7dcf3;text-decoration:none;font-weight:600;font-size:.92rem;white-space:nowrap}.gtm-links a:hover,.gtm-links a.aqui{color:#f2c96b}" +
    ".gtm-esp{flex:1}.gtm-bt{display:grid;place-items:center;flex:none;width:2.5rem;height:2.5rem;padding:0;border-radius:50%;border:1.5px solid #f2c96b;background:transparent;color:#f2c96b;font-size:1.1rem;cursor:pointer;text-decoration:none}" +
    ".gtm-cons{display:none;text-decoration:none;font-weight:800;color:#2a1245;background:linear-gradient(135deg,#ffe2a0,#f2c96b 55%,#d9a441);border-radius:999px;padding:.5rem 1rem;font-size:.9rem;white-space:nowrap}" +
    "@media (min-width:1000px){.gtm-links,.gtm-cons{display:flex}.gtm-bt.ham{display:none}}" +
    ".gtm-migalhas{position:relative;z-index:2;max-width:72rem;margin:.6rem auto 0;padding:0 1rem;font:500 .82rem/1.4 Inter,system-ui,sans-serif;color:#bfaed3}.gtm-migalhas a{color:#e7dcf3;text-decoration:none}.gtm-migalhas b{color:#f2c96b;font-weight:600}" +
    ".gtm-veu{position:fixed;inset:0;background:#0009;z-index:99998;display:none}.gtm-gaveta{position:fixed;top:0;bottom:0;right:0;width:min(23rem,88vw);z-index:99999;background:linear-gradient(170deg,#2a1245,#120722);border-left:1px solid #f2c96b88;box-shadow:-20px 0 50px #000c;overflow-y:auto;padding:1rem 1rem 2rem;transform:translateX(105%);transition:transform .3s ease;font-family:Inter,system-ui,sans-serif}" +
    "html.gtm-aberto .gtm-veu{display:block}html.gtm-aberto .gtm-gaveta{transform:none}html.gtm-aberto{overflow:hidden}" +
    ".gtm-g-topo{display:flex;align-items:center;justify-content:space-between;margin-bottom:.8rem}" +
    ".gtm-pesq{display:flex;gap:.5rem;align-items:center;background:#ffffff12;border:1px solid #f2c96b55;border-radius:999px;padding:.6rem .95rem;color:#e7dcf3;margin-bottom:1rem;font-size:.95rem;text-decoration:none}" +
    ".gtm-sec{border-bottom:1px solid #f2c96b33}.gtm-sec summary{list-style:none;display:flex;justify-content:space-between;align-items:center;padding:.85rem .2rem;font-family:Cinzel,Georgia,serif;font-weight:700;color:#ffe2a0;font-size:1.05rem;cursor:pointer}" +
    ".gtm-sec summary::-webkit-details-marker{display:none}.gtm-sec summary::after{content:'+';color:#f2c96b;font-size:1.3rem}.gtm-sec[open] summary::after{content:'−'}" +
    ".gtm-sec .itens{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;padding:0 0 .9rem}.gtm-sec .itens a{color:#e7dcf3;text-decoration:none;font-size:.9rem;padding:.5rem .6rem;border-radius:.6rem;background:#ffffff0d;border:1px solid #ffffff14}" +
    ".gtm-sec .itens a.aqui{border-color:#f2c96b;color:#f2c96b}" +
    ".gtm-base{display:grid;gap:.6rem;margin-top:1.2rem}.gtm-base a{display:block;text-align:center;text-decoration:none;font-weight:800;border-radius:999px;padding:.75rem}" +
    ".gtm-base .c{color:#2a1245;background:linear-gradient(135deg,#ffe2a0,#f2c96b 55%,#d9a441)}.gtm-base .w{color:#d8ffe6;background:rgba(37,211,102,.16);border:1px solid rgba(37,211,102,.55)}" +
    /* o menu substitui o «‹ genialtarot.com» e a pesquisa do topo; o resto do topo (Entrar, som) fica onde estava */
    "html.gtm-on .topo .backlink,html.gtm-on .gtp-topo,html.gtm-on .voltar-barra .voltar,html.gtm-on a.voltar{display:none!important}html.gtm-on header.topo{min-height:0;padding:0}html.gtm-on body>header:has(>nav.container.nav){display:none}" +
    /* 28/11/2026 (o Portal, pedido dele): no telemóvel UMA faixa no topo (a da Black Friday, enquanto estiver ligada) e só a chamada
       «Tire as suas Dúvidas» a flutuar; a bolinha verde, a etiqueta da Loja e a bola −30% saem (a faixa já anuncia a promoção) */
    "@media (max-width:760px){body:has(.bf-faixa) #vip-faixa,html.gtm-on a.float-wa,html.gtm-on #loja-etq,html.gtm-on .dst-flut,html.gtm-on .dst-bola{display:none!important}}" +
    /* 28/11/2026 (pedido dele): «etiqueta reformulada e mais bonita a dizer Loja Online em todo o portal, para as pessoas entrarem rapidamente
       na loja». Substitui a etiqueta rosa vertical da margem (#loja-etq, vip-faixa.js), que tapava texto: um botão dourado na barra
       (verde-esmeralda, escolha dele 28/11 — contrasta com o roxo e o dourado) e, quando a barra sai do ecrã, a mesma pílula no canto de baixo à ESQUERDA (o direito é da chamada do WhatsApp). Fora da própria loja. */
    "html.gtm-on #loja-etq{display:none!important}" +
    ".gtm-loja,.gtm-lojaf{position:relative;overflow:hidden;display:inline-flex;align-items:center;gap:.4rem;flex:none;text-decoration:none;white-space:nowrap;font:800 .88rem/1 Inter,system-ui,sans-serif;color:#fff;text-shadow:0 1px 1px #0005;" +
    "background:linear-gradient(135deg,#5ef0b0,#13b47a 50%,#0a7a52);border:1px solid #c8ffe6;border-radius:999px;padding:.5rem .85rem .5rem .6rem;box-shadow:0 0 0 1px #0006,0 4px 16px #13b47a66,inset 0 1px 0 #fff6}" +
    ".gtm-loja b,.gtm-lojaf b{font-weight:800;color:#fff3b0}.gtm-loja .i,.gtm-lojaf .i{display:grid;place-items:center;width:1.55rem;height:1.55rem;border-radius:50%;background:#053a27;font-size:.85rem;box-shadow:0 0 8px #5ef0b0}" +
    ".gtm-loja::after,.gtm-lojaf::after{content:'';position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,#ffffffb0,transparent);transform:skewX(-20deg);animation:gtmBrilho 3.6s ease-in-out infinite}" +
    "@keyframes gtmBrilho{0%,62%{left:-60%}100%{left:140%}}" +
    ".gtm-loja:hover,.gtm-lojaf:hover{filter:brightness(1.07);transform:translateY(-1px)}.gtm-loja.aqui{outline:2px solid #c8ffe6;outline-offset:2px}" +
    ".gtm-lojaf{position:fixed;left:14px;bottom:18px;z-index:9989;font-size:.9rem;padding:.6rem 1rem .6rem .6rem;box-shadow:0 8px 24px #000a,0 0 0 1px #0a7a52,0 0 18px #13b47a88;opacity:0;transform:translateY(20px);pointer-events:none;transition:opacity .35s,transform .35s}" +
    ".gtm-lojaf.on{opacity:1;transform:none;pointer-events:auto}" +
    "@media (max-width:560px){.gtm-logo .gtm-nome{display:none}.gtm-barra .gtm-loja{font-size:.74rem;line-height:1.05;padding:.32rem .65rem .32rem .35rem;gap:.35rem}.gtm-barra .gtm-loja>span:last-child{display:flex;flex-direction:column}" +
    /* o «Entrar» (conta.js) é fixo e procura lugar à esquerda da 🔍: o botão da Loja deixa-lhe esse lugar livre */
    "body:has(#gtc-btn) .gtm-barra .gtm-loja{margin-right:6.2rem}}" +
    "@media (prefers-reduced-motion:reduce){.gtm-loja::after,.gtm-lojaf::after{animation:none;display:none}}";

  function monta() {
    if (document.querySelector(".gtm-barra")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var barra = document.createElement("header"); barra.className = "gtm-barra";
    barra.innerHTML = '<a class="gtm-logo" href="/" aria-label="Genial Tarot — início"><img src="/apple-touch-icon.png" alt="" width="32" height="32"><span class="gtm-nome">Genial Tarot</span></a>' +
      '<nav class="gtm-links" aria-label="Temas">' + TEMAS.map(function (t, i) { return '<a href="' + t[2] + '"' + (i === meu ? ' class="aqui"' : "") + ">" + (t[1] === "Revista" ? "📖 " : "") + esc(t[1]) + "</a>"; }).join("") + '</nav>' +
      '<span class="gtm-esp"></span><a class="gtm-loja' + (/^\/loja/.test(P) ? " aqui" : "") + '" href="/loja" aria-label="Loja Online"><span class="i">🛍️</span><span>Loja <b>Online</b></span></a><a class="gtm-cons" href="/consulta-de-tarot-online">💬 Consulta</a>' +
      '<a class="gtm-bt" href="/pesquisa" aria-label="Pesquisar no site">🔍</a><a class="gtm-bt ham" href="#menu" role="button" aria-label="Abrir o menu" aria-expanded="false">☰</a>';
    // as faixas (Black Friday, Lista VIP) ficam POR CIMA do menu, como no resto do site: o menu entra antes do 1.º elemento da página
    var ref = document.body.firstElementChild;
    while (ref && ref.matches(".bf-faixa,#vip-faixa,script,style,noscript")) ref = ref.nextElementSibling;
    document.body.insertBefore(barra, ref);
    // «Início › Tema › Página» (o nome da página é o H1 dela)
    var h1 = document.querySelector("h1"), nome = h1 ? h1.textContent.replace(/\s+/g, " ").trim() : document.title.split(/[|·—:]/)[0].trim();
    var inicio = P === "/" || P === "/index";   // na página inicial não há «Início › …»
    var mig = document.createElement("nav"); mig.className = "gtm-migalhas"; mig.setAttribute("aria-label", "Onde está");
    mig.innerHTML = '<a href="/">Início</a> › ' + (meu >= 0 && TEMAS[meu][2] !== P ? '<a href="' + TEMAS[meu][2] + '">' + esc(TEMAS[meu][1]) + "</a> › " : "") + "<b>" + esc(nome.slice(0, 70)) + "</b>";
    if (!inicio) barra.parentNode.insertBefore(mig, barra.nextSibling);
    // a gaveta
    var veu = document.createElement("div"); veu.className = "gtm-veu";
    var g = document.createElement("aside"); g.className = "gtm-gaveta"; g.setAttribute("aria-label", "Menu");
    g.innerHTML = '<div class="gtm-g-topo"><a class="gtm-logo" href="/"><img src="/apple-touch-icon.png" alt="" width="32" height="32">Genial Tarot</a><button class="gtm-bt fecha" type="button" aria-label="Fechar o menu">✕</button></div>' +
      '<a class="gtm-pesq" href="/pesquisa">🔍 Pesquisar no site…</a>' +
      TEMAS.map(function (t, i) {
        return '<details class="gtm-sec"' + (i === meu ? " open" : "") + "><summary>" + t[0] + " " + esc(t[1]) + '</summary><div class="itens">' +
          [["Ver tudo de " + t[1] + " ›", t[2]]].concat(t[3].filter(function (x) { return x[1] !== t[2]; })).map(function (x) { return '<a href="' + x[1] + '"' + (x[1] === P ? ' class="aqui"' : "") + ">" + esc(x[0]) + (x[1] === P ? " ✓" : "") + "</a>"; }).join("") + "</div></details>";
      }).join("") +
      '<div class="gtm-base"><a class="c" href="/loja">🛍️ Loja</a><a class="c" href="/consulta-de-tarot-online">💬 Marcar consulta</a><a class="w" href="https://wa.me/351914920427" target="_blank" rel="noopener">WhatsApp</a></div>';
    document.body.appendChild(veu); document.body.appendChild(g);
    var ham = barra.querySelector(".ham");
    function abre(s) { document.documentElement.classList.toggle("gtm-aberto", s); ham.setAttribute("aria-expanded", s ? "true" : "false"); }
    ham.addEventListener("click", function (e) { e.preventDefault(); abre(true); });
    g.querySelector(".fecha").addEventListener("click", function () { abre(false); });
    veu.addEventListener("click", function () { abre(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") abre(false); });
    document.documentElement.classList.add("gtm-on");
    if (!/^\/loja/.test(P)) {
      var lf = document.createElement("a"); lf.className = "gtm-lojaf"; lf.href = "/loja"; lf.setAttribute("aria-label", "Loja Online");
      lf.innerHTML = '<span class="i">🛍️</span><span>Loja <b>Online</b></span>'; document.body.appendChild(lf);
      if ("IntersectionObserver" in window) new IntersectionObserver(function (e) { lf.classList.toggle("on", !e[0].isIntersecting); }).observe(barra);
    }
    // a etiqueta rosa «Loja Online» (vip-faixa.js, fixa à direita) desce para baixo da barra, senão tapa o 🔍 e o ☰
    function etiqueta() {
      var t = document.getElementById("loja-etq"); if (!t) return;
      var fundo = barra.getBoundingClientRect().bottom + (window.scrollY || 0) + 12;
      if (t.getBoundingClientRect().top < fundo) t.style.top = fundo + "px";
    }
    etiqueta(); setTimeout(etiqueta, 600); setTimeout(etiqueta, 2000);
    // o botão «Entrar» (conta.js) arruma-se de novo para não ficar por cima do 🔍 e do ☰
    setTimeout(function () { dispatchEvent(new Event("resize")); }, 50); setTimeout(function () { dispatchEvent(new Event("resize")); }, 1500);
  }
  if (document.body) monta(); else document.addEventListener("DOMContentLoaded", monta);
})();
