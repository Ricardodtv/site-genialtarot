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
    ("T01", "cartas-do-tarot-reconciliacao", "cartas-do-tarot-reconciliacao",
     "Cartas do Tarot da reconciliação do baralho do Mestre Alberto: Dois de Copas ao centro, com Seis de Copas, O Julgamento, A Temperança e A Estrela",
     "As cartas do Tarot da reconciliação: o Dois de Copas ao centro, com o Seis de Copas, O Julgamento, A Temperança e A Estrela, do baralho do Mestre Alberto."),
    ("A01", "consulta-de-tarot-online", "consulta-de-tarot-online",
     "Consulta de tarot online: mãos do tarólogo a virar as cartas numa mesa de veludo azul, com velas e uma videochamada ao lado",
     "Consulta de tarot online com o Mestre Alberto: as cartas são lançadas ao vivo e a leitura faz-se por videochamada, chamada ou mensagem."),
    ("A02", "tarot-gratis", "tarot-gratis-online",
     "Tarot grátis online: três cartas de tarot sobre veludo azul, a do meio a brilhar com luz dourada",
     "Tarot grátis online: pense na sua pergunta e tire três cartas do baralho do Mestre Alberto."),
    ("A03", "horoscopo-semanal", "horoscopo-semanal-signos",
     "Horóscopo semanal dos signos: roda do zodíaco dourada com os 12 signos, astrolábio e agenda aberta sob um céu estrelado",
     "O horóscopo semanal dos 12 signos, de segunda a domingo, a partir do céu real da semana."),
    # 03/11/2026: imagens novas dele (cofrecerebro) para A04, A05, L01 e S01; os originais antigos ficaram como <CÓD>.antes-03nov.png
    ("A04", "horoscopo-do-dia", "horoscopo-do-dia",
     "Horóscopo do dia: roda do zodíaco dourada com os 12 signos e o Sol ao centro, bola de cristal e livro de astrologia aberto ao pôr do sol",
     "O horóscopo do dia dos 12 signos, com a Lua e os aspetos dos planetas de hoje."),
    ("A05", "astrologia", "astrologia-ceu-de-hoje",
     "Astrologia de agora: roda do zodíaco dourada, esfera armilar e bola de cristal, com a Lua e Saturno no céu estrelado",
     "A astrologia de agora: onde está cada planeta neste momento, a Lua e os retrógrados, calculados."),
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
    ("L01", "lua-azul", "lua-azul", "Lua Azul: Lua cheia azul enorme no céu da noite, entre nuvens iluminadas pelo luar",
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
     "Os signos de Fogo (Carneiro, Leão e Sagitário): entusiasmo, coragem e ação."),
    ("E02", "elemento-terra", "signos-de-terra", "Signos de Terra: campo lavrado ao pôr do sol, uma árvore antiga e cristais no chão",
     "Os signos de Terra (Touro, Virgem e Capricórnio): estabilidade, paciência e construção."),
    ("E03", "elemento-ar", "signos-de-ar", "Signos de Ar: penas brancas a voar ao vento num céu azul sobre as montanhas",
     "Os signos de Ar (Gémeos, Balança e Aquário): ideias, comunicação e liberdade."),
    ("E04", "elemento-agua", "signos-de-agua", "Signos de Água: onda do mar transparente ao luar, com gotas suspensas no ar",
     "Os signos de Água (Caranguejo, Escorpião e Peixes): emoção, intuição e profundidade."),
    ("M01", "mapa-astral", "mapa-astral", "Mapa astral desenhado à mão em papel antigo, com compasso de latão, cristais e vela acesa",
     "O mapa astral: os planetas no minuto em que nasceu, calculados ao minuto."),
    ("M02", "astrologia-vedica", "astrologia-vedica", "Astrologia védica: templo indiano ao anoitecer e um mapa védico desenhado em tecido cor de açafrão",
     "A astrologia védica (Jyotish): o zodíaco sideral e o seu signo védico."),
    ("S01", "melhores-signos-2027", "melhores-signos-2027",
     "Melhores signos de 2027: o número 2027 dourado no centro da roda do zodíaco, com os 12 signos, bola de cristal e ametistas",
     "Os melhores signos de 2027: quem tem Júpiter a favor e a melhor fase do ano para cada signo."),
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
    # 03/11/2026: Parábolas de Jesus (J), Fábulas de Esopo (F), Parábolas de vida (V) e o Sal (H22) — aprovadas por ele
    ('J01', 'parabola-jesus-filho-prodigo', 'parabola-jesus-filho-prodigo', 'O Filho Pródigo: homem idoso de túnica a correr por um caminho de terra em frente a uma casa de pedra, ao pôr do sol',
     'O Filho Pródigo — ilustração da história.'),
    ('J02', 'parabola-jesus-semeador', 'parabola-jesus-semeador', 'O Semeador: semeador a lançar sementes num campo lavrado, com searas douradas ao pôr do sol',
     'O Semeador — ilustração da história.'),
    ('J03', 'parabola-jesus-talentos', 'parabola-jesus-talentos', 'Os Talentos: bolsa de couro cheia de moedas antigas ao lado de um livro aberto, sobre uma mesa',
     'Os Talentos — ilustração da história.'),
    ('J04', 'parabola-jesus-ovelha-perdida', 'parabola-jesus-ovelha-perdida', 'A Ovelha Perdida: ovelha sozinha no alto de um rochedo, num vale de montanha',
     'A Ovelha Perdida — ilustração da história.'),
    ('J05', 'parabola-jesus-grao-de-mostarda', 'parabola-jesus-grao-de-mostarda', 'O Grão de Mostarda: grande árvore frondosa no meio de um campo ao entardecer',
     'O Grão de Mostarda — ilustração da história.'),
    ('J06', 'parabola-jesus-dez-virgens', 'parabola-jesus-dez-virgens', 'As Dez Virgens: lamparina de azeite acesa ao lado de um frasco e de um jarro de barro, numa sala escura',
     'As Dez Virgens — ilustração da história.'),
    ('J07', 'parabola-jesus-casa-sobre-a-rocha', 'parabola-jesus-casa-sobre-a-rocha', 'A Casa sobre a Rocha: casa de pedra firme no alto de um rochedo à beira-mar, sob uma tempestade',
     'A Casa sobre a Rocha — ilustração da história.'),
    ('J08', 'parabola-jesus-fariseu-e-publicano', 'parabola-jesus-fariseu-e-publicano', 'O Fariseu e o Publicano: homem ajoelhado a rezar sozinho num templo de colunas e arcos de pedra',
     'O Fariseu e o Publicano — ilustração da história.'),
    ('J09', 'parabola-jesus-rico-insensato', 'parabola-jesus-rico-insensato', 'O Rico Insensato: celeiros de pedra rodeados de molhos de trigo, ao fim da tarde',
     'O Rico Insensato — ilustração da história.'),
    ('J10', 'parabola-jesus-bom-samaritano', 'parabola-jesus-bom-samaritano', 'O Bom Samaritano: jarro de barro e um copo de vidro numa pedra à beira de uma estrada no deserto',
     'O Bom Samaritano — ilustração da história.'),
    ('F01', 'fabula-cigarra-e-formiga', 'fabula-cigarra-e-formiga', 'A Cigarra e a Formiga: cigarra pousada numa folha, em grande plano, com luz dourada',
     'A Cigarra e a Formiga — ilustração da história.'),
    ('F02', 'fabula-raposa-e-uvas', 'fabula-raposa-e-uvas', 'A Raposa e as Uvas: raposa a olhar para cima, para cachos de uvas pendurados na videira',
     'A Raposa e as Uvas — ilustração da história.'),
    ('F03', 'fabula-leao-e-rato', 'fabula-leao-e-rato', 'O Leão e o Rato: leão deitado preso numa rede de cordas, num celeiro de madeira',
     'O Leão e o Rato — ilustração da história.'),
    ('F04', 'fabula-lobo-e-cordeiro', 'fabula-lobo-e-cordeiro', 'O Lobo e o Cordeiro: cordeiro a beber água num riacho entre pedras, numa floresta',
     'O Lobo e o Cordeiro — ilustração da história.'),
    ('F05', 'fabula-pastor-e-lobo', 'fabula-pastor-e-lobo', 'O Pastor e o Lobo: rapaz pastor com chapéu em frente ao seu rebanho de ovelhas, num prado',
     'O Pastor e o Lobo — ilustração da história.'),
    ('F06', 'fabula-cao-e-sombra', 'fabula-cao-e-sombra', 'O Cão e a sua Sombra: cão numa ponte de madeira a olhar para o seu reflexo no rio',
     'O Cão e a sua Sombra — ilustração da história.'),
    ('F07', 'fabula-rato-do-campo-e-rato-da-cidade', 'fabula-rato-do-campo-e-rato-da-cidade', 'O Rato do Campo e o Rato da Cidade: mesa redonda posta com pão, queijo e velas numa sala rica',
     'O Rato do Campo e o Rato da Cidade — ilustração da história.'),
    ('F08', 'fabula-vento-e-sol', 'fabula-vento-e-sol', 'O Vento e o Sol: viajante de capa a caminhar por uma estrada com o sol a romper as nuvens',
     'O Vento e o Sol — ilustração da história.'),
    ('F09', 'fabula-formiga-e-pomba', 'fabula-formiga-e-pomba', 'A Formiga e a Pomba: pomba branca à beira de um ribeiro, com uma folha a cair na água',
     'A Formiga e a Pomba — ilustração da história.'),
    ('F10', 'fabula-velho-rapaz-e-burro', 'fabula-velho-rapaz-e-burro', 'O Velho, o Rapaz e o Burro: velho e rapaz a caminhar por uma rua de aldeia, com um burro ao lado',
     'O Velho, o Rapaz e o Burro — ilustração da história.'),
    ('F11', 'fabula-corvo-e-raposa', 'fabula-corvo-e-raposa', 'O Corvo e a Raposa: corvo preto pousado num poste de madeira, num bosque',
     'O Corvo e a Raposa — ilustração da história.'),
    ('F12', 'fabula-galinha-dos-ovos-de-ouro', 'fabula-galinha-dos-ovos-de-ouro', 'A Galinha dos Ovos de Ouro: cesto de vime em forma de galinha cheio de ovos, num celeiro',
     'A Galinha dos Ovos de Ouro — ilustração da história.'),
    ('F13', 'fabula-lebre-e-tartaruga', 'fabula-lebre-e-tartaruga', 'A Lebre e a Tartaruga: tartaruga a avançar devagar por um caminho de terra no campo',
     'A Lebre e a Tartaruga — ilustração da história.'),
    ('F14', 'fabula-raposa-e-cegonha', 'fabula-raposa-e-cegonha', 'A Raposa e a Cegonha: cegonha branca e raposa frente a frente num jardim junto a uma casa de pedra',
     'A Raposa e a Cegonha — ilustração da história.'),
    ('V01', 'parabola-a-aguia-e-o-pardal', 'parabola-a-aguia-e-o-pardal', 'A Águia e o Pardal: águia de asas abertas pousada num ramo, sobre um vale, com outra ave a voar',
     'A Águia e o Pardal — ilustração da história.'),
    ('V02', 'parabola-a-areia-na-mao', 'parabola-a-areia-na-mao', 'A Areia na Mão: mão a segurar areia na praia, ao pôr do sol sobre o mar',
     'A Areia na Mão — ilustração da história.'),
    ('V03', 'parabola-a-bomba-de-agua', 'parabola-a-bomba-de-agua', 'A Bomba de Água: lata de metal antiga e uma garrafa de vidro na areia do deserto',
     'A Bomba de Água — ilustração da história.'),
    ('V04', 'parabola-a-carroca-vazia', 'parabola-a-carroca-vazia', 'A Carroça Vazia: carroça de madeira vazia num caminho de floresta no outono',
     'A Carroça Vazia — ilustração da história.'),
    ('V05', 'parabola-a-formiga-e-a-folha', 'parabola-a-formiga-e-a-folha', 'A Formiga e a Folha: formiga a carregar um pedaço de folha no chão de terra',
     'A Formiga e a Folha — ilustração da história.'),
    ('V06', 'parabola-a-galinha-depenada', 'parabola-a-galinha-depenada', 'A Galinha Depenada: cesto de vime cheio de penas no chão de um pátio',
     'A Galinha Depenada — ilustração da história.'),
    ('V07', 'parabola-a-licao-da-borboleta', 'parabola-a-licao-da-borboleta', 'A Lição da Borboleta: borboleta a sair do casulo pendurado num ramo',
     'A Lição da Borboleta — ilustração da história.'),
    ('V08', 'parabola-as-flores-e-o-arroz', 'parabola-as-flores-e-o-arroz', 'As Flores e o Arroz: taça de pedra com flores frescas sobre uma campa num cemitério relvado',
     'As Flores e o Arroz — ilustração da história.'),
    ('V09', 'parabola-as-maos-do-pai', 'parabola-as-maos-do-pai', 'As Mãos do Pai: mãos envelhecidas de um homem a amassar massa num alguidar de barro',
     'As Mãos do Pai — ilustração da história.'),
    ('V10', 'parabola-a-ultima-casa', 'parabola-a-ultima-casa', 'A Última Casa: casa nova de madeira com as janelas iluminadas ao pôr do sol',
     'A Última Casa — ilustração da história.'),
    ('V11', 'parabola-a-vaca-nao-da-leite', 'parabola-a-vaca-nao-da-leite', 'A Vaca Não Dá Leite: vaca magra num estábulo de madeira, junto a um balde',
     'A Vaca Não Dá Leite — ilustração da história.'),
    ('V12', 'parabola-a-vaquinha', 'parabola-a-vaquinha', 'A Vaquinha: vaca castanha à porta de um barracão, com o campo ao fundo',
     'A Vaquinha — ilustração da história.'),
    ('V13', 'parabola-inocente-ou-culpado', 'parabola-inocente-ou-culpado', 'Inocente ou Culpado: martelo de juiz em madeira sobre uma mesa, com um livro aberto',
     'Inocente ou Culpado — ilustração da história.'),
    ('V14', 'parabola-o-camelo-no-jardim-zoologico', 'parabola-o-camelo-no-jardim-zoologico', 'O Camelo no Jardim Zoológico: camelo atrás de uma cerca de madeira, num recinto',
     'O Camelo no Jardim Zoológico — ilustração da história.'),
    ('V15', 'parabola-a-aguia-criada-entre-galinhas', 'parabola-a-aguia-criada-entre-galinhas', 'A Águia Criada entre Galinhas: águia no chão de uma capoeira, à porta de um galinheiro de madeira',
     'A Águia Criada entre Galinhas — ilustração da história.'),
    ('V16', 'parabola-afiar-o-machado', 'parabola-afiar-o-machado', 'Afiar o Machado: banco de lenhador em madeira junto a uma pilha de lenha, na floresta',
     'Afiar o Machado — ilustração da história.'),
    ('V17', 'parabola-o-burro-no-poco', 'parabola-o-burro-no-poco', 'O Burro no Poço: burro sozinho num pátio de pedra de uma aldeia antiga',
     'O Burro no Poço — ilustração da história.'),
    ('V18', 'parabola-o-cego-e-o-letreiro', 'parabola-o-cego-e-o-letreiro', 'O Cego e o Letreiro: moedas no chão de uma rua de calçada, ao sol da tarde',
     'O Cego e o Letreiro — ilustração da história.'),
    ('V19', 'parabola-o-frasco-e-as-bolas-de-golfe', 'parabola-o-frasco-e-as-bolas-de-golfe', 'O Frasco e as Bolas de Golfe: frasco de vidro com areia e café ao lado de bolas de golfe, numa mesa',
     'O Frasco e as Bolas de Golfe — ilustração da história.'),
    ('V20', 'parabola-o-ladrao-das-cebolas', 'parabola-o-ladrao-das-cebolas', 'O Ladrão das Cebolas: cesto de vime cheio de cebolas roxas numa mesa, numa rua de aldeia',
     'O Ladrão das Cebolas — ilustração da história.'),
    ('V21', 'parabola-o-lenhador-e-a-raposa', 'parabola-o-lenhador-e-a-raposa', 'O Lenhador e a Raposa: berço de madeira numa casa de lenhador, com luz a entrar pela janela',
     'O Lenhador e a Raposa — ilustração da história.'),
    ('V22', 'parabola-o-milho-dos-vizinhos', 'parabola-o-milho-dos-vizinhos', 'O Milho dos Vizinhos: campos de milho maduro em fila até um celeiro, ao pôr do sol',
     'O Milho dos Vizinhos — ilustração da história.'),
    ('V23', 'parabola-o-papel-amarrotado', 'parabola-o-papel-amarrotado', 'O Papel Amarrotado: folha de papel amarrotada numa mesa de madeira',
     'O Papel Amarrotado — ilustração da história.'),
    ('V24', 'parabola-o-rei-e-os-caes', 'parabola-o-rei-e-os-caes', 'O Rei e os Cães: quatro cães deitados lado a lado num pátio de um castelo de pedra',
     'O Rei e os Cães — ilustração da história.'),
    ('V25', 'parabola-os-biscoitos-do-aeroporto', 'parabola-os-biscoitos-do-aeroporto', 'Os Biscoitos do Aeroporto: cadeirão junto a uma janela com vista para um avião na pista',
     'Os Biscoitos do Aeroporto — ilustração da história.'),
    ('V26', 'parabola-os-dois-amigos-no-deserto', 'parabola-os-dois-amigos-no-deserto', 'Os Dois Amigos no Deserto: pegadas na areia das dunas do deserto, ao pôr do sol',
     'Os Dois Amigos no Deserto — ilustração da história.'),
    ('V27', 'parabola-os-dois-lobos', 'parabola-os-dois-lobos', 'Os Dois Lobos: dois lobos frente a frente numa floresta com neve',
     'Os Dois Lobos — ilustração da história.'),
    ('V28', 'parabola-os-vendedores-de-sapatos', 'parabola-os-vendedores-de-sapatos', 'Os Vendedores de Sapatos: caminho de terra batida entre palmeiras e plantas tropicais',
     'Os Vendedores de Sapatos — ilustração da história.'),
    ('V29', 'parabola-quanto-vale-o-anel', 'parabola-quanto-vale-o-anel', 'Quanto Vale o Anel: anel de ouro com uma pedra âmbar sobre um pano de veludo',
     'Quanto Vale o Anel — ilustração da história.'),
    ('V30', 'parabola-sorte-ou-azar', 'parabola-sorte-ou-azar', 'Sorte ou Azar: cavalo a correr junto a uma quinta, num caminho de terra ao amanhecer',
     'Sorte ou Azar — ilustração da história.'),
    ('V31', 'parabola-um-dedo-diferente-por-dia', 'parabola-um-dedo-diferente-por-dia', 'Um Dedo Diferente por Dia: calendário e livro aberto numa mesa, com bule e chávena de chá',
     'Um Dedo Diferente por Dia — ilustração da história.'),
    ('H22', 'conto-como-a-comida-quer-o-sal', 'como-a-comida-quer-o-sal', 'Como a Comida Quer o Sal: taça de madeira cheia de sal grosso com uma colher de pau, numa mesa',
     'Como a Comida Quer o Sal — ilustração da história.'),
    ('H01', 'lenda-justica-de-fafe', 'justica-de-fafe-monumento',
     'Justiça de Fafe: estátua de bronze de um homem do Minho a erguer o varapau contra um fidalgo de casaca, em Fafe, sob o céu azul',
     'O monumento à Justiça de Fafe, na cidade de Fafe: o varapau erguido que deu nome à lenda.'),
    # 03/11/2026: os grandes trânsitos (gerar-transitos.py) — reaproveitam imagens que já existem
    ("P09", "neptuno-em-carneiro", "neptuno-na-astrologia", "Neptuno na astrologia: o planeta Neptuno azul profundo com nuvens brancas",
     "Neptuno em Carneiro: as datas exatas e o que muda para cada um dos 12 signos."),
    ("P07", "saturno-em-carneiro", "saturno-na-astrologia", "Saturno na astrologia: o planeta Saturno com os anéis em grande detalhe",
     "Saturno em Carneiro: as datas exatas e o que muda para cada um dos 12 signos."),
    ("P10", "plutao-em-aquario", "plutao-na-astrologia", "Plutão na astrologia: o planeta-anão Plutão com a planície em forma de coração",
     "Plutão em Aquário: as datas exatas e o que muda para cada um dos 12 signos."),
    ("P08", "urano-em-gemeos", "urano-na-astrologia", "Úrano na astrologia: o planeta Úrano azul-turquesa com anéis finos",
     "Úrano em Gémeos: as datas exatas e o que muda para cada um dos 12 signos."),
    ("P06", "jupiter-em-leao", "jupiter-na-astrologia", "Júpiter na astrologia: o planeta Júpiter com as faixas e a Grande Mancha Vermelha",
     "Júpiter em Leão: as datas exatas e o que muda para cada um dos 12 signos."),
    ("P06", "jupiter-em-virgem", "jupiter-na-astrologia", "Júpiter na astrologia: o planeta Júpiter com as faixas e a Grande Mancha Vermelha",
     "Júpiter em Virgem: as datas exatas e o que muda para cada um dos 12 signos."),
    ("L03", "nodos-lunares-aquario-leao", "eclipse-total-do-sol", "Eclipse total do Sol com a coroa solar visível sobre montanhas ao entardecer",
     "Nodos lunares: Aquário e Leão: as datas exatas e o que muda para cada um dos 12 signos."),
    ("L04", "saturno-e-urano-2032", "alinhamento-dos-planetas", "Alinhamento dos planetas: quatro planetas brilhantes em linha no céu do crepúsculo",
     "Saturno e Úrano em 2032: as datas exatas e o que muda para cada um dos 12 signos."),
    ("L04", "transitos-lentos", "alinhamento-dos-planetas", "Alinhamento dos planetas: quatro planetas brilhantes em linha no céu do crepúsculo",
     "Os grandes trânsitos dos planetas lentos, com as datas calculadas."),
]

