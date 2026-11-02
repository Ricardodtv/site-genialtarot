#!/home/ricardo/.venv-astro/bin/python
# -*- coding: utf-8 -*-
"""Luas Azuis de 2000 a 2045 → lua-azul-dados.js (02/11/2026, pedido dele: «lua azul» a subir no Google Trends; «tem de se
atualizar automaticamente»). A página /lua-azul lê isto e mostra sozinha a próxima a partir do dia de hoje; o
site-ceu-rolante.sh volta a gerar todos os meses (a janela anda com o ano).

Duas definições, as duas usadas:
  · mensal  — a 2.ª Lua Cheia no mesmo mês do calendário. Depende do fuso: calculada para Portugal e para o Brasil.
  · sazonal — a 3.ª de 4 Luas Cheias numa estação astronómica (equinócio → solstício). Não depende do fuso.
Swiss Ephemeris: Luas Cheias exatas e entradas do Sol em 0° de Carneiro/Caranguejo/Balança/Capricórnio.
"""
import json, datetime, os
from zoneinfo import ZoneInfo
import swisseph as swe
EF = "/home/ricardo/.efemerides-swisseph"
if os.path.isdir(EF): swe.set_ephe_path(EF)
AQUI = os.path.dirname(os.path.abspath(__file__))
ano = datetime.date.today().year
A0, A1 = min(2000, ano - 26), ano + 19
FUSOS = {"pt": ZoneInfo("Europe/Lisbon"), "br": ZoneInfo("America/Sao_Paulo")}

def lon(j, c): return swe.calc_ut(j, c)[0][0]
def bis(f, a, b):
    for _ in range(50):
        m = (a + b) / 2
        if f(a) * f(m) <= 0: b = m
        else: a = m
    return (a + b) / 2
w = lambda x: (x + 180) % 360 - 180
def dt(j):
    y, m, d, h = swe.revjul(j)
    return datetime.datetime(y, m, d, tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=h)
ms = lambda j: round(dt(j).timestamp() * 1000)

# Luas Cheias (elongação 180°) e entradas do Sol nos pontos cardeais
cheias, estacoes = [], []
j, fim = swe.julday(A0 - 1, 12, 1), swe.julday(A1 + 1, 1, 31)
passo = 0.5
while j < fim:
    k = j + passo
    g = lambda x: w(lon(x, swe.MOON) - lon(x, swe.SUN) - 180)
    if g(j) < 0 <= g(k) and abs(g(j)) < 20: cheias.append(bis(g, j, k))
    for alvo in (0, 90, 180, 270):
        h = lambda x, a=alvo: w(lon(x, swe.SUN) - a)
        if h(j) < 0 <= h(k) and abs(h(j)) < 5: estacoes.append((bis(h, j, k), alvo))
    j = k

mensal = {}
for f, tz in FUSOS.items():
    l, porMes = [], {}
    for c in cheias:
        d = dt(c).astimezone(tz)
        porMes.setdefault((d.year, d.month), []).append(c)
    for (y, m), cs in sorted(porMes.items()):
        if len(cs) >= 2 and A0 <= y <= A1: l.append(ms(cs[1]))
    mensal[f] = l
sazonal = []
estacoes.sort()
for (e0, _), (e1, _) in zip(estacoes, estacoes[1:]):
    cs = [c for c in cheias if e0 <= c < e1]
    if len(cs) == 4 and A0 <= dt(cs[2]).year <= A1: sazonal.append(ms(cs[2]))
o = {"gerado": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "motor": f"Swiss Ephemeris {swe.version}",
     "anos": [A0, A1], "mensal": mensal, "sazonal": sazonal}
open(os.path.join(AQUI, "lua-azul-dados.js"), "w").write("// Gerado por lua-azul-gerar.py (Swiss Ephemeris). Não editar à mão.\nwindow.LUA_AZUL = "
                                                          + json.dumps(o, separators=(",", ":")) + ";\n")
fmt = lambda t, tz: datetime.datetime.fromtimestamp(t / 1000, tz).strftime("%d/%m/%Y %H:%M")
print("mensal PT:", [fmt(t, FUSOS["pt"]) for t in mensal["pt"] if t > 1.76e12][:5])
print("mensal BR:", [fmt(t, FUSOS["br"]) for t in mensal["br"] if t > 1.76e12][:5])
print("sazonal:", [fmt(t, FUSOS["pt"]) for t in sazonal if t > 1.76e12][:5], "| total", len(mensal["pt"]), len(mensal["br"]), len(sazonal))
