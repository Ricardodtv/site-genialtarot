import { DurableObject } from "cloudflare:workers";
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
  // 21/10/2026: a Calculadora de Ascendente (ascendente.html) também é uma captura
  if (type === "ascendente") {
    return [
      "✨ NOVA CALCULADORA DE ASCENDENTE — Genialtarot",
      "",
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)}`,
      d.phone ? `📱 WhatsApp: ${clean(d.phone, 40)}` : null,
      `🎂 Nascimento: ${clean(d.date_of_birth)} às ${clean(d.birth_time, 20)}`,
      `📍 ${clean(d.city)}, ${clean(d.country)}`,
      "",
      `🔭 ${clean(d.verdict, 600)}`,
    ].filter((l) => l !== null).join("\n");
  }
  // 21/10/2026: pedido do Mapa do Amor completo (mapa-amor.html). Semi-automático:
  // ele confirma o pagamento e só depois diz «envia».
  if (type === "mapa-amor-pedido") {
    const como = { cartao: "💳 Cartão (myPOS)", mbway: "📱 MB WAY", pix: "🇧🇷 PIX" }[d.metodo] || clean(d.metodo, 20);
    return [
      `💗 PEDIDO MAPA DO AMOR ${clean(d.pedido, 20)} — Genialtarot`,
      "",
      `${como} · ${clean(d.valor, 20)}`,
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)}`,
      `🎂 Nascimento: ${clean(d.date_of_birth)} às ${clean(d.birth_time, 20)}`,
      `📍 ${clean(d.city)}, ${clean(d.country)}`,
      `♀ ${clean(d.venus, 60)} · ♂ ${clean(d.marte, 60)}`,
      ...(d.promo === "halloween" ? ["", "🎃 HALLOWEEN: leva também o MAPA ASTRAL completo de OFERTA"] : []),
      "",
      "⏳ Confirma se o pagamento entrou e diz «envia» — só então segue o mapa completo.",
    ].join("\n");
  }
  // 21/10/2026: pedido do Mapa Astral completo (mapa-astral.html) — o mesmo fluxo do Mapa do Amor.
  if (type === "mapa-astral-pedido") {
    const como = { cartao: "💳 Cartão (myPOS)", mbway: "📱 MB WAY", pix: "🇧🇷 PIX (pelo WhatsApp)" }[d.metodo] || clean(d.metodo, 20);
    return [
      `✨ PEDIDO MAPA ASTRAL ${clean(d.pedido, 20)} — Genialtarot`,
      "",
      `${como} · ${clean(d.valor, 40)}`,
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)}`,
      `🎂 Nascimento: ${clean(d.date_of_birth)} às ${clean(d.birth_time, 20)}`,
      `📍 ${clean(d.city)}, ${clean(d.country)}`,
      `☉ ${clean(d.sol, 60)} · ☽ ${clean(d.lua, 60)} · ↑ ${clean(d.asc, 60)}`,
      "",
      "⏳ Confirma se o pagamento entrou e diz «envia» — só então segue o mapa completo.",
    ].join("\n");
  }
  // 29/10/2026: entrada na Lista VIP (vip.html) — é uma CAPTURA com «Novidades: sim»
  if (type === "vip") {
    return [
      "👑 NOVO MEMBRO DA LISTA VIP — Genialtarot",
      "",
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)} · 📬 aceita novidades`,
      `🎂 Nascimento: ${clean(d.date_of_birth)}`,
    ].join("\n");
  }
  // 21/10/2026: amostra grátis de um mapa (Mapa do Amor, Mapa Astral, Ano 2027) — é uma CAPTURA (cria/acrescenta ficha)
  if (type === "mapa-captura") {
    return [
      `🌟 NOVA AMOSTRA — ${clean(d.area, 80)} — Genialtarot`,
      "",
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)}${d.novidades ? " · 📬 aceita novidades" : ""}`,
      d.phone ? `📱 WhatsApp: ${clean(d.phone, 40)}` : null,
      `🎂 Nascimento: ${clean(d.date_of_birth)}${d.birth_time ? " às " + clean(d.birth_time, 20) : ""}`,
      d.city ? `📍 ${clean(d.city)}, ${clean(d.country)}` : null,
      "",
      `🔭 ${clean(d.verdict, 600)}`,
    ].filter((l) => l !== null).join("\n");
  }
  // 21/10/2026: pedido do Ano 2027 (Numerologia) completo — o mesmo fluxo dos outros mapas.
  if (type === "numerologia-pedido") {
    const como = { cartao: "💳 Cartão (myPOS)", mbway: "📱 MB WAY", pix: "🇧🇷 PIX (pelo WhatsApp)" }[d.metodo] || clean(d.metodo, 20);
    return [
      `🔢 PEDIDO ANO 2027 ${clean(d.pedido, 20)} — Genialtarot`,
      "",
      `${como} · ${clean(d.valor, 40)}`,
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)}`,
      `🎂 Nascimento: ${clean(d.date_of_birth)}`,
      `🔢 Ano Pessoal ${clean(String(d.ano_pessoal ?? ""), 4)} · Caminho de Vida ${clean(String(d.caminho ?? ""), 4)}`,
      "",
      "⏳ Confirma se o pagamento entrou e diz «envia» — só então segue o Ano 2027 completo.",
    ].join("\n");
  }
  // 27/10/2026: pedido do Tarot Semestral (tarot-semestral.html) — o mesmo fluxo dos mapas; a Comentada leva áudio dele.
  if (type === "semestral-pedido") {
    const como = { cartao: "💳 Cartão (myPOS)", mbway: "📱 MB WAY", pix: "🇧🇷 PIX" }[d.metodo] || clean(d.metodo, 20);
    const comentada = d.plano === "comentada";
    return [
      `🃏 PEDIDO TAROT SEMESTRAL ${clean(d.pedido, 20)} — Genialtarot`,
      "",
      `${comentada ? "🎧 COMENTADA PELO MESTRE" : "📜 Leitura Completa"} · ${como} · ${clean(d.valor, 40)}${d.presente ? " · 🎁 presente" : ""}`,
      `👤 Nome: ${clean(d.name)}`,
      `📧 Email: ${clean(d.email)}`,
      d.phone ? `📱 WhatsApp: ${clean(d.phone, 40)}` : null,
      `🎂 Nascimento: ${clean(d.date_of_birth)}`,
      `📅 Período: ${clean(d.periodo, 60)}`,
      `🃏 Síntese: ${clean(d.sintese, 60)}`,
      comentada && d.pergunta ? `❓ Pergunta: ${clean(d.pergunta, 500)}` : null,
      "",
      comentada ? "⏳ Confirma o pagamento e diz «envia» — segue o PDF; o áudio de ~10 min é teu, pelo WhatsApp, em 48 h."
                : "⏳ Confirma se o pagamento entrou e diz «envia» — só então segue a leitura completa.",
    ].filter((l) => l !== null).join("\n");
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
  // 04/11/2026 (pedido dele): QUALQUER formulário do site chega aos avisos — também os que vierem a ser criados.
  // Um tipo que ainda não tem mensagem própria sai com todos os campos que trouxe (se trouxer uma pessoa).
  if (d && typeof d === "object" && (d.name || d.email || d.phone)) {
    const linhas = Object.entries(d).filter(([, v]) => v !== null && v !== undefined && v !== "" && typeof v !== "object").slice(0, 20)
      .map(([k, v]) => `• ${clean(k, 30)}: ${clean(String(v), 300)}`);
    return [`📝 FORMULÁRIO DO SITE — ${clean(d.area || type, 80)}`, "", ...linhas].join("\n");
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

// 🛟 12/11/2026: a quota da API do YouTube esgotou-se (quotaExceeded, 403) e os botões dos signos no /horoscopo
// morreram até à meia-noite do Pacífico. Agora cada resultado bom fica guardado no KV (só se mudou, para não gastar
// escritas); quando o YouTube falha, serve-se o último bom em vez de nada. Um vídeo de ontem é melhor que botões mortos.
async function comReserva(env, nome, fn) {
  const chave = "reserva-video:" + nome;
  let data = null;
  try { data = await fn(); } catch (e) { data = null; }
  try {
    if (data) {
      const novo = JSON.stringify(data);
      const velho = await env.CAPTURAS.get(chave);
      if (velho !== novo) await env.CAPTURAS.put(chave, novo);
      return data;
    }
    const guardado = await env.CAPTURAS.get(chave);
    if (guardado) return { ...JSON.parse(guardado), reserva: true };
  } catch (e) { /* o KV nunca pode derrubar a rota */ }
  return data;
}

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

// ===== Contador de visitas, do lado do servidor =====
//
// 08/09/2026. O contador da Cloudflare (Web Analytics) morreu e nao ha como o
// reparar daqui. Medido hoje com o Chromium sem ecra e o registo de rede: o
// beacon carrega, dispara um POST de 812 bytes para
// https://cloudflareinsights.com/cdn-cgi/rum, e a Cloudflare responde 404.
// Tirar o beacon manual de uma pagina tambem nao trouxe de volta a injeccao
// automatica (10 leituras em 5 minutos, nenhuma). Zero visitas desde 22/08.
//
// Este conta AQUI, antes de entregar a pagina:
//   - nao depende de JavaScript, nenhum bloqueador o apanha
//   - sem amostragem: conta todas, nao 1 em 10
//   - da o REFERRER, que e o que responde a "aquele video trouxe gente?"
//   - separa pessoas de robos, que os numeros da zona misturam
//
// 🔒 NAO guarda nada que identifique ninguem: sem IP, sem cookies, sem seguir
// a pessoa de pagina em pagina. So a hora, a pagina, o dominio de onde veio,
// o pais e o tipo de aparelho. A politica de privacidade do site continua
// verdadeira.
//
// 🚨 Contar NUNCA pode derrubar o site: tudo dentro de try/catch e a escrita
// vai por ctx.waitUntil, depois da resposta seguir.

const ROBOS = /google-safety|googleother|google-inspectiontool|google-extended|mediapartners-google|adsbot|apis-google|google-read-aloud|bot\b|bot\/|crawl|spider|slurp|preview|facebookexternalhit|whatsapp|telegram|headless|python-requests|curl\/|wget|scrapy|semrush|ahrefs|mj12|dotbot|petalbot|yandex|baidu|applebot|gptbot|claudebot|ccbot|bytespider|feedfetcher|monitoring|uptime|pingdom|lighthouse/i;

// 01/11/2026 (ele: «separa também os países e as páginas — sem bloquear nada»): os robôs disfarçados de navegador
// normal (o «/» com 1700 entradas, os EUA à frente de Portugal) vêm de SERVIDORES ALUGADOS, não de casas. A Cloudflare
// diz a rede de onde vem cada pedido (cf.asn / cf.asOrganization); rede de servidores = robô. Ninguém é bloqueado:
// só muda a gaveta (blob5). O blob7 guarda o NOME da rede só quando é de servidores (nunca o fornecedor de casa
// de uma pessoa), para se poder conferir quem é quem.
const ASN_SERVIDORES = new Set([32934, 15169, 396982, 19527, 16509, 14618, 8075, 8068, 14061, 16276, 24940, 63949, 20473, 51167,
  132203, 45090, 45102, 37963, 136907, 55990, 31898, 9009, 212238, 60068, 62240, 202425, 12876, 16125, 47583,
  36352, 40021, 397423, 21859, 199524, 35540, 3223, 49453, 211252, 7941, 29802, 46606, 26496, 398324, 22612, 53667]);
const ORG_SERVIDORES = /hosting|cloud|server|data ?cent|datacamp|vps|colocat|amazon|google|microsoft|digitalocean|ovh|hetzner|linode|vultr|choopa|contabo|tencent|alibaba|huawei|oracle|m247|leaseweb|scaleway|ionos|hostinger|godaddy|facebook|meta platforms|gcore|stark industries|clouvider|ponynet|frantech|psychz|quadranet|hostwinds|colocrossing/i;
// ⚠️ Cloudflare, Akamai e Fastly NÃO entram: é por elas que passam pessoas reais (Relay Privado do iCloud nos
// iPhones, a app 1.1.1.1/WARP). Contá-las como robô apagava gente de verdade.
const ORG_PESSOAS = /cloudflare|akamai|fastly|apple/i;
function servidorAlugado(cf) {
  if (!cf) return "";
  const org = String(cf.asOrganization || "");
  if ([13335, 209242, 20940, 16625, 54113, 714, 6185].includes(Number(cf.asn)) || ORG_PESSOAS.test(org)) return "";
  return (ASN_SERVIDORES.has(Number(cf.asn)) || ORG_SERVIDORES.test(org)) ? (org || "AS" + cf.asn).slice(0, 60) : "";
}
function quemE(ua, cf) { return ROBOS.test(ua) || servidorAlugado(cf) ? "robo" : "pessoa"; }

function aparelhoDe(ua) {
  if (!ua) return "?";
  if (/ipad|tablet/i.test(ua)) return "tablet";
  if (/mobi|android|iphone|ipod/i.test(ua)) return "telemovel";
  return "computador";
}

// So o dominio de onde veio -- nunca o endereco completo, que pode levar
// termos de pesquisa ou dados da pessoa.
function origemDe(referer, proprio) {
  if (!referer) return "(directo)";
  try {
    const h = new URL(referer).hostname.replace(/^www\./, "");
    if (h === proprio || h.endsWith("." + proprio)) return "(interno)";
    return h;
  } catch (e) { return "(desconhecido)"; }
}

// 🚨 08/09/2026 -- A MARCA NO LINK. O referrer nao chega para saber quem veio
// do TikTok: quem abre o link dentro da aplicacao cai no navegador interno
// dela, que muitas vezes NAO diz de onde veio. Essas visitas iam parar a
// "(directo)", misturadas com quem escreveu o endereco a mao.
//
// Com uma marca no proprio link -- genialtarot.com/?de=tiktok -- a origem
// deixa de depender da boa vontade do navegador. A pagina abre na mesma;
// ninguem nota nada.
//
// So entram as marcas desta lista. Sem ela, qualquer pessoa escrevia o que
// lhe apetecesse nas estatisticas dele so por abrir o site com ?de=<lixo>.
const MARCAS = new Set(["tiktok", "youtube", "instagram", "facebook", "fb-grupo", "whatsapp",
                        "telegram", "email", "cartao", "bio",
                        "maps",
                        "noticias", "partilha"]);   // 13/11/2026 O-403 (OK dele): ?de=noticias (Notícias do dia) e ?de=partilha (53 ligações) caíam em «marca:?»   // 04/11/2026: as ligações do Google Maps (ficha, publicações, produtos) já usavam ?de=maps

// 01/11/2026 (ele: «passo 1 — trazer o público do canal para o site»): além da marca (?de=youtube), a ligação pode
// levar o CÓDIGO da peça (?c=fds-touro-0111), para se saber QUE vídeo trouxe quem. Fica «marca:youtube/fds-touro-0111».
// Só letras, números e hífen — nada que identifique a pessoa.
function marcaTexto(de, c) {
  const m = String(de || "").toLowerCase().slice(0, 20);
  if (!m) return null;
  // Uma marca desconhecida e' quase sempre um engano a escrever o link.
  // Aparece assim, para dar nas vistas, em vez de se perder em silencio.
  if (!MARCAS.has(m)) return /^[a-z0-9-]{1,20}$/.test(m) ? "marca:?" : null;
  const k = String(c || "").toLowerCase();
  return "marca:" + m + (/^[a-z0-9-]{1,40}$/.test(k) ? "/" + k : "");
}
function marcaDe(url) {
  return marcaTexto(url.searchParams.get("de") || url.searchParams.get("utm_source"),
                    url.searchParams.get("c") || url.searchParams.get("utm_campaign"));
}
// A origem que o vivo.js manda: a marca da ligação manda; o referrer so entra quando ela nao existe.
function origemVivo(d) {
  return (d.marca && marcaTexto(d.marca, d.c)) || origemDe(d.origem ? "https://" + String(d.origem) : "", "genialtarot.com");
}

// 🚨 09/09/2026 — AS PAGINAS QUE EXISTEM MESMO. O crivo anterior aceitava
// tudo o que TIVESSE FEITIO de pagina (um troco em minusculas sem ponto), e a
// prova de que nao chegava veio da propria lista das mais visitadas:
// /settings, /login, /signup, /checkout, /pricing e /aws-credentials --
// varrimentos a procura de falhas e de chaves, contados um a um como PESSOAS.
// Era isso que enchia o site de "visitantes" dos Estados Unidos, de Singapura
// e dos Paises Baixos, quando o publico do canal e' 78% Brasil e 21% Portugal.
//
// ⚠️ ESTA LISTA E' GEMEA DO run_worker_first do wrangler.jsonc. Pagina nova
// entra nos DOIS sitios: no wrangler para o worker correr nela, e aqui para
// ela contar. Se so entrar num, ou nao conta ou nem chega ca.
const PAGINAS = new Set([
  "/", "/index", "/anual", "/arcanos", "/arvore", "/fimdesemana", "/horoscopo",
  "/ascendente", "/loja", "/loja-brasil", "/loja-portugal", "/ir-loja", "/lua", "/mapa-amor", "/mapa-astral", "/numerologia-2027", "/pagar", "/privacidade", "/sobre", "/tarot-gratis", "/termos", "/vip",
  "/arcano-00-o-louco", "/arcano-01-o-mago", "/arcano-02-a-sacerdotisa",
  "/arcano-03-a-imperatriz", "/arcano-04-o-imperador", "/arcano-05-o-hierofante",
  "/arcano-06-os-enamorados", "/arcano-07-o-carro", "/arcano-08-a-forca",
  "/arcano-09-o-eremita", "/arcano-10-a-roda-da-fortuna", "/arcano-11-a-justica",
  "/arcano-12-o-enforcado", "/arcano-13-a-morte", "/arcano-14-a-temperanca",
  "/arcano-15-o-diabo", "/arcano-16-a-torre", "/arcano-17-a-estrela",
  "/arcano-18-a-lua", "/arcano-19-o-sol", "/arcano-20-o-julgamento",
  "/arcano-21-o-mundo",
  // 25/10/2026: as 5 novidades inspiradas no Astro.com
  "/aniversarios", "/amor-do-dia", "/ceu-de-hoje", "/compatibilidade", "/noticias-do-ceu",
  // 25/10/2026: o Horóscopo do Dia
  "/horoscopo-do-dia",
  // 27/10/2026: o Tarot Semestral
  "/tarot-semestral",
  // 28/10/2026: as Novidades (10 páginas em experiência, ideias do astro-seek.com) e a montra delas
  "/novidades", "/revolucao-solar", "/horoscopo-pessoal", "/carta-de-tarot", "/retrogrados", "/trio-astral", "/calendarios", "/horoscopo-chines", "/fase-lua-nascimento", "/adivinha-signo", "/mapa-do-casal",
  // 28/10/2026: o Oráculo das Cores (ideia do astro.com, textos originais)
  "/oraculo-cores", "/efemerides", "/famosos-ceu",
  // 02/11/2026: as pesquisas que o Google Trends mostrou e o site não tinha (horóscopo semanal e de amanhã, tarot cigano, …)
  "/horoscopo-semanal", "/horoscopo-de-amanha", "/tarot-cigano", "/consulta-de-tarot-online", "/datas-dos-signos", "/signos-que-combinam", "/cor-do-ano-2027", "/alinhamento-dos-planetas", "/astrologia-vedica", "/signos-2026", "/melhores-signos-2027", "/astrologia", "/lua-azul", "/tiragem-templo-de-afrodite", "/combinacoes-de-tarot",
  // 03/11/2026: mais 5 pesquisas a subir no Google Trends
  "/tarot-dos-gatos", "/stellium-astrologia", "/astrologia-horaria", "/astrologia-sideral", "/astrologia-sistemica",
  "/tarot-rider-waite", "/tarot-com-inteligencia-artificial",
  // 03/11/2026: os grandes trânsitos lentos (gerar-transitos.py) e 3 páginas de serviço por público
  "/transitos-lentos", "/neptuno-em-carneiro", "/saturno-em-carneiro", "/plutao-em-aquario", "/urano-em-gemeos", "/jupiter-em-leao", "/jupiter-em-virgem", "/nodos-lunares-aquario-leao", "/saturno-e-urano-2032", "/consulta-tarot-casal", "/tarot-para-decisoes", "/tarot-para-emigrantes",
  // 04/11/2026: Escolha um Monte (muda às segundas; as semanas passadas ficam em /escolha-um-monte-<d>-<mês>-<ano>, contadas pelo vivo.js)
  "/escolha-um-monte",
  // 04/11/2026: guia grátis para aprender astrologia (pesquisa «curso astrologia» a subir; NÃO é curso)
  "/aprender-astrologia",
  // 04/11/2026: Astrocartografia (o mapa astral no mapa-mundo; «mapa cartografico astrologia» +6050 % no Brasil)
  "/astrocartografia",
  // 04/11/2026: área de Hipnose (consultas de hipnoterapia; rascunho à espera do OK dele)
  "/hipnose",
  // 04/11/2026: Notícias do dia (2 por dia, ~/noticias-site/gerar.py); os artigos /noticias/<data>-manha|tarde contam pelo vivo.js
  "/noticias",
  // 04/11/2026 (R-122, ideias da análise de paulocardoso.com): página do Curso de Tarot e «Na imprensa»
  "/curso-de-tarot", "/na-imprensa",
  // 04/11/2026 (ideia dele): a comunidade dos 12 grupos de signos, com os membros contados
  "/comunidade",
  // 12/11/2026 (análise da concorrência «Cartas da Maya»): consulta de tarot com preços, canais oficiais, tarot terapêutico e autoconhecimento,
  // e o horóscopo semanal de cada signo (horoscopo-semanal-signos.py, renova às segundas)
  "/consulta-de-tarot", "/canais-oficiais", "/tarot-terapeutico", "/tarot-e-autoconhecimento", "/horoscopo-semanal-carneiro", "/horoscopo-semanal-touro", "/horoscopo-semanal-gemeos", "/horoscopo-semanal-caranguejo", "/horoscopo-semanal-leao", "/horoscopo-semanal-virgem", "/horoscopo-semanal-balanca", "/horoscopo-semanal-escorpiao", "/horoscopo-semanal-sagitario", "/horoscopo-semanal-capricornio", "/horoscopo-semanal-aquario", "/horoscopo-semanal-peixes",
  // 13/11/2026: o horóscopo de amanhã de cada signo (o worker escreve o dia a partir do horoscopo-dia/<amanhã>.json)
  "/horoscopo-de-amanha/carneiro", "/horoscopo-de-amanha/touro", "/horoscopo-de-amanha/gemeos", "/horoscopo-de-amanha/caranguejo", "/horoscopo-de-amanha/leao", "/horoscopo-de-amanha/virgem", "/horoscopo-de-amanha/balanca", "/horoscopo-de-amanha/escorpiao", "/horoscopo-de-amanha/sagitario", "/horoscopo-de-amanha/capricornio", "/horoscopo-de-amanha/aquario", "/horoscopo-de-amanha/peixes",
]);

function contarVisita(request, url, env, ctx) {
  try {
    if (!env || !env.VISITAS || !ctx) return;
    if (request.method !== "GET") return;
    // 🚨 08/09/2026, apanhado nas primeiras horas de dados: o worker tambem
    // corre em tudo o que NAO tem ficheiro (as paginas com ficheiro estao na
    // lista run_worker_first; imagens e CSS nunca chegam ca). Entraram como
    // "pessoas" um pedido de certificado (/.well-known/acme-challenge/<token>)
    // e varrimentos de ataque -- /wp-login.php, /wp-json/, /.git/config.
    //
    // Em vez de uma lista negra que nunca acaba, so se conta o que TEM FEITIO
    // DE PAGINA deste site: a raiz, ou um unico troco em minusculas sem ponto
    // (/horoscopo, /tarot-gratis, /arcano-00-o-louco). Tudo o que traz ponto,
    // maiuscula ou segunda barra nao e' pagina daqui.
    //
    // ⚠️ 09/09: o crivo passou de "tem feitio de pagina" para "E' UMA pagina",
    // depois de /aws-credentials, /login e /checkout aparecerem no topo das
    // mais visitadas. Pagina nova entra na lista PAGINAS la em cima.
    if (!PAGINAS.has(url.pathname)) return;
    const ua = request.headers.get("user-agent") || "";
    const proprio = url.hostname.replace(/^www\./, "");
    const ponto = {
      indexes: [url.pathname.slice(0, 90)],
      blobs: [
        url.pathname.slice(0, 120),
        // A marca do link manda; o referrer so entra quando ela nao existe.
        (marcaDe(url) || origemDe(request.headers.get("referer"), proprio)).slice(0, 120),
        (request.cf && request.cf.country) || "?",
        aparelhoDe(ua),
        quemE(ua, request.cf),
        "",
        servidorAlugado(request.cf),
      ],
      doubles: [1],
    };
    ctx.waitUntil((async () => {
      try { env.VISITAS.writeDataPoint(ponto); } catch (e) { /* silencio */ }
    })());
  } catch (e) { /* contar nunca pode derrubar a pagina */ }
}

// Le o que foi contado. Usa o CF_RUM_TOKEN (Account Analytics:Read), que ja
// existe nos segredos. Cada consulta vai a parte: um erro numa nao deita as
// outras abaixo -- a licao das consultas do RUM, 22/08.
async function perguntarSQL(env, sql) {
  const r = await fetch(
    "https://api.cloudflare.com/client/v4/accounts/" + RUM_CONTA + "/analytics_engine/sql",
    { method: "POST",
      headers: { "Authorization": "Bearer " + env.CF_RUM_TOKEN, "Content-Type": "text/plain" },
      body: sql });
  const t = await r.text();
  try {
    const j = JSON.parse(t);
    return Array.isArray(j.data) ? j.data : { erro: String(t).slice(0, 200) };
  } catch (e) { return { erro: String(t).slice(0, 200) }; }
}

async function estatisticasVisitas(env, dias) {
  if (!env.CF_RUM_TOKEN) return { erro: "falta o CF_RUM_TOKEN" };
  const janela = "timestamp > now() - INTERVAL '" + Math.min(90, Math.max(1, dias)) + "' DAY";
  // 🚨 O mesmo crivo do contarVisita, mas para o que JA ESTA GRAVADO: pedidos
  // de certificado e varrimentos de ataque (/wp-login.php, /.git/config,
  // /wp-json/) entraram antes de o contador aprender a ignora-los. Um ponto
  // ou uma segunda barra chegam para os apanhar a todos.
  //
  // ⚠️ Vai em TODAS as consultas, incluindo a dos dias. Da primeira vez tirei
  // o lixo so da lista de paginas e ficaram 23 no total contra 10 na lista --
  // numeros que nao batem certo tiram a credibilidade a todos os outros.
  // 09/09: passou de lista negra (sem pontos, sem segunda barra) para a LISTA
  // DAS PAGINAS QUE EXISTEM. Assim os dias ja gravados ficam limpos tambem --
  // senao os /aws-credentials e /login de ontem continuavam a contar como
  // pessoas na pagina, mesmo depois de o contador deixar de os gravar.
  // 01/11/2026: mais as páginas novas do SEO, que entram pelo sinal do vivo.js (blob6 = 'vivo'; o worker só as grava
  // se tiverem feitio de página deste site e vierem de genialtarot.com).
  // 01/11/2026 (ele): blob6 = 'js' é a CONFIRMAÇÃO do vivo.js de uma página da lista — não é visita nova, fica fora destas contas.
  const limpo = " AND blob6 != 'js' AND (blob1 IN (" +
    Array.from(PAGINAS).map(p => "'" + p + "'").join(",") + ") OR blob6 = 'vivo')";
  // 01/11/2026 (ele: «as métricas devem ser só das pessoas, assim são realistas»): antes de 01/11 11:27 (UTC = hora
  // de Lisboa em Novembro) os robôs disfarçados de servidores alugados gravavam-se como «pessoa» e não há como os
  // separar agora (não se guardava a rede). Por isso as contas de PESSOAS só começam aí — os dados antigos não se
  // apagam (ficam no Analytics Engine), só não entram nas contas.
  // 01/11 (ele): começa às 11:37 e não às 11:27 para deixar de fora a visita de teste do Claude (11:35, /lua); entre 11:27 e 11:37 só houve essa e as da China.
  const desdeLimpo = " AND timestamp >= toDateTime('2026-11-01 12:12:00')";
  // 01/11/2026 (ele: «tira os que vêm da China, são robôs, não tenho clientes lá»; e depois Hong Kong, Singapura e Coreia do Sul): países sem clientes não contam
  // como pessoas. Só se tira das contas — ninguém é bloqueado.
  const foraPaises = " AND blob3 NOT IN ('CN','HK','SG','KR')";
  // 01/11/2026 12:12 (UTC): PESSOA = só a visita CONFIRMADA pelo vivo.js (blob6 = 'humano': mexeu ou ficou 8 s à vista).
  // A entrada servida pelo worker, sozinha, já não prova nada — o Google-Safety corria a página e saía em 0 s.
  const so = " AND blob5 = 'pessoa' AND blob6 = 'humano'" + desdeLimpo + foraPaises;
  const consultas = {
    dias:     "SELECT toDate(timestamp) AS dia, blob5 AS quem, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + " AND ((blob5 != 'pessoa'" + limpo + ") OR (blob5 = 'pessoa' AND blob6 = 'humano'" + desdeLimpo + foraPaises + ")) GROUP BY dia, quem ORDER BY dia ASC",
    origens:  "SELECT blob2 AS nome, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + so + " GROUP BY nome ORDER BY n DESC LIMIT 20",
    paginas:  "SELECT blob1 AS nome, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + so + " GROUP BY nome ORDER BY n DESC LIMIT 40",
    paises:   "SELECT blob3 AS nome, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + so + " GROUP BY nome ORDER BY n DESC LIMIT 15",
    confirmadas: "SELECT toDate(timestamp) AS dia, blob6 AS tipo, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + " AND blob5 = 'pessoa' AND blob3 NOT IN ('CN','HK','SG','KR') AND blob6 IN ('js','vivo') GROUP BY dia, tipo ORDER BY dia ASC",
    // 01/11/2026 (ele): pessoas vindas do Google, por página de entrada — para a divisão SEO do painel
    // 01/11 (ele: «o mais fiel possível»): «google» só conta quem CONFIRMOU ser navegador a sério (o vivo.js correu); o «google_bruto»
    // é o que diz vir do Google à entrada — inclui robôs que fingem vir de lá (20 em 2 dias contra 1 visto no painel ao vivo).
    google:   "SELECT blob1 AS nome, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + " AND blob5 = 'pessoa' AND blob3 NOT IN ('CN','HK','SG','KR') AND blob6 = 'humano' AND blob2 IN ('google.com','google.pt','google.com.br','com.google.android.googlequicksearchbox') GROUP BY nome ORDER BY n DESC LIMIT 200",
    google_bruto: "SELECT blob1 AS nome, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + so + " AND blob2 IN ('google.com','google.pt','google.com.br','com.google.android.googlequicksearchbox') GROUP BY nome ORDER BY n DESC LIMIT 200",
    aparelhos:"SELECT blob4 AS nome, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + so + " GROUP BY nome ORDER BY n DESC LIMIT 5",
  };
  // 01/11/2026 19:45 (ele: «44 nas pessoas por dia e 7 pessoas hoje em cima?»): o sum() contava PÁGINAS vistas. Agora cada
  // pessoa (sid do vivo.js, blob8) conta uma vez por dia/país/origem/aparelho; as linhas antigas, sem sid, contam como antes.
  const comSid = so + " AND blob8 != ''", semSid = so + " AND blob8 = ''";
  for (const [k, campo] of [["dias", "toDate(timestamp)"], ["origens", "blob2"], ["paises", "blob3"], ["aparelhos", "blob4"]]) {
    consultas["u_" + k] = "SELECT " + campo + " AS nome, count(DISTINCT blob8) AS n FROM visitas_site WHERE " + janela + comSid + " GROUP BY nome";
    consultas["r_" + k] = "SELECT " + campo + " AS nome, sum(_sample_interval) AS n FROM visitas_site WHERE " + janela + semSid + " GROUP BY nome";
  }
  const nomes = Object.keys(consultas);
  const res = await Promise.all(nomes.map(k =>
    perguntarSQL(env, consultas[k]).catch(e => ({ erro: String(e).slice(0, 120) }))));
  const fora = {};
  nomes.forEach((k, i) => { fora[k] = res[i]; });
  const junta = (k) => { const m = {}; for (const x of [].concat(Array.isArray(fora["u_" + k]) ? fora["u_" + k] : [], Array.isArray(fora["r_" + k]) ? fora["r_" + k] : []))
    m[x.nome] = (m[x.nome] || 0) + Number(x.n || 0); delete fora["u_" + k]; delete fora["r_" + k];
    return Object.entries(m).map(([nome, n]) => ({ nome, n })).sort((a, b) => b.n - a.n); };
  try {
    for (const k of ["origens", "paises", "aparelhos"]) { const l = junta(k); if (l.length || Array.isArray(fora[k])) fora[k] = l; }
    const pd = junta("dias");   // as pessoas por dia substituem a linha «pessoa» (as dos robôs ficam como estão)
    if (Array.isArray(fora.dias)) fora.dias = fora.dias.filter((x) => x.quem !== "pessoa").concat(pd.map((x) => ({ dia: x.nome, quem: "pessoa", n: x.n })))
      .sort((a, b) => String(a.dia).localeCompare(String(b.dia)));
  } catch (e) { /* se falhar, ficam os números antigos */ }
  return fora;
}

import REDIR_ANTIGAS from "./redirecoes-antigas.js";

// 07/11/2026 (pedido dele, SEO): o horóscopo do dia já vem no HTML, para o Google e para as IAs que não correm
// JavaScript. Texto do mesmo horoscopo-dia/AAAA-MM-DD.json, dia e horas de Portugal; o JavaScript da página redesenha
// por cima, com o fuso e os nomes escolhidos. Sem JSON fica a página de sempre.
const H_NOMES = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"];
const H_SLUGS = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"];
const H_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
const H_SEMANA = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"];
const hEsc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const hHora = (ms) => new Intl.DateTimeFormat("pt-PT", { timeZone: "Europe/Lisbon", hour: "2-digit", minute: "2-digit" }).format(new Date(ms));
const hDw = (ms) => { const d = new Date(new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon" }).format(new Date(ms)) + "T12:00:00Z"); return d.getUTCDay(); };
const hPor = (t) => hEsc(t).replace(/\{S:(\d+)\}/g, (_, n) => H_NOMES[+n]).replace(/\{H:(\d+)\}/g, (_, ms) => hHora(+ms))
  .replace(/\{D:(\d+)\}/g, (_, ms) => { const w = hDw(+ms); return (w === 0 || w === 6 ? "no " : "na ") + H_SEMANA[w]; }).replace(/\{W:(\d+)\}/g, (_, ms) => H_SEMANA[hDw(+ms)]);
function horoscopoNoHtmlAlvo(url) {
  if (url.pathname === "/horoscopo-do-dia") return -1;
  if (url.pathname === "/horoscopo-de-amanha") return -3;
  if (url.pathname === "/horoscopo-semanal") return -4;
  const m = url.pathname.match(/^\/signo\/([a-z]+)$/);
  const i = m ? H_SLUGS.indexOf(m[1]) : -2;
  return i >= 0 ? i : -2;
}
async function horoscopoNoHtml(url, env, alvo) {
  // sem If-None-Match: o ficheiro estático não muda, mas o que sai daqui muda todos os dias (senão a resposta seria um 304 velho)
  const resp = await env.ASSETS.fetch(new Request(url.toString(), { method: "GET" }));
  if (!resp.ok || !(resp.headers.get("content-type") || "").includes("text/html")) return resp;
  const hoje = new Date(new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon" }).format(new Date()) + "T12:00:00Z");
  const semana_ = alvo === -4;
  const base = new Date(hoje);
  if (alvo === -3) base.setUTCDate(base.getUTCDate() + 1);
  if (semana_) base.setUTCDate(base.getUTCDate() - ((base.getUTCDay() + 6) % 7));
  const iso = base.toISOString().slice(0, 10);
  let x = null;
  try {
    const j = await env.ASSETS.fetch(new Request(new URL(`/horoscopo-${semana_ ? "semana" : "dia"}/${iso}.json`, url), { method: "GET" }));
    if (j.ok) x = await j.json();
  } catch (e) { x = null; }
  if (!x || !Array.isArray(x.s) || x.s.length !== 12) return resp;
  const fd = (d) => `${d.getUTCDate()} de ${H_MESES[d.getUTCMonth()]}`;
  const dia = fd(base), semana = H_SEMANA[base.getUTCDay()], fim = new Date(base); fim.setUTCDate(fim.getUTCDate() + 6);
  const nome = alvo === -1 ? `Horóscopo do Dia, ${dia}` : alvo === -3 ? `Horóscopo de Amanhã, ${dia}` : semana_ ? `Horóscopo Semanal, ${dia} a ${fd(fim)}` : `Horóscopo de ${H_NOMES[alvo]}, ${dia}`;
  const ld = JSON.stringify({ "@context": "https://schema.org", "@type": "WebPage", url: url.origin + url.pathname, inLanguage: "pt", dateModified: hoje.toISOString().slice(0, 10),
    name: nome, author: { "@type": "Person", name: "Mestre Alberto", url: url.origin + "/sobre" } }).replace(/</g, "\\u003c");
  const rw = new HTMLRewriter().on("head", { element(e) { e.append(`<script type="application/ld+json">${ld}</script>`, { html: true }); } });
  const corpo = (y, tit) => `<div class="chave">${hPor(y.k)}</div>${y.t.map((t) => `<p>${hPor(t)}</p>`).join("")}<div class="dica"><b>👉 ${tit}</b> ${hPor(y.d)}</div>`;
  const est = (e) => "★".repeat(Math.round(e)) + "☆".repeat(5 - Math.round(e));
  if (alvo < 0) {
    // 13/11/2026 (SEO «horóscopo de amanhã», aprovado por ele): o título começa pela pesquisa e leva a data
    const titulo = semana_ ? `Horóscopo Semanal, ${dia} a ${fd(fim)} · Mestre Alberto` : alvo === -3 ? `Horóscopo de Amanhã (${dia}) para os 12 signos | Mestre Alberto` : `Horóscopo do Dia, ${dia}: os 12 signos · Mestre Alberto`;
    const ceu = (x.ceu || []).map((l) => `<li>${hPor(l)}</li>`).join("");
    const dc = (i) => { const d = new Date(i + "T12:00:00Z"); return `${H_SEMANA[d.getUTCDay()].toLowerCase()}, ${d.getUTCDate()}`; };
    const grelha = x.s.map((y, s) => `<article class="signo" id="s${s}"><div class="cab"><img class="gli" src="signos/${String(s).padStart(2, "0")}.webp" alt="${H_NOMES[s]}" width="72" height="72" loading="lazy"><div><div class="nome">${H_NOMES[s]}</div><div class="ene" aria-label="Energia ${y.e} de 5">${est(y.e)}<span>${semana_ ? "energia da semana" : "energia"}</span></div></div></div>${corpo(y, semana_ ? "A dica da semana" : alvo === -3 ? "A dica de amanhã" : "A dica de hoje").replace('<div class="dica">', semana_ && y.melhor ? `<div class="dias"><span class="bom">✨ Melhor dia: ${dc(y.melhor.d)}</span>${y.cuidado ? `<span>⚠️ Mais cuidado: ${dc(y.cuidado.d)}</span>` : ""}</div><div class="dica">` : '<div class="dica">')}${alvo === -3 ? `<a class="mais" href="/horoscopo-de-amanha/${H_SLUGS[s]}">${H_NOMES[s]} amanhã, em detalhe →</a>` : ""}</article>`).join("");
    rw.on("title", { element(e) { e.setInnerContent(titulo); } })
      .on("#data", { element(e) { e.setInnerContent(semana_ ? `<small>Esta semana</small>${dia} a ${fd(fim)}` : `<small>${alvo === -3 ? "Amanhã" : "Hoje"} · ${semana}</small>${dia}`, { html: true }); } })
      .on("#ceu", { element(e) { e.setInnerContent(ceu, { html: true }); } })
      .on("#grelha", { element(e) { e.setInnerContent(grelha, { html: true }); } });
    if (alvo === -3) {   // 13/11/2026: os trânsitos datados, o ranking dos 12 signos e o elemento do dia (+ ItemList dos trânsitos)
      try {   // se algo falhar aqui, a página sai como antes (sem esta parte), nunca com erro
        const C = await lerCeu(url, env);
        const d = amanhaDia(x, C, base, semana, dia);
        rw.on("#am-dia", { element(e) { e.setInnerContent(d.html, { html: true }); } });
        if (d.ld) rw.on("head", { element(e) { e.append(`<script type="application/ld+json">${d.ld}</script>`, { html: true }); } });
      } catch (e) { /* fica a página de sempre */ }
    }
  } else {
    const y = x.s[alvo];
    rw.on("#hoje", { element(e) { e.setInnerContent(`<p style="margin:.2rem 0;color:var(--suave)">${semana}, ${dia}</p><div class="ene">${est(y.e)} energia</div>${corpo(y, "A dica de hoje")}`, { html: true }); } });
  }
  const r = new Response(resp.body, resp);
  r.headers.delete("etag"); r.headers.delete("last-modified");
  r.headers.set("Cache-Control", "public, max-age=0, must-revalidate");
  return rw.transform(r);
}

// ── 13/11/2026 (SEO «horóscopo de amanhã», aprovado por ele): o dia de amanhã por signo, /horoscopo-de-amanha/<signo>,
// e mais «dia» na página geral. 12 endereços FIXOS, o texto muda à meia-noite de Portugal (Travão ao SEO: a família não cresce).
// Nada inventado: o resumo é o mesmo horoscopo-dia/<amanhã>.json da página geral; onde está cada planeta vem do ceu-dados.js
// (Swiss Ephemeris, renovado todos os meses pelo ~/site-ceu-rolante.sh); a Lua é a casa «h» do JSON; as frases de «planeta
// na casa N» são as do horóscopo semanal por signo (amanha-textos.js, feito pelo gerar-amanha-signos.py).
import AM from "./amanha-textos.js";
const AM_P = [["Sol", "sol", "☉"], ["Mercúrio", "mercurio", "☿"], ["Vénus", "venus", "♀"], ["Marte", "marte", "♂"], ["Júpiter", "jupiter", "♃"],
  ["Saturno", "saturno", "♄"], ["Úrano", "urano", "♅"], ["Neptuno", "neptuno", "♆"], ["Plutão", "plutao", "♇"]];
const AM_ART = { "Sol": "o Sol", "Lua": "a Lua" };
const amHoraBR = (ms) => new Intl.DateTimeFormat("pt-PT", { timeZone: "America/Sao_Paulo", hour: "2-digit", minute: "2-digit" }).format(new Date(ms));
const amDiaEm = (ms, tz) => new Intl.DateTimeFormat("en-CA", { timeZone: tz }).format(new Date(ms));
const amDoisFusos = (ms) => `${hHora(ms)} em Portugal (${amHoraBR(ms)}${amDiaEm(ms, "Europe/Lisbon") !== amDiaEm(ms, "America/Sao_Paulo") ? " da véspera" : ""} em Brasília)`;
const amJunta = (l) => l.length === 1 ? l[0] : l.slice(0, -1).join(", ") + " e " + l[l.length - 1];
// o papel de cada planeta, para o leitor perceber porque é que ele aparece nessa área
const AM_PAPEL = { "Vénus": "o planeta do amor", "Júpiter": "o planeta da abundância", "Sol": "a vontade", "Mercúrio": "as palavras e os papéis", "Saturno": "o dever", "Marte": "a força" };
const amCap = (t) => t.charAt(0).toUpperCase() + t.slice(1);
const amEst = (e) => "★".repeat(Math.round(e)) + "☆".repeat(5 - Math.round(e));
const amCasa = (sAstro, sLeitor) => ((sAstro - sLeitor + 12) % 12) + 1;
function amSemente(t) { let h = 2166136261; for (const c of t) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }   // o mesmo da app O Teu Céu
async function lerCeu(url, env) {
  try {
    const r = await env.ASSETS.fetch(new Request(new URL("/ceu-dados.js", url), { method: "GET" }));
    if (!r.ok) return null;
    const t = await r.text();
    return JSON.parse(t.slice(t.indexOf("{", t.indexOf("window.CEU"))).trim().replace(/;$/, ""));
  } catch (e) { return null; }
}
// signo e sentido de cada planeta no instante t (ms): o estado do início mais os ingressos e as estações até lá
function amCeuEm(C, t) {
  if (!C || !C.estado_inicio || t < C.inicio_t || t > Date.parse(C.ate + "T23:59:59Z")) return null;
  const st = {};
  for (const k in C.estado_inicio) st[k] = { s: C.estado_inicio[k].s, r: !!C.estado_inicio[k].r };
  const ev = (C.ingressos || []).map((e) => ({ t: e.t, p: e.p, s: e.s, r: !!e.r }))
    .concat((C.estacoes || []).map((e) => ({ t: e.t, p: e.p, s: e.s, r: e.tipo === "R" })))
    .filter((e) => e.t > C.inicio_t && e.t <= t).sort((a, b) => a.t - b.t);
  for (const e of ev) st[e.p] = { s: e.s, r: e.r };
  return st;
}
// o que muda durante o dia (ingressos e estações entre a meia-noite e a meia-noite de Portugal, aproximadas por 00:00–24:00 UTC±1)
function amMudancas(C, base) {
  if (!C) return [];
  const ini = Date.parse(base.toISOString().slice(0, 10) + "T00:00:00Z") - 3600000, fim = ini + 86400000;
  const lx = (t) => new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon" }).format(new Date(t)) === base.toISOString().slice(0, 10);
  const out = [];
  for (const e of C.ingressos || []) if (e.t >= ini && e.t < fim + 7200000 && lx(e.t)) out.push({ t: e.t, p: e.p, s: e.s, tipo: "I" });
  for (const e of C.estacoes || []) if (e.t >= ini && e.t < fim + 7200000 && lx(e.t)) out.push({ t: e.t, p: e.p, s: e.s, tipo: e.tipo });
  return out.sort((a, b) => a.t - b.t);
}
const amNomeP = (k) => (AM_P.find((p) => p[1] === k) || [k])[0];

// a parte nova da página geral: os trânsitos datados, o ranking dos 12 signos e o elemento do dia
function amanhaDia(x, C, base, semana, dia) {
  const st = amCeuEm(C, base.getTime());
  const sLua = (x.s[0].h - 1 + 12) % 12;          // a casa da Lua para Carneiro dá o signo da Lua
  const sem = semana.toLowerCase();
  const itens = (x.ceu || []).map((l) => hPor(l));
  let h = `<h2>Os trânsitos de ${sem}, ${dia}</h2>`;
  h += `<ul class="ceu">${itens.map((l) => `<li>${l}</li>`).join("")}`
    + (x.melhor ? `<li class="mom">✨ Melhor momento: por volta das ${amDoisFusos(x.melhor.t)} · ${hEsc(x.melhor.txt)}</li>` : "")
    + (x.cuidado ? `<li class="mom">⚠️ Mais cuidado por volta das ${amDoisFusos(x.cuidado.t)} · ${hEsc(x.cuidado.txt)}</li>` : "") + "</ul>";
  if (st) {
    const pos = [`☽ a Lua em ${H_NOMES[sLua]}`].concat(AM_P.map(([n, k, g]) => `${g} ${AM_ART[n] || n} em ${H_NOMES[st[k].s]}${st[k].r ? " ℞" : ""}`));
    h += `<p class="am-pos">Onde estão os astros amanhã ao meio-dia: ${pos.join(" · ")}. <small>℞ = retrógrado.</small></p>`;
  }
  // o ranking: a energia de cada signo (as estrelas, de 2 a 5); em empate fica a ordem do zodíaco
  const ord = x.s.map((y, s) => ({ s, e: y.e, k: y.k })).sort((a, b) => b.e - a.e || a.s - b.s);
  h += `<h2>Ranking dos 12 signos amanhã</h2><ol class="am-rank">${ord.map((o) => `<li><a href="/horoscopo-de-amanha/${H_SLUGS[o.s]}">${H_NOMES[o.s]}</a> <span class="est" aria-label="Energia ${o.e} de 5">${amEst(o.e)}</span> <i>${hPor(o.k)}</i></li>`).join("")}</ol>`
    + `<p class="am-nota">Ordenados pela energia que o céu de ${sem} dá a cada signo (as estrelas de cada um, de 2 a 5, as mesmas da grelha acima). Em empate, fica a ordem do zodíaco.</p>`;
  // o elemento do dia: quantos dos 10 astros (Sol a Plutão e a Lua) estão em signos de cada elemento
  if (st) {
    const conta = { "Fogo": [], "Terra": [], "Ar": [], "Água": [] };
    conta[AM.ELEM_SIGNO[sLua]].push("a Lua");
    for (const [n, k] of AM_P) conta[AM.ELEM_SIGNO[st[k].s]].push(AM_ART[n] || n);
    const ELS = ["Fogo", "Terra", "Ar", "Água"];
    const max = Math.max(...ELS.map((el) => conta[el].length));
    const fortes = ELS.filter((el) => conta[el].length === max);
    const quem = (el) => H_NOMES.filter((_, s) => AM.ELEM_SIGNO[s] === el);
    const junta = (l) => l.length === 1 ? l[0] : l.slice(0, -1).join(", ") + " e " + l[l.length - 1];
    const art = (el) => el === "Fogo" ? "o Fogo" : el === "Terra" ? "a Terra" : el === "Ar" ? "o Ar" : "a Água";
    h += `<h2>O elemento do dia</h2>`;
    h += fortes.length === 1
      ? `<p>${(base.getUTCDay() % 6 === 0) ? "No" : "Na"} ${sem}, ${dia}, o elemento com mais astros é ${art(fortes[0])}: ${junta(conta[fortes[0]])} (${max} de 10). É o elemento de ${junta(quem(fortes[0]))}, e quem é de ${fortes[0]} ${hEsc(AM.ELEMENTO[fortes[0]])}.</p>`
      : `<p>${(base.getUTCDay() % 6 === 0) ? "No" : "Na"} ${sem}, ${dia}, ${junta(fortes.map(art))} empatam, com ${max} astros cada. ${fortes.map((el) => `${amCap(art(el))}: ${junta(conta[el])}.`).join(" ")}</p>`;
    h += `<p class="am-nota">Todos os elementos: ${ELS.map((el) => `${el} ${conta[el].length}`).join(" · ")}. Contam o Sol, a Lua e os planetas de Mercúrio a Plutão, pelo signo em que estão ao meio-dia.</p>`;
  }
  const ld = itens.length ? JSON.stringify({ "@context": "https://schema.org", "@type": "ItemList", name: `Os trânsitos de ${sem}, ${dia}`,
    itemListElement: itens.map((t, i) => ({ "@type": "ListItem", position: i + 1, name: t.replace(/&amp;/g, "&").replace(/^[^A-Za-zÀ-ÿ]+/, "") })) }).replace(/</g, "\\u003c") : "";
  return { html: h, ld };
}

async function amanhaSignoNoHtml(url, env, s) {
  const resp = await env.ASSETS.fetch(new Request(url.toString(), { method: "GET" }));
  if (!resp.ok || !(resp.headers.get("content-type") || "").includes("text/html")) return resp;
  const hoje = new Date(new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon" }).format(new Date()) + "T12:00:00Z");
  const base = new Date(hoje); base.setUTCDate(base.getUTCDate() + 1);
  const iso = base.toISOString().slice(0, 10);
  let x = null;
  try {
    const j = await env.ASSETS.fetch(new Request(new URL(`/horoscopo-dia/${iso}.json`, url), { method: "GET" }));
    if (j.ok) x = await j.json();
  } catch (e) { x = null; }
  if (!x || !Array.isArray(x.s) || x.s.length !== 12) return resp;
  const C = await lerCeu(url, env);
  let rw;
  try { rw = amanhaSignoRw(url, x, C, s, hoje, base, iso); } catch (e) { return resp; }   // erro nos dados → o molde, com a ligação para a página geral
  const r = new Response(resp.body, resp);
  r.headers.delete("etag"); r.headers.delete("last-modified");
  r.headers.set("Cache-Control", "public, max-age=0, must-revalidate");
  return rw.transform(r);
}
function amanhaSignoRw(url, x, C, s, hoje, base, iso) {
  const st = amCeuEm(C, base.getTime());
  const y = x.s[s], nm = H_NOMES[s], sl = H_SLUGS[s], br = AM.COM_BR[s] ? AM.COM_BR[s].slice(nm.length + 2, -1) : "";
  const dia = `${base.getUTCDate()} de ${H_MESES[base.getUTCMonth()]}`, semana = H_SEMANA[base.getUTCDay()], sem = semana.toLowerCase();
  const sLua = (s + y.h - 1) % 12;
  const titulo = `${nm} amanhã: horóscopo de ${dia}${br ? ` (${br})` : ""} · Mestre Alberto`;
  const desc = `${nm}${br ? ` (${br})` : ""} amanhã, ${sem}, ${dia}: ${hPor(y.k)} Amor, dinheiro, trabalho, energia, o melhor momento e a carta do dia, no céu calculado.`;
  // a leitura de um planeta pela casa solar deste signo
  const pl = (n) => {
    const k = AM_P.find((p) => p[0] === n)[1], q = st[k], hc = amCasa(q.s, s);
    const ret = q.r ? (n === "Vénus" ? " · retrógrada" : " · retrógrado") : "";
    return `<span class="pl">${AM_ART[n] ? amCap(AM_ART[n]) : n} (${AM_PAPEL[n]}) em ${H_NOMES[q.s]} · casa ${hc}${ret}</span>`
      + `<p>${hEsc(amCap(AM.PC[n][hc]))}${AM.LONGO[n] ? " " + hEsc(AM.LONGO[n][hc]) : ""}${q.r && AM.RETRO[n] ? " " + hEsc(AM.RETRO[n]) : ""}</p>`;
  };
  // quem passa amanhã por uma casa (a Lua incluída): factos do céu calculado, sem leitura
  const ocup = (hc, rot) => {
    const q = (s + hc - 1) % 12;
    const l = (sLua === q ? ["a Lua"] : []).concat(AM_P.filter(([, k]) => st[k].s === q).map(([pn]) => AM_ART[pn] || pn));
    return `<p>A sua casa ${hc}, ${rot}, fica em ${H_NOMES[q]}: ${l.length ? `amanhã ${l.length === 1 ? "está" : "estão"} lá ${amJunta(l)}` : "amanhã não tem nenhum astro de passagem"}.</p>`;
  };
  const muda = amMudancas(C, base).map((m) => {
    const n = amNomeP(m.p), hc = amCasa(m.s, s);
    if (m.tipo === "I") return `Às ${amDoisFusos(m.t)}, ${AM_ART[n] || n} entra em ${H_NOMES[m.s]}: para ${nm}, passa a tocar ${hEsc(AM.CASA[hc])} (casa ${hc}).`;
    return `Às ${amDoisFusos(m.t)}, ${n} ${m.tipo === "R" ? (n === "Vénus" ? "fica retrógrada" : "fica retrógrado") : "volta a andar para a frente"} na sua casa ${hc}: ${m.tipo === "R" ? "é tempo de rever" : "desbloqueia"} o que toca ${hEsc(AM.CASA[hc])}.`;
  });
  // o resumo: o mesmo texto da página geral, mais a Lua e o regente lidos para este signo
  const [reg] = AM.REGENTE[s];
  let regTxt = "";
  if (reg === "Lua") regTxt = `O seu regente é a Lua: amanhã está em ${H_NOMES[sLua]}, na sua casa ${y.h}, e é ${hEsc(AM.CASA[y.h])} que dá o tom ao dia de ${nm}.`;
  else if (st) {
    const k = AM_P.find((p) => p[0] === reg)[1], hc = amCasa(st[k].s, s);
    regTxt = `O seu planeta regente, ${AM_ART[reg] || reg}, está em ${H_NOMES[st[k].s]}, na sua casa ${hc}${st[k].r ? (reg === "Vénus" ? " e retrógrada" : " e retrógrado") : ""}: é ${hEsc(AM.CASA[hc])} que recebe a força maior de ${nm} amanhã.`;
  }
  const resumo = `<h2>${nm} amanhã, ${sem}, ${dia}</h2><div class="ene" aria-label="Energia de amanhã: ${y.e} em 5">${amEst(y.e)}<span>energia de amanhã</span></div>`
    + `<div class="chave">${hPor(y.k)}</div>${y.t.map((t) => `<p>${hPor(t)}</p>`).join("")}`
    + (regTxt ? `<p>${regTxt}</p>` : "")
    + `<div class="dica"><b>👉 A dica de amanhã</b>${hPor(y.d)}</div>`;
  const areas = st ? `<h2>Amor, dinheiro, trabalho e energia</h2>`
    + `<h3>❤️ Amor</h3>${pl("Vénus")}${ocup(7, "a das relações")}`
    + `<h3>💶 Dinheiro</h3>${pl("Júpiter")}${ocup(2, "a do dinheiro")}`
    + `<h3>💼 Trabalho</h3>${pl("Sol")}${pl("Mercúrio")}${pl("Saturno")}${ocup(10, "a da carreira")}`
    + `<h3>⚡ Energia</h3><p>A energia de ${nm} amanhã: <b style="color:var(--ouro)">${amEst(y.e)}</b> (${y.e} em 5). Com a Lua na sua casa ${y.h}: ${hEsc(AM.LUA[y.h])}</p>${pl("Marte")}`
    + (muda.length ? `<h3>🔄 O que muda amanhã</h3>${muda.map((m) => `<p>${m}</p>`).join("")}` : "")
    + `<p class="nota">As áreas leem-se pelas casas solares de ${nm}: Vénus no amor, Júpiter no dinheiro, o Sol, Mercúrio e Saturno no trabalho, Marte na energia. Leituras simbólicas: nada aqui substitui o médico, o advogado ou o contabilista.</p>` : null;
  const mom = `<h2>O melhor momento de amanhã</h2><ul class="am-mom">`
    + (x.melhor ? `<li><b>✨ Por volta das ${amDoisFusos(x.melhor.t)}</b><br>${hEsc(x.melhor.txt)}: o aspeto da Lua mais favorável do dia, para pedir, propor ou começar.</li>` : `<li>Amanhã a Lua não faz nenhum aspeto favorável exato: escolha o momento pelo seu ritmo.</li>`)
    + (x.cuidado ? `<li><b>⚠️ Mais cuidado por volta das ${amDoisFusos(x.cuidado.t)}</b><br>${hEsc(x.cuidado.txt)}: deixe as decisões grandes para outra hora.</li>` : "")
    + `</ul>`;
  const n = amSemente(`amanha|${sl}|${iso}`) % 22, c = AM.CARTAS[n], cn = AM.ARC_NOMES[n];
  const carta = `<h2>A carta de amanhã para ${nm}</h2><div class="am-carta"><a href="/arcano-${c}"><img src="/cartas/${c}.webp" alt="${cn}, carta do baralho do Mestre Alberto" width="969" height="1624" loading="lazy"></a>`
    + `<div><h3>${cn}</h3><p>${hEsc(AM.CARTA_DIA[n])}</p><p class="nota" style="text-align:left">Um Arcano Maior do baralho do Mestre Alberto, tirado para ${nm} e para ${sem}, ${dia}. <a href="/arcano-${c}">O significado de ${cn}</a> · <a href="/tarot-gratis">Tirar as suas cartas</a></p></div></div>`;
  let ceu = `<h2>O céu de ${sem}, ${dia}</h2><ul class="ceu">${(x.ceu || []).map((l) => `<li>${hPor(l)}</li>`).join("")}</ul>`;
  if (st) ceu += `<div class="rolar" style="margin-top:1rem"><table class="tabela"><thead><tr><th>Astro</th><th>Signo</th><th>Casa para ${nm}</th></tr></thead><tbody>`
    + `<tr><td><b>Lua</b></td><td>${H_NOMES[sLua]}</td><td>casa ${y.h} <small>${hEsc(AM.CURTA[y.h])}</small></td></tr>`
    + AM_P.map(([pn, k]) => { const hc = amCasa(st[k].s, s); return `<tr><td><b>${pn}</b>${st[k].r ? " ℞" : ""}</td><td>${H_NOMES[st[k].s]}</td><td>casa ${hc} <small>${hEsc(AM.CURTA[hc])}</small></td></tr>`; }).join("")
    + `</tbody></table></div><p class="nota">Posições ao meio-dia de amanhã. ℞ = retrógrado. Veja também <a href="/ceu-de-hoje">o Céu de Hoje</a> e <a href="/lua">a Lua</a>.</p>`;
  const ld = JSON.stringify({ "@context": "https://schema.org", "@type": "WebPage", url: url.origin + url.pathname, inLanguage: "pt", dateModified: hoje.toISOString().slice(0, 10),
    name: `${nm} amanhã: horóscopo de ${dia}`, author: { "@type": "Person", name: "Mestre Alberto", url: url.origin + "/sobre" } }).replace(/</g, "\\u003c");
  const rw = new HTMLRewriter()
    .on("head", { element(e) { e.append(`<script type="application/ld+json">${ld}</script>`, { html: true }); } })
    .on("title", { element(e) { e.setInnerContent(titulo); } })
    .on('meta[name="description"]', { element(e) { e.setAttribute("content", desc.replace(/&amp;/g, "&").replace(/&quot;/g, "")); } })
    .on('meta[property="og:title"]', { element(e) { e.setAttribute("content", titulo); } })
    .on('meta[property="og:description"]', { element(e) { e.setAttribute("content", desc.replace(/&amp;/g, "&").replace(/&quot;/g, "")); } })
    .on("#am-selo", { element(e) { e.setInnerContent(`Amanhã · ${sem}, ${dia}`); } })
    .on("#am-h1", { element(e) { e.setInnerContent(`<span class="az">${nm}</span> amanhã <small>${br ? `(${br}) · ` : ""}${sem}, ${dia}</small>`, { html: true }); } })
    .on("#am-resumo", { element(e) { e.setInnerContent(resumo, { html: true }); } })
    .on("#am-momento", { element(e) { e.setInnerContent(mom, { html: true }); } })
    .on("#am-carta", { element(e) { e.setInnerContent(carta, { html: true }); } })
    .on("#am-ceu", { element(e) { e.setInnerContent(ceu, { html: true }); } });
  if (areas) rw.on("#am-areas", { element(e) { e.setInnerContent(areas, { html: true }); } });
  return rw;
}

// 07/11/2026 (O-137, O-138): /aniversarios chegava ao Google sem nenhum nome, porque só o JavaScript enchia a lista. O
// JavaScript da página redesenha por cima, com o fuso escolhido. Se os dados falharem fica a página de sempre.
const hDiaMes = (iso) => `${+iso.slice(8)} de ${H_MESES[+iso.slice(5, 7) - 1]}`;
async function aniversariosNoHtml(url, env) {
  const resp = await env.ASSETS.fetch(new Request(url.toString(), { method: "GET" }));
  if (!resp.ok || !(resp.headers.get("content-type") || "").includes("text/html")) return resp;
  let L = null;
  const iso = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon" }).format(new Date());
  try {
    const j = await env.ASSETS.fetch(new Request(new URL("/aniversarios-dados.js", url), { method: "GET" }));
    if (j.ok) { const t = await j.text(); L = JSON.parse(t.slice(t.indexOf("{", t.indexOf("window.ANIVERSARIOS"))).trim().replace(/;$/, ""))[iso.slice(5)]; }
  } catch (e) { L = null; }
  if (!Array.isArray(L) || !L.length) return resp;
  const dia = hDiaMes(iso), ano = +iso.slice(0, 4);
  const sigs = [...new Set(L.map((p) => H_NOMES[p.s]))].join(" ou ");
  const pessoas = L.map((p) => `<article class="pessoa"><div class="topo-p"><span class="nome">${hEsc(p.n)}</span><span class="bandeira" title="${hEsc(p.p)}">${p.p === "PT" ? "🇵🇹" : p.p === "BR" ? "🇧🇷" : "🇧🇷🇵🇹"}</span></div>`
    + `<div class="desc">${hEsc(p.d)}</div><div class="idade">Nasceu a ${dia} de ${p.a} · <b>faz hoje ${ano - p.a} anos</b></div>`
    + `<div class="signo"><b>${H_NOMES[p.s]}</b>${p.c ? " <small>(na cúspide)</small>" : ""}</div>`
    + `<a class="lig" href="/signo/${H_SLUGS[p.s]}">Ver o horóscopo de ${H_NOMES[p.s]} →</a></article>`).join("");
  const rw = new HTMLRewriter()
    .on("#data", { element(e) { e.setInnerContent(`<small>hoje</small>${dia}`, { html: true }); } })
    .on("#frase-dia", { element(e) { e.setInnerContent(`Quem faz anos hoje, ${dia}, é de <b>${sigs}</b>.`, { html: true }); } })
    .on("#pessoas", { element(e) { e.setInnerContent(pessoas, { html: true }); } });
  const r = new Response(resp.body, resp);
  r.headers.delete("etag"); r.headers.delete("last-modified");
  r.headers.set("Cache-Control", "public, max-age=0, must-revalidate");
  return rw.transform(r);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // 31/10/2026 (ele, SEO): o www servia o site inteiro em duplicado. As páginas (as que passam pelo worker)
    // vão com 301 para o endereço oficial sem www. O http:// já vai para https pelo «Always Use HTTPS» da zona.
    if (url.hostname === "www.genialtarot.com" && (request.method === "GET" || request.method === "HEAD")) {
      return Response.redirect("https://genialtarot.com" + url.pathname + url.search, 301);
    }

    // 06/11/2026 (ele, SEO): a Cloudflare manda /x.html para /x com 307 (temporário) e o Google ficou com o .html como canónica em 8 arcanos.
    // Quando a resposta dos ficheiros é esse 307, sai 301. Endereço .html que não exista segue o caminho normal (tabela antiga e página 404).
    if (url.pathname.endsWith(".html") && (request.method === "GET" || request.method === "HEAD")) {
      const r = await env.ASSETS.fetch(request);
      const destino = r.headers.get("location");
      if (r.status >= 300 && r.status < 400 && destino) return Response.redirect(new URL(destino, url.origin).toString(), 301);
    }

    // Contar a visita antes de tudo. So paginas: fora as APIs, o /cdn-cgi/ da
    // Cloudflare e a pagina privada das estatisticas (que sou eu a olhar).
    if (!url.pathname.startsWith("/api/") && !url.pathname.startsWith("/cdn-cgi/") &&
        url.pathname !== "/Estataomp8" && url.pathname !== "/geo" && url.pathname !== "/notify" && url.pathname !== "/sair" && url.pathname !== "/quero") {
      contarVisita(request, url, env, ctx);
    }

    // 05/11/2026: o Consultório Virtual (ver a classe Consultorio, no fim). A página é só uma, a do código é a mesma folha:
    // /consultorio/<código> serve consultorio-sala.html; o código é lido no navegador. Sem indexar e sem mandar o endereço a ninguém.
    if (/^\/consultorio\/[a-hjkmnp-z2-9]{20}\/?$/.test(url.pathname) && (request.method === "GET" || request.method === "HEAD")) {
      const folha = await env.ASSETS.fetch(new Request(new URL("/consultorio-sala", url), { method: "GET" }));
      return new Response(request.method === "HEAD" ? null : folha.body, { status: folha.status, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow", "Referrer-Policy": "no-referrer", "Permissions-Policy": "microphone=(self), camera=(self)" } });
    }
    if (url.pathname.startsWith("/api/consultorio/")) {
      if (!env.CONSULTORIO) return new Response("{}", { status: 503 });
      try { return await env.CONSULTORIO.get(env.CONSULTORIO.idFromName("consultorio")).fetch(request); }
      catch (e) { return new Response(JSON.stringify({ ok: false, erro: "consultorio: " + String(e && e.message || e).slice(0, 300) }), { status: 500, headers: { "Content-Type": "application/json" } }); }
    }

    // 05/11/2026: a conta do visitante e o início de sessão (ver a classe Contas, no fim). /api/conta/* não é ficheiro,
    // por isso chega aqui sem precisar de regra no run_worker_first (como o /api/vivo e o /notify).
    if (url.pathname.startsWith("/api/conta/")) {
      if (!env.CONTAS) return new Response(JSON.stringify({ ok: false, erro: "indisponivel" }), { status: 503, headers: { "Content-Type": "application/json" } });
      try { return await env.CONTAS.get(env.CONTAS.idFromName("contas")).fetch(request); }
      catch (e) { return new Response(JSON.stringify({ ok: false, erro: "indisponivel" }), { status: 500, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } }); }
    }

    // 31/10/2026: quem está no site agora + o chat dele com essa pessoa (ver a classe Sala, no fim)
    // 13/11/2026 O-404 (OK dele): clique num botão de pagamento (myPOS ou PIX), mandado pelo vivo.js com a origem da pessoa.
    // Fica no mesmo contador, mas com blob1 = «/clique-pagamento» e blob5 = «clique»: está fora da lista PAGINAS e não é
    // «pessoa», por isso não entra em nenhuma conta de visitas. blob6 = mypos|pix, blob9 = a página onde carregou.
    if (url.pathname === "/api/vivo/pagar" && request.method === "POST") {
      try {
        const ref = request.headers.get("origin") || request.headers.get("referer") || "";
        const d = await request.json();
        const tipo = d.tipo === "pix" ? "pix" : "mypos";
        const pg = String(d.pagina || "").replace(/\.html$/, "");
        const ck = (request.headers.get("cookie") || "").match(/(?:^|;\s*)gt_o=([a-z0-9/-]{1,64})(?:;|$)/);
        if (env.VISITAS && /genialtarot\.com/.test(ref) && /^\/[a-z0-9-]*(\/[a-z0-9-]+)?$/.test(pg)) {
          const ua = request.headers.get("user-agent") || "";
          env.VISITAS.writeDataPoint({ indexes: ["/clique-pagamento"], doubles: [1], blobs: ["/clique-pagamento", ck ? "marca:" + ck[1] : "(sem origem)",
            (request.cf && request.cf.country) || "?", aparelhoDe(ua), "clique", tipo, servidorAlugado(request.cf),
            String(d.sid || "").replace(/[^a-z0-9]/g, "").slice(0, 40), pg.slice(0, 120)] });
        }
      } catch (e) { /* contar nunca estraga o pagamento */ }
      return new Response("{}", { headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
    }
    if (url.pathname === "/api/vivo" || url.pathname.startsWith("/api/vivo/")) {
      if (!env.SALA) return new Response("{}", { status: 503 });
      // 01/11/2026: as ~500 páginas novas do SEO são servidas sem passar pelo worker, por isso o contarVisita não as vê.
      // O vivo.js manda «novo: true» no primeiro sinal de cada página aberta: conta-se aqui, no mesmo formato,
      // só para as páginas que NÃO estão na lista PAGINAS (essas já contam à entrada — não contar duas vezes).
      if (url.pathname === "/api/vivo" && request.method === "POST" && env.VISITAS) {
        const copia = request.clone();
        ctx.waitUntil((async () => {
          try {
            const d = await copia.json(); const p = String(d.pagina || "").replace(/\.html$/, "");
            const ref = request.headers.get("origin") || request.headers.get("referer") || "";
            // 01/11/2026: blob6 = «humano» — o vivo.js confirmou que mexeu na página ou a teve à vista 8 s. É SÓ ISTO
            // que as estatísticas contam como pessoa (os robôs que correm a página saem em 0 s e nunca confirmam).
            if (d.confirma && /^\/[a-z0-9-]*(\/[a-z0-9-]+)?$/.test(p) && /genialtarot\.com/.test(ref)) {
              const uaH = request.headers.get("user-agent") || "";
              env.VISITAS.writeDataPoint({ indexes: [(p || "/").slice(0, 90)], doubles: [1], blobs: [(p || "/").slice(0, 120), origemVivo(d).slice(0, 120),
                (request.cf && request.cf.country) || "?", aparelhoDe(uaH), quemE(uaH, request.cf), "humano", servidorAlugado(request.cf),
                String(d.sid || "").replace(/[^a-z0-9]/g, "").slice(0, 40)] });   // blob8 = sid (01/11 19:45): cada pessoa conta UMA vez, não cada página
              return;
            }
            if (!d.novo || !/^\/[a-z0-9-]+(\/[a-z0-9-]+)?$/.test(p) || !/genialtarot\.com/.test(ref)) return;
            const ua = request.headers.get("user-agent") || "";
            // 01/11/2026 (ele: «separa os suspeitos»): numa página da lista, o worker já contou a entrada; este sinal só CONFIRMA
            // que era um navegador a sério (correu o vivo.js). Entradas «pessoa» sem confirmação = suspeitos (robôs disfarçados).
            if (PAGINAS.has(p)) { env.VISITAS.writeDataPoint({ indexes: [p.slice(0, 90)], doubles: [1], blobs: [p.slice(0, 120), origemVivo(d).slice(0, 120), (request.cf && request.cf.country) || "?", aparelhoDe(ua), quemE(ua, request.cf), "js", servidorAlugado(request.cf)] }); return; }
            env.VISITAS.writeDataPoint({ indexes: [p.slice(0, 90)], doubles: [1], blobs: [p.slice(0, 120),
              origemVivo(d).slice(0, 120),
              (request.cf && request.cf.country) || "?", aparelhoDe(ua), quemE(ua, request.cf), "vivo", servidorAlugado(request.cf)] });   // blob6 = «vivo»: veio pelo sinal do vivo.js
          } catch (e) { /* contar nunca pode estragar o sinal */ }
        })());
      }
      try { return await env.SALA.get(env.SALA.idFromName("sala")).fetch(request); }
      catch (e) { return new Response(JSON.stringify({ ok: false, erro: "sala: " + String(e && e.message || e).slice(0, 300) }), { status: 500, headers: { "Content-Type": "application/json" } }); }
    }

    // Vídeo diário mais recente + minutos de cada signo (com cache de 15 min)
    // 06/11/2026 (ele): plano dos cartões da página inicial, feito no painel (aba Cartões). Ler é público; gravar exige a chave.
    if (url.pathname === "/api/cartoes-agenda") {
      const resp = (o, st) => new Response(JSON.stringify(o), { status: st || 200, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });
      if (request.method === "POST") {
        if (!env.STATS_KEY || request.headers.get("X-Chave") !== env.STATS_KEY) return resp({ ok: false, error: "chave errada" }, 403);
        const t = await request.text();
        try { JSON.parse(t); } catch (e) { return resp({ ok: false, error: "json" }, 400); }
        if (t.length > 30000) return resp({ ok: false, error: "grande" }, 413);
        await env.CAPTURAS.put("cartoes-agenda", t);
        return resp({ ok: true });
      }
      const t = await env.CAPTURAS.get("cartoes-agenda");
      return new Response(t || "{}", { headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "public, max-age=300" } });
    }

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
        const data = await comReserva(env, "zodiac", () => fetchLatestDailyZodiac(false, env));
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
        const data = await comReserva(env, "fimsemana", () => fetchLatestDailyZodiac(false, env, WEEKEND_PLAYLIST_ID));
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
        const data = await comReserva(env, "anual", () => fetchAnnualZodiac(false, env));
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

    // ── SAIR DA LISTA DE NOVIDADES (29/10/2026) ─────────────────────────
    // Cada email de novidades traz /sair?t=<token> (24 hex, um por pessoa).
    // GET mostra a confirmação; POST (o botão, ou o «cancelar subscrição» do
    // Gmail, RFC 8058) grava «sair-<token>» na fila sem prazo. O cerebro lê
    // estas chaves e tira a pessoa da lista; o fila-capturas.py não lhes toca.
    // ── ABRIU / CARREGOU NUM EMAIL (01/11/2026, pedido dele: «coloca se a pessoa abriu o email e se entrou em algum
    // link») ── /e/a?i=<id do envio> = a imagem invisível (abriu); /e/c?i=<id>&u=<destino> = o clique, que segue logo para
    // o destino. Grava na fila (KV) «aberto-<id>» e «clique-<id>-<n>»; a casa recolhe-os (promocoes.py) e mostra na aba
    // «Envios» (os dados vão também nos metadados, para a casa os ler numa só listagem). O id é aleatório, não diz quem é. Robôs (antivírus do correio, servidores) ficam marcados à parte.
    // Só se segue para o próprio site, o YouTube e o WhatsApp — nunca para endereços de fora (não é um «redirect» aberto).
    if (url.pathname === "/e/a" || url.pathname === "/e/c") {
      const i = (url.searchParams.get("i") || "").toLowerCase();
      const ok = /^[0-9a-f]{16}$/.test(i);
      const uaE = request.headers.get("user-agent") || "";
      const robo = quemE(uaE, request.cf) === "robo";
      const dados = JSON.stringify({ quando: new Date().toISOString(), robo, pais: (request.cf && request.cf.country) || "?", aparelho: aparelhoDe(uaE) });
      if (url.pathname === "/e/a") {
        if (ok) ctx.waitUntil(env.CAPTURAS.put("aberto-" + i + "-" + Date.now().toString(36), dados, { expirationTtl: 60 * 864e2, metadata: JSON.parse(dados) }).catch(() => {}));
        const gif = Uint8Array.from(atob("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"), (ch) => ch.charCodeAt(0));
        return new Response(gif, { headers: { "Content-Type": "image/gif", "Cache-Control": "no-store, max-age=0" } });
      }
      let destino = "https://www.genialtarot.com/";
      try {
        const d = new URL(url.searchParams.get("u") || "");
        if (d.protocol === "https:" && /^(www\.)?genialtarot\.com$|^youtu\.be$|^(www\.|m\.)?youtube\.com$|^wa\.me$/.test(d.hostname)) destino = d.toString();
      } catch (e) { /* fica a página principal */ }
      if (ok) {
        const pg = (() => { try { const d = new URL(destino); return (d.hostname.replace(/^www\./, "") + d.pathname).slice(0, 80); } catch (e) { return "?"; } })();
        ctx.waitUntil(env.CAPTURAS.put("clique-" + i + "-" + Date.now().toString(36), JSON.stringify({ ...JSON.parse(dados), destino: pg }), { expirationTtl: 60 * 864e2, metadata: { ...JSON.parse(dados), destino: pg } }).catch(() => {}));
      }
      return Response.redirect(destino, 302);
    }

    if (url.pathname === "/sair") {
      const t = (url.searchParams.get("t") || "").toLowerCase();
      const pagina = (msg) => new Response(`<!doctype html><html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Deixar de receber — Genial Tarot</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#1b1230;color:#efe8ff;font:17px/1.5 system-ui,sans-serif;padding:16px}main{max-width:440px;text-align:center}h1{font-size:1.3em;color:oklch(0.85 0.13 88)}button{font:inherit;background:oklch(0.85 0.13 88);color:#1b1230;border:0;border-radius:999px;padding:.7em 1.6em;cursor:pointer;font-weight:600}a{color:#cbb8ff}</style></head><body><main>${msg}<p><a href="/">genialtarot.com</a></p></main></body></html>`, { headers: { "Content-Type": "text/html; charset=utf-8" } });
      if (!/^[0-9a-f]{24}$/.test(t)) return pagina("<h1>Link incompleto</h1><p>Este link não está completo. Se quer deixar de receber os emails, responda a um deles com a palavra SAIR.</p>");
      if (request.method === "POST") {
        try { await env.CAPTURAS.put("sair-" + t, JSON.stringify({ quando: new Date().toISOString() })); }
        catch (e) { return pagina("<h1>Não consegui registar</h1><p>Tente outra vez daqui a pouco, ou responda a um dos emails com a palavra SAIR.</p>"); }
        return pagina("<h1>Feito ✔</h1><p>Não voltará a receber os emails de novidades do Mestre Alberto.</p>");
      }
      return pagina(`<h1>Deixar de receber os emails?</h1><p>Deixa de receber as novidades e promoções do Mestre Alberto por email.</p><form method="post"><button type="submit">Sim, não quero receber mais</button></form>`);
    }

    // ── «SIM, QUERO RECEBER NOVIDADES» (29/10/2026) ─────────────────────
    // O botão do email-convite às capturas antigas: /quero?t=<token>. O GET só
    // pergunta (os antivírus do correio abrem links sozinhos e não podem dar
    // o «sim» por ninguém); o POST do botão grava «quero-<token>» na fila.
    if (url.pathname === "/quero") {
      const t = (url.searchParams.get("t") || "").toLowerCase();
      const pagina = (msg) => new Response(`<!doctype html><html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Novidades do Mestre Alberto — Genial Tarot</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#1b1230;color:#efe8ff;font:17px/1.5 system-ui,sans-serif;padding:16px}main{max-width:460px;text-align:center}h1{font-size:1.3em;color:oklch(0.85 0.13 88)}button,.botao{display:inline-block;font:inherit;background:oklch(0.85 0.13 88);color:#1b1230;border:0;border-radius:999px;padding:.7em 1.6em;cursor:pointer;font-weight:600;text-decoration:none}a{color:#cbb8ff}</style></head><body><main>${msg}</main></body></html>`, { headers: { "Content-Type": "text/html; charset=utf-8" } });
      if (!/^[0-9a-f]{24}$/.test(t)) return pagina(`<h1>Link incompleto</h1><p>Este link não está completo. Se quer receber as novidades, responda ao email com a palavra SIM.</p><p><a href="/">genialtarot.com</a></p>`);
      if (request.method === "POST") {
        try { await env.CAPTURAS.put("quero-" + t, JSON.stringify({ quando: new Date().toISOString() })); }
        catch (e) { return pagina(`<h1>Não consegui registar</h1><p>Tente outra vez daqui a pouco, ou responda ao email com a palavra SIM.</p>`); }
        return pagina(`<h1>Obrigado ✨</h1><p>A partir de agora recebe de vez em quando os horóscopos, as novidades e as promoções do Mestre Alberto. Pode deixar de receber quando quiser, com o link no fim de cada email.</p><p><a class="botao" href="/novidades">Ver as novidades do site</a></p>`);
      }
      return pagina(`<h1>Quer receber as novidades?</h1><p>Horóscopos, novidades e promoções do Mestre Alberto, de vez em quando, por email. Pode deixar de receber quando quiser.</p><form method="post"><button type="submit">Sim, quero receber novidades</button></form><p><a href="/">genialtarot.com</a></p>`);
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
        // 13/11/2026 O-401/O-404 (OK dele): o vivo.js guarda no cookie gt_o de onde a pessoa veio (marca e código da ligação,
        // ou o site que a trouxe), até 30 dias. Todos os formulários passam por aqui, por isso a origem entra em todas as
        // capturas sem mexer em cada formulário. Só letras, números, / e - (o mesmo crivo do fila-capturas.py); nada da pessoa.
        try {
          if (data && typeof data === "object" && !/^[a-z0-9/-]{1,64}$/.test(String(data.origem || ""))) {
            const ck = (request.headers.get("cookie") || "").match(/(?:^|;\s*)gt_o=([a-z0-9/-]{1,64})(?:;|$)/);
            if (ck) data.origem = ck[1];
          }
        } catch (e) { /* a origem nunca estraga a captura */ }

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
              // 04/11/2026: o IP e a região, para o cerebro pôr o nome da ficha na visita do painel «Site» (nomes.json, só no cerebro)
              ip: request.headers.get("CF-Connecting-IP") || null,
              regiao: cf2.region || null,
            }), { expirationTtl: 60 * 60 * 24 * 30 });
          }
        } catch (e) { /* nunca estragar o pedido do visitante por causa da fila */ }

        // 30/10/2026: «resultado» é o texto da leitura para o email da pessoa — só vai para a fila
        // (o cerebro manda o email); não é aviso para o Telegram.
        if (type === "resultado") {
          return new Response(JSON.stringify({ ok: true }), { headers: { "Content-Type": "application/json" } });
        }

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
    // 🎯 09/09/2026 — O PUBLICO DO CANAL, para comparar com quem entra no site.
    // Ideia dele: "as entradas do site devem ser parecidas com as estatisticas
    // do canal". Nao sao, e e' isso que interessa ver -- 78% do canal e' Brasil
    // e no site o Brasil sao 2%.
    //
    // 🚨 PORQUE E' QUE ISTO NAO E' UM FICHEIRO DO SITE: seria publico. Fica no
    // mesmo armazem das capturas (KV), que so' se le com a senha dele, e quem
    // escreve e' o cerebro (youtube-publico.py) porque so' ele tem a chave do
    // canal -- o worker nunca ve credenciais do YouTube.
    if (url.pathname === "/api/youtube") {
      const j = (o, s) => new Response(JSON.stringify(o), {
        status: s || 200, headers: { "Content-Type": "application/json" } });
      if (!env.STATS_KEY || url.searchParams.get("chave") !== env.STATS_KEY) {
        return j({ ok: false, error: "chave errada" }, 403);
      }
      if (!env.CAPTURAS) return j({ ok: false, error: "falta o armazem" }, 500);
      if (request.method === "POST") {
        const corpo = await request.text();
        try { JSON.parse(corpo); } catch (e) { return j({ ok: false, error: "nao e' JSON" }, 400); }
        await env.CAPTURAS.put("youtube-publico", corpo);
        return j({ ok: true, guardado: corpo.length });
      }
      return j({ ok: true, canal: await env.CAPTURAS.get("youtube-publico", "json") });
    }

    if (url.pathname === "/api/stats") {
      const jsonResp = (obj, status) => new Response(JSON.stringify(obj), {
        status: status || 200, headers: { "Content-Type": "application/json" },
      });
      if (url.searchParams.get("debug") === "1") {
        return jsonResp({ ok: true, temToken: !!env.CF_API_TOKEN, temZona: !!env.CF_ZONE_ID,
                          temChave: !!env.STATS_KEY, temRum: !!env.CF_RUM_TOKEN });
      }
      // ?debug=rum&chave=... -> devolve a resposta do RUM em bruto, erros
      // incluidos. E' assim que se afina um nome de dimensao sem adivinhar.
      // ?debug=zona -> a resposta CRUA da consulta dos referrers/paginas.
      // E' assim que se sabe se este plano tem o httpRequestsAdaptiveGroups,
      // sem adivinhar. Mesma porta e mesma chave do debug=rum.
      if (url.searchParams.get("debug") === "zona") {
        if (!env.STATS_KEY || url.searchParams.get("chave") !== env.STATS_KEY) {
          return jsonResp({ ok: false, error: "chave errada" }, 403);
        }
        const desdeZ = new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10);
        const hojeZ = new Date().toISOString().slice(0, 10);
        const rz = await fetch("https://api.cloudflare.com/client/v4/graphql", {
          method: "POST",
          headers: { "Authorization": `Bearer ${env.CF_API_TOKEN}`, "Content-Type": "application/json" },
          body: JSON.stringify({
            query: "query($zona:String!,$desde:Date!){viewer{zones(filter:{zoneTag:$zona}){origens:httpRequestsAdaptiveGroups(limit:40,filter:{date_geq:$desde},orderBy:[count_DESC]){count dimensions{clientRefererHost}sum{visits}}}}}",
            variables: { zona: env.CF_ZONE_ID, desde: desdeZ },
          }),
        });
        return jsonResp({ ok: true, hoje: hojeZ, zona: await rz.json() });
      }

      if (url.searchParams.get("debug") === "rum") {
        if (!env.STATS_KEY || url.searchParams.get("chave") !== env.STATS_KEY) {
          return jsonResp({ ok: false, error: "chave errada" }, 403);
        }
        return jsonResp({ ok: true, rum: await estatisticasRum(env, 30) });
      }
      const chave = url.searchParams.get("chave") || "";
      if (!env.STATS_KEY || chave !== env.STATS_KEY) return jsonResp({ ok: false, error: "chave errada" }, 403);
      if (!env.CF_API_TOKEN || !env.CF_ZONE_ID) return jsonResp({ ok: false, error: "faltam CF_API_TOKEN / CF_ZONE_ID nas Variables and Secrets" }, 500);
      // ⚠️ 08/09/2026: isto subia QUALQUER pedido para um minimo de 7 dias, sem
      // o dizer a ninguem. O retrato que se guarda todas as noites no cofre
      // pede 1 dia e recebia 7 -- e ficava gravado com a etiqueta "1 dia".
      // Quem responde nao pode mentir na janela: se pedem 1, e' 1.
      const dias = Math.min(60, Math.max(1, Number(url.searchParams.get("dias")) || 30));
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
              // 08/09/2026: aqui estava `!p.endsWith(".html")`, e por isso esta
              // lista vinha SEMPRE vazia -- os enderecos deste site nao tem
              // extensao (/horoscopo.html responde 307 para /horoscopo). Agora
              // conta como pagina tudo o que nao tenha extensao de ficheiro.
              const ultimo = p.split("/").pop() || "";
              if (p !== "/" && ultimo.includes(".") && !p.endsWith(".html")) continue;
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

        // O RUM nunca deita a resposta abaixo: se falhar, a pagina mostra o
        // que ja mostrava e diz que essa parte nao veio.
        let rum = null;
        try { rum = await estatisticasRum(env, dias); } catch (e) { rum = { erro: String(e).slice(0, 200) }; }

        // O contador proprio (worker). Tambem nunca deita a resposta abaixo.
        let visitas = null;
        try { visitas = await estatisticasVisitas(env, dias); } catch (e) { visitas = { erro: String(e).slice(0, 200) }; }

        // o retrato do publico do canal, posto aqui pelo cerebro (ver /api/youtube)
        let canal = null;
        try { canal = env.CAPTURAS ? await env.CAPTURAS.get("youtube-publico", "json") : null; } catch (e) { canal = null; }

        return jsonResp({
          ok: true,
          canal,
          dias: grupos.map(g => ({ data: g.dimensions.date, paginas: g.sum.pageViews, pedidos: g.sum.requests, visitantes: g.uniq.uniques })),
          paises,
          porPagina,
          rum,
          visitas,
        });
      } catch (e) {
        return jsonResp({ ok: false, error: String(e) }, 502);
      }
    }

    if (url.pathname === "/Estataomp8") {
      return new Response(PAGINA_ESTATISTICAS, { headers: { "Content-Type": "text/html; charset=utf-8" } });
    }

    // 🌍🇧🇷🇵🇹 12/11/2026 (ele): três lojas sincronizadas — a mesma loja.html e o mesmo catálogo, muda só a forma de pagar.
    // A etiqueta «Loja Online» vai a /ir-loja: Brasil → /loja-brasil (só PIX), Portugal → /loja-portugal (sem PIX),
    // qualquer outro país ou origem desconhecida → /loja (Mundo, tudo).
    if (url.pathname === "/ir-loja") {
      const c = (request.cf && request.cf.country) || "";
      const alvo = c === "BR" ? "/loja-brasil" : c === "PT" ? "/loja-portugal" : "/loja";
      return new Response(null, { status: 302, headers: { Location: alvo + url.search, "Cache-Control": "private, no-store" } });
    }
    if ((url.pathname === "/loja-brasil" || url.pathname === "/loja-portugal") && (request.method === "GET" || request.method === "HEAD")) {
      const br = url.pathname === "/loja-brasil";
      const base = await env.ASSETS.fetch(new Request(new URL("/loja", url).toString(), { method: "GET" }));
      if (base.ok) {
        const tit = br ? "Loja Genial Tarot Brasil — pague com PIX · Mestre Alberto" : "Loja Genial Tarot Portugal — Cartão e MB WAY · Mestre Alberto";
        const des = br ? "A loja do Mestre Alberto para o Brasil: consultas de tarot, mapas astrais e rituais, com pagamento por PIX e preços em reais."
                       : "A loja do Mestre Alberto em Portugal: consultas de tarot, mapas astrais, rituais e amuletos, com pagamento por cartão, MB WAY ou transferência.";
        const can = "https://genialtarot.com" + url.pathname;
        const r = new Response(base.body, base);
        r.headers.delete("etag"); r.headers.delete("last-modified");
        return new HTMLRewriter()
          .on("html", { element(e) { e.setAttribute("data-loja", br ? "brasil" : "portugal"); } })
          .on("title", { element(e) { e.setInnerContent(tit); } })
          .on('meta[name="description"]', { element(e) { e.setAttribute("content", des); } })
          .on('link[rel="canonical"]', { element(e) { e.setAttribute("href", can); } })
          .on('meta[property="og:url"]', { element(e) { e.setAttribute("content", can); } })
          .on("h1", { element(e) { e.setInnerContent(br ? "A Loja do Genial Tarot · Brasil" : "A Loja do Genial Tarot · Portugal"); } })
          .transform(r);
      }
    }

    // Tudo o resto: servir o site normalmente
    const hAlvo = request.method === "GET" ? horoscopoNoHtmlAlvo(url) : -2;
    const resp = hAlvo !== -2 ? await horoscopoNoHtml(url, env, hAlvo)
      : request.method === "GET" && url.pathname === "/aniversarios" ? await aniversariosNoHtml(url, env)
      : request.method === "GET" && /^\/horoscopo-de-amanha\/[a-z]+$/.test(url.pathname) && H_SLUGS.includes(url.pathname.slice(21)) ? await amanhaSignoNoHtml(url, env, H_SLUGS.indexOf(url.pathname.slice(21)))
      : await env.ASSETS.fetch(request);
    // 01/11/2026: endereço de PÁGINA que não existe → a 404.html do site (com ligações de volta), sempre com código 404.
    // (Não pelo not_found_handling do wrangler: esse apanhava também /notify, /e/a, /api/vivo… e calava o worker.)
    // 02/11/2026: endereço do site antigo → 301 para a página nova equivalente (redirecoes-antigas.js)
    if (resp.status === 404 && (request.method === "GET" || request.method === "HEAD")) {
      let pa = url.pathname; try { pa = decodeURIComponent(pa); } catch (e) {}
      pa = pa.replace(/\/+$/, "") || "/";
      const novo = REDIR_ANTIGAS[pa];
      if (novo) return Response.redirect(new URL(novo, "https://genialtarot.com").toString(), 301);
    }
    if (resp.status === 404 && request.method === "GET" && !/\.[a-z0-9]{1,5}$/i.test(url.pathname)
        && !/^\/(api|e)\//.test(url.pathname)) {
      const p404 = await env.ASSETS.fetch(new Request(new URL("/404", url), { method: "GET" }));
      if (p404.ok) return new Response(p404.body, { status: 404, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
    }
    return resp;
  },
};

// ===== Web Analytics (o contador que vive nas paginas) =====
//
// 🚨 ISTO E' UMA GAVETA DIFERENTE DA DE CIMA. A consulta anterior pergunta a
// ZONA (o que o CDN ve passar: pedidos, paises). Esta pergunta ao RUM -- o que
// o browser das pessoas reporta: que pagina viram, de onde vieram, com que
// aparelho. Sao dois conjuntos de dados distintos, com tokens distintos:
//    CF_API_TOKEN  -> Zone Analytics:Read     (a zona)
//    CF_RUM_TOKEN  -> Account Analytics:Read  (o RUM)   ← posto a 22/08/2026
//
// ⚠️ E' ao nivel da CONTA, nao da zona -- por isso o accountTag.
//
// As chamadas vao SEPARADAS de proposito. Em GraphQL, um so nome de campo
// errado deita a consulta INTEIRA abaixo; separadas, um engano num nome custa
// um bloco e nao a pagina toda. As dimensoes do primeiro grupo estao
// confirmadas na documentacao; as do segundo (navegador e sistema) nao, e por
// isso e que vao a parte.
const RUM_SITE = "cb93958364f0480799bc19b864fb9c62";
const RUM_CONTA = "7ff4b84ec77c277416a1c036dfb36d18";

async function perguntarRum(token, consulta, variaveis) {
  const r = await fetch("https://api.cloudflare.com/client/v4/graphql", {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ query: consulta, variables: variaveis }),
  });
  const j = await r.json();
  if (j && j.errors && j.errors.length) {
    throw new Error(j.errors.map((e) => e.message).join(" | ").slice(0, 300));
  }
  const c = j && j.data && j.data.viewer && j.data.viewer.accounts && j.data.viewer.accounts[0];
  if (!c) throw new Error("resposta sem accounts: " + JSON.stringify(j).slice(0, 200));
  return c;
}

// Junta os grupos numa lista ordenada, com o nome ja limpo.
function arrumar(grupos, campo, limpar) {
  const mapa = {};
  for (const g of (grupos || [])) {
    let chave = (g.dimensions && g.dimensions[campo]) || "";
    if (limpar) chave = limpar(chave);
    if (chave === null) continue;
    const n = (g.sum && g.sum.visits) || g.count || 0;
    mapa[chave] = (mapa[chave] || 0) + n;
  }
  return Object.entries(mapa).sort((a, b) => b[1] - a[1]).slice(0, 12)
    .map(([nome, visitas]) => ({ nome, visitas }));
}

async function estatisticasRum(env, dias) {
  const token = env.CF_RUM_TOKEN;
  if (!token) return { erro: "falta CF_RUM_TOKEN" };
  const desde = new Date(Date.now() - dias * 864e5).toISOString();
  const erros = [];
  const fora = {};

  // --- grupo 1: dimensoes confirmadas ---
  const q1 = `query($c:String!,$s:String!,$d:Time!){viewer{accounts(filter:{accountTag:$c}){
    paginas:rumPageloadEventsAdaptiveGroups(limit:60,filter:{siteTag:$s,datetime_geq:$d},orderBy:[count_DESC]){count sum{visits} dimensions{requestPath}}
    origens:rumPageloadEventsAdaptiveGroups(limit:60,filter:{siteTag:$s,datetime_geq:$d},orderBy:[count_DESC]){count sum{visits} dimensions{refererHost}}
    aparelhos:rumPageloadEventsAdaptiveGroups(limit:20,filter:{siteTag:$s,datetime_geq:$d},orderBy:[count_DESC]){count sum{visits} dimensions{deviceType}}
    paises:rumPageloadEventsAdaptiveGroups(limit:30,filter:{siteTag:$s,datetime_geq:$d},orderBy:[count_DESC]){count sum{visits} dimensions{countryName}}
  }}}`;
  try {
    const c = await perguntarRum(token, q1, { c: RUM_CONTA, s: RUM_SITE, d: desde });
    fora.paginas = arrumar(c.paginas, "requestPath", (p) => (p || "/").split("?")[0]);
    fora.origens = arrumar(c.origens, "refererHost", (h) => {
      h = (h || "").toLowerCase().replace(/^www\./, "");
      if (h === "genialtarot.com" || h.endsWith(".workers.dev")) return null; // navegacao interna
      return h || "(direto)";
    });
    fora.aparelhos = arrumar(c.aparelhos, "deviceType");
    fora.paises = arrumar(c.paises, "countryName");
  } catch (e) { erros.push("grupo1: " + e.message); }

  // --- grupo 2: navegador e sistema (nomes por confirmar) ---
  const q2 = `query($c:String!,$s:String!,$d:Time!){viewer{accounts(filter:{accountTag:$c}){
    navegadores:rumPageloadEventsAdaptiveGroups(limit:20,filter:{siteTag:$s,datetime_geq:$d},orderBy:[count_DESC]){count sum{visits} dimensions{userAgentBrowser}}
    sistemas:rumPageloadEventsAdaptiveGroups(limit:20,filter:{siteTag:$s,datetime_geq:$d},orderBy:[count_DESC]){count sum{visits} dimensions{userAgentOS}}
  }}}`;
  try {
    const c = await perguntarRum(token, q2, { c: RUM_CONTA, s: RUM_SITE, d: desde });
    fora.navegadores = arrumar(c.navegadores, "userAgentBrowser");
    fora.sistemas = arrumar(c.sistemas, "userAgentOS");
  } catch (e) { erros.push("grupo2: " + e.message); }

  if (erros.length) fora.erros = erros;
  return fora;
}

// ===== Página privada de estatísticas =====
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
/* No telemovel o nome nao cabe ao lado da barra e ficava cortado a meio
   ("Pagina Princ...", "TikTok - lin..."). Passa para cima, em linha inteira,
   e a barra fica por baixo. Visto num ecra de 390 px antes de subir. */
@media (max-width: 480px) {
  .pais { flex-wrap: wrap; row-gap: 0.15rem; margin-bottom: 0.7rem; }
  .pais .nome { flex: 0 0 100%; white-space: normal; overflow: visible; }
  .pais .faixa { flex: 1 1 auto; }
}
.fonte { text-align: center; color: oklch(0.7 0.03 275); font-size: 0.66rem; font-style: italic; margin-top: 0.6rem; }
#canal-linhas .pct { flex-basis: 6rem; }   /* cabem os dois numeros: canal · site */
.nota { color: oklch(0.75 0.03 275); font-size: 0.75rem; margin-top: 0.6rem; text-align: center; }
#zona-dados { display: none; }
</style>
</head>
<body>
<div class="caixa">
  <h1>✦ Estatísticas do Genial Tarot ✦</h1>
  <p class="sub">visitas ao site — contador próprio + Cloudflare, só para os seus olhos</p>

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
      <div class="fonte">fonte: pedidos ao CDN da Cloudflare — inclui robôs, sondas e pré-carregamentos</div>
    </div>
    <div class="painel">
      <div class="titulo-sec">🧭 Contador próprio — pessoas e robôs</div>
      <div id="contador-dias"></div>
      <div class="nota" id="contador-nota"></div>
      <div class="fonte">fonte: contado dentro do servidor a cada página servida — sem JavaScript, sem amostragem e sem bloqueadores. A barra conta pessoas; passe o rato (ou toque) para ver os robôs.</div>
    </div>
    <div class="painel">
      <div class="titulo-sec">📄 Páginas mais visitadas</div>
      <div class="abas-pg"><b>Hoje</b></div>
      <div id="pgs-hoje"></div>
      <div class="abas-pg" style="margin-top:0.9rem"><b id="rot-periodo">No período</b></div>
      <div id="pgs-periodo"></div>
      <div class="fonte" id="f-paginas"></div>
    </div>
    <div class="painel">
      <div class="titulo-sec">🚪 Por onde chegam (origens)</div>
      <div id="origens"></div>
      <div style="text-align:center;color:oklch(0.7 0.03 275);font-size:0.68rem;font-style:italic;margin-top:0.5rem">"Direto" = escreveu o endereço, favoritos ou apps que não anunciam a origem (ex.: WhatsApp)</div>
      <div class="fonte" id="f-origens"></div>
    </div>
    <div class="painel">
      <div class="titulo-sec">🌍 De onde vêm os visitantes</div>
      <div id="paises"></div>
    </div>
    <div class="painel" id="painel-canal" style="display:none">
      <div class="titulo-sec">🎯 O teu público × quem entra no site</div>
      <div class="nota" id="canal-resumo"></div>
      <div class="abas-pg" style="margin-top:0.8rem"><b>&nbsp;</b><span style="float:right">canal · site</span></div>
      <div id="canal-linhas"></div>
      <div class="fonte" id="canal-fonte"></div>
    </div>
    <div class="painel" id="painel-aparelhos">
      <div class="titulo-sec">📱 Com que aparelho e programa</div>
      <div class="abas-pg"><b>Aparelho</b></div>
      <div id="aparelhos"></div>
      <div class="fonte" id="f-aparelhos"></div>
      <div id="bloco-navegadores">
        <div class="abas-pg" style="margin-top:0.9rem"><b>Navegador</b></div>
        <div id="navegadores"></div>
        <div class="abas-pg" style="margin-top:0.9rem"><b>Sistema</b></div>
        <div id="sistemas"></div>
        <div class="fonte">fonte: contador da Cloudflare nas páginas — morreu a 22/08, isto é histórico e não cresce mais</div>
      </div>
    </div>
  </div>

  <p class="rodape">Genial Tarot · página privada — não partilhe este endereço.</p>
</div>
<script>
var diasAtual = 30;
function fmt(n) { return n >= 10000 ? Math.round(n / 1000) + " mil" : String(n); }
function dataPt(iso) { var p = iso.split("-"); return p[2] + "/" + p[1]; }
function plural(n, um, muitos) { return n + " " + (n === 1 ? um : muitos); }
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
        "/anual.html": "📅 Previsão Anual", "/fimdesemana.html": "🌙 Fim de Semana", "/sobre.html": "👤 Sobre o Mestre",
        "/pagar.html": "💳 Pagamento", "/arcanos.html": "🎴 Os Arcanos", "/privacidade.html": "🔒 Privacidade",
        "/termos.html": "📜 Termos" };
      // Os 22 arcanos sao 22 linhas iguais; poe-se o nome a partir do endereco.
      //
      // 🚨 08/09/2026 -- AQUI DENTRO NAO SE ESCREVEM EXPRESSOES REGULARES.
      // Este guiao vive dentro de um template literal do worker (as crases),
      // e o JavaScript come as barras invertidas na viagem: o meu
      // /^\/arcano-\d\d-.../ chegou ao browser como /^/arcano-dd-.../ -- a
      // primeira barra fechou a expressao, deu "Invalid regular expression
      // flags", e o guiao INTEIRO da pagina deixou de correr. A pagina ficou
      // com a caixa da senha e o botao morto durante uma hora.
      // Se for mesmo preciso uma expressao regular, a barra invertida tem de
      // ser dobrada. Aqui nao e' precisa: fazem-se as contas com texto.
      function nomePagina(c) {
        if (NOMES_PG[c]) return NOMES_PG[c];
        if (NOMES_PG[c + ".html"]) return NOMES_PG[c + ".html"];
        var s = String(c);
        if (s.indexOf("/arcano-") === 0) {
          var t = s.slice(8);
          if (t.slice(-5) === ".html") t = t.slice(0, -5);
          var p = t.split("-");
          if (p.length > 1 && p[0].length && !isNaN(Number(p[0]))) p.shift();
          var nome = p.join(" ");
          return "🎴 " + nome.charAt(0).toUpperCase() + nome.slice(1);
        }
        return c;
      }
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
          var nome = nomePagina(p.caminho);
          linha.innerHTML = '<span class="nome">' + nome + '</span><span class="faixa"><span style="width:' + Math.max(3, Math.round(p.visitas / max * 100)) + '%"></span></span><span class="pct">' + p.visitas + '</span>';
          alvo.appendChild(linha);
        });
      }
      var NOMES_ORIG = { "(direto)": "🔗 Direto / desconhecido", "google.com": "🔎 Google", "google.pt": "🔎 Google",
        "facebook.com": "📘 Facebook", "m.facebook.com": "📘 Facebook", "l.facebook.com": "📘 Facebook", "lm.facebook.com": "📘 Facebook",
        "instagram.com": "📸 Instagram", "l.instagram.com": "📸 Instagram", "youtube.com": "▶️ YouTube", "m.youtube.com": "▶️ YouTube",
        "linktr.ee": "🌐 Linktree", "tiktok.com": "🎵 TikTok", "t.co": "🐦 X (Twitter)", "bing.com": "🔎 Bing", "duckduckgo.com": "🔎 DuckDuckGo",
        // Os links marcados (genialtarot.com/?de=tiktok). Estes nao dependem
        // do navegador dizer de onde veio: sao a atribuicao certa.
        "marca:tiktok": "🎵 TikTok — link marcado", "marca:youtube": "▶️ YouTube — link marcado",
        "marca:instagram": "📸 Instagram — link marcado", "marca:facebook": "📘 Facebook — link marcado",
        "marca:whatsapp": "💬 WhatsApp — link marcado", "marca:telegram": "✈️ Telegram — link marcado",
        "marca:email": "✉️ Email — link marcado", "marca:cartao": "🪪 Cartão — link marcado",
        "marca:bio": "🔗 Bio — link marcado", "marca:?": "⚠️ marca que eu não conheço (link mal escrito?)" };
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
      // 🚨 O RUM manda quando existe. Mede PESSOAS (o contador nas paginas);
      // o outro mede PEDIDOS que passam pelo CDN, e ai contam robos, sondas e
      // pre-carregamentos. Numeros diferentes para coisas diferentes -- nao se
      // somam nem se comparam.
      var R = j.rum || {};
      var temRum = !!(R.paginas && R.paginas.length) || !!(R.origens && R.origens.length);

      // 🚨 08/09/2026: acima de tudo manda o CONTADOR PROPRIO (worker). Conta
      // dentro do servidor a cada pagina servida: nao depende de JavaScript,
      // nao e' travado por bloqueadores, nao tem amostragem, e e' o unico que
      // sabe a ORIGEM. O RUM da Cloudflare morreu a 22/08 -- o beacon dispara
      // e o colector responde 404 -- por isso so serve de historico ate 21/08.
      // Ordem: contador proprio > RUM (historico) > zona (pedidos ao CDN).
      var V = j.visitas || {};
      function doContador(l) {   // {nome, n: "12"} -> {nome, visitas: 12}
        if (!Array.isArray(l)) return [];
        return l.filter(function (x) { return x && x.nome !== undefined && x.nome !== null; })
                .map(function (x) { return { nome: String(x.nome), visitas: Number(x.n) || 0 }; });
      }
      var vPaginas = doContador(V.paginas), vOrigens = doContador(V.origens),
          vAparelhos = doContador(V.aparelhos), vPaises = doContador(V.paises);
      var temVis = !!(vPaginas.length || vOrigens.length);
      function fonte(id, txt) { var e = document.getElementById(id); if (e) e.textContent = txt; }
      var F_VIS = "fonte: contador próprio, no servidor — robôs conhecidos deixados de fora";
      var F_RUM = "fonte: contador da Cloudflare nas páginas — parado desde 22/08, isto é histórico";
      var F_CDN = "fonte: pedidos ao CDN — inclui robôs";

      // Contador proprio, dia a dia: pessoas e robos lado a lado.
      var cd = document.getElementById("contador-dias");
      if (cd) {
        var porDia = {}, totPessoas = 0, totRobos = 0;
        (Array.isArray(V.dias) ? V.dias : []).forEach(function (r) {
          if (!r || !r.dia) return;
          var alvo = porDia[r.dia] || (porDia[r.dia] = { pessoa: 0, robo: 0, conf: 0 });
          var n = Number(r.n) || 0;
          if (r.quem === "robo") { alvo.robo += n; totRobos += n; } else { alvo.pessoa += n; totPessoas += n; }
        });
        // 01/11/2026 (ele): separar os suspeitos — confirmadas = páginas em que o vivo.js correu (navegador a sério);
        // suspeitos = entradas «pessoa» sem essa confirmação. Só existe desde 01/11/2026 de manhã.
        var INICIO_CONF = "2026-11-01", totConf = 0, totSusp = 0;
        (Array.isArray(V.confirmadas) ? V.confirmadas : []).forEach(function (r) {
          if (!r || !r.dia || !porDia[r.dia]) return; var n = Number(r.n) || 0; porDia[r.dia].conf += n;
        });
        var diasC = Object.keys(porDia).sort();
        cd.innerHTML = "";
        if (!diasC.length) {
          cd.innerHTML = '<div style="color:oklch(0.75 0.03 275);font-size:0.8rem;padding:0.3rem 0;text-align:center">' +
            (V.erro || (V.dias && V.dias.erro) ? "⚠️ o contador não respondeu" : "ainda sem dados — o contador próprio começou a 08/09/2026") + "</div>";
        } else {
          var maxC = 1;
          diasC.forEach(function (k) { if (porDia[k].pessoa > maxC) maxC = porDia[k].pessoa; });
          var legenda = document.createElement("div");
          legenda.style.cssText = "color:oklch(0.75 0.03 275);font-size:0.75rem;padding:0 0 0.4rem;text-align:center";
          legenda.textContent = "desde 01/11: 👤 pessoas confirmadas (navegador a sério) · 🕵️ suspeitos (robôs disfarçados, em pequenino)";
          cd.appendChild(legenda);
          diasC.forEach(function (k) {
            var l = document.createElement("div");
            l.className = "pais";
            l.title = plural(porDia[k].pessoa, "pessoa", "pessoas") + " · " +
              plural(porDia[k].robo, "robô travado", "robôs travados");
            l.innerHTML = '<span class="nome">' + dataPt(k) + '</span><span class="faixa"><span style="width:' +
              Math.max(3, Math.round((k >= INICIO_CONF ? porDia[k].conf : porDia[k].pessoa) / maxC * 100)) + '%"></span></span><span class="pct">' +
              (k >= INICIO_CONF ? "👤 " + porDia[k].conf + ' <small style="opacity:.6;font-size:0.7em">🕵️ ' + Math.max(0, porDia[k].pessoa - porDia[k].conf) + "</small>" : porDia[k].pessoa) + '</span>';
            if (k >= INICIO_CONF) { totConf += porDia[k].conf; totSusp += Math.max(0, porDia[k].pessoa - porDia[k].conf); }
            cd.appendChild(l);
          });
        }
        fonte("contador-nota", diasC.length
          ? plural(totPessoas, "pessoa", "pessoas") + " e " + plural(totRobos, "robô travado", "robôs travados") +
            " em " + plural(diasC.length, "dia", "dias") + (totConf + totSusp ? " · desde 01/11: " + totConf + " confirmadas, " + totSusp + " suspeitas" : "")
          : "");
      }

      function comoLista(l, campo) {   // uniformiza as duas origens de dados
        return (l || []).map(function (x) {
          return { nome: x.nome !== undefined ? x.nome : x[campo], visitas: x.visitas };
        });
      }
      function encherBarras(id, lista, enfeitar) {
        var alvo = document.getElementById(id);
        if (!alvo) return;
        alvo.innerHTML = "";
        if (!lista || !lista.length) {
          alvo.innerHTML = '<div style="color:oklch(0.75 0.03 275);font-size:0.8rem;padding:0.3rem 0">ainda sem dados</div>';
          return;
        }
        var max = lista[0].visitas || 1;
        lista.forEach(function (x) {
          var linha = document.createElement("div");
          linha.className = "pais";
          var nome = enfeitar ? enfeitar(x.nome) : x.nome;
          linha.innerHTML = '<span class="nome">' + nome + '</span><span class="faixa"><span style="width:' +
            Math.max(3, Math.round(x.visitas / max * 100)) + '%"></span></span><span class="pct">' + x.visitas + '</span>';
          alvo.appendChild(linha);
        });
      }

      document.getElementById("rot-periodo").textContent = "Nos últimos " + diasAtual + " dias";
      if (temVis) {
        encherBarras("pgs-periodo", vPaginas, function (c) { return nomePagina(c); });
        encherBarras("origens", vOrigens, function (o) { return NOMES_ORIG[o] || ("🌐 " + o); });
        document.getElementById("pgs-hoje").innerHTML =
          '<div style="color:oklch(0.75 0.03 275);font-size:0.8rem;padding:0.3rem 0">o detalhe de hoje aparece no período</div>';
        fonte("f-paginas", F_VIS); fonte("f-origens", F_VIS);
      } else if (temRum) {
        encherBarras("pgs-periodo", comoLista(R.paginas), function (c) { return nomePagina(c); });
        encherBarras("origens", comoLista(R.origens), function (o) { return NOMES_ORIG[o] || ("🌐 " + o); });
        document.getElementById("pgs-hoje").innerHTML =
          '<div style="color:oklch(0.75 0.03 275);font-size:0.8rem;padding:0.3rem 0">o detalhe de hoje aparece no período</div>';
        fonte("f-paginas", F_RUM); fonte("f-origens", F_RUM);
      } else {
        encherOrigens(j.porPagina && j.porPagina.origens);
        encherPgs("pgs-hoje", j.porPagina && j.porPagina.hoje);
        encherPgs("pgs-periodo", j.porPagina && j.porPagina.periodo);
        fonte("f-paginas", F_CDN); fonte("f-origens", F_CDN);
      }
      // O contador proprio escreve "computador"/"telemovel"; o RUM escrevia em ingles.
      var APAR = { desktop: "🖥️ Computador", computador: "🖥️ Computador", mobile: "📱 Telemóvel",
        telemovel: "📱 Telemóvel", tablet: "📲 Tablet", other: "❓ Outro", "?": "❓ Não diz" };
      encherBarras("aparelhos", temVis ? vAparelhos : comoLista(R.aparelhos),
        function (a) { return APAR[String(a).toLowerCase()] || a; });
      fonte("f-aparelhos", temVis ? F_VIS : F_RUM);
      // Navegador e sistema so o RUM os sabia. Sem RUM, esconder em vez de
      // deixar duas listas vazias para sempre.
      var bn = document.getElementById("bloco-navegadores");
      if (bn) bn.style.display = temRum ? "block" : "none";
      encherBarras("navegadores", comoLista(R.navegadores));
      encherBarras("sistemas", comoLista(R.sistemas));
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

      // 🎯 O PUBLICO DO CANAL AO LADO DE QUEM ENTRA NO SITE (09/09/2026).
      // ⚠️ So' se comparam PROPORCOES: de um lado sao visualizacoes de video,
      // do outro sao visitas a paginas. Os totais nao se comparam.
      var C = j.canal;
      var pc = document.getElementById("painel-canal");
      if (pc && C && C.paises && C.paises.length && vPaises.length) {
        var mapaC = {}, totC = 0;
        C.paises.forEach(function (x) { mapaC[x[0]] = x[1]; totC += x[1]; });
        var mapaS = {}, totS = 0;
        vPaises.forEach(function (x) { mapaS[x.nome] = x.visitas; totS += x.visitas; });
        var juntos = {};
        Object.keys(mapaC).forEach(function (k) { juntos[k] = 1; });
        Object.keys(mapaS).forEach(function (k) { juntos[k] = 1; });
        var linhasC = Object.keys(juntos).map(function (k) {
          return { pais: k,
                   canal: (mapaC[k] || 0) * 100 / (totC || 1),
                   site: (mapaS[k] || 0) * 100 / (totS || 1) };
        }).sort(function (a, b) {
          return Math.max(b.canal, b.site) - Math.max(a.canal, a.site);
        }).slice(0, 7);
        var alvoC = document.getElementById("canal-linhas");
        alvoC.innerHTML = "";
        var nomesP; try { nomesP = new Intl.DisplayNames(["pt"], { type: "region" }); } catch (e) { nomesP = null; }
        linhasC.forEach(function (x) {
          var band = x.pais.length === 2
            ? String.fromCodePoint(127397 + x.pais.charCodeAt(0), 127397 + x.pais.charCodeAt(1)) : "🌐";
          var nm = x.pais; try { if (nomesP) nm = nomesP.of(x.pais) || x.pais; } catch (e) {}
          var li = document.createElement("div");
          li.className = "pais";
          li.innerHTML = '<span class="nome">' + band + " " + nm + '</span>' +
            '<span class="faixa"><span style="width:' + Math.max(2, Math.round(x.canal)) + '%"></span></span>' +
            '<span class="pct">' + Math.round(x.canal) + "% · " + Math.round(x.site) + '%</span>';
          alvoC.appendChild(li);
        });
        var seuC = ((mapaC.PT || 0) + (mapaC.BR || 0)) * 100 / (totC || 1);
        var seuS = ((mapaS.PT || 0) + (mapaS.BR || 0)) * 100 / (totS || 1);
        document.getElementById("canal-resumo").innerHTML =
          "Portugal e Brasil são <b>" + Math.round(seuC) + "%</b> de quem te vê no canal, " +
          "mas só <b>" + Math.round(seuS) + "%</b> de quem entra no site.";
        document.getElementById("canal-fonte").textContent =
          "canal: visualizações dos últimos " + (C.dias || 28) + " dias · site: o período escolhido em cima · "
          + "a barra desenha o canal; os números são canal · site";
        pc.style.display = "block";
      }
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

