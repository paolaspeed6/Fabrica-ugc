r"""Registro de captchas da Shopee no tablet (compartilhado: robô de afiliados e fila de postagem).

NUNCA resolve nem contorna captcha: só detecta, avisa (bipe + status) e espera o Kevin resolver.
Cada evento vira uma linha em C:\horst\tablet\captcha_log.csv:
  inicio, fim (quando sumiu), minutos_parado, script, abertos_desde_anterior, min_desde_anterior, print
Serve para prever de quanto em quanto tempo / quantos produtos o captcha aparece.
"""
import csv, datetime, os

CSV = r'C:\horst\tablet\captcha_log.csv'
CAMPOS = ['inicio', 'fim', 'minutos_parado', 'script', 'abertos_desde_anterior', 'min_desde_anterior', 'print', 'obs']
CONTADOR = r'C:\horst\tablet\captcha_contador.txt'  # produtos/posts abertos desde o último captcha
PALAVRAS = ('captcha', 'verificação de segurança', 'verificacao de seguranca', 'arraste o controle',
            'deslize para', 'não sou um robô', 'verifique que você', 'arraste a peça', 'complete o quebra',
            'verificação deslizante', 'arraste para completar')
FMT = '%Y-%m-%d %H:%M:%S'


def e_captcha(textos):
    junto = ' '.join(textos).lower()
    return any(p in junto for p in PALAVRAS)


def contar_aberto():
    """Chamar a cada produto aberto / post iniciado."""
    try:
        n = int(open(CONTADOR).read().strip() or 0)
    except Exception:
        n = 0
    open(CONTADOR, 'w').write(str(n + 1))


def _ler():
    try:
        return list(csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';'))
    except Exception:
        return []


def registrar(inicio, fim, script, print_='', obs=''):
    linhas = _ler()
    try:
        abertos = int(open(CONTADOR).read().strip() or 0)
    except Exception:
        abertos = ''
    anterior = linhas[-1]['inicio'] if linhas else None
    desde = ''
    if anterior:
        try:
            desde = round((inicio - datetime.datetime.strptime(anterior, FMT)).total_seconds() / 60)
        except Exception:
            pass
    novo = not os.path.exists(CSV)
    with open(CSV, 'a', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=';')
        if novo:
            w.writeheader()
        w.writerow({'inicio': inicio.strftime(FMT), 'fim': fim.strftime(FMT) if fim else '',
                    'minutos_parado': round((fim - inicio).total_seconds() / 60, 1) if fim else '',
                    'script': script, 'abertos_desde_anterior': abertos, 'min_desde_anterior': desde,
                    'print': print_, 'obs': obs})
    open(CONTADOR, 'w').write('0')
    atualizar_card()


STATUS = r'C:\horst\tablet\central\captcha_status.json'


def atualizar_card():
    """Card 'Captchas' na Central (lido do status JSON; a Central relê sozinha)."""
    import json
    # (o card 'captchas' foi tirado de propósito pela Central: o card Tablet lê o captcha_log.csv. Não recriar.)
    json.dump({'state': 'ok', 'detail': resumo()}, open(STATUS, 'w', encoding='utf-8'), ensure_ascii=False)


def resumo():
    """Texto curto para o card: 'último captcha HH:MM, média a cada N produtos / X min'."""
    ls = _ler()
    if not ls:
        return 'nenhum captcha registrado'
    ult = ls[-1]['inicio'][11:16]
    ns = [int(l['abertos_desde_anterior']) for l in ls[1:] if str(l['abertos_desde_anterior']).isdigit()]
    ms = [int(l['min_desde_anterior']) for l in ls[1:] if str(l['min_desde_anterior']).isdigit()]
    partes = [f'último captcha {ult} ({len(ls)} no total)']
    if ns:
        partes.append(f'média a cada {sum(ns) / len(ns):.0f} produtos')
    if ms:
        partes.append(f'{sum(ms) / len(ms):.0f} min')
    return ', '.join(partes)
