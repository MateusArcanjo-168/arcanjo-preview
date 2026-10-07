"""Teste visual do efeito "estragado" feito por código.

Recorta uma grade 3x2 de comidas e gera uma comparação:
original / só filtro / filtro + efeitos.
- Comidas (índices 1-5): queimado (filtro marrom-escuro + carvão + fumaça).
- Bebidas (índice 0, café): azedo (filtro esverdeado + mofo + moscas + cheiro).

Os filtros reproduzem as funções CSS `filter` que o jogo usará.

Uso: python3 teste_estragado.py grade.png saida.png
"""
import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

src, out = sys.argv[1], sys.argv[2]
img = Image.open(src).convert("RGB")
W, H = img.size
cols, rows = 3, 2
tw, th = W // cols, H // rows
nomes = ["Café coado", "Pão de queijo", "Espaguete", "Misto quente", "Hambúrguer", "Pizza"]


# --- Matrizes dos filtros CSS (Filter Effects spec), para simular o navegador ---
def m_sepia(a):
    s = 1 - a
    return np.array([[0.393 + 0.607 * s, 0.769 - 0.769 * s, 0.189 - 0.189 * s],
                     [0.349 - 0.349 * s, 0.686 + 0.314 * s, 0.168 - 0.168 * s],
                     [0.272 - 0.272 * s, 0.534 - 0.534 * s, 0.131 + 0.869 * s]])


def m_saturate(s):
    return np.array([[0.213 + 0.787 * s, 0.715 - 0.715 * s, 0.072 - 0.072 * s],
                     [0.213 - 0.213 * s, 0.715 + 0.285 * s, 0.072 - 0.072 * s],
                     [0.213 - 0.213 * s, 0.715 - 0.715 * s, 0.072 + 0.928 * s]])


def m_hue(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return np.array([[0.213 + c * 0.787 - s * 0.213, 0.715 - c * 0.715 - s * 0.715, 0.072 - c * 0.072 + s * 0.928],
                     [0.213 - c * 0.213 + s * 0.143, 0.715 + c * 0.285 + s * 0.140, 0.072 - c * 0.072 - s * 0.283],
                     [0.213 - c * 0.213 - s * 0.787, 0.715 - c * 0.715 + s * 0.715, 0.072 + c * 0.928 + s * 0.072]])


def css_filter(tile):
    """filter: sepia(.6) hue-rotate(40deg) saturate(.7) brightness(.75)"""
    a = np.asarray(tile, dtype=np.float32) / 255.0
    for m in (m_sepia(0.6), m_hue(40), m_saturate(0.7)):
        a = np.clip(a @ m.T, 0, 1)
    a = np.clip(a * 0.75, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8))


def mofo(tile, seed):
    rnd = random.Random(seed)
    t = tile.convert("RGBA")
    camada = Image.new("RGBA", t.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    cx, cy = t.width / 2, t.height / 2
    for _ in range(16):
        ang, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 1) ** 0.5
        x, y = cx + math.cos(ang) * r * 150, cy + math.sin(ang) * r * 110
        rad = rnd.uniform(8, 24)
        cor = rnd.choice([(170, 185, 140, 150), (120, 135, 80, 160), (200, 205, 180, 130)])
        d.ellipse([x - rad, y - rad * 0.8, x + rad, y + rad * 0.8], fill=cor)
    camada = camada.filter(ImageFilter.GaussianBlur(4))
    return Image.alpha_composite(t, camada)


