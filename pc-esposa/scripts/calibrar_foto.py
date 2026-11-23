r"""Calibra os limiares de FOTO do placar (placar.foto_score) offline.
Positivos: (a) par real (foto da página do Stanley x miniatura da lista) e (b) miniaturas "viradas página" (ampliadas, com
borrão, JPEG, corte e botões por cima) x a própria miniatura. Negativos: TODOS os outros pares de miniaturas reais
(prints de listas de Minhas Curtidas). Mostra a melhor separação; LIM_FORTE tem que ficar ACIMA do maior negativo.
"""
import glob, os, random, re, sys, io
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pylibs'))
from PIL import Image, ImageDraw, ImageFilter
import placar as P

BASE = os.path.dirname(os.path.abspath(__file__))
random.seed(7)


def thumbs(path, y0=442, passo=205, n=5):
    im = Image.open(path).convert('RGB')
    if im.size != (720, 1600):
        return []
    # só telas "Adicionar Produto > Minhas Curtidas > Mais Recente" sem rolar: sublinhado laranja da aba (y≈355) e "Mais Recente" laranja (y≈401)
    lar = lambda p: p[0] > 200 and 40 < p[1] < 140 and p[2] < 110
    if not (all(lar(im.getpixel((x, 355))) for x in range(220, 380, 20)) and lar(im.getpixel((205, 402))) is not None
            and sum(lar(im.getpixel((x, 401))) for x in range(195, 345)) > 12):
        return []
    out = []
    for k in range(n):
        y = y0 + passo * k
        t = im.crop((24, y, 196, y + 172))
        if P._prep(t) is not None:
            out.append(t)
    return out


def como_pagina(t):
    """Simula a foto grande da página: ampliada, recortada diferente, JPEG, botões redondos por cima."""
    s = random.uniform(2.6, 3.5)
    g = t.resize((int(t.width * s), int(t.height * s)), Image.LANCZOS)
    dx, dy = random.randint(-30, 30), random.randint(-30, 30)
    base = Image.new('RGB', (680, 560), (255, 255, 255))
    base.paste(g, ((680 - g.width) // 2 + dx, (560 - g.height) // 2 + dy))
    d = ImageDraw.Draw(base)
    for cx in (40, 440, 520, 600):
        d.ellipse((cx, 10, cx + 60, 70), fill=(150, 150, 150))
    base = base.filter(ImageFilter.GaussianBlur(random.uniform(0.4, 1.4)))
    b = io.BytesIO(); base.save(b, 'JPEG', quality=random.randint(55, 85)); b.seek(0)
    return Image.open(b).convert('RGB')


todas = []
vistos = set()
fontes = [os.path.join(BASE, 'gravacao', 'p12_lista_pag1.png')] + glob.glob(os.path.join(BASE, 'central', 'prints_atencao', '*.png')) \
    + glob.glob(os.path.join(BASE, 'gravacao', 'pend_*.png')) + glob.glob(os.path.join(BASE, 'central', 'prints', '*.png'))
for f in fontes:
    for t in thumbs(f):
        h = P._prep(t, 16).tobytes()[:300]
        if h in vistos:
            continue
        vistos.add(h)
        todas.append(t)
    if len(todas) >= 120:
        break
print(f'miniaturas únicas: {len(todas)}')

pos, neg = [], []
paginas = [como_pagina(t) for t in todas]
for i, t in enumerate(todas):
    pos.append(P.foto_score(paginas[i], t))
neg_pares = []
for i in range(len(todas)):
    for j in random.sample(range(len(todas)), min(25, len(todas))):
        if i != j:
            s = P.foto_score(paginas[i], todas[j])
            if s is not None:
                neg.append(s); neg_pares.append((s, i, j))
pos = [p for p in pos if p is not None]
pos.sort(); neg.sort()
q = lambda a, p: a[min(len(a) - 1, int(p * len(a)))]
print(f'POSITIVOS simulados: n={len(pos)} min={pos[0]} p5={q(pos, .05)} mediana={q(pos, .5)}')
print(f'NEGATIVOS (pares de produtos de prints diferentes): n={len(neg)} mediana={q(neg, .5)} p99={q(neg, .99)} MAX={neg[-1]}')
print('  distribuição dos negativos: <12:', sum(1 for s in neg if s < 12), '| 12-24:', sum(1 for s in neg if 12 <= s < 25), '| >=25:', sum(1 for s in neg if s >= 25),
      '(>=25 = quase certo que é o MESMO produto aparecendo em 2 prints, não falso positivo)')
dup = [(s, i, j) for s, i, j in neg_pares if s >= 25]
if dup:
    import numpy as np
    i, j = dup[0][1], dup[0][2]
    Image.fromarray(np.hstack([np.asarray(todas[i].resize((172, 172))), np.asarray(todas[j].resize((172, 172)))])).save(os.path.join(os.environ.get('TEMP', '.'), 'neg_alto.png'))
    print('  exemplo de negativo alto salvo em TEMP\\neg_alto.png (pares', dup[0][0], ')')
faixa = [(s, i, j) for s, i, j in neg_pares if 12 <= s < 25]
# agrupa miniaturas do MESMO produto (pontos >= 25, transitivo) e reavalia só os pares de produtos realmente diferentes
pai = list(range(len(todas)))
def raiz(a):
    while pai[a] != a:
        pai[a] = pai[pai[a]]; a = pai[a]
    return a
for s, i, j in neg_pares:
    if s >= 25:
        pai[raiz(i)] = raiz(j)
dif = [(s, i, j) for s, i, j in neg_pares if raiz(i) != raiz(j)]
print(f'  pares de produtos DIFERENTES (após agrupar iguais): {len(dif)} | máximo {max(s for s, _, _ in dif)} | >=12: {sum(1 for s, _, _ in dif if s >= 12)} | >=25: {sum(1 for s, _, _ in dif if s >= 25)}')
print('  produtos diferentes com pontos >= T:', {t: sum(1 for s, _, _ in dif if s >= t) for t in (12, 15, 18, 20, 22, 25, 30)})
print('  (faixa 12-24 antes de agrupar:', len(faixa), '— os que sobram em ">=12" acima são o que "média" aceitaria por engano)')

# par REAL: página do Stanley x miniaturas da lista de 12:28 (linha 1 = Stanley)
real = Image.open(os.path.join(BASE, 'gravacao', 'p1_produto.png')).convert('RGB')
pag = real.crop((int(720 * .04), int(1600 * .09), int(720 * .96), int(1600 * .43)))
ts = thumbs(os.path.join(BASE, 'gravacao', 'p12_lista_pag1.png'))
sc = [P.foto_score(pag, t) for t in ts]
print('REAL Stanley (linha1 = certa):', sc)
print(f'limiares atuais: forte >= {P.LIM_FORTE}, média >= {P.LIM_MEDIA}')
print('negativos >= média:', sum(1 for s in neg if s >= P.LIM_MEDIA), '| >= forte:', sum(1 for s in neg if s >= P.LIM_FORTE))
print('positivos >= média:', sum(1 for s in pos if s >= P.LIM_MEDIA), 'de', len(pos), '| >= forte:', sum(1 for s in pos if s >= P.LIM_FORTE))
