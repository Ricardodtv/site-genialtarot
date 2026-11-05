#!/usr/bin/env python3
"""Consultório Virtual: as rotas da ponte (05/11/2026). Vai para ~/site-painel/ ao lado do servidor.py, que só as chama.
Tudo o que aqui passa fala com a classe Consultorio do worker com a mesma X-Chave (STATS_KEY) do resto do painel; a chave nunca
vai ao navegador. Sem isto ligado, nada muda no painel.

O áudio dele: o painel do HA é http, e num endereço http o navegador não dá microfone. Daí os dois caminhos:
 - «Abrir com microfone»: abre https://genialtarot.com/consultorio/<código>#m=<mtoken>, a mesma conversa do lado dele, com microfone.
 - enviar um ficheiro de áudio pelo painel. Se vier em webm, passa a m4a com o ffmpeg daqui, porque um iPhone antigo não toca webm."""
import json, os, subprocess, tempfile, time, urllib.error, urllib.parse, urllib.request
CODIGO_LETRAS = set("abcdefghjkmnpqrstuvwxyz23456789")
ACORDAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "consultorio-acordar")   # o vigia passa a olhar mais depressa
AUDIO_MAX = 3 << 20
TIPOS = {"audio/mp4", "audio/webm", "audio/ogg", "audio/aac", "audio/mpeg", "audio/x-m4a", "audio/mp3"}
pede = chave = SITE = UA = None
try: import consultorio_ficha as ficha   # nome e nascimento ficam no cerebro: nunca passam pelo worker nem pelo pede()
except Exception: ficha = None
_cache = {}
def liga(pede_, chave_, site, ua):
    global pede, chave, SITE, UA
    pede, chave, SITE, UA = pede_, chave_, site, ua
def codigo(c):
    c = str(c or "")
    return c if len(c) == 20 and set(c) <= CODIGO_LETRAS else ""
def binario(caminho, corpo=None, tipo=None):
    k = chave()
    if not k: return 503, b"", ""
    h = {"User-Agent": UA, "X-Chave": k}
    if tipo: h["Content-Type"] = tipo
    try:
        with urllib.request.urlopen(urllib.request.Request(SITE + caminho, data=corpo, headers=h), timeout=40) as r:
            return r.status, r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e: return e.code, e.read(), e.headers.get("Content-Type", "")
    except Exception: return 502, b"", ""
def para_m4a(dados, sufixo):
    """webm/ogg → m4a. Se falhar, segue o original: é melhor um áudio que nem todos tocam do que áudio nenhum."""
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a" + sufixo), os.path.join(d, "b.m4a")
        open(a, "wb").write(dados)
        try:
            r = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", a, "-vn", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", b], capture_output=True, timeout=60)
            if r.returncode == 0 and os.path.getsize(b) > 0: return open(b, "rb").read(), "audio/mp4"
        except Exception: pass
    return None, None
def get(h, u, q):
    c = codigo(q.get("c")); via = u.path.replace("/api/consultorio/", "")
    if via == "lista":
        agora = time.time()   # vários separadores abertos fazem uma só pergunta (ver a nota da quota de 03/11)
        if "lista" not in _cache or agora - _cache["lista"][0] > 5: _cache["lista"] = (agora, pede("/api/consultorio/lista"))
        st, o = _cache["lista"][1]
        for x in o.get("consultas", []): x["link"] = SITE + "/consultorio/" + x["codigo"]
        return h.responde(st, o)
    if via == "vigia": return h.responde(*pede("/api/consultorio/vigia" + ("?f=1" if q.get("f") else "")))
    if via == "ficha" and c: return h.responde(200, ficha.ver(c) if ficha else {"nome": "", "nasc": "", "codigo": "", "pendente": False})
    if via == "conversa" and c: return h.responde(*pede("/api/consultorio/estado?c=%s&desde=%d" % (c, int(q.get("desde") or 0))))
    if via == "audio" and c:
        st, b, tipo = binario("/api/consultorio/audio?c=%s&id=%d" % (c, int(q.get("id") or 0)))
        h.send_response(st); h.send_header("Content-Type", tipo or "application/octet-stream"); h.send_header("Content-Length", str(len(b))); h.end_headers(); h.wfile.write(b); return
    if via == "anexo" and c:
        st, b, tipo = binario("/api/consultorio/anexo?c=%s&id=%d" % (c, int(q.get("id") or 0)))
        h.send_response(st); h.send_header("Content-Type", tipo or "application/octet-stream"); h.send_header("Content-Length", str(len(b))); h.send_header("X-Content-Type-Options", "nosniff")
        h.send_header("Content-Security-Policy", "sandbox; default-src 'none'"); h.send_header("Content-Disposition", "inline" if tipo.startswith("image/") else "attachment"); h.end_headers(); h.wfile.write(b); return
    return h.responde(404, {"ok": False})
