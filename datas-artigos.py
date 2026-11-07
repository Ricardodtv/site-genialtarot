#!/usr/bin/env python3
"""Datas reais nos dados estruturados (07/11/2026, pedido dele). Nos nós Article sem datePublished, acrescenta a data em que a página
entrou no site e a da última alteração, tiradas do git. Commits que mexem em mais de 40 páginas não contam como alteração. Idempotente."""
import glob, json, os, re, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
real, criada = {}, {}
d, fs = None, []
def fecha():
    if d is None: return
    h = [x for x in fs if x.endswith(".html")]
    for x in h:
        criada[x] = d
        if len(h) <= 40: real.setdefault(x, d)
for l in subprocess.run(["git", "log", "--format=@%cs", "--name-only"], capture_output=True, text=True).stdout.split("\n"):
    if l.startswith("@"): fecha(); d, fs = l[1:], []
    elif l.strip(): fs.append(l.strip().strip('"'))
fecha()
n = 0
BL = re.compile(r'(<script type="application/ld\+json"[^>]*>\s*)(.*?)(\s*</script>)', re.S)
for f in glob.glob("*.html") + glob.glob("signo/*.html") + glob.glob("sonho/*.html") + glob.glob("anjo/*.html"):
    if f not in criada: continue
    s = open(f, encoding="utf-8", errors="ignore").read()
    if '"Article"' not in s: continue
    mudou = False
    def troca(m):
        global mudou
        try: o = json.loads(m.group(2))
        except ValueError: return m.group(0)
        nos = o.get("@graph", [o]) if isinstance(o, dict) else o
        c = False
        for x in nos:
            if isinstance(x, dict) and x.get("@type") == "Article" and "datePublished" not in x:
                x["datePublished"] = criada[f]; x["dateModified"] = real.get(f, criada[f]); c = True
        if not c: return m.group(0)
        mudou = True
        return m.group(1) + json.dumps(o, ensure_ascii=False) + m.group(3)
    s2 = BL.sub(troca, s)
    if mudou: open(f, "w", encoding="utf-8").write(s2); n += 1
print("artigos:", n)
