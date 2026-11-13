#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O Horóscopo de Amanhã POR SIGNO (13/11/2026, aprovado pelo Mestre Alberto: SEO de «horóscopo de amanhã», da análise
do 1.º no Google, em «Central Astrologia/🔭 Mercado e concorrência»). 12 endereços FIXOS, /horoscopo-de-amanha/<signo>,
cujo texto muda todos os dias. A família não cresce (Travão ao SEO, 12/11/2026).

Quem escreve o texto do dia é o WORKER (worker.js, amanhaSignoNoHtml), a cada pedido, como já faz no /horoscopo-de-amanha:
  · o resumo do dia = horoscopo-dia/<amanhã>.json (o mesmo ficheiro da página principal, feito pelo ~/horoscopo_site.py);
  · onde está cada planeta amanhã = ceu-dados.js (Swiss Ephemeris, ~/ceu-site-dados.py, renovado todos os meses pelo
    ~/site-ceu-rolante.sh) e a Lua = a casa «h» do próprio JSON;
  · a leitura de «planeta na casa N» = o banco do horóscopo semanal por signo (~/horoscopo_semanal_signo_textos.py) e
    os nomes das casas (~/horoscopo_site_textos.py), copiados para amanha-textos.js por este programa;
  · a carta de amanhã = um Arcano Maior do baralho do Mestre (/cartas/), tirado por um número estável do signo e do dia
    (como a carta do dia da app O Teu Céu), com a frase da app (o-teu-ceu-linguas.js, adaptada a «você» sem género).
Nada é inventado: sem números da sorte, sem promessas de saúde.

Este programa só faz duas coisas, e pode correr-se as vezes que se quiser (dá sempre o mesmo):
  1. amanha-textos.js — o banco de frases que o worker importa (não é servido: está no .assetsignore);
  2. horoscopo-de-amanha/<signo>.html — os 12 moldes (cabeça, migalhas, ligações, rodapé); o worker enche os
     elementos com id «am-…» com o dia de amanhã. Sem dados, fica o texto de reserva com ligação para a página geral.

    python3 gerar-amanha-signos.py
