/* lista-signo.js — 01/11/2026, pedido dele (passo 2 do ecossistema: «ficar com o contacto de quem vem do canal»).
   A caixa «A previsão do seu signo no seu email» nas páginas /signo/<nome>. Entra na Lista VIP (o mesmo /notify do
   /vip.html, tipo «vip»), com a área «💌 Previsão semanal (<Signo>)» e a origem da visita (a ligação marcada do vídeo).
   O consentimento é o próprio pedido: a pessoa carrega em «Quero receber» depois de ler o que vai receber. */
(function () {
  var sec = document.getElementById("lista-signo");
  if (!sec) return;
  var signo = sec.getAttribute("data-signo") || "";
  var $ = function (s) { return sec.querySelector(s); };
  try { if (localStorage.getItem("vip-entrou")) { $(".ls-form").style.display = "none"; $(".ls-feito").style.display = "block"; return; } } catch (e) {}
  var erro = function (t) { var e = $(".ls-erro"); e.textContent = t; e.style.display = t ? "block" : "none"; };
  $(".ls-form").addEventListener("submit", function (ev) {
    ev.preventDefault(); erro("");
    var nome = $("[name=nome]").value.trim(), email = $("[name=email]").value.trim().toLowerCase(), nasc = $("[name=nasc]").value;
    if (nome.replace(/[^A-Za-zÀ-ÿ]/g, "").length < 2) return erro("Escreva o seu nome, por favor.");
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return erro("Escreva um email válido: é para lá que enviamos a previsão.");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(nasc)) return erro("Escolha a sua data de nascimento (é por ela que sabemos o seu signo).");
    var p = nasc.split("-"), origem = "";
    try { var g = JSON.parse(sessionStorage.getItem("gt_marca") || "null"); if (g) origem = String(g[0]).slice(0, 20) + (g[1] ? "/" + String(g[1]).slice(0, 40) : ""); } catch (e) {}
    var b = $("button"); b.disabled = true; b.textContent = "A registar…";
    fetch("/notify", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "vip", data: { name: nome, email: email, date_of_birth: p[2] + "/" + p[1] + "/" + p[0],
        area: "💌 Previsão semanal (" + signo + ")", novidades: true, origem: origem } }) })
      .then(function (r) { if (!r.ok) throw 0;
        try { localStorage.setItem("vip-entrou", "1"); } catch (e) {}
        $(".ls-feito b").textContent = nome.split(/\s+/)[0];
        $(".ls-form").style.display = "none"; $(".ls-feito").style.display = "block"; })
      .catch(function () { b.disabled = false; b.textContent = "💌 Quero receber"; erro("Não consegui registar agora. Tente outra vez daqui a um minuto."); });
  });
})();
