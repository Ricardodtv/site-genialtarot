#!/usr/bin/env python3
"""As 12 páginas «Signos compatíveis com <signo>» (26/11/2026). Em Portugal o Google sugere «signos compatíveis com
caranguejo», «…com capricórnio», «…com carneiro no amor»: havia os 78 pares e a montra, mas nenhuma página por signo.

Só cria estas 12 páginas e acrescenta UMA ligação para elas na /compatibilidade-entre-signos e em cada /signo/<signo>
(linhas novas, nunca mexe nas que já lá estão). Pode correr-se as vezes que se quiser: o resultado é sempre o mesmo.
NÃO corre o gerar-signos.py nem precisa dele.

  · as notas (1–5) e os textos dos pares vêm de compat-textos-a.py e compat-textos-b.py — os MESMOS das 78 páginas de pares;
  · o que é próprio de cada signo vem de compativeis-textos.py;
  · o molde (cabeça, CSS, bloco gt-casa, rodapé) é copiado da página de um par já publicada.

Correr: python3 gerar-compativeis.py"""
import html, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
SITE = "https://genialtarot.com"
HOJE = "26/11/2026"
E = lambda t: html.escape(t, quote=True)
S = json.load(open("signos-textos.json", encoding="utf-8"))
GLIFO = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
ELEM = ["Fogo", "Terra", "Ar", "Água"]
nm = lambda x: x["pt"] if x["pt"] == x["br"] else f"{x['pt']} ({x['br']})"

CA, CB, TX = {}, {}, {}
exec(open("compat-textos-a.py", encoding="utf-8").read(), CA)
exec(open("compat-textos-b.py", encoding="utf-8").read(), CB)
exec(open("compativeis-textos.py", encoding="utf-8").read(), TX)
TEXTOS = TX["TEXTOS"]
PAR = {}
for c in CA["COMPAT_A"] + CB["COMPAT_B"]:
    PAR[(c["i"], c["j"])] = PAR[(c["j"], c["i"])] = c
assert len(PAR) == 144, len(PAR)
cslug = lambda i, j: f"compatibilidade-{S[min(i, j)]['slug']}-e-{S[max(i, j)]['slug']}"
pslug = lambda i: f"signos-compativeis-com-{S[i]['slug']}"

# as perguntas escritas à mão que citam uma nota têm de bater com a nota do par (as mesmas das páginas de pares)
for i, s in enumerate(S):
    q, r = TEXTOS[s["slug"]]["faq"]
    m = re.search(r"nota do par é (\d)", r)
    if m:
        outros = [j for j in range(12) if re.search(rf"\b{re.escape(S[j]['pt'])}\b", q) and (j != i or q.count(s["pt"]) > 1)]
        assert outros and all(PAR[(i, j)]["nota"] == int(m.group(1)) for j in outros), (s["slug"], q, outros)

