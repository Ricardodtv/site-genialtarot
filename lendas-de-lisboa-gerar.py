#!/usr/bin/env python3
"""Página /lendas-de-lisboa (16/11/2026, O-475, Radar «lendas de lisboa» a subir em Portugal).
Molde: lendas-brasileiras.html (o mesmo <style>, a mesma ordem: topo, texto, «Mais histórias», FAQ).
Em cada lenda, primeiro o que conta a tradição e depois o que está documentado (classe .hist).
A imagem de destaque (LX01) entra pelo imagens-destaque.py e o destaque da casa pelo destaque-casa.py, no pre-commit.
Correr na pasta do repositório: python3 lendas-de-lisboa-gerar.py"""
import html, json, os, re
R = os.path.dirname(os.path.abspath(__file__)); os.chdir(R)
SITE = "https://genialtarot.com"
SLUG = "lendas-de-lisboa"
TITULO = "Lendas de Lisboa: as histórias da cidade e o que é verdade"
DESC = ("Ulisses e Olisipo, os corvos de São Vicente, Martim Moniz, Santo António e a cadeira de São Gens: "
        "as lendas de Lisboa e o que a história confirma.")
IMG_OG = f"{SITE}/lendas-de-lisboa-corvos-sao-vicente-og.jpg"
E = html.escape

INTRO = [
    "Lisboa tem mais de dois mil anos de história, e quase todas as épocas lhe deixaram uma lenda. Algumas vêm de autores romanos; a maior parte nasceu na Idade Média e continua a contar-se nos bairros, sobretudo nas festas de junho.",
    "Em cada lenda encontra primeiro o que conta a tradição e, a seguir, o que os documentos e a arqueologia permitem afirmar. Onde não há provas, dizemos que é tradição.",
]

