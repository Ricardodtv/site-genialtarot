from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
R = "/home/ricardo/site-genialtarot/"
W, H = 1200, 675
img = Image.new("RGB", (W, H))
px = img.load()
# fundo azul-noite em gradiente radial
for y in range(H):
    for x in range(W):
        d = math.hypot((x - W/2)/W, (y - 120)/H*1.2)
        t = min(1, d*1.6)
        c0, c1 = (52, 62, 140), (14, 16, 44)
        px[x, y] = tuple(int(c0[i] + (c1[i]-c0[i])*t) for i in range(3))
d = ImageDraw.Draw(img)
import random; random.seed(7)
for _ in range(140):
    x, y = random.randint(0, W), random.randint(0, H); r = random.choice([1, 1, 1, 2])
    d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 240))
OURO = (232, 196, 110)
cw, ch = 88, 147
cards = {1: "cartas/menores/two-of-swords.webp", 2: "cartas/menores/ace-of-cups.webp", 3: "cartas/menores/knight-of-wands.webp",
         4: "cartas/09-o-eremita.webp", 5: "cartas/menores/six-of-cups.webp", 6: "cartas/menores/four-of-pentacles.webp",
         7: "cartas/17-a-estrela.webp"}
cx = W//2
xl, xc, xr = cx - 60 - cw - cw//2, cx - cw//2, cx + 60 + cw//2
ys = [140, 140+ch+14, 140+2*(ch+14)]
# frontão (o telhado do templo)
top, base = 22, 122
d.polygon([(cx, top), (xl-40, base), (xr+cw+40, base)], outline=OURO, width=4)
d.line([(xl-40, base+4), (xr+cw+40, base+4)], fill=OURO, width=2)
# degraus
yb = ys[2]+ch+10
d.line([(xl-40, yb), (xr+cw+40, yb)], fill=OURO, width=3)
d.line([(xl-60, yb+8), (xr+cw+60, yb+8)], fill=OURO, width=2)
fn = ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 22)
def carta(n, x, y):
    c = Image.open(R + cards[n]).convert("RGB").resize((cw, ch), Image.LANCZOS)
    sh = Image.new("RGBA", (cw+30, ch+30), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([15, 15, cw+15, ch+15], fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(7)); img.paste(sh, (x-12, y-9), sh)
    img.paste(c, (x, y)); d.rectangle([x-1, y-1, x+cw, y+ch], outline=OURO, width=2)
    r = 15; bx, by = x + cw - 6, y + 6
    d.ellipse([bx-r, by-r, bx+r, by+r], fill=(20, 24, 60), outline=OURO, width=2)
    d.text((bx, by), str(n), font=fn, fill=OURO, anchor="mm")
for i, n in enumerate([1, 2, 3]): carta(n, xl, ys[i])
for i, n in enumerate([4, 5, 6]): carta(n, xr, ys[i])
carta(7, xc, ys[1])
# textos dos lados
ft = ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 44)
fs = ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 22)
lx = (xl - 60) // 2
for i, t in enumerate(["Templo", "de", "Afrodite"]):
    d.text((lx, 250 + i*58), t, font=ft, fill=OURO, anchor="mm")
d.text((lx, 440), "tiragem do amor", font=fs, fill=(220, 225, 250), anchor="mm")
d.text((lx, 470), "7 cartas", font=fs, fill=(220, 225, 250), anchor="mm")
rx = (xr + cw + 60 + W) // 2
for i, t in enumerate(["1 · 2 · 3", "você", "", "4 · 5 · 6", "a outra pessoa", "", "7", "o rumo"]):
    d.text((rx, 240 + i*30), t, font=fs, fill=OURO if any(ch_.isdigit() for ch_ in t) else (220, 225, 250), anchor="mm")
d.text((rx, 560), "Baralho do Mestre Alberto", font=ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 18), fill=(200, 205, 235), anchor="mm")
d.text((rx, 588), "genialtarot.com", font=ImageFont.truetype("/home/ricardo/horoscopo-video/fontes/Cinzel.ttf", 18), fill=OURO, anchor="mm")
img.save(R + "tiragem-templo-de-afrodite.webp", "WEBP", quality=86, method=6)
print(img.size)
