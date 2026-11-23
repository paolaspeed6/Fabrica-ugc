r"""Monta o status JSON do card "Afiliados (filtro automático)" a partir de conferidos.csv e
captcha_log.csv (sem IA). Usado pelo conferir_afiliados.py e pelo vigia (vigiar_status.py).
Formato: {state, detail, linhas[5], progresso{feito,total}, quando}."""
import csv, datetime, json, os, shutil, sys

BASE = r'C:\horst\tablet'
sys.path.insert(0, BASE)
import captcha_log  # noqa: E402
import aparelho_atual as ap  # noqa: E402

CSV = os.path.join(BASE, 'afiliados', 'conferidos.csv')
STATUS_GERAL = os.path.join(BASE, 'afiliados', 'status.json')  # o card atual da Central lê este
STATUS = os.path.join(BASE, 'afiliados', f'status_{ap.id_aparelho()}.json') if os.environ.get('HORST_ADB_SERIAL') else STATUS_GERAL


def _linhas_csv():
    try:
        return list(csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';'))
    except Exception:
        return []


def montar(state, feito=None, total=None, aviso=None):
    todas = _linhas_csv()
    hoje = f'{datetime.date.today():%Y-%m-%d}'
    ultimo_por_item = {}
    for l in todas:  # o CSV guarda histórico (reclassificações viram linhas novas): vale a última de cada produto
        ultimo_por_item[l['itemId'] or l['link']] = l
    lh = [l for l in todas if l['data'].startswith(hoje) and ultimo_por_item.get(l['itemId'] or l['link']) is l]
    aprov = [l for l in lh if l['decisao'].startswith('aprovado')]
    rev = sum(1 for l in lh if l['decisao'] == 'revisar')
    desc = sum(1 for l in lh if l['decisao'] == 'descarta')
    erro = sum(1 for l in lh if l['decisao'] == 'erro')

    def media(ls):
        v = [int(l['videos']) for l in ls if str(l['videos']).isdigit()]
        return f'{sum(v) / len(v):.1f}' if v else '-'
    segs = [int(l['segundos']) for l in lh if str(l.get('segundos', '')).isdigit() and l['decisao'] != 'erro']
    seg = sum(segs) / len(segs) if segs else 65
    if feito is not None and total:
        fim = datetime.datetime.now() + datetime.timedelta(seconds=seg * max(0, total - feito))
        ritmo = f'~{seg / 60:.1f} min/produto · lote termina ~{fim:%H:%M}'
    else:
        ritmo = f'~{seg / 60:.1f} min/produto · sem lote rodando'
    if lh:
        u = lh[-1]
        nome = ' '.join(u['nome'].split()[:5]) or u['itemId']
        if str(u.get('videos', '')).isdigit() and int(u['videos']) > 15:
            ultimo = f'Último: {nome}: parou de contar, 16+ vídeos → descarta'
        else:
            ultimo = f'Último: {nome} → {u["decisao"]}'
    else:
        ultimo = 'Último: -'
    cap = captcha_log._ler()
    if cap:
        ms = [int(l['min_desde_anterior']) for l in cap[1:] if str(l['min_desde_anterior']).isdigit()]
        cap_txt = f'Último captcha {cap[-1]["inicio"][11:16]}' + (f' · média a cada {sum(ms) / len(ms):.0f} min' if ms else '')
    else:
        cap_txt = 'Nenhum captcha registrado'
    extra = f' · erros {erro}' if erro else ''
    st = {
        'state': state,
        'detail': aviso or f'Checados hoje {len(lh)} · total {len(todas)}',
        'linhas': [f'Aprovados {len(aprov)} · Prioridade {sum(1 for l in lh if l.get("prioridade") == "sim")} · '
                   f'Revisar {rev} · Descartados {desc}{extra}',
                   f'Média de vídeos {media(lh)} (aprovados {media(aprov)})',
                   ritmo, ultimo, cap_txt],
        'progresso': {'feito': feito, 'total': total} if total else None,
        'quando': f'{datetime.datetime.now():%H:%M:%S}',
    }
    return st


def escrever(state, feito=None, total=None, aviso=None):
    st = montar(state, feito, total, aviso)
    tmp = STATUS + '.tmp'
    json.dump(st, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
    os.replace(tmp, STATUS)
    if STATUS != STATUS_GERAL:
        shutil.copyfile(STATUS, STATUS_GERAL)
    return st


if __name__ == '__main__':
    print(json.dumps(escrever('parado'), ensure_ascii=False, indent=1))
