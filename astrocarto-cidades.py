# Gera astrocarto-cidades.js — as cidades conhecidas que a Astrocartografia procura perto das linhas (04/11/2026).
# Coordenadas tiradas do cidades.json do site (GeoNames, CC BY 4.0); só o nome em português é escrito aqui.
import json, os
raiz = os.path.dirname(os.path.abspath(__file__))
LISTA = {
 "PT": "Lisboa Porto Braga Coimbra Leiria Setúbal Funchal Viseu Aveiro Faro Évora Guimarães Ponta_Delgada Bragança Castelo_Branco Viana_do_Castelo",
 "BR": "São_Paulo Rio_de_Janeiro Belo_Horizonte Salvador Fortaleza Manaus Brasília Curitiba Recife Goiânia Belém Porto_Alegre Maceió Natal Florianópolis Vitória João_Pessoa Campo_Grande Cuiabá Teresina São_Luís Aracaju Porto_Velho Boa_Vista Macapá Palmas Rio_Branco Campinas Londrina Uberlândia Foz_do_Iguaçu",
 "CH": "Zürich:Zurique Geneva:Genebra Basel:Basileia Lausanne Bern:Berna Lugano Luzern:Lucerna",
 "FR": "Paris Marseille:Marselha Lyon:Lyon Toulouse Nice Nantes Strasbourg:Estrasburgo Bordeaux Montpellier Lille",
 "LU": "Luxembourg:Luxemburgo",
 "GB": "London:Londres Manchester Birmingham Edinburgh:Edimburgo Glasgow Liverpool Bristol Belfast",
 "IE": "Dublin",
 "DE": "Berlin:Berlim Hamburg:Hamburgo Munich:Munique Köln:Colónia Frankfurt_am_Main:Frankfurt Düsseldorf Stuttgart",
 "BE": "Brussels:Bruxelas", "NL": "Amsterdam:Amesterdão", "AT": "Vienna:Viena",
 "ES": "Madrid Barcelona Valencia:Valência Sevilla:Sevilha Málaga Bilbao Vigo Las_Palmas_de_Gran_Canaria:Las_Palmas",
 "IT": "Rome:Roma Milan:Milão Naples:Nápoles Florence:Florença Venice:Veneza Turin:Turim",
 "US": "New_York_City:Nova_Iorque Los_Angeles Chicago Miami Orlando Boston Houston San_Francisco:São_Francisco Las_Vegas Washington Newark Seattle Denver Atlanta Honolulu",
 "CA": "Toronto Montréal Vancouver Ottawa Québec Calgary",
 "MX": "Mexico_City:Cidade_do_México Cancún", "AR": "Buenos_Aires", "CL": "Santiago", "PE": "Lima", "CO": "Bogotá", "UY": "Montevideo:Montevidéu", "PY": "Asunción:Assunção",
 "AO": "Luanda", "MZ": "Maputo", "CV": "Praia", "ZA": "Cape_Town:Cidade_do_Cabo Johannesburg:Joanesburgo", "MA": "Marrakesh:Marraquexe", "EG": "Cairo",
 "AE": "Dubai", "JP": "Tokyo:Tóquio", "AU": "Sydney Melbourne", "IN": "Mumbai New_Delhi:Nova_Deli", "TH": "Bangkok:Banguecoque", "GR": "Athens:Atenas", "TR": "Istanbul:Istambul",
 "IL": "Jerusalem:Jerusalém", "RU": "Moscow:Moscovo", "SE": "Stockholm:Estocolmo", "NO": "Oslo", "DK": "Copenhagen:Copenhaga", "PL": "Warsaw:Varsóvia", "CZ": "Prague:Praga",
 "SG": "Singapore:Singapura", "CN": "Shanghai:Xangai Beijing:Pequim", "NZ": "Auckland", "IS": "Reykjavík:Reiquiavique", "MO": "Macau", "TL": "Dili", "ST": "São_Tomé", "GW": "Bissau",
}
d = json.load(open(os.path.join(raiz, "cidades.json")))
prim = {}
for c in d["cidades"]:
    prim.setdefault((c[2], c[0]), c)
out, falta = [], []
for cc, s in LISTA.items():
    for item in s.split():
        geo, _, pt = item.partition(":")
        geo = geo.replace("_", " "); pt = (pt or geo).replace("_", " ")
        c = prim.get((cc, geo))
        if not c: falta.append(cc + ":" + geo); continue
        out.append([pt, cc, c[3], c[4]])
PT_NOMES = {"AT": "Áustria", "MA": "Marrocos", "EG": "Egipto", "AE": "Emirados Árabes Unidos", "AU": "Austrália", "IN": "Índia", "TH": "Tailândia",
            "GR": "Grécia", "TR": "Turquia", "RU": "Rússia", "SE": "Suécia", "NO": "Noruega", "DK": "Dinamarca", "PL": "Polónia", "CZ": "Chéquia",
            "SG": "Singapura", "NZ": "Nova Zelândia", "IS": "Islândia", "MO": "China", "TL": "Timor-Leste"}
paises = {cc: PT_NOMES.get(cc) or d["paises"].get(cc, cc) for cc in LISTA}
with open(os.path.join(raiz, "astrocarto-cidades.js"), "w") as f:
    f.write("/* Cidades conhecidas para a Astrocartografia — gerado por astrocarto-cidades.py (04/11/2026). Coordenadas: GeoNames (CC BY 4.0). */\n")
    f.write("window.CIDADES_CARTO = " + json.dumps({"paises": paises, "cidades": out}, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(out), "cidades; em falta:", falta)
