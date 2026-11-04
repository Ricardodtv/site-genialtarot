#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vídeos do canal nas páginas do site (04/11/2026, pedido dele: «começa pelos vídeos nas páginas» — a ideia n.º 1 da
análise do giatho.com: o canal a puxar pelo site, com o vídeo marcado para o Google).

Para cada página da lista VIDEOS:
  · põe o(s) vídeo(s) logo a seguir ao bloco de topo (e à imagem de destaque, se houver), entre
    <!-- video-pagina:inicio --> e <!-- video-pagina:fim --> (correr outra vez ATUALIZA, não duplica);
  · em /signos-2026, cada signo leva a sua Previsão Anual 2026 dentro do próprio cartão;
  · o vídeo aparece como capa leve (a imagem do YouTube); o leitor do YouTube só carrega quando a pessoa carrega no ▶
    (youtube-nocookie) — a página não fica mais lenta;
  · um JSON-LD VideoObject por vídeo (nome, descrição, capa, data, duração, embedUrl) para o Google.
Os dados dos vídeos (data, duração) vêm de videos-paginas-dados.json — refazer com a chave de leitura do cofre:
    python3 videos-paginas.py --atualizar     → lê o YouTube e grava videos-paginas-dados.json
    python3 videos-paginas.py                 → aplica nas páginas (diz quais mudou); corre no fim do gerar-signos.py
