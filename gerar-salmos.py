#!/usr/bin/env python3
"""Os Salmos dos 72 Anjos (16/11/2026): /salmos, /salmos/<signo> (12), /salmos/salmo-<n> (um por cada salmo distinto dos
72 Nomes), /salmo-do-dia.js (o salmo do dia pelo grau do Sol, usado em /salmos e no Horóscopo do Dia) e as ligações
para dentro (os-72-anjos, signo/*, horoscopo-do-dia, novidades). Aparência e molde copiados de gerar-anjos.py.

Fontes: anjos-textos.py (ANJOS, ordem = graus), anjos-mais-textos.py (livro e versículo de cada anjo; Hahaiah sem
salmo, Jabamiah = Génesis 1:1), arcanos-menores-textos.py (as cartas do site), salmos-textos.py (texto próprio de cada
página) e o texto bíblico da Bíblia Livre (CC BY 3.0 Brasil), ~/salmos-fonte/livre-19.json (getbible v2, livro 19),
numeração de Almeida. Limpeza: espaços e três gralhas (SENOR, SEHOR, «Que do levanta»).

Decanatos → cartas (Golden Dawn): cardinais 2-3-4, fixos 5-6-7, mutáveis 8-9-10; Fogo=Paus, Terra=Ouros, Ar=Espadas,
Água=Copas. Cada decanato (10°) = 2 anjos.

    python3 gerar-salmos.py              → tudo
    python3 gerar-salmos.py --ligacoes   → só volta a pôr as ligações nas páginas dos outros geradores (idempotente)
"""
import datetime, html, importlib.util, json, math, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
FONTE = os.path.expanduser("~/salmos-fonte/livre-19.json")


