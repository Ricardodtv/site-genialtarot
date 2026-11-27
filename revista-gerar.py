#!/usr/bin/env python3
"""A Revista do mês — «Genial · <Mês> <Ano>» (27/11/2026, pedido dele: ideia da análise do myzenmoment.com, que era
uma revista e morreu; e «se se pode auto alimentar com o conteúdo do site»). SE ALIMENTA SOZINHA:
  • o céu do mês ........ efemerides/<ano>.json (Swiss Ephemeris, o mesmo ficheiro da página das Efemérides)
  • as luas ............. idem (fases + o signo da Lua calculado na hora)
  • os 12 signos ........ o que acontece em cada signo no mês, tirado dos acontecimentos (nada inventado)
  • o Mês Pessoal ....... a conta da calculadora (numerologia-2027-textos.js, as palavras dos meses)
  • famosos do mês ...... famosos-ceu-dados.js (Wikidata), quem faz anos no mês, sem política
  • notícias do mês ..... noticias/lista.json (as notícias do céu publicadas nesse mês)
  • novo no site ........ novidades.html (as primeiras da lista)
  • da loja ............. produtos.js (os que têm destaque: true)
  • a carta do mês e o vídeo: revista-cartas.json, preenchido DEPOIS do directo do dia 1 (sem ele, a revista diz que
    a carta sai no directo — nunca se inventa uma tiragem).
Uso: python3 revista-gerar.py 2026-12   → revista-dezembro-2026.html  (molde: eclipses-2027.html)"""
import os, re, sys, json, html, datetime, calendar, glob
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"; e = html.escape
ANO, MES = map(int, (sys.argv[1] if len(sys.argv) > 1 else "2026-12").split("-"))
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
NOME_MES = MESES[MES - 1]; SLUG = f"revista-{NOME_MES.replace('ç', 'c')}-{ANO}"; URL = f"{SITE}/{SLUG}"
EDICAO = (ANO - 2026) * 12 + MES - 11          # Dezembro de 2026 = n.º 1

