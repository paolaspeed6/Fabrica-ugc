"""Ids que o robô de afiliados não confere (lista no Drive, mantida pela nuvem/Kevin)."""
import json

def _achar_central():  # Paola 23/11: o Drive pode não estar na letra G:
    import os
    for letra in 'GHIJKLMNOPQRSTUVWXYZDEF':
        for r in ('Meu Drive', 'My Drive'):
            p = f'{letra}:\\{r}\\Central Esposa'
            if os.path.isdir(p):
                return p
    return r'G:\Meu Drive\Central Esposa'


import os as _os
ARQ = _os.path.join(_achar_central(), 'pular_afiliados.json')
CHAVES = ('produzidos', 'descartados_tinder', 'esposa', 'reaprovados_0611_ja_produzidos', 'kevin')  # Paola: + os do Kevin


def _item(x):
    return str(x).strip().split('.')[-1]


def ids():
    """Conjunto de ids (parte depois do ponto). Se o arquivo faltar, devolve vazio e avisa em erro()."""
    d = json.load(open(ARQ, encoding='utf-8-sig'))
    return {_item(x) for k in CHAVES for x in d.get(k, [])}


def tirar(itens, log=print):
    """Remove da lista os itens a pular. Item: dict com itemId (ou link com o id no fim)."""
    try:
        pular = ids()
    except Exception as e:
        log(f'pular_afiliados.json não lido ({e!r}): sigo sem a lista')
        return itens
    fora = []
    for i in itens:
        chave = _item(i.get('itemId') or str(i.get('link', '')).rstrip('/').split('/')[-1].split('?')[0])
        if chave not in pular:
            fora.append(i)
    if len(fora) != len(itens):
        log(f'pular_afiliados: {len(itens) - len(fora)} ids pulados')
    return fora