def _mod(f):
    s = importlib.util.spec_from_file_location(f.replace("-", "_")[:-3], f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


ANJOS = _mod("anjos-textos.py").ANJOS
MAIS = _mod("anjos-mais-textos.py").MAIS
MENORES = {c["slug"]: c for c in _mod("arcanos-menores-textos.py").MENORES}
_T = _mod("salmos-textos.py"); TXT_SIG, TXT_SAL = _T.SIGNO, _T.SALMO
E = html.escape
SITE = "https://genialtarot.com"
HOJE = "16/11/2026"
SIG = [("Carneiro","♈","carneiro"),("Touro","♉","touro"),("Gémeos","♊","gemeos"),("Caranguejo","♋","caranguejo"),("Leão","♌","leao"),("Virgem","♍","virgem"),
       ("Balança","♎","balanca"),("Escorpião","♏","escorpiao"),("Sagitário","♐","sagitario"),("Capricórnio","♑","capricornio"),("Aquário","♒","aquario"),("Peixes","♓","peixes")]
BR = {"carneiro": "Áries", "gemeos": "Gêmeos", "caranguejo": "Câncer", "balanca": "Libra"}   # como os títulos de signo/*.html
MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
NAIPE = ["paus", "ouros", "espadas", "copas"]          # Fogo, Terra, Ar, Água (ordem dos signos)
NUM = {2: "dois", 3: "tres", 4: "quatro", 5: "cinco", 6: "seis", 7: "sete", 8: "oito", 9: "nove", 10: "dez"}
slug = lambda n: n.lower()
def nome_sig(k, br=True): s, _, sl = SIG[k]; return f"{s} ({BR[sl]})" if br and sl in BR else s


# ─── texto bíblico ───
def limpa(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"(\w) -(\w)", r"\1-\2", t)                  # «Ouve -me» → «Ouve-me»
    t = re.sub(r"\s+([,.;:!?)])", r"\1", t)                 # «vencerem .» → «vencerem.»
    t = re.sub(r"([,;:!?])(?=[^\s\d)»])", r"\1 ", t)        # «bem?Levanta» → «bem? Levanta»
    t = re.sub(r"\.(?=[A-ZÀ-Ú])", ". ", t)                  # «Deus.Eles» → «Deus. Eles»
    return t.replace("SENOR", "SENHOR").replace("SEHOR", "SENHOR").replace("Que do levanta", "Que levanta")


LIVRE = {}; LETRA = {}
for _c in json.load(open(FONTE, encoding="utf-8"))["chapters"]:
    for _v in _c["verses"]:
        t = _v["text"]
        if _c["chapter"] == 119:                            # as estrofes vêm coladas ao 1.º versículo: «Álefe :Bem-aventurados…»
            m = re.match(r"\s*([^\s:]+)\s*:\s*", t)
            if m and _v["verse"] % 8 == 1: LETRA[_v["verse"]] = m.group(1); t = t[m.end():]
        LIVRE.setdefault(_c["chapter"], {})[_v["verse"]] = limpa(t)
assert len(LIVRE) == 150 and len(LIVRE[119]) == 176 and len(LETRA) == 22


def vers(cv):
    """'120:1-2' → (120, [1, 2])"""
    c, v = cv.split(":"); a = [int(x) for x in v.split("-")]
    return int(c), list(range(a[0], a[-1] + 1))


def citacao(cv): c, vs = vers(cv); return " ".join(LIVRE[c][v] for v in vs)


def vulgata(n):
    if n <= 8 or n >= 148: return None
    if n in (9, 10): return "9"
    if n <= 113: return str(n - 1)
    if n in (114, 115): return "113"
    if n == 116: return "114 e 115"
    if n <= 146: return str(n - 1)
    return "146 e 147"


# ─── Sol, datas (iguais a gerar-anjos.py) ───
def sol(d):
    n = (datetime.datetime(d.year, d.month, d.day, 12) - datetime.datetime(2000, 1, 1, 12)).days
    g = math.radians(357.528 + .9856003 * n); L = 280.46 + .9856474 * n
    return (L + 1.915 * math.sin(g) + .02 * math.sin(2 * g)) % 360


DIAS = {}
_d = datetime.date(2027, 3, 21)
for _ in range(365):
    if (_d.month, _d.day) != (2, 29): DIAS.setdefault(int(sol(_d) // 5), []).append(_d)
    _d += datetime.timedelta(days=1)
def _per(a, b):
    if a.month == b.month: return f"{a.day} a {b.day} de {MESES[a.month-1]}"
    return f"{a.day} de {MESES[a.month-1]} a {b.day} de {MESES[b.month-1]}"
def periodo(i): return _per(DIAS[i][0], DIAS[i][-1])
def periodo_dec(k, j): return _per(DIAS[k * 6 + j * 2][0], DIAS[k * 6 + j * 2 + 1][-1])


def carta(k, j):
    """carta numerada do decanato j (0..2) do signo k"""
    n = (2, 5, 8)[k % 3] + j
    return MENORES[f"carta-{NUM[n]}-de-{NAIPE[k % 4]}"]


# ─── cada anjo ───
AN = []
for i, a in enumerate(ANJOS):
    m = MAIS[a[0]]; k = i // 6
    sal = vers(m["cv"])[0] if m["livro"] == "Salmos" else None
    AN.append(dict(i=i, n=a[0], tema=a[1], k=k, g0=(i % 6) * 5, dec=(i % 6) // 2, livro=m["livro"], cv=m["cv"], sal=sal,
                   vs=vers(m["cv"])[1] if sal else [], txt=citacao(m["cv"]) if sal else None))
SALMOS = sorted({a["sal"] for a in AN if a["sal"]})
assert set(SALMOS) == set(TXT_SAL), set(SALMOS) ^ set(TXT_SAL)
POR_SAL = {s: [a for a in AN if a["sal"] == s] for s in SALMOS}

# ─── molde (de gerar-anjos.py) ───
BASE = open("anjo-da-guarda.html", encoding="utf8").read()
HEAD = BASE.split("</head>")[0]
ESTILOS = "\n".join(re.findall(r"(?s)<style>.*?</style>", HEAD))
TOPO = re.search(r'(?s)<body.*?(?=<section class="heroi">)', BASE).group(0)
CASA = re.search(r"(?s)<!-- gt-casa:inicio -->.*?<!-- gt-casa:fim -->", BASE).group(0)
ASA = re.search(r'(?s)<svg class="asa".*?</svg>', BASE).group(0)
EXTRA = """<style>
.vs p{margin:.3rem 0;line-height:1.6}.vs sup{color:var(--ouro);font-weight:700;font-size:.72rem;margin-right:.35rem}
.vs .eu{background:oklch(0.85 0.13 88 / .13);border-left:3px solid var(--ouro);padding:.35rem .7rem;border-radius:.4rem}
.vs h3{margin:1.2rem 0 .3rem;color:var(--ouro);font-size:1rem;letter-spacing:.08em}
.dec{display:grid;grid-template-columns:minmax(0,9rem) 1fr;gap:1.1rem;align-items:start}.dec img{width:100%;height:auto;display:block;border-radius:.7rem;box-shadow:0 8px 28px #0007}
.an2{margin:.2rem 0 1rem}.an2 h3{margin:.2rem 0;color:var(--ouro)}.an2 .mt{font-size:.85rem;color:var(--suave);margin:0 0 .4rem}
.an2 blockquote{margin:.4rem 0}.ref{font-size:.85rem}
.sgr{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,13rem),1fr));gap:.6rem}.sgr a{display:block;padding:.75rem .9rem;border-radius:.9rem;background:var(--vidro);border:1px solid var(--borda);color:inherit;text-decoration:none}
.sgr a:hover{border-color:var(--ouro)}.sgr b{color:var(--ouro);display:block}.sgr span{font-size:.85rem;color:var(--suave)}
.tab{width:100%;border-collapse:collapse;font-size:.92rem}.tab th,.tab td{text-align:left;padding:.45rem .4rem;border-bottom:1px solid var(--borda);vertical-align:top}.tab th{color:var(--suave);font-weight:600;font-size:.8rem}
.tabw{overflow-x:auto}.lic{font-size:.8rem;color:var(--suave);text-align:center}
#salmo-dia .sd-q{margin:.6rem 0}
.tab a,.an2 a,.ref a{color:var(--ouro)}.an2 h3 a{text-decoration:none}
@media(max-width:560px){.tab thead{display:none}.tab tr{display:block;padding:.55rem 0;border-bottom:1px solid var(--borda)}.tab td{display:block;border:0;padding:.12rem 0}
.tab td[data-l]::before{content:attr(data-l) ": ";color:var(--suave);font-size:.8rem}.dec{grid-template-columns:1fr}.dec img{max-width:9rem;margin:0 auto}}
</style>"""
AVISO = ('<p><small>Os 72 anjos e os seus versículos pertencem à tradição da Cabala e da angelologia, não à doutrina da Igreja, que desaconselha dar aos anjos nomes além de Miguel, Gabriel e Rafael. '
         'Os salmos, esses, são de todos: rezam-se na sinagoga e na Igreja há séculos. Aqui ficam como leitura simbólica e devocional: não prometem resultados nem substituem o médico ou outros profissionais.</small></p>')
LIC = ('<p class="lic">Texto bíblico: Bíblia Livre, licença <a href="https://creativecommons.org/licenses/by/3.0/br/" rel="license noopener">CC BY 3.0 Brasil</a> '
       '(numeração de Almeida; corrigimos espaçamentos e três gralhas de digitação).</p>')


def pagina(cam, tit, des, corpo, ld, fim=""):
    url = SITE + cam; t = E(tit, quote=True); d = E(des, quote=True)
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{t}</title>
<meta name="description" content="{d}" />

<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/og-image.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{ESTILOS}
{EXTRA}
</head>
{TOPO}{corpo}
{CASA}
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="/privacidade">Política de Privacidade</a> · <a href="/termos">Termos de Serviço</a>
</footer>
</div>
{fim}<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""


def heroi(h1, sub): return f'<section class="heroi">{ASA}<h1><span class="az">{h1}</span></h1><p class="sub">{sub}</p></section>'


def ld_art(cam, tit, des, migalhas, extra=()):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": tit, "description": des, "inLanguage": "pt-PT", "mainEntityOfPage": SITE + cam,
         "author": {"@type": "Person", "name": "Mestre Alberto"}, "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE},
         "dateModified": datetime.date.today().isoformat()},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": p + 1, "name": n, "item": SITE + c} for p, (n, c) in enumerate(migalhas)]},
        *extra]}


