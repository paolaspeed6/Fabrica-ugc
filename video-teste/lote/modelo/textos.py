"""Junta pNN-textos.json (Fichador) + links de afiliado em textos.json (formato da Lista 22/10 B). uso: python3 -I textos.py"""
import json
from pathlib import Path
B = Path(__file__).resolve().parent
LINKS = {l.split()[0]: l.split()[1] for l in (B / 'links.txt').read_text().split('\n') if l.strip()}
L = json.loads((B / 'links_afiliado.json').read_text()); T = {}
for f in sorted(B.glob('p??-textos.json')):
    k = f.name[:3]; p = json.loads(f.read_text()); lr = L[k]['r']
    leg_r = p['leg_r'] if lr in p['leg_r'] else p['leg_r'].replace('. #', f'. Link do produto: {lr} #', 1)
    assert lr in leg_r, (k, 'leg_r sem ". #"')
    T[k] = dict(slug=p['slug'], nome=p['nome'], link=LINKS[k[1:]], links=L[k], ac=p['ac'], a=p['a'], b=p['b'], r=p['r'], en=p['en'], ext=p['ext'],
                letras=p.get('letras', False), c=p['c'], leg_a=p['leg_a'], leg_b=p['leg_b'], leg_c=p['leg_c'], leg_r=leg_r)
    for v in 'abc': assert len(T[k][f'leg_{v}']) < 150, (k, v, len(T[k][f'leg_{v}']))
    for i, c in enumerate(p['b']['cenas']): assert c[0] and c[1], (k, 'b.cenas', i, 'linha grande vazia: o layout B quebra (Lista 11/11 B)')
import re  # 02/11: o layout desenha emoji como quadradinho (5 ganchos da Lista 02/11 A); tira emoji dos textos do vídeo
_e = re.compile(r'\s*[\U0001F300-\U0001FAFF\u2600-\u27BF]\ufe0f?')
def _sem(x, k=''):
    if isinstance(x, str): return x if k.startswith('leg_') else _e.sub('', x)
    if isinstance(x, list): return [_sem(i, k) for i in x]
    if isinstance(x, dict): return {kk: _sem(v, kk if not k else k) for kk, v in x.items()}
    return x
T = {p: {k: _sem(v, k) for k, v in d.items()} if isinstance(d, dict) else d for p, d in T.items()}
(B / 'textos.json').write_text(json.dumps(T, ensure_ascii=False, indent=1)); print(len(T), 'produtos')
