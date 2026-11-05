#!/usr/bin/env python3
"""Consultório Virtual: o serviço das fichas (05/11/2026). Só aqui a lista de clientes sai do disco, e só para quem tiver sessão no HA.
Guarda igual ao do promocoes.py: token do HA validado no próprio HA (falha fechado) + cofre aberto. Escuta só em 100.100.77.18.
Sem registos de pedidos, e tudo com no-store. Página: /local/consultorio/index.html."""
import http.server, json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import consultorio_clientes as cl
COFRE = os.environ.get("CONSULTORIO_COFRE", "/media/veracrypt23")
HA = os.environ.get("CONSULTORIO_HA", "http://127.0.0.1:8123")
ORIGENS = tuple(os.environ.get("CONSULTORIO_ORIGENS", "http://100.100.77.18:8123,https://cerebro.tail5ae53.ts.net").split(","))
IP, PORTA = os.environ.get("CONSULTORIO_IP", "100.100.77.18"), int(os.environ.get("CONSULTORIO_PORTA", "8811"))
CONVERSA = re.compile(r"^[a-hjkmnp-z2-9]{20}$")
VALIDOS = {}
def cofre_aberto(): return os.path.ismount(COFRE)
def token_ok(cab):
    t = (cab or "").removeprefix("Bearer ").strip()
    if not t or len(t) > 4000: return False
    if VALIDOS.get(t, 0) > time.time(): return True
    try:
        with urllib.request.urlopen(urllib.request.Request(HA + "/api/", headers={"Authorization": "Bearer " + t}), timeout=10) as r: ok = r.status == 200
    except Exception: ok = False
    if ok: VALIDOS[t] = time.time() + 300
    return ok
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def cors(self):
        o = self.headers.get("Origin", "")
        if o in ORIGENS:
            self.send_header("Access-Control-Allow-Origin", o); self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type"); self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    def responde(self, cod, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(cod); self.cors(); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self): self.send_response(204); self.cors(); self.end_headers()
    def guarda(self):
        if not token_ok(self.headers.get("Authorization")): self.responde(401, {"erro": "sem sessão do Home Assistant"}); return False
        if not cofre_aberto(): self.responde(503, {"erro": "o cofre está fechado"}); return False
        return True
    def trata(self, faz):
        try: self.responde(200, faz())
        except Exception as e: print("fichas:", type(e).__name__, flush=True); self.responde(500, {"ok": False, "erro": "Não foi possível."})
    def do_GET(self):
        if not self.guarda(): return
        u = urllib.parse.urlparse(self.path); q = dict(urllib.parse.parse_qsl(u.query))
        if u.path == "/procurar": return self.trata(lambda: {"fichas": cl.procurar(q.get("q", "")[:80])})
        if u.path == "/ficha":
            r = cl.abrir(q.get("cod", ""))
            return self.responde(200, r) if r else self.responde(404, {"erro": "Ficha não encontrada."})
        if u.path == "/conversa" and CONVERSA.match(q.get("c", "")): return self.trata(lambda: cl.conversa(q["c"]))
        self.responde(404, {})
    def do_POST(self):
        if not self.guarda(): return
        n = int(self.headers.get("Content-Length") or 0)
        if n > 20000: self.rfile.read(n); return self.responde(413, {})
        try: d = json.loads(self.rfile.read(n) or b"{}")
        except ValueError: return self.responde(400, {})
        c = str(d.get("c", "")); via = self.path
        if via == "/associar" and CONVERSA.match(c): return self.trata(lambda: cl.associar(c, d.get("cod", "")))
        if via == "/corrigir": return self.trata(lambda: cl.corrigir(d.get("cod"), d.get("campos")))
        if via == "/nota": return self.trata(lambda: cl.nota(d.get("cod"), d.get("texto")))
        if via == "/nova":
            def faz():
                r = cl.nova(d)
                if r.get("ok") and CONVERSA.match(c): cl.associar(c, r["codigo"])
                return r
            return self.trata(faz)
        self.responde(404, {})
http.server.ThreadingHTTPServer((IP, PORTA), H).serve_forever()
