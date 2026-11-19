/* duvidas-wa.js — 16/11/2026, pedido dele: a chamada «Tire as suas Dúvidas» (foto + balão, canto inferior direito, aos 5 s)
   em todas as páginas. Carregada pelo vivo.js, fora do consultório, da app e do pagamento.
   O balão some sozinho 10 s depois de aparecer (pedido dele, 16/11) ou quando a pessoa o fecha; a bolinha com a foto fica sempre. */
(function () {
  if (window.__dwa || document.getElementById("duvidas-wa")) return; window.__dwa = 1;
  var WA = "https://wa.me/351914920427?text=" + encodeURIComponent("Olá Mestre Alberto, tenho uma dúvida.");
  var fechado = false; try { fechado = sessionStorage.getItem("dwaFechado") === "1"; } catch (e) {}
  var css = document.createElement("style");
  css.textContent =
    "#duvidas-wa{position:fixed;right:16px;bottom:16px;z-index:9990;display:flex;align-items:center;gap:10px;opacity:0;transform:translateY(30px);pointer-events:none;transition:opacity .5s,transform .5s cubic-bezier(.2,1.6,.4,1);font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}" +
    "#duvidas-wa.dwa-on{opacity:1;transform:none;pointer-events:auto}" +
    "#duvidas-wa .dwa-balao{position:relative;background:#fff;color:#2b1d4a;border:2px solid #f3c64a;border-radius:14px;padding:8px 26px 8px 12px;font-size:.92rem;line-height:1.25;box-shadow:0 6px 20px rgba(0,0,0,.35);text-decoration:none;max-width:170px}" +
    "#duvidas-wa .dwa-balao.dwa-sai{opacity:0;transform:translateX(20px);transition:opacity .6s,transform .6s;pointer-events:none}" +
    "#duvidas-wa .dwa-balao b{display:block;color:#5b2c9e;font-size:1rem}" +
    "#duvidas-wa .dwa-balao:after{content:'';position:absolute;right:-9px;top:50%;margin-top:-7px;border:7px solid transparent;border-left-color:#f3c64a;border-right:0}" +
    "#duvidas-wa .dwa-x{position:absolute;top:2px;right:6px;background:none;border:0;color:#8a7fa6;font-size:17px;line-height:1;cursor:pointer;padding:2px}" +
    "#duvidas-wa .dwa-bola{position:relative;display:block;width:62px;height:62px;border-radius:50%;border:3px solid #25d366;box-shadow:0 6px 20px rgba(0,0,0,.4);animation:dwa-onda 2s infinite;flex:none}" +
    "#duvidas-wa .dwa-bola img{width:100%;height:100%;border-radius:50%;display:block}" +
    "#duvidas-wa .dwa-bola span{position:absolute;right:-4px;bottom:-4px;width:26px;height:26px;border-radius:50%;background:#25d366;color:#fff;font-size:15px;line-height:26px;text-align:center;border:2px solid #fff}" +
    "@keyframes dwa-onda{0%{box-shadow:0 6px 20px rgba(0,0,0,.4),0 0 0 0 rgba(37,211,102,.6)}70%{box-shadow:0 6px 20px rgba(0,0,0,.4),0 0 0 14px rgba(37,211,102,0)}100%{box-shadow:0 6px 20px rgba(0,0,0,.4),0 0 0 0 rgba(37,211,102,0)}}" +
    "@media (prefers-reduced-motion:reduce){#duvidas-wa .dwa-bola{animation:none}}" +
    "@media print{#duvidas-wa{display:none}}";
  document.head.appendChild(css);
  var d = document.createElement("div"); d.id = "duvidas-wa";
  d.innerHTML = (fechado ? "" :
    '<a class="dwa-balao" href="' + WA + '" target="_blank" rel="noopener"><b>Tire as suas Dúvidas</b>Fale comigo no WhatsApp' +
    '<button type="button" class="dwa-x" aria-label="Fechar">×</button></a>') +
    '<a class="dwa-bola" href="' + WA + '" target="_blank" rel="noopener" aria-label="Tire as suas Dúvidas pelo WhatsApp">' +
    '<img src="/mestre-wa-v2.jpg" alt="" width="62" height="62"><span>✆</span></a>';
  var x = d.querySelector(".dwa-x");
  if (x) x.onclick = function (e) { e.preventDefault(); e.stopPropagation(); x.parentNode.style.display = "none"; try { sessionStorage.setItem("dwaFechado", "1"); } catch (er) {} };
  function por() {
    document.body.appendChild(d);
    setTimeout(function () {
      d.classList.add("dwa-on");
      var b = d.querySelector(".dwa-balao");
      if (b) setTimeout(function () { b.classList.add("dwa-sai"); setTimeout(function () { b.style.display = "none"; }, 700); }, 10000);
    }, 5000);
  }
  if (document.body) por(); else document.addEventListener("DOMContentLoaded", por);
})();
