/* promos.js — 27/11/2026, regra dele: «quando se fizer alguma promoção ou alguma coisa que precise de preço que ainda não
   tenhas … cria uma página temporária … usa para pagamento sempre a etiqueta do myPOS mypos.com/@genialtarot».
   UMA página para todas as promoções: /promo?p=<id>. Cada promoção é uma entrada aqui.
   · inicio/fim: em UTC (Nov–Mar: Lisboa = UTC). Fora do prazo a página diz «terminou» e manda para a loja.
   · valor: com ponto e 2 casas — vai no endereço mypos.com/@genialtarot/<valor>. Tem de ser ÚNICO entre os preços em vigor,
     para se saber pelo valor o que foi comprado.
   · itens[].pedido: o tipo de pedido que segue para o cerebro (/notify) — o mesmo que a página do produto já manda,
     por isso cai na mesma pasta do cofre e no mesmo aviso do Home Assistant.
   · pede: "nascimento" = data + hora + cidade + país (os mapas feitos à medida precisam).
   · entra: endereços que, durante a promoção, vêm dar aqui (ex.: o botão do email). */
window.PROMOS = {
  "black-friday-3-mapas": {
    titulo: "Black Friday: 3 mapas pelo preço de 1",
    subtitulo: "Compre o Ano 2027 e receba de oferta o Mapa Astral e o Mapa do Amor",
    inicio: "2026-11-27T00:00:00Z",
    fim: "2026-11-30T23:59:59Z",                     // ele: «até domingo às 23:59»; 27/11 16h: «deixa aberta até segunda às 23:59» (o assunto do envio dizia segunda)
    valor: "25.00", preco: "25 €", antes: "50 €", poupa: "Poupa 50%",
    imagem: "/black-friday-2026.webp",
    itens: [
      { nome: "Ano 2027 — Mapa Numerológico Completo", nota: "9 capítulos + Linha do Tempo: o que o seu número pessoal lhe traz, mês a mês", preco: "25 €", pedido: "numerologia-pedido", prefixo: "NUM-" },
      { nome: "Mapa Astral completo", nota: "9 capítulos + a sua Mandala de nascimento", preco: "15 €", pedido: "mapa-astral-pedido", prefixo: "MAS-", oferta: true },
      { nome: "Mapa do Amor e da Sedução", nota: "9 capítulos sobre a forma como ama e seduz", preco: "10 €", pedido: "mapa-amor-pedido", prefixo: "MA-", oferta: true }
    ],
    pede: ["nascimento"],
    entra: ["/numerologia-2027?vip=1"]
  }
};