GERAR = "--ligacoes" not in sys.argv   # com --ligacoes não se reescreve nenhuma página nossa


def grava(f, s):
    if not GERAR: return
    os.makedirs(os.path.dirname(f) or ".", exist_ok=True)
    antigo = open(f, encoding="utf8").read() if os.path.exists(f) else None
    if antigo != s: open(f, "w", encoding="utf8").write(s)


def ref(a):
    c, vs = a["sal"], a["vs"]
    return f"Salmo {c}:{vs[0]}" + (f"-{vs[-1]}" if len(vs) > 1 else "")


def ln_sal(a): return f'/salmos/salmo-{a["sal"]}#v{a["vs"][0]}'


def sem_salmo(a):
    if a["livro"] == "Génesis":
        return (f"<p>{a['n']} é o único dos 72 que não tem um salmo: o versículo que a tradição lhe dá é o primeiro da Bíblia, "
                f"Génesis 1:1, «No princípio». Por isso não tem página de salmo.</p>")
    return (f"<p>Para {a['n']}, as listas publicadas não concordam no salmo (a tabela de onde tirámos os versículos mostra um e liga a outro), "
            f"e por isso não o indicamos. A oração da página do anjo serve no lugar dele.</p>")


tamanhos = []
def medir(cam, tit, des): tamanhos.append((len(tit), len(des), cam))

# ─── /salmos/<signo> ───
ORD = ["1.º", "2.º", "3.º"]
for k, (s, g, sl) in enumerate(SIG):
    sn = nome_sig(k)
    tit = f"Salmo do Signo de {sn} e os seus 6 anjos"
    des = f"Os 6 anjos de {sn} na tradição dos 72 Nomes: o versículo dos Salmos de cada um, os graus, as datas e a carta do Tarot de cada decanato."
    if len(des) > 158: des = f"Os 6 anjos de {sn} nos 72 Nomes: o versículo dos Salmos de cada um, as datas e a carta do Tarot de cada decanato."
    medir(f"/salmos/{sl}", tit, des)
    blocos = ""
    for j in range(3):
        c = carta(k, j)
        ans = ""
        for a in AN[k * 6 + j * 2:k * 6 + j * 2 + 2]:
            mt = f'n.º {a["i"]+1} dos 72 · {g} {s} {a["g0"]}° a {a["g0"]+5}° · {periodo(a["i"])}'
            if a["sal"]:
                corpo_a = (f'<blockquote class="ora-c">«{E(a["txt"])}»<footer><a href="{ln_sal(a)}">{ref(a)}</a></footer></blockquote>')
            else:
                corpo_a = sem_salmo(a)
            ans += (f'<div class="an2"><h3><a href="/anjo/{slug(a["n"])}">{a["n"]}</a></h3><p class="mt">{E(a["tema"])} · {mt}</p>{corpo_a}</div>')
        blocos += (f'  <section class="cartao" id="decanato-{j+1}"><h2>{ORD[j]} decanato de {s}: {j*10}° a {j*10+10}°</h2>'
                   f'<p class="sub" style="text-align:left;margin-top:0">{periodo_dec(k, j)} (datas de 2027)</p>'
                   f'<div class="dec"><a href="/{c["slug"]}"><img src="/cartas/menores/{c["img"]}" width="480" height="804" loading="lazy" alt="Carta {c["nome"]} do baralho do Mestre Alberto"></a>'
                   f'<div><p>Na correspondência da Golden Dawn, estes 10 graus pertencem ao <a href="/{c["slug"]}"><b>{c["nome"]}</b></a>: {", ".join(c["palavras"])}.</p>{ans}</div></div></section>\n')
    ant, seg = SIG[(k + 11) % 12], SIG[(k + 1) % 12]
    corpo = f"""{heroi("Salmos de " + s, f"{g} Os 6 anjos de {sn}, os seus versículos e as cartas dos decanatos")}
  <section class="cartao texto"><h2>O fio dos salmos de {s}</h2><p>{E(TXT_SIG[sl])}</p>
    <p>Na tradição dos 72 Nomes, cada anjo rege 5 graus do zodíaco e tem um versículo que se lê ao invocá-lo. {s} tem 30 graus, por isso tem seis anjos, dois em cada decanato de 10 graus. Quando o Sol passa pelos graus de um anjo, esse é o anjo dos dias e o seu versículo é o salmo do dia.</p></section>
{blocos}  <section class="cartao" style="text-align:center"><h2>Continuar a ler</h2>
    <div class="ligas"><a href="/salmos/{ant[2]}">← Salmos de {ant[0]}</a><a href="/salmos">Os salmos dos 12 signos</a><a href="/salmos/{seg[2]}">Salmos de {seg[0]} →</a></div>
    <div class="ligas"><a href="/signo/{sl}">{g} O signo de {s}</a><a href="/decanatos-{sl}">Os decanatos de {s}</a><a href="/os-72-anjos#{sl}">Os anjos de {s}</a></div>
    <p style="margin:.8rem 0 0"><a class="cta" href="/anjo-da-guarda#descobrir">Descobrir o meu anjo</a></p></section>
  <section class="cartao texto">{AVISO}{LIC}</section>"""
    grava(f"salmos/{sl}.html", pagina(f"/salmos/{sl}", tit, des, corpo, ld_art(f"/salmos/{sl}", tit, des, [("Salmos dos Anjos", "/salmos"), (f"Salmos de {s}", f"/salmos/{sl}")])))

