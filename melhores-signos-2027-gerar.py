#!/home/ricardo/.venv-astro/bin/python
# -*- coding: utf-8 -*-
"""Gera melhores-signos-2027.html (02/11/2026, pedido dele: «faz a página dos melhores signos 2027» — «melhores signos 2026»
subiu +24 700 % no Trends; em novembro a procura passa para o ano seguinte).

Céu de 2027 calculado aqui (Swiss Ephemeris, hora de Lisboa). A regra dos «melhores» é a mesma da /signos-2026 e está dita na
página: Júpiter no signo ou em trígono (mesmo elemento) = +2; Saturno em conjunção/quadratura/oposição = −1.
Os textos de cada signo usam as casas solares (palavras do Horóscopo do Dia) e batem com as páginas /horoscopo-2027-<signo>.
Molde: horoscopo-do-dia.html.
    ~/.venv-astro/bin/python ~/site-genialtarot/melhores-signos-2027-gerar.py
"""
import sys, os, re, json, datetime
sys.argv = sys.argv[:1]
sys.path.insert(0, "/home/ricardo")
import horoscopo_site as H
T, sw = H.T, H.swe
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ANO = 2027
PT = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
BR = ["Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem", "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
SLUG = ["carneiro", "touro", "gemeos", "caranguejo", "leao", "virgem", "balanca", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"]
ELEM = ["Fogo", "Terra", "Ar", "Água"]
nome = lambda s: PT[s] + (f" ({BR[s]})" if BR[s] != PT[s] else "")
MES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
dt = lambda t: f"{t.astimezone(H.LX).day} de {MES[t.astimezone(H.LX).month - 1]}"
E = lambda x: x.replace("&", "&amp;").replace("<", "&lt;")
em = lambda x: re.sub(r"\bem (a|o|os|as) ", lambda m: {"a": "na ", "o": "no ", "os": "nos ", "as": "nas "}[m.group(1)], x)

# ── o céu do ano ──
a, b = datetime.datetime(ANO, 1, 1, tzinfo=H.LX), datetime.datetime(ANO + 1, 1, 1, tzinfo=H.LX)
ev, d = [], a
while d < b:
    e = d + datetime.timedelta(days=1)
    ev += [x for x in H.estacoes_e_ingressos(d, e) if x["astro"] != "Sol"]
    d = e
meio = a.replace(month=1, day=2)
s_jup0 = H.sig(H.lon("Júpiter", meio)[0]); s_sat = H.sig(H.lon("Saturno", meio)[0])
JUP = next(x for x in ev if x["astro"] == "Júpiter" and x["tipo"] == "ingresso")
s_jup1 = JUP["s"]
assert all(H.sig(H.lon("Saturno", a + datetime.timedelta(days=k))[0]) == s_sat for k in range(0, 365, 5)), "Saturno muda de signo no ano"
SAT_R = next(x for x in ev if x["astro"] == "Saturno" and x["tipo"] == "retro")
SAT_D = next(x for x in ev if x["astro"] == "Saturno" and x["tipo"] == "directo")
def jd2dt(j):
    y, m, dd, h = sw.revjul(j)
    return datetime.datetime(y, m, dd, tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=h)
ecl, j = [], sw.julday(ANO, 1, 1)
while True:
    r = sw.sol_eclipse_when_glob(j, sw.FLG_SWIEPH, 0); t = r[1][0]
    if t > sw.julday(ANO + 1, 1, 1): break
    ecl.append((jd2dt(t), "do Sol", "total" if r[0] & sw.ECL_TOTAL else "anular" if r[0] & sw.ECL_ANNULAR else "parcial", int(sw.calc_ut(t, sw.SUN)[0][0] // 30)))
    j = t + 1
ECL = next(x for x in ecl if x[2] == "total")
JD = dt(JUP["t"])

def nota(s):
    n, porque = 0, []
    if (s - s_jup0) % 4 == 0: n += 2; porque.append(f"Júpiter em {PT[s_jup0]} até {JD} favorece os signos de {ELEM[s_jup0 % 4]}")
    if (s - s_jup1) % 4 == 0: n += 2; porque.append(f"Júpiter em {PT[s_jup1]} desde {JD} favorece os signos de {ELEM[s_jup1 % 4]}")
    if (s - s_sat) % 3 == 0: n -= 1; porque.append(f"Saturno em {PT[s_sat]} o ano inteiro pede esforço aos signos {['cardinais', 'fixos', 'mutáveis'][s_sat % 3]}")
    return n, porque
GRUPOS = ["🌟 Os mais favorecidos", "⚖️ Ano de altos e baixos", "🌿 Ano estável", "🧱 Ano de construção"]
def grupo(s):
    n = nota(s)[0]
    return GRUPOS[0] if n >= 2 else GRUPOS[1] if n == 1 else GRUPOS[2] if n == 0 else GRUPOS[3]
rank = sorted(range(12), key=lambda s: (-nota(s)[0], s))

def melhor_fase(s):
    if (s - s_jup0) % 4 == 0 and (s - s_jup1) % 4 == 0: return "o ano inteiro"
    if (s - s_jup0) % 4 == 0: return f"de janeiro a {JD}"
    if (s - s_jup1) % 4 == 0: return f"de {JD} ao fim do ano"
    return None

def texto(s):
    k = lambda sg: T.CURTA[H.casa(sg, s)]
    c = lambda sg: T.CASA[H.casa(sg, s)]
    t = [f"Júpiter, o planeta das oportunidades, passa por {PT[s_jup0]} até {JD} e abre portas em {k(s_jup0)}; depois muda para {PT[s_jup1]} e o crescimento passa para {c(s_jup1)}.",
         f"Saturno fica o ano inteiro em {PT[s_sat]} e pede disciplina e paciência em {k(s_sat)}" + (" . Como é no seu próprio signo, o ano fica mais sério e mais construtivo." if s == s_sat else "."),
         f"O eclipse total do Sol de {dt(ECL[0])}, em {PT[ECL[3]]}, marca um recomeço em {k(ECL[3])}."]
    f = melhor_fase(s)
    t.append(f"A sua melhor fase de 2027: {f}." if f else "Sem Júpiter no seu elemento, 2027 recompensa a constância mais do que a sorte: o que construir com calma fica.")
    return [em(x) for x in t]

src = open("horoscopo-do-dia.html", encoding="utf-8").read()
cabeca = src[:src.index("<style>")]
estilo = re.search(r"<style>.*?</style>", src, re.S).group(0)
som = src[src.index('<button id="audio-fab"'):src.index('<div class="estrelas"')]
rodape = src[src.index("<footer>"):src.index("</footer>") + 9]
musica = src[src.index("<script>\n/* 🎵 28/10/2026"):src.index('<script src="/vip-faixa.js"')]
URL = "https://genialtarot.com/melhores-signos-2027"
TIT = "Melhores Signos de 2027: os mais favorecidos · Mestre Alberto"
fav = [PT[s] for s in rank if grupo(s) == GRUPOS[0]]
DESC = f"Os melhores signos de 2027 pelo céu real: {', '.join(fav[:-1])} e {fav[-1]} à frente, com Júpiter a favor. A melhor fase de cada signo e porquê."
assert len(TIT) <= 70 and 110 <= len(DESC) <= 160, (len(TIT), len(DESC))
cabeca = re.sub(r"<title>.*?</title>", f"<title>{TIT}</title>", cabeca).replace("https://genialtarot.com/horoscopo-do-dia", URL)
cabeca = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + DESC, cabeca)
cabeca = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + DESC, cabeca)
cabeca = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>Os Melhores Signos de 2027 — Mestre Alberto", cabeca)
FAQ = [("Quais são os melhores signos de 2027?", f"Pela regra clássica de Júpiter: {', '.join(fav[:-1])} e {fav[-1]}. Júpiter passa por {PT[s_jup0]} até {JD} (favorece os signos de {ELEM[s_jup0 % 4]}) e depois por {PT[s_jup1]} (favorece os de {ELEM[s_jup1 % 4]}), e nenhum destes quatro tem Saturno em tensão."),
       ("Quais são os signos com mais sorte em 2027?", f"Na astrologia, a ideia de sorte liga-se sobretudo a Júpiter, o planeta das oportunidades. Por essa regra, os mais favorecidos em 2027 são {', '.join(fav[:-1])} e {fav[-1]}. Isto mostra uma tendência do céu, não uma garantia de resultados."),
       ("Qual é o signo com o ano mais difícil em 2027?", f"Nenhum signo tem um ano «mau». Os que têm mais trabalho são os que Saturno toca sem a ajuda de Júpiter: {', '.join(nome(s) for s in rank if grupo(s) == GRUPOS[3])}. Saturno pede esforço, mas o que se constrói com ele dura."),
       ("Quando muda Júpiter de signo em 2027?", f"A {JD}, de {PT[s_jup0]} para {PT[s_jup1]}. É a data que separa a melhor fase dos signos de {ELEM[s_jup0 % 4]} (antes) da dos signos de {ELEM[s_jup1 % 4]} (depois)."),
       ("Isto vale para o meu Ascendente?", "Vale a pena ler também o seu Ascendente: muitas pessoas reconhecem-se mais nele. Para saber ao certo como 2027 toca o seu mapa, é preciso a data, a hora e o local de nascimento."),
       ("Como é que isto foi calculado?", "As datas vêm do Swiss Ephemeris, o mesmo cálculo usado pelos astrónomos, em hora de Portugal. A regra dos melhores signos é a tradicional de Júpiter e Saturno, explicada na página.")]
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "name": TIT, "description": DESC, "url": URL, "inLanguage": "pt", "dateModified": datetime.date.today().isoformat(),
     "isPartOf": {"@type": "WebSite", "name": "Genial Tarot", "url": "https://genialtarot.com/"},
     "author": {"@type": "Person", "name": "Mestre Alberto", "url": "https://genialtarot.com/sobre"}},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": "https://genialtarot.com/"},
                                                  {"@type": "ListItem", "position": 2, "name": "Horóscopo 2027", "item": "https://genialtarot.com/horoscopo-2027"},
                                                  {"@type": "ListItem", "position": 3, "name": "Melhores signos de 2027", "item": URL}]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]}]}
