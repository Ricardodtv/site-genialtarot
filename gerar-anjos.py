#!/usr/bin/env python3
"""Páginas do tema Anjo da Guarda (05/11/2026): /anjo/<nome> (72), /carta-do-anjo, /anjo-da-guarda-criancas,
/dia-do-anjo-da-guarda e /anjo-de-portugal. Aparência copiada de anjo-da-guarda.html. Correr: python3 gerar-anjos.py"""
import datetime, html, importlib.util, json, math, os, re
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
_s = importlib.util.spec_from_file_location("t", "anjos-textos.py"); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
ANJOS = _m.ANJOS
BASE = open("anjo-da-guarda.html", encoding="utf8").read()
HEAD = BASE.split("</head>")[0]
ESTILOS = "\n".join(re.findall(r"(?s)<style>.*?</style>", HEAD))
TOPO = re.search(r'(?s)<body.*?(?=<section class="heroi">)', BASE).group(0)
CASA = re.search(r"(?s)<!-- gt-casa:inicio -->.*?<!-- gt-casa:fim -->", BASE).group(0)
ASA = re.search(r'(?s)<svg class="asa".*?</svg>', BASE).group(0)
SITE = "https://genialtarot.com"
COROS = ["Serafins", "Querubins", "Tronos", "Dominações", "Potestades", "Virtudes", "Principados", "Arcanjos", "Anjos"]
SIG = [("Carneiro","♈","carneiro"),("Touro","♉","touro"),("Gémeos","♊","gemeos"),("Caranguejo","♋","caranguejo"),("Leão","♌","leao"),("Virgem","♍","virgem"),
       ("Balança","♎","balanca"),("Escorpião","♏","escorpiao"),("Sagitário","♐","sagitario"),("Capricórnio","♑","capricornio"),("Aquário","♒","aquario"),("Peixes","♓","peixes")]
MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
slug = lambda n: n.lower()
EXTRA = """<style>
.fic{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.7rem;margin:0}.fic div{padding:.8rem;border-radius:.9rem;background:var(--vidro);border:1px solid var(--borda);text-align:center}
.fic dt{font-size:.8rem;color:var(--suave)}.fic dd{margin:.15rem 0 0;font-weight:700}
.cdia{display:grid;grid-template-columns:minmax(0,14rem) 1fr;gap:1.3rem;align-items:center}.cdia img{width:100%;height:auto;display:block;border-radius:.9rem}
.virar{all:unset;display:block;cursor:pointer;width:100%;border-radius:.9rem}.virar:focus-visible{outline:2px solid var(--ouro);outline-offset:3px}
#msg{display:none}#msg.ver{display:block;animation:surge .7s ease}@keyframes surge{from{opacity:0;transform:translateY(10px)}}
.fmail{max-width:30rem;margin:0 auto;text-align:left}.fmail label.c{display:block;font-weight:600;margin:.7rem 0 .25rem}.fmail input[type=text],.fmail input[type=email]{font:inherit;width:100%;box-sizing:border-box;padding:.7rem .9rem;border-radius:.8rem;border:1px solid var(--borda);background:oklch(0.16 0.05 270 / .7);color:var(--texto)}
.fmail .bt{display:block;width:100%}.fmail .er{color:oklch(0.8 0.15 25);min-height:1.2em;margin:.5rem 0 0;text-align:center}
@media(max-width:560px){.cdia{grid-template-columns:1fr}.cdia .virar{max-width:13rem;margin:0 auto}}
</style>"""

def sol(d):
    n = (datetime.datetime(d.year, d.month, d.day, 12) - datetime.datetime(2000, 1, 1, 12)).days
    g = math.radians(357.528 + .9856003 * n); L = 280.46 + .9856474 * n
    return (L + 1.915 * math.sin(g) + .02 * math.sin(2 * g)) % 360

