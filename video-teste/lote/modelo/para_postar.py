"""A dona, 27/10: os vídeos entram SEMPRE sozinhos em "Para postar" (coleção posts da Postagens), sem esperar o Ok dela.
Lê conferir_docs/*.json e grava para_postar/writes.json (lotes de até 48 escritas) para o ArtifactData batch:
posts/<arquivo> com status "pronto" + conferir/<id> com status "ok" (auto). Cartão "resgate" continua só na Conferência.
uso: python3 -I para_postar.py   (depois: ArtifactData batch com cada para_postar/writes_N.json, url da Postagens;
     conferir novo: escreva o conferir_doc já com status "ok" ou rode este script depois do batch dos conferir_docs com if_version 1)"""
import json, glob
from pathlib import Path
B = Path(__file__).resolve().parent; S = B / 'para_postar'; S.mkdir(exist_ok=True)
w = []
for f in sorted(glob.glob(str(B / 'conferir_docs/*.json'))):
    c = json.load(open(f))
    if c.get('tipo') == 'resgate' or not c.get('posts'): continue
    for pid, x in c['posts'].items():
        x = dict(x); x['poster'] = x.get('poster') or c.get('poster', ''); x['status'] = 'pronto'
        (S / f'{pid}.json').write_text(json.dumps(x, ensure_ascii=False))
        w.append({'op': 'set', 'collection': 'posts', 'doc_id': pid, 'file_path': str(S / f'{pid}.json')})
    w.append({'op': 'update', 'collection': 'conferir', 'doc_id': Path(f).stem, 'data': {'status': 'ok', 'auto': True}, 'if_version': 1})
for i in range(0, len(w), 48): (S / f'writes_{i // 48 + 1}.json').write_text(json.dumps(w[i:i + 48]))
print(len(w), 'escritas em', len(range(0, len(w), 48)), 'arquivo(s) em', S)
