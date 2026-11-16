#!/usr/bin/env python3
"""Gera tiragem-em-cruz.html (16/11/2026, O-473, Radar «tarot cruz 5 cartas grátis»).
Molde: tiragem-templo-de-afrodite.html (CSS base, botão de som e música lidos de lá, por marcadores).
O JSON-LD sai dos mesmos textos que a página mostra. Texto corrido passado pelo humanizer.
Correr na pasta do repositório (ou worktree): python3 tiragem-em-cruz-gerar.py"""
import json, html, os
R = os.path.dirname(os.path.abspath(__file__)) + "/"
ref = open(R + "tiragem-templo-de-afrodite.html", encoding="utf-8").read()
i0 = ref.index(":root {"); i1 = ref.index("/* ============ Templo de Afrodite (02/11/2026)")
CSS_BASE = ref[i0:i1].rstrip()
m0 = ref.index("<script>\n/* 🎵 28/10/2026"); MUSICA = ref[m0:ref.index("</script>", m0) + len("</script>")]
BOTAO_SOM = [l for l in ref.split("\n") if l.startswith('<button id="audio-fab"')][0]

URL = "https://genialtarot.com/tiragem-em-cruz"
IMG = "https://genialtarot.com/tiragem-em-cruz.webp"
TITULO = "Tarot em Cruz: tiragem grátis de 5 cartas (Tarô da Cruz)"
DESC = ("Tiragem do tarot em cruz de 5 cartas, grátis, com o baralho do Mestre Alberto: o que está a favor, "
        "o que está contra, o caminho, o resultado e a síntese.")
assert len(TITULO) <= 65 and 110 <= len(DESC) <= 160, (len(TITULO), len(DESC))

PASSOS = [
    ("Escreva a pergunta", "Uma só pergunta, clara, sobre algo que dependa em parte de si. «Devo aceitar a proposta da empresa X?» funciona melhor do que «O que vai ser da minha vida?»"),
    ("Baralhe e corte", "Baralhe as cartas a pensar na pergunta e corte o baralho. Se quiser usar o método antigo, separe antes os 22 Arcanos Maiores."),
    ("Disponha as cartas em cruz", "A carta 1 vai para a esquerda, a 2 para a direita, a 3 para cima, a 4 para baixo e a 5 para o meio. No método antigo tire só as quatro primeiras."),
    ("Leia a balança e depois o caminho", "Compare a carta 1 com a carta 2 para ver qual pesa mais. Depois leia a carta 3, que diz o que fazer, e a carta 4, que mostra onde isso leva."),
    ("Feche com a carta do centro", "A carta 5 junta as outras quatro. No método antigo some os números das quatro cartas; se o total passar de 22, some os algarismos até ficar entre 1 e 22. O 22 é O Louco."),
]

FAQ = [
    ("Quantas cartas tem a tiragem em cruz?",
     "Cinco. Quatro formam os braços da cruz (a favor, contra, o caminho e o resultado) e a quinta fica no centro, com a síntese."),
    ("Qual é a diferença entre a tiragem em cruz e a Cruz Celta?",
     "A Cruz Celta tem dez cartas e olha para a situação em várias camadas: o passado, o que está por baixo, os receios, o ambiente à volta. A tiragem em cruz tem cinco e fica-se por uma pergunta concreta. Faz-se mais depressa e é mais fácil de ler para quem está a começar."),
    ("A carta do centro tira-se ou calcula-se?",
     "As duas formas existem. Com o baralho completo de 78 cartas tira-se, como as outras. No método antigo do Tarot de Marselha, só com os Arcanos Maiores, somam-se os números das quatro cartas e reduz-se o total até ficar entre 1 e 22; o 22 é O Louco."),
    ("A tiragem em cruz serve para perguntas de amor?",
     "Serve. A carta 1 mostra o que ajuda a relação, a 2 o que a trava, a 3 o que pode fazer e a 4 para onde vai. Se quer comparar o que você e a outra pessoa pensam e sentem, o Templo de Afrodite foi feito para isso."),
    ("Posso repetir a tiragem se não gostar da resposta?",
     "Pode, mas a leitura perde força. Muitos tarólogos aconselham esperar uns dias antes de voltar à mesma pergunta, ou mudá-la para algo que dependa mais de si."),
    ("A tiragem em cruz aqui é mesmo grátis?",
     "É. As cartas são baralhadas no seu aparelho, não precisa de se registar e a tiragem não fica guardada."),
]

