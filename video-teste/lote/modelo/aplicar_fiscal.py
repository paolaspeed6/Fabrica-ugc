"""Aplica pNN-cenas/fiscal_imagem.json: imagem reprovada vai para rejeitadas/ e ganha fix_img (1 refação só; reprovada de novo = falhou);
aprovada ganha fix_vid com a frase de risco_animacao. uso: python3 -I aplicar_fiscal.py p01,p02 ...  (imprime refazer=... e animar=...)"""
import json, re, sys
from pathlib import Path
B = Path(__file__).resolve().parent; (B / 'rejeitadas').mkdir(exist_ok=True)
refazer, animar, falhou = [], [], []
for p in sys.argv[1].split(','):
    ff = B / f'{p}-ficha.json'; f = json.loads(ff.read_text()); fi = json.loads((B / f'{p}-cenas/fiscal_imagem.json').read_text())
    for c in f['cenarios']:
        k = c['id']; v = fi.get(k); img = B / f'{p}-cenas/{k}.jpg'
        if not v or not img.exists() or c.get('estado') in ('animar', 'falhou'): continue
        if v['veredito'].upper().startswith('APROV'):
            r = v.get('risco_animacao', ''); m = re.findall(r'"([^"]+)"', r); c['fix_vid'] = ' '.join(m) if m else ''
            c['estado'] = 'animar'; animar.append(f'{p}{k}')
        else:
            n = len(list((B / 'rejeitadas').glob(f'{p}_{k}_v*.jpg'))) + 1; img.rename(B / f'rejeitadas/{p}_{k}_v{n}.jpg')
            rj = B / f'{p}-cenas/reprovacoes.json'; rr = json.loads(rj.read_text()) if rj.exists() else []  # motivo vai para a dona na Conferir (27/10)
            rr.append(dict(cena=k, etapa=f'imagem {n}ª', motivo=(v.get('provas') or v.get('corrigir_prompt') or '')[:300], fiscal=v.get('fiscal', '')))
            rj.write_text(json.dumps(rr, ensure_ascii=False, indent=1))
            if c.get('fix_img'): c['estado'] = 'falhou'; falhou.append(f'{p}{k}')
            else: c['fix_img'] = v.get('corrigir_prompt', ''); refazer.append(f'{p}{k}')
    ff.write_text(json.dumps(f, ensure_ascii=False, indent=1))
print('refazer=' + ' '.join(refazer)); print('animar=' + ' '.join(animar)); print('falhou=' + ' '.join(falhou))
