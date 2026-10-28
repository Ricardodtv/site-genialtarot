/* O Mapa do Casal (sinastria) — textos — Genial Tarot (28/10/2026)
   ╔══════════════════════════════════════════════════════════════════╗
   ║  EXPERIÊNCIA 28/10/2026 — página da área Novidades.              ║
   ║  Textos por aprovar pelo Mestre Alberto.                         ║
   ╚══════════════════════════════════════════════════════════════════╝
   Um texto por par de pontos (Sol, Lua, Vénus, Marte, Ascendente: 15 pares) e pela natureza
   do aspecto (conj = conjunção, har = sextil ou trígono, ten = quadratura ou oposição):
   15 × 3 = 45 textos. O par é simétrico («o Sol de um e a Lua do outro»), por isso os textos
   não dizem quem é quem: os nomes vão no título de cada aspecto.
   Mais cinco leituras da nota de afinidade e as frases de apoio.
   Tom: caloroso e honesto; nenhum céu garante nem condena um amor. */
(function (raiz) {
  const PAR = {
    "sol|sol": {
      conj: "Os dois Sóis no mesmo lugar: vocês têm a mesma essência e a mesma maneira de brilhar. Há um reconhecimento imediato; o cuidado é não disputarem o mesmo palco.",
      har: "Os Sóis de vocês combinam bem: as vontades caminham na mesma direção e cada um respeita o jeito do outro. É a base de uma boa amizade dentro do amor.",
      ten: "Os Sóis de vocês puxam para lados diferentes: duas personalidades fortes, dois ritmos. A relação cresce quando cada um deixa o outro ser quem é, sem o querer mudar.",
    },
    "sol|lua": {
      conj: "O Sol de um pousa na Lua do outro, um dos encontros mais clássicos do amor. Um ilumina, o outro acolhe, e há aquela sensação de se conhecerem há muito tempo.",
      har: "O Sol de um e a Lua do outro entendem-se sem esforço. Um sente-se compreendido, o outro sente-se seguro: é uma harmonia que dá vontade de construir juntos.",
      ten: "O Sol de um desafia a Lua do outro: o que um precisa nem sempre é o que o outro oferece. Com diálogo, esta tensão ensina muito sobre cuidar um do outro.",
    },
    "sol|venus": {
      conj: "O Sol de um encontra a Vénus do outro: há admiração, ternura e um prazer genuíno na companhia. É um dos aspectos mais doces entre duas pessoas.",
      har: "O Sol e a Vénus de vocês conversam com carinho: elogios fáceis, gostos parecidos e vontade de agradar.",
      ten: "O Sol de um e a Vénus do outro desencontram-se nos gostos e nos mimos. Nada que não se resolva com atenção àquilo que faz o outro feliz.",
    },
    "sol|marte": {
      conj: "O Sol de um acende o Marte do outro: há energia, iniciativa e muita vida a dois. Juntos fazem acontecer; convém só não transformar tudo em competição.",
      har: "O Sol e o Marte de vocês dão força ao casal: um motiva o outro, e os projetos a dois saem do papel.",
      ten: "O Sol de um e o Marte do outro chocam às vezes: discussões rápidas, orgulhos feridos. É energia a mais; posta num objetivo comum, vira motor.",
    },
    "sol|asc": {
      conj: "O Sol de um cai no Ascendente do outro: há atração à primeira vista e a sensação de que o outro revela quem você é. Um laço forte de identificação.",
      har: "O Sol de um favorece o Ascendente do outro: vocês sentem-se à vontade juntos e apresentam-se bem como casal.",
      ten: "O Sol de um e o Ascendente do outro estranham-se no início: maneiras diferentes de estar no mundo. Com o tempo, a diferença pode virar complemento.",
    },
    "lua|lua": {
      conj: "As duas Luas juntas: vocês sentem da mesma maneira e precisam das mesmas coisas para estar bem. Um ninho comum, cheio de entendimento.",
      har: "As Luas de vocês harmonizam-se: os humores encaixam, e um sabe acalmar o outro.",
      ten: "As Luas de vocês têm necessidades diferentes: um quer proximidade quando o outro quer espaço, ou ao contrário. Falar do que cada um sente evita mágoas guardadas.",
    },
    "lua|venus": {
      conj: "A Lua de um e a Vénus do outro juntas: ternura pura. É um aspecto de carinho, de mimo e de vontade de cuidar.",
      har: "A Lua e a Vénus de vocês entendem-se bem: afeto fácil, gestos de cuidado e uma doçura que se nota.",
      ten: "A Lua de um e a Vénus do outro pedem afinação: a forma de um mostrar carinho nem sempre é a que o outro reconhece. Aprender a «língua» do outro faz toda a diferença.",
    },
    "lua|marte": {
      conj: "A Lua de um e o Marte do outro juntos: paixão e intensidade emocional. Há desejo, mas também sensibilidade à flor da pele; a palavra-chave é delicadeza.",
      har: "A Lua e o Marte de vocês dão calor à relação: o desejo e o carinho andam juntos, e há coragem para enfrentar o que vier.",
      ten: "A Lua de um e o Marte do outro podem magoar-se sem querer: uma palavra brusca cai fundo. Com cuidado, esta faísca vira paixão em vez de mágoa.",
    },
    "lua|asc": {
      conj: "A Lua de um no Ascendente do outro: uma familiaridade instintiva. Um sente-se em casa ao lado do outro, quase sem explicação.",
      har: "A Lua e o Ascendente de vocês combinam: há conforto e naturalidade no dia a dia juntos.",
      ten: "A Lua de um e o Ascendente do outro desencontram-se às vezes: o que um mostra por fora não é o que o outro precisa por dentro. Paciência e perguntas sinceras ajudam.",
    },
    "venus|venus": {
      conj: "As duas Vénus juntas: os mesmos gostos, a mesma forma de amar. Os programas a dois saem com facilidade e o prazer é partilhado.",
      har: "As Vénus de vocês combinam: gostos que se completam e uma maneira parecida de dar e de receber amor.",
      ten: "As Vénus de vocês têm gostos diferentes, no amor e na vida. Pode ser um desafio ou uma riqueza: cada um apresenta ao outro um mundo novo.",
    },
    "venus|marte": {
      conj: "A Vénus de um e o Marte do outro juntos: o aspecto clássico da atração. Química forte, desejo e vontade de estar perto.",
      har: "A Vénus e o Marte de vocês conversam muito bem: atração natural, um ritmo parecido e um romance que flui.",
      ten: "A Vénus de um e o Marte do outro em tensão: atração com faísca. Há química e também alguma provocação; é essa tensão que mantém a chama acesa, desde que haja respeito.",
    },
    "venus|asc": {
      conj: "A Vénus de um no Ascendente do outro: um acha o outro bonito, simplesmente. Há encanto e admiração desde o primeiro olhar.",
      har: "A Vénus e o Ascendente de vocês harmonizam-se: gentileza, charme e vontade de agradar.",
      ten: "A Vénus de um e o Ascendente do outro estranham-se no estilo: o que um acha bonito, o outro faz de outra forma. Pequenas diferenças que pedem humor e tolerância.",
    },
    "marte|marte": {
      conj: "Os dois Martes juntos: a mesma garra e o mesmo ritmo. Juntos têm muita força, mas convém combinar quem decide o quê.",
      har: "Os Martes de vocês fazem uma boa dupla: energias que se somam e iniciativas que se apoiam.",
      ten: "Os Martes de vocês chocam: duas vontades fortes, com pressa em direções diferentes. As discussões podem surgir depressa; o segredo é escolher as batalhas.",
    },
    "marte|asc": {
      conj: "O Marte de um no Ascendente do outro: há impacto, atração física e uma energia que desperta. Às vezes é intenso demais; o equilíbrio vem com o tempo.",
      har: "O Marte e o Ascendente de vocês combinam: um encoraja o outro a agir e a mostrar-se com confiança.",
      ten: "O Marte de um e o Ascendente do outro podem soar a provocação: um empurra, o outro sente-se pressionado. São ritmos diferentes que pedem negociação.",
    },
    "asc|asc": {
      conj: "Os Ascendentes no mesmo grau: vocês têm um jeito parecido de estar no mundo, e as outras pessoas notam a semelhança.",
      har: "Os Ascendentes de vocês combinam bem: estilos que se completam e uma imagem de casal harmoniosa.",
      ten: "Os Ascendentes de vocês têm estilos diferentes de chegar às coisas. Nada de grave: é só respeitar a maneira do outro.",
    },
  };

  // A leitura da nota (de cima para baixo: a primeira cujo mínimo a nota alcança)
  const NOTA = [
    [85, "Uma sintonia rara", "Os céus de vocês conversam com uma facilidade pouco comum: há muitos pontos de encontro e poucos atritos. É um bom começo; o resto, como em qualquer amor, quem constrói são os dois."],
    [70, "Uma ligação forte", "Há mais harmonia do que tensão entre os céus de vocês, e os encontros importantes estão lá. Os desafios que aparecem são do tamanho certo para os dois crescerem."],
    [55, "Uma boa base, com contrastes", "Os céus de vocês têm pontos de encontro e também diferenças claras. É um casal que se completa quando aprende a respeitar o ritmo de cada um."],
    [40, "Um encontro que pede trabalho a dois", "Há tensões marcadas entre os céus de vocês, ao lado de alguns pontos de harmonia. Não é um mau sinal: muitas relações fortes nascem de diferenças que os dois decidem compreender."],
    [0, "Dois céus muito diferentes", "Os mapas de vocês falam línguas diferentes, e isso pede paciência e conversa. A diferença também atrai e ensina; o céu mostra o terreno, não decide o caminho."],
  ];
  const HONESTA = "A nota é um retrato simbólico do encontro dos dois céus, não uma sentença: há casais felizes com notas modestas e casais com notas altas que não se entendem. O que faz uma relação é o que os dois constroem.";
  const POUCOS = "Os céus de vocês fazem poucos aspectos fortes entre si. Quando isso acontece, a relação depende menos dos astros e mais das escolhas de cada dia.";
  const POUCOS_TITULO = "Poucos laços fortes entre os dois céus";
  const INCERTO = "aproximado: sem a hora de nascimento, a Lua pode estar uns graus ao lado";

  raiz.TextosCasal = { PAR, NOTA, HONESTA, POUCOS, POUCOS_TITULO, INCERTO };
})(typeof window !== "undefined" ? window : globalThis);