# ---------- o exemplo (inventado, dito como exemplo) ----------
EXEMPLO = [
    (1, "A favor", "Três de Paus", "/cartas/menores/three-of-wands.webp", "/carta-tres-de-paus",
     "A Joana já olha para longe. O Três de Paus é horizonte e expansão: a vontade de ir existe e tem por onde crescer."),
    (2, "Contra", "Dez de Paus", "/cartas/menores/ten-of-wands.webp", "/carta-dez-de-paus",
     "O peso está nela. O Dez de Paus é carregar tudo sozinha: o medo de não dar conta da mudança, da casa nova e do trabalho ao mesmo tempo."),
    (3, "O caminho", "A Temperança", "/cartas/14-a-temperanca.webp", "/arcano-14-a-temperanca",
     "Ir com calma e juntar o velho com o novo: negociar a data de entrada, levar o que já funciona e pedir ajuda."),
    (4, "O resultado", "Seis de Paus", "/cartas/menores/six-of-wands.webp", "/carta-seis-de-paus",
     "Reconhecimento. Se fizer a mudança ao seu ritmo, o trabalho novo tende a correr bem e a ser notado."),
    (5, "A síntese", "O Carro", "/cartas/07-o-carro.webp", "/arcano-07-o-carro",
     "Decidir e seguir com direção. O Carro diz que a resposta depende de ela pegar nas rédeas."),
]

def e(s): return html.escape(s, quote=True)

passos_html = "".join(f"<li><b>{e(t)}.</b> {e(x)}</li>" for t, x in PASSOS)
faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in FAQ)
exemplo_html = "".join(
    f'<figure class="ex"><a href="{href}"><img src="{src}" alt="Carta {e(nome)} do baralho do Mestre Alberto, exemplo da tiragem em cruz, carta {n}" width="480" height="804" loading="lazy"></a>'
    f'<figcaption><b>Carta {n} · {e(pos)}</b><a href="{href}">{e(nome)}</a><span>{e(txt)}</span></figcaption></figure>'
    for n, pos, nome, src, href, txt in EXEMPLO)

ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#pagina", "name": TITULO, "description": DESC, "url": URL, "inLanguage": "pt",
     "isPartOf": {"@type": "WebSite", "name": "Genial Tarot", "url": "https://genialtarot.com/"},
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": "https://genialtarot.com/sobre"},
     "primaryImageOfPage": {"@id": IMG + "#imagem"}, "breadcrumb": {"@id": URL + "#migalhas"}},
    {"@type": "ImageObject", "@id": IMG + "#imagem", "contentUrl": IMG, "url": IMG, "width": 1200, "height": 675,
     "name": "Tiragem em cruz de 5 cartas com o baralho do Mestre Alberto",
     "caption": "As cinco cartas da tiragem em cruz com o baralho do Mestre Alberto: a favor à esquerda, contra à direita, o caminho em cima, o resultado em baixo e a síntese ao centro.",
     "creator": {"@type": "Person", "name": "Mestre Alberto", "url": "https://genialtarot.com/sobre"},
     "copyrightHolder": {"@type": "Organization", "name": "Genial Tarot", "url": "https://genialtarot.com/"},
     "creditText": "Genial Tarot · Mestre Alberto", "inLanguage": "pt"},
    {"@type": "BreadcrumbList", "@id": URL + "#migalhas", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://genialtarot.com/"},
        {"@type": "ListItem", "position": 2, "name": "Tarot por tema", "item": "https://genialtarot.com/tarot-por-tema"},
        {"@type": "ListItem", "position": 3, "name": "Tiragem em Cruz", "item": URL}]},
    {"@type": "HowTo", "name": "Como fazer a tiragem em cruz de 5 cartas no tarot",
     "description": "Os passos para tirar e ler as cinco cartas da tiragem em cruz: a favor, contra, o caminho, o resultado e a síntese.",
     "image": IMG, "inLanguage": "pt",
     "supply": [{"@type": "HowToSupply", "name": "Um baralho de tarot (78 cartas, ou só os 22 Arcanos Maiores no método antigo)"}],
     "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": x, "url": URL + "#como-se-faz"} for i, (t, x) in enumerate(PASSOS)]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}
