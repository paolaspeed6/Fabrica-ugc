# Assiste os vídeos do perfil do criador (nome em layout.json) na Shopee, 15s cada, e passa para o próximo.
# Roda sozinho. Para parar: feche a janela ou crie o arquivo PARAR nesta pasta.
# Xiaomi 1: Live e Vídeo, perfil no canto superior esquerdo.
# Xiaomi 2: a conta do aparelho é outra; o perfil abre digitando o nome.

import json
import os
import random
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAYOUT_PATH = ROOT / "layout.json"
_L0 = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
PERFIL_NOME = _L0["profile_name"]            # nome exibido do perfil (layout.json)
PERFIL_USUARIO = _L0["search_query"].lower()  # usuario digitado na busca (layout.json)
GRADE_BAIXA = {hw for hw, ph in _L0["phones"].items() if ph.get("grade_baixa")}
STATUS = ROOT / "status"
STOP_FILE = ROOT / "PARAR"
# ro.serialno → id da Central. Sem argumento, assiste os dois.
APA_POR_HW = {hw: ph.get("id_central", "") for hw, ph in _L0["phones"].items()}
SIG_PS1 = ROOT / "sig.ps1"
ADB = Path(os.environ.get("HORST_ADB") or r"C:\horst\tablet\platform-tools\adb.exe")
LOCK = threading.Lock()

def log(msg):
    line = f"{datetime.now():%H:%M:%S} {msg}"
    print(line, flush=True)
    STATUS.mkdir(exist_ok=True)
    with LOCK:
        with (STATUS / "assistir.log").open("a", encoding="utf-8") as f:
            f.write(line + "\n")

def load_layout():
    return json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))

def stop_requested():
    return STOP_FILE.exists()

def adb(serial, *args, timeout=25):
    cmd = [str(ADB)]
    if serial:
        cmd += ["-s", serial]
    cmd += list(args)
    proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr

def shell(serial, *args, timeout=20):
    return adb(serial, "shell", *args, timeout=timeout)

def unique_devices():
    code, out, err = adb(None, "devices")
    text = out.decode("utf-8", "replace")
    ids = []
    for line in text.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            ids.append(parts[0])
    chosen = {}
    for serial in ids:
        code, out, err = shell(serial, "getprop", "ro.serialno")
        hw = out.decode("utf-8", "replace").strip()
        if not hw:
            continue
        prev = chosen.get(hw)
        if prev is None or (":" in prev and ":" not in serial):
            chosen[hw] = serial
    return chosen

def wake(serial):
    shell(serial, "input", "keyevent", "224")

def focus(serial):
    code, out, err = shell(serial, "dumpsys", "window", timeout=12)
    for line in out.decode("utf-8", "replace").splitlines():
        if "mCurrentFocus" in line:
            return line.strip()
    return ""

def dump_ui(serial):
    remote = "/sdcard/openbot_ui.xml"
    code, out, err = shell(serial, "uiautomator", "dump", remote, timeout=15)
    msg = (out + err).decode("utf-8", "replace")
    if "dumped" not in msg.lower():
        return None
    local = STATUS / f"ui-{serial.replace(':', '_')}.xml"
    code, out, err = adb(serial, "pull", remote, str(local), timeout=15)
    if not local.exists() or local.stat().st_size < 50:
        return None
    try:
        return ET.parse(local).getroot()
    except ET.ParseError:
        return None

def node_text(node):
    return ((node.attrib.get("text") or "") + " " + (node.attrib.get("content-desc") or "")).strip()

def texts_of(root):
    if root is None:
        return ""
    parts = []
    for node in root.iter("node"):
        label = node_text(node)
        if label:
            parts.append(label)
    return "\n".join(parts)

def center(bounds):
    a, b = bounds.split("][")
    x1, y1 = [int(v) for v in a.strip("[]").split(",")]
    x2, y2 = [int(v) for v in b.strip("[]").split(",")]
    return (x1 + x2) // 2, (y1 + y2) // 2

def find_center(root, text=None, desc=None):
    if root is None:
        return None
    for node in root.iter("node"):
        if text and text not in (node.attrib.get("text") or ""):
            continue
        if desc and desc not in (node.attrib.get("content-desc") or ""):
            continue
        bounds = node.attrib.get("bounds")
        if bounds:
            return center(bounds)
    return None

