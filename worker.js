// Genial Tarot — Cloudflare Pages worker
// Serve o site estático e expõe /notify, que envia avisos para o Telegram.
// O token do bot fica guardado em segredo na Cloudflare (nunca aparece no site).
//
// Variáveis a configurar na Cloudflare (Settings → Variables and Secrets):
//   TELEGRAM_BOT_TOKEN  → token do bot (do @BotFather)
//   TELEGRAM_CHAT_ID    → o teu chat id do Telegram

function buildMessage(type, d = {}) {
  const clean = (v, max = 300) => String(v ?? "").slice(0, max);
  if (type === "reading") {
    return [
      "🔮 NOVA LEITURA DE TAROT — Genialtarot",
      "",
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)}`,
      `📍 ${clean(d.city)}, ${clean(d.country)}`,
      `🎂 Nascimento: ${clean(d.date_of_birth)}`,
      `🎯 Área: ${clean(d.area)}`,
      "",
      "📜 Veredito:",
      clean(d.verdict, 3000),
    ].join("\n");
  }
  if (type === "rating") {
    const stars = "⭐".repeat(Math.max(1, Math.min(5, Number(d.rating) || 0)));
    return `${stars} AVALIAÇÃO — Genialtarot\n\n👤 ${clean(d.name)}\n🎯 Área: ${clean(d.area)}\n Nota: ${clean(d.rating)}/5`;
  }
  if (type === "ratelimit") {
    return `⛔ LIMITE DIÁRIO ATINGIDO — Genialtarot\n\n👤 ${clean(d.name)}\n📧 ${clean(d.email)}\nTentou fazer mais de 2 leituras hoje.`;
  }
  if (type === "blocked") {
    return `🚫 ACESSO BLOQUEADO — Genialtarot\n\nUm visitante foi bloqueado por dados inválidos repetidos.\n👤 Último nome usado: ${clean(d.name)}`;
  }
  return null;
}

// ===================== Horóscopo diário (YouTube) =====================
const ZODIAC_PLAYLIST_ID = "PL1CDtoz2ES7SiWoZTboxt124gX-BKn8p6";
const SIGN_PATTERNS = {
  carneiro: /carneiro|♈|aries|áries/i,
  touro: /touro|♉|taurus/i,
  gemeos: /g[eé]m[eé]os|♊|gemini/i,
  caranguejo: /caranguejo|c[aâ]ncer|♋|cancer/i,
  leao: /le[aã]o|♌|leo/i,
  virgem: /virgem|♍|virgo/i,
  balanca: /balan[cç]a|♎|libra/i,
  escorpiao: /escorpi[aã]o|♏|scorpio/i,
  sagitario: /sagit[aá]rio|♐|sagittarius/i,
  capricornio: /capric[oó]rnio|♑|capricorn/i,
  aquario: /aqu[aá]rio|♒|aquarius/i,
  peixes: /peixes|♓|pisces/i,
};
const YT_HEADERS = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
  "accept-language": "pt-PT,pt;q=0.9,en;q=0.7",
};

function parseTimestampToSeconds(timestamp) {
  const parts = timestamp.replace(/\./g, ":").split(":").map((p) => Number.parseInt(p, 10));
  if (parts.some(Number.isNaN)) return null;
  if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
  if (parts.length === 2) return parts[0] * 60 + parts[1];
  return null;
}

function extractTimestamps(description) {
  const timestamps = {};
  const timestampPattern = /(\d{1,2}[:.]\d{2}(?:[:.]\d{2})?)/;
  for (const line of description.split(/\r?\n/)) {
    const match = line.match(timestampPattern);
    if (!match) continue;
    const seconds = parseTimestampToSeconds(match[1]);
    if (seconds === null) continue;
    const signText = line.replace(match[1], " ");
    for (const [key, pattern] of Object.entries(SIGN_PATTERNS)) {
      if (timestamps[key] === undefined && pattern.test(signText)) {
        timestamps[key] = seconds;
        break;
      }
    }
  }
  return timestamps;
}

async function fetchText(url) {
  const response = await fetch(url, { headers: YT_HEADERS, redirect: "follow" });
  if (!response.ok) return null;
  return response.text();
}

function decodeJsonString(value) {
  try {
    return JSON.parse(`"${value}"`);
  } catch {
    return value.replace(/\\n/g, "\n").replace(/\\"/g, '"').replace(/\\u0026/g, "&");
  }
}

function readJsonField(html, field) {
  const pattern = new RegExp(`"${field}":"((?:[^"\\\\]|\\\\.)*)"`);
  return decodeJsonString(html.match(pattern)?.[1] ?? "");
}

function pickBest(candidates) {
  const valid = candidates.filter(Boolean);
  valid.sort((a, b) => {
    const byDate = String(b.published).localeCompare(String(a.published));
    return byDate !== 0 ? byDate : (a.index ?? 0) - (b.index ?? 0);
  });
  return valid[0] ?? null;
}

