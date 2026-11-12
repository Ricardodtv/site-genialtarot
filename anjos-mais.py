#!/usr/bin/env python3
"""Acrescenta a cada /anjo/<nome> (72) o bloco <!-- anjo-mais:inicio/fim --> com texto próprio do anjo (12/11/2026,
«travão» ao SEO: as 72 páginas eram 60% iguais entre si e tinham ~180 palavras).

Idempotente: se o bloco já existe, substitui-o; se não, põe-no logo a seguir à secção «Um gesto para hoje». Não toca em
mais nada da página (ligações li-gt, gt-casa, etc. ficam). Textos em anjos-mais-textos.py. Chamado no fim do gerar-anjos.py.
    python3 anjos-mais.py            → as 72
"""
import html, importlib.util, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)


def _mod(f):
    s = importlib.util.spec_from_file_location(f.replace("-", "_")[:-3], f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


ANJOS = _mod("anjos-textos.py").ANJOS
MAIS = _mod("anjos-mais-textos.py").MAIS
E = html.escape
A, B = "<!-- anjo-mais:inicio -->", "<!-- anjo-mais:fim -->"


def hora(m): return f"{m // 60:02d}:{m % 60:02d}"


def bloco(i, n):
    d = MAIS[n]
    fim = n[-2:].lower()
    suf = ("a terminação «-el» é a palavra hebraica para Deus" if fim == "el" else
           "a terminação «-iah» / «-ah» lembra «Yah», a forma curta do nome divino" if fim in ("ah", "ia") else
           "como os outros 71, é lido como um nome de Deus e não como o nome de uma pessoa")
    if d["cv"]:
        c, v = d["cv"].split(":", 1)
        if d["livro"] == "Salmos":
            verso = (f"Na tradição dos 72 Nomes, cada anjo tem um versículo que se lê ao invocá-lo. Para {n} é o Salmo {c}, "
                     f"{'versículos' if '-' in v else 'versículo'} {v.replace('-', ' e ')}, na numeração da Bíblia de Almeida. "
                     f"Noutras edições, sobretudo nas que seguem a numeração antiga da Vulgata, o número do salmo ou do versículo pode mudar um pouco.")
        else:
            verso = (f"Na tradição dos 72 Nomes, cada anjo tem um versículo que se lê ao invocá-lo. {n} é o único da lista "
                     f"que não tem um salmo: o seu versículo é o primeiro da Bíblia, Génesis {c}, {v}, «No princípio».")
    else:
        verso = (f"Na tradição dos 72 Nomes, cada anjo tem um versículo que se lê ao invocá-lo. Para {n}, as listas publicadas não "
                 f"concordam no salmo, e por isso não o indicamos aqui: a oração desta página serve no lugar dele.")
    ini = i * 20
    reg = (f"Numa tradição muito divulgada, cada um dos 72 guarda vinte minutos do dia, a contar da meia-noite: "
           f"a {n} cabem os minutos das {hora(ini)} às {hora((ini + 20) % 1440)}. É uma boa hora para o chamar, mas qualquer hora serve.")
    return (f'{A}\n  <section class="cartao texto">'
            f'<h2>O nome e o versículo de {n}</h2>'
            f'<p>Os 72 Nomes saem de três versículos seguidos do Êxodo (14, 19 a 21), com 72 letras hebraicas cada um. Lidos em conjunto, '
            f'dão 72 grupos de três letras. O de {n}, o n.º {i + 1}, escreve-se <span lang="he" dir="rtl">{E(d["heb"])}</span>, e {suf}.</p>'
            f'<p>{E(verso)}</p>'
            f'<h2>Quando pedir a ajuda de {n}</h2><p>{E(d["quando"])}</p>'
            f'<h2>Como invocar {n}</h2><p>{E(d["invocar"])}</p><p>{E(reg)}</p>'
            f'<h2>Uma reflexão para esta semana</h2><p>{E(d["reflexao"])}</p></section>\n{B}')


def aplicar(f, novo):
    s = open(f, encoding="utf8").read()
    if A in s:
        i, j = s.index(A), s.index(B) + len(B)
        t = s[:i] + novo + s[j:]
    else:
        k = s.find("<h2>Um gesto para hoje</h2>")
        if k < 0: raise SystemExit(f"{f}: não encontrei «Um gesto para hoje»")
        k = s.index("</section>", k) + len("</section>")
        t = s[:k] + "\n" + novo + s[k:]
    if t != s:
        open(f, "w", encoding="utf8").write(t)
        return True
    return False


if __name__ == "__main__":
    assert len(MAIS) == 72 and all(a[0] in MAIS for a in ANJOS)
    mud = sum(aplicar(f"anjo/{a[0].lower()}.html", bloco(i, a[0])) for i, a in enumerate(ANJOS))
    print(f"anjos-mais: {mud} páginas mudadas")
