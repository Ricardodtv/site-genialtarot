#!/usr/bin/env python3
"""Página /lendas-de-coimbra (22/11/2026, Radar «lendas de coimbra» +38400 % em Portugal).
Molde: lendas-de-lisboa-gerar.py (o mesmo <style> de lendas-brasileiras.html, a mesma ordem: topo, texto, «Mais histórias», FAQ).
Em cada lenda, primeiro o que conta a tradição e depois o que está documentado (classe .hist).
A imagem de destaque (LC01) entra pelo imagens-destaque.py e o destaque da casa pelo destaque-casa.py, no pre-commit.
Correr na pasta do repositório: python3 lendas-de-coimbra-gerar.py"""
import html, json, os, re
R = os.path.dirname(os.path.abspath(__file__)); os.chdir(R)
SITE = "https://genialtarot.com"
SLUG = "lendas-de-coimbra"
TITULO = "Lendas de Coimbra: Pedro e Inês, a Cabra e o que é verdade"
DESC = ("A Fonte das Lágrimas de Pedro e Inês, a Cabra da Universidade, o brasão de Cindazunda e a Rainha Santa: "
        "as lendas de Coimbra e o que a história confirma.")
IMG_OG = f"{SITE}/lendas-de-coimbra-fonte-das-lagrimas-og.jpg"
E = html.escape

INTRO = ['Coimbra foi capital do reino durante mais de um século e é cidade universitária desde 1537. Juntou lendas de reis e de santos, e outras que os estudantes foram inventando e passando de curso em '
 'curso.',
 'Em cada lenda encontra primeiro o que conta a tradição e, a seguir, o que os documentos permitem afirmar. Onde não há provas, dizemos que é tradição.']

