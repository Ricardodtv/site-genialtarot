/* ============================================================
   LOJA MÍSTICA — OS SEUS PRODUTOS (ficheiro que o Alberto edita)
   ============================================================
   COMO ADICIONAR UM PRODUTO:
   1. Copie um bloco inteiro, do { até ao }, incluindo a vírgula final
   2. Cole-o por baixo do último bloco da categoria certa
   3. Mude os textos entre aspas
   4. Guarde/faça Commit — a loja monta-se sozinha

   O QUE É CADA CAMPO:
   nome      → o nome do produto ou serviço
   categoria → "Consultas", "Rituais", "Emergências", "Amuletos",
               "Mapas Astrais", "Cursos"... (novas criam secção sozinhas)
   preco     → ex.: "45 €" (deixe "" para não mostrar preço)
   foto      → nome do ficheiro da foto subida ao GitHub, ou https://...
               Deixe "" para aparecer um símbolo místico no lugar.
   descricao → 1 a 3 frases apelativas sobre o produto
   link      → para onde vai o botão 🛒 Comprar Aqui (link de pagamento).
               Deixe "" para abrir o WhatsApp com mensagem pronta.
   destaque  → true mostra o selo verde ✦ POPULAR ✦ e põe o produto
               em primeiro lugar na sua secção (opcional)
   etiqueta  → texto para um selo próprio no estilo do POPULAR
               (ex.: "MAPA ASTRAL", "SUPER PROMOÇÃO") — opcional
   cor       → a cor da etiqueta: "verde", "violeta", "vermelho",
               "azul", "laranja", "rosa" ou "dourado"
               (se não escrever nada, fica violeta)
   estrelas  → número de ⭐ por cima da etiqueta, de 1 a 5 (opcional)
   topvendas → true mostra o selo DOURADO "✦ Top Vendas ✦" com
               ⭐⭐⭐ por cima (opcional; também põe o produto à frente)
   ============================================================ */