// =====================================================================
// 31/10/2026, pedido dele: «quem está no site AGORA — IP, país — e um chat
// para escrever directamente a essa pessoa, como no chat da aplicação».
//
// Tudo numa sala só (Durable Object «Sala», com SQLite). O /vivo.js de cada
// página diz «estou aqui» de 20 em 20 s; o painel dele (no cerebro, pelo HA)
// lê com a chave das estatísticas (STATS_KEY). Os IPs só se guardam 24 h; as conversas 30 dias.
// =====================================================================
export class Sala extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.escreve = new Map();   // "sid|quem" -> quando escreveu a última tecla (para os «…»)
    this.sql.exec(`CREATE TABLE IF NOT EXISTS vis (sid TEXT PRIMARY KEY, ip TEXT, pais TEXT, cidade TEXT, regiao TEXT,
      aparelho TEXT, ua TEXT, pagina TEXT, titulo TEXT, origem TEXT, primeiro INTEGER, visto INTEGER, n INTEGER, paginas TEXT)`);
    try { this.sql.exec("ALTER TABLE vis ADD COLUMN humano INTEGER DEFAULT 0"); } catch (e) { /* já existe */ }   // 01/11: confirmou ser pessoa
    this.sql.exec(`CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, sid TEXT, quando INTEGER, de TEXT, texto TEXT)`);
    this.sql.exec(`CREATE TABLE IF NOT EXISTS aberto (sid TEXT PRIMARY KEY, aberto INTEGER)`);
    // 03/11/2026 20h: a quota grátis de LEITURAS do Durable Object esgotou («Exceeded allowed rows read»). O painel do HA
    // pergunta de 3 em 3 s e cada pergunta lia a tabela INTEIRA (30 dias, robôs incluídos) por falta de índice na data;
    // e cada visitante novo fazia um COUNT(*) à tabela toda. Índices + contagem guardada em memória.
    this.sql.exec("CREATE INDEX IF NOT EXISTS vis_visto ON vis(visto)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS chat_sid ON chat(sid)");
    this.total = null;
  }
  linhas(q, ...a) { return [...this.sql.exec(q, ...a)]; }
  limpar(agora) {
    if (this.ultimaLimpeza && agora - this.ultimaLimpeza < 600000) return;
    this.ultimaLimpeza = agora;
    this.sql.exec("DELETE FROM vis WHERE visto < ?", agora - 30 * 864e5);   // 01/11 (ele): histórico de 30 dias (era 24 h); a regra dos 30 dias
    this.sql.exec("DELETE FROM chat WHERE quando < ?", agora - 30 * 864e5);
    this.total = this.linhas("SELECT COUNT(*) AS c FROM vis")[0].c;   // 03/11: contado aqui (de 10 em 10 min), não a cada visitante
  }
  async fetch(request) {
    const url = new URL(request.url), p = url.pathname, agora = Date.now();
    const J = (o, s) => new Response(JSON.stringify(o), { status: s || 200, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
    const d = request.method === "POST" ? await request.json().catch(() => ({})) : {};
    const sid = String(d.sid || url.searchParams.get("sid") || "");
    const sidOk = /^[a-z0-9]{12,40}$/.test(sid);
    this.limpar(agora);
    // ---------- do lado de quem visita ----------
    if (p === "/api/vivo") {
      if (!sidOk) return J({ ok: false }, 400);
      const cf = request.cf || {}, ua = request.headers.get("user-agent") || "";
      const pagina = String(d.pagina || "/").slice(0, 120), titulo = String(d.titulo || "").slice(0, 120);
      const r = this.linhas("SELECT paginas, n, pagina FROM vis WHERE sid=?", sid)[0];
      if (r) {
        let ps = []; try { ps = JSON.parse(r.paginas || "[]"); } catch (e) {}
        if (r.pagina !== pagina) { ps.push([agora, pagina]); ps = ps.slice(-30); }
        this.sql.exec("UPDATE vis SET ip=?, pais=?, cidade=?, regiao=?, pagina=?, titulo=?, visto=?, n=?, paginas=? WHERE sid=?",
          request.headers.get("CF-Connecting-IP") || "?", cf.country || "?", cf.city || "", cf.region || "", pagina, titulo, agora,
          (r.n || 0) + (r.pagina !== pagina ? 1 : 0), JSON.stringify(ps), sid);
      } else {
        if ((this.total || 0) > 30000) return J({ ok: false }, 429);
        this.total = (this.total || 0) + 1;
        // 01/11: com a lista das colunas — a coluna «humano» acrescentada deixava o INSERT sem colunas a rebentar (erro 1101)
        try {
          this.sql.exec("INSERT INTO vis (sid, ip, pais, cidade, regiao, aparelho, ua, pagina, titulo, origem, primeiro, visto, n, paginas) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", sid, request.headers.get("CF-Connecting-IP") || "?",
            cf.country || "?", cf.city || "", cf.region || "", aparelhoDe(ua), ua.slice(0, 160), pagina, titulo,
            String(d.origem || "").slice(0, 80), agora, agora, 1, JSON.stringify([[agora, pagina]]));
        } catch (e) { return J({ ok: false, erro: String(e && e.message || e).slice(0, 200) }, 500); }   // 01/11: o erro à vista, em vez do 1101 mudo
      }
      if (d.confirma) this.sql.exec("UPDATE vis SET humano=1 WHERE sid=?", sid);
      const ab = this.linhas("SELECT aberto FROM aberto WHERE sid=?", sid)[0];
      return J({ ok: true, aberto: !!(ab && ab.aberto) });
    }
    if (p === "/api/vivo/chat" && request.method === "GET") {
      if (!sidOk) return J({ ok: false }, 400);
      const ab = this.linhas("SELECT aberto FROM aberto WHERE sid=?", sid)[0];
      const msgs = this.linhas("SELECT id, quando, de, texto FROM chat WHERE sid=? AND id>? ORDER BY id", sid, Number(url.searchParams.get("desde")) || 0);
      return J({ aberto: !!(ab && ab.aberto), msgs, escreve: agora - (this.escreve.get(sid + "|mestre") || 0) < 4000 });
    }
    if (p === "/api/vivo/chat" && request.method === "POST") {
      const t = String(d.texto || "").trim().slice(0, 1000);
      const ab = sidOk && this.linhas("SELECT aberto FROM aberto WHERE sid=?", sid)[0];
      if (!ab || !ab.aberto || !t) return J({ ok: false }, 400);   // só se responde a uma conversa que ELE abriu
      this.sql.exec("INSERT INTO chat (sid, quando, de, texto) VALUES (?,?,?,?)", sid, agora, "pessoa", t);
      return J({ ok: true });
    }
    if (p === "/api/vivo/escreve") { if (sidOk) this.escreve.set(sid + "|pessoa", agora); return J({ ok: true }); }
    if (p === "/api/vivo/fechar") {
      if (sidOk) this.sql.exec("INSERT OR REPLACE INTO aberto VALUES (?,0)", sid);
      if (sidOk) this.sql.exec("INSERT INTO chat (sid, quando, de, texto) VALUES (?,?,?,?)", sid, agora, "sistema", "fechou o chat ✕");
      return J({ ok: true });
    }
    // ---------- do lado dele (o painel) ----------
    if (!this.env.STATS_KEY || request.headers.get("X-Chave") !== this.env.STATS_KEY) return J({ ok: false, erro: "chave" }, 403);
    if (p === "/api/vivo/painel") {
      const dias = Math.min(30, Math.max(1, parseInt(url.searchParams.get("dias")) || 1));
      const vis = this.linhas("SELECT sid, ip, pais, cidade, regiao, aparelho, ua, humano, pagina, titulo, origem, primeiro, visto, n, paginas FROM vis WHERE visto >= ? ORDER BY visto DESC LIMIT ?",
        agora - dias * 864e5, dias === 1 ? 600 : 5000);
      const abertos = new Set(this.linhas("SELECT sid FROM aberto WHERE aberto=1").map((r) => r.sid));
      const ult = {}; for (const r of this.linhas("SELECT sid, MAX(id) AS id, MAX(quando) AS q FROM chat WHERE de='pessoa' GROUP BY sid")) ult[r.sid] = r.q;
      const entrada = (t) => { try { return JSON.parse(t || "[]")[0][1]; } catch (e) { return ""; } };   // 01/11: a página onde a visita entrou
      return J({ agora, vis: vis.map(({ paginas, ...v }) => ({ ...v, entrada: entrada(paginas), online: agora - v.visto < 45000, chat: abertos.has(v.sid), respondeu: ult[v.sid] || 0 })) });
    }
    if (p === "/api/vivo/pessoa") {
      const v = this.linhas("SELECT * FROM vis WHERE sid=?", sid)[0] || null;
      const ab = this.linhas("SELECT aberto FROM aberto WHERE sid=?", sid)[0];
      return J({ v, aberto: !!(ab && ab.aberto), chat: this.linhas("SELECT id, quando, de, texto FROM chat WHERE sid=? ORDER BY id", sid),
        escreve: agora - (this.escreve.get(sid + "|pessoa") || 0) < 4000 });
    }
    if (p === "/api/vivo/mestre") {
      if (!sidOk) return J({ ok: false }, 400);
      this.sql.exec("INSERT OR REPLACE INTO aberto VALUES (?,1)", sid);
      const t = String(d.texto || "").trim().slice(0, 1000);
      if (t) this.sql.exec("INSERT INTO chat (sid, quando, de, texto) VALUES (?,?,?,?)", sid, agora, "mestre", t);
      return J({ ok: true });
    }
    if (p === "/api/vivo/mfechar") { if (sidOk) this.sql.exec("INSERT OR REPLACE INTO aberto VALUES (?,0)", sid); return J({ ok: true }); }
    if (p === "/api/vivo/mescreve") { if (sidOk) this.escreve.set(sid + "|mestre", agora); return J({ ok: true }); }
    return J({ ok: false }, 404);
  }
}

// ---------------------------------------------------------------------------------------------------------------------
// 05/11/2026, pedido dele: o Consultório Virtual. Ele cria um link para UMA pessoa; ela entra na sala de espera; ele é
// avisado; ao atender, as portas abrem-se e os dois escrevem e mandam áudio. Durable Object À PARTE da Sala: não mexe no
// chat do site, e uma avaria aqui não cala o /api/vivo.
// ⚠️ Plano GRÁTIS (5 M linhas lidas/dia, partilhadas com a Sala; ver a nota de 03/11): nada de ler tabelas inteiras. Tudo
// vai por chave primária ou índice, a presença fica em MEMÓRIA (nunca uma escrita por pergunta), e as esperas entre
// perguntas são decididas no navegador (consultorio-sala.html). Sem R2: o áudio vive aqui, partido em pedaços, porque cada
// linha do SQLite do Durable Object tem de ficar abaixo de 2 MB.
// As escolhas por defeito (ele ainda pode mudar) estão todas nesta tabela:
const CONSULTORIO = {
  VALIDADE_H: 24,            // o link vale 24 h desde que é criado, ou até ele fechar a conversa
  CONVERSA_H: 6,             // uma conversa aberta perto do fim da validade ganha pelo menos mais estas horas
  RETENCAO_DIAS: 30,         // escrita e voz apagam-se aos 30 dias (está em privacidade.html: mudar lá também)
  TEXTO_MAX: 2000,           // letras por mensagem
  AUDIO_MAX_S: 90,           // o navegador pára aos 90 s; o servidor dá uma pequena folga
  AUDIO_MAX_BYTES: 3 << 20,  // 3 MB chegam para 90 s, mesmo no iPhone, que às vezes ignora o débito pedido
  PEDACO: 256 << 10,         // bem abaixo do limite de 2 MB por linha
  AUDIOS_MAX: 80,            // por conversa e por pessoa: para um link esquecido não encher o armazenamento
  ANEXO_MAX_BYTES: 3 << 20,  // fotos (já reduzidas no navegador) e PDF
  ANEXOS_MAX: 40,            // por conversa e por lado
  CHAMADA_TOCA_MS: 60000,    // sem atender, a chamada corta aqui
  CHAMADA_LIGAR_MS: 60000,   // depois de atender, tempo máximo até os dois aparelhos se ligarem
  CHAMADA_SOZINHA_MS: 90000, // chamada ligada de que um dos lados deixou de perguntar
  SDP_MAX: 32768,            // oferta ou resposta, com todos os candidatos lá dentro
  ESPERA_MIN: 5,             // contador da sala de espera, se ele não escolher outro tempo
  ESPERA_OCUPADO_MIN: 15,    // com outra pessoa no consultório, a contagem nunca começa abaixo disto
  ESPERA_MAX_MIN: 180,       // tecto da soma de minutos no painel
  TIPOS_AUDIO: ["audio/mp4", "audio/webm", "audio/ogg", "audio/aac", "audio/mpeg"],
};
const CODIGO_OK = /^[a-hjkmnp-z2-9]{20}$/;
// O tipo de um anexo decide-se pelos primeiros bytes, nunca pelo nome nem pelo que o navegador declara. SVG e HTML não passam aqui.
function tipoAnexo(b) {
  const ini = (...x) => x.every((v, i) => b[i] === v);
  if (ini(0xff, 0xd8, 0xff)) return "image/jpeg";
  if (ini(0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a)) return "image/png";
  if (ini(0x52, 0x49, 0x46, 0x46) && b[8] === 0x57 && b[9] === 0x45 && b[10] === 0x42 && b[11] === 0x50) return "image/webp";
  if (ini(0x25, 0x50, 0x44, 0x46, 0x2d)) return "application/pdf";
  return "";
}
function novoCodigo() {   // 20 letras de 31 (sem i, l, o, 0, 1), ~99 bits: impossível de adivinhar
  const A = "abcdefghjkmnpqrstuvwxyz23456789"; let c = "";
  while (c.length < 20) for (const b of crypto.getRandomValues(new Uint8Array(24))) { if (b < 248 && c.length < 20) c += A[b % 31]; }
  return c;
}
export class Consultorio extends DurableObject {
  // 06/11 (ele): chat instantâneo. A ligação directa só avisa «há novidade» e cada lado vai logo buscá-la pelo /estado de sempre;
  // as perguntas de 3 em 3 segundos ficam como rede de segurança e continuam a medir quem está presente.
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/api/consultorio/ws") {
      if ((request.headers.get("Upgrade") || "").toLowerCase() !== "websocket") return new Response("", { status: 426 });
      const c = String(url.searchParams.get("c") || "");
      if (!this.consulta(c, Date.now())) return new Response("", { status: 404 });
      if (this.ctx.getWebSockets(c).length >= 8) return new Response("", { status: 429 });
      const par = new WebSocketPair();
      this.ctx.acceptWebSocket(par[1], [c]);
      return new Response(null, { status: 101, webSocket: par[0] });
    }
    const o = {}, res = await this.tratar(request, o);
    if (o.c) for (const ws of this.ctx.getWebSockets(o.c)) { try { ws.send("1"); } catch (e) {} }
    return res;
  }
  webSocketMessage(ws, m) { if (m === "p") { try { ws.send("k"); } catch (e) {} } }
  webSocketClose(ws) { try { ws.close(); } catch (e) {} }
  webSocketError(ws) { try { ws.close(); } catch (e) {} }
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.visto = new Map();     // código -> quando a pessoa perguntou por último (em memória: uma escrita por pergunta gastava a quota)
    this.vistoM = new Map();    // o mesmo para ele
    this.escreve = new Map();   // "código|quem" -> a última tecla (para os «…»)
    this.sql.exec(`CREATE TABLE IF NOT EXISTS consultas (codigo TEXT PRIMARY KEY, mtoken TEXT, etiqueta TEXT, estado TEXT, criado INTEGER, expira INTEGER,
      entrou INTEGER, aceitou INTEGER, atendido INTEGER, fechado INTEGER, pais TEXT, aparelho TEXT, ult_pessoa INTEGER DEFAULT 0, audios_p INTEGER DEFAULT 0, audios_m INTEGER DEFAULT 0)`);
    this.sql.exec(`CREATE TABLE IF NOT EXISTS msgs (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo TEXT, quando INTEGER, de TEXT, tipo TEXT, texto TEXT, mime TEXT, dur REAL, tam INTEGER)`);
    this.sql.exec("CREATE TABLE IF NOT EXISTS audio (msg INTEGER, pos INTEGER, dados BLOB, PRIMARY KEY (msg, pos))");
    // 05/11: o contador da sala. A tabela já existe no site publicado, daí o ALTER (como na Sala). fim_espera é o relógio do servidor:
    // sobrevive a recarregar a página, e o navegador só desconta os segundos sem perguntar nada.
    try { this.sql.exec("ALTER TABLE consultas ADD COLUMN espera_min INTEGER"); } catch (e) { /* já existe */ }
    try { this.sql.exec("ALTER TABLE consultas ADD COLUMN fim_espera INTEGER"); } catch (e) { /* já existe */ }
    try { this.sql.exec("ALTER TABLE consultas ADD COLUMN anexos_p INTEGER DEFAULT 0"); } catch (e) { /* já existe */ }
    try { this.sql.exec("ALTER TABLE consultas ADD COLUMN anexos_m INTEGER DEFAULT 0"); } catch (e) { /* já existe */ }
    // 05/11: chamadas de voz e vídeo (WebRTC, um para um). Só a sinalização passa por aqui; o som e a imagem vão directamente entre os
    // dois aparelhos e NÃO são gravados. Uma linha por conversa, com a oferta e a resposta já com todos os candidatos: são duas escritas
    // por chamada em vez de uma por candidato. A linha apaga-se no fim da chamada, com os endereços de rede que lá vinham.
    this.sql.exec(`CREATE TABLE IF NOT EXISTS chamadas (codigo TEXT PRIMARY KEY, id INTEGER, modo TEXT, estado TEXT, criada INTEGER, atendida INTEGER, ligada INTEGER,
      ver INTEGER DEFAULT 1, pede INTEGER DEFAULT 0, oferta TEXT, resposta TEXT, tem TEXT)`);
    this.sql.exec("CREATE INDEX IF NOT EXISTS msgs_cod ON msgs(codigo, id)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS msgs_q ON msgs(quando)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS cons_estado ON consultas(estado)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS cons_criado ON consultas(criado)");
  }
  linhas(q, ...a) { return [...this.sql.exec(q, ...a)]; }
  minutos(v) { const n = Math.floor(Number(v)); return n >= 1 && n <= CONSULTORIO.ESPERA_MAX_MIN ? n : 0; }
  // A regra dos 30 dias não pode depender de haver visitas: o alarme acorda o objecto mesmo que ninguém cá venha.
  limpar(agora) {
    const lim = agora - CONSULTORIO.RETENCAO_DIAS * 864e5;
    this.sql.exec("DELETE FROM audio WHERE msg IN (SELECT id FROM msgs WHERE quando < ? AND tipo IN ('audio','anexo'))", lim);
    this.sql.exec("DELETE FROM msgs WHERE quando < ?", lim);
    this.sql.exec("DELETE FROM chamadas WHERE criada < ?", agora - 864e5);   // sobra de uma chamada abandonada; os endereços de rede não ficam
    this.sql.exec("DELETE FROM consultas WHERE criado < ? AND NOT EXISTS (SELECT 1 FROM msgs m WHERE m.codigo = consultas.codigo)", lim);
    for (const [k, v] of this.visto) if (agora - v > 864e5) this.visto.delete(k);
    for (const [k, v] of this.vistoM) if (agora - v > 864e5) this.vistoM.delete(k);
    for (const [k, v] of this.escreve) if (agora - v > 60000) this.escreve.delete(k);
    this.ultimaLimpeza = agora;
  }
  async alarm() {
    const agora = Date.now(); this.limpar(agora);
    if (this.linhas("SELECT 1 AS h FROM consultas LIMIT 1").length) await this.ctx.storage.setAlarm(agora + 864e5);
  }
  // Uma linha da consulta, já com a validade aplicada (expira sozinha, sem depender de ninguém).
  consulta(c, agora) {
    if (!CODIGO_OK.test(c)) return null;
    const r = this.linhas("SELECT * FROM consultas WHERE codigo=?", c)[0];
    if (r && agora > r.expira && ["criado", "espera", "conversa"].includes(r.estado)) {
      this.sql.exec("UPDATE consultas SET estado='expirado' WHERE codigo=?", c); r.estado = "expirado";
    }
    return r || null;
  }
  // A chamada em curso, com os limites de tempo aplicados aqui, para não dependerem de nenhum navegador.
  chamadaViva(c, agora) {
    const ch = this.linhas("SELECT * FROM chamadas WHERE codigo=?", c)[0];
    if (!ch) return null;
    const v = this.visto.get(c), m = this.vistoM.get(c), so = CONSULTORIO.CHAMADA_SOZINHA_MS;
    if (ch.estado === "toca" && agora - ch.criada > CONSULTORIO.CHAMADA_TOCA_MS) return this.fimChamada(c, ch, "perdida", agora);
    if (ch.estado === "atendeu" && agora - ch.atendida > CONSULTORIO.CHAMADA_LIGAR_MS) return this.fimChamada(c, ch, "falhou", agora);
    if (ch.estado === "ligada" && ((v && agora - v > so) || (m && agora - m > so))) return this.fimChamada(c, ch, "terminada", agora);
    return ch;
  }
  fimChamada(c, ch, motivo, agora) {
    const nome = ch.modo === "video" ? "Videochamada" : "Chamada de voz", dur = ch.ligada ? Math.round((agora - ch.ligada) / 1000) : 0;
    const t = (ch.modo === "cartas"   // 06/11 (ele): câmara só do Mestre, para mostrar as cartas; nada da pessoa é pedido e a imagem não é gravada
      ? { terminada: "Cartas mostradas", recusada: "Cartas não mostradas", perdida: "Cartas não mostradas", cancelada: "Cartas não mostradas", falhou: "Cartas: não foi possível ligar" }
      : { terminada: nome + " terminada", recusada: nome + " recusada", perdida: nome + " sem resposta", cancelada: nome + " cancelada", falhou: nome + ": não foi possível ligar" })[motivo];
    this.sql.exec("DELETE FROM chamadas WHERE codigo=?", c);
    this.novaMsg(c, agora, "sistema", "chamada", dur ? t + " · " + Math.floor(dur / 60) + ":" + String(dur % 60).padStart(2, "0") : t, motivo, dur);   // mime leva o motivo
    return null;
  }
  novaMsg(c, agora, de, tipo, texto, mime, dur, tam) {
    return this.linhas("INSERT INTO msgs (codigo, quando, de, tipo, texto, mime, dur, tam) VALUES (?,?,?,?,?,?,?,?) RETURNING id", c, agora, de, tipo, texto, mime || "", dur || 0, tam || 0)[0].id;
  }
  async tratar(request, aviso) {
    const url = new URL(request.url), p = url.pathname.replace("/api/consultorio/", ""), agora = Date.now();
    const J = (o, s) => new Response(JSON.stringify(o), { status: s || 200, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", "X-Robots-Tag": "noindex" } });
    if (!this.ultimaLimpeza || agora - this.ultimaLimpeza > 600000 || p === "reabrir") this.limpar(agora);
    const chaveOk = !!this.env.STATS_KEY && request.headers.get("X-Chave") === this.env.STATS_KEY;
    const binario = p === "audio" && request.method === "POST", semJson = binario || (p === "anexo" && request.method === "POST");
    const d = request.method === "POST" && !semJson ? await request.json().catch(() => ({})) : {};
    const c = String(d.c || url.searchParams.get("c") || ""), m = String(d.m || url.searchParams.get("m") || "");
    if (request.method === "POST") aviso.c = c;   // qualquer escrita desta conversa avisa quem está ligado

    // ---------- só com a chave (o painel do HA, pelo servidor.py) ----------
    if (p === "criar" || p === "lista" || p === "vigia") {
      if (!chaveOk) return J({ ok: false, erro: "chave" }, 403);
      if (p === "criar") {
        const codigo = novoCodigo(), mtoken = [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, "0")).join("");
        const expira = agora + CONSULTORIO.VALIDADE_H * 36e5;
        this.sql.exec("INSERT INTO consultas (codigo, mtoken, etiqueta, estado, criado, expira, espera_min) VALUES (?,?,?,'criado',?,?,?)", codigo, mtoken, String(d.etiqueta || "").trim().slice(0, 60), agora, expira, this.minutos(d.minutos) || CONSULTORIO.ESPERA_MIN);
        if (!(await this.ctx.storage.getAlarm())) await this.ctx.storage.setAlarm(agora + 864e5);
        return J({ ok: true, codigo, mtoken, expira, url: "/consultorio/" + codigo });
      }
      if (p === "vigia") {   // o vigia do cerebro pergunta muito: só as linhas em curso, pelo índice do estado
        const r = this.linhas("SELECT codigo, etiqueta, estado, entrou, expira FROM consultas WHERE estado IN ('criado','espera','conversa')").filter((x) => agora <= x.expira);
        // ?f=1 (de vez em quando): as conversas fechadas nas últimas 24 h, porque ele também as fecha na página https, onde o cerebro não vê
        const fechadas = url.searchParams.get("f") ? this.linhas("SELECT codigo, fechado FROM consultas WHERE estado='fechado' AND fechado > ?", agora - 864e5) : undefined;
        return J({ ok: true, agora, ativos: r.length, fechadas, espera: r.filter((x) => x.estado === "espera").map(({ codigo, etiqueta, entrou }) => ({ codigo, etiqueta, entrou, online: agora - (this.visto.get(codigo) || 0) < 45000 })) });
      }
      const r = this.linhas("SELECT codigo, mtoken, etiqueta, estado, criado, expira, entrou, atendido, fechado, pais, aparelho, ult_pessoa, espera_min, fim_espera FROM consultas ORDER BY criado DESC LIMIT 30");
      return J({ ok: true, agora, consultas: r.map((x) => {
        const v = this.visto.get(x.codigo) || 0;
        if (agora > x.expira && ["criado", "espera", "conversa"].includes(x.estado)) x.estado = "expirado";
        return { ...x, visto: v, online: agora - v < 45000, reabrivel: ["fechado", "expirado"].includes(x.estado) };   // a linha só existe enquanto a retenção não a apagou
      }) });
    }

    const r = this.consulta(c, agora);
    if (!r) return J({ ok: false, estado: "invalido" }, 404);
    const mestre = chaveOk || (m.length === 32 && m === r.mtoken);   // o mtoken abre a mesma conversa numa página HTTPS (o microfone no HA em http não funciona)
    const de = mestre ? "mestre" : "pessoa";
    const viva = r.estado === "conversa";

    // 06/11 (ele): servidor intermédio da Cloudflare, para as redes que bloqueiam a ligação directa. A credencial dura 4 horas e sai daqui,
    // para a chave nunca chegar ao navegador. Sem chave, as chamadas seguem como antes, só com ligação directa.
    if (p === "ice" && request.method === "GET") {
      if (!viva || !this.env.TURN_ID || !this.env.TURN_KEY) return J({ ok: false });
      const t = await fetch("https://rtc.live.cloudflare.com/v1/turn/keys/" + this.env.TURN_ID + "/credentials/generate-ice-servers", { method: "POST",
        headers: { Authorization: "Bearer " + this.env.TURN_KEY, "Content-Type": "application/json" }, body: JSON.stringify({ ttl: 14400 }) }).catch(() => null);
      if (!t || !t.ok) return J({ ok: false });
      const j = await t.json().catch(() => ({}));
      return J({ ok: !!j.iceServers, iceServers: j.iceServers });
    }

    // ---------- dos dois lados ----------
    if (p === "estado" && request.method === "GET") {
      (mestre ? this.vistoM : this.visto).set(c, agora);
      const base = { ok: true, estado: r.estado, papel: de, agora, max_audio_s: CONSULTORIO.AUDIO_MAX_S, aceite: !!r.aceitou, fim_espera: r.estado === "espera" ? r.fim_espera : undefined };
      // conversa fechada ou expirada: à pessoa já não se mostra nada, mesmo com o link
      if (!mestre && !["espera", "conversa"].includes(r.estado)) return J(base);
      // antes das mensagens: uma chamada que acabe aqui deixa logo a sua linha na conversa
      const ch = r.estado === "conversa" ? this.chamadaViva(c, agora) : null, cv = Number(url.searchParams.get("cv")) || 0;
      const chamada = ch ? { id: ch.id, modo: ch.modo, estado: ch.estado, criada: ch.criada, ligada: ch.ligada, ver: ch.ver, pede: ch.pede, tem: ch.tem,
        oferta: !mestre && cv < ch.ver ? ch.oferta : undefined, resposta: mestre && ch.resposta && cv < ch.ver ? ch.resposta : undefined } : null;
      const msgs = this.linhas("SELECT id, quando, de, tipo, texto, dur, mime, tam FROM msgs WHERE codigo=? AND id>? ORDER BY id LIMIT 200", c, Number(url.searchParams.get("desde")) || 0);
      const outro = mestre ? "pessoa" : "mestre";
      return J({ ...base, msgs, chamada, escreve: agora - (this.escreve.get(c + "|" + outro) || 0) < 5000,
        presente: mestre ? agora - (this.visto.get(c) || 0) < 45000 : undefined, etiqueta: mestre ? r.etiqueta : undefined });
    }
    if (p === "entrar" && request.method === "POST") {
      if (!["criado", "espera", "conversa"].includes(r.estado)) return J({ ok: false, estado: r.estado }, 410);
      if (d.aceitou !== true && !r.aceitou) return J({ ok: false, erro: "aceitar" }, 400);   // sem aceitar a guarda da escrita e da voz, não se entra; numa ligação reaberta já aceitou
      this.visto.set(c, agora);
      if (r.estado === "criado") {
        const cf = request.cf || {}, ua = request.headers.get("user-agent") || "";
        // Consultório ocupado: outra conversa aberta, ou outra pessoa presente na sala. Quem saiu sem fechar não conta como à espera.
        const outras = this.linhas("SELECT codigo, estado FROM consultas WHERE estado IN ('conversa','espera') AND codigo<>? AND expira>=?", c, agora);
        const ocupado = outras.some((x) => x.estado === "conversa" || agora - (this.visto.get(x.codigo) || 0) < 300000);
        const escolhido = r.espera_min || CONSULTORIO.ESPERA_MIN, min = ocupado ? Math.max(CONSULTORIO.ESPERA_OCUPADO_MIN, escolhido) : escolhido;
        r.fim_espera = agora + min * 60000;
        this.sql.exec("UPDATE consultas SET estado='espera', entrou=?, aceitou=COALESCE(aceitou, ?), pais=?, aparelho=?, fim_espera=? WHERE codigo=?", agora, agora, cf.country || "?", aparelhoDe(ua), r.fim_espera, c);
        r.estado = "espera";
      }
      return J({ ok: true, estado: r.estado, agora, fim_espera: r.estado === "espera" ? r.fim_espera : undefined });
    }
    if (p === "msg" && request.method === "POST") {
      const t = String(d.texto || "").trim().slice(0, CONSULTORIO.TEXTO_MAX);
      if (!viva || !t) return J({ ok: false, estado: r.estado }, 400);   // tal como no chat do site: só depois de ele abrir a porta
      const id = this.novaMsg(c, agora, de, "texto", t);
      if (!mestre) this.sql.exec("UPDATE consultas SET ult_pessoa=? WHERE codigo=?", agora, c);
      this.escreve.delete(c + "|" + de);
      return J({ ok: true, id });
    }
    if (p === "escreve") { if (viva) this.escreve.set(c + "|" + de, agora); return J({ ok: true }); }
    if (p === "audio" && request.method === "GET") {
      const a = this.linhas("SELECT mime FROM msgs WHERE id=? AND codigo=? AND tipo='audio'", Number(url.searchParams.get("id")) || 0, c)[0];
      if (!a || (!mestre && !["espera", "conversa"].includes(r.estado))) return J({ ok: false }, 404);
      const partes = this.linhas("SELECT dados FROM audio WHERE msg=? ORDER BY pos", Number(url.searchParams.get("id"))).map((x) => new Uint8Array(x.dados));
      const tudo = new Uint8Array(partes.reduce((n, x) => n + x.length, 0)); let o = 0; for (const x of partes) { tudo.set(x, o); o += x.length; }
      return new Response(tudo, { headers: { "Content-Type": a.mime, "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff", "X-Robots-Tag": "noindex",
        "Content-Security-Policy": "sandbox; default-src 'none'" } });
    }
    if (p === "anexo" && request.method === "GET") {
      const id = Number(url.searchParams.get("id")) || 0, a = this.linhas("SELECT mime, texto FROM msgs WHERE id=? AND codigo=? AND tipo='anexo'", id, c)[0];
      if (!a || (!mestre && !["espera", "conversa"].includes(r.estado))) return J({ ok: false }, 404);
      const partes = this.linhas("SELECT dados FROM audio WHERE msg=? ORDER BY pos", id).map((x) => new Uint8Array(x.dados));
      const tudo = new Uint8Array(partes.reduce((n, x) => n + x.length, 0)); let o = 0; for (const x of partes) { tudo.set(x, o); o += x.length; }
      const nome = a.texto.replace(/[^\w.-]+/g, "_").slice(0, 80) || "anexo";
      return new Response(tudo, { headers: { "Content-Type": a.mime, "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff", "X-Robots-Tag": "noindex",
        "Content-Security-Policy": "sandbox; default-src 'none'", "Content-Disposition": (a.mime.startsWith("image/") ? "inline" : "attachment") + '; filename="' + nome + '"' } });
    }
    if (p === "anexo" && request.method === "POST") {
      if (!viva) return J({ ok: false, estado: r.estado }, 400);
      if ((mestre ? r.anexos_m : r.anexos_p) >= CONSULTORIO.ANEXOS_MAX) return J({ ok: false, erro: "muitos" }, 429);
      if (Number(request.headers.get("Content-Length")) > CONSULTORIO.ANEXO_MAX_BYTES * 4) return J({ ok: false, erro: "grande" }, 413);
      const b = new Uint8Array(await request.arrayBuffer());
      if (!b.length) return J({ ok: false, erro: "vazio" }, 400);
      if (b.length > CONSULTORIO.ANEXO_MAX_BYTES) return J({ ok: false, erro: "grande" }, 413);
      const mime = tipoAnexo(b);
      if (!mime) return J({ ok: false, erro: "formato" }, 415);
      const nome = String(url.searchParams.get("nome") || "anexo").replace(/[\x00-\x1f<>:"/\\|?*]+/g, " ").trim().slice(0, 80) || "anexo";
      const id = this.ctx.storage.transactionSync(() => {
        const n = this.novaMsg(c, agora, de, "anexo", nome, mime, 0, b.length);
        for (let i = 0, pos = 0; i < b.length; i += CONSULTORIO.PEDACO, pos++) this.sql.exec("INSERT INTO audio (msg, pos, dados) VALUES (?,?,?)", n, pos, b.slice(i, i + CONSULTORIO.PEDACO).buffer);
        this.sql.exec(`UPDATE consultas SET ${mestre ? "anexos_m=anexos_m+1" : "anexos_p=anexos_p+1, ult_pessoa=" + agora} WHERE codigo=?`, c);
        return n;
      });
      return J({ ok: true, id, mime });
    }
    if (binario) {
      if (!viva) return J({ ok: false, estado: r.estado }, 400);
      const mime = String(request.headers.get("Content-Type") || "").split(";")[0].trim().toLowerCase();
      const dur = Math.min(CONSULTORIO.AUDIO_MAX_S + 3, Math.max(0, Number(url.searchParams.get("dur")) || 0));
      if (!CONSULTORIO.TIPOS_AUDIO.includes(mime)) return J({ ok: false, erro: "formato" }, 415);
      if (Number(url.searchParams.get("dur")) > CONSULTORIO.AUDIO_MAX_S + 3) return J({ ok: false, erro: "longo" }, 413);
      if ((mestre ? r.audios_m : r.audios_p) >= CONSULTORIO.AUDIOS_MAX) return J({ ok: false, erro: "muitos" }, 429);
      if (Number(request.headers.get("Content-Length")) > CONSULTORIO.AUDIO_MAX_BYTES * 4) return J({ ok: false, erro: "grande" }, 413);   // só o exagero se corta sem ler
      const b = new Uint8Array(await request.arrayBuffer());
      if (!b.length) return J({ ok: false, erro: "vazio" }, 400);
      if (b.length > CONSULTORIO.AUDIO_MAX_BYTES) return J({ ok: false, erro: "grande" }, 413);
      const id = this.ctx.storage.transactionSync(() => {
        const n = this.novaMsg(c, agora, de, "audio", "", mime, dur, b.length);
        for (let i = 0, pos = 0; i < b.length; i += CONSULTORIO.PEDACO, pos++) this.sql.exec("INSERT INTO audio (msg, pos, dados) VALUES (?,?,?)", n, pos, b.slice(i, i + CONSULTORIO.PEDACO).buffer);
        this.sql.exec(`UPDATE consultas SET ${mestre ? "audios_m=audios_m+1" : "audios_p=audios_p+1, ult_pessoa=" + agora} WHERE codigo=?`, c);
        return n;
      });
      return J({ ok: true, id });
    }

    // ---------- a chamada: só com a conversa aberta. Só ele liga; só a pessoa atende ou recusa ----------
    if (p === "chamada" && request.method === "POST") {
      const a = String(d.acao || ""), sdp = String(d.sdp || "");
      if (!viva) return J({ ok: false, estado: r.estado }, 409);
      if (sdp.length > CONSULTORIO.SDP_MAX) return J({ ok: false, erro: "grande" }, 413);
      const ch = this.chamadaViva(c, agora);
      if (a === "ligar") {
        if (!mestre) return J({ ok: false }, 403);
        if (ch) return J({ ok: false, erro: "ocupado", id: ch.id }, 409);
        if (!["voz", "video", "cartas"].includes(d.modo) || !sdp) return J({ ok: false }, 400);
        this.sql.exec("INSERT INTO chamadas (codigo, id, modo, estado, criada, oferta) VALUES (?,?,?,'toca',?,?)", c, agora, d.modo, agora, sdp);
        return J({ ok: true, id: agora, ver: 1 });
      }
      if (!ch || Number(d.id) !== ch.id) return J({ ok: false, erro: "acabou" }, 410);
      if (a === "desligar") {
        const motivo = ch.estado === "toca" ? (mestre ? "cancelada" : "recusada") : d.motivo === "falhou" && !ch.ligada ? "falhou" : ch.ligada ? "terminada" : "cancelada";
        this.fimChamada(c, ch, motivo, agora); return J({ ok: true });
      }
      if (a === "ligada") { if (!ch.ligada) this.sql.exec("UPDATE chamadas SET estado='ligada', ligada=? WHERE codigo=?", agora, c); return J({ ok: true }); }
      if (mestre) {
        if (a !== "oferta" || !sdp) return J({ ok: false }, 400);
        this.sql.exec("UPDATE chamadas SET ver=ver+1, pede=0, oferta=?, resposta=NULL WHERE codigo=?", sdp, c);   // voltar a ligar sem desligar: recarregar, ou mudar de rede
        return J({ ok: true, ver: ch.ver + 1 });
      }
      if (a === "atender") { if (ch.estado !== "toca") return J({ ok: false }, 409); this.sql.exec("UPDATE chamadas SET estado='atendeu', atendida=? WHERE codigo=?", agora, c); return J({ ok: true }); }
      if (a === "resposta") {
        if (!sdp || Number(d.ver) !== ch.ver) return J({ ok: false }, 409);
        this.sql.exec("UPDATE chamadas SET resposta=?, tem=? WHERE codigo=?", sdp, String(d.tem || "").slice(0, 20), c);
        return J({ ok: true });
      }
      if (a === "religar") { this.sql.exec("UPDATE chamadas SET pede=1 WHERE codigo=?", c); return J({ ok: true }); }
      return J({ ok: false }, 400);
    }

    // ---------- só ele (pela chave, ou pelo mtoken desta conversa) ----------
    // Fechar a consulta é dos dois lados (botão no cabeçalho do chat); reabrir, só dele
    if (p === "fechar") {
      if (!["criado", "espera", "conversa"].includes(r.estado)) return J({ ok: true, estado: r.estado });
      const ch = this.linhas("SELECT * FROM chamadas WHERE codigo=?", c)[0];
      if (ch) this.fimChamada(c, ch, ch.ligada ? "terminada" : "cancelada", agora);
      this.sql.exec("UPDATE consultas SET estado='fechado', fechado=? WHERE codigo=?", agora, c);
      return J({ ok: true, estado: "fechado" });
    }
    if (!mestre) return J({ ok: false }, ["atender", "reabrir", "tempo"].includes(p) ? 403 : 404);
    // Os botões de minutos: antes de a pessoa entrar escolhem o tempo; com ela na sala, somam. A 0 soma-se a partir de agora.
    if (p === "tempo") {
      const n = this.minutos(d.minutos);
      if (!n) return J({ ok: false, erro: "minutos" }, 400);
      if (r.estado === "criado") { this.sql.exec("UPDATE consultas SET espera_min=? WHERE codigo=?", n, c); return J({ ok: true, estado: r.estado, espera_min: n }); }
      if (r.estado !== "espera") return J({ ok: false, estado: r.estado }, 409);
      const fim = Math.min(Math.max(r.fim_espera || 0, agora) + n * 60000, agora + CONSULTORIO.ESPERA_MAX_MIN * 60000);
      this.sql.exec("UPDATE consultas SET fim_espera=? WHERE codigo=?", fim, c);
      return J({ ok: true, estado: r.estado, agora, fim_espera: fim });
    }
    if (p === "atender") {
      if (r.estado !== "espera") return J({ ok: false, estado: r.estado }, 409);   // só se atende quem está na sala
      this.sql.exec("UPDATE consultas SET estado='conversa', atendido=?, expira=max(expira, ?) WHERE codigo=?", agora, agora + CONSULTORIO.CONVERSA_H * 36e5, c);
      return J({ ok: true, estado: "conversa" });
    }
    // Reabrir: a MESMA ligação volta a funcionar, com o histórico, por mais VALIDADE_H a contar de agora. Depois da retenção a linha já
    // não existe e isto dá 404. «criado» conta de novo a partir daqui: sem isso, a limpeza podia apagar uma ligação viva sem mensagens.
    if (p === "reabrir") {
      if (!["fechado", "expirado"].includes(r.estado)) return J({ ok: false, estado: r.estado }, 409);
      const expira = agora + CONSULTORIO.VALIDADE_H * 36e5;
      this.sql.exec("UPDATE consultas SET estado='criado', criado=?, expira=?, entrou=NULL, atendido=NULL, fechado=NULL, fim_espera=NULL WHERE codigo=?", agora, expira, c);
      return J({ ok: true, estado: "criado", expira });
    }
    return J({ ok: false }, 404);
  }
}

// ===== CONTA E INÍCIO DE SESSÃO (05/11/2026, pedido dele) =====
// Entrar por Google (ID token verificado aqui pelas chaves públicas da Google, sem segredo) ou por nome + email com ligação
// de confirmação, sem palavra-passe. Durable Object próprio, separado da Sala e do Consultorio: as contas não dependem deles.
//
// - O worker não envia correio: o pedido fica na tabela «fila» e a campainha (WebSocket em hibernação, sem gastar pedidos
//   enquanto ninguém entra) acorda o vigia do cerebro, conta-painel/conta-vigia.py, que envia pelo SMTP das promoções.
// - Sessão: cookie HttpOnly com um token aleatório; aqui só fica o hash. O navegador nunca lê o token.
// - Só se pergunta ao servidor se o navegador tem a marca de sessão (conta.js): quem não entrou não gasta pedidos.
// - Marketing: caixa à parte, por marcar. Cada alteração fica em «consentimentos» com data, texto e versão.
// - Apagar conta apaga as linhas todas; para a casa saber quem tirar da lista fica só um hash, até o vigia o ir buscar.
const CONTA = {
  GOOGLE_CLIENT_ID: "602619603227-shd1e0g3vb45190il3itdgur5jmiosur.apps.googleusercontent.com",      // público (criado a 06/11/2026, projecto cerebro). Vazio = botão Google escondido e /google recusado.
  JWKS: "https://www.googleapis.com/oauth2/v3/certs",
  LIGACAO_MIN: 15,           // validade da ligação do email; serve uma só vez
  SESSAO_DIAS: 90,           // renova-se sozinha para quem continua a vir
  FILA_MIN: 15,              // um email por enviar ao fim disto já não serve: a ligação caducou
  EVENTOS_DIAS: 30,          // se a casa nunca os for buscar, não ficam para sempre
  CONSENT_VERSAO: "2026-11-05",
  // O mesmo texto da caixa dos formulários do site. Se mudar, muda a versão.
  CONSENT_TEXTO: "Quero receber novidades do Mestre Alberto por email (horóscopos, mapas e promoções). Pode cancelar quando quiser.",
  // [máximo, janela em minutos]
  LIM_IP: [[5, 15], [20, 1440]],
  LIM_EMAIL: [[3, 15], [8, 1440]],
  LIM_TOTAL: [[60, 60], [300, 1440]],   // tudo somado: o Gmail aguenta ~500/dia e as promoções também saem por lá
  LIM_ACCAO: [[40, 15]],                // confirmar, Google, guardar dados: por IP
};
const CONTA_EMAIL = /^[^@\s<>"']{1,64}@[^@\s<>"']{1,190}\.[A-Za-z]{2,}$/;
const contaLimpo = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u001f\u007f<>]/g, " ").replace(/\s+/g, " ").trim().slice(0, n);
function contaData(v) {   // AAAA-MM-DD real, entre 1900 e hoje
  if (!/^\d{4}-\d{2}-\d{2}$/.test(v || "")) return null;
  const d = new Date(v + "T00:00:00Z");
  return !isNaN(d) && d.toISOString().slice(0, 10) === v && v >= "1900-01-01" && d.getTime() <= Date.now() ? v : null;
}
async function contaSha(t) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");
}
function contaAleatorio() { return [...crypto.getRandomValues(new Uint8Array(32))].map((x) => x.toString(16).padStart(2, "0")).join(""); }
function contaB64(s) {
  const b = atob(s.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(s.length / 4) * 4, "="));
  return Uint8Array.from(b, (c) => c.charCodeAt(0));
}

