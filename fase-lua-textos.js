/* Textos de «Em que fase da Lua você nasceu» — Genial Tarot (28/10/2026)
   EXPERIÊNCIA 28/10/2026 — textos por aprovar pelo Mestre Alberto.
   Uma fase por texto, pela ordem do AstroNasc.FASES8 (nascimento-calc.js): da Nova à Minguante (Balsâmica).
   A leitura das 8 fases segue a tradição da astrologia lunar (o ciclo como semente, crescimento,
   plenitude e entrega). Escritos de raiz, por «você», sem promessas. */
(function (raiz) {
  // [nome, nome da tradição (ou ""), emoji, a frase curta, o texto]
  const FASES = [
    ["Lua Nova", "", "🌑", "a semente",
     "Você nasceu com a Lua escondida, no começo de um ciclo novo. É a fase das sementes: quem nasce nela costuma agir por instinto, abrir caminhos e sentir que a vida está sempre a recomeçar. Às vezes nem sabe explicar porque escolhe o que escolhe, mas sente que tem de ir. O seu desafio é dar tempo às coisas para crescerem, sem desistir delas antes de mostrarem o que valem."],
    ["Lua Crescente", "", "🌒", "o impulso",
     "Você nasceu quando a primeira luz da Lua aparecia no céu. É a fase do impulso: a semente rompe a terra e tem de lutar por espaço. Quem nasce nela tem garra para sair do lugar de onde veio e construir algo seu, mesmo contra o peso do passado. O seu caminho é confiar no que é novo em você, sem se deixar travar pelo medo de falhar."],
    ["Quarto Crescente", "", "🌓", "a decisão",
     "Você nasceu com meia Lua acesa e o ciclo em plena ação. É a fase das decisões e dos obstáculos que se vencem a fazer. Quem nasce nela tem força para construir, organizar e enfrentar crises, e cresce precisamente quando há um problema para resolver. O seu desafio é escolher bem as batalhas, para que a energia vá para o que importa."],
    ["Lua Gibosa Crescente", "", "🌔", "o aperfeiçoamento",
     "Você nasceu com a Lua quase cheia, a ganhar os últimos raios de luz. É a fase de quem aperfeiçoa: analisa, pergunta, afina os pormenores e quer perceber o sentido das coisas. Quem nasce nela tem um enorme sentido de propósito e gosta de se dedicar a algo maior. O seu caminho é aceitar que nem tudo precisa de estar perfeito para ser bom."],
    ["Lua Cheia", "", "🌕", "a plenitude",
     "Você nasceu com a Lua inteira a brilhar, em frente ao Sol. É a fase da plenitude e da consciência: quem nasce nela vive muito através das relações, vê com clareza o que sente e precisa de dar forma visível ao que tem por dentro. As emoções são fortes e os encontros marcam a sua vida. O seu desafio é encontrar o equilíbrio entre o que quer para si e o que vive com os outros."],
    ["Lua Gibosa Minguante", "a Disseminadora", "🌖", "a partilha",
     "Você nasceu quando a Lua cheia começava a ceder a sua luz. A tradição chama-lhe a Disseminadora: é a fase de quem partilha o que aprendeu. Quem nasce nela tem jeito para ensinar, comunicar e passar uma mensagem, e sente necessidade de dar sentido à experiência. O seu caminho é partilhar com generosidade, sem querer convencer toda a gente."],
    ["Quarto Minguante", "", "🌗", "a viragem",
     "Você nasceu com meia Lua acesa, mas já a caminho do fim do ciclo. É a fase da viragem interior: quem nasce nela questiona as regras, revê o que herdou e tem coragem de mudar de ideias quando percebe que algo já não faz sentido. Muitas vezes sente-se à frente do seu tempo. O seu desafio é viver as suas convicções com serenidade, sem guerra contra o mundo."],
    ["Lua Minguante", "a Balsâmica", "🌘", "a entrega",
     "Você nasceu com a Lua a desaparecer, no fim de um ciclo inteiro. A tradição chama-lhe a Balsâmica: é a fase do bálsamo, de quem fecha, cura e prepara o que vem depois. Quem nasce nela tem uma sensibilidade funda, um lado sábio e muitas vezes a sensação de carregar algo antigo. O seu caminho é soltar o que já não lhe pertence e confiar no futuro que está a ajudar a semear."],
  ];
  raiz.TextosFase = { FASES };
})(typeof window !== "undefined" ? window : globalThis);
