#!/home/ricardo/.venv-astro/bin/python
# -*- coding: utf-8 -*-
"""Astrologia védica — os dados da calculadora de genialtarot.com/astrologia-vedica (02/11/2026).

Tudo CALCULADO com o Swiss Ephemeris. Para 1929-12-01 a 2031-01-31 grava em vedica-dados.json o instante (UTC) em que
o Sol entra em cada signo:
  t: zodíaco TROPICAL (o ocidental: 0° Carneiro/Áries = equinócio de março)
  s: zodíaco SIDERAL com o ayanamsa de LAHIRI (swe.SIDM_LAHIRI), o mais usado na astrologia védica
«ay»: o ayanamsa de Lahiri a 1 de janeiro de cada ano desde «ay0» (milésimos de grau), só para mostrar.
Cada lista tem pares [segundos desde 1970-01-01 UTC, signo 0–11], por ordem. A página só consulta a tabela:
o signo é o da última entrada antes do instante de nascimento.

    ~/.venv-astro/bin/python ~/site-genialtarot/vedica-calc.py            → grava o JSON
    ~/.venv-astro/bin/python ~/site-genialtarot/vedica-calc.py --conferir → 3 datas conferidas directamente com swe
"""
import sys, os, json, datetime
import swisseph as swe

EFEMERIDES = "/home/ricardo/.efemerides-swisseph"
if os.path.isdir(EFEMERIDES): swe.set_ephe_path(EFEMERIDES)
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vedica-dados.json")
INICIO = swe.julday(1929, 12, 1, 0)
FIM = swe.julday(2031, 1, 31, 0)
EPOCA = swe.julday(1970, 1, 1, 0)
swe.set_sid_mode(swe.SIDM_LAHIRI)
TROP = swe.FLG_SWIEPH
SID = swe.FLG_SWIEPH | swe.FLG_SIDEREAL


def lon(j, fl): return swe.calc_ut(j, swe.SUN, fl)[0][0]


def ingressos(fl):
    """Instantes em que a longitude do Sol cruza um múltiplo de 30° (bissecção até < 1 segundo)."""
    out, j, passo = [], INICIO, 0.5
    s0 = int(lon(j, fl) // 30)
    while j < FIM:
        j2 = j + passo
        s1 = int(lon(j2, fl) // 30)
        if s1 != s0:
            a, b = j, j2
            while b - a > 1e-5:
                m = (a + b) / 2
                if int(lon(m, fl) // 30) == s0: a = m
                else: b = m
            out.append([round((b - EPOCA) * 86400), s1])
            s0 = s1
        j = j2
    return out


def utc(segundos): return datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=segundos)


def conferir():
    NOMES = ["Carneiro", "Touro", "Gémeos", "Caranguejo", "Leão", "Virgem", "Balança", "Escorpião", "Sagitário",
             "Capricórnio", "Aquário", "Peixes"]
    for (a, m, d, h) in [(1985, 7, 10, 12.0), (1962, 3, 25, 6.5), (2000, 1, 1, 12.0), (2010, 12, 15, 0.0)]:
        j = swe.julday(a, m, d, h)
        t, s = lon(j, TROP), lon(j, SID)
        print(f"{a}-{m:02}-{d:02} {h:05.2f} UTC  tropical {t:7.3f}° = {NOMES[int(t // 30)]:11}  "
              f"sideral {s:7.3f}° = {NOMES[int(s // 30)]:11}  ayanamsa {swe.get_ayanamsa_ut(j):.4f}°")


def main():
    if "--conferir" in sys.argv: return conferir()
    t, s = ingressos(TROP), ingressos(SID)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump({"gerado": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                   "ayanamsa": "Lahiri", "unidade": "segundos UTC desde 1970-01-01",
                   "ay0": 1930, "ay": [round(swe.get_ayanamsa_ut(swe.julday(a, 1, 1, 0)) * 1000) for a in range(1930, 2032)],
                   "t": t, "s": s}, f, separators=(",", ":"))
    print("gravado", SAIDA, os.path.getsize(SAIDA), "bytes;", len(t), "entradas tropicais,", len(s), "siderais")
    print("primeira tropical", utc(t[0][0]), t[0][1], "| primeira sideral", utc(s[0][0]), s[0][1])


if __name__ == "__main__":
    main()