# ── o molde: copiado de uma página de par já publicada (mesma cabeça, mesmo CSS, mesmo bloco gt-casa e rodapé)
MOLDE = open("compatibilidade-caranguejo-e-leao.html", encoding="utf-8").read()
ESTILO = re.search(r"<style>.*?</style>", MOLDE, re.S).group(0)
CASA = re.search(r"<!-- gt-casa:inicio -->.*?<!-- gt-casa:fim -->\n", MOLDE, re.S).group(0)
FIM = MOLDE[MOLDE.index("<footer>"):]
FONTES = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com" />.*?rel="stylesheet" />\n', MOLDE, re.S).group(0)
AUTOR = {"@type": "Person", "name": "Mestre Alberto", "url": SITE + "/sobre"}
EDITOR = {"@type": "Organization", "name": "Genial Tarot", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/og-image.jpg"}}
EXTRA_CSS = """<style>
/* 26/11/2026: «Signos compatíveis com …» — a resposta rápida e a lista dos 12 */
.resposta { border: 1.5px solid oklch(0.85 0.13 88 / .6); }
.resposta p { margin: .45rem 0; }
.resposta b { color: var(--ouro); }
.doze-pares { list-style: none; padding: 0; margin: .8rem 0 0; }
.doze-pares li { padding: .7rem 0; border-top: 1px solid var(--borda); line-height: 1.5; }
.doze-pares li:first-child { border-top: 0; }
.doze-pares .nota { color: var(--ouro); letter-spacing: .08em; white-space: nowrap; margin-right: .35rem; }
.doze-pares a { font-weight: 700; }
</style>
"""


def frase(t, n=1):
    """as primeiras n frases de um texto"""
    p = re.split(r"(?<=[.!?])\s+", t.strip())
    return " ".join(p[:n])


def lista(nomes):
    return nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " e " + nomes[-1]


def coracoes(n): return "♥" * n + "♡" * (5 - n)


def pagina(i):
    s = S[i]; t = TEXTOS[s["slug"]]; X = nm(s); slug = pslug(i); url = f"{SITE}/{slug}"
    img = f"{SITE}/signos/signo-{s['slug']}.webp"
    # ordem: nota mais alta primeiro; no empate, o mesmo elemento, depois a ordem do zodíaco a contar do próprio signo
    ordem = sorted(range(12), key=lambda j: (-PAR[(i, j)]["nota"], j % 4 != i % 4, (j - i) % 12))
    notas = sorted({PAR[(i, j)]["nota"] for j in range(12)}, reverse=True)
    top, seg, baixo = ([j for j in ordem if PAR[(i, j)]["nota"] == n] for n in (notas[0], notas[1], notas[-1]))
    nomes = lambda L: lista([f"outro {s['pt']}" if j == i else nm(S[j]) for j in L])
    reg = s["regente"]; reg = ("pela " + reg[2:]) if reg.startswith("a ") else ("pelo " + reg[2:]) if reg.startswith("o ") else "por " + reg
    def sem_rotulo(t):   # «Na amizade, guardam…» → «Guardam…» (o rótulo já está à frente)
        t = frase(t); m = re.match(r"(Na amizade|Como amigos|Enquanto amigos|Como amigo), ", t)
        return t[m.end()].upper() + t[m.end() + 1:] if m else t
    op = (i + 6) % 12

    titulo = f"Signos compatíveis com {X} no amor e na amizade"
    if len(titulo) > 65: titulo = f"Signos compatíveis com {s['pt']} no amor e na amizade"
    desc = f"Com quem combina {X}? Os mais compatíveis são {lista([S[j]['pt'] for j in top])}; os mais difíceis, {lista([S[j]['pt'] for j in baixo])}. A nota dos 12 pares."
    if len(desc) > 160: desc = f"Com quem combina {X}? Os mais compatíveis são {lista([S[j]['pt'] for j in top])}. Veja os mais difíceis e a nota dos 12 pares."
    if len(desc) > 160: desc = f"Com quem combina {X}? Os signos mais compatíveis, os mais difíceis e a nota de cada um dos 12 pares no amor e na amizade."
    assert len(titulo) <= 65 and 110 <= len(desc) <= 160, (slug, len(titulo), len(desc), desc)

    # perguntas frequentes: 4 tiradas dos dados dos pares + 1 escrita à mão para este signo
    p1 = PAR[(i, top[0])]; pb = PAR[(i, baixo[0])]
    faq = [
        (f"Qual é o signo mais compatível com {s['pt']}?",
         f"Pela nota de afinidade do Genial Tarot, {'são' if len(top) > 1 else 'é'} {nomes(top)}, com {notas[0]} em 5. {frase(p1['amor'])}"),
        (f"Com que signos {s['pt']} tem mais dificuldade?",
         f"As notas mais baixas de {s['pt']}, {notas[-1]} em 5, são com {nomes(baixo)}. {frase(pb['desafios'])} Uma nota baixa mostra onde é mais provável haver atrito; com conversa, muitos destes pares resultam."),
        (f"E na amizade, com quem se dá melhor {s['pt']}?",
         f"{t['amizade']} A nota do site é a mesma para o amor e para a amizade, e as mais altas são com {nomes(top)}."),
    ]
    if s["slug"] in ("escorpiao", "aquario", "peixes"):   # a pergunta escrita à mão já é sobre o par consigo próprio
        po = PAR[(i, op)]
        faq.append((f"{s['pt']} combina com {S[op]['pt']}, o signo oposto?", f"A nota do par é {po['nota']} em 5. {frase(po['resumo'])} {frase(po['conselho'])}"))
    else:
        pp = PAR[(i, i)]
        faq.append((f"{s['pt']} combina com outro {s['pt']}?", f"A nota do par {s['pt']} com {s['pt']} é {pp['nota']} em 5. {frase(pp['resumo'], 2)}"))
    faq.append(t["faq"])

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": titulo, "description": desc, "image": img, "inLanguage": "pt", "author": AUTOR, "publisher": EDITOR, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Compatibilidade entre signos", "item": SITE + "/compatibilidade-entre-signos"},
            {"@type": "ListItem", "position": 3, "name": f"Signos compatíveis com {s['pt']}", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]}]}

    linhas = "".join(
        f'      <li><span class="nota" aria-label="afinidade {PAR[(i, j)]["nota"]} em 5">{coracoes(PAR[(i, j)]["nota"])}</span>'
        f'<a href="/{cslug(i, j)}">{GLIFO[j]}︎ {E(s["pt"])} e {E(S[j]["pt"])}</a> · {E(frase(PAR[(i, j)]["resumo"]))}</li>\n' for j in ordem)
    outros = "".join(f'<a href="/{pslug(k)}">{GLIFO[k]}︎ {E(S[k]["pt"])}</a>' for k in range(12) if k != i)
    meio = [j for j in ordem if j not in top + seg + baixo]
    corpo = f"""  <section class="heroi">
    <img class="foto-mestre" src="/signos/signo-{s['slug']}.webp" alt="Signo de {E(s['pt'])}" width="100" height="100" />
    <h1><span class="az">Signos compatíveis com {E(X)}</span></h1>
    <p class="sub">{E(s['datas'])} · {ELEM[i % 4]} · regido {E(reg)}</p>
  </section>
  <section class="cartao texto resposta">
    <h2>Com quem combina {E(s['pt'])}</h2>
    <p><b>Mais compatíveis ({notas[0]} em 5):</b> {E(nomes(top))}.{f" A seguir, com {notas[1]} em 5: {E(nomes(seg))}." if seg else ""}</p>
    {f'<p><b>A meio caminho ({notas[2]} em 5):</b> {E(nomes(meio))}.</p>' if meio else ''}
    <p><b>Mais desafiantes ({notas[-1]} em 5):</b> {E(nomes(baixo))}.</p>
    <p><b>No amor:</b> {E(frase(p1['amor']))}</p>
    <p><b>Na amizade:</b> {E(sem_rotulo(p1['amizade']))}</p>
  </section>
  <section class="cartao texto">
    <h2>O que {E(s['pt'])} procura numa relação</h2><p>{E(t['abre'])}</p>
    <h2>Porque se dá bem com uns</h2><p>{E(t['fortes'])}</p>
    <h2>E porque tropeça noutros</h2><p>{E(t['dificeis'])}</p>
    <h2>{E(s['pt'])} na amizade</h2><p>{E(t['amizade'])}</p>
  </section>
  <section class="cartao texto">
    <h2>Os 12 signos com {E(s['pt'])}, do mais ao menos compatível</h2>
    <ol class="doze-pares">
{linhas}    </ol>
    <p style="color:var(--suave);font-size:.95rem">A nota de 1 a 5 corações é a mesma das páginas de cada par e segue a astrologia tradicional. O signo solar é só uma parte do mapa: para ver uma relação a sério, compare os dois mapas no <a href="/mapa-do-casal">Mapa do Casal</a> ou na <a href="/compatibilidade">Compatibilidade</a> com as datas de nascimento.</p>
  </section>
  <section class="cartao" style="text-align:center">
    <h2>Os outros signos</h2><div class="ligas">{outros}</div>
    <p><a href="/signo/{s['slug']}">Tudo sobre o signo {E(X)}</a> · <a href="/compatibilidade-entre-signos">Os 78 pares</a> · <a href="/tarot-do-amor">Tarot do Amor</a></p>
  </section>
  <section class="cartao texto"><h2>Perguntas frequentes</h2>
""" + "".join(f"    <h3>{E(q)}</h3><p>{E(r)}</p>\n" for q, r in faq) + "  </section>\n"

    cab = f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{E(titulo)}</title>
