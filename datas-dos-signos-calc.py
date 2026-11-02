#!/home/ricardo/.venv-astro/bin/python
# -*- coding: utf-8 -*-
"""Datas dos Signos — as entradas EXATAS do Sol em cada signo em 2026 e 2027 (02/11/2026).

Para a página genialtarot.com/datas-dos-signos. Calculado com o Swiss Ephemeris (zodíaco tropical, longitude
geocêntrica aparente do Sol), pelo mesmo método do ~/horoscopo_site.py: passo de 1 dia até o signo mudar e
depois bissecção até ao segundo. As horas saem em Lisboa e em Brasília (America/Sao_Paulo).

    ~/.venv-astro/bin/python ~/site-genialtarot/datas-dos-signos-calc.py          → tabela em texto
    ~/.venv-astro/bin/python ~/site-genialtarot/datas-dos-signos-calc.py --json   → JSON (o que foi para o HTML)
"""
import sys, os, json, datetime
from zoneinfo import ZoneInfo
import swisseph as swe

EFEMERIDES = "/home/ricardo/.efemerides-swisseph"
if os.path.isdir(EFEMERIDES): swe.set_ephe_path(EFEMERIDES)
UTC = datetime.timezone.utc
LX, BR = ZoneInfo("Europe/Lisbon"), ZoneInfo("America/Sao_Paulo")
SIGNOS = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança",
          "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]


def jd(t):
    u = t.astimezone(UTC)
    return swe.julday(u.year, u.month, u.day, u.hour + u.minute / 60 + u.second / 3600)


def sol(t):
    r, flag = swe.calc_ut(jd(t), swe.SUN)
    return r[0] % 360, flag


def w180(x): return (x + 180) % 360 - 180


def bissectar(f, a, b, n=50):
    fa = f(a)
    for _ in range(n):
        m = a + (b - a) / 2
        fm = f(m)
        if (fm < 0) == (fa < 0): a, fa = m, fm
        else: b = m
    return a + (b - a) / 2


def ingressos(ano):
    t = datetime.datetime(ano, 1, 1, tzinfo=UTC) - datetime.timedelta(days=1)
    fim = datetime.datetime(ano + 1, 1, 1, tzinfo=UTC) + datetime.timedelta(days=1)
    out, passo = [], datetime.timedelta(days=1)
    while t < fim:
        u = t + passo
        sa, sb = int(sol(t)[0] // 30), int(sol(u)[0] // 30)
        if sa != sb:
            x = bissectar(lambda y: w180(sol(y)[0] - sb * 30), t, u)
            if x.year == ano:
                out.append((sb, x))
        t = u
    return out


if __name__ == "__main__":
    flag = sol(datetime.datetime(2026, 1, 1, tzinfo=UTC))[1]
    fonte = "ficheiros Swiss Ephemeris" if flag & swe.FLG_SWIEPH else "Moshier (analítico, sem ficheiros sepl)"
    dados = {}
    for ano in (2026, 2027):
        dados[ano] = []
        for s, x in sorted(ingressos(ano), key=lambda e: e[1]):
            m = (x + datetime.timedelta(seconds=30)).replace(second=0, microsecond=0)   # arredonda ao minuto
            lx, br = m.astimezone(LX), m.astimezone(BR)
            dados[ano].append({"s": s, "signo": SIGNOS[s], "utc": x.strftime("%Y-%m-%dT%H:%M:%SZ"),
                               "lisboa": lx.strftime("%d/%m %H:%M"), "brasilia": br.strftime("%d/%m %H:%M")})
    if "--json" in sys.argv:
        print(json.dumps(dados, ensure_ascii=False, indent=1))
    else:
        print("Efemérides:", fonte, "· swisseph", swe.version)
        for ano, lista in dados.items():
            print(f"\n{ano}")
            for e in lista:
                print(f"  {e['signo']:<12} UTC {e['utc']}   Lisboa {e['lisboa']}   Brasília {e['brasilia']}")
