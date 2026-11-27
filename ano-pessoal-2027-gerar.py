#!/usr/bin/env python3
"""Gera as 9 páginas /ano-pessoal-N-2027 (27/11/2026, pedido dele depois da análise da helenasousa.pt).
Textos: ano-pessoal-2027-textos.py + numerologia-2027-textos.js (abertura e oportunidades, os mesmos da calculadora).
Molde: o <style>, o bloco gt-casa, o rodapé e os scripts são copiados de eclipses-2027.html, para ficarem iguais ao resto.
O cálculo é o da calculadora (numerologia-2027.html): Ano Pessoal = reduz(dia + mês + 2027); Mês Pessoal = reduz(ano + reduz(mês))."""
import os, re, json, html, importlib.util
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE, ANO = "https://genialtarot.com", 2027

spec = importlib.util.spec_from_file_location("t", "ano-pessoal-2027-textos.py"); t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
js = open("numerologia-2027-textos.js", encoding="utf-8").read()
def arr(nome):
    bloco = re.search(r"const %s = \[(.*?)\];" % nome, js, re.S).group(1)
    return [None] + re.findall(r'"((?:[^"\\]|\\.)*)"', bloco)
TITULO, MOTIVACAO, MES = arr("TITULO"), arr("MOTIVACAO"), arr("MES")
OPORT = [None] + [re.findall(r'"([^"]*)"', l) for l in re.findall(r"\[(\"[^\]]*)\]", re.search(r"const OPORTUNIDADES = \[(.*?)\];", js, re.S).group(1))]
assert len(TITULO) == len(MOTIVACAO) == len(OPORT) == len(MES) == 10

somaAlg = lambda n: sum(int(d) for d in str(n))
def reduz(n):
    while n > 9: n = somaAlg(n)
    return n
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

molde = open("eclipses-2027.html", encoding="utf-8").read()
ESTILO = re.search(r"<style>.*?</style>", molde, re.S).group(0)
CASA = re.search(r"<!-- gt-casa:inicio -->.*?<!-- gt-casa:fim -->", molde, re.S).group(0)
FIM = molde[molde.index("<footer>"):]
e = html.escape

def exemplo(n):
    # uma data de exemplo que dá o número n: mês = n, o primeiro dia a partir de 10 que acerta
    m = n
    d = next(d for d in range(10, 29) if reduz(d + m + ANO) == n)
    s = d + m + ANO; passos = [str(s)]
    while s > 9:
        s2 = somaAlg(s); passos.append(" + ".join(str(s)) + " = " + str(s2)); s = s2
    return d, m, passos

