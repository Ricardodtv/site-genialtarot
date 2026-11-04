#!/usr/bin/env python3
"""Escolha um Monte — a mensagem do Tarot da semana (04/11/2026, pedido dele: «agora faz o escolha um monte»;
ideia n.º 1 da análise do giatho.com: o formato «pick a pile», que muda todas as semanas e nunca se repete).

Gera, a partir de escolha-um-monte-textos.py (SEMANAS = {segunda-feira: [3 montes]}, textos escritos de raiz):
  · escolha-um-monte.html                         → a semana de hoje (hora de Lisboa)
  · escolha-um-monte-<d>-<mês>-<ano>.html          → cada semana JÁ PASSADA fica arquivada na sua própria página
CSS base, botão de som e música copiados da horoscopo-do-dia.html (como as outras tiragens).
    python3 escolha-um-monte-gerar.py [AAAA-MM-DD]   → gera para essa data (por omissão, hoje)
Corre todas as segundas às 00:10 pelo escolha-um-monte.timer (escolha-um-monte-publicar.sh: gera, commit e push).
⚠️ Antes de acabarem as semanas escritas, o gerador avisa (faltam ≤ 3) — é preciso escrever mais."""
import datetime, html, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
e = lambda s: html.escape(str(s), quote=True)

T = {}; exec(open("escolha-um-monte-textos.py", encoding="utf-8").read(), T)
SEMANAS = T["SEMANAS"]

# ── as cartas: nome, imagem e página do site ──
MAIORES = {}
for f in sorted(os.listdir("cartas")):
    m = re.match(r"(\d\d)-(.+)\.webp$", f)
    if m:
        h = open(f"arcano-{m.group(1)}-{m.group(2)}.html", encoding="utf-8").read()
        nome = re.search(r"<title>([^<:—|]+)", h).group(1).strip()
        nome = re.sub(r"\s*\(.*$", "", re.sub(r"\s+no Tarot.*$", "", nome)).strip()
        MAIORES[f[:-5]] = {"nome": nome, "img": f"/cartas/{f}", "url": f"/arcano-{f[:-5]}"}
MT = {}; exec(open("arcanos-menores-textos.py", encoding="utf-8").read(), MT)
MENORES = {c["slug"]: {"nome": c["nome"], "img": f"/cartas/menores/{c['img']}", "url": f"/{c['slug']}"} for c in MT["MENORES"]}
CARTA = {**MAIORES, **MENORES}

from zoneinfo import ZoneInfo
hoje = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now(ZoneInfo("Europe/Lisbon")).date()
segs = sorted(SEMANAS)
atual = max([s for s in segs if s <= hoje.isoformat()], default=None)
if not atual: sys.exit("nenhuma semana escrita começa antes de " + hoje.isoformat())
faltam = len([s for s in segs if s > atual])
if faltam <= 3: print(f"⚠️ ESCOLHA UM MONTE: só faltam {faltam} semana(s) escritas depois de {atual} — escrever mais")

def intervalo(seg):
    a = datetime.date.fromisoformat(seg); b = a + datetime.timedelta(days=6)
    if a.month == b.month: return f"{a.day} a {b.day} de {MESES[a.month - 1]} de {a.year}"
    if a.year == b.year: return f"{a.day} de {MESES[a.month - 1]} a {b.day} de {MESES[b.month - 1]} de {a.year}"
    return f"{a.day} de {MESES[a.month - 1]} de {a.year} a {b.day} de {MESES[b.month - 1]} de {b.year}"
def slug_semana(seg):
    a = datetime.date.fromisoformat(seg); return f"escolha-um-monte-{a.day}-{MESES[a.month - 1].replace('ç', 'c')}-{a.year}"

