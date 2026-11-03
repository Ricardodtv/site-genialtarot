# 03/11/2026 — os grandes trânsitos lentos (pedido dele: «uma página por grande trânsito, feita antes de ele acontecer»).
# Corre DENTRO do gerar-signos.py (exec), por isso usa as peças de lá: pagina(), E, S, GLIFO, SITE, PROD, WA, nm.
# Textos em transitos-textos.py; datas em transitos-datas.json (Swiss Ephemeris, hora de Lisboa — refazer com
# ~/.venv-astro/bin/python transitos-calc.py); perguntas frequentes em faq-textos-transitos.py.
# Faz 8 páginas de trânsitos + a montra /transitos-lentos.
D = json.load(open("transitos-datas.json", encoding="utf-8"))
TX = {}; exec(open("transitos-textos.py", encoding="utf-8").read(), TX)
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
def dt(s, hora=True):
    a, m, d = s[:10].split("-"); t = f"{int(d)} de {MESES[int(m) - 1]} de {a}"
    return t + (f", às {s[11:16]}" if hora and len(s) > 11 else "")
NOMEPL = {"jupiter": "Júpiter", "saturno": "Saturno", "urano": "Úrano", "neptuno": "Neptuno", "plutao": "Plutão", "nodo_verdadeiro": "O Nodo Norte"}
def datas(t):
    pl, sg = t["planeta"], t["signo"]
    if pl == "saturno_urano":
        a = [x for x in D["aspectos"] if x["aspecto"] == "saturno conjunção urano"][0]
        sat = [e for e in D["ingressos"]["saturno"] if e["para"] == "Gémeos" and e["data"] > "2030"][0]
        ur = [e for e in D["ingressos"]["urano"] if e["de"] == "Gémeos" or e["para"] == "Gémeos"]
        ur = [e for e in ur if e["data"] > "2032"]
        return [(dt(sat["data"]), "Saturno entra em Gémeos"), (dt(a["data"]), f"Saturno e Úrano em conjunção exata ({a['pos'].split(' / ')[0]})")] + \
               [(dt(e["data"]), f"Úrano {'entra em ' + e['para'] if e['sentido'] == 'directo' else 'volta a ' + e['para']}") for e in ur]
    ev = D["ingressos"][pl]; L = []
    idx = [i for i, e in enumerate(ev) if e["de"] == sg or e["para"] == sg]
    # só a passagem destes anos: corta quando há mais de 5 anos entre dois eventos (ex.: Júpiter volta a Leão em 2038)
    for k in range(1, len(idx)):
        if ev[idx[k - 1]]["de"] == sg and int(ev[idx[k]]["data"][:4]) - int(ev[idx[k - 1]]["data"][:4]) > 5: idx = idx[:k]; break   # saiu e só volta anos depois
    for i in idx:
        e = ev[i]; nome = NOMEPL[pl]
        dire = e["sentido"] == "directo" or pl.startswith("nodo")   # os nodos andam sempre para trás: aí não há «voltar»
        if e["para"] == sg: L.append((dt(e["data"]), f"{nome} {'entra em' if dire else 'volta a'} {sg}"))
        else: L.append((dt(e["data"]), f"{nome} {'sai para' if dire else 'recua para'} {e['para']}"))
    if pl.startswith("nodo"):   # o eixo seguinte
        prox = ev[idx[-1] + 1]; L.append((dt(prox["data"]), f"O Nodo Norte sai de {prox['de']} para {prox['para']}"))
        medio = [e for e in D["ingressos"]["nodo_medio"] if e["para"] == sg][0]
        L.insert(1, (dt(medio["data"]), f"(nodo médio) o Nodo Norte entra em {sg}"))
        return L
    # as paragens (retrógrado / direto) com o planeta dentro do signo, a partir de 2026 e no máximo até ao fim de 2028
    ini = ev[idx[0]]["data"]; fim = ev[idx[-1]]["data"]
    for e in D["estacoes"][pl]:
        if ini < e["data"] < fim and "2026" <= e["data"] < "2029" and e["pos"].endswith(sg):
            L.append((dt(e["data"]), f"{NOMEPL[pl]} {e['tipo'].replace('directo', 'direto')} a {e['pos'].replace(' ' + sg, '')} de {sg}"))
    return L
def ordena(L):   # ordena pelas datas escritas por extenso
    def chave(x):
        m = re.match(r"(\d+) de (\w+) de (\d{4})(?:, às (\d\d:\d\d))?", x[0]); return (m.group(3), MESES.index(m.group(2)), int(m.group(1)), m.group(4) or "")
    return sorted(L, key=chave)
SEM_BR = lambda p: re.sub(r" \((Áries|Câncer|Libra|Gêmeos)\)", "", p)
def prod(*nomes):
    r = []
    for q in nomes:
        for n, pr in PROD:
            if q.lower() in n.lower() and (n, pr) not in r: r.append((n, pr))
    return r
