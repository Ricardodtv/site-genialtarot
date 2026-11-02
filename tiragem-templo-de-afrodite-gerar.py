#!/usr/bin/env python3
"""Gera ~/site-genialtarot/tiragem-templo-de-afrodite.html (02/11/2026).
CSS base, botão de som e música copiados da horoscopo-do-dia.html; o JSON-LD sai dos mesmos textos que a página mostra."""
import json, html
R = "/home/ricardo/site-genialtarot/"
ref = open(R + "horoscopo-do-dia.html", encoding="utf-8").read().split("\n")
CSS_BASE = "\n".join(ref[23:59]) + "\n" + "\n".join(ref[87:116])   # :root..foto-mestre + aviso..som (linhas 24-59, 88-116)
MUSICA = "\n".join(ref[245:321])                                    # <script> da música (linhas 246-321)
assert MUSICA.startswith("<script>") and MUSICA.endswith("</script>"), "os blocos da referência mudaram de sítio"
BOTAO_SOM = [l for l in ref if l.startswith('<button id="audio-fab"')][0]

URL = "https://genialtarot.com/tiragem-templo-de-afrodite"
IMG = "https://genialtarot.com/tiragem-templo-de-afrodite.webp"
TITULO = "Templo de Afrodite no Tarot: tiragem do amor grátis de 7 cartas"
DESC = ("Tiragem Templo de Afrodite no tarot, grátis, com o baralho do Mestre Alberto: as 7 posições, "
        "o que cada um pensa, sente e deseja, e um exemplo de leitura.")
assert len(TITULO) <= 65 and 110 <= len(DESC) <= 160, (len(TITULO), len(DESC))

PASSOS = [
    ("Escolha a pessoa e a pergunta", "Pense numa só relação de cada vez: um namoro, um casamento, alguém que conheceu há pouco ou alguém que ficou no passado. Formule a pergunta com calma, por exemplo: «Como está a nossa relação e para onde vai?»"),
    ("Decida que coluna é de quem", "Antes de abrir o jogo, decida qual das colunas é a sua e qual é a da outra pessoa. Aqui usamos a forma mais comum: as casas 1, 2 e 3 são suas; as casas 4, 5 e 6 são da outra pessoa."),
    ("Baralhe e corte", "Baralhe as 78 cartas a pensar na pergunta e corte o baralho. Se quiser dar um prazo à casa 7, diga-o antes de tirar as cartas, por exemplo «nos próximos três meses»."),
    ("Disponha as sete cartas", "Coloque as cartas 1, 2 e 3 de cima para baixo numa coluna, as cartas 4, 5 e 6 na coluna ao lado, e a carta 7 no centro, entre as duas."),
    ("Leia por pares e feche com a casa 7", "Compare as cartas linha a linha: 1 com 4 (o que pensam), 2 com 5 (o que sentem), 3 com 6 (a atração e as atitudes). Só no fim leia a casa 7, à luz de tudo o que viu antes."),
]

FAQ = [
    ("O que é a tiragem Templo de Afrodite?",
     "É uma tiragem de tarot de sete cartas para o amor. Põe lado a lado duas pessoas em três planos, o que pensam, o que sentem e a atração e atitudes de cada uma, e fecha com uma carta central sobre o rumo da relação. É associada ao tarólogo brasileiro Nei Naiff, que a apresenta no livro «Tarô e Amor: Templo de Afrodite»."),
    ("Quais são as posições do Templo de Afrodite?",
     "Na forma mais comum, as casas 1, 2 e 3 são de quem pergunta e as casas 4, 5 e 6 são da outra pessoa. As casas 1 e 4 mostram o que cada um pensa; as casas 2 e 5, o que cada um sente; as casas 3 e 6, a atração, o desejo e as atitudes. A casa 7, ao centro, mostra o rumo da relação e o conselho."),
    ("A casa 1 é sempre de quem pergunta?",
     "Não há acordo entre as fontes. A maioria dos textos põe as casas 1, 2 e 3 do lado de quem pergunta, mas há quem diga que na versão original de Nei Naiff é ao contrário, e há quem deixe a escolha a quem tira as cartas, desde que a decisão seja tomada antes de abrir o jogo. O importante é decidir antes e manter a mesma regra sempre."),
    ("Posso usar o Templo de Afrodite para amizades ou família?",
     "Pode. As casas 1, 2, 4 e 5 funcionam em qualquer relação. Nas casas 3 e 6, que no amor falam de atração e desejo, numa amizade ou na família leem-se como a atitude, o comportamento e a forma como cada um se mostra ao outro."),
    ("A casa 7 diz se vamos ficar juntos?",
     "A casa 7 mostra a tendência da relação, não uma sentença. Há tarólogos que a leem como o rumo para os próximos três meses e outros como um conselho e um prognóstico ao mesmo tempo. Leia-a sempre com as outras seis cartas: é o conjunto que dá a resposta."),
    ("Posso fazer a tiragem só para mim, sem outra pessoa?",
     "Há quem abra só uma coluna e a casa 7, para olhar a sua própria forma de pensar, sentir e agir no amor. Mas o Templo de Afrodite foi pensado para duas pessoas: é na comparação entre as duas colunas que está a sua força."),
]