cards = []
for s in rank:
    cards.append(f'''<article class="signo" id="{SLUG[s]}"><div class="cab"><img class="gli" src="signos/signo-{SLUG[s]}.webp" alt="Ilustração do signo {nome(s)} — Genial Tarot" width="72" height="72" loading="lazy"><div><div class="nome">{nome(s)}</div><div class="ene">{grupo(s)}</div></div></div>
{"".join(f"<p>{E(x)}</p>" for x in texto(s))}
<div class="dica"><b>👉 O ano completo</b><a href="/horoscopo-2027-{SLUG[s]}">Horóscopo 2027 de {PT[s]}: amor, dinheiro e trabalho</a></div></article>''')
html = cabeca + estilo + "\n" + f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False)}\n</script>\n</head>\n<body>\n' + som + f'''<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo"><a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a></header>
  <section class="heroi">
    <img class="foto-mestre" src="mestre-diario.jpg" alt="Mestre Alberto" width="120" height="120" />
    <div><span class="selo">🌟 Os 12 signos ✦ 2027</span></div>
    <h1>Os <span class="az">Melhores Signos</span> de 2027</h1>
    <p class="sub">Quem tem Júpiter a favor, quem tem Saturno a pedir esforço, e a melhor fase do ano para cada signo, a partir do céu real de 2027.</p>
  </section>
  <section class="cartao">
    <h2>Os melhores signos de 2027</h2>
    <ul class="ceu">''' + "".join(f"<li><b>{g}:</b> {', '.join(nome(x) for x in rank if grupo(x) == g)}</li>" for g in GRUPOS if any(grupo(x) == g for x in rank)) + f'''</ul>
    <p style="font-family:var(--serifa);font-size:1.1rem;color:var(--lavanda);max-width:44rem;margin:1rem auto 0;text-align:center">A regra: Júpiter, o planeta das oportunidades, favorece o signo onde passa e os do mesmo elemento; Saturno pede mais esforço aos signos com quem faz tensão. Em 2027 Júpiter está em {PT[s_jup0]} até {JD} e depois em {PT[s_jup1]}; Saturno fica o ano todo em {PT[s_sat]}. Quem tem as duas coisas fica com um ano de altos e baixos.</p>
  </section>
  <section class="cartao">
    <h2>As datas que mudam tudo</h2>
    <ul class="ceu"><li><b>{dt(ecl[0][0])}</b> · 🌑 Eclipse {ecl[0][2]} do Sol em {PT[ecl[0][3]]}</li><li><b>{JD}</b> · ♃ Júpiter entra em {PT[s_jup1]}: a sorte muda de elemento</li><li><b>{dt(ECL[0])}</b> · 🌑 Eclipse total do Sol em {PT[ECL[3]]}</li><li><b>{dt(SAT_R['t'])}</b> · ♄ Saturno fica retrógrado em {PT[s_sat]} (até {dt(SAT_D['t'])})</li></ul>
    <p class="fonte">Calculado com o Swiss Ephemeris (zodíaco tropical), em hora de Portugal.</p>
  </section>
  <section class="cartao">
    <h2>Signo a signo, do mais favorecido para o que mais constrói</h2>
    <nav class="atalhos">''' + "".join(f'<a href="#{SLUG[s]}"><img src="signos/signo-{SLUG[s]}.webp" alt="" width="28" height="28">{PT[s]}</a>' for s in range(12)) + '''</nav>
    <div class="grelha">''' + "".join(cards) + '''</div>
  </section>
  <section class="cartao chamada">
    <h2>E o <span class="az">seu</span> 2027?</h2>
    <p>O signo solar dá a tendência; o seu mapa dá o pormenor. Numa consulta olho para o seu ano inteiro, mês a mês.</p>
    <div class="botoes"><a class="btn" href="/horoscopo-2027">✨ Horóscopo 2027</a><a class="btn" href="/signos-2026">↩️ Como foi 2026</a><a class="btn ouro" href="loja.html#cat-consultas">🔮 Marcar uma consulta</a></div>
  </section>
</div>
<!-- seo-extra -->
<section class="faq-genial" style="max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6"><h2 style="margin-top:0">Perguntas frequentes</h2>''' + \
    "".join(f'<h3 style="font-size:1.05rem;margin:1rem 0 .3rem">{E(q)}</h3><p style="margin:0">{E(r)}</p>' for q, r in FAQ) + "</section>\n" + rodape + "\n" + musica + \
    '<script src="/vip-faixa.js" defer></script>\n<script src="/vivo.js" defer></script>\n</body>\n</html>\n'
open("melhores-signos-2027.html", "w", encoding="utf-8").write(html)
print("melhores-signos-2027.html", len(html), "|", len(TIT), len(DESC), "|", {g: [PT[s] for s in rank if grupo(s) == g] for g in GRUPOS})