CTA = prod("Mapa Astral – Versão Completa", "Previsão Anual", "Consulta de Tarot Online")
outros = lambda atual: "".join(f'<a href="/{x["slug"]}">{E(x["h1"])}</a>' for x in TX["TRANSITOS"] if x["slug"] != atual)
PLANETA_PAG = {"jupiter": "planeta-jupiter", "saturno": "planeta-saturno", "urano": "planeta-urano", "neptuno": "planeta-neptuno", "plutao": "planeta-plutao", "nodo_verdadeiro": "planeta-lua", "saturno_urano": "planeta-saturno"}
for t in TX["TRANSITOS"]:
    L = ordena(datas(t))
    lista = "".join(f"<li><b>{E(a)}</b> — {E(b)}</li>" for a, b in L)
    secs = "".join(f"<h2>{E(h)}</h2><p>{p}</p>" for h, p in t["seccoes"])
    signos = "".join(f'<h3><a href="/signo/{S[i]["slug"]}" style="color:inherit;text-decoration:none">{GLIFO[i]}︎ {E(nm(S[i]))}</a></h3><p>{E(SEM_BR(p))}</p>' for i, p in enumerate(t["signos"]))
    cta = "".join(f'<a href="{"/mapa-astral" if "Mapa Astral" in n else "/loja"}">{E(n)}{" · " + E(pr) if pr else ""}</a>' for n, pr in CTA)
    corpo = f"""  <section class="heroi"><h1><span class="az">{E(t['h1'])}</span></h1><p class="sub">{E(t['sub'])}</p></section>
  <section class="cartao texto"><p>{t['intro']}</p>
    <h2>As datas, em hora de Portugal</h2><ul>{lista}</ul>
    <p style="color:var(--suave);font-size:.9rem">Datas calculadas com o Swiss Ephemeris, em hora de Lisboa{" (nodo verdadeiro, salvo indicação)" if t["planeta"].startswith("nodo") else ""}. No Brasil, a hora é três ou quatro horas mais cedo, o que pode mudar o dia nos eventos perto da meia-noite.</p>
    {secs}</section>
  <section class="cartao texto"><h2>O que muda para cada signo</h2>
    <p>As casas contam-se a partir do signo solar, como no <a href="/horoscopo-2027">Horóscopo 2027</a>. Se souber o seu Ascendente, leia também o texto do signo do Ascendente: costuma ser ainda mais certeiro.</p>
    {signos}</section>
  <section class="cartao texto" style="text-align:center"><h2>Este trânsito no seu mapa</h2>
    <p>O signo solar dá uma boa orientação, mas o que este trânsito faz na sua vida depende do mapa inteiro: onde cai em casas, que planetas toca e quando. O Mapa Astral é calculado ao minuto a partir do seu nascimento; a Previsão Anual e as consultas são feitas pelo Mestre Alberto.</p>
    <div class="ligas">{cta}</div>
    <a class="cta" href="{WA}">Falar com o Mestre Alberto</a></section>
  <section class="cartao" style="text-align:center"><h2>Outros grandes trânsitos</h2><div class="ligas">{outros(t['slug'])}<a href="/transitos-lentos">Todos os trânsitos</a><a href="/{PLANETA_PAG[t['planeta']]}">{E({"jupiter": "Júpiter", "saturno": "Saturno", "urano": "Úrano", "neptuno": "Neptuno", "plutao": "Plutão", "nodo_verdadeiro": "A Lua", "saturno_urano": "Saturno"}[t["planeta"]])} na astrologia</a><a href="/retrogrados">Os retrógrados agora</a></div></section>
"""
    pagina(t["slug"], t["titulo"], t["desc"], f"{SITE}/{t['img']}-og.jpg", [("Astrologia", "/astrologia"), ("Trânsitos lentos", "/transitos-lentos")], corpo)
# a montra
M = TX["MONTRA"]
def resumo(t):
    L = ordena(datas(t)); return f"{L[0][0].split(',')[0]} → {L[-1][0].split(',')[0]}" if L else ""
grelha = "".join(f'<a href="/{t["slug"]}"><span><b>{E(t["h1"])}</b><small>{E(t["sub"])}</small></span></a>' for t in TX["TRANSITOS"])
tabela = "".join(f'<li><a href="/{t["slug"]}">{E(t["h1"])}</a> — {E(resumo(t))}</li>' for t in TX["TRANSITOS"])
pagina(M["slug"], M["titulo"], M["desc"], f"{SITE}/alinhamento-dos-planetas-og.jpg", [("Astrologia", "/astrologia")],
       f"""  <section class="heroi"><h1><span class="az">{E(M['h1'])}</span></h1><p class="sub">{E(M['sub'])}</p></section>
  <section class="cartao texto"><p>{E(M['intro'])}</p><h2>As datas de cada trânsito</h2><ul>{tabela}</ul><p style="color:var(--suave);font-size:.9rem">{E(M['nota'])}</p></section>
  <section><div class="doze">{grelha}</div></section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/horoscopo-2027">Horóscopo 2027</a><a href="/eclipses-2027">Eclipses de 2027</a><a href="/retrogrados-2027">Retrógrados 2027</a><a href="/mapa-astral">Mapa Astral</a></div>
    <a class="cta" href="{WA}">Falar com o Mestre Alberto</a></section>
""")

