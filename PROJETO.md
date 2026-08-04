# PROJETO GENIALTAROT — Bilhete de Identidade do Site

> Documento de contexto para o Claude (Cowork). Se estás a ler isto numa conversa
> nova: este ficheiro descreve toda a arquitetura do site do Alberto (Mestre
> Alberto, Genial Tarot). Lê-o antes de fazer alterações.
>
> **REGRA DE MANUTENÇÃO:** sempre que fizeres uma alteração significativa ao site
> (página nova, rota nova no worker, mudança de arquitetura ou de links), atualiza
> este PROJETO.md e entrega-o ao Alberto junto com os ficheiros alterados, para
> ele subir tudo ao repositório de uma só vez.
>
> **SEGURANÇA:** este repositório é PÚBLICO. Nunca colocar aqui tokens, senhas,
> chaves privadas ou dados pessoais de clientes — segredos vivem só na Cloudflare
> (Variables and Secrets).

## O essencial

- **Site no ar:** https://genialtarot.com (e www.genialtarot.com)
- **Código:** GitHub, repositório público `ricardodtv/site-genialtarot` (branch `main`)
- **Publicação:** Cloudflare Workers (projeto `site-genialtarot`, conta chequesegredo@gmail.com).
  A Cloudflare está ligada ao GitHub: **cada commit publica automaticamente** (~1 min).
- **Endereço técnico de reserva:** https://site-genialtarot.chequesegredo.workers.dev
- **Domínio registado na Hostinger** (só o registo — renovar anualmente lá!).
  Nameservers: chip/gigi.ns.cloudflare.com. Alojamento Hostinger: dispensado.
- **Fluxo de trabalho:** o Claude edita os ficheiros e entrega zip → o Alberto faz
  upload no GitHub (Add file → Upload files → Commit) → Cloudflare publica sozinha.
  O Alberto NÃO é técnico: dar instruções passo a passo, simples, em PT-PT.

## Estrutura (tudo ficheiros soltos na raiz, SEM pastas — importante!)

