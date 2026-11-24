#!/usr/bin/env python3
"""Página /codigos-de-grabovoi (24/11/2026, pedido dele pelo Telegram, depois de um TikTok com 156 mil visualizações
sobre os «números de Grabovoi»: «avança com a página»).
Linha da página: explicar com verdade o que são, de onde vêm, quem foi Grabovoi e o que se sabe (e não se sabe) sobre o efeito.
Nada de promessas de cura, de dinheiro ou de resultados; uso só simbólico, como foco de intenção.
Molde: lendas-de-coimbra-gerar.py (head, FAQ visível + FAQPage, vip-faixa, vivo.js, rodapé); o <style> é o de numerologia.html.
Correr na pasta do repositório: python3 codigos-de-grabovoi-gerar.py"""
import html, json, os, re
R = os.path.dirname(os.path.abspath(__file__)); os.chdir(R)
SITE = "https://genialtarot.com"
SLUG = "codigos-de-grabovoi"
TITULO = "Códigos de Grabovoi: o que são, se funcionam e a história real"
DESC = ("Os números de Grabovoi, como o 520 e o 5197148, explicados com verdade: de onde vêm, quem foi Grigori Grabovoi, "
        "se funcionam e como usá-los sem ilusões.")
HOJE = "2026-11-24"
E = html.escape

INTRO = ['Nas redes sociais circulam listas de números com nomes de promessa: o 520 para o «dinheiro inesperado», o 5197148 para «tudo é possível». '
 'Chamam-lhes códigos ou sequências de Grabovoi, e há quem os repita em voz alta, os escreva na mão ou os ponha no fundo do telemóvel.',
 'Muita gente chega aqui a perguntar se funcionam. Nesta página encontra o que são, de onde vêm, quem foi o homem que lhes deu o nome e o que se pode, '
 'com honestidade, fazer com eles.']

SECCOES = [
 ('o-que-sao', 'O que são os códigos de Grabovoi',
  ['São sequências de algarismos, umas curtas e outras com sete, nove ou mais números, a que se atribui um efeito: atrair dinheiro, trazer paz, resolver um problema. '
   'A ideia, tal como é apresentada, é que cada sequência «sintoniza» a pessoa com aquilo que deseja, desde que se concentre nela, a diga ou a escreva.',
   'Não são <a href="/numerologia">numerologia</a>. A numerologia parte da sua data de nascimento e do seu nome para descrever ciclos e tendências da sua vida. '
   'Os códigos de Grabovoi são listas fixas, iguais para toda a gente, cada uma com o seu «para quê».']),
 ('quem-foi', 'Quem foi Grigori Grabovoi',
  ['Grigori Grabovoi nasceu em 1963 no Cazaquistão, então parte da União Soviética, e estudou mecânica aplicada na Universidade de Tashkent. '
   'Nos anos 90, já na Rússia, começou a apresentar-se como homem de poderes paranormais e curador, e publicou livros com sequências de números que, segundo ele, ajudavam a recuperar o corpo pela concentração.',
   'Em 2004, depois do massacre da escola de Beslan, em que morreram centenas de pessoas, muitas delas crianças, anunciou que era capaz de ressuscitar os mortos. '
   'Mães que tinham perdido os filhos denunciaram-no por lhes ter cobrado dinheiro com essa promessa.',
   'Foi preso em 2006 e, em 2008, um tribunal de Moscovo condenou-o a 11 anos de prisão por burla. A pena foi depois reduzida e ele saiu em liberdade condicional em 2010. '
   'Por isso, quando ouvir que «esteve 11 anos preso porque havia filas à porta dele», saiba que os 11 anos foram a pena, não o tempo que cumpriu, e que a razão foi a burla.']),
 ('os-mais-falados', 'Os números mais falados nas redes',
  ['Estas são as sequências que mais aparecem nos vídeos e nas publicações, com o significado que essas listas lhes dão:',
   '<ul><li><b>520</b>: «dinheiro inesperado»;</li><li><b>5197148</b>: «tudo é possível»;</li><li><b>318 798</b>: «aumento do dinheiro»;</li>'
   '<li><b>741</b>: muito partilhado, com significados que mudam de lista para lista.</li></ul>',
   'As listas não coincidem entre si, e não é possível confirmar que todas estas sequências saíram dos livros do próprio Grabovoi. '
   'Muitas foram acrescentadas ou reinterpretadas ao passar de site em site e de vídeo em vídeo.']),
 ('funcionam', 'Os códigos de Grabovoi funcionam?',
  ['Não há nenhum estudo que mostre que uma sequência de números traga dinheiro, cure uma doença ou mude um acontecimento. As afirmações de que «está provado» não têm fonte.',
   'O que se observa é outra coisa, que acontece com qualquer prática de concentração: parar uns minutos, pensar com clareza no que se deseja e repetir uma intenção '
   'pode acalmar e ajudar a pessoa a agir com mais foco. Esse efeito vem da atenção que se dá ao assunto, não dos algarismos em si.',
   'Há um cuidado que não se pode esquecer: nenhum número trata a ansiedade, a depressão ou qualquer doença. Se está a passar por isso, fale com o seu médico ou com um psicólogo. '
   'E desconfie de quem lhe vende «códigos personalizados» com promessas de resultado.']),
 ('como-usar', 'Se quiser usá-los, faça-o com os pés na terra',
  ['Se gosta da ideia, use o número como usaria uma oração curta ou uma afirmação: um ponto de foco, não um feitiço. '
   'Escolha um, diga-o devagar durante um ou dois minutos e, no fim, escreva uma coisa concreta que pode fazer hoje por aquilo que pediu.',
   'É esse passo concreto que muda alguma coisa. O número é só o lembrete. Se procura uma forma de olhar para os seus números com sentido pessoal, '
   'a <a href="/numerologia">numerologia</a> parte da sua própria data de nascimento, e o <a href="/numerologia-2027">seu ano de 2027</a> pode ser calculado aqui no site.'])]