export class Contas extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.jwks = null;           // as chaves públicas da Google, em memória
    this.sql.exec(`CREATE TABLE IF NOT EXISTS contas (id TEXT PRIMARY KEY, email TEXT UNIQUE, nome TEXT, nasc TEXT, hora TEXT, local TEXT, google TEXT UNIQUE,
      marketing INTEGER DEFAULT 0, marketing_em INTEGER, criado INTEGER)`);
    this.sql.exec("CREATE TABLE IF NOT EXISTS sessoes (hash TEXT PRIMARY KEY, conta TEXT, criado INTEGER, expira INTEGER)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS sess_conta ON sessoes(conta)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS sess_expira ON sessoes(expira)");
    this.sql.exec("CREATE TABLE IF NOT EXISTS ligacoes (hash TEXT PRIMARY KEY, email TEXT, nome TEXT, expira INTEGER)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS lig_expira ON ligacoes(expira)");
    // Email por enviar: o único sítio onde a ligação está legível, e só até o vigia confirmar o envio.
    this.sql.exec("CREATE TABLE IF NOT EXISTS fila (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, link TEXT, criado INTEGER)");
    this.sql.exec(`CREATE TABLE IF NOT EXISTS consentimentos (id INTEGER PRIMARY KEY AUTOINCREMENT, conta TEXT, accao TEXT, quando INTEGER, versao TEXT, texto TEXT)`);
    this.sql.exec("CREATE INDEX IF NOT EXISTS cons_conta ON consentimentos(conta)");
    // Para a lista de promoções (preparado, por ligar no vigia). Depois de apagar a conta, só o hash do email.
    this.sql.exec("CREATE TABLE IF NOT EXISTS eventos (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, conta TEXT, email TEXT, nome TEXT, hash TEXT, quando INTEGER, versao TEXT, texto TEXT)");
    this.sql.exec("CREATE INDEX IF NOT EXISTS ev_conta ON eventos(conta)");
    this.sql.exec("CREATE TABLE IF NOT EXISTS limites (chave TEXT, inicio INTEGER, n INTEGER, PRIMARY KEY (chave, inicio))");
  }
  linhas(q, ...a) { return [...this.sql.exec(q, ...a)]; }
  limpar(agora) {
    if (this.ultimaLimpeza && agora - this.ultimaLimpeza < 600000) return;
    this.ultimaLimpeza = agora;
    this.sql.exec("DELETE FROM sessoes WHERE expira < ?", agora);
    this.sql.exec("DELETE FROM ligacoes WHERE expira < ?", agora);
    this.sql.exec("DELETE FROM fila WHERE criado < ?", agora - CONTA.FILA_MIN * 6e4);
    this.sql.exec("DELETE FROM limites WHERE inicio < ?", agora - 1500 * 6e4);
    this.sql.exec("DELETE FROM eventos WHERE quando < ?", agora - CONTA.EVENTOS_DIAS * 864e5);
  }
  async alarm() {   // o que caduca sai mesmo que ninguém cá venha; dorme quando não há nada que caducar
    const agora = Date.now(); this.ultimaLimpeza = 0; this.limpar(agora);
    if (this.linhas("SELECT 1 AS h FROM sessoes UNION ALL SELECT 1 FROM ligacoes UNION ALL SELECT 1 FROM eventos UNION ALL SELECT 1 FROM limites LIMIT 1").length) await this.ctx.storage.setAlarm(agora + 864e5);
  }
  async acordar() { if (!(await this.ctx.storage.getAlarm())) await this.ctx.storage.setAlarm(Date.now() + 864e5); }
  // Conta uma tentativa em cada janela; devolve false se alguma já estava cheia. Os IP e os emails só entram com hash.
  async dentro(tipo, valor, regras, agora) {
    const h = (await contaSha((this.env.STATS_KEY || "") + "|" + tipo + "|" + valor)).slice(0, 32);
    let ok = true;
    for (const [max, min] of regras) {
      const inicio = Math.floor(agora / (min * 6e4)) * min * 6e4, k = h + ":" + min;
      const n = this.linhas("INSERT INTO limites (chave, inicio, n) VALUES (?,?,1) ON CONFLICT (chave, inicio) DO UPDATE SET n = n + 1 RETURNING n", k, inicio)[0].n;
      if (n > max) ok = false;
    }
    return ok;
  }
  cookie(request, valor, maxIdade) {
    const host = new URL(request.url).hostname;
    return `gt_sessao=${valor}; Path=/; Max-Age=${maxIdade}; HttpOnly; Secure; SameSite=Lax` + (/(^|\.)genialtarot\.com$/.test(host) ? "; Domain=genialtarot.com" : "");
  }
  async sessao(request, agora) {
    const m = (request.headers.get("cookie") || "").match(/(?:^|;\s*)gt_sessao=([0-9a-f]{64})/);
    if (!m) return null;
    const s = this.linhas("SELECT s.hash, s.expira, c.* FROM sessoes s JOIN contas c ON c.id = s.conta WHERE s.hash=? AND s.expira>?", await contaSha(m[1]), agora)[0];
    if (s) s.token = m[1];
    return s || null;
  }
  async abrirSessao(request, id, agora) {
    const t = contaAleatorio(), dias = CONTA.SESSAO_DIAS;
    this.sql.exec("INSERT INTO sessoes (hash, conta, criado, expira) VALUES (?,?,?,?)", await contaSha(t), id, agora, agora + dias * 864e5);
    await this.acordar();
    return this.cookie(request, t, dias * 86400);
  }
  publico(c) {
    return { nome: c.nome || "", email: c.email, nasc: c.nasc || "", hora: c.hora || "", local: c.local || "", google: !!c.google,
      marketing: !!c.marketing, marketing_em: c.marketing_em || 0 };
  }
  consentir(c, quer, agora) {
    if (!!c.marketing === quer) return;
    this.sql.exec("UPDATE contas SET marketing=?, marketing_em=? WHERE id=?", quer ? 1 : 0, agora, c.id);
    this.sql.exec("INSERT INTO consentimentos (conta, accao, quando, versao, texto) VALUES (?,?,?,?,?)", c.id, quer ? "deu" : "retirou", agora, CONTA.CONSENT_VERSAO, CONTA.CONSENT_TEXTO);
    // O evento mais recente é o que conta: consentir e retirar seguidos não deixam um «deu» pendente.
    this.sql.exec("DELETE FROM eventos WHERE conta=?", c.id);
    this.sql.exec("INSERT INTO eventos (tipo, conta, email, nome, quando, versao, texto) VALUES (?,?,?,?,?,?,?)", quer ? "deu" : "retirou", c.id, c.email, c.nome || "", agora, CONTA.CONSENT_VERSAO, CONTA.CONSENT_TEXTO);
    c.marketing = quer ? 1 : 0; c.marketing_em = agora;
  }
  async chavesGoogle(kid, agora) {
    const base = this.env.CONTA_JWKS_TESTE || CONTA.JWKS;
    if (!this.jwks || agora - this.jwks.em > 36e5 || (!this.jwks.keys.some((k) => k.kid === kid) && agora - this.jwks.em > 3e5)) {
      const r = await fetch(base); if (!r.ok) throw new Error("jwks " + r.status);
      this.jwks = { keys: (await r.json()).keys || [], em: agora };
    }
    return this.jwks.keys.find((k) => k.kid === kid) || null;
  }
  // O ID token da Google: assinatura RS256 pela chave pública + emissor, destinatário, validade e email confirmado.
  async tokenGoogle(cred, agora) {
    const cliente = this.env.CONTA_GOOGLE_ID_TESTE || CONTA.GOOGLE_CLIENT_ID;
    const p = String(cred || "").split(".");
    if (!cliente || p.length !== 3) return null;
    let cab, dados;
    try { cab = JSON.parse(new TextDecoder().decode(contaB64(p[0]))); dados = JSON.parse(new TextDecoder().decode(contaB64(p[1]))); } catch (e) { return null; }
    if (cab.alg !== "RS256" || !cab.kid) return null;
    const jwk = await this.chavesGoogle(cab.kid, agora);
    if (!jwk) return null;
    const chave = await crypto.subtle.importKey("jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
    const certo = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", chave, contaB64(p[2]), new TextEncoder().encode(p[0] + "." + p[1]));
    const seg = agora / 1000;
    if (!certo || !["accounts.google.com", "https://accounts.google.com"].includes(dados.iss) || dados.aud !== cliente) return null;
    if (!(dados.exp > seg) || !(dados.iat < seg + 300) || dados.email_verified !== true || !dados.sub || !CONTA_EMAIL.test(dados.email || "")) return null;
    return dados;
  }
  webSocketMessage() { /* a campainha só toca para lá; o vigia não manda nada */ }
  webSocketClose(ws) { try { ws.close(); } catch (e) {} }
  async fetch(request) {
    const url = new URL(request.url), p = url.pathname.replace("/api/conta/", ""), agora = Date.now();
    const J = (o, s, cookie) => {
      const h = new Headers({ "Content-Type": "application/json", "Cache-Control": "no-store", "X-Robots-Tag": "noindex" });
      if (cookie) h.append("Set-Cookie", cookie);
      return new Response(JSON.stringify(o), { status: s || 200, headers: h });
    };
    this.limpar(agora);

    // ---------- só com a chave (o vigia do cerebro) ----------
    if (p === "campainha" || p === "fila" || p === "feito" || p === "painel") {
      if (!this.env.STATS_KEY || request.headers.get("X-Chave") !== this.env.STATS_KEY) return J({ ok: false, erro: "chave" }, 403);
      if (p === "painel") {   // 06/11/2026: lista só para o painel protegido do HA. Entrar no site não cria ficha.
        const meia = new Date(agora); meia.setUTCHours(0, 0, 0, 0);
        const conta1 = (q, ...a) => (this.linhas(q, ...a)[0] || {}).n || 0;
        return J({ ok: true, total: conta1("SELECT COUNT(*) n FROM contas"), google: conta1("SELECT COUNT(*) n FROM contas WHERE google IS NOT NULL AND google<>''"),
          promo: conta1("SELECT COUNT(*) n FROM contas WHERE marketing=1"), novas_hoje: conta1("SELECT COUNT(*) n FROM contas WHERE criado>=?", meia.getTime()),
          entraram_hoje: conta1("SELECT COUNT(DISTINCT conta) n FROM sessoes WHERE criado>=?", meia.getTime()),
          contas: this.linhas("SELECT id, nome, email, nasc, hora, local, marketing, criado, CASE WHEN google IS NOT NULL AND google<>'' THEN 1 ELSE 0 END g FROM contas ORDER BY criado DESC LIMIT 500") });
      }
      if (p === "campainha") {
        if (request.headers.get("Upgrade") !== "websocket") return J({ ok: false }, 426);
        for (const v of this.ctx.getWebSockets("vigia")) { try { v.close(1000, "outro"); } catch (e) {} }   // só há um vigia
        const par = new WebSocketPair();
        this.ctx.acceptWebSocket(par[1], ["vigia"]);
        return new Response(null, { status: 101, webSocket: par[0] });
      }
      if (p === "fila") return J({ ok: true, emails: this.linhas("SELECT id, email, link, criado FROM fila ORDER BY id LIMIT 50"),
        eventos: this.linhas("SELECT id, tipo, email, nome, hash, quando, versao, texto FROM eventos ORDER BY id LIMIT 200") });
      const d = await request.json().catch(() => ({}));
      for (const i of (d.emails || []).slice(0, 200)) this.sql.exec("DELETE FROM fila WHERE id=?", Number(i) || 0);
      for (const i of (d.eventos || []).slice(0, 200)) this.sql.exec("DELETE FROM eventos WHERE id=?", Number(i) || 0);
      return J({ ok: true });
    }

    if (p === "config" && request.method === "GET")   // o texto da caixa vem daqui: o que se mostra é o que fica registado
      return J({ ok: true, google: this.env.CONTA_GOOGLE_ID_TESTE || CONTA.GOOGLE_CLIENT_ID, consent: { versao: CONTA.CONSENT_VERSAO, texto: CONTA.CONSENT_TEXTO }, ligacao_min: CONTA.LIGACAO_MIN });

    if (p === "eu" && request.method === "GET") {
      const c = await this.sessao(request, agora);
      if (!c) return J({ ok: true, sessao: false }, 200, request.headers.has("cookie") && /gt_sessao=/.test(request.headers.get("cookie")) ? this.cookie(request, "", 0) : null);
      let renova = null;
      if (c.expira - agora < (CONTA.SESSAO_DIAS - 7) * 864e5) {   // no máximo uma escrita por semana
        this.sql.exec("UPDATE sessoes SET expira=? WHERE hash=?", agora + CONTA.SESSAO_DIAS * 864e5, c.hash);
        renova = this.cookie(request, c.token, CONTA.SESSAO_DIAS * 86400);
      }
      return J({ ok: true, sessao: true, conta: this.publico(c) }, 200, renova);
    }

    if (request.method !== "POST") return J({ ok: false }, 405);
    // Pedido de outro site nunca passa: a origem tem de ser esta (com ou sem www) e o corpo JSON.
    const origem = request.headers.get("origin") || "";
    let mesma = false; try { mesma = new URL(origem).host === url.host; } catch (e) {}
    if (!mesma || !/^application\/json/.test(request.headers.get("content-type") || "")) return J({ ok: false, erro: "origem" }, 403);
    const d = await request.json().catch(() => ({}));
    const ip = request.headers.get("CF-Connecting-IP") || "?";

    // ---------- pedir a ligação: a resposta é igual exista ou não a conta ----------
    if (p === "pedir") {
      const nome = contaLimpo(d.nome, 80), email = contaLimpo(d.email, 254).toLowerCase();
      if (d.site) return J({ ok: true });   // o campo escondido: só os robôs o preenchem
      if (nome.length < 2) return J({ ok: false, erro: "nome" }, 400);
      if (!CONTA_EMAIL.test(email)) return J({ ok: false, erro: "email" }, 400);
      if (!(await this.dentro("ip", ip, CONTA.LIM_IP, agora))) return J({ ok: false, erro: "muitos" }, 429);
      const porEmail = await this.dentro("email", email, CONTA.LIM_EMAIL, agora), porTotal = await this.dentro("total", "site", CONTA.LIM_TOTAL, agora);
      if (porEmail && porTotal) {
        const t = contaAleatorio();
        this.sql.exec("INSERT INTO ligacoes (hash, email, nome, expira) VALUES (?,?,?,?)", await contaSha(t), email, nome, agora + CONTA.LIGACAO_MIN * 6e4);
        this.sql.exec("INSERT INTO fila (email, link, criado) VALUES (?,?,?)", email, url.origin + "/conta#t=" + t, agora);
        await this.acordar();
        for (const v of this.ctx.getWebSockets("vigia")) { try { v.send("fila"); } catch (e) {} }
      }
      return J({ ok: true });
    }

    if (!(await this.dentro("accao", ip, CONTA.LIM_ACCAO, agora))) return J({ ok: false, erro: "muitos" }, 429);

    // ---------- a ligação do email: só com POST do botão (os antivírus do correio abrem ligações sozinhos) ----------
    if (p === "confirmar") {
      const t = String(d.t || "");
      if (!/^[0-9a-f]{64}$/.test(t)) return J({ ok: false, erro: "ligacao" }, 400);
      const h = await contaSha(t), l = this.linhas("SELECT * FROM ligacoes WHERE hash=? AND expira>?", h, agora)[0];
      if (!l) return J({ ok: false, erro: "ligacao" }, 400);
      this.sql.exec("DELETE FROM ligacoes WHERE email=?", l.email);   // serve uma vez, e leva as irmãs consigo
      let c = this.linhas("SELECT * FROM contas WHERE email=?", l.email)[0];
      if (!c) {
        const id = crypto.randomUUID();
        this.sql.exec("INSERT INTO contas (id, email, nome, criado) VALUES (?,?,?,?)", id, l.email, l.nome, agora);
        c = this.linhas("SELECT * FROM contas WHERE id=?", id)[0];
      }
      return J({ ok: true, sessao: true, conta: this.publico(c) }, 200, await this.abrirSessao(request, c.id, agora));
    }

    if (p === "google") {
      let g = null;
      try { g = await this.tokenGoogle(d.credential, agora); } catch (e) { return J({ ok: false, erro: "google-fora" }, 502); }
      if (!g) return J({ ok: false, erro: "google" }, 400);
      const email = g.email.toLowerCase();
      let c = this.linhas("SELECT * FROM contas WHERE google=?", g.sub)[0] || this.linhas("SELECT * FROM contas WHERE email=?", email)[0];
      if (c && !c.google) { this.sql.exec("UPDATE contas SET google=? WHERE id=?", g.sub, c.id); c.google = g.sub; }
      if (!c) {
        const id = crypto.randomUUID();
        this.sql.exec("INSERT INTO contas (id, email, nome, google, criado) VALUES (?,?,?,?,?)", id, email, contaLimpo(g.name, 80), g.sub, agora);
        c = this.linhas("SELECT * FROM contas WHERE id=?", id)[0];
      }
      return J({ ok: true, sessao: true, conta: this.publico(c) }, 200, await this.abrirSessao(request, c.id, agora));
    }

    // ---------- daqui para baixo, só com sessão ----------
    const c = await this.sessao(request, agora);
    if (!c) return J({ ok: false, erro: "sessao" }, 401);

    if (p === "perfil") {
      const nome = contaLimpo(d.nome, 80) || c.nome, hora = contaLimpo(d.hora, 5), local = contaLimpo(d.local, 120);
      const nasc = d.nasc ? contaData(d.nasc) : "";
      if (nasc === null) return J({ ok: false, erro: "data" }, 400);
      if (d.marketing === true && d.versao !== CONTA.CONSENT_VERSAO) return J({ ok: false, erro: "versao" }, 409);
      if (hora && !/^([01]\d|2[0-3]):[0-5]\d$/.test(hora)) return J({ ok: false, erro: "hora" }, 400);
      this.sql.exec("UPDATE contas SET nome=?, nasc=?, hora=?, local=? WHERE id=?", nome, nasc, hora, local, c.id);
      Object.assign(c, { nome, nasc, hora, local });
      // Só a caixa marcada pela pessoa, sobre o texto que lhe foi mostrado. Ausente = não mexe.
      if (typeof d.marketing === "boolean") this.consentir(c, d.marketing, agora);
      return J({ ok: true, conta: this.publico(c) });
    }
    if (p === "consentimento") {
      if (d.marketing !== true && d.marketing !== false) return J({ ok: false }, 400);
      if (d.marketing && d.versao !== CONTA.CONSENT_VERSAO) return J({ ok: false, erro: "versao" }, 409);
      this.consentir(c, d.marketing, agora);
      return J({ ok: true, conta: this.publico(c) });
    }
    if (p === "sair") {
      this.sql.exec("DELETE FROM sessoes WHERE hash=?", c.hash);
      return J({ ok: true }, 200, this.cookie(request, "", 0));
    }
    if (p === "apagar") {
      if (d.confirmo !== true) return J({ ok: false }, 400);
      const deu = this.linhas("SELECT 1 AS h FROM consentimentos WHERE conta=? LIMIT 1", c.id).length > 0;
      const hash = deu ? await contaSha((this.env.STATS_KEY || "") + "|" + c.email) : "";
      this.ctx.storage.transactionSync(() => {
        for (const q of ["DELETE FROM sessoes WHERE conta=?", "DELETE FROM consentimentos WHERE conta=?", "DELETE FROM eventos WHERE conta=?", "DELETE FROM contas WHERE id=?"]) this.sql.exec(q, c.id);
        this.sql.exec("DELETE FROM ligacoes WHERE email=?", c.email);
        this.sql.exec("DELETE FROM fila WHERE email=?", c.email);
        if (deu) this.sql.exec("INSERT INTO eventos (tipo, hash, quando) VALUES ('apagou',?,?)", hash, agora);
      });
      return J({ ok: true }, 200, this.cookie(request, "", 0));
    }
    return J({ ok: false }, 404);
  }
}
