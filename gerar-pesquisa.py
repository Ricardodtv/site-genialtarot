#!/usr/bin/env python3
"""Gera o pesquisa-indice.json — o índice da pesquisa do site (16/11/2026, pedido dele: «colocar uma pesquisa na página
principal para poder rapidamente encontrar conteúdo: coloco uma palavra e mostras tudo o que está relacionado»).
Entram as MESMAS páginas do sitemap.xml (o gerar-sitemap.py já tira as noindex, o pagamento, a app, os painéis, a conta,
o consultório, o pix e o email), menos a página principal. Por página: endereço limpo, título (sem «· Mestre Alberto»,
«| Genial Tarot»…), descrição, categoria (pelo caminho), um pouco do H1/H2 para enriquecer e o peso (ligações que recebe).
Quem o usa: pesquisa.js (a caixa da página principal e a página /pesquisa). Carrega-se só quando a pessoa foca a caixa.
Corre sozinho no pre-commit, logo a seguir ao gerar-sitemap.py (sempre que o commit leva .html)."""
import os, re, html, json
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"
LIMITE_KB = 400          # alvo: o ficheiro sem compressão abaixo disto; se passar, encurta-se o texto extra
FORA = {"/", "/pesquisa"}

# A ordem desta lista é a ordem dos grupos nos resultados. (categoria, padrão do caminho sem a barra inicial)
CATS = [
    ("Signos", r"^(signo/|signos-|signos$|datas-dos-signos|ascendente|decanatos-|elemento-|[a-z]+-no-tarot$|adivinha-signo|trio-astral)"),
    ("Horóscopo", r"^(horoscopo|anual$|fimdesemana$|amor-do-dia$|aniversarios$|o-meu-dia$|melhores-signos|cor-do-ano|numerologia)"),
    ("Compatibilidade", r"^(compatibilidade|signos-que-combinam|mapa-do-casal|mapa-amor)"),
    ("Tarot e Cartas", r"^(arcano|carta-(?!do-anjo)|cartas-|tiragem-|tarot|combinacoes-de-tarot|cartomancia|leitura-de-cartas|curso-de-tarot|escolha-um-monte|consulta|tarologo|oraculo-cores|livro$|arvore$)"),
    ("Anjos", r"^(anjo|os-72-anjos|carta-do-anjo|dia-do-anjo)"),
    ("Salmos", r"^salmos"),
    ("Rezas e Orações", r"^(reza|rezas|oracao|responso|talhar|benzimentos|glossario-benzeduras|desbloqueios|nossa-senhora|santa-|santo-|sao-|santos-populares|rituais|amuletos)"),
    ("Sonhos", r"^(sonho|sonhos$)"),
    ("Astrologia", r"^(astrolog|aprender-astrologia|mapa-astral|revolucao-solar|lua|planeta-|venus-|marte-|jupiter-|saturno-|urano-|neptuno-|plutao-|nodos-|casa-|transitos|retrogrados|mercurio-|eclipses|efemerides|famosos-ceu|ceu-de-hoje|alinhamento|astrocartografia|stellium|quiron|guia-sistema-solar|fase-lua|calendarios|signos-2026)"),
    ("Notícias do Céu", r"^noticias"),
    ("Lendas e Histórias", r"^(lenda|conto|fabula|parabola|historia)"),
    ("Esoterismo", r"^(quiromancia|linha|montes-da-mao|tipos-de-mao|como-ler-a-mao|como-usar-o-pendulo|pendulo|consulta-de-pendulo|limpar-o-pendulo|mostradores|tipos-de-pendulo|radiestesia|esoterismo|espiritualidade|tacas-tibetanas|hipnose|medos-e-receios|aconselhamento|sexta-feira-13)"),
]
OUTRAS = "Outras páginas"
NOMES = [c for c, _ in CATS] + [OUTRAS]

def categoria(c):
    p = c.lstrip("/")
    if p.startswith("consulta-de-pendulo"): return "Esoterismo"
    for nome, rx in CATS:
        if re.search(rx, p): return nome
    return OUTRAS

