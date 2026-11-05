#!/usr/bin/env python3
"""O vigia das contas do site (05/11/2026). PREPARADO, POR LIGAR: ver LIGAR.md.

O worker não envia correio. Quando alguém pede para entrar, o pedido fica na fila do Durable Object Contas e a «campainha»
(WebSocket em hibernação) toca: este vigia recebe o toque em menos de 1 s, vai buscar a fila e envia pelo SMTP das promoções.

Porquê campainha e não perguntar de 5 em 5 s: seriam 17 mil pedidos por dia no plano grátis (100 mil), que já esteve apertado
a 03/11. Assim gasta 1 ligação, mais 1 pergunta de reserva a cada 5 minutos (288/dia) para o caso de um toque se perder.

- As chaves ficam em memória: lêem-se do cofre quando ele está aberto, e a madrugada de cofre fechado continua a enviar.
- ~/.nao-enviar-email.txt: tem códigos, por isso lê-se o email da ficha desses códigos (como em promocoes.py). Quem lá está não
  recebe o email; a fila apaga-se na mesma e o site responde igual. Nunca se imprimem emails, nem ligações.
- O email leva só a ligação: sem o nome escrito no site (um estranho podia usá-lo para meter texto em emails nossos), sem
  rastreio e sem botão de promoções.
- Lista de promoções: só com o ficheiro «promo-LIGADA» ao lado deste guião. Enquanto não existir, os eventos ficam no site.
  Entrar na lista é pelo extras.json (o caminho sem ficha de cliente); retirar é pelo saidas.json (ganha a tudo, como o /sair).
"""
import datetime, email.message, email.utils, glob, hashlib, html, io, json, os, re, smtplib, subprocess, sys, time, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("CONTA_VIGIA_PROMOCOES", os.path.expanduser("~/promocoes")))
import promocoes as P
from websockets.sync.client import connect

BASE = os.environ.get("CONTA_VIGIA_BASE", "https://genialtarot.com")
ENSAIO = os.environ.get("CONTA_VIGIA_ENSAIO", "")     # pasta: em vez de enviar, escreve lá os emails
UA = "genialtarot-conta-vigia/1"
RESERVA = 300         # segundos entre perguntas de reserva
RELER_COFRE = 3600    # de quanto em quanto se relê a lista de quem não recebe email
aviso_em = {}


def avisar(tipo, texto):
    """Sem dados de ninguém; no máximo 1 aviso por hora de cada tipo. O silêncio não pode ser ambíguo."""
    if time.time() - aviso_em.get(tipo, 0) < 3600: return
    aviso_em[tipo] = time.time()
    try:
        subprocess.run([P.NOTIFY, "👤 Contas do site: " + texto], timeout=30, capture_output=True)
    except Exception:
        pass


def bloqueados():
    """Os emails das fichas cujos códigos estão em ~/.nao-enviar-email.txt."""
    nao = {l.strip().upper() for l in open(P.NAO, encoding="utf-8") if l.strip() and not l.startswith("#")} if os.path.exists(P.NAO) else set()
    fora = set()
    for f in glob.glob(glob.escape(P.CLIENTES) + "/*.md"):
        t = io.open(f, encoding="utf-8", errors="replace").read()
        fm = P.frontmatter(t)
        cod = fm.get("codigo") or (re.search(r"(?m)^\*\*Código:\*\*\s*(C-\d{3})", t) or [None, ""])[1]
        if cod.upper() not in nao: continue
        em = (fm.get("email") or fm.get("Email") or "").strip().lower()
        if not P.EMAIL_RE.match(em):
            m = re.search(r"(?mi)^\*{0,2}e-?mail:?\*{0,2}:?\s*([^\s@]+@[^\s@]+\.[a-z]{2,})\s*$", t)
            em = m.group(1).lower() if m else ""
        if em: fora.add(em)
    return fora


class Estado:
    chave = senha = None
    fora = None           # None = ainda não se conseguiu ler: não se envia a ninguém (cumprir a lista vem primeiro)
    lido_em = 0


def carregar():
    if os.environ.get("CONTA_VIGIA_CHAVE"):   # só para os testes
        Estado.chave, Estado.senha, Estado.fora = os.environ["CONTA_VIGIA_CHAVE"], "", set(); return True
    if not P.cofre_aberto(): return Estado.chave is not None
    Estado.chave = open(os.path.join(P.CHAVES, "site-estatisticas.pass")).read().strip()
    Estado.senha = open(P.SENHA).read().strip()
    Estado.fora = bloqueados(); Estado.lido_em = time.time()
    return True