LD = json.dumps(ld, ensure_ascii=False)

CSS_PROPRIO = r"""
/* ============ Tiragem em Cruz (16/11/2026, O-473) ============ */
.destaque { display: block; width: 100%; height: auto; max-width: 60rem; margin: 0 auto 1.2rem; border-radius: 1.2rem; border: 1px solid var(--borda); box-shadow: 0 20px 60px #0008; }
.texto { font-family: var(--serifa); font-size: 1.15rem; color: var(--lavanda); }
.texto h2 { text-align: left; margin-top: 1.4rem; color: var(--texto); }
.texto h2:first-child { margin-top: 0; }
.texto h3 { font-family: var(--titulo); font-size: 1.05rem; color: var(--ouro); margin: 1.2rem 0 .3rem; }
.texto p { margin: 0 0 .8rem; } .texto ol, .texto ul { padding-left: 1.3rem; } .texto li { margin: 0 0 .5rem; }
.texto b { color: var(--texto); }
.nota { font-size: 1rem; border-left: 3px solid var(--ouro); padding: .4rem .9rem; margin: 1rem 0; background: oklch(0.85 0.13 88 / .07); border-radius: 0 .6rem .6rem 0; }
/* as cinco casas desenhadas em cruz, também no texto */
.casas { display: grid; gap: .6rem; grid-template-columns: repeat(3, 1fr); margin: .6rem 0 1rem; font-family: Inter, sans-serif; font-size: .9rem; }
.casas div { background: var(--vidro); border: 1px solid var(--borda); border-radius: .9rem; padding: .6rem .8rem; }
.casas .c1 { grid-area: 2 / 1; } .casas .c2 { grid-area: 2 / 3; } .casas .c3 { grid-area: 1 / 2; } .casas .c4 { grid-area: 3 / 2; }
.casas .c5 { grid-area: 2 / 2; border-color: oklch(0.85 0.13 88 / .7); }
.casas b { color: var(--ouro); display: block; font-size: .76rem; letter-spacing: .08em; text-transform: uppercase; }
/* a tiragem interativa: 3 × 3 com os cantos vazios */
.cruz { display: grid; grid-template-columns: repeat(3, 1fr); gap: .7rem .9rem; max-width: 22rem; margin: 1.2rem auto 0; }
.lugar { position: relative; perspective: 900px; aspect-ratio: 480 / 804; }
.lugar[data-p="1"] { grid-area: 2 / 1; } .lugar[data-p="2"] { grid-area: 2 / 3; } .lugar[data-p="3"] { grid-area: 1 / 2; }
.lugar[data-p="4"] { grid-area: 3 / 2; } .lugar[data-p="5"] { grid-area: 2 / 2; }
.lugar[data-p="5"] .vira img { border-color: var(--ouro); box-shadow: 0 0 26px oklch(0.85 0.13 88 / .45), 0 8px 22px #000a; }
.vira { position: absolute; inset: 0; transform-style: preserve-3d; transition: transform .8s cubic-bezier(.3,.7,.3,1); }
.lugar.aberta .vira { transform: rotateY(180deg); }
.vira img { position: absolute; inset: 0; width: 100%; height: 100%; border-radius: .5rem; backface-visibility: hidden; -webkit-backface-visibility: hidden; box-shadow: 0 8px 22px #000a; border: 1px solid oklch(0.85 0.13 88 / .55); }
.vira .frente { transform: rotateY(180deg); }
.num { position: absolute; top: -.55rem; right: -.55rem; z-index: 2; width: 1.6rem; height: 1.6rem; border-radius: 50%; display: grid; place-items: center; font-family: var(--titulo); font-weight: 700; font-size: .85rem; color: var(--ouro); background: oklch(0.20 0.07 272); border: 1.5px solid var(--ouro); }
.rot { position: absolute; left: 0; right: 0; bottom: -1.25rem; text-align: center; font-size: .66rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: var(--suave); }
.cruz .lugar { margin-bottom: 1.1rem; }
.metodo { display: flex; gap: .6rem; align-items: flex-start; justify-content: center; max-width: 30rem; margin: 1.4rem auto 0; font-size: .9rem; color: var(--lavanda); cursor: pointer; }
.metodo input { width: 1.2rem; height: 1.2rem; margin-top: .15rem; accent-color: oklch(0.85 0.13 88); flex: none; }
.accoes { text-align: center; margin: 1.1rem 0 .4rem; }
.accoes button { font: inherit; cursor: pointer; border: 0; }
.leitura { display: grid; gap: .7rem; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr)); margin-top: 1.2rem; }
.leitura .pos { display: flex; gap: .8rem; align-items: center; background: oklch(0.20 0.06 272 / .88); border: 1px solid var(--borda); border-radius: 1rem; padding: .7rem .8rem; }
.leitura .pos img { width: 3.2rem; height: auto; border-radius: .3rem; flex: none; }
.leitura .pos b { display: block; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: var(--ouro); }
.leitura .pos a { font-family: var(--titulo); font-weight: 700; color: var(--texto); }
.leitura .pos small { display: block; color: var(--suave); font-size: .82rem; }
.leitura .pos .ler { font-family: Inter, sans-serif; font-weight: 600; font-size: .8rem; color: var(--azul-claro); }
.leitura .soma { grid-column: 1 / -1; text-align: center; font-size: .9rem; color: var(--lavanda); }
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
@media (max-width: 30rem) { .heroi h1 { font-size: 1.85rem; } .cruz { gap: .5rem .55rem; } .casas { font-size: .8rem; gap: .4rem; } .casas div { padding: .45rem .5rem; } .texto { font-size: 1.08rem; } .rot { font-size: .58rem; } }
@media (prefers-reduced-motion: reduce) { .vira { transition: none; } }
"""

