/* Textos da Carta de Tarot de Nascimento — Genial Tarot (28/10/2026)
   EXPERIÊNCIA 28/10/2026 — textos por aprovar pelo Mestre Alberto.
   NASC: um texto por arcano, lido como carta de nascimento (o arcano 1, O Mago, só aparece como par:
   pelo método de Greer nunca é a carta principal). SIGNO: uma frase para o arcano de cada signo
   (Golden Dawn), de Áries a Peixes. Escritos de raiz, por «você», para servir ao Brasil e a Portugal. */
(function (raiz) {
  // [nome, número romano, imagem (o baralho oficial, a mesma do tarot-gratis.html), página do arcano no site]
  const ARCANOS = [
    ["O Louco", "0", "the-fool", "arcano-00-o-louco.html"],
    ["O Mago", "I", "the-magician", "arcano-01-o-mago.html"],
    ["A Sacerdotisa", "II", "the-high-priestess", "arcano-02-a-sacerdotisa.html"],
    ["A Imperatriz", "III", "the-empress", "arcano-03-a-imperatriz.html"],
    ["O Imperador", "IV", "the-emperor", "arcano-04-o-imperador.html"],
    ["O Hierofante", "V", "the-heirophant", "arcano-05-o-hierofante.html"],
    ["Os Enamorados", "VI", "the-lovers", "arcano-06-os-enamorados.html"],
    ["O Carro", "VII", "the-chariot", "arcano-07-o-carro.html"],
    ["A Força", "VIII", "strength", "arcano-08-a-forca.html"],
    ["O Eremita", "IX", "the-hermit", "arcano-09-o-eremita.html"],
    ["A Roda da Fortuna", "X", "wheel-of-fortune", "arcano-10-a-roda-da-fortuna.html"],
    ["A Justiça", "XI", "justice", "arcano-11-a-justica.html"],
    ["O Enforcado", "XII", "the-hanged-man", "arcano-12-o-enforcado.html"],
    ["A Morte", "XIII", "death", "arcano-13-a-morte.html"],
    ["A Temperança", "XIV", "temperance", "arcano-14-a-temperanca.html"],
    ["O Diabo", "XV", "the-devil", "arcano-15-o-diabo.html"],
    ["A Torre", "XVI", "the-tower", "arcano-16-a-torre.html"],
    ["A Estrela", "XVII", "the-star", "arcano-17-a-estrela.html"],
    ["A Lua", "XVIII", "the-moon", "arcano-18-a-lua.html"],
    ["O Sol", "XIX", "the-sun", "arcano-19-o-sol.html"],
    ["O Julgamento", "XX", "judgement", "arcano-20-o-julgamento.html"],
    ["O Mundo", "XXI", "the-world", "arcano-21-o-mundo.html"],
  ];

  const NASC = [
    /* 0 O Louco */ "Você veio ao mundo com a coragem de quem começa do zero. A sua alma aprende andando: precisa de liberdade, de ar novo e de espaço para errar sem se castigar. O desafio é não fugir quando o caminho pede compromisso; a sua força é lembrar aos outros que a vida também se faz de saltos de confiança.",
    /* 1 O Mago */ "O Mago dá-lhe o dom de transformar ideias em coisas reais. Você tem jeito com as mãos, com as palavras ou com as duas, e sente-se vivo quando cria. O cuidado está em não dispersar o talento por mil projetos: quando escolhe um e põe nele a sua vontade, as coisas acontecem.",
    /* 2 A Sacerdotisa */ "Você nasceu com um saber que não vem dos livros. Sente as pessoas antes de elas falarem e muitas vezes sabe a resposta antes de ter as provas. A Sacerdotisa pede-lhe que confie nesse silêncio interior e que não o esconda por medo de parecer estranho: a sua intuição é uma bússola, não um defeito.",
    /* 3 A Imperatriz */ "A Imperatriz faz de você alguém que cuida, que alimenta e que faz crescer. Onde você está, as coisas florescem: pessoas, plantas, projetos, uma casa. A lição é aprender a receber tanto quanto dá, e a lembrar que você também merece ser cuidado. A beleza e o prazer não são luxos na sua vida, são combustível.",
    /* 4 O Imperador */ "Você nasceu para construir bases sólidas. Gosta de ordem, de palavra dada e de saber onde pisa, e os outros sentem-se seguros ao seu lado. O Imperador pede-lhe que use essa força para proteger e não para controlar: quando a firmeza vem com ternura, você torna-se um porto de abrigo.",
    /* 5 O Hierofante */ "O Hierofante liga você àquilo que tem raízes: a família, a fé, os mestres, as tradições que dão sentido à vida. Você aprende com quem veio antes e tem jeito para ensinar. O desafio é distinguir o que herdou e ainda lhe serve do que já pode deixar ir, para que a sua crença seja sua e não emprestada.",
    /* 6 Os Enamorados */ "A sua vida faz-se de escolhas do coração. Os Enamorados dão-lhe um enorme poder de ligação: você sente a fundo o amor, a amizade e a parceria. A grande aprendizagem é escolher de acordo com os seus valores, mesmo quando isso custa, porque é aí que você se reconhece por inteiro.",
    /* 7 O Carro */ "Você nasceu com vontade de avançar. Quando decide um rumo, junta forças que nem sabia que tinha e segue em frente. O Carro pede-lhe que segure as rédeas com calma: nem tudo se vence a correr, e as maiores vitórias da sua vida vêm quando sabe para onde vai e porquê.",
    /* 8 A Força */ "A Força dá-lhe uma coragem suave: a de quem acalma em vez de gritar. Você tem uma resistência interior que aparece nos momentos difíceis e uma paciência que conquista até os mais desconfiados. O caminho é tratar os seus próprios medos com a mesma ternura com que trata os dos outros.",
    /* 9 O Eremita */ "Você nasceu com uma lanterna na mão. Precisa de tempo a sós para pensar, para estudar e para ouvir a sua própria voz, e é desse silêncio que tira a sabedoria que depois partilha. O Eremita lembra-lhe que recolher-se não é fugir; mas também que a luz que encontra foi feita para iluminar o caminho de mais alguém.",
    /* 10 A Roda da Fortuna */ "A Roda da Fortuna diz que a sua vida se move em ciclos, e que você tem um talento especial para se adaptar quando tudo gira. Há fases de subida e fases de espera, e você aprende com as duas. O segredo é não se agarrar ao que já passou: quando aceita o movimento, encontra sempre um novo ponto de apoio.",
    /* 11 A Justiça */ "Você nasceu com um sentido apurado do que é justo. Pesa as coisas, procura a verdade e não descansa enquanto algo está torto. A Justiça pede-lhe honestidade, primeiro consigo mesmo, e um pouco de compaixão na balança: ser justo também é saber dar uma segunda oportunidade.",
    /* 12 O Enforcado */ "O Enforcado dá-lhe uma forma diferente de olhar o mundo. Você vê o que os outros não veem porque é capaz de parar, de esperar e de virar o problema ao contrário. A lição é não confundir entrega com sacrifício: as suas pausas têm valor quando lhe trazem um olhar novo, não quando o prendem.",
    /* 13 A Morte */ "Esta carta não fala de fim, fala de renovação. Você nasceu com a capacidade rara de fechar capítulos e de renascer deles mais inteiro. As mudanças profundas fazem parte do seu caminho, e cada uma deixa-o mais verdadeiro. O desafio é largar a tempo o que já acabou, para dar espaço ao que quer nascer.",
    /* 14 A Temperança */ "A Temperança faz de você um alquimista do dia a dia: junta o que parece oposto e encontra o meio-termo onde os outros só veem conflito. Tem um dom natural para curar, acalmar e reconciliar. O seu caminho pede paciência com os próprios processos, porque o que você constrói devagar fica para durar.",
    /* 15 O Diabo */ "O Diabo, como carta de nascimento, fala de uma enorme força vital: desejo, magnetismo, ambição e coragem para olhar a sombra de frente. Você conhece o lado intenso da vida. A lição é perceber o que o prende, seja um hábito, um medo ou uma relação, porque quando se liberta disso a sua energia torna-se imparável.",
    /* 16 A Torre */ "A Torre dá-lhe a coragem de dizer a verdade e de derrubar o que é falso. Na sua vida, os grandes passos vêm muitas vezes de abanões que parecem desastres e acabam por ser libertações. Você aprende a reconstruir sobre bases mais honestas; e com o tempo torna-se a pessoa que ajuda os outros a fazer o mesmo.",
    /* 17 A Estrela */ "Você nasceu com uma luz de esperança que não se apaga com facilidade. A Estrela dá-lhe inspiração, sensibilidade e um jeito especial de devolver a fé a quem a perdeu. O seu desafio é acreditar em si com a mesma generosidade com que acredita nos outros, e deixar-se ser visto como é.",
    /* 18 A Lua */ "A Lua dá-lhe uma imaginação funda e uma sensibilidade que capta o que não se diz. Os sonhos, as emoções e os pressentimentos falam alto em você. O caminho é aprender a distinguir a intuição do medo, e a atravessar a noite sem pressa: muitas das suas melhores respostas chegam quando aceita não ver tudo de uma vez.",
    /* 19 O Sol */ "O Sol faz de você alguém que aquece o ambiente onde entra. Tem alegria, clareza e uma vontade sincera de brilhar e de ver os outros brilhar também. A lição é não depender do aplauso para se sentir inteiro, e lembrar que até o Sol precisa de descanso. Quando é autêntico, a sua luz chega longe.",
    /* 20 O Julgamento */ "O Julgamento traz-lhe um chamado: o de despertar e de se reinventar ao longo da vida. Você tem a capacidade de fazer balanços honestos e de recomeçar com mais sabedoria. O desafio é não se julgar com dureza, porque o seu propósito é renascer, não castigar-se pelo que já foi.",
    /* 21 O Mundo */ "O Mundo é a carta de quem nasceu para fechar ciclos com plenitude. Você procura ver o quadro inteiro, juntar as peças e dar sentido ao caminho. Tem jeito para levar as coisas até ao fim e um coração aberto a outras culturas e lugares. A lição é celebrar cada conquista antes de partir para a próxima.",
  ];

  // O arcano de cada signo pela Golden Dawn: [n.º do arcano, a frase]
  const SIGNO = [
    /* Áries */ [4, "O Imperador é a vontade de Áries posta ao serviço de algo que dura: liderar, abrir caminho e assumir a responsabilidade pelo que começa."],
    /* Touro */ [5, "O Hierofante é a paciência de Touro: aprender devagar, guardar o que tem valor e transmitir o que se sabe com os pés bem assentes na terra."],
    /* Gémeos */ [6, "Os Enamorados são a escolha de Gémeos: duas vozes, dois caminhos, e a arte de ligar pessoas e ideias até encontrar a sua verdade."],
    /* Câncer */ [7, "O Carro é a força protetora de Câncer: uma carapaça que guarda o que se ama e uma determinação enorme quando a família ou a casa precisam."],
    /* Leão */ [8, "A Força é o coração de Leão: coragem, dignidade e a capacidade de domar o próprio orgulho com generosidade."],
    /* Virgem */ [9, "O Eremita é o olhar atento de Virgem: estudar, aperfeiçoar e servir com humildade, sem fazer alarde."],
    /* Libra */ [11, "A Justiça é a balança de Libra: procurar o equilíbrio, ouvir os dois lados e decidir com justiça e com elegância."],
    /* Escorpião */ [13, "A Morte é a transformação de Escorpião: descer ao fundo, largar o que já não vive e renascer com mais verdade."],
    /* Sagitário */ [14, "A Temperança é a procura de Sagitário: misturar mundos, ideias e crenças até encontrar um sentido maior para a viagem."],
    /* Capricórnio */ [15, "O Diabo é a ambição de Capricórnio: a força para subir a montanha e a lição de não se deixar prender pelo poder ou pelo medo."],
    /* Aquário */ [17, "A Estrela é o sonho de Aquário: a esperança no futuro, a vontade de ajudar o coletivo e a liberdade de ser diferente."],
    /* Peixes */ [18, "A Lua é a sensibilidade de Peixes: a imaginação, os sonhos e a intuição que atravessa as águas mais fundas."],
  ];

  raiz.TextosCarta = { ARCANOS, NASC, SIGNO };
})(typeof window !== "undefined" ? window : globalThis);