| Ficheiro | O que é |
|---|---|
| `index.html` | **Página principal** — foto redonda grande (mestre-principal.jpg, círculo 14,5/18rem) com anéis de pulso + sistema solar; 9 Atalhos Místicos (Loja Online é o 2.º: fúchsia, etiqueta NOVA, anel a piscar → loja.html); botão dourado Jogar Tarot; bloco de botões da Loja; carrossel 22 arcanos, contactos |
| `tarot-gratis.html` | **Tarot Grátis** — jogo: formulário, 8 cartas, veredito, avaliação ⭐. TODO o texto (interface e vereditos) em tratamento formal "você" — manter assim em alterações futuras. Em ago/2026 foram REMOVIDAS a pedido do Alberto as secções "Como funciona o Genialtarot", "Porquê confiar no Genialtarot", "Escolhe a área que queres trabalhar" (grelha de áreas; os chips do formulário mantêm-se) e "Envolva-se no ambiente esotérico" — não recriar sem ele pedir |
| `horoscopo.html` | **Mensagens do Universo** — signos diários (tempos do último vídeo). Foto redonda própria (mestre-diario.jpg, círculo 16/20/22rem). Sem vídeos fixos; botões da Loja + contacto WhatsApp pulsante |
| `anual.html` | **Mensagem Anual** — Previsão Anual 2026, um vídeo por signo. Tema rubi/granada. Foto redonda própria (mestre-anual.jpg). Sem NENHUM vídeo fixo; botões da Loja + contacto WhatsApp pulsante |
| `fimdesemana.html` | **Mensagem do Fim de Semana** — signos com tempos do último vídeo semanal. Tema verde-esmeralda. Foto redonda própria (mestre-fds.jpg, círculo 16/20/22rem). Sem vídeos fixos; botões da Loja + contacto WhatsApp pulsante |
| `arvore.html` | **Árvore da Vida** — tiragem de Cabala: 10 Arcanos Maiores nas 10 Sefirot, animação de baixo para cima. Em cada nó: nome da carta → pergunta (dourada) → resposta (branca, frases variadas a cada tiragem, com o nome da pessoa destacado a dourado, tal como a síntese). Formulário de contacto obrigatório antes de lançar (grava no Supabase + avisa o Telegram com dados + síntese). **Limite: 1 tiragem por dia** por visitante (localStorage + verificação por IP no Supabase; excesso avisa o Telegram). Balão verde GRÁTIS no botão de lançar. Som de fundo místico gerado por Web Audio (sem ficheiro de áudio), **ligado por defeito**, volume 0.45; botão de som unificado no canto superior direito. Foto redonda própria no topo (mestre-arvore.jpg, círculo 16/20/22rem). A antiga lista de serviços do fundo foi SUBSTITUÍDA pelo bloco de botões da Loja (logo a seguir à árvore, com separador). Fundo esotérico animado (nebulosas violeta/índigo a derivar, estrelas a cintilar, círculos de geometria sagrada ténues) mantendo contraste — caixas de texto têm fundo sólido. Seta-guia amarela flutuante durante a leitura: "(Nome), IMPORTANTE — depois veja a SÍNTESE"; clique leva à síntese, esconde-se quando ela fica visível. Sefirot com nome em português + original entre parênteses. Síntese RESUMIDA (sem repetir as cartas) + 3 conselhos verdes para progredir; a antiga "leitura posição a posição" foi removida. Separadores místicos ☽✦☾ (árvore→síntese e WhatsApp→serviços). Tema azul-noite/dourado, contacto WhatsApp |
| `loja.html` | **Loja Mística** — topo: foto redonda (profile.png) com anéis, título e botões-categoria em 3 filas (Emergências grande com sirene a girar e sublinhado vermelho a piscar / Consultas+Rituais / Amuletos+Mapas Astrais+Cursos). Cartas de produto: foto quadrada, descrição, preço dourado grande, botão 🛒 Comprar Aqui (a piscar) → link myPOS, e lista "Outras formas de pagamento" (logo MB Way + 914 920 427 + WhatsApp mini a pulsar; transferência via WhatsApp). Fundo com cartas de tarot e símbolos a flutuar. **VERSAO_FOTOS** no JS: subir o número sempre que se troque uma foto mantendo o nome (anti-cache; atualmente 7) |
| `produtos.js` | **A lista de produtos da loja** — o ALBERTO edita este ficheiro (instruções lá dentro). 21 produtos em 6 categorias (Cursos sempre no fim). Selos: `destaque` (verde POPULAR), `topvendas` (dourado ⭐⭐⭐), `etiqueta`+`cor` (verde/violeta/vermelho/azul/laranja/rosa/dourado) +`estrelas` (1-5). Atuais: Pergunta=POPULAR; 30min=TOP VENDAS; 1h=A MAIS COMPLETA vermelho 5⭐; Anual=SEU FUTURO azul 3⭐; Casais=VOLTE A AMAR rosa 3⭐; Emergência=CONSULTA DE EMERGÊNCIA vermelho 5⭐; Prosperidade Fin.+Proteção=POPULAR; Mapa Astral=etiqueta violeta. Fotos: subir imagem ao GitHub + nome no campo `foto` (e subir VERSAO_FOTOS na loja.html se o nome repetir) |
| `ritual-exemplo.jpg` | Foto do produto de exemplo da loja (vela dourada) |
| `worker.js` | A "ponte" Cloudflare: serve o site + APIs (ver abaixo) |
| `wrangler.jsonc` | Config Cloudflare (main: worker.js, assets: raiz) |
| `.assetsignore` | Esconde ficheiros técnicos do público |
| imagens/áudio | Fotos redondas das páginas: `mestre-principal.jpg` (index), `mestre-diario.jpg` (horóscopo), `mestre-anual.jpg` (anual), `mestre-fds.jpg` (fim de semana), `mestre-arvore.jpg` (árvore), `profile.png` (loja), `mestre-horoscopo.jpg` (antiga, ainda no repo), `mestre-alberto.jpg` (tarot). Fotos de produtos: 21 .jpg (pergunta-escrita, consulta-*, previsao-anual, terapia-casais, parecer-cartas, quiromancia, prosperidade-financeira, protecao-limpeza, vela-guia, ritual-lua-cheia, incenso-oracao, abertura-caminhos, atracao-amor, ritual-prosperidade, consulta-emergencia, amuleto-*, mapa-astral, analise-signo, curso-tarot) + `mbway.png`. Áudio: `mystic-ambient.mp3`, `ambient.mp3`. Outros: `tudo-aqui.png`, `favicon.ico`, `og-image.png` |

O deck de tarot (78 cartas + textos do veredito) está EMBUTIDO dentro de
`tarot-gratis.html`. As cartas do carrossel vêm de imagens da Wikimedia; as do
jogo de trustedtarot.com.

## worker.js — rotas da ponte

- `/notify` (POST) → envia avisos ao **Telegram** (leituras, avaliações ⭐, limite diário, bloqueios).
  Segredos na Cloudflare (Settings → Variables and Secrets): `TELEGRAM_BOT_TOKEN`
  (bot @GenialtarotAvisosbot) e `TELEGRAM_CHAT_ID` (387064533 = Telegram pessoal do Alberto).
  Cada aviso inclui no fim a localização REAL detetada pela Cloudflare (cidade,
  região, país) e o IP do visitante — útil para comparar com o que a pessoa escreveu.
  Diagnóstico: `/notify?test=1` (GET) envia mensagem de teste e mostra estado.
- `/api/zodiac` → último vídeo do Horóscopo Diário + minutos por signo
  (playlist `PL1CDtoz2ES7SiWoZTboxt124gX-BKn8p6`), via feed RSS do YouTube. Cache 15 min.
  ⚠️ Só o RSS funciona da Cloudflare — as páginas/API interna do YouTube são bloqueadas.
