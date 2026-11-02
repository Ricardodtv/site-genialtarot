#!/home/ricardo/.venv-astro/bin/python
# -*- coding: utf-8 -*-
"""Alinhamento dos planetas — os dados da página genialtarot.com/alinhamento-dos-planetas (02/11/2026).

Tudo CALCULADO com o Swiss Ephemeris (zodíaco tropical, posições geocêntricas aparentes).
Para cada dia de 2026-11-01 a 2027-12-31, às 21:00 UTC (18:00 em Brasília; 21:00 ou 22:00 em Lisboa — a hora
do anoitecer), grava em alinhamento-dados.json:
  - a longitude eclíptica do Sol, da Lua e dos planetas de Mercúrio a Neptuno (décimas de grau, inteiros)
  - a elongação de cada planeta ao Sol (graus inteiros; com sinal + quando está a ESTE do Sol = céu do anoitecer,
    − quando está a OESTE = céu da madrugada)
e a lista dos «alinhamentos»: os períodos em que 4, 5, 6 ou 7 planetas (Mercúrio a Neptuno) cabem num arco
pequeno do zodíaco (limites em LIMITE, abaixo — são uma convenção nossa, não uma definição astronómica).

O arco é o MENOR arco de longitude que contém os planetas escolhidos: ordena-se o círculo e tira-se o maior buraco.

    ~/.venv-astro/bin/python ~/site-genialtarot/alinhamento-calc.py            → grava o JSON
    ~/.venv-astro/bin/python ~/site-genialtarot/alinhamento-calc.py --ver      → mostra a lista, não grava
"""
import sys, os, json, datetime, itertools
import swisseph as swe

EFEMERIDES = "/home/ricardo/.efemerides-swisseph"
if os.path.isdir(EFEMERIDES): swe.set_ephe_path(EFEMERIDES)
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alinhamento-dados.json")

INICIO, FIM = datetime.date(2026, 11, 1), datetime.date(2027, 12, 31)
HORA_UTC = 21
CORPOS = [("Sol", swe.SUN), ("Lua", swe.MOON), ("Mercúrio", swe.MERCURY), ("Vénus", swe.VENUS), ("Marte", swe.MARS),
          ("Júpiter", swe.JUPITER), ("Saturno", swe.SATURN), ("Úrano", swe.URANUS), ("Neptuno", swe.NEPTUNE)]
PLANETAS = CORPOS[2:]                       # os que entram na contagem do alinhamento (a Lua passa por todos os meses)
VISIVEIS = {"Mercúrio", "Vénus", "Marte", "Júpiter", "Saturno"}   # a olho nu; Úrano e Neptuno precisam de binóculos/telescópio
LIMITE = {4: 45, 5: 60, 6: 135, 7: 150}     # graus: «cabem em» — convenção da página, dita no texto
DESFILE_MIN = 3                             # «desfile»: pelo menos 3 planetas a olho nu no mesmo céu (anoitecer ou madrugada)
ELONG_MIN = 15                              # critério simples de visibilidade: pelo menos 15° afastado do Sol
FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED


def menor_arco(lons):
    """Menor arco (graus) do círculo que contém todas as longitudes, e onde começa."""
    s = sorted(x % 360 for x in lons)
    n = len(s)
    if n == 1: return 0.0, s[0]
    buracos = [((s[(i + 1) % n] - s[i]) % 360, i) for i in range(n)]
    g, i = max(buracos)
    return 360 - g, s[(i + 1) % n]


def dia(d):
    j = swe.julday(d.year, d.month, d.day, HORA_UTC)
    lon = {}
    for nome, c in CORPOS:
        lon[nome] = swe.calc_ut(j, c, FLAGS)[0][0]
    elong = {}
    for nome, c in PLANETAS:
        e = swe.pheno_ut(j, c, FLAGS)[2]          # elongação verdadeira (graus, com latitude)
        leste = (lon[nome] - lon["Sol"]) % 360 < 180
        elong[nome] = e if leste else -e
    return lon, elong


def melhores(lon):
    """Para cada k, o melhor conjunto de k planetas (menor arco)."""
    nomes = [n for n, _ in PLANETAS]
    r = {}
    for k in (4, 5, 6, 7):
        melhor = None
        for comb in itertools.combinations(nomes, k):
            a, ini = menor_arco([lon[n] for n in comb])
            if melhor is None or a < melhor[0]: melhor = (a, comb, ini)
        r[k] = melhor
    return r