FAQ = [('O que são os códigos de Grabovoi?',
  'São sequências de números, como o 520 ou o 5197148, a que as listas das redes sociais atribuem um efeito, por exemplo atrair dinheiro ou abrir caminhos. '
  'O nome vem de Grigori Grabovoi, um russo que nos anos 90 publicou livros com sequências de números para concentração.'),
 ('Os números de Grabovoi funcionam?',
  'Não há nenhum estudo que o mostre. Concentrar-se num número pode acalmar e ajudar a focar a intenção, como uma afirmação, mas o efeito vem da atenção que se dá ao assunto, '
  'não do número. Nenhum código substitui o médico nem garante dinheiro.'),
 ('O que significa o código 520?',
  'Nas listas que circulam nas redes, o 520 aparece como o código do «dinheiro inesperado». É um significado atribuído por essas listas e não um resultado comprovado.'),
 ('Porque foi Grabovoi preso?',
  'Por burla. Depois do massacre de Beslan, em 2004, prometeu a mães que tinham perdido os filhos que os podia ressuscitar e cobrou-lhes dinheiro. '
  'Foi condenado em 2008 a 11 anos de prisão, a pena foi reduzida e saiu em liberdade condicional em 2010.'),
 ('Os códigos de Grabovoi são numerologia?',
  'Não. A numerologia calcula números a partir da sua data de nascimento e do seu nome e lê-os como ciclos da sua vida. '
  'Os códigos de Grabovoi são listas fixas, iguais para toda a gente.')]

estilo = re.search(r"<style>.*?</style>", open("numerologia.html", encoding="utf-8").read(), re.S).group(0)
estilo = estilo.replace("</style>", """.indice { display: flex; flex-wrap: wrap; gap: .45rem; justify-content: center; margin: .2rem 0 0; }
.indice a { text-decoration: none; font-size: .88rem; font-weight: 700; color: var(--texto); border: 1px solid var(--borda); background: var(--vidro); border-radius: 999px; padding: .4rem .85rem; }
.indice a:hover { border-color: var(--ouro); }
.texto h2[id] { scroll-margin-top: 1rem; }
.texto ul { margin: .4rem 0 .9rem 1.2rem; } .texto li { margin: .25rem 0; }
.aviso { margin: .9rem 0 0; padding: .85rem 1rem; border-radius: 1rem; background: oklch(0.85 0.13 88 / .08); border: 1px solid oklch(0.85 0.13 88 / .32); font-size: .92rem; }
</style>""")