# ─── /salmos/salmo-<n> ───
for p, n in enumerate(SALMOS):
    ans = POR_SAL[n]; nomes = [a["n"] for a in ans]
    lista = nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " e " + nomes[-1]
    sigs = []
    for a in ans:
        if nome_sig(a["k"], False) not in sigs: sigs.append(nome_sig(a["k"], False))
    lsig = sigs[0] if len(sigs) == 1 else ", ".join(sigs[:-1]) + " e " + sigs[-1]
    if len(ans) == 1: tit = f"Salmo {n}: texto completo e o anjo {nomes[0]} ({sigs[0]})"
    elif len(ans) == 2: tit = f"Salmo {n}: texto completo e os anjos {nomes[0]} e {nomes[1]}"
    else: tit = f"Salmo {n}: texto completo e os {len(ans)} anjos que o leem"
    inicio = LIVRE[n][1].rstrip(".;:,")
    if len(inicio) > 62: inicio = inicio[:60].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    des = f"Salmo {n} completo: «{inicio}». Na tradição dos 72 Nomes é o salmo de {lista}, em {lsig}."
    if len(des) > 158: des = f"Salmo {n} completo: «{inicio}». Na tradição dos 72 Nomes, {len(ans)} anjos de {lsig} leem nele o seu versículo."
    if len(des) > 158: des = f"Salmo {n} completo: «{inicio}». Nos 72 Nomes é o salmo de {len(ans)} anjos, com signo, datas e carta."
    if len(des) > 158: des = f"Salmo {n} completo, na Bíblia Livre, e os {len(ans)} anjos dos 72 Nomes que leem nele o seu versículo, com signo, datas e carta."
    medir(f"/salmos/salmo-{n}", tit, des)
    deles = {v: a for a in ans for v in a["vs"]}
    vs = ""
    for v, t in LIVRE[n].items():
        if n == 119 and v in LETRA: vs += f'<h3>{E(LETRA[v])}</h3>'
        cl = ' class="eu"' if v in deles else ""
        vs += f'<p id="v{v}"{cl}><sup>{v}</sup>{E(t)}</p>'
    linhas = ""
    for a in ans:
        c = carta(a["k"], a["dec"]); s, g, sl = SIG[a["k"]]
        linhas += (f'<tr><td><a href="/anjo/{slug(a["n"])}"><b>{a["n"]}</b></a><br><small>n.º {a["i"]+1}</small></td><td data-l="Versículo"><a href="#v{a["vs"][0]}">{a["sal"]}:{"-".join(str(x) for x in (a["vs"][0], a["vs"][-1])) if len(a["vs"]) > 1 else a["vs"][0]}</a></td>'
                   f'<td data-l="Signo"><a href="/salmos/{sl}">{g} {s}</a> <small>{a["g0"]}° a {a["g0"]+5}°</small></td><td data-l="Datas">{periodo(a["i"])}</td><td data-l="Carta"><a href="/{c["slug"]}">{c["nome"]}</a></td></tr>')
    vu = vulgata(n)
    num = ("O número é o mesmo em todas as Bíblias." if vu is None else
           f"Nas Bíblias católicas que seguem a numeração grega (Vulgata), este salmo é o {vu}." if " e " not in vu else
           f"Nas Bíblias católicas que seguem a numeração grega (Vulgata), este salmo aparece dividido em dois, os salmos {vu}.")
    if n == 9: num = "Nas Bíblias católicas que seguem a numeração grega (Vulgata), os salmos 9 e 10 formam um só, o Salmo 9."
    ant, seg = SALMOS[p - 1], SALMOS[(p + 1) % len(SALMOS)]
    corpo = f"""{heroi(f"Salmo {n}", "O texto completo e os anjos que o leem na tradição dos 72 Nomes")}
  <section class="cartao texto"><h2>Sobre o Salmo {n}</h2><p>{E(TXT_SAL[n])}</p><p><small>{num} Os versículos contam-se como na Bíblia de Almeida, sem o título.</small></p></section>
  <section class="cartao"><h2>{"O anjo" if len(ans) == 1 else "Os anjos"} do Salmo {n}</h2>
    <div class="tabw"><table class="tab"><thead><tr><th>Anjo</th><th>Versículo</th><th>Signo e graus</th><th>Datas (2027)</th><th>Carta do decanato</th></tr></thead><tbody>{linhas}</tbody></table></div>
    <p class="sub" style="font-size:.88rem;margin-top:.7rem">Nos dias em que o Sol passa por esses graus, este é o salmo do dia. As datas seguem o grau real do Sol e podem mudar um dia de ano para ano.</p></section>
  <section class="cartao texto vs"><h2>Salmo {n} completo</h2>{vs}{LIC}</section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/salmos/salmo-{ant}">← Salmo {ant}</a><a href="/salmos">Os salmos dos 72 anjos</a><a href="/salmos/salmo-{seg}">Salmo {seg} →</a></div>
    <p style="margin:.8rem 0 0"><a class="cta" href="/anjo-da-guarda#descobrir">Descobrir o meu anjo</a></p></section>
  <section class="cartao texto">{AVISO}</section>"""
    grava(f"salmos/salmo-{n}.html", pagina(f"/salmos/salmo-{n}", tit, des, corpo, ld_art(f"/salmos/salmo-{n}", tit, des, [("Salmos dos Anjos", "/salmos"), (f"Salmo {n}", f"/salmos/salmo-{n}")])))

