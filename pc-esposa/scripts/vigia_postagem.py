r"""Vigia da fila de postagem (Python puro, sem IA) — Kevin 05/11: "bug = fechar e reabrir".

A cada 30 s: se a fila parou com erro.txt e o motivo é "não postado" comum (nada publicado), arquiva
o erro em erros_resolvidos\, espera 2 min e relança rodar_fila.cmd no Celular 1 (máx. 5 vezes por hora).
NUNCA relança: PARAR existe, robô de afiliados com o aparelho, captcha/login/PIN/bloqueio, INCERTO,
PRODUTO ERRADO ou "postado, mas". Sem erro.txt (Desligar/parada normal) também nunca relança.
Nesses casos só registra; o aviso segue na Central. Log: vigia_postagem.log. Desligar: criar VIGIA_POSTAGEM_PARAR.
"""
import datetime, json, os, re, shutil, subprocess, sys, time

BASE = r'C:\horst\tablet'
ERRO = os.path.join(BASE, 'erro.txt')
LOCK = os.path.join(BASE, 'rodar_fila.lock')
PARAR = os.path.join(BASE, 'PARAR')
LOCK_ROBO = os.path.join(BASE, 'afiliados', 'conferir.lock')
ESTADO = os.path.join(BASE, 'vigia_postagem.json')  # a Central lê: ligado, relançamentos, último evento
DESLIGA = os.path.join(BASE, 'VIGIA_POSTAGEM_PARAR')
LOG = os.path.join(BASE, 'vigia_postagem.log')
CMD = os.path.join(BASE, 'rodar_fila.cmd')
MEU_LOCK = os.path.join(BASE, 'vigia_postagem.lock')
RESOLVIDOS = os.path.join(BASE, 'erros_resolvidos')
MAX_HORA, ESPERA = 5, 120
SEM_JANELA = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
NUNCA = re.compile(r'captcha|login|\bPIN\b|senha|bloque|restri|INCERTO|PRODUTO ERRADO|postado, mas', re.I)


def log(m):
    open(LOG, 'a', encoding='utf-8').write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {m}\n')


def pid_vivo(pid):
    try:  # 22/11: pid reaproveitado por outro programa não é robô vivo
        import pid_real
        return pid_real.e_robo(int(pid))
    except ImportError:
        pass
    except ValueError:
        return False
    try:
        out = subprocess.run(['tasklist', '/FI', f'PID eq {int(pid)}', '/NH'], capture_output=True, text=True,
                             timeout=15, creationflags=SEM_JANELA).stdout
        return str(int(pid)) in out
    except Exception:
        return True  # na dúvida, não relança


def fila_viva():
    try:
        return pid_vivo(open(LOCK).read().strip())
    except Exception:
        return False


def robo_vivo():
    try:
        return pid_vivo(open(LOCK_ROBO).read().strip())
    except Exception:
        return False


def publicar(est):
    agora = time.time()
    try:
        json.dump({'pid': os.getpid(), 'em': agora, 'relancou_na_hora': len([t for t in est.get('tent', []) if agora - t < 3600]),
                   'max_hora': MAX_HORA, 'aguardando': bool(est.get('desde'))},
                  open(ESTADO, 'w', encoding='utf-8'))
    except Exception:
        pass


def relancavel(txt):
    return 'não postado' in txt and not NUNCA.search(txt)


def registra_parar(est):
    """Anota no log quando o PARAR aparece/some. Quem criou o Windows não informa: registra a hora e
    os arquivos do tablet alterados nos 2 min antes (pista de qual sessão mexeu)."""
    tem = os.path.exists(PARAR)
    if est.get('parar') is None:
        est['parar'] = tem
    if tem != est['parar']:
        est['parar'] = tem
        agora = time.time()
        rec = [n for n in os.listdir(BASE) if n.endswith(('.py', '.pyw', '.cmd', '.json'))
               and agora - os.path.getmtime(os.path.join(BASE, n)) < 120][:8]
        log(('PARAR criado' if tem else 'PARAR apagado') + f'; fila viva={fila_viva()}; alterados há <2 min: {rec}')


def ciclo(est):
    registra_parar(est)
    publicar(est)
    if fila_viva() or not os.path.exists(ERRO) or os.path.exists(PARAR):
        est['desde'] = None
        return
    if robo_vivo():  # o robô está com o aparelho: não relança agora (a espera recomeça)
        est['desde'] = None
        return
    txt = open(ERRO, encoding='utf-8', errors='ignore').read()
    if not relancavel(txt):
        if est.get('avisado') != txt:
            est['avisado'] = txt
            log('parada que não relanço: ' + ' | '.join(txt.splitlines()[:3])[:250])
        return
    agora = time.time()
    est['tent'] = [t for t in est.get('tent', []) if agora - t < 3600]
    if len(est['tent']) >= MAX_HORA:
        if est.get('avisado') != 'max':
            est['avisado'] = 'max'
            log(f'esgotei {MAX_HORA} relançamentos em 1 h: deixo parado com o aviso na Central')
        return
    if not est.get('desde'):
        est['desde'] = agora
        log('fila parou por erro comum: espero 2 min e relanço. ' + ' | '.join(txt.splitlines()[1:3])[:200])
        return
    if agora - est['desde'] < ESPERA:
        return
    os.makedirs(RESOLVIDOS, exist_ok=True)
    shutil.move(ERRO, os.path.join(RESOLVIDOS, f'erro_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt'))
    subprocess.Popen(['cmd', '/c', 'start', '/min', '', CMD], cwd=BASE, creationflags=SEM_JANELA)
    est['tent'].append(agora)
    est['desde'] = None
    log(f'relancei a fila: tentativa {len(est["tent"])}/{MAX_HORA} nesta hora')


def main():
    try:
        if pid_vivo(open(MEU_LOCK).read().strip()):
            return
    except Exception:
        pass
    open(MEU_LOCK, 'w').write(str(os.getpid()))
    log('vigia da postagem ligado')
    est = {}
    while not os.path.exists(DESLIGA):
        try:
            ciclo(est)
        except Exception as e:
            log(f'erro no vigia: {e!r}')
        time.sleep(30)
    log('VIGIA_POSTAGEM_PARAR: desligado')


if __name__ == '__main__':
    main()
