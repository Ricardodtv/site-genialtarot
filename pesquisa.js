/* pesquisa.js — 16/11/2026, pedido dele: «colocar uma pesquisa na página principal para poder rapidamente encontrar conteúdo:
   coloco uma palavra e mostras tudo o que está relacionado com essa palavra no site para a pessoa escolher».
   Serve a caixa da página principal (lista por baixo da caixa) e a página /pesquisa (lista completa na página).
   O índice (pesquisa-indice.json, gerado pelo gerar-pesquisa.py no pre-commit) só se carrega quando a pessoa foca ou escreve.
   Sem acentos e sem maiúsculas; várias palavras = todas têm de aparecer; o título pesa mais do que a descrição;
   nomes do Brasil (câncer, libra, áries) encontram os de Portugal e ao contrário. */
(function () {
  "use strict";
  var INDICE = "/pesquisa-indice.json", dados = null, aCarregar = null;
  var SIN = { cancer: ["caranguejo"], caranguejo: ["cancer"], libra: ["balanca"], balanca: ["libra"], aries: ["carneiro"], carneiro: ["aries"],
    sonho: ["sonhar"], sonhar: ["sonho"], sonhos: ["sonhar", "sonho"], reza: ["benzedura", "benzer"], rezas: ["reza", "benzedura"], oracao: ["reza"],
    oracoes: ["oracao", "reza"], cigana: ["cigano"], cigano: ["cigana"] };
  var VAZIAS = { de: 1, da: 1, do: 1, das: 1, dos: 1, o: 1, a: 1, os: 1, as: 1, e: 1, com: 1, em: 1, no: 1, na: 1, nos: 1, nas: 1,
    um: 1, uma: 1, para: 1, pra: 1, por: 1, que: 1, se: 1, ao: 1, aos: 1, meu: 1, minha: 1 };

  function norm1(c) { var n = c.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); return n.length === 1 ? n : c.toLowerCase().charAt(0) || " "; }
  function norm(s) { return String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim(); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function carregar() {
    if (dados) return Promise.resolve(dados);
    if (aCarregar) return aCarregar;
    aCarregar = fetch(INDICE).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (j) {
      j.p.forEach(function (p) {
        p.nt = " " + norm(p[1]) + " "; p.nu = " " + norm(p[0]) + " "; p.nx = " " + norm(p[4]) + " "; p.nd = " " + norm(p[2]) + " ";
      });
      return (dados = j);
    });
    aCarregar.catch(function () { aCarregar = null; });
    return aCarregar;
  }

  function palavras(q) {
    var t = norm(q).split(" ").filter(Boolean), uteis = t.filter(function (x) { return !VAZIAS[x] && (x.length > 1 || /\d/.test(x)); });
    if (!uteis.length) uteis = t;
    return uteis.map(function (x) {
      var alts = [x].concat(SIN[x] || []);
      if (x.length > 4 && /s$/.test(x)) alts.push(x.replace(/(oe|ae)s$/, "ao").replace(/s$/, ""));   // anjos → anjo, orações → oracao
      return alts;
    });
  }

  function pontua(p, toks, frase) {
    var tot = 0;
    for (var i = 0; i < toks.length; i++) {
      var melhor = 0;
      for (var j = 0; j < toks[i].length; j++) {
        var a = toks[i][j], s = 0;
        // Só conta a palavra inteira ou o começo de uma palavra («reza» não apanha «natureza»); o plural vale como a palavra
        if (p.nt.indexOf(" " + a + " ") >= 0 || p.nt.indexOf(" " + a + "s ") >= 0) s = 12;   // palavra inteira no título
        else if (p.nt.indexOf(" " + a) >= 0) s = 9;              // começo de palavra no título
        else if (p.nu.indexOf(" " + a) >= 0) s = 5;              // no endereço
        else if (p.nx.indexOf(" " + a) >= 0) s = 4;              // nos subtítulos da página
        else if (p.nd.indexOf(" " + a) >= 0) s = 3;              // na descrição
        if (j > 0) s = s * 0.8;                                  // o sinónimo vale um pouco menos do que a palavra escrita
        if (s > melhor) melhor = s;
      }
      if (!melhor) return 0;
      tot += melhor;
    }
    if (frase.length > 2) {
      if (p.nt.indexOf(" " + frase + " ") >= 0 || p.nt.indexOf(" " + frase + "s ") >= 0) tot += 15; else if (p.nt.indexOf(" " + frase) >= 0) tot += 10;
    }
    // Uma palavra só, igual ao fim do endereço (/signo/touro, /signo/caranguejo para «câncer»): é a página dessa coisa
    if (toks.length === 1) { var fim = p.nu.trim().split(" ").slice(-1)[0]; if (toks[0].indexOf(fim) >= 0) tot += 8; }
    // As páginas-mãe (mais ligações no site) e as secções principais sobem um pouco; em empate, o título mais curto primeiro
    return tot + (p[5] || 0) * 0.8 + (dados.cats.length - p[3]) * 0.4 - Math.min(p[1].length, 90) / 90;
  }

  function procurar(q) {
    var toks = palavras(q), frase = norm(q), res = [];
    if (!toks.length || !dados) return { grupos: [], total: 0 };
    dados.p.forEach(function (p) { var s = pontua(p, toks, frase); if (s > 0) res.push({ p: p, s: s }); });
    res.sort(function (a, b) { return b.s - a.s; });
    var g = {}, ordem = [];
    res.forEach(function (r) { var k = r.p[3]; if (!g[k]) { g[k] = { nome: dados.cats[k], k: k, itens: [], melhor: r.s }; ordem.push(g[k]); } g[k].itens.push(r.p); });
    return { grupos: ordem, total: res.length, toks: toks };
  }

  // Realça no título as palavras encontradas (comparando sem acentos, letra a letra)
  function realca(txt, toks) {
    var n = "", i;
    for (i = 0; i < txt.length; i++) n += norm1(txt.charAt(i));
    var marca = new Array(txt.length + 1).join("0").split("");
    toks.forEach(function (alts) {
      alts.forEach(function (a) {
        if (a.length < 2) return;
        var k = 0, x;
        while ((x = n.indexOf(a, k)) >= 0) { if (x === 0 || !/[a-z0-9]/.test(n.charAt(x - 1))) for (i = x; i < x + a.length; i++) marca[i] = "1"; k = x + 1; }
      });
    });
    var out = "", dentro = false;
    for (i = 0; i < txt.length; i++) {
      if (marca[i] === "1" && !dentro) { out += "<mark>"; dentro = true; }
      if (marca[i] !== "1" && dentro) { out += "</mark>"; dentro = false; }
      out += esc(txt.charAt(i));
    }
    return out + (dentro ? "</mark>" : "");
  }

  function corta(s, n) { return s.length > n ? s.slice(0, n).replace(/\s+\S*$/, "") + "…" : s; }

  function montar(form) {
    if (form.__gtp) return; form.__gtp = 1;
    var pagina = form.classList.contains("gtp-pagina");
    var inp = form.querySelector("input"), lista = form.querySelector(".gtp-lista"), estado = form.querySelector(".gtp-estado"), limpa = form.querySelector(".gtp-limpa");
    var POR_GRUPO = pagina ? 1e9 : 5, MAX = pagina ? 1e9 : 25;
    var ops = [], ativo = -1, tm = 0, ultima = "";

    function abrir(sim) { lista.hidden = !sim; inp.setAttribute("aria-expanded", sim ? "true" : "false"); if (!sim) marcar(-1); }
    function marcar(i) {
      if (ops[ativo]) ops[ativo].classList.remove("ativo");
      ativo = i;
      if (ops[i]) { ops[i].classList.add("ativo"); inp.setAttribute("aria-activedescendant", ops[i].id); ops[i].scrollIntoView({ block: "nearest" }); }
      else inp.removeAttribute("aria-activedescendant");
    }
    function desenhar() {
      var q = inp.value.trim();
      if (limpa) limpa.hidden = !q;
      if (pagina) { try { history.replaceState(null, "", q ? "?q=" + encodeURIComponent(q) : location.pathname); } catch (e) {} }
      if (norm(q).length < 2) { lista.innerHTML = ""; ops = []; abrir(false); estado.textContent = ""; ultima = ""; return; }
      if (!dados) { carregar().then(desenhar, function () { lista.innerHTML = '<div class="gtp-nada">Não foi possível carregar a pesquisa. Tente outra vez daqui a pouco.</div>'; abrir(true); }); return; }
      if (q === ultima && lista.innerHTML) { abrir(true); return; }
      ultima = q;
      var r = procurar(q), h = "", n = 0, id = 0, mostrados = 0;
      r.grupos.forEach(function (g) {
        if (n >= MAX) return;
        var itens = g.itens.slice(0, Math.min(POR_GRUPO, MAX - n)); n += itens.length;
        h += '<div class="gtp-grupo" role="group" aria-labelledby="gtp-g' + g.k + '"><div class="gtp-gtit" id="gtp-g' + g.k + '">' + esc(g.nome) +
          (g.itens.length > itens.length ? "<small>" + itens.length + " de " + g.itens.length + "</small>" : "<small>" + g.itens.length + "</small>") + "</div>";
        itens.forEach(function (p) {
          h += '<a class="gtp-op" role="option" id="gtp-o' + (id++) + '" href="' + esc(p[0]) + '"><b>' + realca(p[1], r.toks) + "</b><span>" + esc(pagina ? p[2] : corta(p[2], 115)) + "</span></a>";
        });
        h += "</div>"; mostrados += itens.length;
      });
      if (!pagina && r.total > mostrados) h += '<a class="gtp-todos" role="option" id="gtp-o' + (id++) + '" href="/pesquisa?q=' + encodeURIComponent(q) + '">Ver todos os ' + r.total + " resultados →</a>";
      if (!r.total) h = '<div class="gtp-nada">Nada encontrado para «' + esc(q) + '». Experimente outra palavra (por exemplo: o seu signo, um sonho, um anjo, uma carta) ou veja o <a href="/mapa-do-site">mapa do site</a>.</div>';
      lista.innerHTML = h;
      ops = [].slice.call(lista.querySelectorAll(".gtp-op,.gtp-todos")); ativo = -1; inp.removeAttribute("aria-activedescendant");
      abrir(true);
      estado.textContent = r.total ? r.total + (r.total === 1 ? " resultado" : " resultados") + " em " + r.grupos.length + (r.grupos.length === 1 ? " secção" : " secções") : "Nenhum resultado";
    }
    function agenda() { clearTimeout(tm); tm = setTimeout(desenhar, 160); }
    function ir(i) { var a = ops[i]; if (a) location.href = a.getAttribute("href"); }

    inp.addEventListener("focus", function () { carregar().catch(function () {}); if (inp.value.trim() && !pagina) desenhar(); }, { passive: true });
    inp.addEventListener("input", function () { carregar().catch(function () {}); agenda(); });
    inp.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        if (lista.hidden) { if (ops.length) abrir(true); else return; }
        e.preventDefault(); var d = e.key === "ArrowDown" ? 1 : -1, n = ops.length;
        if (n) marcar(ativo < 0 ? (d > 0 ? 0 : n - 1) : (ativo + d + n) % n);
      } else if (e.key === "Enter") {
        e.preventDefault(); clearTimeout(tm);
        var q = inp.value.trim(); if (norm(q).length < 2) return;
        if (ativo >= 0) return ir(ativo);
        carregar().then(function () { if (q !== ultima) desenhar(); ir(0); });
      } else if (e.key === "Escape") {
        if (!lista.hidden && !pagina) { e.preventDefault(); abrir(false); } else if (inp.value) { e.preventDefault(); inp.value = ""; desenhar(); }
      }
    });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    if (limpa) limpa.addEventListener("click", function () { inp.value = ""; desenhar(); inp.focus(); });
    if (!pagina) {
      document.addEventListener("pointerdown", function (e) { if (!form.contains(e.target)) abrir(false); }, { passive: true });
      form.addEventListener("focusout", function (e) { if (e.relatedTarget && !form.contains(e.relatedTarget)) abrir(false); });
    }
    [].forEach.call(form.querySelectorAll(".gtp-dicas a"), function (a) {
      a.addEventListener("click", function (e) { e.preventDefault(); inp.value = a.textContent.trim(); inp.focus(); desenhar(); });
    });
    if (pagina) {
      var q0 = new URLSearchParams(location.search).get("q");
      if (q0) { inp.value = q0.slice(0, 100); desenhar(); }
    }
  }

  function arranca() { [].forEach.call(document.querySelectorAll("form.gtp"), montar); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arranca); else arranca();
  window.GTPesquisa = { procurar: function (q) { return carregar().then(function () { return procurar(q); }); } };
})();
