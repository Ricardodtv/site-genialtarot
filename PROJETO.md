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
| `index.html` | **Página principal** — montra com atalhos, carrossel 22 arcanos, contactos |
| `tarot-gratis.html` | **Tarot Grátis** — jogo: formulário, 8 cartas, veredito, avaliação ⭐. TODO o texto (interface e vereditos) em tratamento formal "você" — manter assim em alterações futuras |
| `horoscopo.html` | **Mensagens do Universo** — signos diários (tempos do último vídeo). Sem vídeos fixos; contacto WhatsApp pulsante |
| `anual.html` | **Mensagem Anual** — Previsão Anual 2026, um vídeo por signo. Tema próprio: rubi/granada. Sem NENHUM vídeo fixo (só os que abrem por signo); tem secção de contacto WhatsApp pulsante (Consultas · Rituais · Amuletos) |
| `fimdesemana.html` | **Mensagem do Fim de Semana** — signos com tempos do último vídeo semanal. Tema verde-esmeralda (Diário é roxo). Sem vídeos fixos; contacto WhatsApp pulsante |
| `arvore.html` | **Árvore da Vida** — tiragem de Cabala: 10 Arcanos Maiores nas 10 Sefirot, animação de baixo para cima. Em cada nó: nome da carta → pergunta (dourada) → resposta (branca, frases variadas a cada tiragem, com o nome da pessoa destacado a dourado, tal como a síntese). Formulário de contacto obrigatório antes de lançar (grava no Supabase + avisa o Telegram com dados + síntese). **Limite: 1 tiragem por dia** por visitante (localStorage + verificação por IP no Supabase; excesso avisa o Telegram). Balão verde GRÁTIS no botão de lançar. Som de fundo místico gerado por Web Audio (sem ficheiro de áudio), **ligado por defeito** (os navegadores só deixam começar ao 1.º toque/clique do visitante); botão flutuante ♪ com risco vermelho diagonal quando desligado. Lista de serviços (Árvore, Mapas Astrais, Conselhos Empresariais/Espirituais, Hipnose) por baixo do WhatsApp. Fundo esotérico animado (nebulosas violeta/índigo a derivar, estrelas a cintilar, círculos de geometria sagrada ténues) mantendo contraste — caixas de texto têm fundo sólido. Seta-guia amarela flutuante durante a leitura: "(Nome), IMPORTANTE — depois veja a SÍNTESE"; clique leva à síntese, esconde-se quando ela fica visível. Sefirot com nome em português + original entre parênteses. Síntese RESUMIDA (sem repetir as cartas) + 3 conselhos verdes para progredir; a antiga "leitura posição a posição" foi removida. Separadores místicos ☽✦☾ (árvore→síntese e WhatsApp→serviços). Tema azul-noite/dourado, contacto WhatsApp |
| `worker.js` | A "ponte" Cloudflare: serve o site + APIs (ver abaixo) |
| `wrangler.jsonc` | Config Cloudflare (main: worker.js, assets: raiz) |
| `.assetsignore` | Esconde ficheiros técnicos do público |
| imagens/áudio | `profile.png`, `tudo-aqui.png`, `mestre-alberto.jpg` (tarot), `mestre-horoscopo.jpg`, `mystic-ambient.mp3`, `ambient.mp3`, `favicon.ico`, `og-image.png` |

O deck de tarot (78 cartas + textos do veredito) está EMBUTIDO dentro de
`tarot-gratis.html`. As cartas do carrossel vêm de imagens da Wikimedia; as do
jogo de trustedtarot.com.

## worker.js — rotas da ponte

- `/notify` (POST) → envia avisos ao **Telegram** (leituras, avaliações ⭐, limite diário, bloqueios).
  Segredos na Cloudflare (Settings → Variables and Secrets): `TELEGRAM_BOT_TOKEN`
  (bot @GenialtarotAvisosbot) e `TELEGRAM_CHAT_ID` (387064533 = Telegram pessoal do Alberto).
  Diagnóstico: `/notify?test=1` (GET) envia mensagem de teste e mostra estado.
- `/api/zodiac` → último vídeo do Horóscopo Diário + minutos por signo
  (playlist `PL1CDtoz2ES7SiWoZTboxt124gX-BKn8p6`), via feed RSS do YouTube. Cache 15 min.
  ⚠️ Só o RSS funciona da Cloudflare — as páginas/API interna do YouTube são bloqueadas.
- `/api/fimsemana` → idem, playlist Fim de Semana `PL1CDtoz2ES7SMhQqxpoRsJ2uzsi8caP48`.
- `/api/anual` → playlist Anual `PL1CDtoz2ES7Rj4Pgnzsk1B0yMJ5MsZRim`, organiza
  vídeos por signo pelo TÍTULO. Cache 1h. (Virgem em falta na playlist — acende sozinho se for adicionado.)
- Todas as rotas aceitam `?debug=1` para diagnóstico.

## Base de dados (leituras do Tarot)

- Supabase gerido pelo **Lovable Cloud** (projeto bjucptcepnjlkicxcnmh), tabela
  `tarot_readings` — o URL e a chave pública estão dentro de `tarot-gratis.html`.
- ⚠️ NÃO apagar os projetos do Lovable: a base de dados morre com eles.
- **TAREFA FUTURA:** migrar para conta Supabase própria do Alberto (criar conta grátis,
  recriar tabelas/políticas, copiar leituras, trocar URL+chave no tarot-gratis.html).
- Limite de 2 leituras/dia e bloqueios são geridos no navegador do visitante (localStorage).

## Outras notas

- Navegação cruzada: as 3 páginas de horóscopo têm 2 botões grandes cada, a apontar
  para as OUTRAS duas (nenhuma página tem botão para si própria). Na página principal,
  os botões Diário/Anual/Fim de Semana usam as cores das páginas de destino
  (roxo/rubi/esmeralda) e os efeitos pesados (halos blur) estão desligados em ecrãs ≤640px.
  Atalho "Árvore da Vida" (azul-noite/dourado, ícone SVG com o esquema das 10 Sefirot)
  aponta para arvore.html e pulsa como os restantes.
- Áudio de fundo: TODAS as páginas têm som ligado POR DEFEITO (arranca ao 1.º toque se o
  navegador travar o autoplay) com fade-in. Botão de som UNIFICADO em todas as páginas:
  círculo ♪ fixo no canto superior direito, anel amarelo a piscar (1,1s), dourado quando
  ligado, risco vermelho diagonal quando desligado. Volume IGUAL em todas (0.02),
  exceto a árvore (0.45, som gerado por Web Audio). Fade index: 1s.
  **Continuidade:** a música partilhada (mystic-ambient: index + 3 horóscopos) continua no
  mesmo ponto ao mudar de página (sessionStorage `mus_mystic`; tarot-gratis usa `mus_ambient`).
  Se o visitante desligar o som, fica desligado durante a sessão.
- Links externos que se mantêm: WhatsApp +351 914 920 427, Agenda (calendar.app.google),
  Loja (linktr.ee/genialtarot), Livro (Amazon), Observação do Céu (tutiempo), redes sociais.
- Futuro desejado: email profissional contacto@genialtarot.com via Cloudflare Email
  Routing → Gmail (chequesegredo@gmail.com).
- História: o site nasceu de 3 projetos Lovable convertidos para estático em jul/2026.
