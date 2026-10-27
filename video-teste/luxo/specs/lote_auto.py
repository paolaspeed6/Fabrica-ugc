"""Edição automática de um lote criado do zero nos 3 layouts DA DONA (a dona, 26/10: economizar o uso do Claude; nada escrito à mão
por produto). Lê <lote>/textos.json (Fichador) e <lote>/pNN-cenas/aprovado.json + fiscal_video.json (trechos limpos da Fiscal de vídeo),
copia os clipes limpos para trabalhos/<id>-<slug>/src e monta as tomadas: cada vídeo abre com uma cena diferente (A, B, C), nenhuma
tomada passa do fim do trecho limpo, transições whip/zoom (estilo natural do produto.py).
uso: python3 lote_auto.py <pasta do lote> <primeiro id da dona, ex. 67> [p01,p02,...]   -> imprime "pNN -> trabalhos/pXX-slug" """
import json, math, shutil, subprocess, sys
from pathlib import Path
L = Path(sys.argv[1]).resolve(); n0 = int(sys.argv[2])
T = json.loads((L / 'textos.json').read_text())
so = sys.argv[3].split(',') if len(sys.argv) > 3 else sorted(T)
RAIZ = Path(__file__).resolve().parents[3]

CUTS = {'a': (0, 3.0, 5.6, 8.2, 10.8, 15), 'b': (0, 5.0, 10.0, 15), 'c': (0, 3.2, 9.0, 11.6, 15)}
ABRE = {'a': 0, 'b': 1, 'c': 2}  # índice da cena que abre cada versão (rodízio do take inicial, regra 12)


def tomadas(cenas, lens):
    """cenas: ['A','B','C'] disponíveis; lens: fim limpo de cada uma. Cada intervalo vira tomadas que cabem no trecho limpo."""
    out = {}
    for v, cuts in CUTS.items():
        ordem = cenas[ABRE[v] % len(cenas):] + cenas[:ABRE[v] % len(cenas)]
        segs, i, ss = [], 0, {c: 0.0 for c in cenas}
        if ABRE[v] >= len(cenas):  # menos cenas que versões: abre a mesma cena mais adiante (outro quadro, regra 12)
            ss[ordem[0]] = round(max(0.0, min(1.8, lens[ordem[0]] - 3.4)), 2)
        for a, b in zip(cuts, cuts[1:]):
            dur = b - a; seg = []
            while dur > 0.01:
                c = ordem[i % len(ordem)]; i += 1
                d = min(dur, lens[c] - 0.1)
                if dur - d < 0.6 and dur - d > 0.01: d = dur  # sobra pequena: estica a última se couber
                d = min(d, lens[c] - 0.1)
                st = ss[c] if ss[c] + d <= lens[c] - 0.05 else 0.0
                zm = 1.12 if v == 'b' else 1.06  # B: o vídeo sobe 300 px e a câmera parecia parada (17 B reprovados no 25/10 A)
                z = (1.0, zm) if len(seg) % 2 == 0 else (zm, 1.0)  # zoom maior: auditor reprovou cena quase parada (p67 B)
                seg.append((c, round(st, 2), z[0], z[1], {'d': round(d, 3)}))
                ss[c] = st + d if st + d < lens[c] - 1.0 else 0.0
                dur -= d
            segs.append(seg)
        out[v] = segs
    return out


def cfg(k, n):
    t = T[k]; d = L / f'{k}-cenas'
    if not (d / 'aprovado.json').exists(): return None, None  # nenhuma cena aprovada (aprovar.py: SEM CENA APROVADA)
    fv = json.loads((d / 'fiscal_video.json').read_text()) if (d / 'fiscal_video.json').exists() else {}
    pid = f'p{n}'; W = RAIZ / 'trabalhos' / f'{pid}-{t["slug"]}'
    for s in ('src', 'specs', 'out2'): (W / s).mkdir(parents=True, exist_ok=True)
    cenas, lens = [], {}
    for c in 'ABC':
        v = fv.get(c) or {}; fim = float(v.get('fim') or 0); ini = float(v.get('inicio') or 0)
        src = d / (f'{c}_ini.mp4' if ini > 0 and (d / f'{c}_ini.mp4').exists() else f'{c}_fixa.mp4' if (d / f'{c}_fixa.mp4').exists() else f'{c}.mp4')
        if fim - ini < 1.5 or not src.exists(): continue
        shutil.copy(src, W / 'src' / f'{c}.mp4'); cenas.append(c); lens[c] = round(min(fim - ini, 4.0), 2)  # só os 4 primeiros s: o fim do clipe é onde a IA mais estraga (26/10)
    if not cenas: return None, W
    A = dict(t['a']); C = dict(t['c'])
    A.setdefault('eyebrow', t['nome'])
    C.setdefault('eyebrow', t['b'].get('kicker') or t['nome']); C.setdefault('onde', A.get('cta') or ['Leve pra casa.'])
    kit = any(w in t['nome'].lower() for w in ('kit', 'cadeiras', 'banquetas', 'bancos'))
    return dict(id=pid, accent=tuple(t.get('ac') or (200, 160, 120)), clips=lens, leve='o seu' if kit else 'a sua',
                tem='*o kit tem:*' if kit else '*ele tem:*', a=A, b=dict(t['b']), c=C, tomadas=tomadas(cenas, lens)), W


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    n = n0; mapa = {}
    for k in so:
        if k not in T: continue
        c, W = cfg(k, n)
        if not c: print(k, 'SEM CENA LIMPA'); continue
        subprocess.run([sys.executable, '-c', f'import json,sys; sys.argv=[""]; from produto import *; print(fazer_produto(json.load(open("{W}/specs/_cfg.json"))))']
                       if (W / 'specs' / '_cfg.json').write_text(json.dumps(c, ensure_ascii=False)) or True else [],
                       cwd=Path(__file__).resolve().parent, env={**__import__('os').environ, 'LUXO_DIR': str(W)}, check=True)
        mapa[k] = W.name; print(k, '->', f'trabalhos/{W.name}', c['clips'], flush=True); n += 1
    (L / 'trabalhos.json').write_text(json.dumps(mapa, ensure_ascii=False, indent=1))
