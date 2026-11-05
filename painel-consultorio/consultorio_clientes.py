#!/usr/bin/env python3
"""Ficha ligada à lista de clientes (pedido dele, 05/11/2026). Corre só no cerebro; quem corre isto nunca vê nomes.
Procura, abre, corrige e cria fichas em Central Tarot/Clientes, e liga cada conversa do Consultório a uma ficha.
Só o serviço consultorio-fichas.py (token do HA + cofre aberto) serve estes dados. A 8768 só chama ao_fechar(), que devolve o código.

Regras de escrita: nunca se apaga nem se reescreve o resto do ficheiro. Lê-se em bruto (sem mexer em acentos nem em fins de linha),
muda-se só a linha pedida, e grava-se de forma atómica, confirmando antes que o ficheiro não mudou desde a leitura.
Histórico: a linha mais nova vai no FIM da secção (medido em 44 fichas, confirmado por ele; ver a memória da marcação)."""
import collections, datetime, glob, io, json, os, re, shutil, stat, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import consultorio_ficha as ficha   # o molde, a numeração e o ficheiro das conversas são os de lá
CAMPOS = {"nome": "nome", "nasc": "Data Nascimento", "contato": "Contato", "email": "email", "cidade": "Cidade", "pais": "País"}
LINHA = "conversa no Consultório Virtual"
HIST = re.compile(r"(?m)^#\s*🎯\s*Histórico de Consultas[ \t]*\r?$")
NOTAS = re.compile(r"(?m)^#\s*✍\S*\s*Notas da Consulta[ \t]*\r?$")
PROX = re.compile(r"(?m)^# ")
CODIGO = re.compile(r"^C-\d{3,4}$")
CAB_MAX, HIST_N, NOTAS_LINHAS, NOTAS_CHARS, LINHA_MAX = 16384, 10, 30, 6000, 400
_cache = {}   # ficheiro -> (mtime, código, nome, nascimento); só em memória, no serviço
def C(): return ficha.C
def _abre(f): return io.open(f, "r", encoding="utf-8", errors="surrogateescape", newline="")
def _dentro(f):
    """O caminho final tem de ficar dentro de Clientes, sem ligações simbólicas para fora."""
    base = os.path.realpath(C()); r = os.path.realpath(f)
    return os.path.dirname(r) == base and r.endswith(".md")
def _indice():
    vistos = set(); fichas = []
    for f in glob.glob(glob.escape(C()) + "/*.md"):
        vistos.add(f); m = os.path.getmtime(f); x = _cache.get(f)
        if not x or x[0] != m:
            with _abre(f) as g: t = g.read(CAB_MAX)
            a = re.search(r"(?m)^\s*(?:codigo:|\*\*Código:\*\*)\s*C-(\d{3,4})\s*\r?$", t) or re.match(r"C-(\d{3,4}) ", os.path.basename(f))
            n = re.search(r"(?m)^nome:[ \t]*(.*?)[ \t]*\r?$", t); d = re.search(r"(?m)^Data Nascimento:[ \t]*(.*?)[ \t]*\r?$", t)
            nome = (n.group(1) if n else "").strip('"') or re.sub(r"^C-\d+ ", "", os.path.basename(f)[:-3])
            x = _cache[f] = (m, "C-" + a.group(1) if a else "", nome, d.group(1) if d else "")
        fichas.append((f,) + x[1:])
    for f in [f for f in _cache if f not in vistos]: _cache.pop(f)
    return fichas
def caminho(cod):
    """O ficheiro de um código que exista mesmo, e dentro de Clientes. None em todos os outros casos."""
    if not CODIGO.match(str(cod or "")): return None
    for f, c, *_ in _indice():
        if c == cod and _dentro(f): return f
    return None
def procurar(q):
    n = ficha._normal(q); d = re.sub(r"\D", "", q or "")
    if len(n) < 2: return []
    pals = n.split(); r = []
    for _, cod, nome, nasc in _indice():
        nn = ficha._normal(nome)
        if all(p in nn for p in pals) or n.upper() == cod or (len(d) >= 4 and d in re.sub(r"\D", "", nasc)):
            r.append({"codigo": cod, "nome": nome, "nasc": nasc})
    return sorted(r, key=lambda x: x["nome"])[:30]
def abrir(cod):
    """O último estado sem carregar a ficha inteira: lê linha a linha e guarda só a cauda de cada secção."""
    f = caminho(cod)
    if not f: return None
    topo = {}; hist = collections.deque(maxlen=HIST_N); notas = collections.deque(maxlen=NOTAS_LINHAS); sec = ""; fm = 0
    with _abre(f) as g:
        for i, l in enumerate(g):
            l = l.rstrip("\r\n")[:LINHA_MAX]
            if fm < 2:
                if l.strip() == "---": fm += 1; continue
                if fm == 1:
                    m = re.match(r"([^:\s][^:]*):[ \t]*(.*)$", l)
                    if m and m.group(1) in CAMPOS.values(): topo[m.group(1)] = m.group(2).strip().strip('"')
                    continue
            if HIST.match(l): sec = "h"; continue
            if NOTAS.match(l): sec = "n"; continue
            if l.startswith("# "): sec = ""; continue
            if sec == "h" and l.strip(): hist.append(l)
            elif sec == "n" and l.strip(): notas.append(l)
    n = list(notas)
    while sum(len(x) for x in n) > NOTAS_CHARS: n.pop(0)
    return {"codigo": cod, "campos": {k: topo.get(v, "") for k, v in CAMPOS.items()}, "historico": list(hist), "notas": n}
