# Recorta o fundo branco da foto 01 (flood fill a partir das bordas) e monta a camada do cartão desfocado.
# uso: card.py foto01.jpg saida_prefixo [W] [--sem-recorte]
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
src, out = sys.argv[1], sys.argv[2]; W = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 290
sem = '--sem-recorte' in sys.argv
pad, r = 14, 28
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(int)
if not sem:
    clara = (a.min(axis=2) > 232) & ((a.max(axis=2) - a.min(axis=2)) < 18)
    lab, _ = ndimage.label(clara)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fundo = np.isin(lab, list(borda))
    alpha = np.where(fundo, 0, 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.2)))
    rgba = np.dstack([a.astype(np.uint8), alpha]); fg = Image.fromarray(rgba, 'RGBA')
    bb = fg.getbbox(); fg = fg.crop(bb)
else:
    fg = im.convert('RGBA')
    m = Image.new('L', fg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fg.width - 1, fg.height - 1), 18, fill=255); fg.putalpha(m)
fg.thumbnail((W - 2 * pad, W - 2 * pad), Image.LANCZOS)
H = W  # cartão quadrado
layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
d.rounded_rectangle((0, 0, W - 1, H - 1), r, fill=(255, 255, 255, 46), outline=(255, 255, 255, 110), width=2)
if not sem:  # sombra leve para os itens se destacarem do fundo borrado
    sh = Image.new('RGBA', layer.size, (0, 0, 0, 0)); sa = fg.split()[3].point(lambda v: v * 0.45)
    blk = Image.new('RGBA', fg.size, (0, 0, 0, 255)); blk.putalpha(sa)
    sh.alpha_composite(blk, ((W - fg.width) // 2 + 2, (H - fg.height) // 2 + 4)); sh = sh.filter(ImageFilter.GaussianBlur(5)); layer.alpha_composite(sh)
layer.alpha_composite(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
layer.save(out + '_fg.png')
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), r, fill=255); m.save(out + '_mask.png')
print(W, H)