def tap(serial, x, y):
    shell(serial, "input", "tap", str(x), str(y))

def swipe(serial, layout, direction, variar=False):
    x = random.randint(150, 280) if variar else layout["swipe_x"]
    ms = random.randint(220, 420) if variar else layout["swipe_ms"]
    y1 = layout["swipe_y_from"]
    y2 = layout["swipe_y_to"]
    if direction == "down":
        y1, y2 = y2, y1
    shell(serial, "input", "swipe", str(x), str(y1), str(x), str(y2), str(ms))

def screencap(serial, path):
    for _ in range(2):
        code, out, err = adb(serial, "exec-out", "screencap", "-p", timeout=15)
        if out.startswith(b"\x89PNG"):
            path.write_bytes(out)
            return True
        time.sleep(0.4)
    return False

def image_sig(serial, label, crop, white=None):
    STATUS.mkdir(exist_ok=True)
    png = STATUS / f"tela-{label}.png"
    if not screencap(serial, png):
        return None, None
    args = [str(crop[0]), str(crop[1]), str(crop[2]), str(crop[3])]
    if white:
        args += [str(white[0]), str(white[1]), str(white[2]), str(white[3])]
    proc = None
    # Os dois celulares não podem abrir o PowerShell juntos: o Add-Type falha e a faixa volta vazia.
    with LOCK:
        for _ in range(3):
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SIG_PS1), str(png), *args],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                break
            time.sleep(0.4)
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if not lines:
        if "grade" in label:
            err = (proc.stderr or "").strip().splitlines()
            log(f"{label} medida vazia code={proc.returncode} {err[-1] if err else ''}")
        return None, None
    branco = None
    if len(lines) > 1:
        try:
            branco = float(lines[1].replace(",", "."))
        except ValueError:
            branco = None
    if "grade" in label and (branco is None or branco >= 0.5):
        log(f"{label} medida {branco}")
    return lines[0], branco


def caption_sig(serial, label):
    assinatura, _branco = image_sig(serial, label, (8, 1268, 560, 60))
    return assinatura

def kind_of(serial):
    activity = focus(serial)
    if "NativePlayerActivity" in activity:
        return "player", None
    root = dump_ui(serial)
    blob = texts_of(root)
    if eh_perfil_horst(root):
        return "profile", root
    if "Espectadores" in blob or "Diga alguma coisa" in blob:
        return "live", root
    if "Postar vídeo" in blob and "Curtido" not in blob:
        return "empty", root
    if "NativePlayerActivity" in activity:
        return "player", root
    if na_aba_live(root):
        return "live_tab", root
    return "other", root

def sleep_ok(seconds):
    end = time.time() + seconds
    while time.time() < end:
        if stop_requested():
            return False
        time.sleep(min(1, end - time.time()))
    return True

def tap_marker(serial, root, text=None, desc=None, fallback=None):
    point = find_center(root, text=text, desc=desc)
    if point is None and fallback:
        point = fallback["x"], fallback["y"]
    if point is None:
        return False
    tap(serial, point[0], point[1])
    return True

def na_aba_live(root):
    """A aba Live e Vídeo de verdade. O texto do menu de baixo também aparece na aba de produtos."""
    if root is None:
        return False
    if find_center(root, desc="click search icon") is None:
        return False
    blob = texts_of(root)
    return "Para você" in blob or ("Vídeos" in blob and "Lives" in blob)


def eh_perfil_horst(root):
    blob = texts_of(root)
    if not blob or "Criadores de Conteúdo" in blob or eh_busca_produto(root):
        return False
    baixo = blob.lower()
    if PERFIL_NOME in blob and "Vídeos" in blob:
        return True
    if "Curtido" in blob and (PERFIL_NOME in blob or PERFIL_USUARIO in baixo):
        return True
    return all(word in blob for word in ("Ao Vivo", "Produtos", "Curtido"))


