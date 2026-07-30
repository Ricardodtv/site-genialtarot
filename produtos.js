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
    nome: "Ritual da Chama Dourada",
    categoria: "Rituais",
    preco: "45 €",
    foto: "ritual-exemplo.jpg",
    descricao: "Ritual de proteção e abertura de caminhos, realizado pelo Mestre Alberto com vela consagrada e oração dedicada ao seu caso. Inclui relatório final com fotografias do ritual. Ideal para momentos de bloqueio, inveja ou recomeço.",
    link: "",
    destaque: true,
  },

];
