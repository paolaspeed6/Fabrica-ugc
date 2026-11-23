r"""Destrava a fila de postagem SEM depender da Central nem do Claude (Kevin 21/11).

Uso:   python destravar_fila.py [azul|verde|celular1|celular2] [--sem-ligar]
Faz, nesta ordem:
  1. arquiva erro.txt / erro_<celular>.txt (em gravacao\erro_AAAAMMDD_HHMMSS.txt) e apaga PARAR / PARAR_<celular>;
  2. zera os contadores de travamento (travou.json);
  3. remove locks de processos MORTOS (rodar_fila*.lock) e claims presos (fila_claims de dono sem fila viva);
  4. relança rodar_fila.py no celular escolhido, se não houver fila viva nele e se o celular não estiver com outro robô
     (filtro de afiliados / assistir / interagir curtidas): nunca mata robô vivo.
Imprime em português simples o que fez e o que não deu para fazer.
"""
import datetime, glob, json, os, re, shutil, subprocess, sys, time

BASE = r'C:\horst\tablet'
PY = r'C:\horst\python\python.exe'
ADB = os.path.join(BASE, 'platform-tools', 'adb.exe')
CELULARES = {'azul': 'celular1', 'celular1': 'celular1', 'verde': 'celular2', 'celular2': 'celular2'}
NOMES = {'celular1': 'Poco azul', 'celular2': 'Poco verde'}
SEM_JANELA = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def _ps(cmd, timeout=40):
    return subprocess.run(['powershell', '-NoProfile', '-Command', cmd], capture_output=True, text=True, timeout=timeout,
                          creationflags=SEM_JANELA).stdout


def processos_python():
    """[(pid, linha_de_comando)] dos python vivos (para saber quem está usando cada celular)."""
    out = _ps("Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'python' } | ForEach-Object { \"$($_.ProcessId)`t$($_.CommandLine)\" }")
    res = []
    for linha in out.splitlines():
        if '\t' in linha:
            pid, cmd = linha.split('\t', 1)
            if pid.strip().isdigit():
                res.append((int(pid), cmd))
    return res


def pid_vivo(pid):
    try:  # 22/11: pid reaproveitado (ex.: audiodg.exe) não conta como robô vivo
        import pid_real
        return pid_real.e_robo(int(pid))
    except ImportError:
        pass
    try:
        return str(int(pid)) in _ps(f'tasklist /FI "PID eq {int(pid)}" /NH', 20)
    except Exception:
        return False


def serial_de(celular):
    """Serial adb do celular (Wi-Fi se estiver ligado, senão USB)."""
    try:
        cfg = json.load(open(os.path.join(BASE, 'aparelhos.json'), encoding='utf-8-sig'))
        c = cfg.get(celular) or {}
    except Exception:
        c = {}
    saida = subprocess.run([ADB, 'devices'], capture_output=True, text=True, timeout=20, creationflags=SEM_JANELA).stdout
    ligados = {l.split()[0] for l in saida.splitlines()[1:] if l.strip().endswith('device')}
    for s in (c.get('wifi'), c.get('usb')):
        if s and s in ligados:
            return s
    return None


def quem_usa(celular, procs):
    """Nome do robô vivo que usa este celular (outro cartão), ou ''."""
    nomes = {'candidatos': 'filtro de afiliados', 'conferir_afiliados': 'filtro de afiliados',
             'assistir.py': 'Assistir', 'interagir_curtidas': 'Interagir curtidas'}
    try:
        cfg = json.load(open(os.path.join(BASE, 'aparelhos.json'), encoding='utf-8-sig'))[celular]
        ids = {str(cfg.get('usb')), str(cfg.get('wifi'))}
    except Exception:
        ids = set()
    for pid, cmd in procs:
        for chave, nome in nomes.items():
            if chave in cmd and (celular in cmd or any(i and i in cmd for i in ids)):
                return nome
    # filtro: o lock por aparelho diz quem está nele
    for pref in ('conferir', 'candidatos'):
        lk = os.path.join(BASE, 'afiliados', f'{pref}_{celular}.lock')
        try:
            if pid_vivo(int(open(lk).read().strip())):
                return 'filtro de afiliados'
        except Exception:
            pass
    return ''