const PRODUTOS = [

  /* ================= CONSULTAS ================= */

  {
    nome: "🔮 1 Pergunta de Tarot por Escrito – Feita pelo Mestre Alberto 📜",
    categoria: "Consultas",
    preco: "25 €",
    foto: "pergunta-escrita.jpg",
    descricao: "Faça a sua pergunta e receba a resposta do Mestre Alberto por escrito, tirada nas cartas com dedicação exclusiva ao seu caso. Clara, direta e guardada para reler sempre que precisar. Sem marcações, sem esperas — a orientação chega até si.",
    link: "https://mypos.com/vmp/btn/BKXR2JQ2BEB19",
    destaque: true,
  },

  {
    nome: "🔮 Consulta de Tarot Online – 30 Minutos com Mestre Alberto ⏰",
    categoria: "Consultas",
    preco: "65 €",
    foto: "consulta-30min.jpg",
    descricao: "Meia hora a sós com as cartas e com o Mestre. Ideal para uma ou duas questões objetivas — amor, trabalho, decisões — com resposta clara e orientação prática, por chamada ou vídeo, no conforto da sua casa.",
    link: "https://mypos.com/vmp/btn/BTSGROA5LPZ61",
    topvendas: true,
  },

  {
    nome: "🔮 Consulta de Tarot Online – Todos os Temas (1 Hora com Mestre Alberto) ⏰",
    categoria: "Consultas",
    preco: "85 €",
    foto: "consulta-1hora.jpg",
    descricao: "Uma hora completa para abrir o jogo da sua vida: amor, carreira, família, dinheiro, caminhos. Tempo para aprofundar cada tema, fazer todas as perguntas e sair com um rumo definido.",
    link: "https://mypos.com/vmp/btn/B35PHJ9OQMU04",
    etiqueta: "A MAIS COMPLETA", cor: "vermelho", estrelas: 5,
  },

  {
    nome: "🔮 Previsão Anual para 12 Meses – Feita pelo Mestre Alberto (Escrita) 📅",
    categoria: "Consultas",
    preco: "185 €",
    foto: "previsao-anual.jpg",
    descricao: "Os seus próximos 12 meses, mês a mês, escritos pelo Mestre Alberto: amor, dinheiro, saúde e os caminhos a abraçar ou evitar. Um documento para guardar e consultar durante todo o ano.",
    link: "https://mypos.com/vmp/btn/B5IA82S63VN50",
    etiqueta: "SEU FUTURO", cor: "azul", estrelas: 3,
  },

  {
    nome: "💑 Consulta de Terapia de Casais Online – 1 Hora com Mestre Alberto ⏰",
    categoria: "Consultas",
    preco: "185 €",
    foto: "terapia-casais.jpg",
    descricao: "Uma hora dedicada aos dois. As cartas revelam o que une, o que desgasta e o que pode renascer na relação — com orientação franca e caminhos concretos para reencontrarem o equilíbrio.",
    link: "https://mypos.com/vmp/btn/B1CMBQSYWEW69",
    etiqueta: "VOLTE A AMAR", cor: "rosa", estrelas: 3,
  },

  {
    nome: "🔮 Parecer sobre Qualquer Assunto pelas Cartas – Escrito pelo Mestre Alberto 📜",
    categoria: "Consultas",
    preco: "125 €",
    foto: "parecer-cartas.jpg",
    descricao: "Vai tomar uma decisão importante — um negócio, uma mudança, uma proposta? O Mestre Alberto consulta as cartas sobre o seu assunto e envia-lhe um parecer escrito, claro e fundamentado, para decidir com segurança.",
    link: "https://mypos.com/vmp/btn/BLQ1NIUDJ2K11",
  },

  {
    nome: "✋ Leitura da Sua Mão por Quiromancia Online – Pelo Mestre Alberto 🔮",
    categoria: "Consultas",
    preco: "80 €",
    foto: "quiromancia.jpg",
    descricao: "As linhas da sua mão contam a sua história. Envie as fotografias das suas mãos e receba a leitura do Mestre Alberto: linha da vida, do coração e do destino — o que está escrito em si.",
    link: "https://mypos.com/vmp/btn/BG2QB2ADANJ52",
  },

  /* ================= RITUAIS ================= */

  {
    nome: "💰 Ritual de Prosperidade Financeira – Pelo Mestre Alberto ✨",
    categoria: "Rituais",
    preco: "895 €",
    foto: "prosperidade-financeira.jpg",
    descricao: "O grande ritual da abundância pessoal: um trabalho completo para desbloquear a sua vida financeira e atrair dinheiro e oportunidades, realizado com Buda dourado, velas e oferendas. Inclui registo do processo.",
    link: "https://mypos.com/vmp/btn/BGBNMQV89HH04",
    destaque: true,
  },

  {
    nome: "🛡️ Ritual de Proteção e Limpeza – Pelo Mestre Alberto ✨",
    categoria: "Rituais",
    preco: "795 €",
    foto: "protecao-limpeza.jpg",
    descricao: "Limpeza espiritual profunda seguida de selamento de proteção: remove energias pesadas, inveja e mau-olhado, e ergue um escudo à sua volta. O passo essencial antes de qualquer novo começo.",
    link: "https://mypos.com/vmp/btn/BOIQ5HO2K6G26",
    destaque: true,
  },

  {
    nome: "🕯️ Vela Guia, Oração e Proteção – Com o Mestre Alberto 🙏",
    categoria: "Rituais",
    preco: "95 €",
    foto: "vela-guia.jpg",
    descricao: "Durante 5 dias, o Mestre Alberto acende uma vela consagrada e reza uma oração dedicada ao seu nome e à sua intenção — proteção, saúde ou gratidão. Receberá o registo do ritual realizado.",
    link: "https://mypos.com/vmp/btn/BL5R83HROAB31",
  },

  {
    nome: "🌕 Ritual de Lua Cheia para Atrair Dinheiro – Feito pelo Mestre Alberto 💰",
    categoria: "Rituais",
    preco: "225 €",
    foto: "ritual-lua-cheia.jpg",
    descricao: "Realizado na noite exata de Lua Cheia — o momento mais poderoso para a abundância: moedas, sal e velas trabalham a favor da sua prosperidade. Inclui relatório com fotografias do ritual.",
    link: "https://mypos.com/vmp/btn/BVSDFYHECEI85",
  },

  {
    nome: "🕯️ Incenso + Oração para Destino e Proteção – Pelo Mestre Alberto 🙏",
    categoria: "Rituais",
    preco: "125 €",
    foto: "incenso-oracao.jpg",
    descricao: "Incensos consagrados e a Oração do Destino, queimados em seu nome para limpar bloqueios e proteger o seu caminho. Um trabalho silencioso que abre espaço ao que está destinado a chegar.",
    link: "https://mypos.com/vmp/btn/BX27E8EEOBJ38",
  },

  {
    nome: "🚪 Ritual de Abertura de Caminhos – Pelo Mestre Alberto ✨",
    categoria: "Rituais",
    preco: "560 €",
    foto: "abertura-caminhos.jpg",
    descricao: "Quando tudo parece travado — trabalho, amor, dinheiro — este ritual profundo, apoiado na tradição de São Cipriano, destranca as portas e devolve o movimento à sua vida. Trabalho completo com registo do processo.",
    link: "https://mypos.com/vmp/btn/BJVR1FZMNW472",
  },

  {
    nome: "💖 Ritual de Atração Forte para o Amor – Pelo Mestre Alberto ❤️",
    categoria: "Rituais",
    preco: "995 €",
    foto: "atracao-amor.jpg",
    descricao: "O trabalho mais poderoso do Mestre Alberto para o amor: um ritual intenso de atração, feito com dedicação absoluta ao seu caso, para aproximar quem está destinado a si. Acompanhamento pessoal durante todo o processo.",
    link: "https://mypos.com/vmp/btn/B54ARU9RI3645",
  },

  {
    nome: "💼 Ritual de Prosperidade para Empresas e Negócios 💰",
    categoria: "Rituais",
    preco: "995 €",
    foto: "ritual-prosperidade.jpg",
    descricao: "Para empresários e negócios: um trabalho energético dedicado à sua empresa, para atrair clientes, destravar vendas e sustentar o crescimento. Energia, discrição e acompanhamento do Mestre.",
    link: "https://mypos.com/vmp/btn/BRUEKAEBD7X05",
  },

  /* ================= EMERGÊNCIAS ================= */

  {
    nome: "🚨 Consulta de Emergência com Mestre Alberto (Resposta em Máx. 1h) ⏰ – Duração: 40 Minutos",
    categoria: "Emergências",
    preco: "110 €",
    foto: "consulta-emergencia.jpg",
    descricao: "Para quando a alma não pode esperar: resposta garantida no máximo numa hora. 40 minutos inteiramente dedicados ao seu caso urgente, com prioridade absoluta na agenda do Mestre.",
    link: "https://mypos.com/vmp/btn/BKXKXFVMT7M49",
    etiqueta: "CONSULTA DE EMERGÊNCIA", cor: "vermelho", estrelas: 5,
  },

  /* ================= AMULETOS ================= */

  {
    nome: "✨ Amuleto Cruz da Boa Energia e Sucesso – Envio para Todo o Mundo, Feito pelo Mestre Alberto 🌍",
    categoria: "Amuletos",
    preco: "145 €",
    foto: "amuleto-cruz.jpg",
    descricao: "Uma cruz consagrada pelo Mestre Alberto para atrair boa energia e sucesso, preparada individualmente para quem a vai usar. Envio registado para qualquer parte do mundo.",
    link: "https://mypos.com/vmp/btn/B5588K5PTFM42",
  },

  {
    nome: "⭐ Amuleto Pentagrama de Equilíbrio com Ritual – Envio para Todo o Mundo, Pelo Mestre Alberto 🌍",
    categoria: "Amuletos",
    preco: "165 €",
    foto: "amuleto-pentagrama.jpg",
    descricao: "O símbolo do equilíbrio entre os quatro elementos e o espírito, consagrado em ritual dedicado a si. Proteção e harmonia para trazer ao peito ou guardar em casa. Envio para todo o mundo.",
    link: "https://mypos.com/vmp/btn/B2PA7QQ3QA346",
  },

  /* ================= MAPAS ASTRAIS ================= */

  {
    nome: "✨ Mapa Astral Conheça Sua Personalidade – Feito pelo Mestre Alberto 🌟",
    categoria: "Mapas Astrais",
    preco: "195 €",
    foto: "mapa-astral.jpg",
    descricao: "O retrato mais profundo de si: o seu mapa astral completo, interpretado pelo Mestre Alberto — talentos, desafios, missão de vida e o que os astros desenharam para si desde o nascimento. Entregue por escrito, para guardar para sempre.",
    link: "https://mypos.com/vmp/btn/BF6O2I7O68M52",
    etiqueta: "MAPA ASTRAL",
  },

  {
    nome: "🔮 Análise ao Seu Signo e Personalidade – Escrita pelo Mestre Alberto ✨",
    categoria: "Mapas Astrais",
    preco: "145 €",
    foto: "analise-signo.jpg",
    descricao: "Muito além do horóscopo: uma análise escrita e personalizada do seu signo e personalidade — forças, sombras e a forma única como o céu se expressa em si.",
    link: "https://mypos.com/vmp/btn/BWEHSTP6TUV40",
  },

  /* ================= CURSOS (no final) ================= */

  {
    nome: "📚 Curso de Tarot Online 3 Meses com Mestre Alberto – Aprenda a Ler Cartas e Ganhar Confiança",
    categoria: "Cursos",
    preco: "2450 €",
    foto: "curso-tarot.jpg",
    descricao: "Três meses de formação direta com o Mestre Alberto para aprender a ler as cartas do zero: arcanos, métodos de tiragem, prática acompanhada e a confiança para fazer as suas próprias leituras. Vagas limitadas.",
    link: "https://mypos.com/vmp/btn/B8Q8NUM8CSD06",
  },

];
