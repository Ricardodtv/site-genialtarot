/* Mapa do Amor e da Sedução — cálculo de Vénus e Marte — Genial Tarot (21/10/2026)
   RASCUNHO — página em pré-visualização, ainda não publicada.
   O cálculo é feito no navegador da pessoa: longitude eclíptica tropical e
   geocêntrica de Vénus e de Marte no minuto do nascimento.
   Método: elementos keplerianos do JPL (E. M. Standish, "Approximate Positions
   of the Planets", tabela 1, 1800–2050), Vénus/Marte menos o baricentro
   Terra-Lua, correcção do tempo de luz, precessão até à data, nutação (termo
   maior) e aberração anual. Conferido no cerebro contra o Swiss Ephemeris em
   milhares de datas entre 1940 e 2010 (ver o relatório no fim deste ficheiro).
   A hora local → UTC usa o AstroAsc.localParaUTC (ascendente-calc.js). */
(function (raiz) {
  const R = Math.PI / 180;
  const norm = (x) => ((x % 360) + 360) % 360;

  // [a, e, I, L, varpi, Omega] e as taxas por século (J2000, eclíptica e equinócio J2000)
  const EL = {
    venus: [[0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255],
            [0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418]],
    terra: [[1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0],
            [0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0]],
    marte: [[1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891],
            [0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343]],
  };

  // Posição heliocêntrica (x, y, z em UA, eclíptica J2000) no dia juliano jd
  function helio(nome, jd) {
    const T = (jd - 2451545) / 36525, [b, t] = EL[nome];
    const a = b[0] + t[0] * T, e = b[1] + t[1] * T, I = (b[2] + t[2] * T) * R;
    const L = b[3] + t[3] * T, vp = b[4] + t[4] * T, Om = b[5] + t[5] * T;
    const w = (vp - Om) * R, M = norm(L - vp) * R, O = Om * R;
    let E = M + e * Math.sin(M);
    for (let k = 0; k < 8; k++) E -= (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));   // Kepler
    const xp = a * (Math.cos(E) - e), yp = a * Math.sqrt(1 - e * e) * Math.sin(E);
    const cw = Math.cos(w), sw = Math.sin(w), cO = Math.cos(O), sO = Math.sin(O), cI = Math.cos(I), sI = Math.sin(I);
    return [(cw * cO - sw * sO * cI) * xp + (-sw * cO - cw * sO * cI) * yp,
            (cw * sO + sw * cO * cI) * xp + (-sw * sO + cw * cO * cI) * yp,
            (sw * sI) * xp + (cw * sI) * yp];
  }

  // Longitude geocêntrica aparente (graus, eclíptica e equinócio da data)
  function longitude(nome, jd) {
    const t0 = helio("terra", jd);
    let p = helio(nome, jd), d = 0;
    for (let k = 0; k < 2; k++) {                 // tempo de luz
      const x = p[0] - t0[0], y = p[1] - t0[1], z = p[2] - t0[2];
      d = Math.hypot(x, y, z);
      p = helio(nome, jd - 0.0057755183 * d);
    }
    const x = p[0] - t0[0], y = p[1] - t0[1];
    let lon = Math.atan2(y, x) / R;
    const T = (jd - 2451545) / 36525;
    lon += 1.396971 * T + 0.0003086 * T * T;      // precessão geral em longitude
    const Om = (125.04452 - 1934.136261 * T) * R, Ls = (280.4665 + 36000.7698 * T) * R;
    lon += (-17.20 * Math.sin(Om) - 1.32 * Math.sin(2 * Ls)) / 3600;   // nutação
    const sol = Math.atan2(-t0[1], -t0[0]) / R + 1.396971 * T;        // Sol geocêntrico (≈)
    lon += -20.4955 * Math.cos((sol - lon) * R) / 3600;                // aberração anual
    return norm(lon);
  }

  function venusMarte(msUTC) {
    const jd = msUTC / 86400000 + 2440587.5 + 69 / 86400;   // UT → TT (≈ ΔT; no séc. XX vale segundos de arco)
    return { venus: longitude("venus", jd), marte: longitude("marte", jd) };
  }

  raiz.AstroAmor = { venusMarte, longitude };
})(typeof window !== "undefined" ? window : globalThis);
