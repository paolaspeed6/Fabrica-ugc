"""Só para o lote que já estava rodando com a versão antiga: reescreve o status do card no
formato novo a cada 5 s até o robô terminar (lê o progresso do log). Depois sai sozinho."""
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import status_card  # noqa: E402

PASTA = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.join(PASTA, 'conferir.lock')
LOG = os.path.join(PASTA, 'conferir_afiliados.log')


def progresso():
    ls = open(LOG, encoding='utf-8').read().splitlines()
    ini = max(i for i, l in enumerate(ls) if re.search(r'== \d+ produto', l))
    total = int(re.search(r'== (\d+) produto', ls[ini])[1])
    feito = sum(1 for l in ls[ini + 1:] if '-> ' in l and ' s:' in l or ('-> erro' in l))
    return feito, total


while os.path.exists(LOCK):
    try:
        f, t = progresso()
        st = open(status_card.STATUS, encoding='utf-8').read()
        estado = 'alerta' if '"alerta"' in st or 'CAPTCHA' in st else 'rodando'
        status_card.escrever(estado, f, t, 'CAPTCHA no tablet — resolva à mão' if estado == 'alerta' else None)
    except Exception as e:
        print('vigia:', e)
    time.sleep(5)
status_card.escrever('parado')