CORPOS = ["Sol", "Lua", "Mercúrio", "Vénus", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno", "Plutão", "Nodo Norte", "Quíron", "Lilith"]
SIG = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
SIG_BR = {"Carneiro": "Áries", "Gémeos": "Gêmeos", "Caranguejo": "Câncer", "Balança": "Libra"}
SLUGS = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"]
GLIFO = "♈♉♊♋♌♍♎♏♐♑♒♓"
nomeS = lambda s: SIG[s] + (f" ({SIG_BR[SIG[s]]})" if SIG[s] in SIG_BR else "")
FASES = [("🌑", "Lua Nova"), ("🌓", "Quarto Crescente"), ("🌕", "Lua Cheia"), ("🌗", "Quarto Minguante")]
ASP = {0: "conjunção", 60: "sextil", 90: "quadratura", 120: "trígono", 180: "oposição"}
LENTOS = {5, 6, 7, 8, 9}                        # Júpiter…Plutão: os aspectos que contam para o mês

# ---------- o céu (efemérides do próprio site) ----------
EF = json.load(open(f"efemerides/{ANO}.json"))
B = datetime.datetime(ANO, 1, 1)
quando = lambda m: B + datetime.timedelta(minutes=m)
G = []                                          # longitudes por dia (graus), reconstruídas das diferenças
for a in EF["g"]:
    o, v = [], 0
    for k, x in enumerate(a): v = x if k == 0 else v + x; o.append((v % 1296000) / 3600)
    G.append(o)
def lon(i, m):                                  # longitude do corpo i no minuto m (interpolação diária)
    k, f = divmod(m, 1440); k = int(k); a = G[i][k]; b = G[i][min(k + 1, len(G[i]) - 1)]
    d = (b - a + 540) % 360 - 180; return (a + d * f / 1440) % 360
def hora(t):                                    # Portugal (UTC no inverno, UTC+1 no verão aprox.) e Brasília (UTC-3)
    pt = t + datetime.timedelta(hours=1 if 4 <= t.month <= 10 else 0); br = t - datetime.timedelta(hours=3)
    return f"{pt:%d/%m às %H:%M} em Portugal · {br:%H:%M} no Brasil"
ev = [x for x in EF["ev"] if quando(x[1]).month == MES]
luas, ingressos, estacoes, aspectos, eclipses = [], [], [], [], []
for x in ev:
    t = quando(x[1])
    if x[0] == "f": luas.append((t, x[2], int(lon(1, x[1]) // 30)))
    elif x[0] == "i" and x[2] not in (1, 10, 12): ingressos.append((t, x[2], x[3]))
    elif x[0] == "s": estacoes.append((t, x[2], x[3], int(lon(x[2], x[1]) // 30)))
    elif x[0] == "a" and (x[2] in LENTOS or x[3] in LENTOS) and x[4] in (0, 90, 120, 180): aspectos.append((t, x[2], x[3], x[4]))
    elif x[0] in ("es", "el"): eclipses.append((t, x[0], int(lon(1, x[1]) // 30)))
dia1 = (datetime.datetime(ANO, MES, 1) - B).days
retro = [CORPOS[i] for i in range(2, 10) if (EF["r"][dia1] >> i) & 1]
sol_ini = int(G[0][dia1] // 30)

# ---------- os 12 signos: o que o céu do mês toca em cada um ----------
porSigno = {s: [] for s in range(12)}
for t, f, s in luas: porSigno[s].append(f"{FASES[f][1]} no seu signo a {t:%d/%m}")
for t, c, s in ingressos: porSigno[s].append(f"{CORPOS[c]} entra no seu signo a {t:%d/%m}")
for t, c, d, s in estacoes: porSigno[s].append(f"{CORPOS[c]} fica {'retrógrado' if d == 'R' else 'directo'} no seu signo a {t:%d/%m}")
for t, k, s in eclipses: porSigno[s].append(f"eclipse no seu signo a {t:%d/%m}")
_sol_sai = next((t for t, c, s in ingressos if c == 0), None)
sol_txt = {sol_ini: "o Sol está no seu signo" + (f" até {_sol_sai - datetime.timedelta(days=1):%d/%m}" if _sol_sai else "") + ": é o mês dos seus aniversários"}
porSigno = {s: [x if not x.startswith("Sol entra") else x + ": começa o mês dos seus aniversários" for x in v] for s, v in porSigno.items()}

# ---------- numerologia: o Mês Pessoal ----------
js = open("numerologia-2027-textos.js", encoding="utf-8").read()
PAL = [None] + re.findall(r'"([^"]*)"', re.search(r"const MES = \[(.*?)\];", js, re.S).group(1))
reduz = lambda n: n if n <= 9 else reduz(sum(map(int, str(n))))
mes_pessoal = [(n, reduz(n + reduz(MES))) for n in range(1, 10)]

# ---------- famosos que fazem anos no mês ----------
_f = open("famosos-ceu-dados.js", encoding="utf-8").read(); FAM = json.loads(_f[_f.index("["):_f.rindex("]") + 1])
fam, por = [], {"PT": 0, "BR": 0}
for p in FAM:
    if p[2] == MES and p[7] != "politica" and por.get(p[5], 9) < 6: fam.append(p); por[p[5]] += 1
fam.sort(key=lambda p: p[3])

# ---------- notícias do mês, novidades e loja ----------
noticias = [n for n in json.load(open("noticias/lista.json")) if n.get("pub", "").startswith(f"{ANO}-{MES:02d}")][:8]
nov = re.findall(r'<a class="nova" href="(/[^"]+)"><span class="eti">[^<]*</span><span class="ico">([^<]*)</span><span><b>([^<]+)</b><small>([^<]*)</small>', open("novidades.html", encoding="utf-8").read())[:8]
loja = []
for bloco in re.findall(r"\{[^{}]*?destaque:\s*true[^{}]*?\}", open("produtos.js", encoding="utf-8").read(), re.S):
    g = lambda k: (re.search(k + r':\s*"([^"]*)"', bloco) or [None, ""])[1]
    loja.append((g("nome"), g("preco"), g("pagina") or "/loja", g("foto")))   # sem preço = pedirInfo (os rituais, decisão dele): mostra «Pedir informações»
loja = loja[:4]

# ---------- a carta do mês (só depois do directo) ----------
cartas = json.load(open("revista-cartas.json")) if os.path.exists("revista-cartas.json") else {}
cm = cartas.get(f"{ANO}-{MES:02d}")

# ================= a página: uma REVISTA que se folheia (27/11, ele: «capa e as pessoas poderem andar pelas páginas
# como se fosse mesmo uma revista») =================
# Todo o texto está no HTML (o Google lê tudo); o revista-folhear.js só esconde as outras páginas e dá o virar.
# Sem JavaScript, as páginas aparecem umas por baixo das outras.
mes_t = NOME_MES.capitalize()
TITULO = f"Revista Genial · {mes_t} {ANO}: o céu, as luas, os signos e os números do mês"
DESC = f"A revista do mês do Genial Tarot: as luas de {NOME_MES} com hora de Portugal e do Brasil, o céu calculado, os 12 signos, o seu Mês Pessoal, os famosos do mês e a carta do Mestre Alberto."
partes = lambda L, n: [L[i:i + n] for i in range(0, len(L), n)] or [[]]
PAGS = []                                       # (id, título da página, título no índice ou None, html)
def pag(id_, tit, html_, indice=True): PAGS.append((id_, tit, tit if indice else None, html_))

# --- as rubricas ---
carta_h = (f'<p class="chave">{e(cm["carta"])}</p><p>{e(cm.get("texto", ""))}</p>' + (f'<p class="pergunta"><b>A pergunta para levar o mês inteiro</b>{e(cm["pergunta"])}</p>' if cm.get("pergunta") else "")
           if cm else f'<p class="chave">Revelada no directo de 1 de {NOME_MES}</p><p>No primeiro directo do mês, o Mestre Alberto tira a carta que dá o tom a {NOME_MES} para todos. A carta, a leitura e uma pergunta de <a href="/tarot-terapeutico">Tarot terapêutico</a> para levar o mês inteiro entram nesta página logo a seguir.</p><div class="verso"><img src="/cartas/verso-gt.webp" alt="O verso do baralho do Mestre Alberto: a carta do mês ainda por revelar" loading="lazy"></div>')
video_h = f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{e(cm["video"])}" title="O vídeo do mês" allowfullscreen loading="lazy"></iframe></div>' if cm and cm.get("video") else ""
pag("carta", "🃏 A carta do mês", carta_h + video_h)
pag("luas", f"🌙 As luas de {NOME_MES}", '<div class="cx luas">' + "".join(f'<div><span class="ic">{FASES[f][0]}</span><b>{FASES[f][1]} em {e(nomeS(s))}</b><small>{hora(t)}</small></div>' for t, f, s in luas) + '</div><p class="fonte">Calculadas com a Swiss Ephemeris. A de hoje: <a href="/lua">Calendário Lunar</a>.</p>')
ceu = sorted([(t, f"{CORPOS[c]} entra em {e(nomeS(s))}") for t, c, s in ingressos]
             + [(t, f"{CORPOS[c]} fica {'retrógrado' if d == 'R' else 'directo'} em {e(nomeS(s))}") for t, c, d, s in estacoes]
             + [(t, f"{CORPOS[a]} em {ASP[g]} com {CORPOS[b]}") for t, a, b, g in aspectos]
             + [(t, f"eclipse {'do Sol' if k == 'es' else 'da Lua'} em {e(nomeS(s))}") for t, k, s in eclipses])
for k, bloco in enumerate(partes(ceu, 10)):
    intro = f'<p>Retrógrados no dia 1: <b>{", ".join(retro) or "nenhum"}</b>. O Sol começa o mês em {e(nomeS(sol_ini))}.</p>' if k == 0 else ""
    pag(f"ceu{k + 1}", "🪐 O céu do mês" + (f" ({k + 1})" if len(ceu) > 10 else ""), intro + '<ul class="ceu-mes">' + "".join(f"<li><b>{t:%d/%m}</b>{x}</li>" for t, x in bloco) + '</ul>' + ('<p class="fonte">Tudo ao minuto nas <a href="/efemerides">Efemérides</a>.</p>' if k == len(partes(ceu, 10)) - 1 else ""), indice=k == 0)
for k, bloco in enumerate(partes(list(range(12)), 6)):
    pag(f"signos{k + 1}", f"♈ Os 12 signos em {NOME_MES}" + (" (1)" if k == 0 else " (2)"), '<div class="sgs">' + "".join(
        f'<a href="/signo/{SLUGS[s]}"><span class="gl">{GLIFO[s]}</span><span><b>{e(nomeS(s))}</b><small>{e("; ".join(([sol_txt[s]] if s in sol_txt else []) + porSigno[s]) or "um mês sem acontecimentos no seu signo: é o céu dos outros que o(a) move")}.</small></span></a>' for s in bloco) + '</div>', indice=k == 0)
pag("numeros", "🔢 O seu Mês Pessoal", f'<p>Em {NOME_MES}, a vibração muda de pessoa para pessoa: soma-se o seu Ano Pessoal de {ANO} ao número do mês. Não sabe o seu? <a href="/numerologia-2027">Calcule aqui</a>.</p><div class="cx num">'
    + "".join(f'<div><b>Ano {n}</b><span class="big">{m}</span><small>{e(PAL[m])}</small></div>' for n, m in mes_pessoal) + '</div>'
    + (('<p class="fonte">E 2027? O seu Ano Pessoal: ' + " · ".join(f'<a href="/ano-pessoal-{n}-2027">{n}</a>' for n in range(1, 10)) + '</p>') if ANO == 2026 else ""))
for k, bloco in enumerate(partes(fam, 6)):
    pag(f"famosos{k + 1}", f"🎂 Fazem anos em {NOME_MES}" + (f" ({k + 1})" if len(fam) > 6 else ""), '<ul class="famosos">' + "".join(f'<li><b>{"🇵🇹" if p[5] == "PT" else "🇧🇷"} {e(p[0])}</b><small>{p[3]:02d}/{p[2]:02d}/{p[1]} · {e(p[4])}</small></li>' for p in bloco) + '</ul>' + ('<p class="fonte">Com quem partilha o seu céu? <a href="/famosos-ceu">Famosos com o seu céu</a>.</p>' if k == len(partes(fam, 6)) - 1 else ""), indice=k == 0)
pag("noticias", "📰 Notícias do céu", ('<ul class="ceu-mes noticias">' + "".join(f'<li><a href="/noticias/{e(n["slug"])}">{e(n["titulo"])}</a></li>' for n in noticias) + "</ul>") if noticias else f'<p>As notícias do céu de {NOME_MES} entram nesta página à medida que saem, de manhã e à tarde.</p><p>Até lá, veja as últimas em <a href="/noticias-do-ceu">Notícias do Céu</a>.</p>')
# 27/11 (ele): «mais novidades do site na revista» — 8 novidades em 2 páginas, as ferramentas grátis e a loja com fotos
for k, bloco in enumerate(partes(nov, 4)):
    pag(f"novo{k + 1}", "✨ Novo no site" + (f" ({k + 1})" if len(nov) > 4 else ""), '<div class="cx novas">' + "".join(f'<a class="nv" href="{h}"><span class="ic">{i}</span><b>{e(t)}</b><small>{e(d)}</small></a>' for h, i, t, d in bloco) + '</div>' + ('<p class="fonte"><a href="/novidades">Todas as novidades</a></p>' if k == len(partes(nov, 4)) - 1 else ""), indice=k == 0)
GRATIS = [("/tarot-gratis", "🃏", "Tarot grátis", "Tire as suas cartas agora"), ("/o-meu-dia", "☀️", "O meu dia", "O seu signo, a sua carta e a Lua de hoje"),
          ("/horoscopo-de-amanha", "🌙", "A antevisão do Mestre", "O céu de amanhã para os 12 signos"), ("/numerologia-2027", "🔢", "O seu Ano 2027", "A calculadora da numerologia"),
          ("/ascendente", "✨", "O seu Ascendente", "Sol, Lua e Ascendente ao minuto"), ("/carta-da-semana", "✉️", "A Carta da Semana", "Todos os domingos")]
pag("gratis", "🎁 Grátis no site", '<div class="cx novas">' + "".join(f'<a class="nv" href="{h}"><span class="ic">{i}</span><b>{e(t)}</b><small>{e(d)}</small></a>' for h, i, t, d in GRATIS) + '</div>')
pag("loja", "🛍️ Da loja", '<div class="cx lojas">' + "".join(f'<a class="lj" href="{pg}">' + (f'<img src="/{e(ft)}" alt="" loading="lazy">' if ft else "") + f'<b>{e(n)}</b>' + (f'<span class="preco">{e(pr)}</span>' if pr.strip() else '<span class="info">💬 Pedir informações</span>') + '</a>' for n, pr, pg, ft in loja) + '</div><p style="text-align:center"><a class="cta" href="/loja">Ver a loja</a></p>')
pag("fim", "📩 Até ao próximo mês", f'<p>A revista do mês seguinte sai três dias antes de o mês acabar e vai-se completando ao longo do mês, com as notícias do céu e a carta do directo. As edições anteriores ficam todas guardadas.</p><p style="text-align:center"><a class="cta" href="/vip">Receber a revista no email</a></p><p style="text-align:center"><a class="cta azul" href="/consulta-de-tarot-online">Marcar uma consulta</a></p><p class="fonte">Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.</p>', indice=False)

# --- a capa e o índice ---
chamadas = []
nova = next(((t, s) for t, f, s in luas if f == 0), None); cheia = next(((t, s) for t, f, s in luas if f == 2), None)
if nova: chamadas.append(f"Lua Nova em {nomeS(nova[1])} a {nova[0]:%d/%m}")
if cheia: chamadas.append(f"Lua Cheia em {nomeS(cheia[1])} a {cheia[0]:%d/%m}")
for t, c, d, s in estacoes:
    if c in (5, 6) or d == "R": chamadas.append(f"{CORPOS[c]} {'retrógrado' if d == 'R' else 'directo'} em {SIG[s]}"); break
chamadas.append("O seu Mês Pessoal"); chamadas.append("Fazem anos: " + ", ".join(p[0] for p in fam[:3] if len(p[0]) < 20)[:60])
capa = f"""<div class="capa-in"><div class="topo-capa"><span>N.º {EDICAO}</span><span>{mes_t} {ANO}</span><span>Grátis</span></div>
  <div class="sub-mast">a revista do Tarot, dos astros e dos números</div>
  <span class="carimbo">A carta<br>do mês</span>
  <div class="meio-capa"><div class="chamadas-cx"><div class="manchete">{e(chamadas[0]) if chamadas else ""}</div><ul class="chamadas">{"".join(f"<li>{e(c)}</li>" for c in chamadas[1:])}</ul></div>
  <figure class="foto-arco"><img src="/revista-mestre.webp" alt="Mestre Alberto com a carta do Sol" width="540" height="720"><figcaption>Mestre Alberto</figcaption></figure></div>
  <div class="pe-capa"><b>Mestre Alberto</b> · genialtarot.com</div></div>"""
indice = '<ol class="indice">' + "".join(f'<li><a href="#{i}" data-ir="{i}">{e(t)}</a><span>{n + 3}</span></li>' for n, (i, _t, t, _h) in enumerate(PAGS) if t) + '</ol>'
folhas = [("capa", None, capa), ("indice", "Nesta edição", indice + f'<p class="fonte">Toque nas setas, deslize com o dedo ou use as teclas ← →.</p>')] + [(i, t, h) for i, t, _ix, h in PAGS]
livro = "".join(f'<article class="folha{ {"capa": " capa", "fim": " contracapa"}.get(i, "") }" id="{i}" data-n="{n + 1}">' + (f'<h2>{e(t)}</h2>' if t else "") + (f'<div class="corpo">{h}</div>' if i == "capa" else f'<div class="corpo vidro">{h}</div>') + (f'<div class="rodape-pag"><span><b>Genial</b> · {mes_t} {ANO}</span><span>{n + 1} / {len(folhas)}</span></div>' if i != "capa" else "") + ('<button class="vira" type="button" aria-label="Virar a página"></button>' if n < len(folhas) - 1 else "") + '</article>' for n, (i, t, h) in enumerate(folhas))
corpo = f"""<h1 class="so-leitores">Revista Genial · {mes_t} {ANO}</h1>
  <div class="leitura-barra"><a href="/" id="voltar-site">← <b>Voltar ao site</b></a><span><button type="button" id="musica" aria-pressed="true" aria-label="Música">🎵 Música</button> <button type="button" id="som-folha" aria-pressed="true" aria-label="Som das páginas">🔊 Som</button></span></div>
  <div class="revista" id="revista" data-total="{len(folhas)}">{livro}</div>
  <nav class="comandos" aria-label="Folhear a revista"><button id="ant" aria-label="Página anterior">‹</button><span id="pagnum">1 / {len(folhas)}</span><button id="seg" aria-label="Página seguinte">›</button></nav>
  <p class="arquivo"><a href="/revista">Todas as edições</a></p>"""

ld = {"@context": "https://schema.org", "@type": "Article", "headline": TITULO, "description": DESC, "image": f"{SITE}/og-image.jpg", "inLanguage": "pt",
      "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"}, "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE},
      "datePublished": f"{ANO}-{MES:02d}-01", "dateModified": datetime.date.today().isoformat(), "mainEntityOfPage": URL}
molde = open("eclipses-2027.html", encoding="utf-8").read()
ESTILO = re.search(r"<style>.*?</style>", molde, re.S).group(0)
FIM = molde[molde.index("<footer>"):]
extra = open("revista.css", encoding="utf-8").read()
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
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{ESTILO}
<style>
{extra}
</style>
</head>
<body class="pag-revista leitura">
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
  {corpo}
{FIM.replace('<script src="/vip-faixa.js" defer></script>', '<script src="/revista-folhear.js" defer></script>\n<script src="/vip-faixa.js" defer></script>')}"""
saida = sys.argv[2] if len(sys.argv) > 2 else f"{SLUG}.html"
open(saida, "w", encoding="utf-8").write(pagina)
print(saida, f"· {len(folhas)} páginas · {len(luas)} luas, {len(ceu)} no céu, {len(fam)} famosos, {len(noticias)} notícias, {len(nov)} novidades, {len(loja)} da loja, carta={'sim' if cm else 'por revelar'}")

# ---------- o arquivo: /revista com todas as edições (a mais nova primeiro) ----------
eds = []
for f in glob.glob("revista-*-*.html"):
    m = re.match(r"revista-([a-z]+)-(\d{4})\.html$", f)
    if not m: continue
    nm = [x.replace("ç", "c") for x in MESES].index(m.group(1)) + 1 if m.group(1) in [x.replace("ç", "c") for x in MESES] else 0
    if nm: eds.append((int(m.group(2)), nm, f[:-5]))
eds.sort(reverse=True)
lista = "".join(f'<a class="ed" href="/{s_}" target="_blank" rel="noopener"><span class="n">N.º {(a_ - 2026) * 12 + m_ - 11}</span><b>{MESES[m_ - 1].capitalize()} {a_}</b><small>Folhear →</small></a>' for a_, m_, s_ in eds)
arq = pagina.split("<body")[0]
arq = re.sub(r"<title>.*?</title>", "<title>Revista Genial — todas as edições · Mestre Alberto</title>", arq, flags=re.S)
arq = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Todas as edições da Revista Genial, a revista do mês do Genial Tarot: o céu, as luas, os signos e os números de cada mês."', arq)
arq = arq.replace(f'href="{URL}"', f'href="{SITE}/revista"').replace(f'content="{URL}"', f'content="{SITE}/revista"')
arq = re.sub(r'<script type="application/ld\+json">.*?</script>', "", arq, flags=re.S)
arq += f"""<body><div class="estrelas" aria-hidden="true"></div><div class="caixa"><header class="topo"><a class="backlink" href="/">genialtarot.com</a></header>
<section class="heroi"><span class="selo">Revista do mês</span><h1><span class="az">Revista Genial</span></h1><p class="sub">Uma edição por mês, no dia 1: o céu, as luas, os 12 signos, os números e a carta do Mestre Alberto.</p></section>
<section class="cartao"><div class="eds">{lista}</div></section>
<style>.eds{{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(12rem,1fr))}}.ed{{display:flex;flex-direction:column;gap:.3rem;text-decoration:none;color:var(--texto);padding:1.4rem 1rem;border-radius:.5rem 1rem 1rem .5rem;border:2px solid var(--ouro);background:radial-gradient(120% 80% at 50% 30%,oklch(0.42 0.17 300),oklch(0.16 0.06 285));box-shadow:inset 10px 0 14px -10px #000a,0 14px 30px #0008}}.ed .n{{font-size:.75rem;letter-spacing:.2em;color:var(--ouro);font-weight:800}}.ed b{{font-family:var(--titulo);font-size:1.5rem}}.ed small{{color:var(--suave)}}</style>
{FIM}"""
open("revista.html", "w", encoding="utf-8").write(arq)
print("revista.html ·", len(eds), "edição(ões)")

# ---------- a página inicial: a revista SEMPRE em destaque (27/11, ele: «Ler a nossa revista mensal»), pequena ----------
if eds:
    a_, m_, s_ = eds[0]
    bloco = f"""<!-- revista-casa:inicio --><section class="rv-casa" aria-label="A revista do mês"><style>
.rv-casa{{max-width:46rem;margin:0 auto 1.4rem;padding:0}}.rv-casa a.rv{{display:flex;gap:1rem;align-items:center;text-decoration:none;color:#f7f0fb;padding:.9rem;border-radius:1.2rem;
background:linear-gradient(135deg,#2a1245,#170830);border:1px solid #f2c96b99;box-shadow:0 14px 40px #0008}}
.rv-casa .rv-capa{{flex:none;width:6.4rem;aspect-ratio:1094/1438;border-radius:.3rem .7rem .7rem .3rem;background:url(/revista-capa-mini.webp) center/cover;box-shadow:inset 6px 0 8px -6px #000a,0 8px 18px #000a;transform:rotate(-3deg);border:1px solid #f2c96b}}
.rv-casa small{{display:block;font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:#f2c96b;font-weight:800}}.rv-casa b{{display:block;font-family:Cinzel,Georgia,serif;font-size:clamp(1.15rem,4.5vw,1.5rem);color:#ffe2a0;margin:.2rem 0}}
.rv-casa span.t{{display:block;font-size:.92rem;color:#d9cbe9;line-height:1.4}}.rv-casa .rv-bt{{display:inline-block;margin-top:.6rem;padding:.55rem 1.1rem;border-radius:999px;font-weight:800;color:#2a1245;background:linear-gradient(135deg,#ffe2a0,#f2c96b 55%,#d9a441)}}
.rv-casa .rv-ant{{display:block;text-align:right;margin-top:.4rem;font-size:.85rem;color:#d9cbe9}}.rv-casa .rv-ant a{{color:#d9cbe9}}</style>
<a class="rv" href="/{s_}" target="_blank" rel="noopener"><span class="rv-capa" role="img" aria-label="Capa da Revista Genial"></span><span><small>📖 Revista do mês · N.º {(a_ - 2026) * 12 + m_ - 11}</small><b>Revista Genial · {MESES[m_ - 1].capitalize()} {a_}</b>
<span class="t">As luas, o céu do mês, os 12 signos, o seu Mês Pessoal e a carta do Mestre. Folheie como uma revista.</span><span class="rv-bt">Ler a nossa revista mensal →</span></span></a>
<span class="rv-ant"><a href="/carta-da-semana">✉️ A Carta da Semana</a> · <a href="/revista">Edições anteriores →</a></span></section><!-- revista-casa:fim -->"""
    ih = open("index.html", encoding="utf-8").read()
    novo = re.sub(r"<!-- revista-casa:inicio -->.*?<!-- revista-casa:fim -->", lambda _m: bloco, ih, count=1, flags=re.S)
    if novo != ih: open("index.html", "w", encoding="utf-8").write(novo); print("index.html · a revista em destaque:", s_)
