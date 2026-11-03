#!/usr/bin/env python3
"""O destaque do site principal dentro de TODAS as páginas (03/11/2026, pedido dele: «todas as páginas devem ter um destaque
dentro delas para o site principal; as páginas devem ser cativantes e bonitas, que as pessoas se sintam atraídas»).

Um cartão com a foto do Mestre Alberto, uma frase, quatro portas (Tarot Grátis, Horóscopo de Hoje, os 12 Signos, Sonhos)
e dois botões (página inicial e marcar consulta), posto antes do rodapé de cada página. Idempotente: tira o bloco antigo
(entre <!-- gt-casa:inicio --> e <!-- gt-casa:fim -->) e põe o atual. Corre no pre-commit (como o imagens-destaque.py),
por isso volta a entrar sozinho quando um gerador reescreve uma página. Imprime as páginas que mudou.
  python3 destaque-casa.py            # todas
  python3 destaque-casa.py --tirar    # tira de todas
"""
import glob, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
FORA = {"index.html", "404.html", "pagar.html", "30-dias.html", "30-dias-autorizacao.html", "privacidade.html", "termos.html",
        "sair.html", "obrigado.html", "mapa-do-site.html"}
FORA_PREFIXO = ("o-teu-ceu", "google", "yandex", "bing", "teste", "rascunho")
INI, FIM = "<!-- gt-casa:inicio -->", "<!-- gt-casa:fim -->"
PORTAS = [("/tarot-gratis", "🃏", "Tarot Grátis", "Tire as suas cartas agora"),
          ("/horoscopo-do-dia", "🔮", "Horóscopo de Hoje", "O seu signo, com o céu real"),
          ("/signos-do-zodiaco", "♈︎", "Os 12 Signos", "Personalidade, amor e datas"),
          ("/sonhos", "🌙", "Sonhos", "O que o seu sonho quer dizer"),
          ("/horoscopo-semanal", "📅", "Horóscopo Semanal", "A semana de cada signo")]
CSS = """<style>
.gt-casa{max-width:900px;margin:2.6rem auto 1.6rem;padding:0 14px;font-family:inherit}
.gt-casa .gc-cx{position:relative;border-radius:22px;padding:1.6rem 1.4rem 1.4rem;overflow:hidden;color:#f7f0fb;text-align:center;
 background:radial-gradient(120% 90% at 50% 0%,rgba(242,201,107,.20),transparent 60%),linear-gradient(160deg,#2a1245 0%,#1a0b30 55%,#120722 100%);
 border:1px solid rgba(242,201,107,.45);box-shadow:0 18px 50px rgba(0,0,0,.35),inset 0 0 40px rgba(242,201,107,.06)}
.gt-casa .gc-cx::before{content:"";position:absolute;inset:-40%;background:conic-gradient(from 0deg,transparent 0 70%,rgba(242,201,107,.16) 80%,transparent 90%);animation:gc-gira 14s linear infinite;pointer-events:none}
@keyframes gc-gira{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.gt-casa .gc-cx::before{animation:none}}
.gt-casa .gc-in{position:relative}
.gt-casa .gc-foto{width:92px;height:92px;border-radius:50%;object-fit:cover;border:3px solid #f2c96b;box-shadow:0 0 0 6px rgba(242,201,107,.15),0 8px 24px rgba(0,0,0,.4);display:block;margin:0 auto .7rem}
.gt-casa .gc-sel{font-size:.78rem;letter-spacing:.28em;text-transform:uppercase;color:#f2c96b;opacity:.9}
.gt-casa .gc-tit{font-family:Cinzel,Georgia,"Times New Roman",serif;font-size:clamp(1.25rem,3.6vw,1.75rem);margin:.35rem 0 .45rem;color:#ffe2a0;line-height:1.25}
.gt-casa .gc-txt{margin:0 auto 1.1rem;max-width:560px;color:#e7dcf3;line-height:1.55;font-size:1rem}
.gt-casa .gc-portas{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:0 0 1.1rem}
.gt-casa .gc-portas a{display:flex;flex-direction:column;align-items:center;gap:2px;padding:.8rem .6rem;border-radius:14px;text-decoration:none;color:#f7f0fb;
 background:rgba(255,255,255,.06);border:1px solid rgba(242,201,107,.22);transition:transform .2s,background .2s,border-color .2s}
.gt-casa .gc-portas a:hover,.gt-casa .gc-portas a:focus-visible{transform:translateY(-3px);background:rgba(242,201,107,.13);border-color:#f2c96b}
.gt-casa .gc-portas i{font-style:normal;font-size:1.6rem;line-height:1.2}
.gt-casa .gc-portas b{font-size:.98rem;color:#ffe2a0}
.gt-casa .gc-portas small{font-size:.8rem;color:#bfaed3}
.gt-casa .gc-bot{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.gt-casa .gc-bot a{display:inline-block;padding:.75rem 1.3rem;border-radius:999px;font-weight:700;text-decoration:none;font-size:1rem}
.gt-casa .gc-casa{background:linear-gradient(135deg,#ffe2a0,#f2c96b 55%,#d9a441);color:#2a1245;box-shadow:0 6px 18px rgba(242,201,107,.35)}
.gt-casa .gc-wa{background:rgba(37,211,102,.16);color:#d8ffe6;border:1px solid rgba(37,211,102,.55)}
.gt-casa .gc-bot a:hover{filter:brightness(1.08)}
</style>"""


