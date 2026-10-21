/* Mapa do Ano 2027 (Numerologia) — textos da amostra grátis — Genial Tarot (21/10/2026)
   ╔══════════════════════════════════════════════════════════════════╗
   ║  MAQUETE — textos por aprovar pelo Mestre Alberto.               ║
   ║  Nada disto está publicado. Não ligar a página sem o «sim» dele. ║
   ╚══════════════════════════════════════════════════════════════════╝
   Numerologia pitagórica. Ano Pessoal = dia + mês de nascimento + o ano em
   análise, somando os algarismos até ficar um só (1 a 9). Mês Pessoal = Ano
   Pessoal + o número do mês, reduzido da mesma forma. Caminho de Vida = todos
   os algarismos da data de nascimento, reduzidos.
   Tom: caloroso, honesto, tendências e não destino. Índice 1 a 9 (o 0 não se usa). */
(function (raiz) {
  const TITULO = [, "O ano dos começos", "O ano das parcerias", "O ano da expressão", "O ano das bases sólidas",
    "O ano da mudança", "O ano do amor e da família", "O ano da alma", "O ano da colheita", "O ano dos fechos"];

  // «A sua motivação para 2027»
  const MOTIVACAO = [,
    "2027 é para você um Ano Pessoal 1: um ciclo de nove anos fecha-se e outro começa. É o momento de plantar sementes novas, de tomar a iniciativa e de dizer «sim» àquilo que adiou. A energia do ano favorece quem ousa dar o primeiro passo, mesmo sem ter tudo planeado. O que começar agora vai acompanhá-lo(a) durante muito tempo: escolha com o coração e avance com coragem.",
    "2027 é para você um Ano Pessoal 2: depois do arranque, chega o tempo de cultivar. É um ano de paciência, de escuta e de alianças. As coisas crescem devagar, por baixo da terra, e as melhores oportunidades chegam através das pessoas. A diplomacia, a sensibilidade e a cooperação são a sua maior força. Não force o ritmo: o que é seu está a amadurecer.",
    "2027 é para você um Ano Pessoal 3: um ano de alegria, de criatividade e de comunicação. Tudo o que tem a ver com falar, escrever, criar, aparecer e conviver está favorecido. É tempo de mostrar quem é, de se divertir e de expandir o seu círculo. O desafio é não dispersar a energia por demasiadas coisas: escolha onde brilhar.",
    "2027 é para você um Ano Pessoal 4: um ano de trabalho, de organização e de construção. É o momento de pôr ordem na casa, nas contas e na saúde, e de assentar os alicerces do que quer para os próximos anos. Pode parecer um ano mais exigente, mas cada esforço conta a dobrar. Disciplina hoje é liberdade amanhã.",
    "2027 é para você um Ano Pessoal 5: o ano da mudança e da liberdade. Viagens, novidades, encontros inesperados e portas que se abrem de repente. É tempo de sair da rotina, de experimentar e de se adaptar. A vida pede movimento: quem resiste à mudança cansa-se, quem dança com ela descobre caminhos novos.",
    "2027 é para você um Ano Pessoal 6: o ano do amor, da família e da responsabilidade. O coração e a casa ficam no centro de tudo: relações que se aprofundam, compromissos, cuidar e ser cuidado(a). É um ano favorável para casar, reconciliar, mudar de casa ou embelezar a vida. O desafio é cuidar dos outros sem se esquecer de si.",
    "2027 é para você um Ano Pessoal 7: o ano da alma. Um tempo mais calmo e interior, de estudo, de reflexão e de espiritualidade. As respostas não vêm de fora: vêm do silêncio. É um ano excelente para aprender, para se conhecer melhor e para se afastar do ruído. Confie na sua intuição: ela vai estar mais afiada do que nunca.",
    "2027 é para você um Ano Pessoal 8: o ano da colheita e do poder pessoal. O esforço dos últimos anos começa a dar frutos, sobretudo no trabalho e no dinheiro. É tempo de ambição, de negociar, de assumir o comando e de pedir o que merece. O equilíbrio entre o material e o espiritual é a chave para que a colheita seja farta.",
    "2027 é para você um Ano Pessoal 9: o ano dos fechos. Um ciclo de nove anos chega ao fim, e a vida pede-lhe que arrume, perdoe e liberte o que já cumpriu o seu papel. É um ano de generosidade, de compaixão e de balanço. Largar não é perder: é abrir espaço para o recomeço que vem em 2028.",
  ];

  // «As oportunidades mais fortes»
  const OPORTUNIDADES = [,
    ["Começar um projecto novo", "Mudar de rumo profissional", "Afirmar a sua independência"],
    ["Parcerias e sociedades", "Aprofundar uma relação", "Resolver com diplomacia"],
    ["Criatividade e comunicação", "Vida social e novos amigos", "Mostrar o seu talento"],
    ["Organizar as finanças", "Construir algo duradouro", "Cuidar da saúde e do corpo"],
    ["Viagens e mudanças", "Novas experiências", "Libertar-se da rotina"],
    ["Casamento e compromisso", "Harmonia em casa", "Reconciliações"],
    ["Estudo e especialização", "Espiritualidade", "Autoconhecimento"],
    ["Dinheiro e negócios", "Reconhecimento profissional", "Liderança"],
    ["Fechar ciclos com gratidão", "Perdoar e libertar", "Ajudar os outros"],
  ];

  // O Caminho de Vida (a missão de fundo, que dá o tom a todos os anos)
  const CAMINHO = [,
    "o caminho do líder: veio para abrir caminhos e ser você mesmo(a).",
    "o caminho do diplomata: veio para unir, acolher e cooperar.",
    "o caminho do comunicador: veio para criar, inspirar e alegrar.",
    "o caminho do construtor: veio para dar forma, ordem e segurança.",
    "o caminho do aventureiro: veio para experimentar e ser livre.",
    "o caminho do protector: veio para amar, cuidar e harmonizar.",
    "o caminho do sábio: veio para procurar a verdade e a fé.",
    "o caminho do realizador: veio para conquistar e prosperar.",
    "o caminho do humanitário: veio para servir e compreender.",
  ];

  // A palavra de cada Mês Pessoal (a Linha do Tempo)
  const MES = [, "Começar", "Cooperar", "Expressar", "Construir", "Mudar", "Amar", "Reflectir", "Conquistar", "Libertar"];

  raiz.TextosNumerologia = { TITULO, MOTIVACAO, OPORTUNIDADES, CAMINHO, MES };
})(typeof window !== "undefined" ? window : globalThis);