# (âncora, título, [parágrafos da lenda], [parágrafos da história]) — o HTML das ligações vai já no texto
LENDAS = [
 ("ulisses", "Ulisses e a fundação de Olisipo",
  ["Conta a tradição que Ulisses, o herói grego da Odisseia, entrou no Tejo durante os dez anos que levou a voltar a casa depois da guerra de Troia. Gostou tanto do sítio que fundou ali uma cidade com o seu nome, Ulisseia, que com o tempo passou a Olisipo e depois a Lisboa.",
   "Há uma versão mais romanesca. A terra era governada por Ofiusa, uma rainha metade mulher e metade serpente, que se apaixonou pelo navegador. Quando ele partiu às escondidas, ela seguiu-o pela costa, e as voltas do seu corpo a bater no chão levantaram as colinas onde a cidade assenta."],
  ["A ligação a Ulisses é antiga: no século III, o autor latino Solino já escrevia que Olisipo tinha sido fundada por ele. É uma explicação erudita, feita a partir da parecença dos nomes. O nome Olisipo é anterior aos romanos e a sua origem continua por esclarecer; uma das hipóteses que os linguistas discutem aponta para o fenício.",
   "A arqueologia mostra que havia gente a viver no morro do castelo muito antes dos romanos e que os fenícios comerciavam ali pelo menos desde o século VIII antes de Cristo. Ofiusa também tem um fio real: Ophiussa, a terra das serpentes, era um dos nomes que os gregos davam ao extremo ocidental da Península, e aparece no poema Ora Maritima, de Avieno. A rainha serpente é acrescento posterior. Fernando Pessoa, no poema «Ulisses» da Mensagem, escreveu o verso que melhor resume esta lenda: «O mito é o nada que é tudo.»"]),

 ("corvos", "São Vicente e os corvos do brasão",
  ["São Vicente era diácono em Saragoça e morreu mártir em Valência, no ano de 304, durante a perseguição do imperador Diocleciano. Conta a tradição que o corpo foi atirado aos animais e que um corvo o guardou, a afastar os lobos e as aves de rapina.",
   "Mais tarde, cristãos que fugiam da invasão muçulmana levaram as relíquias de barco até ao cabo do Algarve que ficou com o nome do santo, o Cabo de São Vicente, e ali os corvos continuaram de guarda ao túmulo. Em 1173, D. Afonso Henriques mandou trazer o corpo para Lisboa. Diz a lenda que dois corvos acompanharam o barco a viagem inteira, um à proa e outro à popa, até a nau entrar no Tejo."],
  ["O martírio de Vicente em Valência é antigo e bem atestado: por volta do ano 400, o poeta Prudêncio já lhe dedicava um hino. Há relatos árabes do século XII sobre a igreja do cabo e os corvos que por lá andavam, e a trasladação das relíquias para Lisboa, em 1173, ficou registada num texto latino escrito na cidade pouco depois.",
   "Os dois corvos ficaram no brasão de Lisboa, sobre uma nau, e São Vicente é o padroeiro oficial da cidade, festejado a 22 de janeiro. A parte dos corvos a guiar o barco pertence à lenda."]),

 ("martim-moniz", "O Milagre de Ourique e Martim Moniz no cerco de 1147",
  ["A conquista de Lisboa começa, para os velhos cronistas, num milagre. Conta a tradição que na madrugada da batalha de Ourique, a 25 de julho de 1139, Cristo apareceu no céu a D. Afonso Henriques e lhe prometeu a vitória sobre cinco reis mouros. O príncipe venceu, foi aclamado rei pelos seus homens e pôs no escudo as cinco quinas, em memória das chagas de Cristo.",
   "Oito anos depois, no verão de 1147, o rei cercou Lisboa com a ajuda de cruzados ingleses, flamengos e alemães que iam a caminho da Terra Santa. Num dos ataques ao castelo, diz a lenda, um cavaleiro chamado Martim Moniz viu uma porta a fechar-se e atirou-se para o vão. Os defensores não a conseguiram fechar por causa do corpo dele, que ficou entalado entre as portadas, e os portugueses entraram por ali. A porta do castelo tem hoje o seu nome e um busto a lembrá-lo, e a praça onde começa a Mouraria também se chama Martim Moniz."],
  ["A batalha de Ourique está registada em anais da época, embora não se saiba ao certo onde foi travada. O milagre só aparece por escrito no século XV, e o documento do juramento do rei, que apareceu em Alcobaça no fim do século XVI, é tido como falso desde que Alexandre Herculano o contestou no século XIX.",
   "O cerco de Lisboa está entre os acontecimentos mais bem documentados do século XII português. Um dos cruzados que lá esteve escreveu uma longa carta em latim, conhecida como De expugnatione Lyxbonensi, que o conta quase dia a dia: começou no início de julho e a cidade rendeu-se em outubro, depois de meses de fome e de ataques com torres de assalto. Essa carta não fala de Martim Moniz nem da porta. Houve nobres com esse nome na época, mas o episódio só aparece em textos muito posteriores, e os historiadores tratam-no como lenda."]),

 ("santo-antonio", "Santo António, os peixes e os casamentos",
  ["Santo António nasceu em Lisboa e foi batizado com o nome de Fernando. Diz a tradição que nasceu numa casa junto à Sé, onde hoje está a Igreja de Santo António. Das histórias que se contam dele, há duas que toda a gente conhece.",
   "Na primeira, em Rimini, na Itália, ninguém o queria ouvir pregar. Foi então para a beira-mar falar aos peixes, e os peixes juntaram-se em filas, de cabeça fora de água, a escutá-lo. Na segunda, uma rapariga pobre não tinha dote para casar e pediu-lhe ajuda. O santo deu-lhe um papel escrito para levar a um comerciante, que o pôs na balança e lhe pagou em prata o que o papel pesava: deu exatamente para o dote. É por isso que as raparigas lhe pedem noivo e que em Lisboa lhe chamam santo casamenteiro."],
  ["Fernando nasceu em Lisboa entre 1190 e 1195. Foi cónego regrante de Santo Agostinho, primeiro em São Vicente de Fora e depois em Santa Cruz de Coimbra, e em 1220 entrou para os franciscanos, já com o nome de António. Pregou em Itália e em França, morreu perto de Pádua a 13 de junho de 1231 e foi canonizado no ano seguinte, um dos processos mais rápidos da história da Igreja.",
   "O sermão aos peixes vem de coleções de milagres escritas depois da sua morte, e foi dele que o padre António Vieira partiu para o Sermão de Santo António aos Peixes, pregado no Maranhão em 1654. A história do dote é tradição popular. Os casamentos de Santo António que a cidade organiza começaram nos anos 1950, e as marchas populares saíram à rua pela primeira vez em 1932."]),

 ("moura", "A moura do castelo e a Mouraria",
  ["Como em tantas terras de Portugal, também em Lisboa se conta que os mouros, ao deixarem a cidade, esconderam tesouros e deixaram filhas encantadas a guardá-los. No castelo e nas ruas apertadas da Mouraria, a moura aparece em noites de São João, a pentear os cabelos com um pente de ouro, à espera de quem lhe quebre o encanto.",
   "Quem a encontra tem de fazer o que ela pede sem medo e sem contar a ninguém. Se falhar, o ouro vira carvão e a moura fica presa por mais cem anos. Não há uma versão fixa: cada contador acrescenta o seu pormenor, e a mesma moura muda de fonte, de rua e de tesouro."],
  ["As mouras encantadas aparecem em lendas de norte a sul do país, e a de Lisboa é uma entre muitas. O fundo histórico está no bairro. Depois de 1147, os muçulmanos que ficaram na cidade tiveram de ir viver fora da muralha, na encosta norte do castelo, e em 1170 D. Afonso Henriques deu-lhes uma carta de foral que lhes garantia proteção e regras próprias. Esse bairro é a Mouraria, que guardou o nome até hoje."]),

 ("sao-gens", "A cadeira de São Gens, na Senhora do Monte",
  ["No alto da Graça, na Ermida de Nossa Senhora do Monte, há uma cadeira de pedra antiga a que chamam a cadeira de São Gens. A tradição diz que São Gens foi o primeiro bispo de Lisboa, morto pelos romanos por ser cristão, e que era ali que se sentava.",
   "Diz-se que, durante séculos, as grávidas de Lisboa subiam à ermida para se sentarem na cadeira e pedir um bom parto. Conta-se que até rainhas o fizeram."],
  ["A ermida existe desde a Idade Média e o miradouro ao lado é um dos pontos mais altos da cidade. A existência de São Gens não está provada: não há documentos romanos com o seu nome, e o primeiro bispo de Lisboa de que há registo seguro é Potâmio, no século IV. O costume das grávidas, esse, é tradição antiga da cidade."]),
]

