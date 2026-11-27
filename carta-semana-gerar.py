#!/usr/bin/env python3
"""A Carta da Semana — a newsletter do Genial Tarot no site (27/11/2026, ele: «um newsletter que se atualize de forma automática
para a semana, ao domingo; para já fica no site, se der certo vemos o envio»). Ideia vinda da newsletter da Dani Silvestre.
Sai ao DOMINGO para a semana de segunda a domingo seguinte, e alimenta-se SOZINHA:
  • o céu da semana e os 12 signos ... horoscopo-semana/<segunda>.json (o Horóscopo Semanal, céu calculado)
  • famosos que fazem anos ......... famosos-ceu-dados.js (Wikidata), sem política
  • notícias do céu da semana ....... noticias/lista.json (os últimos 7 dias)
  • a revista do mês ............... a edição mais nova (revista-*-*.html)
  • da loja ......................... produtos.js (o 1.º com destaque: true)
Uso: python3 carta-semana-gerar.py [AAAA-MM-DD da segunda-feira]  (sem data: a próxima segunda, ou hoje se for segunda)
→ carta-da-semana-<segunda>.html + o arquivo carta-da-semana.html. Molde: eclipses-2027.html (como o resto do site)."""
import os, re, sys, json, glob, html, datetime
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"; e = html.escape
hoje = datetime.date.today()
seg = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else hoje + datetime.timedelta(days=(7 - hoje.weekday()) % 7)
dom = seg + datetime.timedelta(days=6); pub = seg - datetime.timedelta(days=1)
SLUG = f"carta-da-semana-{seg.isoformat()}"; URL = f"{SITE}/{SLUG}"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
SIG = ["Carneiro (Áries)", "Touro", "Gémeos (Gêmeos)", "Caranguejo (Câncer)", "Leão", "Virgem", "Balança (Libra)", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
SLUGS = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"]
SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
fd = lambda d: f"{d.day} de {MESES[d.month - 1]}"

W = json.load(open(f"horoscopo-semana/{seg.isoformat()}.json"))
def lisboa(ms):                                  # hora de Portugal (UTC no inverno, UTC+1 de abril a outubro, aprox.)
    t = datetime.datetime.fromtimestamp(int(ms) / 1000, datetime.timezone.utc).replace(tzinfo=None); return t + datetime.timedelta(hours=1 if 4 <= t.month <= 10 else 0)
def por(s):
    s = e(s)
    s = re.sub(r"\{S:(\d+)\}", lambda m: SIG[int(m.group(1))], s)
    s = re.sub(r"\{H:(\d+)\}", lambda m: f"{lisboa(m.group(1)):%H:%M}", s)
    s = re.sub(r"\{D:(\d+)\}", lambda m: (lambda d: ("no " if d.weekday() >= 5 else "na ") + SEMANA[d.weekday()])(lisboa(m.group(1))), s)
    return re.sub(r"\{W:(\d+)\}", lambda m: SEMANA[lisboa(m.group(1)).weekday()], s)
est = lambda x: "★" * int(round(x)) + "☆" * (5 - int(round(x)))
dia = lambda iso: (lambda d: f"{SEMANA[d.weekday()]}, {d.day}")(datetime.date.fromisoformat(iso))

_f = open("famosos-ceu-dados.js", encoding="utf-8").read(); FAM = json.loads(_f[_f.index("["):_f.rindex("]") + 1])
dias = {(seg + datetime.timedelta(days=i)).strftime("%m-%d") for i in range(7)}
fam, por_pais = [], {"PT": 0, "BR": 0}
for p in FAM:
    if f"{p[2]:02d}-{p[3]:02d}" in dias and p[7] != "politica" and por_pais.get(p[5], 9) < 3: fam.append(p); por_pais[p[5]] += 1
fam.sort(key=lambda p: (p[2], p[3]))
corte = (pub - datetime.timedelta(days=7)).isoformat()
noticias = [n for n in json.load(open("noticias/lista.json")) if corte <= n.get("pub", "")[:10] <= pub.isoformat()][:5]
revs = sorted(f for f in glob.glob("revista-*-*.html") if re.match(r"revista-[a-z]+-\d{4}\.html$", f))
mesnum = {m.replace("ç", "c"): i for i, m in enumerate(MESES)}
revs.sort(key=lambda f: (int(f[-9:-5]), mesnum.get(f.split("-")[1], 0)))
rev = revs[-1][:-5] if revs else None
loja = None
for bloco in re.findall(r"\{[^{}]*?destaque:\s*true[^{}]*?\}", open("produtos.js", encoding="utf-8").read(), re.S):
    g = lambda k: (re.search(k + r':\s*"([^"]*)"', bloco) or [None, ""])[1]
    loja = (g("nome"), g("preco"), g("pagina") or "/loja", g("descricao")); break

# ---------- o texto ----------
TITULO = f"A Carta da Semana · {fd(seg)} a {fd(dom)} de {dom.year}"
DESC = f"A newsletter do Genial Tarot para a semana de {fd(seg)} a {fd(dom)}: o céu da semana, os 12 signos com o melhor dia e a dica, os famosos que fazem anos e as novidades do Mestre Alberto."
ceu = "".join(f"<li>{por(l)}</li>" for l in W["ceu"]) or "<li>Uma semana calma no céu: sem Luas Nova ou Cheia nem planetas a mudar de signo.</li>"
signos = "".join(
    f'<article class="cs-sg"><a class="cab" href="/horoscopo-semanal#s{i}"><img src="/signos/{i:02d}.webp" alt="" width="44" height="44" loading="lazy"><span><b>{e(SIG[i])}</b><span class="est" aria-label="Energia {y["e"]} de 5">{est(y["e"])}</span></span></a>'
    f'<p class="k">{por(y["k"])}</p><p>{por(y["t"][0])}</p>'
    f'<p class="dias">✨ Melhor dia: <b>{dia(y["melhor"]["d"])}</b>' + (f' · ⚠️ Cuidado: {dia(y["cuidado"]["d"])}' if y.get("cuidado") else "") + '</p>'
    f'<p class="dica">👉 {por(y["d"])}</p></article>' for i, y in enumerate(W["s"]))
melhor = max(range(12), key=lambda i: W["s"][i]["e"])
corpo = f"""<section class="cs-capa"><div class="cs-sel">✉️ A Carta da Semana · Genial Tarot</div><h1>{fd(seg).capitalize()} a {fd(dom)}</h1>
  <p class="cs-ola">Olá! Esta é a sua carta de domingo: o céu que vem aí, o que pede ao seu signo e o melhor dia para cada um. Leia com calma e guarde a dica da semana.</p>
  <p class="cs-dest">A semana com mais energia: <b>{e(SIG[melhor])}</b> {est(W["s"][melhor]["e"])}</p></section>
  <section class="cartao texto"><h2>🪐 O céu da semana</h2><ul class="cs-ceu">{ceu}</ul><p class="fonte">Calculado com a Swiss Ephemeris, hora de Portugal. Tudo dia a dia no <a href="/horoscopo-semanal">Horóscopo Semanal</a>.</p></section>
  <section class="cartao texto"><h2>♈ A semana de cada signo</h2><div class="cs-sgs">{signos}</div></section>
  {('<section class="cartao texto"><h2>🎂 Fazem anos esta semana</h2><ul class="famosos">' + "".join(f'<li><b>{"🇵🇹" if p[5] == "PT" else "🇧🇷"} {e(p[0])}</b><small>{p[3]:02d}/{p[2]:02d} · {e(p[4])}</small></li>' for p in fam) + '</ul><p class="fonte">Com quem partilha o seu céu? <a href="/famosos-ceu">Famosos com o seu céu</a>.</p></section>') if fam else ""}
  {('<section class="cartao texto"><h2>📰 Notícias do céu desta semana</h2><ul class="cs-ceu">' + "".join(f'<li><a href="/noticias/{e(n["slug"])}">{e(n["titulo"])}</a></li>' for n in noticias) + '</ul></section>') if noticias else ""}
  <section class="cartao texto cs-dois">{f'<a class="cs-cx" href="/{rev}"><span class="rv-capa"></span><span><small>📖 A revista do mês</small><b>Folheie a Revista Genial</b><span>As luas, o céu, os signos e os números do mês.</span></span></a>' if rev else ""}
  {f'<a class="cs-cx" href="{loja[2]}"><span><small>🛍️ Da loja</small><b>{e(loja[0])}</b><span>{e(loja[1])}</span></span></a>' if loja else ""}</section>
  <section class="cartao texto" style="text-align:center"><h2>💬 Até domingo</h2><p>Se a sua pergunta não cabe numa carta para todos, o Mestre Alberto responde só para si.</p><p><a class="cta" href="/consulta-de-tarot-online">Marcar uma consulta</a></p><p class="fonte"><a href="/carta-da-semana">Todas as cartas da semana</a> · Leituras simbólicas, não substituem aconselhamento profissional.</p></section>"""
ld = {"@context": "https://schema.org", "@type": "Article", "headline": TITULO, "description": DESC, "image": f"{SITE}/revista-contracapa.webp", "inLanguage": "pt",
      "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"}, "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE},
      "datePublished": pub.isoformat(), "dateModified": hoje.isoformat(), "mainEntityOfPage": URL}