# ── a base visual (da horoscopo-do-dia.html) ──
ref = open("horoscopo-do-dia.html", encoding="utf-8").read().split("\n")
CSS_BASE = "\n".join(ref[23:59]) + "\n" + "\n".join(ref[87:116])
assert CSS_BASE.lstrip().startswith(":root") or ":root" in CSS_BASE[:400], "os blocos da referência mudaram de sítio (CSS)"
i0 = next(i for i, l in enumerate(ref) if l.startswith("<script>") and "audio" in "\n".join(ref[i:i + 15]).lower())
i1 = next(i for i in range(i0, len(ref)) if ref[i].startswith("</script>"))
MUSICA = "\n".join(ref[i0:i1 + 1])
BOTAO_SOM = [l for l in ref if l.startswith('<button id="audio-fab"')][0]

CSS = r"""
/* ============ Escolha um Monte (04/11/2026) ============ */
.texto { font-family: var(--serifa); font-size: 1.15rem; color: var(--lavanda); }
.texto h2 { text-align: left; } .texto p { margin: 0 0 .8rem; } .texto b { color: var(--texto); }
.texto h3 { font-family: var(--titulo); font-size: 1.05rem; color: var(--ouro); margin: 1.1rem 0 .3rem; }
.semana { display: inline-block; font-family: Inter, sans-serif; font-weight: 700; font-size: .85rem; letter-spacing: .08em; color: var(--ouro);
  border: 1px solid oklch(0.85 0.13 88 / .5); border-radius: 999px; padding: .3rem .9rem; margin-bottom: .4rem; }
.montes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; max-width: 40rem; margin: 1.6rem auto .6rem; }
.monte { position: relative; border: 0; background: none; padding: 0 0 2.2rem; cursor: pointer; color: var(--texto); font: inherit;
  transition: transform .35s, opacity .4s, filter .4s; -webkit-tap-highlight-color: transparent; }
.monte .pilha { position: relative; display: block; aspect-ratio: 480 / 804; margin: 0 11%; animation: monte-flutua 5s ease-in-out infinite; }   /* margem: as cartas de lado não saem do ecrã */
.monte:nth-child(2) .pilha { animation-delay: -1.6s; } .monte:nth-child(3) .pilha { animation-delay: -3.2s; }
.monte .pilha img { position: absolute; inset: 0; width: 100%; height: 100%; border-radius: .55rem; border: 1px solid oklch(0.85 0.13 88 / .6);
  box-shadow: 0 10px 26px #000b; transition: transform .45s cubic-bezier(.3,.7,.3,1); }
.monte .pilha img:nth-child(1) { transform: translate(-7%, 5%) rotate(-7deg); }
.monte .pilha img:nth-child(2) { transform: translate(6%, 3%) rotate(6deg); }
.monte .pilha img:nth-child(3) { transform: translate(0, 0) rotate(-1deg); }
.monte:hover .pilha img:nth-child(1), .monte:focus-visible .pilha img:nth-child(1) { transform: translate(-16%, 4%) rotate(-13deg); }
.monte:hover .pilha img:nth-child(2), .monte:focus-visible .pilha img:nth-child(2) { transform: translate(15%, 3%) rotate(12deg); }
.monte:hover .pilha img:nth-child(3), .monte:focus-visible .pilha img:nth-child(3) { transform: translateY(-6%); }
.monte .rotulo { position: absolute; left: 0; right: 0; bottom: 0; font-family: var(--titulo); font-weight: 700; font-size: 1.05rem; color: var(--ouro); }
.monte .rotulo small { display: block; font-family: Inter, sans-serif; font-weight: 600; font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; color: var(--suave); }
.montes.escolhido .monte:not(.este) { opacity: .35; filter: grayscale(.6); transform: scale(.92); }
.montes.escolhido .monte.este { transform: translateY(-4px); }
@keyframes monte-flutua { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
.dica-monte { text-align: center; font-family: var(--serifa); font-size: 1.15rem; color: var(--lavanda); max-width: 34rem; margin: 0 auto; }
.leitura-monte { scroll-margin-top: 1rem; }
.js .leitura-monte { display: none; }
.js .leitura-monte.vista { display: block; animation: monte-surge .7s ease both; }
@keyframes monte-surge { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
.tres { display: grid; grid-template-columns: repeat(3, 1fr); gap: .8rem; max-width: 30rem; margin: .8rem auto 1.2rem; perspective: 900px; }
.tres a { display: block; text-decoration: none; color: var(--texto); text-align: center; font-family: Inter, sans-serif; font-size: .82rem; font-weight: 700; }
.tres .vira { position: relative; display: block; aspect-ratio: 480 / 804; transform-style: preserve-3d; transition: transform .9s cubic-bezier(.3,.7,.3,1); margin-bottom: .4rem; }
/* 04/11: a viragem, carta a carta (o JS põe .virada em cada uma, com o som): levanta-se, gira em 3D e acende um brilho dourado */
.js .leitura-monte .tres .vira { transform: rotateY(180deg); transition: none; }
.js .leitura-monte .tres a.virada .vira { animation: carta-vira 1.05s cubic-bezier(.3,.7,.3,1) forwards; }
.js .leitura-monte .tres a.virada .vira img:not(.costas) { animation: carta-brilho 1.8s ease .55s; }
@keyframes carta-vira { 0% { transform: rotateY(180deg) translateY(0) scale(1); } 45% { transform: rotateY(95deg) translateY(-16px) scale(1.14); }
  75% { transform: rotateY(-8deg) translateY(-4px) scale(1.04); } 100% { transform: rotateY(0) translateY(0) scale(1); } }
@keyframes carta-brilho { 0%, 100% { box-shadow: 0 8px 22px #000a; } 35% { box-shadow: 0 0 32px oklch(0.85 0.13 88 / .9), 0 0 6px oklch(0.95 0.08 90), 0 8px 22px #000a; } }
/* ao escolher, o monte «baralha-se» antes de abrir */
.monte.baralha .pilha img:nth-child(1) { animation: baralha-a .32s ease-in-out 2; }
.monte.baralha .pilha img:nth-child(2) { animation: baralha-b .32s ease-in-out 2; }
.monte.baralha .pilha img:nth-child(3) { animation: baralha-c .32s ease-in-out 2; }
@keyframes baralha-a { 0%, 100% { transform: translate(-7%, 5%) rotate(-7deg); } 50% { transform: translate(-34%, -2%) rotate(-18deg); } }
@keyframes baralha-b { 0%, 100% { transform: translate(6%, 3%) rotate(6deg); } 50% { transform: translate(33%, -3%) rotate(17deg); } }
@keyframes baralha-c { 0%, 100% { transform: translate(0, 0) rotate(-1deg); } 50% { transform: translateY(-14%) rotate(2deg); } }
.tres .vira img { position: absolute; inset: 0; width: 100%; height: 100%; border-radius: .5rem; border: 1px solid oklch(0.85 0.13 88 / .6);
  box-shadow: 0 8px 22px #000a; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
.tres .vira img.costas { transform: rotateY(180deg); }
.tres a:hover { color: var(--ouro); }
.titulo-monte { font-family: var(--serifa); font-style: italic; font-weight: 600; font-size: 1.5rem; color: var(--ouro); text-align: center; margin: 0 0 .6rem; }
.areas { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; margin: 1rem 0; font-family: Inter, sans-serif; font-size: .95rem; }
.areas div { background: var(--vidro); border: 1px solid var(--borda); border-radius: .9rem; padding: .7rem .9rem; color: var(--lavanda); }
.areas b { display: block; color: var(--ouro); font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; margin-bottom: .2rem; }
.conselho { font-family: var(--serifa); font-size: 1.2rem; border-left: 3px solid var(--ouro); padding: .4rem .9rem; background: oklch(0.85 0.13 88 / .07); border-radius: 0 .6rem .6rem 0; }
.outros { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; margin-top: 1rem; }
.arquivo { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; }
.arquivo a { text-decoration: none; font-family: Inter, sans-serif; font-size: .85rem; font-weight: 700; color: var(--texto); border: 1px solid var(--borda);
  background: var(--vidro); border-radius: 999px; padding: .4rem .9rem; }
.arquivo a:hover { border-color: var(--ouro); }
@media (max-width: 34rem) { .montes { gap: .6rem; } .monte .rotulo { font-size: .92rem; } .areas { grid-template-columns: 1fr; } .tres { gap: .5rem; } }
@media (prefers-reduced-motion: reduce) { .monte .pilha, .monte.baralha .pilha img, .js .leitura-monte .tres a.virada .vira img { animation: none; }
  .tres .vira, .monte, .monte .pilha img { transition: none; } .js .leitura-monte .tres .vira, .js .leitura-monte .tres a.virada .vira { transform: none; animation: none; } }
"""

