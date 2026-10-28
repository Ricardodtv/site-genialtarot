/* Oráculo das Cores — textos — Genial Tarot (28/10/2026)
   ╔══════════════════════════════════════════════════════════════════╗
   ║  EXPERIÊNCIA — textos por aprovar pelo Mestre Alberto.           ║
   ╚══════════════════════════════════════════════════════════════════╝
   Ideia: o «Oráculo das Cores» do astro.com (teste de cores de Johannes Schneider) — a MECÂNICA (25 cores,
   6 preferidas e 6 rejeitadas, escolhidas alternadamente). Os textos são TODOS originais, escritos para o
   Genial Tarot com a simbologia tradicional das cores; não se copiou nada dos textos do astro.com.
   Tom: caloroso, por «você», sem previsões, sem preços. Famílias: q quentes · a claras · v verdes · z profundas · n neutra. */
(function (raiz) {
  const OURO = "linear-gradient(135deg,#fff3b0,#e2b33c 45%,#a7741a 70%,#f6d778)";
  const PRATA = "linear-gradient(135deg,#ffffff,#c9ced6 45%,#8a919b 70%,#eef1f5)";

  const CORES = [
    // ── quentes
    { nome: "Carmim", hex: "#B0105A", fam: "q",
      agrada: { tema: "Paixão pela vida", texto: "Procura intensidade: sentir de verdade, viver com o coração aberto e dar cor aos dias. Há em si um desejo de entrega e de prazer que não quer ser adiado.", pergunta: "Onde é que a sua paixão está a ser vivida — e onde está apenas a ser imaginada?" },
      incomoda: { tema: "Cansaço das emoções fortes", texto: "Neste momento as emoções intensas pesam-lhe. Prefere calma a drama, e afasta-se de quem exige demasiado do seu coração." } },
    { nome: "Vermelho", hex: "#CC1A1A", fam: "q",
      agrada: { tema: "Força para agir", texto: "Tem energia para avançar e vontade de conquistar. Quer resultados, quer movimento, e não gosta de ficar à espera que as coisas aconteçam sozinhas.", pergunta: "Essa força está a abrir caminho — ou a empurrar quem está à sua volta?" },
      incomoda: { tema: "Pressão a mais", texto: "Sente que lhe pedem demasiado e demasiado depressa. A competição e a pressa cansam-no(a); o que precisa agora é de recuperar fôlego." } },
    { nome: "Laranja", hex: "#FF6A10", fam: "q",
      agrada: { tema: "Alegria de partilhar", texto: "Procura gente, conversa, movimento e boa disposição. Há em si vontade de celebrar, de criar e de sair da rotina para respirar ar novo.", pergunta: "Com quem gostaria de partilhar mais a sua alegria nestes dias?" },
      incomoda: { tema: "Necessidade de recolhimento", texto: "O barulho e a agitação social incomodam-no(a). Não é tristeza: é o seu lado mais íntimo a pedir silêncio e tempo para si." } },
    { nome: "Telha", hex: "#7A2E0A", fam: "q",
      agrada: { tema: "Raízes e segurança", texto: "Valoriza o que é sólido e conhecido: a casa, a família, os hábitos que o(a) protegem. Quer sentir o chão firme debaixo dos pés antes de dar o próximo passo.", pergunta: "O que é que, na sua vida, lhe dá verdadeiramente sensação de lar?" },
      incomoda: { tema: "Peso do passado", texto: "Há obrigações antigas e rotinas que já não fazem sentido e que o(a) prendem. Algo em si quer libertar-se do que é só hábito." } },
    { nome: "Dourado", hex: "#E2B33C", fundo: OURO, fam: "q",
      agrada: { tema: "Brilho e reconhecimento", texto: "Quer ser visto(a) pelo que vale e sente que merece abundância. É um momento de confiança no seu próprio valor e de vontade de brilhar.", pergunta: "Já reconheceu a si próprio(a) aquilo que espera que os outros reconheçam?" },
      incomoda: { tema: "Desconfiança das aparências", texto: "O luxo, a vaidade e as promessas brilhantes não o(a) convencem agora. Procura o que é autêntico, mesmo que seja simples." } },
    { nome: "Rosa", hex: "#FFC9D3", fam: "q",
      agrada: { tema: "Ternura e cuidado", texto: "O seu coração pede carinho, delicadeza e afeto sem condições. Quer cuidar e ser cuidado(a), e sente que a gentileza é a sua maior força.", pergunta: "Está a dar a si próprio(a) a mesma ternura que dá aos outros?" },
      incomoda: { tema: "Recusa de ser frágil", texto: "Neste momento não quer mostrar-se vulnerável. Prefere a firmeza à doçura, talvez porque já se sentiu desprotegido(a)." } },
    // ── claras
    { nome: "Âmbar", hex: "#FFC20A", fam: "a",
      agrada: { tema: "Otimismo luminoso", texto: "Há uma luz em si que quer crescer: confiança no futuro, vontade de projetos novos e de dias mais leves. A esperança está a guiá-lo(a).", pergunta: "Qual é o pequeno passo que pode dar hoje na direção dessa luz?" },
      incomoda: { tema: "Esperança cansada", texto: "Tem desconfiado das boas notícias e das promessas fáceis. Depois de algumas desilusões, prefere ver para crer." } },
    { nome: "Amarelo", hex: "#FFEA10", fam: "a",
      agrada: { tema: "Mente aberta e liberdade", texto: "Quer novidade, aprender, mudar de ares. A sua mente está desperta e curiosa, e sente que o mundo tem muito mais para lhe mostrar.", pergunta: "O que é que gostaria de aprender ou experimentar pela primeira vez?" },
      incomoda: { tema: "Cautela com a mudança", texto: "As mudanças repentinas inquietam-no(a). Precisa de estabilidade antes de abrir portas novas, e isso é sabedoria, não medo." } },
    { nome: "Verde-lima", hex: "#A8CF1E", fam: "a",
      agrada: { tema: "Renovação", texto: "Sente o impulso de começar de novo: um hábito, um projeto, uma forma diferente de olhar para si. É energia de primavera, fresca e cheia de vontade.", pergunta: "O que é que já está pronto para nascer na sua vida?" },
      incomoda: { tema: "Impaciência com começos", texto: "Recomeçar outra vez cansa-o(a). Prefere aprofundar o que já tem a abrir mais frentes novas." } },
    { nome: "Ocre", hex: "#B57826", fam: "a",
      agrada: { tema: "Sabedoria prática", texto: "Confia na experiência e no bom senso. Quer soluções concretas, feitas à mão e com paciência, e valoriza tudo o que é útil e verdadeiro.", pergunta: "Que conselho daria a si próprio(a) com base em tudo o que já viveu?" },
      incomoda: { tema: "Cansaço do dever", texto: "O peso das responsabilidades práticas está a tirar-lhe leveza. Algo em si pede um pouco de sonho no meio de tanta obrigação." } },
    { nome: "Branco", hex: "#F7F7F5", fam: "a",
      agrada: { tema: "Clareza e recomeço", texto: "Procura limpeza interior: arrumar a mente, simplificar, ver tudo com transparência. É o desejo de uma página em branco para escrever de novo.", pergunta: "O que é que precisa de deixar ir para ficar mais leve?" },
      incomoda: { tema: "Recusa do vazio", texto: "A perfeição e a frieza incomodam-no(a). Prefere a vida com as suas cores e imperfeições a uma calma demasiado distante." } },
    { nome: "Creme", hex: "#FCFBC4", fam: "a",
      agrada: { tema: "Conforto sereno", texto: "Quer suavidade: um dia tranquilo, um abraço, uma casa acolhedora. Está a aprender que descansar também é uma forma de cuidar de si.", pergunta: "Quando foi a última vez que se deu um dia só para si?" },
      incomoda: { tema: "Medo da acomodação", texto: "O conforto demasiado parado inquieta-o(a). Sente que, se ficar muito tempo no mesmo sítio, deixa de crescer." } },
    // ── verdes
    { nome: "Verde-folha", hex: "#2F7A14", fam: "v",
      agrada: { tema: "Crescimento firme", texto: "Quer evoluir passo a passo, com raízes fortes. Tem paciência para construir e confiança de que o que planta com cuidado vai dar fruto.", pergunta: "O que está a cultivar neste momento que precisa de mais paciência sua?" },
      incomoda: { tema: "Cansaço de esperar", texto: "Os processos lentos deixam-no(a) inquieto(a). Gostaria de ver resultados já, e custa-lhe aceitar o tempo natural das coisas." } },
    { nome: "Verde-floresta", hex: "#0B5C28", fam: "v",
      agrada: { tema: "Autonomia e firmeza", texto: "Quer decidir por si e manter a sua posição. Não aceita bem que lhe digam o que fazer, e sente que a sua independência é um tesouro a proteger.", pergunta: "A sua firmeza está a protegê-lo(a) — ou a afastá-lo(a) de quem o(a) quer ajudar?" },
      incomoda: { tema: "Rigidez à sua volta", texto: "A teimosia e as regras sem sentido irritam-no(a). Precisa de mais flexibilidade, nas outras pessoas e talvez também em si." } },
    { nome: "Turquesa", hex: "#00828F", fam: "v",
      agrada: { tema: "Proteção e clareza", texto: "Está atento(a) e protege o seu espaço com calma. Escolhe bem com quem partilha a sua energia e procura relações limpas e sinceras.", pergunta: "Há alguém de quem precisa de pôr um limite com mais clareza?" },
      incomoda: { tema: "Desconfiança da distância", texto: "A frieza e o distanciamento dos outros magoam-no(a). Quer proximidade verdadeira e não apenas boas maneiras." } },
    { nome: "Oliva", hex: "#686600", fam: "v",
      agrada: { tema: "Paz com o que é", texto: "Aceita a vida como ela vem, com maturidade. Não precisa de provar nada a ninguém: procura apenas viver em paz com as suas escolhas.", pergunta: "O que é que já fez as pazes consigo — e o que ainda espera por isso?" },
      incomoda: { tema: "Recusa da resignação", texto: "Não aceita conformar-se. Sente que merece mais do que o «é assim mesmo», e isso dá-lhe vontade de mudar." } },
    { nome: "Prateado", hex: "#B9BFC8", fundo: PRATA, fam: "v",
      agrada: { tema: "Intuição desperta", texto: "A sua intuição está afinada: sente as coisas antes de as ver. Há uma ligação forte com a Lua, com os sonhos e com o lado invisível da vida.", pergunta: "Que sinal a sua intuição lhe tem dado e que ainda não escutou?" },
      incomoda: { tema: "Desconfiança do incerto", texto: "O que é vago e indefinido inquieta-o(a). Quer respostas claras e factos, e menos mistério neste momento." } },
    { nome: "Verde-água", hex: "#AEE8D5", fam: "v",
      agrada: { tema: "Cura e frescura", texto: "Procura curar-se de algo: um cansaço, uma mágoa, um período difícil. Precisa de ar livre, de água, de natureza e de leveza para se renovar.", pergunta: "O que é que o(a) ajuda verdadeiramente a sentir-se renovado(a)?" },
      incomoda: { tema: "Impaciência com a fragilidade", texto: "Não tem paciência para tratar das feridas devagar. Quer seguir em frente, mesmo que ainda não esteja totalmente recuperado(a)." } },
    // ── profundas
    { nome: "Azul-real", hex: "#0A2E9C", fam: "z",
      agrada: { tema: "Lealdade e confiança", texto: "Valoriza a palavra dada e as relações que duram. Quer à sua volta pessoas em quem possa confiar de olhos fechados, e oferece o mesmo em troca.", pergunta: "Em quem confia de verdade — e já lhe disse isso?" },
      incomoda: { tema: "Desilusão com promessas", texto: "Sente que alguém não cumpriu o que prometeu. A confiança está ferida e precisa de tempo para voltar." } },
    { nome: "Azul-noite", hex: "#04066A", fam: "z",
      agrada: { tema: "Calma profunda", texto: "Precisa de silêncio, de descanso e de tempo para estar consigo. É no sossego que encontra as suas respostas e recupera a energia.", pergunta: "O que é que a sua alma lhe diz quando, finalmente, faz silêncio?" },
      incomoda: { tema: "Inquietação interior", texto: "Neste momento custa-lhe parar. A quietude traz à superfície pensamentos que preferia não ouvir." } },
    { nome: "Violeta", hex: "#561062", fam: "z",
      agrada: { tema: "Magia e espiritualidade", texto: "Sente-se atraído(a) pelo mistério, pelo sagrado e pelo que não se explica. Há em si uma busca de sentido que vai além do dia a dia.", pergunta: "Que prática espiritual o(a) faz sentir mais ligado(a) a si?" },
      incomoda: { tema: "Os pés na terra", texto: "O que é demasiado místico ou fantasioso afasta-o(a) neste momento. Quer coisas reais, palpáveis, que se possam comprovar." } },
    { nome: "Castanho", hex: "#4D2A18", fam: "z",
      agrada: { tema: "Necessidade de abrigo", texto: "Quer sentir-se seguro(a), aconchegado(a) e protegido(a). O corpo pede descanso, boa comida e um lugar onde possa simplesmente ser.", pergunta: "O que é que o seu corpo lhe está a pedir e ainda não lhe deu?" },
      incomoda: { tema: "Recusa do que é pesado", texto: "O que é pesado, lento ou demasiado material está a cansá-lo(a). Procura leveza e um pouco mais de alegria." } },
    { nome: "Preto", hex: "#0A0A0A", fam: "z",
      agrada: { tema: "Proteção e limites", texto: "Neste momento precisa de se proteger e de dizer «não». Fecha-se para guardar a sua energia, e isso pode ser exatamente o que precisa.", pergunta: "Do que é que se está a proteger — e até quando vai precisar dessa proteção?" },
      incomoda: { tema: "Vontade de luz", texto: "Recusa a tristeza e o fechamento. Quer sair de um período escuro e abrir as janelas da sua vida." } },
    { nome: "Azul-céu", hex: "#C6DAFF", fam: "z",
      agrada: { tema: "Leveza e sonho", texto: "Quer respirar, sonhar e sentir-se livre de preocupações. A sua imaginação está viva e procura horizontes largos e tranquilos.", pergunta: "Que sonho tem guardado e merece voltar a ver a luz?" },
      incomoda: { tema: "Desconfiança da ingenuidade", texto: "Os sonhos demasiado distantes da realidade não o(a) convencem agora. Prefere o que pode ver e tocar." } },
    // ── neutra
    { nome: "Cinzento", hex: "#6B6B6B", fam: "n",
      agrada: { tema: "Distância que protege", texto: "Precisa de se manter um pouco à parte, observar sem se envolver e não tomar partido. É uma pausa para perceber o que realmente sente.", pergunta: "De que é que se está a manter à distância — e porquê?" },
      incomoda: { tema: "Vontade de se envolver", texto: "Não quer ficar em cima do muro. Quer participar, decidir e viver as coisas por inteiro, sem meias-tintas." } },
  ];

  // a energia geral: a família que mais o(a) atrai + a família que mais o(a) incomoda (pesadas pela ordem)
  const FAMILIA = {
    q: { atrai: "Neste momento, o que o(a) move é a vontade de agir, de sentir com intensidade e de ser visto(a).",
         afasta: "Ao mesmo tempo, a pressão e o excesso de emoções cansam-no(a): precisa de doseá-las.",
         mesma: "É uma energia forte e contraditória: deseja e teme a intensidade ao mesmo tempo." },
    a: { atrai: "Neste momento, o que o(a) move é a abertura: luz, novidade, clareza e esperança no que vem.",
         afasta: "Ao mesmo tempo, desconfia das promessas fáceis e da mudança feita à pressa.",
         mesma: "Há em si uma oscilação entre querer abrir-se ao novo e ter receio de se desiludir." },
    v: { atrai: "Neste momento, o que o(a) move é a necessidade de firmeza, de autonomia e de crescer com raízes.",
         afasta: "Ao mesmo tempo, a rigidez e a espera custam-lhe: quer estabilidade sem ficar preso(a).",
         mesma: "Procura segurança e, ao mesmo tempo, sente-se apertado(a) por ela: é altura de afinar o equilíbrio." },
    z: { atrai: "Neste momento, o que o(a) move é a procura de calma, de profundidade e de sentido.",
         afasta: "Ao mesmo tempo, fugir para dentro de si nem sempre o(a) descansa: precisa de alguma luz e companhia.",
         mesma: "Atrai-o(a) a profundidade mas também a teme: há algo cá dentro à espera de ser olhado com carinho." },
    n: { atrai: "Neste momento, prefere observar à distância antes de decidir.",
         afasta: "Ao mesmo tempo, quer envolver-se e tomar posição, sem meias-tintas.",
         mesma: "Está entre o observar e o agir, à espera do momento certo." },
  };

  // a frase que liga cada posição (1.ª a 6.ª) — preferidas e rejeitadas
  const LIGA_MAIS = ["O que mais o(a) move agora…", "O que procura de forma consciente…", "Aquilo de que mais precisa…",
                     "Como quer viver este momento…", "O que lhe dá força…", "Para onde está a caminhar…"];
  const LIGA_MENOS = ["O que mais o(a) inquieta…", "O que está a pôr de lado…", "O que lhe pesa…",
                      "O que prefere evitar…", "O que já não quer…", "O que pode transformar…"];

  raiz.OraculoCores = { CORES, FAMILIA, LIGA_MAIS, LIGA_MENOS };
})(typeof window !== "undefined" ? window : globalThis);