# (âncora, título, [parágrafos da lenda], [parágrafos da história]) — o HTML das ligações vai já no texto
LENDAS = [('pedro-e-ines',
  'Pedro e Inês e a Fonte das Lágrimas',
  ['Inês de Castro chegou a Portugal como dama de D. Constança, a mulher do infante D. Pedro, e o infante apaixonou-se por ela. Depois de Constança morrer, Pedro e Inês viveram juntos em Coimbra e '
   'tiveram filhos. O rei D. Afonso IV, pai de Pedro, temia a influência dos irmãos de Inês, nobres castelhanos, e mandou matá-la.',
   'Conta a lenda que Inês foi morta junto a uma fonte, no sítio onde os dois se encontravam, e que as lágrimas que chorou fizeram nascer a Fonte das Lágrimas. As manchas vermelhas nas pedras do '
   "fundo seriam o sangue dela, que nunca mais saiu. Camões pôs esta versão em verso n'Os Lusíadas:",
   '<blockquote>«As filhas do Mondego a morte escura / Longo tempo chorando memoraram, / E, por memória eterna, em fonte pura / As lágrimas choradas transformaram.»</blockquote>',
   'Quando subiu ao trono, diz ainda a lenda, Pedro mandou desenterrar Inês, sentá-la num trono, coroá-la rainha e obrigar a corte a beijar-lhe a mão.'],
  ['Inês foi morta em Coimbra a 7 de janeiro de 1355, por ordem de D. Afonso IV. Pedro revoltou-se contra o pai e, já rei, declarou em Cantanhede, em 1360, que tinha casado com ela em segredo. No '
   'ano seguinte vingou-se de dois dos executores, Pêro Coelho e Álvaro Gonçalves, a quem mandou arrancar o coração; o terceiro, Diogo Lopes Pacheco, fugiu. Fernão Lopes conta tudo isto na crónica '
   'de D. Pedro, e conta também a trasladação solene do corpo de Inês de Coimbra para o mosteiro de Alcobaça, onde os túmulos dos dois estão até hoje.',
   'A coroação do cadáver e o beija-mão não aparecem em Fernão Lopes. Vêm de autores posteriores, e os historiadores tratam-nos como lenda, embora Camões já chamasse a Inês «aquela que depois de ser '
   'morta foi Rainha».',
   'A Fonte das Lágrimas existe e fica na Quinta das Lágrimas, na margem esquerda do rio, perto de Santa Clara. O nome da quinta só se fixou no século XVIII, e não há prova de que Inês tenha morrido '
   'ali. O vermelho das pedras é uma alga, a Hildenbrandia rivularis, que cresce agarrada às pedras da nascente.']),
 ('rainha-santa',
  'A Rainha Santa e o Milagre das Rosas',
  ['A outra grande lenda de Coimbra é a da Rainha Santa Isabel. Conta-se que levava pão escondido no regaço para dar aos pobres e que, apanhada pelo rei D. Dinis, abriu o manto e o pão tinha-se '
   'transformado em rosas, em pleno janeiro. A história completa, com as várias versões, está no <a href="/lenda-milagre-das-rosas">Milagre das Rosas</a>.'],
  ['Isabel de Aragão casou com D. Dinis em 1282 e, viúva, viveu os últimos anos junto ao mosteiro de Santa Clara, que tinha mandado reconstruir na margem esquerda do Mondego. Morreu em Estremoz em '
   '1336, foi sepultada em Santa Clara e canonizada em 1625. As cheias do rio iam afogando o velho mosteiro, e em 1677 o corpo foi levado para Santa Clara-a-Nova, mais acima no monte, onde está '
   'hoje. É a padroeira de Coimbra, e as Festas da Rainha Santa, com a procissão da imagem pela cidade, fazem-se em julho, de dois em dois anos.']),
 ('cabra',
  'A Cabra, o sino da Universidade',
  ['Em Coimbra, o sino da torre da Universidade tem nome: Cabra. Há quem diga que o nome vem do som, rouco como um balido, e há quem jure que foram os estudantes a amaldiçoá-lo, porque era ele que '
   'os mandava para as aulas e, à noite, para casa. O sino maior, de som mais grave, ficou a ser o Cabrão.',
   'Segundo a tradição da praxe, o caloiro apanhado na rua depois de a Cabra tocar à noite podia cair nas mãos das trupes, grupos de estudantes mais velhos que andavam pela cidade a fazer cumprir as '
   'regras académicas. Conta-se também que o relógio da Universidade andava de propósito um quarto de hora atrasado em relação ao da cidade, e é essa a origem que muitos dão ao quarto de hora '
   'académico, a tolerância antes de as aulas começarem.'],
  ['A torre foi construída entre 1728 e 1733, no Paço das Escolas, e o projeto é atribuído ao arquiteto italiano António Canevari. Tem quatro sinos, e a Cabra marcou durante séculos o horário da '
   'Universidade e de boa parte da cidade. A tolerância do quarto de hora académico existe; o relógio atrasado de propósito é a explicação que a tradição repete. No mesmo edifício conserva-se a '
   'antiga prisão académica, onde estudantes e funcionários podiam ser presos por decisão da própria Universidade, que teve foro próprio até ao século XIX.',
   'A Universidade nasceu em Lisboa em 1290, andou entre as duas cidades e instalou-se de vez em Coimbra em 1537. Desde 2013, a Universidade de Coimbra, Alta e Sofia, é Património Mundial da '
   'UNESCO.']),
 ('brasao',
  'Cindazunda e o brasão de Coimbra',
  ['O brasão de Coimbra mostra uma donzela coroada dentro de uma taça de ouro, entre um leão e uma serpe alada. A lenda que o explica passa-se no século V, quando Alanos, Suevos e Visigodos '
   'disputavam a Lusitânia.',
   'Ataces, rei dos Alanos, tomou a cidade. Hermenerico, rei dos Suevos, veio cercá-la, perdeu e fugiu com Ataces no encalço. Para fazer as pazes, ofereceu-lhe a mão da filha, a princesa Cindazunda. '
   'A taça é a boda, o leão é o emblema de Ataces e a serpe o de Hermenerico. Diz-se ainda que Ataces, já casado, mandou reconstruir a cidade.'],
  ['Ataces e Hermenerico (Hermerico, nos documentos) existiram. O bispo Hidácio, que escreveu uma crónica no século V, fala dos dois: dos Alanos instalados na Lusitânia depois de 411 e dos Suevos, '
   'que se fixaram no noroeste da Península. Cindazunda não aparece nessa crónica. O casamento ganhou forma com Frei Bernardo de Brito, na Monarquia Lusitana, publicada a partir de 1597, uma obra '
   'que já no seu tempo misturava documentos com invenção. O brasão da cidade, com estas figuras, foi fixado oficialmente em 1930.',
   'A cidade é bem mais antiga do que a lenda. No alto do monte ficava Aeminium, cidade romana, e o criptopórtico do fórum, com as suas galerias de arcos, conserva-se debaixo do Museu Nacional '
   'Machado de Castro. O nome Coimbra veio de Conímbriga, a cidade romana a uns 15 km dali: quando os bispos de Conímbriga se mudaram para Aeminium, no fim do século VI, o nome mudou-se com eles.']),
 ('torre-de-anto',
  'A Torre de Anto, a torre do poeta',
  ['Na Alta, encostada ao que resta da muralha medieval, há uma torre estreita a que toda a gente chama Torre de Anto. Anto era o nome que o poeta António Nobre dava a si próprio. Conta-se em '
   'Coimbra que ali viveu sozinho e triste, a escrever versos enquanto as guitarras dos estudantes passavam na rua, e que a torre lhe ficou com o nome e com a melancolia.'],
  ['A torre fazia parte da muralha da cidade e ainda guarda um pedaço do caminho de ronda. Também foi conhecida como torre do Prior do Ameal. Foi adaptada a casa no tempo de D. Manuel e voltou a '
   'mudar no século XIX, quando lhe abriram janelas. António Nobre, estudante de Direito, viveu lá entre 1888 e 1890. Não acabou o curso em Coimbra: foi para Paris, onde publicou o livro Só, em '
   '1892, com muitos poemas sobre a cidade. A torre é monumento nacional desde 1935 e hoje acolhe o Núcleo da Guitarra e do Fado de Coimbra.']),
 ('sereia',
  'A Sereia que é um tritão',
  ['Se perguntar em Coimbra pelo Parque de Santa Cruz, talvez demorem a perceber. Pelo Jardim da Sereia, mandam-no logo para trás da Praça da República. O nome, diz-se, vem da sereia da fonte, lá no '
   'alto da escadaria.'],
  ['A estátua da fonte é um tritão barbudo, com dois golfinhos, e a alcunha de sereia pegou de tal forma que passou a ser o nome do jardim. O parque é do século XVIII: fazia parte da cerca do '
   'mosteiro de Santa Cruz e foi arranjado no tempo de Frei Gaspar da Encarnação, que reformou o mosteiro entre 1723 e 1752. Na igreja de Santa Cruz estão sepultados os dois primeiros reis de '
   'Portugal, D. Afonso Henriques e D. Sancho I.'])]

