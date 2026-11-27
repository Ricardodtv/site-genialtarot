#!/usr/bin/env python3
"""Gera /tarot-terapeutico (27/11/2026, pedido dele: ideia n.º 4 da análise do myzenmoment.com, que tinha a rubrica
«Tarot terapêutico» e já não existe). Molde de eclipses-2027.html (estilo, gt-casa, rodapé), como o ano-pessoal-2027-gerar.py.
Regra: o Tarot como espelho e autoconhecimento; diz claramente que NÃO substitui psicólogo nem médico. Sem preços aqui
(os preços vivem no produtos.js e na /consulta-de-tarot-online). Texto: mudar AQUI e correr o gerador."""
import os, re, json, html
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"; URL = f"{SITE}/tarot-terapeutico"
e = html.escape
molde = open("eclipses-2027.html", encoding="utf-8").read()
ESTILO = re.search(r"<style>.*?</style>", molde, re.S).group(0)
CASA = re.search(r"<!-- gt-casa:inicio -->.*?<!-- gt-casa:fim -->", molde, re.S).group(0)
FIM = molde[molde.index("<footer>"):]

TITULO = "Tarot terapêutico: o Tarot como espelho para se conhecer"
DESC = "O que é o tarot terapêutico, como funciona uma leitura de autoconhecimento, as perguntas que cada carta faz e o que o Tarot não substitui. Com o Mestre Alberto."

CARTAS = [  # (arcano, página, a pergunta que a carta faz)
    ("O Eremita", "/arcano-09-o-eremita", "De que é que eu preciso de me afastar para ouvir a minha própria voz?"),
    ("A Torre", "/arcano-16-a-torre", "O que está a cair na minha vida, e o que é que essa queda me liberta?"),
    ("A Estrela", "/arcano-17-a-estrela", "Onde está a minha esperança, e o que a alimenta todos os dias?"),
    ("A Morte", "/arcano-13-a-morte", "Que fase já terminou e eu ainda não deixei ir?"),
]
FAQ = [
    ("O que é o tarot terapêutico?", "É uma forma de usar o Tarot para o autoconhecimento, e não para adivinhar o futuro. As cartas funcionam como um espelho: as imagens ajudam a pôr em palavras o que se sente e a olhar para uma situação de outro ângulo."),
    ("O tarot terapêutico substitui um psicólogo?", "Não. É uma leitura simbólica de reflexão e não substitui acompanhamento psicológico, psiquiátrico ou médico. Se está a passar por sofrimento intenso, procure um profissional de saúde; o Tarot pode caminhar ao lado, nunca no lugar dele."),
    ("Qual é a diferença para uma leitura de Tarot normal?", "Numa leitura de previsão pergunta-se «o que vai acontecer?». No tarot terapêutico pergunta-se «o que é que isto me mostra sobre mim?» e «o que posso fazer agora?». O foco está nas escolhas e não no destino."),
    ("Que perguntas posso levar a uma leitura destas?", "Perguntas sobre si: porque repito o mesmo padrão no amor, o que me impede de mudar de trabalho, como fechar uma fase, o que quero para o próximo ano. As melhores perguntas começam por «como» e «o que posso»."),
    ("Posso fazer tarot terapêutico à distância?", "Sim. As consultas do Mestre Alberto fazem-se online, por chamada, vídeo, áudio no WhatsApp ou por escrito, e as cartas são lançadas ao vivo."),
]

