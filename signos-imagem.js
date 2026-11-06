/* Pedido dele (06/11/2026): em todo o site, o símbolo gráfico de cada signo dá lugar à nossa imagem, com o tamanho a acompanhar o texto.
   Um só ficheiro, carregado por vivo.js: cobre páginas novas e o que aparece depois de a página abrir.
   Fica com o símbolo o que não aceita imagem (títulos, listas de escolha, campos) e os mapas em SVG e canvas.
   Se a mesma imagem já está ao lado (cartão, linha de tabela), o símbolo sai em vez de a repetir.
   Tabelas técnicas ficam com o símbolo: é leitura rápida, e a 20 px as imagens não se distinguem.
   Para excluir um bloco: data-sem-signo-img. */
(function () {
  var NOMES = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"];
  var ROTULO = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"];
  var TECNICAS = /^\/(efemerides)(\/|\.html|$)/;
  if (TECNICAS.test(location.pathname)) return;
  var RE = /[♈-♓][︎️]?/g;
  var SALTA = /^(SCRIPT|STYLE|TITLE|TEXTAREA|OPTION|SELECT|INPUT|CANVAS|NOSCRIPT|TEMPLATE|svg|text|tspan|textPath)$/;
  function poeEstilo() {
    if (document.getElementById("sg-img-css")) return;
    var c = document.createElement("style"); c.id = "sg-img-css";
    c.textContent = "img.sg-img{display:inline-block;width:1.45em;height:1.45em;min-width:20px;min-height:20px;vertical-align:-.36em;margin:0 .12em;border-radius:50%;object-fit:cover;max-width:none}"
      + "h1 img.sg-img,h2 img.sg-img,h3 img.sg-img{width:1.2em;height:1.2em;vertical-align:-.2em}"
      + ".anel i img.sg-img,.mini-roda-anel i img.sg-img{position:static;inset:auto;width:100%;height:100%;min-width:0;min-height:0;margin:0;vertical-align:top;border:0}";
    document.head.appendChild(c);
  }
  function excluido(n) {
    for (var p = n.parentNode; p && p.nodeType === 1; p = p.parentNode) {
      if (SALTA.test(p.nodeName) || p.isContentEditable || p.hasAttribute("data-sem-signo-img")) return true;
    }
    return false;
  }
  // A foto do signo já à vista no mesmo cartão ou linha: procura até 4 níveis acima, sem sair da secção.
  function jaEstaAoLado(i, pai) {
    var nn = ("0" + i).slice(-2), n = 0;
    for (var p = pai; p && p.nodeType === 1 && n < 4 && !/^(BODY|MAIN|SECTION|TABLE|TBODY|UL|OL|NAV)$/.test(p.nodeName); p = p.parentNode, n++) {
      var q = p.getElementsByTagName("img");
      for (var k = 0; k < q.length; k++) {
        var src = q[k].getAttribute("src") || "";
        if (q[k].className !== "sg-img" && (src.indexOf("signo-" + NOMES[i]) > -1 || src.indexOf("/signos/" + nn + ".webp") > -1)) return true;
      }
    }
    return false;
  }
  function imagem(i, pai) {
    var g = new Image(), fs = parseFloat(getComputedStyle(pai).fontSize) || 16;
    g.src = fs > 32 ? "/signos/signo-" + NOMES[i] + ".webp" : "/signos/m/" + NOMES[i] + ".webp";
    g.className = "sg-img"; g.decoding = "async"; g.draggable = false;
    g.alt = (pai.textContent || "").toLowerCase().indexOf(ROTULO[i].toLowerCase()) > -1 ? "" : ROTULO[i];
    return g;
  }
  function troca(t) {
    var s = t.nodeValue, pai = t.parentNode, f = document.createDocumentFragment(), u = 0, m;
    RE.lastIndex = 0;
    while ((m = RE.exec(s))) {
      if (m.index > u) f.appendChild(document.createTextNode(s.slice(u, m.index)));
      var c = m[0].charCodeAt(0) - 0x2648;
      if (!jaEstaAoLado(c, pai)) f.appendChild(imagem(c, pai));
      u = m.index + m[0].length;
    }
    if (u < s.length) f.appendChild(document.createTextNode(s.slice(u)));
    pai.replaceChild(f, t);
  }
  function anda(r) {
    var w = document.createTreeWalker(r, NodeFilter.SHOW_TEXT), l = [], n;
    while ((n = w.nextNode())) { RE.lastIndex = 0; if (RE.test(n.nodeValue) && !excluido(n)) l.push(n); }
    for (var i = 0; i < l.length; i++) troca(l[i]);
  }
  function arranca() {
    poeEstilo(); anda(document.body);
    new MutationObserver(function (ms) {
      for (var i = 0; i < ms.length; i++) {
        if (ms[i].type === "characterData") { var t = ms[i].target; if (t.parentNode) anda(t.parentNode); continue; }
        var a = ms[i].addedNodes;
        for (var j = 0; j < a.length; j++) {
          if (a[j].nodeType === 1 && a[j].parentNode) anda(a[j]);
          else if (a[j].nodeType === 3 && a[j].parentNode) anda(a[j].parentNode);
        }
      }
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
  }
  if (document.body) arranca(); else document.addEventListener("DOMContentLoaded", arranca);
})();
