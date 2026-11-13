"""Varredura diária -> docs do Tinder (coleção candidatos) com link de afiliado Vp.
uso: python3 semear_diaria.py AAAA-MM-DD   (lê candidatos-<data>.json, grava listas/<DDMM>_varredura_docs/)"""
import json, sys, time, glob, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendas'))
from link_subid import link
dia = sys.argv[1]; aa, mm, dd = dia[2:4], dia[5:7], dia[8:10]
d = json.load(open(f'candidatos-{dia}.json'))
fora = set()
E = json.load(open('excluidos.json'))
for v in E.values(): fora |= set(map(str, v))
fora |= set(map(str, json.load(open('vistos.json'))))
for f in glob.glob('listas/*_docs/*.json'): fora.add(os.path.basename(f)[:-5])
pasta = f'listas/{dd}{mm}_varredura_docs'; os.makedirs(pasta, exist_ok=True)
ok, n, fo = [], 0, 0
for x in d:
    if str(x['id']) in fora: fo += 1; continue
    n += 1; url = None
    for t in range(6):
        try: s, url = link(x['link'], f'Vp{n:03d}', '', f'{aa}{mm}{dd}'); break
        except Exception: time.sleep(10 * (t + 1))
    if not url: n -= 1; print('sem link', x['id']); continue
    doc = {k: v for k, v in x.items() if k != 'id'}
    doc.update(link_afiliado=url, sub_id=s, dia=dia, ordem=n, origem='varredura')
    json.dump(doc, open(f'{pasta}/{x["id"]}.json', 'w'), ensure_ascii=False); ok.append(str(x['id']))
print(len(ok), 'semeados;', fo, 'fora (Kevin/repetidos)')
json.dump(ok, open(f'{pasta}.ids.json', 'w'))
