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
(B / 'textos.json').write_text(json.dumps(T, ensure_ascii=False, indent=1)); print(len(T), 'produtos')
