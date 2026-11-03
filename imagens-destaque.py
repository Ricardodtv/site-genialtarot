#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Imagens de destaque das páginas (02/11/2026, pedido dele: imagens geradas por ele, com nomes e títulos otimizados para
o Google Imagens). Para cada página da lista IMAGENS:
  · põe a imagem logo a seguir ao bloco de topo (<section class="heroi"> ou <section class="hero">), entre as marcas
    <!-- img-destaque:inicio --> e <!-- img-destaque:fim --> (correr outra vez ATUALIZA, não duplica);
  · a imagem de partilha (og:image, Facebook/WhatsApp) passa a ser a da página, em JPG 1200×630, com og:image:alt;
  · um JSON-LD ImageObject (nome, legenda, autor, crédito) para o Google.
Corre no pre-commit (.git/hooks/pre-commit): se um gerador reescrever a página, a imagem volta a entrar no commit seguinte.

Imagem nova: o original (PNG/JPG do gerador) em ~/site-genialtarot-dados/imagens-originais/<CÓDIGO>.png e uma linha em
IMAGENS. `python3 imagens-destaque.py --converter` faz o <nome>.webp (1200 px) e o <nome>-og.jpg (1200×630).
    python3 ~/site-genialtarot/imagens-destaque.py              → aplica nas páginas (diz quais mudou)
    python3 ~/site-genialtarot/imagens-destaque.py --converter  → (re)faz os ficheiros de imagem a partir dos originais