def destravar(alvo='azul', ligar=True):
    """Executa o destravar e devolve (ok, [linhas em português])."""
    log = []
    celular = CELULARES.get(str(alvo).lower(), 'celular1')
    nome = NOMES[celular]
    procs = processos_python()
    filas_vivas = [(p, c) for p, c in procs if 'rodar_fila.py' in c]
    # 1) erros / PARAR
    arq = os.path.join(BASE, 'gravacao')
    os.makedirs(arq, exist_ok=True)
    for n in ('erro.txt', f'erro_{celular}.txt'):
        p = os.path.join(BASE, n)
        if os.path.exists(p):
            dst = os.path.join(arq, f'erro_{datetime.datetime.now():%Y%m%d_%H%M%S}_{n}')
            shutil.move(p, dst)
            log.append(f'Arquivei o erro "{n}" (guardado em gravacao).')
    for n in ('PARAR', f'PARAR_{celular}'):
        p = os.path.join(BASE, n)
        if os.path.exists(p):
            os.remove(p)
            log.append(f'Apaguei o pedido de parar "{n}".')
    # 2) contadores de travamento
    tj = os.path.join(BASE, 'travou.json')
    if os.path.exists(tj):
        json.dump({}, open(tj, 'w', encoding='utf-8'))
        log.append('Zerei o contador de travamentos.')
    # 3) locks de processo morto e claims presos
    for lk in glob.glob(os.path.join(BASE, 'rodar_fila*.lock')):
        try:
            pid = int(open(lk).read().strip())
        except Exception:
            pid = None
        if pid is None or not pid_vivo(pid):
            os.remove(lk)
            log.append(f'Removi o lock de uma fila que já tinha morrido ({os.path.basename(lk)}).')
    vivos = {c for c in ('celular1', 'celular2') if os.path.exists(os.path.join(BASE, f'rodar_fila_{c}.lock'))}
    pasta_claims = os.path.join(BASE, 'fila_claims')
    n_claims = 0
    for cl in glob.glob(os.path.join(pasta_claims, '*.txt')) if os.path.isdir(pasta_claims) else []:
        try:
            dono = open(cl, encoding='utf-8').read().strip()
        except OSError:
            continue
        if dono not in vivos and not filas_vivas:  # dono sem fila viva: reserva presa
            os.remove(cl)
            n_claims += 1
    if n_claims:
        log.append(f'Limpei {n_claims} reserva(s) de vídeo presa(s) por uma fila que já não existe.')
    if not ligar:
        return True, log + ['Pronto (não liguei a fila, como pedido).']
    # 4) relança
    if filas_vivas:
        return True, log + [f'A fila já está rodando (processo {filas_vivas[0][0]}): não liguei outra.']
    ocupado = quem_usa(celular, procs)
    if ocupado:
        outro = 'celular2' if celular == 'celular1' else 'celular1'
        livre = '' if quem_usa(outro, procs) else f' O {NOMES[outro]} está livre: escolha ele.'
        return False, log + [f'Não liguei: o {nome} está com o robô "{ocupado}".{livre}']
    serial = serial_de(celular)
    if not serial:
        return False, log + [f'Não liguei: o {nome} não aparece no adb (cabo USB / Wi-Fi). Ligue o cabo e tente de novo.']
    env = dict(os.environ, HORST_ADB_SERIAL=serial, PYTHONIOENCODING='utf-8', PYTHONPATH=os.path.join(BASE, 'pylibs'))
    subprocess.Popen([PY, 'rodar_fila.py', '--seguido', '--ignorar-horario'], cwd=BASE, env=env, creationflags=SEM_JANELA)
    time.sleep(4)
    log.append(f'Liguei a fila no {nome} ({serial}).')
    return True, log


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    ok, linhas = destravar(args[0] if args else 'azul', ligar='--sem-ligar' not in sys.argv)
    print('\n'.join(('✔ ' if ok else '✖ ') + l if i == len(linhas) - 1 else '  ' + l for i, l in enumerate(linhas)))
    sys.exit(0 if ok else 1)
