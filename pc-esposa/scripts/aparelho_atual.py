r"""Um robô de afiliados por aparelho (Kevin 06/11): nome do aparelho, trava do CSV e reserva de produto.

id_aparelho(): 'celular1', 'celular2'... pelo HORST_ADB_SERIAL (aparelhos.json).
trava_csv():   só um processo por vez escreve no conferidos.csv.
reservar():    dois robôs nunca conferem o mesmo itemId (arquivo criado de forma atômica).
"""
import contextlib, csv, datetime, json, os, re, time

BASE = r'C:\horst\tablet'
PASTA = os.path.join(BASE, 'afiliados')
APARELHOS = os.path.join(BASE, 'aparelhos.json')
CSV = os.path.join(PASTA, 'conferidos.csv')
RESERVAS = os.path.join(PASTA, 'reservas')
TRAVA = CSV + '.trava'
RESERVA_MIN = 30   # reserva sem resultado vence em 30 min (robô caiu no meio do produto)


def id_aparelho(serial=None):
    s = serial or os.environ.get('HORST_ADB_SERIAL') or ''
    try:
        d = json.load(open(APARELHOS, encoding='utf-8-sig'))
        for nome, c in d.items():
            if isinstance(c, dict) and s and s in (c.get('usb'), c.get('wifi')):
                return nome
    except Exception:
        pass
    return re.sub(r'\W+', '_', s) or 'padrao'


def wifi_de(serial=None):
    s = serial or os.environ.get('HORST_ADB_SERIAL') or ''
    if ':' in s:
        return s
    try:
        c = json.load(open(APARELHOS, encoding='utf-8-sig')).get(id_aparelho(s)) or {}
        return c.get('wifi')
    except Exception:
        return None


@contextlib.contextmanager
def trava_csv(limite=120):
    """Trava entre processos. Trava com mais de 3 min é de um processo morto e é retirada."""
    fim = time.time() + limite
    while True:
        try:
            fd = os.open(TRAVA, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(TRAVA) > 180:
                    os.remove(TRAVA)
                    continue
            except OSError:
                pass
            if time.time() > fim:
                raise TimeoutError('conferidos.csv travado por mais de 2 min')
            time.sleep(0.2)
    try:
        yield
    finally:
        os.close(fd)
        with contextlib.suppress(OSError):
            os.remove(TRAVA)


def _item(x):
    return str(x or '').strip().split('.')[-1]


def _arq(item):
    return os.path.join(RESERVAS, re.sub(r'\W+', '_', _item(item)) + '.txt')


def reservar(item, dono):
    """True se este aparelho pode conferir o item. Atômico: o 2º a chegar recebe False."""
    if not _item(item):
        return True
    os.makedirs(RESERVAS, exist_ok=True)
    arq = _arq(item)
    for _ in range(2):
        try:
            fd = os.open(arq, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f'{dono} {datetime.datetime.now():%Y-%m-%d %H:%M:%S}'.encode())
            os.close(fd)
            return True
        except FileExistsError:
            try:
                if open(arq, encoding='utf-8').read().split(' ')[0] == dono:
                    return True
                if time.time() - os.path.getmtime(arq) < RESERVA_MIN * 60:
                    return False
                os.remove(arq)  # venceu: o outro robô caiu no meio
            except OSError:
                return False
    return False


def liberar(item):
    with contextlib.suppress(OSError):
        os.remove(_arq(item))


def ja_conferido(item):
    """O item já tem resultado (que não seja erro) no CSV?"""
    alvo = _item(item)
    if not alvo:
        return False
    try:
        for l in csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';'):
            if _item(l.get('itemId')) == alvo and l.get('decisao') != 'erro':
                return True
    except Exception:
        pass
    return False


def gravar_parada(aid, motivo):
    """Motivo da última parada do robô deste aparelho (o vigia lê)."""
    with contextlib.suppress(OSError):
        open(os.path.join(PASTA, f'parada_{aid}.txt'), 'w', encoding='utf-8').write(str(motivo))


def limpar_parada(aid):
    with contextlib.suppress(OSError):
        os.remove(os.path.join(PASTA, f'parada_{aid}.txt'))
