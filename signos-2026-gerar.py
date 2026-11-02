#!/home/ricardo/.venv-astro/bin/python
# -*- coding: utf-8 -*-
"""Gera signos-2026.html (02/11/2026, pedido dele: «faz já a página dos signos 2026» — «astrologia signos 2026»,
«melhores signos 2026», «previsões signos 2026» e «signos 2026» a subir no Google Trends em PT e BR).

As datas vêm do Swiss Ephemeris (calculadas aqui, hora de Lisboa); o texto de cada signo sai das casas solares
(mesmas palavras do Horóscopo do Dia, ~/horoscopo_site_textos.py). Os «melhores signos» seguem uma regra dita na página:
Júpiter no signo ou em trígono (mesmo elemento) = ano favorecido; Saturno em conjunção, quadratura ou oposição = ano exigente.
Molde: horoscopo-do-dia.html (head, som, faixa VIP, vivo.js, rodapé).
    ~/.venv-astro/bin/python ~/site-genialtarot/signos-2026-gerar.py
"""
import sys, os, re, json, datetime
sys.argv = sys.argv[:1]
sys.path.insert(0, "/home/ricardo")
import horoscopo_site as H
T = H.T
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PT = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
BR = ["Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem", "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
SLUG = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"]
nome = lambda s: PT[s] + (f" ({BR[s]})" if BR[s] != PT[s] else "")
MES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
dt = lambda t: f"{t.astimezone(H.LX).day} de {MES[t.astimezone(H.LX).month - 1]}"

# ── o céu de 2026, calculado ──
a, b = datetime.datetime(2026, 1, 1, tzinfo=H.LX), datetime.datetime(2027, 1, 1, tzinfo=H.LX)
ev, d = [], a
while d < b:
    e = d + datetime.timedelta(days=1)
    ev += [x for x in H.estacoes_e_ingressos(d, e) if x["astro"] != "Sol"]
    d = e
def um(astro, tipo, s=None):
    return next(x for x in ev if x["astro"] == astro and x["tipo"] == tipo and (s is None or x["s"] == s))
SAT = um("Saturno", "ingresso", 0); NEP = um("Neptuno", "ingresso", 0); URA = um("Úrano", "ingresso", 2)
JUP = um("Júpiter", "ingresso", 4); JUP_R = um("Júpiter", "retro"); SAT_D = um("Saturno", "directo"); NEP_D = um("Neptuno", "directo")
MARTE_VIR = um("Marte", "ingresso", 5)
retros = [(x, next(y for y in ev if y["astro"] == x["astro"] and y["tipo"] == "directo" and y["t"] > x["t"]))
          for x in ev if x["tipo"] == "retro" and x["astro"] in ("Mercúrio", "Vénus")]
# eclipses
sw = H.swe
def jd2dt(j):
    y, m, dd, h = sw.revjul(j)
    return datetime.datetime(y, m, dd, tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=h)
ecl, j = [], sw.julday(2026, 1, 1)
while True:
    r = sw.sol_eclipse_when_glob(j, sw.FLG_SWIEPH, 0); t = r[1][0]
    if t > sw.julday(2027, 1, 1): break
    tipo = "total" if r[0] & sw.ECL_TOTAL else "anular" if r[0] & sw.ECL_ANNULAR else "parcial"
    ecl.append((jd2dt(t), "do Sol", tipo, int(sw.calc_ut(t, sw.SUN)[0][0] // 30))); j = t + 1
j = sw.julday(2026, 1, 1)
while True:
    r = sw.lun_eclipse_when(j, sw.FLG_SWIEPH, 0); t = r[1][0]
    if t > sw.julday(2027, 1, 1): break
    tipo = "total" if r[0] & sw.ECL_TOTAL else "parcial" if r[0] & sw.ECL_PARTIAL else "penumbral"
    ecl.append((jd2dt(t), "da Lua", tipo, int(sw.calc_ut(t, sw.MOON)[0][0] // 30))); j = t + 1
ecl.sort()

# ── melhores signos (a regra está escrita na página) ──
def nota(s):
    n, porque = 0, []
    if (s - 3) % 4 == 0: n += 2; porque.append(f"Júpiter em Caranguejo até {dt(JUP['t'])} favoreceu os signos de Água")
    if (s - 4) % 4 == 0: n += 2; porque.append(f"Júpiter em Leão desde {dt(JUP['t'])} favorece os signos de Fogo")
    if s in (0, 3, 6, 9): n -= 1; porque.append("Saturno em Carneiro pediu esforço aos signos cardinais")
    return n, porque
rank = sorted(range(12), key=lambda s: (-nota(s)[0], s))
GRUPOS = ["🌟 Os mais favorecidos", "⚖️ Ano de altos e baixos", "🌿 Ano estável", "🧱 Ano de construção"]
def grupo(s):
    n = nota(s)[0]
    return GRUPOS[0] if n >= 2 else GRUPOS[1] if n == 1 else GRUPOS[2] if n == 0 else GRUPOS[3]

def texto(s):
    c = lambda sg: T.CASA[H.casa(sg, s)]
    k = lambda sg: T.CURTA[H.casa(sg, s)]   # depois de «em»: a forma curta (na família, no romance)
    t = [f"Saturno entrou em Carneiro a {dt(SAT['t'])} e passou a pedir disciplina e responsabilidade em {k(0)}.",
         f"Júpiter, o planeta das oportunidades, passou a primeira metade do ano em Caranguejo, a abrir portas em {k(3)}; a {dt(JUP['t'])} mudou para Leão e o crescimento passou para {c(4)}.",
         f"Úrano entrou em Gémeos a {dt(URA['t'])}: surpresas e vontade de mudar em {k(2)}."]
    e = next(x for x in ecl if x[1] == "do Sol" and x[2] == "total")
    t.append(f"O eclipse total do Sol de {dt(e[0])}, em {PT[e[3]]}, marcou um recomeço em {k(e[3])}.")
    return [re.sub(r"\bem (a|o|os|as) ", lambda m: {"a": "na ", "o": "no ", "os": "nos ", "as": "nas "}[m.group(1)], x) for x in t]

# ── HTML ──
src = open("horoscopo-do-dia.html", encoding="utf-8").read()
cabeca = src[:src.index("<style>")]
estilo = re.search(r"<style>.*?</style>", src, re.S).group(0)
som = src[src.index('<button id="audio-fab"'):src.index('<div class="estrelas"')]
rodape = src[src.index("<footer>"):src.index("</footer>") + 9]
musica = src[src.index("<script>\n/* 🎵 28/10/2026"):src.index('<script src="/vip-faixa.js"')]
URL = "https://genialtarot.com/signos-2026"
TIT = "Signos 2026: o ano de cada signo e os melhores signos · Mestre Alberto"
DESC = "Signos 2026: o que o céu real trouxe a cada signo — Saturno e Neptuno em Carneiro, Júpiter em Leão, os eclipses — e quais os melhores signos do ano."
cabeca = re.sub(r"<title>.*?</title>", f"<title>{TIT}</title>", cabeca)
cabeca = cabeca.replace("https://genialtarot.com/horoscopo-do-dia", URL)
cabeca = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + DESC, cabeca)
cabeca = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + DESC, cabeca)
cabeca = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>Signos 2026 — Mestre Alberto", cabeca)
FAQ = [("Quais foram os melhores signos de 2026?", f"Pela regra clássica de Júpiter, os signos de Água (Caranguejo, Escorpião e Peixes) na primeira metade do ano e os de Fogo (Leão, Carneiro e Sagitário) desde {dt(JUP['t'])}. Peixes, Escorpião, Leão e Sagitário juntam isso a um Saturno sem tensão, e por isso aparecem no topo."),
       ("O que marcou a astrologia de 2026?", f"A entrada de Neptuno ({dt(NEP['t'])}) e de Saturno ({dt(SAT['t'])}) em Carneiro, a de Úrano em Gémeos ({dt(URA['t'])}) e a passagem de Júpiter para Leão ({dt(JUP['t'])}). São planetas lentos: ficam anos no mesmo signo, por isso 2026 abriu um ciclo novo."),
       ("Quantos eclipses houve em 2026?", "Quatro: " + "; ".join(f"{dt(x[0])}, eclipse {x[2]} {x[1]} em {PT[x[3]]}" for x in ecl) + "."),
       ("O que falta acontecer até ao fim de 2026?", f"Marte entra em Virgem a {dt(MARTE_VIR['t'])}, Saturno volta a andar para a frente a {dt(SAT_D['t'])}, Neptuno a {dt(NEP_D['t'])}, e Júpiter fica retrógrado em Leão a {dt(JUP_R['t'])}, a preparar 2027."),
       ("Como é que estas datas foram calculadas?", "Com o Swiss Ephemeris, o mesmo cálculo usado pelos astrónomos, em hora de Portugal. As leituras de cada signo contam as casas a partir do signo solar; para uma leitura pessoal é preciso o mapa com a hora de nascimento.")]
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "name": TIT, "description": DESC, "url": URL, "inLanguage": "pt", "dateModified": datetime.date.today().isoformat(),
     "isPartOf": {"@type": "WebSite", "name": "Genial Tarot", "url": "https://genialtarot.com/"},
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": "https://genialtarot.com/sobre"}},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": "https://genialtarot.com/"},
                                                  {"@type": "ListItem", "position": 2, "name": "Signos 2026", "item": URL}]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]}]}
