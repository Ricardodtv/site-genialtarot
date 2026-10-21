/* Calculadora de Ascendente — Genial Tarot (21/10/2026)
   O cálculo é feito no navegador da pessoa: Sol, Lua e Ascendente.
   Fórmulas: Meeus, "Astronomical Algorithms" (Sol cap. 25, Lua cap. 47 com os
   termos maiores, tempo sideral cap. 12). Conferido no cerebro contra o Swiss
   Ephemeris em milhares de datas antes de ir para o site.
   A hora local passa a UTC pelo fuso IANA do local (o navegador sabe os fusos
   e as horas de verão antigas, incluindo as do Brasil). */
(function (raiz) {
  const R = Math.PI / 180;
  const norm = (x) => ((x % 360) + 360) % 360;
  const SIGNOS = ["Carneiro", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
                  "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"];

  function diaJuliano(ms) { return ms / 86400000 + 2440587.5; }

  function sol(jd) {
    const T = (jd - 2451545) / 36525;
    const L0 = norm(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
    const M = norm(357.52911 + 35999.05029 * T - 0.0001537 * T * T) * R;
    const C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(M)
            + (0.019993 - 0.000101 * T) * Math.sin(2 * M) + 0.000289 * Math.sin(3 * M);
    const omega = (125.04 - 1934.136 * T) * R;
    return norm(L0 + C - 0.00569 - 0.00478 * Math.sin(omega));
  }

  function lua(jd) {
    const T = (jd - 2451545) / 36525;
    const Lp = norm(218.3164477 + 481267.88123421 * T - 0.0015786 * T * T);
    const D = norm(297.8501921 + 445267.1114034 * T - 0.0018819 * T * T) * R;
    const M = norm(357.5291092 + 35999.0502909 * T - 0.0001536 * T * T) * R;
    const Mp = norm(134.9633964 + 477198.8675055 * T + 0.0087414 * T * T) * R;
    const F = norm(93.272095 + 483202.0175233 * T - 0.0036539 * T * T) * R;
    const E = 1 - 0.002516 * T;
    // termos maiores da Tabela 47.A (em milionésimos de grau)
    const t = [[0,0,1,0,6288774],[2,0,-1,0,1274027],[2,0,0,0,658314],[0,0,2,0,213618],
      [0,1,0,0,-185116],[0,0,0,2,-114332],[2,0,-2,0,58793],[2,-1,-1,0,57066],[2,0,1,0,53322],
      [2,-1,0,0,45758],[0,1,-1,0,-40923],[1,0,0,0,-34720],[0,1,1,0,-30383],[2,0,0,-2,15327],
      [0,0,1,2,-12528],[0,0,1,-2,10980],[4,0,-1,0,10675],[0,0,3,0,10034],[4,0,-2,0,8548],
      [2,1,-1,0,-7888],[2,1,0,0,-6766],[1,0,-1,0,-5163],[1,1,0,0,4987],[2,-1,1,0,4036],
      [2,0,2,0,3994],[4,0,0,0,3861],[2,0,-3,0,3665],[0,1,-2,0,-2689],[2,0,-1,2,-2602],
      [2,-1,-2,0,2390],[1,0,1,0,-2348],[2,-2,0,0,2236],[0,1,2,0,-2120],[0,2,0,0,-2069]];
    let s = 0;
    for (const [d, m, mp, f, c] of t) {
      const e = Math.abs(m) === 1 ? E : Math.abs(m) === 2 ? E * E : 1;
      s += c * e * Math.sin(d * D + m * M + mp * Mp + f * F);
    }
    const A1 = norm(119.75 + 131.849 * T) * R, A2 = norm(53.09 + 479264.29 * T) * R;
    s += 3958 * Math.sin(A1) + 1962 * Math.sin(Lp * R - F) + 318 * Math.sin(A2);
    return norm(Lp + s / 1e6);
  }

  function ascendente(jd, lat, lon) {
    const T = (jd - 2451545) / 36525;
    const gmst = norm(280.46061837 + 360.98564736629 * (jd - 2451545) + 0.000387933 * T * T - T * T * T / 38710000);
    const ramc = norm(gmst + lon) * R;
    const eps = (23.4392911 - 0.0130042 * T) * R;
    const fi = lat * R;
    return norm(Math.atan2(Math.cos(ramc), -(Math.sin(ramc) * Math.cos(eps) + Math.tan(fi) * Math.sin(eps))) / R);
  }

  // Desvio do fuso (minutos) num instante, pelo nome IANA do local
  function desvioFuso(ms, tz) {
    const p = new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", year: "numeric", month: "2-digit",
      day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" }).formatToParts(new Date(ms));
    const v = Object.fromEntries(p.map((x) => [x.type, x.value]));
    return (Date.UTC(+v.year, +v.month - 1, +v.day, +v.hour % 24, +v.minute, +v.second) - ms) / 60000;
  }
  // Hora local (no fuso tz) → milissegundos UTC; duas passagens resolvem a hora de verão
  function localParaUTC(ano, mes, dia, hora, minuto, tz) {
    const ingenuo = Date.UTC(ano, mes - 1, dia, hora, minuto);
    let ms = ingenuo - desvioFuso(ingenuo, tz) * 60000;
    ms = ingenuo - desvioFuso(ms, tz) * 60000;
    return ms;
  }

  function signo(lon) { return SIGNOS[Math.floor(norm(lon) / 30)]; }
  function grau(lon) { const g = norm(lon) % 30; return Math.floor(g) + "°" + String(Math.floor((g % 1) * 60)).padStart(2, "0") + "'"; }

  function mapa(msUTC, lat, lon) {
    const jd = diaJuliano(msUTC);
    const s = sol(jd), l = lua(jd), a = ascendente(jd, lat, lon);
    return { sol: { lon: s, signo: signo(s), grau: grau(s) }, lua: { lon: l, signo: signo(l), grau: grau(l) },
             asc: { lon: a, signo: signo(a), grau: grau(a) } };
  }

  raiz.AstroAsc = { SIGNOS, diaJuliano, sol, lua, ascendente, localParaUTC, desvioFuso, signo, grau, mapa };
})(typeof window !== "undefined" ? window : globalThis);
