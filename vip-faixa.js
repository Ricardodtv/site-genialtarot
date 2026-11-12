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

/* 01/11/2026 (pedido dele): a etiqueta «Loja Online». 3.ª versão: AO ALTO, na vertical, colada à borda direita, em cima
   (por baixo da faixa VIP e do botão do som) — estreita, para não invadir a página. Etiqueta de preço com furo e fio,
   rosa→roxo e dourado, a bater como um coração e a balançar do furo. Leva à Loja. Aparece a toda a gente (VIP incluídos),
   menos na própria Loja, no pagamento e na app «O Teu Céu». */
(function () {
  if (/^\/(loja|pagar|o-teu-ceu)(\.html)?$/.test(location.pathname)) return;
  if (document.getElementById("loja-etq")) return;
  const css = `
#loja-etq{position:fixed;right:0;top:calc(1rem + 3.9rem);z-index:9998;display:block;text-decoration:none;cursor:pointer;
  transform-origin:50% 0;animation:lojaBateV 2.2s ease-in-out infinite;
  filter:drop-shadow(-3px 4px 0 rgba(70,20,90,.85)) drop-shadow(0 8px 14px rgba(0,0,0,.5))}
html.vip-on #loja-etq{top:calc(1rem + 54px + 3.9rem)}
#loja-etq .lc{position:relative;display:flex;flex-direction:column;align-items:center;gap:.45rem;padding:1.75rem .5rem .85rem;
  font:800 14px/1 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#fff;letter-spacing:.06em;
  background:linear-gradient(180deg,#ff7ac3 0%,#c43c9b 35%,#7a2bb0 75%,#4b1475 100%);
  clip-path:polygon(0 15px,50% 0,100% 15px,100% 100%,0 100%);border-radius:0 0 0 6px}
#loja-etq .lc::before{content:"";position:absolute;inset:3px 3px 3px 3px;clip-path:polygon(0 13px,50% 0,100% 13px,100% 100%,0 100%);
  border:1.5px dashed rgba(255,226,140,.85);border-top:0;pointer-events:none}
#loja-etq .lf{position:absolute;top:11px;left:50%;width:8px;height:8px;margin-left:-4px;border-radius:50%;background:#2a0b40;
  box-shadow:0 0 0 2px #ffd978,inset 0 1px 2px rgba(0,0,0,.7)}
#loja-etq .lfio{position:absolute;top:-14px;left:50%;width:2px;height:28px;margin-left:-1px;background:linear-gradient(0deg,#ffd978,transparent);border-radius:2px}
#loja-etq .lt{writing-mode:vertical-rl;text-orientation:mixed;white-space:nowrap}
#loja-etq b{color:#ffe28c;text-shadow:0 1px 0 rgba(80,10,60,.6)}
#loja-etq .le{font-size:18px;display:inline-block;animation:lojaSaco 2.2s ease-in-out infinite;filter:drop-shadow(0 0 4px rgba(255,220,140,.8))}
#loja-etq .lb{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,transparent 35%,rgba(255,255,255,.5) 48%,transparent 60%);
  background-size:100% 260%;animation:lojaBrilhoV 3.4s ease-in-out infinite}
#loja-etq .lv{position:absolute;color:#ffe9a8;font-size:11px;pointer-events:none;animation:lojaEstrela 2.2s ease-in-out infinite;text-shadow:0 0 6px #ffd978}
#loja-etq .lo{position:absolute;inset:6px -4px -5px -5px;border-radius:8px 0 0 8px;pointer-events:none;box-shadow:0 0 0 0 rgba(255,122,195,.7);animation:lojaOnda 2.2s ease-out infinite}
#loja-etq:hover{animation-play-state:paused}
@keyframes lojaBateV{0%,100%{transform:rotate(0) scale(1)}12%{transform:rotate(-4deg) scale(1.1)}24%{transform:rotate(2deg) scale(1.02)}
  36%{transform:rotate(-3deg) scale(1.08)}55%{transform:rotate(1deg) scale(1)}75%{transform:rotate(-1deg)}}
@keyframes lojaOnda{0%,8%{box-shadow:0 0 0 0 rgba(255,122,195,.75)}60%,100%{box-shadow:0 0 0 14px rgba(255,122,195,0)}}
@keyframes lojaSaco{0%,100%{transform:rotate(-10deg)}12%,36%{transform:rotate(12deg) scale(1.15)}}
@keyframes lojaBrilhoV{0%{background-position:0 160%}55%,100%{background-position:0 -110%}}
@keyframes lojaEstrela{0%,100%{opacity:0;transform:scale(.3) rotate(0)}40%{opacity:1;transform:scale(1.2) rotate(45deg)}}
@media (max-width:520px){#loja-etq .lc{font-size:12.5px;padding:1.6rem .42rem .75rem}#loja-etq .le{font-size:16px}}
@media (prefers-reduced-motion:reduce){#loja-etq,#loja-etq .le,#loja-etq .lb,#loja-etq .lv,#loja-etq .lo{animation:none}}`;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  const a = document.createElement("a");
  a.id = "loja-etq"; a.href = "/ir-loja";   /* 12/11/2026 (ele): a loja do país de quem visita — o worker escolhe */ a.setAttribute("aria-label", "Loja Online");
  a.innerHTML = '<span class="lo" aria-hidden="true"></span><span class="lfio" aria-hidden="true"></span>' +
    '<span class="lc"><span class="lf" aria-hidden="true"></span><span class="le" aria-hidden="true">🛍️</span><span class="lt"><b>Loja</b> Online</span><span class="lb" aria-hidden="true"></span></span>' +
    [[-70, 18, 0], [-55, 70, .9], [-80, 95, 1.6]].map(([x, y, d]) => `<span class="lv" aria-hidden="true" style="left:${x}%;top:${y}%;animation-delay:${d}s">✦</span>`).join("");
  const pôr = () => document.body.appendChild(a);
  if (document.body) pôr(); else document.addEventListener("DOMContentLoaded", pôr);
})();
