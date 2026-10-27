"""Produto sem cena aprovada (a dona 27/10: antes de descartar o produto, ela confere as cenas reprovadas e pode aproveitar uma,
senão foram 3 gerações pagas sem nenhum vídeo). Monta um doc "resgate" por produto para a aba Conferir da Postagens.
Clipes reprovados vão ao Drive em "<dia>/descartadas"; imagens sem clipe vão só como miniatura.
uso: python3 -I descartadas.py "Lista 25/10 A" 2026-10-26 [pNN,...]   (sem lista: todos os produtos sem aprovado.json)
Depois: ArtifactData batch (set, coleção "conferir", doc_id = nome do arquivo sem .json) na página Postagens.
Ela marca as cenas e toca "Usar estas cenas" (status resgatar, campo escolha) ou "Descartar produto" (status descartado)."""
import base64, json, shutil, subprocess, sys
from pathlib import Path
B = Path(__file__).resolve().parent
nome_lote, dia = sys.argv[1], sys.argv[2]
pre = B.name.replace('lista', '').upper()
T = json.loads((B / 'textos.json').read_text())
LINKS = {l.split()[0]: l.split()[1] for l in (B / 'links.txt').read_text().splitlines() if l.strip() and '<loja>' not in l}
so = sys.argv[3].split(',') if len(sys.argv) > 3 else [k for k in sorted(T) if (B / f'{k}-cenas').exists() and not (B / f'{k}-cenas/aprovado.json').exists()]
env = B / 'descartadas'; env.mkdir(exist_ok=True); out = B / 'conferir_docs'; out.mkdir(exist_ok=True)


def mini(src, ss=None):
    a = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss is not None else []) + ['-i', str(src), '-frames:v', '1', '-vf', 'scale=200:-2',
                                                                                   '-q:v', '6', '-f', 'image2', '-c:v', 'mjpeg', '-']
    return 'data:image/jpeg;base64,' + base64.b64encode(subprocess.run(a, capture_output=True, check=True).stdout).decode()


def ler(p):
    return json.loads(p.read_text()) if p.exists() else {}


for k in so:
    t = T[k]; d = B / f'{k}-cenas'; nn = k[1:]; fv, fi = ler(d / 'fiscal_video.json'), ler(d / 'fiscal_imagem.json'); cenas = []
    for c in 'ABC':
        mp4 = d / f'{c}_fixa.mp4' if (d / f'{c}_fixa.mp4').exists() else d / f'{c}.mp4'
        if mp4.exists():
            nome = f"{pre}_{nn}_{t['slug']}_cena{c}.mp4"; shutil.copy(mp4, env / nome)
            cenas.append(dict(id=c, tipo='video', arquivo=nome, poster=mini(mp4, 0.5), motivo='; '.join((fv.get(c) or {}).get('defeitos') or [])[:220]))
            continue
        imgs = sorted(B.glob(f'rejeitadas/{k}_{c}_v*.jpg')) or ([d / f'{c}.jpg'] if (d / f'{c}.jpg').exists() else [])
        if imgs:
            cenas.append(dict(id=c, tipo='imagem', poster=mini(imgs[-1]), motivo=((fi.get(c) or {}).get('provas') or 'imagem reprovada')[:220]))
    if not cenas: continue
    doc = dict(tipo='resgate', lote=nome_lote, dia=dia, ordem=int(nn), n=int(nn), produto=t['nome'], link_anuncio=LINKS.get(nn, ''),
               poster=cenas[0]['poster'], cenas=cenas, status='pendente', processado=False)
    (out / f'{pre}-{nn}.json').write_text(json.dumps(doc, ensure_ascii=False)); print(f'{pre}-{nn}', t['nome'], len(cenas), 'cenas')
if any(env.glob('*.mp4')):
    subprocess.run([sys.executable, str(B.parents[1] / 'drive_backup.py'), str(env), '--dia', f'{dia}/descartadas'], check=True)
    links = ler(env / 'drive_links.json')
    for f in out.glob(f'{pre}-*.json'):
        doc = json.loads(f.read_text())
        if doc.get('tipo') != 'resgate': continue
        for c in doc['cenas']:
            if c.get('arquivo') in links: c['drive_url'] = links[c['arquivo']]
        f.write_text(json.dumps(doc, ensure_ascii=False))