# ─── salmo-do-dia.js (o mesmo cálculo de sol(): 12h UT do dia, 5 graus por anjo) ───
J_AN = [[a["n"], a["k"], a["sal"] or 0, ref(a) if a["sal"] else ("Génesis 1:1" if a["livro"] == "Génesis" else ""), a["txt"] or "", a["vs"][0] if a["vs"] else 0] for a in AN]
J_SIG = [[nome_sig(k), s[2]] for k, s in enumerate(SIG)]
J_CAR = [[carta(k, j)["nome"], carta(k, j)["slug"]] for k in range(12) for j in range(3)]
JS = """/* O salmo do dia pelo grau do Sol (gerado por gerar-salmos.py — não editar à mão).
   Desenha em #salmo-dia; segue o dia mostrado no Horóscopo do Dia (evento «gt-dia», window.GT_DIA). */
(function () {
var A = %s, S = %s, C = %s;
var M = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
function sol(iso) { var p = iso.split("-").map(Number), n = Math.round((Date.UTC(p[0], p[1] - 1, p[2]) - Date.UTC(2000, 0, 1)) / 864e5);
  var g = (357.528 + .9856003 * n) * Math.PI / 180, L = 280.46 + .9856474 * n; return ((L + 1.915 * Math.sin(g) + .02 * Math.sin(2 * g)) %% 360 + 360) %% 360; }
function hoje() { return new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date()); }
function e(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
function nomeSig(k) { var G = window.GT; return G && G.nomes ? G.nomes()[k] : S[k][0]; }
function desenha(el, iso) {
  var x = sol(iso), i = Math.floor(x / 5), a = A[i], k = a[1], c = C[k * 3 + Math.floor((i %% 6) / 2)], p = iso.split("-").map(Number);
  var h = '<p class="sd-sol">' + p[2] + " de " + M[p[1] - 1] + ": o Sol está a " + Math.floor(x %% 30) + "° de " + e(nomeSig(k)) + ". O anjo destes dias é <b>" + e(a[0]) + "</b>, n.º " + (i + 1) + " dos 72.</p>";
  if (a[2]) h += '<blockquote class="ora-c sd-q">«' + e(a[4]) + '»<footer>' + e(a[3]) + "</footer></blockquote>"
    + '<p class="ligas"><a href="/salmos/salmo-' + a[2] + "#v" + a[5] + '">Ler o Salmo ' + a[2] + " completo</a>";
  else h += "<p>" + (a[3] ? e(a[0]) + " é o único dos 72 sem salmo: o seu versículo é o primeiro da Bíblia, Génesis 1:1, «No princípio»." : "Para " + e(a[0]) + " as listas não concordam no salmo, e por isso não o indicamos: a oração do anjo serve no lugar dele.") + '</p><p class="ligas">';
  h += '<a href="/anjo/' + a[0].toLowerCase() + '">Conhecer ' + e(a[0]) + '</a><a href="/salmos/' + S[k][1] + '">Os salmos de ' + e(nomeSig(k)) + '</a><a href="/' + c[1] + '">Carta do decanato: ' + e(c[0]) + "</a></p>";
  el.innerHTML = h;
}
window.salmoDoDia = desenha;
var el = document.getElementById("salmo-dia-caixa"); if (!el) return;
desenha(el, window.GT_DIA || hoje());
document.addEventListener("gt-dia", function (v) { desenha(el, v.detail); });
})();
""" % tuple(json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in (J_AN, J_SIG, J_CAR))
grava("salmo-do-dia.js", JS)