E = lambda x: x.replace("&", "&amp;").replace("<", "&lt;")
datas = [(SAT["t"], f"♄ Saturno entra em Carneiro"), (NEP["t"], "♆ Neptuno entra em Carneiro"), (URA["t"], "♅ Úrano entra em Gémeos (Gêmeos)"),
         (JUP["t"], "♃ Júpiter entra em Leão")] + [(x[0], f"{'🌑' if x[1] == 'do Sol' else '🌕'} Eclipse {x[2]} {x[1]} em {PT[x[3]]}") for x in ecl] + \
        [(r[0]["t"], f"℞ {r[0]['astro']} retrógrado até {dt(r[1]['t'])}") for r in retros]
datas.sort(key=lambda z: z[0])
cards = []
for s in range(12):
    n, porque = nota(s)
    selo = grupo(s)
    cards.append(f'''<article class="signo" id="{SLUG[s]}"><div class="cab"><img class="gli" src="signos/{s:02d}.webp" alt="{PT[s]}" width="72" height="72" loading="lazy"><div><div class="nome">{nome(s)}</div><div class="ene">{selo}</div></div></div>
{"".join(f"<p>{E(x)}</p>" for x in texto(s))}
<div class="dica"><b>👉 E em 2027?</b><a href="/horoscopo-2027-{SLUG[s]}">O horóscopo 2027 de {PT[s]}</a> · <a href="/signo/{SLUG[s]}">tudo sobre o signo</a></div></article>''')
html = cabeca + estilo + "\n" + f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False)}\n</script>\n</head>\n<body>\n' + som + '''<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo"><a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a></header>
  <section class="heroi">
    <img class="foto-mestre" src="mestre-diario.jpg" alt="Mestre Alberto" width="120" height="120" />
    <div><span class="selo">✦ Os 12 signos ✦ 2026</span></div>
    <h1>Os <span class="az">Signos</span> em 2026</h1>
    <p class="sub">O que o céu verdadeiro de 2026 trouxe a cada signo, os melhores signos do ano e o que ainda falta até dezembro.</p>
  </section>
  <section class="cartao">
    <h2>O céu de 2026 em datas</h2>
    <ul class="ceu">''' + "".join(f"<li><b>{dt(t)}</b> · {E(x)}</li>" for t, x in datas) + '''</ul>
    <p class="fonte">Calculado com o Swiss Ephemeris (zodíaco tropical), em hora de Portugal.</p>
  </section>
  <section class="cartao">
    <h2>Os melhores signos de 2026</h2>
    <p style="font-family:var(--serifa);font-size:1.1rem;color:var(--lavanda);max-width:44rem;margin:0 auto 1rem;text-align:center">A regra clássica: Júpiter, o planeta das oportunidades, favorece o signo onde passa e os do mesmo elemento; Saturno pede mais esforço aos signos com quem faz tensão (conjunção, quadratura ou oposição). Em 2026 Júpiter esteve em Caranguejo e depois em Leão, e Saturno entrou em Carneiro.</p>
    <ul class="ceu">''' + "".join(f"<li><b>{g}:</b> {', '.join(nome(x) for x in rank if grupo(x) == g)}</li>" for g in GRUPOS if any(grupo(x) == g for x in rank)) + '''</ul>
    <p class="fonte">Porquê: ''' + E(f"Júpiter em Caranguejo até {dt(JUP['t'])} favoreceu os signos de Água; Júpiter em Leão desde então favorece os de Fogo; Saturno em Carneiro pede esforço aos signos cardinais (Carneiro, Caranguejo, Balança, Capricórnio). Quem tem Júpiter a favor e Saturno a pesar fica com um ano de altos e baixos.") + '''</p>
  </section>
  <section class="cartao">
    <h2>2026 signo a signo</h2>
    <nav class="atalhos">''' + "".join(f'<a href="#{SLUG[s]}"><img src="signos/{s:02d}.webp" alt="" width="28" height="28">{PT[s]}</a>' for s in range(12)) + '''</nav>
    <div class="grelha">''' + "".join(cards) + f'''</div>
  </section>
  <section class="cartao">
    <h2>O que ainda falta de 2026</h2>
    <ul class="ceu"><li><b>{dt(MARTE_VIR['t'])}</b> · ♂ Marte entra em Virgem</li><li><b>{dt(SAT_D['t'])}</b> · ♄ Saturno volta a andar para a frente</li><li><b>{dt(NEP_D['t'])}</b> · ♆ Neptuno volta a andar para a frente</li><li><b>{dt(JUP_R['t'])}</b> · ♃ Júpiter fica retrógrado em Leão, até 2027</li></ul>
    <p class="fonte">Veja o dia a dia no <a href="/horoscopo-do-dia">Horóscopo do Dia</a> e a semana no <a href="/horoscopo-semanal">Horóscopo Semanal</a>; o ano que vem em <a href="/horoscopo-2027">Horóscopo 2027</a> e <a href="/cor-do-ano-2027">a cor do ano 2027</a>.</p>
  </section>
  <section class="cartao chamada">
    <h2>E o <span class="az">seu</span> 2027?</h2>
    <p>O signo solar é só o começo. Numa consulta olho para o seu mapa completo e para o ano que aí vem.</p>
    <div class="botoes"><a class="btn" href="/horoscopo-2027">✨ Horóscopo 2027</a><a class="btn ouro" href="loja.html#cat-consultas">🔮 Marcar uma consulta</a></div>
  </section>
</div>
<!-- seo-extra -->
<section class="faq-genial" style="max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6"><h2 style="margin-top:0">Perguntas frequentes</h2>''' + \
    "".join(f'<h3 style="font-size:1.05rem;margin:1rem 0 .3rem">{E(q)}</h3><p style="margin:0">{E(r)}</p>' for q, r in FAQ) + "</section>\n" + rodape + "\n" + musica + \
    '<script src="/vip-faixa.js" defer></script>\n<script src="/vivo.js" defer></script>\n</body>\n</html>\n'
open("signos-2026.html", "w", encoding="utf-8").write(html)
print("signos-2026.html", len(html), "ranking:", [PT[s] for s in rank])
