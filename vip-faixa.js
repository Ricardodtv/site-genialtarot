/* 29/10/2026: a faixa «Lista VIP» no topo de todas as páginas (pedido dele: estreita, vistosa, a chamar).
   O worker põe este script em todas as páginas HTML. Não aparece na própria /vip, nem a quem já entrou
   (localStorage «vip-entrou»); o × esconde-a só até fechar o separador. */
(function () {
  try {
    if (/^\/(vip|o-teu-ceu)(\.html)?$/.test(location.pathname)) return;   // nem na página VIP nem na app «O Teu Céu»
    // 29/10/2026: quem chega por um email da lista (os links levam «vip=1») já é VIP — nunca mais vê a faixa
    if (new URLSearchParams(location.search).get("vip") === "1") { localStorage.setItem("vip-entrou", "1"); return; }
    if (localStorage.getItem("vip-entrou")) return;
    if (sessionStorage.getItem("vip-fechada")) return;
  } catch (e) { /* sem armazenamento: mostra na mesma */ }
  if (document.getElementById("vip-faixa")) return;

  const css = `
#vip-faixa{position:sticky;top:0;z-index:9999;display:flex;align-items:center;justify-content:center;gap:.7rem;
  padding:.55rem 2.6rem .55rem .9rem;min-height:54px;box-sizing:border-box;text-decoration:none;cursor:pointer;
  font:700 15.5px/1.25 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#fff;text-align:center;
  background:linear-gradient(100deg,#3b0f5c 0%,#6d1f8f 30%,#a0307a 55%,#6d1f8f 80%,#3b0f5c 100%);background-size:250% 100%;
  border-bottom:2px solid #ffd978;box-shadow:0 0 0 1px rgba(255,217,120,.25),0 6px 26px -4px rgba(255,200,90,.75);animation:vipMove 6s linear infinite;overflow:hidden}
#vip-faixa::after{content:"";position:absolute;top:0;left:-40%;width:35%;height:100%;pointer-events:none;
  background:linear-gradient(100deg,transparent,rgba(255,240,180,.7),transparent);animation:vipBrilho 3.2s ease-in-out infinite}
#vip-faixa .vc{font-size:24px;filter:drop-shadow(0 0 6px rgba(255,215,120,.9));animation:vipCoroa 1.6s ease-in-out infinite;display:inline-block}
#vip-faixa b{color:#ffd978;letter-spacing:.04em}
#vip-faixa .vb{flex:none;padding:.38rem .9rem;border-radius:999px;background:linear-gradient(135deg,#ffe49a,#f0b440);color:#2a1300;
  font-weight:900;font-size:14px;padding:.45rem 1.05rem;white-space:nowrap;box-shadow:0 0 0 0 rgba(255,215,120,.7);animation:vipPulsa 1.6s ease-out infinite,vipAbana 4s ease-in-out infinite}
#vip-faixa .ve{position:absolute;color:#ffe9a8;font-size:11px;pointer-events:none;animation:vipEstrela 2.4s ease-in-out infinite}
html.vip-on .som-fix,html.vip-on .btn-som,html.vip-on .backlink{top:calc(1rem + 54px)!important}
#vip-faixa .vx{position:absolute;right:.4rem;top:50%;transform:translateY(-50%);width:30px;height:30px;border:0;border-radius:50%;
  background:transparent;color:#fff;opacity:.6;font-size:18px;line-height:1;cursor:pointer}
#vip-faixa .vx:hover{opacity:1;background:rgba(255,255,255,.12)}
@keyframes vipMove{to{background-position:-250% 0}}
@keyframes vipBrilho{0%{left:-40%}60%,100%{left:120%}}
@keyframes vipCoroa{0%,100%{transform:translateY(0) rotate(-6deg)}50%{transform:translateY(-2px) rotate(6deg)}}
@keyframes vipAbana{0%,86%,100%{transform:rotate(0)}88%{transform:rotate(-5deg) scale(1.06)}90%{transform:rotate(5deg) scale(1.06)}92%{transform:rotate(-4deg)}94%{transform:rotate(3deg)}}
@keyframes vipEstrela{0%,100%{opacity:0;transform:scale(.4)}50%{opacity:1;transform:scale(1.2)}}
@keyframes vipPulsa{0%{box-shadow:0 0 0 0 rgba(255,215,120,.75)}80%,100%{box-shadow:0 0 0 12px rgba(255,215,120,0)}}
@media (max-width:520px){#vip-faixa{font-size:14px;gap:.5rem;padding-left:.6rem}#vip-faixa .vl{display:none}#vip-faixa .vb{font-size:13px;padding:.42rem .8rem}}
@media (prefers-reduced-motion:reduce){#vip-faixa,#vip-faixa::after,#vip-faixa .vc,#vip-faixa .vb,#vip-faixa .ve{animation:none}}`;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  const a = document.createElement("a");
  a.id = "vip-faixa"; a.href = "/vip";
  a.innerHTML = `<span class="vc" aria-hidden="true">👑</span><span>Entre na <b>Lista VIP</b> grátis<span class="vl"> — promoções e presentes só para membros</span></span>` +
    `<span class="vb">Quero entrar ✨</span>` +
    [[6, 20, 0], [18, 70, .8], [62, 18, 1.4], [80, 68, .4], [93, 30, 1.9]].map(([x, y, d]) => `<span class="ve" aria-hidden="true" style="left:${x}%;top:${y}%;animation-delay:${d}s">✦</span>`).join("") +
    `<button class="vx" type="button" aria-label="Fechar">×</button>`;
  document.documentElement.classList.add("vip-on");
  a.querySelector(".vx").addEventListener("click", (e) => {
    e.preventDefault(); e.stopPropagation(); a.remove(); document.documentElement.classList.remove("vip-on");
    try { sessionStorage.setItem("vip-fechada", "1"); } catch (er) {}
  });
  const pôr = () => document.body.insertBefore(a, document.body.firstChild);
  if (document.body) pôr(); else document.addEventListener("DOMContentLoaded", pôr);
})();
