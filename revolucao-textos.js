/* Revolução Solar — textos da amostra grátis — Genial Tarot (28/10/2026)
   ╔══════════════════════════════════════════════════════════════════╗
   ║  EXPERIÊNCIA — textos por aprovar pelo Mestre Alberto.           ║
   ╚══════════════════════════════════════════════════════════════════╝
   Significados da astrologia clássica da Revolução Solar: o Ascendente do ano
   (o tom, a forma como o ano se apresenta), a casa onde cai o Sol (a área da
   vida onde se joga o ano) e a Lua do ano (as emoções e as necessidades desses
   doze meses). Tom: caloroso, honesto, sem promessas. Ordem: 0 Áries … 11 Peixes;
   as casas vão de 0 (casa 1) a 11 (casa 12). */
(function (raiz) {
  const ASC = [
    "Você começa este ano com energia de recomeço. O Ascendente em Áries pede iniciativa: é um ciclo para dar o primeiro passo, decidir mais depressa e assumir o que quer, sem esperar pela autorização de ninguém. Cuidado só com a pressa e com as discussões por impulso.",
    "Você entra num ano para construir com calma. O Ascendente em Touro traz vontade de estabilidade, de conforto e de pôr a vida material em ordem. O que plantar com paciência tende a crescer; o que forçar à pressa, demora mais. É um bom ano para cuidar do corpo e do dinheiro.",
    "Você vive um ano de movimento e de conversas. O Ascendente em Gêmeos abre portas através de contactos, estudos, viagens curtas e novas ideias. Há muita coisa a acontecer ao mesmo tempo: o segredo está em escolher onde pôr a sua atenção.",
    "Você começa um ano voltado para dentro e para os seus. O Ascendente em Câncer põe a casa, a família e as emoções no centro. É um ciclo para criar raízes, proteger quem ama e ouvir mais o que sente. A sensibilidade fica à flor da pele: use-a como bússola, não como peso.",
    "Você entra num ano para brilhar. O Ascendente em Leão pede que se mostre, que confie no seu talento e que ocupe o seu lugar. A criatividade, o amor e o reconhecimento ganham força. Lembre-se apenas de que a luz verdadeira aquece os outros, não os ofusca.",
    "Você vive um ano de arrumação e de aperfeiçoamento. O Ascendente em Virgem convida a organizar a rotina, a cuidar da saúde e a fazer bem feito o que faz. Os resultados vêm dos detalhes. Não deixe que a exigência consigo próprio(a) se transforme em crítica constante.",
    "Você começa um ano dedicado às relações. O Ascendente em Libra traz parcerias, acordos e a busca de equilíbrio. Os outros têm um papel importante no seu caminho, no amor e no trabalho. É tempo de escolher com o coração e com a cabeça, e de não se perder a agradar a todos.",
    "Você entra num ano intenso e transformador. O Ascendente em Escorpião pede coragem para ir ao fundo das coisas, largar o que já morreu e renascer mais forte. Os temas guardados vêm à superfície. O que parecer uma crise pode ser, na verdade, uma libertação.",
    "Você vive um ano de horizontes largos. O Ascendente em Sagitário traz vontade de aprender, viajar, acreditar e expandir. É um ciclo de optimismo e de sentido: procure o que lhe dá fé no futuro. Só não prometa mais do que consegue cumprir.",
    "Você começa um ano de responsabilidade e de conquista. O Ascendente em Capricórnio pede disciplina, metas claras e trabalho constante. O esforço deste ano é a base dos próximos. Não é um ano de atalhos, mas é um ano em que o que se constrói fica.",
    "Você entra num ano de liberdade e de mudança. O Ascendente em Aquário traz novidades, pessoas diferentes e vontade de fazer as coisas à sua maneira. Os amigos e os projectos em grupo ganham peso. Abra espaço para o inesperado: pode trazer o que procurava.",
    "Você vive um ano sensível e inspirado. O Ascendente em Peixes abre a intuição, a espiritualidade e a compaixão. É um ciclo para sonhar, criar e confiar no que sente, mas também para pôr limites claros e não carregar o peso dos outros. Os sinais vão falar consigo: preste atenção.",
  ];

  const CASA = [
    "Casa 1: este é um ano sobre você. O Sol no início do mapa põe a sua identidade, a sua imagem e as suas escolhas no centro de tudo. É tempo de se reinventar, de cuidar de si e de decidir que pessoa quer ser daqui para a frente.",
    "Casa 2: este é um ano sobre o seu valor e os seus recursos. O dinheiro, os bens e a segurança material pedem atenção. É um bom ciclo para organizar as finanças, ganhar com o seu talento e perceber, também, quanto você vale.",
    "Casa 3: este é um ano de aprender e de comunicar. Estudos, cursos, escrita, conversas importantes, irmãos e vizinhos ganham destaque. As palavras abrem caminhos: diga o que precisa de ser dito.",
    "Casa 4: este é um ano sobre a casa e a família. Mudanças de casa, obras, assuntos de família ou um regresso às raízes estão em foco. É tempo de cuidar da sua base para depois poder ir mais longe.",
    "Casa 5: este é um ano de prazer, de amor e de criatividade. Romance, filhos, passatempos e projectos pessoais trazem alegria. Permita-se brincar, criar e apaixonar-se: o seu coração quer espaço.",
    "Casa 6: este é um ano de rotina, trabalho e saúde. O dia a dia pede organização, hábitos melhores e atenção ao corpo. Pequenas mudanças diárias fazem uma grande diferença ao fim de doze meses.",
    "Casa 7: este é um ano sobre os outros. Casamento, namoro sério, sociedades e acordos estão no centro. Uma relação pode começar, aprofundar-se ou ser revista. Você cresce através de quem tem ao lado.",
    "Casa 8: este é um ano de transformação profunda. Partilhas, heranças, dívidas, intimidade e tudo o que é escondido vêm à luz. É tempo de largar o que já não serve e de renascer por dentro.",
    "Casa 9: este é um ano de expansão. Viagens longas, estudos superiores, assuntos com o estrangeiro e a procura de sentido abrem os seus horizontes. Acredite mais no seu caminho.",
    "Casa 10: este é um ano de carreira e de reconhecimento. O trabalho, a reputação e os objectivos de vida ficam em destaque. É um ciclo para subir um degrau, assumir mais responsabilidade e ser visto(a) pelo que faz.",
    "Casa 11: este é um ano de amigos e de projectos. Grupos, redes, novas amizades e sonhos para o futuro ganham força. Quem está à sua volta pode abrir portas: partilhe os seus planos.",
    "Casa 12: este é um ano de recolhimento e de fecho de ciclo. É tempo de descansar, meditar, perdoar e preparar o terreno para o que vem. O trabalho é interior, e os frutos chegam no ano seguinte.",
  ];

  const LUA = [
    "Com a Lua do ano em Áries, as suas emoções andam rápidas e directas. Vai sentir necessidade de agir, de ter autonomia e de não ficar parado(a) à espera. Cuide da impaciência: nem tudo se resolve no primeiro impulso.",
    "Com a Lua do ano em Touro, o seu coração pede calma e segurança. Vai procurar conforto, rotina e pessoas de confiança. É uma Lua que acalma e estabiliza, desde que não se agarre ao que precisa de mudar.",
    "Com a Lua do ano em Gêmeos, as emoções passam pela cabeça e pela palavra. Vai precisar de conversar, de trocar ideias e de variedade. Escrever o que sente pode ajudá-lo(a) a perceber-se melhor.",
    "Com a Lua do ano em Câncer, a sensibilidade está em casa. A família, o lar e as memórias tocam-no(a) mais do que o costume. Precisa de colo e de dar colo. Proteja o seu espaço emocional.",
    "Com a Lua do ano em Leão, o seu coração quer ser visto e reconhecido. Vai precisar de carinho, de expressão e de momentos de alegria. Dê-se o direito de ser o centro da sua própria vida.",
    "Com a Lua do ano em Virgem, as emoções pedem ordem. Sente-se melhor quando a rotina funciona e quando é útil a alguém. Cuidado com a preocupação em excesso: nem tudo precisa de ser perfeito.",
    "Com a Lua do ano em Libra, o seu bem-estar depende da harmonia à sua volta. As relações e a beleza fazem-lhe bem; os conflitos pesam-lhe mais. Procure o equilíbrio sem esquecer o que você sente.",
    "Com a Lua do ano em Escorpião, as emoções são profundas e intensas. Vai sentir tudo com mais força: o amor, o ciúme, a intuição. É uma Lua de cura, se tiver coragem de olhar para dentro.",
    "Com a Lua do ano em Sagitário, o coração pede liberdade e horizonte. Vai precisar de aventura, de aprender e de acreditar em algo maior. O optimismo será o seu melhor remédio.",
    "Com a Lua do ano em Capricórnio, as emoções ficam mais contidas e responsáveis. Vai sentir necessidade de controlo e de segurança a longo prazo. Lembre-se de que também tem direito a descansar e a pedir ajuda.",
    "Com a Lua do ano em Aquário, o seu coração pede espaço e independência. Os amigos serão um apoio importante. Pode sentir-se diferente ou à frente do seu tempo: aceite essa parte de si.",
    "Com a Lua do ano em Peixes, a sensibilidade e a intuição estão no máximo. Vai sentir o que os outros sentem, sonhar mais e precisar de momentos de silêncio. Proteja-se do cansaço emocional e confie no que sente.",
  ];

  raiz.TextosRS = { ASC, CASA, LUA };
})(typeof window !== "undefined" ? window : globalThis);