def ir_para_aba_live(serial, layout):
    for _ in range(5):
        if stop_requested():
            return None
        root = dump_ui(serial)
        if na_aba_live(root):
            log("aba Live e Vídeo confirmada")
            return root
        blob = texts_of(root)
        if eh_busca_produto(root) or "Buscar na Shopee" in blob or "Criadores de Conteúdo" in blob:
            shell(serial, "input", "keyevent", "4")
            time.sleep(1)
            continue
        if not tap_marker(serial, root, text=layout["live_tab"]["text"], fallback=layout["live_tab"]):
            shell(serial, "input", "keyevent", "4")
            time.sleep(1)
            continue
        time.sleep(2)
    log("não entrei na aba Live e Vídeo")
    return None

def digitar(serial, texto, limpar=False):
    if limpar:
        for _ in range(24):
            shell(serial, "input", "keyevent", "67")
            time.sleep(0.02)
    for ch in texto:
        if stop_requested():
            return
        shell(serial, "input", "text", ch)
        time.sleep(0.12)


def fechar_e_abrir(serial, label):
    log(f"{label} fechando e abrindo a Shopee")
    wake(serial)
    shell(serial, "am", "force-stop", "com.shopee.br")
    time.sleep(1)
    shell(serial, "am", "start", "-n", "com.shopee.br/com.shopee.app.ui.home.HomeActivity_")
    time.sleep(5)


def eh_busca_produto(root):
    """Lista do marketplace. O perfil do criador também tem a aba Produtos, então não basta essa palavra."""
    blob = texts_of(root)
    if not blob:
        return False
    if "Curtido" in blob and ("Vídeos" in blob or PERFIL_NOME in blob or PERFIL_USUARIO in blob.lower()):
        return False
    marcas = ("Filtro", "Relevância", "Ver Loja", "Vendido", "Enviado De")
    return sum(marca in blob for marca in marcas) >= 2


def grade_no_fim(serial, label):
    """O vazio debaixo da última fileira. A fileira em si não é branca, só o espaço abaixo dela."""
    # No perfil azul, essa faixa inclui o fundo branco do cabeçalho e gera falso positivo.
    # A detecção de fim por imagem estável durante a rolagem continua ativa.
    if serial in GRADE_BAIXA:
        return False
    branco = None
    for _ in range(2):
        _, branco = image_sig(serial, label + "-grade", (40, 420, 640, 200), (16, 1372, 500, 70))
        if branco is not None:
            break
    if branco is not None and branco >= 0.85:
        log(f"{label} faixa {branco}")
        return True
    return False


def _rolar_grade(serial, y1, y2):
    shell(serial, "input", "swipe", "180", str(y1), "180", str(y2), "220")
    time.sleep(1.0)


def medir_fim(serial, label):
    """Rola até o fim. Devolve (chegou, gestos). O gesto sobe o dedo e revela os vídeos antigos."""
    root = dump_ui(serial)
    if eh_busca_produto(root):
        log(f"{label} busca de produto, não rolo")
        shell(serial, "input", "keyevent", "4")
        time.sleep(1)
        return False, 0
    if grade_no_fim(serial, label):
        log(f"{label} chegou no fim da grade (faixa vazia)")
        return True, 0
    anterior = None
    iguais = 0
    for n in range(80):
        if stop_requested():
            return False, n
        _rolar_grade(serial, 1280, 360)
        if grade_no_fim(serial, label):
            log(f"{label} chegou no fim da grade (faixa vazia)")
            return True, n + 1
        agora, _branco = image_sig(serial, label + "-grade", (40, 420, 640, 400))
        if agora and agora == anterior:
            iguais += 1
            if iguais >= 2:
                log(f"{label} chegou no fim da grade (parou de mover)")
                return True, n + 1
        else:
            iguais = 0
        anterior = agora
        if n and n % 10 == 0:
            log(f"{label} ainda rolando a grade, {n}")
    log(f"{label} não cheguei no primeiro vídeo")
    return False, 80


def scroll_ate_o_fim(serial, label):
    """Rola até a grade parar ou até sobrar a faixa branca do fim. Não abre vídeo no meio."""
    chegou, _passos = medir_fim(serial, label)
    return chegou


