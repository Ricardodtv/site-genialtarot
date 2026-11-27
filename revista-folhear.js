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
  // 27/11 (ele): o som de uma folha a virar; desliga-se no 🔊 (fica guardado neste aparelho)
  var somLigado = true;
  try { somLigado = localStorage.getItem("revista-som") !== "0"; } catch (e) {}
  var bt = document.getElementById("som-folha");
  function pintaSom() { if (bt) { bt.textContent = somLigado ? "🔊 Som" : "🔇 Sem som"; bt.setAttribute("aria-pressed", somLigado ? "true" : "false"); } }
  pintaSom();
  if (bt) bt.addEventListener("click", function () { somLigado = !somLigado; try { localStorage.setItem("revista-som", somLigado ? "1" : "0"); } catch (e) {} pintaSom(); if (somLigado) folha(); });
  // 27/11 (ele: «o som é horrível, não tens outro mais suave?»): agora é uma GRAVAÇÃO de uma folha de papel verdadeira
  // (pacote «Book Flip Sounds», OpenGameArt, CC0), suavizada (sem agudos, fim em esvaimento) — revista-folha.mp3, 12 KB.
  var somF = null;
  function folha() {
    if (!somLigado) return;
    try {
      if (!somF) { somF = new Audio("/revista-folha.mp3"); somF.preload = "auto"; }
      somF.volume = 0.55; somF.currentTime = 0;
      var p = somF.play(); if (p && p.catch) p.catch(function () {});
    } catch (e) {}
  }
  // 27/11 (ele): música relaxante a tocar logo ao abrir, em tom baixo — a mesma do Tarot Grátis (ambient.mp3), em repetição.
  // Os navegadores não deixam tocar som antes de a pessoa mexer na página: tenta logo; se for bloqueado, começa ao 1.º toque/tecla.
  var musLigada = true, mus = null, btM = document.getElementById("musica");
  try { musLigada = localStorage.getItem("revista-musica") !== "0"; } catch (e) {}
  function pintaMus() { if (btM) { btM.textContent = musLigada ? "🎵 Música" : "🎵 Sem música"; btM.setAttribute("aria-pressed", musLigada ? "true" : "false"); } }
  function tocaMus() {
    if (!musLigada) return;
    try {
      if (!mus) { mus = new Audio("/ambient.mp3"); mus.loop = true; mus.volume = 0.12; mus.preload = "auto"; }
      var p = mus.play(); if (p && p.catch) p.catch(function () {});
    } catch (e) {}
  }
  pintaMus(); tocaMus();
  function primeiro() { tocaMus(); ["pointerdown", "keydown", "touchstart"].forEach(function (t) { removeEventListener(t, primeiro, true); }); }
  ["pointerdown", "keydown", "touchstart"].forEach(function (t) { addEventListener(t, primeiro, true); });
  if (btM) btM.addEventListener("click", function (ev) {
    ev.stopPropagation(); musLigada = !musLigada; try { localStorage.setItem("revista-musica", musLigada ? "1" : "0"); } catch (e) {}
    pintaMus(); if (musLigada) tocaMus(); else if (mus) mus.pause();
  });
  document.addEventListener("visibilitychange", function () { if (!mus) return; if (document.hidden) mus.pause(); else if (musLigada) tocaMus(); });
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