// Estratégia 1: feed RSS público da playlist (uma só chamada, sem chave)
async function zodiacViaRss(diag) {
  const xml = await fetchText(
    `https://www.youtube.com/feeds/videos.xml?playlist_id=${ZODIAC_PLAYLIST_ID}`,
  );
  if (!xml) { diag.rss = "falhou"; return null; }
  diag.rss = `ok (${xml.length} bytes)`;
  const entries = xml.split("<entry>").slice(1);
  const candidates = entries.map((entry, index) => {
    const videoId = entry.match(/<yt:videoId>([\w-]{11})<\/yt:videoId>/)?.[1];
    if (!videoId) return null;
    const title = entry.match(/<title>([\s\S]*?)<\/title>/)?.[1] ?? "";
    const published = entry.match(/<published>([\s\S]*?)<\/published>/)?.[1] ?? "";
    const rawDesc = entry.match(/<media:description>([\s\S]*?)<\/media:description>/)?.[1] ?? "";
    const description = rawDesc
      .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"').replace(/&#39;/g, "'");
    const timestamps = extractTimestamps(description);
    diag.candidatos.push({ via: "rss", videoId, titulo: title.slice(0, 50), publicado: published, nSignos: Object.keys(timestamps).length });
    if (Object.keys(timestamps).length < 10) return null;
    return { videoId, title, published, index, timestamps };
  });
  return pickBest(candidates);
}

// Estratégia 2: API oficial do YouTube (precisa da chave YT_API_KEY na Cloudflare)
async function zodiacViaApi(diag, apiKey) {
  if (!apiKey) { diag.apiOficial = "sem chave YT_API_KEY"; return null; }
  const listRes = await fetch(
    `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=12&playlistId=${ZODIAC_PLAYLIST_ID}&key=${apiKey}`,
  );
  if (!listRes.ok) { diag.apiOficial = `playlistItems ${listRes.status}`; return null; }
  const list = await listRes.json();
  const ids = (list.items ?? []).map((i) => i.contentDetails?.videoId).filter(Boolean);
  if (!ids.length) { diag.apiOficial = "sem vídeos"; return null; }
  const vidsRes = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${ids.join(",")}&key=${apiKey}`,
  );
  if (!vidsRes.ok) { diag.apiOficial = `videos ${vidsRes.status}`; return null; }
  const vids = await vidsRes.json();
  diag.apiOficial = `ok (${(vids.items ?? []).length} vídeos)`;
  const candidates = (vids.items ?? []).map((v, index) => {
    const description = v.snippet?.description ?? "";
    const timestamps = extractTimestamps(description);
    diag.candidatos.push({ via: "api", videoId: v.id, titulo: (v.snippet?.title ?? "").slice(0, 50), publicado: v.snippet?.publishedAt, nSignos: Object.keys(timestamps).length });
    if (Object.keys(timestamps).length < 10) return null;
    return { videoId: v.id, title: v.snippet?.title ?? "", published: v.snippet?.publishedAt ?? "", index, timestamps };
  });
  return pickBest(candidates);
}

// ============ Previsão Anual 2026: um vídeo por signo ============
const ANNUAL_PLAYLIST_ID = "PL1CDtoz2ES7Rj4Pgnzsk1B0yMJ5MsZRim";

async function fetchAnnualZodiac(debug) {
  const diag = { entradas: 0, porSigno: {} };
  const xml = await fetchText(
    `https://www.youtube.com/feeds/videos.xml?playlist_id=${ANNUAL_PLAYLIST_ID}`,
  );
  if (!xml) {
    if (debug) return { data: null, diag: { ...diag, rss: "falhou" } };
    throw new Error("Não foi possível consultar a playlist anual");
  }
  diag.rss = `ok (${xml.length} bytes)`;
  const entries = xml.split("<entry>").slice(1);
  diag.entradas = entries.length;
  const signs = {};
  for (const entry of entries) {
    const videoId = entry.match(/<yt:videoId>([\w-]{11})<\/yt:videoId>/)?.[1];
    if (!videoId) continue;
    const title = (entry.match(/<title>([\s\S]*?)<\/title>/)?.[1] ?? "")
      .replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
    const rawDesc = entry.match(/<media:description>([\s\S]*?)<\/media:description>/)?.[1] ?? "";
    for (const [key, pattern] of Object.entries(SIGN_PATTERNS)) {
      if (!signs[key] && (pattern.test(title) || pattern.test(rawDesc.slice(0, 200)))) {
        signs[key] = { videoId, title };
        diag.porSigno[key] = title.slice(0, 60);
        break;
      }
    }
  }
  const data = Object.keys(signs).length > 0 ? { signs, encontrados: Object.keys(signs).length } : null;
  return debug ? { data, diag } : data;
}
// ==================================================================