# 03/11/2026: fotos de FORA com licença livre (ele: «vai buscar foto do monumento público, licença livre + crédito»).
# A CC BY-SA pede o autor, a licença com ligação e a fonte; e o JSON-LD não pode dizer «© Genial Tarot».
CREDITOS = {
    "H01": {"autor": "Vitor Oliveira", "licenca": "CC BY-SA 2.0", "licenca_url": "https://creativecommons.org/licenses/by-sa/2.0/",
            "fonte": "https://commons.wikimedia.org/wiki/File:Monumento_%C3%A0_Justi%C3%A7a_de_Fafe_-_Portugal_(6766195051)_(cropped).jpg",
            "nota": "adaptada (enquadrada com fundo desfocado)"},
}

FIG = ('<!-- img-destaque:inicio -->\n<figure class="img-destaque" style="max-width:72rem;margin:0 auto 2rem;padding:0 1rem;position:relative;z-index:1">'
       '<img src="/{nome}.webp" alt="{alt}" title="{alt}" width="1200" height="800" fetchpriority="high" decoding="async" '
       'style="display:block;width:100%;height:auto;border-radius:1.2rem;border:1px solid rgba(212,175,55,.35);box-shadow:0 18px 50px #0008">'
       '<figcaption style="text-align:center;font-size:.85rem;color:#c9c2e0;margin-top:.6rem">{leg}</figcaption></figure>\n<!-- img-destaque:fim -->\n')


