/* Limite das amostras grátis — Genial Tarot (21/10/2026)
   Regra dele, para TODOS os mapas com amostra grátis: cada pessoa pode fazer a
   amostra 2 vezes no mesmo dia; depois espera 5 dias (contados a partir do dia
   da primeira) para poder fazer outra.
   Rever o MESMO mapa (mesmos dados) não conta como amostra nova.
   Guarda-se no próprio navegador (localStorage): o cálculo também é feito lá,
   por isso é aí que a regra se aplica. Num modo privado ou noutro navegador
   começa do zero — não há forma de o impedir sem guardar dados da pessoa. */
(function (raiz) {
  const POR_DIA = 2, ESPERA = 5;
  const meiaNoite = (ms) => { const d = new Date(ms); d.setHours(0, 0, 0, 0); return d.getTime(); };
  // dias de calendário (não 24 h certas: na mudança de hora um dia tem 23 ou 25 h)
  const maisDias = (ms, n) => { const d = new Date(ms); d.setDate(d.getDate() + n); return d.getTime(); };
  const ler = (k) => { try { return JSON.parse(localStorage.getItem("amostra:" + k)) || null; } catch (e) { return null; } };
  const gravar = (k, v) => { try { localStorage.setItem("amostra:" + k, JSON.stringify(v)); } catch (e) { /* sem memória: deixa passar */ } };

  // chave = o mapa ("mapa-amor", "mapa-astral", ...); assinatura = os dados de nascimento usados
  // Devolve { ok: true, nova } (nova = amostra nova; false = rever o mesmo mapa) ou { ok: false, proxima: Date }
  function usar(chave, assinatura, agora = Date.now()) {
    const e = ler(chave);
    if (e && agora < maisDias(e.inicio, ESPERA)) {
      if (e.usos.includes(assinatura)) return { ok: true, nova: false };
      if (agora < maisDias(e.inicio, 1) && e.usos.length < POR_DIA) { e.usos.push(assinatura); gravar(chave, e); return { ok: true, nova: true }; }
      return { ok: false, proxima: new Date(maisDias(e.inicio, ESPERA)) };
    }
    gravar(chave, { inicio: meiaNoite(agora), usos: [assinatura] });
    return { ok: true, nova: true };
  }

  const dataCurta = (d) => d.toLocaleDateString("pt-PT", { day: "2-digit", month: "2-digit" });
  raiz.AmostraLimite = { usar, dataCurta, POR_DIA, ESPERA };
})(typeof window !== "undefined" ? window : globalThis);