DIAS = {}
_d = datetime.date(2027, 3, 21)
for _ in range(365):  # 09/11/2026: até 19/03/2028; os 366 dias davam «21 a 20 de Março» ao 1.º anjo
    if (_d.month, _d.day) != (2, 29): DIAS.setdefault(int(sol(_d) // 5), []).append(_d)  # 2027 não tem 29 de Fevereiro
    _d += datetime.timedelta(days=1)
def periodo(i):
    a, b = DIAS[i][0], DIAS[i][-1]
    if a.month == b.month: return f"{a.day} a {b.day} de {MESES[a.month-1]}"
    return f"{a.day} de {MESES[a.month-1]} a {b.day} de {MESES[b.month-1]}"

def pagina(cam, tit, des, corpo, ld=None, fim="", og="og-image.jpg", tipo="article"):
    url = SITE + cam; t = html.escape(tit, quote=True); d = html.escape(des, quote=True)
    ld = ld or {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": tit, "description": des, "inLanguage": "pt-PT", "mainEntityOfPage": url,
          "author": {"@type": "Person", "name": "Mestre Alberto"}, "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE}, "dateModified": datetime.date.today().isoformat()}]}
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{t}</title>
<meta name="description" content="{d}" />

<meta name="theme-color" content="#1d2350" />
<link rel="icon" href="/favicon.ico" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:type" content="{tipo}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/{og}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{ESTILOS}
{EXTRA}
</head>
{TOPO}{corpo}
{CASA}
<footer>
  Genial Tarot · Mestre Alberto · Leituras simbólicas, não substituem aconselhamento profissional.<br>
  <a href="/privacidade">Política de Privacidade</a> · <a href="/termos">Termos de Serviço</a>
</footer>
</div>
{fim}<script src="/vip-faixa.js" defer></script>
<script src="/vivo.js" defer></script>
</body>
</html>
"""

def heroi(h1, sub): return f'<section class="heroi">{ASA}<h1><span class="az">{h1}</span></h1><p class="sub">{sub}</p></section>'
def grava(f, s):
    open(f, "w", encoding="utf8").write(s)

# ─── 72 anjos ───
AVISO = ('<p><small>Os 72 anjos pertencem à tradição da Cabala e da angelologia, não à doutrina da Igreja, que desaconselha dar aos anjos nomes além de Miguel, Gabriel e Rafael. '
         'Quem segue a fé católica pode rezar ao seu <a href="/anjo-da-guarda">Anjo da Guarda</a> sem lhe saber o nome. É uma leitura simbólica: não promete resultados nem substitui o médico ou outros profissionais.</small></p>')
tamanhos = []
for i, (n, tema, ped, txt, gesto, ora) in enumerate(ANJOS):
    s, g, sl = SIG[i // 6]; coro = COROS[i // 8]; g0 = (i % 6) * 5
    tit = f"Anjo {n}: {tema}, datas e oração"
    des = f"{n}, anjo n.º {i+1} dos 72 Nomes: {tema[0].lower()+tema[1:]}. Veja as datas em {s}, o coro e uma oração para {ped}."
    if len(des) > 158: des = f"{n}, anjo n.º {i+1} dos 72 Nomes: {tema[0].lower()+tema[1:]}. Veja as datas em {s}, o coro e uma oração."
    tamanhos.append((len(tit), len(des)))
    ant, seg = ANJOS[(i + 71) % 72][0], ANJOS[(i + 1) % 72][0]
    ir = "".join(f'<a href="/anjo/{slug(ANJOS[k][0])}">{ANJOS[k][0]}</a>' for k in range(i // 6 * 6, i // 6 * 6 + 6) if k != i)
    corpo = f"""{heroi("Anjo " + n, f"{tema} · n.º {i+1} dos 72 Nomes")}
  <section class="cartao"><dl class="fic"><div><dt>Coro</dt><dd>{coro}</dd></div><div><dt>Signo</dt><dd>{g} {s}, {g0}° a {g0+5}°</dd></div><div><dt>Datas em 2027</dt><dd>{periodo(i)}</dd></div></dl>
    <p class="sub" style="font-size:.92rem;text-align:center;margin-top:.8rem">As datas seguem o grau real do Sol e podem mudar um dia de ano para ano.</p></section>
  <section class="cartao texto"><h2>Quem é {n}</h2><p>{txt}</p><p>Na tradição dos 72 Nomes, pede-se a {n} ajuda para {ped}.</p>
    <h2>Oração a {n}</h2><blockquote class="ora-c">{ora}<br>Amém.<footer>Oração simbólica, da tradição dos 72 Nomes</footer></blockquote>
    <h2>Um gesto para hoje</h2><p>{gesto}</p></section>
  <section class="cartao" style="text-align:center"><h2>Os outros anjos de {s}</h2><div class="ligas">{ir}</div>
    <div class="ligas"><a href="/anjo/{slug(ant)}">← {ant}</a><a href="/signo/{sl}">{g} {s}</a><a href="/anjo/{slug(seg)}">{seg} →</a></div>
    <p style="margin:.8rem 0"><a href="/os-72-anjos">Ver os 72 anjos, signo a signo</a></p>
    <a class="cta" href="/anjo-da-guarda#descobrir">Descobrir o meu anjo</a></section>
  <section class="cartao texto">{AVISO}</section>"""
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": tit, "description": des, "inLanguage": "pt-PT", "mainEntityOfPage": f"{SITE}/anjo/{slug(n)}",
          "author": {"@type": "Person", "name": "Mestre Alberto"}, "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE}},
          {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Anjo da Guarda", "item": SITE + "/anjo-da-guarda"}, {"@type": "ListItem", "position": 2, "name": f"Anjo {n}", "item": f"{SITE}/anjo/{slug(n)}"}]}]}
    grava(f"anjo/{slug(n)}.html", pagina("/anjo/" + slug(n), tit, des, corpo, ld))
assert len({x[0] for x in ANJOS}) == 72
print("título máx", max(t for t, _ in tamanhos), "descrição máx", max(d for _, d in tamanhos))

# ─── Carta do Anjo do dia ───
ARC = [("00-o-louco","arcano-00-o-louco","O Louco","Hoje o convite é dar um passo sem ter tudo planeado, com os pés bem assentes."),
 ("01-o-mago","arcano-01-o-mago","O Mago","Já tem nas mãos mais do que pensa. Olhe para o que tem e use-o."),
 ("02-a-sacerdotisa","arcano-02-a-sacerdotisa","A Sacerdotisa","Nem tudo precisa de ser dito hoje. Fique atento ao que sente em silêncio."),
 ("03-a-imperatriz","arcano-03-a-imperatriz","A Imperatriz","É um bom dia para cuidar: de si, da casa, do que está a crescer."),
 ("04-o-imperador","arcano-04-o-imperador","O Imperador","Ponha ordem no que depende de si. A estrutura também é uma forma de carinho."),
 ("05-o-hierofante","arcano-05-o-hierofante","O Hierofante","Vá buscar um conselho a quem já percorreu este caminho."),
 ("06-os-enamorados","arcano-06-os-enamorados","Os Enamorados","Há uma escolha do coração à sua frente. Escolha com verdade."),
 ("07-o-carro","arcano-07-o-carro","O Carro","Decida para onde vai e mantenha as rédeas na mão."),
 ("08-a-forca","arcano-08-a-forca","A Força","A brandura pode mais do que o grito. Hoje vença com calma."),
 ("09-o-eremita","arcano-09-o-eremita","O Eremita","Reserve um momento só para si. A resposta vem no recolhimento."),
 ("10-a-roda-da-fortuna","arcano-10-a-roda-da-fortuna","A Roda da Fortuna","As coisas mudam. Aproveite o que está a girar a seu favor e aceite o resto."),
 ("11-a-justica","arcano-11-a-justica","A Justiça","Pese bem antes de decidir e seja honesto consigo."),
 ("12-o-enforcado","arcano-12-o-enforcado","O Enforcado","Veja a situação de outro ângulo. Parar também é avançar."),
 ("13-a-morte","arcano-13-a-morte","A Morte","Algo pede para terminar. Deixar ir abre espaço ao que vem."),
 ("14-a-temperanca","arcano-14-a-temperanca","A Temperança","Procure o meio-termo. Hoje a medida certa vale mais do que a pressa."),
 ("15-o-diabo","arcano-15-o-diabo","O Diabo","Repare no que o prende por hábito. Dar-lhe nome já começa a soltar."),
 ("16-a-torre","arcano-16-a-torre","A Torre","Se algo abanar hoje, olhe para o que estava mal assente. Dá para reconstruir melhor."),
 ("17-a-estrela","arcano-17-a-estrela","A Estrela","Mantenha a esperança acesa. Um pequeno sinal de luz chega para continuar."),
 ("18-a-lua","arcano-18-a-lua","A Lua","Nem tudo o que teme é real. Espere pela luz do dia antes de concluir."),
 ("19-o-sol","arcano-19-o-sol","O Sol","Deixe entrar a alegria simples e partilhe-a com alguém."),
 ("20-o-julgamento","arcano-20-o-julgamento","O Julgamento","É hora de responder a um chamamento antigo e de se perdoar pelo passado."),
 ("21-o-mundo","arcano-21-o-mundo","O Mundo","Reconheça o que já completou. Um ciclo merece ser celebrado.")]
J_AN = json.dumps([[a[0], a[1], a[2], a[5], a[4]] for a in ANJOS], ensure_ascii=False, separators=(",", ":"))
J_AR = json.dumps(ARC, ensure_ascii=False, separators=(",", ":"))
CORPO_C = f"""{heroi("A Carta do Anjo", '<span id="hoje">A carta de hoje</span>')}
  <section class="cartao"><h2>A sua carta de hoje</h2><p class="sub" style="text-align:center">É uma só por dia, igual para todos os que a abrem hoje. Toque para a virar.</p>
    <div class="cdia"><button class="virar" id="vira" type="button" aria-label="Virar a carta do dia"><img id="img" src="/cartas/verso-gt.webp" width="969" height="1624" alt="Verso da carta" /></button>
    <div id="pre"><p>Respire fundo, pense em quem ou no que quer entregar hoje ao seu anjo, e vire a carta.</p></div>
    <div id="msg"><small id="m-ar"></small><h3 id="m-n" style="margin:.2rem 0;color:var(--ouro)"></h3><p id="m-t"></p><blockquote class="ora-c" id="m-o"></blockquote><p id="m-g"></p>
      <div class="ligas" style="justify-content:flex-start"><a id="l-an" href="#">Conhecer este anjo</a><a id="l-ar" href="#">Ler sobre esta carta</a><a id="l-wa" target="_blank" rel="noopener">Partilhar no WhatsApp</a></div></div></div>
    <noscript><p>Esta carta precisa de JavaScript ligado para aparecer.</p></noscript></section>
  <section class="cartao"><h2>Receber novidades do Mestre Alberto</h2>
    <form class="fmail" id="fm" novalidate><label class="c" for="nome">O seu nome</label><input type="text" id="nome" maxlength="80" autocomplete="given-name" />
      <label class="c" for="email">O seu email</label><input type="email" id="email" maxlength="120" autocomplete="email" />
      <label class="caixa-novidades" style="display:flex;gap:.6em;align-items:flex-start;font-size:.92em;line-height:1.4;margin:.6em 0;cursor:pointer;text-align:left"><input type="checkbox" id="novidades" style="width:1.15em;height:1.15em;min-width:0;padding:0;margin:.15em 0 0;flex:none;accent-color:oklch(0.85 0.13 88)" /><span>Quero receber novidades do Mestre Alberto por email (horóscopos, mapas e promoções). Pode cancelar quando quiser.</span></label>
      <button class="bt" type="submit">Quero receber</button><p class="er" id="er" role="alert"></p></form>
    <p id="ok" style="display:none;text-align:center">Obrigado! Já está na lista do Mestre Alberto.</p>
    <p class="sub" style="font-size:.85rem;text-align:center">Consulte a <a href="/privacidade">Política de Privacidade</a>.</p></section>
  <section class="cartao texto"><h2>Como funciona</h2><p>Cada dia junta um dos 72 anjos da tradição dos Nomes a um dos 22 Arcanos Maiores do baralho do Mestre Alberto. A combinação é tirada pela data e muda à meia-noite de Lisboa. É um convite à reflexão e não uma previsão.</p>{AVISO}</section>"""
JS_C = """<script>
const AN=%s,AR=%s;
const $=i=>document.getElementById(i);
function mistura(n,s){const v=[...Array(n).keys()];for(let i=n-1;i>0;i--){s=(s*1103515245+12345)%%2147483648;const j=s%%(i+1);[v[i],v[j]]=[v[j],v[i]]}return v}
const P=new Intl.DateTimeFormat("en-CA",{timeZone:"Europe/Lisbon",year:"numeric",month:"2-digit",day:"2-digit"}).format(new Date()).split("-").map(Number);
const dia=Math.floor(Date.UTC(P[0],P[1]-1,P[2])/864e5);
const pa=mistura(72,20261105),pr=mistura(22,19160513),a=AN[pa[dia%%72]],r=AR[pr[dia%%22]];
$("hoje").textContent="A carta de "+new Intl.DateTimeFormat("pt-PT",{timeZone:"Europe/Lisbon",day:"numeric",month:"long",year:"numeric"}).format(new Date());
let virada=false;
$("vira").onclick=()=>{if(virada)return;virada=true;$("img").src="/cartas/"+r[0]+".webp";$("img").alt="Carta "+r[2]+" do baralho do Mestre Alberto";
$("m-ar").textContent=r[2]+" com o anjo "+a[0];$("m-n").textContent=a[1];$("m-t").textContent=r[3];$("m-o").textContent="«"+a[3]+" Amém.»";$("m-g").textContent="Gesto de hoje: "+a[4];
$("l-an").href="/anjo/"+a[0].toLowerCase();$("l-ar").href="/"+r[1];$("l-wa").href="https://wa.me/?text="+encodeURIComponent("A carta do anjo de hoje é "+r[2]+" com "+a[0]+": https://genialtarot.com/carta-do-anjo?de=partilha");
$("pre").style.display="none";$("msg").classList.add("ver")};
$("fm").addEventListener("submit",async e=>{e.preventDefault();const n=$("nome").value.trim(),m=$("email").value.trim().toLowerCase(),er=t=>$("er").textContent=t;er("");
if(n.replace(/[^A-Za-zÀ-ÿ]/g,"").length<2)return er("Escreva o seu nome, por favor.");
if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]{2,}$/.test(m))return er("Escreva um email válido.");
if(!$("novidades").checked)return er("Sem a caixa marcada não guardamos o seu email.");
const b=$("fm").querySelector("button");b.disabled=true;
try{const r=await fetch("/notify",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({type:"vip",data:{name:n,email:m,date_of_birth:"",area:"👼 Carta do Anjo",novidades:true}})});if(!r.ok)throw 0;
$("fm").style.display="none";$("ok").style.display="block"}catch(x){b.disabled=false;er("Não consegui registar agora. Tente daqui a um minuto.")}});
</script>
<script src="/novidades-caixa.js" defer></script>
""" % (J_AN, J_AR)
grava("carta-do-anjo.html", pagina("/carta-do-anjo", "Carta do Anjo: a sua mensagem grátis de hoje", "Uma carta grátis por dia, com um dos 72 anjos, um Arcano do baralho do Mestre Alberto, uma oração curta e um gesto para hoje.", CORPO_C, fim=JS_C, tipo="website"))

# ─── Crianças e bebés ───
FAQ_K = [("Com que idade se pode ensinar a oração do Anjo da Guarda?", "Assim que a criança começa a repetir frases. A oração «Anjo da Guarda, minha companhia» é curta e rima, por isso costuma ser das primeiras a ficar na memória."),
         ("Como explicar o Anjo da Guarda a uma criança?", "Com palavras simples: é um amigo de Deus que a acompanha sempre, de dia e de noite. Evite usá-lo como ameaça ou como vigilante. Deve ser uma ideia que dá sossego, não medo."),
         ("O bebé já tem Anjo da Guarda antes do batizado?", "O Catecismo diz que, desde o início até à morte, a vida humana é rodeada pela proteção dos anjos (n.º 336), sem pôr essa proteção a depender do batizado."),
         ("Posso descobrir o anjo do meu filho pela data de nascimento?", "Sim, na tradição dos 72 Nomes, que é simbólica e não é doutrina da Igreja. Basta usar a calculadora da página do Anjo da Guarda.")]
CORPO_K = f"""{heroi("Anjo da Guarda das crianças e dos bebés", "Orações para o berço, para a noite e para o batizado")}
  <section class="cartao texto"><h2>Uma companhia desde o berço</h2><p>Para muitas famílias portuguesas e brasileiras, a primeira oração de uma criança é a do Anjo da Guarda. Jesus fala dos pequeninos e diz que os seus anjos «veem sempre a face» do Pai (Mateus 18,10). E o Catecismo da Igreja Católica ensina que, desde o início da vida, cada pessoa está rodeada pela proteção dos anjos (n.º 336).</p></section>
  <section class="cartao texto"><h2>Orações para rezar com as crianças</h2>
    <h3>A primeira de todas</h3><blockquote class="ora-c">Anjo da Guarda, minha companhia,<br>guardai a minha alma de noite e de dia.<footer>Oração tradicional</footer></blockquote>
    <h3>Santo Anjo do Senhor</h3><blockquote class="ora-c">Santo Anjo do Senhor, meu zeloso guardador,<br>se a ti me confiou a piedade divina,<br>sempre me rege, guarda, governa e ilumina.<br>Amém.<footer>Oração tradicional</footer></blockquote>
    <h3>Junto ao berço</h3><blockquote class="ora-c">Anjo da Guarda deste menino,<br>vela o seu sono, guarda o seu caminho.<br>Fica ao seu lado quando eu não puder,<br>hoje, amanhã e sempre que for preciso. Amém.<footer>Para os pais rezarem. Diga «desta menina» ou o nome do bebé.</footer></blockquote>
    <h3>No dia do batizado</h3><blockquote class="ora-c">Santo Anjo, hoje entregamos-te esta criança.<br>Ensina-a a amar, a ser verdadeira e a confiar.<br>Acompanha-a nos dias bons e nos dias difíceis.<br>Amém.<footer>Para os pais e padrinhos</footer></blockquote>
    <h3>Quando tem medo do escuro</h3><blockquote class="ora-c">Meu anjo amigo, fica aqui comigo.<br>Com a tua luz não tenho medo.<br>Boa noite, até amanhã. Amém.<footer>Para repetir com a criança, devagar</footer></blockquote>
    <h3>À saída para a escola</h3><blockquote class="ora-c">Anjo da Guarda, vai comigo hoje.<br>Ajuda-me a aprender, a brincar e a ser bom amigo.<br>Amém.<footer>Uma frase à porta de casa</footer></blockquote></section>
  <section class="cartao texto"><h2>Como criar o hábito em casa</h2>
    <ol class="passos"><li><b>Escolha um só momento.</b> Antes de dormir é o mais fácil, porque faz parte do ritual da noite.</li><li><b>Rezem juntos.</b> As crianças aprendem por imitação: diga a oração com ela, sem a corrigir.</li><li><b>Deixe-a falar com o anjo.</b> Pergunte por quem quer rezar hoje e deixe-a dizer por palavras suas.</li><li><b>Nunca use o anjo para assustar.</b> Frases como «o anjo está a ver o que fazes» transformam a companhia em vigilância.</li></ol></section>
  <section class="cartao texto"><h2>Uma lembrança para o batizado</h2><p>Uma das lembranças mais simples é escrever à mão a oração do berço num cartão, com o nome da criança e a data, assinada pelos pais e padrinhos. Guardada, um dia será ela a lê-la. E se quiser, procure o anjo da data de nascimento e escreva o nome no verso, como curiosidade da tradição dos 72 Nomes.</p></section>
  <section class="cartao texto"><h2>Perguntas frequentes</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ_K)}<p><small>⚠️ As orações são práticas espirituais e não substituem o médico nem outros profissionais.</small></p></section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/anjo-da-guarda">Anjo da Guarda</a><a href="/os-72-anjos">Os 72 Anjos</a><a href="/rezas-para-criancas">Rezas para Crianças</a><a href="/carta-do-anjo">Carta do Anjo</a></div></section>"""
