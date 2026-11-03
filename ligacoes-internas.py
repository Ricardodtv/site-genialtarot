#!/usr/bin/env python3
"""Ligações internas DENTRO dos textos (03/11/2026, pedido dele: «em todos os textos das minhas páginas, cerca de 2 links
em palavras-chave que levem a outras páginas sobre essa palavra»).

Regras (combinadas com ele):
  • 2 a 3 por página (MAX), só na 1.ª vez que a palavra aparece, só em parágrafos de texto (<p>, <li>)
  • nunca em títulos, botões, ligações que já existem, menus, rodapé, o cartão gt-casa, scripts
  • nunca para a própria página nem para uma página para onde o texto já liga
  • prioridade às páginas que estão perto do topo do Google e às novas (PESO)
Cada ligação leva class="li-gt" — reversível: python3 ligacoes-internas.py --tirar
  python3 ligacoes-internas.py pagina.html [...]   # só estas
  python3 ligacoes-internas.py --todas            # todas (imprime as que mudou — para o pre-commit)
"""
import glob, hashlib, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
MAX = 3
FORA = {"index.html", "404.html", "pagar.html", "30-dias.html", "30-dias-autorizacao.html", "privacidade.html", "termos.html",
        "sair.html", "obrigado.html", "mapa-do-site.html"}
# (padrão, página, peso)  — o padrão é procurado no texto; (?i) só onde não há risco de confundir
_I = "(?i)"
SIGNOS = [("Carneiro|Áries", "carneiro"), ("Touro", "touro"), ("Gémeos|Gêmeos", "gemeos"), ("Caranguejo|Câncer", "caranguejo"),
          ("Leão", "leao"), ("Virgem", "virgem"), ("Balança|Libra", "balanca"), ("Escorpião", "escorpiao"), ("Sagitário", "sagitario"),
          ("Capricórnio", "capricornio"), ("Aquário", "aquario"), ("Peixes", "peixes")]
