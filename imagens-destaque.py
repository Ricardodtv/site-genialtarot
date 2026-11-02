#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Imagens de destaque das páginas (02/11/2026, pedido dele: imagens geradas por ele, com nomes e títulos otimizados para
o Google Imagens). Para cada página da lista IMAGENS:
  · põe a imagem logo a seguir ao bloco de topo (<section class="heroi"> ou <section class="hero">), entre as marcas
    <!-- img-destaque:inicio --> e <!-- img-destaque:fim --> (correr outra vez ATUALIZA, não duplica);
  · a imagem de partilha (og:image, Facebook/WhatsApp) passa a ser a da página, em JPG 1200×630, com og:image:alt;
  · um JSON-LD ImageObject (nome, legenda, autor, crédito) para o Google.
Corre no pre-commit (.git/hooks/pre-commit): se um gerador reescrever a página, a imagem volta a entrar no commit seguinte.

Imagem nova: o original (PNG/JPG do gerador) em ~/site-genialtarot-dados/imagens-originais/<CÓDIGO>.png e uma linha em
IMAGENS. `python3 imagens-destaque.py --converter` faz o <nome>.webp (1200 px) e o <nome>-og.jpg (1200×630).
    python3 ~/site-genialtarot/imagens-destaque.py              → aplica nas páginas (diz quais mudou)
    python3 ~/site-genialtarot/imagens-destaque.py --converter  → (re)faz os ficheiros de imagem a partir dos originais
