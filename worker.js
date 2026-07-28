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

async function fetchLatestDailyZodiac(debug) {
  const diag = { playlistOk: false, videoIds: 0, candidatos: [] };
  const playlistHtml = await fetchText(
    `https://www.youtube.com/playlist?list=${ZODIAC_PLAYLIST_ID}&hl=pt-PT&gl=PT`,
  );
  if (!playlistHtml) {
    if (debug) return { data: null, diag };
    throw new Error("Não foi possível consultar a playlist diária");
  }
  diag.playlistOk = true;
  diag.playlistTamanho = playlistHtml.length;

  const videoIds = Array.from(
    new Set(Array.from(playlistHtml.matchAll(/"videoId":"([\w-]{11})"/g), (m) => m[1])),
  ).slice(0, 12);
  diag.videoIds = videoIds.length;
  if (videoIds.length === 0) {
    if (debug) return { data: null, diag };
    throw new Error("A playlist diária não devolveu vídeos");
  }

  const candidates = await Promise.all(videoIds.map(async (videoId) => {
    const html = await fetchText(`https://www.youtube.com/watch?v=${videoId}&hl=pt-PT&gl=PT`);
    if (!html) {
      diag.candidatos.push({ videoId, erro: "sem html" });
      return null;
    }
    const description = readJsonField(html, "shortDescription");
    const timestamps = extractTimestamps(description);
    diag.candidatos.push({
      videoId,
      titulo: readJsonField(html, "title").slice(0, 50),
      htmlTamanho: html.length,
      descTamanho: description.length,
      nSignos: Object.keys(timestamps).length,
    });
    if (Object.keys(timestamps).length < 10) return null;
    return {
      videoId,
      title: readJsonField(html, "title"),
      published: readJsonField(html, "publishDate") || readJsonField(html, "uploadDate"),
      timestamps,
    };
  }));

  const valid = candidates.filter(Boolean);
  valid.sort((a, b) => b.published.localeCompare(a.published));
  const best = valid[0] ?? null;
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
          const result = await fetchLatestDailyZodiac(true);
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
        const data = await fetchLatestDailyZodiac();
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
