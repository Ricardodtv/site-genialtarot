#!/usr/bin/env python3
"""Gera o sitemap.xml do genialtarot.com (31/10/2026, pedido dele: o robots.txt anunciava um sitemap que não existia — 404).
Entra toda a página .html (raiz e sonho/) que NÃO tenha <meta name="robots" content="noindex">, menos as da lista FORA.
Endereços sem «.html» (o Cloudflare manda o .html para lá com 307). lastmod = a data do último commit do ficheiro.
Correr à mão depois de publicar página nova (ou que deixa de ser noindex): python3 gerar-sitemap.py"""
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
for f in sorted(glob.glob("*.html") + glob.glob("sonho/*.html")):
    if f in FORA: continue
    s = open(f, encoding="utf-8", errors="ignore").read()
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s, re.I): continue
    caminho = "/" if f == "index.html" else "/" + f[:-5]
    prio = "1.0" if f == "index.html" else "0.8" if "/" not in f and not f.startswith("arcano-") else "0.6"
    urls.append((caminho, data(f), prio))
linhas = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for c, d, p in urls:
    linhas.append("  <url><loc>%s</loc>%s<priority>%s</priority></url>" % (html.escape(SITE + c), "<lastmod>%s</lastmod>" % d if d else "", p))
linhas.append("</urlset>")
novo = "\n".join(linhas) + "\n"
antigo = open("sitemap.xml").read() if os.path.exists("sitemap.xml") else ""
if novo != antigo: open("sitemap.xml", "w").write(novo)
print("sitemap.xml:", len(urls), "páginas")