def pagina(n):
    x = t.T[n]; url = f"{SITE}/ano-pessoal-{n}-{ANO}"
    titulo = f"Ano Pessoal {n} em 2027: {TITULO[n].lower()} na Numerologia"
    desc = f"O que significa o Ano Pessoal {n} em 2027: amor, trabalho e dinheiro, o desafio do ano, os meses mais fortes e como calcular. {x['chave'].capitalize()}."
    faq = x["faq"] + [t.FAQ_CALCULO]
    d, m, passos = exemplo(n)
    meses = [(MESES[i], reduz(n + reduz(i + 1))) for i in range(12)]
    fortes = [nome for nome, v in meses if v == n]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": titulo, "description": desc, "image": f"{SITE}/og-image.jpg", "inLanguage": "pt",
         "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"},
         "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE},
         "datePublished": "2026-11-27", "dateModified": "2026-11-27", "mainEntityOfPage": url},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Genial Tarot", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Numerologia 2027", "item": f"{SITE}/numerologia-2027"},
            {"@type": "ListItem", "position": 3, "name": f"Ano Pessoal {n}", "item": url}]}]}
    outros = "".join(f'<a href="/ano-pessoal-{k}-{ANO}">Ano Pessoal {k}<br><small>{e(TITULO[k])}</small></a>' if k != n else "" for k in range(1, 10))
    tabela = "".join(f'<div{" class=\"forte\"" if v == n else ""}><b>{nome}</b>{v} · {e(MES[v])}</div>' for nome, v in meses)
    corpo = f"""<section class="heroi"><span class="selo">Numerologia 2027</span><h1><span class="az">Ano Pessoal {n} em 2027</span></h1>
  <p class="sub">{e(TITULO[n])}: {e(x['chave'])}.</p></section>
  <section class="cartao texto">
    <p class="chave" style="font-family:var(--serifa);font-size:1.3rem;color:var(--ouro)">{e(MOTIVACAO[n])}</p>
    <p>{e(x['intro'])}</p>
    <h2>As oportunidades mais fortes do Ano Pessoal {n}</h2>
    <div class="perfil">{"".join(f"<div>{e(o)}</div>" for o in OPORT[n])}</div>
    <h2>O amor no Ano Pessoal {n}</h2><p>{e(x['amor'])}</p>
    <h2>Trabalho e dinheiro no Ano Pessoal {n}</h2><p>{e(x['trabalho'])}</p>
    <h2>O desafio do ano</h2><p>{e(x['desafio'])}</p>
    <h2>Três gestos para aproveitar o seu 2027</h2><ul>{"".join(f"<li>{e(c)}</li>" for c in x['conselhos'])}</ul>
  </section>
  <section class="cartao texto">
    <h2>Os seus meses em 2027</h2>
    <p>Dentro do ano, cada mês tem a sua vibração: o Mês Pessoal soma o seu Ano Pessoal ao número do mês. O mês em que o número {n} se repete, e a energia do seu ano fica no auge, é {" e ".join(fortes)}, marcado a dourado.</p>
    <div class="perfil meses">{tabela}</div>
  </section>
  <section class="cartao texto">
    <h2>Como se calcula o Ano Pessoal</h2>
    <p>Some o dia e o mês do seu nascimento com o ano de 2027, e reduza o resultado somando os algarismos até ficar um só número. Por exemplo, quem nasceu a {d} de {MESES[m-1]}: {d} + {m} + 2027 = {" → ".join(passos)}. Está no Ano Pessoal {n}.</p>
    <p>2027 é, para todos, um Ano Universal 11 (2 + 0 + 2 + 7), um número mestre que se reduz a 2: um ano colectivo de intuição, de alianças e de sensibilidade, que dá um fundo de cooperação a todos os Anos Pessoais. A numerologia mostra tendências e ritmos, não um destino fechado: o que faz com elas é sempre seu.</p>
    <p style="text-align:center"><a class="cta" href="/numerologia-2027">Calcular o meu Ano Pessoal grátis</a></p>
  </section>
  <section class="cartao texto"><h2>Perguntas frequentes</h2>
    {"".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq)}
  </section>
  <section class="cartao" style="text-align:center"><h2>Os outros Anos Pessoais de 2027</h2><div class="doze anos">{outros}</div>
    <div class="ligas"><a href="/numerologia-2027">Calculadora do Ano 2027</a><a href="/numerologia">Numerologia: o significado dos números</a><a href="/horoscopo-2027">Horóscopo 2027</a><a href="/melhores-signos-2027">Melhores signos de 2027</a><a href="/cor-do-ano-2027">A cor do ano 2027</a></div>
  </section>"""
    extra = """<style>
.texto h3 { font-family: var(--serifa); font-size: 1.2rem; color: var(--ouro); margin: 1rem 0 .2rem; }
.texto ul { font-family: var(--serifa); font-size: 1.08rem; color: var(--lavanda); padding-left: 1.2rem; } .texto li { margin: .3rem 0; }
.meses div.forte { border-color: var(--ouro); box-shadow: 0 0 18px oklch(0.85 0.13 88 / .3); color: var(--ouro); }
.anos a { flex-direction: column; align-items: flex-start; gap: 0; font-weight: 700; }
</style>"""
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
<meta property="og:image" content="{SITE}/og-image.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{ESTILO}
{extra}
</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/numerologia-2027"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>Numerologia 2027</a>
  </header>
  {corpo}
{CASA}
{FIM}"""

for n in range(1, 10):
    open(f"ano-pessoal-{n}-{ANO}.html", "w", encoding="utf-8").write(pagina(n))
    print(f"ano-pessoal-{n}-{ANO}.html")