corpo = f"""<section class="heroi"><span class="selo">Tarot e autoconhecimento</span><h1><span class="az">Tarot terapêutico</span></h1>
  <p class="sub">Quando as cartas não servem para adivinhar, mas para se ouvir a si mesmo(a).</p></section>
  <section class="cartao texto">
    <p>O tarot terapêutico é uma maneira de usar as cartas virada para dentro. Em vez de perguntar o que o futuro reserva, pergunta-se o que a situação de hoje mostra sobre quem a vive. As 78 cartas do Tarot são imagens antigas de momentos humanos: começos, perdas, escolhas, esperas, reencontros. Quando uma delas aparece, dá forma a uma coisa que muitas vezes se sente mas ainda não se disse.</p>
    <p>É por isso que tanta gente sai de uma leitura com a sensação de ter sido compreendida. Não porque as cartas adivinharam, mas porque ajudaram a pôr em palavras o que já estava lá.</p>
    <h2>Como funciona uma leitura de autoconhecimento</h2>
    <ul>
      <li><b>Uma pergunta sobre si.</b> Começa-se por aquilo que quer compreender: um padrão que se repete, uma decisão, uma fase que custa a fechar.</li>
      <li><b>As cartas como espelho.</b> Cada carta é lida como uma pergunta, não como uma sentença. O que vê na imagem? Onde é que isso já aconteceu na sua vida?</li>
      <li><b>Um gesto no fim.</b> A leitura acaba com algo concreto para fazer nos dias seguintes, por pequeno que seja. O Tarot aponta; o passo é seu.</li>
    </ul>
    <h2>As perguntas que as cartas fazem</h2>
    <p>No tarot terapêutico, cada arcano traz uma pergunta. Alguns exemplos:</p>
    <div class="perfil">{"".join(f'<div><b><a href="{u}">{e(n)}</a></b>{e(q)}</div>' for n, u, q in CARTAS)}</div>
    <p>Pode conhecer o significado de cada uma nos <a href="/arcanos">22 Arcanos Maiores</a>, ou tirar uma carta agora no <a href="/tarot-gratis">Tarot Grátis</a> e fazer-lhe a sua pergunta.</p>
    <h2>O que o Tarot não substitui</h2>
    <p>O tarot terapêutico é uma leitura simbólica de reflexão. Não é uma terapia no sentido clínico, não faz diagnósticos e <b>não substitui acompanhamento psicológico, psiquiátrico ou médico</b>. Se está a passar por um momento de sofrimento intenso, o primeiro passo é falar com um profissional de saúde. O Tarot pode ser um apoio ao lado desse caminho, nunca no lugar dele.</p>
    <p style="text-align:center"><a class="cta" href="/consulta-de-tarot-online">Marcar uma leitura com o Mestre Alberto</a></p>
  </section>
  <section class="cartao texto"><h2>Perguntas frequentes</h2>
    {"".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in FAQ)}
  </section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/consulta-de-tarot-online">Consulta de Tarot online</a><a href="/arcanos">Os 22 Arcanos Maiores</a><a href="/tarot-gratis">Tarot Grátis</a><a href="/numerologia-2027">O seu Ano Pessoal 2027</a></div></section>"""

ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Article", "headline": TITULO, "description": DESC, "image": f"{SITE}/og-image.jpg", "inLanguage": "pt",
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"},
     "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE},
     "datePublished": "2026-11-27", "dateModified": "2026-11-27", "mainEntityOfPage": URL},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
extra = """<style>
.texto h3 { font-family: var(--serifa); font-size: 1.2rem; color: var(--ouro); margin: 1rem 0 .2rem; }
.texto ul { font-family: var(--serifa); font-size: 1.08rem; color: var(--lavanda); padding-left: 1.2rem; } .texto li { margin: .4rem 0; }
.perfil div { text-align: left; font-family: var(--serifa); font-size: 1.05rem; color: var(--lavanda); } .perfil div b { margin-bottom: .2rem; }
.perfil div b a { color: var(--ouro); text-decoration: none; }
</style>"""
pagina = f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(TITULO)}</title>
<meta name="description" content="{e(DESC)}" />

<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{URL}" />
<meta property="og:title" content="{e(TITULO)}" />
<meta property="og:description" content="{e(DESC)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:image" content="{SITE}/og-image.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{ESTILO}
{extra}
</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
  {corpo}
{CASA}
{FIM}"""
open("tarot-terapeutico.html", "w", encoding="utf-8").write(pagina)
print("tarot-terapeutico.html")