NOMES_POS = ["A favor", "Contra", "O caminho", "O resultado", "A síntese"]
LUGARES = "".join(
    f'<div class="lugar" data-p="{p}"><span class="num">{p}</span><div class="vira">'
    f'<img class="verso" src="/cartas/verso-gt.webp" alt="Verso da carta {p} do baralho do Mestre Alberto, ainda por virar, na tiragem em cruz" width="480" height="804" loading="lazy">'
    f'<img class="frente" alt="" width="480" height="804"></div><span class="rot">{NOMES_POS[p-1]}</span></div>'
    for p in range(1, 6))

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
<meta property="og:image:alt" content="As cinco cartas da tiragem em cruz com o baralho do Mestre Alberto" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<style>
/* ============ Tiragem em Cruz: azul-noite e ouro, base copiada da tiragem-templo-de-afrodite.html (16/11/2026) ============ */
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
    <div><span class="selo">✚ Tiragem em cruz ✦ 5 cartas</span></div>
    <h1>A <span class="az">Tiragem em Cruz</span> de 5 cartas</h1>
    <p class="sub">Cinco cartas em cruz para uma pergunta concreta: o que joga a seu favor, o que pesa contra, o caminho a seguir e o resultado provável. Tire-as aqui, grátis, com o baralho do Mestre Alberto.</p>
    <img class="destaque" src="/tiragem-em-cruz.webp" alt="Tiragem em cruz com o baralho do Mestre Alberto: Três de Paus à esquerda, Dez de Paus à direita, A Temperança em cima, Seis de Paus em baixo e O Carro ao centro" width="1200" height="675" fetchpriority="high" />
    <div class="botoes"><a class="btn ouro" href="#tirar">✨ Tirar as minhas 5 cartas</a><a class="btn" href="#como-se-faz">Como se faz</a></div>
  </section>

  <section class="cartao texto">
    <h2>O que é a tiragem em cruz</h2>
    <p>A tiragem em cruz usa cinco cartas: quatro formam os braços de uma cruz e a quinta fica no meio. Em França chamam-lhe <i>tirage en croix</i> e é um dos métodos mais antigos do Tarot de Marselha. No Brasil é conhecida como método da cruz ou jogo da cruz.</p>
    <p>Serve para uma pergunta de cada vez. Põe frente a frente o que está a seu favor e o que pesa contra, mostra o caminho entre os dois e o resultado provável, e no centro junta tudo numa carta. Para olhar para a vida inteira com mais pormenor, a <a href="/tiragem-cruz-celta">Cruz Celta</a> usa dez cartas. A cruz de cinco é mais curta e vai direta à pergunta.</p>
    <h2>As cinco posições da cruz</h2>
    <p>As cartas ficam como estão desenhadas aqui em baixo. Leia primeiro a linha do meio, da esquerda para a direita, e depois a coluna, de cima para baixo.</p>
    <div class="casas">
      <div class="c3"><b>Carta 3 · em cima</b>O caminho: a atitude que a situação lhe pede. Na tradição francesa é «o juiz», que decide entre a carta 1 e a carta 2.</div>
      <div class="c1"><b>Carta 1 · à esquerda</b>A favor: as suas forças, as pessoas do seu lado, o que ajuda.</div>
      <div class="c5"><b>Carta 5 · ao centro</b>A síntese: o centro da questão, a resposta numa só carta.</div>
      <div class="c2"><b>Carta 2 · à direita</b>Contra: o obstáculo, o que trava, às vezes um receio que ainda não quer ver.</div>
      <div class="c4"><b>Carta 4 · em baixo</b>O resultado: para onde a questão tende se seguir o caminho da carta 3.</div>
    </div>
    <p class="nota"><b>Há mais do que uma forma de ler a cruz.</b> Na mais comum, que é a que uso aqui, a esquerda é o que está a favor e a direita o que está contra. Há tarólogos que a leem no tempo: o centro é o presente, a esquerda o passado, a direita o futuro próximo, em cima o que ajuda e em baixo o que trava. E no método antigo, só com os 22 Arcanos Maiores, a quinta carta não se tira do baralho: calcula-se pela soma das outras quatro. Na tiragem grátis desta página pode escolher esse método.</p>
    <h2>Para que perguntas serve</h2>
    <ul>
      <li>Uma decisão com prós e contras: aceitar um emprego, mudar de casa, começar um projeto.</li>
      <li>Um problema que se arrasta e que não sabe por onde pegar.</li>
      <li>Uma relação em que quer perceber o que ajuda e o que atrapalha.</li>
      <li>Uma questão de dinheiro ou de trabalho com um prazo à vista.</li>
    </ul>
    <p>Para uma resposta rápida há o <a href="/tiragem-sim-ou-nao">Tarot Sim ou Não</a>. Para ver uma história no tempo, chega a <a href="/tiragem-tres-cartas">tiragem de 3 cartas</a> (passado, presente e futuro).</p>

    <h2 id="como-se-faz">Como se faz, passo a passo</h2>
    <ol>{passos_html}</ol>

    <h2>Como ler as cinco cartas em conjunto</h2>
    <p>Comece pela balança entre a carta 1 e a carta 2. Um Arcano Maior pesa mais do que um Menor: se o obstáculo é A Torre e o que está a favor é um Dois de Ouros, quem manda é o obstáculo, e a pergunta passa a ser como atravessá-lo.</p>
    <p>Os naipes dizem de onde vem cada coisa. Copas fala de sentimentos, Paus de vontade e ação, Espadas de pensamentos e conflitos, Ouros de dinheiro, corpo e trabalho. Um obstáculo de Espadas costuma estar na cabeça de quem pergunta, numa preocupação ou numa conversa que ficou por ter.</p>
    <p>Leia a carta 4 sempre depois da carta 3. O resultado é para onde as coisas vão se seguir o conselho do caminho. Se a carta 4 não lhe agrada, volte à 3, porque é aí que está o que pode mudar.</p>
    <p>A carta do centro responde à pergunta tal como a fez. Se lhe parecer que não encaixa, pergunte-se se era mesmo aquela a pergunta que queria fazer.</p>
  </section>

  <section class="cartao" id="tirar">
    <h2>A sua <span class="az">tiragem em cruz</span>, grátis</h2>
    <p class="sub" style="text-align:center">Pense na sua pergunta. Quando estiver pronta ou pronto, carregue no botão: as cartas do baralho do Mestre Alberto são baralhadas e cinco viram na cruz.</p>
    <div class="cruz" id="mesa">{LUGARES}</div>
    <label class="metodo"><input type="checkbox" id="antigo"><span>Método antigo: só os 22 Arcanos Maiores, com a carta do centro calculada pela soma das outras quatro.</span></label>
    <div class="accoes"><button type="button" class="btn ouro" id="tirarBtn">🔮 Baralhar e tirar as 5 cartas</button></div>
    <div class="leitura" id="leitura" aria-live="polite"></div>
    <p class="fonte">As cartas são baralhadas no seu aparelho com um gerador aleatório criptográfico. Cada tiragem é única e não fica guardada.</p>
  </section>

  <section class="cartao texto">
    <h2>Um exemplo de leitura</h2>
    <p><i>Este exemplo foi inventado para mostrar como se lê a tiragem; não é a consulta de ninguém.</i> A Joana recebeu uma proposta de trabalho noutra cidade e pergunta: «Devo aceitar?»</p>
    <div class="exemplo">{exemplo_html}</div>
    <p>A balança pende para a carta 1: a vontade de ir é real, e o Dez de Paus fala mais de cansaço por antecipação do que de um perigo vindo de fora. A Temperança pede à Joana que não carregue tudo de uma vez, e com isso o Seis de Paus mostra um bom resultado. O Carro, ao centro, diz que a decisão é dela e que está em condições de a tomar.</p>
    <p>Com o método antigo a conta seria outra. Se a Joana tivesse tirado A Imperatriz (3), O Carro (7), O Enforcado (12) e O Sol (19), a soma dava 41. Como passa de 22, somam-se os algarismos, 4 + 1 = 5, e a carta do centro seria O Hierofante, que aconselha a ouvir quem já fez o mesmo caminho.</p>
  </section>

  <section class="cartao texto">
    <h2>Perguntas frequentes</h2>
    {faq_html}
  </section>

  <section class="cartao chamada">
    <h2>Quer que eu leia as <span class="az">suas</span> cartas?</h2>
    <p>A tiragem grátis dá-lhe as cartas. Numa consulta leio-as consigo, com a sua pergunta e a sua história, como faço há 18 anos.</p>
    <div class="botoes"><a class="btn ouro" href="loja.html#cat-consultas">🔮 Marcar uma consulta</a></div>
    <div class="ligas"><a href="/tiragem-cruz-celta">A Cruz Celta (10 cartas)</a><a href="/tarot-gratis">🃏 Tarot Grátis</a><a href="/tiragem-tres-cartas">Tiragem de 3 cartas</a><a href="/tiragem-ferradura">Tiragem da Ferradura</a><a href="/tiragem-sim-ou-nao">Tarot Sim ou Não</a><a href="/tiragem-templo-de-afrodite">💞 Templo de Afrodite</a><a href="/tiragem-do-amor">💗 Tiragem do Amor</a></div>
  </section>

  <p class="fonte fontes">A disposição segue o método clássico da cruz do Tarot de Marselha (<i>tirage en croix</i>). As leituras são simbólicas e não substituem aconselhamento profissional.</p>
