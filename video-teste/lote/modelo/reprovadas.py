"""Lista as reprovações de cena de um produto com o motivo (a dona 27/10: "me traga junto com o motivo quando alguma cena for reprovada").
Fontes: pNN-cenas/reprovacoes.json (aplicar_fiscal.py), fiscal_video.json (clipe reprovado ou cortado), e para lotes antigos os
log_fiscal_*.txt e o fix_img da ficha. uso: from reprovadas import reprovadas; reprovadas(B, 'p01') -> [{cena, etapa, motivo}]"""
import json, re
from pathlib import Path


def reprovadas(B, k):
    B = Path(B); d = B / f'{k}-cenas'; out = []
    rj = d / 'reprovacoes.json'
    if rj.exists(): out += json.loads(rj.read_text())
    else:  # lote antigo: motivos dos logs da Fiscal Gemini + correção pedida na ficha
        vistos = set()
        for lg in sorted(B.glob('log_fiscal_img*.txt')) + sorted(B.glob('log_fiscal_gemini*.txt')):  # só os da Fiscal de imagem
            for l in lg.read_text(errors='ignore').splitlines():
                m = re.match(rf'{k}([ABC]) REPROVADO \| (.+)', l)
                if m and m.groups() not in vistos: vistos.add(m.groups()); out.append(dict(cena=m[1], etapa='imagem', motivo=m[2][:300]))
        try: f = json.loads((B / f'{k}-ficha.json').read_text())
        except Exception: f = {'cenarios': []}
        for c in f['cenarios']:
            if c.get('fix_img') and not any(x['cena'] == c['id'] for x in out):
                out.append(dict(cena=c['id'], etapa='imagem', motivo='refeita; correção pedida: ' + c['fix_img'][:250]))
            if c.get('estado') == 'falhou': out.append(dict(cena=c['id'], etapa='imagem', motivo='reprovada 2 vezes: cena descartada (só 1 refação)'))
    fv = json.loads((d / 'fiscal_video.json').read_text()) if (d / 'fiscal_video.json').exists() else {}
    for c, v in sorted(fv.items()):
        df = '; '.join(v.get('defeitos') or [])
        if v.get('veredito', '').upper().startswith('REPROV'): out.append(dict(cena=c, etapa='vídeo', motivo=df[:300] or 'clipe reprovado'))
        elif df and float(v.get('fim') or 5) < 3.9: out.append(dict(cena=c, etapa='vídeo (cortado)', motivo=f"usado até {v.get('fim')} s: {df}"[:300]))
    return out
