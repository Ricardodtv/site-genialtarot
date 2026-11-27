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
    ["🔮", "Horóscopo", "/horoscopo-do-dia", [["Do dia", "/horoscopo-do-dia"], ["De amanhã", "/horoscopo-de-amanha"], ["Semanal", "/horoscopo-semanal"], ["Fim de semana", "/fimdesemana"],
      ["Horóscopo 2027", "/horoscopo-2027"], ["Os 12 signos", "/signos-do-zodiaco"], ["Compatibilidade", "/compatibilidade"], ["Horóscopo chinês", "/horoscopo-chines"]], /^\/(horoscopo|signo\/|fimdesemana|signos-|compat|melhores-signos)/],
    ["🃏", "Tarot", "/tarot-gratis", [["Tarot grátis", "/tarot-gratis"], ["A carta do dia", "/tiragem-carta-do-dia"], ["Os Arcanos Maiores", "/arcanos"], ["Os Arcanos Menores", "/arcanos-menores"],
      ["Tarot do amor", "/tarot-do-amor"], ["Tarot por tema", "/tarot-por-tema"], ["Tarot terapêutico", "/tarot-terapeutico"], ["Tarot cigano", "/tarot-cigano"]], /^\/(tarot|tiragem|arcano|carta-|amor-do-dia|leia-o-tarot)/],
    ["🪐", "Astrologia", "/mapa-astral", [["Mapa astral", "/mapa-astral"], ["Ascendente", "/ascendente"], ["Calendário lunar", "/lua"], ["Notícias do céu", "/noticias-do-ceu"],
      ["Efemérides", "/efemerides"], ["Retrógrados 2027", "/retrogrados-2027"], ["Eclipses 2027", "/eclipses-2027"], ["Famosos com o seu céu", "/famosos-ceu"]], /^\/(mapa-astral|ascendente|lua|noticias|efemerides|retrogrados|eclipses|mercurio|famosos|astrolog|alinhamento|decanatos)/],
    ["🔢", "Numerologia", "/numerologia", [["Os números da sua vida", "/numerologia"], ["Calculadora 2027", "/numerologia-2027"]].concat([1, 2, 3, 4, 5, 6, 7, 8, 9].map(function (n) { return ["Ano Pessoal " + n, "/ano-pessoal-" + n + "-2027"]; })), /^\/(numerolog|ano-pessoal)/],
    ["🙏", "Fé e tradição", "/rezas-e-oracoes", [["Rezas e orações", "/rezas-e-oracoes"], ["Benzimentos", "/benzimentos"], ["Rezas de proteção", "/rezas-de-protecao"], ["Salmos", "/salmos"],
      ["Anjo da guarda", "/anjo-da-guarda"], ["Sonhos", "/sonhos"], ["Pêndulo", "/pendulo"], ["Quiromancia", "/quiromancia"]], /^\/(reza|benz|salmo|anjo|sonho|pendulo|quiromancia)/],
    ["📖", "Revista", "/revista", [["A revista do mês", "/revista"]], /^\/revista/]
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
    "html.gtm-on .topo .backlink,html.gtm-on .gtp-topo,html.gtm-on .voltar-barra .voltar,html.gtm-on a.voltar{display:none!important}html.gtm-on header.topo{min-height:0;padding:0}html.gtm-on body>header:has(>nav.container.nav){display:none}";

  function monta() {
    if (document.querySelector(".gtm-barra")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var barra = document.createElement("header"); barra.className = "gtm-barra";
    barra.innerHTML = '<a class="gtm-logo" href="/"><img src="/apple-touch-icon.png" alt="" width="32" height="32">Genial Tarot</a>' +
      '<nav class="gtm-links" aria-label="Temas">' + TEMAS.map(function (t, i) { return '<a href="' + t[2] + '"' + (i === meu ? ' class="aqui"' : "") + ">" + (t[1] === "Revista" ? "📖 " : "") + esc(t[1]) + "</a>"; }).join("") + '<a href="/loja">Loja</a></nav>' +
      '<span class="gtm-esp"></span><a class="gtm-cons" href="/consulta-de-tarot-online">💬 Consulta</a>' +
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
          t[3].map(function (x) { return '<a href="' + x[1] + '"' + (x[1] === P ? ' class="aqui"' : "") + ">" + esc(x[0]) + (x[1] === P ? " ✓" : "") + "</a>"; }).join("") + "</div></details>";
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
