/* Contas das páginas da área Novidades — Genial Tarot (28/10/2026)
   EXPERIÊNCIA 28/10/2026 — usado por carta-de-tarot.html, fase-lua-nascimento.html e adivinha-signo.html.
   Não tem astronomia própria: o Sol vem do AstroRS.solPreciso (revolucao-calc.js) e a Lua do
   AstroAsc.lua (ascendente-calc.js), os dois já conferidos contra o Swiss Ephemeris. Aqui só se juntam:
   - a Carta de Nascimento pela numerologia (método de Mary K. Greer);
   - o signo do Sol num dia SEM hora, com a pergunta honesta «o Sol mudou de signo nesse dia?»;
   - a fase da Lua em 8 passos, com a regra do site para a Cheia (≥ 98 %) e a Nova (≤ 2 %).
   Testes no cerebro (node + pyswisseph), ver o relatório de 28/10/2026. */
(function (raiz) {
  const norm = (x) => ((x % 360) + 360) % 360;
  const somaAlg = (n) => String(n).split("").reduce((s, c) => s + +c, 0);

  // ===== Carta de Nascimento (Mary K. Greer) =====
  // dia + mês + ano (15/03/1990 → 2008); somam-se os algarismos até dar 22 ou menos (2+0+0+8 = 10).
  // Se for 10 ou mais, reduz-se outra vez e a carta reduzida forma o par (10 → 1). O 19 dá três: 19 → 10 → 1.
  // O 22 é O Louco (o arcano 0) e faz par com o 4 (2+2), O Imperador.
  // Devolve { soma, cartas: [n.º dos arcanos, do principal para o mais reduzido] }; o 22 vem já como 0.
  function cartaGreer(a, m, d) {
    const soma = a + m + d;
    let n = soma;
    while (n > 22) n = somaAlg(n);
    const seq = [n];
    let k = n;
    while (k >= 10) { k = somaAlg(k); seq.push(k); }
    return { soma, cartas: seq.map((x) => (x === 22 ? 0 : x)) };
  }

  // ===== O Sol num dia sem hora =====
  const solEm = (ms) => AstroRS.solPreciso(AstroAsc.diaJuliano(ms));
  const signoEm = (ms) => Math.floor(norm(solEm(ms)) / 30);
  // O «dia» de uma pessoa sem cidade pode ser qualquer dia civil da Terra: começa às 00:00 em UTC+14
  // (10:00 UTC da véspera) e acaba às 24:00 em UTC−12 (12:00 UTC do dia seguinte). Se o Sol muda de
  // signo dentro dessa janela, sem a hora e a cidade não se sabe; não se adivinha.
  const JANELA_MUNDO = [-14, 12];
  function signoDoDia(a, m, d, janela = JANELA_MUNDO) {
    const meio = Date.UTC(a, m - 1, d, 12, 0);
    const ini = Date.UTC(a, m - 1, d, 0, 0) + janela[0] * 3600000, fim = Date.UTC(a, m - 1, d, 24, 0) + janela[1] * 3600000;
    const s0 = signoEm(ini), s1 = signoEm(fim);
    if (s0 === s1) return { signo: signoEm(meio), cuspide: false };
    // o instante do ingresso, por bissecção (o Sol anda ~1° por dia: só há uma mudança na janela)
    let lo = ini, hi = fim;
    while (hi - lo > 30000) { const mid = (lo + hi) / 2; if (signoEm(mid) === s0) lo = mid; else hi = mid; }
    return { signo: null, cuspide: true, de: s0, para: s1, ingresso: Math.round((lo + hi) / 2) };
  }

  // ===== A fase da Lua =====
  // Elongação = longitude da Lua − longitude do Sol (0° Nova, 90° Quarto Crescente, 180° Cheia, 270° Quarto Minguante).
  // Iluminada = (1 − cos e) / 2: a mesma conta do lua.html.
  // Regra do site (21/10/2026): «Cheia» só a partir de 98 % e «Nova» só até 2 %.
  // Os Quartos (decisão de 28/10/2026, por aprovar): entre 40 % e 60 % iluminada, perto da meia Lua.
  const FASES8 = ["nova", "crescente", "quarto-crescente", "gibosa-crescente", "cheia", "gibosa-minguante", "quarto-minguante", "minguante"];
  function faseDe(e) {
    const il = (1 - Math.cos(e * Math.PI / 180)) / 2 * 100;
    if (il <= 2) return 0;
    if (il >= 98) return 4;
    const cresce = e < 180;
    if (il >= 40 && il <= 60) return cresce ? 2 : 6;
    if (cresce) return il < 40 ? 1 : 3;
    return il > 60 ? 5 : 7;
  }
  function fase(ms) {
    const jd = AstroAsc.diaJuliano(ms);
    const e = norm(AstroAsc.lua(jd) - AstroRS.solPreciso(jd));
    const ilum = (1 - Math.cos(e * Math.PI / 180)) / 2 * 100;
    return { e, ilum, i: faseDe(e) };
  }
  // As fases por onde a Lua passa num dia civil (no fuso tz), de hora a hora; [] de uma só = o dia não mudou de fase
  function fasesDoDia(a, m, d, tz) {
    const vistas = [];
    for (let h = 0; h <= 24; h++) {
      const ms = h < 24 ? AstroAsc.localParaUTC(a, m, d, h, 0, tz) : AstroAsc.localParaUTC(a, m, d, 23, 59, tz);
      const i = fase(ms).i;
      if (vistas[vistas.length - 1] !== i) vistas.push(i);
    }
    return vistas;
  }

  raiz.AstroNasc = { cartaGreer, solEm, signoEm, signoDoDia, JANELA_MUNDO, FASES8, faseDe, fase, fasesDoDia };
})(typeof window !== "undefined" ? window : globalThis);
