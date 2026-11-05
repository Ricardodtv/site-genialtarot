#!/usr/bin/env python3
"""Ficha do Consultório Virtual (pedido dele, 05/11/2026): nome e nascimento escritos por baixo da conversa, no painel.
A ficha é criada em Central Tarot/Clientes quando ele FECHA a conversa, a seguir à numeração que lá existe.
Estes dados ficam no cerebro: nunca passam pelo worker. Quem correr isto só vê códigos.
Cofre fechado: fica pendente em ~/.consultorio-fichas.json (600) e o vigia acaba o trabalho quando o cofre abrir.
Nome «teste» não cria ficha nem gasta código."""
import datetime, fcntl, glob, io, json, os, re, subprocess, unicodedata
C = os.environ.get("CONSULTORIO_CLIENTES", "/media/veracrypt23/ObsidianS/CentralS/Central Tarot/Clientes")
LIV = os.environ.get("CONSULTORIO_LIVRO", "/media/veracrypt23/Codigos/livro.tsv")
EST = os.environ.get("CONSULTORIO_FICHAS", os.path.expanduser("~/.consultorio-fichas.json"))
NOTIFY = os.environ.get("CONSULTORIO_NOTIFY", os.path.expanduser("~/.claude/telegram-service/notify.sh"))
def _ler():
    try: return json.load(open(EST, encoding="utf-8"))
    except (OSError, ValueError): return {}
def _grava(e):
    t = EST + ".tmp"; json.dump(e, open(t, "w", encoding="utf-8"), ensure_ascii=False); os.chmod(t, 0o600); os.replace(t, EST)
def _normal(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()).strip().lower()
def _digitos(s):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    if m: return m.group(3) + m.group(2) + m.group(1)
    m = re.search(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})", s or "")
    return "%02d%02d%s" % (int(m.group(1)), int(m.group(2)), m.group(3)) if m else ""
def _aviso(t):
    subprocess.run(["bash", NOTIFY, t], timeout=60)
def _tranca():
    l = open(EST + ".lock", "w"); fcntl.flock(l, fcntl.LOCK_EX); return l
def ver(c):
    x = _ler().get(c, {}); return {"nome": x.get("nome", ""), "nasc": x.get("nasc", ""), "codigo": x.get("codigo", ""), "pendente": bool(x.get("pendente"))}
def guardar(c, nome, nasc):
    nome = re.sub(r"\s+", " ", str(nome or "")).strip()[:80]; nasc = str(nasc or "").strip()[:10]
    if nasc and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", nasc): return {"ok": False, "erro": "Data inválida."}
    with _tranca():
        e = _ler(); x = e.setdefault(c, {}); x.update(nome=nome, nasc=nasc); _grava(e)
    return {"ok": True, **ver(c)}
def ao_fechar(c):
    """Chamado quando ele fecha a conversa. Sem nome escrito, não há ficha."""
    with _tranca():
        e = _ler(); x = e.get(c)
        if not x or not x.get("nome"): return {"ok": True, "codigo": ""}
        x["pendente"] = True; _grava(e)
    return processar(c)
def _fichas():
    cod_max, por = 0, []
    for f in glob.glob(C + "/*.md"):
        t = io.open(f, encoding="utf-8", errors="replace").read()
        m = re.search(r"(?m)^\s*(?:codigo:|\*\*Código:\*\*)\s*C-(\d{3})\s*$", t)
        if m: cod_max = max(cod_max, int(m.group(1)))
        n = re.search(r"(?m)^nome:\s*(.+)$", t); d = re.search(r"(?m)^Data Nascimento:[ \t]*(.*)$", t)
        por.append((f, "C-" + m.group(1) if m else "", _normal(n.group(1)) if n else "", _digitos(d.group(1)) if d else ""))
    if os.path.exists(LIV):
        for l in io.open(LIV, encoding="utf-8"):
            m = re.match(r"C-(\d{3})\t", l)
            if m: cod_max = max(cod_max, int(m.group(1)))
    return cod_max, por
