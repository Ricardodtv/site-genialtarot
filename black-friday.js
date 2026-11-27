/* black-friday.js — 27/11/2026, pedido dele: «faz um anúncio de Black Friday e coloca em destaque em todo o site com 30% de
   desconto em tudo … marcação na loja online nos produtos, chamativa … promoção activa até domingo à meia-noite».
   · Os botões do myPOS têm o preço FIXO; durante a promoção paga-se pela etiqueta dele, mypos.com/@genialtarot/<valor>
     (ideia dele 27/11: o valor no endereço fica FIXO no checkout — medido). Cada produto só mostra −30% se tiver «link» (TABELA).
     Sem botão novo, fica ao preço normal — nunca se anuncia um preço que o pagamento não cobra.
   · A faixa de cima e o destaque só aparecem com TODOS os botões preenchidos («30% em tudo» tem de ser verdade).
   · Fim: domingo 29/11/2026 23:59:59 em Lisboa (= UTC em Novembro). Depois disso tudo volta sozinho ao normal.
   · Carregado pelo vivo.js em todas as páginas, e pela loja e pelo pagar.html directamente.
   · Ver antes de ligar: ?bf=ver (mostra preços e faixa SEM trocar os botões — só para conferir o aspecto). */
(function () {
  var INICIO = Date.parse("2026-11-27T00:00:00Z"), FIM = Date.parse("2026-11-29T23:59:59Z");
  // chave = o botão myPOS de sempre · n = número na lista que lhe mandei · link = o botão NOVO com −30% (vazio = ainda não há)
  var TABELA = {
    "B325FU28AAM77": { pag: "/leia-o-tarot-sem-decorar", n:  1, de: "14,90 €", para: "10,43 €", link: "https://mypos.com/@genialtarot/10.43" },   // Leia o Tarot Sem Decorar
    "BR3QBMEV89Y96": { pag: "/o-seu-2027", n:  2, de: "7 €", para: "4,90 €", link: "https://mypos.com/@genialtarot/4.90" },   // O Seu 2027
    "BIKOETG3DIP04": { pag: "/mapa-amor", n:  3, de: "10 €", para: "6,99 €", link: "https://mypos.com/@genialtarot/6.99" },   // Mapa do Amor e da Sedução
    "BXHAKT4BHSD02": { pag: "/numerologia-2027", n:  4, de: "25 €", para: "17,50 €", link: "https://mypos.com/@genialtarot/17.50" },   // Ano 2027
    "BUQ28DVM5JR98": { pag: "/tarot-semestral", n:  5, de: "15 €", para: "10,50 €", link: "https://mypos.com/@genialtarot/10.50" },   // Tarot Semestral
    "BBGBCIOKNQY86": { n:  6, de: "45 €", para: "31,50 €", link: "https://mypos.com/@genialtarot/31.50" },   // Tarot Semestral
    "BQMNGTHSAHA83": { pag: "/mapa-astral", n:  7, de: "15 €", para: "10,50 €", link: "https://mypos.com/@genialtarot/10.50" },   // Mapa Astral
    "BKXR2JQ2BEB19": { n:  8, de: "25 €", para: "17,50 €", link: "https://mypos.com/@genialtarot/17.50" },   // 1 Pergunta de Tarot por Escrito
    "BTSGROA5LPZ61": { n:  9, de: "65 €", para: "45,50 €", link: "https://mypos.com/@genialtarot/45.50" },   // Consulta de Tarot Online
    "B35PHJ9OQMU04": { n: 10, de: "85 €", para: "59,50 €", link: "https://mypos.com/@genialtarot/59.50" },   // Consulta de Tarot Online
    "B5IA82S63VN50": { n: 11, de: "185 €", para: "129,50 €", link: "https://mypos.com/@genialtarot/129.50" },   // Previsão Anual para 12 Meses
    "B1CMBQSYWEW69": { n: 12, de: "185 €", para: "129,50 €", link: "https://mypos.com/@genialtarot/129.50" },   // Consulta de Terapia de Casais Online
    "BLQ1NIUDJ2K11": { n: 13, de: "125 €", para: "87,50 €", link: "https://mypos.com/@genialtarot/87.50" },   // Parecer sobre Qualquer Assunto pelas Cartas
    "BG2QB2ADANJ52": { n: 14, de: "80 €", para: "56,00 €", link: "https://mypos.com/@genialtarot/56.00" },   // Leitura da Sua Mão por Quiromancia Online
    "BNNCED4W9IU06": { n: 15, de: "40 €", para: "28,00 €", link: "https://mypos.com/@genialtarot/28.00" },   // Consulta de Pêndulo
    "BVQ7RWY5ITA62": { n: 16, de: "65 €", para: "45,50 €", link: "https://mypos.com/@genialtarot/45.50" },   // Consulta de Pêndulo
    "BKXKXFVMT7M49": { n: 17, de: "110 €", para: "77,00 €", link: "https://mypos.com/@genialtarot/77.00" },   // Consulta de Emergência com Mestre Alberto (Respost
    "B5588K5PTFM42": { n: 18, de: "145 €", para: "101,50 €", link: "https://mypos.com/@genialtarot/101.50" },   // Amuleto Cruz da Boa Energia e Sucesso
    "B2PA7QQ3QA346": { n: 19, de: "165 €", para: "115,50 €", link: "https://mypos.com/@genialtarot/115.50" },   // Amuleto Pentagrama de Equilíbrio com Ritual
    "BF6O2I7O68M52": { n: 20, de: "195 €", para: "136,50 €", link: "https://mypos.com/@genialtarot/136.50" },   // Mapa Astral Conheça Sua Personalidade
    "BWEHSTP6TUV40": { n: 21, de: "145 €", para: "101,50 €", link: "https://mypos.com/@genialtarot/101.50" },   // Análise ao Seu Signo e Personalidade
    "B8Q8NUM8CSD06": { n: 22, de: "2450 €", para: "1715,00 €", link: "https://mypos.com/@genialtarot/1715.00" },   // Curso de Tarot Online 3 Meses com Mestre Alberto
    "BTY99VSJMLA69": { n: 23, de: "19 €", para: "13,30 €", link: "https://mypos.com/@genialtarot/13.30" },   // Astrologia 2027
  };
  // sem botão myPOS (compra pelo WhatsApp): o preço com desconto vale assim que a promoção estiver ligada
  var WHATSAPP = [
    { nome: "Respondida em Áudio", de: "15 €", para: "10,50 €" },
    { nome: "Sessão de Hipnose", de: "125 €", para: "87,50 €" }
  ];
  var ver = /[?&]bf=ver\b/.test(location.search);
  var agora = Date.now();
  var dentro = ver || (agora >= INICIO && agora <= FIM);
  var ids = Object.keys(TABELA);
  var todos = ids.every(function (k) { return !!TABELA[k].link; });
  function idDe(u) { var m = String(u || "").match(/mypos\.com\/vmp\/btn\/([A-Z0-9]+)/); return m ? m[1] : ""; }
  function entrada(u) { var e = dentro && TABELA[idDe(u)]; return e && (e.link || ver) ? e : null; }
  var BF = window.BF = {
    fim: FIM, ativo: dentro && (todos || ver), ver: ver, TABELA: TABELA,
    entrada: entrada,
    novoLink: function (u) { var e = entrada(u); return e && e.link ? e.link : u; },
    /* a loja chama isto antes de desenhar: troca preço, botão e etiqueta dos produtos que têm botão novo */
    aplica: function (lista) {
      if (!dentro || !lista) return;
      lista.forEach(function (p) {
        if (p.__bf) return;
        var e = null;
        if (p.link) e = entrada(p.link);
        if (!e && p.pagina) ids.forEach(function (k) { if (TABELA[k].pag === p.pagina && (TABELA[k].link || ver)) e = TABELA[k]; });
        if (!e && !p.link && !p.pagina && BF.ativo) WHATSAPP.forEach(function (w) { if (String(p.nome).indexOf(w.nome) >= 0) e = w; });
        if (!e || String(p.preco).trim() !== e.de) return;       // sem preço igual (ex.: rituais) não se mexe
        p.__bf = 1; p.precoAntes = p.preco; p.preco = e.para;
        if (p.link && e.link) p.link = e.link;
        p.etiqueta = "Black Friday −30%"; p.cor = "vermelho"; p.estrelas = 0; p.topvendas = false; p.destaque = true;
      });
    },
    precoHtml: function (p) {
      var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
      return p.precoAntes ? '<s class="bf-antes">' + esc(p.precoAntes) + '</s> <span class="bf-agora">' + esc(p.preco) + "</span>" : esc(p.preco);
    }
  };
  if (window.__bfFeito) return; window.__bfFeito = 1;
  if (!dentro) return;

  function falta() {
    var s = Math.max(0, Math.floor((FIM - Date.now()) / 1000)), d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
    return (d ? d + "d " : "") + ("0" + h).slice(-2) + ":" + ("0" + m).slice(-2) + ":" + ("0" + x).slice(-2);
  }
  function montar() {
    // os botões myPOS antigos espalhados pelo site passam para os novos (?u= da pagar.html incluído)
    Array.prototype.forEach.call(document.querySelectorAll('a[href*="mypos.com/vmp/btn/"]'), function (a) {
      var h = a.getAttribute("href"), e = entrada(decodeURIComponent(h));
      if (!e || !e.link) return;
      var velho = "https://mypos.com/vmp/btn/" + idDe(decodeURIComponent(h));
      h = h.replace(velho, e.link).replace(encodeURIComponent(velho), encodeURIComponent(e.link)).replace(/([?&]v=)[^&]*/, "" + encodeURIComponent(e.para));
      a.setAttribute("href", h);
    });
    if (!BF.ativo || /^\/(consultorio|o-teu-ceu|pagar)(\/|\.html|-sala|$)/.test(location.pathname)) return;
    var st = document.createElement("style");
    st.textContent = ".bf-faixa{position:sticky;top:0;z-index:9999;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:.35rem .9rem;"
      + "padding:.55rem 1rem;background:linear-gradient(90deg,#000,#1a1208 50%,#000);border-bottom:2px solid #e2a93a;color:#fff;text-decoration:none;"
      + "font:700 .95rem/1.25 Inter,system-ui,sans-serif;text-align:center;box-shadow:0 6px 20px -8px #000}"
      + ".bf-faixa b{font-family:Cinzel,Georgia,serif;font-weight:900;letter-spacing:.08em;color:#ffd978}"
      + ".bf-faixa .bf-pct{background:#d81f2a;color:#fff;border-radius:6px;padding:.1rem .5rem;font-weight:900}"
      + ".bf-faixa .bf-t{font-variant-numeric:tabular-nums;color:#ffe9a6}"
      + ".bf-faixa .bf-ir{background:linear-gradient(135deg,#ffe9a6,#e2a93a);color:#1a1208;border-radius:999px;padding:.25rem .8rem}"
      + "@media(max-width:560px){.bf-faixa{font-size:.82rem;padding:.45rem .6rem}.bf-faixa .bf-sub{display:none}}";
    document.head.appendChild(st);
    var f = document.createElement("a"); f.className = "bf-faixa"; f.href = "/loja?de=site&c=black-friday";
    f.innerHTML = '<b>BLACK FRIDAY</b><span class="bf-pct">−30%</span><span>em tudo na loja</span>'
      + '<span class="bf-sub">· termina em <span class="bf-t">' + falta() + '</span></span><span class="bf-ir">Ver ofertas →</span>';
    document.body.insertBefore(f, document.body.firstChild);
    var t = f.querySelector(".bf-t");
    setInterval(function () { if (Date.now() > FIM) { f.remove(); return; } t.textContent = falta(); }, 1000);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();