FECHO = ('Há mais lendas portuguesas no site com a mesma separação entre tradição e história: as <a href="/lendas-de-lisboa">Lendas de Lisboa</a>, de Ulisses aos corvos de São Vicente, a <a '
 'href="/lenda-padeira-de-aljubarrota">Padeira de Aljubarrota</a> e a <a href="/lenda-moura-encantada">Moura Encantada</a>. Estão todas reunidas em <a href="/historias-e-lendas">Histórias e '
 'Lendas</a>.')

FAQ = [('Quais são as lendas de Coimbra mais conhecidas?',
  'As mais contadas são a de Pedro e Inês e da Fonte das Lágrimas, a do Milagre das Rosas da Rainha Santa Isabel, a do brasão com a princesa Cindazunda, a da Cabra, o sino da Universidade, a da '
  'Torre de Anto e a do Jardim da Sereia.'),
 ('A Fonte das Lágrimas existe mesmo?',
  'Existe, na Quinta das Lágrimas, na margem esquerda do Mondego. A lenda diz que nasceu das lágrimas de Inês de Castro e que o vermelho das pedras é o sangue dela. O vermelho vem de uma alga, e não '
  'há prova de que Inês tenha sido morta naquele sítio.'),
 ('Porque se chama Cabra o sino da Universidade de Coimbra?',
  'Foi a alcunha que os estudantes lhe deram. Uns dizem que é pelo som, outros que era a maneira de o amaldiçoar, porque tocava para as aulas e para o recolher. A torre foi construída entre 1728 e '
  '1733 e tem quatro sinos; o maior chama-se Cabrão.'),
 ('Inês de Castro foi coroada depois de morta?',
  'Não há documentos que o provem. Fernão Lopes, o cronista que conta a vingança de D. Pedro e a trasladação do corpo para Alcobaça, não fala de coroação nem de beija-mão. Essa parte é lenda, e foi '
  'a que ficou na memória, também por causa de Camões.'),
 ('O que significa o brasão de Coimbra?',
  'Segundo a lenda, a donzela é a princesa Cindazunda, a taça é o casamento dela com Ataces, rei dos Alanos, o leão é o emblema de Ataces e a serpe o do pai dela, Hermenerico, rei dos Suevos. Os '
  'dois reis existiram no século V; a princesa e o casamento só aparecem em autores do fim do século XVI.')]