"""
import json, os, re, sys, html
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
ORIG = "/home/ricardo/site-genialtarot-dados/imagens-originais"
SITE = "https://genialtarot.com"

# código, página, nome do ficheiro (o que o Google lê), texto alternativo, legenda
IMAGENS = [
    ("A01", "consulta-de-tarot-online", "consulta-de-tarot-online",
     "Consulta de tarot online: mãos do tarólogo a virar as cartas numa mesa de veludo azul, com velas e uma videochamada ao lado",
     "Consulta de tarot online com o Mestre Alberto: as cartas são lançadas ao vivo e a leitura faz-se por videochamada, chamada ou mensagem."),
    ("A02", "tarot-gratis", "tarot-gratis-online",
     "Tarot grátis online: três cartas de tarot sobre veludo azul, a do meio a brilhar com luz dourada",
     "Tarot grátis online: pense na sua pergunta e tire três cartas do baralho do Mestre Alberto."),
    ("A03", "horoscopo-semanal", "horoscopo-semanal-signos",
     "Horóscopo semanal dos signos: roda do zodíaco dourada com os 12 signos, astrolábio e agenda aberta sob um céu estrelado",
     "O horóscopo semanal dos 12 signos, de segunda a domingo, a partir do céu real da semana."),
    ("A04", "horoscopo-do-dia", "horoscopo-do-dia",
     "Horóscopo do dia: nascer do sol sobre o mar com a Lua no céu e as constelações do zodíaco desenhadas em dourado",
     "O horóscopo do dia dos 12 signos, com a Lua e os aspetos dos planetas de hoje."),
    ("A05", "astrologia", "astrologia-ceu-de-hoje",
     "Astrologia e o céu de hoje: astrólogo a observar a Via Láctea e os planetas alinhados, com um mapa astral e um astrolábio na mesa",
     "Astrologia: o céu de agora, calculado, e tudo para ler os signos e o seu mapa astral."),
    ("A06", "tiragem-sim-ou-nao", "tarot-sim-ou-nao",
     "Tarot sim ou não: mão a escolher entre duas cartas de tarot, uma iluminada e outra na sombra, sobre veludo azul",
     "Tarot sim ou não: uma carta para uma pergunta direta, e como ler a resposta."),
    ("A07", "tarot-do-amor", "tarot-do-amor",
     "Tarot do amor: mãos de um casal entrelaçadas sobre uma tiragem de tarot com pétalas de rosa vermelha e velas cor-de-rosa",
     "Tarot do amor: o que as cartas dizem sobre a sua relação e o seu coração."),
    ("A08", "signos-que-combinam", "signos-que-combinam",
     "Signos que combinam: casal abraçado a olhar o céu estrelado, com duas constelações a brilhar por cima",
     "Signos que combinam: o par ideal de cada signo e os que se desafiam, pela regra dos elementos."),
    # 02/11/2026: os 10 planetas (P01–P10)
    ("P01", "planeta-sol", "sol-na-astrologia", "O Sol na astrologia: o Sol com erupções douradas no espaço, sobre fundo estrelado",
     "O Sol na astrologia: a identidade, a vontade e a energia vital de cada signo."),
    ("P02", "planeta-lua", "lua-na-astrologia", "A Lua na astrologia: Lua cheia a nascer sobre o mar calmo com reflexo prateado",
     "A Lua na astrologia: as emoções, a intuição e o que nos faz sentir em casa."),
    ("P03", "planeta-mercurio", "mercurio-na-astrologia", "Mercúrio na astrologia: o planeta Mercúrio com crateras diante do Sol",
     "Mercúrio na astrologia: a mente, a comunicação e as viagens curtas."),
    ("P04", "planeta-venus", "venus-na-astrologia", "Vénus na astrologia: o planeta Vénus a brilhar no céu do entardecer sobre o mar",
     "Vénus na astrologia: o amor, a beleza, o prazer e o dinheiro."),
    ("P05", "planeta-marte", "marte-na-astrologia", "Marte na astrologia: o planeta vermelho com tempestades de poeira e as suas luas",
     "Marte na astrologia: a coragem, a iniciativa, a paixão e a forma de lutar."),
    ("P06", "planeta-jupiter", "jupiter-na-astrologia", "Júpiter na astrologia: o planeta Júpiter com as faixas e a Grande Mancha Vermelha",
     "Júpiter na astrologia: a sorte, a expansão, a fé e as oportunidades."),
    ("P07", "planeta-saturno", "saturno-na-astrologia", "Saturno na astrologia: o planeta Saturno com os anéis em grande detalhe",
     "Saturno na astrologia: a disciplina, o tempo, as responsabilidades e a maturidade."),
    ("P08", "planeta-urano", "urano-na-astrologia", "Úrano na astrologia: o planeta Úrano azul-turquesa com anéis finos",
     "Úrano na astrologia: as mudanças súbitas, a liberdade e a originalidade."),
    ("P09", "planeta-neptuno", "neptuno-na-astrologia", "Neptuno na astrologia: o planeta Neptuno azul profundo com nuvens brancas",
     "Neptuno na astrologia: a inspiração, a espiritualidade, os sonhos e as ilusões."),
    ("P10", "planeta-plutao", "plutao-na-astrologia", "Plutão na astrologia: o planeta-anão Plutão com a planície em forma de coração",
     "Plutão na astrologia: a transformação profunda, o poder e o renascimento."),
    # 02/11/2026: a Lua, os eclipses e o céu (L01–L06)
    ("L01", "lua-azul", "lua-azul", "Lua Azul: Lua cheia enorme a nascer sobre um lago entre montanhas, com reflexo na água",
     "A Lua Azul: a Lua Cheia «a mais», e quando é a próxima."),
    ("L02", "lua", "fases-da-lua", "Fases da Lua: as oito fases da Lua em linha, da Lua Nova à Lua Cheia e de volta",
     "As fases da Lua e a Lua nos signos, dia a dia, no Calendário Lunar."),
    ("L03", "eclipses-2027", "eclipse-total-do-sol", "Eclipse total do Sol com a coroa solar visível sobre montanhas ao entardecer",
     "Os eclipses de 2027: as datas, os signos e o que significam na astrologia."),
    ("L04", "alinhamento-dos-planetas", "alinhamento-dos-planetas", "Alinhamento dos planetas: quatro planetas brilhantes em linha no céu do crepúsculo",
     "O alinhamento dos planetas: quando se juntam no céu e quais se veem."),
    ("L05", "retrogrados", "mercurio-retrogrado", "Planetas retrógrados: ampulheta dourada sob um céu estrelado e a Via Láctea",
     "Os planetas retrógrados: Mercúrio retrógrado e os outros, quando e onde andam para trás."),
    ("L06", "cor-do-ano-2027", "cor-do-ano-2027-dourado", "Cor do ano 2027: passagem de ano na praia com roupas e flores douradas e fogo de artifício dourado",
     "A cor do ano 2027 na astrologia: o dourado e o amarelo do Sol, regente do ano."),
    # 02/11/2026: os 4 elementos, o mapa astral e a astrologia védica (E01–E04, M01–M02)
    ("E01", "elemento-fogo", "signos-de-fogo", "Signos de Fogo: fogueira viva com faíscas a subir para o céu estrelado",
     "Os signos de Fogo — Carneiro, Leão e Sagitário: entusiasmo, coragem e ação."),
    ("E02", "elemento-terra", "signos-de-terra", "Signos de Terra: campo lavrado ao pôr do sol, uma árvore antiga e cristais no chão",
     "Os signos de Terra — Touro, Virgem e Capricórnio: estabilidade, paciência e construção."),
    ("E03", "elemento-ar", "signos-de-ar", "Signos de Ar: penas brancas a voar ao vento num céu azul sobre as montanhas",
     "Os signos de Ar — Gémeos, Balança e Aquário: ideias, comunicação e liberdade."),
    ("E04", "elemento-agua", "signos-de-agua", "Signos de Água: onda do mar transparente ao luar, com gotas suspensas no ar",
     "Os signos de Água — Caranguejo, Escorpião e Peixes: emoção, intuição e profundidade."),
    ("M01", "mapa-astral", "mapa-astral", "Mapa astral desenhado à mão em papel antigo, com compasso de latão, cristais e vela acesa",
     "O mapa astral: os planetas no minuto em que nasceu, calculados ao minuto."),
    ("M02", "astrologia-vedica", "astrologia-vedica", "Astrologia védica: templo indiano ao anoitecer e um mapa védico desenhado em tecido cor de açafrão",
     "A astrologia védica (Jyotish): o zodíaco sideral e o seu signo védico."),
    # 03/11/2026: Histórias e Lendas + Contos tradicionais (H01–H25), geradas no renko (~/lendas-img)
    ('H02', 'lenda-galo-de-barcelos', 'lenda-do-galo-de-barcelos', 'Lenda do Galo de Barcelos: galo vermelho e preto em cima de uma mesa de madeira com velas acesas, numa sala de pedra',
     'A Lenda do Galo de Barcelos: o galo que cantou para provar a inocência do peregrino.'),
    ('H03', 'lenda-milagre-das-rosas', 'milagre-das-rosas-rainha-santa-isabel', 'Milagre das Rosas: jovem rainha de vestido azul com rosas vermelhas nas mãos, no pátio de um castelo coberto de neve',
     'O Milagre das Rosas: o pão da Rainha Santa Isabel transformado em rosas em pleno inverno.'),
    ('H04', 'lenda-amendoeiras-em-flor', 'lenda-das-amendoeiras-em-flor-algarve', 'Lenda das amendoeiras em flor: amendoeira florida, branca como neve, diante de uma casa branca do Algarve',
     'A Lenda das Amendoeiras em Flor: a «neve» que o rei mouro deu à princesa do Norte.'),
    ('H05', 'lenda-moura-encantada', 'lenda-da-moura-encantada', 'Lenda da Moura Encantada: fontes de pedra num jardim florido ao amanhecer, com luz dourada',
     'A Lenda da Moura Encantada: o pente de ouro junto à fonte na manhã de São João.'),
    ('H06', 'lenda-sao-martinho', 'lenda-de-sao-martinho', 'Lenda de São Martinho: soldado de capa vermelha a cavalo num campo de outono, com o sol a romper as nuvens',
     'A Lenda de São Martinho: a capa cortada ao meio e o verão que veio em novembro.'),
    ('H07', 'lenda-ponte-da-misarela', 'lenda-da-ponte-da-misarela', 'Lenda da Ponte da Misarela: ponte de pedra em arco sobre o rio num desfiladeiro, de noite, com névoa',
     'A Lenda da Ponte da Misarela: a ponte que o Diabo fez numa noite.'),
    ('H08', 'lenda-pedro-sem', 'lenda-de-pedro-sem-porto', 'Lenda de Pedro Sem: torre de pedra no alto de uma falésia sobre o mar, com tempestade e relâmpagos',
     'A Lenda de Pedro Sem: o rico do Porto que desafiou o céu da sua torre.'),
    ('H09', 'lenda-padeira-de-aljubarrota', 'padeira-de-aljubarrota-pa-do-forno', 'Padeira de Aljubarrota: padeira de avental junto ao forno de lenha aceso, com pães acabados de cozer',
     'A Padeira de Aljubarrota: Brites de Almeida e a pá do forno.'),
    ('H10', 'lenda-nazare-fuas-roupinho', 'lenda-da-nazare-fuas-roupinho', 'Lenda da Nazaré: cavaleiro a cavalo a travar à beira da falésia, sobre um mar de nevoeiro',
     'A Lenda da Nazaré: D. Fuas Roupinho salvo à beira do abismo.'),
    ('H11', 'lenda-sete-cidades', 'lenda-das-sete-cidades-lagoa-azul-verde', 'Lenda das Sete Cidades: lagoa dentro de uma cratera verde nos Açores, com o mar ao fundo',
     'A Lenda das Sete Cidades: as lágrimas da princesa e do pastor que fizeram duas lagoas.'),
    ('H12', 'historia-aparicoes-de-fatima', 'historia-de-fatima-cova-da-iria', 'História de Fátima: azinheira num campo pedregoso ao pôr do sol, com a luz a descer sobre a Cova da Iria',
     'A História de Fátima: os três pastorinhos da Cova da Iria em 1917.'),
    ('H13', 'historia-promessa-a-sao-bentinho', 'promessa-a-sao-bentinho', 'Promessa a São Bentinho: velas acesas numa capela antiga de pedra, com uma lanterna no chão',
     'A Promessa a São Bentinho: a história de um homem que não acreditava em promessas.'),
    ('H14', 'historia-o-velho-rico-e-a-moca-nova', 'o-velho-rico-e-a-moca-nova', 'O Velho Rico e a Moça Nova: bolsa de couro no parapeito de uma janela antiga com sardinheiras vermelhas',
     'O Velho Rico e a Moça Nova: a cantiga de quem sabe que nem tudo se compra.'),
    ('H15', 'conto-sopa-de-pedra', 'sopa-de-pedra-conto-tradicional', 'Sopa de Pedra: panela grande com chouriço, couve e legumes numa cozinha antiga com lareira',
     'A Sopa de Pedra: o conto do frade esperto que deu nome ao prato de Almeirim.'),
    ('H16', 'conto-carochinha-e-joao-ratao', 'carochinha-e-joao-ratao', 'A Carochinha e o João Ratão: ratinho à janela de uma casa antiga, com flores amarelas',
     'A Carochinha e o João Ratão: a moeda, a janela e a gulodice que estragou a boda.'),
    ('H18', 'conto-tres-conselhos', 'conto-dos-tres-conselhos', 'Os Três Conselhos: viajante de chapéu e cajado numa estrada de campo ao amanhecer',
     'Os Três Conselhos: o criado que trocou o salário por três conselhos.'),
    ('H19', 'conto-formiga-e-a-neve', 'conto-da-formiga-e-a-neve', 'A Formiga e a Neve: formiga sobre neve fresca ao sol, vista de muito perto',
     'A Formiga e a Neve: o conto de encadear sobre quem é mais forte.'),
    ('H20', 'conto-principe-orelhas-de-burro', 'principe-com-orelhas-de-burro', 'O Príncipe com Orelhas de Burro: o barbeiro a cortar o cabelo ao príncipe, com a coroa ao lado',
     'O Príncipe com Orelhas de Burro: o segredo que o barbeiro não conseguiu guardar.'),
    ('H21', 'conto-velha-e-a-cabacinha', 'a-velha-e-a-cabacinha', 'A Velha e a Cabacinha: cabaça grande num caminho de terra pelo monte, na floresta de outono',
     'A Velha e a Cabacinha: a cabaça que rolou pelo monte abaixo e enganou os lobos.'),
    ('H23', 'conto-a-manta-partida', 'a-manta-partida-ao-meio', 'A Manta Partida: manta de lã sobre uma cadeira de madeira num quarto de casa de lavoura',
     'A Manta Partida ao Meio: o conto sobre como tratamos os mais velhos.'),
    ('H24', 'conto-frei-joao-sem-cuidados', 'frei-joao-sem-cuidados', 'Frei João Sem Cuidados: moinho de água de pedra junto ao rio, numa floresta de outono',
     'Frei João Sem Cuidados: as três perguntas do rei e o moleiro que respondeu.'),
    ('H17', 'conto-coelhinho-branco', 'conto-do-coelhinho-branco', 'O Coelhinho Branco: coelho branco de casaco ao lado da porta da sua toca, num prado ao fim da tarde',
     'O Coelhinho Branco: a cabra cabrês e o pequeno herói que a tirou da toca.'),
    ('H25', 'conto-menina-e-o-figo', 'a-menina-e-o-figo', 'A Menina e o Figo: figos maduros roxos pendurados num ramo de figueira, com folhas verdes ao sol',
     'A Menina e o Figo: o capim que cantou e a verdade que não ficou enterrada.'),
]

FIG = ('<!-- img-destaque:inicio -->\n<figure class="img-destaque" style="max-width:72rem;margin:0 auto 2rem;padding:0 1rem;position:relative;z-index:1">'
       '<img src="/{nome}.webp" alt="{alt}" title="{alt}" width="1200" height="800" fetchpriority="high" decoding="async" '
       'style="display:block;width:100%;height:auto;border-radius:1.2rem;border:1px solid rgba(212,175,55,.35);box-shadow:0 18px 50px #0008">'
       '<figcaption style="text-align:center;font-size:.85rem;color:#c9c2e0;margin-top:.6rem">{leg}</figcaption></figure>\n<!-- img-destaque:fim -->\n')


def converter():
    from PIL import Image
    for cod, _, nome, _, _ in IMAGENS:
        src = next((f"{ORIG}/{cod}.{e}" for e in ("png", "jpg", "jpeg", "webp") if os.path.exists(f"{ORIG}/{cod}.{e}")), None)
        if not src: print(cod, "sem original"); continue
        im = Image.open(src).convert("RGB")
        w = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        if w.height != 800:   # 3:2 certinho
            t = (w.height - 800) // 2; w = w.crop((0, max(0, t), 1200, max(0, t) + 800))
        w.save(f"{nome}.webp", "WEBP", quality=82, method=6)
        h = round(1200 * 630 / 1200); og = w.crop((0, (800 - 630) // 2, 1200, (800 - 630) // 2 + 630))
        og.save(f"{nome}-og.jpg", "JPEG", quality=84, optimize=True, progressive=True)
        w.resize((600, 400), Image.LANCZOS).save(f"{nome}-mini.webp", "WEBP", quality=78, method=6)   # 03/11: cartões dos índices
        print(cod, nome, os.path.getsize(f"{nome}.webp") // 1024, "KB webp,", os.path.getsize(f"{nome}-og.jpg") // 1024, "KB og")


def aplicar():
    mudadas = []
    for cod, pag, nome, alt, leg in IMAGENS:
        f = f"{pag}.html"
        if not (os.path.exists(f) and os.path.exists(f"{nome}.webp")): continue
        h0 = h = open(f, encoding="utf-8").read()
        fig = FIG.format(nome=nome, alt=html.escape(alt), leg=html.escape(leg))
        h = re.sub(r"<!-- img-destaque:inicio -->.*?<!-- img-destaque:fim -->\n", "", h, flags=re.S)   # tira exactamente o que pôs
        m = re.search(r'<section class="hero[i]?"[^>]*>', h)
        if not m: print("⚠️", f, "sem bloco de topo"); continue
        fim = h.index("</section>", m.end()) + len("</section>")
        if h[fim:fim + 1] == "\n": fim += 1
        h = h[:fim] + fig + h[fim:]
        og = f"{SITE}/{nome}-og.jpg"
        h = re.sub(r'(<meta property="og:image" content=")[^"]*', r"\g<1>" + og, h, count=1)
        h = re.sub(r'(<meta property="og:image:width" content=")[^"]*', r"\g<1>1200", h, count=1)
        h = re.sub(r'(<meta property="og:image:height" content=")[^"]*', r"\g<1>630", h, count=1)
        h = re.sub(r'\n?<meta property="og:image:alt"[^>]*>', "", h)
        h = h.replace(f'<meta property="og:image" content="{og}" />', f'<meta property="og:image" content="{og}" />\n<meta property="og:image:alt" content="{html.escape(alt)}" />', 1)
        ld = {"@context": "https://schema.org", "@type": "ImageObject", "contentUrl": f"{SITE}/{nome}.webp", "url": f"{SITE}/{nome}.webp",
              "name": alt.split(":")[0], "caption": leg, "description": alt, "width": 1200, "height": 800,
              "creator": {"@type": "Organization", "name": "Genial Tarot"}, "copyrightHolder": {"@type": "Organization", "name": "Genial Tarot"},
              "creditText": "Genial Tarot · Mestre Alberto", "copyrightNotice": "© Genial Tarot", "representativeOfPage": True}
        h = re.sub(r'<script type="application/ld\+json" data-img-destaque>.*?</script>\n?', "", h, flags=re.S)
        h = h.replace("</head>", f'<script type="application/ld+json" data-img-destaque>{json.dumps(ld, ensure_ascii=False)}</script>\n</head>', 1)
        if h != h0:
            open(f, "w", encoding="utf-8").write(h); mudadas.append(f)
    for f in mudadas: print(f)


# 03/11/2026 (ele: «põe também imagens nos cartões do índice das histórias»): nos índices (HUBS), cada cartão <a href="/pág">
# de uma página com imagem ganha a miniatura em cima. Marcado com class="com-foto" e <img class="mini">, para se tirar e repor
# sem duplicar; o estilo vai entre <!-- cartoes-foto:inicio/fim -->. Cartões sem imagem ficam como estavam.
HUBS = ["historias-e-lendas", "contos-tradicionais", "parabolas", "parabolas-de-jesus", "fabulas-de-esopo"]
CSS_CARTOES = ('<!-- cartoes-foto:inicio --><style>.doze a.com-foto{flex-direction:column;align-items:stretch;gap:0;padding:0;overflow:hidden}'
               '.doze a.com-foto img.mini{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:0;display:block}'
               '.doze a.com-foto>span{padding:.8rem 1rem}</style><!-- cartoes-foto:fim -->\n')


def cartoes():
    por_pag = {pag: (nome, alt) for _, pag, nome, alt, _ in IMAGENS if os.path.exists(f"{nome}-mini.webp")}
    for hub in HUBS:
        f = f"{hub}.html"
        if not os.path.exists(f): continue
        h0 = h = open(f, encoding="utf-8").read()
        h = re.sub(r'<a href="(/[^"]+)" class="com-foto"><img class="mini"[^>]*>', r'<a href="\1">', h)
        h = re.sub(r"<!-- cartoes-foto:inicio -->.*?<!-- cartoes-foto:fim -->\n", "", h, flags=re.S)
        n = 0
        def poe(m):
            nonlocal n
            pag = m.group(1)
            if pag not in por_pag: return m.group(0)
            nome, alt = por_pag[pag]; n += 1
            return (f'<a href="/{pag}" class="com-foto"><img class="mini" src="/{nome}-mini.webp" alt="{html.escape(alt)}" '
                    f'width="600" height="400" loading="lazy" decoding="async">')
        i = h.find('<div class="doze">')
        if i < 0: continue
        j = h.find("</section>", i)
        h = h[:i] + re.sub(r'<a href="/([^"/]+)">', poe, h[i:j]) + h[j:]
        if n: h = h.replace("</head>", CSS_CARTOES + "</head>", 1)
        if h != h0:
            open(f, "w", encoding="utf-8").write(h); print(f, n, "cartões com imagem")


if __name__ == "__main__":
    if "--converter" in sys.argv: converter()
    else: aplicar(); cartoes()
