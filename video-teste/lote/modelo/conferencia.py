"""Passo 13 (obrigatório, a dona 2026-10-24): monta um doc por produto para a página Conferência.
Lê final/drive_links.json (drive_backup.py) + textos.json (textos.py) + links.txt e grava conferir_docs/<LOTE>-<NN>.json
no formato do kit (lote, dia, ordem, n, produto, link_anuncio, drive_a, poster 240 px, status pendente).
Depois: ArtifactData batch (set, coleção "conferir", doc_id = nome do arquivo sem .json) na página POSTAGENS (MINHAS_PAGINAS.md).
A dona confere na aba "Conferir" da Postagens: Ok cria sozinho os posts (campo posts) em "Para postar", sem o Claude (a dona, 27/10).
uso: python3 -I conferencia.py "Lista 24/10 A" 2026-10-24"""
import base64, json, subprocess, sys
from pathlib import Path
B = Path(__file__).resolve().parent
nome_lote, dia = sys.argv[1], sys.argv[2]
pre = B.name.replace('lista', '').upper()
drive = {k: v for k, v in json.loads((B / 'final' / 'drive_links.json').read_text()).items() if (B / 'final' / k).exists()}  # só o que está em final/ (aprovado e inteiro)
T = json.loads((B / 'textos.json').read_text())
LINKS = {l.split()[0]: l.split()[1] for l in (B / 'links.txt').read_text().splitlines() if l.strip() and '<loja>' not in l}
out = B / 'conferir_docs'; out.mkdir(exist_ok=True)
for k, t in sorted(T.items()):
    nn = k[1:]
    a = next((f for f in sorted(drive) if f.startswith(f'{pre}_{nn}_') and f[-6:] in ('_A.mp4', '_B.mp4', '_C.mp4')), None)  # 1º aprovado (A, B ou C)
    if not a: continue  # entrega em partes (de 15 em 15): só os que já estão no Drive
    jpg = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '0.05', '-i', str(B / 'final' / a), '-frames:v', '1', '-vf', 'scale=240:-2',
                          '-q:v', '5', '-f', 'image2', '-c:v', 'mjpeg', '-'], capture_output=True, check=True).stdout
    doc = dict(lote=nome_lote, dia=dia, ordem=int(nn), n=int(nn), produto=t['nome'], link_anuncio=LINKS[nn], drive_a=drive[a],
               drive_urls={v: drive[a[:-5] + f'{v}.mp4'] for v in 'ABC' if a[:-5] + f'{v}.mp4' in drive},
               poster='data:image/jpeg;base64,' + base64.b64encode(jpg).decode(), status='pendente', processado=False, enviado=False)
    doc['posts'] = {f[:-4]: dict(produto=t['nome'], versao='Shopee ' + f[-5], conta='Shopee Vídeo', legenda=t.get('leg_' + f[-5].lower(), ''),
                                 link_produto=(t.get('links') or {}).get(f[-5].lower(), ''), drive_url=drive[f], dia=dia, ordem=int(nn) * 10 + 'ABC'.index(f[-5]))
                    for f in sorted(drive) if f.startswith(f'{pre}_{nn}_') and f[-6:] in ('_A.mp4', '_B.mp4', '_C.mp4') and (B / 'final' / f).exists()}
    (out / f'{pre}-{nn}.json').write_text(json.dumps(doc, ensure_ascii=False))
    print(f'{pre}-{nn}', t['nome'])
