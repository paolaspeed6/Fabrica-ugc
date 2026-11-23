r"""Vigia leve do filtro de afiliados do Poco verde (celular2). Kevin 10/11: lote novo na fila_filtro.json tem que ser
conferido sem ele clicar Ligar.

A cada 60 s: se NÃO há rodar_candidatos/conferir vivo neste celular, a última parada foi "normal: lista acabou"
(nunca relança depois de captcha/login/erro/PARAR/meta) e existem candidatos novos (não conferidos, comissão ok),
relança o rodar_candidatos.py do celular2. Nunca mata nada; o rodar_candidatos novo também relê a lista quando muda.
"""
import csv, datetime, json, os, subprocess, sys, time

BASE = r'C:\horst\tablet'
PASTA = os.path.join(BASE, 'afiliados')
ID = 'celular2'
SERIAL = '<SERIAL_CELULAR2>'
PY = r'C:\horst\python\python.exe'
LOG = os.path.join(PASTA, 'vigia_candidatos.log')
COMISSAO_MIN = 15.0


def log(m):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {m}\n')


def vivo(arq):
    try:  # 22/11: pid_real = python + script do robô + criado antes do lock (pid reaproveitado = lock morto, removido)
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import pid_real
        return pid_real.lock_vivo(arq)
    except ImportError:
        pass
    try:
        pid = int(open(arq).read())
        s = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'], capture_output=True, text=True, timeout=15,
                           creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
        return any(str(pid) in l and 'python' in l.lower() for l in s.splitlines())  # 13/11: PID reaproveitado por outro programa não é robô vivo
    except Exception:
        return False


def novos():
    lista = json.load(open(os.path.join(PASTA, 'fila_filtro.json'), encoding='utf-8-sig'))
    linhas = list(csv.DictReader(open(os.path.join(PASTA, 'conferidos.csv'), encoding='utf-8-sig'), delimiter=';'))
    feitos = {str(l['itemId']).split('.')[-1] for l in linhas if l['decisao'] != 'erro'}
    hoje, erros = f'{datetime.date.today():%Y-%m-%d}', {}
    for l in linhas:
        if l['decisao'] == 'erro' and str(l.get('data', '')).startswith(hoje):
            k = str(l['itemId']).split('.')[-1]
            erros[k] = erros.get(k, 0) + 1
    feitos |= {k for k, n in erros.items() if n >= 2}
    return [c for c in lista if str(c['itemId']).split('.')[-1] not in feitos
            and (c.get('comissao_rs') is None or float(c['comissao_rs']) >= COMISSAO_MIN)]


def main():
    log('vigia iniciado')
    sys.path.insert(0, PASTA)
    import ponte_candidatos
    while True:
        try:
            ponte_candidatos.importar()  # 13/11: candidatos-AAAA-MM-DD.json do Drive entram na fila_filtro.json
            parada = ''
            try:
                parada = open(os.path.join(PASTA, f'parada_{ID}.txt'), encoding='utf-8').read().strip()
            except OSError:
                pass
            parado = not (vivo(os.path.join(PASTA, f'candidatos_{ID}.lock')) or vivo(os.path.join(PASTA, f'conferir_{ID}.lock')))
            try:  # 11/11: assistir do Kevin no celular: não relança o filtro
                sys.path.insert(0, BASE)
                import assistir_uso
                assistindo = assistir_uso.assistir_usa(ID)
            except Exception:
                assistindo = False
            if (parado and not assistindo and parada == 'normal: lista acabou' and not os.path.exists(os.path.join(PASTA, 'PARAR'))
                    and not os.path.exists(os.path.join(PASTA, f'PARAR_{ID}'))):
                n = novos()
                if n:
                    log(f'{len(n)} candidatos novos e filtro parado ("lista acabou"): relançando rodar_candidatos')
                    env = dict(os.environ, HORST_ADB_SERIAL=SERIAL, HORST_ID=ID, PYTHONIOENCODING='utf-8',
                               PYTHONPATH=os.path.join(BASE, 'pylibs'), HORST_INTERVALO='0')
                    out = open(os.path.join(PASTA, f'rodar_candidatos_{ID}.out2'), 'a')
                    subprocess.Popen([PY, os.path.join(PASTA, 'rodar_candidatos.py')], cwd=BASE, env=env, stdout=out,
                                     stderr=out, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                    time.sleep(120)
        except Exception as e:
            log(f'erro: {e!r}')
        time.sleep(60)


if __name__ == '__main__':
    main()
