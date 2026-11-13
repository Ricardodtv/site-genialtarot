/* sexta13.js — 13/11/2026, pedido dele: «sempre que a sexta-feira 13 aparecer, no dia anterior um destaque no site».
   Carregado pelo vivo.js em todas as páginas. Mostra-se SÓ na véspera (quinta 12) e no próprio dia (sexta 13), hora de Lisboa.
   · página inicial: cartão grande logo a seguir ao topo
   · outras páginas: cartão flutuante no canto (o × esconde-o até fechar o separador)
   Para ver fora do dia: ?sexta13=hoje ou ?sexta13=amanha */
(function () {
  if (window.__sexta13) return; window.__sexta13 = 1;
  if (/^\/(sexta-feira-13|consultorio|o-teu-ceu|pagar)(\/|\.html|-sala|$)/.test(location.pathname)) return;
  var t = new Date(new Date().toLocaleString("en-US", { timeZone: "Europe/Lisbon" }));
  var amanha = new Date(t); amanha.setDate(t.getDate() + 1);
  var modo = t.getDate() === 13 && t.getDay() === 5 ? "hoje" : (amanha.getDate() === 13 && amanha.getDay() === 5 ? "amanha" : "");
  try { var f = new URLSearchParams(location.search).get("sexta13"); if (f === "hoje" || f === "amanha") modo = f; } catch (e) {}
  if (!modo) return;
  var inicio = location.pathname === "/" || /^\/index(\.html)?$/.test(location.pathname);
  if (!inicio) { try { if (sessionStorage.getItem("s13-fechado")) return; } catch (e) {} }

  var tit = modo === "hoje" ? "Hoje é Sexta-feira 13" : "Amanhã é Sexta-feira 13";
  var txt = modo === "hoje" ? "O dia mais misterioso do calendário chegou. Descubra a origem do medo e como virar a sorte a seu favor."
                            : "Prepare-se para o dia mais misterioso do calendário: a origem, as lendas e como virar a sorte.";
  var gato = '<svg viewBox="0 0 120 120" aria-hidden="true"><defs><radialGradient id="s13l" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#fff6dc"/><stop offset=".7" stop-color="#f3d58e"/><stop offset="1" stop-color="#c99a3f"/></radialGradient></defs>'
    + '<circle cx="60" cy="52" r="42" fill="url(#s13l)"/><path d="M38 116c-3-22 2-40 16-50l-4-20 13 11c4-1 8-1 12 0l13-11-4 20c14 10 19 28 16 50z" fill="#0b0408"/>'
    + '<ellipse class="s13o" cx="57" cy="86" rx="3.5" ry="4.5" fill="#ffd34d"/><ellipse class="s13o" cx="73" cy="86" rx="3.5" ry="4.5" fill="#ffd34d"/></svg>';
  var css = ''
    + '.s13{font-family:Inter,system-ui,sans-serif;color:#f6eef4;text-decoration:none;display:flex;align-items:center;gap:1rem;box-sizing:border-box;'
    + 'background:radial-gradient(ellipse at 15% 0%,#5c1748 0%,#2a0a24 45%,#12050f 100%);border:1px solid rgba(255,217,120,.45);box-shadow:0 0 0 1px rgba(255,217,120,.15),0 18px 50px -10px rgba(160,40,110,.7)}'
    + '.s13 svg{flex:none;filter:drop-shadow(0 0 14px rgba(255,215,120,.55))}'
    + '.s13 .s13t{font-family:Cinzel,"Cormorant Garamond",Georgia,serif;font-weight:900;color:#ffd978;letter-spacing:.02em;line-height:1.1;display:block}'
    + '.s13 .s13p{display:block;color:#e6d3e0;line-height:1.4}'
    + '.s13 .s13b{display:inline-block;margin-top:.55rem;padding:.5rem 1.1rem;border-radius:999px;font-weight:800;color:#2a0c18;background:linear-gradient(135deg,#ffe9a6,#e2a93a);animation:s13p 1.8s ease-out infinite}'
    + '.s13o{animation:s13pi 4.5s infinite;transform-box:fill-box;transform-origin:center}'
    + '@keyframes s13pi{0%,46%,50%,100%{transform:scaleY(1)}48%{transform:scaleY(.1)}}'
    + '@keyframes s13p{0%{box-shadow:0 0 0 0 rgba(255,215,120,.7)}80%,100%{box-shadow:0 0 0 12px rgba(255,215,120,0)}}'
    + '.s13-grande{position:relative;width:min(60rem,calc(100% - 2rem));margin:1.2rem auto 1.6rem;border-radius:1.5rem;padding:1.2rem 1.6rem;overflow:hidden}'
    + '.s13-grande svg{width:8.5rem;height:8.5rem}.s13-grande .s13t{font-size:clamp(1.5rem,4.4vw,2.4rem)}.s13-grande .s13p{font-size:1.02rem;margin-top:.35rem}'
    + '.s13-grande .s13n{position:absolute;right:-.5rem;bottom:-2.6rem;font:900 9rem/1 Cinzel,serif;color:rgba(255,217,120,.09);pointer-events:none}'
    + '.s13-flut{position:fixed;left:1rem;bottom:1rem;z-index:9998;width:min(23rem,calc(100% - 2rem));border-radius:1.2rem;padding:.8rem 2.2rem .8rem .8rem;animation:s13e .6s ease-out}'
    + '.s13-flut svg{width:4.4rem;height:4.4rem}.s13-flut .s13t{font-size:1.12rem}.s13-flut .s13p{font-size:.84rem;margin-top:.2rem}.s13-flut .s13b{font-size:.85rem;padding:.4rem .9rem;margin-top:.4rem}'
    + '.s13x{position:absolute;right:.3rem;top:.3rem;width:28px;height:28px;border:0;border-radius:50%;background:transparent;color:#fff;opacity:.65;font-size:17px;cursor:pointer}'
    + '@keyframes s13e{from{transform:translateY(120%);opacity:0}to{transform:none;opacity:1}}'
    + '@media (max-width:560px){.s13-grande{flex-direction:column;text-align:center}.s13-grande svg{width:6.5rem;height:6.5rem}}'
    + '@media (prefers-reduced-motion:reduce){.s13 *,.s13{animation:none!important}}';
  function montar() {
    if (document.querySelector(".s13")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var a = document.createElement("a"); a.href = "/sexta-feira-13?de=site&c=destaque-" + modo;
    a.className = "s13 " + (inicio ? "s13-grande" : "s13-flut");
    a.innerHTML = gato + '<span><span class="s13t">🐈‍⬛ ' + tit + '</span><span class="s13p">' + txt + '</span><span class="s13b">Descobrir o mistério →</span></span>'
      + (inicio ? '<span class="s13n" aria-hidden="true">13</span>' : '<button class="s13x" aria-label="Fechar">×</button>');
    if (inicio) {
      var heroi = document.querySelector("section.hero");
      if (heroi && heroi.parentNode) heroi.parentNode.insertBefore(a, heroi.nextSibling);
      else document.body.insertBefore(a, document.body.firstChild);
    } else {
      document.body.appendChild(a);
      a.querySelector(".s13x").addEventListener("click", function (e) {
        e.preventDefault(); e.stopPropagation(); a.remove(); try { sessionStorage.setItem("s13-fechado", "1"); } catch (er) {}
      });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();
