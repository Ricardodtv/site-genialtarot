/* O Trio Astral (Sol · Lua · Ascendente) — as frases do cartão — Genial Tarot (28/10/2026)
   ╔══════════════════════════════════════════════════════════════════╗
   ║  EXPERIÊNCIA 28/10/2026 — página da área Novidades.              ║
   ║  Textos por aprovar pelo Mestre Alberto.                         ║
   ╚══════════════════════════════════════════════════════════════════╝
   Uma frase curta por signo, para caber no cartão de partilhar (até ~55 letras):
   o Sol (a essência), a Lua (as emoções) e o Ascendente (como o mundo a vê).
   Sem género gramatical (o cartão serve a qualquer pessoa). Ordem: 0 Áries … 11 Peixes. */
(function (raiz) {
  const SOL = [
    "Coragem para começar o que os outros só sonham.",
    "Uma força serena que constrói para durar.",
    "Uma mente curiosa que liga tudo a todos.",
    "Um coração que cuida e nunca esquece.",
    "Um brilho generoso que aquece quem está perto.",
    "Mãos atentas que tornam tudo melhor.",
    "Um talento natural para a harmonia e o encontro.",
    "Uma intensidade que renasce sempre mais forte.",
    "Uma fé no horizonte que não se apaga.",
    "Passo a passo, chega sempre ao cume.",
    "Livre, original e à frente do seu tempo.",
    "Uma sensibilidade que sente o invisível.",
  ];
  const LUA = [
    "Sente tudo depressa e com fogo.",
    "Encontra a paz no conforto e no afeto.",
    "Entende o que sente quando conversa.",
    "Emoções fundas e um ninho para quem ama.",
    "Um coração que pede calor e devolve em dobro.",
    "Mostra o amor em gestos de cuidado.",
    "Precisa de harmonia para respirar em paz.",
    "Sente a dobrar e ama sem meias medidas.",
    "Uma alma livre que precisa de horizonte.",
    "Emoções firmes, guardadas com dignidade.",
    "Sente com a cabeça e precisa de espaço.",
    "Uma onda de ternura e de intuição.",
  ];
  const ASC = [
    "Chega com energia e deixa marca.",
    "Transmite calma, charme e confiança.",
    "Transmite leveza, curiosidade e juventude.",
    "Acolhe à primeira vista, com doçura.",
    "Entra e ilumina a sala.",
    "Elegância discreta e um olhar atento a tudo.",
    "Simpatia e beleza que abrem portas.",
    "Um olhar magnético que intriga.",
    "Alegria contagiante e alma de viajante.",
    "Uma postura serena que inspira respeito.",
    "Um jeito único que ninguém esquece.",
    "Um encanto suave, quase de sonho.",
  ];
  // Sem a hora de nascimento não há Ascendente
  const SEM_ASC = "Com a hora de nascimento, descubra o seu Ascendente.";

  raiz.TextosTrio = { SOL, LUA, ASC, SEM_ASC };
})(typeof window !== "undefined" ? window : globalThis);