FAQ = [
    ("Como funciona o Escolha um Monte?",
     "Pense numa pergunta ou numa situação da sua vida, respire fundo e escolha o monte que mais o chama: o 1, o 2 ou o 3. Cada monte tem três cartas do baralho do Mestre Alberto e uma mensagem escrita para essa combinação. Não há monte certo nem errado: escolha pela intuição, sem pensar muito."),
    ("A mensagem muda quando?",
     "Todas as segundas-feiras há três montes novos, com cartas e mensagens novas. As semanas que já passaram ficam guardadas no arquivo, no fim da página, para poder voltar a elas."),
    ("Posso escolher mais do que um monte?",
     "Pode ler os três, mas a mensagem que é para si costuma ser a do monte que escolheu primeiro, sem pensar. Se os três lhe falarem, leia-os como um todo: o que se repete é o mais importante."),
    ("É grátis?",
     "Sim. O Escolha um Monte é grátis e não precisa de dar o seu email. Se quiser uma leitura só sua, com as cartas tiradas para a sua pergunta, pode pedir uma consulta ao Mestre Alberto."),
    ("As cartas saem ao acaso?",
     "Não: nesta tiragem coletiva, as cartas de cada monte são escolhidas e lidas em conjunto, semana a semana, para que cada mensagem tenha princípio, meio e fim. Para uma tiragem ao acaso, só para si, use o Tarot Grátis."),
]