def main():
    ver = "--ver" in sys.argv
    dias, linhas = [], []
    d = INICIO
    while d <= FIM:
        lon, elong = dia(d)
        dias.append((d, lon, elong, melhores(lon)))
        d += datetime.timedelta(days=1)

    # episódios: dias seguidos em que o melhor conjunto de k planetas cabe em LIMITE[k]
    episodios = []
    for k in (4, 5, 6, 7):
        cur = None
        for (d, lon, elong, m) in dias + [(None, None, None, None)]:
            dentro = m is not None and m[k][0] <= LIMITE[k]
            if dentro:
                if cur is None: cur = {"k": k, "ini": d, "fim": d, "best": (d, lon, elong, m)}
                else:
                    cur["fim"] = d
                    if m[k][0] < cur["best"][3][k][0]: cur["best"] = (d, lon, elong, m)
            elif cur is not None:
                episodios.append(cur); cur = None

    lista = []
    for e in episodios:
        d, lon, elong, m = e["best"]
        a, comb, ini = m[e["k"]]
        noite = [n for n in comb if n in VISIVEIS and elong[n] >= ELONG_MIN]
        madrugada = [n for n in comb if n in VISIVEIS and elong[n] <= -ELONG_MIN]
        perto_sol = [n for n in comb if abs(elong[n]) < ELONG_MIN]
        lista.append({"k": e["k"], "ini": e["ini"].isoformat(), "fim": e["fim"].isoformat(), "dia": d.isoformat(),
                      "arco": round(a, 1), "pl": list(comb), "noite": noite, "madr": madrugada, "sol": perto_sol})
    lista.sort(key=lambda x: (x["ini"], x["k"]))

    # desfiles: dias seguidos com o MESMO conjunto de ≥ DESFILE_MIN planetas a olho nu no céu do anoitecer
    # (elongação a este ≥ ELONG_MIN) ou da madrugada (a oeste ≥ ELONG_MIN)
    desfiles = []
    for ceu, sinal in (("noite", 1), ("madrugada", -1)):
        cur = None
        for (d, lon, elong, m) in dias + [(None, None, None, None)]:
            conj = tuple(n for n, _ in PLANETAS if n in VISIVEIS and elong[n] * sinal >= ELONG_MIN) if d else ()
            if len(conj) >= DESFILE_MIN and cur and cur["pl"] == list(conj):
                cur["fim"] = d.isoformat()
            else:
                if cur: desfiles.append(cur); cur = None
                if len(conj) >= DESFILE_MIN:
                    cur = {"ceu": ceu, "ini": d.isoformat(), "fim": d.isoformat(), "pl": list(conj)}
    desfiles.sort(key=lambda x: x["ini"])

    if ver:
        for x in lista:
            print(f'{x["k"]} planetas  {x["ini"]} → {x["fim"]}  melhor {x["dia"]}  arco {x["arco"]:5.1f}°  '
                  f'{", ".join(x["pl"])}  | anoitecer: {", ".join(x["noite"]) or "—"} | madrugada: {", ".join(x["madr"]) or "—"}'
                  f' | junto ao Sol: {", ".join(x["sol"]) or "—"}')
        for x in desfiles:
            print(f'desfile {x["ceu"]:9} {x["ini"]} → {x["fim"]}  {", ".join(x["pl"])}')
        return

    out = {
        "gerado": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "inicio": INICIO.isoformat(), "hora_utc": HORA_UTC,
        "corpos": [n for n, _ in CORPOS], "limite": LIMITE, "elong_min": ELONG_MIN,
        # l: longitudes ×10 (inteiros) pela ordem de «corpos»; e: elongações dos planetas (Mercúrio→Neptuno), graus com sinal
        "dias": [{"l": [round(lon[n] * 10) % 3600 for n, _ in CORPOS], "e": [round(elong[n]) for n, _ in PLANETAS]}
                 for (d, lon, elong, m) in dias],
        "alinhamentos": lista,
        "desfiles": desfiles,
    }
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("gravado", SAIDA, os.path.getsize(SAIDA), "bytes,", len(dias), "dias,", len(lista), "alinhamentos")


if __name__ == "__main__":
    main()
