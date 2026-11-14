"""Sobe as fotos de um carrossel para o Drive (Fabrica Videos/<dia>/Redes Sociais/<nome>) e grava drive_links.json.
uso: python3 subir_carrossel.py carrosseis/<nome>/final AAAA-MM-DD "Carrossel <nome>" """
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'video-teste'))
import drive_backup as D

pasta_local, dia, nome = sys.argv[1:4]
tk = D.token(); p = D.pasta(tk, D.RAIZ, 'root')
for parte in [dia, 'Redes Sociais', nome]: p = D.pasta(tk, parte, p)
ja = {f['name'] for f in D.listar(tk, f"'{p}' in parents and trashed = false")}
for n in sorted(os.listdir(pasta_local), reverse=True):
    if n.endswith('.jpg') and n not in ja: D.enviar(tk, os.path.join(pasta_local, n), p, 'image/jpeg'); print('ok', n)
links = {f['name']: f"https://drive.google.com/file/d/{f['id']}/view" for f in D.listar(tk, f"'{p}' in parents and trashed = false")}
links['_pasta'] = f'https://drive.google.com/drive/folders/{p}'
json.dump(links, open(os.path.join(pasta_local, 'drive_links.json'), 'w'), indent=1); print(links['_pasta'])