# 16/11/2026 (pedido dele): o mesmo salmo do dia já no HTML para o Google. Módulo para o worker.js, que o escreve em
# #salmo-dia-caixa no /horoscopo-do-dia (dia de Portugal); o salmo-do-dia.js redesenha por cima no navegador.
MOD = """// Gerado por gerar-salmos.py — não editar à mão. Usado pelo worker.js (salmo do dia no HTML do /horoscopo-do-dia).
const A = %s, S = %s, C = %s;
const M = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
function sol(iso) { const p = iso.split("-").map(Number), n = Math.round((Date.UTC(p[0], p[1] - 1, p[2]) - Date.UTC(2000, 0, 1)) / 864e5);
  const g = (357.528 + .9856003 * n) * Math.PI / 180, L = 280.46 + .9856474 * n; return ((L + 1.915 * Math.sin(g) + .02 * Math.sin(2 * g)) %% 360 + 360) %% 360; }
const e = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
export function salmoDoDiaHtml(iso) {
  const x = sol(iso), i = Math.floor(x / 5), a = A[i], k = a[1], c = C[k * 3 + Math.floor((i %% 6) / 2)], p = iso.split("-").map(Number);
  let h = '<p class="sd-sol">' + p[2] + " de " + M[p[1] - 1] + ": o Sol está a " + Math.floor(x %% 30) + "° de " + e(S[k][0]) + ". O anjo destes dias é <b>" + e(a[0]) + "</b>, n.º " + (i + 1) + " dos 72.</p>";
  if (a[2]) h += '<blockquote class="ora-c sd-q">«' + e(a[4]) + '»<footer>' + e(a[3]) + "</footer></blockquote>"
    + '<p class="ligas"><a href="/salmos/salmo-' + a[2] + "#v" + a[5] + '">Ler o Salmo ' + a[2] + " completo</a>";
  else h += "<p>" + (a[3] ? e(a[0]) + " é o único dos 72 sem salmo: o seu versículo é o primeiro da Bíblia, Génesis 1:1, «No princípio»." : "Para " + e(a[0]) + " as listas não concordam no salmo, e por isso não o indicamos: a oração do anjo serve no lugar dele.") + '</p><p class="ligas">';
  h += '<a href="/anjo/' + a[0].toLowerCase() + '">Conhecer ' + e(a[0]) + '</a><a href="/salmos/' + S[k][1] + '">Os salmos de ' + e(S[k][0]) + '</a><a href="/' + c[1] + '">Carta do decanato: ' + e(c[0]) + "</a></p>";
  return h;
}
""" % tuple(json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in (J_AN, J_SIG, J_CAR))
grava("salmo-dia-dados.js", MOD)

# ─── /salmos ───
FAQ = [("Qual é o salmo do dia?", "Na tradição dos 72 Nomes, é o versículo do anjo que rege o grau em que o Sol está hoje. Cada anjo cobre 5 graus, cerca de cinco dias, por isso o salmo do dia muda mais ou menos de cinco em cinco dias. A caixa no topo desta página calcula-o para hoje."),
       ("Qual é o salmo do meu signo?", "Cada signo tem seis anjos e, por isso, seis versículos, um para cada 5 graus. O salmo mais seu é o do anjo do grau em que o Sol estava no dia em que nasceu: escolha o seu signo na lista e procure as suas datas."),
       ("Porque é que o número do salmo muda de uma Bíblia para outra?", "As Bíblias de Almeida e as hebraicas numeram os salmos de uma maneira; muitas Bíblias católicas seguem a numeração grega (Vulgata), que junta e divide alguns salmos. Entre o 10 e o 147 a diferença é quase sempre de um número: o Salmo 91 de Almeida é o 90 nessas Bíblias. Aqui usamos a numeração de Almeida, a mais comum no Brasil."),
       ("Que tradução da Bíblia usam?", "A Bíblia Livre, uma tradução portuguesa publicada com licença Creative Commons, que permite reproduzi-la com atribuição. Corrigimos apenas espaçamentos e três gralhas de digitação."),
       ("A Igreja Católica reconhece os anjos dos salmos?", "Não. A ligação entre os 72 anjos, os graus do zodíaco e os versículos é uma tradição da Cabala e da angelologia, não da doutrina da Igreja. Os salmos em si são oração comum de judeus e cristãos.")]
grelha = ""
for k, (s, g, sl) in enumerate(SIG):
    cs = " · ".join(carta(k, j)["nome"] for j in range(3))
    grelha += f'<a href="/salmos/{sl}"><b>{g} {nome_sig(k)}</b><span>{_per(DIAS[k*6][0], DIAS[k*6+5][-1])}<br>{cs}</span></a>'