def _hist(f, linha, nasc=""):
    t = io.open(f, encoding="utf-8", errors="replace").read()
    if linha in t: return
    r = "# 🎯 Histórico de Consultas\n"
    t = t.replace(r + "\n", r + "\n" + linha + "\n", 1) if r + "\n" in t else t.rstrip() + "\n\n" + r + "\n" + linha + "\n"
    if nasc: t = re.sub(r"(?m)^Data Nascimento:[ \t]*$", "Data Nascimento: " + nasc, t, count=1)
    io.open(f, "w", encoding="utf-8").write(t)
def _ficha(cod, nome, nasc, agora):
    return f"""---
tags:
  - Consultantes
  - Consultas
  - clientes
  - tarot
codigo: {cod}
nome: {nome}
email: 
Contato: 
Data Nascimento: {nasc}
Signo: 
Cidade: 
País: 
Area: 
Novidades: 
Preço Consulta: 
Tempo Consulta: 
Captura ?: 
Created: {agora}
Updated: {agora}
---

> 🚪 **Ficha criada no Consultório Virtual** a {agora}.

# 🎯 Objetivos da Consulta



# ✍️ Notas da Consulta



# 🎯 Histórico de Consultas

- {agora[:10]} — conversa no Consultório Virtual

# 📎 Anexos

"""
def processar(c=None):
    """Trata as fichas pendentes. Devolve o resultado da conversa c, se pedida."""
    with _tranca():
        e = _ler(); res = {"ok": True, "codigo": e.get(c, {}).get("codigo", "") if c else ""}
        pend = [k for k, x in e.items() if x.get("pendente")]
        if not pend: return res
        if not os.path.isdir(C):
            if c in pend: res.update(pendente=True); _aviso("🚪 Consultório: o cofre está fechado. A ficha fica à espera e crio-a quando o cofre abrir.")
            return res
        for k in pend:
            x = e[k]; agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M"); linha = f"- {agora[:10]} — conversa no Consultório Virtual"
            nasc = "/".join(reversed(x["nasc"].split("-"))) if x.get("nasc") else ""
            if _normal(x["nome"]) in ("teste", "test"):
                x.update(pendente=False, nome="", nasc=""); _aviso("🧪 Consultório: nome «teste», não criei ficha nem gastei código."); continue
            cod_max, fichas = _fichas()
            f = next((p for p in fichas if p[1] and p[1] == x.get("codigo")), None)
            if not f:
                iguais = [p for p in fichas if p[2] == _normal(x["nome"])]
                d = _digitos(nasc)
                f = next((p for p in iguais if d and p[3] == d), None) or next((p for p in iguais if not d or not p[3]), None)
                outra = bool(iguais) and not f
            else: outra = False
            if f:
                _hist(f[0], linha, nasc); x["codigo"] = f[1]; _aviso(f"🚪 Consultório: acrescentei a conversa à ficha da *{f[1]}*.")
            else:
                n = cod_max + 1
                while glob.glob(C + "/C-%03d *.md" % n): n += 1
                cod = "C-%03d" % n; nome = re.sub(r'[/\\:*?"<>|]', "-", x["nome"]).strip() or "Consultório " + cod
                dest = os.path.join(C, f"{cod} {nome}.md"); io.open(dest, "x", encoding="utf-8").write(_ficha(cod, x["nome"], nasc, agora)); os.chmod(dest, 0o600)
                with io.open(LIV, "a", encoding="utf-8") as g: g.write("%s\t%s\t%s\n" % (cod, os.path.basename(dest), datetime.date.today()))
                x["codigo"] = cod; _aviso(f"🌳 Ficha nova: *{cod}*, do Consultório Virtual." + (" Atenção: há outra ficha com o mesmo nome e data diferente." if outra else ""))
            x["pendente"] = False
            if k == c: res["codigo"] = x["codigo"]
            _grava(e)
        _grava(e); return res
