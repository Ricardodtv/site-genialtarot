/* O Meu Dia — o service worker do aviso das 8h (15/11/2026)
   Só trata do aviso: não guarda páginas nem mexe nos pedidos (o scope é /o-meu-dia).
   O aviso chega SEM conteúdo (push sem dados: não é preciso cifrar nada no servidor). Ao chegar,
   este guião lê o signo guardado (Cache Storage «gt-meudia», escrito pela página) e o horóscopo
   de hoje, e mostra a frase-chave do signo. Sem signo ou sem rede, mostra um texto geral. */
const NOMES = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"];
const NOMES_BR = ["Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem", "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"];
const GLIFOS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"];

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

function hoje() {
  const d = new Date();
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}

async function texto() {
  let s = null;
  try { const r = await (await caches.open("gt-meudia")).match("/o-meu-dia/signo"); if (r) s = parseInt(await r.text(), 10); } catch (e) {}
  const pt = (Intl.DateTimeFormat().resolvedOptions().timeZone || "").startsWith("Europe");
  const N = pt ? NOMES : NOMES_BR;
  if (!(s >= 0 && s < 12)) return { title: "✨ O seu dia já chegou", body: "O seu horóscopo e a sua carta de hoje estão à sua espera." };
  try {
    const x = await (await fetch("/horoscopo-dia/" + hoje() + ".json")).json();
    const hora = (ms) => new Date(+ms).toLocaleTimeString("pt-PT", { hour: "2-digit", minute: "2-digit" });
    const k = String(x.s[s].k).replace(/\{S:(\d+)\}/g, (_, n) => N[+n]).replace(/\{H:(\d+)\}/g, (_, ms) => hora(ms));
    return { title: GLIFOS[s] + " " + N[s] + " · o seu dia", body: k + " A sua carta de hoje está à espera." };
  } catch (e) {
    return { title: GLIFOS[s] + " " + N[s] + " · o seu dia", body: "O seu horóscopo e a sua carta de hoje estão à sua espera." };
  }
}

self.addEventListener("push", (e) => {
  e.waitUntil(texto().then((t) => self.registration.showNotification(t.title, {
    body: t.body, icon: "/o-meu-dia-icone-192.png", badge: "/o-meu-dia-icone-96.png", tag: "o-meu-dia", data: { url: "/o-meu-dia?de=aviso" },
  })));
});

self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || "/o-meu-dia?de=aviso";
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((l) => {
    for (const c of l) if (new URL(c.url).pathname === "/o-meu-dia" && "focus" in c) { c.navigate(url); return c.focus(); }
    return self.clients.openWindow(url);
  }));
});