def pedir(caminho, corpo=None):
    req = urllib.request.Request(BASE + "/api/conta/" + caminho, data=json.dumps(corpo).encode() if corpo is not None else None,
                                 headers={"X-Chave": Estado.chave, "User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def compor(para, link):
    m = email.message.EmailMessage()
    m["Subject"] = "A sua ligação para entrar no Genial Tarot"
    m["From"] = email.utils.formataddr(("Genial Tarot", P.CONTA))
    m["To"] = para
    m["Date"] = email.utils.formatdate(localtime=True)
    m["Message-ID"] = email.utils.make_msgid(domain="genialtarot.com")
    m["Auto-Submitted"] = "auto-generated"
    m.set_content("Olá,\n\nPara entrar no Genial Tarot, abra esta ligação e carregue em «Confirmar e entrar»:\n\n" + link +
                  "\n\nÉ válida durante 15 minutos e só funciona uma vez.\nSe não foi você que pediu, ignore este email: nada acontece sem carregar na ligação.\n\nGenial Tarot\nhttps://genialtarot.com\n")
    l = html.escape(link, quote=True)
    m.add_alternative(f"""<!doctype html><html lang="pt"><body style="margin:0;background:#12061f;padding:24px 12px;font-family:Arial,Helvetica,sans-serif">
<table role="presentation" width="100%" style="max-width:480px;margin:0 auto;background:#1f0d33;border:1px solid #6b3f8f;border-radius:16px"><tr><td style="padding:28px 24px;color:#f6efff;font-size:16px;line-height:1.55">
<p style="margin:0 0 14px;color:#f2c96b;font-size:22px;font-weight:bold">Entrar no Genial Tarot</p>
<p style="margin:0 0 22px">Olá. Carregue no botão para confirmar o seu email e entrar.</p>
<p style="margin:0 0 22px"><a href="{l}" style="display:inline-block;padding:13px 24px;border-radius:12px;background:#f2c96b;color:#2a1300;font-weight:bold;text-decoration:none">Abrir e confirmar</a></p>
<p style="margin:0 0 10px;font-size:14px;color:#cdb8e6">É válida durante 15 minutos e só funciona uma vez.</p>
<p style="margin:0;font-size:14px;color:#cdb8e6">Se não foi você que pediu, ignore este email: nada acontece sem carregar na ligação.</p>
</td></tr></table></body></html>""", subtype="html")
    return m


def enviar_todos(emails):
    feitos, s = [], None
    try:
        for e in emails:
            para = e["email"].strip().lower()
            if para in Estado.fora:
                feitos.append(e["id"]); continue
            m = compor(para, e["link"])
            if ENSAIO:
                os.makedirs(ENSAIO, exist_ok=True)
                open(os.path.join(ENSAIO, "%d.eml" % e["id"]), "wb").write(bytes(m))
            else:
                if s is None:
                    s = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30); s.login(P.CONTA, Estado.senha)
                s.send_message(m)
            feitos.append(e["id"])
    finally:
        if s is not None:
            try: s.quit()
            except Exception: pass
        if feitos: pedir("feito", {"emails": feitos})
    return len(feitos)


def aplicar_evento(ev, chave):
    """Promoções: uma alteração de cada vez, nos mesmos ficheiros que promocoes.py lê. Retirar ganha sempre."""
    extras = P.ler_json("extras.json", []); saidas = P.ler_json("saidas.json", {})
    hoje = datetime.date.today().isoformat(); agora = datetime.datetime.now().isoformat(timespec="minutes")
    if ev["tipo"] == "apagou":
        tokens = P.ler_json("tokens.json", {})
        h = lambda em: hashlib.sha256((chave + "|" + em).encode()).hexdigest()
        minhas = [x["email"].lower() for x in extras if x.get("codigo") == "conta" and h(x["email"].lower()) == ev["hash"]]
        if minhas:
            P.gravar_json("extras.json", [x for x in extras if x["email"].lower() not in minhas])
            for em in minhas: tokens.pop(em, None); saidas.pop(em, None)
            P.gravar_json("tokens.json", tokens); P.gravar_json("saidas.json", saidas)
        else:   # era da lista por outro caminho (ficha): não apaga a ficha, mas deixa de receber
            for em in tokens:
                if h(em) == ev["hash"]: saidas[em] = agora; P.gravar_json("saidas.json", saidas)
        return
    em = ev["email"].lower()
    if ev["tipo"] == "deu":
        if not any(x["email"].lower() == em for x in extras):
            extras.append({"email": em, "nome": ev.get("nome") or "", "codigo": "conta", "grupo": "autorizou", "desde": hoje,
                           "consentimento": {"quando": ev["quando"], "versao": ev["versao"], "texto": ev["texto"]}})
            P.gravar_json("extras.json", extras)
        if em in saidas:
            del saidas[em]; P.gravar_json("saidas.json", saidas)
    elif ev["tipo"] == "retirou":
        saidas[em] = agora; P.gravar_json("saidas.json", saidas)
        P.gravar_json("extras.json", [x for x in extras if x["email"].lower() != em])


def tratar():
    r = pedir("fila")
    if r.get("emails"):
        if Estado.fora is None:
            avisar("cofre", "há pedidos à espera, mas a lista de quem não recebe email ainda não foi lida (cofre fechado desde o arranque).")
        else:
            enviar_todos(r["emails"])
    if r.get("eventos") and os.path.exists(os.path.join(AQUI, "promo-LIGADA")) and P.cofre_aberto():
        feitos = []
        for ev in r["eventos"]:
            aplicar_evento(ev, Estado.chave); feitos.append(ev["id"])
        pedir("feito", {"eventos": feitos})


def main():
    while not carregar():
        avisar("cofre", "à espera do cofre aberto para ler as chaves; até lá não saem emails de entrada.")
        time.sleep(30)
    pausa, caido_desde = 5, None
    url = BASE.replace("https://", "wss://").replace("http://", "ws://") + "/api/conta/campainha"
    while True:
        try:
            with connect(url, additional_headers={"X-Chave": Estado.chave}, user_agent_header=UA, open_timeout=20, ping_interval=25, ping_timeout=20) as ws:
                pausa, caido_desde = 5, None
                tratar()
                while True:
                    try: ws.recv(timeout=RESERVA)
                    except TimeoutError: pass
                    if time.time() - Estado.lido_em > RELER_COFRE and P.cofre_aberto(): carregar()
                    tratar()
        except KeyboardInterrupt:
            return
        except Exception as e:
            caido_desde = caido_desde or time.time()
            print("campainha em baixo:", type(e).__name__, flush=True)
            try: tratar()
            except Exception as e2: print("fila em baixo:", type(e2).__name__, flush=True)
            if time.time() - caido_desde > 300:
                avisar("ligacao", "sem ligação ao site há mais de 5 minutos: os emails de entrada podem não estar a sair.")
            time.sleep(pausa); pausa = min(pausa * 2, 60)


if __name__ == "__main__":
    main()
