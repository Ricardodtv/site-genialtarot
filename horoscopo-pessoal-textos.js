/* Horóscopo Pessoal do Dia — textos — Genial Tarot (28/10/2026)
   ╔══════════════════════════════════════════════════════════════════╗
   ║  EXPERIÊNCIA 28/10/2026 — página da área Novidades.              ║
   ║  Textos por aprovar pelo Mestre Alberto.                         ║
   ╚══════════════════════════════════════════════════════════════════╝
   Cada trânsito lê-se em duas frases: a do planeta de hoje (PLANETA, pela natureza do
   aspecto: conj = conjunção, har = sextil ou trígono, ten = quadratura ou oposição) e a do
   ponto natal que ele toca (ALVO). A casa da Lua de hoje tem um texto para cada uma das 12.
   Tom: caloroso, honesto, sem promessas de saúde, dinheiro ou amor. Trata-se por «você».
   Evitam-se as palavras que só se usam de um lado do Atlântico (facto/fato, equipa/equipe…). */
(function (raiz) {
  // O planeta de hoje × a natureza do aspecto (10 × 3 = 30 textos)
  const PLANETA = {
    lua: {
      conj: "A Lua passa hoje por cima de um ponto sensível do seu mapa, e as emoções ficam mais à flor da pele. O que sentir hoje vem com força: vale a pena escutar antes de decidir.",
      har: "A Lua de hoje conversa bem com o seu céu. É um dia de humor mais leve, em que as pessoas e as situações tendem a colaborar sem grande esforço.",
      ten: "A Lua de hoje cria algum atrito no seu céu: pequenas irritações, cansaço ou uma sensibilidade maior do que o costume. Passa depressa, porque a Lua muda de lugar em poucas horas, por isso não leve tudo a peito.",
    },
    sol: {
      conj: "O Sol de hoje ilumina em cheio este ponto do seu mapa. É um dia de destaque: o que você fizer fica mais à vista, tanto o que já está bom como o que ainda pede ajuste.",
      har: "O Sol de hoje lhe dá um empurrão de vitalidade e de confiança. Bom momento para dar a cara, pedir o que precisa e avançar com um plano.",
      ten: "O Sol de hoje pede mais esforço do que o habitual. Pode sentir que tem de provar o seu valor, ou que a energia rende menos. Dose as forças e escolha bem as batalhas.",
    },
    mercurio: {
      conj: "Mercúrio de hoje põe a cabeça a trabalhar neste ponto do seu mapa: muitas ideias, mensagens e conversas. Anote o que lhe ocorrer, porque há boas pistas no meio do barulho.",
      har: "Mercúrio favorece as conversas, os estudos e os papéis. Se tem algo para dizer, explicar ou combinar, hoje as palavras saem com mais clareza.",
      ten: "Mercúrio de hoje traz algum ruído: mal-entendidos, atrasos, mensagens que não chegam como queria. Releia antes de enviar e confirme o que é importante.",
    },
    venus: {
      conj: "Vénus de hoje toca este ponto do seu mapa com doçura. Dia bom para o carinho, para o que é belo e para se tratar bem.",
      har: "Vénus abre espaço para a gentileza: um elogio, um reencontro, um gesto simpático. É um dia que favorece a harmonia e os pequenos prazeres.",
      ten: "Vénus de hoje pode trazer vontade de mais do que há: mais atenção, mais mimo, mais compras. Pergunte a si mesmo(a) do que precisa de verdade antes de pedir aos outros.",
    },
    marte: {
      conj: "Marte de hoje acende este ponto do seu mapa. Há energia de sobra e vontade de agir já. Use-a num objetivo concreto: parada, ela vira impaciência.",
      har: "Marte dá coragem e iniciativa. Bom dia para começar o que tem adiado, para mexer o corpo e para defender com calma o que é seu.",
      ten: "Marte de hoje deixa o pavio mais curto, em você ou à sua volta. Respire antes de responder e evite a pressa, ao volante e nas decisões.",
    },
    jupiter: {
      conj: "Júpiter passa por este ponto do seu mapa, um encontro que só acontece a cada doze anos. Traz confiança, vontade de crescer e portas que se entreabrem: vale a pena reparar nelas.",
      har: "Júpiter sopra a seu favor: mais otimismo, mais boa vontade à sua volta e mais vontade de aprender. Aproveite para semear algo que queira ver crescer.",
      ten: "Júpiter em tensão convida ao exagero: prometer demais, gastar demais, esperar demais. Nestes dias, a medida certa é a sua melhor aliada.",
    },
    saturno: {
      conj: "Saturno pousa neste ponto do seu mapa, um encontro que se repete mais ou menos a cada 29 anos. É tempo de assumir responsabilidades e construir com paciência. Pesa, mas o que se faz agora fica sólido.",
      har: "Saturno dá estrutura e constância. Bom momento para organizar, cumprir prazos e dar um passo sério num projeto de longo prazo.",
      ten: "Saturno em tensão pode trazer a sensação de que tudo anda devagar, ou de que há obstáculos no caminho. Não desista: é um teste de persistência, não um muro.",
    },
    urano: {
      conj: "Urano, o planeta das surpresas, passa por este ponto do seu mapa. Algo pede renovação: uma rotina, uma ideia sobre si mesmo(a), uma forma de viver. Esteja aberto(a) ao inesperado.",
      har: "Urano traz ideias novas e vontade de experimentar. Um pequeno risco bem pensado, uma mudança de ares ou uma conversa diferente podem ser muito bem-vindos.",
      ten: "Urano em tensão mexe com o que parecia estável: imprevistos, mudanças de planos, inquietação. Deixe alguma folga na agenda e flexibilidade no coração.",
    },
    neptuno: {
      conj: "Neptuno, o planeta dos sonhos, envolve este ponto do seu mapa. A intuição fica mais fina, e a sensibilidade também. Bom para a fé, a arte e o descanso; menos bom para assinar sem ler.",
      har: "Neptuno favorece a intuição, a imaginação e a compaixão. Preste atenção aos sonhos, às coincidências e ao que sente sem saber explicar.",
      ten: "Neptuno em tensão pode deixar as coisas menos nítidas: dúvidas, cansaço, promessas pouco claras. Confirme tudo duas vezes e não decida enquanto estiver tudo turvo.",
    },
    plutao: {
      conj: "Plutão, o planeta da transformação profunda, trabalha este ponto do seu mapa durante uma longa temporada. Algo antigo vai dando lugar a algo novo, e você sai disto mais forte e mais verdadeiro(a).",
      har: "Plutão dá força interior e vontade de ir ao fundo das questões. Bom momento para largar um hábito, resolver uma pendência antiga ou recomeçar com mais verdade.",
      ten: "Plutão em tensão traz à superfície o que estava escondido: medos, ciúmes, disputas de poder. Olhe para isso com coragem e sem dramatismo: é assim que se cura.",
    },
  };

  // O ponto natal tocado × a natureza do aspecto (4 × 3 = 12 textos)
  const ALVO = {
    sol: {
      conj: "Ao tocar no seu Sol natal, o tema do dia é você: a sua vontade, a sua energia e o rumo que quer dar à vida.",
      har: "Ao tocar no seu Sol natal, reforça a sua confiança e ajuda a mostrar o melhor de si.",
      ten: "Ao tocar no seu Sol natal, põe à prova a sua paciência e o seu orgulho. Lembre-se do que é realmente importante para você.",
    },
    lua: {
      conj: "Ao tocar na sua Lua natal, o dia fala ao coração: a casa, a família e aquilo de que precisa para se sentir em segurança.",
      har: "Ao tocar na sua Lua natal, traz conforto emocional: bom dia para estar com quem ama e cuidar do seu canto.",
      ten: "Ao tocar na sua Lua natal, mexe com emoções antigas. Seja gentil consigo e não tome decisões de cabeça quente.",
    },
    venus: {
      conj: "Ao tocar na sua Vénus natal, o tema é o afeto: o amor, as amizades e o prazer de viver.",
      har: "Ao tocar na sua Vénus natal, favorece o amor, as amizades e o gosto pelas coisas bonitas.",
      ten: "Ao tocar na sua Vénus natal, pede atenção ao equilíbrio entre dar e receber nos afetos.",
    },
    asc: {
      conj: "Ao tocar no seu Ascendente, mexe com a forma como você se apresenta: a imagem, o corpo e a primeira impressão.",
      har: "Ao tocar no seu Ascendente, ajuda a causar boa impressão e a abrir caminhos novos.",
      ten: "Ao tocar no seu Ascendente, aumenta a exposição ao olhar dos outros. Seja autêntico(a) e não se justifique demais.",
    },
  };

  // A casa por onde passa a Lua de hoje (12 textos; ordem: Casa 1 … Casa 12)
  const CASA = [
    ["a casa do eu", "Você está mais visível e mais sensível ao mesmo tempo. Dia para cuidar da imagem e do corpo, e para começar algo que seja só seu."],
    ["a casa dos recursos e do valor próprio", "As emoções andam ligadas à segurança material. Bom dia para rever as contas com calma, e para se lembrar do quanto você vale."],
    ["a casa das conversas e dos caminhos curtos", "Mensagens, telefonemas e ideias circulam mais. Um recado bem dado, uma visita a um irmão ou a um vizinho, uma volta pelo bairro: o dia anda pela palavra."],
    ["a casa do lar e das raízes", "O coração pede casa, família e recolhimento. Um bom dia para arrumar o seu espaço, cozinhar algo com carinho e recarregar energia."],
    ["a casa da alegria e do romance", "Dê espaço ao prazer: um passatempo, uma brincadeira, um encontro que aqueça o coração. A criatividade está mais solta."],
    ["a casa da rotina e do trabalho do dia a dia", "Bom dia para pôr ordem nas tarefas, organizar a semana e cuidar de si com pequenos gestos: dormir bem, comer com calma, caminhar."],
    ["a casa dos outros e das parcerias", "As relações pedem atenção, no amor, na sociedade ou na amizade. Ouvir o outro com calma vale mais do que ter razão."],
    ["a casa das emoções profundas", "Dia intenso por dentro. Bom para conversas sinceras, para largar o que pesa e para olhar a fundo o que sente."],
    ["a casa dos horizontes largos", "A alma pede sentido e novidade: viagens, estudos, fé. Um livro, um curso ou um plano de viagem podem animar o dia."],
    ["a casa da carreira e do lugar no mundo", "O que você faz fica mais à vista. Dia para mostrar o seu trabalho e pensar com calma nos seus objetivos."],
    ["a casa dos amigos e dos projetos", "Bom dia para retomar uma amizade, juntar-se a um grupo e partilhar os seus sonhos com quem os apoia."],
    ["a casa do silêncio e do mundo interior", "A energia anda mais baixa e a intuição mais alta. Descanse, reze, medite, e não se cobre demais hoje."],
  ];

  // Quando o céu de hoje faz poucos aspectos fortes ao mapa
  const CALMO = "Hoje há poucos aspectos fortes ao seu mapa: um dia mais sereno, bom para seguir o seu próprio ritmo e preparar com calma o que vem a seguir.";

  // As oito fases da Lua (só o nome; o ângulo Lua − Sol decide)
  const FASES = ["Lua Nova", "Lua Crescente", "Quarto Crescente", "Lua Gibosa Crescente", "Lua Cheia", "Lua Gibosa Minguante", "Quarto Minguante", "Lua Minguante"];

  raiz.TextosHoroscopo = { PLANETA, ALVO, CASA, CALMO, FASES };
})(typeof window !== "undefined" ? window : globalThis);