FECHO = ('Se gosta destas histórias, há mais lendas portuguesas no site com o mesmo cuidado entre tradição e história: '
         'a <a href="/lenda-padeira-de-aljubarrota">Padeira de Aljubarrota</a>, que também tem a ver com a independência do reino, '
         'a <a href="/lenda-nazare-fuas-roupinho">Lenda da Nazaré</a>, com D. Fuas Roupinho, que combateu ao lado de D. Afonso Henriques, '
         'e a <a href="/lenda-moura-encantada">Moura Encantada</a>, na versão mais completa. Todas estão reunidas em '
         '<a href="/historias-e-lendas">Histórias e Lendas</a>.')

FAQ = [
 ("Quais são as lendas de Lisboa mais conhecidas?",
  "As mais contadas são a de Ulisses como fundador da cidade, a dos corvos de São Vicente que estão no brasão, a de Martim Moniz no cerco de 1147, as de Santo António, a da moura encantada do castelo e a da cadeira de São Gens, na Senhora do Monte."),
 ("Lisboa foi mesmo fundada por Ulisses?",
  "Não há nenhuma prova disso. A ideia já aparece no autor latino Solino, no século III, e nasceu da parecença entre os nomes Olisipo e Ulisses. A arqueologia mostra que o morro do castelo já era habitado antes dos romanos e que os fenícios lá comerciavam desde o século VIII antes de Cristo."),
 ("Porque há dois corvos no brasão de Lisboa?",
  "Por causa de São Vicente, o padroeiro oficial da cidade. Segundo a lenda, quando D. Afonso Henriques mandou trazer as relíquias do santo do Algarve para Lisboa, em 1173, dois corvos acompanharam o barco, um à proa e outro à popa. A trasladação está documentada; os corvos a guiar a nau são tradição."),
 ("Martim Moniz existiu?",
  "Houve nobres com esse nome no tempo de D. Afonso Henriques, mas o episódio da porta do castelo não aparece na carta do cruzado que descreveu o cerco de 1147. Só surge em textos muito posteriores, e os historiadores tratam-no como lenda."),
 ("Quem é o padroeiro de Lisboa?",
  "O padroeiro oficial é São Vicente, festejado a 22 de janeiro. Santo António, que nasceu em Lisboa, é o santo mais popular da cidade e a sua festa, a 13 de junho, é o ponto alto dos Santos Populares."),
]

