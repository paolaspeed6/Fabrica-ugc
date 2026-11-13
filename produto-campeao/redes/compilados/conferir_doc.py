"""Monta o doc da Conferir (página Postagens) para um vídeo de vários produtos.
Uso: python3 conferir_doc.py pedido.json video.mp4 drive_links.json docs_videos_dir saida.json "legenda" ordem
"""
import json, sys, subprocess, base64, os

ped, mp4, links, ddir, saida, legenda, ordem = sys.argv[1:8]
P = json.load(open(ped))
nome = os.path.basename(mp4)
url = json.load(open(links))[nome]
jpg = mp4 + '.jpg'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1', '-i', mp4, '-frames:v', '1', '-vf', 'scale=360:-1', '-q:v', '5', jpg], check=True)
poster = 'data:image/jpeg;base64,' + base64.b64encode(open(jpg, 'rb').read()).decode()
prods = [json.load(open(f"{ddir}/{it['video']}.json")) for it in P['itens']]
lk = [(p.get('links') or {}).get('A') or p.get('link_anuncio') for p in prods]
chave = nome[:-4]
doc = {'lote': 'Redes Sociais 13/11', 'dia': '2026-11-13', 'ordem': str(ordem), 'n': str(ordem),
       'produto': 'Vídeo com 4 produtos: ' + P['gancho'], 'link_anuncio': prods[0].get('link_anuncio', ''),
       'drive_a': url, 'drive_urls': {'A': url}, 'poster': poster, 'status': 'pendente', 'processado': False, 'enviado': False,
       'tipo': 'compilado', 'pedido': P['pedido'], 'videos': [it['video'] for it in P['itens']],
       'links_produtos': lk,
       'posts': {chave: {'conta': 'TikTok e Instagram', 'dia': '2026-11-13', 'drive_url': url, 'legenda': legenda,
                         'link_produto': lk[0], 'links_produtos': lk, 'ordem': str(ordem), 'poster': poster,
                         'produto': P['gancho'], 'versao': 'Vários produtos'}}}
json.dump(doc, open(saida, 'w'), ensure_ascii=False)
print(chave, url, len(poster))
