#!/usr/bin/env python3
"""As páginas dos 12 signos (/signo/<nome>) e a montra /signos-do-zodiaco — 31/10/2026, pedido dele (SEO: «Signos»,
«Horóscopo», variantes por signo, com o nome de Portugal E do Brasil). Textos em signos-textos.json (POR APROVAR por ele:
enquanto APROVADO = True   # 31/10/2026: ele mandou abrir todas as variantes ao Google, as páginas saem com noindex e ficam fora do sitemap). O horóscopo de hoje de cada signo vem do
mesmo horoscopo-dia/AAAA-MM-DD.json da página Horóscopo do Dia. Correr: python3 gerar-signos.py"""
import json, os, re, html
APROVADO = True   # 31/10/2026: ele mandou abrir todas as variantes ao Google
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"
S = json.load(open("signos-textos.json", encoding="utf-8"))
ELEM = ["Fogo", "Terra", "Ar", "Água"]; MOD = ["cardinal", "fixo", "mutável"]
GLIFO = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]
E = lambda t: html.escape(t, quote=True)
estilo = re.search(r"<style>.*?</style>", open("horoscopo-do-dia.html", encoding="utf-8").read(), re.S).group(0)
estilo = estilo.replace("</style>", """
.perfil { display: grid; gap: .5rem; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); margin: 1rem 0 0; }
.perfil div { background: var(--vidro); border: 1px solid var(--borda); border-radius: 1rem; padding: .6rem .8rem; text-align: center; }
.perfil b { display: block; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: var(--suave); }
.texto h2 { text-align: left; margin-top: 1.4rem; } .texto p { font-size: 1.05rem; }
.ligas { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; margin: 1rem 0; }
.ligas a { text-decoration: none; font-weight: 700; color: var(--texto); border: 1px solid var(--borda); background: var(--vidro); border-radius: 999px; padding: .5rem 1rem; }
.ligas a:hover { border-color: var(--ouro); }
.hoje .chave { font-family: var(--serifa); font-size: 1.3rem; color: var(--ouro); margin: .4rem 0; }
.cta { display: inline-block; margin-top: .8rem; text-decoration: none; font-weight: 800; color: oklch(0.22 0.06 270); background: var(--grad-ouro); border-radius: 999px; padding: .75rem 1.4rem; }
.doze { display: grid; gap: .8rem; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); }
.doze a { display: flex; gap: .8rem; align-items: center; text-decoration: none; color: var(--texto); background: oklch(0.20 0.06 272 / .88); border: 1px solid var(--borda); border-radius: 1.2rem; padding: .8rem 1rem; }
.doze a:hover { border-color: var(--ouro); } .doze img { width: 3.6rem; height: 3.6rem; border-radius: 50%; }
.doze small { display: block; color: var(--suave); }
.gmaps-btn{display:inline-flex;align-items:center;gap:.8rem;padding:.7rem 1.3rem .7rem 1rem;border-radius:999px;background:#fff;color:#202124;text-decoration:none;box-shadow:0 6px 24px rgba(0,0,0,.35);text-align:left}
.gmaps-btn b{display:block;font-size:1.02rem} .gmaps-btn small{display:block;color:#5f6368;font-size:.8rem}
</style>""")
def cabeca(titulo, desc, url, img, ld, indexar):
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{E(titulo)}</title>
<meta name="description" content="{E(desc)}" />
{'' if indexar else '<meta name="robots" content="noindex" />'}
<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{E(titulo)}" />
<meta property="og:description" content="{E(desc)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{img}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{estilo}
</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
"""
RODAPE = """<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="/privacidade">Política de Privacidade</a> · <a href="/termos">Termos de Serviço</a>
</footer>
</div>
<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""
AUTOR = {"@type": "Person", "name": "Mestre Alberto", "url": SITE + "/sobre"}
EDITOR = {"@type": "Organization", "name": "Genial Tarot", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/og-image.jpg"}}
os.makedirs("signo", exist_ok=True)
for i, s in enumerate(S):
    url = f"{SITE}/signo/{s['slug']}"; img = f"{SITE}/signos/{i:02d}.webp"
    nome = s["pt"] if s["pt"] == s["br"] else f"{s['pt']} ({s['br']})"
    titulo = f"Signo {nome}: características, amor e horóscopo de hoje"
    desc = f"O signo {nome} ({s['datas']}): personalidade, amor, trabalho e dinheiro, compatibilidades e o horóscopo de hoje, pelo Mestre Alberto."
    el = ELEM[i % 4]; md = MOD[i % 3]; op = S[(i + 6) % 12]
    afins = [S[j] for j in range(12) if j != i and (j % 4 == i % 4 or (i % 4 in (0, 2) and j % 4 in (0, 2)) or (i % 4 in (1, 3) and j % 4 in (1, 3)))]
    nm = lambda x: x["pt"] if x["pt"] == x["br"] else f"{x['pt']} ({x['br']})"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": titulo, "description": desc, "image": img, "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Os 12 Signos", "item": SITE + "/signos-do-zodiaco"},
            {"@type": "ListItem", "position": 3, "name": nome, "item": url}]}]}
    corpo = f"""  <section class="heroi">
    <img class="foto-mestre" src="/signos/{i:02d}.webp" alt="Signo {E(nome)}" width="120" height="120" />
    <h1><span class="az">{GLIFO[i]}︎ Signo {E(nome)}</span></h1>
    <p class="sub">{E(s['datas'])} · signo de {el} · regido por {E(s['regente'])}</p>
  </section>
  <section class="cartao hoje">
    <h2>✨ Horóscopo de hoje para {E(s['pt'])}</h2>
    <div id="hoje"><p class="aviso">A carregar o céu de hoje…</p></div>
    <div class="ligas"><a href="/horoscopo-do-dia#s{i}">Ver os 12 signos de hoje</a><a href="/fimdesemana">Fim de semana</a><a href="/anual">Previsão anual</a></div>
  </section>
  <section class="cartao texto">
    <div class="perfil">
      <div><b>Datas</b>{E(s['datas'])}</div><div><b>Elemento</b>{el}</div><div><b>Modalidade</b>{md}</div><div><b>Regente</b>{E(s['regente'])}</div><div><b>Signo oposto</b><a href="/signo/{op['slug']}">{E(nm(op))}</a></div>
    </div>
    <h2>A personalidade de {E(s['pt'])}</h2><p>{E(s['essencia'])}</p>
    <h2>{E(s['pt'])} no amor</h2><p>{E(s['amor'])}</p>
    <h2>Trabalho e dinheiro</h2><p>{E(s['trabalho'])}</p>
    <h2>O desafio de {E(s['pt'])}</h2><p>{E(s['desafio'])}</p>
    <h2>Com que signos combina {E(s['pt'])}?</h2>
    <p>Pela tradição dos elementos, {E(s['pt'])} entende-se naturalmente com {", ".join(f'<a href="/signo/{x["slug"]}">{E(nm(x))}</a>' for x in afins)}. Mas um casal é muito mais do que o signo solar: para ver a ligação a sério, use a <a href="/compatibilidade">Compatibilidade</a> ou o <a href="/mapa-do-casal">Mapa do Casal</a>.</p>
    <p>Nasceu perto do início ou do fim destas datas? O dia exato da mudança de signo varia de ano para ano. E o seu <a href="/ascendente">Ascendente</a> diz tanto sobre si como o signo solar.</p>
  </section>
  <section class="cartao" style="text-align:center">
    <h2>Quer saber o que as cartas dizem para si?</h2>
    <p>Faça uma tiragem no <a href="/tarot-gratis">Tarot Grátis</a> ou marque uma consulta com o Mestre Alberto.</p>
    <a class="cta" href="/loja">Marcar consulta</a>
    <div class="ligas">{"".join(f'<a href="/signo/{x["slug"]}">{GLIFO[j]}︎ {E(x["pt"])}</a>' for j, x in enumerate(S) if j != i)}</div>
  </section>
"""
    js = f"""<script>
(function () {{
  var i = {i}, tz = (Intl.DateTimeFormat().resolvedOptions().timeZone || "").indexOf("Europe") === 0 ? "Europe/Lisbon" : "America/Sao_Paulo";
  try {{ tz = localStorage.getItem("lua-fuso") || tz; }} catch (e) {{}}
  var PT = ["Carneiro","Touro","Gémeos","Caranguejo","Leão","Virgem","Balança","Escorpião","Sagitário","Capricórnio","Aquário","Peixes"],
      BR = ["Áries","Touro","Gêmeos","Câncer","Leão","Virgem","Libra","Escorpião","Sagitário","Capricórnio","Aquário","Peixes"], N = tz === "Europe/Lisbon" ? PT : BR;
  var ESC = function (s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }}[c]; }}); }};
  var hora = function (ms) {{ return new Intl.DateTimeFormat("pt-PT", {{ timeZone: tz, hour: "2-digit", minute: "2-digit" }}).format(new Date(ms)); }};
  var por = function (t) {{ return ESC(t).replace(/\\{{S:(\\d+)\\}}/g, function (_, n) {{ return N[+n]; }}).replace(/\\{{H:(\\d+)\\}}/g, function (_, ms) {{ return hora(+ms); }}); }};
  var iso = new Intl.DateTimeFormat("en-CA", {{ timeZone: tz }}).format(new Date());
  fetch("/horoscopo-dia/" + iso + ".json").then(function (r) {{ if (!r.ok) throw 0; return r.json(); }}).then(function (x) {{
    var y = x.s[i];
    document.getElementById("hoje").innerHTML = '<div class="ene">' + "★".repeat(y.e) + "☆".repeat(5 - y.e) + ' energia</div><div class="chave">' + por(y.k) + "</div>"
      + y.t.map(function (t) {{ return "<p>" + por(t) + "</p>"; }}).join("") + '<div class="dica"><b>👉 A dica de hoje</b> ' + por(y.d) + "</div>";
  }}).catch(function () {{ document.getElementById("hoje").innerHTML = '<p><a href="/horoscopo-do-dia#s{i}">Ver o horóscopo de hoje</a></p>'; }});
}})();
</script>
"""
    open(f"signo/{s['slug']}.html", "w", encoding="utf-8").write(cabeca(titulo, desc, url, img, ld, APROVADO) + corpo + js + RODAPE)
