r"""Vigia da conferência por aparelho (Python puro, sem IA) — 06/11, um robô por celular.

A cada 30 s, para cada aparelho de aparelhos.json com robô de afiliados (celular1, celular2):
- vivo (candidatos_<id>.lock ou conferir_<id>.lock com processo vivo)   -> nada;
- parou: lê afiliados\parada_<id>.txt (motivo gravado pelo robô; sem ele, o final do log):
    normal (PARAR, META, lista acabou) -> não relança;
    captcha, login, PIN, bateria        -> não relança (espera o Kevin);
    bloqueio/restrição da conta         -> não relança e nem tenta de novo;
    qualquer outro erro                 -> espera 2 min e relança SÓ esse aparelho
                                           (ligar_aparelho.cmd <id>), máx. 5 vezes por hora por aparelho.
- esgotou as tentativas ou bloqueio: grava VIGIA_ESGOTADO_<id>.txt e o aviso no status do aparelho.
  Depois de 15 min sem resposta, se nenhum aparelho estiver rodando e nada mais estiver trabalhando no
  PC (suspender.pode_suspender), põe o PC em espera uma vez.

Nunca resolve captcha, nunca faz login. Só liga aparelho que já estava trabalhando (viu vivo).
Desligar: criar afiliados\VIGIA_PARAR. Parar um aparelho: PARAR_<id> (o vigia respeita).
"""
import datetime, json, os, re, subprocess, sys, time

BASE = r'C:\horst\tablet'
PASTA = os.path.join(BASE, 'afiliados')
LOG_ROBO = os.path.join(PASTA, 'conferir_afiliados.log')
LOG = os.path.join(PASTA, 'vigia_conferencia.log')
PARAR = os.path.join(PASTA, 'PARAR')
DESLIGA = os.path.join(PASTA, 'VIGIA_PARAR')
MEU_LOCK = os.path.join(PASTA, 'vigia.lock')
LIGAR = os.path.join(PASTA, 'ligar_aparelho.cmd')
IDS = ('celular1', 'celular2')
MAX_HORA, ESPERA, ESPERA_RESPOSTA = 5, 120, 15 * 60
SEM_JANELA = getattr(subprocess, 'CREATE_NO_WINDOW', 0)

NORMAL = re.compile(r'META batida|lista acabou|PARAR encontrado|arquivo PARAR|PARAR durante|^normal', re.I)
BLOQUEIO = re.compile(r'BLOQUEIO|RESTRITA|restri', re.I)
ESPERA_KEVIN = re.compile(r'captcha|login|\bPIN\b|senha|bateria', re.I)


def log(m):
    linha = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} [vigia] {m}'
    print(linha, flush=True)
    open(LOG, 'a', encoding='utf-8').write(linha + '\n')


def pid_vivo(pid):
    try:  # 22/11: pid reaproveitado por outro programa não é robô vivo
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    except ValueError:
        return False
    except Exception:
        return True  # na dúvida, não relança


def vivo(aid):
    for nome in (f'candidatos_{aid}.lock', f'conferir_{aid}.lock'):
        try:
            if pid_vivo(open(os.path.join(PASTA, nome)).read().strip()):
                return True
        except OSError:
            pass
    return False


def motivo(aid):
    """Motivo gravado pelo robô; sem arquivo (robô antigo), o último PAROU/erro do log."""
    try:
        return open(os.path.join(PASTA, f'parada_{aid}.txt'), encoding='utf-8').read().strip()
    except OSError:
        pass
    try:
        ls = open(LOG_ROBO, encoding='utf-8', errors='ignore').read().splitlines()[-300:]
    except OSError:
        return ''
    for l in reversed(ls):
        if re.search(r'PAROU|META batida|lista acabou|PARAR encontrado|erro inesperado', l):
            return l.replace('(captcha/login/erro)', '')
    return ''


def classificar(m):
    if BLOQUEIO.search(m):
        return 'bloqueio'
    if ESPERA_KEVIN.search(m):
        return 'espera_kevin'
    if NORMAL.search(m):
        return 'normal'
    return 'erro'


def relancar(aid):
    if os.environ.get('HORST_VIGIA_SIMULAR') == '1':
        return 'simulado'
    subprocess.Popen(['cmd', '/c', LIGAR, aid], cwd=BASE, creationflags=SEM_JANELA)
    return 'ok'