TERMOS = [
    (_I + r"calcular o (seu )?ascendente|signo ascendente|o (seu )?ascendente", "/ascendente", 9),
    (_I + r"mapa astral|mapa de nascimento", "/mapa-astral", 8),
    (_I + r"tarot grátis|tiragem grátis|tirar as cartas", "/tarot-gratis", 8),
    (_I + r"horóscopo (de hoje|do dia)", "/horoscopo-do-dia", 7),
    (_I + r"horóscopo semanal|horóscopo da semana", "/horoscopo-semanal", 7),
    (_I + r"quem faz anos hoje", "/aniversarios", 8),
    (_I + r"significado dos sonhos|interpretação (dos|de) sonhos", "/sonhos", 7),
    (_I + r"tarot cigano|baralho cigano", "/tarot-cigano", 7),
    (_I + r"merc[uú]rio retr[oó]grado|planetas retr[oó]grados", "/retrogrados", 6),
    (_I + r"lua cheia|lua nova|fases da lua", "/lua", 6),
    (_I + r"lua azul", "/lua-azul", 6),
    (_I + r"eclipses?", "/eclipses-2027", 5),
    (_I + r"compatibilidade entre signos|signos que combinam", "/signos-que-combinam", 7),
    (_I + r"compatibilidade amorosa|compatibilidade no amor", "/compatibilidade-entre-signos", 6),
    (_I + r"datas dos signos", "/datas-dos-signos", 6),
    (_I + r"(os )?(12|doze) signos( do zodíaco)?|signos do zodíaco|signos astrológicos", "/signos-do-zodiaco", 5),
    (_I + r"arcanos maiores", "/arcanos", 6), (_I + r"arcanos menores", "/arcanos-menores", 6),
    (_I + r"cruz celta", "/tiragem-cruz-celta", 5), (_I + r"rider-?waite", "/tarot-rider-waite", 6),
    (_I + r"consulta de tarot|leitura de tarot", "/consulta-de-tarot-online", 6),
    (_I + r"numerologia", "/numerologia", 5), (_I + r"quiromancia", "/quiromancia", 4),
    (_I + r"horóscopo chinês|signos chineses", "/horoscopo-chines", 5),
    (_I + r"astrologia védica", "/astrologia-vedica", 5), (_I + r"zodíaco sideral|astrologia sideral", "/astrologia-sideral", 6),
    (_I + r"astrologia horária", "/astrologia-horaria", 6), (_I + r"stellium", "/stellium-astrologia", 6),
    (_I + r"revolução solar", "/revolucao-solar", 5), (_I + r"carta de tarot pela data|arcano pessoal", "/carta-de-tarot", 6),
    (_I + r"elemento fogo|signos de fogo", "/elemento-fogo", 4), (_I + r"elemento terra|signos de terra", "/elemento-terra", 4),
    (_I + r"elemento ar|signos de ar", "/elemento-ar", 4), (_I + r"elemento água|signos de água", "/elemento-agua", 4),
    (r"Júpiter", "/planeta-jupiter", 3), (r"Saturno", "/planeta-saturno", 3), (r"Vénus|Vênus", "/planeta-venus", 3),
    (r"Marte", "/planeta-marte", 3), (r"Plutão", "/planeta-plutao", 3), (r"Neptuno|Netuno", "/planeta-neptuno", 3),
    (r"Úrano|Urano", "/planeta-urano", 3), (r"Mercúrio", "/planeta-mercurio", 3),
    # arcanos com maiúscula (para «a morte», «o carro» do dia a dia não contarem)
    (r"[oO] Louco", "/arcano-00-o-louco", 4), (r"[oO] Mago", "/arcano-01-o-mago", 4), (r"[aA] Sacerdotisa|[aA] Papisa", "/arcano-02-a-sacerdotisa", 4),
    (r"[aA] Imperatriz", "/arcano-03-a-imperatriz", 4), (r"[oO] Imperador", "/arcano-04-o-imperador", 4), (r"[oO] Hierofante", "/arcano-05-o-hierofante", 4),
    (r"[oO]s Enamorados", "/arcano-06-os-enamorados", 4), (r"a carta do Carro|o Carro", "/arcano-07-o-carro", 4), (r"[aA] Força", "/arcano-08-a-forca", 4),
    (r"[oO] Eremita", "/arcano-09-o-eremita", 4), (r"[aA] Roda da Fortuna", "/arcano-10-a-roda-da-fortuna", 4), (r"[aA] Justiça", "/arcano-11-a-justica", 4),
    (r"[oO] Enforcado|[oO] Pendurado", "/arcano-12-o-enforcado", 4), (r"a carta da Morte|a Morte", "/arcano-13-a-morte", 4),
    (r"[aA] Temperança", "/arcano-14-a-temperanca", 4), (r"[oO] Diabo", "/arcano-15-o-diabo", 4), (r"[aA] Torre", "/arcano-16-a-torre", 4),
    (r"[aA] Estrela", "/arcano-17-a-estrela", 4), (r"[oO] Julgamento", "/arcano-20-o-julgamento", 4),
    # 03/11: palavras gerais, com peso baixo (só entram se não houver melhor) — para cada página chegar às ~2 ligações
    (_I + r"tiragem do amor", "/tiragem-do-amor", 5), (_I + r"sim ou não", "/tiragem-sim-ou-nao", 5), (_I + r"carta do dia", "/tiragem-carta-do-dia", 5),
    (_I + r"rituais|ritual", "/rituais", 3), (_I + r"amuletos?", "/amuletos", 3), (_I + r"orações|oração|rezas", "/rezas-e-oracoes", 3),
    (_I + r"pesadelos?", "/sonho/pesadelos", 3), (_I + r"os sonhos|um sonho|sonhos", "/sonhos", 2),
    (r"[aA] Lua", "/lua", 2), (r"[oO] Sol", "/planeta-sol", 2), (_I + r"astrologia", "/astrologia", 2),
    (_I + r"horóscopo", "/horoscopo", 2), (_I + r"compatibilidade", "/compatibilidade-entre-signos", 2),
    (_I + r"cartomancia", "/cartomancia", 3), (_I + r"benzimentos?|benzeduras?", "/benzimentos", 3),
    (r"(?:[oO]|[dD]o|[nN]o) Tarot", "/arcanos", 1),
    (_I + r"(?:a |uma |na |numa )relação|o amor|no amor", "/tarot-do-amor", 1), (_I + r"o dinheiro|no dinheiro|finanças", "/tarot-dinheiro", 1),
    (_I + r"o trabalho|no trabalho|carreira", "/tarot-trabalho", 1), (_I + r"a família|na família", "/tarot-familia", 1),
    (_I + r"fim de (um )?ciclo|recomeço|mudança de vida", "/cartas-do-tarot-mudanca", 1),
] + [(rf"\b(?:{p})\b(?! no Tarot)", f"/signo/{s}", 4) for p, s in SIGNOS]
# 03/11: os sonhos ligam-se entre si pela palavra do sonho («gato», «cobra», «água»…), tirada dos próprios endereços
_SONHO_PAL = {"agua": "água|águas", "cafe": "café", "caixao": "caixão", "pao": "pão", "maos": "mãos", "pes": "pés", "telemovel": "telemóvel",
              "traicao": "traição", "doenca": "doença", "discussao": "discussão", "cemiterio": "cemitério", "crianca": "criança|crianças",
              "bebe": "bebé|bebê", "mae": "mãe", "aviao": "avião", "tubarao": "tubarão", "jacare": "jacaré", "leao": "leão", "prisao": "prisão",
              "passaros": "pássaros", "cachorro": "cachorro|cão", "gato": "gato|gatos", "cobra": "cobra|cobras|serpente", "dinheiro": "dinheiro",
              "casamento": "casamento", "fogo": "fogo", "mar": "mar", "chuva": "chuva", "ouro": "ouro", "flores": "flores", "espelho": "espelho",
              "aranha": "aranha|aranhas", "rato": "rato|ratos", "lobo": "lobo|lobos", "cavalo": "cavalo|cavalos", "peixe": "peixe|peixes",
              "borboleta": "borboleta|borboletas", "anjo": "anjo|anjos", "chave": "chave|chaves", "porta": "porta|portas", "escada": "escada|escadas",
              "igreja": "igreja", "velas": "vela|velas", "sangue": "sangue", "fantasma": "fantasma|fantasmas", "bruxa": "bruxa|bruxas", "ovos": "ovo|ovos",
              "unhas": "unhas", "cabelo": "cabelo", "beijo": "beijo", "festa": "festa", "neve": "neve", "rio": "rio", "lama": "lama", "vinho": "vinho",
              "bolo": "bolo", "doces": "doces", "carne": "carne", "fruta": "fruta|frutas", "roupa": "roupa", "sapatos": "sapatos", "anel": "anel",
              "olhos": "olhos", "carro": "carro", "casa": "casa", "deus": "Deus", "diabo": "diabo"}
