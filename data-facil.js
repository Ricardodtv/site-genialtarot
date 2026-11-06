/* 05/11/2026, pedido dele: as datas devem ser fáceis de escrever em todos os formulários do site.
   A pessoa escreve como quiser (23/01/1976, 23 01 1976, 23 janeiro de 1976, 23011976, 23/1/76) e isto organiza.
   - input[type=date]: fica escondido, a guardar a data certa (AAAA-MM-DD), para o código da página continuar igual;
     à frente aparece um campo de texto simples, com o exemplo em cinza clarinho.
   - campos de data já em texto: deixam escrever letras no telemóvel e levam o mesmo exemplo.
   Dia sempre antes do mês. Não se aplica à aplicação «O Teu Céu». */
(function () {
  if (/^\/o-teu-ceu/.test(location.pathname)) return;
  var EX = "Ex.: 23/01/1976 ou 23 janeiro 1976", EXC = "Ex.: 23/01/1976";
  var ME = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"], NM = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var ALT = { feb: 2, apr: 4, may: 5, aug: 8, sep: 9, oct: 10, dec: 12, ene: 1, dic: 12 };
  function sem(t) { return String(t || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim(); }
  function ler(txt) {
    var t = sem(txt), iso = t.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/), p, m;
    if (iso) p = [iso[3], iso[2], iso[1]];
    else {
      t = t.replace(/\b(de|do|dia|ano|o)\b/g, " ").replace(/\b([a-z]{3,})\.?/g, function (w, n) {
        var k = n.slice(0, 3), i = ME.indexOf(k); return i >= 0 ? " " + (i + 1) + " " : ALT[k] ? " " + ALT[k] + " " : " ? ";
      });
      if (t.indexOf("?") >= 0) return null;
      p = t.match(/\d+/g) || [];
      if (p.length === 1 && /^\d{8}$/.test(p[0])) p = [p[0].slice(0, 2), p[0].slice(2, 4), p[0].slice(4)];
      else if (p.length === 1 && /^\d{6}$/.test(p[0])) p = [p[0].slice(0, 2), p[0].slice(2, 4), p[0].slice(4)];
    }
    if (p.length !== 3) return null;
    var d = +p[0], mes = +p[1], a = +p[2];
    if (p[2].length <= 2) a += a <= new Date().getFullYear() % 100 ? 2000 : 1900;
    m = new Date(Date.UTC(a, mes - 1, d));
    if (a < 100 || m.getUTCMonth() !== mes - 1 || m.getUTCDate() !== d) return null;
    return { d: d, m: mes, a: a, iso: ("000" + a).slice(-4) + "-" + ("0" + mes).slice(-2) + "-" + ("0" + d).slice(-2) };
  }
  function bonita(r) { return r.d + " de " + NM[r.m - 1] + " de " + r.a; }
  function barra(r) { return ("0" + r.d).slice(-2) + "/" + ("0" + r.m).slice(-2) + "/" + r.a; }
  function estilo() {
    if (document.getElementById("data-facil-css")) return;
    var s = document.createElement("style"); s.id = "data-facil-css";
    s.textContent = "input.data-facil::placeholder{color:#d3d3dc;opacity:.72}input.data-facil::-webkit-input-placeholder{color:#d3d3dc;opacity:.72}.data-facil-msg{display:block;min-height:1.2em;margin:.25rem 0 0;font-size:.82rem;line-height:1.25;color:#e8cf95;text-align:inherit}.data-facil-msg.mal{color:#ff9d9d}";
    document.head.appendChild(s);
    var s2 = document.createElement("style");
    s2.textContent = ".df-convite{display:block;margin:.3rem 0 0;font-size:.82rem;line-height:1.3;font-weight:600;color:#ffd978}input.df-falta{border-color:#ffd978!important;animation:dfPulsa 1.8s ease-out infinite}@keyframes dfPulsa{0%{box-shadow:0 0 0 0 rgba(255,217,120,.6)}80%,100%{box-shadow:0 0 0 9px rgba(255,217,120,0)}}@media (prefers-reduced-motion:reduce){input.df-falta{animation:none;box-shadow:0 0 0 2px rgba(255,217,120,.7)}}";
    document.head.appendChild(s2);
  }
  function exemplo(el) { el.placeholder = el.offsetWidth && el.offsetWidth < 270 ? EXC : EX; }
  // 06/11/2026 (ele): o exemplo fica só 30 segundos, porque as pessoas pensavam que o campo já vinha preenchido.
  // Conta a partir de o campo estar à vista. Depois fica vazio, com o rebordo a pulsar e o convite a escrever.
  var VIGIADOS = [];
  function temTexto(el) { return !!(el.value && el.value.trim()); }
  function atualiza() {
    VIGIADOS.forEach(function (c) {
      var ver = !temTexto(c.el) && !c.el.disabled && !c.el.readOnly;
      c.nota.style.display = ver ? "" : "none"; c.el.classList.toggle("df-falta", ver && c.fim);
    });
  }
  function acaba(c) { c.fim = true; c.el.placeholder = ""; atualiza(); }
  function rotulo(el) {
    var l = el.id && document.querySelector('label[for="' + el.id + '"]'), t = (l && l.textContent) || (el.closest("label") || {}).textContent || "";
    if (!t) { for (var p = el.previousElementSibling; p && !t; p = p.previousElementSibling) t = p.textContent || ""; }
    return sem(t + " " + (el.getAttribute("aria-label") || "") + " " + el.id + " " + el.name);
  }
  function convite(el, antes, depois) {
    if (el.dataset.dfConvite) return; el.dataset.dfConvite = "1";
    var r = rotulo(el), nota = document.createElement("span"), c = { el: el, nota: nota, fim: false };
    nota.className = "df-convite"; nota.textContent = "✍️ " + (/nasc|dob/.test(r) ? depois : antes);
    (el.parentNode).insertBefore(nota, el.nextSibling);
    VIGIADOS.push(c);
    el.addEventListener("input", atualiza); el.addEventListener("change", atualiza);
    var conta = function () { setTimeout(function () { acaba(c); }, 30000); };
    if (window.IntersectionObserver) { var o = new IntersectionObserver(function (l, ob) { if (l.some(function (x) { return x.isIntersecting; })) { ob.disconnect(); conta(); } }, { threshold: .5 }); o.observe(el); } else conta();
    atualiza();
  }
  function preparaTexto(el) {
    if (el.dataset.dataFacil) return; el.dataset.dataFacil = "1";
    el.classList.add("data-facil"); el.setAttribute("inputmode", "text"); el.setAttribute("maxlength", "32"); el.setAttribute("autocomplete", "off"); exemplo(el);
    el.addEventListener("blur", function () { var r = ler(el.value); if (r) el.value = barra(r); });
    convite(el, "Escreva aqui a data", "Escreva aqui a sua data de nascimento");
  }
  function preparaData(o) {
    if (o.dataset.dataFacil) return; o.dataset.dataFacil = "1";
    var cs = getComputedStyle(o), v = document.createElement("input"), msg = document.createElement("span");
    v.type = "text"; v.className = "data-facil " + o.className; v.setAttribute("inputmode", "text"); v.setAttribute("autocomplete", "off"); v.setAttribute("maxlength", "32");
    v.id = (o.id || "data") + "-facil"; if (o.required) { v.required = true; o.required = false; }
    ["backgroundColor", "backgroundImage", "color", "borderTopWidth", "borderTopStyle", "borderTopColor", "borderRightWidth", "borderRightStyle", "borderRightColor", "borderBottomWidth", "borderBottomStyle", "borderBottomColor", "borderLeftWidth", "borderLeftStyle", "borderLeftColor", "borderTopLeftRadius", "borderTopRightRadius", "borderBottomLeftRadius", "borderBottomRightRadius", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "fontFamily", "fontSize", "fontWeight", "textAlign", "boxSizing", "marginTop", "marginRight", "marginBottom", "marginLeft"].forEach(function (k) { v.style[k] = cs[k]; });
    v.style.width = o.style.width || (o.offsetWidth ? "100%" : ""); if (o.offsetWidth) { v.style.maxWidth = o.offsetWidth + "px"; }
    msg.className = "data-facil-msg"; msg.setAttribute("aria-live", "polite"); msg.id = v.id + "-msg"; v.setAttribute("aria-describedby", msg.id);
    if (o.id) { var l = document.querySelector('label[for="' + o.id + '"]'); if (l) l.htmlFor = v.id; }
    if (!(o.id && document.querySelector('label[for="' + v.id + '"]'))) { var pai = o.closest("label"); if (pai) v.setAttribute("aria-label", (pai.textContent || "Data").trim().slice(0, 80)); }
    o.parentNode.insertBefore(v, o); o.parentNode.insertBefore(msg, o); o.style.display = "none"; o.tabIndex = -1; o.setAttribute("aria-hidden", "true");
    var proto = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value");
    function pega() { return proto.get.call(o); }
    function poe(iso, avisar) { var ant = pega(); proto.set.call(o, iso); if (avisar && ant !== iso) { o.dispatchEvent(new Event("input", { bubbles: true })); o.dispatchEvent(new Event("change", { bubbles: true })); } }
    Object.defineProperty(o, "value", { configurable: true, get: pega, set: function (x) { proto.set.call(o, x); var r = ler(x); v.value = r ? barra(r) : ""; msg.textContent = ""; } });
    if (pega()) { var i0 = ler(pega()); if (i0) v.value = barra(i0); }
    exemplo(v); convite(v, "Escreva aqui a data", "Escreva aqui a sua data de nascimento");
    function confere(fim) {
      var t = v.value.trim(), r = ler(t), mau = "";
      if (!t) { poe("", true); v.setCustomValidity(""); msg.textContent = ""; msg.classList.remove("mal"); return; }
      if (!r) mau = "Não percebi a data. " + EX + ".";
      else if ((o.min && r.iso < o.min) || (o.max && r.iso > o.max)) mau = "Confirme o ano: " + bonita(r) + " está fora do que este cálculo aceita.";
      if (mau) { poe("", true); if (fim) { v.setCustomValidity(mau); msg.textContent = mau; msg.classList.add("mal"); } else { v.setCustomValidity(""); msg.textContent = ""; msg.classList.remove("mal"); } return; }
      poe(r.iso, true); v.setCustomValidity(""); msg.textContent = "✓ " + bonita(r); msg.classList.remove("mal");
      if (fim) v.value = barra(r);
    }
    v.addEventListener("input", function () { v.setCustomValidity(""); confere(false); });
    v.addEventListener("blur", function () { confere(true); });
    var f = o.form || v.form; if (f) f.addEventListener("submit", function () { confere(true); }, true);
    v.addEventListener("keydown", function (e) { if (e.key === "Enter") confere(true); });
  }
  function varre(r) {
    (r.querySelectorAll ? r : document).querySelectorAll('input[type="date"]').forEach(preparaData);
    (r.querySelectorAll ? r : document).querySelectorAll("input#data,input#data2,input#asc-rapido-data,input#qs-data,input#f-dob").forEach(preparaTexto);
    (r.querySelectorAll ? r : document).querySelectorAll('input[placeholder^="HH:MM"]').forEach(function (el) { convite(el, "Escreva aqui a hora", "Escreva aqui a hora em que nasceu"); });
  }
  function arranca() {
    estilo(); varre(document);
    new MutationObserver(function (l) { l.forEach(function (x) { x.addedNodes.forEach(function (n) { if (n.nodeType === 1) { if (n.matches && n.matches('input[type="date"]')) preparaData(n); else varre(n); } }); }); }).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arranca); else arranca();
  setInterval(atualiza, 1500);   // valores postos pelo código da página (dados guardados, «Não sei a hora»)
  window.dataFacil = { ler: ler };
})();
