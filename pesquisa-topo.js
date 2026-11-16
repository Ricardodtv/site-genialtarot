/* pesquisa-topo.js — 16/11/2026 (pedido dele: a pesquisa do site): a ligação «Pesquisar» ao lado do «‹ genialtarot.com» no topo das
   páginas que o têm (cerca de 750). Carrega-se pelo vivo.js, que já está em todas, para não mexer em cada ficheiro.
   Leva à página /pesquisa. Depois de entrar, pede ao conta.js para voltar a arrumar o botão «Entrar» (escuta o resize). */
(function () {
  if (window.__gtpTopo || /^\/(pesquisa|consultorio|o-teu-ceu|pagar)(\/|\.html|-sala|$)/.test(location.pathname)) return;
  window.__gtpTopo = 1;
  function por() {
    // 16/11/2026 (ele): também nos sonhos (.voltar-barra .voltar) e nos arcanos (a.voltar), que têm outro botão de voltar.
    var b = document.querySelector(".topo .backlink") || document.querySelector(".voltar-barra .voltar") || document.querySelector("a.voltar");
    if (!b || document.querySelector(".gtp-topo")) return;
    var s = document.createElement("style");
    s.textContent = ".gtp-topo{display:inline-flex;align-items:center;gap:.375rem;margin:0 auto 0 .5rem;border-radius:9999px;padding:.5rem .875rem;background:oklch(0.23 0.06 270 / .7);border:1px solid oklch(0.82 0.13 85 / .4);font:inherit;font-size:.8rem;line-height:inherit;color:inherit;text-decoration:none;white-space:nowrap}" +
      ".gtp-topo svg{width:1rem;height:1rem;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round}.gtp-topo:hover{color:oklch(0.85 0.13 88)}" +
      "@media (max-width:520px){.gtp-topo{padding:.5rem .6rem}.gtp-topo span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}";
    document.head.appendChild(s);
    var a = document.createElement("a");
    a.className = "gtp-topo"; a.href = "/pesquisa"; a.title = "Pesquisar no site";
    a.style.color = getComputedStyle(b).color;
    a.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><span>Pesquisar</span>';
    b.insertAdjacentElement("afterend", a);
    // O conta.js arruma o «Entrar» ao ouvir o resize; repete-se porque às vezes ele ainda não estava a ouvir (visto nos sonhos, 16/11).
    [0, 400, 1500, 3500].forEach(function (t) { setTimeout(function () { try { dispatchEvent(new Event("resize")); } catch (e) {} }, t); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", por); else por();
})();