for _f in glob.glob("sonho/sonhar-com-*.html"):
    _k = _f[len("sonho/sonhar-com-"):-5]
    if _k in _SONHO_PAL: TERMOS.append((_I + rf"(?:{_SONHO_PAL[_k]})", f"/sonho/sonhar-com-{_k}", 4))
TERMOS = [(re.compile(rf"(?<![\w-])(?:{p})(?![\w-])" if not p.startswith(_I) else _I + rf"(?<![\w-])(?:{p[len(_I):]})(?![\w-])"), u, w)
          for p, u, w in TERMOS if os.path.exists(u.lstrip("/") + ".html")]

ZONAS = re.compile(r'<a\b[^>]*>.*?</a>|<section class="(?:heroi|hero)[^"]*".*?</section>|<p class="(?:sub|resumo|cat)[^"]*".*?</p>|' r"<(header|nav|footer|aside|script|style|h[1-6]|button|figure|figcaption|select|label|form)\b.*?</\1>|<!-- gt-casa:inicio -->.*?<!-- gt-casa:fim -->", re.S | re.I)
BLOCO = re.compile(r"<(p|li)\b[^>]*>.*?</\1>", re.S | re.I)
LIG = re.compile(r'<a class="li-gt" href="[^"]*">(.*?)</a>', re.S)


