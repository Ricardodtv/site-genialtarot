/* Astrocartografia — as linhas dos planetas no mapa-mundo — Genial Tarot (04/11/2026)
   RASCUNHO — página em pré-visualização, ainda não publicada.
   O cálculo é feito no navegador da pessoa. Linhas «zodiacais»: cada planeta é
   posto sobre a eclíptica (latitude eclíptica 0), como na maioria dos programas
   de astrologia para a Lua e o Sol; nos outros a diferença é de poucos graus.
   Longitudes: Sol e Lua do AstroAsc (ascendente-calc.js), os outros do
   AstroAmor.planetas (mapa-amor-calc.js), ambos conferidos contra o Swiss Ephemeris.
   λ → α, δ com a obliquidade média; tempo sideral de Greenwich (IAU, Meeus cap. 12).
   Para cada planeta (L = longitude geográfica, leste positivo):
     MC: L = α − GMST          IC: MC + 180°
     ASC/DSC à latitude φ: cos H₀ = −tan φ · tan δ;  ASC: L = α − GMST − H₀;  DSC: L = α − GMST + H₀
   Conferido no cerebro contra o Swiss Ephemeris (astrocarto-teste.py). */
(function (raiz) {
  const R = Math.PI / 180;
  const norm = (x) => ((x % 360) + 360) % 360;
  const n180 = (x) => { const v = norm(x + 180) - 180; return v === -180 ? 180 : v; };

  function gmst(jd) {
    const T = (jd - 2451545) / 36525;
    return norm(280.46061837 + 360.98564736629 * (jd - 2451545) + 0.000387933 * T * T - T * T * T / 38710000);
  }
  function obliquidade(jd) { return 23.4392911 - 0.0130042 * (jd - 2451545) / 36525; }

  // eclíptica (λ, β=0) → equatorial (α, δ) em graus
  function equatorial(lam, eps) {
    const l = lam * R, e = eps * R;
    const a = Math.atan2(Math.sin(l) * Math.cos(e), Math.cos(l));
    const d = Math.asin(Math.sin(l) * Math.sin(e));
    return { ra: norm(a / R), dec: d / R };
  }

  // A linha do Ascendente (sinal −1) ou do Descendente (+1) de um planeta: lista de troços [[lat, lon], ...]
  // partida onde atravessa o antimeridiano (±180°), para se poder desenhar sem riscos de lado a lado.
  function curva(mc, dec, sinal, passo = 0.5, latMax = 66) {
    const trocos = []; let atual = [];
    const td = Math.tan(dec * R);
    for (let lat = -latMax; lat <= latMax + 1e-9; lat += passo) {
      const c = -Math.tan(lat * R) * td;
      if (Math.abs(c) > 1) { if (atual.length) { trocos.push(atual); atual = []; } continue; }
      const H = Math.acos(c) / R;
      const lon = n180(mc + sinal * H);
      if (atual.length && Math.abs(lon - atual[atual.length - 1][1]) > 180) { trocos.push(atual); atual = []; }
      atual.push([+lat.toFixed(3), lon]);
    }
    if (atual.length) trocos.push(atual);
    return trocos;
  }

  const ORDEM = ["sol", "lua", "mercurio", "venus", "marte", "jupiter", "saturno", "urano", "neptuno", "plutao"];

  // Tudo de uma vez: msUTC = instante do nascimento em milissegundos UTC
  function linhas(msUTC) {
    const jd = msUTC / 86400000 + 2440587.5;
    const g = gmst(jd), eps = obliquidade(jd);
    const lon = { sol: raiz.AstroAsc.sol(jd), lua: raiz.AstroAsc.lua(jd), ...raiz.AstroAmor.planetas(msUTC) };
    const r = { gmst: g, eps, planetas: {} };
    for (const k of ORDEM) {
      const { ra, dec } = equatorial(lon[k], eps);
      const mc = n180(ra - g);
      r.planetas[k] = { lam: lon[k], ra, dec, mc, ic: n180(mc + 180), asc: curva(mc, dec, -1), dsc: curva(mc, dec, +1) };
    }
    return r;
  }

  // Distância (km) de um ponto à linha MC/IC (meio meridiano de longitude L)
  const RT = 6371;
  function distMeridiano(lat, lon, L) {
    const dl = Math.abs(n180(lon - L));
    if (dl >= 90) return Infinity;                       // está do outro lado do globo: é a outra metade
    return RT * Math.asin(Math.cos(lat * R) * Math.sin(dl * R));
  }
  function haversine(la1, lo1, la2, lo2) {
    const a = Math.sin((la2 - la1) * R / 2) ** 2 + Math.cos(la1 * R) * Math.cos(la2 * R) * Math.sin((lo2 - lo1) * R / 2) ** 2;
    return 2 * RT * Math.asin(Math.min(1, Math.sqrt(a)));
  }
  // Distância (km) de um ponto a uma curva ASC/DSC (troços de [lat, lon]); densifica os segmentos longos
  function distCurva(lat, lon, trocos) {
    let m = Infinity;
    for (const t of trocos) for (let i = 0; i < t.length; i++) {
      const [a1, o1] = t[i];
      m = Math.min(m, haversine(lat, lon, a1, o1));
      if (i + 1 < t.length) {
        const [a2, o2] = t[i + 1], n = Math.ceil(Math.max(Math.abs(o2 - o1), Math.abs(a2 - a1)) / 0.25);
        for (let k = 1; k < n; k++) m = Math.min(m, haversine(lat, lon, a1 + (a2 - a1) * k / n, o1 + (o2 - o1) * k / n));
      }
    }
    return m;
  }
  function distancias(p, lat, lon) {
    return { mc: distMeridiano(lat, lon, p.mc), ic: distMeridiano(lat, lon, p.ic), asc: distCurva(lat, lon, p.asc), dsc: distCurva(lat, lon, p.dsc) };
  }

  raiz.AstroCarto = { ORDEM, gmst, obliquidade, equatorial, curva, linhas, distancias, distMeridiano, distCurva, n180 };
})(typeof window !== "undefined" ? window : globalThis);