def avisar(aid, texto):
    try:
        json.dump({'state': 'alerta', 'detail': texto, 'linhas': [], 'quando': f'{datetime.datetime.now():%H:%M:%S}'},
                  open(os.path.join(PASTA, f'status_{aid}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception:
        pass


def esgotar(est, aid, tipo, m):
    txt = f'{datetime.datetime.now():%d/%m %H:%M} {aid} {tipo}\n{m}\n'
    open(os.path.join(PASTA, f'VIGIA_ESGOTADO_{aid}.txt'), 'w', encoding='utf-8').write(txt)
    avisar(aid, f'{aid}: {tipo}. {m[-120:]}')
    log(f'{aid} {tipo}: {m[:160]}')
    est['esgotou_em'] = time.time()


def talvez_suspender(geral):
    """15 min sem resposta depois de esgotar/bloqueio: suspende 1 vez se nada mais estiver rodando."""
    t0 = geral.get('esgotou_em')
    if not t0 or geral.get('suspendeu') or time.time() - t0 < ESPERA_RESPOSTA:
        return
    if any(vivo(a) for a in IDS) or time.time() - geral.get('checou', 0) < 300:
        return
    geral['checou'] = time.time()
    sys.path.insert(0, PASTA)
    import suspender
    ok, por = suspender.pode_suspender()
    if not ok:
        log(f'15 min sem resposta, mas não suspendo: {por}')
        return
    log('15 min sem resposta e nada rodando: PC em espera')
    geral['suspendeu'] = True
    log(f'PC voltou da espera ({suspender.suspender()}); nada é religado sozinho')


def ciclo_aparelho(est, aid, geral):
    if vivo(aid):
        est.update(viu_vivo=True, desde=None)
        if est.pop('esgotado', None):
            geral.pop('esgotou_em', None)
            geral.pop('suspendeu', None)
            with_arq = os.path.join(PASTA, f'VIGIA_ESGOTADO_{aid}.txt')
            if os.path.exists(with_arq):
                os.remove(with_arq)
        return
    if not est.get('viu_vivo') or est.get('esgotado'):
        return  # nunca liga aparelho que não estava trabalhando
    if os.path.exists(PARAR) or os.path.exists(f'{PARAR}_{aid}'):
        est['desde'] = None
        return
    m = motivo(aid)
    tipo = classificar(m)
    if m != est.get('ultimo'):
        est['ultimo'] = m
        log(f'{aid} parou ({tipo}): {m[:200] or "sem mensagem"}')
    if tipo == 'normal':
        est['viu_vivo'] = False
        return
    if tipo == 'espera_kevin':
        return
    if tipo == 'bloqueio':
        est['esgotado'] = True
        return esgotar(geral, aid, 'bloqueio/restrição: não relanço', m)
    agora = time.time()
    est['tent'] = [t for t in est.get('tent', []) if agora - t < 3600]
    if len(est['tent']) >= MAX_HORA:
        est['esgotado'] = True
        return esgotar(geral, aid, f'esgotou {MAX_HORA} relançamentos em 1 h', m)
    if not est.get('desde'):
        est['desde'] = agora
        log(f'{aid}: espero {ESPERA // 60} min antes de relançar')
        return
    if agora - est['desde'] < ESPERA:
        return
    r = relancar(aid)
    est['tent'].append(agora)
    est['desde'] = None
    log(f'{aid}: relancei ({r}), tentativa {len(est["tent"])}/{MAX_HORA} nesta hora')


def main():
    try:
        if pid_vivo(open(MEU_LOCK).read().strip()):
            print('vigia já está rodando')
            return
    except OSError:
        pass
    open(MEU_LOCK, 'w').write(str(os.getpid()))
    log(f'vigia por aparelho ligado ({", ".join(IDS)}; máx {MAX_HORA}/h por aparelho)')
    estados, geral = {a: {} for a in IDS}, {}
    try:
        while not os.path.exists(DESLIGA):
            for a in IDS:
                try:
                    ciclo_aparelho(estados[a], a, geral)
                except Exception as e:
                    log(f'{a}: erro no vigia: {e!r}')
            try:
                talvez_suspender(geral)
            except Exception as e:
                log(f'suspender: {e!r}')
            time.sleep(30)
        log('VIGIA_PARAR encontrado: desligado')
    finally:
        try:
            os.remove(MEU_LOCK)
        except OSError:
            pass


if __name__ == '__main__':
    main()
