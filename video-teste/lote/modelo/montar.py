"""Monta as 3 versões aprovadas (padrao_app) de um produto da Lista 24/10 A (cópia da Lista 2110).
uso: LUXO_DIR=<scratchpad>/pNN-luxo python3 -I montar.py pNN
Lê textos.json e pNN-cenas/aprovado.json {"A": seg_limpo, "B": "A" (cena reprovada: usa a A ao contrário), ...}.
Se existir pNN-cenas/<C>_recorte.mp4 (produto inteiro da foto colado, recorte_inteiro.py), usa ele no lugar do clipe gerado.
SEM zoom de encaixe no começo (Kevin 2026-10-21): o produto já vem encaixado entre o texto e o CTA na própria imagem; lift 0."""
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[2]) + '/luxo/specs')
from padrao_app import fazer_app
from opcao_c import opcao_c
from produto import _segs, trilha
PRE = os.environ.get('PREFIXO') or Path(__file__).resolve().parent.name.replace('lista', '').upper()  # ex.: lista2410a -> 2410A
import padrao_app
# trilha por vídeo com id único deste lote (a rotação guarda a música pelo id; pNN se repete entre listas)
padrao_app.trilha = lambda vid, conta='shopee': trilha(PRE + '_' + vid, conta)
B = Path(__file__).resolve().parent; k = sys.argv[1]
t = json.loads((B / 'textos.json').read_text())[k]
ok = json.loads((B / f'{k}-cenas/aprovado.json').read_text())
src = Path(os.environ['LUXO_DIR']) / 'src'; src.mkdir(parents=True, exist_ok=True)
MIN = 5.3  # cada bloco usa até 5,2 s do clipe


_trav = {c for c in 'ABC' if (B / f'{k}-cenas/{c}_travada.mp4').exists() or (B / f'{k}-cenas/{c}_fixa.mp4').exists()}  # câmera parada na IA
# cena que usa clipe travado (dela mesma ou reaproveitado de outra cena, ao contrário) ganha câmera por código
TRAV = {c for c in 'ABC' if (ok[c] if isinstance(ok[c], str) else c) in _trav}


def orig(c):
    """<C>_travada.mp4 (fixar.py: câmera parada na IA, produto travado no 1º quadro, cenário animado) vence;
    depois <C>_recorte.mp4; depois o clipe gerado."""
    for n in ('_ini', '_travada', '_recorte', '_fixa', ''):  # _ini: clipe cortado no início (aprovar.py)  # _fixa: câmera parada sem colagem (padrão desde 2026-10-22 05:54)
        r = B / f'{k}-cenas/{c}{n}.mp4'
        if r.exists():
            return str(r)


SO_FRENTE = os.environ.get('IDA_VOLTA', '0') != '1'  # grupo B (Kevin 2026-10-22 06:52): só o trecho limpo do início, desacelerado, sem ida e volta


def preparar(o, dest, ate, reverso=False):
    if SO_FRENTE:  # trecho limpo [0, ate] esticado até MIN s com interpolação de movimento; reaproveitado de outra cena = mesmo trecho
        lento = max(1.0, MIN / ate)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', o, '-filter_complex',
                        f'[0:v]trim=0:{ate},setpts={lento:.3f}*(PTS-STARTPTS),fps=24,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir[v]',
                        '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', dest], check=True)
        return round(ate * lento, 2)
    """ida e volta do trecho limpo [0, ate]; trecho curto é desacelerado com interpolação de movimento até MIN s."""
    lento = max(1.0, MIN / (2 * ate)); interp = ',minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir' if lento > 1.3 else ''
    ordem = '[r][f]' if reverso else '[f][r]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', o, '-filter_complex',
                    f'[0:v]trim=0:{ate},setpts={lento:.3f}*(PTS-STARTPTS),fps=24{interp},split[f][r0];[r0]reverse[r];{ordem}concat=n=2:v=1[v]',
                    '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', dest], check=True)
    return round(2 * ate * lento, 2)


clips = {}
for c in 'ABC':
    v = ok[c]
    clips[c] = preparar(orig(v), str(src / f'{c}.mp4'), ok[v], reverso=True) if isinstance(v, str) else preparar(orig(c), str(src / f'{c}.mp4'), v)
Z = (1.0, float(os.environ.get('ZMAX', '1.03')))
_lado = [0]


def _cam(c, ss):
    """clipe travado (a IA não move a câmera): aproximação + deslize por código, alternando o lado; o produto segue entre texto e CTA."""
    if c not in TRAV:
        return (c, ss, *Z)
    _lado[0] ^= 1; d = 40 if _lado[0] else -40  # centro acima do produto: com 1,13 ele fica entre y 690 e 1338 de 1920
    return (c, ss, 1.0, 1.13, {'c0': [360, 640], 'c1': [360 + d, 595]})
# cada Shopee abre com uma geração diferente (Kevin 2026-10-22): A abre na cena A, B na B, C na C; o Reels abre na B do meio
cfg = dict(id=k, accent=tuple(t['ac']), clips=clips, a=t['a'], b=t['b'], r=t['r'],
           tomadas=dict(a=[[_cam('A', 0.0)], [_cam('A', 1.5)], [_cam('B', 0.0)], [_cam('C', 0.0)], [_cam('B', 1.0)]],
                        b=[[_cam('B', 0.0)], [_cam('A', 0.0)], [_cam('C', 0.0)]], r=[[_cam('B', 1.0)], [_cam('C', 0.0)], [_cam('A', 0.0)]]))
nomes = fazer_app(cfg)
tc = [[_cam('C', 0.0)], [_cam('A', 0.0)], [_cam('B', 0.0)], [_cam('C', 1.0)], [_cam('A', 1.0)]]
opcao_c(f'{k}_c_lista', t['c'], _segs((0, 3.4, 6.0, 8.6, 11.2, 15), tc, clips), estilo='lista', bed=[trilha(f'{PRE}_{k}_c_lista')], accent=tuple(t['ac']))
nomes.append(f'{k}_c_lista')
for n in nomes:
    f = Path(os.environ['LUXO_DIR']) / 'specs' / f'{n}.json'; sp = json.loads(f.read_text()); sp['lift'] = 0
    f.write_text(json.dumps(sp, ensure_ascii=False, indent=1))
print(nomes, clips)