def pagina(seg, atual_pag):
    montes = SEMANAS[seg]
    assert len(montes) == 3
    quando = intervalo(seg)
    if atual_pag:
        slug = "escolha-um-monte"
        titulo = "Escolha um Monte: a mensagem do Tarot desta semana"
        desc = f"Escolha um monte de cartas e leia a mensagem do Tarot para esta semana, de {quando}. Grátis, com o baralho do Mestre Alberto. Muda às segundas."
        h1 = 'Escolha um <span class="az">Monte</span>'
    else:
        slug = slug_semana(seg)
        titulo = f"Escolha um Monte: semana de {quando.split(' de 20')[0]}"
        desc = f"O Escolha um Monte da semana de {quando}: três montes de cartas do Tarot e a mensagem de cada um, pelo baralho do Mestre Alberto."
        h1 = f'Escolha um <span class="az">Monte</span><br><small style="font-size:.5em">semana de {e(quando)}</small>'
    if len(titulo) > 65: titulo = titulo[:62].rsplit(" ", 1)[0] + "…"
    while len(desc) > 160: desc = desc.rsplit(" ", 1)[0].rstrip(",.") + "."
    url = f"{SITE}/{slug}"
    verso = '<img src="/cartas/verso-gt.webp" alt="" width="480" height="804">'
    botoes = "".join(
        f'<button type="button" class="monte" data-m="{n}" aria-controls="monte-{n}" aria-label="Escolher o monte {n}">'
        f'<span class="pilha">{verso * 3}</span><span class="rotulo">Monte {n}<small>escolher</small></span></button>' for n in (1, 2, 3))
    leituras = ""
    for n, m in enumerate(montes, 1):
        cs = [CARTA[c] for c in m["cartas"]]
        tres = "".join(f'<a href="{c["url"]}"><span class="vira"><img src="{c["img"]}" alt="Carta {e(c["nome"])} do baralho do Mestre Alberto — Escolha um Monte, monte {n}" width="480" height="804" loading="lazy">'
                       f'<img class="costas" src="/cartas/verso-gt.webp" alt="" width="480" height="804" loading="lazy"></span>{e(c["nome"])}</a>' for c in cs)
        outros = "".join(f'<button type="button" class="btn" data-ver="{k}">Ver o monte {k}</button>' for k in (1, 2, 3) if k != n)
        leituras += f"""
  <section class="cartao texto leitura-monte" id="monte-{n}">
    <h2>Monte {n}</h2>
    <p class="titulo-monte">{e(m['titulo'])}</p>
    <div class="tres">{tres}</div>
    <p>{e(m['mensagem'])}</p>
    <div class="areas"><div><b>💗 No amor</b>{e(m['amor'])}</div><div><b>💼 No trabalho e no dinheiro</b>{e(m['trabalho'])}</div></div>
    <p class="conselho"><b>O conselho da semana:</b> {e(m['conselho'])}</p>
    <div class="outros">{outros}<a class="btn ouro" href="/tarot-gratis">🃏 Tirar as minhas cartas</a></div>
  </section>"""
    passadas = [s for s in segs if s < atual]
    arquivo = "".join(f'<a href="/{slug_semana(s)}">{e(intervalo(s).split(" de 20")[0])}</a>' for s in reversed(passadas) if s != seg)
    arquivo_html = (f'<section class="cartao"><h2>Semanas anteriores</h2><div class="arquivo">{arquivo}</div></section>' if arquivo else "")
    if not atual_pag:
        arquivo_html = (f'<section class="cartao" style="text-align:center"><h2>Esta semana</h2><p class="dica-monte">Os montes desta semana já são outros.</p>'
                        f'<div class="botoes" style="justify-content:center"><a class="btn ouro" href="/escolha-um-monte">🔮 Escolher o monte desta semana</a></div></section>') + arquivo_html
    faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in FAQ)
    img_og = f"{SITE}/escolha-um-monte-og.jpg"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#pagina", "name": titulo, "description": desc, "url": url, "inLanguage": "pt",
         "datePublished": seg, "dateModified": seg,
         "isPartOf": {"@type": "WebSite", "name": "Genial Tarot", "url": SITE + "/"},
         "author": {"@type": "Person", "name": "Mestre Alberto", "url": SITE + "/sobre"}, "breadcrumb": {"@id": url + "#migalhas"}},
        {"@type": "BreadcrumbList", "@id": url + "#migalhas", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Tarot Grátis", "item": SITE + "/tarot-gratis"},
            {"@type": "ListItem", "position": 3, "name": "Escolha um Monte", "item": SITE + "/escolha-um-monte"}]
            + ([] if atual_pag else [{"@type": "ListItem", "position": 4, "name": f"Semana de {quando}", "item": url}])},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    return slug, f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}" />