async function fetchLatestDailyZodiac(debug, env) {
  const diag = { candidatos: [] };
  let best = null;
  try { best = await zodiacViaRss(diag); } catch (e) { diag.rss = `erro: ${String(e).slice(0, 80)}`; }
  if (!best) {
    try { best = await zodiacViaApi(diag, env?.YT_API_KEY); } catch (e) { diag.apiOficial = `erro: ${String(e).slice(0, 80)}`; }
  }
  return debug ? { data: best, diag } : best;
}
// ======================================================================

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Vídeo diário mais recente + minutos de cada signo (com cache de 15 min)
    if (url.pathname === "/api/zodiac") {
      if (url.searchParams.get("debug") === "1") {
        try {
          const result = await fetchLatestDailyZodiac(true, env);
          return new Response(JSON.stringify({ ok: true, ...result }), {
            headers: { "Content-Type": "application/json" },
          });
        } catch (e) {
          return new Response(JSON.stringify({ ok: false, error: String(e) }), {
            status: 502, headers: { "Content-Type": "application/json" },
          });
        }
      }
      const cacheKey = new Request(`https://cache.genialtarot/api/zodiac`);
      const cache = caches.default;
      const cached = await cache.match(cacheKey);
      if (cached) return cached;
      try {
        const data = await fetchLatestDailyZodiac(false, env);
        const response = new Response(JSON.stringify({ ok: true, data }), {
          headers: {
            "Content-Type": "application/json",
            "Cache-Control": "public, s-maxage=900, max-age=300",
          },
        });
        if (data) ctx.waitUntil(cache.put(cacheKey, response.clone()));
        return response;
      } catch (e) {
        return new Response(JSON.stringify({ ok: false, error: String(e) }), {
          status: 502, headers: { "Content-Type": "application/json" },
        });
      }
    }

    // Previsão Anual 2026: vídeos organizados por signo (cache 1h)
    if (url.pathname === "/api/anual") {
      if (url.searchParams.get("debug") === "1") {
        try {
          const result = await fetchAnnualZodiac(true);
          return new Response(JSON.stringify({ ok: true, ...result }), {
            headers: { "Content-Type": "application/json" },
          });
        } catch (e) {
          return new Response(JSON.stringify({ ok: false, error: String(e) }), {
            status: 502, headers: { "Content-Type": "application/json" },
          });
        }
      }
      const cacheKey = new Request(`https://cache.genialtarot/api/anual`);
      const cache = caches.default;
      const cached = await cache.match(cacheKey);
      if (cached) return cached;
      try {
        const data = await fetchAnnualZodiac(false);
        const response = new Response(JSON.stringify({ ok: true, data }), {
          headers: {
            "Content-Type": "application/json",
            "Cache-Control": "public, s-maxage=3600, max-age=600",
          },
        });
        if (data) ctx.waitUntil(cache.put(cacheKey, response.clone()));
        return response;
      } catch (e) {
        return new Response(JSON.stringify({ ok: false, error: String(e) }), {
          status: 502, headers: { "Content-Type": "application/json" },
        });
      }
    }

    if (url.pathname === "/notify") {
      if (request.method !== "POST") {
        // Modo diagnóstico: /notify?test=1 envia uma mensagem de teste ao Telegram
        const diag = {
          ok: true,
          temToken: Boolean(env.TELEGRAM_BOT_TOKEN),
          temChatId: Boolean(env.TELEGRAM_CHAT_ID),
        };
        if (url.searchParams.get("test") === "1" && diag.temToken && diag.temChatId) {
          try {
            const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text: "🔔 Teste da ponte Genial Tarot — se estás a ler isto, está tudo a funcionar!" }),
            });
            const body = await r.json().catch(() => null);
            diag.telegramRespondeu = r.ok;
            diag.telegramErro = body && body.ok === false ? body.description : null;
          } catch (e) {
            diag.telegramRespondeu = false;
            diag.telegramErro = String(e);
          }
        }
        return new Response(JSON.stringify(diag), {
          headers: { "Content-Type": "application/json" },
        });
      }
      try {
        const { type, data } = await request.json();
        const text = buildMessage(type, data);
        if (!text) throw new Error("tipo inválido");
        if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_CHAT_ID) {
          return new Response(JSON.stringify({ ok: false, error: "faltam segredos TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID" }), {
            status: 500, headers: { "Content-Type": "application/json" },
          });
        }
        const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text }),
        });
        return new Response(JSON.stringify({ ok: r.ok }), {
          headers: { "Content-Type": "application/json" },
        });
      } catch (e) {
        return new Response(JSON.stringify({ ok: false }), {
          status: 400, headers: { "Content-Type": "application/json" },
        });
      }
    }

    // Tudo o resto: servir o site normalmente
    return env.ASSETS.fetch(request);
  },
};
