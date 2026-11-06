/* Cartões da página inicial conforme o dia e o período (06/11/2026, pedido dele). O plano faz-se no painel e vem de /api/cartoes-agenda.
   Só muda a ORDEM: todos os cartões continuam na página e nas ligações, por causa do Google. Sem plano para este período fica tudo como está.
   Manhã até às 11:59 e tarde daí até à meia-noite, pela hora de quem visita. */
(() => {
  const K = "gt-cartoes", D = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"];
  function aplica(a) {
    const box = document.querySelector(".portas"); if (!box || !a || !a.slots) return;
    const d = new Date(), L = a.slots[D[d.getDay()] + "-" + (d.getHours() < 12 ? "m" : "t")] || [];
    [...box.children].forEach((e) => { e.style.order = ""; });
    box.style.gridAutoFlow = L.length ? "dense" : "";
    L.forEach((id, i) => { const s = a.sel && a.sel[id], e = s && document.querySelector(s); if (e) e.style.order = i - L.length; });
  }
  try { aplica(JSON.parse(localStorage.getItem(K))); } catch (e) {}   // o último plano entra logo, para os cartões não saltarem
  fetch("/api/cartoes-agenda").then((r) => r.ok ? r.json() : null).then((a) => {
    if (!a) return; aplica(a); try { localStorage.setItem(K, JSON.stringify(a)); } catch (e) {}
  }).catch(() => {});
})();
