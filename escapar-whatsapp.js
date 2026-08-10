/* =========================================================================
   ESCAPAR AO NAVEGADOR DO WHATSAPP  —  genialtarot.com
   Escrito a 10/08/2026.

   O PROBLEMA
   O checkout do myPOS nao abre dentro do WhatsApp (nem no Android nem no
   iPhone): mostra "O link de pagamento expirou ou foi desativado pelo
   comerciante". Nao e o link que esta mau -- e o navegador embutido da
   aplicacao, que o myPOS recusa por nao parecer um navegador a serio.

   Como o genialtarot.com so tem o WhatsApp como forma de contacto, este era
   o caminho natural de toda a gente que quer comprar. O cliente carregava,
   via "expirou", e ia-se embora SEM AVISAR.

   O QUE ESTE CODIGO FAZ
   Intercepta os cliques nos botoes de compra. Se estivermos num navegador
   normal, nao faz nada -- segue como sempre. Se estivermos dentro do
   WhatsApp (ou Instagram, ou Facebook), tenta abrir no navegador verdadeiro:
     · Android -> intent://  obriga a abrir no Chrome
     · iPhone  -> x-safari-https://  obriga a abrir no Safari
   E se nada disso resultar, mostra um aviso com o link para copiar, em vez
   de deixar o cliente bater numa parede.

   COMO INSTALAR
   Juntar esta linha ao fim da pagina da loja, antes de </body>:
       <script src="/escapar-whatsapp.js"></script>
   ========================================================================= */
(function () {
  "use strict";

  // --- estamos dentro de uma aplicacao? --------------------------------
  var ua = navigator.userAgent || "";
  var dentroDeApp = /WhatsApp|FBAN|FBAV|FB_IAB|Instagram|Line\/|MicroMessenger|Snapchat/i.test(ua);
  if (!dentroDeApp) return;          // navegador normal: nao mexe em nada

  var android = /Android/i.test(ua);
  var ios = /iPhone|iPad|iPod/i.test(ua);

  function abrirLaFora(url) {
    if (android) {
      // intent:// entrega o endereco ao Chrome, saindo da aplicacao
      var semEsquema = url.replace(/^https?:\/\//, "");
      window.location.href =
        "intent://" + semEsquema +
        "#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url=" +
        encodeURIComponent(url) + ";end";
      return true;
    }
    if (ios) {
      // x-safari-https:// e o esquema que o Safari reconhece; funciona na
      // maioria dos navegadores embutidos do iPhone
      window.location.href = url.replace(/^https:/, "x-safari-https:");
      return true;
    }
    return false;
  }

  function avisar(url) {
    var fundo = document.createElement("div");
    fundo.setAttribute("style",
      "position:fixed;inset:0;background:rgba(20,10,35,.92);z-index:99999;" +
      "display:flex;align-items:center;justify-content:center;padding:24px;" +
      "font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;");
    fundo.innerHTML =
      '<div style="background:#fff;border-radius:16px;padding:26px 22px;max-width:340px;text-align:center;">' +
        '<div style="font-size:34px;">🔒</div>' +
        '<h3 style="margin:12px 0 8px;font-size:18px;color:#2e2a3d;">Falta só um passo</h3>' +
        '<p style="margin:0 0 16px;font-size:15px;line-height:1.55;color:#5a5470;">' +
          'A página de pagamento não abre aqui dentro do WhatsApp, por segurança.<br><br>' +
          'Toque no menu <b>⋮</b> (ou <b>···</b>) no canto e escolha <b>“Abrir no browser”</b>.' +
        '</p>' +
        '<button id="gt-copiar" style="width:100%;background:#5b2c9e;color:#fff;border:0;' +
          'border-radius:10px;padding:14px;font-size:15px;font-weight:bold;">Copiar o link</button>' +
        '<button id="gt-fechar" style="width:100%;background:none;border:0;color:#8a849c;' +
          'padding:12px;font-size:14px;margin-top:4px;">Voltar</button>' +
      '</div>';
    document.body.appendChild(fundo);
    fundo.querySelector("#gt-copiar").onclick = function () {
      var t = this;
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject())
        .then(function () { t.textContent = "Link copiado ✓"; })
        .catch(function () { window.prompt("Copie o link:", url); });
    };
    fundo.querySelector("#gt-fechar").onclick = function () { fundo.remove(); };
  }

  // --- apanhar os cliques nos botoes de compra --------------------------
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a") : null;
    if (!a || !a.href) return;
    if (a.href.indexOf("mypos.com") === -1) return;   // so os de pagamento

    e.preventDefault();
    var url = a.href;
    if (!abrirLaFora(url)) { avisar(url); return; }

    // Se ao fim de 1,2 segundos ainda ca estamos, o salto falhou --
    // mostra-se o aviso em vez de deixar o cliente sem nada.
    setTimeout(function () {
      if (!document.hidden) avisar(url);
    }, 1200);
  }, true);
})();