def moscas_e_cheiro(tile, seed):
    rnd = random.Random(seed + 100)
    t = tile.copy()
    d = ImageDraw.Draw(t, "RGBA")
    # linhas de mau cheiro (onduladas, verdes)
    for i in range(3):
        x0 = t.width / 2 - 70 + i * 70
        pts = [(x0 + math.sin(k / 6) * 10, 150 - k * 2.2) for k in range(0, 45)]
        d.line(pts, fill=(110, 160, 60, 210), width=7, joint="curve")
    # moscas
    for _ in range(3):
        x, y = rnd.uniform(110, 400), rnd.uniform(30, 140)
        d.ellipse([x - 16, y - 20, x + 2, y - 4], fill=(230, 240, 255, 170), outline=(90, 90, 110, 200), width=2)
        d.ellipse([x - 2, y - 20, x + 16, y - 4], fill=(230, 240, 255, 170), outline=(90, 90, 110, 200), width=2)
        d.ellipse([x - 9, y - 7, x + 9, y + 9], fill=(25, 25, 30, 255))
    return t



def css_queimado(tile):
    """filter: brightness(.55) sepia(1) saturate(2) brightness(.75) contrast(1.25)"""
    a = np.asarray(tile, dtype=np.float32) / 255.0
    a = a * 0.55
    for m in (m_sepia(1), m_saturate(2)):
        a = np.clip(a @ m.T, 0, 1)
    a = np.clip(a * 0.75, 0, 1)
    a = np.clip((a - 0.5) * 1.25 + 0.5, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8))


def carvao(tile, seed):
    rnd = random.Random(seed)
    t = tile.convert("RGBA")
    camada = Image.new("RGBA", t.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    cx, cy = t.width / 2, t.height / 2
    for _ in range(14):
        ang, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 1) ** 0.5
        x, y = cx + math.cos(ang) * r * 120, cy + math.sin(ang) * r * 85
        rad = rnd.uniform(10, 26)
        d.ellipse([x - rad, y - rad * 0.8, x + rad, y + rad * 0.8], fill=(15, 10, 8, rnd.randint(140, 200)))
    camada = camada.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(t, camada)


def fumaca(tile, seed):
    rnd = random.Random(seed + 7)
    t = tile.convert("RGBA")
    camada = Image.new("RGBA", t.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    for i in range(3):
        x0 = t.width / 2 - 80 + i * 80
        for k in range(9):
            y = 190 - k * 20
            x = x0 + math.sin(k / 1.6 + i) * 18
            rad = 14 + k * 3.2
            alpha = int(200 - k * 18)
            g = rnd.randint(140, 170)
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(g, g, g, alpha))
    camada = camada.filter(ImageFilter.GaussianBlur(7))
    return Image.alpha_composite(t, camada)


tiles = [img.crop((c * tw, r * th, (c + 1) * tw, (r + 1) * th)) for r in range(rows) for c in range(cols)]
liquido = {0}
leve, completo = [], []
for i, t in enumerate(tiles):
    if i in liquido:
        leve.append(css_filter(t))
        completo.append(moscas_e_cheiro(mofo(css_filter(t), i), i).convert("RGB"))
    else:
        leve.append(css_queimado(t))
        completo.append(fumaca(carvao(css_queimado(t), i), i).convert("RGB"))

S, label_w, head_h, pad = 230, 270, 50, 10
grid_rows = [("Original", tiles), ("Só filtro", leve), ("Filtro + efeitos\n(fumaça / carvão\nou mofo / moscas)", completo)]
nomes2 = ["Café (azedo)", "Pão de queijo", "Espaguete", "Misto quente", "Hambúrguer", "Pizza"]
canvas = Image.new("RGB", (label_w + 6 * (S + pad) + pad, head_h + 3 * (S + pad) + pad), (250, 247, 242))
d = ImageDraw.Draw(canvas)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
for i, n in enumerate(nomes2):
    x = label_w + pad + i * (S + pad)
    d.text((x + S / 2, head_h / 2), n, font=fs, fill=(60, 50, 40), anchor="mm")
for r, (rotulo, ts) in enumerate(grid_rows):
    y = head_h + pad + r * (S + pad)
    d.multiline_text((16, y + S / 2), rotulo, font=f, fill=(60, 50, 40), anchor="lm", spacing=6)
    for i, t in enumerate(ts):
        canvas.paste(t.resize((S, S), Image.LANCZOS), (label_w + pad + i * (S + pad), y))
canvas.save(out)
print(canvas.size)
