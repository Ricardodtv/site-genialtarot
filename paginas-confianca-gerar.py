#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quatro páginas novas (12/11/2026, pedido dele, das lacunas encontradas na análise da concorrente «Cartas da Maya»):
  /consulta-de-tarot        Consulta de Tarot em Portugal (e à distância): preços À VISTA, marcação e pagamento
  /canais-oficiais          as contas oficiais e o aviso contra perfis falsos («consultas gratuitas»)
  /tarot-terapeutico        o tarot como espelho e reflexão — NÃO substitui psicólogo nem médico
  /tarot-e-autoconhecimento o tarot para se conhecer melhor

Preços: SÓ do produtos.js (e PIX do pix.js), lidos aqui com o node e escritos no HTML; o JavaScript da página volta a
lê-los no navegador, para nunca ficarem diferentes da loja. Molde visual: o CSS de aconselhamento-espiritual.html.
As imagens de partilha (…-og.jpg, 1200×630) saem das fotos dele (acervo das capas) e do baralho oficial.

    python3 paginas-confianca-gerar.py          (na raiz do repositório)
Página reescrita = perdem-se as camadas que o pre-commit volta a pôr sozinho (gt-casa, li-gt): por isso correr antes
do commit, nunca depois.
"""
import os, re, json, html, subprocess, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = "https://genialtarot.com"
WA = "351914920427"
ESC = html.escape
HOJE = datetime.date.today().isoformat()


def node(expr, ficheiro):
    js = open(os.path.join(AQUI, ficheiro), encoding="utf-8").read()
    r = subprocess.run(["node", "-e", f"const f=new Function({json.dumps(js + '; return ' + expr + ';')});process.stdout.write(JSON.stringify(f()))"],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


PRODUTOS = node("PRODUTOS", "produtos.js")
PIX = node("PIX_PRODUTOS", "pix.js")


def produto(procura):
    for p in PRODUTOS:
        if procura in p["nome"]: return p
    raise SystemExit(f"produto não encontrado no produtos.js: {procura}")


def pix_valor(p):
    d = PIX.get(p["nome"])
    return d["normal"]["valor"] if d else None


CSS_BASE = re.search(r"<style>(.*?)</style>", open(os.path.join(AQUI, "aconselhamento-espiritual.html"), encoding="utf-8").read(), re.S).group(1)
CSS_EXTRA = r"""
.texto ul, .texto ol { font-size: 1.05rem; padding-left: 1.3rem; } .texto li { margin: .3rem 0; }
.aviso-forte { border: 2px solid oklch(0.70 0.20 25); background: linear-gradient(160deg, oklch(0.30 0.10 25 / .55), oklch(0.20 0.07 272)); border-radius: 1.4rem; padding: clamp(1rem, 3vw, 1.6rem); text-align: center; }
.aviso-forte h2 { color: oklch(0.88 0.12 60); }
.aviso-forte p { font-size: 1.12rem; margin: .4rem auto; max-width: 40rem; }
.aviso-forte .grande { font-family: var(--serifa); font-size: clamp(1.25rem, 3vw, 1.55rem); font-weight: 700; color: var(--texto); line-height: 1.35; }
.contas { display: grid; gap: .7rem; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); margin: 1rem 0; }
.contas a { display: flex; gap: .8rem; align-items: center; text-decoration: none; color: var(--texto); background: oklch(0.20 0.06 272 / .88); border: 1px solid var(--borda); border-radius: 1.1rem; padding: .8rem 1rem; }
.contas a:hover { border-color: var(--ouro); }
.contas i { font-style: normal; font-size: 1.7rem; width: 2.4rem; text-align: center; flex: none; }
.contas b { display: block; } .contas small { display: block; color: var(--suave); font-size: .85rem; overflow-wrap: anywhere; }
.precos { width: 100%; border-collapse: collapse; margin: .8rem 0; }
.precos th { text-align: left; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: var(--ouro); padding: .45rem .5rem; border-bottom: 1px solid var(--borda); }
.precos td { padding: .7rem .5rem; border-bottom: 1px solid oklch(0.75 0.10 260 / 0.15); vertical-align: top; }
.precos td small { display: block; color: var(--suave); font-size: .85rem; margin-top: .15rem; }
.precos .eur { font-weight: 800; font-size: 1.15rem; color: var(--ouro); white-space: nowrap; }
.precos .brl { display: block; font-size: .8rem; color: oklch(0.85 0.12 170); font-weight: 700; white-space: nowrap; }
.precos .acoes { display: flex; flex-direction: column; gap: .35rem; min-width: 8.5rem; }
.precos .acoes a, .precos .acoes button { font: inherit; font-size: .82rem; font-weight: 800; text-align: center; text-decoration: none; border-radius: 999px; padding: .45rem .7rem; cursor: pointer; }
.precos .acoes a { color: oklch(0.22 0.06 270); background: var(--grad-ouro); border: 0; }
.precos .acoes button { color: white; background: oklch(0.24 0.05 200 / .9); border: 1.5px solid #32BCAD; }
@media (max-width: 560px) { .precos thead { display: none; } .precos tr { display: grid; grid-template-columns: 1fr auto; gap: .3rem .8rem; padding: .7rem 0; border-bottom: 1px solid oklch(0.75 0.10 260 / 0.2); }
  .precos td { border: 0; padding: 0; } .precos td:first-child { grid-column: 1 / -1; } .precos .acoes { flex-direction: row; } }
.passos { counter-reset: p; list-style: none; padding: 0 !important; display: grid; gap: .7rem; }
.passos li { counter-increment: p; position: relative; padding: .8rem 1rem .8rem 3.2rem; border-radius: 1rem; background: oklch(0.20 0.06 272 / .85); border: 1px solid var(--borda); }
.passos li::before { content: counter(p); position: absolute; left: .9rem; top: .75rem; width: 1.7rem; height: 1.7rem; border-radius: 50%; display: grid; place-items: center; font-weight: 800; color: oklch(0.22 0.06 270); background: var(--grad-ouro); }
.duas { display: grid; gap: .8rem; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); margin: 1rem 0; }
.duas div { border-radius: 1rem; padding: .9rem 1rem; background: oklch(0.20 0.06 272 / .85); border: 1px solid var(--borda); }
.duas h3 { font-family: var(--titulo); font-size: 1.05rem; margin: 0 0 .4rem; color: var(--ouro); }
.duas p { margin: 0; font-size: 1rem; }
.cartas-fila { display: flex; justify-content: center; gap: .6rem; margin: 1rem 0; flex-wrap: wrap; }
.cartas-fila figure { margin: 0; text-align: center; width: 7.2rem; }
.cartas-fila img { width: 100%; height: auto; border-radius: .5rem; box-shadow: 0 8px 24px #0009; }
.cartas-fila figcaption { font-size: .8rem; color: var(--suave); margin-top: .3rem; }
.nota-saude { border-left: 4px solid var(--ouro); background: oklch(0.85 0.13 88 / .08); border-radius: .8rem; padding: .8rem 1rem; font-size: .98rem; }
.promessa { font-family: var(--titulo); color: var(--ouro); font-size: 1.3rem; text-align: center; margin: .6rem 0 0; }
.pix-fundo { position: fixed; inset: 0; z-index: 100; display: none; place-items: center; background: rgba(5,5,20,.82); padding: 1rem; }
.pix-fundo.aberto { display: grid; }
.pix-caixa { position: relative; width: 100%; max-width: 24rem; max-height: 92vh; overflow-y: auto; border-radius: 1rem; background: #fff; color: #1d1d2b; padding: 1.2rem 1.2rem 1.4rem; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,.6); }
.pix-fechar { position: absolute; top: .4rem; right: .6rem; border: 0; background: none; font-size: 1.6rem; color: #666; cursor: pointer; }
.pix-caixa h4 { font-size: 1.15rem; color: #0f766e; margin: .2rem 0 .3rem; }
.pix-caixa .pix-prod { font-size: .82rem; color: #555; line-height: 1.35; }
.pix-caixa .pix-valor { font-size: 1.9rem; font-weight: 800; color: #0f766e; margin: .3rem 0 0; }
.pix-caixa .pix-passo { margin: .6rem 0; font-size: .86rem; background: #fef9c3; border-radius: .6rem; padding: .5rem; line-height: 1.4; }
.pix-caixa img.pix-qr { width: 15rem; max-width: 100%; height: auto; image-rendering: pixelated; margin: .2rem auto; display: block; }
.pix-copiar { width: 100%; border: 0; border-radius: .6rem; background: #32BCAD; color: white; font-weight: 700; font-size: .95rem; padding: .7rem; margin-top: .5rem; cursor: pointer; }
.pix-aviso { font-size: .78rem; color: #555; margin-top: .7rem; line-height: 1.45; }
.pix-wa { display: inline-block; margin-top: .6rem; border-radius: 999px; background: #25D366; color: white; font-weight: 700; font-size: .86rem; padding: .55rem 1rem; text-decoration: none; }
"""

# o mesmo modal de PIX da página do Ascendente e da loja (código e QR do pix.js, valor «normal»: a promoção acabou a 11/11)
JS_PRECOS = r"""<script src="/produtos.js"></script>
<script src="/pix.js"></script>
<script>
(function () {
  var ESC = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var L = (typeof PRODUTOS !== "undefined" && Array.isArray(PRODUTOS)) ? PRODUTOS : [];
  var P = (typeof PIX_PRODUTOS !== "undefined") ? PIX_PRODUTOS : {};
  var promo = function () { return typeof PIX_PROMO_FIM !== "undefined" && Date.now() < PIX_PROMO_FIM; };
  var brl = function (v) { return "R$ " + Number(v).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  /* os preços escritos no HTML voltam a ser lidos da loja (produtos.js), para nunca ficarem diferentes */
  document.querySelectorAll("[data-produto]").forEach(function (tr) {
    var p = L.find(function (x) { return x.nome === tr.getAttribute("data-produto"); }); if (!p) return;
    var e = tr.querySelector(".eur-v"); if (e && p.preco) e.textContent = p.preco;
    var d = P[p.nome], b = tr.querySelector(".brl");
    if (d && b) b.textContent = "PIX " + brl((promo() ? d.promo : d.normal).valor);
  });
  function abrir(nome) {
    var p = L.find(function (x) { return x.nome === nome; }), d = p && P[p.nome]; if (!d) return;
    var e = promo() ? d.promo : d.normal;
    var msg = "Olá Mestre Alberto, paguei por PIX " + brl(e.valor) + ": " + p.nome + ". Segue o comprovante.";
    var f = document.getElementById("pix-fundo");
    if (!f) { f = document.createElement("div"); f.id = "pix-fundo"; f.className = "pix-fundo"; document.body.appendChild(f);
      f.addEventListener("click", function (ev) { if (ev.target === f || ev.target.closest(".pix-fechar")) f.classList.remove("aberto"); }); }
    f.innerHTML = '<div class="pix-caixa" role="dialog" aria-modal="true"><button type="button" class="pix-fechar" aria-label="Fechar">×</button>'
      + '<h4>Pagar com PIX</h4><div class="pix-prod">' + ESC(p.nome) + '</div><div class="pix-valor">' + brl(e.valor) + '</div>'
      + '<div class="pix-passo">📱 Abra a <b>app do seu banco</b> → <b>Pix</b> → <b>Ler QR Code</b>.<br>Confirme o valor: <b>' + brl(e.valor) + '</b>.</div>'
      + '<img class="pix-qr" src="/' + ESC(e.qr) + '" alt="QR Code PIX ' + brl(e.valor) + '" width="240" height="240">'
      + '<button type="button" class="pix-copiar" data-codigo="' + ESC(e.codigo) + '">📋 Copiar código PIX (copia e cola)</button>'
      + '<div class="pix-aviso">O pagamento aparece em nome de <b>' + ESC(typeof PIX_NOME !== "undefined" ? PIX_NOME : "") + '</b>, da equipe do Mestre Alberto.<br>Depois de pagar, envie o comprovante pelo WhatsApp:</div>'
      + '<a class="pix-wa" href="https://wa.me/351914920427?text=' + encodeURIComponent(msg) + '" target="_blank" rel="noopener noreferrer">💬 Enviar comprovante</a></div>';
    f.classList.add("aberto");
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-pix]"); if (b) { abrir(b.getAttribute("data-pix")); return; }
    var c = e.target.closest(".pix-copiar"); if (!c) return;
    var t = c.getAttribute("data-codigo"), ok = function () { c.textContent = "✅ Código copiado! Cole no seu banco em Pix → Copia e Cola"; };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(t).then(ok, function () { prompt("Copie o código:", t); }); else prompt("Copie o código:", t);
  });
})();
</script>"""


def faq_html(faq):
    corpo = "".join(f'<h3 style="font-size:1.05rem;margin:1rem 0 .3rem">{ESC(q)}</h3><p style="margin:0">{a}</p>' for q, a in faq)
    return ('<section class="faq-genial" style="max-width:760px;margin:2rem auto;padding:1.2rem 1.4rem;border:1px solid rgba(212,175,55,.35);'
            f'border-radius:16px;background:rgba(255,255,255,.04);line-height:1.6"><h2 style="margin-top:0">Perguntas frequentes</h2>{corpo}</section>')


def sem_tags(t): return re.sub(r"<[^>]+>", "", t)


def pagina(slug, titulo, desc, h1, sub, foto, corpo, faq=None, migalha="", og_alt="", extra_js="", tipo="Article"):
    url = f"{SITE}/{slug}"
    assert len(titulo) <= 65, (slug, len(titulo))
    assert 110 <= len(desc) <= 160, (slug, len(desc))
    graf = [{"@type": tipo, "headline" if tipo == "Article" else "name": titulo, "description": desc, "image": f"{SITE}/{slug}-og.jpg", "inLanguage": "pt",
             "author": {"@type": "Person", "name": "Mestre Alberto", "url": f"{SITE}/sobre"},
             "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": f"{SITE}/", "logo": {"@type": "ImageObject", "url": f"{SITE}/og-image.jpg"}},
             "mainEntityOfPage" if tipo == "Article" else "url": url, "datePublished": "2026-11-12", "dateModified": HOJE},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": migalha or h1, "item": url}]}]
    lds = [{"@context": "https://schema.org", "@graph": graf}]
    if faq:
        lds.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": sem_tags(a)}} for q, a in faq]})
    ld = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False)}\n</script>' for x in lds)
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{ESC(titulo)}</title>
<meta name="description" content="{ESC(desc)}" />
<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{ESC(titulo)}" />
<meta property="og:description" content="{ESC(desc)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/{slug}-og.jpg" />
<meta property="og:image:alt" content="{ESC(og_alt)}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
{ld}
<style>{CSS_BASE}{CSS_EXTRA}</style>
</head>
<body>
<div class="estrelas" aria-hidden="true"></div>
<div class="caixa">
  <header class="topo">
    <a class="backlink" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>genialtarot.com</a>
  </header>
  <section class="heroi">
    <img class="foto-mestre" src="/{foto}" alt="Mestre Alberto, tarólogo e astrólogo do Genial Tarot" width="120" height="120" />
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
  </section>
{corpo}
{faq_html(faq) if faq else ""}
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="/canais-oficiais">Canais oficiais</a> · <a href="/privacidade">Política de Privacidade</a> · <a href="/termos">Termos de Serviço</a>
</footer>
</div>
{extra_js}
<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""


def wa(txt): return f"https://wa.me/{WA}?text=" + re.sub(r"[^A-Za-z0-9\-_.~]", lambda m: "".join(f"%{b:02X}" for b in m.group(0).encode()), txt)


# ═════════════════════════════════ B · /consulta-de-tarot ═════════════════════════════════
def linha_preco(procura, titulo, explica):
    p = produto(procura)
    pv = pix_valor(p)
    brl = f'<span class="brl">PIX R$ {pv:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".") + "</span>" if pv else ""
    if p.get("link"):
        pagar = f'/pagar.html?u={ESC(p["link"])}&amp;n={ESC(re.sub(r"[^A-Za-z0-9]+", "+", titulo))}&amp;v={ESC(p["preco"].replace(" ", "+"))}'
        cartao = f'<a href="{pagar}" rel="nofollow">💳 Pagar com cartão</a>'
    else:
        cartao = f'<a href="{ESC(wa("Olá Mestre Alberto, quero marcar: " + p["nome"]))}" target="_blank" rel="noopener noreferrer">💬 Marcar no WhatsApp</a>'
    pixb = f'<button type="button" data-pix="{ESC(p["nome"])}">PIX (Brasil)</button>' if pv else ""
    return (f'<tr data-produto="{ESC(p["nome"])}"><td><b>{ESC(titulo)}</b><small>{explica}</small></td>'
            f'<td class="eur"><span class="eur-v">{ESC(p["preco"])}</span>{brl}</td><td><div class="acoes">{cartao}{pixb}</div></td></tr>'), p


def pagina_consulta():
    linhas, usados = [], []
    for procura, tit, exp in [
        ("1 Pergunta Respondida em Áudio", "1 pergunta respondida em áudio", "Envia a pergunta pelo WhatsApp e recebe um áudio com a leitura, feito só para si."),
        ("1 Pergunta de Tarot por Escrito", "1 pergunta respondida por escrito", "A resposta tirada nas cartas, por escrito, para guardar e reler."),
        ("Consulta de Tarot Online – 30 Minutos", "Consulta de Tarot · 30 minutos", "Meia hora em conversa, por videochamada ou chamada: uma ou duas questões concretas."),
        ("Todos os Temas (1 Hora", "Consulta de Tarot · 1 hora", "Uma hora para o amor, o trabalho, a família e o dinheiro, com tempo para todas as perguntas."),
        ("Consulta de Emergência", "Consulta de Emergência · 40 minutos", "Para quando não dá para esperar: resposta no máximo numa hora, com prioridade na agenda."),
        ("Parecer sobre Qualquer Assunto", "Parecer escrito sobre um assunto", "Para uma decisão importante: um parecer completo, tirado nas cartas e escrito."),
        ("Previsão Anual para 12 Meses", "Previsão Anual escrita · 12 meses", "Os seus próximos doze meses, mês a mês, escritos pelo Mestre Alberto."),
    ]:
        l, p = linha_preco(procura, tit, exp); linhas.append(l); usados.append(p)
    p30, p1h = produto("Consulta de Tarot Online – 30 Minutos"), produto("Todos os Temas (1 Hora")
    corpo = f"""  <section class="cartao texto">
    <p>Meu Querido Jardim de Almas! Há 18 anos que leio as cartas, no consultório em Fafe e à distância, para quem está em Portugal, no Brasil ou noutro país qualquer. Nesta página está tudo o que precisa de saber antes de marcar: como é uma consulta, quanto custa, como se marca e como se paga. Sem letras pequenas.</p>
    <h2>O que é uma consulta de tarot</h2>
    <p>Uma consulta de tarot é uma conversa com as cartas na mesa. Traz a sua pergunta, eu baralho e tiro as cartas por si, e leio o que elas mostram sobre o momento que está a viver: o que está a pesar, o que está a mudar e os caminhos que se abrem. O tarot não decide por si nem lhe tira a liberdade de escolher. Ajuda-o a ver com mais clareza para escolher melhor.</p>
    <p>Leio com o meu próprio baralho, desenhado para o Genial Tarot, e falo consigo em português claro, sem rodeios e sem assustar. Se a resposta das cartas não for a que esperava, digo-lha na mesma, com cuidado. É para isso que lá estou.</p>
    <h2>Presencial em Fafe ou à distância</h2>
    <div class="duas">
      <div><h3>🏠 No consultório, em Fafe</h3><p>Na Rua da Barreira, 92, em Golães (Fafe). Para quem mora no Minho ou vem de visita e gosta de ver as cartas a serem tiradas à sua frente. A marcação faz-se pelo WhatsApp. Veja <a href="/tarologo-fafe">como chegar ao consultório</a>.</p></div>
      <div><h3>🌍 À distância, em qualquer país</h3><p>Por videochamada ou chamada, ou com uma resposta em áudio ou por escrito. A leitura é a mesma do consultório: as cartas não precisam da sua presença, precisam da sua pergunta. Veja as <a href="/consulta-de-tarot-online">consultas online</a> e as <a href="/consultas-a-distancia">consultas à distância</a>.</p></div>
    </div>
  </section>
  <section class="cartao texto" id="precos">
    <h2>Preços das consultas</h2>
    <p>Os preços são os da <a href="/loja">Loja</a>, iguais para Portugal e para qualquer país. Quem está no Brasil pode pagar em reais, por PIX.</p>
    <div style="overflow-x:auto"><table class="precos"><thead><tr><th>Consulta</th><th>Preço</th><th>Pagar</th></tr></thead><tbody>{"".join(linhas)}</tbody></table></div>
    <p style="font-size:.95rem;color:var(--suave)">Não sabe qual escolher? Para uma dúvida concreta chega uma pergunta em áudio ou por escrito. Para olhar a vida com calma, a consulta de 1 hora ({ESC(p1h["preco"])}) é a mais completa. Tem outras perguntas? Escreva-me antes de pagar.</p>
  </section>
  <section class="cartao texto">
    <h2>Como marcar e pagar, passo a passo</h2>
    <ol class="passos">
      <li><b>Escolha a consulta</b> na tabela acima ou na <a href="/loja">Loja</a>. Se tiver dúvidas, pergunte primeiro no WhatsApp: +351 914 920 427.</li>
      <li><b>Pague da forma que lhe der mais jeito.</b> Com cartão, pelo botão «Pagar com cartão», que abre o pagamento seguro do myPOS. Em Portugal pode também pagar por MB WAY ou transferência bancária: os dados pedem-se no WhatsApp. No Brasil, por PIX, com o QR Code ou o código copia e cola.</li>
      <li><b>Envie-me o comprovativo e a sua pergunta</b> pelo WhatsApp. Combinamos o dia e a hora (na consulta de emergência, a resposta chega no máximo numa hora).</li>
      <li><b>A consulta:</b> por videochamada, chamada, áudio ou por escrito, conforme o que escolheu. Nas consultas ao vivo, tenha as suas perguntas apontadas: rende muito mais.</li>
    </ol>
    <p class="nota-saude">🛡️ Só marco consultas por este site, genialtarot.com, e pelo meu WhatsApp oficial. Nunca peço pagamentos nem dados por mensagem privada nas redes sociais, e não ofereço «consultas grátis» por mensagem. Se alguém o fizer em meu nome, é um perfil falso: veja os <a href="/canais-oficiais">canais oficiais</a>.</p>
  </section>
  <section class="cartao texto">
    <h2>Para quem está no Brasil e para quem vive fora</h2>
    <p>Mais de metade de quem me acompanha no YouTube está no Brasil. A consulta é a mesma: marca-se pelo WhatsApp e paga-se por PIX, em reais, sem cartão internacional. Os horários combinam-se tendo em conta o fuso (Brasília está três horas atrás de Lisboa no inverno e quatro no verão).</p>
    <p>Para quem emigrou, a consulta é feita em português de Portugal, onde quer que esteja. As perguntas de quem vive longe têm o seu peso próprio (voltar ou ficar, a família que ficou, a casa) e tenho uma página só para elas: <a href="/tarot-para-emigrantes">Tarot para emigrantes</a>.</p>
    <h2>Como se preparar</h2>
    <ul>
      <li>Escreva as perguntas antes. «O que devo saber sobre este trabalho novo?» rende mais do que «como vai ser a minha vida?».</li>
      <li>Escolha um sítio calmo, onde possa falar à vontade.</li>
      <li>Venha de mente aberta. As cartas mostram tendências e caminhos, não uma sentença fechada.</li>
    </ul>
    <h2>O que não faço</h2>
    <p>Não prometo curas, nem resultados garantidos, nem «trabalhos» para prejudicar ninguém. O tarot não substitui o médico, o psicólogo, o advogado ou o contabilista: se o que me trouxer precisar de um deles, digo-lho. Se quiser perceber melhor como uso as cartas para a reflexão pessoal, leia sobre o <a href="/tarot-terapeutico">tarot terapêutico</a> e o <a href="/tarot-e-autoconhecimento">tarot e o autoconhecimento</a>.</p>
    <p class="promessa">Eu tenho a sua resposta!</p>
    <p style="text-align:center"><a class="cta" href="{ESC(wa("Olá Mestre Alberto, quero marcar uma consulta de tarot."))}" target="_blank" rel="noopener noreferrer">💬 Marcar no WhatsApp</a></p>
  </section>
  <section class="cartao" style="text-align:center"><h2>Antes de marcar, experimente</h2><div class="ligas"><a href="/tarot-gratis">🃏 Tarot Grátis</a><a href="/carta-de-tarot">A sua carta de hoje</a><a href="/tiragem-tres-cartas">Tiragem de três cartas</a><a href="/tiragem-sim-ou-nao">Sim ou não</a><a href="/tarot-do-amor">💖 Tarot do amor</a><a href="/tarot-para-decisoes">⚖️ Decisões</a><a href="/sobre">Quem é o Mestre Alberto</a></div></section>"""
    faq = [
        ("Quanto custa uma consulta de tarot?", f"Na Loja do Genial Tarot, uma pergunta respondida em áudio custa {produto('1 Pergunta Respondida em Áudio')['preco']}, por escrito {produto('1 Pergunta de Tarot por Escrito')['preco']}, a consulta de 30 minutos {p30['preco']} e a de 1 hora {p1h['preco']}. No Brasil paga-se em reais, por PIX."),
        ("Posso fazer a consulta presencialmente?", "Sim, no consultório em Fafe (Rua da Barreira, 92, Golães), com marcação prévia pelo WhatsApp. Quem está longe pode fazê-la por videochamada, chamada, áudio ou por escrito."),
        ("Como posso pagar a consulta?", "Com cartão, pelo pagamento seguro do myPOS. Em Portugal também por MB WAY ou transferência bancária (os dados pedem-se no WhatsApp). No Brasil, por PIX."),
        ("A consulta à distância vale o mesmo que a presencial?", "Sim. O Mestre Alberto baralha e tira as cartas por si da mesma maneira; muda só o caminho por onde a resposta chega."),
        ("O Mestre Alberto oferece consultas grátis por mensagem?", 'Não. As consultas marcam-se só por este site e pelo WhatsApp oficial (+351 914 920 427). Perfis que ofereçam «consultas grátis» ou peçam dinheiro por mensagem privada são falsos. Veja a lista dos <a href="/canais-oficiais">canais oficiais</a>.'),
        ("O tarot substitui um médico ou um psicólogo?", "Não. A consulta de tarot é um apoio à reflexão e à decisão. Não substitui aconselhamento médico, psicológico, jurídico ou financeiro."),
    ]
    return pagina("consulta-de-tarot", "Consulta de Tarot em Portugal e à distância: preços e marcação",
                  "Consulta de tarot com o Mestre Alberto em Fafe ou à distância: preços à vista, marcação pelo WhatsApp e pagamento por cartão, MB WAY ou PIX.",
                  '<span class="az">Consulta de Tarot</span> em Portugal', "No consultório em Fafe ou à distância, para Portugal, o Brasil e quem vive fora: preços à vista e marcação simples.",
                  "mestre-r07.jpg", corpo, faq, "Consulta de Tarot", "O Mestre Alberto numa consulta de tarot online, sorridente, com as cartas na mesa",
                  JS_PRECOS), usados


# ═════════════════════════════════ C · /canais-oficiais ═════════════════════════════════
GRUPOS = None


def grupos():
    s = open(os.path.join(AQUI, "comunidade.html"), encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<a[^>]*href="(https://www\.facebook\.com/groups/[^"]+)"[^>]*>(.*?)</a>', s, re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        nome = re.sub(r"\s*[\d\s]+membros.*$", "", t).replace("︎", "").strip()
        out.append((m.group(1), nome))
    assert len(out) == 12, out
    return out


def pagina_canais():
    contas = [
        ("🌐", "genialtarot.com", "O site oficial: consultas, loja e pagamentos", f"{SITE}/"),
        ("💬", "WhatsApp +351 914 920 427", "O único número para marcar consultas", f"https://wa.me/{WA}"),
        ("▶️", "YouTube · Tarot e Horóscopo", "youtube.com/@Genialtarot", "https://www.youtube.com/@Genialtarot"),
        ("🎬", "YouTube · Mestre Alberto Responde", "youtube.com/@MestreAlbertoResponde · os cortes dos vídeos", "https://www.youtube.com/@MestreAlbertoResponde"),
        ("📘", "Facebook · Genial Tarot", "facebook.com/genial.tarot", "https://www.facebook.com/genial.tarot"),
        ("📘", "Facebook · Mestre Alberto", "facebook.com/Mestre.Alberto", "https://www.facebook.com/Mestre.Alberto"),
        ("📘", "Facebook · Loja Espiritual", "facebook.com/LojaEspiritualbr", "https://www.facebook.com/LojaEspiritualbr"),
        ("📸", "Instagram", "instagram.com/genialtarot", "https://www.instagram.com/genialtarot/"),
        ("🎵", "TikTok", "tiktok.com/@genialtarot", "https://www.tiktok.com/@genialtarot"),
        ("📍", "Google Maps · Genialtarot - Mestre Alberto", "O consultório em Fafe", "https://maps.google.com/?cid=17405932589735170894"),
    ]
    cx = "".join(f'<a href="{ESC(u)}" target="_blank" rel="noopener noreferrer me"><i aria-hidden="true">{i}</i><span><b>{ESC(n)}</b><small>{ESC(d)}</small></span></a>' for i, n, d, u in contas)
    gx = "".join(f'<a href="{ESC(u)}" target="_blank" rel="noopener noreferrer"><i aria-hidden="true">👥</i><span><b>{ESC(n)}</b><small>Grupo do Facebook</small></span></a>' for u, n in grupos())
    corpo = f"""  <section class="aviso-forte">
    <h2>⚠️ Atenção aos perfis falsos</h2>
    <p class="grande">O Mestre Alberto nunca pede pagamentos nem dados por mensagem privada. As consultas marcam-se só pelo site oficial, genialtarot.com, e pelo WhatsApp +351 914 920 427.</p>
    <p>Há perfis falsos a usar o nome e as fotos de tarólogos conhecidos para oferecer «consultas gratuitas» e, depois, pedir dinheiro, códigos ou dados do cartão. Se receber uma mensagem destas, não responda, não pague e denuncie o perfil na própria rede social.</p>
  </section>
  <section class="cartao texto">
    <h2>As contas oficiais</h2>
    <p>Meu Querido Jardim de Almas! Estas são as únicas contas do Genial Tarot e do Mestre Alberto. Qualquer outra que use o meu nome não é minha.</p>
    <div class="contas">{cx}</div>
  </section>
  <section class="cartao texto">
    <h2>Os 12 grupos dos signos</h2>
    <p>Cada signo tem o seu grupo no Facebook, onde partilho as previsões e as curiosidades do signo. Veja os números de cada um na página da <a href="/comunidade">comunidade</a>.</p>
    <div class="contas">{gx}</div>
  </section>
  <section class="cartao texto">
    <h2>Como reconhecer um perfil falso</h2>
    <ul>
      <li><b>Escreve-lhe primeiro</b>, sem ter pedido nada, a oferecer uma leitura «grátis» ou a dizer que viu «algo grave» no seu futuro.</li>
      <li><b>Pede dinheiro para «desfazer» um mal</b>, para um «trabalho urgente» ou para «libertar» a consulta grátis.</li>
      <li><b>Pede dados</b>: códigos que chegam por SMS, números de cartão, fotografias de documentos.</li>
      <li><b>Tem poucos seguidores ou foi criado há pouco tempo</b>, com as mesmas fotos de uma conta conhecida e um nome quase igual.</li>
      <li><b>Manda ligações de pagamento</b> que não são do site genialtarot.com.</li>
    </ul>
    <p>Na dúvida, confirme sempre pelo WhatsApp oficial antes de pagar seja o que for. Os pagamentos verdadeiros fazem-se pelos botões do site (cartão pelo myPOS e PIX para o Brasil) ou com os dados que eu próprio lhe envio do número oficial.</p>
    <h2>Se já pagou a um perfil falso</h2>
    <p>Fale logo com o seu banco: em alguns casos ainda é possível travar ou contestar o pagamento. Guarde as conversas e as provas do pagamento, denuncie o perfil na rede social e apresente queixa às autoridades (em Portugal, na PSP, na GNR ou no Ministério Público; no Brasil, numa delegacia, que em muitos estados aceita o registo pela internet).</p>
  </section>
  <section class="cartao" style="text-align:center">
    <h2>Marcar uma consulta verdadeira</h2>
    <p>Os preços estão à vista e o pagamento é seguro. Veja <a href="/consulta-de-tarot">como funciona a consulta de tarot</a> ou fale comigo diretamente.</p>
    <p class="promessa">Eu tenho a sua resposta!</p>
    <a class="cta" href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">💬 WhatsApp oficial: +351 914 920 427</a>
    <div class="ligas"><a href="/sobre">Quem é o Mestre Alberto</a><a href="/na-imprensa">Na imprensa</a><a href="/tarologo-fafe">O consultório em Fafe</a><a href="/loja">Loja</a></div>
  </section>"""
    faq = [
        ("O Mestre Alberto pede pagamentos por mensagem privada?", "Não. Nunca pede pagamentos nem dados por mensagem privada. As consultas marcam-se só pelo site genialtarot.com e pelo WhatsApp +351 914 920 427."),
        ("Recebi uma oferta de consulta grátis em nome do Mestre Alberto. É verdadeira?", "Não. O Mestre Alberto não oferece consultas grátis por mensagem. É um perfil falso: não responda, não pague e denuncie o perfil na rede social."),
        ("Quais são as redes sociais oficiais do Genial Tarot?", "O YouTube @Genialtarot e @MestreAlbertoResponde, as páginas de Facebook genial.tarot, Mestre.Alberto e LojaEspiritualbr, o Instagram genialtarot, o TikTok @genialtarot e os 12 grupos dos signos listados nesta página."),
    ]
    sameas = [u for _, _, _, u in contas if "youtube" in u or "facebook" in u or "instagram" in u or "tiktok" in u]
    p = pagina("canais-oficiais", "Canais oficiais do Mestre Alberto e aviso de perfis falsos",
               "As contas oficiais do Mestre Alberto e do Genial Tarot. Atenção: ele nunca pede pagamentos nem dados por mensagem privada; consultas só pelo site.",
               'Os <span class="az">canais oficiais</span>', "Onde encontrar o Mestre Alberto de verdade, e como não cair nos perfis falsos.",
               "mestre-r11.jpg", corpo, faq, "Canais oficiais", "O Mestre Alberto de braços abertos, no consultório, a dar as boas-vindas", tipo="WebPage")
    org = json.dumps({"@context": "https://schema.org", "@type": "Organization", "@id": f"{SITE}/#organizacao", "name": "Genial Tarot", "url": f"{SITE}/",
                      "logo": f"{SITE}/og-image.jpg", "sameAs": sameas,
                      "contactPoint": {"@type": "ContactPoint", "telephone": "+351914920427", "contactType": "customer service", "availableLanguage": ["pt-PT", "pt-BR"]}}, ensure_ascii=False)
    return p.replace("<style>", f'<script type="application/ld+json">\n{org}\n</script>\n<style>', 1)


# ═════════════════════════════════ D · tarot terapêutico e autoconhecimento ═════════════════════════════════
def cartas(lista):
    return '<div class="cartas-fila">' + "".join(
        f'<figure><img src="/cartas/{f}.webp" alt="A carta {ESC(n)} do baralho do Mestre Alberto" width="969" height="1624" loading="lazy"><figcaption>{ESC(n)}</figcaption></figure>'
        for f, n in lista) + "</div>"


NOTA_SAUDE = ('<p class="nota-saude">⚠️ <b>Uma nota importante.</b> O tarot é um espelho para a reflexão. Não é terapia no sentido clínico e '
              'não substitui um psicólogo, um psiquiatra ou um médico. Se está a passar por ansiedade forte, depressão, luto difícil ou pensamentos '
              'de se fazer mal, procure ajuda profissional. Em Portugal pode ligar para o SNS 24 (808 24 24 24); no Brasil, para o CVV (188). '
              'Em perigo imediato, ligue 112 (Portugal) ou 192 (Brasil).</p>')


def pagina_terapeutico():
    corpo = f"""  <section class="cartao texto">
    <p>Meu Querido Jardim de Almas! Chamam «tarot terapêutico» a uma maneira de usar as cartas que não está virada para adivinhar o futuro, mas para olhar para dentro. Em vez de perguntar «o que vai acontecer?», pergunta-se «o que é que eu estou a sentir, e porquê?». As cartas deixam de ser um oráculo e passam a ser um espelho.</p>
    <h2>As cartas como espelho</h2>
    <p>Cada carta do tarot é uma imagem cheia de símbolos: uma figura, um gesto, uma paisagem, uma cor. Quando olhamos para ela com uma pergunta na cabeça, a imagem puxa por coisas que já estavam cá dentro e que ainda não tinham nome. É por isso que duas pessoas podem ver a mesma carta e sentir coisas diferentes. O que a carta faz é abrir a conversa; o que aparece nessa conversa é seu.</p>
    {cartas([("09-o-eremita", "O Eremita"), ("17-a-estrela", "A Estrela"), ("18-a-lua", "A Lua")])}
    <p>O Eremita, por exemplo, com a sua lanterna, convida a parar e a ouvir-se, longe do barulho. A Estrela fala de esperança depois de um tempo difícil. A Lua mostra os medos e as dúvidas que crescem quando não há luz. Nenhuma destas cartas diz o que lhe vai acontecer amanhã. Todas ajudam a perceber onde está hoje.</p>
    <h2>Para que serve</h2>
    <ul>
      <li><b>Dar nome ao que sente.</b> Muitas vezes sabemos que algo não está bem, mas não conseguimos dizer o quê. Uma imagem ajuda a pôr palavras.</li>
      <li><b>Ver um problema de outro ângulo.</b> Uma relação, uma decisão, um medo antigo: a carta mostra uma perspetiva em que ainda não tinha pensado.</li>
      <li><b>Perceber padrões.</b> Quando a mesma carta, ou o mesmo tema, aparece vezes sem conta, vale a pena perguntar o que se está a repetir na sua vida.</li>
      <li><b>Escolher com mais calma.</b> Antes de uma decisão, as cartas ajudam a separar o que quer do que tem medo de perder.</li>
    </ul>
    <h2>Como é uma leitura com esta intenção</h2>
    <p>Numa consulta, começamos pela pergunta. Não precisa de ser bonita nem certa: «sinto-me preso no trabalho e não sei porquê» chega. Tiro as cartas e, antes de dizer o que eu leio nelas, pergunto-lhe muitas vezes o que vê. O que lhe salta à vista na imagem? Que sentimento lhe desperta? É dessa troca, entre o que as cartas mostram e o que a pessoa reconhece, que nasce a leitura.</p>
    <p>Uma tiragem simples, como as <a href="/tiragem-tres-cartas">três cartas</a> (o que pesa, o que ajuda, o próximo passo), costuma chegar. Para temas grandes, a <a href="/tiragem-cruz-celta">Cruz Celta</a> dá mais espaço. Pode experimentar sozinho no <a href="/tarot-gratis">Tarot Grátis</a> e levar as cartas que lhe saíram para a consulta.</p>
    <h2>O que o tarot terapêutico não é</h2>
    <p>Não é psicoterapia. Um psicólogo tem uma formação clínica, segue métodos comprovados e acompanha a pessoa ao longo do tempo; um tarólogo não faz isso, e eu não faço de conta que faço. O tarot também não cura doenças, não resolve sozinho um luto nem tira uma depressão. O que pode fazer é ajudar a pensar, acolher e dar coragem para dar o passo seguinte, que às vezes é precisamente pedir ajuda a um profissional de saúde.</p>
    {NOTA_SAUDE}
    <h2>Quando faz sentido</h2>
    <p>Faz sentido quando quer refletir sobre um momento da sua vida, preparar uma conversa difícil, perceber o que sente numa relação ou fechar um ciclo com mais serenidade. Há quem me procure exatamente por isso: não para saber o futuro, mas para se ouvir melhor. Se também quer conhecer-se melhor através das cartas, leia sobre <a href="/tarot-e-autoconhecimento">o tarot e o autoconhecimento</a>.</p>
  </section>
  <section class="cartao" style="text-align:center">
    <h2>Uma consulta para se ouvir</h2>
    <p>Por videochamada, chamada, áudio ou por escrito, em Fafe ou à distância. Os preços estão à vista na página da <a href="/consulta-de-tarot">consulta de tarot</a>.</p>
    <p class="promessa">Eu tenho a sua resposta!</p>
    <a class="cta" href="/consulta-de-tarot">🔮 Ver as consultas e os preços</a>
    <div class="ligas"><a href="/aconselhamento-espiritual">Aconselhamento espiritual</a><a href="/medos-e-receios">Medos e receios</a><a href="/tarot-para-decisoes">Tarot para decisões</a><a href="/arcanos">Os 22 Arcanos Maiores</a><a href="/carta-de-tarot">A sua carta de hoje</a></div>
  </section>"""
    faq = [
        ("O que é o tarot terapêutico?", "É uma forma de usar as cartas como espelho para a reflexão pessoal: em vez de prever o futuro, ajudam a pôr nome ao que se sente, a ver um problema de outro ângulo e a escolher com mais calma."),
        ("O tarot terapêutico substitui a psicoterapia?", "Não. O tarot não é terapia clínica e não substitui um psicólogo, um psiquiatra ou um médico. Em caso de sofrimento forte, procure ajuda profissional (SNS 24 em Portugal, CVV 188 no Brasil)."),
        ("Preciso de saber tarot para fazer uma leitura destas?", 'Não. Basta trazer a pergunta. O Mestre Alberto tira as cartas e conversa consigo sobre o que elas mostram. Se quiser, pode antes experimentar o <a href="/tarot-gratis">Tarot Grátis</a>.'),
        ("Que cartas aparecem mais nestas leituras?", "Todas podem aparecer. Os Arcanos Maiores, como O Eremita, A Estrela ou A Lua, costumam falar dos grandes temas interiores; os Menores, das situações do dia a dia."),
    ]
    return pagina("tarot-terapeutico", "Tarot terapêutico: as cartas como espelho | Mestre Alberto",
                  "Tarot terapêutico com o Mestre Alberto: as cartas como espelho para a reflexão pessoal. Para que serve, como é a leitura e o que não substitui.",
                  'Tarot <span class="az">terapêutico</span>', "As cartas como espelho: para se ouvir, pôr nome ao que sente e escolher com mais calma.",
                  "mestre-r15.jpg", corpo, faq, "Tarot terapêutico", "O Mestre Alberto de mãos juntas, concentrado, com o baralho do Genial Tarot")


def pagina_autoconhecimento():
    corpo = f"""  <section class="cartao texto">
    <p>Meu Querido Jardim de Almas! «Conhece-te a ti mesmo» estava escrito à entrada do templo de Delfos há mais de dois mil anos, e continua a ser o conselho mais difícil de seguir. O tarot pode ajudar neste caminho. Não porque saiba mais sobre si do que você, mas porque as imagens das cartas fazem perguntas que raramente fazemos a nós próprios.</p>
    <h2>O caminho do Louco</h2>
    <p>Os 22 Arcanos Maiores contam uma história: a viagem do Louco, que parte de mochila às costas sem saber o que o espera. Pelo caminho encontra o Mago, que lhe mostra o que é capaz de fazer; a Sacerdotisa, que lhe ensina a ouvir a intuição; a Força, que lhe mostra que a coragem também pode ser suave; a Torre, que derruba o que estava mal construído; e chega por fim ao Mundo, quando um ciclo se completa.</p>
    {cartas([("00-o-louco", "O Louco"), ("08-a-forca", "A Força"), ("16-a-torre", "A Torre"), ("21-o-mundo", "O Mundo")])}
    <p>Esta história é a de qualquer pessoa. Há fases em que somos o Louco, cheios de vontade e sem mapa. Há outras em que vivemos a Torre, quando alguma coisa cai e nos obriga a recomeçar. Saber em que ponto do caminho estamos já é uma forma de nos conhecermos. Pode ler cada uma destas cartas na página dos <a href="/arcanos">22 Arcanos Maiores</a>.</p>
    <h2>Três exercícios para fazer em casa</h2>
    <ol>
      <li><b>A carta do dia.</b> De manhã, tire uma carta (pode usar <a href="/carta-de-tarot">a carta de tarot do site</a>) e escreva numa linha o que ela lhe faz pensar. À noite, releia. Ao fim de um mês terá um diário de si próprio.</li>
      <li><b>A carta que o incomoda.</b> Escolha, entre as 22, a carta de que menos gosta. Pergunte-se porquê. O que nos incomoda numa imagem diz muitas vezes respeito a uma parte de nós que preferimos não ver.</li>
      <li><b>Três cartas para uma pergunta.</b> Faça uma pergunta sobre si, não sobre os outros («o que me impede de…?») e tire <a href="/tiragem-tres-cartas">três cartas</a>: o que está a acontecer, o que precisa de largar, o que pode fazer agora.</li>
    </ol>
    <h2>As cartas e o seu signo</h2>
    <p>A astrologia e o tarot falam a mesma língua de símbolos. Cada signo tem um arcano que lhe corresponde e, no seu <a href="/mapa-astral">mapa astral</a>, o Sol, a Lua e o <a href="/ascendente">Ascendente</a> mostram três faces diferentes de quem é. Muitas pessoas descobrem que se reconhecem mais na descrição do Ascendente do que na do signo solar, e isso já é autoconhecimento.</p>
    <h2>O que esperar, com honestidade</h2>
    <p>O tarot não lhe vai dizer quem é: essa resposta é sua. O que faz é pôr à sua frente imagens que despertam memórias, desejos e medos, e convidá-lo a olhar para eles com calma. Não há cartas boas e cartas más; há cartas que nos confortam e cartas que nos desafiam, e as segundas costumam ensinar mais.</p>
    <p>Também não é um atalho. Conhecer-se leva tempo, e às vezes pede a ajuda de um profissional. O tarot pode ser um companheiro nesse caminho, nunca um substituto.</p>
    {NOTA_SAUDE}
    <h2>Numa consulta</h2>
    <p>Quando alguém me procura para se conhecer melhor, a consulta é mais uma conversa do que uma previsão. Olhamos juntos para as cartas e para o momento da sua vida, e eu digo-lhe o que leio, com franqueza e carinho. Há 18 anos que leio as cartas. Se quiser ir mais fundo no lado da reflexão, leia sobre o <a href="/tarot-terapeutico">tarot terapêutico</a>.</p>
  </section>
  <section class="cartao" style="text-align:center">
    <h2>Conheça-se através das cartas</h2>
    <p>Comece pelo <a href="/tarot-gratis">Tarot Grátis</a> ou marque uma <a href="/consulta-de-tarot">consulta de tarot</a>, em Fafe ou à distância.</p>
    <p class="promessa">Eu tenho a sua resposta!</p>
    <a class="cta" href="/consulta-de-tarot">🔮 Marcar uma consulta</a>
    <div class="ligas"><a href="/espiritualidade">Espiritualidade</a><a href="/aconselhamento-espiritual">Aconselhamento espiritual</a><a href="/numerologia">Numerologia</a><a href="/signos-do-zodiaco">Os 12 signos</a><a href="/arcanos-menores">Os 56 Arcanos Menores</a></div>
  </section>"""
    faq = [
        ("O tarot ajuda no autoconhecimento?", "Pode ajudar. As imagens das cartas despertam perguntas, memórias e sentimentos, e convidam a olhar para eles com calma. A resposta sobre quem é continua a ser sua."),
        ("Como posso usar o tarot sozinho para me conhecer melhor?", 'Tire uma carta por dia e escreva o que ela lhe faz pensar, reflita sobre a carta que menos gosta, ou faça uma tiragem de três cartas sobre si. O site tem a <a href="/carta-de-tarot">carta do dia</a> e o <a href="/tarot-gratis">Tarot Grátis</a>.'),
        ("Existem cartas boas e cartas más?", "Não. Há cartas que confortam e cartas que desafiam. A Torre ou A Morte assustam à primeira vista, mas falam de mudança e de recomeço, não de desgraça."),
        ("O tarot substitui um psicólogo?", "Não. É uma ferramenta de reflexão, não terapia clínica. Para sofrimento emocional forte, procure um profissional de saúde."),
    ]
    return pagina("tarot-e-autoconhecimento", "Tarot e autoconhecimento: conhecer-se através das cartas",
                  "Como o tarot ajuda no autoconhecimento: o caminho do Louco, três exercícios para fazer em casa e o que esperar, com honestidade. Pelo Mestre Alberto.",
                  'Tarot e <span class="az">autoconhecimento</span>', "As cartas fazem as perguntas que raramente fazemos a nós próprios.",
                  "mestre-r18.jpg", corpo, faq, "Tarot e autoconhecimento", "O Mestre Alberto, sorridente, junto a uma porta para um jardim, com um livro")


# ═════════════════════════════════ imagens de partilha ═════════════════════════════════
def og(slug, foto, titulo, sub, cartas_lista=()):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    F = "/home/ricardo/horoscopo-video/fontes/"
    W, Hh = 1200, 630
    im = Image.new("RGB", (W, Hh))
    px = im.load()
    for y in range(Hh):
        for x in range(0, W, 4):
            t = x / W
            c = (int(14 + 30 * (1 - t)), int(14 + 12 * (1 - t)), int(48 + 40 * (1 - t)))
            for k in range(4): px[x + k, y] = c
    ft = Image.open(foto).convert("RGB")
    esc = Hh / ft.height
    ft = ft.resize((int(ft.width * esc), Hh), Image.LANCZOS)
    mask = Image.new("L", ft.size, 255)
    md = ImageDraw.Draw(mask)
    for x in range(160): md.line([(x, 0), (x, Hh)], fill=int(255 * x / 160))
    im.paste(ft, (W - ft.width, 0), mask)
    d = ImageDraw.Draw(im)
    cin = lambda n: ImageFont.truetype(F + "Cinzel.ttf", n)
    cor = ImageFont.truetype(F + "Cormorant-Italic.ttf", 40)
    for i, cfile in enumerate(cartas_lista):
        c = Image.open(cfile).convert("RGBA"); c = c.resize((96, int(96 * c.height / c.width)), Image.LANCZOS)
        c = c.rotate(-8 + i * 8, expand=True, resample=Image.BICUBIC)
        im.paste(c, (60 + i * 90, 398 - (8 if i == 1 else 0)), c)
    y = 70
    d.text((60, y), "GENIAL TAROT · MESTRE ALBERTO", font=cin(24), fill=(242, 201, 107)); y += 55
    tam = 64
    linhas = titulo.split("\n")
    while max(d.textlength(l, font=cin(tam)) for l in linhas) > 640: tam -= 2
    for l in linhas: d.text((60, y), l, font=cin(tam), fill=(255, 236, 190)); y += int(tam * 1.15)
    y += 10
    for l in sub.split("\n"): d.text((60, y), l, font=cor, fill=(225, 215, 245)); y += 46
    d.text((60, 585), "genialtarot.com", font=cin(22), fill=(242, 201, 107))
    im.save(os.path.join(AQUI, f"{slug}-og.jpg"), quality=86, optimize=True, progressive=True)


if __name__ == "__main__":
    B, usados = pagina_consulta()
    paginas = {"consulta-de-tarot": B, "canais-oficiais": pagina_canais(), "tarot-terapeutico": pagina_terapeutico(),
               "tarot-e-autoconhecimento": pagina_autoconhecimento()}
    for slug, s in paginas.items():
        assert "vidente" not in s.lower(), slug
        open(os.path.join(AQUI, f"{slug}.html"), "w", encoding="utf-8").write(s)
        corpo = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s[s.find("<body"):], flags=re.S)
        print(slug, len(re.sub(r"<[^>]+>", " ", corpo).split()), "palavras")
    print("preços usados:", [(p["nome"][:45], p["preco"], pix_valor(p)) for p in usados])
    FOT = "/media/veracrypt23/ObsidianS/CentralS/Central Claude/Capas YouTube/fontes/"
    if os.path.isdir(FOT):
        C = os.path.join(AQUI, "cartas")
        og("consulta-de-tarot", FOT + "07-sorri-bordeaux-consulta-online.png", "Consulta de Tarot\nem Portugal", "Em Fafe ou à distância\npreços à vista", [f"{C}/10-a-roda-da-fortuna.webp", f"{C}/19-o-sol.webp", f"{C}/17-a-estrela.webp"])
        og("canais-oficiais", FOT + "11-acolhedor-rosa-bracos-abertos.png", "Os canais\noficiais", "Nunca peço pagamentos\npor mensagem privada")
        og("tarot-terapeutico", FOT + "15-intenso-azul-marinho-maos-juntas.png", "Tarot\nterapêutico", "As cartas como espelho", [f"{C}/09-o-eremita.webp", f"{C}/17-a-estrela.webp", f"{C}/18-a-lua.webp"])
        og("tarot-e-autoconhecimento", FOT + "18-acolhedor-azul-porta-jardim.png", "Tarot e\nautoconhecimento", "O caminho do Louco", [f"{C}/00-o-louco.webp", f"{C}/08-a-forca.webp", f"{C}/21-o-mundo.webp"])
        print("imagens de partilha feitas")
    else:
        print("⚠️ cofre fechado: as imagens de partilha não foram refeitas")
