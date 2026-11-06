/* Faixa do signo por cima do vídeo (06/11/2026, pedido dele). O corte de cada signo abre cerca de 6 segundos antes do início:
   mostra a imagem do signo e a contagem, para a pessoa perceber que está no signo certo. Fica fora do vídeo, nunca o tapa. */
(() => {
  const m = document.getElementById("sign-modal"), bar = m && m.querySelector(".sign-modal-bar"); if (!bar) return;
  const SEG = 6, st = document.createElement("style");
  st.textContent = `.sc-fita{display:flex;align-items:center;gap:.7rem;margin:0 0 .5rem;padding:.45rem .7rem;border-radius:.8rem;background:linear-gradient(135deg,#3a2160,#1d0d36);border:1px solid #f2c96b;color:#f7f0fb}
  .sc-fita img{width:3rem;height:3rem;border-radius:50%;object-fit:cover;border:2px solid #f2c96b;flex:none}.sc-fita b{display:block;color:#f2c96b;font-size:1.15rem;line-height:1.2}.sc-fita span{font-size:.92rem}
  .sc-fita strong{display:inline-block;min-width:1.5em;text-align:center;font-size:1.25rem;color:#fff}.sc-fita.pronto span{color:#3ddc84;font-weight:600}
  .sc-barra{height:4px;border-radius:9px;margin:-.3rem 0 .5rem;background:rgba(255,255,255,.12);overflow:hidden}.sc-barra i{display:block;height:100%;width:100%;background:#f2c96b;transform-origin:left}`;
  document.head.appendChild(st);
  const f = document.createElement("div"), b = document.createElement("div"); f.className = "sc-fita"; b.className = "sc-barra"; b.innerHTML = "<i></i>"; bar.after(f, b); f.hidden = b.hidden = true;
  const chave = (t) => { const k = t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim().split(/\s+/)[0]; return { aries: "carneiro", cancer: "caranguejo", libra: "balanca" }[k] || k; };
  let tempo = null, ligado = false;
  function para() { clearInterval(tempo); clearTimeout(tempo); ligado = false; f.hidden = b.hidden = true; }
  function conta(nome) {
    let n = SEG; const i = b.firstChild; i.style.transition = "none"; i.style.transform = "scaleX(1)"; void i.offsetWidth;
    i.style.transition = `transform ${SEG}s linear`; i.style.transform = "scaleX(0)";
    tempo = setInterval(() => { n--; const s = f.querySelector("strong");
      if (n > 0 && s) s.textContent = n; else { clearInterval(tempo); f.classList.add("pronto"); f.querySelector("span").textContent = "✓ A ver agora"; b.hidden = true; } }, 1000);
  }
  function abre() {
    const nome = document.getElementById("sign-modal-name").textContent.trim(); if (!nome) return;
    ligado = true; f.classList.remove("pronto"); f.hidden = b.hidden = false;
    f.innerHTML = `<img src="/signos/m/${chave(nome)}.webp" alt="" width="96" height="96"><div><b>${nome.replace(/</g, "&lt;")}</b><span>começa em <strong>${SEG}</strong> segundos</span></div>`;
    const v = m.querySelector("iframe"); let foi = false; const vai = () => { if (foi || !ligado) return; foi = true; conta(nome); };
    if (v) v.addEventListener("load", vai, { once: true }); tempo = setTimeout(vai, 2500);
  }
  new MutationObserver(() => { const o = m.classList.contains("open"); if (o && !ligado) abre(); else if (!o && ligado) para(); }).observe(m, { attributes: true, attributeFilter: ["class"] });
})();
