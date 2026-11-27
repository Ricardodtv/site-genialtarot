/* revista-folhear.js — folhear a Revista do mês como uma revista (27/11/2026, pedido dele).
   Sem este ficheiro as páginas aparecem umas por baixo das outras (o Google lê tudo na mesma).
   Setas, deslizar com o dedo, teclas ← →, índice e endereço #pagina (para partilhar uma página). */
(function () {
  var r = document.getElementById("revista"); if (!r) return;
  var F = Array.prototype.slice.call(r.querySelectorAll(".folha")); if (!F.length) return;
  var ant = document.getElementById("ant"), seg = document.getElementById("seg"), num = document.getElementById("pagnum");
  var i = 0;
  r.classList.add("js");
  function mostra(n, anima) {
    n = Math.max(0, Math.min(F.length - 1, n)); if (n === i && anima) return;
    var velho = F[i], frente = n > i;
    F.forEach(function (f) { f.classList.remove("ativa", "sai", "volta"); });
    F[n].classList.add("ativa");
    if (anima && velho !== F[n]) {
      if (frente) { velho.classList.add("sai"); setTimeout(function () { velho.classList.remove("sai"); }, 700); }
      else { F[n].classList.add("volta"); setTimeout(function () { F[n].classList.remove("volta"); }, 700); }
    }
    if (anima && velho !== F[n] && typeof folha === "function") folha();
    i = n;
    ant.disabled = i === 0; seg.disabled = i === F.length - 1;
    num.textContent = (i + 1) + " / " + F.length;
    try { history.replaceState(null, "", i ? "#" + F[i].id : location.pathname + location.search); } catch (e) {}
    if (anima) { var top = r.getBoundingClientRect().top + scrollY - 70; if (scrollY > top) scrollTo({ top: top, behavior: "smooth" }); }
  }
  // 27/11 (ele): o som de uma folha a virar — feito na hora com o WebAudio (ruído filtrado), sem ficheiro; desliga-se no 🔊
  var somLigado = true, ctx = null;
  try { somLigado = localStorage.getItem("revista-som") !== "0"; } catch (e) {}
  var bt = document.getElementById("som-folha");
  function pintaSom() { if (bt) { bt.textContent = somLigado ? "🔊 Som" : "🔇 Sem som"; bt.setAttribute("aria-pressed", somLigado ? "true" : "false"); } }
  pintaSom();
  if (bt) bt.addEventListener("click", function () { somLigado = !somLigado; try { localStorage.setItem("revista-som", somLigado ? "1" : "0"); } catch (e) {} pintaSom(); if (somLigado) folha(); });
  function folha() {
    if (!somLigado) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      if (ctx.state === "suspended") ctx.resume();
      var dur = 0.42, n = Math.floor(ctx.sampleRate * dur), buf = ctx.createBuffer(1, n, ctx.sampleRate), d = buf.getChannelData(0);
      for (var k = 0; k < n; k++) { var t = k / n; d[k] = (Math.random() * 2 - 1) * Math.pow(Math.sin(Math.PI * t), 1.6) * (0.55 + 0.45 * Math.random()); }
      var src = ctx.createBufferSource(); src.buffer = buf;
      var bp = ctx.createBiquadFilter(); bp.type = "bandpass"; bp.Q.value = 0.9;
      bp.frequency.setValueAtTime(900, ctx.currentTime); bp.frequency.exponentialRampToValueAtTime(3800, ctx.currentTime + dur * 0.6); bp.frequency.exponentialRampToValueAtTime(1600, ctx.currentTime + dur);
      var g = ctx.createGain(); g.gain.setValueAtTime(0.0001, ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.5, ctx.currentTime + 0.05); g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + dur);
      src.connect(bp); bp.connect(g); g.connect(ctx.destination); src.start();
    } catch (e) {}
  }
  // a ponta da folha que se dobra: vira a página
  r.addEventListener("click", function (ev) { if (ev.target.closest(".vira")) { ev.stopPropagation(); mostra(i + 1, true); } }, true);
  ant.addEventListener("click", function () { mostra(i - 1, true); });
  seg.addEventListener("click", function () { mostra(i + 1, true); });
  document.addEventListener("keydown", function (ev) {
    if (/input|textarea|select/i.test((ev.target || {}).tagName || "")) return;
    if (ev.key === "ArrowRight") mostra(i + 1, true); else if (ev.key === "ArrowLeft") mostra(i - 1, true);
  });
  // deslizar com o dedo (só na horizontal: o deslizar vertical continua a rolar a página)
  var x0 = null, y0 = null;
  r.addEventListener("touchstart", function (ev) { x0 = ev.touches[0].clientX; y0 = ev.touches[0].clientY; }, { passive: true });
  r.addEventListener("touchend", function (ev) {
    if (x0 === null) return; var dx = ev.changedTouches[0].clientX - x0, dy = ev.changedTouches[0].clientY - y0; x0 = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.3) mostra(i + (dx < 0 ? 1 : -1), true);
  }, { passive: true });
  // tocar na capa abre a revista
  F[0].addEventListener("click", function (ev) { if (!ev.target.closest("a")) mostra(1, true); });
  F[0].style.cursor = "pointer";
  // o índice
  r.addEventListener("click", function (ev) {
    var a = ev.target.closest("[data-ir]"); if (!a) return; ev.preventDefault();
    var n = F.findIndex(function (f) { return f.id === a.getAttribute("data-ir"); }); if (n >= 0) mostra(n, true);
  });
  var volta = document.getElementById("voltar-site");
  if (volta) volta.addEventListener("click", function (ev) { if (window.opener && !window.opener.closed) { ev.preventDefault(); try { window.opener.focus(); } catch (e) {} window.close(); } });
  var h = location.hash.slice(1), k = h ? F.findIndex(function (f) { return f.id === h; }) : -1;
  mostra(k > 0 ? k : 0, false);
})();