# ---------- o exemplo (inventado, dito como exemplo) ----------
EXEMPLO = [
    (1, "O que você pensa", "Dois de Espadas", "/cartas/menores/two-of-swords.webp", "/carta-dois-de-espadas",
     "A Marta pensa na relação mas não decide nada: a venda nos olhos do Dois de Espadas mostra alguém que prefere não ver para não ter de escolher."),
    (2, "O que você sente", "Ás de Copas", "/cartas/menores/ace-of-cups.webp", "/carta-as-de-copas",
     "No coração, a resposta é clara: o Ás de Copas é um sentimento novo, verdadeiro e generoso. Ela gosta mais do que admite."),
    (3, "Atração e atitudes (você)", "Cavaleiro de Paus", "/cartas/menores/knight-of-wands.webp", "/carta-cavaleiro-de-paus",
     "O desejo é forte e ela tem vontade de avançar. O Cavaleiro de Paus é impulso, energia e pressa."),
    (4, "O que a outra pessoa pensa", "O Eremita", "/cartas/09-o-eremita.webp", "/arcano-09-o-eremita",
     "O Rui pensa muito e diz pouco. O Eremita mostra alguém que precisa de tempo e de espaço para perceber o que quer."),
    (5, "O que a outra pessoa sente", "Seis de Copas", "/cartas/menores/six-of-cups.webp", "/carta-seis-de-copas",
     "Há carinho e ternura verdadeira, mas o Seis de Copas também fala do passado: pode haver uma história antiga que ainda pesa."),
    (6, "Atração e atitudes (a outra pessoa)", "Quatro de Ouros", "/cartas/menores/four-of-pentacles.webp", "/carta-quatro-de-ouros",
     "Na prática, ele segura-se. O Quatro de Ouros é contenção: a atração existe, mas ele protege-se e não se entrega."),
    (7, "O rumo da relação", "A Estrela", "/cartas/17-a-estrela.webp", "/arcano-17-a-estrela",
     "A Estrela é esperança e cura. A relação tem futuro, desde que se dê tempo ao tempo e não se force o ritmo."),
]

def e(s): return html.escape(s, quote=True)

passos_html = "".join(f"<li><b>{e(t)}.</b> {e(x)}</li>" for t, x in PASSOS)
faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in FAQ)
exemplo_html = "".join(
    f'<figure class="ex"><a href="{href}"><img src="{src}" alt="Carta {e(nome)} do baralho do Mestre Alberto — exemplo da tiragem Templo de Afrodite, casa {n}" width="480" height="804" loading="lazy"></a>'
    f'<figcaption><b>Casa {n} · {e(pos)}</b><a href="{href}">{e(nome)}</a><span>{e(txt)}</span></figcaption></figure>'
    for n, pos, nome, src, href, txt in EXEMPLO)

ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#pagina", "name": TITULO, "description": DESC, "url": URL, "inLanguage": "pt",
     "isPartOf": {"@type": "WebSite", "name": "Genial Tarot", "url": "https://genialtarot.com/"},
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": "https://genialtarot.com/sobre"},
     "primaryImageOfPage": {"@id": IMG + "#imagem"}, "breadcrumb": {"@id": URL + "#migalhas"}},
    {"@type": "ImageObject", "@id": IMG + "#imagem", "contentUrl": IMG, "url": IMG, "width": 1200, "height": 675,
     "name": "Tiragem Templo de Afrodite com o baralho do Mestre Alberto",
     "caption": "As sete cartas da tiragem Templo de Afrodite dispostas em forma de templo, com as cartas do baralho do Mestre Alberto: duas colunas de três cartas e a sétima ao centro.",
     "creator": {"@type": "Person", "name": "Mestre Alberto", "url": "https://genialtarot.com/sobre"},
     "copyrightHolder": {"@type": "Organization", "name": "Genial Tarot", "url": "https://genialtarot.com/"},
     "creditText": "Genial Tarot · Mestre Alberto", "inLanguage": "pt"},
    {"@type": "BreadcrumbList", "@id": URL + "#migalhas", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://genialtarot.com/"},
        {"@type": "ListItem", "position": 2, "name": "Tarot por tema", "item": "https://genialtarot.com/tarot-por-tema"},
        {"@type": "ListItem", "position": 3, "name": "Tiragem Templo de Afrodite", "item": URL}]},
    {"@type": "HowTo", "name": "Como fazer a tiragem Templo de Afrodite no tarot",
     "description": "Os passos para tirar e ler as sete cartas do Templo de Afrodite, a tiragem do tarot para o amor.",
     "image": IMG, "inLanguage": "pt",
     "supply": [{"@type": "HowToSupply", "name": "Um baralho de tarot de 78 cartas"}],
     "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": x, "url": URL + "#como-se-faz"} for i, (t, x) in enumerate(PASSOS)]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}
