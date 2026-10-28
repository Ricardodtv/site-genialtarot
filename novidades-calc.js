/* Novidades — o cálculo comum das três páginas em experiência — Genial Tarot (28/10/2026)
   EXPERIÊNCIA 28/10/2026 — páginas da área Novidades; textos por aprovar pelo Mestre Alberto.
   Serve o horoscopo-pessoal.html (trânsitos de hoje ao mapa natal), o trio-astral.html
   (Sol, Lua e Ascendente) e o mapa-do-casal.html (sinastria). Não calcula nada de novo:
   usa os motores que já estão no site e não se lhes mexe —
     · AstroAsc (ascendente-calc.js): Lua, Ascendente, dia juliano;
     · AstroRS.solPreciso (revolucao-calc.js): o Sol corrigido (erro médio 2,3"), que decide
       melhor o signo de quem nasce no dia da mudança;
     · AstroAmor.planetas (mapa-amor-calc.js): Mercúrio a Plutão (Standish, válido de 1800 a 2050).
   Não há tabelas pré-calculadas: o céu de hoje sai da hora do aparelho, todos os dias.
   Conferido no cerebro contra o Swiss Ephemeris a 28/10/2026 (teste no relatório da entrega). */
(function (raiz) {
  const norm = (x) => ((x % 360) + 360) % 360;
  // distância angular mais curta entre duas longitudes, de 0 a 180
  const dist = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180);
  const ANO_LIMITE = 2050;   // o fim da tabela do Standish: depois disto a página avisa em vez de calcular

  // Os cinco aspectos maiores. nat: "conj" (fusão), "har" (harmonia) ou "ten" (tensão)
  const ASPECTOS = {
    conj: { ang: 0, glifo: "☌", nome: "conjunção", nat: "conj" },
    sext: { ang: 60, glifo: "⚹", nome: "sextil", nat: "har" },
    quad: { ang: 90, glifo: "□", nome: "quadratura", nat: "ten" },
    trig: { ang: 120, glifo: "△", nome: "trígono", nat: "har" },
    opos: { ang: 180, glifo: "☍", nome: "oposição", nat: "ten" },
  };

  // O aspecto (se houver) entre duas longitudes, com a orbe de cada aspecto em graus.
  // Devolve { asp, dif, exato } — exato vai de 1 (exacto ao grau) a 0 (no limite da orbe) — ou null.
  function aspecto(a, b, orbes) {
    const d = dist(a, b);
    let melhor = null;
    for (const k in ASPECTOS) {
      const dif = Math.abs(d - ASPECTOS[k].ang), orbe = orbes[k];
      if (dif <= orbe && (!melhor || dif / orbe < 1 - melhor.exato)) melhor = { asp: k, dif, exato: 1 - dif / orbe };
    }
    return melhor;
  }

  // O mapa natal: Sol, Lua, Vénus, Marte e Ascendente (null sem a hora).
  // Sem a hora calcula-se ao meio-dia e a Lua fica marcada como incerta (anda ~13° num dia).
  function natal(msUTC, lat, lon, semhora) {
    const jd = AstroAsc.diaJuliano(msUTC), pl = AstroAmor.planetas(msUTC);
    return { sol: AstroRS.solPreciso(jd), lua: AstroAsc.lua(jd), venus: pl.venus, marte: pl.marte,
             asc: semhora ? null : AstroAsc.ascendente(jd, lat, lon), luaIncerta: !!semhora };
  }

  // O céu de um instante (o de hoje): os dez planetas
  function ceu(msUTC) {
    const jd = AstroAsc.diaJuliano(msUTC);
    return { sol: AstroRS.solPreciso(jd), lua: AstroAsc.lua(jd), ...AstroAmor.planetas(msUTC) };
  }

  // ===== Horóscopo Pessoal: os trânsitos de hoje ao Sol, à Lua, a Vénus e ao Ascendente natais =====
  // Orbe = orbe do aspecto × o andamento do planeta: a Lua de hoje (13°/dia) leva a orbe inteira;
  // os lentos levam pouca, senão o mesmo trânsito de Plutão aparecia dois anos seguidos todas as manhãs.
  const ORBE_TR = { conj: 8, opos: 8, quad: 7, trig: 7, sext: 4.5 };
  const FATOR_TR = { lua: 1, sol: .85, mercurio: .7, venus: .75, marte: .75, jupiter: .45, saturno: .45, urano: .3, neptuno: .3, plutao: .3 };
  // Força = peso do planeta × peso do ponto natal × peso do aspecto × exactidão (1 → 0).
  // A Lua de hoje pesa mais (é ela que muda o dia) e a Lua natal também (pedido: prioridade à Lua).
  const PESO_TR = { lua: 1.6, sol: 1.1, mercurio: 1, venus: 1.1, marte: 1.1, jupiter: 1.15, saturno: 1.15, urano: 1, neptuno: 1, plutao: 1 };
  const PESO_ALVO = { lua: 1.25, sol: 1.15, asc: 1.1, venus: 1 };
  const PESO_ASP = { conj: 1, opos: .9, quad: .9, trig: .85, sext: .7 };

  // Os pontos natais que entram: sem a hora não há Ascendente, e a Lua natal sai
  // (o erro de ±6,5° é do tamanho da orbe e daria trânsitos inventados).
  function alvos(nat) {
    const r = ["sol"];
    if (!nat.luaIncerta) r.push("lua");
    r.push("venus");
    if (nat.asc != null) r.push("asc");
    return r;
  }

  function transitos(nat, hoje) {
    const r = [];
    for (const p in FATOR_TR) for (const a of alvos(nat)) {
      const orbes = {};
      for (const k in ORBE_TR) orbes[k] = ORBE_TR[k] * FATOR_TR[p];
      const x = aspecto(hoje[p], nat[a], orbes);
      if (x) r.push({ planeta: p, alvo: a, ...x, forca: PESO_TR[p] * PESO_ALVO[a] * PESO_ASP[x.asp] * x.exato });
    }
    return r.sort((u, v) => v.forca - u.forca);
  }

  // A casa por onde passa a Lua de hoje. Com a hora: casas iguais a partir do Ascendente (como no
  // mapa-astral.html). Sem a hora: casas solares, a 1.ª é o signo do Sol natal inteiro.
  function casaDaLua(luaHoje, nat) {
    if (nat.asc != null) return { casa: Math.floor(norm(luaHoje - nat.asc) / 30) + 1, solares: false };
    return { casa: Math.floor(norm(luaHoje - Math.floor(norm(nat.sol) / 30) * 30) / 30) + 1, solares: true };
  }

  // ===== Mapa do Casal: aspectos cruzados entre Sol, Lua, Vénus, Marte e Ascendente =====
  const PONTOS = ["sol", "lua", "venus", "marte", "asc"];
  const ORBE_SIN = { conj: 8, opos: 8, quad: 6, trig: 7, sext: 4.5 };
  // Peso de cada par (é simétrico: o Sol de um com a Lua do outro vale o mesmo nos dois sentidos).
  // Os pares clássicos do amor pesam mais: Sol–Lua, Vénus–Marte, Lua–Vénus.
  const PESO_PAR = {
    "sol|sol": 1, "sol|lua": 1.5, "sol|venus": 1.2, "sol|marte": 1, "sol|asc": 1.1,
    "lua|lua": 1.2, "lua|venus": 1.3, "lua|marte": 1, "lua|asc": 1,
    "venus|venus": 1, "venus|marte": 1.5, "venus|asc": 1.1,
    "marte|marte": .8, "marte|asc": .9, "asc|asc": .9,
  };
  const par = (p, q) => PONTOS.indexOf(p) <= PONTOS.indexOf(q) ? p + "|" + q : q + "|" + p;
  // Quanto cada aspecto soma (+) ou tira (−) à afinidade.
  function valor(chave, asp) {
    if (chave === "venus|marte") return { conj: 1, trig: 1, sext: .8, quad: .35, opos: .5 }[asp];   // atracção: até a tensão aquece
    const comMarte = chave.includes("marte");
    return { conj: comMarte ? .5 : .9, trig: 1, sext: .8, quad: -.7, opos: -.45 }[asp];
  }

  function sinastria(A, B) {
    const lista = [];
    for (const p of PONTOS) for (const q of PONTOS) {
      if (A[p] == null || B[q] == null) continue;           // Ascendente sem a hora
      const chave = par(p, q), luminar = /sol|lua/.test(chave);
      const orbes = {};
      for (const k in ORBE_SIN) orbes[k] = ORBE_SIN[k] * (luminar ? 1 : .8);
      const x = aspecto(A[p], B[q], orbes);
      if (!x) continue;
      // Lua sem hora: o aspecto pode não existir; conta metade
      const incerto = (p === "lua" && A.luaIncerta) || (q === "lua" && B.luaIncerta);
      const peso = PESO_PAR[chave] * (incerto ? .5 : 1);
      lista.push({ p, q, chave, ...x, incerto, forca: peso * x.exato, contributo: peso * x.exato * valor(chave, x.asp) });
    }
    lista.sort((u, v) => v.forca - u.forca);
    // A NOTA DE AFINIDADE (0–100):
    //   S = Σ (peso do par × exactidão × valor do aspecto), sobre todos os aspectos cruzados;
    //       exactidão = 1 − desvio/orbe; valor: trígono +1, sextil +0,8, conjunção +0,9 (+0,5 com Marte),
    //       quadratura −0,7, oposição −0,45; Vénus–Marte é atracção: quadratura +0,35, oposição +0,5.
    //   nota = 50 + 48 × tanh(S / 3), arredondada e presa entre 5 e 98.
    //   O tanh faz que os primeiros contactos contem muito e os seguintes cada vez menos, e que
    //   nunca se chegue a 0 nem a 100: nenhum céu condena nem garante um casal.
    //   K = 3 foi afinado no cerebro em 20 000 pares ao acaso: metade dos casais fica entre 56 e 79 (mediana 69; 5 % abaixo de 38 e 5 % acima de 90).
    const S = lista.reduce((t, x) => t + x.contributo, 0);
    const nota = Math.max(5, Math.min(98, Math.round(50 + 48 * Math.tanh(S / 3))));
    return { aspectos: lista, S, nota };
  }

  raiz.AstroNov = { ASPECTOS, ANO_LIMITE, norm, dist, aspecto, natal, ceu, alvos, transitos, casaDaLua, sinastria, ORBE_TR, FATOR_TR, ORBE_SIN, PESO_PAR };
})(typeof window !== "undefined" ? window : globalThis);
