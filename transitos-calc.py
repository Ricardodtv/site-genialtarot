#!/home/ricardo/.venv-astro/bin/python
"""Rascunho 03/11/2026: entradas/saídas de signo dos planetas lentos e nodos (Swiss Ephemeris), em hora de Lisboa.
Também as estações (R/D) dentro das janelas e os aspectos exactos entre lentos. Saída: transitos-datas.json"""
import swisseph as swe, json, datetime, os
from zoneinfo import ZoneInfo
swe.set_ephe_path("/home/ricardo/.efemerides-swisseph")
LX = ZoneInfo("Europe/Lisbon")
SIG = ["Carneiro","Touro","Gémeos","Caranguejo","Leão","Virgem","Balança","Escorpião","Sagitário","Capricórnio","Aquário","Peixes"]
P = {"jupiter": swe.JUPITER, "saturno": swe.SATURN, "urano": swe.URANUS, "neptuno": swe.NEPTUNE, "plutao": swe.PLUTO, "nodo_verdadeiro": swe.TRUE_NODE, "nodo_medio": swe.MEAN_NODE}
lon = lambda j, c: swe.calc_ut(j, c, swe.FLG_SPEED)[0][0]
vel = lambda j, c: swe.calc_ut(j, c, swe.FLG_SPEED)[0][3]
def lx(j):
    a, m, d, h = swe.revjul(j); u = datetime.datetime(a, m, d, tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=h)
    return u.astimezone(LX).strftime("%Y-%m-%d %H:%M")
def bis(f, a, b):
    fa = f(a)
    for _ in range(60):
        m = (a + b) / 2; fm = f(m)
        if (fm > 0) == (fa > 0): a, fa = m, fm
        else: b = m
    return (a + b) / 2
J0, J1 = swe.julday(2018, 1, 1), swe.julday(2045, 1, 1)
out = {"motor": "Swiss Ephemeris " + swe.version, "fuso": "Europe/Lisbon", "ingressos": {}, "estacoes": {}, "aspectos": []}
for n, c in P.items():
    ev = []; j = J0; s = int(lon(j, c) // 30); passo = 0.25
    while j < J1:
        j2 = j + passo; s2 = int(lon(j2, c) // 30)
        if s2 != s:
            b = s * 30 if (s2 - s) % 12 == 11 else s2 * 30   # fronteira cruzada
            jt = bis(lambda x: ((lon(x, c) - b + 180) % 360) - 180, j, j2)
            ev.append({"data": lx(jt), "de": SIG[s], "para": SIG[s2], "sentido": "retro" if (s2 - s) % 12 == 11 else "directo"})
            s = s2
        j = j2
    out["ingressos"][n] = ev
    if not n.startswith("nodo"):
        st = []; j = J0; v = vel(j, c)
        while j < J1:
            j2 = j + 1; v2 = vel(j2, c)
            if (v > 0) != (v2 > 0):
                jt = bis(lambda x: vel(x, c), j, j2); L = lon(jt, c)
                st.append({"data": lx(jt), "tipo": "fica retrógrado" if v > 0 else "fica directo", "pos": f"{int(L%30)}°{int((L%1)*60):02d}' {SIG[int(L//30)]}"})
            j, v = j2, v2
        out["estacoes"][n] = st
# aspectos exactos entre lentos 2024-2040
LENT = ["jupiter", "saturno", "urano", "neptuno", "plutao"]
ASP = {0: "conjunção", 60: "sextil", 90: "quadratura", 120: "trígono", 180: "oposição"}
for i in range(5):
    for k in range(i + 1, 5):
        a, b = P[LENT[i]], P[LENT[k]]
        for ang, nome in ASP.items():
            f = lambda x: ((lon(x, a) - lon(x, b) - ang + 180) % 360) - 180
            g = lambda x: ((lon(x, a) - lon(x, b) + ang + 180) % 360) - 180
            for fn in ([f] if ang in (0, 180) else [f, g]):
                j = swe.julday(2024, 1, 1); y = fn(j)
                while j < swe.julday(2040, 1, 1):
                    j2 = j + 2; y2 = fn(j2)
                    if (y > 0) != (y2 > 0) and abs(y - y2) < 30:
                        jt = bis(fn, j, j2); L = lon(jt, a); L2 = lon(jt, b)
                        out["aspectos"].append({"data": lx(jt), "aspecto": f"{LENT[i]} {nome} {LENT[k]}", "pos": f"{int(L%30)}°{int((L%1)*60):02d}' {SIG[int(L//30)]} / {int(L2%30)}°{int((L2%1)*60):02d}' {SIG[int(L2//30)]}"})
                    j, y = j2, y2
out["aspectos"].sort(key=lambda x: x["data"])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "transitos-datas.json"), "w"), ensure_ascii=False, indent=1)
for n, ev in out["ingressos"].items():
    print("==", n)
    for e in ev:
        if "2019" < e["data"] < "2041": print("  ", e["data"], e["de"], "->", e["para"], e["sentido"])