# 03/11/2026: onde cortar quando o original não é 3:2 (0 = encostado à esquerda, 0.5 = ao centro, 1 = à direita)
CORTE = {"A04": 0.05, "A05": 0.35}


def converter(so=None):
    from PIL import Image
    for cod, _, nome, _, _ in IMAGENS:
        if so and cod not in so: continue
        src = next((f"{ORIG}/{cod}.{e}" for e in ("png", "jpg", "jpeg", "webp") if os.path.exists(f"{ORIG}/{cod}.{e}")), None)
        if not src: print(cod, "sem original"); continue
        im = Image.open(src).convert("RGB")
        if abs(im.width / im.height - 1.5) > 0.01:   # 03/11: cortar para 3:2 antes de reduzir (16:9 → sem faixas pretas)
            if im.width / im.height > 1.5:
                cw = round(im.height * 1.5); x = round((im.width - cw) * CORTE.get(cod, 0.5)); im = im.crop((x, 0, x + cw, im.height))
            else:
                ch = round(im.width / 1.5); y = (im.height - ch) // 2; im = im.crop((0, y, im.width, y + ch))
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
        cr = CREDITOS.get(cod)
        legh = html.escape(leg)
        if cr:
            legh += (f'<br><small style="opacity:.75">Foto: {html.escape(cr["autor"])}, <a href="{cr["licenca_url"]}" rel="license noopener" '
                     f'style="color:inherit">{cr["licenca"]}</a>, via <a href="{cr["fonte"]}" rel="noopener" style="color:inherit">Wikimedia Commons</a>'
                     f'{" — " + html.escape(cr["nota"]) if cr.get("nota") else ""}</small>')
        fig = FIG.format(nome=nome, alt=html.escape(alt), leg=legh)
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
        if cr:
            ld.update({"creator": {"@type": "Person", "name": cr["autor"]}, "license": cr["licenca_url"], "acquireLicensePage": cr["fonte"],
                       "creditText": f'{cr["autor"]} ({cr["licenca"]}, via Wikimedia Commons)', "copyrightNotice": f'© {cr["autor"]}, {cr["licenca"]}'})
            ld.pop("copyrightHolder", None)
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
    if "--converter" in sys.argv: converter([a for a in sys.argv[1:] if not a.startswith("--")] or None)   # 03/11: --converter A04 L01 … = só esses
    else: aplicar(); cartoes()