def post(h, u):
    q = dict(urllib.parse.parse_qsl(u.query)); via = u.path.replace("/api/consultorio/", "")
    n = int(h.headers.get("Content-Length") or 0)
    if via == "audio":
        c = codigo(q.get("c")); tipo = str(h.headers.get("Content-Type") or "").split(";")[0].strip().lower().replace("video/", "audio/")   # um .webm do disco chega como video/webm
        if n > AUDIO_MAX + 1024: h.rfile.read(n); return h.responde(413, {"ok": False, "erro": "O áudio não pode passar de 3 MB."})
        dados = h.rfile.read(n)
        if not c or tipo not in TIPOS: return h.responde(415, {"ok": False, "erro": "Formato não aceite."})
        if tipo in ("audio/webm", "audio/ogg"):
            novo, t = para_m4a(dados, ".webm" if tipo == "audio/webm" else ".ogg")
            if novo: dados, tipo = novo, t
        tipo = {"audio/x-m4a": "audio/mp4", "audio/mp3": "audio/mpeg"}.get(tipo, tipo)
        st, b, _ = binario("/api/consultorio/audio?c=%s&dur=%.1f" % (c, min(93, float(q.get("dur") or 0))), dados, tipo)
        try: o = json.loads(b or b"{}")
        except Exception: o = {"ok": False}
        return h.responde(st, o)
    if via == "anexo":
        c = codigo(q.get("c"))
        if n > AUDIO_MAX + 1024: h.rfile.read(n); return h.responde(413, {"ok": False, "erro": "O ficheiro não pode passar de 3 MB."})
        dados = h.rfile.read(n)
        if not c: return h.responde(400, {"ok": False})
        st, b, _ = binario("/api/consultorio/anexo?c=%s&nome=%s" % (c, urllib.parse.quote(str(q.get("nome") or "anexo")[:80])), dados, "application/octet-stream")
        try: o = json.loads(b or b"{}")
        except Exception: o = {"ok": False}
        return h.responde(st, o)
    try: d = json.loads(h.rfile.read(min(n, 20000)) or b"{}")
    except Exception: d = {}
    if via == "criar":
        st, o = pede("/api/consultorio/criar", {"etiqueta": str(d.get("etiqueta", ""))[:60], "minutos": d.get("minutos")})
        if o.get("ok"):
            o["link"] = SITE + o["url"]; _cache.pop("lista", None)
            try: open(ACORDAR, "w").close()
            except OSError: pass
        return h.responde(st, o)
    c = codigo(d.get("c"))
    if via == "ficha" and c:
        return h.responde(200, ficha.guardar(c, d.get("nome"), d.get("nasc")) if ficha else {"ok": False, "erro": "Falta o consultorio_ficha.py."})
    if via == "tempo" and c:
        _cache.pop("lista", None)
        return h.responde(*pede("/api/consultorio/tempo", {"c": c, "minutos": d.get("minutos")}))
    if via in ("atender", "fechar", "escreve", "msg", "reabrir") and c:
        _cache.pop("lista", None)
        st, o = pede("/api/consultorio/" + via, {"c": c, "texto": str(d.get("texto", ""))[:2000]})
        if via == "reabrir" and o.get("ok"):
            try: open(ACORDAR, "w").close()   # a pessoa pode voltar já: o vigia passa a olhar mais depressa
            except OSError: pass
        if via == "fechar" and o.get("ok"):   # só depois de o worker confirmar; uma falha aqui nunca impede o fecho
            try:
                f = ficha.ao_fechar(c); o["codigo"] = f.get("codigo", ""); o["pendente"] = bool(f.get("pendente"))
            except Exception as e: o["codigo"] = ""; o["pendente"] = False; print("ficha ao fechar falhou:", type(e).__name__, flush=True)
        return h.responde(st, o)
    return h.responde(404, {"ok": False})