def _muda(f, funcao):
    """Lê, aplica e grava de forma atómica; se o ficheiro mudar entretanto (Obsidian, fila-capturas), repete sobre o novo."""
    if not _dentro(f): raise ValueError("fora de Clientes")
    for _ in range(4):
        m0 = os.stat(f).st_mtime_ns
        with _abre(f) as g: t = g.read()
        novo = funcao(t)
        if novo == t: return False
        d = tempfile.NamedTemporaryFile("w", encoding="utf-8", errors="surrogateescape", newline="", dir=os.path.dirname(f), prefix=".consultorio-", suffix=".tmp", delete=False)
        try:
            d.write(novo); d.flush(); os.fsync(d.fileno()); d.close(); shutil.copystat(f, d.name)
            if os.stat(f).st_mtime_ns == m0: os.replace(d.name, f); _cache.pop(f, None); return True
        finally:
            if os.path.exists(d.name): os.unlink(d.name)
        time.sleep(.3)
    raise OSError("a ficha está a mudar")
def _valor(v):
    v = re.sub(r"[\x00-\x1f\x7f]", " ", str(v or "")).strip()[:120]
    return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"' if re.search(r': |^[\[\]{}#&*!|>%@`\'"-]| #', v) else v
def _nl(t): return "\r\n" if "\r\n" in t[:2000] else "\n"
def _campos(t, novos):
    """Só dentro do bloco de cima, e só as linhas destes campos."""
    m = re.match(r"---\r?\n", t); nl = _nl(t)
    fim = re.compile(r"(?m)^---[ \t]*\r?$").search(t, m.end()) if m else None
    if not fim: return t
    bloco = t[m.end():fim.start()]
    for chave, v in novos.items():
        pad = re.compile(r"(?m)^" + re.escape(chave) + r":[^\r\n]*")
        lin = chave + ": " + _valor(v) if v else chave + ": "
        bloco = pad.sub(lambda _: lin, bloco, count=1) if pad.search(bloco) else bloco + lin + nl
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    if re.search(r"(?m)^Updated:", bloco): bloco = re.sub(r"(?m)^Updated:[^\r\n]*", "Updated: " + agora, bloco, count=1)
    return t[:m.end()] + bloco + t[fim.start():]
def _no_fim(t, titulo, secao, linha):
    """A linha vai no fim da secção, antes dos espaços em branco que a separam da seguinte."""
    nl = _nl(t); m = secao.search(t)
    if not m: return t.rstrip() + nl + nl + titulo + nl + nl + linha + nl
    p = PROX.search(t, m.end()); fim = p.start() if p else len(t)
    corpo = t[m.end():fim]; cheio = corpo.rstrip(); resto = corpo[len(cheio):]
    return t[:m.end()] + cheio + nl + linha + (resto or nl) + t[fim:]
def corrigir(cod, campos):
    f = caminho(cod)
    if not f: return {"ok": False, "erro": "Ficha não encontrada."}
    novos = {CAMPOS[k]: v for k, v in (campos or {}).items() if k in CAMPOS}
    n = str(novos.get("Data Nascimento", ""))
    if n and not re.fullmatch(r"\d{2}/\d{2}/\d{4}", n): return {"ok": False, "erro": "Data no formato dd/mm/aaaa."}
    if "nome" in novos and not str(novos["nome"]).strip(): return {"ok": False, "erro": "O nome não pode ficar vazio."}
    _muda(f, lambda t: _campos(t, novos)); return {"ok": True}
def nota(cod, texto):
    f = caminho(cod); texto = re.sub(r"\s+", " ", str(texto or "")).strip()[:2000]
    if not f or not texto: return {"ok": False, "erro": "Sem ficha ou sem texto."}
    linha = "- " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M") + " — " + texto
    _muda(f, lambda t: _no_fim(t, "# ✍️ Notas da Consulta", NOTAS, linha)); return {"ok": True}