molde = open("eclipses-2027.html", encoding="utf-8").read()
ESTILO = re.search(r"<style>.*?</style>", molde, re.S).group(0)
FIM = molde[molde.index("<footer>"):]
extra = """<style>
.cs-capa{position:relative;z-index:1;max-width:46rem;margin:0 auto 1.6rem;padding:2rem 1.2rem 1.6rem;text-align:center;border-radius:1.4rem;border:1px solid #f2c96b99;
  background:linear-gradient(180deg,#160a2c55,#160a2cee 70%),url(/revista-contracapa-mini.webp) center 30%/cover;box-shadow:0 20px 50px #000a}
.cs-sel{font-size:.78rem;letter-spacing:.2em;text-transform:uppercase;color:#f2c96b;font-weight:800}
.cs-capa h1{font-family:var(--titulo);font-size:clamp(1.7rem,6vw,2.6rem);margin:.5rem 0;background:linear-gradient(180deg,#fff3c4,#f2c96b 55%,#c48a2c);-webkit-background-clip:text;background-clip:text;color:transparent}
.cs-ola{font-family:var(--serifa);font-size:1.2rem;color:#f2e6ff;max-width:34rem;margin:0 auto .8rem}.cs-dest{color:#ffe2a0;margin:0}
.cs-ceu{font-family:var(--serifa);font-size:1.08rem;color:var(--lavanda);padding-left:1.1rem}.cs-ceu li{margin:.3rem 0}
.cs-sgs{display:grid;gap:.8rem;grid-template-columns:repeat(auto-fit,minmax(17rem,1fr))}
.cs-sg{background:oklch(0.18 0.06 272 / .7);border:1px solid var(--borda);border-radius:1rem;padding:.8rem .9rem}
.cs-sg .cab{display:flex;gap:.6rem;align-items:center;text-decoration:none;color:var(--texto)}.cs-sg .cab img{border-radius:50%}
.cs-sg .cab b{display:block;font-family:var(--titulo)}.cs-sg .est{color:var(--ouro);font-size:.85rem}
.cs-sg p{font-size:.98rem !important;margin:.4rem 0 !important}.cs-sg .k{color:var(--ouro) !important;font-style:italic}.cs-sg .dias{font-family:Inter,sans-serif;font-size:.85rem !important;color:var(--suave) !important}
.cs-sg .dica{background:#f2c96b1a;border:1px solid #f2c96b55;border-radius:.6rem;padding:.4rem .6rem}
.famosos{list-style:none;padding:0;display:grid;gap:.5rem;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr))}.famosos li{background:var(--vidro);border:1px solid var(--borda);border-radius:.9rem;padding:.55rem .8rem}.famosos small{display:block;color:var(--suave);font-size:.8rem}
.cs-dois{display:grid;gap:.8rem;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr))}
.cs-cx{display:flex;gap:.8rem;align-items:center;text-decoration:none;color:var(--texto);background:oklch(0.18 0.06 272 / .7);border:1px solid #f2c96b77;border-radius:1rem;padding:.8rem}
.cs-cx small{display:block;color:#f2c96b;font-weight:800;letter-spacing:.1em;text-transform:uppercase;font-size:.72rem}.cs-cx b{display:block;font-family:var(--titulo);color:#ffe2a0;margin:.15rem 0}.cs-cx span span{color:var(--suave);font-size:.9rem}
.cs-cx .rv-capa{flex:none;width:4rem;aspect-ratio:1094/1438;border-radius:.2rem .5rem .5rem .2rem;background:url(/revista-capa-mini.webp) center/cover;border:1px solid #f2c96b;transform:rotate(-3deg)}
</style>"""
def pagina(titulo, desc, url, corpo_, ld_):
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}" />