<meta name="description" content="{E(desc)}" />
<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{E(titulo)}" />
<meta property="og:description" content="{E(desc)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{img}" />
<meta property="og:locale" content="pt_PT" />
<meta property="og:site_name" content="Genial Tarot" />
<meta name="twitter:card" content="summary_large_image" />
{FONTES}<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{ESTILO}
{EXTRA_CSS}</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
"""
    novo = cab + corpo + CASA + FIM
    f = slug + ".html"
    velho = open(f, encoding="utf-8").read() if os.path.exists(f) else None
    if velho != novo: open(f, "w", encoding="utf-8").write(novo)
    return f, velho != novo


def acrescenta_linha(f, depois_de, linha, marca):
    """insere `linha` a seguir à 1.ª linha que contém `depois_de` — só se `marca` ainda não estiver no ficheiro"""
    x = open(f, encoding="utf-8").read()
    if marca in x: return False
    L = x.split("\n")
    k = next(n for n, l in enumerate(L) if depois_de(n, L))
    L.insert(k + 1, linha)
    open(f, "w", encoding="utf-8").write("\n".join(L))
    return True


if __name__ == "__main__":
    for i in range(12):
        f, mudou = pagina(i)
        print(("escrita " if mudou else "igual   ") + f)
    # a montra: um bloco novo logo a seguir ao topo (com a marca «dd/mm/aaaa: ligações», que o gerar-signos.py guarda)
    bloco = (f'<!-- {HOJE}: ligações às 12 páginas «Signos compatíveis com» --><section class="cartao" style="text-align:center;margin-bottom:1rem">'
             '<h2>Com quem combina cada signo</h2><div class="ligas">'
             + "".join(f'<a href="/{pslug(k)}">{GLIFO[k]}︎ {E(S[k]["pt"])}</a>' for k in range(12)) + "</div></section>")
    print("montra:", acrescenta_linha("compatibilidade-entre-signos.html",
                                      lambda n, L: L[n].lstrip().startswith('<p class="sub">Os 78 pares'), bloco, "signos-compativeis-com-"))
    for i, s in enumerate(S):
        f = f"signo/{s['slug']}.html"
        linha = (f'<!-- {HOJE}: ligação à página «Signos compatíveis com {s["pt"]}» --><section class="cartao" style="text-align:center">'
                 f'<div class="ligas"><a href="/{pslug(i)}">💞 Signos compatíveis com {E(s["pt"])}: do mais ao menos compatível</a></div></section>')
        print(f, acrescenta_linha(f, lambda n, L: n > 0 and "<h2>Compatibilidade de " in L[n - 1] and L[n].strip() == "</section>", linha, pslug(i)))
