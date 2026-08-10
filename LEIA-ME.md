---
tags:
  - site
  - genialtarot
  - pagamentos
Created: 2026-08-10
---
[[Central Tecnologia]]

# Escapar ao navegador do WhatsApp

**O problema, descoberto a 10/08/2026:** o checkout do myPOS **não abre dentro do WhatsApp** — nem no Android nem no iPhone. Mostra *"O link de pagamento expirou ou foi desativado pelo comerciante"*.

Como o `genialtarot.com` **só tem o WhatsApp como forma de contacto**, era por aí que a conversa de venda acontecia — e era por aí que morria. O cliente carregava, via "expirou", e ia-se embora **sem avisar**.

**Não é o link. É o navegador embutido da aplicação**, que o myPOS recusa por não parecer um navegador a sério.

---

## Os dois ficheiros

### 1. `escapar-whatsapp.js` — a correcção de fundo

Apanha os cliques em qualquer botão que aponte ao myPOS. **Num navegador normal não faz nada.** Dentro do WhatsApp (ou Instagram, ou Facebook) força a abertura no navegador verdadeiro, e se não conseguir mostra um aviso com o link para copiar — em vez de deixar o cliente a bater numa parede.

**Vale para os 21 produtos de uma vez**, e também para os links que já andam partilhados por aí.

**Instalar:** juntar ao fim da página da loja, antes de `</body>`:
```html
<script src="/escapar-whatsapp.js"></script>
```

### 2. `pagar.html` — para mandar links pelo WhatsApp

Uma página com endereço bonito, que abre em qualquer lado e depois trata de encaminhar. **Já leva os 21 produtos lá dentro**, com o preço e o link do myPOS.

```
genialtarot.com/pagar.html?c=30min       →  65 €
genialtarot.com/pagar.html?c=1hora       →  85 €
genialtarot.com/pagar.html?c=1pergunta   →  25 €
genialtarot.com/pagar.html?c=emergencia  →  110 €
```

**Instalar:** pôr o ficheiro na raiz do site, ao lado do `index.html`.

---

## Como funciona, por dentro

**Navegador normal** → encaminha para o myPOS ao fim de 1 segundo, sem o cliente dar por nada.

**Dentro do WhatsApp:**
- **Android** → `intent://` entrega o endereço ao Chrome e sai da aplicação
- **iPhone** → `x-safari-https://` obriga o Safari a abrir
- **Se nenhum resultar** → mostra *"toque no menu ⋮ e escolha Abrir no browser"* e um botão para copiar o link

**A ideia é nunca deixar o cliente ver um erro.** Ou paga, ou recebe instruções claras — nunca um "expirou" que o faz desistir e pensar mal do negócio.

---

## ⚠️ Por testar

**Nada disto foi testado a sério** — foi escrito, não experimentado. O `intent://` do Android é fiável e muito usado; o `x-safari-https://` do iPhone **funciona na maioria dos casos mas não em todos**, e é por isso que existe sempre o botão de copiar o link por baixo.

**Depois de instalar, testar assim:**
1. Mandar `genialtarot.com/pagar.html?c=30min` a si próprio pelo WhatsApp
2. Abrir no Android → deve saltar para o Chrome e mostrar os 65,00 EUR
3. Abrir no iPhone → deve saltar para o Safari; se não saltar, deve aparecer o aviso com o botão de copiar
4. Abrir num navegador normal → deve encaminhar sozinho

---

## O que dizer no WhatsApp entretanto

**Enquanto isto não estiver instalado**, e mesmo depois como rede de segurança:

> Não mandar o link do myPOS directamente. Mandar `genialtarot.com/loja` e dizer *"escolhe aí o serviço"*.

⚠️ **Atenção:** isso sozinho **só resolve metade** — a loja abre bem no WhatsApp, mas quando o cliente carrega em *Comprar Aqui* vai para o myPOS ainda dentro da aplicação e leva com o mesmo erro. **É precisamente isso que o `escapar-whatsapp.js` corrige.**

**Por email não há problema nenhum** — o email entrega os links ao navegador verdadeiro. A rotina automática das marcações está a salvo.

Ver [[Preços e Links de Pagamento]] e [[Dados Bancários]].
