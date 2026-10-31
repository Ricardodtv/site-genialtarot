/* vivo.js — 31/10/2026, pedido dele: saber quem está no site agora e poder falar com essa pessoa.
   Diz «estou aqui» ao worker de 10 em 10 s (só com a página à vista). Não mostra nada até o Mestre Alberto
   abrir uma conversa no painel dele; aí aparece o chat, com a foto dele, como na aplicação. */
(function () {
  if (window.__vivo) return; window.__vivo = 1;
  var A = "/api/vivo", sid;
  try { sid = localStorage.getItem("gt_vivo"); } catch (e) {}
  if (!sid || !/^[a-z0-9]{12,40}$/.test(sid)) {
    sid = (Date.now().toString(36) + Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2)).replace(/[^a-z0-9]/g, "").slice(0, 32);
    try { localStorage.setItem("gt_vivo", sid); } catch (e) {}
  }
  var aberto = false, desde = 0, el = null, ctx = null, tEsc = 0;
  function post(u, d) { return fetch(A + u, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(d), keepalive: true }); }
  function ola() {
    if (document.visibilityState !== "visible") return;
    var o = ""; try { o = document.referrer ? new URL(document.referrer).hostname : ""; } catch (e) {}
    post("", { sid: sid, pagina: location.pathname, titulo: document.title, origem: o }).then(function (r) { return r.json(); })
      .then(function (r) { if (r && r.aberto && !aberto) verChat(); }).catch(function () {});
  }
  // os sons (baixinhos, nunca alto): abrir = sino a subir; fechar = duas notas a descer; mensagem = «plim» curto
  function som(q) {
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === "suspended") ctx.resume();
      var t = ctx.currentTime, n = { abre: [[523.3, 0], [659.3, .12], [784, .24], [1046.5, .38]], fecha: [[784, 0], [523.3, .22]], msg: [[880, 0]] }[q];
      n.forEach(function (x) { var o = ctx.createOscillator(), g = ctx.createGain(), t0 = t + x[1]; o.type = "sine"; o.frequency.value = x[0];
        g.gain.setValueAtTime(.0001, t0); g.gain.exponentialRampToValueAtTime(q === "msg" ? .015 : .06, t0 + .02);
        g.gain.exponentialRampToValueAtTime(.0001, t0 + (q === "abre" ? 1.6 : q === "msg" ? .25 : 1.1)); o.connect(g).connect(ctx.destination); o.start(t0); o.stop(t0 + 1.7); });
    } catch (e) {}
  }
  ["pointerup", "touchend", "keydown"].forEach(function (x) { addEventListener(x, function () { try { ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === "suspended") ctx.resume(); } catch (e) {} }, { passive: true }); });
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function montar() {
    if (el) return;
    var css = document.createElement("style");
    css.textContent = "#gt-chat{position:fixed;right:14px;bottom:14px;z-index:2147483000;width:min(360px,calc(100vw - 28px));max-height:min(520px,calc(100vh - 28px));display:none;flex-direction:column;" +
      "background:#1d0d36;color:#f7f0fb;border:1px solid rgba(242,201,107,.45);border-radius:18px;box-shadow:0 12px 40px rgba(0,0,0,.55);font:15px/1.45 system-ui,sans-serif;overflow:hidden}" +
      "#gt-chat.on{display:flex;animation:gtEntra .35s ease}@keyframes gtEntra{from{transform:translateY(20px);opacity:0}to{transform:none;opacity:1}}" +
      "#gt-chat .cab{display:flex;gap:10px;align-items:center;padding:10px 12px;background:linear-gradient(135deg,#3b1a63,#25104a);border-bottom:1px solid rgba(242,201,107,.25)}" +
      "#gt-chat .cab img{width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid #25d366}" +
      "#gt-chat .cab b{color:#f2c96b;display:block;font-size:16px}#gt-chat .cab small{color:#25d366;font-size:12px}" +
      "#gt-chat .x{margin-left:auto;background:none;border:0;color:#a893bd;font-size:22px;cursor:pointer;padding:2px 6px}" +
      "#gt-chat .msgs{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:6px;min-height:160px}" +
      "#gt-chat .m{max-width:82%;padding:7px 11px;border-radius:14px;white-space:pre-wrap;word-wrap:break-word}" +
      "#gt-chat .m.mestre{align-self:flex-start;background:rgba(242,201,107,.18)}#gt-chat .m.pessoa{align-self:flex-end;background:rgba(37,211,102,.2)}" +
      "#gt-chat .m.sistema{align-self:center;background:none;color:#a893bd;font-size:12px}" +
      "#gt-chat .m time{display:block;font-size:11px;color:#a893bd;text-align:right}" +
      "#gt-chat .esc{display:none;align-self:flex-start;background:rgba(242,201,107,.18);border-radius:14px;padding:9px 12px}#gt-chat .esc.on{display:block}" +
      "#gt-chat .esc i{display:inline-block;width:7px;height:7px;margin:0 2px;border-radius:50%;background:#f2c96b;animation:gtPt 1.2s infinite}" +
      "#gt-chat .esc i:nth-child(2){animation-delay:.2s}#gt-chat .esc i:nth-child(3){animation-delay:.4s}@keyframes gtPt{0%,60%,100%{opacity:.3;transform:none}30%{opacity:1;transform:translateY(-3px)}}" +
      "#gt-chat .emo{display:flex;flex-wrap:wrap;gap:0;padding:2px 8px}#gt-chat .emo button{background:none;border:0;font-size:20px;padding:2px 4px;cursor:pointer}" +
      "#gt-chat form{display:flex;gap:6px;padding:8px;border-top:1px solid rgba(255,255,255,.08)}" +
      "#gt-chat input{flex:1;min-width:0;padding:10px;border-radius:12px;border:1px solid rgba(242,201,107,.3);background:#140826;color:#f7f0fb;font:inherit}" +
      "#gt-chat form button{border:0;border-radius:12px;padding:0 14px;background:#25d366;color:#08331a;font-weight:700;cursor:pointer}";
    document.head.appendChild(css);
    el = document.createElement("div"); el.id = "gt-chat";
    el.innerHTML = '<div class="cab"><img src="/mestre-avatar@2x.jpg" alt="Mestre Alberto"><div><b>Mestre Alberto</b><small>● online — a falar consigo</small></div>' +
      '<button class="x" type="button" aria-label="Fechar">✕</button></div><div class="msgs"></div>' +
      '<div class="emo">' + ["😊", "🙏", "❤️", "✨", "🌙", "🥰", "😂", "🤗", "👍", "🔮", "⭐", "🍀"].map(function (x) { return "<button type=button>" + x + "</button>"; }).join("") + "</div>" +
      '<form><input placeholder="Escreva aqui…" autocomplete="off" maxlength="1000"><button>Enviar</button></form>';
    document.body.appendChild(el);
    var msgs = el.querySelector(".msgs"), inp = el.querySelector("input");
    var pts = document.createElement("div"); pts.className = "esc"; pts.innerHTML = "<i></i><i></i><i></i>"; msgs.appendChild(pts);
    el.querySelector(".x").onclick = function () { el.classList.remove("on"); aberto = false; som("fecha"); post("/fechar", { sid: sid }).catch(function () {}); };
    el.querySelector(".emo").onclick = function (e) { var b = e.target.closest("button"); if (b) { inp.value += b.textContent; inp.focus(); } };
    inp.addEventListener("input", function () { if (Date.now() - tEsc < 2000) return; tEsc = Date.now(); post("/escreve", { sid: sid }).catch(function () {}); });
    el.querySelector("form").onsubmit = function (e) { e.preventDefault(); var t = inp.value.trim(); if (!t) return; inp.value = "";
      post("/chat", { sid: sid, texto: t }).then(verChat).catch(function () {}); };
  }
  function verChat() {
    if (document.visibilityState !== "visible") return Promise.resolve();
    return fetch(A + "/chat?sid=" + sid + "&desde=" + (aberto ? desde : 0), { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (r) {
      if (r.aberto) {
        montar(); var msgs = el.querySelector(".msgs"), pts = el.querySelector(".esc");
        if (!aberto) { [].slice.call(msgs.querySelectorAll(".m")).forEach(function (x) { x.remove(); }); desde = 0; }
        var novaDele = false;
        (r.msgs || []).forEach(function (m) { if (m.id <= desde) return; desde = m.id; if (m.de === "mestre") novaDele = true;
          var d = document.createElement("div"); d.className = "m " + m.de; d.innerHTML = esc(m.texto) +
            (m.de === "sistema" ? "" : "<time>" + new Date(m.quando).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) + "</time>");
          msgs.insertBefore(d, pts); });
        pts.classList.toggle("on", !!r.escreve);
        if (!aberto) { el.classList.add("on"); som("abre"); } else if (novaDele) som("msg");
        msgs.scrollTop = 1e6;
      } else if (aberto && el) { el.classList.remove("on"); som("fecha"); }
      aberto = !!r.aberto;
    }).catch(function () {});
  }
  (function roda() { (aberto ? verChat() : Promise.resolve()).then(function () { setTimeout(roda, 2000); }); })();
  ola(); setInterval(ola, 10000);   // de 10 em 10 s: é também o que faz o chat aparecer quando ele o abre
  document.addEventListener("visibilitychange", function () { if (document.visibilityState === "visible") ola(); });
})();
