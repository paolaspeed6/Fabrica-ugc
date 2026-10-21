"""Processo padrão de um produto (a dona, 2026-10-18): 3 vídeos (A Um dia, B Faixas, C Direto) a partir de um cfg.
A voz (Kokoro dora_nicole) é gerada FRASE POR FRASE e juntada com pausas fixas: os tempos de cada frase saem
exatos e viram os cortes e a entrada dos textos. As cenas de cada momento ("tomadas") dividem o tempo sozinhas.

cfg = dict(
  id='p03', dir=LUXO_DIR, accent=(r,g,b), shiftx=0, esq=False, tem='*ela tem:*', leve='a sua',
  clips={'A': 6.0, 'B': 6.0, 'C': 6.0},          # duração de cada cena
  a=dict(eyebrow, gancho=[..], momentos=[(rótulo, legenda)]*3, falas=[gancho, m1, m2, m3]),
  b=dict(kicker, cenas=[(l1, l2, sub)]*3, falas=[cena1, cena2, cena3]),
  c=dict(eyebrow, gancho=[..], itens=[3], onde=[..], falas_gancho, falas_itens=[3], fala_onde),
  tomadas={'a': [[(clip, ss, z0, z1), ...] por momento (5: gancho, m1, m2, m3, cta)],
           'b': [... 3 cenas], 'c': [... 4: gancho, lista, onde, cta]},
)
Regras: produto inteiro e sem mão no 1º quadro (regra 13); cada opção abre com um take diferente (regra 12);
itens só com qualidades reais (regra 11)."""
import os, json, subprocess
import numpy as np
from novos import *

LUXO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TRILHA = os.path.join(LUXO, 'trilha_piano.wav')
PAUSA = 0.32
SR = 24000


def _voz(frases, pasta, nome):
    """gera cada frase (cache por texto), junta com pausas e devolve (wav, inícios, fim)."""
    os.makedirs(pasta, exist_ok=True)
    partes, inicios, t = [], [], 0.0
    for i, f in enumerate(frases):
        w = f'{pasta}/{nome}_{i}.wav'; txt = f'{pasta}/{nome}_{i}.txt'
        if not (os.path.exists(w) and open(txt).read() == f):
            subprocess.run(['python3', '-I', f'{LUXO}/tts_kokoro.py', f, w], check=True, stderr=subprocess.DEVNULL)
            open(txt, 'w').write(f)
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', w, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.int16)
        nz = np.nonzero(np.abs(x) > 300)[0]  # corta silêncio das pontas
        x = x[max(0, nz[0] - 600):nz[-1] + 1200] if len(nz) else x
        inicios.append(t); partes += [x, np.zeros(int(PAUSA * SR), np.int16)]; t += len(x) / SR + PAUSA
    y = np.concatenate(partes)
    out = f'{pasta}/{nome}_t.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', out],
                   input=y.tobytes(), check=True)
    return out, inicios, t - PAUSA


def _segs(cuts, tomadas, clips, sx=None):
    """divide cada intervalo [cuts[i], cuts[i+1]] entre as tomadas dele; tomada com {'d': x} tem duração fixa
    (ex.: trecho curto antes de uma mão entrar), as outras dividem o resto igualmente."""
    out = []
    for (a, b), tm in zip(zip(cuts, cuts[1:]), tomadas):
        fixo = sum(tk[4]['d'] for tk in tm if len(tk) > 4 and 'd' in tk[4])
        livres = [tk for tk in tm if not (len(tk) > 4 and 'd' in tk[4])]
        resto = (b - a - fixo) / max(1, len(livres))
        for tk in tm:
            src, ss, z0, z1 = tk[:4]; extra = dict(tk[4]) if len(tk) > 4 else {}
            d = extra.pop('d', resto)
            ss = max(0.0, min(ss, clips[src] - d - 0.05))
            out.append(seg(src, round(ss, 3), round(d, 4), (z0, z1), **extra))
    tot = sum(s['dur'] for s in out); out[-1]['dur'] = round(out[-1]['dur'] + 15 - tot, 4)
    return out


MUSICA = os.environ.get('MUSICA', TRILHA)  # música calma de fundo quando não há voz
COM_VOZ = os.environ.get('COM_VOZ') == '1'  # a dona, 2026-10-18: SEM voz por enquanto (a Kokoro soou estrangeira); só música


NATURAL = os.environ.get('ESTILO', 'natural') == 'natural'  # a dona, 2026-10-21: sem filtro + transições


def _natural(nome, cuts):
    """estilo 2026-10-21: sem filtro (resolução cheia), sem mergulho ao preto, transição whip/zoom em cada virada."""
    if not NATURAL: return
    f = f'{S}/specs/{nome}.json'; sp = json.load(open(f))
    sp['natural'] = 1; sp.pop('dips', None)
    sp['trans'] = [[c, ('whip', 'zoom')[i % 2]] for i, c in enumerate(cuts[1:]) if 0 < c < 15]
    json.dump(sp, open(f, 'w'), ensure_ascii=False, indent=1)