def voltar_ao_topo(serial, label):
    """Desce o dedo até a grade parar no começo, onde estão os vídeos novos."""
    anterior = None
    iguais = 0
    for n in range(80):
        if stop_requested():
            return False
        _rolar_grade(serial, 360, 1280)
        agora, _branco = image_sig(serial, label + "-topo", (40, 420, 640, 400))
        if agora and agora == anterior:
            iguais += 1
            if iguais >= 2:
                log(f"{label} voltou ao começo da grade")
                return True
        else:
            iguais = 0
        anterior = agora
        if n and n % 10 == 0:
            log(f"{label} ainda voltando ao começo, {n}")
    log(f"{label} não confirmei o começo da grade")
    return False


def ir_para_o_meio(serial, label):
    """Mede a grade até o fim e volta metade dos gestos. O meio fica no centro da tela."""
    if grade_no_fim(serial, label) and not voltar_ao_topo(serial, label):
        return False
    chegou, passos = medir_fim(serial, label)
    if not chegou:
        return False
    voltas = passos // 2
    log(f"{label} meio da grade, volto {voltas} de {passos}")
    for _ in range(voltas):
        if stop_requested():
            return False
        _rolar_grade(serial, 360, 1280)
    return True


MEIO_CELLS = [[360, 730], [120, 730], [600, 730], [360, 420], [360, 1040]]


def abrir_celulas(serial, layout, label, celulas, de_onde):
    for x, y in celulas:
        if stop_requested():
            return False
        _, branco = image_sig(
            serial, label + "-celula", (8, 8, 40, 20), (x - 70, y - 80, 140, 160)
        )
        if branco is not None and branco >= 0.72:
            continue
        tap(serial, x, y)
        time.sleep(2.5)
        kind, root = kind_of(serial)
        blob = texts_of(root)
        if "Postar" in blob:
            shell(serial, "input", "keyevent", "4")
            time.sleep(1)
            continue
        if "Removido" in blob:
            continue
        if kind == "player":
            log(f"{label} abriu um vídeo do {de_onde}")
            return True
    return False


def abrir_mais_antigo(serial, layout, label):
    return abrir_celulas(serial, layout, label, layout["oldest_cells"], "fim da grade")


def achar_criador(root):
    """O nome do usuário na seção Criadores. O meio da linha é vazio e o toque não abre."""
    if root is None:
        return None
    blob = texts_of(root).lower()
    if "criadores" not in blob or "seguidores" not in blob:
        return None
    for node in root.iter("node"):
        proprio = (node.attrib.get("text") or "").strip().lower()
        bounds = node.attrib.get("bounds") or ""
        if proprio != PERFIL_USUARIO or not bounds:
            continue
        try:
            y1 = int(bounds.split(",")[1].split("]")[0])
        except ValueError:
            continue
        if y1 < 200:
            continue
        return center(bounds)
    return None


def search_profile(serial, layout):
    root = ir_para_aba_live(serial, layout)
    if root is None:
        return False
    if not tap_marker(serial, root, desc=layout["search_icon"]["desc"], fallback=layout["search_icon"]):
        log("não achei a busca da aba Live e Vídeo")
        return False
    time.sleep(1.2)
    digitar(serial, layout.get("search_query") or PERFIL_USUARIO, limpar=True)
    time.sleep(2.5)
    for _tentativa in range(6):
        root = dump_ui(serial)
        if eh_busca_produto(root):
            log("busca de produto no lugar do perfil, volto")
            shell(serial, "input", "keyevent", "4")
            time.sleep(1)
            return False
        alvo = achar_criador(root)
        if alvo:
            log(f"toquei o criador {PERFIL_USUARIO} em {alvo[0]},{alvo[1]}")
            tap(serial, alvo[0], alvo[1])
            time.sleep(2.5)
            return True
        time.sleep(1.2)
    return False


def parece_perfil(serial, kind):
    return kind == "profile"


def abrir_da_grade(serial, layout, label, ordem="fim_comeco"):
    if ordem == "comeco_fim":
        return abrir_celulas(serial, layout, label, layout["cells"], "começo da grade")
    if ordem in ("meio_comeco", "meio_fim"):
        if not ir_para_o_meio(serial, label):
            return False
        return abrir_celulas(serial, layout, label, MEIO_CELLS, "meio da grade")
    if not scroll_ate_o_fim(serial, label):
        return False
    return abrir_mais_antigo(serial, layout, label)


