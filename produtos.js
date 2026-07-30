/* ============================================================
   LOJA MÍSTICA — OS SEUS PRODUTOS (ficheiro que o Alberto edita)
   ============================================================
   COMO ADICIONAR UM PRODUTO:
   1. Copie um bloco inteiro, do { até ao }, incluindo a vírgula final
   2. Cole-o por baixo do último bloco
   3. Mude os textos entre aspas
   4. Guarde/faça Commit — a loja monta-se sozinha

   O QUE É CADA CAMPO:
   nome      → o nome do produto ou serviço
   categoria → "Consultas", "Rituais", "Emergências", "Amuletos"...
               (pode inventar novas — a loja cria a secção sozinha)
   preco     → ex.: "45 €" (deixe "" para não mostrar preço)
   foto      → nome do ficheiro da foto que subiu ao GitHub
               (ex.: "ritual-exemplo.jpg") ou um endereço https://...
               Deixe "" para aparecer um símbolo místico no lugar.
   descricao → 1 a 3 frases apelativas sobre o produto
   link      → para onde vai o botão ✦ Adquirir ✦ (o link de compra).
               Deixe "" para abrir o seu WhatsApp com mensagem pronta.
   destaque  → true mostra o selo ✦ POPULAR ✦ no canto (opcional)
   ============================================================ */

const PRODUTOS = [

  {
    nome: "🔮 1 Pergunta de Tarot por Escrito – Feita pelo Mestre Alberto 📜",
    categoria: "Consultas",
    preco: "25 €",
    foto: "pergunta-escrita.jpg",
    descricao: "Faça a sua pergunta e receba a resposta do Mestre Alberto por escrito, tirada nas cartas com dedicação exclusiva ao seu caso. Clara, direta e guardada para reler sempre que precisar. Sem marcações, sem esperas — a orientação chega até si.",
    link: "https://mypos.com/vmp/btn/BKXR2JQ2BEB19",
    destaque: true,
  },

];
