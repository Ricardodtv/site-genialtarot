/* destaque.js — 13/11/2026, pedido dele (com captura): «gosto do destaque a aparecer assim … deveria aparecer em todo o site e estar visível
   quando a pessoa abre a página por 8 segundos, e este estilo de destaque pode ser usado no futuro para outras coisas».
   Um só componente para TODOS os destaques do site. Carregado pelo vivo.js em todas as páginas.
   · ao abrir a página: o cartão entra, fica 8 s (barrinha dourada a contar) e sai; fica um botão redondo no canto para o reabrir
   · o × fecha-o até fechar o separador (fica só o botão redondo)
   · na página inicial há também a versão grande, logo a seguir ao topo
   Para acrescentar um destaque novo: uma entrada em DESTAQUES (o 1.º que estiver activo é o que aparece).
   Para ver um destaque fora do dia: ?destaque=<id>  (a sexta-feira 13 aceita também ?sexta13=hoje|amanha) */
(function () {
  if (window.__destaque) return; window.__destaque = 1;
  if (/^\/(consultorio|o-teu-ceu|pagar)(\/|\.html|-sala|$)/.test(location.pathname)) return;
  var SEGUNDOS = 8;
  var agora = new Date(new Date().toLocaleString("en-US", { timeZone: "Europe/Lisbon" }));
  var dia = function (d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); };
  var hoje = dia(agora), amanhaD = new Date(agora); amanhaD.setDate(agora.getDate() + 1);
  var q = new URLSearchParams(location.search);

  var GATO = '<svg viewBox="0 0 120 120" aria-hidden="true"><defs><radialGradient id="dsl" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#fff6dc"/><stop offset=".7" stop-color="#f3d58e"/><stop offset="1" stop-color="#c99a3f"/></radialGradient></defs>'
    + '<circle cx="60" cy="52" r="42" fill="url(#dsl)"/><path d="M38 116c-3-22 2-40 16-50l-4-20 13 11c4-1 8-1 12 0l13-11-4 20c14 10 19 28 16 50z" fill="#0b0408"/>'
    + '<ellipse class="dso" cx="57" cy="86" rx="3.5" ry="4.5" fill="#ffd34d"/><ellipse class="dso" cx="73" cy="86" rx="3.5" ry="4.5" fill="#ffd34d"/></svg>';

  /* ── a lista dos destaques ── cada um: id, activo() → true/false, titulo, texto, botao, link, arte (svg), e opcional pagina (onde NÃO aparece) */
  /* 27/11/2026 (ele): Black Friday −30% em tudo até domingo 23:59 — só com a promoção ligada no black-friday.js (todos os botões novos) */
  var ETIQ = '<svg viewBox="0 0 120 120" aria-hidden="true"><g transform="rotate(-12 60 60)"><path d="M60 6l9 12 15-4 2 15 15 5-6 14 10 12-13 8 1 15-15 1-6 14-14-6-13 9-8-13-15 1 1-15-13-8 10-12-6-14 15-5 2-15 15 4z" fill="#d81f2a" stroke="#ffd978" stroke-width="3"/>'
    + '<text x="60" y="58" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="900" font-size="30" fill="#fff">−30%</text>'
    + '<text x="60" y="80" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="11" letter-spacing="1" fill="#ffd978">BLACK FRIDAY</text></g></svg>';
  var DESTAQUES = [
    { id: "blackfriday", classe: "dst-bf", antes: "section.hero form.gtp", pagina: /^\/(loja|promo)(\.html)?$/,   // 27/11: nem na página do pack (/promo)
      activo: function () { return !!(window.BF && window.BF.ativo); },
      titulo: "Black Friday: −30% em tudo",
      texto: "Consultas, mapas, amuletos e cursos com 30% de desconto. Só até domingo à meia-noite.",
      botao: "Ver as ofertas →",
      link: "/loja?de=site&c=destaque-black-friday",
      arte: ETIQ, imagem: "/black-friday-2026.webp", imagemMini: "/black-friday-2026-mini.webp", marca: "%",
      fim: function () { return window.BF && window.BF.fim; } },   // 27/11 (ele): contagem decrescente por cima da imagem   // a imagem é a dele (27/11)
    /* 27/11/2026 (ele): a Revista do mês (revista-gerar.py, sai sozinha no dia 1) — em destaque do dia 1 ao dia 10 de cada mês.
       Nunca na própria revista. Liga sozinho a 01/12/2026 (a Black Friday acaba a 29/11). */
    { id: "revista", pagina: /^\/revista/,
      activo: function () { return hoje >= "2026-12-01" && agora.getDate() <= 10 && (agora.getDate() > 1 || agora.getHours() >= 6); },   // no dia 1 só a partir das 6h: a revista nasce às 00:05 e o site leva uns minutos a publicar
      titulo: function () { return "Já saiu a Revista de " + ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"][agora.getMonth()]; },
      texto: "As luas, o céu do mês, os 12 signos, o seu Mês Pessoal e a carta do Mestre. Folheie como uma revista.",
      botao: "Abrir a revista →",
      link: function () { return "/revista-" + ["janeiro","fevereiro","marco","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"][agora.getMonth()] + "-" + agora.getFullYear() + "?de=site&c=destaque-revista"; },
      arte: '<svg viewBox="0 0 120 120" aria-hidden="true"><g transform="rotate(-8 60 60)"><rect x="26" y="14" width="68" height="92" rx="5" fill="#3a1670" stroke="#f2c96b" stroke-width="4"/>'
        + '<text x="60" y="42" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="900" font-size="17" fill="#f2c96b">GENIAL</text>'
        + '<circle cx="60" cy="70" r="17" fill="#f2c96b"/><circle cx="66" cy="65" r="13" fill="#3a1670"/><path d="M36 94h48M36 100h30" stroke="#f2c96b" stroke-width="3"/></g></svg>',
      marca: "N.º" },
    { id: "sexta13", pagina: /^\/sexta-feira-13(\.html)?$/,
      activo: function () {
        var f = q.get("sexta13"); if (f === "hoje" || f === "amanha") { this.modo = f; return true; }
        if (agora.getDate() === 13 && agora.getDay() === 5) { this.modo = "hoje"; return true; }
        if (amanhaD.getDate() === 13 && amanhaD.getDay() === 5) { this.modo = "amanha"; return true; }
        return false;
      },
      titulo: function () { return this.modo === "hoje" ? "Hoje é Sexta-feira 13" : "Amanhã é Sexta-feira 13"; },
      texto: function () { return this.modo === "hoje" ? "O dia mais misterioso do calendário chegou. Descubra a origem do medo e como virar a sorte a seu favor."
                                                      : "Prepare-se para o dia mais misterioso do calendário: a origem, as lendas e como virar a sorte."; },
      botao: "Descobrir o mistério →",
      link: function () { return "/sexta-feira-13?de=site&c=destaque-" + this.modo; },
      arte: GATO, marca: "13" }
    /* exemplo para o futuro:
    ,{ id: "natal", activo: function () { return hoje >= "2026-12-20" && hoje <= "2026-12-25"; }, titulo: "…", texto: "…", botao: "Ver →", link: "/…", arte: "<svg…>" } */
  ];
  var val = function (x, d) { return typeof x === "function" ? x.call(d) : x; };
  var D = null;
  for (var i = 0; i < DESTAQUES.length; i++) {
    var d = DESTAQUES[i];
    if (d.pagina && d.pagina.test(location.pathname)) continue;
    if (q.get("destaque") === d.id || d.activo()) { if (q.get("destaque") === d.id && !d.modo) d.modo = "hoje"; D = d; break; }
  }
  if (!D) return;
  var inicio = location.pathname === "/" || /^\/index(\.html)?$/.test(location.pathname);
  var fechado = false; try { fechado = !!sessionStorage.getItem("dst-fechado-" + D.id); } catch (e) {}

  var css = ''
    + '.dst{font-family:Inter,system-ui,sans-serif;color:#f6eef4;text-decoration:none;display:flex;align-items:center;gap:1rem;box-sizing:border-box;'
    + 'background:radial-gradient(ellipse at 15% 0%,#5c1748 0%,#2a0a24 45%,#12050f 100%);border:1px solid rgba(255,217,120,.45);box-shadow:0 0 0 1px rgba(255,217,120,.15),0 18px 50px -10px rgba(160,40,110,.7)}'
    + '.dst svg{flex:none;filter:drop-shadow(0 0 14px rgba(255,215,120,.55))}'
    + '.dst .dt{font-family:Cinzel,"Cormorant Garamond",Georgia,serif;font-weight:900;color:#ffd978;letter-spacing:.02em;line-height:1.1;display:block}'
    + '.dst .dp{display:block;color:#e6d3e0;line-height:1.4}'
    + '.dst .db{display:inline-block;margin-top:.55rem;padding:.5rem 1.1rem;border-radius:999px;font-weight:800;color:#2a0c18;background:linear-gradient(135deg,#ffe9a6,#e2a93a);animation:dstp 1.8s ease-out infinite}'
    + '.dso{animation:dstpi 4.5s infinite;transform-box:fill-box;transform-origin:center}'
    + '@keyframes dstpi{0%,46%,50%,100%{transform:scaleY(1)}48%{transform:scaleY(.1)}}'
    + '@keyframes dstp{0%{box-shadow:0 0 0 0 rgba(255,215,120,.7)}80%,100%{box-shadow:0 0 0 12px rgba(255,215,120,0)}}'
    + '.dst-grande{position:relative;width:min(60rem,calc(100% - 2rem));margin:1.2rem auto 1.6rem;border-radius:1.5rem;padding:1.2rem 1.6rem;overflow:hidden}'
    + '.dst-grande svg{width:8.5rem;height:8.5rem}.dst-grande .dt{font-size:clamp(1.5rem,4.4vw,2.4rem)}.dst-grande .dp{font-size:1.02rem;margin-top:.35rem}'
    + '.dst-grande .dn{position:absolute;right:-.5rem;bottom:-2.6rem;font:900 9rem/1 Cinzel,serif;color:rgba(255,217,120,.09);pointer-events:none}'
    + '.dst-flut{position:fixed;left:1rem;bottom:1rem;z-index:9998;width:min(23rem,calc(100% - 2rem));border-radius:1.2rem;padding:.8rem 2.2rem 1rem .8rem;overflow:hidden;'
    + 'transition:transform .55s cubic-bezier(.5,0,.75,0),opacity .55s;animation:dste .6s ease-out}'
    + '.dst-flut.sai{transform:translateY(130%);opacity:0;pointer-events:none}'
    + '.dst-flut svg{width:4.4rem;height:4.4rem}.dst-flut .dt{font-size:1.12rem}.dst-flut .dp{font-size:.84rem;margin-top:.2rem}.dst-flut .db{font-size:.85rem;padding:.4rem .9rem;margin-top:.4rem}'
    + '.dst-flut .dtempo{position:absolute;left:0;bottom:0;height:4px;width:100%;background:linear-gradient(90deg,#ffe9a6,#e2a93a);transform-origin:left;animation:dstt ' + SEGUNDOS + 's linear forwards}'
    + '.dst-flut:hover .dtempo{animation-play-state:paused}'
    + '@keyframes dstt{from{transform:scaleX(1)}to{transform:scaleX(0)}}'
    + '.dstx{position:absolute;right:.3rem;top:.3rem;width:28px;height:28px;border:0;border-radius:50%;background:transparent;color:#fff;opacity:.65;font-size:17px;cursor:pointer}'
    + '.dst-bola{position:fixed;left:1rem;bottom:1rem;z-index:9998;width:58px;height:58px;border-radius:50%;padding:0;cursor:pointer;display:grid;place-items:center;'
    + 'background:radial-gradient(circle at 30% 20%,#5c1748,#12050f);border:1.5px solid rgba(255,217,120,.7);box-shadow:0 8px 26px -6px rgba(160,40,110,.9);transform:scale(0);transition:transform .35s cubic-bezier(.3,1.6,.6,1)}'
    + '.dst-bola.ve{transform:scale(1);animation:dstp 2.4s ease-out infinite}'
    + '.dst-bola svg{width:46px;height:46px}'
    + '.dst-bola b{position:absolute;right:-4px;top:-4px;min-width:22px;height:22px;border-radius:11px;background:linear-gradient(135deg,#ffe9a6,#e2a93a);color:#2a0c18;font:900 11px/22px Cinzel,serif;text-align:center}'
    + '@keyframes dste{from{transform:translateY(120%);opacity:0}to{transform:none;opacity:1}}'
    + '@media (max-width:560px){.dst-grande{flex-direction:column;text-align:center}.dst-grande svg{width:6.5rem;height:6.5rem}}'
    + '.dst.dst-bf,.dst-bola.dst-bf{background:radial-gradient(ellipse at 15% 0%,#4a1470 0%,#1c0630 45%,#07010d 100%);box-shadow:0 0 0 1px rgba(255,217,120,.2),0 18px 50px -10px rgba(170,60,255,.7)}'
    + '.dst .dst-img{flex:none;display:block;border-radius:.9rem;border:1px solid rgba(255,217,120,.5);box-shadow:0 0 18px rgba(190,90,255,.55)}'
    + '.dst-grande .dst-img{width:min(24rem,42%);height:auto}.dst-flut .dst-img{width:6.5rem;height:auto;border-radius:.6rem}'
    + '@media (max-width:560px){.dst-grande .dst-img{width:100%}}'
    + '.dst-grande.dst-bf{animation:dstbf 1.7s ease-in-out infinite;border:2px solid #ffd978;text-align:left}'
    + '@keyframes dstbf{0%,100%{transform:scale(1);box-shadow:0 0 0 0 rgba(216,31,42,.75),0 18px 50px -10px rgba(216,31,42,.7)}50%{transform:scale(1.015);box-shadow:0 0 0 14px rgba(216,31,42,0),0 18px 60px -6px rgba(255,120,60,.85)}}'
    + '.dst-cxi{position:relative;flex:none;display:block;line-height:0}.dst-grande .dst-cxi{width:min(24rem,42%)}.dst-grande .dst-cxi .dst-img{width:100%}'
    + '.dst-cd{position:absolute;left:50%;top:.6rem;transform:translateX(-50%);white-space:nowrap;line-height:1.15;text-align:center;padding:.35rem .9rem;border-radius:.8rem;'
    + 'background:rgba(10,2,16,.82);border:1.5px solid #ffd978;box-shadow:0 0 18px rgba(216,31,42,.75);color:#ffe9a6;font:700 1rem/1.15 Inter,system-ui,sans-serif;font-variant-numeric:tabular-nums}'
    + '.dst-cd small{display:block;font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:#ff8a8a;font-weight:800}'
    + '.dst-cd b{font-family:Cinzel,Georgia,serif;font-size:1.35em;font-weight:900;color:#fff}'
    + '.dst-flut .dst-cd{top:auto;bottom:.25rem;padding:.1rem .35rem;font-size:.6rem;border-width:1px;border-radius:.4rem}'
    + '@media (max-width:560px){.dst-grande .dst-cxi{width:100%}}'
    + '@media (prefers-reduced-motion:reduce){.dst *,.dst,.dst-bola{animation:none!important;transition:none!important}}';

  function conteudo(grande) {
    var arte = D.imagem ? '<img class="dst-img" alt="" src="' + (grande ? D.imagem : (D.imagemMini || D.imagem)) + '">' : D.arte;
    if (D.imagem && D.fim && val(D.fim, D)) arte = '<span class="dst-cxi">' + arte + '<span class="dst-cd" aria-label="Tempo até ao fim">'
      + (grande ? '<small>Termina em</small>' : '') + '<span class="dst-cdt">' + contagem() + '</span></span></span>';
    return arte + '<span><span class="dt">' + val(D.titulo, D) + '</span><span class="dp">' + val(D.texto, D) + '</span><span class="db">' + D.botao + '</span></span>';
  }
  function contagem() {
    var s = Math.max(0, Math.floor((val(D.fim, D) - Date.now()) / 1000)), d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
    var z = function (n) { return ("0" + n).slice(-2); };
    return (d ? '<b>' + d + '</b>d ' : '') + '<b>' + z(h) + '</b>h <b>' + z(m) + '</b>m <b>' + z(x) + '</b>s';
  }
  function montar() {
    if (document.querySelector(".dst-flut,.dst-bola")) return;
    if (D.fim && val(D.fim, D)) setInterval(function () {
      var c = contagem(); Array.prototype.forEach.call(document.querySelectorAll(".dst-cdt"), function (e) { e.innerHTML = c; });
    }, 1000);
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var link = val(D.link, D);
    if (inicio) {
      var g = document.createElement("a"); g.href = link; g.className = "dst dst-grande" + (D.classe ? " " + D.classe : "");
      g.innerHTML = conteudo(true) + (D.marca ? '<span class="dn" aria-hidden="true">' + D.marca + '</span>' : "");
      var heroi = document.querySelector("section.hero"), ant = D.antes && document.querySelector(D.antes);
      if (ant && ant.parentNode) ant.parentNode.insertBefore(g, ant);   // 27/11: a Black Friday vai acima da pesquisa, à vista logo ao abrir
      else if (heroi && heroi.parentNode) heroi.parentNode.insertBefore(g, heroi.nextSibling); else document.body.insertBefore(g, document.body.firstChild);
    }
    var f = document.createElement("a"); f.href = link; f.className = "dst dst-flut" + (D.classe ? " " + D.classe : "") + (fechado ? " sai" : "");
    f.innerHTML = conteudo() + '<button class="dstx" aria-label="Fechar">×</button><span class="dtempo"></span>';
    var b = document.createElement("button"); b.className = "dst-bola" + (D.classe ? " " + D.classe : ""); b.setAttribute("aria-label", val(D.titulo, D));
    b.innerHTML = D.arte + (D.marca ? "<b>" + D.marca + "</b>" : "");
    document.body.appendChild(f); document.body.appendChild(b);
    var temp = null;
    function esconde() { clearTimeout(temp); f.classList.add("sai"); setTimeout(function () { b.classList.add("ve"); }, 350); }
    function mostra() {
      b.classList.remove("ve"); f.classList.remove("sai");
      var t = f.querySelector(".dtempo"); t.style.animation = "none"; void t.offsetWidth; t.style.animation = "";
      clearTimeout(temp); temp = setTimeout(esconde, SEGUNDOS * 1000);
    }
    var pausado = 0;
    f.addEventListener("mouseenter", function () { clearTimeout(temp); pausado = 1; });
    f.addEventListener("mouseleave", function () { if (pausado) { pausado = 0; temp = setTimeout(esconde, 2500); } });
    f.querySelector(".dstx").addEventListener("click", function (e) {
      e.preventDefault(); e.stopPropagation(); esconde(); try { sessionStorage.setItem("dst-fechado-" + D.id, "1"); } catch (er) {}
    });
    b.addEventListener("click", mostra);
    if (fechado) b.classList.add("ve"); else temp = setTimeout(esconde, SEGUNDOS * 1000);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();
