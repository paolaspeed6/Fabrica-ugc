"""Escolhe a trilha de fundo de cada vídeo, alternando a biblioteca.
- O mesmo vídeo (mesmo id) sempre recebe a mesma trilha (re-render não troca a música).
- Fora isso, pega a trilha usada há mais tempo; nunca repete uma das últimas N/2 na mesma conta.
Uso: from escolher import escolher; escolher('p07_b_faixas', conta='shopee')"""
import os, json, glob, time, random
try:
    import fcntl
except ImportError:
    fcntl = None

PASTA = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(PASTA, 'biblioteca')
REG = os.path.join(PASTA, 'usadas.json')


def escolher(video_id, conta='geral'):
    trilhas = sorted(glob.glob(os.path.join(BIB, '*.wav')))
    if not trilhas:
        raise FileNotFoundError('biblioteca de trilhas vazia: ' + BIB)
    with open(REG + '.lock', 'w') as lk:
        if fcntl:
            try:
                fcntl.flock(lk, fcntl.LOCK_EX)
            except OSError:
                pass
        try:
            reg = json.load(open(REG))
        except (OSError, ValueError):
            reg = []
        for r in reg:
            if r['video'] == video_id and os.path.exists(os.path.join(BIB, r['trilha'])):
                return os.path.join(BIB, r['trilha'])
        nomes = [os.path.basename(t) for t in trilhas]
        recentes = [r['trilha'] for r in reg if r.get('conta') == conta][-(len(nomes) // 2):]
        ultimo = {r['trilha']: i for i, r in enumerate(reg)}
        livres = [x for x in nomes if x not in recentes] or nomes
        random.Random(video_id).shuffle(livres)
        escolha = min(livres, key=lambda x: ultimo.get(x, -1))
        reg.append(dict(video=video_id, conta=conta, trilha=escolha, quando=time.strftime('%Y-%m-%d %H:%M')))
        tmp = REG + '.tmp'
        json.dump(reg[-2000:], open(tmp, 'w'), ensure_ascii=False, indent=0)
        os.replace(tmp, REG)
        return os.path.join(BIB, escolha)
