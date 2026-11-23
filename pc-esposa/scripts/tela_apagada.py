r"""Mantém a tela FÍSICA do tablet apagada enquanto o robô trabalha (economiza bateria).

Usa o scrcpy 5 em segundo plano, sem janela: `scrcpy -s <serial> --no-window --no-audio -S -w`
(-S = turn-screen-off, -w = stay-awake). O Android continua desenhando a tela, então
`adb screencap` e `input tap/swipe` funcionam normalmente (testado em 05/11/2026).

    import tela_apagada
    tela_apagada.garantir(serial)   # inicia, ou reinicia se caiu (chamar a cada produto)
    tela_apagada.parar()            # no fim (a tela volta a acender ao tocar no tablet)
"""
import os, subprocess

BASE = r'C:\horst\tablet'
SCRCPY = os.path.join(BASE, 'scrcpy', 'scrcpy.exe')
ADB = os.path.join(BASE, 'platform-tools', 'adb.exe')  # o mesmo adb dos scripts (evita 2 servidores brigando)
LOG = os.path.join(BASE, 'afiliados', 'scrcpy.log')
SEM_JANELA = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
TELA_LIGADA = os.path.join(BASE, 'TELA_LIGADA')
_proc = None


def ativo():
    return _proc is not None and _proc.poll() is None


def garantir(serial):
    """Inicia o scrcpy (tela apagada) se não estiver rodando. Nunca derruba quem chamou."""
    global _proc
    if os.path.exists(TELA_LIGADA):  # Kevin quer acompanhar: não apaga a tela (apague o arquivo para voltar)
        return False
    if ativo() or not serial or not os.path.exists(SCRCPY):
        return ativo()
    try:
        env = dict(os.environ, ADB=ADB)
        _proc = subprocess.Popen([SCRCPY, '-s', serial, '--no-window', '--no-audio', '-S', '-w'],
                                 stdout=open(LOG, 'a'), stderr=subprocess.STDOUT, env=env,
                                 creationflags=SEM_JANELA)
        return True
    except Exception:
        _proc = None
        return False


def parar():
    global _proc
    if ativo():
        try:
            _proc.terminate()
            _proc.wait(10)
        except Exception:
            pass
    _proc = None