URL = f"{SITE}/{SLUG}"
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Article", "headline": TITULO, "description": DESC, "image": {"@type": "ImageObject", "url": f"{SITE}/og-image.jpg"}, "inLanguage": "pt",
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"},
     "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": f"{SITE}/", "logo": {"@type": "ImageObject", "url": f"{SITE}/og-image.jpg"}},
     "mainEntityOfPage": URL, "datePublished": HOJE, "dateModified": HOJE,
     "about": [{"@type": "Person", "name": "Grigori Grabovoi"}, {"@type": "Thing", "name": "Códigos de Grabovoi"}, {"@type": "Thing", "name": "Numerologia"}]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Numerologia", "item": f"{SITE}/numerologia"},
        {"@type": "ListItem", "position": 3, "name": "Códigos de Grabovoi", "item": URL}]}]}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", r)}} for q, r in FAQ]}

def par(x):
    return x if x.startswith("<ul") else f"<p>{x}</p>"

corpo = "".join(f"<p>{x}</p>" for x in INTRO)
corpo += '<nav class="indice" aria-label="Nesta página">' + "".join(f'<a href="#{a}">{E(t)}</a>' for a, t, _ in SECCOES) + "</nav>"
for a, t, ps in SECCOES:
    corpo += f'<h2 id="{a}">{E(t)}</h2>' + "".join(par(x) for x in ps)
corpo += ('<p class="aviso">⚠️ Conteúdo informativo. Os códigos de Grabovoi não têm efeito comprovado e não substituem o médico, o psicólogo nem '
          'qualquer outro profissional.</p>')

faq_html = ('<section class="faq-genial" style="max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6">'
            '<h2 style="margin-top:0">Perguntas frequentes sobre os códigos de Grabovoi</h2>'
            + "".join(f'<h3 style="font-size:1.05rem;margin:1rem 0 .3rem">{E(q)}</h3><p style="margin:0">{r}</p>' for q, r in FAQ) + "</section>")

pagina = f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{E(TITULO)}</title>
<meta name="description" content="{E(DESC)}" />

<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{URL}" />
<meta property="og:title" content="{E(TITULO)}" />
<meta property="og:description" content="{E(DESC)}" />
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
{estilo}
<script type="application/ld+json">
{json.dumps(faq_ld, ensure_ascii=False)}
</script>
</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/numerologia"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>Numerologia</a>
  </header>
  <section class="heroi">
    <h1><span class="az">Códigos de Grabovoi</span></h1>
    <p class="sub">Os números de Grabovoi explicados com verdade: o que são, de onde vêm e o que se pode esperar deles, pelo Mestre Alberto.</p>
  </section>
  <section class="cartao texto">{corpo}</section>
  <section class="cartao" style="text-align:center"><h2>Os números que falam de si</h2><div class="ligas"><a href="/numerologia">🔢 Numerologia</a><a href="/numerologia-2027">📅 O seu Ano 2027</a><a href="/os-72-anjos">👼 Os 72 Anjos</a><a href="/rezas-e-oracoes">🙏 Rezas e Orações</a><a href="/esoterismo">✨ Esoterismo</a></div>
    <a class="cta" href="https://wa.me/351914920427">Falar com o Mestre Alberto</a>
  </section>
{faq_html}
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="/privacidade">Política de Privacidade</a> · <a href="/termos">Termos de Serviço</a>
</footer>
</div>
<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""
open(f"{SLUG}.html", "w", encoding="utf-8").write(pagina)
print(SLUG + ".html", len(pagina), "bytes;", len(TITULO), "car. no título;", len(DESC), "na descrição")
