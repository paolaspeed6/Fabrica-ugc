"""Filtro do PC -> Tinder (a dona, 25/11: "a parte da Central que escolhe os produtos não está sincronizada com o Tinder").
Lê afiliados\\conferidos.csv e grava a última decisão de cada produto em <Drive>\\Central Esposa\\filtro_resultado.json.
A rotina da nuvem (central_drive.py filtro) lê esse arquivo e atualiza o Tinder: "descarta" sai do Escolher,
"aprovado" sobe para o topo com selo (⭐ = prioridade). Chamado pelo conferir_afiliados.py depois de cada produto.
"""
import csv, json, os, time
from ponte_candidatos import DRIVE

PASTA = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(PASTA, 'conferidos.csv')
_ult = [0.0]


def exportar(forcar=False):
    if not forcar and time.time() - _ult[0] < 60:  # no máximo 1 vez por minuto
        return
    _ult[0] = time.time()
    if not os.path.isdir(DRIVE) or not os.path.exists(CSV):
        return
    r = {}
    for l in csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';'):
        d, i = (l.get('decisao') or ''), (l.get('itemId') or '').strip()
        if i and d in ('aprovado', 'descarta', 'revisar'):
            r[i] = [d, l.get('prioridade') or '', l.get('videos') or '', l.get('vendas') or '', l.get('data') or '']
    dest = os.path.join(DRIVE, 'filtro_resultado.json')
    tmp = dest + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({'quando': time.strftime('%Y-%m-%d %H:%M'), 'r': r}, f, ensure_ascii=False)
    os.replace(tmp, dest)


if __name__ == '__main__':
    exportar(True)
    print('filtro_resultado.json gravado em', DRIVE)
