"""Economia sem perder qualidade (a dona, 26/10). Grátis, sem IA paga e sem Claude:
1) mede a folha de cada cena pelo recorte do produto (rembg): % de folga à esquerda/direita/cima/baixo e % da largura;
   cena com produto encostando (folga < 3%) ou largo demais (> 88%) é REPROVADA aqui mesmo (fiscal_imagem.json, motivo "borda"),
   sem gastar Gemini nem Claude: foi o motivo nº 1 das reprovações da Lista 25/10 A;
2) monta pNN-cenas/folha.jpg: foto do anúncio + cenas A, B, C lado a lado, com as medidas escritas em cima.
   A Fiscal (Gemini e depois Sonnet) olha 1 imagem por produto em vez de 4 a 8.
uso: python3 -I folha.py p01,p02,...   (só cenas sem veredito; FORCAR=1 refaz tudo)"""
import json, os, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
B = Path(__file__).resolve().parent
_S = None
CORRIGIR_BORDA = ("The whole product (all items together) fills at most 60 percent of the frame width, with at least 12 percent empty space on the "
                  "left and on the right and clear space above and below; the camera stands farther back so nothing touches the frame edges.")


def mascara(img):
    global _S
    from rembg import remove, new_session
    _S = _S or new_session('u2net')
    return np.array(remove(img, session=_S, only_mask=True)) > 128


def medir(img):
    m = mascara(img); ys, xs = np.where(m)
    if not len(xs): return None
    W, H = m.shape[1], m.shape[0]
    return dict(esq=round(xs.min() / W * 100, 1), dir=round((W - 1 - xs.max()) / W * 100, 1), cima=round(ys.min() / H * 100, 1),
                baixo=round((H - 1 - ys.max()) / H * 100, 1), largura=round((xs.max() - xs.min()) / W * 100, 1))


def fonte(n):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf'):
        if os.path.exists(f): return ImageFont.truetype(f, n)
    return ImageFont.load_default()


def referencia(p):
    f = json.loads((B / f'{p}-ficha.json').read_text())
    for r in (f.get('fotos_ref') or []):
        q = B / f'{p}-fotos' / (r if str(r).endswith('.jpg') else f'{r}.jpg')
        if q.exists(): return q
    for n in ('01_limpa.jpg', '01.jpg'):
        if (B / f'{p}-fotos' / n).exists(): return B / f'{p}-fotos' / n


def produto(p):
    d = B / f'{p}-cenas'; fj = d / 'fiscal_imagem.json'; fi = json.loads(fj.read_text()) if fj.exists() else {}
    H = 640; quadros, med = [], {}
    ref = Image.open(referencia(p)).convert('RGB'); ref.thumbnail((H, H)); quadros.append(('ANÚNCIO', ref, None))
    for c in 'ABC':
        q = d / f'{c}.jpg'
        if not q.exists(): continue
        im = Image.open(q).convert('RGB'); m = medir(im); med[c] = m
        if m and (min(m['esq'], m['dir']) < 3 or m['largura'] > 88) and (os.environ.get('FORCAR') or c not in fi):
            fi[c] = dict(veredito='REPROVADO', provas=f"borda medida por código: folga esq {m['esq']}%, dir {m['dir']}%, largura {m['largura']}%",
                         corrigir_prompt=CORRIGIR_BORDA, risco_animacao='', fiscal='folha.py (rembg)')
        t = im.copy(); t.thumbnail((H * 9 // 16 + 1, H)); quadros.append((c, t, m))
    fj.write_text(json.dumps(fi, ensure_ascii=False, indent=1))
    Wt = sum(q[1].width for q in quadros) + 12 * (len(quadros) + 1)
    folha = Image.new('RGB', (Wt, H + 70), (245, 245, 245)); dr = ImageDraw.Draw(folha); x = 12; fn = fonte(18)
    for nome, im, m in quadros:
        folha.paste(im, (x, 60)); txt = nome if not m else f"{nome}  esq {m['esq']:.0f}% dir {m['dir']:.0f}% larg {m['largura']:.0f}%"
        cor = (190, 30, 30) if m and (min(m['esq'], m['dir']) < 3 or m['largura'] > 88) else (20, 20, 20)
        dr.text((x, 20), txt, fill=cor, font=fn); x += im.width + 12
    folha.save(d / 'folha.jpg', quality=85)
    return med


if __name__ == '__main__':
    for p in sys.argv[1].split(','):
        m = produto(p)
        print(p, ' '.join(f"{c}:{v['largura']:.0f}%/{min(v['esq'], v['dir']):.0f}%" for c, v in m.items() if v), flush=True)
