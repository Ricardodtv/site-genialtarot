/* 🌙 «Amanhã para o seu signo» — 15/11/2026 (O-450, aba Voltar: só 3% das pessoas voltam noutro dia).
   No fim das páginas muito vistas (horóscopo do dia, tarot grátis, fichas dos signos) dá uma razão concreta para voltar amanhã:
   a primeira metade da frase-chave de amanhã (a mesma do O Meu Dia, de /horoscopo-dia/<amanhã>.json); o resto abre amanhã.
   O signo: o guardado neste aparelho (localStorage «gt_meudia», escrito em /o-meu-dia), ou o da página /signo/<x>; sem nenhum,
   mostra os 12 signos e um toque leva a /o-meu-dia já com o signo escolhido (?s=<slug>). Marca ?de=amanha&c=<página>.
   Hábito sim, pressão não: sem contagens, sem medo, sem «só hoje». Entra antes do bloco gt-casa (ou do rodapé). */
(function () {
  "use strict";
  if (document.getElementById("gt-amanha")) return;
  var SLUGS = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"];
  var PT = (Intl.DateTimeFormat().resolvedOptions().timeZone || "").indexOf("Europe") === 0;
  var N = PT ? ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
             : ["Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem", "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"];
  var G = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"];
  var ESC = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var pag = location.pathname.replace(/^\/|\.html$/g, "").replace(/\//g, "-").slice(0, 40) || "inicio";
  var ir = function (slug) { return "/o-meu-dia?" + (slug ? "s=" + slug + "&" : "") + "de=amanha&c=" + encodeURIComponent(pag); };

  var guardado = null;
  try { var E = JSON.parse(localStorage.getItem("gt_meudia") || "null"); if (E && E.signo != null) guardado = +E.signo; } catch (e) {}
  var m = location.pathname.match(/^\/signo\/([a-z]+)/), daPagina = m ? SLUGS.indexOf(m[1]) : -1;
  var s = guardado != null ? guardado : daPagina >= 0 ? daPagina : null;

  var css = document.createElement("style");
  css.textContent =
    "#gt-amanha{max-width:620px;margin:2.2rem auto 1rem;padding:0 14px;font-family:inherit}" +
    "#gt-amanha .ga-cx{border-radius:20px;padding:1.3rem 1.2rem 1.2rem;text-align:center;color:#f7f0fb;" +
    "background:linear-gradient(160deg,rgba(40,20,70,.92),rgba(22,12,40,.95));border:1px solid rgba(242,201,107,.5);box-shadow:0 10px 30px rgba(0,0,0,.35)}" +
    "#gt-amanha .ga-eti{font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:#f2c96b}" +
    "#gt-amanha .ga-frase{font-family:Cinzel,Georgia,serif;font-size:clamp(1.15rem,4.4vw,1.45rem);line-height:1.35;margin:.55rem 0 .4rem;color:#ffe2a0}" +
    "#gt-amanha .ga-frase span{opacity:.45;filter:blur(2.5px);user-select:none}" +
    "#gt-amanha .ga-sub{font-size:.92rem;color:#e7dcf3;line-height:1.5;margin:0 0 .9rem}" +
    "#gt-amanha .ga-bot{display:inline-block;padding:.72rem 1.25rem;border-radius:999px;font-weight:700;text-decoration:none;color:#2a1245;" +
    "background:linear-gradient(135deg,#ffe2a0,#f2c96b 55%,#d9a441);box-shadow:0 6px 18px rgba(242,201,107,.3)}" +
    "#gt-amanha .ga-bot:hover{filter:brightness(1.08)}" +
    "#gt-amanha .ga-12{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:.2rem}" +
    "#gt-amanha .ga-12 a{display:flex;flex-direction:column;align-items:center;gap:1px;padding:.5rem .2rem;border-radius:12px;text-decoration:none;color:#f7f0fb;" +
    "background:rgba(255,255,255,.06);border:1px solid rgba(242,201,107,.22);font-size:.82rem}" +
    "#gt-amanha .ga-12 a:hover,#gt-amanha .ga-12 a:focus-visible{background:rgba(242,201,107,.14);border-color:#f2c96b}" +
    "#gt-amanha .ga-12 i{font-style:normal;font-size:1.3rem;line-height:1.2}" +
    "@media (max-width:380px){#gt-amanha .ga-12{grid-template-columns:repeat(3,1fr)}}";

  var caixa = document.createElement("aside");
  caixa.id = "gt-amanha"; caixa.setAttribute("aria-label", "Amanhã para o seu signo");

  function mostra(html) {
    caixa.innerHTML = '<div class="ga-cx">' + html + "</div>";
    var antes = document.querySelector("aside.gt-casa") || document.querySelector("footer");
    if (!antes || !antes.parentNode) return;
    document.head.appendChild(css);
    antes.parentNode.insertBefore(caixa, antes);
  }

  if (s == null) {
    // sem signo: um toque escolhe-o e abre O Meu Dia já com ele
    mostra('<div class="ga-eti">🌙 Amanhã para o seu signo</div>' +
      '<p class="ga-sub" style="margin-top:.5rem">Escolha o seu signo e fica guardado neste aparelho. Todas as manhãs encontra lá o seu horóscopo, a sua carta e a primeira frase do dia seguinte.</p>' +
      '<nav class="ga-12">' + N.map(function (n, i) { return '<a href="' + ir(SLUGS[i]) + '"><i aria-hidden="true">' + G[i] + "︎</i>" + n + "</a>"; }).join("") + "</nav>");
    return;
  }

  var d = new Date(); d.setDate(d.getDate() + 1);
  var amanha = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  var botao = guardado != null ? "Abrir o meu dia →" : "Guardar " + N[s] + " e ver amanhã →";
  var link = ir(guardado != null ? "" : SLUGS[s]);
  fetch("/horoscopo-dia/" + amanha + ".json").then(function (r) { if (!r.ok) throw r.status; return r.json(); }).then(function (x) {
    var k = ESC(x.s[s].k).replace(/\{S:(\d+)\}/g, function (_, n) { return N[+n]; }).split(" "), meio = Math.max(2, Math.ceil(k.length / 2));
    mostra('<div class="ga-eti">🌙 Amanhã para ' + N[s] + " " + G[s] + "︎</div>" +
      '<p class="ga-frase">«' + k.slice(0, meio).join(" ") + ' <span aria-hidden="true">' + k.slice(meio).join(" ").replace(/./g, function (c) { return c === " " ? " " : "•"; }) + "</span>»</p>" +
      '<p class="ga-sub">A frase inteira abre amanhã de manhã, no O Meu Dia, com a sua carta e a Lua.</p>' +
      '<a class="ga-bot" href="' + link + '">' + botao + "</a>");
  }).catch(function () {
    mostra('<div class="ga-eti">🌙 Amanhã para ' + N[s] + " " + G[s] + "︎</div>" +
      '<p class="ga-sub" style="margin-top:.5rem">Todas as manhãs, o seu horóscopo, a sua carta e a Lua, num só sítio.</p>' +
      '<a class="ga-bot" href="' + link + '">' + botao + "</a>");
  });
})();