"""
import json, os, re, sys, html
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
ORIG = "/home/ricardo/site-genialtarot-dados/imagens-originais"
SITE = "https://genialtarot.com"

# código, página, nome do ficheiro (o que o Google lê), texto alternativo, legenda
IMAGENS = [
    ("A01", "consulta-de-tarot-online", "consulta-de-tarot-online",
     "Consulta de tarot online: mãos do tarólogo a virar as cartas numa mesa de veludo azul, com velas e uma videochamada ao lado",
     "Consulta de tarot online com o Mestre Alberto: as cartas são lançadas ao vivo e a leitura faz-se por videochamada, chamada ou mensagem."),
    ("A02", "tarot-gratis", "tarot-gratis-online",
     "Tarot grátis online: três cartas de tarot sobre veludo azul, a do meio a brilhar com luz dourada",
     "Tarot grátis online: pense na sua pergunta e tire três cartas do baralho do Mestre Alberto."),
    ("A03", "horoscopo-semanal", "horoscopo-semanal-signos",
     "Horóscopo semanal dos signos: roda do zodíaco dourada com os 12 signos, astrolábio e agenda aberta sob um céu estrelado",
     "O horóscopo semanal dos 12 signos, de segunda a domingo, a partir do céu real da semana."),
    ("A04", "horoscopo-do-dia", "horoscopo-do-dia",
     "Horóscopo do dia: nascer do sol sobre o mar com a Lua no céu e as constelações do zodíaco desenhadas em dourado",
     "O horóscopo do dia dos 12 signos, com a Lua e os aspetos dos planetas de hoje."),
    ("A05", "astrologia", "astrologia-ceu-de-hoje",
     "Astrologia e o céu de hoje: astrólogo a observar a Via Láctea e os planetas alinhados, com um mapa astral e um astrolábio na mesa",
     "Astrologia: o céu de agora, calculado, e tudo para ler os signos e o seu mapa astral."),
    ("A06", "tiragem-sim-ou-nao", "tarot-sim-ou-nao",
     "Tarot sim ou não: mão a escolher entre duas cartas de tarot, uma iluminada e outra na sombra, sobre veludo azul",
     "Tarot sim ou não: uma carta para uma pergunta direta, e como ler a resposta."),
    ("A07", "tarot-do-amor", "tarot-do-amor",
     "Tarot do amor: mãos de um casal entrelaçadas sobre uma tiragem de tarot com pétalas de rosa vermelha e velas cor-de-rosa",
     "Tarot do amor: o que as cartas dizem sobre a sua relação e o seu coração."),
    ("A08", "signos-que-combinam", "signos-que-combinam",
     "Signos que combinam: casal abraçado a olhar o céu estrelado, com duas constelações a brilhar por cima",
     "Signos que combinam: o par ideal de cada signo e os que se desafiam, pela regra dos elementos."),
]

FIG = ('<!-- img-destaque:inicio -->\n<figure class="img-destaque" style="max-width:72rem;margin:0 auto 2rem;padding:0 1rem;position:relative;z-index:1">'
       '<img src="/{nome}.webp" alt="{alt}" title="{alt}" width="1200" height="800" fetchpriority="high" decoding="async" '
       'style="display:block;width:100%;height:auto;border-radius:1.2rem;border:1px solid rgba(212,175,55,.35);box-shadow:0 18px 50px #0008">'
       '<figcaption style="text-align:center;font-size:.85rem;color:#c9c2e0;margin-top:.6rem">{leg}</figcaption></figure>\n<!-- img-destaque:fim -->\n')


def converter():
    from PIL import Image
    for cod, _, nome, _, _ in IMAGENS:
        src = next((f"{ORIG}/{cod}.{e}" for e in ("png", "jpg", "jpeg", "webp") if os.path.exists(f"{ORIG}/{cod}.{e}")), None)
        if not src: print(cod, "sem original"); continue
        im = Image.open(src).convert("RGB")
        w = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        if w.height != 800:   # 3:2 certinho
            t = (w.height - 800) // 2; w = w.crop((0, max(0, t), 1200, max(0, t) + 800))
        w.save(f"{nome}.webp", "WEBP", quality=82, method=6)
        h = round(1200 * 630 / 1200); og = w.crop((0, (800 - 630) // 2, 1200, (800 - 630) // 2 + 630))
        og.save(f"{nome}-og.jpg", "JPEG", quality=84, optimize=True, progressive=True)
        print(cod, nome, os.path.getsize(f"{nome}.webp") // 1024, "KB webp,", os.path.getsize(f"{nome}-og.jpg") // 1024, "KB og")


def aplicar():
    mudadas = []
    for cod, pag, nome, alt, leg in IMAGENS:
        f = f"{pag}.html"
        if not (os.path.exists(f) and os.path.exists(f"{nome}.webp")): continue
        h0 = h = open(f, encoding="utf-8").read()
        fig = FIG.format(nome=nome, alt=html.escape(alt), leg=html.escape(leg))
        h = re.sub(r"<!-- img-destaque:inicio -->.*?<!-- img-destaque:fim -->\n", "", h, flags=re.S)   # tira exactamente o que pôs
        m = re.search(r'<section class="hero[i]?"[^>]*>', h)
        if not m: print("⚠️", f, "sem bloco de topo"); continue
        fim = h.index("</section>", m.end()) + len("</section>")
        if h[fim:fim + 1] == "\n": fim += 1
        h = h[:fim] + fig + h[fim:]
        og = f"{SITE}/{nome}-og.jpg"
        h = re.sub(r'(<meta property="og:image" content=")[^"]*', r"\g<1>" + og, h, count=1)
        h = re.sub(r'(<meta property="og:image:width" content=")[^"]*', r"\g<1>1200", h, count=1)
        h = re.sub(r'(<meta property="og:image:height" content=")[^"]*', r"\g<1>630", h, count=1)
        h = re.sub(r'\n?<meta property="og:image:alt"[^>]*>', "", h)
        h = h.replace(f'<meta property="og:image" content="{og}" />', f'<meta property="og:image" content="{og}" />\n<meta property="og:image:alt" content="{html.escape(alt)}" />', 1)
        ld = {"@context": "https://schema.org", "@type": "ImageObject", "contentUrl": f"{SITE}/{nome}.webp", "url": f"{SITE}/{nome}.webp",
              "name": alt.split(":")[0], "caption": leg, "description": alt, "width": 1200, "height": 800,
              "creator": {"@type": "Organization", "name": "Genial Tarot"}, "copyrightHolder": {"@type": "Organization", "name": "Genial Tarot"},
              "creditText": "Genial Tarot · Mestre Alberto", "copyrightNotice": "© Genial Tarot", "representativeOfPage": True}
        h = re.sub(r'<script type="application/ld\+json" data-img-destaque>.*?</script>\n?', "", h, flags=re.S)
        h = h.replace("</head>", f'<script type="application/ld+json" data-img-destaque>{json.dumps(ld, ensure_ascii=False)}</script>\n</head>', 1)
        if h != h0:
            open(f, "w", encoding="utf-8").write(h); mudadas.append(f)
    for f in mudadas: print(f)


if __name__ == "__main__":
    if "--converter" in sys.argv: converter()
    else: aplicar()
