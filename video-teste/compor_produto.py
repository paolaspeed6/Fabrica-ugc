"""Compõe a foto real do anúncio (fundo branco) sobre um cenário: os pixels do produto ficam intactos."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
foto, fundo, saida, y_chao = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
larg_frac = float(sys.argv[5]) if len(sys.argv) > 5 else 0.94
im = Image.open(foto).convert("RGB")
a = np.asarray(im).astype(float)
m = 24; a[:m] = 255; a[-m:] = 255; a[:, :m] = 255; a[:, -m:] = 255  # tira marcas da borda
dist = 255 - a.min(axis=2)
caixa = Image.fromarray((dist > 40).astype("uint8") * 255).getbbox()
x0, y0, x1, y1 = caixa; y1 = min(a.shape[0], y1 + 25)  # inclui a sombra no chão
a = a[y0:y1, x0:x1]
bg = Image.open(fundo).convert("RGB"); W, H = bg.size
larg = int(W * larg_frac); alt = int(a.shape[0] * larg / a.shape[1])
a = np.asarray(Image.fromarray(a.astype("uint8")).resize((larg, alt), Image.LANCZOS)).astype(float)
x = (W - larg) // 2; y = int(H * y_chao) - alt
sombra = Image.new("L", bg.size, 0)
ImageDraw.Draw(sombra).ellipse([x + 20, y + alt - 40, x + larg - 20, y + alt - 8], fill=70)
bgn = np.asarray(Image.composite(Image.new("RGB", bg.size, (20, 15, 10)), bg, sombra.filter(ImageFilter.GaussianBlur(12)))).astype(float)
reg = bgn[y:y + alt, x:x + larg]
alfa = np.clip((255 - a.min(axis=2) - 110) / 60, 0, 1)[..., None]  # sólido = pixel original
reg[:] = alfa * a + (1 - alfa) * reg * a / 255  # claro/branco = multiplicar (some o branco, sombra escurece)
Image.fromarray(bgn.astype("uint8")).save(saida, quality=95); print(saida, larg, alt, x, y)
