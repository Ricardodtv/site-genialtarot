#!/usr/bin/env python3
"""Regra dele (06/11/2026): em todos os cartões da página inicial, atuais e novos, o rosto fica no centro da imagem.
Procura o rosto de cada foto de .porta-foto e escreve --fx, --fy e --ar no cartão; o CSS de .porta-foto.foco faz o resto.
Corre no pre-commit quando entra o index.html. Foto sem rosto fica como está; capa de vídeo (data-video) muda sozinha e fica de fora.
Modelo: ~/.cache/genialtarot/yunet.onnx (YuNet, OpenCV Zoo). Sem ele avisa e não mexe em nada."""
import os, re, sys
import numpy as np, cv2
from PIL import Image
RAIZ = os.path.dirname(os.path.abspath(__file__)); PAG = os.path.join(RAIZ, "index.html")
MODELO = os.path.expanduser("~/.cache/genialtarot/yunet.onnx")
CONF, ALTURA = 0.85, 0.10   # abaixo disto são desenhos nos signos ou caras no fundo: medido nas 16 fotos a 06/11
# Fotos cortadas na origem, onde centrar à risca deixava só o rosto: fica o centro do ficheiro, já recortado à mão.
FIXO = {"atracao-amor-cartao.webp": (0.5, 0.5, 0.5, 1.5)}
FORMATOS = {"computador": 3 / 2, "telemovel": 2 / 1}

def rosto(f):
    im = Image.open(f).convert("RGB"); w, h = im.size; e = 960 / max(w, h)
    a = cv2.cvtColor(np.array(im.resize((int(w * e), int(h * e)))), cv2.COLOR_RGB2BGR); H, W = a.shape[:2]
    d = cv2.FaceDetectorYN_create(MODELO, "", (W, H), 0.6, 0.3, 50); _, r = d.detect(a)
    bons = [(x[0] + x[2] / 2, x[1] + x[3] / 2, x[3]) for x in (r if r is not None else []) if x[-1] >= CONF and x[3] / H >= ALTURA]
    if not bons: return None
    x, y, a_ = max(bons, key=lambda b: b[2]); return x / W, y / H, a_ / H, w / h

def peso(fx, fy, alt, ar, fr):
    """Quanto da altura do cartão o rosto ocupa depois de centrado."""
    return alt * max(1 / (2 * min(fy, 1 - fy)), fr / (2 * min(fx, 1 - fx) * ar), 1, fr / ar)

def main():
    if not os.path.exists(MODELO): print("cartoes-foco: falta o modelo " + MODELO, file=sys.stderr); return
    s = o = open(PAG, encoding="utf-8").read()
    def troca(m):
        cl, st, img = m.group(1), m.group(2), m.group(3)
        if "data-video" in img: return m.group(0)
        src = re.search(r'src="/([^"]+)"', img).group(1); f = os.path.join(RAIZ, src)
        r = FIXO.get(src) or (rosto(f) if os.path.exists(f) else None)
        st = re.sub(r"--(fx|fy|ar):[^;]*;?", "", st).rstrip(";"); cl = re.sub(r"\s*foco\b", "", cl)
        if r:
            fx, fy, alt, ar = r; cl += " foco"; st += f";--fx:{fx:.3f};--fy:{fy:.3f};--ar:{ar:.3f}"
            for n, fr in FORMATOS.items():
                p = peso(fx, fy, alt, ar, fr)
                if p > 0.95: print(f"cartoes-foco: {src} no {n}: o rosto ocupa {p:.0%} da altura do cartão, precisa de foto com mais margem", file=sys.stderr)
        return f'<span class="{cl}" style="{st}">{img}'
    s = re.sub(r'<span class="(porta-visual porta-foto[^"]*)" style="([^"]*)">(<img [^>]+>)', troca, s)
    if s != o: open(PAG, "w", encoding="utf-8").write(s); print("index.html")

if __name__ == "__main__": main()
