/* 🔮🔔 Os sons do Escolha um Monte (04/11/2026, pedido dele: «um efeito de viragem das cartas e um som ao virar»).
   Irmão do som-cigano.js: tudo feito no navegador (Web Audio), sem ficheiros. Volume BAIXO de propósito (regra dele: nunca som
   alto). Só toca depois de um gesto da pessoa (o navegador não deixa antes) e não toca com «menos movimento» ligado.
   window.somBaralhar()  — ao escolher o monte: o restolhar das cartas a serem baralhadas
   window.somVirar(i)    — cada carta que vira: o «swish» da carta + um sininho de cristal (i muda o tom: 0, 1, 2 sobem) */
(function () {
  let ac = null;
  const reduz = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function ctx() {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    if (!ac) ac = new AC();
    if (ac.state === "suspended") ac.resume().catch(() => {});
    return ac;
  }
  function ruido(a, dur) {
    const n = Math.floor(a.sampleRate * dur), b = a.createBuffer(1, n, a.sampleRate), d = b.getChannelData(0);
    for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / n);
    const s = a.createBufferSource(); s.buffer = b; return s;
  }
  function swish(a, t, f0, f1, vol, dur) {
    const s = ruido(a, dur), bp = a.createBiquadFilter(), g = a.createGain();
    bp.type = "bandpass"; bp.Q.value = 1.2;
    bp.frequency.setValueAtTime(f0, t); bp.frequency.exponentialRampToValueAtTime(f1, t + dur * 0.9);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    s.connect(bp).connect(g).connect(a.destination); s.start(t); s.stop(t + dur + 0.02);
  }
  window.somBaralhar = function () {
    if (reduz()) return;
    try {
      const a = ctx(); if (!a) return;
      const t = a.currentTime;
      for (let j = 0; j < 7; j++) swish(a, t + j * 0.045 + Math.random() * 0.012, 1400 + Math.random() * 500, 3200 + Math.random() * 600, 0.06, 0.06);
    } catch (e) {}
  };
  window.somVirar = function (i) {
    if (reduz()) return;
    try {
      const a = ctx(); if (!a) return;
      const t = a.currentTime, k = (i || 0) % 3;
      swish(a, t, 700 + k * 80, 2500 + k * 150, 0.15, 0.17);
      // o sininho de cristal: uma nota da escala pentatónica que sobe de carta para carta, com um harmónico suave
      const notas = [1046.5, 1318.5, 1568.0];   // dó, mi, sol (6.ª oitava)
      for (const [f, v, d] of [[notas[k], 0.05, 1.3], [notas[k] * 2.01, 0.018, 0.7], [notas[k] * 3.02, 0.008, 0.45]]) {
        const o = a.createOscillator(), g = a.createGain(), t0 = t + 0.12;
        o.type = "sine"; o.frequency.setValueAtTime(f, t0);
        g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(v, t0 + 0.008); g.gain.exponentialRampToValueAtTime(0.0001, t0 + d);
        o.connect(g).connect(a.destination); o.start(t0); o.stop(t0 + d + 0.05);
      }
    } catch (e) {}
  };
})();