<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="favicon.ico" />
<meta property="og:title" content="{e(titulo)}" />
<meta property="og:description" content="{e(desc)}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{url}" />
<link rel="canonical" href="{url}" />
<meta property="og:image" content="{img_og}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Três montes de cartas do baralho do Mestre Alberto, viradas para baixo, para escolher um" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script>document.documentElement.classList.add("js");</script>
<style>
/* ============ Escolha um Monte — base copiada da horoscopo-do-dia.html (04/11/2026) ============ */
{CSS_BASE}
{CSS}
</style>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
</head>
<body>
{BOTAO_SOM}
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
  <section class="heroi">
    <div><span class="selo">🔮 Tarot da semana ✦ grátis</span></div>
    <h1>{h1}</h1>
    {'<div class="semana">' + e(quando) + '</div>' if atual_pag else ''}
    <p class="sub">Pense numa pergunta, respire fundo e escolha um dos três montes. As cartas viram-se e mostram a mensagem para a sua semana.</p>
    <div class="montes" id="montes">{botoes}</div>
    <p class="dica-monte">Escolha pela intuição: o primeiro monte que lhe chamar a atenção é o seu.</p>
  </section>
{leituras}
  <section class="cartao texto">
    <h2>O que é o Escolha um Monte</h2>
    <p>O <b>Escolha um Monte</b> é uma tiragem coletiva de Tarot: em vez de baralhar as cartas só para si, escolhe entre três montes já preparados, cada um com três cartas e uma mensagem. Ficou famosa nos vídeos de Tarot, onde se pede a quem vê que escolha o monte 1, 2 ou 3 antes de o tarólogo revelar as cartas.</p>
    <p>Aqui funciona da mesma forma, com o <a href="/tarot-gratis">baralho do Mestre Alberto</a>. Cada monte fala de uma energia diferente para a semana, no amor, no trabalho e no dinheiro, e fecha com um conselho. Os montes mudam todas as segundas-feiras.</p>
    <h2>Perguntas frequentes</h2>
    {faq_html}
  </section>
  {arquivo_html}
  <section class="cartao chamada">
    <h2>Quer uma leitura <span class="az">só sua</span>?</h2>
    <p>O Escolha um Monte é uma mensagem para muitas pessoas ao mesmo tempo. Numa consulta, o Mestre Alberto tira as cartas para a sua pergunta e lê-as com a sua história.</p>
    <div class="botoes"><a class="btn ouro" href="loja.html#cat-consultas">🔮 Marcar uma consulta</a></div>
    <div class="ligas"><a href="/tarot-gratis">🃏 Tarot Grátis</a><a href="/tarot-sim-ou-nao">Tarot Sim ou Não</a><a href="/horoscopo-semanal">📅 Horóscopo Semanal</a><a href="/tarot-cigano">Tarot Cigano</a><a href="/tiragem-templo-de-afrodite">Templo de Afrodite</a></div>
  </section>
