#!/usr/bin/env python3
"""Vigia do Consultório Virtual (05/11/2026): avisa no Telegram quando alguém entra na sala de espera, e volta a avisar uma vez
se ainda lá estiver ao fim de VOLTA_S. Pergunta à ponte local (site-painel), por isso não precisa de chave nenhuma.
Sem ligações em curso quase não gasta: pergunta de PAUSA_S em PAUSA_S; a criação de uma ligação no painel acorda-o.
Calado das 03:00 às 07:00 não é daqui: o notify.sh guarda o aviso e manda-o às 07:00."""
import json, os, subprocess, time, urllib.request
PONTE = os.environ.get("CONSULTORIO_PONTE", "http://100.100.77.18:8768")
NOTIFY = os.environ.get("CONSULTORIO_NOTIFY", os.path.expanduser("~/.claude/telegram-service/notify.sh"))
ESTADO = os.environ.get("CONSULTORIO_ESTADO", os.path.expanduser("~/.consultorio-vigia.json"))
ACORDAR = os.environ.get("CONSULTORIO_ACORDAR", os.path.expanduser("~/site-painel/consultorio-acordar"))
ATIVO_S, PAUSA_S, VOLTA_S, TICK_S = 20, 120, 300, 5
def ler():
    try: return json.load(open(ESTADO))
    except Exception: return {}
def gravar(e):
    t = ESTADO + ".tmp"; json.dump(e, open(t, "w")); os.chmod(t, 0o600); os.replace(t, ESTADO)
def avisa(txt):
    try: subprocess.run(["bash", NOTIFY, txt], timeout=30, check=False)
    except Exception as x: print("aviso falhou:", x, flush=True)
def ronda(e):
    r = json.load(urllib.request.urlopen(PONTE + "/api/consultorio/vigia", timeout=30))
    if not r.get("ok"): return 0
    agora = time.time(); na_sala = set()
    for p in r.get("espera", []):
        c = p["codigo"]; na_sala.add(c); nome = p.get("etiqueta") or "sem etiqueta"
        v = e.get(c)
        if v is None:
            avisa(f"🚪 Alguém entrou na sala de espera do Consultório Virtual ({nome}). Atender: HA → Site → Consultório.")
            e[c] = {"t": agora, "volta": False}; gravar(e)
        elif not v["volta"] and agora - v["t"] > VOLTA_S and p.get("online"):
            avisa(f"🚪 Continua alguém à espera na sala do Consultório Virtual ({nome}), há mais de {VOLTA_S // 60} minutos.")
            v["volta"] = True; gravar(e)
    for c in [c for c in e if c not in na_sala]: e.pop(c); gravar(e)   # já foi atendida, fechada ou expirou
    return r.get("ativos", 0)
def principal():
    e = ler(); proxima = 0; ativos = 0; visto = 0
    while True:
        try: m = os.path.getmtime(ACORDAR)
        except OSError: m = 0
        if m > visto: visto = m; proxima = 0
        if time.time() >= proxima:
            try: ativos = ronda(e)
            except Exception as x: print("ronda falhou:", str(x)[:120], flush=True); ativos = 0   # a ponte em baixo ou o cofre fechado: tenta depois
            proxima = time.time() + (ATIVO_S if ativos else PAUSA_S)
        time.sleep(TICK_S)
if __name__ == "__main__": principal()
