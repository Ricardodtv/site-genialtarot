#!/usr/bin/env python3
"""Gera o sitemap.xml do genialtarot.com (31/10/2026, pedido dele: o robots.txt anunciava um sitemap que não existia — 404).
Entra toda a página .html (raiz, sonho/ e signo/ — o signo/ faltava até 01/11) que NÃO tenha <meta name="robots" content="noindex">, menos as da lista FORA.
Endereços sem «.html» (o Cloudflare manda o .html para lá com 307). lastmod = a data do último commit do ficheiro.
Corre sozinho no pre-commit (.git/hooks/pre-commit, ligado por ele a 31/10 com ~/ligar-sitemap-auto.sh) sempre que o commit leva .html."""
import glob, os, re, subprocess, html
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"
FORA = {"pagar.html", "o-teu-ceu.html", "30-dias.html", "30-dias-autorizacao.html"}   # pagamento e a app: não são para pesquisa
import datetime
PREPARADOS = set(subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True).stdout.split())
def data(f):
    if f in PREPARADOS: return datetime.date.today().isoformat()   # vai entrar neste commit
    d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip()
    return d or None
urls = []
for f in sorted(glob.glob("*.html") + glob.glob("sonho/*.html") + glob.glob("signo/*.html") + glob.glob("noticias/*.html")):
    if f in FORA: continue
    s = open(f, encoding="utf-8", errors="ignore").read()
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s, re.I): continue
    caminho = "/" if f == "index.html" else "/" + f[:-5]
    prio = "1.0" if f == "index.html" else "0.8" if ("/" not in f or f.startswith("signo/")) and not f.startswith("arcano-") else "0.6"
    urls.append((caminho, data(f), prio))
linhas = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for c, d, p in urls:
    linhas.append("  <url><loc>%s</loc>%s<priority>%s</priority></url>" % (html.escape(SITE + c), "<lastmod>%s</lastmod>" % d if d else "", p))
linhas.append("</urlset>")
novo = "\n".join(linhas) + "\n"
antigo = open("sitemap.xml").read() if os.path.exists("sitemap.xml") else ""
if novo != antigo: open("sitemap.xml", "w").write(novo)
print("sitemap.xml:", len(urls), "páginas")

# 02/11/2026 (SEO de imagens, pedido dele): sitemap-imagens.xml — para cada página, as imagens que contam (o baralho do
# Mestre, as ilustrações dos signos, os sonhos, o baralho cigano, as imagens próprias das páginas); fora os ícones,
# a foto repetida do Mestre e as imagens sem texto alternativo (decorativas). O robots.txt anuncia-o.
IMG_OK = re.compile(r"^/?(cartas/|cartas-ciganas/|signos/signo-|sonho/img/|[a-z0-9-]+\.(webp|jpg|png)$)")
IMG_FORA = re.compile(r"mestre-(avatar|diario|r\d+)|favicon|icone|logo|og-image")
linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
n_img = 0
for c, d, p in urls:
    f = "index.html" if c == "/" else c[1:] + ".html"
    s = open(f, encoding="utf-8", errors="ignore").read()
    vistas = []
    for tag in re.findall(r"<img\b[^>]*>", s):
        src = re.search(r'src=["\']([^"\'$]+)["\']', tag); alt = re.search(r'alt=["\']([^"\']*)["\']', tag)
        if not src or not alt or not alt.group(1).strip(): continue
        u = src.group(1).split("?")[0]
        if u.startswith("http"):
            if not u.startswith(SITE): continue
            u = u[len(SITE):]
        if not IMG_OK.search(u) or IMG_FORA.search(u): continue
        u = "/" + u.lstrip("/")
        if u not in vistas and os.path.exists(u[1:]): vistas.append(u)
    if vistas:
        linhas.append(f"  <url><loc>{SITE}{c}</loc>" + "".join(f"<image:image><image:loc>{SITE}{html.escape(u)}</image:loc></image:image>" for u in vistas[:1000]) + "</url>")
        n_img += len(vistas)
linhas.append("</urlset>")
novo = "\n".join(linhas) + "\n"
antigo = open("sitemap-imagens.xml").read() if os.path.exists("sitemap-imagens.xml") else ""
if novo != antigo: open("sitemap-imagens.xml", "w").write(novo)
print("sitemap-imagens.xml:", n_img, "imagens em", sum(1 for l in linhas if l.startswith("  <url>")), "páginas")
