/* 30/10/2026 (pedido dele): a caixa «Quero receber novidades» mais vistosa, e — só a quem NÃO a marcou —
   uma janela bonita ao carregar no botão do pedido, com «Sim, aceito» e «Não aceito».
   Serve as 13 páginas que têm a caixa (input#novidades dentro de label.caixa-novidades).
   O consentimento continua a ser escolha da pessoa: a caixa nunca vem marcada e o «Não aceito» está à vista. */
(function () {
  const caixa = document.getElementById("novidades");
  if (!caixa) return;

  const css = `
.caixa-novidades{position:relative;padding:.9em 1em!important;margin:.6em 0!important;border-radius:14px;
  background:linear-gradient(135deg,rgba(255,217,120,.16),rgba(160,48,122,.22));border:1.5px solid rgba(255,217,120,.7);
  box-shadow:0 0 0 0 rgba(255,215,120,.55),0 6px 22px -8px rgba(255,200,90,.55);animation:novPulsa 2.4s ease-out infinite;transition:background .25s}
.caixa-novidades.marcada{animation:none;background:linear-gradient(135deg,rgba(255,217,120,.30),rgba(160,48,122,.30));border-color:#ffd978}
.caixa-novidades .nov-tit{display:block;font-weight:800;color:#ffd978;font-size:1.06em;margin-bottom:.2em;letter-spacing:.01em}
.caixa-novidades input#novidades{width:1.55em!important;height:1.55em!important;margin:.1em 0 0!important;accent-color:#f0b440!important;cursor:pointer}
@keyframes novPulsa{0%{box-shadow:0 0 0 0 rgba(255,215,120,.5),0 6px 22px -8px rgba(255,200,90,.55)}70%,100%{box-shadow:0 0 0 10px rgba(255,215,120,0),0 6px 22px -8px rgba(255,200,90,.55)}}
#nov-fundo{position:fixed;inset:0;z-index:100000;display:flex;align-items:center;justify-content:center;padding:1.2rem;
  background:rgba(10,3,20,.72);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);animation:novEntra .25s ease-out}
#nov-jan{position:relative;max-width:420px;width:100%;box-sizing:border-box;padding:2rem 1.5rem 1.4rem;border-radius:22px;text-align:center;
  font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#fff;
  background:radial-gradient(120% 90% at 50% 0%,#6d1f8f 0%,#3b0f5c 55%,#1c0630 100%);border:2px solid #ffd978;
  box-shadow:0 0 0 1px rgba(255,217,120,.25),0 20px 60px -10px rgba(255,200,90,.55);animation:novSobe .35s cubic-bezier(.2,.9,.3,1.2)}
#nov-jan .ni{font-size:52px;line-height:1;filter:drop-shadow(0 0 12px rgba(255,215,120,.9));animation:novPresente 1.8s ease-in-out infinite;display:inline-block}
#nov-jan h3{margin:.6rem 0 .5rem;font-size:1.35rem;line-height:1.25;color:#ffd978;font-weight:800}
#nov-jan p{margin:0 0 1.2rem;font-size:1rem;line-height:1.5;color:#f1e6ff}
#nov-jan ul{list-style:none;margin:0 0 1.3rem;padding:0;text-align:left;display:inline-block;font-size:.98rem;line-height:1.8;color:#fff}
#nov-jan .ns{display:block;width:100%;padding:.95rem 1rem;border:0;border-radius:999px;cursor:pointer;font:900 1.08rem Inter,system-ui,sans-serif;
  color:#2a1300;background:linear-gradient(135deg,#ffe49a,#f0b440);box-shadow:0 8px 24px -6px rgba(240,180,64,.8);animation:novPulsaB 1.6s ease-out infinite}
#nov-jan .nn{display:block;width:100%;margin-top:.7rem;padding:.8rem 1rem;border-radius:999px;cursor:pointer;font:700 1rem Inter,system-ui,sans-serif;
  color:#f1e6ff;background:transparent;border:1.5px solid rgba(241,230,255,.45)}
#nov-jan .nn:hover{background:rgba(255,255,255,.08)}
#nov-jan small{display:block;margin-top:1rem;font-size:.8rem;color:#cdb8e6}
@keyframes novEntra{from{opacity:0}}
@keyframes novSobe{from{opacity:0;transform:translateY(24px) scale(.95)}}
@keyframes novPresente{0%,100%{transform:translateY(0) rotate(-6deg)}50%{transform:translateY(-4px) rotate(6deg)}}
@keyframes novPulsaB{0%{box-shadow:0 0 0 0 rgba(255,215,120,.7)}80%,100%{box-shadow:0 0 0 12px rgba(255,215,120,0)}}
@media (prefers-reduced-motion:reduce){.caixa-novidades,#nov-jan,#nov-jan .ni,#nov-jan .ns,#nov-fundo{animation:none}}`;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  // ── a caixa: título dourado por cima do texto que já lá estava ──
  const lab = caixa.closest("label");
  if (lab) {
    const span = lab.querySelector("span");
    if (span && !lab.querySelector(".nov-tit")) {
      const t = document.createElement("b"); t.className = "nov-tit"; t.textContent = "🎁 Presentes e promoções do Mestre Alberto";
      span.prepend(t);
    }
    const marca = () => lab.classList.toggle("marcada", caixa.checked);
    caixa.addEventListener("change", marca); marca();
  }

  // ── a janela: só se a caixa não estiver marcada, com um email válido escrito, e uma vez por visita ──
  let respondeu = false;
  const jaVip = () => { try { return !!localStorage.getItem("vip-entrou"); } catch (e) { return false; } };
  const emailOk = () => {
    const e = document.querySelector('input[type="email"]');
    return !!e && /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(e.value.trim());
  };
  const deveParar = () => !respondeu && !caixa.checked && !jaVip() && emailOk();

  function janela(continuar) {
    const f = document.createElement("div"); f.id = "nov-fundo";
    f.innerHTML = `<div id="nov-jan" role="dialog" aria-modal="true" aria-labelledby="nov-t">
      <span class="ni">🎁</span>
      <h3 id="nov-t">Quer receber os presentes do Mestre Alberto?</h3>
      <ul><li>🔮 Horóscopos e previsões</li><li>🌙 Mapas e leituras especiais</li><li>💛 Promoções só para quem está na lista</li></ul>
      <button type="button" class="ns">✨ Sim, aceito</button>
      <button type="button" class="nn">Não aceito</button>
      <small>Só no seu email. Pode cancelar quando quiser.</small></div>`;
    document.body.appendChild(f);
    const fecha = (sim) => {
      respondeu = true;
      if (sim) { caixa.checked = true; caixa.dispatchEvent(new Event("change", { bubbles: true })); }
      f.remove(); continuar();
    };
    f.querySelector(".ns").addEventListener("click", () => fecha(true));
    f.querySelector(".nn").addEventListener("click", () => fecha(false));
    f.querySelector(".ns").focus();
  }

  // Páginas com <form>: apanha o envio antes da página (fase de captura no document).
  document.addEventListener("submit", (ev) => {
    const form = ev.target;
    if (!form.contains(caixa) || !deveParar()) return;
    ev.preventDefault(); ev.stopImmediatePropagation();
    janela(() => (form.requestSubmit ? form.requestSubmit() : form.submit()));
  }, true);

  // Páginas sem <form> (Tarot Grátis, Árvore da Vida): o botão de jogar.
  ["play-btn", "btn-lancar"].forEach((id) => {
    const b = document.getElementById(id);
    if (!b) return;
    document.addEventListener("click", (ev) => {
      if (!b.contains(ev.target) || !deveParar()) return;
      ev.preventDefault(); ev.stopImmediatePropagation();
      janela(() => b.click());
    }, true);
  });
  // ── 30/10/2026 (pedido dele): o resultado vai também para o email da pessoa ──
  // Quando a página manda a captura para a ponte, espera que o resultado apareça, tira-lhe o texto
  // (sem botões nem a parte paga) e manda-o à fila como «resultado». O cerebro envia o email.
  const CAPTURAS = ["reading", "ascendente", "mapa-captura"];
  const textoDe = (el) => {
    const c = el.cloneNode(true);
    c.querySelectorAll("button,input,select,textarea,form,script,style,svg,canvas,audio,video,iframe,[aria-hidden=true],.btn,.cta,.lock,.bloqueado,[class*=desbloq],[class*=compra],[class*=partilh],[class*=paga]").forEach((x) => x.remove());
    c.querySelectorAll("a").forEach((a) => { if (/→|comprar|desbloquear|partilhar|saber mais|significado|ler tudo/i.test(a.textContent)) a.remove(); });
    c.querySelectorAll("h1,h2,h3,h4,h5,p,li,section,article,blockquote,[class*=tema],[class*=bloco],[class*=cartao]").forEach((x) => x.insertAdjacentHTML("beforebegin", "<br><br>"));
    c.style.cssText = "position:absolute;left:-99999px;top:0;width:600px"; document.body.appendChild(c);
    const t = (c.innerText || "").split("\n").map((l) => l.replace(/\s+/g, " ").trim()).filter((l) => !l || /[\p{L}\d]/u.test(l)).join("\n");
    c.remove();
    return t.replace(/\n{3,}/g, "\n\n").slice(0, 12000);
  };
  // 30/10 (ele: «o texto podia estar mais organizado»): além do texto, a ESTRUTURA do resultado — títulos,
  // etiquetas, parágrafos, listas e grelhas (os meses, os números) — para o email ser desenhado como a página.
  const LIXO = "button,input,select,textarea,form,script,style,svg,canvas,audio,video,iframe,[aria-hidden=true],.btn,.cta,.lock,.bloqueado,[class*=desbloq],[class*=compra],[class*=partilh],[class*=paga]";
  const blocos = (el) => {
    const out = [], visto = new Set();
    const cs = (x) => getComputedStyle(x);
    const txt = (x) => (x.innerText || "").replace(/\s+/g, " ").trim();
    const bloco = (x) => /^(block|flex|grid|list-item|table|inline-flex|inline-grid)$/.test(cs(x).display);
    const anda = (x) => {
      if (visto.has(x) || x.matches(LIXO) || cs(x).display === "none" || cs(x).visibility === "hidden") return;
      if (x.tagName === "A" && /→|comprar|desbloquear|partilhar|saber mais|significado|ler tudo/i.test(x.textContent)) return;
      const filhos = [...x.children].filter((c) => !c.matches(LIXO) && cs(c).display !== "none" && txt(c));
      const st = cs(x);
      // grelha: muitos filhos curtos lado a lado (os 12 meses, os números do cálculo)
      if (/(grid|flex)/.test(st.display) && filhos.length >= 3 && filhos.every((c) => txt(c).length <= 40) && st.flexDirection !== "column") {
        out.push({ k: "grade", i: filhos.map((c) => (c.innerText || "").split("\n").map((l) => l.trim()).filter(Boolean).join(" · ")) }); return;
      }
      const temBlocos = filhos.some(bloco);
      if (!temBlocos) {
        const t = txt(x); if (!t || !/[\p{L}\d]/u.test(t)) return;
        const tag = x.tagName, peso = parseInt(st.fontWeight) || 400, tam = parseFloat(st.fontSize) || 16;
        const k = /^H[1-4]$/.test(tag) || (peso >= 600 && tam >= 18 && t.length < 120) ? "h"
          : tag === "LI" ? "li"
          : (st.textTransform === "uppercase" || t === t.toUpperCase()) && t.length <= 40 ? "e"
          : "p";
        out.push({ k, t: t.slice(0, 2000) }); return;
      }
      [...x.children].forEach(anda);
    };
    anda(el);
    return out.slice(0, 250);
  };
  const enviarResultado = (d) => {
    const el = document.getElementById("resultado") || document.getElementById("leitura");
    const texto = el && el.offsetParent !== null ? textoDe(el) : "";
    let estrutura = [];
    try { estrutura = el && el.offsetParent !== null ? blocos(el) : []; } catch (e) {}
    const tit = (document.getElementById("res-titulo") || {}).textContent || "";
    fetch("/notify", { method: "POST", headers: { "Content-Type": "application/json" }, keepalive: true,
      body: JSON.stringify({ type: "resultado", data: { name: d.name, email: d.email, city: d.city || "", area: d.area || "",
        titulo: tit.trim().slice(0, 200), texto, estrutura, verdict: d.verdict || "", pagina: location.pathname, novidades: !!caixa.checked } }) }).catch(() => {});
  };
  const fOrig = window.fetch;
  window.fetch = function (url, opt) {
    try {
      if (String(url).endsWith("/notify") && opt && opt.body) {
        const b = JSON.parse(opt.body);
        if (b && CAPTURAS.includes(b.type) && b.data && b.data.email) setTimeout(() => enviarResultado(b.data), 3500);
      }
    } catch (e) {}
    return fOrig.apply(this, arguments);
  };
})();