- `/api/fimsemana` → idem, playlist Fim de Semana `PL1CDtoz2ES7SMhQqxpoRsJ2uzsi8caP48`.
- `/api/anual` → playlist Anual `PL1CDtoz2ES7Rj4Pgnzsk1B0yMJ5MsZRim`, organiza
  vídeos por signo pelo TÍTULO. Cache 1h. (Virgem em falta na playlist — acende sozinho se for adicionado.)
- `/Estataomp8` → página PRIVADA de visitas (endereço discreto de propósito; protegida por palavra-passe) com gráfico
  de barras, totais, painéis "Páginas mais visitadas" (hoje + período) e "Por onde chegam" (origens/referrers: Facebook, Instagram, Google, Linktree...; dataset detalhado da Cloudflare, guarda poucos dias no plano gratuito; apps como WhatsApp aparecem como Direto) e painel "De onde vêm os visitantes" (países com bandeiras e %); `/api/stats` vai buscar os números à API da Cloudflare.
  Precisa de 3 valores em Settings → Variables and Secrets do Worker:
  `CF_API_TOKEN` (Secret; token com permissão Analytics:Read na zona),
  `CF_ZONE_ID` (texto; Zone ID na página Overview do domínio),
  `STATS_KEY` (Secret; a palavra-passe da página). Diagnóstico: `/api/stats?debug=1`.
- Todas as rotas aceitam `?debug=1` para diagnóstico.

## Base de dados (leituras do Tarot)

- Supabase gerido pelo **Lovable Cloud** (projeto bjucptcepnjlkicxcnmh), tabela
  `tarot_readings` — o URL e a chave pública estão dentro de `tarot-gratis.html`.
- ⚠️ NÃO apagar os projetos do Lovable: a base de dados morre com eles.
- **TAREFA FUTURA:** migrar para conta Supabase própria do Alberto (criar conta grátis,
  recriar tabelas/políticas, copiar leituras, trocar URL+chave no tarot-gratis.html).
- Limite de 2 leituras/dia e bloqueios são geridos no navegador do visitante (localStorage).

## Outras notas

- **REGRA DOS BOTÕES DA LOJA:** o bloco de botões da Loja Mística (separador ☽✦☾ +
  nav-loja: Emergências com sirene a girar/Consultas/Rituais/Amuletos/Mapas Astrais/Cursos,
  a apontar para loja.html#cat-...) existe em: loja.html (topo), index.html (após o botão Jogar Tarot Agora),
  arvore.html, horoscopo.html, anual.html e fimdesemana.html. QUALQUER alteração a estes botões
  ou aos seus links deve ser replicada em TODAS estas páginas.

- Navegação cruzada: as 3 páginas de horóscopo têm 2 botões grandes cada, a apontar
  para as OUTRAS duas (nenhuma página tem botão para si própria). Na página principal,
  os botões Diário/Anual/Fim de Semana usam as cores das páginas de destino
  (roxo/rubi/esmeralda) e os efeitos pesados (halos blur) estão desligados em ecrãs ≤640px.
  Atalho "Árvore da Vida" (azul-noite/dourado, ícone SVG fino com o esquema das 10 Sefirot)
  aponta para arvore.html e pulsa como os restantes. (O atalho "Horóscopo Escrito" foi
  criado e depois REMOVIDO a pedido do Alberto — não recriar sem ele pedir.)
  Fotos redondas das 5 páginas + índex têm círculos AUMENTADOS (16/20/22rem nas páginas;
  14,5/18rem no índex) com a pessoa centrada — manter estes tamanhos.
- Áudio de fundo: TODAS as páginas têm som ligado POR DEFEITO (arranca ao 1.º toque se o
  navegador travar o autoplay) com fade-in. Botão de som UNIFICADO em todas as páginas:
  círculo ♪ fixo no canto superior direito, anel amarelo a piscar (1,1s), dourado quando
  ligado, risco vermelho diagonal quando desligado. Volume IGUAL em todas (0.02),
  exceto a árvore (0.45, som gerado por Web Audio). Fade index: 1s.
  **Continuidade:** a música partilhada (mystic-ambient: index + 3 horóscopos) continua no
  mesmo ponto ao mudar de página (sessionStorage `mus_mystic`; tarot-gratis usa `mus_ambient`).
  Se o visitante desligar o som, fica desligado durante a sessão.
- Links externos que se mantêm: WhatsApp +351 914 920 427, Agenda (calendar.app.google),
  Livro (Amazon), Observação do Céu (tutiempo), redes sociais. O botão "Loja Online" da
  página principal (2.º atalho, fúchsia com etiqueta NOVA e anel a piscar) aponta para
  loja.html (a antiga ligação ao linktr.ee foi substituída).
- Futuro desejado: email profissional contacto@genialtarot.com via Cloudflare Email
  Routing → Gmail (chequesegredo@gmail.com).
- História: o site nasceu de 3 projetos Lovable convertidos para estático em jul/2026.