def open_profile_video(serial, layout, phone):
    label = phone["label"]
    buscas = 0
    for _ in range(6):
        if stop_requested():
            return False
        kind, root = kind_of(serial)
        log(f"{label} tela={kind}")
        if parece_perfil(serial, kind):
            return abrir_da_grade(serial, layout, label, phone.get("ordem") or "fim_comeco")
        if kind == "player":
            # Um voltar sai do vídeo para a grade. Se continuar no vídeo, fica nele.
            shell(serial, "input", "keyevent", "4")
            time.sleep(1.4)
            kind2, _root2 = kind_of(serial)
            if parece_perfil(serial, kind2):
                return abrir_da_grade(serial, layout, label, phone.get("ordem") or "fim_comeco")
            if kind2 == "player":
                log(f"{label} o vídeo não soltou a grade, sigo neste")
                return True
        if phone["mode"] == "perfil_conectado":
            root = ir_para_aba_live(serial, layout)
            if root is None:
                return False
            if not tap_marker(serial, root, desc=layout["profile_icon"]["desc"], fallback=layout["profile_icon"]):
                return False
            time.sleep(2.5)
            continue
        if buscas >= 2:
            log(f"{label} não achei o perfil {PERFIL_USUARIO}")
            return False
        buscas += 1
        if not search_profile(serial, layout):
            shot = STATUS / f"layout-{label}.png"
            screencap(serial, shot)
            log(f"{label} não achei {PERFIL_USUARIO}, print em {shot.name}")
            continue
        for _espera in range(4):
            time.sleep(1.5)
            kind, root = kind_of(serial)
            log(f"{label} depois da busca tela={kind}")
            if parece_perfil(serial, kind):
                return abrir_da_grade(serial, layout, label, phone.get("ordem") or "fim_comeco")
            if kind == "player":
                log(f"{label} abriu direto no vídeo")
                return True
            if eh_busca_produto(root):
                log(f"{label} abriu produto, volto")
                shell(serial, "input", "keyevent", "4")
                time.sleep(1)
                break
    return False

def save_state(state):
    with LOCK:
        (STATUS / "estado.json").write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
        )

def gravar_pid():
    STATUS.mkdir(exist_ok=True)
    (STATUS / "pid.txt").write_text(str(os.getpid()), encoding="utf-8")

def limpar_pid():
    try:
        caminho = STATUS / "pid.txt"
        if caminho.is_file() and caminho.read_text(encoding="utf-8").strip() == str(os.getpid()):
            caminho.unlink()
    except OSError:
        pass

ORDEM_SENTIDO = {
    "fim_comeco": "down",
    "comeco_fim": "up",
    "meio_comeco": "down",
    "meio_fim": "up",
}

def pedido_e_ordem():
    nomes = []
    ordem = "fim_comeco"
    for arg in sys.argv[1:]:
        for parte in str(arg).split(","):
            parte = parte.strip()
            if not parte:
                continue
            if parte in ORDEM_SENTIDO:
                ordem = parte
            else:
                nomes.append(parte)
    return nomes, ordem

def gravar_alvos(aparelhos, ordem):
    STATUS.mkdir(exist_ok=True)
    (STATUS / "alvos.json").write_text(
        json.dumps({"pid": os.getpid(), "aparelhos": aparelhos, "ordem": ordem}, ensure_ascii=False),
        encoding="utf-8",
    )

def limpar_alvos():
    try:
        caminho = STATUS / "alvos.json"
        if not caminho.is_file():
            return
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        if int(dados.get("pid") or 0) == os.getpid():
            caminho.unlink()
    except (OSError, ValueError, json.JSONDecodeError):
        pass

