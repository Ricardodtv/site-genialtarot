#!/usr/bin/env python3
"""Aplica os textos do seo-textos-extra.py (01/11/2026): um bloco «cartão» antes das Perguntas frequentes (ou do rodapé)
em cada página que estava abaixo das 300 palavras. Idempotente (marca <!-- seo-extra -->); o gerar-signos.py chama-o no
fim, para as páginas refeitas não perderem o texto."""
import os, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))
MARCA = "<!-- seo-extra -->"
d = {}
exec(open("seo-textos-extra.py", encoding="utf-8").read(), d)
feitas = 0
for slug, (titulo, pars) in d["EXTRA"].items():
    f = slug + ".html"
    if not os.path.exists(f): print("⚠️ não existe:", f); continue
    s = open(f, encoding="utf-8").read()
    if MARCA in s: continue
    bloco = (f'{MARCA}\n<section class="faq-genial" style="max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);'
             f'border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6"><h2 style="margin-top:0">{html.escape(titulo)}</h2>'
             + "".join(f'<p style="margin:0 0 .8rem">{html.escape(p)}</p>' for p in pars) + "</section>\n")
    for alvo in ('<section class="faq-genial"', '<section class="cartao texto"><h2>Perguntas frequentes', "<footer", "</body>"):
        i = s.find(alvo) if alvo != "</body>" else s.rfind(alvo)
        if i >= 0: break
    if i < 0: print("⚠️ sem sítio:", f); continue
    s = s[:i] + bloco + s[i:]
    open(f, "w", encoding="utf-8").write(s); feitas += 1
print(f"seo-extra: {feitas} páginas com texto novo")
