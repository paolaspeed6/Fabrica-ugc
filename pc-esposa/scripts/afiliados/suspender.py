r"""Colocar o PC em ESPERA (S3) quando um captcha fica sem resposta à noite (pedido do Kevin, 05/11).

Regras (sem IA):
- a qualquer hora (Kevin, 05/11); HORST_SUSPENDER_HORAS="22-8" limita a um horário;
- nunca se existir afiliados\NAO_SUSPENDER (chave para desligar);
- nunca se algo além da conferência estiver trabalhando: fila de postagem (lock), render/voz do
  YouTube (ffmpeg, node, Applio/RVC, youtube-espaco, video2_ia), outro python, download do Chrome
  em andamento (.crdownload) ou Google Drive sincronizando (CPU alta);
- suspende com SetSuspendState('Suspend') — espera, não hiberna e não fecha nenhum app.
- HORST_SIMULAR_SUSPENSAO=1: só registra o que faria (para teste).
"""
import datetime, glob, json, os, subprocess, time

BASE = r'C:\horst\tablet'
PASTA = os.path.join(BASE, 'afiliados')
CHAVE = os.path.join(PASTA, 'NAO_SUSPENDER')
LOCK_FILA = os.path.join(BASE, 'rodar_fila.lock')
SEM_JANELA = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
# processos que são da própria conferência / Central (podem estar rodando)
NOSSOS = ('conferir_afiliados.py', 'rodar_candidatos.py', 'central_horst.pyw', 'status_card.py',
          'vigia_conferencia.py', 'suspender.py', 'vigia_postagem.py')
PESADOS = ('ffmpeg.exe', 'ffprobe.exe', 'node.exe', 'blender.exe', 'handbrakecli.exe', 'obs64.exe')
MARCAS = ('youtube-espaco', 'video2_ia', 'applio', 'core.py infer', 'rvc\\')  # 'render' não: Edge/Claude têm --type=renderer


def _ps(cmd, timeout=40):
    r = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', cmd], capture_output=True,
                       timeout=timeout, creationflags=SEM_JANELA)
    return r.stdout.decode('utf-8', 'ignore')


def _pid_vivo(pid):
    try:
        out = subprocess.run(['tasklist', '/FI', f'PID eq {int(pid)}', '/NH'], capture_output=True, text=True,
                             timeout=15, creationflags=SEM_JANELA).stdout
        return str(int(pid)) in out
    except Exception:
        return False


def processos():
    txt = _ps('[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-CimInstance Win32_Process | '
              'Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress')
    try:
        d = json.loads(txt)
        return d if isinstance(d, list) else [d]
    except Exception:
        return None


def drive_ocupado(seg=5, limite=0.15):
    """Google Drive usando mais de ~15% de um núcleo = sincronizando."""
    cmd = '(Get-Process GoogleDriveFS -ErrorAction SilentlyContinue | Measure-Object CPU -Sum).Sum'
    try:
        a = float(_ps(cmd).strip() or 0)
        time.sleep(seg)
        b = float(_ps(cmd).strip() or 0)
        return (b - a) / seg > limite
    except Exception:
        return False


def no_horario(agora=None):
    agora = agora or datetime.datetime.now()
    try:
        ini, fim = (int(x) for x in os.environ.get('HORST_SUSPENDER_HORAS', '0-24').split('-'))
    except Exception:
        ini, fim = 22, 8
    h = agora.hour
    return (h >= ini or h < fim) if ini > fim else (ini <= h < fim)


def ocupado(lista=None):
    """Devolve o motivo se algo além da conferência estiver trabalhando no PC, senão ''."""
    try:
        if os.path.exists(LOCK_FILA) and _pid_vivo(open(LOCK_FILA).read().strip()):
            return 'fila de postagem rodando'
    except Exception:
        pass
    lista = processos() if lista is None else lista
    if lista is None:
        return 'não consegui listar os processos'
    meu = os.getpid()
    robos = sum(1 for p in lista if 'conferir_afiliados.py' in (p.get('CommandLine') or '').lower())
    if robos > 1:
        return 'outro aparelho ainda conferindo'
    for p in lista:
        nome = (p.get('Name') or '').lower()
        cl = (p.get('CommandLine') or '').lower()
        if p.get('ProcessId') == meu:
            continue
        if nome in PESADOS:
            return f'{nome} rodando'
        if any(m in cl for m in MARCAS) and 'claude' not in nome:
            return f'trabalho do YouTube/voz rodando ({nome})'
        if nome in ('python.exe', 'pythonw.exe') and not any(n in cl for n in NOSSOS):
            return f'outro python rodando ({cl[:80]})'
    pastas = [os.path.join(os.path.expanduser('~'), 'Downloads')]
    if any(glob.glob(os.path.join(d, '**', '*.crdownload'), recursive=True) for d in pastas):
        return 'download do Chrome em andamento'
    if drive_ocupado():
        return 'Google Drive sincronizando'
    return ''


def pode_suspender():
    if os.path.exists(CHAVE):
        return False, 'chave NAO_SUSPENDER ligada'
    if not no_horario():
        return False, 'fora do horário configurado'
    m = ocupado()
    if m:
        return False, m
    return True, ''


def suspender():
    """Espera (S3). Não hiberna (força=False, desliga eventos de acordar = False)."""
    if os.environ.get('HORST_SIMULAR_SUSPENSAO') == '1':
        return 'simulado'
    _ps("Add-Type -AssemblyName System.Windows.Forms; "
        "[void][System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)", timeout=120)
    return 'suspenso'


if __name__ == '__main__':
    print('horário noite:', no_horario(), '| ocupado:', ocupado() or 'nada', '| pode:', pode_suspender())