def watch_phone(serial, layout, phone, state):
    label = phone["label"]
    direction = phone.get("sentido") or "down"
    watched = 0
    travou = 0
    kind, _root = kind_of(serial)
    if grade_no_fim(serial, label):
        log(f"{label} já está no fim da grade")
    elif kind == "profile":
        log(f"{label} segue na grade do perfil")
    else:
        fechar_e_abrir(serial, label)
    if not open_profile_video(serial, layout, phone):
        log(f"{label} não abriu o vídeo mais antigo")
    while not stop_requested():
        try:
            wake(serial)
            kind, _root = kind_of(serial)
            if kind != "player":
                log(f"{label} saiu do vídeo, abrindo o perfil de novo")
                if not open_profile_video(serial, layout, phone):
                    if not sleep_ok(15):
                        return
                    continue
                travou = 0
            segundos = random.randint(layout["watch_min"], layout["watch_max"])
            before = caption_sig(serial, label)
            log(f"{label} assistindo {segundos}s")
            if not sleep_ok(segundos):
                return
            if not sleep_ok(random.uniform(0.2, 1.1)):
                return
            swipe(serial, layout, direction, variar=True)
            time.sleep(1.8)
            after = caption_sig(serial, label)
            if before and after and before == after:
                other = "down" if direction == "up" else "up"
                swipe(serial, layout, other)
                time.sleep(1.8)
                flipped = caption_sig(serial, label)
                if flipped and flipped != after:
                    direction = other
                    log(f"{label} o vídeo seguinte ficou no outro sentido")
                    watched += 1
                    travou = 0
                else:
                    travou += 1
                    direction = other
                    log(f"{label} não mudou de vídeo, sentido {direction} ({travou})")
                    if travou >= 3:
                        log(f"{label} travou no mesmo vídeo, reabro o perfil")
                        shell(serial, "input", "keyevent", "4")
                        time.sleep(1)
                        open_profile_video(serial, layout, phone)
                        travou = 0
            else:
                travou = 0
                watched += 1
                log(f"{label} passou para o próximo, total {watched}")
            state[label] = {
                "serial": serial,
                "mode": phone["mode"],
                "assistidos": watched,
                "quando": datetime.now().isoformat(timespec="seconds"),
            }
            save_state(state)
        except Exception as exc:
            log(f"{label} erro {exc}")
            if not sleep_ok(8):
                return

def main():
    if not ADB.exists():
        log(f"adb não encontrado em {ADB}")
        return
    if STOP_FILE.exists():
        STOP_FILE.unlink()
    gravar_pid()
    try:
        _rodar()
    finally:
        limpar_pid()
        limpar_alvos()

def _rodar():
    layout = load_layout()
    STATUS.mkdir(exist_ok=True)
    pedido, ordem = pedido_e_ordem()
    log(f"ordem {ordem}")
    phones = unique_devices()
    if not phones:
        log("nenhum celular no adb")
        return
    state = {}
    threads = []
    alvos = []
    for hw, serial in phones.items():
        phone = layout["phones"].get(hw)
        if not phone:
            log(f"sem regra para {hw} em {serial}")
            continue
        aparelho = APA_POR_HW.get(hw) or ""
        if pedido and aparelho not in pedido:
            log(f"{phone['label']} fora do pedido, não assiste")
            continue
        log(f"{phone['label']} {serial} modo {phone['mode']}")
        phone = dict(phone)
        phone["ordem"] = ordem
        phone["sentido"] = ORDEM_SENTIDO[ordem]
        # Aparelho com 'grade_baixa': true no layout.json tem cabeçalho de perfil mais alto (grade mais abaixo).
        # Calibrar estes pontos para o aparelho dela (ver INSTRUCOES).
        phone_layout = dict(layout)
        if serial in GRADE_BAIXA:
            phone_layout["cells"] = [[120, 900], [360, 900], [600, 900],
                                     [120, 1190], [360, 1190], [600, 1190]]
            phone_layout["oldest_cells"] = [[600, 1450], [360, 1450], [120, 1450],
                                            [600, 1300], [360, 1300], [120, 1300]]
        if aparelho:
            alvos.append(aparelho)
        thread = threading.Thread(
            target=watch_phone, args=(serial, phone_layout, phone, state), name=phone["label"], daemon=False
        )
        thread.start()
        threads.append(thread)
    if not threads:
        log("nenhum celular no pedido")
        return
    gravar_alvos(alvos, ordem)
    for thread in threads:
        thread.join()
    log("parou")

if __name__ == "__main__":
    main()
