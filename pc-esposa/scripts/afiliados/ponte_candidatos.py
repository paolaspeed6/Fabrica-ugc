r"""Ponte automática Drive -> fila do filtro de afiliados (Kevin 13/11: os produtos da varredura não chegavam ao filtro).

A varredura diária grava candidatos-AAAA-MM-DD.json em G:\Meu Drive\Central Esposa. Este script (chamado a cada 60 s
pelo vigia_candidatos.py, sem depender do Claude) copia para afiliados\fila_filtro.json os produtos novos:
- só arquivos com nome exato candidatos-AAAA-MM-DD.json que ainda não foram importados (ponte_importados.json);
- tira ids que já estão na fila ou em conferidos.csv; não guarda a foto (base64) para a fila não pesar;
- grava a fila de forma atômica, com backup fila_filtro.json.antes_ponte.
O rodar_candidatos.py relê a fila quando ela muda e aplica comissão mínima e a lista de pulados.
"""
import csv, datetime, json, os, re

def _achar_central():  # Paola 23/11: o Drive pode não estar na letra G:
    import os
    for letra in 'GHIJKLMNOPQRSTUVWXYZDEF':
        for r in ('Meu Drive', 'My Drive'):
            p = f'{letra}:\\{r}\\Central Esposa'
            if os.path.isdir(p):
                return p
    return r'G:\Meu Drive\Central Esposa'


DRIVE = _achar_central()
PASTA = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(PASTA, 'fila_filtro.json')
CSV = os.path.join(PASTA, 'conferidos.csv')
IMPORTADOS = os.path.join(PASTA, 'ponte_importados.json')
LOG = os.path.join(PASTA, 'ponte_candidatos.log')
NOME = re.compile(r'^candidatos-(\d{4})-(\d{2})-(\d{2})(?:_tarde)?\.json$')  # Paola: 2 varreduras por dia


def log(m):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {m}\n')


def _id(x):
    return str(x).strip().split('.')[-1]


def _ler(caminho):
    for enc in ('utf-8', 'utf-8-sig'):
        try:
            with open(caminho, encoding=enc) as f:
                return json.load(f)
        except UnicodeDecodeError:
            continue
    raise ValueError('encoding')


def importar():
    """Devolve quantos produtos novos entraram na fila (0 se nada a fazer). Nunca levanta erro."""
    try:
        if not os.path.isdir(DRIVE):
            return 0
        try:
            feitos = set(json.load(open(IMPORTADOS, encoding='utf-8')))
        except Exception:
            feitos = set()
        novos_arqs = sorted(n for n in os.listdir(DRIVE) if NOME.match(n) and n not in feitos)
        if not novos_arqs:
            return 0
        fila = _ler(FILA) if os.path.exists(FILA) else []
        vistos = {_id(i.get('itemId')) for i in fila}
        try:
            vistos |= {_id(l['itemId']) for l in csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';')
                       if l.get('decisao') != 'erro'}
        except Exception:
            pass
        entrou = []
        for nome in novos_arqs:
            try:
                dados = _ler(os.path.join(DRIVE, nome))
            except Exception as e:  # arquivo ainda sincronizando/incompleto: tenta de novo no próximo ciclo
                log(f'{nome}: ainda não legível ({e!r})')
                continue
            if not isinstance(dados, list):
                log(f'{nome}: formato inesperado, ignorado')
                feitos.add(nome)
                continue
            dia = NOME.match(nome)
            origem = f'busca {dia.group(3)}/{dia.group(2)}'
            n = 0
            for c in dados:
                iid = _id(c.get('itemId') or c.get('id') or '')
                if not iid or iid in vistos:
                    continue
                vistos.add(iid)
                item = {'itemId': iid, 'link': c.get('link'), 'nome': c.get('nome', ''),
                        'comissao_rs': c.get('comissao_rs'), 'comissao_pct': c.get('comissao_pct'),
                        'origem': origem, 'status_tinder': 'novo', 'pontos': c.get('pontos')}
                if not item['link']:
                    continue
                entrou.append(item)
                n += 1
            log(f'{nome}: {n} produtos novos de {len(dados)}')
            feitos.add(nome)
        if entrou:
            try:
                import shutil
                if os.path.exists(FILA):
                    shutil.copy2(FILA, FILA + '.antes_ponte')
            except Exception:
                pass
            tmp = FILA + '.ponte.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:  # sem BOM: o rodar_candidatos lê como utf-8
                json.dump(fila + entrou, f, ensure_ascii=False)
            os.replace(tmp, FILA)
            log(f'fila_filtro.json: +{len(entrou)} (total {len(fila) + len(entrou)})')
        json.dump(sorted(feitos), open(IMPORTADOS, 'w', encoding='utf-8'))
        return len(entrou)
    except Exception as e:
        log(f'erro: {e!r}')
        return 0


if __name__ == '__main__':
    print(importar())
