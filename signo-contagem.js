/* Faixa do signo por cima do vídeo (06/11/2026, pedido dele). O corte de cada signo abre cerca de 6 segundos antes do início:
   mostra a imagem do signo e a contagem, para a pessoa perceber que está no signo certo. Fica fora do vídeo, nunca o tapa. */
(() => {
  const m = document.getElementById("sign-modal"), bar = m && m.querySelector(".sign-modal-bar"); if (!bar) return;
  const SEG = 6, st = document.createElement("style");
  st.textContent = `.sc-fita{display:flex;align-items:center;gap:.7rem;margin:.2rem 0 .6rem;padding:.5rem .75rem;border-radius:.8rem;background:linear-gradient(135deg,#ffe28a,#f5b13d);border:2px solid #fff6d0;color:#2a1240;box-shadow:0 0 10px 2px rgba(255,200,70,.55);animation:sc-pulso 1s ease-in-out infinite}
  @keyframes sc-pulso{50%{box-shadow:0 0 26px 9px rgba(255,214,90,.95)}}
  .sc-fita img{width:3rem;height:3rem;border-radius:50%;object-fit:cover;border:2px solid #fff;flex:none}.sc-fita b{display:block;color:#3a1460;font-size:1.2rem;line-height:1.2;font-weight:800}.sc-fita span{font-size:.95rem;font-weight:600}
  .sc-fita strong{display:inline-block;min-width:1.55em;margin:0 .1em;padding:0 .2em;border-radius:.4em;text-align:center;font-size:1.3rem;color:#ffe28a;background:#3a1460}
  .sc-fita.pronto{animation:none;background:linear-gradient(135deg,#3a2160,#1d0d36);border-color:#3ddc84;color:#f7f0fb;box-shadow:0 0 8px rgba(61,220,132,.45)}.sc-fita.pronto b{color:#f2c96b}.sc-fita.pronto span{color:#3ddc84}
  .sc-barra{height:4px;border-radius:9px;margin:-.2rem 0 .5rem;background:rgba(255,255,255,.12);overflow:hidden}.sc-barra i{display:block;height:100%;width:100%;background:#ffd76a;transform-origin:left}
  @media (prefers-reduced-motion:reduce){.sc-fita{animation:none}}`;
  document.head.appendChild(st);
  const f = document.createElement("div"), b = document.createElement("div"); f.className = "sc-fita"; b.className = "sc-barra"; b.innerHTML = "<i></i>"; bar.after(f, b); f.hidden = b.hidden = true;
  const chave = (t) => { const k = t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim().split(/\s+/)[0]; return { aries: "carneiro", cancer: "caranguejo", libra: "balanca" }[k] || k; };
  let tempo = null, ligado = false;
  function para() { clearInterval(tempo); clearTimeout(tempo); ligado = false; bar.querySelector(".name").style.visibility = ""; f.hidden = b.hidden = true; }
  function conta(nome) {
    let n = SEG; const i = b.firstChild; i.style.transition = "none"; i.style.transform = "scaleX(1)"; void i.offsetWidth;
    i.style.transition = `transform ${SEG}s linear`; i.style.transform = "scaleX(0)";
    tempo = setInterval(() => { n--; const s = f.querySelector("strong");
      if (n > 0 && s) { s.textContent = n; s.parentElement.lastChild.textContent = n === 1 ? " segundo" : " segundos"; } else { clearInterval(tempo); f.classList.add("pronto"); f.querySelector("span").textContent = "✓ A ver agora"; b.hidden = true; } }, 1000);
  }
  function abre() {
    const nome = document.getElementById("sign-modal-name").textContent.trim(); if (!nome) return;
    ligado = true; bar.querySelector(".name").style.visibility = "hidden"; f.classList.remove("pronto"); f.hidden = b.hidden = false;
    f.innerHTML = `<img src="/signos/m/${chave(nome)}.webp" alt="" width="96" height="96"><div><b>${nome.replace(/</g, "&lt;")}</b><span>começa em <strong>${SEG}</strong> segundos</span></div>`;
    const v = m.querySelector("iframe"); let foi = false; const vai = () => { if (foi || !ligado) return; foi = true; conta(nome); };
    if (v) v.addEventListener("load", vai, { once: true }); tempo = setTimeout(vai, 2500);
  }
  new MutationObserver(() => { const o = m.classList.contains("open"); if (o && !ligado) abre(); else if (!o && ligado) para(); }).observe(m, { attributes: true, attributeFilter: ["class"] });
})();
