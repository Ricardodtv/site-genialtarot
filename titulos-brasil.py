#!/usr/bin/env python3
"""Nomes do Brasil nos títulos (07/11/2026, pedido dele): Caranguejo (Câncer), Balança (Libra), Vénus (Vênus)...
Idempotente. Só muda o <title> e o og:title quando cabem em 65 caracteres, encurtando o fim do título se for preciso.
Chamado no fim do gerar-signos.py, que reescreve os títulos."""
import glob, html, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PAR = [("Carneiro", "Áries"), ("Gémeos", "Gêmeos"), ("Caranguejo", "Câncer"), ("Balança", "Libra"), ("Vénus", "Vênus"), ("Neptuno", "Netuno")]
CURTOS = [(": compatibilidade no amor e na amizade", ": compatibilidade no amor"), (": a carta O ", ": "), (": a carta A ", ": "), (" e o seu significado", ""),
          (": como ama, o que a atrai e como seduz", ": como ama e seduz"), (": o que deseja e como age", "")]
FORA = {"index.html", "404.html"}
def novo(t):
    r = t
    for a, b in PAR:
        if a in r and b not in r: r = r.replace(a, f"{a} ({b})", 1)
    if r == t: return t
    for a, b in CURTOS:
        if len(r) <= 65: break
        r = r.replace(a, b)
    return r if len(r) <= 65 else t
n = 0
for f in glob.glob("*.html") + glob.glob("signo/*.html"):
    if f in FORA: continue
    s = open(f, encoding="utf-8", errors="ignore").read()
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if not m: continue
    t = html.unescape(m.group(1)).strip(); r = novo(t)
    if r == t: continue
    e = html.escape(r, quote=True)
    s2 = s.replace(m.group(0), f"<title>{e}</title>", 1)
    s2 = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda k: k.group(1) + e + k.group(2), s2, count=1)
    open(f, "w", encoding="utf-8").write(s2); n += 1
print("títulos:", n)