Vídeo novo: uma linha em VIDEOS e --atualizar. Só vídeos PÚBLICOS e incorporáveis (o --atualizar avisa)."""
import html, json, os, re, sys, urllib.request
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
DADOS = "videos-paginas-dados.json"
SITE = "https://genialtarot.com"

# página → [(id do vídeo, título limpo, legenda)] — títulos e legendas escritos aqui (os títulos antigos do canal
# têm listas de palavras soltas); o JSON-LD usa estes.
VIDEOS = {
    "rituais": [
        ("A2Le_BizljE", "Ritual para o Amor e a Prosperidade",
         "O Mestre Alberto explica um ritual para o amor e a prosperidade, passo a passo."),
        ("1l9K8CaahIk", "Rituais de Limpeza",
         "Em um minuto, o Mestre Alberto fala dos rituais de limpeza e de quando fazem sentido."),
    ],
    "amuletos": [
        ("WkcEJfXniZ8", "A Cruz da Boa Energia: sucesso e proteção",
         "O Mestre Alberto apresenta a Cruz da Boa Energia, o amuleto de proteção e sucesso."),
    ],
    "lua": [
        ("ziv87x9KWd4", "A Super Lua Cheia e as suas energias",
         "A Super Lua Cheia e a energia de transformação que traz, em menos de um minuto."),
    ],
    "mapa-astral": [
        ("WS8_kn83tuk", "O Mapa Astral, pelo Mestre Alberto",
         "O que o Mapa Astral mostra: as energias, os movimentos dos planetas e a personalidade."),
    ],
    "parabola-quanto-vale-o-anel": [
        ("oR13zXl63X0", "Parábola: o Menino e o Anel",
         "A parábola do anel contada pelo Mestre Alberto: quanto vale aquilo que somos."),
    ],
}
# /signos-2026: a Previsão Anual 2026 de cada signo, dentro do cartão do signo (playlist «Previsão Anual 2026 Todos os Signos»)
SIGNOS_2026 = {
    "carneiro": "sYvV52nILsg", "touro": "PBDNKmuCGjE", "gemeos": "EdzVicTufXw", "caranguejo": "G_Ox4x7wl_M",
    "leao": "dto1ayURroc", "virgem": "S63ep0UfuI0", "balanca": "_596jwAtBl0", "escorpiao": "vDhtOX8kixs",
    "sagitario": "SPco2eROtps", "capricornio": "hrTjuSE8VmM", "aquario": "iXnf_orBfDs", "peixes": "60VId99VP8Y",
}
NOMES = {"carneiro": "Carneiro", "touro": "Touro", "gemeos": "Gémeos", "caranguejo": "Caranguejo", "leao": "Leão", "virgem": "Virgem",
         "balanca": "Balança", "escorpiao": "Escorpião", "sagitario": "Sagitário", "capricornio": "Capricórnio", "aquario": "Aquário",
         "peixes": "Peixes"}


def atualizar():
    chave = "/media/veracrypt23/Chaves/youtube.chave"
    if not os.path.exists(chave): sys.exit("cofre fechado: sem a chave de leitura do YouTube")
    K = open(chave).read().strip()
    ids = [v[0] for L in VIDEOS.values() for v in L] + list(SIGNOS_2026.values())
    d = {}
    for i in range(0, len(ids), 50):
        u = (f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,status&id={','.join(ids[i:i + 50])}&key={K}")
        for v in json.load(urllib.request.urlopen(u, timeout=60))["items"]:
            st = v["status"]
            if st["privacyStatus"] != "public" or not st.get("embeddable", True):
                print("⚠️ fora (não público ou não incorporável):", v["id"], v["snippet"]["title"][:60]); continue
            d[v["id"]] = {"t": v["snippet"]["title"], "d": v["snippet"]["publishedAt"], "dur": v["contentDetails"]["duration"]}
    for i in ids:
        if i not in d: print("⚠️ sem dados (privado/apagado?):", i)
    json.dump(d, open(DADOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(d), "vídeos em", DADOS)


def minutos(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m: return ""
    h, mi, s = (int(x or 0) for x in m.groups()); mi += h * 60
    return f"{mi} min" if mi else f"{s} s"


def figura(vid, titulo, legenda, info):
    e = html.escape
    return (f'<figure class="gt-video"><button type="button" class="gt-video-capa" data-id="{vid}" aria-label="Ver o vídeo: {e(titulo)}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{e(titulo)} — vídeo do Mestre Alberto" width="480" height="360" '
            f'loading="lazy" decoding="async"><span class="gt-play" aria-hidden="true">▶</span></button>'
            f'<figcaption><b>{e(titulo)}</b> · {e(legenda)}{" · " + minutos(info.get("dur")) if info.get("dur") else ""}</figcaption></figure>')


def ld(vid, titulo, legenda, info):
    return {"@type": "VideoObject", "name": titulo, "description": legenda,
            "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg", f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg"],
            "uploadDate": info["d"], "duration": info["dur"], "embedUrl": f"https://www.youtube.com/embed/{vid}",
            "url": f"https://www.youtube.com/watch?v={vid}",
            "creator": {"@type": "Person", "name": "Mestre Alberto", "url": SITE + "/sobre"},
            "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE}}


ESTILO = ('<!-- video-pagina:js:inicio --><style>'
          '.gt-videos{max-width:46rem;margin:0 auto 2rem;padding:0 1rem;position:relative;z-index:1;display:grid;gap:1.2rem}'
          '.gt-videos h2{text-align:center;margin:0}'
          '.gt-video{margin:0}.gt-video-capa,.gt-video iframe{display:block;position:relative;width:100%;aspect-ratio:16/9;border:1px solid rgba(212,175,55,.4);'
          'border-radius:1rem;overflow:hidden;background:#000;padding:0;cursor:pointer;box-shadow:0 14px 40px #0007}'
          '.gt-video-capa img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s,filter .5s}'
          '.gt-video-capa:hover img,.gt-video-capa:focus-visible img{transform:scale(1.04);filter:brightness(1.1)}'
          '.gt-play{position:absolute;inset:0;margin:auto;width:4.4rem;height:3.1rem;border-radius:.9rem;background:#e01b1b;color:#fff;'
          'font-size:1.5rem;display:grid;place-items:center;box-shadow:0 4px 18px #0008}'
          '.gt-video figcaption{font-size:.88rem;opacity:.85;margin-top:.55rem;text-align:center;line-height:1.45}'
          '.signo .gt-video{margin:.9rem 0 .4rem}'
          '</style><script>document.addEventListener("click",function(e){var b=e.target.closest(".gt-video-capa");if(!b)return;'
          'var f=document.createElement("iframe");f.src="https://www.youtube-nocookie.com/embed/"+b.dataset.id+"?autoplay=1&rel=0";'
          'f.title=b.getAttribute("aria-label");f.allow="autoplay; encrypted-media; picture-in-picture; fullscreen";f.allowFullscreen=true;'
          'f.style.border="0";b.replaceWith(f);});</script><!-- video-pagina:js:fim -->\n')


def limpar(h):
    h = re.sub(r"<!-- video-pagina:[\w-]*:?inicio -->.*?<!-- video-pagina:[\w-]*:?fim -->\n?", "", h, flags=re.S)
    return re.sub(r'<script type="application/ld\+json" data-video-pagina>.*?</script>\n?', "", h, flags=re.S)


def por_ld(h, objs):
    if not objs: return h
    j = json.dumps({"@context": "https://schema.org", "@graph": objs}, ensure_ascii=False)
    return h.replace("</head>", f'<script type="application/ld+json" data-video-pagina>{j}</script>\n</head>', 1)


def aplicar():
    if not os.path.exists(DADOS): return
    D = json.load(open(DADOS, encoding="utf-8")); mudadas = []
    for pag, lista in VIDEOS.items():
        f = f"{pag}.html"
        if not os.path.exists(f): continue
        h0 = open(f, encoding="utf-8").read(); h = limpar(h0)
        lista = [v for v in lista if v[0] in D]
        if not lista: continue
        tit = "🎬 Em vídeo, com o Mestre Alberto" if len(lista) > 1 else "🎬 Veja o vídeo do Mestre Alberto"
        bloco = (f'<!-- video-pagina:inicio -->\n<section class="gt-videos" aria-label="Vídeos do Mestre Alberto"><h2>{tit}</h2>'
                 + "".join(figura(v, t, l, D[v]) for v, t, l in lista) + '</section>\n<!-- video-pagina:fim -->\n')
        if "<!-- img-destaque:fim -->\n" in h:
            i = h.index("<!-- img-destaque:fim -->\n") + len("<!-- img-destaque:fim -->\n")
        else:
            m = re.search(r'<section class="hero[i]?"[^>]*>', h)
            if not m: print("⚠️", f, "sem bloco de topo"); continue
            i = h.index("</section>", m.end()) + len("</section>")
            if h[i:i + 1] == "\n": i += 1
        h = h[:i] + bloco + h[i:]
        h = h.replace("</body>", ESTILO + "</body>", 1)
        h = por_ld(h, [ld(v, t, l, D[v]) for v, t, l in lista])
        if h != h0: open(f, "w", encoding="utf-8").write(h); mudadas.append(f)
    # /signos-2026: dentro do cartão de cada signo, antes da ligação «E em 2027?»
    f = "signos-2026.html"
    if os.path.exists(f):
        h0 = open(f, encoding="utf-8").read(); h = limpar(h0); objs = []
        for slug, vid in SIGNOS_2026.items():
            if vid not in D: continue
            alvo = f'<div class="dica"><b>👉 E em 2027?</b><a href="/horoscopo-2027-{slug}"'
            if alvo not in h: continue
            t = f"Previsão Anual 2026 de {NOMES[slug]}"; l = f"Os 12 meses de 2026 para {NOMES[slug]}, em vídeo, pelo Mestre Alberto."
            h = h.replace(alvo, f"<!-- video-pagina:{slug}:inicio -->" + figura(vid, t, l, D[vid]) + f"<!-- video-pagina:{slug}:fim -->\n" + alvo, 1)
            objs.append(ld(vid, t, l, D[vid]))
        if objs:
            h = h.replace("</body>", ESTILO + "</body>", 1); h = por_ld(h, objs)
        if h != h0: open(f, "w", encoding="utf-8").write(h); mudadas.append(f)
    for f in mudadas: print(f)


if __name__ == "__main__":
    atualizar() if "--atualizar" in sys.argv else aplicar()
