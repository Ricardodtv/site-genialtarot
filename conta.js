/* conta.js — 05/11/2026, pedido dele: o botão «Entrar», em cima à direita, em todas as páginas.
   Carregado pelo vivo.js (que já está em todas), por isso não há nada a pôr em cada página.
   - Quem nunca entrou não faz pedido nenhum ao servidor: só se pergunta com a marca «gt_conta» (o primeiro nome) no navegador.
     A sessão a sério é um cookie HttpOnly, que este código não consegue ler.
   - Com sessão, preenche os formulários; quem mudar um campo, muda. Sem sessão, os formulários ficam como sempre foram.
   - #data2, #nome2 e #hora2 são da outra pessoa (Mapa do Casal): ficam vazios de propósito. */
(function () {
  if (window.gtConta) return;
  if (/^\/(consultorio|o-teu-ceu|pagar)(\/|\.html|-sala|$)/.test(location.pathname)) return;
  var A = "/api/conta/", MARCA = "gt_conta", CACHE = "gt_conta_dados", VOLTA = "gt_conta_volta", DEZ_MIN = 6e5;
  var conta = null, config = null, btn = null, menu = null, dlg = null;

  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} return null; }
  function api(c, corpo) {
    var o = { credentials: "same-origin", cache: "no-store" };
    if (corpo) { o.method = "POST"; o.headers = { "Content-Type": "application/json" }; o.body = JSON.stringify(corpo); }
    return fetch(A + c, o).then(function (r) { return r.json().catch(function () { return { ok: false }; }); });
  }
  function primeiro(n) { return String(n || "").trim().split(/\s+/)[0] || "A minha conta"; }
  function guardar(c) {
    conta = c; ls(MARCA, primeiro(c.nome));
    try { sessionStorage.setItem(CACHE, JSON.stringify({ t: Date.now(), c: c })); } catch (e) {}
    desenhar();
  }
  function esquecer() {
    conta = null; ls(MARCA, null);
    try { sessionStorage.removeItem(CACHE); } catch (e) {}
    desenhar();
  }
  function ler() {   // devolve a conta, ou null
    if (!ls(MARCA)) return Promise.resolve(null);
    try { var g = JSON.parse(sessionStorage.getItem(CACHE) || "null"); if (g && Date.now() - g.t < DEZ_MIN) { conta = g.c; return Promise.resolve(g.c); } } catch (e) {}
    return api("eu").then(function (r) { if (r && r.ok) { if (r.sessao) guardar(r.conta); else esquecer(); } return conta; }).catch(function () { return null; });
  }
  function fresco() { try { sessionStorage.removeItem(CACHE); } catch (e) {} return ler(); }
  function pedirConfig() {
    if (config) return Promise.resolve(config);
    return api("config").then(function (r) { if (r && r.ok) config = r; return config; }).catch(function () { return null; });
  }

  // ---------- o aspecto ----------
  function estilo() {
    var s = document.createElement("style"); s.id = "gtc-css";
    s.textContent = "#gtc-btn{position:fixed;top:1rem;right:4.5rem;z-index:9990;display:inline-flex;align-items:center;gap:.4rem;box-sizing:border-box;height:3rem;max-width:9.5rem;margin:0;padding:0 .95rem;border-radius:9999px;border:1.5px solid oklch(0.82 0.11 85);background:oklch(0.22 0.05 265 / .92);color:oklch(0.82 0.11 85);font:600 15px/1 Inter,system-ui,-apple-system,'Segoe UI',sans-serif;box-shadow:0 6px 22px rgba(0,0,0,.5);cursor:pointer;transition:transform .25s}" +
      "#gtc-btn:hover{transform:scale(1.05)}#gtc-btn svg{flex:none;width:18px;height:18px}#gtc-btn span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}" +
      "html.gtc-sem-som #gtc-btn{right:1rem}html.vip-on #gtc-btn{top:calc(1rem + 54px)}" +
      "#gtc-menu{position:fixed;z-index:9991;min-width:190px;padding:.35rem;box-sizing:border-box;background:#1d0d36;border:1px solid rgba(242,201,107,.45);border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.55);font:500 15px/1.3 Inter,system-ui,sans-serif}" +
      "#gtc-menu[hidden]{display:none}#gtc-menu a,#gtc-menu button{display:block;box-sizing:border-box;width:100%;padding:.65rem .8rem;border:0;border-radius:9px;background:none;color:#f7f0fb;font:inherit;text-align:left;text-decoration:none;cursor:pointer}" +
      "#gtc-menu a:hover,#gtc-menu button:hover,#gtc-menu a:focus,#gtc-menu button:focus{background:rgba(242,201,107,.15)}#gtc-menu .gtc-perigo{color:#ffb0b0}" +
      "#gtc-dlg{box-sizing:border-box;width:min(430px,calc(100vw - 24px));max-height:calc(100dvh - 24px);margin:auto;padding:1.5rem 1.35rem 1.3rem;overflow:auto;background:#1d0d36;color:#f7f0fb;border:1px solid rgba(242,201,107,.45);border-radius:20px;box-shadow:0 18px 60px rgba(0,0,0,.65);font:16px/1.5 Inter,system-ui,-apple-system,'Segoe UI',sans-serif}" +
      "#gtc-dlg::backdrop{background:rgba(10,3,20,.72)}#gtc-dlg h2{margin:0 2rem .35rem 0;color:#f2c96b;font:700 1.45rem/1.2 Cinzel,Georgia,serif;letter-spacing:0}#gtc-dlg p{margin:.4rem 0;color:#e5d8f2;font-size:.95rem}" +
      "#gtc-dlg .gtc-x{position:absolute;top:.7rem;right:.7rem;width:36px;height:36px;padding:0;border:0;border-radius:50%;background:none;color:#cdb8e6;font-size:22px;line-height:1;cursor:pointer}#gtc-dlg .gtc-x:hover{background:rgba(255,255,255,.1)}" +
      "#gtc-dlg .gtc-conv{display:block;margin:.3rem 0 0;font-size:.8rem;line-height:1.3;font-weight:600;color:#ffd978}#gtc-dlg input.gtc-falta{border-color:#ffd978;animation:gtcPulsa 1.8s ease-out infinite}@keyframes gtcPulsa{0%{box-shadow:0 0 0 0 rgba(255,217,120,.6)}80%,100%{box-shadow:0 0 0 8px rgba(255,217,120,0)}}" +
      "#gtc-dlg .gtc-seta{flex:none;width:1.6em;height:1.4em;margin:.05em .15em 0 0;animation:gtcSeta .9s ease-in-out infinite;filter:drop-shadow(0 0 5px rgba(255,215,120,.95))}@keyframes gtcSeta{0%,100%{opacity:1;transform:translateX(0)}50%{opacity:.25;transform:translateX(4px)}}@media (prefers-reduced-motion:reduce){#gtc-dlg .gtc-seta,#gtc-dlg input.gtc-falta{animation:none}}" +
      "#gtc-dlg label.gtc-c{display:block;margin:.8rem 0 0;color:#f6efff;font-size:.9rem;font-weight:600}#gtc-dlg label.gtc-c small{font-weight:400;color:#cdb8e6}" +
      "#gtc-dlg input.gtc-i{display:block;box-sizing:border-box;width:100%;height:auto;margin:.3rem 0 0;padding:.7rem .8rem;border:1px solid rgba(242,201,107,.4);border-radius:11px;background:#140826;color:#f7f0fb;font:16px/1.3 Inter,system-ui,sans-serif}#gtc-dlg input.gtc-i::placeholder{color:#9d8cb3;opacity:1}#gtc-dlg input.gtc-i:focus{outline:2px solid #f2c96b;outline-offset:1px}" +
      "#gtc-dlg .gtc-ok{display:block;box-sizing:border-box;width:100%;margin:1rem 0 0;padding:.8rem 1rem;border:0;border-radius:12px;background:linear-gradient(135deg,#ffe49a,#f0b440);color:#2a1300;font:800 16px/1.2 Inter,system-ui,sans-serif;cursor:pointer}#gtc-dlg .gtc-ok:disabled{opacity:.6;cursor:wait}" +
      "#gtc-dlg .gtc-2{display:block;width:100%;margin:.5rem 0 0;padding:.6rem;border:0;background:none;color:#cdb8e6;font:500 14.5px Inter,system-ui,sans-serif;cursor:pointer;text-decoration:underline}" +
      "#gtc-dlg .gtc-ou{display:flex;align-items:center;gap:.7rem;margin:1rem 0 .1rem;color:#a893bd;font-size:.85rem}#gtc-dlg .gtc-ou::before,#gtc-dlg .gtc-ou::after{content:'';flex:1;height:1px;background:rgba(255,255,255,.14)}" +
      "#gtc-dlg #gtc-g{display:flex;justify-content:center;align-items:center;min-height:64px;margin:1.1rem 0 .4rem}" +
      "#gtc-dlg .gtc-mail{margin:.6rem 0 0}#gtc-dlg .gtc-mail summary{display:block;width:max-content;max-width:100%;margin:0 auto;padding:.5rem .6rem;list-style:none;color:#cdb8e6;font-size:.85rem;text-decoration:underline;text-underline-offset:3px;cursor:pointer}#gtc-dlg .gtc-mail summary::-webkit-details-marker{display:none}" +
      "#gtc-dlg .gtc-mail label.gtc-c{margin-top:.5rem;font-size:.82rem}#gtc-dlg .gtc-mail input.gtc-i{padding:.5rem .7rem;font-size:.9rem}#gtc-dlg .gtc-mail .gtc-ok{margin-top:.7rem;padding:.55rem .8rem;border:1px solid rgba(242,201,107,.55);background:transparent;color:#f2c96b;font-size:.88rem}" +
      " #gtc-dlg .gtc-er{min-height:1.2em;margin:.6rem 0 0;color:#ff9d9d;font-size:.9rem}" +
      "#gtc-dlg .gtc-peq{margin-top:.8rem;color:#b9a6cf;font-size:.8rem}#gtc-dlg a{color:#f2c96b}#gtc-dlg .gtc-msg{min-height:1.2em;margin:.2rem 0 0;color:#e8cf95;font-size:.82rem}" +
      "#gtc-dlg label.gtc-mkt{display:flex;gap:.6em;align-items:flex-start;margin:1rem 0 0;font-size:.88rem;line-height:1.4;color:#e5d8f2;cursor:pointer}#gtc-dlg label.gtc-mkt input{flex:none;width:1.15em;height:1.15em;margin:.15em 0 0;accent-color:#f2c96b}" +
      "@media (max-width:520px){#gtc-btn{height:2.75rem;top:1.12rem;padding:0 .75rem;max-width:7.6rem;font-size:14px}html.vip-on #gtc-btn{top:calc(1.12rem + 54px)}}" +
      "#gtc-btn.gtc-so{gap:0;width:2.75rem;padding:0;justify-content:center}#gtc-btn.gtc-so span{display:none}" +
      "@media (max-width:430px){.brand-sub{display:none}}@media (max-width:360px){#gtc-btn{gap:0;padding:0 .7rem;max-width:5.2rem}#gtc-btn svg{display:none}}" +
      "@media (prefers-reduced-motion:reduce){#gtc-btn{transition:none}}";
    document.head.appendChild(s);
  }
  var ICONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>';

  function desenhar() {
    if (!btn) return;
    var nome = ls(MARCA);
    btn.innerHTML = ICONE + "<span></span>"; btn.lastChild.textContent = nome || "Entrar";
    btn.setAttribute("aria-label", nome ? "A sua conta: " + nome : "Entrar");
    if (nome) btn.setAttribute("aria-haspopup", "menu"); else btn.removeAttribute("aria-haspopup");
    fecharMenu(); posicionar();
  }
  // Cerca de 110 páginas têm no topo direito uma ligação ou um título próprio. Se o sítio normal bater nalguma coisa, procura-se o primeiro livre.
  function posicionar() {
    if (!btn) return;
    var W = document.documentElement.clientWidth, Y = window.scrollY || 0, ob = [];
    btn.style.top = btn.style.right = ""; btn.classList.remove("gtc-so");
    var r = btn.getBoundingClientRect(), base = { t: r.top, d: W - r.right, w: r.width, h: r.height };
    function junta(q) { if (q.width && q.height && q.left < W && q.top < 170) ob.push({ l: q.left, r: q.right, t: q.top, b: q.bottom }); }
    [].forEach.call(document.querySelectorAll('body a,.marca,.som-fix,.btn-som,#loja-etq'), function (e) {
      if (e === btn || e.closest("#vip-faixa,#gt-chat,#gtc-menu,#gtc-dlg") || !(e.textContent || "").trim() && !e.matches(".som-fix,.btn-som")) return;
      var q = e.getBoundingClientRect(), fixo = e.matches(".som-fix,.btn-som,#loja-etq");
      if (!fixo && Y) q = { left: q.left, right: q.right, top: q.top + Y, bottom: q.bottom + Y, width: q.width, height: q.height };
      if (fixo || q.width < W * 0.7) return junta(q);
      var g = document.createRange(); g.selectNodeContents(e);
      [].forEach.call(g.getClientRects(), function (c) { junta({ left: c.left, right: c.right, top: c.top + Y, bottom: c.bottom + Y, width: c.width, height: c.height }); });
    });
    function bate(t, d, w) {
      var l = W - d - w, f = W - d;
      return ob.some(function (o) { return l < o.r + 4 && f > o.l - 4 && t < o.b + 2 && t + base.h > o.t - 2; });
    }
    if (!bate(base.t, base.d, base.w)) return;
    var so = base.h, cand = [], i;
    cand.push([base.t, base.d, base.w, 0]);
    if (W <= 520) cand.push([base.t, base.d, so, 1]);
    ob.forEach(function (o) { if (o.t < base.t + base.h && o.l > W / 2) cand.push([base.t, W - o.l + 8, base.w, 0]); });
    var fundo = Math.max.apply(null, ob.filter(function (o) { return o.t < base.t + base.h && o.b > base.t; }).map(function (o) { return o.b; }));
    [base.d, 56, 72].forEach(function (d) { cand.push([fundo + 8, d, base.w, 0]); });
    for (i = 0; i < cand.length; i++) {
      if (W - cand[i][1] - cand[i][2] >= 8 && !bate(cand[i][0], cand[i][1], cand[i][2])) {
        btn.style.top = cand[i][0] + "px"; btn.style.right = cand[i][1] + "px"; btn.classList.toggle("gtc-so", !!cand[i][3]);
        return;
      }
    }
  }
  function fecharMenu() { if (menu) { menu.hidden = true; if (btn) btn.setAttribute("aria-expanded", "false"); } }
  function abrirMenu() {
    if (!menu) {
      menu = document.createElement("div"); menu.id = "gtc-menu"; menu.setAttribute("role", "menu"); menu.hidden = true;
      menu.innerHTML = '<a role="menuitem" href="/conta">Os meus dados</a><button role="menuitem" type="button" data-a="sair">Sair</button><a role="menuitem" class="gtc-perigo" href="/conta#apagar">Apagar conta</a>';
      menu.querySelector("[data-a=sair]").onclick = sair;
      document.body.appendChild(menu);
    }
    var r = btn.getBoundingClientRect();
    menu.style.top = Math.round(r.bottom + 8) + "px"; menu.style.right = Math.max(8, Math.round(document.documentElement.clientWidth - r.right)) + "px";
    menu.hidden = false; btn.setAttribute("aria-expanded", "true");
    var p = menu.querySelector("a,button"); if (p) p.focus();
  }
  function sair() {
    fecharMenu();
    return api("sair", {}).catch(function () {}).then(function () { esquecer(); location.reload(); });
  }

  // ---------- as janelas ----------
  function janela(html) {
    if (!dlg) {
      dlg = document.createElement("dialog"); dlg.id = "gtc-dlg"; dlg.setAttribute("aria-labelledby", "gtc-t");
      document.body.appendChild(dlg);
    }
    dlg.oncancel = null;
    dlg.innerHTML = '<button class="gtc-x" type="button" aria-label="Fechar">×</button>' + html;
    dlg.querySelector(".gtc-x").onclick = function () { dlg.close(); };
    if (!dlg.open) dlg.showModal();
    return dlg;
  }
  var ERROS = { nome: "Escreva o seu nome.", email: "Esse email não parece certo. Confirme, por favor.", muitos: "Foram muitos pedidos seguidos. Tente daqui a alguns minutos.",
    data: "Essa data não parece certa. Confirme, por favor.", hora: "Essa hora não parece certa. Escreva, por exemplo, 14:30.", sessao: "A sua sessão terminou. Entre outra vez.", google: "Não foi possível entrar com o Google. Tente outra vez." };
  function erroDe(r) { return ERROS[r && r.erro] || "Não foi possível agora. Tente outra vez daqui a pouco."; }

  function abrirEntrar() {
    var d = janela('<h2 id="gtc-t">Entrar</h2><p>Entre uma vez e deixa de preencher o nome e a data de nascimento nos formulários do site.</p>' +
      '<div id="gtc-gz"><div id="gtc-g"></div></div>' +
      '<details class="gtc-mail"><summary>Prefiro entrar com o email</summary>' +
      '<form novalidate><label class="gtc-c">Nome<input class="gtc-i" name="nome" autocomplete="name" maxlength="80" required></label>' +
      '<label class="gtc-c">Email<input class="gtc-i" name="email" type="email" autocomplete="email" maxlength="254" required></label>' +
      '<input name="site" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">' +
      '<button class="gtc-ok" type="submit">Enviar ligação para entrar</button><p class="gtc-er" role="alert"></p></form>' +
      '<p class="gtc-peq">Sem palavra-passe: enviamos-lhe uma ligação para confirmar o email.</p></details>' +
      '<p class="gtc-peq">Saiba como tratamos os seus dados na <a href="/privacidade">Política de Privacidade</a>.</p>');
    var f = d.querySelector("form"), er = d.querySelector(".gtc-er"), mail = d.querySelector(".gtc-mail");
    // 07/11 (ele): o Google vem primeiro, grande, por ser mais rápido; o email fica recolhido. Sem Google, o email abre sozinho.
    function soEmail() { var z = d.querySelector("#gtc-gz"); if (z) z.hidden = true; mail.open = true; f.nome.focus(); }
    mail.addEventListener("toggle", function () { if (mail.open) f.nome.focus(); });
    f.onsubmit = function (e) {
      e.preventDefault(); er.textContent = "";
      var b = f.querySelector("button"), email = f.email.value.trim(); b.disabled = true;
      api("pedir", { nome: f.nome.value.trim(), email: email, site: f.site.value }).then(function (r) {
        b.disabled = false;
        if (!r || !r.ok) { er.textContent = erroDe(r); return; }
        ls(VOLTA, location.pathname + location.search);
        aEspera(email);
      }).catch(function () { b.disabled = false; er.textContent = erroDe(); });
    };
    pedirConfig().then(function (c) { if (!dlg.open) return; if (c && c.google) google(c.google, soEmail); else soEmail(); }, soEmail);
  }
  function aEspera(email) {
    var d = janela('<h2 id="gtc-t">Veja o seu email</h2><p>Vamos enviar uma ligação para <b></b>. Deve chegar dentro de segundos e é válida durante 15 minutos.</p>' +
      '<p>Se não a encontrar, veja na pasta de Spam ou de Promoções. Depois de carregar nela, volta aqui já com a sessão aberta.</p><button class="gtc-ok" type="button">Percebi</button><button class="gtc-2" type="button">Enganei-me no email</button>');
    d.querySelector("b").textContent = email;
    d.querySelector(".gtc-ok").onclick = function () { d.close(); };
    d.querySelector(".gtc-2").onclick = abrirEntrar;
  }
  function google(id, falhou) {
    function mostra() {
      if (!window.google || !google_id() || !dlg.open) return falhou && falhou();
      var z = dlg.querySelector("#gtc-gz"), g = dlg.querySelector("#gtc-g"); if (!z) return;
      google_id().initialize({ client_id: id, callback: credencial, ux_mode: "popup", auto_select: false, context: "signin" });
      var esc = 1.22;   // o Google não faz botões maiores que «large»: aumenta-se por fora
      g.innerHTML = '<div id="gtc-g2"></div>'; g.firstChild.style.transform = "scale(" + esc + ")";
      google_id().renderButton(g.firstChild, { theme: "filled_blue", size: "large", text: "continue_with", shape: "pill", locale: "pt-PT", width: Math.min(400, Math.round((g.clientWidth || 300) / esc)) });
    }
    if (window.google && google_id()) return mostra();
    var s = document.createElement("script"); s.src = "https://accounts.google.com/gsi/client"; s.async = true; s.onload = mostra; s.onerror = function () { if (falhou) falhou(); }; document.head.appendChild(s);
  }
  function google_id() { return window.google && window.google.accounts && window.google.accounts.id; }
  function credencial(r) {
    api("google", { credential: r.credential }).then(function (x) {
      if (x && x.ok) return entrou(x);
      var er = dlg && dlg.querySelector(".gtc-er"); if (er) er.textContent = erroDe(x);
    }).catch(function () { var er = dlg && dlg.querySelector(".gtc-er"); if (er) er.textContent = erroDe(); });
  }
  function entrou(r, depois) {
    guardar(r.conta);
    if (!r.conta.nasc) return primeiraVez(depois);
    if (dlg && dlg.open) dlg.close();
    preencher();
    if (depois) depois();
  }
  function comDataFacil() {
    if (window.dataFacil) return Promise.resolve();
    return new Promise(function (ok) { var s = document.createElement("script"); s.src = "/data-facil.js"; s.onload = ok; s.onerror = ok; document.head.appendChild(s); });
  }
  function lerHora(t) {   // 14:30, 14h30, 1430, 9h, 9 → «HH:MM»; vazio devolve «»; inválida devolve null
    t = String(t || "").trim(); if (!t) return "";
    var m = t.match(/^(\d{1,2})(?:\s*[:hH.]\s*(\d{2})?)?\s*$/) || t.match(/^(\d{2})(\d{2})$/);
    if (!m || +m[1] > 23 || +(m[2] || 0) > 59) return null;
    return ("0" + m[1]).slice(-2) + ":" + (m[2] || "00");
  }
  function primeiraVez(depois) {
    var d = janela('<h2 id="gtc-t">Só mais um passo</h2><p>Com a sua data de nascimento, os mapas e os cálculos do site já vêm preenchidos. Pode alterar quando quiser.</p>' +
      '<form novalidate><label class="gtc-c">Data de nascimento<input class="gtc-i" name="nasc" autocomplete="bday" maxlength="32" placeholder="Ex.: 23/01/1976 ou 23 janeiro 1976"></label><p class="gtc-msg" aria-live="polite"></p>' +
      '<label class="gtc-c">Hora de nascimento <small>(opcional)</small><input class="gtc-i" name="hora" inputmode="numeric" autocomplete="off" maxlength="8" placeholder="Ex.: 14:30"></label>' +
      '<label class="gtc-c">Local de nascimento <small>(opcional)</small><input class="gtc-i" name="local" autocomplete="off" maxlength="120" placeholder="Ex.: Porto, Portugal"></label>' +
      '<div id="gtc-mz"></div><button class="gtc-ok" type="submit">Guardar</button><p class="gtc-er" role="alert"></p><button class="gtc-2" type="button">Agora não</button></form>');
    var f = d.querySelector("form"), er = d.querySelector(".gtc-er"), msg = d.querySelector(".gtc-msg"), versao = "";
    function acabar() { d.close(); preencher(); if (depois) depois(); }
    d.querySelector(".gtc-2").onclick = acabar;
    d.querySelector(".gtc-x").onclick = acabar;
    d.oncancel = function (e) { e.preventDefault(); acabar(); };
    comDataFacil();
    f.nasc.focus();
    pedirConfig().then(function (c) {
      if (!c || !c.consent || !d.querySelector("#gtc-mz")) return;
      versao = c.consent.versao;
      d.querySelector("#gtc-mz").innerHTML = '<label class="gtc-mkt"><input type="checkbox" name="mkt"><span></span></label>';
      d.querySelector("#gtc-mz span").textContent = c.consent.texto;
      // setinha a piscar até a pessoa marcar a caixa; a caixa nunca vem marcada
      var cx = d.querySelector('#gtc-mz input'), seta = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      seta.setAttribute("class", "gtc-seta"); seta.setAttribute("viewBox", "0 0 34 30"); seta.setAttribute("aria-hidden", "true");
      seta.innerHTML = '<path d="M1 10h17V1l15 14-15 14v-9H1z" fill="#ffd978" stroke="#7a4b00" stroke-width="1.5" stroke-linejoin="round"/>';
      cx.parentNode.insertBefore(seta, cx); cx.addEventListener("change", function () { seta.style.display = cx.checked ? "none" : ""; });
    });
    // 06/11/2026 (ele): a mesma regra dos formulários. O exemplo fica 30 segundos, depois o campo fica vazio, a pulsar, com o convite a escrever.
    var CONV = [[f.nasc, "Escreva aqui a sua data de nascimento"], [f.hora, "Escreva aqui a hora em que nasceu"], [f.local, "Escreva aqui a cidade onde nasceu"]].map(function (x) {
      var n = document.createElement("span"); n.className = "gtc-conv"; n.textContent = "✍️ " + x[1]; x[0].parentNode.insertBefore(n, x[0].nextSibling); return { el: x[0], n: n };
    }), acabou = false;
    function convites() { CONV.forEach(function (c) { var v = !c.el.value.trim(); c.n.style.display = v ? "" : "none"; c.el.classList.toggle("gtc-falta", v && acabou); }); }
    f.addEventListener("input", convites); convites();
    var fim = setTimeout(function () { if (!d.open) return; acabou = true; CONV.forEach(function (c) { c.el.placeholder = ""; }); convites(); }, 30000);
    d.addEventListener("close", function () { clearTimeout(fim); });
    f.nasc.onblur = function () {
      var r = window.dataFacil && window.dataFacil.ler(f.nasc.value);
      if (r) { f.nasc.value = ("0" + r.d).slice(-2) + "/" + ("0" + r.m).slice(-2) + "/" + r.a; msg.textContent = "✓ " + new Date(Date.UTC(r.a, r.m - 1, r.d)).toLocaleDateString("pt-PT", { timeZone: "UTC", day: "numeric", month: "long", year: "numeric" }); } else msg.textContent = "";
    };
    f.hora.onblur = function () { var h = lerHora(f.hora.value); if (h) f.hora.value = h; };
    f.onsubmit = function (e) {
      e.preventDefault(); er.textContent = "";
      comDataFacil().then(function () {
        var r = window.dataFacil && window.dataFacil.ler(f.nasc.value), h = lerHora(f.hora.value), b = f.querySelector(".gtc-ok");
        if (!r) { er.textContent = f.nasc.value.trim() ? ERROS.data : "Escreva a sua data de nascimento."; f.nasc.focus(); return; }
        if (h === null) { er.textContent = ERROS.hora; f.hora.focus(); return; }
        var quer = !!(f.mkt && f.mkt.checked), corpo = { nome: conta.nome, nasc: r.iso, hora: h, local: f.local.value.trim() };
        if (quer) { corpo.marketing = true; corpo.versao = versao; }
        b.disabled = true;
        api("perfil", corpo).then(function (x) {
          b.disabled = false;
          if (x && x.ok) { guardar(x.conta); acabar(); return; }
          if (x && x.erro === "sessao") { esquecer(); d.close(); return; }
          er.textContent = erroDe(x);
        }).catch(function () { b.disabled = false; er.textContent = erroDe(); });
      });
    };
  }

  // ---------- preencher os formulários ----------
  var CAMPOS = {
    nome: 'input#nome,input#f-name,input[name="nome"]',
    email: 'input#email,input#f-email,input[name="email"],input#email-pedido',
    nasc: 'input#data,input#f-dob,input#qs-data,input#asc-rapido-data,input#nasc,input#dn,input[name="nasc"],input[type="date"]#d,input[type="date"]#m-data',
    hora: "input#hora,input#qs-hora,input#hn",
  };
  function dobra(t) { return String(t || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim(); }
  function vazio(el) { return !el.disabled && !el.readOnly && !el.dataset.gtc && (!el.value || el.value === el.defaultValue); }
  function pôr(el, v) {
    el.dataset.gtc = "1"; el.value = v;
    el.dispatchEvent(new Event("input", { bubbles: true })); el.dispatchEvent(new Event("change", { bubbles: true }));
    if (el.type === "text") el.dispatchEvent(new Event("blur"));   // é no blur que estas páginas arrumam a data e a hora
  }
  function cidadeAuto(el, lista, cidade, pais) {
    // Nas calculadoras, a cidade tem de sair da lista: é ela que traz o fuso e as coordenadas. Só fica escolhida se houver um resultado certo.
    el.dataset.gtc = "1"; el.value = cidade;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    var n = 0, t = setInterval(function () {
      var bs = [].slice.call(lista.querySelectorAll("button[data-i]"));
      if (!bs.length && ++n < 40) return;
      clearInterval(t);
      if (document.activeElement === el) return;   // a pessoa já está a escrever
      var alvo = bs.filter(function (b) {
        var x = dobra(b.textContent); return x.indexOf(dobra(cidade)) === 0 && (!pais || x.indexOf(dobra(pais)) >= 0);
      })[0];
      if (alvo) alvo.click();
      else { el.value = ""; delete el.dataset.gtc; lista.classList.remove("aberta"); }
    }, 150);
  }
  function preencher() {
    if (!conta) return;
    var c = conta, nasc = c.nasc ? c.nasc.split("-") : null;
    function cada(sel, f) { [].forEach.call(document.querySelectorAll(sel), function (el) { if (vazio(el)) f(el); }); }
    if (c.nome) cada(CAMPOS.nome, function (el) { pôr(el, c.nome); });
    if (c.email) cada(CAMPOS.email, function (el) { pôr(el, c.email); });
    if (nasc) cada(CAMPOS.nasc, function (el) { pôr(el, el.type === "date" ? c.nasc : nasc[2] + "/" + nasc[1] + "/" + nasc[0]); });
    if (c.hora) cada(CAMPOS.hora, function (el) { pôr(el, c.hora); });
    if (c.local) {
      var p = c.local.split(","), cidade = p[0].trim(), pais = p.length > 1 ? p[p.length - 1].trim() : "";
      cada("input#f-city", function (el) { pôr(el, cidade); });
      if (pais) cada("input#f-country", function (el) { pôr(el, pais); });
      var el = document.querySelector("input#cidade"), lista = document.getElementById("lista-cid");
      if (el && vazio(el)) { if (lista) cidadeAuto(el, lista, cidade, pais); else pôr(el, cidade); }
    }
  }
  var vigiaFormularios = null;
  function vigiar() {   // formulários que nascem depois (só com sessão: quem não entrou não paga nada por isto)
    if (vigiaFormularios || !conta) return;
    var t = 0;
    vigiaFormularios = new MutationObserver(function () { clearTimeout(t); t = setTimeout(preencher, 200); });
    vigiaFormularios.observe(document.body, { childList: true, subtree: true });
  }

  // ---------- arranque ----------
  function arranca() {
    estilo();
    var som = document.querySelector(".som-fix,.btn-som");
    if (!som || getComputedStyle(som).display === "none") document.documentElement.classList.add("gtc-sem-som");
    btn = document.createElement("button"); btn.id = "gtc-btn"; btn.type = "button";
    document.body.appendChild(btn); desenhar();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(posicionar);
    var tp = 0; addEventListener("resize", function () { clearTimeout(tp); tp = setTimeout(posicionar, 200); });
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (!ls(MARCA)) return abrirEntrar();
      if (menu && !menu.hidden) fecharMenu(); else abrirMenu();
    });
    document.addEventListener("click", function (e) { if (menu && !menu.hidden && !menu.contains(e.target)) fecharMenu(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && menu && !menu.hidden) { fecharMenu(); btn.focus(); } });
    addEventListener("storage", function (e) {   // entrou ou saiu noutro separador
      if (e.key !== MARCA) return;
      if (e.newValue) fresco().then(function () { desenhar(); preencher(); vigiar(); }); else { esquecer(); }
    });
    ler().then(function () { desenhar(); if (conta) { preencher(); vigiar(); } });
  }
  window.gtConta = { api: api, ler: ler, fresco: fresco, guardar: guardar, esquecer: esquecer, entrou: entrou, abrirEntrar: abrirEntrar, primeiraVez: primeiraVez, sair: sair, config: pedirConfig, comDataFacil: comDataFacil, lerHora: lerHora, volta: function () { var v = ls(VOLTA); ls(VOLTA, null); return v; } };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arranca); else arranca();
})();
