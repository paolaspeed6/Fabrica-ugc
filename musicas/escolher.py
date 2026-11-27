"""Escolhe a trilha de fundo de cada vídeo, alternando a biblioteca.
- a dona 27/11 ("muito repetitivo"): 10 ESTILOS (lounge, pop alegre, comercial, tropical, violão feliz, funk, bossa,
  piano bonito, cinematográfico, eletrônico chill). Primeiro escolhe o estilo usado há mais tempo (nunca um dos 5 últimos
  da conta), depois a trilha desse estilo usada há mais tempo.
- O mesmo vídeo (mesmo id) sempre recebe a mesma trilha (re-render não troca a música).
- Fora isso, pega a trilha usada há mais tempo; nunca repete uma das últimas N/2 na mesma conta.
Uso: from escolher import escolher; escolher('p07_b_faixas', conta='shopee')"""
import os, re, json, glob, time, random
try:
    import fcntl
except ImportError:
    fcntl = None

PASTA = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(PASTA, 'biblioteca')
REG = os.path.join(PASTA, 'usadas.json')


def estilo(nome):
    """'pop_alegre_03_piano_assobio.flac' -> 'pop_alegre'; as 12 animadas antigas são o estilo 'lounge'."""
    if nome.startswith('animada_'):
        return 'lounge'
    m = re.match(r'(.+?)_\d\d_', nome)
    return m.group(1) if m else nome


def escolher(video_id, conta='geral'):
    trilhas = sorted(glob.glob(os.path.join(BIB, '*.wav')) + glob.glob(os.path.join(BIB, '*.flac')))
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
        ultimo = {r['trilha']: i for i, r in enumerate(reg)}
        estilos = sorted({estilo(x) for x in nomes})
        da_conta = [estilo(r['trilha']) for r in reg if r.get('conta') == conta]
        recentes_e = set(da_conta[-(len(estilos) // 2):])
        ult_e = {e: i for i, e in enumerate(da_conta)}
        livres_e = [e for e in estilos if e not in recentes_e] or estilos
        random.Random(video_id).shuffle(livres_e)
        est = min(livres_e, key=lambda e: ult_e.get(e, -1))
        livres = [x for x in nomes if estilo(x) == est]
        random.Random(video_id).shuffle(livres)
        escolha = min(livres, key=lambda x: ultimo.get(x, -1))
        reg.append(dict(video=video_id, conta=conta, trilha=escolha, quando=time.strftime('%Y-%m-%d %H:%M')))
        tmp = REG + '.tmp'
        json.dump(reg[-2000:], open(tmp, 'w'), ensure_ascii=False, indent=0)
        os.replace(tmp, REG)
        return os.path.join(BIB, escolha)