def bloco(pagina):
    eu = "/" + re.sub(r"\.html$", "", pagina)
    portas = [p for p in PORTAS if p[0] != eu][:4]
    return (f'{INI}\n<aside class="gt-casa" aria-label="Genial Tarot — o site do Mestre Alberto">{CSS}<div class="gc-cx"><div class="gc-in">'
            '<img class="gc-foto" src="/mestre-avatar.jpg" srcset="/mestre-avatar.jpg 1x, /mestre-avatar@2x.jpg 2x" width="92" height="92" '
            'alt="Mestre Alberto, tarólogo e astrólogo do Genial Tarot" loading="lazy" decoding="async">'
            '<div class="gc-sel">✦ Genial Tarot ✦</div>'
            '<p class="gc-tit">Há 18 anos a ler o Tarot e os astros</p>'
            '<p class="gc-txt">Este é o site do Mestre Alberto. Tire as cartas, leia o seu signo e descubra o que o céu diz de si — '
            'e quando precisar de uma resposta só sua, fale com ele numa consulta por videochamada.</p>'
            '<nav class="gc-portas">' + "".join(f'<a href="{u}"><i aria-hidden="true">{ic}</i><b>{t}</b><small>{d}</small></a>' for u, ic, t, d in portas) + '</nav>'
            '<div class="gc-bot"><a class="gc-casa" href="/">✨ Ir para a página inicial</a>'
            '<a class="gc-wa" href="https://wa.me/351914920427" rel="noopener">💬 Marcar consulta</a></div>'
            f'</div></div></aside>\n{FIM}\n')


def main():
    tirar = "--tirar" in sys.argv
    for f in sorted(glob.glob("*.html") + glob.glob("signo/*.html") + glob.glob("sonho/*.html")):
        nome = os.path.basename(f)
        if f.startswith((".git", "node_modules")) or nome in FORA or nome.startswith(FORA_PREFIXO): continue
        h = open(f, encoding="utf-8").read()
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', h, re.I) or "<body" not in h: continue
        novo = re.sub(re.escape(INI) + r".*?" + re.escape(FIM) + r"\n?", "", h, flags=re.S)
        if not tirar:
            i = novo.rfind("<footer")
            if i < 0: i = novo.rfind("</body>")
            if i < 0: continue
            novo = novo[:i] + bloco(f) + novo[i:]
        if novo != h:
            open(f, "w", encoding="utf-8").write(novo); print(f)


if __name__ == "__main__":
    main()
