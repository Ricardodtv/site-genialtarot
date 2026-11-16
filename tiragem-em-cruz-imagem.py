"""Imagem própria da /tiragem-em-cruz (16/11/2026, O-473), no molde de tiragem-templo-de-afrodite-imagem.py:
as cinco cartas do exemplo da página, do baralho do Mestre Alberto, dispostas em cruz. Correr na pasta do repositório."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random
R = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1200, 675
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    for x in range(W):
        d = math.hypot((x - W/2)/W, (y - H/2)/H*1.1)
        t = min(1, d*1.7)
        c0, c1 = (52, 62, 140), (14, 16, 44)
        px[x, y] = tuple(int(c0[i] + (c1[i]-c0[i])*t) for i in range(3))
d = ImageDraw.Draw(img)
random.seed(16)
for _ in range(150):
    x, y = random.randint(0, W), random.randint(0, H); r = random.choice([1, 1, 1, 2])
    d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 240))
OURO = (232, 196, 110)
CLARO = (220, 225, 250)
cw, ch = 116, 194
gap = 18
cards = {1: "cartas/menores/three-of-wands.webp", 2: "cartas/menores/ten-of-wands.webp", 3: "cartas/14-a-temperanca.webp",
         4: "cartas/menores/six-of-wands.webp", 5: "cartas/07-o-carro.webp"}
cx, cy = W//2, H//2
x5, y5 = cx - cw//2, cy - ch//2
pos = {5: (x5, y5), 1: (x5 - cw - gap - 10, y5), 2: (x5 + cw + gap + 10, y5),
       3: (x5, y5 - ch//2 - gap - 70), 4: (x5, y5 + ch//2 + gap + 70)}
# a cruz em ouro por trás das cartas
d.line([(pos[1][0] - 30, cy), (pos[2][0] + cw + 30, cy)], fill=OURO, width=3)
d.line([(cx, pos[3][1] - 22), (cx, pos[4][1] + ch + 22)], fill=OURO, width=3)
fn = ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 22)
def carta(n, x, y, h=ch, brilho=False):
    w = cw
    c = Image.open(R + cards[n]).convert("RGB").resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (w+40, h+40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([20, 20, w+20, h+20], fill=(232, 196, 110, 120) if brilho else (0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(10 if brilho else 7)); img.paste(sh, (x-20, y-16), sh)
    img.paste(c, (x, y)); d.rectangle([x-1, y-1, x+w, y+h], outline=OURO, width=3 if brilho else 2)
    r = 16; bx, by = x + w - 6, y + 6
    d.ellipse([bx-r, by-r, bx+r, by+r], fill=(20, 24, 60), outline=OURO, width=2)
    d.text((bx, by), str(n), font=fn, fill=OURO, anchor="mm")
# as cartas de cima e de baixo ficam mais baixas para a cruz caber na altura
chv = 150
cw_v = int(chv * 480 / 804)
def carta_v(n, y):
    global cw
    old = cw; cw = cw_v; carta(n, cx - cw_v//2, y, chv); cw = old
carta_v(3, 22)
carta_v(4, H - 22 - chv)
for n in (1, 2): carta(n, *pos[n])
carta(5, *pos[5], brilho=True)
ft = ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 46)
fs = ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 22)
fp = ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 18)
lx = (pos[1][0] - 30) // 2
for i, t in enumerate(["Tiragem", "em Cruz"]):
    d.text((lx, 270 + i*60), t, font=ft, fill=OURO, anchor="mm")
d.text((lx, 400), "5 cartas · grátis", font=fs, fill=CLARO, anchor="mm")
rx = (pos[2][0] + cw + 30 + W) // 2
for i, (num, t) in enumerate([("1", "a favor"), ("2", "contra"), ("3", "o caminho"), ("4", "o resultado"), ("5", "a síntese")]):
    d.text((rx - 70, 220 + i*40), num, font=fs, fill=OURO, anchor="mm")
    d.text((rx - 50, 220 + i*40), t, font=fs, fill=CLARO, anchor="lm")
d.text((rx, 470), "Baralho do Mestre Alberto", font=fp, fill=(200, 205, 235), anchor="mm")
d.text((rx, 498), "genialtarot.com", font=fp, fill=OURO, anchor="mm")
img.save(R + "tiragem-em-cruz.webp", "WEBP", quality=86, method=6)
print(img.size)
