/* 26/11/2026 (sim dele: «sim ao formulário e ao botão ligar»): nas páginas dos anúncios, 15 pessoas tocaram no WhatsApp
   e nenhuma enviou a mensagem. Aqui juntam-se duas portas novas, para quem não quer escrever no WhatsApp:
   1) «📞 Ligar agora» (tel:) logo a seguir ao primeiro botão do WhatsApp;
   2) um formulário curto «Prefere que eu lhe ligue?» antes do rodapé → /notify (type «contacto») → aviso no Telegram
      + ficha (fila-capturas). Se a pessoa veio de um anúncio, o worker põe também a conversão na fila «gads-…».
   Relatório: Central Claude/Anúncios Genial Tarot/Relatório — 1023 cliques e 0 contactos (26-11-2026). */
(function () {
  if (document.getElementById("ca-form")) return;
  var TEL = "+351914920427";
  var p = location.pathname.replace(/\.html$/, "").replace(/\/$/, "");
  var MESA = p === "/tarot-a-mesa";
  var NOME = { "/tarot-a-mesa": "Tarot à Mesa", "/consulta-de-tarot-online": "Consulta de Tarot Online",
    "/consulta-tarot-casal": "Consulta de Tarot para Casais", "/consulta-de-pendulo": "Consulta de Pêndulo",
    "/consultas-a-distancia": "Consulta à Distância" }[p] || "Consulta";
  var css = "" +
    ".ca-lig{display:flex;gap:.6rem;flex-wrap:wrap;justify-content:center;margin:.8rem 0 0}" +
    ".ca-lig a{flex:1 1 13rem;text-align:center;text-decoration:none;font:800 1.02rem/1.2 Inter,system-ui,sans-serif;padding:.85rem 1rem;border-radius:999px;border:2px solid #E8C15A;color:#E8C15A;background:#160F04cc}" +
    ".ca-lig a:hover{filter:brightness(1.12)}" +
    "#ca-form{max-width:34rem;margin:2.2rem auto;padding:1.4rem 1.2rem;border:2px solid #E8C15A;border-radius:1.2rem;background:#160F04e6;color:#f4ead2;font:400 1rem/1.45 Inter,system-ui,sans-serif;box-sizing:border-box}" +
    "#ca-form h2{margin:0 0 .3rem;text-align:center;color:#E8C15A;font-size:1.35rem}" +
    "#ca-form p.ca-sub{margin:0 0 1rem;text-align:center;opacity:.9}" +
    "#ca-form label{display:block;margin:.7rem 0 .25rem;font-weight:700}" +
    "#ca-form input,#ca-form textarea{width:100%;box-sizing:border-box;padding:.75rem .8rem;border-radius:.7rem;border:1px solid #E8C15A88;background:#0d0903;color:#fff;font:400 1rem Inter,system-ui,sans-serif}" +
    "#ca-form textarea{min-height:4.2rem;resize:vertical}" +
    "#ca-form button{display:block;width:100%;margin-top:1.1rem;padding:1rem;border:0;border-radius:999px;background:#E8C15A;color:#160F04;font:800 1.08rem Inter,system-ui,sans-serif;cursor:pointer}" +
    "#ca-form button:disabled{opacity:.6}" +
    "#ca-form .ca-priv{font-size:.82rem;opacity:.75;margin:.8rem 0 0;text-align:center}" +
    "#ca-form .ca-erro{color:#ff9d8a;font-weight:700;margin:.6rem 0 0;text-align:center}" +
    "#ca-form .ca-ok{text-align:center;font-size:1.1rem}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  // 1) «Ligar agora» a seguir ao primeiro botão do WhatsApp
  var wa = document.querySelector("a.wa[href*='wa.me'], a[href*='wa.me/']");
  if (wa && !document.querySelector(".ca-lig")) {
    var d = document.createElement("div"); d.className = "ca-lig";
    d.innerHTML = '<a href="tel:' + TEL + '" class="ca-tel">📞 Ligar agora</a><a href="#ca-form" class="ca-ir">✍️ Prefiro que me liguem</a>';
    wa.insertAdjacentElement("afterend", d);
  }

  // 2) o formulário, antes do rodapé
  var f = document.createElement("form"); f.id = "ca-form"; f.noValidate = true;
  f.innerHTML =
    '<h2>Prefere que o Mestre Alberto lhe ligue?</h2>' +
    '<p class="ca-sub">Deixe o nome e o telemóvel. Ele liga-lhe assim que possível.</p>' +
    '<label for="ca-nome">Nome</label><input id="ca-nome" autocomplete="name" maxlength="80" required>' +
    '<label for="ca-tel">Telemóvel</label><input id="ca-tel" type="tel" inputmode="tel" autocomplete="tel" maxlength="25" placeholder="9xx xxx xxx" required>' +
    (MESA ? '<label for="ca-quando">Para quando é o jantar ou a festa? <small>(opcional)</small></label><input id="ca-quando" maxlength="80" placeholder="ex.: 12 de dezembro, 10 pessoas">'
          : '') +
    '<label for="ca-msg">' + (MESA ? "Alguma nota?" : "O que gostava de perguntar às cartas?") + ' <small>(opcional)</small></label><textarea id="ca-msg" maxlength="500"></textarea>' +
    '<button type="submit">📞 Quero que me liguem</button>' +
    '<p class="ca-erro" hidden></p>' +
    '<p class="ca-priv">O seu número serve só para responder a este pedido.</p>';
  var foot = document.querySelector("footer");
  if (foot) foot.parentNode.insertBefore(f, foot); else document.body.appendChild(f);

  var $ = function (id) { return document.getElementById(id); };
  var erro = function (t) { var e = f.querySelector(".ca-erro"); e.textContent = t; e.hidden = false; };
  f.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var nome = $("ca-nome").value.trim(), tel = $("ca-tel").value.trim();
    var quando = $("ca-quando") ? $("ca-quando").value.trim() : "", msg = $("ca-msg").value.trim();
    if (nome.replace(/[^A-Za-zÀ-ÿ]/g, "").length < 2) return erro("Escreva o seu nome, por favor.");
    if (tel.replace(/\D/g, "").length < 9) return erro("Confirme o número de telemóvel (pelo menos 9 algarismos).");
    var b = f.querySelector("button"); b.disabled = true; b.textContent = "A enviar…";
    fetch("/notify", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "contacto", data: { name: nome, phone: tel, area: "📞 Pedido de contacto — " + NOME,
        quando: quando, mensagem: msg, pagina: p,
        verdict: "📞 Pediu que lhe liguem (" + NOME + ")" + (quando ? "\n📅 Quando: " + quando : "") + (msg ? "\n💬 " + msg : "") } }) })
      .then(function (r) { if (!r.ok) throw new Error(r.status);
        f.innerHTML = '<p class="ca-ok">✅ Recebido, ' + nome.split(/\s+/)[0].replace(/[<>&"]/g, "") + '!<br>O Mestre Alberto vai ligar-lhe para o número que deixou.</p>'; })
      .catch(function () { b.disabled = false; b.textContent = "📞 Quero que me liguem";
        erro("Não consegui enviar agora. Tente outra vez, ou carregue em «Ligar agora»."); });
  });
})();