def nova(dados):
    """Código seguinte, com tranca própria. A fila-capturas.py cria fichas sem tranca: daí o modo «x» e a segunda confirmação."""
    nome = re.sub(r"\s+", " ", str(dados.get("nome") or "")).strip()[:80]; nasc = str(dados.get("nasc") or "").strip()
    if ficha._normal(nome) in ("teste", "test"): return {"ok": False, "erro": "O nome «teste» não cria ficha."}
    if nasc and not re.fullmatch(r"\d{2}/\d{2}/\d{4}", nasc): return {"ok": False, "erro": "Data no formato dd/mm/aaaa."}
    if not os.path.isdir(C()): return {"ok": False, "erro": "Cofre fechado."}
    with ficha._tranca():
        n = _proximo()
        for _ in range(40):
            cod = "C-%03d" % n; limpo = re.sub(r'[/\\:*?"<>|]', "-", nome).strip() or "Consultório"
            dest = os.path.join(C(), f"{cod} {limpo}.md")
            if glob.glob(glob.escape(C()) + "/" + cod + " *.md") or not _dentro(dest): n += 1; continue
            agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            t = _campos(ficha._ficha(cod, nome, nasc, agora), {CAMPOS[k]: dados[k] for k in ("contato", "email", "cidade", "pais") if dados.get(k)})
            try:
                with io.open(dest, "x", encoding="utf-8") as g: g.write(t)
            except FileExistsError: n += 1; continue
            os.chmod(dest, 0o600)
            if len(glob.glob(glob.escape(C()) + "/" + cod + " *.md")) > 1: os.unlink(dest); n += 1; continue   # a fila chegou ao mesmo número
            with io.open(ficha.LIV, "a", encoding="utf-8") as g: g.write("%s\t%s\t%s\n" % (cod, os.path.basename(dest), datetime.date.today()))
            return {"ok": True, "codigo": cod}
    return {"ok": False, "erro": "Não encontrei um número livre."}
def _proximo():
    m = 0
    for _, c, *_r in _indice():
        if c: m = max(m, int(c[2:]))
    if os.path.exists(ficha.LIV):
        for l in io.open(ficha.LIV, encoding="utf-8"):
            x = re.match(r"C-(\d{3,4})\t", l)
            if x: m = max(m, int(x.group(1)))
    return m + 1
# ---------- a conversa e a sua ficha, no mesmo ficheiro de ~/.consultorio-fichas.json ----------
def associar(c, cod):
    if cod and not caminho(cod): return {"ok": False, "erro": "Ficha não encontrada."}
    with ficha._tranca():
        e = ficha._ler(); x = e.setdefault(c, {}); x["assoc"] = cod or ""; ficha._grava(e)
    return {"ok": True, "codigo": cod or ""}
def conversa(c):
    x = ficha._ler().get(c, {}); return {"codigo": x.get("assoc", ""), "pendente": bool(x.get("pend_hist"))}
def _linha_hist(cod, dia):
    f = caminho(cod)
    if not f: return False
    linha = f"- {dia} — {LINHA}"
    _muda(f, lambda t: t if linha in t else _no_fim(t, "# 🎯 Histórico de Consultas", HIST, linha)); return True
def ao_fechar(c, fechado=None):
    """Acrescenta a linha ao Histórico da ficha escolhida. Sem ficha escolhida, nada. Nunca cria ficha."""
    with ficha._tranca():
        e = ficha._ler(); x = e.get(c)
        if not x or not x.get("assoc"): return {"ok": True, "codigo": ""}
        if fechado and x.get("fechou_ms") and abs(x["fechou_ms"] - fechado) < 300000: return {"ok": True, "codigo": x["assoc"]}
        x["fechou_ms"] = fechado or int(time.time() * 1000); x["pend_hist"] = datetime.date.today().strftime("%d/%m/%Y"); cod = x["assoc"]; ficha._grava(e)
    return processar(c) or {"ok": True, "codigo": cod}
def processar(c=None):
    """Linhas à espera do cofre. Devolve o resultado da conversa c, se pedida."""
    e = ficha._ler(); pend = [(k, x) for k, x in e.items() if x.get("pend_hist")]; res = None
    if not pend: return res
    if not os.path.isdir(C()):
        if c in dict(pend): res = {"ok": True, "codigo": e[c]["assoc"], "pendente": True}; ficha._aviso("🚪 Consultório: o cofre está fechado. A linha do Histórico fica à espera e escrevo-a quando o cofre abrir.")
        return res
    for k, x in pend:
        cod = x["assoc"]; ok = _linha_hist(cod, x["pend_hist"])
        with ficha._tranca():
            e2 = ficha._ler(); e2.get(k, {}).pop("pend_hist", None); ficha._grava(e2)
        ficha._aviso(f"🚪 Consultório: acrescentei a conversa à ficha da *{cod}*." if ok else f"🚪 Consultório: não encontrei a ficha da *{cod}*; não criei nenhuma.")
        if k == c: res = {"ok": True, "codigo": cod, "pendente": False}
    return res
def migrar():
    """Uma vez, ao aplicar: quem já tinha ficha criada pelo botão antigo fica associado a ela. Só conta; não imprime nomes."""
    if not os.path.exists(ficha.EST): print("nada a migrar"); return
    copia = ficha.EST + ".antes-clientes"
    if not os.path.exists(copia): shutil.copy2(ficha.EST, copia); os.chmod(copia, 0o600)
    with ficha._tranca():
        e = ficha._ler(); assoc = sem = 0
        for x in e.values():
            if x.get("codigo") and not x.get("assoc"): x["assoc"] = x["codigo"]; assoc += 1
            elif x.get("nome") and not x.get("codigo") and not x.get("assoc"): sem += 1
        ficha._grava(e)
    print(f"associadas: {assoc}; com nome e sem ficha, por ligar à mão: {sem}")
if __name__ == "__main__" and sys.argv[1:] == ["migrar"]: migrar()
