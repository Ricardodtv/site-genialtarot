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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/notify") {
      if (request.method !== "POST") {
        return new Response(JSON.stringify({ ok: true, info: "usa POST" }), {
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
