/* Cartões da página inicial conforme o dia e o período (06/11/2026, pedido dele). O plano faz-se no painel e vem de /api/cartoes-agenda.
   Regra dele (06/11): em cada período só aparecem os cartões ligados a esse período, pela ordem do plano.
   Período vazio ou sem plano: a página fica como está, para nunca ficar sem cartões.
   Manhã até às 11:59 e tarde daí até à meia-noite, pela hora de quem visita. */
(() => {
  const K = "gt-cartoes", D = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"];
  function aplica(a) {
    const box = document.querySelector(".portas"); if (!box || !a || !a.slots) return;
    const d = new Date(), L = a.slots[D[d.getDay()] + "-" + (d.getHours() < 12 ? "m" : "t")] || [];
    [...box.children].forEach((e) => { e.style.order = ""; e.style.removeProperty("display"); });
    if (L.length) Object.entries(a.sel || {}).forEach(([id, q]) => { const e = !L.includes(id) && document.querySelector(q); if (e) e.style.setProperty("display", "none", "important"); });
    box.style.gridAutoFlow = L.length ? "dense" : "";
    L.forEach((id, i) => { const s = a.sel && a.sel[id], e = s && document.querySelector(s); if (e) e.style.order = i - L.length; });
  }
  try { aplica(JSON.parse(localStorage.getItem(K))); } catch (e) {}   // o último plano entra logo, para os cartões não saltarem
  fetch("/api/cartoes-agenda").then((r) => r.ok ? r.json() : null).then((a) => {
    if (!a) return; aplica(a); try { localStorage.setItem(K, JSON.stringify(a)); } catch (e) {}
  }).catch(() => {});
})();
