"""Varredura diária -> docs do Tinder (coleção candidatos) com link de afiliado Vp.
uso: python3 semear_diaria.py AAAA-MM-DD [tarde]   (lê candidatos-<data>.json, grava listas/<DDMM>_varredura_docs/)
2 varreduras por dia (a dona, 15/11): a da tarde continua a numeração do Sub ID e grava os ids em <DDMM>_varredura_docs_tarde.ids.json."""
import json, sys, time, glob, os, base64, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendas'))
from link_subid import link
tarde = len(sys.argv) > 2 and sys.argv[2] == 'tarde'
dia = sys.argv[1]; aa, mm, dd = dia[2:4], dia[5:7], dia[8:10]
d = json.load(open(f'candidatos-natal-{dia}.json'))
fora = set()
E = json.load(open('excluidos.json'))
for v in E.values(): fora |= set(map(str, v))
fora |= set(map(str, json.load(open('vistos.json'))))
for f in glob.glob('listas/*_docs/*.json'): fora.add(os.path.basename(f)[:-5])
pasta = f'listas/{dd}{mm}_natal_docs'; os.makedirs(pasta, exist_ok=True)
ok, fo = [], 0
n = len(glob.glob(f'{pasta}/*.json'))  # continua a numeração (Vp) da varredura da manhã
for x in d:
    if str(x['id']) in fora: fo += 1; continue
    n += 1; url = None
    for t in range(6):
        try: s, url = link(x['link'], f'Vn{n:03d}', '', f'{aa}{mm}{dd}'); break
        except Exception: time.sleep(10 * (t + 1))
    if not url: n -= 1; print('sem link', x['id']); continue
    doc = {k: v for k, v in x.items() if k != 'id'}
    f = doc.get('foto') or ''
    if f.startswith('data:image') and len(f) > 25000:  # 15/11: fotos grandes encheram o banco do Tinder (a lista parou de carregar)
        try:
            from PIL import Image
            im = Image.open(io.BytesIO(base64.b64decode(f.split(',', 1)[1]))).convert('RGB'); im.thumbnail((420, 420))
            b = io.BytesIO(); im.save(b, 'JPEG', quality=62); doc['foto'] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
        except Exception: pass
    doc.update(link_afiliado=url, sub_id=s, dia=dia, ordem=n, origem='natal', natal=True)
    json.dump(doc, open(f'{pasta}/{x["id"]}.json', 'w'), ensure_ascii=False); ok.append(str(x['id']))
print(len(ok), 'semeados;', fo, 'fora (Kevin/repetidos)')
json.dump(ok, open(f'{pasta}_tarde.ids.json' if tarde else f'{pasta}.ids.json', 'w'))