# o <style> é o da página irmã, para as páginas de lendas ficarem iguais
irma = open("lendas-brasileiras.html", encoding="utf-8").read()
estilo = re.search(r"<style>.*?</style>", irma, re.S).group(0)
estilo = estilo.replace("</style>", """.indice { display: flex; flex-wrap: wrap; gap: .45rem; justify-content: center; margin: .2rem 0 0; }
.indice a { text-decoration: none; font-size: .88rem; font-weight: 700; color: var(--texto); border: 1px solid var(--borda); background: var(--vidro); border-radius: 999px; padding: .4rem .85rem; }
.indice a:hover { border-color: var(--ouro); }
.texto h2[id] { scroll-margin-top: 1rem; }
.hist { margin: .9rem 0 1.2rem; padding: .85rem 1rem; border-radius: 1rem; background: oklch(0.85 0.13 88 / .08); border: 1px solid oklch(0.85 0.13 88 / .32); }
.hist .eti { display: block; font-size: .72rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; color: var(--ouro); margin-bottom: .3rem; }
.hist p { margin: 0 0 .5rem; } .hist p:last-child { margin-bottom: 0; }
.lenda-eti { display: block; font-size: .72rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; color: var(--suave); margin: .2rem 0 .1rem; }
.texto blockquote { margin: .6rem 0 .9rem; padding: .2rem 0 .2rem 1rem; border-left: 3px solid var(--ouro); font-style: italic; }
</style>""")

URL = f"{SITE}/{SLUG}"
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Article", "headline": TITULO, "description": DESC, "image": {"@type": "ImageObject", "url": IMG_OG}, "inLanguage": "pt",
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"},
     "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": f"{SITE}/", "logo": {"@type": "ImageObject", "url": f"{SITE}/og-image.jpg"}},
     "mainEntityOfPage": URL, "datePublished": "2026-11-22", "dateModified": "2026-11-22",
     "about": [{"@type": "Place", "name": "Coimbra"}, {"@type": "Thing", "name": "Lendas portuguesas"},
               {"@type": "Person", "name": "Inês de Castro"}, {"@type": "Person", "name": "Isabel de Aragão, Rainha Santa"}]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Histórias e Lendas", "item": f"{SITE}/historias-e-lendas"},
        {"@type": "ListItem", "position": 3, "name": "Lendas de Coimbra", "item": URL}]}]}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", r)}} for q, r in FAQ]}

def par(x):
    return x if x.startswith("<blockquote") else f"<p>{x}</p>"

corpo = "".join(f"<p>{x}</p>" for x in INTRO)
corpo += '<nav class="indice" aria-label="As lendas desta página">' + "".join(f'<a href="#{a}">{E(t)}</a>' for a, t, _, _ in LENDAS) + "</nav>"
for a, t, lenda, hist in LENDAS:
    corpo += f'<h2 id="{a}">{E(t)}</h2><span class="lenda-eti">O que conta a lenda</span>' + "".join(par(x) for x in lenda)
    corpo += '<div class="hist"><span class="eti">O que diz a história</span>' + "".join(par(x) for x in hist) + "</div>"
corpo += f"<h2>Mais lendas de Portugal</h2><p>{FECHO}</p>"

faq_html = ('<section class="faq-genial" style="max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6">'
            '<h2 style="margin-top:0">Perguntas frequentes sobre as lendas de Coimbra</h2>'
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
<meta property="og:image" content="{IMG_OG}" />
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
    <a class="backlink" href="/historias-e-lendas"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>Histórias e Lendas</a>
  </header>
  <section class="heroi">
    <h1><span class="az">Lendas de Coimbra</span></h1>
    <p class="sub">Seis lendas da cidade do Mondego, da Fonte das Lágrimas à Cabra da Universidade, com o que é tradição e o que é história, contadas pelo Mestre Alberto.</p>
  </section>
  <section class="cartao texto">{corpo}</section>
  <section class="cartao" style="text-align:center"><h2>Mais histórias</h2><div class="ligas"><a href="/historias-e-lendas">📜 Lendas de Portugal</a><a href="/lendas-de-lisboa">🏰 Lendas de Lisboa</a><a href="/lenda-milagre-das-rosas">🌹 O Milagre das Rosas</a><a href="/lenda-padeira-de-aljubarrota">🍞 A Padeira de Aljubarrota</a><a href="/lenda-moura-encantada">🌊 A Moura Encantada</a><a href="/lendas-brasileiras">🇧🇷 Lendas Brasileiras</a></div>
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