# o <style> é o da página irmã, para as duas ficarem iguais
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
</style>""")

URL = f"{SITE}/{SLUG}"
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Article", "headline": TITULO, "description": DESC, "image": {"@type": "ImageObject", "url": IMG_OG}, "inLanguage": "pt",
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"},
     "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": f"{SITE}/", "logo": {"@type": "ImageObject", "url": f"{SITE}/og-image.jpg"}},
     "mainEntityOfPage": URL, "datePublished": "2026-11-16", "dateModified": "2026-11-16",
     "about": [{"@type": "Place", "name": "Lisboa"}, {"@type": "Thing", "name": "Lendas portuguesas"}]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Histórias e Lendas", "item": f"{SITE}/historias-e-lendas"},
        {"@type": "ListItem", "position": 3, "name": "Lendas de Lisboa", "item": URL}]}]}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]}

corpo = "".join(f"<p>{x}</p>" for x in INTRO)
corpo += '<nav class="indice" aria-label="As lendas desta página">' + "".join(f'<a href="#{a}">{E(t)}</a>' for a, t, _, _ in LENDAS) + "</nav>"
for a, t, lenda, hist in LENDAS:
    corpo += f'<h2 id="{a}">{E(t)}</h2><span class="lenda-eti">O que conta a lenda</span>' + "".join(f"<p>{x}</p>" for x in lenda)
    corpo += '<div class="hist"><span class="eti">O que diz a história</span>' + "".join(f"<p>{x}</p>" for x in hist) + "</div>"
corpo += f"<h2>Mais lendas de Portugal</h2><p>{FECHO}</p>"

faq_html = ('<section class="faq-genial" style="max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6">'
            '<h2 style="margin-top:0">Perguntas frequentes sobre as lendas de Lisboa</h2>'
            + "".join(f'<h3 style="font-size:1.05rem;margin:1rem 0 .3rem">{E(q)}</h3><p style="margin:0">{E(r)}</p>' for q, r in FAQ) + "</section>")

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
    <h1><span class="az">Lendas de Lisboa</span></h1>
    <p class="sub">Seis lendas da cidade, de Ulisses a Santo António, com o que é tradição e o que é história, contadas pelo Mestre Alberto.</p>
  </section>
  <section class="cartao texto">{corpo}</section>
  <section class="cartao" style="text-align:center"><h2>Mais histórias</h2><div class="ligas"><a href="/historias-e-lendas">📜 Lendas de Portugal</a><a href="/lenda-padeira-de-aljubarrota">🍞 A Padeira de Aljubarrota</a><a href="/lenda-nazare-fuas-roupinho">🐎 A Lenda da Nazaré</a><a href="/lenda-moura-encantada">🌊 A Moura Encantada</a><a href="/lenda-milagre-das-rosas">🌹 O Milagre das Rosas</a><a href="/lendas-brasileiras">🇧🇷 Lendas Brasileiras</a></div>
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