LD = json.dumps(ld, ensure_ascii=False)

CSS_PROPRIO = r"""
/* ============ Templo de Afrodite (02/11/2026) ============ */
.destaque { display: block; width: 100%; height: auto; max-width: 60rem; margin: 0 auto 1.2rem; border-radius: 1.2rem; border: 1px solid var(--borda); box-shadow: 0 20px 60px #0008; }
.texto { font-family: var(--serifa); font-size: 1.15rem; color: var(--lavanda); }
.texto h2 { text-align: left; margin-top: 1.4rem; color: var(--texto); }
.texto h2:first-child { margin-top: 0; }
.texto h3 { font-family: var(--titulo); font-size: 1.05rem; color: var(--ouro); margin: 1.2rem 0 .3rem; }
.texto p { margin: 0 0 .8rem; } .texto ol, .texto ul { padding-left: 1.3rem; } .texto li { margin: 0 0 .5rem; }
.texto b { color: var(--texto); }
.nota { font-size: 1rem; border-left: 3px solid var(--ouro); padding: .4rem .9rem; margin: 1rem 0; background: oklch(0.85 0.13 88 / .07); border-radius: 0 .6rem .6rem 0; }
.casas { display: grid; gap: .6rem; grid-template-columns: 1fr 1fr; margin: .6rem 0 1rem; font-family: Inter, sans-serif; font-size: .92rem; }
.casas div { background: var(--vidro); border: 1px solid var(--borda); border-radius: .9rem; padding: .6rem .8rem; }
.casas .sete { grid-column: 1 / -1; border-color: oklch(0.85 0.13 88 / .6); }
.casas b { color: var(--ouro); display: block; font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; }
/* a tiragem interativa: duas colunas (os pilares) e a sétima carta ao centro, debaixo de um frontão */
.templo { position: relative; max-width: 30rem; margin: 1rem auto 0; padding-top: 4.2rem; }
.frontao { position: absolute; top: 0; left: -4%; right: -4%; height: 3.6rem; }
.frontao svg { width: 100%; height: 100%; display: block; }
.mesa { display: grid; grid-template-columns: repeat(3, 1fr); gap: .7rem .9rem; border-bottom: 3px solid var(--ouro); padding-bottom: .8rem; }
.lugar { position: relative; perspective: 900px; aspect-ratio: 480 / 804; }
.lugar[data-p="1"] { grid-area: 1 / 1; } .lugar[data-p="2"] { grid-area: 2 / 1; } .lugar[data-p="3"] { grid-area: 3 / 1; }
.lugar[data-p="4"] { grid-area: 1 / 3; } .lugar[data-p="5"] { grid-area: 2 / 3; } .lugar[data-p="6"] { grid-area: 3 / 3; }
.lugar[data-p="7"] { grid-area: 2 / 2; }
.vira { position: absolute; inset: 0; transform-style: preserve-3d; transition: transform .8s cubic-bezier(.3,.7,.3,1); }
.lugar.aberta .vira { transform: rotateY(180deg); }
.vira img { position: absolute; inset: 0; width: 100%; height: 100%; border-radius: .5rem; backface-visibility: hidden; -webkit-backface-visibility: hidden; box-shadow: 0 8px 22px #000a; border: 1px solid oklch(0.85 0.13 88 / .55); }
.vira .frente { transform: rotateY(180deg); }
.num { position: absolute; top: -.55rem; right: -.55rem; z-index: 2; width: 1.6rem; height: 1.6rem; border-radius: 50%; display: grid; place-items: center; font-family: var(--titulo); font-weight: 700; font-size: .85rem; color: var(--ouro); background: oklch(0.20 0.07 272); border: 1.5px solid var(--ouro); }
.legenda-mesa { display: grid; grid-template-columns: repeat(3, 1fr); gap: .9rem; text-align: center; font-size: .72rem; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: var(--suave); margin-top: .5rem; }
.accoes { text-align: center; margin: 1.3rem 0 .4rem; }
.accoes button { font: inherit; cursor: pointer; border: 0; }
.leitura { display: grid; gap: .7rem; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr)); margin-top: 1.2rem; }
.leitura .pos { display: flex; gap: .8rem; align-items: center; background: oklch(0.20 0.06 272 / .88); border: 1px solid var(--borda); border-radius: 1rem; padding: .7rem .8rem; }
.leitura .pos img { width: 3.2rem; height: auto; border-radius: .3rem; flex: none; }
.leitura .pos b { display: block; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: var(--ouro); }
.leitura .pos a { font-family: var(--titulo); font-weight: 700; color: var(--texto); }
.leitura .pos small { display: block; color: var(--suave); font-size: .82rem; }
.leitura .pos .ler { font-family: Inter, sans-serif; font-weight: 600; font-size: .8rem; color: var(--azul-claro); }
.exemplo { display: grid; gap: .8rem; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); margin: 1rem 0; }
.ex { margin: 0; display: flex; gap: .8rem; align-items: flex-start; background: oklch(0.20 0.06 272 / .7); border: 1px solid var(--borda); border-radius: 1rem; padding: .7rem; }
.ex img { width: 4.2rem; height: auto; border-radius: .35rem; flex: none; }
.ex figcaption { font-family: Inter, sans-serif; font-size: .9rem; color: var(--lavanda); }
.ex figcaption b { display: block; font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: var(--ouro); }
.ex figcaption a { display: block; font-family: var(--titulo); font-weight: 700; color: var(--texto); margin: .1rem 0 .25rem; }
.ligas { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; margin: 1.2rem 0 0; }
.ligas a { text-decoration: none; font-weight: 700; font-size: .9rem; color: var(--texto); border: 1px solid var(--borda); background: var(--vidro); border-radius: 999px; padding: .5rem 1rem; }
.ligas a:hover { border-color: var(--ouro); }
.fontes { font-family: Inter, sans-serif; font-size: .8rem; color: var(--suave); }
.fontes a { color: var(--suave); }
@media (max-width: 30rem) { .mesa { gap: .55rem .6rem; } .casas { font-size: .84rem; gap: .45rem; } .casas div { padding: .5rem .6rem; } .texto { font-size: 1.08rem; } }
@media (prefers-reduced-motion: reduce) { .vira { transition: none; } }
"""