def limpa(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

def titulo(s):
    m = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    t = limpa(m.group(1)) if m else ""
    return re.sub(r"\s*[|·—–-]\s*(Mestre Alberto|Genial Tarot)(\s*[|·—–-]\s*(Mestre Alberto|Genial Tarot))?\s*$", "", t).strip()

def meta(s, nome):
    m = re.search(r'<meta[^>]+name=["\']%s["\'][^>]*>' % nome, s, re.I)
    if not m: return ""
    c = re.search(r'content=["\']([^"\']*)["\']', m.group(0))
    return limpa(c.group(1)) if c else ""

def titulos_dentro(s, t):
    """H1 e H2 da página que não repetem o título (para enriquecer a pesquisa)."""
    s = re.sub(r"<(script|style|template)\b.*?</\1>", " ", s, flags=re.S | re.I)
    vistos, out = {t.lower()}, []
    for h in re.findall(r"<h[12]\b[^>]*>(.*?)</h[12]>", s, re.S | re.I):
        h = limpa(h)
        if h and h.lower() not in vistos and len(h) < 120:
            vistos.add(h.lower()); out.append(h)
    return " · ".join(out)

paginas = []
for loc in re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml", encoding="utf-8").read()):
    c = html.unescape(loc)[len(SITE):] or "/"
    if c in FORA: continue
    f = c[1:] + ".html"
    if not os.path.exists(f): continue
    s = open(f, encoding="utf-8", errors="ignore").read()
    t = titulo(s)
    if not t: continue
    paginas.append([c, t, meta(s, "description"), NOMES.index(categoria(c)), titulos_dentro(s, t)])

# Os subtítulos que se repetem em muitas páginas («Perguntas frequentes», «Veja também», «Outros temas»…) não dizem nada
# sobre a página: só fariam aparecer meio site numa pesquisa. Ficam os que existem em poucas páginas.
from collections import Counter
_conta = Counter(h for p in paginas for h in set(p[4].split(" · ")) if h)
for p in paginas:
    p[4] = " · ".join(h for h in p[4].split(" · ") if h and _conta[h] <= 6)

# Peso de cada página = quantas páginas do site lhe apontam (escala log2, de 0 a 8). As páginas-mãe (/signo/touro,
# /os-72-anjos, /rezas-e-oracoes, /salmos) sobem acima das fichas soltas quando o resto empata.
import glob, math
_urls = {p[0] for p in paginas}
_entram = Counter()
for _f in glob.glob("*.html") + glob.glob("*/*.html"):
    _s = open(_f, encoding="utf-8", errors="ignore").read(); _de = "/" + _f[:-5]
    for _h in set(re.findall(r'href="(?:https://genialtarot\.com)?(/[^"#?]*)', _s)):
        _h = _h[:-5] if _h.endswith(".html") else _h
        if _h != _de and _h in _urls: _entram[_h] += 1
for p in paginas: p.append(min(8, round(math.log2(1 + _entram[p[0]]))))

def escreve(corte):
    dados = {"v": 1, "cats": NOMES, "p": [[u, t, d[:220], k, x[:corte].rstrip(" ·"), w] for u, t, d, k, x, w in paginas]}
    return json.dumps(dados, ensure_ascii=False, separators=(",", ":"))

corte = 300
txt = escreve(corte)
while len(txt.encode()) > LIMITE_KB * 1024 and corte > 0:
    corte -= 50; txt = escreve(corte)
antigo = open("pesquisa-indice.json", encoding="utf-8").read() if os.path.exists("pesquisa-indice.json") else ""
if txt + "\n" != antigo: open("pesquisa-indice.json", "w", encoding="utf-8").write(txt + "\n")
por_cat = {}
for p in paginas: por_cat[NOMES[p[3]]] = por_cat.get(NOMES[p[3]], 0) + 1
print("pesquisa-indice.json: %d páginas, %.0f KB (texto extra até %d letras)" % (len(paginas), len(txt.encode()) / 1024, corte))
print("  " + ", ".join("%s %d" % (k, por_cat.get(k, 0)) for k in NOMES))
