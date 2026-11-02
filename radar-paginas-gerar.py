#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Páginas pedidas pelo Radar de temas (02/11/2026, pedido dele: «o que farias para pôr no site, mas tem de se atualizar
automaticamente»). Escreve:
  · astrologia.html — a porta da astrologia («astrologia», «astrologia signos», «astrologia hoje» no Trends): o céu de AGORA
    (planetas e Lua, a partir de ceu-dados.js e lua-dados.js, que o site-ceu-rolante.sh renova todos os meses) e o mapa
    de todas as páginas de astrologia do site
  · lua-azul.html — «lua azul»: o que é (mensal e sazonal) e a PRÓXIMA a contar de hoje, de lua-azul-dados.js
    (lua-azul-gerar.py, também no site-ceu-rolante.sh)
Molde: horoscopo-do-dia.html (head, cores, fuso Brasil/Portugal, som, faixa VIP, vivo.js, rodapé).
    python3 ~/site-genialtarot/radar-paginas-gerar.py
"""
import json, os, re, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = open("horoscopo-do-dia.html", encoding="utf-8").read()
CAB = src[:src.index("<style>")]
EST = re.search(r"<style>.*?</style>", src, re.S).group(0)
SOM = src[src.index('<button id="audio-fab"'):src.index('<div class="estrelas"')]
ROD = src[src.index("<footer>"):src.index("</footer>") + 9]
GT = src[src.index("<script>\n/* comum às páginas novas"):src.index("</script>", src.index("/* comum às páginas novas")) + 9]
MUS = src[src.index("<script>\n/* 🎵 28/10/2026"):src.index('<script src="/vip-faixa.js"')]
E = lambda x: x.replace("&", "&amp;").replace("<", "&lt;")
ST = 'max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6'
EXTRA = """
.links { display: grid; gap: .8rem; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); }
.links a { display: block; text-decoration: none; color: var(--texto); padding: .8rem 1rem; border-radius: 1rem; background: oklch(0.20 0.06 272 / .88); border: 1px solid var(--borda); }
.links a:hover { border-color: var(--ouro); }
.links b { display: block; font-family: var(--titulo); color: var(--ouro); font-size: 1rem; }
.links small { color: var(--suave); }
.agora { display: grid; gap: .5rem; grid-template-columns: repeat(auto-fill, minmax(10.5rem, 1fr)); max-width: 52rem; margin: 0 auto; }
.agora div { padding: .6rem .8rem; border-radius: .9rem; background: oklch(0.16 0.05 270 / .7); border: 1px solid var(--borda); }
.agora b { display: block; color: var(--ouro); font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; }
.agora span { font-family: var(--serifa); font-size: 1.15rem; }
.grande { font-family: var(--titulo); font-size: clamp(1.4rem, 4vw, 2.1rem); text-align: center; margin: .3rem 0; color: var(--ouro); }
.tabela { width: 100%; max-width: 40rem; margin: 0 auto; border-collapse: collapse; }
.tabela td, .tabela th { padding: .45rem .6rem; border-bottom: 1px solid var(--borda); text-align: left; }
.tabela th { color: var(--suave); font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; }
"""


def pagina(slug, tit, desc, ogt, crumb, corpo, faq, scripts):
    url = f"https://genialtarot.com/{slug}"
    assert len(tit) <= 65 and 110 <= len(desc) <= 160, (slug, len(tit), len(desc))
    c = re.sub(r"<title>.*?</title>", f"<title>{tit}</title>", CAB).replace("https://genialtarot.com/horoscopo-do-dia", url)
    c = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + desc, c)
    c = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + desc, c)
    c = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + ogt, c)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": tit, "description": desc, "url": url, "inLanguage": "pt", "dateModified": datetime.date.today().isoformat(),
         "isPartOf": {"@type": "WebSite", "name": "Genial Tarot", "url": "https://genialtarot.com/"},
         "author": {"@type": "Person", "name": "Mestre Alberto", "url": "https://genialtarot.com/sobre"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": "https://genialtarot.com/"},
                                                      {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]}]}
    h = (c + EST.replace("</style>", EXTRA + "</style>") + f'\n<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False)}\n</script>\n</head>\n<body>\n'
         + SOM + '<div class="estrelas" aria-hidden="true"></div>\n<div class="caixa">\n'
         '  <header class="topo"><a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a></header>\n'
         + corpo + "\n</div>\n<!-- seo-extra -->\n"
         + f'<section class="faq-genial" style="{ST}"><h2 style="margin-top:0">Perguntas frequentes</h2>'
         + "".join(f'<h3 style="font-size:1.05rem;margin:1rem 0 .3rem">{E(q)}</h3><p style="margin:0">{E(r)}</p>' for q, r in faq) + "</section>\n"
         + ROD + "\n" + GT + "\n" + scripts + "\n" + MUS + '<script src="/vip-faixa.js" defer></script>\n<script src="/vivo.js" defer></script>\n</body>\n</html>\n')
    open(f"{slug}.html", "w", encoding="utf-8").write(h)
    print(slug, len(h))


HEROI = lambda selo, h1, sub: f'''  <section class="heroi">
    <img class="foto-mestre" src="mestre-diario.jpg" alt="Mestre Alberto" width="120" height="120" />
    <div><span class="selo">{selo}</span></div>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <div class="fuso" role="group" aria-label="Fuso horário"><button type="button" data-tz="America/Sao_Paulo">🇧🇷 Brasil</button><button type="button" data-tz="Europe/Lisbon">🇵🇹 Portugal</button></div>
  </section>'''

# ───────────── /astrologia ─────────────
GRUPOS = [
    ("O céu de cada dia", [("/horoscopo-do-dia", "Horóscopo do Dia", "Os 12 signos com o céu real de hoje"), ("/horoscopo-de-amanha", "Horóscopo de Amanhã", "Prepare o dia seguinte"),
                           ("/horoscopo-semanal", "Horóscopo Semanal", "A semana, o melhor dia e o de cuidado"), ("/ceu-de-hoje", "O Céu de Hoje", "Onde está cada planeta agora"),
                           ("/noticias-do-ceu", "Notícias do Céu", "O que está a acontecer lá em cima"), ("/lua", "Calendário Lunar", "Fases da Lua e a Lua nos signos")]),
    ("O seu mapa", [("/mapa-astral", "Mapa Astral", "Os planetas no minuto em que nasceu"), ("/ascendente", "Calculadora de Ascendente", "O signo que nascia no horizonte"),
                    ("/revolucao-solar", "Revolução Solar", "O seu ano de aniversário a aniversário"), ("/horoscopo-pessoal", "Horóscopo Pessoal", "O céu de hoje no seu mapa"),
                    ("/fase-lua-nascimento", "A Lua em que nasceu", "A fase da Lua no seu nascimento"), ("/astrologia-vedica", "Astrologia Védica", "O seu signo no zodíaco sideral")]),
    ("Os signos", [("/signos-do-zodiaco", "Os 12 Signos", "Características, datas e elementos"), ("/datas-dos-signos", "Datas dos Signos", "A hora exata da mudança de signo"),
                   ("/signos-que-combinam", "Signos que Combinam", "O par ideal de cada signo"), ("/compatibilidade", "Compatibilidade", "Os 78 pares de signos no amor"),
                   ("/trio-astral", "Trio Astral", "Sol, Lua e Ascendente juntos"), ("/mapa-do-casal", "Mapa do Casal", "Os dois mapas lado a lado")]),
    ("O ano e os ciclos", [("/signos-2026", "Signos 2026", "O que o ano trouxe a cada signo"), ("/melhores-signos-2027", "Melhores Signos de 2027", "Quem tem Júpiter a favor"),
                           ("/horoscopo-2027", "Horóscopo 2027", "O ano de cada signo"), ("/retrogrados", "Planetas Retrógrados", "Quando e onde andam para trás"),
                           ("/eclipses-2027", "Eclipses 2027", "As datas e os signos tocados"), ("/alinhamento-dos-planetas", "Alinhamento dos Planetas", "Quando se juntam no céu"),
                           ("/lua-azul", "Lua Azul", "A próxima e porque é rara"), ("/cor-do-ano-2027", "Cor do Ano 2027", "O regente do ano"),
                           ("/horoscopo-chines", "Horóscopo Chinês", "Os 12 animais"), ("/calendarios", "Calendários", "Luas, eclipses e retrógrados no seu telemóvel")]),
    ("Aprender astrologia", [("/planeta-sol", "Os Planetas", "O que cada planeta representa"), ("/casa-1", "As 12 Casas", "As áreas da vida no mapa"),
                             ("/elemento-fogo", "Os 4 Elementos", "Fogo, Terra, Ar e Água"), ("/efemerides", "Efemérides", "As posições dos planetas dia a dia"),
                             ("/famosos-ceu", "Famosos e o seu céu", "O mapa de pessoas conhecidas")]),
]
for g in GRUPOS:
    for u, _, _ in g[1]: assert os.path.exists(u[1:] + ".html") or u in ("/astrologia", "/lua-azul"), u
corpo = HEROI("✦ Astrologia ✦ céu real", 'A <span class="az">Astrologia</span> no Genial Tarot',
              "O céu deste momento e tudo o que precisa para ler os signos, o seu mapa e os ciclos do ano, sempre com o céu calculado e não inventado.") + '''
  <section class="cartao">
    <h2>O céu agora</h2>
    <p class="grande" id="ag-quando"></p>
    <div class="agora" id="ag"></div>
    <p class="fonte" id="ag-lua"></p>
    <p class="fonte">Calculado com o Swiss Ephemeris (zodíaco tropical). Atualiza-se sozinho: volte amanhã e o céu já mudou. ℞ = retrógrado.</p>
  </section>
''' + "".join(f'''  <section class="cartao"><h2>{t}</h2><div class="links">''' + "".join(f'<a href="{u}"><b>{n}</b><small>{d}</small></a>' for u, n, d in l) + "</div></section>\n" for t, l in GRUPOS) + '''  <section class="cartao chamada">
    <h2>A <span class="az">sua</span> leitura</h2>
    <p>O céu é igual para todos; o seu mapa não. Numa consulta junto a astrologia e o tarot para olhar para a sua vida em particular.</p>
    <div class="botoes"><a class="btn" href="/mapa-astral">✨ O meu Mapa Astral</a><a class="btn ouro" href="loja.html#cat-consultas">🔮 Marcar uma consulta</a></div>
  </section>'''
FAQ_A = [("O que é a astrologia?", "É a leitura simbólica das posições do Sol, da Lua e dos planetas: em que signo estão e que aspetos fazem entre si. A astrologia de signo olha para o céu de todos; a do mapa astral olha para o céu do minuto em que nasceu."),
         ("O que é a astrologia de hoje?", "É o céu deste momento: o signo de cada planeta, a fase e o signo da Lua, e os planetas retrógrados. Nesta página está sempre o céu atual, calculado, e o Horóscopo do Dia lê-o para cada signo."),
         ("Qual é a diferença entre signo e mapa astral?", "O signo é a posição do Sol quando nasceu. O mapa astral junta todos os planetas, a Lua, o Ascendente e as casas, e por isso precisa da data, da hora e do local de nascimento."),
         ("As datas e posições são calculadas?", "Sim. Todas as posições vêm do Swiss Ephemeris, o mesmo cálculo usado pelos astrónomos, no zodíaco tropical, e renovam-se sozinhas todos os meses.")]
JS_A = '''<script src="ceu-dados.js"></script>
<script src="lua-dados.js"></script>
<script>
/* 02/11/2026: o céu de AGORA — signo de cada planeta pelo estado inicial + ingressos (ceu-dados.js) e a Lua (lua-dados.js),
   os dois renovados todos os meses pelo site-ceu-rolante.sh */
(function () {
  const G = window.GT, C = window.CEU, L = window.LUA, $ = (i) => document.getElementById(i);
  const P = [["sol", "☉ Sol"], ["mercurio", "☿ Mercúrio"], ["venus", "♀ Vénus"], ["marte", "♂ Marte"], ["jupiter", "♃ Júpiter"],
             ["saturno", "♄ Saturno"], ["urano", "♅ Úrano"], ["neptuno", "♆ Neptuno"], ["plutao", "♇ Plutão"]];
  const FASE = ["Lua Nova", "Quarto Crescente", "Lua Cheia", "Quarto Minguante"];
  function desenha() {
    const agora = Date.now(), nomes = G.nomes(), est = {};
    for (const [p] of P) est[p] = Object.assign({}, C.estado_inicio[p]);
    for (const x of C.ingressos) if (x.t <= agora) est[x.p] = { s: x.s, r: x.r };
    for (const x of C.estacoes) if (x.t <= agora) est[x.p].r = x.tipo === "R";
    const pa = G.partes(agora);
    $("ag-quando").textContent = pa.d + " de " + G.MESES[pa.m - 1] + ", " + G.hora(agora);
    let h = P.map(([p, n]) => `<div><b>${n}</b><span>${G.GLIFOS[est[p].s]} ${nomes[est[p].s]}${est[p].r ? " ℞" : ""}</span></div>`).join("");
    let sl = null; for (const x of L.ingressos) if (x.t <= agora) sl = x.s;
    if (sl !== null) h = `<div><b>☽ Lua</b><span>${G.GLIFOS[sl]} ${nomes[sl]}</span></div>` + h;
    $("ag").innerHTML = h;
    const prox = L.fases.find((x) => x.t > agora);
    $("ag-lua").textContent = prox ? `Próxima fase: ${FASE[prox.f]} a ${G.data(prox.t)}, às ${G.hora(prox.t)}, em ${nomes[prox.s]}.` : "";
  }
  G.ligarFuso(desenha); desenha(); setInterval(desenha, 60000);
})();
</script>'''
pagina("astrologia", "Astrologia: o céu de hoje, os signos e o mapa · Mestre Alberto",
       "Astrologia no Genial Tarot: o céu de agora, calculado, os 12 signos, o mapa astral, o horóscopo do dia e da semana e os ciclos do ano.",
       "A Astrologia no Genial Tarot — Mestre Alberto", "Astrologia", corpo, FAQ_A, JS_A)

# ───────────── /lua-azul ─────────────
corpo = HEROI("🌕 Lua Azul ✦ calculada", 'A <span class="az">Lua Azul</span>',
              "O que é uma Lua Azul, porque é rara e quando é a próxima, calculada para Portugal e para o Brasil.") + '''
  <section class="cartao">
    <h2>A próxima Lua Azul</h2>
    <p class="grande" id="la-prox"></p>
    <p class="fonte" id="la-falta" style="font-size:1rem"></p>
    <p class="fonte" id="la-saz" style="font-size:1rem"></p>
  </section>
  <section class="cartao texto">
    <h2>O que é uma Lua Azul?</h2>
    <p style="font-family:var(--serifa);font-size:1.15rem;color:var(--lavanda);max-width:46rem;margin:0 auto .8rem">Não é azul. «Lua Azul» é o nome que se dá a uma Lua Cheia «a mais». Há duas formas de a contar, e as duas são usadas:</p>
    <ul style="font-family:var(--serifa);font-size:1.15rem;color:var(--lavanda);max-width:46rem;margin:0 auto .8rem">
      <li><b>Lua Azul mensal:</b> a segunda Lua Cheia no mesmo mês do calendário. Como depende do relógio, pode acontecer em Portugal e não no Brasil, ou ao contrário.</li>
      <li><b>Lua Azul sazonal:</b> a terceira de quatro Luas Cheias numa estação do ano (de equinócio a solstício). É a definição mais antiga, dos almanaques agrícolas.</li>
    </ul>
    <p style="font-family:var(--serifa);font-size:1.15rem;color:var(--lavanda);max-width:46rem;margin:0 auto .8rem">O ciclo da Lua dura cerca de 29,5 dias, um pouco menos do que a maior parte dos meses. Por isso, de dois em dois ou de três em três anos, sobra uma Lua Cheia. Na astrologia, uma Lua Cheia extra é lida como uma segunda oportunidade para terminar, libertar e agradecer o que ficou por fechar.</p>
  </section>
  <section class="cartao">
    <h2>As próximas Luas Azuis</h2>
    <table class="tabela"><thead><tr><th>Data</th><th>Tipo</th></tr></thead><tbody id="la-lista"></tbody></table>
    <p class="fonte">Calculado com o Swiss Ephemeris. Horas no fuso escolhido em cima. Veja também o <a href="/lua">Calendário Lunar</a> e a <a href="/astrologia">Astrologia de hoje</a>.</p>
  </section>'''
FAQ_L = [("A Lua Azul é mesmo azul?", "Não. O nome vem de uma expressão antiga para algo raro. A Lua só parece azulada em casos excecionais, por fumo ou cinzas na atmosfera, e isso nada tem a ver com a Lua Azul do calendário."),
         ("Quando é a próxima Lua Azul?", "Está no topo desta página, calculada a partir de hoje para Portugal e para o Brasil. A página atualiza-se sozinha: quando uma passa, mostra a seguinte."),
         ("De quanto em quanto tempo há Lua Azul?", "Em média a cada dois ou três anos, em cada uma das definições. Por isso se diz «uma vez na vida de uma Lua Azul» para algo raro."),
         ("O que significa a Lua Azul na astrologia?", "Como todas as Luas Cheias, é um momento de culminar e de libertar. Sendo uma Lua Cheia extra, lê-se como uma segunda oportunidade para fechar o que ficou pendente.")]
JS_L = '''<script src="lua-azul-dados.js"></script>
<script>
/* 02/11/2026: a próxima Lua Azul a partir de hoje (lua-azul-dados.js, lua-azul-gerar.py, renovado todos os meses) */
(function () {
  const G = window.GT, A = window.LUA_AZUL, $ = (i) => document.getElementById(i);
  function desenha() {
    const agora = Date.now(), f = G.tz === "Europe/Lisbon" ? "pt" : "br";
    const quando = (t) => { const p = G.partes(t); return `${G.SEMANA[p.dw]}, ${p.d} de ${G.MESES[p.m - 1]} de ${p.a}, às ${G.hora(t)}`; };
    const m = A.mensal[f].filter((t) => t > agora), s = A.sazonal.filter((t) => t > agora);
    const prox = [...m.map((t) => [t, "mensal"]), ...s.map((t) => [t, "sazonal"])].sort((a, b) => a[0] - b[0]);
    if (!prox.length) { $("la-prox").textContent = "—"; return; }
    const [t0, tipo] = prox[0];
    $("la-prox").textContent = quando(t0);
    const dias = Math.ceil((t0 - agora) / 864e5);
    $("la-falta").textContent = `Lua Azul ${tipo} · faltam ${dias} dias` + (tipo === "mensal" ? ` (contada no fuso de ${f === "pt" ? "Portugal" : "Brasil"})` : "");
    const ms = m[0];
    $("la-saz").textContent = tipo === "sazonal" && ms ? `A próxima Lua Azul mensal: ${quando(ms)}.` : (s[0] ? `A próxima Lua Azul sazonal: ${quando(s[0])}.` : "");
    $("la-lista").innerHTML = prox.slice(0, 8).map(([t, k]) => `<tr><td>${quando(t)}</td><td>${k === "mensal" ? "2.ª Lua Cheia do mês" : "3.ª de 4 na estação"}</td></tr>`).join("");
  }
  G.ligarFuso(desenha); desenha();
})();
</script>'''
pagina("lua-azul", "Lua Azul: o que é e quando é a próxima · Mestre Alberto",
       "Lua Azul: o que é, porque é rara e quando é a próxima, calculada para Portugal e para o Brasil. A segunda Lua Cheia do mês e a sazonal, explicadas.",
       "A Lua Azul — Mestre Alberto", "Lua Azul", corpo, FAQ_L, JS_L)