FRONTAO_SVG = '<svg viewBox="0 0 300 40" preserveAspectRatio="none" aria-hidden="true"><polygon points="150,3 4,37 296,37" fill="none" stroke="oklch(0.85 0.13 88)" stroke-width="2.2" vector-effect="non-scaling-stroke"/></svg>'

LUGARES = "".join(
    f'<div class="lugar" data-p="{p}"><span class="num">{p}</span><div class="vira">'
    f'<img class="verso" src="/cartas/verso-gt.webp" alt="Verso da carta {p} do baralho do Mestre Alberto, ainda por virar — tiragem Templo de Afrodite" width="480" height="804" loading="lazy">'
    f'<img class="frente" alt="" width="480" height="804"></div></div>'
    for p in range(1, 8))

PAGINA = f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(TITULO)}</title>
<meta name="description" content="{e(DESC)}" />
<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="favicon.ico" />
<meta property="og:title" content="{e(TITULO)}" />
<meta property="og:description" content="{e(DESC)}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{URL}" />
<link rel="canonical" href="{URL}" />
<meta property="og:image" content="{IMG}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="675" />
<meta property="og:image:alt" content="As sete cartas da tiragem Templo de Afrodite em forma de templo, com o baralho do Mestre Alberto" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<style>
/* ============ Tiragem Templo de Afrodite — azul-noite e ouro, base copiada da horoscopo-do-dia.html (02/11/2026) ============ */
{CSS_BASE}
{CSS_PROPRIO}
</style>
<script type="application/ld+json">
{LD}
</script>
</head>
<body>
{BOTAO_SOM}
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
  <section class="heroi">
    <div><span class="selo">💞 Tiragem do amor ✦ 7 cartas</span></div>
    <h1>O <span class="az">Templo de Afrodite</span> no Tarot</h1>
    <p class="sub">A tiragem que põe frente a frente o que você e a outra pessoa pensam, sentem e desejam. Faça-a aqui, grátis, com o baralho do Mestre Alberto.</p>
    <img class="destaque" src="/tiragem-templo-de-afrodite.webp" alt="Tiragem Templo de Afrodite com o baralho do Mestre Alberto: duas colunas de três cartas debaixo de um frontão de templo e A Estrela ao centro" width="1200" height="675" fetchpriority="high" />
    <div class="botoes"><a class="btn ouro" href="#tirar">✨ Tirar as minhas 7 cartas</a><a class="btn" href="#como-se-faz">Como se faz</a></div>
  </section>

  <section class="cartao texto">
    <h2>O que é o Templo de Afrodite</h2>
    <p>O Templo de Afrodite é uma tiragem de tarot de <b>sete cartas</b> feita para o amor. Em vez de perguntar apenas «ele gosta de mim?», compara as duas pessoas lado a lado em três planos: <b>o que pensam</b>, <b>o que sentem</b> e <b>a atração e as atitudes</b> de cada uma. A sétima carta, ao centro, fala do <b>rumo da relação</b>.</p>
    <p>É associada ao tarólogo brasileiro Nei Naiff, que a apresenta no livro <i>Tarô e Amor: Templo de Afrodite</i>, e hoje é usada por muitos tarólogos, com pequenas diferenças de um para outro, que explico mais abaixo.</p>
    <h2>A forma do templo e as sete casas</h2>
    <p>As cartas ficam em <b>duas colunas de três</b>, uma para cada pessoa, e a <b>sétima ao centro</b>, entre as duas. Pode vê-la como um templo: as duas colunas são os pilares que seguram a relação e a carta do meio é o lugar onde as duas vidas se encontram. As colunas leem-se em pares, linha a linha:</p>
    <div class="casas">
      <div><b>Casa 1 · você</b>O que pensa da outra pessoa e da relação: as intenções, as dúvidas, os motivos.</div>
      <div><b>Casa 4 · a outra pessoa</b>O que ela pensa de si e da relação.</div>
      <div><b>Casa 2 · você</b>O que sente de verdade, mesmo que pense ou diga outra coisa.</div>
      <div><b>Casa 5 · a outra pessoa</b>O que ela sente de verdade e o que deseja.</div>
      <div><b>Casa 3 · você</b>A atração, o desejo e a forma como age na prática.</div>
      <div><b>Casa 6 · a outra pessoa</b>A atração, o desejo e as atitudes dela.</div>
      <div class="sete"><b>Casa 7 · ao centro</b>O rumo da relação: a tendência para os próximos tempos e o conselho para os dois.</div>
    </div>
    <p class="nota"><b>Onde as fontes não concordam.</b> A maioria dos textos põe as casas 1, 2 e 3 do lado de quem pergunta; há quem diga que na versão original de Nei Naiff é ao contrário (as primeiras três seriam da outra pessoa), e há tarólogos que deixam a escolha a quem tira, desde que se decida antes de abrir o jogo. Também a casa 7 é lida de formas diferentes: para uns é a tendência dos próximos três meses, para outros é um conselho e um prognóstico ao mesmo tempo. Aqui uso a forma mais comum: 1 a 3 são suas, 4 a 6 da outra pessoa.</p>
    <h2>Para que perguntas serve</h2>
    <ul>
      <li>Uma relação que começou há pouco e ainda não se percebe para onde vai.</li>
      <li>Um namoro ou casamento em que um sente que o outro está diferente.</li>
      <li>Alguém de quem gosta e que não sabe se sente o mesmo.</li>
      <li>Uma pessoa do passado: um ex, uma reconciliação possível.</li>
      <li>Também amizades e família: aí as casas 3 e 6 leem-se como a atitude e o comportamento de cada um, e não como desejo.</li>
    </ul>
    <p>Não é a tiragem certa para perguntas de sim ou não, nem para quem ainda não tem ninguém em vista. Para isso há a <a href="/tiragem-do-amor">tiragem do amor de 5 cartas</a> ou o <a href="/tarot-do-amor">tarot do amor</a>.</p>

    <h2 id="como-se-faz">Como se faz, passo a passo</h2>
    <ol>{passos_html}</ol>

    <h2>Como ler as posições em conjunto</h2>
    <p><b>Leia por linhas, não carta a carta.</b> A força do Templo de Afrodite está na comparação. Se na casa 2 sai uma carta de Copas cheia de sentimento e na casa 5 sai uma carta fria, a diferença entre as duas é a mensagem: um dá mais do que o outro.</p>
    <p><b>Veja onde as duas colunas se parecem e onde se afastam.</b> Pensamentos parecidos (1 e 4) mostram que os dois veem a relação da mesma forma. Sentimentos parecidos (2 e 5) são a base mais forte que pode haver. Atração forte nas casas 3 e 6 com sentimentos fracos em 2 e 5 fala de uma relação mais de pele do que de coração.</p>
    <p><b>Procure a contradição dentro de cada pessoa.</b> Quando a casa 1 diz uma coisa e a casa 2 diz outra, a pessoa pensa uma coisa e sente outra. É muito comum e é muitas vezes o centro da consulta.</p>
    <p><b>Repare nas figuras.</b> Há tarólogos que leem os Reis e as Rainhas como pessoas reais envolvidas na relação. Se aparecerem, pergunte-se quem podem ser.</p>
    <p><b>Feche com a casa 7.</b> Só depois de ver as seis cartas é que a sétima faz sentido. Ela não é uma sentença: é para onde as coisas vão se nada mudar, e o conselho para o que pode ser mudado.</p>
  </section>

  <section class="cartao" id="tirar">
    <h2>A sua tiragem <span class="az">Templo de Afrodite</span>, grátis</h2>
    <p class="sub" style="text-align:center">Pense na pessoa e na relação. Quando estiver pronta ou pronto, carregue no botão: as 78 cartas do baralho do Mestre Alberto são baralhadas e sete viram no templo.</p>
    <div class="templo">
      <div class="frontao">{FRONTAO_SVG}</div>
      <div class="mesa" id="mesa">{LUGARES}</div>
      <div class="legenda-mesa"><span>Você</span><span>O rumo</span><span>A outra pessoa</span></div>
    </div>
    <div class="accoes"><button type="button" class="btn ouro" id="tirarBtn">🔮 Baralhar e tirar as 7 cartas</button></div>
    <div class="leitura" id="leitura" aria-live="polite"></div>
    <p class="fonte" id="fonteTiragem">As cartas são baralhadas no seu aparelho com um gerador aleatório criptográfico. Cada tiragem é única e não fica guardada.</p>
  </section>

  <section class="cartao texto">
    <h2>Um exemplo de leitura completa</h2>
    <p><i>Este exemplo foi inventado para mostrar como se lê a tiragem; não é a consulta de ninguém.</i> A Marta sai há quatro meses com o Rui e pergunta: «O que se passa entre nós e para onde vai isto?»</p>
    <div class="exemplo">{exemplo_html}</div>
    <p><b>A leitura em conjunto.</b> Na linha do sentimento (casas 2 e 5) há afeto dos dois lados, e isso é a boa notícia. A diferença está no ritmo: a Marta sente com força (Ás de Copas) e quer avançar (Cavaleiro de Paus), mas ainda não decidiu o que quer (Dois de Espadas); o Rui gosta, mas está fechado em si (O Eremita) e segura-se (Quatro de Ouros), talvez por causa de algo do passado (Seis de Copas). Se ela o apressar, ele recua ainda mais.</p>
    <p>A Estrela na casa 7 dá o conselho: paciência e confiança. Primeiro a Marta tem de tirar a venda e decidir o que quer; depois, deixar o Rui chegar ao ritmo dele. Lida assim, a relação tem caminho.</p>
  </section>

  <section class="cartao texto">
    <h2>Perguntas frequentes</h2>
    {faq_html}
  </section>

  <section class="cartao chamada">
    <h2>Quer que eu leia as <span class="az">suas</span> cartas?</h2>
    <p>A tiragem grátis dá-lhe as cartas; numa consulta leio-as consigo, com a sua história e a da outra pessoa, como faço há 18 anos.</p>
    <div class="botoes"><a class="btn ouro" href="loja.html#cat-consultas">🔮 Marcar uma consulta</a></div>
    <div class="ligas"><a href="/tiragem-do-amor">💗 Tiragem do Amor (5 cartas)</a><a href="/tarot-do-amor">❤️ Tarot do Amor</a><a href="/tarot-gratis">🃏 Tarot Grátis</a><a href="/signos-que-combinam">✨ Signos que combinam</a><a href="/tiragem-ferradura">Tiragem da Ferradura</a><a href="/tiragem-cruz-celta">A Cruz Celta</a></div>
  </section>

  <p class="fonte fontes">Sobre as posições: consultámos o livro <i>Tarô e Amor: Templo de Afrodite</i>, de Nei Naiff (Editora Alfabeto), tal como é descrito pelas livrarias, e os textos de vários tarólogos, como <a href="https://olunariotarot.home.blog/2020/03/22/metodos-do-tarot-o-templo-de-afrodite/" rel="nofollow noopener" target="_blank">O Lunário</a>, <a href="https://www.cartasdodestino.com/2011/06/metodo-de-taro-templo-de-afrodite.html" rel="nofollow noopener" target="_blank">Cartas do Destino</a> e <a href="https://yubmiranda.com.br/post/reflexoes-sobre-o-templo-de-afrodite/" rel="nofollow noopener" target="_blank">Yub Miranda</a>. Onde divergem, dizemo-lo no texto. As leituras são simbólicas e não substituem aconselhamento profissional.</p>