def eu_de(f):
    return "/" + re.sub(r"\.html$", "", f).replace("index", "")


def aplicar(f, tirar=False):
    h0 = open(f, encoding="utf-8").read()
    h = LIG.sub(r"\1", h0)
    if tirar:
        return h if h != h0 else None
    eu = eu_de(f)
    if "<body" not in h or re.search(r'<meta[^>]+name="robots"[^>]+noindex', h, re.I): return None
    corpo_i = h.find("<body"); fim = h.find("<!-- gt-casa:inicio -->"); fim = fim if fim > 0 else h.rfind("</body>")
    proibido = [(m.start(), m.end()) for m in ZONAS.finditer(h)]
    dentro = lambda i: any(a <= i < b for a, b in proibido)
    # 03/11: só conta o que JÁ está ligado dentro do texto (os menus e as caixas de temas não impedem uma ligação no texto)
    ja = {u for b in BLOCO.finditer(h, corpo_i, fim) for u in re.findall(r'href="(?:https://genialtarot\.com)?(/[^"#?]*)"', b.group(0))}
    # candidatos: (peso, ordem estável por página, posição, termo)
    sal = int(hashlib.md5(f.encode()).hexdigest(), 16)
    cands = []
    for k, (rx, u, w) in enumerate(TERMOS):
        if u == eu or u in ja or (eu.startswith("/signo/") and u.startswith("/signo/")): continue
        if u.startswith("/sonho/") and not eu.startswith("/sonho"): continue   # as palavras dos sonhos só ligam entre sonhos
        for b in BLOCO.finditer(h, corpo_i, fim):
            if dentro(b.start()): continue
            # só texto fora de etiquetas e de <a> dentro do bloco
            seg = b.group(0); off = b.start()
            fora_a = re.sub(r"<a\b.*?</a>", lambda m: "\0" * len(m.group(0)), seg, flags=re.S)
            fora_a = re.sub(r"<[^>]+>", lambda m: "\0" * len(m.group(0)), fora_a)
            m = rx.search(fora_a)
            if m:
                cands.append((-w, (sal >> (k % 60)) & 7, off + m.start(), off + m.end(), u)); break
    cands.sort()
    escolha, alvos = [], set()
    for c in cands:
        if c[4] in alvos or any(not (c[3] <= e[2] or c[2] >= e[3]) for e in escolha): continue
        # no máximo 1 por parágrafo
        if any(BLOCO_DE(h, c[2]) == BLOCO_DE(h, e[2]) for e in escolha): continue
        escolha.append(c); alvos.add(c[4])
        if len(escolha) == MAX: break
    for _, _, a, b, u in sorted(escolha, key=lambda x: -x[2]):
        h = h[:a] + f'<a class="li-gt" href="{u}">' + h[a:b] + "</a>" + h[b:]
    return h if h != h0 else None


def BLOCO_DE(h, i):
    a = max(h.rfind("<p", 0, i), h.rfind("<li", 0, i)); return a


if __name__ == "__main__":
    tirar = "--tirar" in sys.argv
    if "--todas" in sys.argv or tirar:
        fs = [f for f in sorted(glob.glob("*.html") + glob.glob("signo/*.html") + glob.glob("sonho/*.html"))
              if os.path.basename(f) not in FORA and not os.path.basename(f).startswith(("o-teu-ceu", "google"))]
    else:
        fs = [a for a in sys.argv[1:] if a.endswith(".html")]
    for f in fs:
        n = aplicar(f, tirar)
        if n is not None:
            open(f, "w", encoding="utf-8").write(n); print(f)