def sem_voz(cfg):
    """3 vídeos só com música: textos em ritmo fixo e calmo (sem narração)."""
    pid = cfg['id']
    comum = dict(accent=cfg['accent'], **({'shiftx': cfg['shiftx']} if cfg.get('shiftx') else {}))
    A, B, C = cfg['a'], cfg['b'], cfg['c']
    cuts = (0, 3.0, 5.6, 8.2, 10.8)
    opcao_a(f'{pid}_a_umdia', dict(eyebrow=A['eyebrow'], gancho=A['gancho'], momentos=A['momentos'], **comum),
            _segs(cuts + (15,), cfg['tomadas']['a'], cfg['clips']), None, bed=[MUSICA], cuts=cuts)
    _natural(f'{pid}_a_umdia', cuts)
    cuts = (0, 5.0, 10.0, 15)
    opcao_b_faixas(f'{pid}_b_faixas', dict(kicker=B['kicker'], cenas=B['cenas'], cta='Toque no carrinho', lift=cfg.get('lift', 300), **comum),
                   _segs(cuts, cfg['tomadas']['b'], cfg['clips']), None, bed=[MUSICA], cuts=cuts)
    _natural(f'{pid}_b_faixas', cuts)
    cuts = (0, 3.2, 9.0, 11.6, 15)
    opcao_d(f'{pid}_c_direto', dict(eyebrow=C['eyebrow'], gancho=C['gancho'], itens=C['itens'], onde=C['onde'],
            tem=cfg.get('tem', '*ela tem:*'), itens_t=[4.3, 5.9, 7.5], esq=cfg.get('esq', False),
            **({'escala': cfg['escala'], 'item_size': cfg['item_size']} if cfg.get('esq') else {}), **comum),
            _segs(cuts, cfg['tomadas']['c'], cfg['clips']), None, bed=[MUSICA], cuts=cuts)
    _natural(f'{pid}_c_direto', cuts)
    return [f'{pid}_a_umdia', f'{pid}_b_faixas', f'{pid}_c_direto']


def fazer_produto(cfg):
    if not COM_VOZ:
        return sem_voz(cfg)
    pid, pasta = cfg['id'], f"{S}/tts"
    comum = dict(accent=cfg['accent'], **({'shiftx': cfg['shiftx']} if cfg.get('shiftx') else {}))
    at = 0.6  # a voz começa 0,6 s depois do 1º quadro
    # A: gancho + 3 momentos + CTA
    A = cfg['a']
    w, ini, fim = _voz(A['falas'] + ['Toque no link e leve pra casa.'], pasta, 'a')
    cuts = (0, at + ini[1] - 0.15, at + ini[2] - 0.15, at + ini[3] - 0.15, at + ini[4] - 0.15)
    opcao_a(f'{pid}_a_umdia', dict(eyebrow=A['eyebrow'], gancho=A['gancho'], momentos=A['momentos'], **comum),
            _segs(cuts + (15,), cfg['tomadas']['a'], cfg['clips']), w, narr_at=at, bed=[TRILHA], cuts=cuts)
    # B: 3 cenas (a 3ª leva o CTA)
    B = cfg['b']
    w, ini, fim = _voz(B['falas'] + [f"Toque no carrinho e leve {cfg.get('leve', 'a sua')}."], pasta, 'b')
    cuts = (0, at + ini[1] - 0.15, at + ini[2] - 0.15, 15)
    opcao_b_faixas(f'{pid}_b_faixas', dict(kicker=B['kicker'], cenas=B['cenas'], cta='Toque no carrinho',
                   lift=cfg.get('lift', 300), **comum),
                   _segs(cuts, cfg['tomadas']['b'], cfg['clips']), w, narr_at=at, bed=[TRILHA], cuts=cuts)
    # C: gancho, "Olha o que ela tem:" + 3 itens, onde, CTA
    C = cfg['c']
    tem = cfg.get('tem', '*ela tem:*').replace('*', '').rstrip(':')
    frases = [C['fala_gancho'], f'Olha o que {tem}:'] + C['falas_itens'] + [C['fala_onde'], 'Toque no carrinho e veja o preço.']
    w, ini, fim = _voz(frases, pasta, 'c')
    cuts = (0, at + ini[1] - 0.15, at + ini[5] - 0.15, at + ini[6] - 0.15, 15)
    opcao_d(f'{pid}_c_direto', dict(eyebrow=C['eyebrow'], gancho=C['gancho'], itens=C['itens'], onde=C['onde'],
            tem=cfg.get('tem', '*ela tem:*'), itens_t=[at + ini[k] for k in (2, 3, 4)],
            esq=cfg.get('esq', False), **({'escala': cfg['escala'], 'item_size': cfg['item_size']} if cfg.get('esq') else {}), **comum),
            _segs(cuts, cfg['tomadas']['c'], cfg['clips']), w, narr_at=at, bed=[TRILHA], cuts=cuts)
    return [f'{pid}_a_umdia', f'{pid}_b_faixas', f'{pid}_c_direto']