</div>
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="privacidade.html">Política de Privacidade</a> · <a href="termos.html">Termos de Serviço</a>
</footer>
<script>
/* Escolha um Monte: escolher um monte → a leitura desse monte aparece e as três cartas viram-se */
(function () {{
  var montes = document.getElementById("montes");
  var timers = [];
  var som = function (f, i) {{ if (window[f]) window[f](i); }};   // som-monte.js (Web Audio, volume baixo)
  function abrir(n, doTopo) {{
    timers.forEach(clearTimeout); timers = [];
    var b = document.querySelector('.monte[data-m="' + n + '"]');
    document.querySelectorAll(".monte").forEach(function (x) {{ x.classList.toggle("este", x === b); x.classList.remove("baralha"); }});
    montes.classList.add("escolhido");
    var espera = 0;
    if (doTopo) {{ void b.offsetWidth; b.classList.add("baralha"); som("somBaralhar"); espera = 700; }}   // o monte baralha-se antes de abrir
    timers.push(setTimeout(function () {{
      document.querySelectorAll(".leitura-monte").forEach(function (s) {{ s.classList.remove("vista"); s.querySelectorAll(".tres a").forEach(function (a) {{ a.classList.remove("virada"); }}); }});
      var s = document.getElementById("monte-" + n);
      s.classList.add("vista");
      s.scrollIntoView({{ behavior: "smooth", block: "start" }});
      // depois de a leitura chegar ao ecrã, as três cartas viram uma a uma, cada uma com o seu som
      s.querySelectorAll(".tres a").forEach(function (a, i) {{
        timers.push(setTimeout(function () {{ a.classList.add("virada"); som("somVirar", i); }}, 750 + i * 560));
      }});
    }}, espera));
  }}
  document.querySelectorAll(".monte").forEach(function (b) {{ b.addEventListener("click", function () {{ abrir(b.dataset.m, true); }}); }});
  document.querySelectorAll("[data-ver]").forEach(function (b) {{ b.addEventListener("click", function () {{ abrir(b.dataset.ver); }}); }});
}})();
</script>
<script src="/som-monte.js" defer></script>
{MUSICA}
<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""


feitas = []
for seg in segs:
    if seg > atual: break
    slug, h = pagina(seg, False) if seg < atual else pagina(seg, True)
    f = f"{slug}.html"
    if not os.path.exists(f) or open(f, encoding="utf-8").read() != h:
        open(f, "w", encoding="utf-8").write(h); feitas.append(f)
for f in feitas: print(f)
