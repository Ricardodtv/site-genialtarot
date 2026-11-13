/* destaque.js — 13/11/2026, pedido dele (com captura): «gosto do destaque a aparecer assim … deveria aparecer em todo o site e estar visível
   quando a pessoa abre a página por 8 segundos, e este estilo de destaque pode ser usado no futuro para outras coisas».
   Um só componente para TODOS os destaques do site. Carregado pelo vivo.js em todas as páginas.
   · ao abrir a página: o cartão entra, fica 8 s (barrinha dourada a contar) e sai; fica um botão redondo no canto para o reabrir
   · o × fecha-o até fechar o separador (fica só o botão redondo)
   · na página inicial há também a versão grande, logo a seguir ao topo
   Para acrescentar um destaque novo: uma entrada em DESTAQUES (o 1.º que estiver activo é o que aparece).
   Para ver um destaque fora do dia: ?destaque=<id>  (a sexta-feira 13 aceita também ?sexta13=hoje|amanha) */
(function () {
  if (window.__destaque) return; window.__destaque = 1;
  if (/^\/(consultorio|o-teu-ceu|pagar)(\/|\.html|-sala|$)/.test(location.pathname)) return;
  var SEGUNDOS = 8;
  var agora = new Date(new Date().toLocaleString("en-US", { timeZone: "Europe/Lisbon" }));
  var dia = function (d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); };
  var hoje = dia(agora), amanhaD = new Date(agora); amanhaD.setDate(agora.getDate() + 1);
  var q = new URLSearchParams(location.search);

  var GATO = '<svg viewBox="0 0 120 120" aria-hidden="true"><defs><radialGradient id="dsl" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#fff6dc"/><stop offset=".7" stop-color="#f3d58e"/><stop offset="1" stop-color="#c99a3f"/></radialGradient></defs>'
    + '<circle cx="60" cy="52" r="42" fill="url(#dsl)"/><path d="M38 116c-3-22 2-40 16-50l-4-20 13 11c4-1 8-1 12 0l13-11-4 20c14 10 19 28 16 50z" fill="#0b0408"/>'
    + '<ellipse class="dso" cx="57" cy="86" rx="3.5" ry="4.5" fill="#ffd34d"/><ellipse class="dso" cx="73" cy="86" rx="3.5" ry="4.5" fill="#ffd34d"/></svg>';

  /* ── a lista dos destaques ── cada um: id, activo() → true/false, titulo, texto, botao, link, arte (svg), e opcional pagina (onde NÃO aparece) */
  var DESTAQUES = [
    { id: "sexta13", pagina: /^\/sexta-feira-13(\.html)?$/,
      activo: function () {
        var f = q.get("sexta13"); if (f === "hoje" || f === "amanha") { this.modo = f; return true; }
        if (agora.getDate() === 13 && agora.getDay() === 5) { this.modo = "hoje"; return true; }
        if (amanhaD.getDate() === 13 && amanhaD.getDay() === 5) { this.modo = "amanha"; return true; }
        return false;
      },
      titulo: function () { return this.modo === "hoje" ? "Hoje é Sexta-feira 13" : "Amanhã é Sexta-feira 13"; },
      texto: function () { return this.modo === "hoje" ? "O dia mais misterioso do calendário chegou. Descubra a origem do medo e como virar a sorte a seu favor."
                                                      : "Prepare-se para o dia mais misterioso do calendário: a origem, as lendas e como virar a sorte."; },
      botao: "Descobrir o mistério →",
      link: function () { return "/sexta-feira-13?de=site&c=destaque-" + this.modo; },
      arte: GATO, marca: "13" }
    /* exemplo para o futuro:
    ,{ id: "natal", activo: function () { return hoje >= "2026-12-20" && hoje <= "2026-12-25"; }, titulo: "…", texto: "…", botao: "Ver →", link: "/…", arte: "<svg…>" } */
  ];
  var val = function (x, d) { return typeof x === "function" ? x.call(d) : x; };
  var D = null;
  for (var i = 0; i < DESTAQUES.length; i++) {
    var d = DESTAQUES[i];
    if (d.pagina && d.pagina.test(location.pathname)) continue;
    if (q.get("destaque") === d.id || d.activo()) { if (q.get("destaque") === d.id && !d.modo) d.modo = "hoje"; D = d; break; }
  }
  if (!D) return;
  var inicio = location.pathname === "/" || /^\/index(\.html)?$/.test(location.pathname);
  var fechado = false; try { fechado = !!sessionStorage.getItem("dst-fechado-" + D.id); } catch (e) {}

  var css = ''
    + '.dst{font-family:Inter,system-ui,sans-serif;color:#f6eef4;text-decoration:none;display:flex;align-items:center;gap:1rem;box-sizing:border-box;'
    + 'background:radial-gradient(ellipse at 15% 0%,#5c1748 0%,#2a0a24 45%,#12050f 100%);border:1px solid rgba(255,217,120,.45);box-shadow:0 0 0 1px rgba(255,217,120,.15),0 18px 50px -10px rgba(160,40,110,.7)}'
    + '.dst svg{flex:none;filter:drop-shadow(0 0 14px rgba(255,215,120,.55))}'
    + '.dst .dt{font-family:Cinzel,"Cormorant Garamond",Georgia,serif;font-weight:900;color:#ffd978;letter-spacing:.02em;line-height:1.1;display:block}'
    + '.dst .dp{display:block;color:#e6d3e0;line-height:1.4}'
    + '.dst .db{display:inline-block;margin-top:.55rem;padding:.5rem 1.1rem;border-radius:999px;font-weight:800;color:#2a0c18;background:linear-gradient(135deg,#ffe9a6,#e2a93a);animation:dstp 1.8s ease-out infinite}'
    + '.dso{animation:dstpi 4.5s infinite;transform-box:fill-box;transform-origin:center}'
    + '@keyframes dstpi{0%,46%,50%,100%{transform:scaleY(1)}48%{transform:scaleY(.1)}}'
    + '@keyframes dstp{0%{box-shadow:0 0 0 0 rgba(255,215,120,.7)}80%,100%{box-shadow:0 0 0 12px rgba(255,215,120,0)}}'
    + '.dst-grande{position:relative;width:min(60rem,calc(100% - 2rem));margin:1.2rem auto 1.6rem;border-radius:1.5rem;padding:1.2rem 1.6rem;overflow:hidden}'
    + '.dst-grande svg{width:8.5rem;height:8.5rem}.dst-grande .dt{font-size:clamp(1.5rem,4.4vw,2.4rem)}.dst-grande .dp{font-size:1.02rem;margin-top:.35rem}'
    + '.dst-grande .dn{position:absolute;right:-.5rem;bottom:-2.6rem;font:900 9rem/1 Cinzel,serif;color:rgba(255,217,120,.09);pointer-events:none}'
    + '.dst-flut{position:fixed;left:1rem;bottom:1rem;z-index:9998;width:min(23rem,calc(100% - 2rem));border-radius:1.2rem;padding:.8rem 2.2rem 1rem .8rem;overflow:hidden;'
    + 'transition:transform .55s cubic-bezier(.5,0,.75,0),opacity .55s;animation:dste .6s ease-out}'
    + '.dst-flut.sai{transform:translateY(130%);opacity:0;pointer-events:none}'
    + '.dst-flut svg{width:4.4rem;height:4.4rem}.dst-flut .dt{font-size:1.12rem}.dst-flut .dp{font-size:.84rem;margin-top:.2rem}.dst-flut .db{font-size:.85rem;padding:.4rem .9rem;margin-top:.4rem}'
    + '.dst-flut .dtempo{position:absolute;left:0;bottom:0;height:4px;width:100%;background:linear-gradient(90deg,#ffe9a6,#e2a93a);transform-origin:left;animation:dstt ' + SEGUNDOS + 's linear forwards}'
    + '.dst-flut:hover .dtempo{animation-play-state:paused}'
    + '@keyframes dstt{from{transform:scaleX(1)}to{transform:scaleX(0)}}'
    + '.dstx{position:absolute;right:.3rem;top:.3rem;width:28px;height:28px;border:0;border-radius:50%;background:transparent;color:#fff;opacity:.65;font-size:17px;cursor:pointer}'
    + '.dst-bola{position:fixed;left:1rem;bottom:1rem;z-index:9998;width:58px;height:58px;border-radius:50%;padding:0;cursor:pointer;display:grid;place-items:center;'
    + 'background:radial-gradient(circle at 30% 20%,#5c1748,#12050f);border:1.5px solid rgba(255,217,120,.7);box-shadow:0 8px 26px -6px rgba(160,40,110,.9);transform:scale(0);transition:transform .35s cubic-bezier(.3,1.6,.6,1)}'
    + '.dst-bola.ve{transform:scale(1);animation:dstp 2.4s ease-out infinite}'
    + '.dst-bola svg{width:46px;height:46px}'
    + '.dst-bola b{position:absolute;right:-4px;top:-4px;min-width:22px;height:22px;border-radius:11px;background:linear-gradient(135deg,#ffe9a6,#e2a93a);color:#2a0c18;font:900 11px/22px Cinzel,serif;text-align:center}'
    + '@keyframes dste{from{transform:translateY(120%);opacity:0}to{transform:none;opacity:1}}'
    + '@media (max-width:560px){.dst-grande{flex-direction:column;text-align:center}.dst-grande svg{width:6.5rem;height:6.5rem}}'
    + '@media (prefers-reduced-motion:reduce){.dst *,.dst,.dst-bola{animation:none!important;transition:none!important}}';

  function conteudo() {
    return D.arte + '<span><span class="dt">' + val(D.titulo, D) + '</span><span class="dp">' + val(D.texto, D) + '</span><span class="db">' + D.botao + '</span></span>';
  }
  function montar() {
    if (document.querySelector(".dst-flut,.dst-bola")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var link = val(D.link, D);
    if (inicio) {
      var g = document.createElement("a"); g.href = link; g.className = "dst dst-grande";
      g.innerHTML = conteudo() + (D.marca ? '<span class="dn" aria-hidden="true">' + D.marca + '</span>' : "");
      var heroi = document.querySelector("section.hero");
      if (heroi && heroi.parentNode) heroi.parentNode.insertBefore(g, heroi.nextSibling); else document.body.insertBefore(g, document.body.firstChild);
    }
    var f = document.createElement("a"); f.href = link; f.className = "dst dst-flut" + (fechado ? " sai" : "");
    f.innerHTML = conteudo() + '<button class="dstx" aria-label="Fechar">×</button><span class="dtempo"></span>';
    var b = document.createElement("button"); b.className = "dst-bola"; b.setAttribute("aria-label", val(D.titulo, D));
    b.innerHTML = D.arte + (D.marca ? "<b>" + D.marca + "</b>" : "");
    document.body.appendChild(f); document.body.appendChild(b);
    var temp = null;
    function esconde() { clearTimeout(temp); f.classList.add("sai"); setTimeout(function () { b.classList.add("ve"); }, 350); }
    function mostra() {
      b.classList.remove("ve"); f.classList.remove("sai");
      var t = f.querySelector(".dtempo"); t.style.animation = "none"; void t.offsetWidth; t.style.animation = "";
      clearTimeout(temp); temp = setTimeout(esconde, SEGUNDOS * 1000);
    }
    var pausado = 0;
    f.addEventListener("mouseenter", function () { clearTimeout(temp); pausado = 1; });
    f.addEventListener("mouseleave", function () { if (pausado) { pausado = 0; temp = setTimeout(esconde, 2500); } });
    f.querySelector(".dstx").addEventListener("click", function (e) {
      e.preventDefault(); e.stopPropagation(); esconde(); try { sessionStorage.setItem("dst-fechado-" + D.id, "1"); } catch (er) {}
    });
    b.addEventListener("click", mostra);
    if (fechado) b.classList.add("ve"); else temp = setTimeout(esconde, SEGUNDOS * 1000);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();