</div>
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="privacidade.html">Política de Privacidade</a> · <a href="termos.html">Termos de Serviço</a>
</footer>

<script>
/* 🔮 A tiragem em cruz (16/11/2026, O-473). Baralho do Mestre Alberto, montado como no Templo de Afrodite
   (Maiores em /cartas/NN-slug.webp, Menores em /cartas/menores/<rank>-of-<naipe>.webp, sem cartas invertidas).
   Método antigo: só os 22 Maiores; a carta 5 é a soma das 4 (O Louco conta 0), reduzida até ficar entre 1 e 22; 22 = O Louco. */
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
  ].map(([f, nome, k], n) => ({{ nome, k, n, img: "/cartas/" + f + ".webp", url: "/arcano-" + f }}));
  const NAIPES = [["Paus","paus","wands",["paixão","ação"]],["Copas","copas","cups",["emoções","afeto"]],["Espadas","espadas","swords",["pensamento","decisões"]],["Ouros","ouros","pentacles",["material","trabalho"]]];
  const NUMEROS = [["Ás","as","ace","semente"],["Dois","dois","two","escolha"],["Três","tres","three","crescimento"],["Quatro","quatro","four","estabilidade"],
    ["Cinco","cinco","five","desafio"],["Seis","seis","six","harmonia"],["Sete","sete","seven","estratégia"],["Oito","oito","eight","movimento"],
    ["Nove","nove","nine","realização"],["Dez","dez","ten","ciclo completo"],["Valete","valete","page","mensagem"],["Cavaleiro","cavaleiro","knight","ação decidida"],
    ["Rainha","rainha","queen","maturidade"],["Rei","rei","king","liderança"]];
  const MENORES = NAIPES.flatMap(([n, np, ne, tema]) => NUMEROS.map(([r, rp, re, k]) => ({{
    nome: r + " de " + n, k: [k, ...tema], img: "/cartas/menores/" + re + "-of-" + ne + ".webp", url: "/carta-" + rp + "-de-" + np }})));
  const BARALHO = [...MAIORES, ...MENORES];   // 78
  const CASAS = ["A favor","Contra","O caminho","O resultado","A síntese"];
  function aleatorio(n) {{   // inteiro uniforme em [0, n) sem enviesamento
    const lim = Math.floor(0x100000000 / n) * n, u = new Uint32Array(1);
    do {{ crypto.getRandomValues(u); }} while (u[0] >= lim);
    return u[0] % n;
  }}
  function baralhar(a) {{ a = a.slice(); for (let i = a.length - 1; i > 0; i--) {{ const j = aleatorio(i + 1); [a[i], a[j]] = [a[j], a[i]]; }} return a; }}
  function reduzir(s) {{ while (s > 22) s = String(s).split("").reduce((t, d) => t + +d, 0); return s; }}
  const ESC = (s) => s.replace(/[&<>"]/g, c => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }}[c]));
  const lugares = [...document.querySelectorAll("#mesa .lugar")];
  const btn = document.getElementById("tirarBtn"), leitura = document.getElementById("leitura"), antigo = document.getElementById("antigo");
  let ocupado = false;
  btn.addEventListener("click", () => {{
    if (ocupado) return; ocupado = true; btn.disabled = true;
    let tiradas, soma = "";
    if (antigo.checked) {{
      tiradas = baralhar(MAIORES).slice(0, 4);
      const total = tiradas.reduce((t, c) => t + c.n, 0), r = reduzir(total);
      tiradas.push(MAIORES[r === 22 ? 0 : r]);
      soma = "Método antigo: " + tiradas.slice(0, 4).map(c => c.n).join(" + ") + " = " + total
        + (total > 22 ? " → " + String(total).split("").join(" + ") + " = " + reduzir(total) : "") + ", e a carta do centro é " + tiradas[4].nome + ".";
    }} else tiradas = baralhar(BARALHO).slice(0, 5);
    leitura.innerHTML = "";
    lugares.forEach(l => l.classList.remove("aberta"));
    setTimeout(() => {{
      Promise.all(tiradas.map(c => new Promise(ok => {{ const i = new Image(); i.onload = i.onerror = ok; i.src = c.img; }}))).then(() => {{
        tiradas.forEach((c, i) => {{
          const l = lugares.find(x => +x.dataset.p === i + 1), f = l.querySelector(".frente");
          f.src = c.img;
          f.alt = "Carta " + c.nome + " do baralho do Mestre Alberto, tiragem em cruz, carta " + (i + 1) + ": " + CASAS[i].toLowerCase();
          setTimeout(() => l.classList.add("aberta"), 350 * i);
        }});
        setTimeout(() => {{
          leitura.innerHTML = tiradas.map((c, i) =>
            `<div class="pos"><img src="${{c.img}}" alt="Carta ${{ESC(c.nome)}} do baralho do Mestre Alberto, tiragem em cruz, carta ${{i + 1}}" width="480" height="804" loading="lazy">`
            + `<div><b>Carta ${{i + 1}} · ${{CASAS[i]}}</b><a href="${{c.url}}">${{ESC(c.nome)}}</a><small>${{c.k.join(" · ")}}</small>`
            + `<a class="ler" href="${{c.url}}">Ler o significado da carta →</a></div></div>`).join("")
            + (soma ? `<p class="soma">${{ESC(soma)}}</p>` : "");
          btn.textContent = "🔮 Baralhar de novo"; btn.disabled = false; ocupado = false;
        }}, 350 * 5 + 500);
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
open(R + "tiragem-em-cruz.html", "w", encoding="utf-8").write(PAGINA)
print("título", len(TITULO), "descrição", len(DESC))