LD_K = {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": "Anjo da Guarda das crianças: orações para o berço e o batizado", "inLanguage": "pt-PT", "mainEntityOfPage": SITE + "/anjo-da-guarda-criancas", "author": {"@type": "Person", "name": "Mestre Alberto"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_K]}]}
grava("anjo-da-guarda-criancas.html", pagina("/anjo-da-guarda-criancas", "Oração do Anjo da Guarda para Crianças: «Santo Anjo do Senhor»", "«Santo Anjo do Senhor», «Anjo da Guarda, minha companhia» e orações curtas para rezar com as crianças: no berço, no batizado, ao deitar e à saída para a escola.", CORPO_K, LD_K))

# ─── 2 de Outubro ───
CONTA = """<script>
const f=(m,d)=>{const h=new Date(),y=(h.getMonth()+1>m||(h.getMonth()+1===m&&h.getDate()>d))?h.getFullYear()+1:h.getFullYear(),a=new Date(y,m-1,d),n=Math.ceil((a-new Date(h.getFullYear(),h.getMonth(),h.getDate()))/864e5);
document.getElementById("cd").textContent=n?`Faltam ${n} dias para ${new Intl.DateTimeFormat("pt-PT",{weekday:"long",day:"numeric",month:"long",year:"numeric"}).format(a)}.`:"É hoje!"};f(%d,%d);
</script>
"""
CORPO_O = f"""{heroi("Dia do Anjo da Guarda", "2 de Outubro, festa dos Santos Anjos da Guarda")}
  <section class="cartao" style="text-align:center"><p id="cd" style="font-size:1.15rem;font-weight:700;margin:0"></p></section>
  <section class="cartao texto"><h2>Porque se celebra a 2 de Outubro</h2><p>A 2 de Outubro, a Igreja Católica lembra os Santos Anjos da Guarda. É o dia de agradecer a companhia que, na fé católica, cada pessoa recebe ao longo da vida. O Catecismo diz que «cada fiel tem ao seu lado um anjo como protetor e pastor» (n.º 336).</p>
    <p>A data calha três dias depois de 29 de Setembro, em que se celebram os arcanjos <a href="/sao-miguel-arcanjo">São Miguel</a>, São Gabriel e São Rafael.</p>
    <p>Na festa de 2014, o Papa Francisco falou do anjo como companheiro de viagem e deixou perguntas para cada um fazer a si próprio: como é a minha relação com o meu anjo? Dou-lhe os bons-dias de manhã? Peço-lhe que me guarde enquanto durmo?</p></section>
  <section class="cartao texto"><h2>Como viver este dia</h2><ol class="passos"><li><b>De manhã,</b> reze uma das orações tradicionais, antes de pegar no telemóvel.</li><li><b>Ao longo do dia,</b> agradeça por uma vez em que se sentiu protegido.</li><li><b>Com as crianças,</b> ensine-lhes a <a href="/anjo-da-guarda-criancas">primeira oração do Anjo da Guarda</a>.</li><li><b>À noite,</b> entregue ao seu anjo o que ficou por resolver.</li></ol>
    <blockquote class="ora-c">Santo Anjo do Senhor, meu zeloso guardador,<br>se a ti me confiou a piedade divina,<br>sempre me rege, guarda, governa e ilumina.<br>Amém.<footer>Oração tradicional</footer></blockquote></section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/anjo-da-guarda">Anjo da Guarda</a><a href="/os-72-anjos">Os 72 Anjos</a><a href="/anjo-de-portugal">Anjo de Portugal</a><a href="/carta-do-anjo">Carta do Anjo</a></div></section>"""
grava("dia-do-anjo-da-guarda.html", pagina("/dia-do-anjo-da-guarda", "Dia do Anjo da Guarda: 2 de Outubro e como o viver", "Porque se celebra o Dia do Anjo da Guarda a 2 de Outubro, o que diz o Catecismo, e como viver a data com orações e gestos simples.", CORPO_O, fim=CONTA % (10, 2)))

# ─── Anjo de Portugal ───
CORPO_P = f"""{heroi("Anjo de Portugal", "O Anjo Custódio, celebrado a 10 de Junho")}
  <section class="cartao" style="text-align:center"><p id="cd" style="font-size:1.15rem;font-weight:700;margin:0"></p></section>
  <section class="cartao texto"><h2>Um país com anjo próprio</h2><p>Portugal honra um Anjo da Guarda próprio, também chamado Anjo Custódio ou Anjo da Paz. A 10 de Junho, o dia de Portugal, é também a sua festa no calendário litúrgico português.</p>
    <h2>Uma história de séculos</h2><ul><li><b>Batalha:</b> no Mosteiro da Batalha, cuja construção começou em 1386, houve um altar dedicado ao Anjo da Guarda de Portugal.</li><li><b>1504:</b> a pedido do rei D. Manuel I, o Papa Júlio II instituiu a festa.</li><li><b>Depois do século XVII:</b> a devoção foi perdendo força.</li><li><b>1952:</b> foi restaurada oficialmente, e o Papa Pio XII inseriu a festa no calendário litúrgico português.</li></ul>
    <h2>O Anjo da Paz em Fátima</h2><p>Lúcia dos Santos e os primos Francisco e Jacinta Marto contaram que, em 1916, um ano antes das aparições de Nossa Senhora, um anjo os visitou três vezes. Apresentou-se como o Anjo da Paz e, segundo as memórias da Irmã Lúcia, ensinou-lhes orações. Esta é uma delas:</p>
    <blockquote class="ora-c">Meu Deus, eu creio, adoro, espero e amo-Vos.<br>Peço-Vos perdão para os que não creem, não adoram, não esperam e não Vos amam.<footer>Oração do Anjo, Fátima</footer></blockquote></section>
  <section class="cartao texto"><h2>Como viver o 10 de Junho</h2><ol class="passos"><li><b>Reze a oração do Anjo</b> três vezes, devagar.</li><li><b>Peça pelo país</b> e por quem vive longe dele: Portugal também é a sua diáspora.</li><li><b>Lembre-se de uma pessoa</b> de quem tem saudades e diga-lhe isso.</li></ol></section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/anjo-da-guarda">Anjo da Guarda</a><a href="/os-72-anjos">Os 72 Anjos</a><a href="/dia-do-anjo-da-guarda">Dia do Anjo da Guarda</a><a href="/sao-miguel-arcanjo">São Miguel Arcanjo</a></div></section>"""
grava("anjo-de-portugal.html", pagina("/anjo-de-portugal", "Anjo de Portugal: a história do Anjo Custódio e da oração", "O Anjo de Portugal: a festa de 10 de Junho, D. Manuel I, Pio XII, o Anjo da Paz em Fátima em 1916, e a oração que ensinou aos pastorinhos.", CORPO_P, fim=CONTA % (6, 10)))
# ─── Os 72 anjos, por signo (pedido dele, 05/11/2026: lista com ligações, mini resumo e o anjo de cada signo) ───
def resumo(a):
    return re.split(r"(?<=[.!?])\s", a[3])[0]
CHIPS = "".join(f'<a href="#{s[2]}">{s[1]} {s[0]}</a>' for s in SIG)
BLOCOS = ""
for n, (sg, sim, sl) in enumerate(SIG):
    its = "".join(f'<a class="an" href="/anjo/{slug(a[0])}"><span class="nr">{n * 6 + j + 1}</span><span class="tx"><b>{a[0]}</b><i>{a[1]} · {periodo(n * 6 + j)}</i><span>{resumo(a)}</span></span></a>' for j, a in enumerate(ANJOS[n * 6:n * 6 + 6]))
    BLOCOS += f'<section class="cartao" id="{sl}"><h2>{sim} Anjos de {sg}</h2><div class="anl">{its}</div><p style="text-align:center;margin:.8rem 0 0"><a href="/signo/{sl}">Ver o signo de {sg}</a></p></section>\n'
EST_L = """<style>
.chips{display:flex;flex-wrap:wrap;gap:.45rem;justify-content:center}.chips a{padding:.42rem .75rem;border-radius:99px;border:1px solid var(--borda);background:var(--vidro);color:inherit;text-decoration:none;font-weight:600;font-size:.92rem}.chips a:hover{border-color:var(--ouro);color:var(--ouro)}
.anl{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,21rem),1fr));gap:.7rem}.an{display:flex;gap:.7rem;padding:.8rem;border-radius:.9rem;background:var(--vidro);border:1px solid var(--borda);color:inherit;text-decoration:none}.an:hover{border-color:var(--ouro)}
.an .nr{flex:none;width:2.1rem;height:2.1rem;border-radius:50%;display:grid;place-items:center;border:1px solid var(--ouro);color:var(--ouro);font-weight:700;font-size:.85rem}
.an .tx{display:flex;flex-direction:column;gap:.15rem;min-width:0}.an b{color:var(--ouro);font-size:1.08rem}.an i{font-style:normal;font-size:.82rem;color:var(--suave)}.an .tx span{font-size:.95rem;line-height:1.4}
section[id]{scroll-margin-top:1rem}
.busca{max-width:30rem;margin:.6rem auto 1.1rem;text-align:left}.busca label{display:block;text-align:center;font-weight:600;margin-bottom:.4rem;color:var(--ouro)}.bc{display:flex;gap:.45rem}
.bc input{flex:1;min-width:0;font:inherit;font-size:1rem;padding:.72rem .95rem;border-radius:99px;border:1px solid var(--ouro);background:var(--vidro);color:inherit}.bc input::placeholder{color:var(--suave)}
.bc button{all:unset;cursor:pointer;padding:.72rem 1.05rem;border-radius:99px;background:var(--ouro);color:#1d1140;font-weight:700}.bc button:focus-visible,.br a:focus-visible{outline:2px solid #fff;outline-offset:2px}
.br a{display:flex;flex-direction:column;margin-top:.45rem;padding:.65rem .9rem;border-radius:.8rem;background:var(--vidro);border:1px solid var(--borda);color:inherit;text-decoration:none}.br a:hover{border-color:var(--ouro)}.br b{color:var(--ouro)}.br span{font-size:.88rem;color:var(--suave)}.br p{text-align:center;margin:.6rem 0 0}
</style>"""
J_BUSCA = json.dumps([[a[0], a[1], SIG[i // 6][0], "/anjo/" + slug(a[0])] for i, a in enumerate(ANJOS)] + [["Miguel", "São Miguel Arcanjo", "Arcanjo", "/sao-miguel-arcanjo"]], ensure_ascii=False, separators=(",", ":"))
BUSCA = """<form class="busca" id="bf" role="search" autocomplete="off"><label for="bi">Procurar um anjo pelo nome</label><div class="bc"><input id="bi" type="search" placeholder="Escreva o nome do anjo" enterkeyhint="search" aria-controls="br"><button type="submit">Procurar</button></div><div id="br" class="br" aria-live="polite"></div></form>"""
JS_L = """<script>(function(){var A=""" + J_BUSCA + """,i=document.getElementById("bi"),r=document.getElementById("br");
function n(t){return t.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase().trim()}
function e(t){var d=document.createElement("div");d.textContent=t;return d.innerHTML}
function acha(q){q=n(q);if(!q)return[];var a=A.filter(function(x){return n(x[0]).indexOf(q)===0}),b=A.filter(function(x){return n(x[0]).indexOf(q)>0}),c=q.length>2?A.filter(function(x){return n(x[1]).indexOf(q)>=0&&n(x[0]).indexOf(q)<0}):[];return a.concat(b,c).slice(0,6)}
i.addEventListener("input",function(){var q=i.value,l=acha(q);r.innerHTML=!q.trim()?"":l.length?l.map(function(x){return'<a href="'+x[3]+'"><b>'+e(x[0])+'</b><span>'+e(x[1])+' · '+e(x[2])+'</span></a>'}).join(""):'<p>Não encontrei esse anjo. Veja se o nome está bem escrito, ou procure na lista abaixo.</p>'});
document.getElementById("bf").addEventListener("submit",function(v){v.preventDefault();var l=acha(i.value);if(l.length)location.href=l[0][3]})})();</script>
"""
FAQ_L = [("O que são os 72 anjos?", "São 72 nomes que a Cabala tirou de três versículos do Êxodo (14,19-21). Mais tarde, cada nome foi ligado a um anjo e a 5 graus do zodíaco."),
         ("Como sei qual é o meu anjo?", "Pela data de nascimento: procure o seu signo nesta lista e veja em que datas cai o seu dia. Na página do Anjo da Guarda, a data de nascimento mostra-lhe o anjo diretamente."),
         ("Quantos anjos tem cada signo?", "Seis. Cada signo tem 30 graus e a cada 5 graus corresponde um anjo."),
         ("As datas de cada anjo são sempre as mesmas?", "Não exatamente. As datas seguem o grau real do Sol e podem mudar um dia de ano para ano, sobretudo perto do início e do fim de cada intervalo."),
         ("A Igreja Católica reconhece os 72 anjos?", "Não. Pertencem à tradição da Cabala e da angelologia. A Igreja desaconselha dar aos anjos nomes além de Miguel, Gabriel e Rafael, e quem segue a fé católica pode rezar ao seu Anjo da Guarda sem lhe saber o nome.")]
LD_L = {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": "Os 72 Anjos: lista completa e o anjo de cada signo", "description": "Os 72 anjos da tradição, organizados por signo: nome, tema, datas e um pequeno resumo de cada um, com ligação à sua oração e história.", "inLanguage": "pt-PT", "mainEntityOfPage": f"{SITE}/os-72-anjos",
          "author": {"@type": "Person", "name": "Mestre Alberto"}, "publisher": {"@type": "Organization", "name": "Genial Tarot", "url": SITE}, "dateModified": datetime.date.today().isoformat()},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_L]}]}
CORPO_L = f"""{EST_L}{heroi("Os 72 Anjos", "A lista completa: o anjo de cada signo, as suas datas e um pequeno resumo").replace(ASA, ASA + BUSCA)}
  <section class="cartao" style="text-align:center"><p>Cada signo tem 30 graus e a cada 5 graus corresponde um anjo, por isso cada signo reúne 6 dos 72. Escolha o seu signo e toque num anjo para ler a história, a oração e um gesto para hoje.</p><div class="chips">{CHIPS}</div><p style="margin:.9rem 0 0"><a class="bt" href="/anjo-da-guarda">Descobrir o meu anjo pela data de nascimento</a></p></section>
{BLOCOS}  <section class="cartao texto"><h2>Perguntas frequentes</h2>{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ_L)}</section>
  <section class="cartao">{AVISO}</section>
  <section class="cartao" style="text-align:center"><div class="ligas"><a href="/anjo-da-guarda">Anjo da Guarda</a><a href="/carta-do-anjo">Carta do Anjo</a><a href="/dia-do-anjo-da-guarda">Dia do Anjo da Guarda</a><a href="/anjo-de-portugal">Anjo de Portugal</a></div></section>
"""
grava("os-72-anjos.html", pagina("/os-72-anjos", "Os 72 Anjos: lista completa e o anjo de cada signo", "Os 72 anjos da tradição, organizados por signo: nome, tema, datas e um pequeno resumo de cada um, com ligação à sua oração e história.", CORPO_L, ld=LD_L, fim=JS_L))
print("feito")
# 12/11/2026: o texto próprio de cada anjo (bloco anjo-mais) volta a entrar depois de as 72 páginas serem refeitas
import subprocess as _sp; _sp.run(["python3", "anjos-mais.py"], check=False)