# a montra dos 12
url = SITE + "/signos-do-zodiaco"
titulo = "Os 12 Signos do Zodiaco: datas, características e horóscopo".replace("Zodiaco", "Zodíaco")
desc = "Descubra o seu signo: as datas dos 12 signos do zodíaco, a personalidade, o amor e o horóscopo de hoje de cada um, pelo Mestre Alberto."
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": titulo, "description": desc, "url": url, "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Os 12 Signos", "item": url}]}]}
grelha = "".join(f'<a href="/signo/{x["slug"]}"><img src="/signos/{j:02d}.webp" alt="" width="58" height="58" loading="lazy"><span><b>{GLIFO[j]}︎ {E(x["pt"] if x["pt"] == x["br"] else x["pt"] + " (" + x["br"] + ")")}</b><small>{E(x["datas"])} · {ELEM[j % 4]}</small></span></a>' for j, x in enumerate(S))
corpo = f"""  <section class="heroi">
    <h1><span class="az">Os 12 Signos do Zodíaco</span></h1>
    <p class="sub">Escolha o seu signo para ver a personalidade, o amor, o trabalho e o horóscopo de hoje.</p>
  </section>
  <section><div class="doze">{grelha}</div></section>
  <section class="cartao texto">
    <h2>Os quatro elementos</h2>
    <p>Os signos dividem-se em quatro elementos. <b>Fogo</b> (Carneiro, Leão, Sagitário): entusiasmo e ação. <b>Terra</b> (Touro, Virgem, Capricórnio): estabilidade e sentido prático. <b>Ar</b> (Gémeos, Balança, Aquário): ideias e comunicação. <b>Água</b> (Caranguejo, Escorpião, Peixes): emoção e intuição.</p>
    <p>No Brasil, alguns signos têm outro nome: Carneiro é Áries, Gémeos é Gêmeos, Caranguejo é Câncer e Balança é Libra.</p>
    <div class="ligas"><a href="/horoscopo-do-dia">Horóscopo de hoje</a><a href="/ascendente">Calcular o Ascendente</a><a href="/compatibilidade">Compatibilidade</a><a href="/lua">A Lua de hoje</a></div>
  </section>
"""
open("signos-do-zodiaco.html", "w", encoding="utf-8").write(cabeca(titulo, desc, url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
print("13 páginas", "(aprovadas)" if APROVADO else "(noindex: por aprovar)")

# ── A página local: Tarólogo em Fafe (31/10/2026: ele atende no consultório de Fafe; ficha no Google Maps
#    «Genialtarot - Mestre Alberto»). Nome, morada e telefone IGUAIS aos do Maps (o Google cruza-os).
MAPS = "https://maps.google.com/?cid=17405932589735170894"
url = SITE + "/tarologo-fafe"
titulo = "Tarólogo em Fafe: consultas de Tarot com o Mestre Alberto"
desc = "Consultas de Tarot e astrologia no consultório do Mestre Alberto em Fafe (Golães) ou à distância, para Portugal e Brasil. 18 anos de prática. Marcações por WhatsApp."
NEGOCIO = {"@type": "ProfessionalService", "@id": SITE + "/#consultorio", "name": "Genialtarot - Mestre Alberto", "url": SITE + "/",
           "image": SITE + "/mestre-r13.jpg", "telephone": "+351914920427", "hasMap": MAPS,
           "address": {"@type": "PostalAddress", "streetAddress": "Rua da Barreira, 92", "addressLocality": "Fafe", "postalCode": "4820-474", "addressRegion": "Braga", "addressCountry": "PT"},
           "geo": {"@type": "GeoCoordinates", "latitude": 41.4682778, "longitude": -8.1984452},
           "founder": AUTOR, "areaServed": ["Fafe", "Guimarães", "Braga", "Portugal", "Brasil"],
           "sameAs": ["https://www.youtube.com/@Genialtarot", "https://www.facebook.com/genial.tarot", "https://www.instagram.com/genialtarot/", "https://www.tiktok.com/@genialtarot"]}
ld = {"@context": "https://schema.org", "@graph": [NEGOCIO,
      {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Tarólogo em Fafe", "item": url}]}]}
corpo = f"""  <section class="heroi">
    <img class="foto-mestre" src="/mestre-r13.jpg" alt="Mestre Alberto, tarólogo em Fafe" width="120" height="120" />
    <h1><span class="az">Tarólogo em Fafe</span></h1>
    <p class="sub">Consultas de Tarot com o Mestre Alberto, no consultório em Fafe ou à distância.</p>
    <a class="cta" href="https://wa.me/351914920427">Marcar pelo WhatsApp</a>
  </section>
  <section class="cartao texto">
    <h2>Consultas de Tarot em Fafe</h2>
    <p>O Mestre Alberto lê as cartas há 18 anos e atende no seu consultório em Fafe, em Golães. Cada consulta é feita por ele, com o seu próprio baralho: não é uma plataforma com vários tarólogos, é uma pessoa que o ouve, lê as cartas e lhe responde com sinceridade.</p>
    <p>As consultas ajudam a ganhar clareza no amor, no trabalho, na família e nas decisões importantes da vida. O Tarot não substitui um médico, um advogado ou um psicólogo, mas pode ajudar a ver o seu momento com outros olhos.</p>
    <h2>Também à distância</h2>
    <p>Se não está perto de Fafe, pode fazer a consulta à distância, a partir de qualquer ponto de Portugal, do Brasil ou do mundo. A marcação é sempre pelo WhatsApp.</p>
    <h2>Onde fica o consultório</h2>
    <div class="perfil"><div><b>Morada</b>Rua da Barreira, 92<br>4820-474 Golães, Fafe</div><div><b>Marcações</b><a href="https://wa.me/351914920427">WhatsApp +351 914 920 427</a></div><div><b>Mapa</b><a href="{MAPS}">Abrir no Google Maps</a></div></div>
    <p style="text-align:center"><a class="gmaps-btn" href="{MAPS}" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 34" width="26" height="36" aria-hidden="true"><defs><linearGradient id="gm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4285F4"/><stop offset=".35" stop-color="#4285F4"/><stop offset=".35" stop-color="#EA4335"/><stop offset=".6" stop-color="#EA4335"/><stop offset=".6" stop-color="#FBBC04"/><stop offset=".78" stop-color="#FBBC04"/><stop offset=".78" stop-color="#34A853"/></linearGradient></defs><path d="M12 0C5.4 0 0 5.3 0 11.9 0 20.8 12 34 12 34s12-13.2 12-22.1C24 5.3 18.6 0 12 0z" fill="url(#gm)"/><circle cx="12" cy="12" r="4.6" fill="#fff"/></svg><span><b>Encontre-nos no Google Maps</b><small>Rua da Barreira, 92 · Golães, Fafe</small></span></a></p>
    <p>Atende quem vem de Fafe, Guimarães, Felgueiras, Cabeceiras de Basto, Póvoa de Lanhoso, Braga e de todo o Norte do país.</p>
  </section>
  <section class="cartao" style="text-align:center">
    <h2>Antes de marcar</h2>
    <p>Conheça o <a href="/sobre">Mestre Alberto</a>, veja os <a href="/loja">tipos de consulta</a>, ou experimente o <a href="/tarot-gratis">Tarot Grátis</a> e o <a href="/horoscopo-do-dia">Horóscopo do Dia</a>.</p>
    <a class="cta" href="https://wa.me/351914920427">Marcar consulta</a>
  </section>
"""
open("tarologo-fafe.html", "w", encoding="utf-8").write(cabeca(titulo, desc, url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
print("tarologo-fafe", "(aprovada)" if APROVADO else "(noindex: por aprovar)")

# ── Tarot por tema (31/10/2026, pedido dele): Amor, Dinheiro, Trabalho, Família, Heranças, Negócios, Medos e Receios,
#    Rituais, Amuletos, Cura do Medo / Talhar o Medo, Talhar o Ar, Cartomancia, Leitura de Cartas. Textos em temas-textos.py;
#    os produtos (nome e preço) lêem-se do produtos.js, para nunca ficarem desactualizados.
EXCERTO = lambda linhas: ('<h2>Um excerto da reza</h2><blockquote style="font-family:var(--serifa);font-size:1.25rem;font-style:italic;color:var(--lavanda);border-left:3px solid var(--ouro);margin:0;padding:.3rem 0 .3rem 1rem">'
    + "<br>".join(E(l) for l in linhas) + '</blockquote><p style="font-size:.9rem;color:var(--suave)">A reza completa é feita pelo Mestre Alberto, no consultório em Fafe ou à distância.</p>')
TEMAS = {}; exec(open("temas-textos.py", encoding="utf-8").read(), TEMAS); TEMAS = TEMAS["TEMAS"]
PROD = [(re.sub(r"\s+", " ", m.group(1)).strip(), m.group(2)) for m in re.finditer(r'nome\s*:\s*"([^"]+)"[\s\S]*?preco\s*:\s*"([^"]*)"', open("produtos.js", encoding="utf-8").read())]
WA = "https://wa.me/351914920427"
menu = lambda atual: "".join(f'<a href="/{t["slug"]}">{E(t["menu"])}</a>' for t in TEMAS if t["slug"] != atual)
for t in TEMAS:
    url = f"{SITE}/{t['slug']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": t["titulo"], "description": t["desc"], "image": SITE + "/og-image.jpg", "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Tarot por tema", "item": SITE + "/tarot-por-tema"},
            {"@type": "ListItem", "position": 3, "name": t["h1"], "item": url}]}]}
    secs = "".join(f"<h2>{E(h)}</h2><p>{p}</p>" for h, p in t["seccoes"])   # os parágrafos podem levar <a> (escritos por mim)
    perg = ("<h2>Perguntas que pode fazer às cartas</h2><ul>" + "".join(f"<li>{E(q)}</li>" for q in t["perguntas"]) + "</ul>") if t["perguntas"] else ""
    prods = [(n, pr) for q in t["produtos"] for n, pr in PROD if q.lower() in n.lower()]
    vistos = []; [vistos.append(x) for x in prods if x not in vistos]
    lista = ("<h2>Serviços do Mestre Alberto para este tema</h2><div class=\"ligas\">" + "".join(f'<a href="/loja">{E(n)}{" · " + E(pr) if pr else ""}</a>' for n, pr in vistos) + "</div>") if vistos else ""
    aviso = f'<p style="font-size:.9rem;color:var(--suave)">⚠️ {E(t["aviso"])}</p>' if t.get("aviso") else ""
    if t.get("reza"): secs += EXCERTO(t["reza"])
    corpo = f"""  <section class="heroi">
    <img class="foto-mestre" src="/mestre-r13.jpg" alt="Mestre Alberto" width="120" height="120" />
    <h1><span class="az">{E(t['h1'])}</span></h1>
    <p class="sub">{E(t['sub'])}</p>
    <a class="cta" href="{WA}">Falar com o Mestre Alberto</a>
  </section>
  <section class="cartao texto">{secs}{perg}{aviso}</section>
  <section class="cartao texto" style="text-align:center">{lista}
    <p>Pode fazer a consulta no <a href="/tarologo-fafe">consultório em Fafe</a> ou à distância, a partir de Portugal, do Brasil ou de qualquer país.</p>
    <a class="cta" href="{WA}">Marcar pelo WhatsApp</a>
  </section>
  <section class="cartao" style="text-align:center"><h2>Outros temas</h2><div class="ligas">{menu(t['slug'])}<a href="/signos-do-zodiaco">♈︎ Os 12 Signos</a><a href="/tarot-gratis">🃏 Tarot Grátis</a></div></section>
"""
    open(f"{t['slug']}.html", "w", encoding="utf-8").write(cabeca(t["titulo"], t["desc"], url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
url = SITE + "/tarot-por-tema"; titulo = "Tarot por tema: amor, dinheiro, trabalho, família e mais"
desc = "Escolha o tema da sua pergunta: amor, dinheiro, trabalho, família, heranças, negócios, medos, rituais, amuletos e tradições portuguesas, com o Mestre Alberto."
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": titulo, "description": desc, "url": url, "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Tarot por tema", "item": url}]}]}
grelha = "".join(f'<a href="/{t["slug"]}"><span><b>{E(t["menu"])}</b><small>{E(t["sub"])}</small></span></a>' for t in TEMAS)
corpo = f"""  <section class="heroi">
    <h1><span class="az">Tarot por tema</span></h1>
    <p class="sub">Escolha o tema da sua pergunta e veja como as cartas e o Mestre Alberto o podem ajudar.</p>
  </section>
  <section><div class="doze">{grelha}</div></section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/signos-do-zodiaco">♈︎ Os 12 Signos</a><a href="/tarot-gratis">🃏 Tarot Grátis</a><a href="/tarologo-fafe">📍 Consultório em Fafe</a><a href="/loja">🛍️ Loja</a></div></section>
"""
open("tarot-por-tema.html", "w", encoding="utf-8").write(cabeca(titulo, desc, url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
print(len(TEMAS), "temas + a montra /tarot-por-tema")

# ── Rezas e Orações (31/10/2026, pedido dele): a tradição explicada + só um EXCERTO da reza (nunca a reza inteira).
#    Textos em rezas-textos.py (fonte: o Obsidian dele). Montra /rezas-e-oracoes.
REZ = {}; exec(open("rezas-textos.py", encoding="utf-8").read(), REZ); REZAS = REZ["REZAS"]
ligadas = [("talhar-o-ar", "Talhar o Ar"), ("talhar-o-medo", "Cura do Medo · Talhar o Medo")]
todas = [(r["slug"], r["menu"]) for r in REZAS] + ligadas
for r in REZAS:
    url = f"{SITE}/{r['slug']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": r["titulo"], "description": r["desc"], "image": SITE + "/og-image.jpg", "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Rezas e Orações", "item": SITE + "/rezas-e-oracoes"},
            {"@type": "ListItem", "position": 3, "name": r["h1"], "item": url}]}]}
    secs = "".join(f"<h2>{E(h)}</h2><p>{p}</p>" for h, p in r["seccoes"]) + (EXCERTO(r["reza"]) if r["reza"] else "")
    aviso = f'<p style="font-size:.9rem;color:var(--suave)">⚠️ {E(r.get("aviso") or REZ["CUIDADO"])}</p>'
    outras = "".join(f'<a href="/{s}">{E(m)}</a>' for s, m in todas if s != r["slug"])
    corpo = f"""  <section class="heroi">
    <img class="foto-mestre" src="/mestre-r13.jpg" alt="Mestre Alberto" width="120" height="120" />
    <h1><span class="az">{E(r['h1'])}</span></h1>
    <p class="sub">{E(r['sub'])}</p>
    <a class="cta" href="{WA}">Pedir esta reza ao Mestre Alberto</a>
  </section>
  <section class="cartao texto">{secs}{aviso}</section>
  <section class="cartao" style="text-align:center">
    <h2>O Mestre Alberto faz esta reza</h2>
    <p>No <a href="/tarologo-fafe">consultório em Fafe</a> ou à distância, para Portugal, Brasil e todo o mundo. Fale com ele pelo WhatsApp.</p>
    <a class="cta" href="{WA}">Marcar pelo WhatsApp</a>
    <h2 style="margin-top:1.4rem">Outras rezas e benzeduras</h2><div class="ligas">{outras}<a href="/benzimentos">✝️ Benzimentos</a></div>
  </section>
"""
    open(f"{r['slug']}.html", "w", encoding="utf-8").write(cabeca(r["titulo"], r["desc"], url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
url = SITE + "/rezas-e-oracoes"; titulo = "Rezas e Orações tradicionais portuguesas: quebranto, mau olhado, talhar o ar"
desc = "As rezas e benzeduras da tradição portuguesa: tirar o quebranto, mau olhado, mal de inveja, talhar o ar, o sol e o medo, espinhela caída, responsos a Santo António. Com o Mestre Alberto."
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": titulo, "description": desc, "url": url, "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Rezas e Orações", "item": url}]}]}
grelha = "".join(f'<a href="/{r["slug"]}"><span><b>🙏 {E(r["h1"])}</b><small>{E(r["sub"])}</small></span></a>' for r in REZAS) + "".join(f'<a href="/{s}"><span><b>🙏 {E(m)}</b></span></a>' for s, m in ligadas)
corpo = f"""  <section class="heroi">
    <h1><span class="az">Rezas e Orações</span></h1>
    <p class="sub">As rezas e benzeduras que as nossas avós guardaram, explicadas pelo Mestre Alberto, que as faz no consultório em Fafe e à distância.</p>
    <a class="cta" href="{WA}">Falar com o Mestre Alberto</a>
  </section>
  <section><div class="doze">{grelha}</div></section>
  <section class="cartao texto"><p style="font-size:.9rem;color:var(--suave)">⚠️ {E(REZ["CUIDADO"])} Perante qualquer sintoma físico, procure sempre um profissional de saúde.</p>
  <div class="ligas"><a href="/benzimentos">✝️ Benzimentos</a><a href="/rituais">🕯️ Rituais</a><a href="/tarot-por-tema">🃏 Tarot por tema</a><a href="/tarologo-fafe">📍 Consultório em Fafe</a></div></section>
"""
open("rezas-e-oracoes.html", "w", encoding="utf-8").write(cabeca(titulo, desc, url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
print(len(REZAS), "rezas + a montra /rezas-e-oracoes")

# ── Parábolas e Histórias (31/10/2026, pedido dele). Primeiro quis só amostra; depois decidiu: «coloca no site a parábola
#    completa». A fonte (recontada por palavras nossas) vive no cofre (Obsidian); a página leva a história, a lição e a
#    reflexão. Se o cofre estiver fechado, as páginas já feitas ficam como estão. Montra /parabolas.
PAR_F = "/media/veracrypt23/ObsidianS/CentralS/Central Tarot/📖 Parábolas recontadas (conteúdo pago)/parabolas-textos.py"
if os.path.exists(PAR_F):
    PAR = {}; exec(open(PAR_F, encoding="utf-8").read(), PAR); PAR = PAR["PARABOLAS"]
    TEMA_TXT = lambda p: " · ".join(p.get("temas", []))
    for k, p in enumerate(PAR):
        url = f"{SITE}/{p['slug']}"
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "headline": p["titulo"], "description": p["desc"], "image": SITE + "/og-image.jpg", "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR, "mainEntityOfPage": url, "keywords": ", ".join(["parábola"] + p.get("temas", []))},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Parábolas", "item": SITE + "/parabolas"},
                {"@type": "ListItem", "position": 3, "name": p["titulo_curto"], "item": url}]}]}
        viz = [PAR[(k + d) % len(PAR)] for d in (1, 2, 3, -1)]
        corpo = f"""  <section class="heroi">
    <h1><span class="az">{E(p['titulo_curto'])}</span></h1>
    <p class="sub">Uma parábola contada pelo Mestre Alberto{(" · " + E(TEMA_TXT(p))) if p.get("temas") else ""}</p>
  </section>
  <section class="cartao texto">{"".join(f"<p>{E(x)}</p>" for x in p["historia"])}
    <h2>A lição</h2><blockquote style="font-family:var(--serifa);font-size:1.3rem;font-style:italic;color:var(--ouro);border-left:3px solid var(--ouro);margin:0;padding:.3rem 0 .3rem 1rem">{E(p['moral'])}</blockquote>
    <h2>Para a sua vida</h2><p>{E(p['reflexao'])}</p>
    <div style="text-align:center;margin-top:1rem"><a class="cta" href="{WA}">Falar com o Mestre Alberto</a></div>
  </section>
  <section class="cartao" style="text-align:center">
    <h2>Outras parábolas</h2><div class="ligas">{"".join(f'<a href="/{v["slug"]}">{E(v["titulo_curto"])}</a>' for v in viz)}<a href="/parabolas">📖 Todas as parábolas</a></div>
    <p>Experimente também o <a href="/tarot-gratis">Tarot Grátis</a> ou veja as <a href="/rezas-e-oracoes">Rezas e Orações</a>.</p>
  </section>
"""
        open(f"{p['slug']}.html", "w", encoding="utf-8").write(cabeca(p["titulo"], p["desc"], url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
    url = SITE + "/parabolas"; titulo = "Parábolas e Histórias com Lição de Vida | Mestre Alberto"
    desc = "Parábolas e histórias com lição de vida sobre escolhas, amor, persistência, gratidão e coragem, contadas pelo Mestre Alberto. Pequenas histórias para pensar."
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": titulo, "description": desc, "url": url, "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Parábolas", "item": url}]}]}
    grelha = "".join(f'<a href="/{p["slug"]}"><span><b>📖 {E(p["titulo_curto"])}</b><small>{E(TEMA_TXT(p))}</small></span></a>' for p in PAR)
    corpo = f"""  <section class="heroi">
    <h1><span class="az">Parábolas e Histórias</span></h1>
    <p class="sub">Pequenas histórias com grandes lições, para pensar sobre as escolhas, o amor e o caminho de cada um.</p>
  </section>
  <section><div class="doze">{grelha}</div></section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/rezas-e-oracoes">🙏 Rezas e Orações</a><a href="/tarot-por-tema">🃏 Tarot por tema</a><a href="/signos-do-zodiaco">♈︎ Os 12 Signos</a></div></section>
"""
    open("parabolas.html", "w", encoding="utf-8").write(cabeca(titulo, desc, url, SITE + "/og-image.jpg", ld, APROVADO) + corpo + RODAPE)
    print(len(PAR), "parábolas + a montra /parabolas")