"""
import os, sys, re, json, html, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"
ESC = html.escape


def carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


P = carregar("sst", "/home/ricardo/horoscopo_semanal_signo_textos.py")
T = carregar("hst", "/home/ricardo/horoscopo_site_textos.py")

NOMES = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
SLUG = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"]
COM_BR = {0: "Carneiro (Áries)", 2: "Gémeos (Gêmeos)", 3: "Caranguejo (Câncer)", 6: "Balança (Libra)"}
SIMB = "♈♉♊♋♌♍♎♏♐♑♒♓"

# o banco é do semanal: três frases falam de «semana» e uma de «dias»; aqui é um dia só
DIA = [("o coração da semana está em casa", "o coração destes dias está em casa"),
       ("É semana de olhar", "É altura de olhar"),
       ("é boa semana para", "é boa altura para"),
       ("Bons dias para recados", "Boa altura para recados")]


def ao_dia(t):
    for a, b in DIA: t = t.replace(a, b)
    assert "semana" not in t, t
    return t


PLANETAS = ["Sol", "Mercúrio", "Vénus", "Marte", "Júpiter", "Saturno"]
PC = {n: {h: ao_dia(P.PC[n][h]) for h in range(1, 13)} for n in PLANETAS}
LONGO = {n: {h: P.LONGO[n][h] for h in range(1, 13)} for n in ("Júpiter", "Saturno")}
LUA = {h: ao_dia(P.LUA_CASA[h]) for h in range(1, 13)}

# os 22 Arcanos Maiores do baralho do Mestre (as imagens de /cartas/ e as páginas /arcano-NN-…)
CARTAS = sorted(f[:-5] for f in os.listdir("cartas") if re.match(r"^\d\d-.*\.webp$", f))
assert len(CARTAS) == 22, CARTAS
ARC_NOMES = ["O Louco", "O Mago", "A Sacerdotisa", "A Imperatriz", "O Imperador", "O Hierofante", "Os Enamorados", "O Carro", "A Força",
             "O Eremita", "A Roda da Fortuna", "A Justiça", "O Enforcado", "A Morte", "A Temperança", "O Diabo", "A Torre", "A Estrela",
             "A Lua", "O Sol", "O Julgamento", "O Mundo"]
for c in CARTAS: assert os.path.exists(f"arcano-{c}.html"), c
# a frase da carta do dia da app (o-teu-ceu-linguas.js, carta_dia em português); três diziam «atenta», «justa», «a prende»
LG = open("o-teu-ceu-linguas.js", encoding="utf-8").read()
_i = LG.index("carta_dia: [")
CARTA_DIA = json.loads(LG[_i + len("carta_dia: "): LG.index("]", _i) + 1])
assert len(CARTA_DIA) == 22
CARTA_DIA = [t.replace("Esteja atenta às oportunidades", "Fique atento às oportunidades que aparecem")
              .replace("Seja justa consigo e com os outros", "Use de justiça consigo e com os outros")
              .replace("Repare no que a prende", "Repare no que lhe prende os passos") for t in CARTA_DIA]
for t in CARTA_DIA: assert not re.search(r"\b(atenta|justa|a prende)\b", t), t

ELEM_SIGNO = [P.REGENTE[s][1] for s in range(12)]

dados = {
    "PC": PC, "LONGO": LONGO, "LUA": LUA, "RETRO": {n: P.RETRO[n] for n in PLANETAS if n in P.RETRO},
    "CASA": {h: T.CASA[h] for h in range(1, 13)}, "CURTA": {h: T.CURTA[h] for h in range(1, 13)},
    "REGENTE": {s: list(P.REGENTE[s]) for s in range(12)}, "ELEMENTO": P.ELEMENTO, "MODO_FRASE": P.MODO_FRASE,
    "ELEM_SIGNO": ELEM_SIGNO, "COM_BR": COM_BR,
    "CARTAS": CARTAS, "ARC_NOMES": ARC_NOMES, "CARTA_DIA": CARTA_DIA,
}
js = ("// Gerado por gerar-amanha-signos.py (13/11/2026). Não editar à mão: as frases vêm de ~/horoscopo_semanal_signo_textos.py,\n"
      "// ~/horoscopo_site_textos.py e o-teu-ceu-linguas.js. Usado pelo worker.js nas páginas /horoscopo-de-amanha/<signo>.\n"
      "export default " + json.dumps(dados, ensure_ascii=False, indent=0) + ";\n")
if not os.path.exists("amanha-textos.js") or open("amanha-textos.js", encoding="utf-8").read() != js:
    open("amanha-textos.js", "w", encoding="utf-8").write(js)

# ── os 12 moldes ──────────────────────────────────────────────────────────────────────────────────────────────────
MODELO = open("horoscopo-semanal-carneiro.html", encoding="utf-8").read()
CSS = MODELO[MODELO.index("<style>"): MODELO.index("</style>") + len("</style>")]
CASA_BLOCO = MODELO[MODELO.index("<!-- gt-casa:inicio -->"): MODELO.index("<!-- gt-casa:fim -->") + len("<!-- gt-casa:fim -->")]
CSS_MAIS = """<style>
.am p { margin: 0 0 .7rem; font-family: var(--serifa); font-size: 1.16rem; line-height: 1.5; color: var(--lavanda); }
.am h2 { margin-top: 0; }
.am h3 { font-family: var(--titulo); font-size: 1.08rem; color: var(--ouro); margin: 1.2rem 0 .35rem; }
.am h3:first-child { margin-top: 0; }
.am .pl { font-family: Inter, sans-serif; font-size: .78rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--suave); display: block; margin-bottom: .15rem; }
.am-carta { display: flex; gap: 1.1rem; align-items: center; flex-wrap: wrap; justify-content: center; }
.am-carta img { width: 8.5rem; height: auto; border-radius: .8rem; box-shadow: 0 10px 30px #0008; border: 1px solid oklch(0.85 0.13 88 / .4); }
.am-carta div { flex: 1 1 16rem; }
.am-mom { list-style: none; padding: 0; margin: 0; display: grid; gap: .5rem; }
.am-mom li { padding: .7rem .9rem; border-radius: .9rem; background: oklch(0.20 0.06 272 / .85); border: 1px solid var(--borda); color: var(--lavanda); }
.am-mom li b { color: var(--ouro); }
</style>"""


def pagina(s):
    nm, nb, sl = NOMES[s], COM_BR.get(s, NOMES[s]), SLUG[s]
    url = f"{SITE}/horoscopo-de-amanha/{sl}"
    tit = f"{nm} amanhã: horóscopo de amanhã para {nb} | Mestre Alberto"
    des = (f"O horóscopo de amanhã para {nb}: amor, dinheiro, trabalho, energia, o melhor momento do dia e a carta de amanhã, "
           f"lidos no céu calculado. Renova-se todos os dias. Mestre Alberto.")
    migalhas = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Horóscopo de amanhã", "item": SITE + "/horoscopo-de-amanha"},
        {"@type": "ListItem", "position": 3, "name": f"{nm} amanhã", "item": url}]}
    doze = "".join(f'<a href="/horoscopo-de-amanha/{SLUG[k]}"{" aria-current=\"page\"" if k == s else ""}><img src="/signos/{k:02d}.webp" alt="" width="40" height="40" loading="lazy">{NOMES[k]}</a>' for k in range(12))
    oposto = (s + 6) % 12
    reg, elem, modo = P.REGENTE[s]
    reserva = f'<p>O texto de amanhã para {ESC(nm)} está na <a href="/horoscopo-de-amanha#s{s}">página do horóscopo de amanhã</a>.</p>'
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<title>{ESC(tit)}</title>
<meta name="description" content="{ESC(des)}" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{ESC(tit)}" />
<meta property="og:description" content="{ESC(des)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/signos/signo-{sl}.webp" />
<meta property="og:image:alt" content="O signo de {ESC(nm)}, ilustração do Genial Tarot" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{json.dumps(migalhas, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
{CSS}
{CSS_MAIS}
</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/horoscopo-de-amanha"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>Horóscopo de Amanhã</a>
  </header>
  <section class="heroi">
    <img class="gli" src="/signos/{s:02d}.webp" alt="O signo de {ESC(nm)}" width="120" height="120" />
    <div><span class="selo" id="am-selo">{SIMB[s]}&#xFE0E; Amanhã</span></div>
    <h1 id="am-h1"><span class="az">{ESC(nm)}</span> amanhã{f" <small>({nb[len(nm) + 2:-1]})</small>" if s in COM_BR else ""}</h1>
    <p class="sub">Meu Querido Jardim de Almas! O dia de amanhã de {ESC(nm)}, lido no céu verdadeiro: o amor, o dinheiro, o trabalho, a energia, o melhor momento do dia e a carta que o baralho traz.</p>
  </section>
  <section class="cartao am" id="am-resumo">{reserva}</section>
  <section class="cartao am" id="am-areas"><h2>Amor, dinheiro, trabalho e energia</h2>{reserva}</section>
  <section class="cartao am" id="am-momento"><h2>O melhor momento de amanhã</h2>{reserva}</section>
  <section class="cartao am" id="am-carta"><h2>A carta de amanhã para {ESC(nm)}</h2><p>Tire a sua no <a href="/tarot-gratis">Tarot Grátis</a>.</p></section>
  <section class="cartao am" id="am-ceu"><h2>O céu de amanhã</h2><p>As posições dos planetas estão na <a href="/horoscopo-de-amanha">página do horóscopo de amanhã</a> e no <a href="/ceu-de-hoje">Céu de Hoje</a>.</p></section>
  <section class="cartao am">
    <h2>{ESC(nm)}: o signo por trás do dia</h2>
    <p>{ESC(nm)} é um signo de {elem}: {ESC(P.ELEMENTO[elem])}. {ESC(P.MODO_FRASE[modo])}. O astro que o rege é {ESC(T.ASTRO[reg][0] if reg in T.ASTRO else reg)}, e por isso o lugar onde ele anda pesa mais no seu dia do que nos outros signos.</p>
    <p>Este horóscopo é o do signo solar. As casas contam-se a partir de {ESC(nm)}: o mesmo céu toca áreas diferentes da vida em cada signo, e é isso que faz o dia de {ESC(nm)} diferente do dos outros onze. Se conhece o seu Ascendente, leia também o desse signo.</p>
  </section>
  <section class="cartao chamada">
    <h2>Quer saber o que amanhã guarda para <span class="az">si</span>?</h2>
    <p>O horóscopo fala de todo o signo de {ESC(nm)}. Numa consulta, o Mestre Alberto olha para a sua vida em particular: o seu mapa, as suas cartas e as perguntas que tem agora.</p>
    <p class="promessa">Eu tenho a sua resposta!</p>
    <div class="botoes"><a class="btn ouro" href="/consulta-de-tarot">🔮 Marcar uma consulta</a><a class="btn" href="/horoscopo-do-dia#s{s}">☀️ {ESC(nm)} hoje</a></div>
  </section>
  <section class="cartao">
    <h2>Amanhã para os outros signos</h2>
    <nav class="doze" aria-label="Horóscopo de amanhã dos 12 signos">{doze}</nav>
    <h2 style="margin-top:1.4rem;font-size:1.15rem">Mais sobre {ESC(nm)}</h2>
    <div class="ligas"><a href="/signo/{sl}">{ESC(nb)}: personalidade e hoje</a><a href="/horoscopo-de-amanha">Horóscopo de amanhã: os 12 signos</a><a href="/horoscopo-do-dia">Horóscopo do dia</a><a href="/horoscopo-semanal-{sl}">A semana de {ESC(nm)}</a><a href="/horoscopo-2027-{sl}">Horóscopo 2027 de {ESC(nm)}</a><a href="/ascendente-em-{sl}">Ascendente em {ESC(nm)}</a><a href="/horoscopo-de-amanha/{SLUG[oposto]}">O signo oposto: {ESC(NOMES[oposto])} amanhã</a></div>
  </section>
  <p class="fonte">Céu calculado com o Swiss Ephemeris (zodíaco tropical), para o dia de Portugal; horas de Portugal, com Brasília ao lado. As casas solares contam-se a partir de {ESC(nm)}. A página muda à meia-noite de Portugal: amanhã passa a ser o dia seguinte. São leituras simbólicas, para inspirar o seu dia: não substituem aconselhamento médico, psicológico, jurídico ou financeiro.</p>
</div>
{CASA_BLOCO}
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="/canais-oficiais">Canais oficiais</a> · <a href="/privacidade">Política de Privacidade</a> · <a href="/termos">Termos de Serviço</a>
</footer>
<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""


os.makedirs("horoscopo-de-amanha", exist_ok=True)
for s in range(12):
    f = f"horoscopo-de-amanha/{SLUG[s]}.html"
    novo = pagina(s)
    if not os.path.exists(f) or open(f, encoding="utf-8").read() != novo:
        open(f, "w", encoding="utf-8").write(novo)
print("amanha-textos.js e 12 páginas horoscopo-de-amanha/<signo>.html")
