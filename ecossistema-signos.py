#!/usr/bin/env python3
"""Ecossistema (01/11/2026, pedido dele: «trazer pessoas, ficar com o contacto, vender de forma automática»).
Nas 12 páginas /signo/<nome>, que é onde chegam as ligações dos vídeos do canal:
  • passo 2 — a caixa «A previsão do seu signo no seu email» (lista-signo.js), logo a seguir ao horóscopo de hoje;
  • passo 4 — «Tudo sobre <Signo>»: ligações a todas as páginas desse signo (Google: páginas parecidas ligadas entre si).
Idempotente (marca <!-- ecossistema-signo -->): corre-se outra vez sem duplicar. O gerar-signos.py chama-o no fim,
para que as páginas refeitas não percam as caixas."""
import os, re, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))
MARCA = "<!-- ecossistema-signo -->"
S = [("carneiro", "Carneiro", "Áries"), ("touro", "Touro", ""), ("gemeos", "Gémeos", "Gêmeos"), ("caranguejo", "Caranguejo", "Câncer"),
     ("leao", "Leão", ""), ("virgem", "Virgem", ""), ("balanca", "Balança", "Libra"), ("escorpiao", "Escorpião", ""),
     ("sagitario", "Sagitário", ""), ("capricornio", "Capricórnio", ""), ("aquario", "Aquário", ""), ("peixes", "Peixes", "")]
CSS = """<style>
#lista-signo{border:1.5px solid rgba(255,217,120,.7);background:linear-gradient(135deg,rgba(255,217,120,.12),rgba(160,48,122,.22))}
#lista-signo h2{margin-top:0}#lista-signo .ls-form{display:grid;gap:.6rem;max-width:420px;margin:0 auto}
#lista-signo input{font:inherit;padding:.75rem .9rem;border-radius:12px;border:1px solid rgba(255,255,255,.25);background:rgba(0,0,0,.25);color:inherit}
#lista-signo label{font-size:.85rem;text-align:left;opacity:.85}
#lista-signo button{font:inherit;font-weight:800;padding:.85rem 1rem;border:0;border-radius:999px;background:#ffd978;color:#2a0c3e;cursor:pointer}
#lista-signo .ls-legal{font-size:.78rem;opacity:.75;margin:.3rem 0 0}#lista-signo .ls-erro{display:none;color:#ffb4b4;font-weight:700}
#lista-signo .ls-feito{display:none;text-align:center}
</style>"""
feitos = 0
for slug, pt, br in S:
    f = f"signo/{slug}.html"
    if not os.path.exists(f): continue
    s = open(f, encoding="utf-8").read()
    if MARCA in s: continue
    nome = pt + (f" ({br})" if br else "")
    caixa = f"""{MARCA}{CSS}
  <section class="cartao" id="lista-signo" data-signo="{html.escape(pt)}" style="text-align:center">
    <h2>💌 A previsão de {html.escape(nome)} no seu email</h2>
    <p>Todas as sextas-feiras o Mestre Alberto envia-lhe a previsão do fim de semana para o seu signo, os avisos das noites
    mágicas do céu (Luas Cheias, eclipses e retrógrados) e, no seu aniversário, um presente. É grátis.</p>
    <form class="ls-form" novalidate>
      <input name="nome" autocomplete="given-name" placeholder="O seu nome" aria-label="O seu nome">
      <input name="email" type="email" autocomplete="email" placeholder="O seu email" aria-label="O seu email">
      <label>A sua data de nascimento (para sabermos o seu signo)<input name="nasc" type="date" min="1920-01-01" max="2012-12-31" style="width:100%;box-sizing:border-box;margin-top:.3rem"></label>
      <button type="submit">💌 Quero receber</button>
      <div class="ls-erro" role="alert"></div>
      <p class="ls-legal">Ao carregar em «Quero receber», aceita receber os emails do Mestre Alberto (previsões, novidades e promoções). Pode sair quando quiser, com um clique no fim de cada email. <a href="/privacidade">Privacidade</a></p>
    </form>
    <div class="ls-feito" aria-live="polite"><p style="font-size:2rem;margin:.2rem">💌✨</p><p>Obrigado, <b></b>! A primeira previsão chega na sexta-feira. Se não a vir, espreite a pasta Promoções ou Spam.</p></div>
  </section>"""
    pags = [(f"horoscopo-2027-{slug}", f"Horóscopo 2027 de {pt}"), (f"decanatos-{slug}", f"Os decanatos de {pt}"),
            (f"ascendente-em-{slug}", f"Ascendente em {pt}"), (f"lua-em-{slug}", f"Lua em {pt}"), (f"venus-em-{slug}", f"Vénus em {pt}"),
            (f"marte-em-{slug}", f"Marte em {pt}"), (f"{slug}-no-tarot", f"{pt} no Tarot"), ("compatibilidade-entre-signos", "Compatibilidade"),
            ("tarot-gratis", "Tarot Grátis"), ("carta-de-tarot", "A sua carta de Tarot"), ("mapa-astral", "O seu Mapa Astral")]
    ligas = "".join(f'<a href="/{a}">{html.escape(b)}</a>' for a, b in pags if os.path.exists(a + ".html"))
    hub = f'\n  <section class="cartao" style="text-align:center"><h2>Tudo sobre {html.escape(pt)}</h2><div class="ligas">{ligas}</div></section>\n'
    # a caixa logo depois do «Horóscopo de hoje» (a secção com id="hoje")
    i = s.find('id="hoje"'); j = s.find("</section>", i) if i >= 0 else -1
    if j < 0: print("⚠️ sem secção do horóscopo de hoje:", f); continue
    j += len("</section>")
    s = s[:j] + "\n" + caixa + s[j:]
    s = s.replace("<footer>", hub + "<footer>", 1) if "<footer>" in s else s
    s = s.replace("</body>", '<script src="/lista-signo.js" defer></script>\n</body>', 1)
    open(f, "w", encoding="utf-8").write(s); feitos += 1
print(f"ecossistema: {feitos} páginas de signo actualizadas")
