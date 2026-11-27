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
    i = n;
    ant.disabled = i === 0; seg.disabled = i === F.length - 1;
    num.textContent = (i + 1) + " / " + F.length;
    try { history.replaceState(null, "", i ? "#" + F[i].id : location.pathname + location.search); } catch (e) {}
    if (anima) { var top = r.getBoundingClientRect().top + scrollY - 70; if (scrollY > top) scrollTo({ top: top, behavior: "smooth" }); }
  }
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
  var h = location.hash.slice(1), k = h ? F.findIndex(function (f) { return f.id === h; }) : -1;
  mostra(k > 0 ? k : 0, false);
})();