</div>
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="privacidade.html">Política de Privacidade</a> · <a href="termos.html">Termos de Serviço</a>
</footer>

<script>
/* 🔮 A tiragem Templo de Afrodite (02/11/2026). O baralho é o do Mestre Alberto, montado como no tarot-gratis.html
   (Maiores em /cartas/NN-slug.webp, Menores em /cartas/menores/<rank>-of-<naipe>.webp, sem cartas invertidas).
   Nos Menores o nome é «Valete» (é o que está impresso nas cartas dele e o que usam as páginas /carta-valete-de-…). */
(function () {{
  const MAIORES = [
    ["00-o-louco","O Louco",["novos começos","liberdade","salto de fé"]],["01-o-mago","O Mago",["manifestação","ação","vontade"]],
    ["02-a-sacerdotisa","A Sacerdotisa",["intuição","mistério","saber interior"]],["03-a-imperatriz","A Imperatriz",["abundância","cuidado","criatividade"]],
    ["04-o-imperador","O Imperador",["estrutura","autoridade","estabilidade"]],["05-o-hierofante","O Hierofante",["tradição","valores","conselho"]],
    ["06-os-enamorados","Os Enamorados",["escolha","união","harmonia"]],["07-o-carro","O Carro",["determinação","vitória","movimento"]],
    ["08-a-forca","A Força",["coragem","paciência","ternura"]],["09-o-eremita","O Eremita",["introspeção","silêncio","guia interior"]],
    ["10-a-roda-da-fortuna","A Roda da Fortuna",["ciclos","destino","viragem"]],["11-a-justica","A Justiça",["verdade","equilíbrio","consequência"]],
    ["12-o-enforcado","O Enforcado",["pausa","perspetiva","espera"]],["13-a-morte","A Morte",["fim de ciclo","transformação","renovação"]],
    ["14-a-temperanca","A Temperança",["equilíbrio","moderação","harmonia"]],["15-o-diabo","O Diabo",["apego","tentação","padrões"]],
    ["16-a-torre","A Torre",["rutura","revelação","verdade"]],["17-a-estrela","A Estrela",["esperança","inspiração","cura"]],
    ["18-a-lua","A Lua",["ilusão","intuição","medo"]],["19-o-sol","O Sol",["alegria","sucesso","clareza"]],
    ["20-o-julgamento","O Julgamento",["despertar","balanço","renovação"]],["21-o-mundo","O Mundo",["realização","conclusão","plenitude"]]
  ].map(([f, nome, k]) => ({{ nome, k, img: "/cartas/" + f + ".webp", url: "/arcano-" + f }}));
  const NAIPES = [["Paus","paus","wands",["paixão","ação"]],["Copas","copas","cups",["emoções","afeto"]],["Espadas","espadas","swords",["pensamento","decisões"]],["Ouros","ouros","pentacles",["material","trabalho"]]];
  const NUMEROS = [["Ás","as","ace","semente"],["Dois","dois","two","escolha"],["Três","tres","three","crescimento"],["Quatro","quatro","four","estabilidade"],
    ["Cinco","cinco","five","desafio"],["Seis","seis","six","harmonia"],["Sete","sete","seven","estratégia"],["Oito","oito","eight","movimento"],
    ["Nove","nove","nine","realização"],["Dez","dez","ten","ciclo completo"],["Valete","valete","page","mensagem"],["Cavaleiro","cavaleiro","knight","ação decidida"],
    ["Rainha","rainha","queen","maturidade"],["Rei","rei","king","liderança"]];
  const MENORES = NAIPES.flatMap(([n, np, ne, tema]) => NUMEROS.map(([r, rp, re, k]) => ({{
    nome: r + " de " + n, k: [k, ...tema], img: "/cartas/menores/" + re + "-of-" + ne + ".webp", url: "/carta-" + rp + "-de-" + np }})));
  const BARALHO = [...MAIORES, ...MENORES];   // 78
  const CASAS = ["O que você pensa","O que você sente","A sua atração e atitudes","O que a outra pessoa pensa","O que a outra pessoa sente","A atração e as atitudes dela","O rumo da relação"];
  function aleatorio(n) {{   // inteiro uniforme em [0, n) sem enviesamento
    const lim = Math.floor(0x100000000 / n) * n, u = new Uint32Array(1);
    do {{ crypto.getRandomValues(u); }} while (u[0] >= lim);
    return u[0] % n;
  }}
  function baralhar(a) {{ a = a.slice(); for (let i = a.length - 1; i > 0; i--) {{ const j = aleatorio(i + 1); [a[i], a[j]] = [a[j], a[i]]; }} return a; }}
  const ESC = (s) => s.replace(/[&<>"]/g, c => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }}[c]));
  const lugares = [...document.querySelectorAll("#mesa .lugar")];
  const btn = document.getElementById("tirarBtn"), leitura = document.getElementById("leitura");
  let ocupado = false;
  btn.addEventListener("click", () => {{
    if (ocupado) return; ocupado = true; btn.disabled = true;
    const tiradas = baralhar(BARALHO).slice(0, 7);
    leitura.innerHTML = "";
    lugares.forEach(l => l.classList.remove("aberta"));
    // espera que as cartas acabem de voltar ao verso antes de trocar as frentes
    setTimeout(() => {{
      // pré-carrega as sete frentes e só depois as vira, pela ordem das casas
      Promise.all(tiradas.map(c => new Promise(ok => {{ const i = new Image(); i.onload = i.onerror = ok; i.src = c.img; }}))).then(() => {{
        tiradas.forEach((c, i) => {{
          const l = lugares.find(x => +x.dataset.p === i + 1), f = l.querySelector(".frente");
          f.src = c.img;
          f.alt = "Carta " + c.nome + " do baralho do Mestre Alberto — tiragem Templo de Afrodite, casa " + (i + 1) + ": " + CASAS[i].toLowerCase();
          setTimeout(() => l.classList.add("aberta"), 350 * i);
        }});
        setTimeout(() => {{
          leitura.innerHTML = tiradas.map((c, i) =>
            `<div class="pos"><img src="${{c.img}}" alt="Carta ${{ESC(c.nome)}} do baralho do Mestre Alberto — tiragem Templo de Afrodite, casa ${{i + 1}}" width="480" height="804" loading="lazy">`
            + `<div><b>Casa ${{i + 1}} · ${{CASAS[i]}}</b><a href="${{c.url}}">${{ESC(c.nome)}}</a><small>${{c.k.join(" · ")}}</small>`
            + `<a class="ler" href="${{c.url}}">Ler o significado da carta →</a></div></div>`).join("");
          btn.textContent = "🔮 Baralhar de novo"; btn.disabled = false; ocupado = false;
        }}, 350 * 7 + 500);
      }});
    }}, lugares.some(l => l.classList.contains("aberta")) ? 850 : 0);
  }});
}})();
</script>
{MUSICA}
<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""
open(R + "tiragem-templo-de-afrodite.html", "w", encoding="utf-8").write(PAGINA)
print("título", len(TITULO), "descrição", len(DESC))
