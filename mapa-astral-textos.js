/* Mapa Astral — textos da amostra grátis — Genial Tarot (21/10/2026)
   ╔══════════════════════════════════════════════════════════════════╗
   ║  MAQUETE — textos por aprovar pelo Mestre Alberto.               ║
   ║  Nada disto está publicado. Não ligar a página sem o «sim» dele. ║
   ╚══════════════════════════════════════════════════════════════════╝
   Significados da astrologia clássica: o Sol (a essência, a vontade, o que
   se vem brilhar), a Lua (as emoções, o que acalma, a memória da infância) e
   o Ascendente (a máscara, a primeira impressão, o caminho). Os textos do
   Ascendente são os mesmos da calculadora de Ascendente (ascendente.html).
   Tom: caloroso, honesto, sem promessas. Ordem: 0 Áries … 11 Peixes. */
(function (raiz) {
  const ELEMENTOS = ["Fogo", "Terra", "Ar", "Água"];

  // «A sua essência» — o Sol
  const SOL = [
    "O seu Sol em Áries faz de você uma pessoa de iniciativa, que prefere fazer a esperar. Tem coragem para começar o que os outros só imaginam, e uma energia que contagia quem está à volta. Brilha quando tem um desafio pela frente. O seu caminho é aprender que nem tudo se ganha à primeira, e que a paciência também é uma forma de coragem.",
    "O seu Sol em Touro dá-lhe uma força serena e uma lealdade que não se quebra. Você gosta do que é bom, do que é belo e do que dura. Constrói devagar, mas constrói para sempre. O seu caminho é confiar na mudança quando ela chega: a terra mais fértil é a que se deixa lavrar.",
    "O seu Sol em Gêmeos dá-lhe uma mente viva, curiosa e cheia de perguntas. Você aprende depressa, conversa com toda a gente e encontra ligações onde os outros não vêem nada. Brilha quando partilha o que sabe. O seu caminho é escolher, entre tantos interesses, aqueles que merecem a sua dedicação inteira.",
    "O seu Sol em Câncer faz de você o coração da casa. Sente tudo com profundidade, protege quem ama e nunca esquece um gesto de carinho. A sua força está na memória e no cuidado. O seu caminho é cuidar de si com a mesma ternura com que cuida dos outros.",
    "O seu Sol em Leão dá-lhe presença, calor e um coração enorme. Você nasceu para brilhar e para fazer os outros brilharem consigo. É generoso(a), criativo(a) e leal até ao fim. O seu caminho é lembrar que o seu valor não depende dos aplausos: a sua luz é sua, mesmo quando ninguém está a ver.",
    "O seu Sol em Virgem dá-lhe um olhar atento e mãos que sabem resolver. Você repara nos pormenores, gosta de ser útil e torna melhor tudo aquilo em que toca. Brilha no trabalho bem feito. O seu caminho é aceitar que o imperfeito também é bonito, sobretudo em si mesmo(a).",
    "O seu Sol em Libra faz de você uma pessoa de harmonia, beleza e diálogo. Tem um sentido de justiça apurado e um talento natural para unir pessoas. Brilha nas parcerias. O seu caminho é decidir sem medo de desagradar: a paz verdadeira começa quando você também tem voz.",
    "O seu Sol em Escorpião dá-lhe intensidade, profundidade e uma força interior rara. Você vai ao fundo das coisas e das pessoas, e não se contenta com meias verdades. Renasce de cada crise mais forte. O seu caminho é confiar e largar o controlo: a sua maior magia é a transformação.",
    "O seu Sol em Sagitário dá-lhe optimismo, sede de liberdade e uma fé que não se apaga. Você precisa de horizonte, de viagens, de ideias grandes e de sentido para a vida. Brilha quando ensina e quando explora. O seu caminho é dar raízes aos seus sonhos para que eles cheguem longe.",
    "O seu Sol em Capricórnio dá-lhe ambição serena, disciplina e uma palavra que vale ouro. Você sobe a montanha passo a passo e chega onde quer chegar. Os outros confiam em si. O seu caminho é permitir-se descansar e celebrar o caminho, não só o cume.",
    "O seu Sol em Aquário faz de você uma pessoa original, livre e à frente do seu tempo. Pensa diferente, defende causas e trata toda a gente de igual para igual. Brilha em grupo e no futuro. O seu caminho é deixar que o coração acompanhe a cabeça, e aceitar a proximidade sem perder a liberdade.",
    "O seu Sol em Peixes dá-lhe sensibilidade, intuição e uma compaixão sem fronteiras. Você sente o que os outros não dizem e tem um mundo interior rico de sonhos e de arte. Brilha quando se entrega a algo maior. O seu caminho é proteger a sua energia e pôr limites com amor.",
  ];

  // «O seu mundo emocional» — a Lua
  const LUA = [
    "Com a Lua em Áries, as suas emoções são rápidas e intensas: explode depressa e passa depressa. Precisa de acção para se sentir bem e não suporta ficar parado(a) a remoer. Acalma-se a fazer, a mexer o corpo, a resolver. O seu desafio é dar tempo às emoções antes de reagir.",
    "Com a Lua em Touro, você precisa de segurança, rotina e conforto para se sentir em paz. Uma boa refeição, a natureza e o toque de quem ama são o seu remédio. As suas emoções são estáveis e leais. O seu desafio é largar o que já não lhe faz bem, mesmo quando é familiar.",
    "Com a Lua em Gêmeos, você sente através das palavras: precisa de conversar, de perceber e de partilhar o que sente. Uma boa conversa acalma-o(a) mais do que tudo. O seu desafio é não fugir para a cabeça quando o coração pede silêncio.",
    "Com a Lua em Câncer, a Lua está em casa: as suas emoções são profundas, protectoras e cheias de memória. Precisa de um ninho, de família e de sentir que pertence. O seu desafio é não se fechar na concha quando se sente magoado(a).",
    "Com a Lua em Leão, você precisa de se sentir visto(a), admirado(a) e amado(a) de forma calorosa. Dá muito carinho e espera reconhecimento. Acalma-se a criar, a brincar e a celebrar. O seu desafio é dar-se a si mesmo(a) o valor que procura nos outros.",
    "Com a Lua em Virgem, você sente-se bem quando tudo está no lugar. Cuida dos outros com gestos práticos e preocupa-se com os pormenores. Acalma-se a organizar e a ser útil. O seu desafio é calar a voz da autocrítica e permitir-se simplesmente sentir.",
    "Com a Lua em Libra, você precisa de harmonia, de beleza e de companhia para estar em paz. Um conflito tira-lhe o sono. É doce, diplomático(a) e atento(a) ao outro. O seu desafio é reconhecer o que você sente, e não só o que os outros sentem.",
    "Com a Lua em Escorpião, as suas emoções são profundas como o oceano: sente tudo a dobrar e guarda muito para si. É leal até ao fim e não esquece. Acalma-se na intimidade verdadeira. O seu desafio é perdoar e deixar ir, para que a ferida se transforme em força.",
    "Com a Lua em Sagitário, você precisa de liberdade, de horizonte e de esperança para se sentir bem. Fica triste quando se sente preso(a). Acalma-se a viajar, a aprender e a rir. O seu desafio é ficar com as emoções difíceis em vez de fugir delas.",
    "Com a Lua em Capricórnio, você guarda as emoções com dignidade e mostra o amor com responsabilidade e presença. Sente-se seguro(a) quando tem as coisas sob controlo. O seu desafio é permitir-se ser frágil: pedir colo também é ser forte.",
    "Com a Lua em Aquário, você sente com alguma distância e precisa de espaço para respirar. Os amigos são a sua família escolhida. Acalma-se a pensar e a estar com quem o(a) aceita como é. O seu desafio é deixar-se tocar pelas emoções sem as explicar.",
    "Com a Lua em Peixes, você é uma esponja emocional: sente o ambiente, as pessoas e até o que ainda não aconteceu. Tem uma intuição enorme e uma compaixão imensa. Acalma-se na música, no mar e na oração. O seu desafio é proteger-se do que não é seu.",
  ];

  // «Como o mundo o(a) vê» — o Ascendente (os mesmos da calculadora de Ascendente)
  const ASC = [
    "Com Ascendente em Áries, você chega primeiro e chega inteiro(a). As pessoas vêem coragem, pressa e uma chama que não se apaga. A sua missão é aprender a liderar sem se queimar.",
    "Com Ascendente em Touro, você transmite calma, confiança e uma beleza serena. Quem se aproxima sente que pode contar consigo. O seu caminho é construir, devagar e para sempre.",
    "Com Ascendente em Gêmeos, você encanta pela conversa, pela curiosidade e pelo humor rápido. Parece sempre mais novo(a) do que é. O seu caminho é ligar pessoas e ideias.",
    "Com Ascendente em Câncer, você acolhe antes de falar. Os outros sentem a sua sensibilidade e o seu cuidado de mãe ou de pai. O seu caminho é proteger sem se esconder.",
    "Com Ascendente em Leão, você não passa despercebido(a): tem presença, calor e um brilho natural. O seu caminho é mostrar o seu coração ao mundo, com generosidade.",
    "Com Ascendente em Virgem, você transmite elegância discreta, inteligência e vontade de ajudar. Repara em tudo. O seu caminho é servir com amor, sem se exigir a perfeição.",
    "Com Ascendente em Libra, você conquista pela gentileza, pelo charme e pelo sentido de justiça. As pessoas sentem-se bem ao seu lado. O seu caminho é o equilíbrio e as parcerias.",
    "Com Ascendente em Escorpião, você tem um olhar profundo e magnético, que parece ler a alma dos outros. É intenso(a) e reservado(a). O seu caminho é a transformação.",
    "Com Ascendente em Sagitário, você traz alegria, optimismo e sede de liberdade. Parece sempre pronto(a) para uma viagem. O seu caminho é procurar sentido e ensinar o que aprende.",
    "Com Ascendente em Capricórnio, você transmite seriedade, maturidade e força. Os outros confiam na sua palavra. O seu caminho é subir a montanha com paciência e chegar lá acima.",
    "Com Ascendente em Aquário, você é original, livre e um pouco à frente do seu tempo. As pessoas vêem em si um amigo diferente de todos. O seu caminho é ser quem é, sem pedir licença.",
    "Com Ascendente em Peixes, você tem um ar sonhador, doce e intuitivo, e sente o que os outros não dizem. O seu caminho é a espiritualidade, a arte e a compaixão.",
  ];

  raiz.TextosAstral = { ELEMENTOS, SOL, LUA, ASC };
})(typeof window !== "undefined" ? window : globalThis);
