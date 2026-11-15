"""K31 (a dona, 15/11: "produtos muito diferentes das imagens de referência, outras variações do anúncio, detalhes que nem existem").
Causa achada: fotos_ref da ficha levava fotos de OUTRA variante do anúncio (ex.: Cadeiras Savana, foto 01 com pés dourados e foto 03
com pés pretos -> o vídeo saiu com pés pretos). O Nano Banana mistura tudo o que recebe.
Este script (grátis, Gemini) compara cada foto de fotos_ref com a foto 01 e TIRA as que não são exatamente o mesmo produto e a mesma
variante (cor, cor dos pés/metal, tecido, modelo, formato, nº de peças). Rode ANTES de gerar imagens (o produzir.sh fase1 já roda).
Guarda as tiradas em fotos_ref_tiradas. Na dúvida, tira (fica só a 01).
uso: python3 -I refs_variante.py p01,p02,..."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fiscal_gemini import B, b64, chamar

PEDIDO = """A 1ª imagem é a FOTO 01 de um anúncio da Shopee (o produto exato que a cliente recebe). A 2ª é outra foto do mesmo anúncio.
O anúncio pode ter várias cores, acabamentos ou modelos. A 2ª foto mostra EXATAMENTE o mesmo produto e a mesma variante da foto 01?
Compare: cor e tom, cor dos pés/base/metal (dourado x preto x cromado), tecido/material, formato, modelo, número de peças, puxadores, detalhes.
Responda só JSON: {"mesma": true ou false, "motivo": "curto, em português"}. Na dúvida, false."""

def principal(p, refs):
    for r in refs:
        if Path(r).name in ('01.jpg', '01_limpa.jpg'): return r
    return refs[0]

for p in sys.argv[1].split(','):
    fj = B / f'{p}-ficha.json'
    if not fj.exists(): print(p, 'sem ficha'); continue
    f = json.loads(fj.read_text()); refs = f.get('fotos_ref') or []
    caminho = lambda x: B / (x if '/' in x else f'{p}-fotos/{x}')
    um = principal(p, refs); fica, tira = [], []
    for r in refs:
        if Path(r).name in ('01.jpg', '01_limpa.jpg') or not caminho(r).exists(): fica.append(r); continue
        try:
            v = chamar([{'text': PEDIDO}, {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(caminho(um))}},
                        {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(caminho(r))}}])
            if isinstance(v, list): v = v[0]
        except Exception as e: v = {'mesma': False, 'motivo': f'Gemini falhou ({e}); na dúvida, tira'}
        if v.get('mesma') is True: fica.append(r)
        else: tira.append({'foto': r, 'motivo': v.get('motivo', '')})
    if tira:
        f['fotos_ref'] = fica; f['fotos_ref_tiradas'] = f.get('fotos_ref_tiradas', []) + tira
        fj.write_text(json.dumps(f, ensure_ascii=False, indent=1))
    print(p, 'fica', [Path(x).name for x in fica], '| tirou', [(Path(t['foto']).name, t['motivo'][:60]) for t in tira], flush=True)
