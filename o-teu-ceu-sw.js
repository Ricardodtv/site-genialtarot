/* O Teu Céu — o service worker (28/10/2026)
   Guarda a casca da app para abrir sem rede. O horóscopo do dia vai primeiro à rede
   e só usa a cópia guardada se não houver ligação. Subir VERSAO a cada mudança. */
const VERSAO = "teuceu-v7";
const CASCA = [
  "/o-teu-ceu", "/o-teu-ceu.webmanifest", "/o-teu-ceu-icone-192.png", "/o-teu-ceu-icone-512.png",
  "/o-teu-ceu-icone.svg", "/lua-cheia-240.png", "/ascendente-calc.js", "/carta-de-tarot-textos.js", "/o-teu-ceu-linguas.js"
];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSAO).then((c) => c.addAll(CASCA)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith("teuceu-") && k !== VERSAO).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const r = e.request;
  if (r.method !== "GET") return;
  const u = new URL(r.url);
  // 29/10/2026: também os .js da app vêm da rede primeiro (página nova + textos velhos em cache = botões «undefined»)
  const daRede = u.origin === location.origin && (u.pathname === "/o-teu-ceu" || u.pathname.startsWith("/horoscopo-dia/") || u.pathname.endsWith(".js"));
  if (daRede) {
    // rede primeiro: a página e o céu do dia têm de estar frescos
    e.respondWith(fetch(r).then((res) => { const c = res.clone(); caches.open(VERSAO).then((k) => k.put(r, c)); return res; })
      .catch(() => caches.match(r, { ignoreSearch: true })));
    return;
  }
  e.respondWith(caches.match(r, { ignoreSearch: true }).then((m) => m || fetch(r).then((res) => {
    if (res.ok || res.type === "opaque") { const c = res.clone(); caches.open(VERSAO).then((k) => k.put(r, c)); }
    return res;
  })));
});
