/* 🃏🔔 O som das cartas ciganas (02/11/2026, pedido dele: «um som engraçado ao girar as cartas»).
   O mesmo «swish» de carta do Tarot Grátis, seguido de um tilintar de pandeireta — tudo feito no navegador (Web Audio),
   sem ficheiros. Volume BAIXO de propósito (regra dele: nunca som alto). Só toca depois de um gesto da pessoa (o navegador
   não deixa antes) e não toca com «menos movimento» ligado.
   Uso: window.somCigano(i)  — i (opcional) muda ligeiramente o tom, para cartas seguidas não soarem iguais. */
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
  window.somCigano = function (i) {
    if (reduz()) return;
    try {
      const a = ctx(); if (!a) return;
      const t = a.currentTime, k = (i || 0) % 5;
      // 1) o «swish» da carta a virar
      const s = ruido(a, 0.16), bp = a.createBiquadFilter(), g = a.createGain();
      bp.type = "bandpass"; bp.Q.value = 1.1;
      bp.frequency.setValueAtTime(800 + k * 60, t); bp.frequency.exponentialRampToValueAtTime(2600 + k * 120, t + 0.14);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.16, t + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.16);
      s.connect(bp).connect(g).connect(a.destination); s.start(t); s.stop(t + 0.18);
      // 2) a pandeireta: três sacudidelas rápidas de platinelas (ruído agudo + dois tons metálicos)
      for (let j = 0; j < 3; j++) {
        const t0 = t + 0.13 + j * 0.055 + Math.random() * 0.01;
        const z = ruido(a, 0.07), hp = a.createBiquadFilter(), gz = a.createGain();
        hp.type = "highpass"; hp.frequency.value = 6500;
        gz.gain.setValueAtTime(0.0001, t0); gz.gain.exponentialRampToValueAtTime(0.09 - j * 0.02, t0 + 0.004); gz.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.07);
        z.connect(hp).connect(gz).connect(a.destination); z.start(t0); z.stop(t0 + 0.08);
        for (const f of [3150 + k * 90 + j * 140, 4720 + k * 110 + j * 170]) {
          const o = a.createOscillator(), go = a.createGain();
          o.type = "triangle"; o.frequency.setValueAtTime(f, t0);
          go.gain.setValueAtTime(0.0001, t0); go.gain.exponentialRampToValueAtTime(0.035, t0 + 0.003); go.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.12);
          o.connect(go).connect(a.destination); o.start(t0); o.stop(t0 + 0.13);
        }
      }
    } catch (e) {}
  };
})();