lsal = "".join(f'<a href="/salmos/salmo-{n}"><b>Salmo {n}</b><span>{", ".join(a["n"] for a in POR_SAL[n])}</span></a>' for n in SALMOS)
sem = [a for a in AN if not a["sal"]]
TIT = "Salmo do Dia e o Salmo do seu Signo pelos 72 Anjos"
DES = "O salmo de hoje pelo grau do Sol, o salmo de cada signo e a carta do Tarot de cada decanato, na tradição dos 72 Anjos. Texto da Bíblia Livre."
medir("/salmos", TIT, DES)
CORPO = f"""{heroi("Os Salmos dos 72 Anjos", "O salmo do dia, o salmo do seu signo e a carta do Tarot de cada decanato")}
  <section class="cartao" id="salmo-dia"><h2>O salmo de hoje</h2><div id="salmo-dia-caixa"><p>A calcular o grau do Sol de hoje…</p></div>
    <noscript><p>Esta caixa precisa de JavaScript para calcular o grau do Sol. Sem ele, escolha o seu signo na lista abaixo.</p></noscript></section>
  <section class="cartao texto"><h2>Como um salmo se liga a um signo e a uma carta</h2>
    <p>A ponte entre os Salmos e o zodíaco é a tradição dos 72 Nomes, ou Shem HaMephorash. Os cabalistas tiraram 72 nomes de três versículos seguidos do Êxodo (14,19-21), e mais tarde cada nome foi tratado como um anjo, com um versículo próprio, quase sempre dos Salmos, para se ler ao invocá-lo.</p>
    <ol class="passos"><li><b>Do salmo ao anjo.</b> Cada um dos 72 anjos tem o seu versículo. Alguns salmos servem vários anjos: o 145 serve cinco.</li>
      <li><b>Do anjo aos graus.</b> O zodíaco tem 360 graus e 360 ÷ 72 = 5. Cada anjo rege 5 graus, a começar em 0° de Carneiro.</li>
      <li><b>Dos graus ao signo.</b> Cada signo tem 30 graus, ou seja, seis anjos. Pelo grau do Sol de um dia sabe-se o anjo e o versículo desse dia.</li>
      <li><b>Do signo à carta.</b> Na correspondência da Golden Dawn, cada decanato (10 graus, dois anjos) é uma carta numerada dos Arcanos Menores: nos signos cardinais o 2, 3 e 4, nos fixos o 5, 6 e 7, nos mutáveis o 8, 9 e 10. O naipe é o do elemento: Fogo é Paus, Terra é Ouros, Ar é Espadas, Água é Copas.</li></ol>
    <p>Um exemplo: o Sol a 3° de Carneiro está nos graus de Vehuiah, cujo versículo é o Salmo 3:3, «tu, SENHOR, és escudo para mim». É o primeiro decanato de Carneiro, que a Golden Dawn liga ao Dois de Paus.</p></section>
  <section class="cartao"><h2>O salmo de cada signo</h2><div class="sgr">{grelha}</div><p class="sub" style="font-size:.88rem;margin-top:.7rem">Datas pelo grau do Sol em 2027: podem mudar um dia de ano para ano.</p></section>
  <section class="cartao"><h2>Os {len(SALMOS)} salmos dos anjos</h2><p>Dos 72 anjos, {72 - len(sem)} têm um versículo dos Salmos, tirado de {len(SALMOS)} salmos diferentes. Os outros dois ficam de fora: {sem[0]["n"]}, porque as listas publicadas não concordam no salmo, e {sem[1]["n"]}, cujo versículo é Génesis 1:1.</p><div class="sgr">{lsal}</div></section>
  <section class="cartao texto"><h2>Perguntas frequentes</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ)}</section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/os-72-anjos">Os 72 Anjos</a><a href="/anjo-da-guarda">Anjo da Guarda</a><a href="/arcanos-menores">Os Arcanos Menores</a><a href="/horoscopo-do-dia">Horóscopo do Dia</a></div>
    <p style="margin:.8rem 0 0"><a class="cta" href="/anjo-da-guarda#descobrir">Descobrir o meu anjo</a></p></section>
  <section class="cartao texto">{AVISO}{LIC}</section>"""
LD = ld_art("/salmos", TIT, DES, [("Salmos dos Anjos", "/salmos")], [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}])


def gerar_paginas():
    grava("salmos.html", pagina("/salmos", TIT, DES, CORPO, LD, fim='<script src="/salmo-do-dia.js" defer></script>\n'))


# ─── ligações para dentro (idempotentes; os blocos «<!-- dd/mm/aaaa: ligações … -->» sobrevivem ao gerar-signos.py) ───
def _troca(f, novo_fn):
    s = open(f, encoding="utf8").read(); t = novo_fn(s)
    if t != s: open(f, "w", encoding="utf8").write(t); return True
    return False


def _bloco_antes_casa(s, marca, bloco):
    m = re.search(r"<!-- \d\d/\d\d/\d{4}: " + re.escape(marca) + r" -->\n(.*?</section>)\n?", s, flags=re.S)
    if m and re.sub(r'<a class="li-gt" href="[^"]*">(.*?)</a>', r"\1", m.group(1)) == bloco.strip("\n"):
        return s   # igual (as ligações li-gt são do ligacoes-internas.py, no pre-commit): não mexer
    s = re.sub(r"<!-- \d\d/\d\d/\d{4}: " + re.escape(marca) + r" -->.*?</section>\n?", "", s, flags=re.S)
    k = s.find("<!-- gt-casa:inicio -->")
    if k < 0: k = s.find("<footer")
    return s[:k] + f"<!-- {HOJE}: {marca} -->\n{bloco}\n" + s[k:]