<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{e(titulo)}" />
<meta property="og:description" content="{e(desc)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/revista-contracapa.webp" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
{('<script type="application/ld+json">' + json.dumps(ld_, ensure_ascii=False) + '</script>') if ld_ else ""}
{ESTILO}
{extra}
</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
  {corpo_}
{FIM}"""
open(f"{SLUG}.html", "w", encoding="utf-8").write(pagina(TITULO, DESC, URL, corpo, ld))
# ---------- o arquivo /carta-da-semana ----------
cartas = sorted((f[16:26] for f in glob.glob("carta-da-semana-????-??-??.html")), reverse=True)
lista = "".join(f'<a class="cs-cx" href="/carta-da-semana-{d}"><span><small>✉️ Semana de</small><b>{fd(datetime.date.fromisoformat(d))} a {fd(datetime.date.fromisoformat(d) + datetime.timedelta(days=6))}</b><span>{d[:4]}</span></span></a>' for d in cartas)
arq = f"""<section class="cs-capa"><div class="cs-sel">✉️ Genial Tarot</div><h1>A Carta da Semana</h1><p class="cs-ola">Todos os domingos, a carta para a semana que começa: o céu, os 12 signos, o melhor dia e a dica de cada um.</p>
  {f'<p><a class="cta" href="/{SLUG}">Ler a carta desta semana</a></p>' if cartas else ""}</section>
  <section class="cartao texto"><h2>Todas as cartas</h2><div class="cs-dois">{lista}</div></section>"""
open("carta-da-semana.html", "w", encoding="utf-8").write(pagina("A Carta da Semana — a newsletter do Genial Tarot", "Todas as Cartas da Semana do Genial Tarot: o céu da semana, os 12 signos, o melhor dia e a dica de cada um, todos os domingos.", f"{SITE}/carta-da-semana", arq, None))
print(f"{SLUG}.html · {len(W['ceu'])} no céu, {len(fam)} famosos, {len(noticias)} notícias, revista={rev}, loja={'sim' if loja else 'não'} · carta-da-semana.html ({len(cartas)})")
