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
const WEEKEND_PLAYLIST_ID = "PL1CDtoz2ES7SMhQqxpoRsJ2uzsi8caP48";
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
async function zodiacViaRss(diag, playlistId) {
  const xml = await fetchText(
    `https://www.youtube.com/feeds/videos.xml?playlist_id=${playlistId}`,
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
async function zodiacViaApi(diag, apiKey, playlistId) {
  if (!apiKey) { diag.apiOficial = "sem chave YT_API_KEY"; return null; }
  const listRes = await fetch(
    `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=12&playlistId=${playlistId}&key=${apiKey}`,
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

// Plano B do anual: a API oficial do YouTube.
//
// ⚠️ 21/08/2026: o YouTube MATOU os feeds RSS de playlists (dão 404). As três
// páginas de signos do site ficaram sem fonte. O diário e o fim-de-semana tinham
// plano B; o anual NÃO tinha nenhum -- só tentava o RSS e desistia. É por isso
// que esta função existe.
async function annualViaApi(diag, apiKey) {
  if (!apiKey) { diag.apiOficial = "sem chave YT_API_KEY"; return null; }
  const listRes = await fetch(
    `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=25&playlistId=${ANNUAL_PLAYLIST_ID}&key=${apiKey}`,
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
  const signs = {};
  for (const v of vids.items ?? []) {
    const title = v.snippet?.title ?? "";
    const desc = (v.snippet?.description ?? "").slice(0, 200);
    for (const [key, pattern] of Object.entries(SIGN_PATTERNS)) {
      if (!signs[key] && (pattern.test(title) || pattern.test(desc))) {
        signs[key] = { videoId: v.id, title };
        diag.porSigno[key] = title.slice(0, 60);
        break;
      }
    }
  }
  return Object.keys(signs).length > 0
    ? { signs, encontrados: Object.keys(signs).length }
    : null;
}

async function fetchAnnualZodiac(debug, env) {
  const diag = { entradas: 0, porSigno: {} };
  const xml = await fetchText(
    `https://www.youtube.com/feeds/videos.xml?playlist_id=${ANNUAL_PLAYLIST_ID}`,
  );
  if (!xml) {
    diag.rss = "falhou";
    // ⚠️ já não se desiste aqui: tenta-se a API oficial antes de dar erro.
    const porApi = await annualViaApi(diag, env?.YT_API_KEY);
    if (porApi) return debug ? { data: porApi, diag } : porApi;
    if (debug) return { data: null, diag };
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
  let data = Object.keys(signs).length > 0 ? { signs, encontrados: Object.keys(signs).length } : null;
  // ⚠️ o RSS pode responder e ainda assim vir incompleto (playlist truncada).
  // Se não trouxer os 12 signos, tenta-se a API oficial e fica-se com a melhor.
  if (!data || data.encontrados < 12) {
    const porApi = await annualViaApi(diag, env?.YT_API_KEY);
    if (porApi && (!data || porApi.encontrados > data.encontrados)) data = porApi;
  }
  return debug ? { data, diag } : data;
}
// ==================================================================

async function fetchLatestDailyZodiac(debug, env, playlistId = ZODIAC_PLAYLIST_ID) {
  const diag = { candidatos: [] };
  let best = null;
  try { best = await zodiacViaRss(diag, playlistId); } catch (e) { diag.rss = `erro: ${String(e).slice(0, 80)}`; }
  if (!best) {
    try { best = await zodiacViaApi(diag, env?.YT_API_KEY, playlistId); } catch (e) { diag.apiOficial = `erro: ${String(e).slice(0, 80)}`; }
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
            // ⚠️ 21/08/2026: uma falha PASSAGEIRA não pode ficar guardada 15
            // minutos -- a página fica morta e parece avaria permanente. Com
            // dados, guarda-se; sem dados, não se guarda e tenta-se outra vez.
            "Cache-Control": data
              ? "public, s-maxage=900, max-age=300"
              : "no-store",
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

    // Horóscopo Fim de Semana: último vídeo + minutos por signo (cache 15 min)
    if (url.pathname === "/api/fimsemana") {
      if (url.searchParams.get("debug") === "1") {
        try {
          const result = await fetchLatestDailyZodiac(true, env, WEEKEND_PLAYLIST_ID);
          return new Response(JSON.stringify({ ok: true, ...result }), {
            headers: { "Content-Type": "application/json" },
          });
        } catch (e) {
          return new Response(JSON.stringify({ ok: false, error: String(e) }), {
            status: 502, headers: { "Content-Type": "application/json" },
          });
        }
      }
      const cacheKey = new Request(`https://cache.genialtarot/api/fimsemana`);
      const cache = caches.default;
      const cached = await cache.match(cacheKey);
      if (cached) return cached;
      try {
        const data = await fetchLatestDailyZodiac(false, env, WEEKEND_PLAYLIST_ID);
        const response = new Response(JSON.stringify({ ok: true, data }), {
          headers: {
            "Content-Type": "application/json",
            // ⚠️ 21/08/2026: uma falha PASSAGEIRA não pode ficar guardada 15
            // minutos -- a página fica morta e parece avaria permanente. Com
            // dados, guarda-se; sem dados, não se guarda e tenta-se outra vez.
            "Cache-Control": data
              ? "public, s-maxage=900, max-age=300"
              : "no-store",
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
          const result = await fetchAnnualZodiac(true, env);
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
        const data = await fetchAnnualZodiac(false, env);
        const response = new Response(JSON.stringify({ ok: true, data }), {
          headers: {
            "Content-Type": "application/json",
            // ⚠️ ver a nota acima: falha passageira não se guarda.
            "Cache-Control": data
              ? "public, s-maxage=3600, max-age=600"
              : "no-store",
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

    // Diz a pagina de que pais vem o visitante, para o formulario ja vir
    // preenchido com o pais certo em vez de "Portugal" para toda a gente.
    // Posto a 16/08/2026: ele reparou que 62 registos diziam Portugal com
    // cidade estrangeira, porque o campo vinha com valor por omissao.
    if (url.pathname === "/geo") {
      const g = request.cf || {};
      return new Response(JSON.stringify({
        country: g.country || null,
        city: g.city || null,
      }), { headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
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

        // ── REDE DE SEGURANCA (16/08/2026) ───────────────────────────────
        // Guarda a captura numa fila da Cloudflare ANTES de qualquer outra
        // coisa. O cerebro vai la busca-la de minuto a minuto, cria a ficha
        // com codigo e apaga. Se a casa estiver desligada, fica a espera.
        // ⚠️ POR ACRESCIMO: nao substitui o Telegram nem o Supabase. Se esta
        // parte falhar, o resto segue na mesma -- por isso o try/catch mudo.
        try {
          if (env.CAPTURAS) {
            const cf2 = request.cf || {};
            const chave = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
            await env.CAPTURAS.put(chave, JSON.stringify({
              type, data,
              recebido: new Date().toISOString(),
              cidade: cf2.city || null,
              pais: cf2.country || null,
            }), { expirationTtl: 60 * 60 * 24 * 30 });
          }
        } catch (e) { /* nunca estragar o pedido do visitante por causa da fila */ }

        let text = buildMessage(type, data);
        if (!text) throw new Error("tipo inválido");
        // Localização REAL detetada pela Cloudflare (cidade/país do visitante) + IP
        const cf = request.cf || {};
        const ip = request.headers.get("CF-Connecting-IP") || "";
        const local = [cf.city, cf.region, cf.country].filter(Boolean).join(", ");
        if (local || ip) {
          text += `\n\n📍 Detetado: ${local || "local desconhecido"}${ip ? `\n🖥 IP: ${ip}` : ""}`;
        }
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

    // ===== Estatísticas de visitas (página privada, dados da Cloudflare) =====
    // Precisa de 3 valores em Settings → Variables and Secrets:
    //   CF_API_TOKEN (Secret)  → token da API com permissão "Analytics: Read" na zona
    //   CF_ZONE_ID   (texto)   → Zone ID do domínio (página Overview, coluna direita)
    //   STATS_KEY    (Secret)  → a palavra-passe que abre a página de estatísticas
    if (url.pathname === "/api/stats") {
      const jsonResp = (obj, status) => new Response(JSON.stringify(obj), {
        status: status || 200, headers: { "Content-Type": "application/json" },
      });
      if (url.searchParams.get("debug") === "1") {
        return jsonResp({ ok: true, temToken: !!env.CF_API_TOKEN, temZona: !!env.CF_ZONE_ID, temChave: !!env.STATS_KEY });
      }
      const chave = url.searchParams.get("chave") || "";
      if (!env.STATS_KEY || chave !== env.STATS_KEY) return jsonResp({ ok: false, error: "chave errada" }, 403);
      if (!env.CF_API_TOKEN || !env.CF_ZONE_ID) return jsonResp({ ok: false, error: "faltam CF_API_TOKEN / CF_ZONE_ID nas Variables and Secrets" }, 500);
      const dias = Math.min(60, Math.max(7, Number(url.searchParams.get("dias")) || 30));
      const desde = new Date(Date.now() - dias * 864e5).toISOString().slice(0, 10);
      try {
        const consulta = {
          query: "query($zona:String!,$desde:Date!){viewer{zones(filter:{zoneTag:$zona}){httpRequests1dGroups(limit:70,filter:{date_geq:$desde},orderBy:[date_ASC]){dimensions{date}sum{requests pageViews countryMap{clientCountryName requests}}uniq{uniques}}}}}",
          variables: { zona: env.CF_ZONE_ID, desde },
        };
        const r = await fetch("https://api.cloudflare.com/client/v4/graphql", {
          method: "POST",
          headers: { "Authorization": `Bearer ${env.CF_API_TOKEN}`, "Content-Type": "application/json" },
          body: JSON.stringify(consulta),
        });
        const j = await r.json();
        const grupos = j && j.data && j.data.viewer && j.data.viewer.zones && j.data.viewer.zones[0]
          ? j.data.viewer.zones[0].httpRequests1dGroups : null;
        if (!grupos) return jsonResp({ ok: false, error: "Cloudflare respondeu: " + JSON.stringify(j && j.errors ? j.errors : j).slice(0, 300) }, 502);
        const porPais = {};
        for (const g of grupos) {
          for (const p of (g.sum.countryMap || [])) {
            porPais[p.clientCountryName] = (porPais[p.clientCountryName] || 0) + p.requests;
          }
        }
        const paises = Object.entries(porPais)
          .sort((a, b) => b[1] - a[1]).slice(0, 12)
          .map(([codigo, pedidos]) => ({ codigo, pedidos }));

        // Páginas mais visitadas (hoje + período) — dataset detalhado; pode não existir em todos os planos
        let porPagina = null;
        try {
          const hoje = new Date().toISOString().slice(0, 10);
          const consulta2 = {
            query: "query($zona:String!,$desde:Date!,$hoje:Date!){viewer{zones(filter:{zoneTag:$zona}){periodo:httpRequestsAdaptiveGroups(limit:100,filter:{date_geq:$desde},orderBy:[count_DESC]){count dimensions{clientRequestPath}sum{visits}}hoje:httpRequestsAdaptiveGroups(limit:60,filter:{date:$hoje},orderBy:[count_DESC]){count dimensions{clientRequestPath}sum{visits}}origens:httpRequestsAdaptiveGroups(limit:60,filter:{date_geq:$desde},orderBy:[count_DESC]){count dimensions{clientRefererHost}sum{visits}}}}}",
            variables: { zona: env.CF_ZONE_ID, desde, hoje },
          };
          const r2 = await fetch("https://api.cloudflare.com/client/v4/graphql", {
            method: "POST",
            headers: { "Authorization": `Bearer ${env.CF_API_TOKEN}`, "Content-Type": "application/json" },
            body: JSON.stringify(consulta2),
          });
          const j2 = await r2.json();
          const z2 = j2 && j2.data && j2.data.viewer && j2.data.viewer.zones && j2.data.viewer.zones[0];
          const filtrar = (lista) => {
            const mapa = {};
            for (const g of (lista || [])) {
              const p = (g.dimensions.clientRequestPath || "").split("?")[0];
              if (p !== "/" && !p.endsWith(".html")) continue;
              const n = (g.sum && g.sum.visits) || g.count || 0;
              mapa[p] = (mapa[p] || 0) + n;
            }
            return Object.entries(mapa).sort((a, b) => b[1] - a[1]).slice(0, 12)
              .map(([caminho, visitas]) => ({ caminho, visitas }));
          };
          if (z2) porPagina = { hoje: filtrar(z2.hoje), periodo: filtrar(z2.periodo) };
          if (z2 && z2.origens) {
            const mapa = {};
            for (const g of z2.origens) {
              let hostv = (g.dimensions.clientRefererHost || "").toLowerCase();
              if (hostv.startsWith("www.")) hostv = hostv.slice(4);
              if (hostv === "genialtarot.com" || hostv.endsWith(".workers.dev")) continue; // navegação interna
              if (!hostv) hostv = "(direto)";
              const n = (g.sum && g.sum.visits) || g.count || 0;
              mapa[hostv] = (mapa[hostv] || 0) + n;
            }
            porPagina.origens = Object.entries(mapa).sort((a, b) => b[1] - a[1]).slice(0, 12)
              .map(([origem, visitas]) => ({ origem, visitas }));
          }
        } catch (e) { porPagina = null; }

        return jsonResp({
          ok: true,
          dias: grupos.map(g => ({ data: g.dimensions.date, paginas: g.sum.pageViews, pedidos: g.sum.requests, visitantes: g.uniq.uniques })),
          paises,
          porPagina,
        });
      } catch (e) {
        return jsonResp({ ok: false, error: String(e) }, 502);
      }
    }

    if (url.pathname === "/Estataomp8") {
      return new Response(PAGINA_ESTATISTICAS, { headers: { "Content-Type": "text/html; charset=utf-8" } });
    }

    // Tudo o resto: servir o site normalmente, com o beacon das estatisticas
    const resposta = await env.ASSETS.fetch(request);

    // ===== Cloudflare Web Analytics =====
    // 🚨 PORQUE E' QUE ISTO TEM DE ESTAR AQUI, e nao chega ligar no painel:
    // o site de Web Analytics existe na conta desde 28/07/2026 com
    // auto_install ligado -- e mesmo assim NENHUMA pagina trazia o beacon.
    // Medido a 22/08/2026: `curl https://genialtarot.com/ | grep
    // cloudflareinsights` deu ZERO em duas paginas diferentes. A instalacao
    // automatica da Cloudflare injecta o beacon nas respostas que passam pelo
    // proxy dela; as respostas deste site sao geradas pelo Worker, e a essas
    // ela nao toca. Resultado: quase um mes ligado a nao recolher nada.
    //
    // Sem o beacon nao ha paginas mais vistas, nem origens do trafego, nem
    // navegadores -- que e exactamente o que faltava na /Estataomp8.
    //
    // O token daqui NAO e' segredo: vai no HTML de todas as paginas e qualquer
    // visitante o ve. Veio da propria API da Cloudflare (rum/site_info).
    const tipo = resposta.headers.get("content-type") || "";
    if (!tipo.includes("text/html")) return resposta;
    return new HTMLRewriter()
      .on("head", { element(e) { e.append(BEACON_ESTATISTICAS, { html: true }); } })
      .transform(resposta);
  },
};

// ===== Página privada de estatísticas =====
// O codigo que conta as visitas. Copiado tal e qual do que a API da Cloudflare
// devolve em rum/site_info -- nao foi escrito a mao.
const BEACON_ESTATISTICAS = `<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "803a58a6fccd4bd9ac12cce898a73bce"}'></script><!-- End Cloudflare Web Analytics -->`;

const PAGINA_ESTATISTICAS = `<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex, nofollow" />
<title>Estatísticas — Genial Tarot</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: radial-gradient(ellipse at 50% -10%, oklch(0.22 0.05 270), oklch(0.15 0.03 265) 55%, oklch(0.1 0.03 262)); background-attachment: fixed; min-height: 100vh; color: oklch(0.95 0.01 280); font-family: system-ui, sans-serif; padding: 1.2rem; }
.caixa { max-width: 46rem; margin: 0 auto; }
h1 { font-family: Georgia, serif; color: oklch(0.88 0.08 90); text-align: center; margin: 1rem 0 0.3rem; font-size: 1.7rem; }
.sub { text-align: center; color: oklch(0.75 0.03 275); font-size: 0.85rem; margin-bottom: 1.4rem; }
.painel { border: 1px solid oklch(0.82 0.11 85 / 0.35); border-radius: 1rem; background: oklch(0.2 0.05 265 / 0.75); padding: 1.2rem; margin-bottom: 1rem; }
input { width: 100%; background: oklch(0.26 0.05 265); border: 1px solid oklch(0.82 0.11 85 / 0.35); color: inherit; border-radius: 0.6rem; padding: 0.7rem 0.9rem; font: inherit; outline: none; }
input:focus { border-color: oklch(0.82 0.11 85); }
button { margin-top: 0.7rem; width: 100%; border: none; border-radius: 9999px; padding: 0.75rem; font: inherit; font-weight: 700; background: linear-gradient(180deg, oklch(0.85 0.13 88), oklch(0.72 0.13 78)); color: oklch(0.2 0.04 270); cursor: pointer; }
.erro { color: oklch(0.78 0.14 25); text-align: center; margin-top: 0.6rem; font-size: 0.85rem; }
.cartoes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.7rem; margin-bottom: 1rem; }
.cartao { border: 1px solid oklch(0.82 0.11 85 / 0.3); border-radius: 0.8rem; background: oklch(0.2 0.05 265 / 0.75); padding: 0.8rem 0.6rem; text-align: center; }
.cartao .num { font-size: 1.5rem; font-weight: 800; color: oklch(0.88 0.08 90); }
.cartao .rot { font-size: 0.68rem; color: oklch(0.75 0.03 275); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.2rem; }
.grafico { display: flex; align-items: flex-end; gap: 2px; height: 180px; padding-top: 0.5rem; }
.barra { flex: 1; background: linear-gradient(180deg, oklch(0.85 0.13 88), oklch(0.6 0.11 78)); border-radius: 3px 3px 0 0; min-height: 2px; position: relative; }
.barra:hover { background: linear-gradient(180deg, oklch(0.92 0.14 90), oklch(0.7 0.12 80)); }
.legenda { display: flex; justify-content: space-between; color: oklch(0.75 0.03 275); font-size: 0.7rem; margin-top: 0.4rem; }
.filtros { display: flex; gap: 0.5rem; justify-content: center; margin-bottom: 1rem; }
.filtros button { width: auto; margin: 0; padding: 0.4rem 1.1rem; font-size: 0.85rem; background: oklch(0.26 0.05 265); color: oklch(0.85 0.05 90); border: 1px solid oklch(0.82 0.11 85 / 0.35); }
.filtros button.ativo { background: linear-gradient(180deg, oklch(0.85 0.13 88), oklch(0.72 0.13 78)); color: oklch(0.2 0.04 270); }
.rodape { text-align: center; color: oklch(0.7 0.03 275); font-size: 0.75rem; margin-top: 1.5rem; }
.titulo-sec { color: oklch(0.88 0.08 90); font-size: 0.9rem; letter-spacing: 0.08em; margin-bottom: 0.8rem; text-align: center; }
.abas-pg { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.15em; color: oklch(0.75 0.03 275); margin-bottom: 0.4rem; }
.pais { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.45rem; font-size: 0.85rem; }
.pais .nome { flex: 0 0 10rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pais .faixa { flex: 1; height: 0.85rem; border-radius: 4px; background: oklch(0.26 0.05 265); overflow: hidden; }
.pais .faixa span { display: block; height: 100%; background: linear-gradient(90deg, oklch(0.72 0.13 78), oklch(0.85 0.13 88)); border-radius: 4px; }
.pais .pct { flex: 0 0 3.2rem; text-align: right; color: oklch(0.85 0.05 90); }
@media (max-width: 480px) { .pais .nome { flex-basis: 7.5rem; } }
#zona-dados { display: none; }
</style>
</head>
<body>
<div class="caixa">
  <h1>✦ Estatísticas do Genial Tarot ✦</h1>
  <p class="sub">visitas ao site — dados da Cloudflare, só para os seus olhos</p>

  <div class="painel" id="zona-chave">
    <input id="chave" type="password" placeholder="Palavra-passe" />
    <button id="entrar">Ver estatísticas</button>
    <div class="erro" id="msg-erro"></div>
  </div>

  <div id="zona-dados">
    <div class="filtros">
      <button data-d="7">7 dias</button>
      <button data-d="30" class="ativo">30 dias</button>
      <button data-d="60">60 dias</button>
    </div>
    <div class="cartoes">
      <div class="cartao"><div class="num" id="t-paginas">–</div><div class="rot">Páginas vistas</div></div>
      <div class="cartao"><div class="num" id="t-visitantes">–</div><div class="rot">Visitantes</div></div>
      <div class="cartao"><div class="num" id="t-media">–</div><div class="rot">Média/dia</div></div>
    </div>
    <div class="painel">
      <div class="grafico" id="grafico"></div>
      <div class="legenda"><span id="l-ini"></span><span>páginas vistas por dia</span><span id="l-fim"></span></div>
    </div>
    <div class="painel">
      <div class="titulo-sec">📄 Páginas mais visitadas</div>
      <div class="abas-pg"><b>Hoje</b></div>
      <div id="pgs-hoje"></div>
      <div class="abas-pg" style="margin-top:0.9rem"><b id="rot-periodo">No período</b></div>
      <div id="pgs-periodo"></div>
    </div>
    <div class="painel">
      <div class="titulo-sec">🚪 Por onde chegam (origens)</div>
      <div id="origens"></div>
      <div style="text-align:center;color:oklch(0.7 0.03 275);font-size:0.68rem;font-style:italic;margin-top:0.5rem">"Direto" = escreveu o endereço, favoritos ou apps que não anunciam a origem (ex.: WhatsApp)</div>
    </div>
    <div class="painel">
      <div class="titulo-sec">🌍 De onde vêm os visitantes</div>
      <div id="paises"></div>
    </div>
  </div>

  <p class="rodape">Genial Tarot · página privada — não partilhe este endereço.</p>
</div>
<script>
var diasAtual = 30;
function fmt(n) { return n >= 10000 ? Math.round(n / 1000) + " mil" : String(n); }
function dataPt(iso) { var p = iso.split("-"); return p[2] + "/" + p[1]; }
function carregar() {
  var chave = document.getElementById("chave").value || localStorage.getItem("stats_chave") || "";
  if (!chave) return;
  document.getElementById("msg-erro").textContent = "A carregar…";
  fetch("/api/stats?chave=" + encodeURIComponent(chave) + "&dias=" + diasAtual)
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (!j.ok) { document.getElementById("msg-erro").textContent = "⚠️ " + (j.error || "erro"); return; }
      localStorage.setItem("stats_chave", chave);
      document.getElementById("zona-chave").style.display = "none";
      document.getElementById("zona-dados").style.display = "block";
      var d = j.dias, totP = 0, totV = 0, max = 1;
      d.forEach(function (x) { totP += x.paginas; totV += x.visitantes; if (x.paginas > max) max = x.paginas; });
      document.getElementById("t-paginas").textContent = fmt(totP);
      document.getElementById("t-visitantes").textContent = fmt(totV);
      document.getElementById("t-media").textContent = fmt(Math.round(totP / Math.max(1, d.length)));
      var g = document.getElementById("grafico");
      g.innerHTML = "";
      d.forEach(function (x) {
        var b = document.createElement("div");
        b.className = "barra";
        b.style.height = Math.max(2, Math.round(x.paginas / max * 170)) + "px";
        b.title = dataPt(x.data) + " — " + x.paginas + " páginas · " + x.visitantes + " visitantes";
        g.appendChild(b);
      });
      if (d.length) {
        document.getElementById("l-ini").textContent = dataPt(d[0].data);
        document.getElementById("l-fim").textContent = dataPt(d[d.length - 1].data);
      }
      var NOMES_PG = { "/": "🏠 Página Principal", "/index.html": "🏠 Página Principal", "/loja.html": "🛍️ Loja Mística",
        "/tarot-gratis.html": "🃏 Tarot Grátis", "/arvore.html": "🌳 Árvore da Vida", "/horoscopo.html": "🔮 Horóscopo Diário",
        "/anual.html": "📅 Previsão Anual", "/fimdesemana.html": "🌙 Fim de Semana" };
      function encherPgs(id, lista) {
        var alvo = document.getElementById(id);
        alvo.innerHTML = "";
        if (!lista || !lista.length) {
          alvo.innerHTML = '<div style="color:oklch(0.75 0.03 275);font-size:0.8rem;padding:0.3rem 0">sem dados (o plano gratuito guarda este detalhe só por alguns dias)</div>';
          return;
        }
        var max = lista[0].visitas || 1;
        lista.forEach(function (p) {
          var linha = document.createElement("div");
          linha.className = "pais";
          var nome = NOMES_PG[p.caminho] || p.caminho;
          linha.innerHTML = '<span class="nome">' + nome + '</span><span class="faixa"><span style="width:' + Math.max(3, Math.round(p.visitas / max * 100)) + '%"></span></span><span class="pct">' + p.visitas + '</span>';
          alvo.appendChild(linha);
        });
      }
      var NOMES_ORIG = { "(direto)": "🔗 Direto / desconhecido", "google.com": "🔎 Google", "google.pt": "🔎 Google",
        "facebook.com": "📘 Facebook", "m.facebook.com": "📘 Facebook", "l.facebook.com": "📘 Facebook", "lm.facebook.com": "📘 Facebook",
        "instagram.com": "📸 Instagram", "l.instagram.com": "📸 Instagram", "youtube.com": "▶️ YouTube", "m.youtube.com": "▶️ YouTube",
        "linktr.ee": "🌐 Linktree", "tiktok.com": "🎵 TikTok", "t.co": "🐦 X (Twitter)", "bing.com": "🔎 Bing", "duckduckgo.com": "🔎 DuckDuckGo" };
      function encherOrigens(lista) {
        var alvo = document.getElementById("origens");
        alvo.innerHTML = "";
        if (!lista || !lista.length) {
          alvo.innerHTML = '<div style="color:oklch(0.75 0.03 275);font-size:0.8rem;padding:0.3rem 0">sem dados de origens neste período</div>';
          return;
        }
        var max = lista[0].visitas || 1;
        lista.forEach(function (o) {
          var linha = document.createElement("div");
          linha.className = "pais";
          var nome = NOMES_ORIG[o.origem] || ("🌐 " + o.origem);
          linha.innerHTML = '<span class="nome">' + nome + '</span><span class="faixa"><span style="width:' + Math.max(3, Math.round(o.visitas / max * 100)) + '%"></span></span><span class="pct">' + o.visitas + '</span>';
          alvo.appendChild(linha);
        });
      }
      encherOrigens(j.porPagina && j.porPagina.origens);
      document.getElementById("rot-periodo").textContent = "Nos últimos " + diasAtual + " dias";
      encherPgs("pgs-hoje", j.porPagina && j.porPagina.hoje);
      encherPgs("pgs-periodo", j.porPagina && j.porPagina.periodo);
      var zp = document.getElementById("paises");
      zp.innerHTML = "";
      var ps = j.paises || [];
      var totPed = 0; ps.forEach(function (p) { totPed += p.pedidos; });
      var nomes;
      try { nomes = new Intl.DisplayNames(["pt"], { type: "region" }); } catch (e) { nomes = null; }
      if (!ps.length) zp.innerHTML = '<div style="text-align:center;color:oklch(0.75 0.03 275);font-size:0.85rem">sem dados de países neste período</div>';
      ps.forEach(function (p) {
        var cod = p.codigo || "";
        var bandeira = cod.length === 2 ? String.fromCodePoint(127397 + cod.charCodeAt(0), 127397 + cod.charCodeAt(1)) : "🌐";
        var nome = cod; try { if (nomes) nome = nomes.of(cod) || cod; } catch (e) {}
        var pct = totPed ? Math.round(p.pedidos / totPed * 100) : 0;
        var linha = document.createElement("div");
        linha.className = "pais";
        linha.innerHTML = '<span class="nome">' + bandeira + " " + nome + '</span><span class="faixa"><span style="width:' + Math.max(2, pct) + '%"></span></span><span class="pct">' + pct + '%</span>';
        zp.appendChild(linha);
      });
    })
    .catch(function () { document.getElementById("msg-erro").textContent = "⚠️ Não foi possível carregar."; });
}
document.getElementById("entrar").addEventListener("click", carregar);
document.getElementById("chave").addEventListener("keydown", function (e) { if (e.key === "Enter") carregar(); });
document.querySelectorAll(".filtros button").forEach(function (b) {
  b.addEventListener("click", function () {
    document.querySelectorAll(".filtros button").forEach(function (x) { x.classList.remove("ativo"); });
    b.classList.add("ativo");
    diasAtual = Number(b.dataset.d);
    carregar();
  });
});
if (localStorage.getItem("stats_chave")) { document.getElementById("chave").value = localStorage.getItem("stats_chave"); carregar(); }
</script>
</body>
</html>`;