def ligacoes():
    mud = []
    # signo/*.html
    for k, (s, g, sl) in enumerate(SIG):
        b = (f'  <section class="cartao" style="text-align:center"><h2>📖 Os salmos de {s}</h2><p>Na tradição dos 72 Anjos, cada 5 graus de {s} têm um anjo e um versículo dos Salmos, '
             f'e cada decanato uma carta dos Arcanos Menores.</p><div class="ligas"><a href="/salmos/{sl}">Os salmos de {s}</a><a href="/salmos">O salmo de hoje</a></div></section>')
        if _troca(f"signo/{sl}.html", lambda x: _bloco_antes_casa(x, "ligações aos salmos", b)): mud.append(f"signo/{sl}.html")
    # os-72-anjos.html: um bloco + «Os salmos de X» ao lado de «Ver o signo de X» (o mesmo que o gerar-anjos.py já escreve)
    def f72(x):
        b = ('  <section class="cartao" style="text-align:center"><h2>📖 Os salmos dos anjos</h2><p>Cada anjo tem um versículo dos Salmos. '
             'Pelo grau do Sol sabe-se o anjo e o salmo de cada dia.</p><div class="ligas"><a href="/salmos">O salmo de hoje e os salmos dos 12 signos</a></div></section>')
        x = _bloco_antes_casa(x, "ligações aos salmos", b)
        for s, g, sl in SIG:
            v = f'<a href="/signo/{sl}">Ver o signo de {s}</a></p>'
            if v in x and f'href="/salmos/{sl}"' not in x: x = x.replace(v, v[:-4] + f' · <a href="/salmos/{sl}">Os salmos de {s}</a></p>', 1)
        return x
    if _troca("os-72-anjos.html", f72): mud.append("os-72-anjos.html")
    # horoscopo-do-dia.html: a caixa «O salmo do dia» e o aviso do dia mostrado (evento gt-dia)
    caixa = ('<!-- salmo-dia:inicio -->\n  <section class="cartao" id="salmo-dia" style="text-align:center"><style>#salmo-dia .ora-c{font-family:var(--serifa,Georgia,serif);font-style:italic;font-size:1.15rem;'
             'margin:.7rem auto;max-width:40rem;padding:.8rem 1rem;border-left:3px solid var(--ouro);background:var(--vidro);border-radius:.6rem;text-align:left}#salmo-dia .ora-c footer{font-style:normal;font-size:.85rem;color:var(--suave);margin-top:.3rem;padding:0;text-align:left}'
             '#salmo-dia .ligas{display:flex;flex-wrap:wrap;gap:.4rem;justify-content:center}#salmo-dia .ligas a{padding:.35rem .8rem;border:1px solid var(--borda);border-radius:999px;background:var(--vidro);color:inherit;text-decoration:none;font-size:.88rem}'
             '#salmo-dia .ligas a:hover{border-color:var(--ouro)}</style><h2>📖 O salmo do dia</h2><div id="salmo-dia-caixa"><p>O salmo do dia é o versículo do anjo que rege o grau do Sol. '
             '<a href="/salmos">Veja o salmo de hoje</a>.</p></div><p class="fonte">Tradição dos 72 Anjos, leitura simbólica. Texto bíblico: Bíblia Livre, '
             '<a href="https://creativecommons.org/licenses/by/3.0/br/" rel="license noopener">CC BY 3.0 Brasil</a>.</p></section>\n'
             '<script src="/salmo-do-dia.js" defer></script>\n<!-- salmo-dia:fim -->\n')
    def fh(x):
        x = re.sub(r"<!-- salmo-dia:inicio -->.*?<!-- salmo-dia:fim -->\n", "", x, flags=re.S)
        a = "  <!-- 13/11/2026: o horóscopo de amanhã de cada signo -->"
        if a not in x: raise SystemExit("horoscopo-do-dia.html: não encontrei onde pôr o salmo do dia")
        x = x.replace(a, caixa + a, 1)
        q = "    const q = diaISO();\n"
        if "gt-dia" not in x:
            if q not in x: raise SystemExit("horoscopo-do-dia.html: não encontrei diaISO()")
            x = x.replace(q, '    const q = diaISO();\n    window.GT_DIA = q.iso; document.dispatchEvent(new CustomEvent("gt-dia", { detail: q.iso }));   // 16/11/2026: o salmo do dia segue o dia mostrado\n', 1)
        return x
    if _troca("horoscopo-do-dia.html", fh): mud.append("horoscopo-do-dia.html")
    # novidades.html (lista à mão: uma linha no topo)
    def fn(x):
        if 'href="/salmos"' in x: return x
        a = '<nav class="novas" aria-label="Páginas novas">\n'
        return x.replace(a, a + '      <a class="nova" href="/salmos"><span class="eti">Novo</span><span class="ico">📖</span><span><b>Os Salmos dos 72 Anjos</b><small>O salmo de hoje pelo grau do Sol, o salmo do seu signo e a carta do Tarot de cada decanato.</small></span></a>\n', 1)
    if _troca("novidades.html", fn): mud.append("novidades.html")
    print("ligações:", len(mud), "páginas mudadas")


if __name__ == "__main__":
    if "--ligacoes" not in sys.argv:
        gerar_paginas()
        print(f"páginas: 1 + 12 signos + {len(SALMOS)} salmos; salmo-do-dia.js")
        print("título máx", max(tamanhos), "\ndescrição máx", max(tamanhos, key=lambda x: x[1]))
    ligacoes()
