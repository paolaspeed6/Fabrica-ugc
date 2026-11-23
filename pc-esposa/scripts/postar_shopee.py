r"""Rascunho: posta um Shopee Vídeo no tablet CM8800Ultra via adb.

Uso:
  python postar_shopee.py VIDEO.mp4 LINK_PRODUTO "LEGENDA" [--seco]

--seco : faz tudo e PARA antes de tocar em "Postar" (salva print em gravacao\seco_final.png).

Cada passo: toca, espera, tira print e confere a tela (texto via uiautomator e/ou cor de pixel).
Se a tela não for a esperada, para e diz em qual passo parou. Coordenadas: gravacao\passos.md.

Legenda: usa o teclado ADBKeyboard (com.android.adbkeyboard) para digitar acentos/emoji.
Ele NÃO está instalado; instalar exige o OK do dono (ver mensagem de erro).

AINDA NÃO TESTADO CONTRA A SHOPEE.
"""
import argparse, base64, contextlib, io, os, random, re, subprocess, sys, time

from PIL import Image

ADB = r'C:\horst\tablet\platform-tools\adb.exe'
PASTA = r'C:\horst\tablet\gravacao'
PKG = 'com.shopee.br'
DESTINO = '/sdcard/DCIM/HorstAds'
ARQUIVO_MORTO = '/sdcard/HorstAds_postados'  # pasta antiga: aparece na galeria; enviar() só a esvazia


EM_CAPTCHA = False
OCUPADO = False  # enviando vídeo / reconectando: a tela fica parada de propósito
PRODUTO_TEXTOS = None
TITULO_ESPERADO = None  # nome do produto do link; conferido no 1º de "Minhas Curtidas" (rodar_fila define)
TITULO_CACHE = None     # nome já confirmado deste itemId (titulos.json); rodar_fila define antes de postar
TITULO_APROVADO = None  # 10/11: nome da linha que o Kevin aprovou na Central (titulos.json "_aprovados")
LINHAS_VISTAS = []      # nomes das linhas vistas em Minhas Curtidas (vão para o pendente de aprovação)
PRINT_LISTA = None      # print da lista Adicionar mais útil para o Kevin decidir
SEM_JANELA = getattr(subprocess, 'CREATE_NO_WINDOW', 0)  # adb/powershell sem abrir janela de console
# Endereço do tablet: C:\horst\tablet\aparelhos.json (serial USB e/ou IP:5555 do adb Wi-Fi;
# arquivo mantido por outra sessão, aqui só lido). Prioridade: variável HORST_ADB_SERIAL > USB
# conectado > Wi-Fi (adb connect). Sem o arquivo: serial USB padrão <SERIAL_TABLET>.
APARELHOS = r'C:\horst\tablet\aparelhos.json'
SERIAL_PADRAO = '<SERIAL_TABLET>'
RECONECTAR_MAX = 120  # s tentando reconectar antes de parar com segurança


class Desconectado(Exception):
    """Tablet sumiu do adb e não voltou em RECONECTAR_MAX segundos."""


def enderecos_tablet():
    """(serial_usb, ip_porta) lidos do aparelhos.json, aceitando alguns formatos."""
    import json
    try:
        d = json.load(open(APARELHOS, encoding='utf-8-sig'))
    except Exception:
        return SERIAL_PADRAO, None
    if isinstance(d, dict):
        fixo = os.environ.get('HORST_ADB_SERIAL')  # aparelho da fila: o do endereço pedido, senão o Celular 1
        cand = next((c for c in d.values() if isinstance(c, dict) and fixo and fixo in (c.get('usb'), c.get('wifi'))), None)
        cand = cand or d.get('celular1') or d.get('tablet') or d.get('aparelhos') or d.get('devices') or d
    else:
        cand = d
    if isinstance(cand, list):
        cand = next((x for x in cand if isinstance(x, dict) and
                     ('tablet' in str(x.get('nome', x.get('id', ''))).lower() or 'tablet' in str(x.get('papel', '')).lower())),
                    cand[0] if cand else {})
    if not isinstance(cand, dict):
        return SERIAL_PADRAO, None
    usb = cand.get('serial') or cand.get('usb') or cand.get('serial_usb') or SERIAL_PADRAO
    ip = cand.get('wifi') or cand.get('ip_porta') or cand.get('endereco') or cand.get('ip')
    if ip and ':' not in str(ip):
        ip = f'{ip}:{cand.get("porta", 5555)}'
    return str(usb), (str(ip) if ip else None)


BATIMENTO = 0.0  # última hora em que o script concluiu algo (a vigia de passo olha)


def bater():
    global BATIMENTO
    BATIMENTO = time.time()


def _exec(cmd, timeout):
    """subprocess com timeout de verdade: se estourar, mata e não fica esperando o pipe do adb."""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=SEM_JANELA)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        try:
            p.communicate(timeout=3)
        except Exception:
            pass
        raise
    return subprocess.CompletedProcess(cmd, p.returncode, out, err)


def _estado(serial):
    try:
        r = _exec([ADB, '-s', serial, 'get-state'], 10)
        return r.stdout.decode('utf-8', 'ignore').strip()
    except Exception:
        return ''


def escolher_tablet(reconectar=True):
    """Devolve o endereço adb que está respondendo; tenta 'adb connect' no Wi-Fi até RECONECTAR_MAX."""
    fixo = os.environ.get('HORST_ADB_SERIAL')
    usb, ip = enderecos_tablet()
    fim = time.time() + (RECONECTAR_MAX if reconectar else 0)
    # depois de reiniciar o PC o adb esquece o Wi-Fi: tenta o endereço pedido, depois USB, e reconecta
    enderecos = [s for s in dict.fromkeys([fixo, usb, ip]) if s]
    while True:
        for s in enderecos:
            if _estado(s) == 'device':
                return s
        for s in enderecos:
            if ':' in s:
                try:
                    _exec([ADB, 'connect', s], 15)
                except Exception:
                    pass
                if _estado(s) == 'device':
                    return s
        if time.time() >= fim:
            raise Desconectado(f'aparelho não responde no adb ({", ".join(enderecos)}) há {RECONECTAR_MAX} s')
        time.sleep(5)


SERIAL = None
ADB_CMD = [ADB]


def _usar(serial):
    global SERIAL, ADB_CMD
    SERIAL = serial
    ADB_CMD = [ADB, '-s', serial]


def conectar():
    global OCUPADO
    OCUPADO = True
    try:
        _usar(escolher_tablet())
    finally:
        OCUPADO = False
    return SERIAL


try:  # escolhe já ao importar, sem esperar (se não achar, a 1ª chamada ao adb reconecta)
    _usar(escolher_tablet(reconectar=False))
except Exception:
    _usar(os.environ.get('HORST_ADB_SERIAL') or SERIAL_PADRAO)


class Parou(Exception):
    pass


# ---------------------------------------------------------------- perfis de tela (05/11)
# Todas as posições abaixo foram medidas no TABLET (800x1280) e continuam valendo nele sem mudança.
# No celular POCO (720x1600, Android 15) a posição vem de POCO[nome] (medida no modo --seco) ou,
# enquanto não foi medida, de uma ESTIMATIVA: x * 0.9; y no topo * 0.9 + barra de status;
# y no rodapé ancorado embaixo (1600 - barra de navegação - (1280 - y) * 0.9).
PERFIL = 'tablet'
TAM = (800, 1280)
POCO = {  # nome -> (x, y) medidos no Celular 1 (calibração em modo --seco, 05/11)
    'coracao': (680, 836),  # x do coração ao lado de 'Vendido' (y vem do texto)
    'nome_produto': (685, 808),  # '>' da linha do nome na página leve (abre a completa)
    'compre1': (300, 955), 'compre2': (500, 955),  # botão laranja 'Compre Agora' da página leve
    'aba_live': (360, 1450),  # aba 'Live e Vídeo' (a Home do celular abre em 'Início')
    'icone_perfil': (52, 132),  # ícone de perfil no topo do feed Live e Vídeo
    'fb_Postar vídeo': (558, 1433),  # botão laranja '+ Postar vídeo' no perfil
    'miniatura1': (80, 380),  # meio da 1ª miniatura da galeria (o círculo em 150,306 seleciona; não usar)
    # tela "Adicionar legenda" (medida SEM produto vinculado; conferir de novo com produto)
    # perfil e vídeo (conferência depois de postar)
    'perfil_br1': (500, 420), 'perfil_br2': (500, 100), 'perfil_lar1': (445, 1434), 'perfil_lar2': (670, 1434),
    'puxar_de': (360, 800), 'puxar_ate': (360, 1300), 'video1': (120, 900),
    'painel_de': (360, 1200), 'painel_ate': (360, 400),
    'cab': (560, 118), 'postar': (230, 1436), 'postar_toque': (428, 1436), 'leg_rodape': (30, 1370),
    'ok_teclado': (667, 119), 'campo_legenda': (470, 222), 'leg_area1': (258, 200), 'leg_area2': (700, 400),
    'add_produto': (440, 545),
    # botões COM produto vinculado (sem produto ficam 202 px acima; o script só usa com produto)
    'reuso': (642, 862), 'ia': (642, 1160),
    'card_nome1': (100, 612), 'card_nome2': (610, 640), 'card_preco1': (100, 716), 'card_preco2': (222, 744),
    # lista "Adicionar Produto" (Minhas Curtidas > Mais Recente já vem selecionado)
    'busca_prod': (400, 212), 'curtidas': (296, 313), 'mais_recente': (270, 401),
    # com o aviso amarelo o 1º Adicionar fica em y~690; sem o aviso, em y~560
    'add_x': (600, 300), 'add_y1': (600, 540), 'add_y2': (600, 800),
    'lista_y': (0, 430),  # nomes de produto só abaixo dos filtros (evita ler a aba 'Minhas Curtidas')
    # janela "Editar informações do produto". ATENÇÃO: Feito fica quase em cima do Postar; tocar 1 vez só
    'feito_cor': (200, 1446), 'feito': (360, 1446),
}
POCO_STATUS, POCO_NAV = 40, 0  # px da barra de status / navegação (gestos) no POCO — conferir


def detectar_perfil():
    """'poco720' se a tela for 720x1600, senão 'tablet' (sem mudança)."""
    global PERFIL, TAM, FATOR
    try:
        m = re.search(r'(\d+)x(\d+)', sh('wm size'))
        w, h = int(m[1]), int(m[2])
    except Exception:
        return PERFIL
    TAM = (w, h)
    PERFIL = 'poco720' if (w, h) == (720, 1600) else 'tablet'
    if PERFIL == 'poco720':
        FATOR = 0.33  # Kevin 05/11: celular é rápido, metade das esperas fixas do tablet (0.65)
    return PERFIL


def P(nome, x, y):
    """Posição (x, y) do tablet convertida para o aparelho atual."""
    if PERFIL == 'tablet':
        return x, y
    if nome in POCO:
        return POCO[nome]
    w, h = TAM
    sx = w / 800
    nx = round(x * sx)
    if y < 640:
        ny = round(y * sx + POCO_STATUS * (y > 30))
    else:
        ny = round(h - POCO_NAV - (1280 - y) * sx)
    return min(w - 1, max(0, nx)), min(h - 1, max(0, ny))


def PX(nome, x, y):
    """Mesmo que P, para conferir cor de pixel."""
    return P(nome, x, y)


UI_NAO_E_NOME = re.compile(
    r'(R\$|ou R\$|no Pix|Compre com|Compre Agora|Comprar|Cupom|Acaba em|\d+\s+Vendido|Vendido|Frete|Entrega|'
    r'SParcelado|Parcele|Arraste|Escolhas|\d+\s+Varia|Varia[çc]|Dispon[íi]ve|Avalia[çc]|Busque por|Ver mais|'
    r'Boa Qualidade|Bom Desempenho|Taxa de comiss|Sem Cupom|Leve \d|Compre \d|Ganhe |Desconto|Oferta|Promo[çc]|'
    r'Este item sai|com o ShopeeVIP|ShopeeVIP|Parcelado|Frete gr)', re.I)
SECAO_FIM = re.compile(r'(Avalia[çc][õo]es do produto|Escolhas Populares|Ver mais|Busque por)', re.I)


def titulo_de(vis):
    """Nome do produto entre os textos de uma página/painel: o texto MAIS LONGO da região em volta
    de "N Vendido(s)", parando nas seções de baixo (avaliações, recomendados). Textos de tela só
    valem como lixo quando COMEÇAM com a frase (filtrar por trecho derrubava nomes reais: "Compre"
    em "Compressor"); promoções ("Leve 2 e aproveite...") ficam de fora por serem frases curtas
    perto do nome, e o mais longo resolve mesmo se surgir uma promoção nova."""
    def valido(v):
        return len(v) >= 15 and not UI_NAO_E_NOME.match(v.strip())
    pos = next((i for i, v in enumerate(vis) if 'Vendido' in v), None)
    fim = next((i for i, v in enumerate(vis) if SECAO_FIM.match(v.strip()) and (pos is None or i > pos)), len(vis))
    cands = [v for i, v in enumerate(vis[:fim]) if valido(v) and (pos is None or abs(i - pos) <= 12)]
    if not cands:
        return None
    return max(cands, key=len).replace('&amp;', '&')


class PaginaErrada(Parou):
    """O link abriu outro produto. Nada foi tocado; a fila fecha a Shopee e tenta de novo."""


PAGINA_DUVIDA = None  # 10/11: motivo de dúvida no nome da página do link; o passo 12 então captura a lista e vira pendente


class NomeDiferente(PaginaErrada):
    """A página abriu pelo itemId, mas o nome não bate com o esperado (nada publicado). rodar_fila manda
    o item para PENDENTES (Kevin decide), em vez de travar a fila."""


VALIDAR_PAGINA = None  # rodar_fila define: f(titulo, textos) -> motivo do erro ou None


class ProdutoDaLista(Exception):
    """O produto esperado não está em Minhas Curtidas (antes de Postar: nada publicado)."""


class ProdutoIndisponivel(Exception):
    """A linha do produto certo está em Minhas Curtidas, mas não dá para adicionar (indisponível,
    não listado, esgotado, sem botão Adicionar). Nada publicado: a fila pula o produto."""


# rótulos que aparecem na linha de um produto que não pode ser vinculado
INDISPONIVEL_RE = re.compile(r'indispon|n[aã]o\s+(est[aá]\s+)?listad|esgotad|n[aã]o\s+(est[aá]\s+)?dispon|'
                             r'n[aã]o\s+pode\s+ser\s+adicionad|removid|encerrad|sem\s+estoque|fora\s+de\s+estoque',
                             re.I)


class ProdutoEsgotado(Exception):
    """A página do produto (aberta pelo itemId) diz que o vendedor está de férias / produto indisponível.
    Nada publicado; rodar_fila pula o produto (todas as versões) e marca como esgotado."""


# textos da página do produto que dizem que NÃO dá para vender/vincular (Kevin 10/11: "vendedor está de férias")
FERIAS_RE = re.compile(r'vendedor\s+est[aá]\s+de\s+f[eé]rias|loja\s+(?:est[aá]\s+)?(?:de|em)\s+f[eé]rias|'
                       r'modo\s+f[eé]rias|produto\s+(?:est[aá]\s+)?indispon[ií]vel|este\s+produto\s+n[aã]o\s+est[aá]\s+dispon|'
                       r'produto\s+n[aã]o\s+(?:foi\s+)?encontrad|este\s+produto\s+n[aã]o\s+existe|'
                       r'(?:produto|item)\s+(?:est[aá]\s+)?esgotad|produto\s+sem\s+estoque', re.I)

# 20/11 (Kevin): aviso de esgotado ao favoritar (toast/mensagem) = o produto vai direto para esgotados
ESGOTADO_RE = re.compile(r'esgotad|sem\s+estoque|fora\s+de\s+estoque|indispon[ií]vel', re.I)


class ConfirmarNome(ProdutoIndisponivel):
    """Nome do produto em dúvida (página do link sem nome/nome diferente, ou sem nome esperado): nada publicado.
    Já vem com o print da lista "Adicionar produto" e os nomes das linhas (LINHAS_VISTAS) para o Kevin escolher."""


class Incerto(Exception):
    """Tocou em Postar mas não viu a confirmação."""


def janela_whatsapp(im):
    """Janela 'Compartilhe no Whatsapp / Vídeo postado!': caixa branca no meio (x 124-676,
    y 526-722) sobre o feed escurecido, com o 'OK' laranja à direita."""
    caixa = all(e_branco(cor(im, *PX(f'wa_caixa{i}', x, y))) for i, (x, y) in
                enumerate([(200, 545), (600, 545), (200, 650), (600, 650)]))
    fora = not e_branco(cor(im, *PX('wa_fora1', 400, 760))) and not e_branco(cor(im, *PX('wa_fora2', 400, 480)))
    ok = any(r > 200 and g < 120 for r, g, b in (cor(im, *PX('wa_ok', x, 690)) for x in range(525, 555, 3)))
    return caixa and fora and ok


def confirmar_postado(limite=300):
    """Vídeos grandes demoram 2+ min para subir. Confere a janela do WhatsApp por pixel a cada
    ~2 s; o uiautomator (lento, ~11 s sobre live) só a cada 5 rodadas."""
    fim = time.time() + limite
    teto = time.time() + 900  # enquanto a barra "Carregando... xx%" aparece, continua esperando (máx. 15 min)
    n = 0
    while True:
        im = print_tela()
        if janela_whatsapp(im):
            return True
        if subindo(im):
            fim = min(teto, max(fim, time.time() + 30))
        if n % 5 == 4:
            vis, _ = textos_na_tela()
            if any('Vídeo postado' in v or 'Enviado com sucesso' in v for v in vis):
                return True
        if time.time() > fim:
            return janela_whatsapp(print_tela())
        n += 1
        time.sleep(1.5)


def subindo(im):
    """Barra de upload no topo do feed: caixa branca 'Carregando... xx%' com barra laranja embaixo."""
    return (e_branco(cor(im, *PX('sub1', 400, 125))) and e_branco(cor(im, *PX('sub2', 700, 150)))
            and e_laranja(cor(im, *PX('sub3', 60, 177))) and e_laranja(cor(im, *PX('sub4', 300, 177))))


def fechar_whatsapp():
    """Fecha a janela 'Compartilhe no Whatsapp' (Cancelar; até 3x; depois tecla voltar)."""
    for _ in range(3):
        if not janela_whatsapp(print_tela()):
            return
        sh('input tap %d %d' % P('wa_cancelar', 260, 690))
        time.sleep(2)
    if janela_whatsapp(print_tela()):
        sh('input keyevent KEYCODE_BACK')
        time.sleep(2)


def mandar_para_lixeira(caminho):
    """Move o arquivo para a Lixeira do Windows (dá para recuperar)."""
    ps = ("Add-Type -AssemblyName Microsoft.VisualBasic; "
          "[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($env:ALVO, 'OnlyErrorDialogs', 'SendToRecycleBin')")
    subprocess.run(['powershell', '-NoProfile', '-Command', ps], env={**os.environ, 'ALVO': caminho},
                   creationflags=SEM_JANELA,
                   capture_output=True, timeout=60)


def registrar(doc, status, obs=''):
    import json, datetime
    caminho = r'C:\horst\tablet\postados.json'
    try:
        dados = json.load(open(caminho, encoding='utf-8'))
    except Exception:
        dados = []
    dados.append({'doc': doc, 'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                  'resultado': status, 'obs': obs})
    json.dump(dados, open(caminho, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def _rodar(args, timeout):
    """Roda adb; se o tablet caiu (offline/not found/timeout), reconecta (até RECONECTAR_MAX)
    e repete UMA vez. Se não voltar, levanta Desconectado (para com segurança)."""
    for tentativa in range(2):
        try:
            r = _exec([*ADB_CMD, *args], timeout)
            bater()
            err = r.stderr.decode('utf-8', 'ignore').lower()
            caiu = r.returncode != 0 and any(k in err for k in ('not found', 'offline', 'no devices',
                                                                 'closed', 'unauthorized', 'protocol fault'))
            if not caiu:
                return r
        except subprocess.TimeoutExpired:
            if tentativa:
                raise Desconectado(f'adb {args[:2]} sem resposta em {timeout} s')
        if tentativa == 0:
            print(f'  [adb] conexão com o celular caiu; reconectando (até {RECONECTAR_MAX} s)...')
            conectar()
            print(f'  [adb] reconectado em {SERIAL}')
    raise Desconectado(f'adb {args[:2]} falhou mesmo depois de reconectar')


def adb(*args, timeout=90):
    return _rodar(list(args), timeout).stdout.decode('utf-8', 'ignore')


def sh(cmd, timeout=90):
    return adb('shell', cmd, timeout=timeout)


def print_tela(nome=None):
    # Wi-Fi é mais lento que USB: timeout maior; imagem vazia/corrompida = tenta de novo após reconectar
    for tentativa in range(2):
        raw = _rodar(['exec-out', 'screencap', '-p'], 60).stdout
        try:
            im = Image.open(io.BytesIO(raw)).convert('RGB')
            break
        except Exception:
            if tentativa:
                raise Desconectado('screencap veio vazio duas vezes')
            conectar()
    if nome:
        im.save(os.path.join(PASTA, nome))
    return im


def textos_na_tela(limite=8):
    """Texto visível via uiautomator (lento neste tablet: 3-6 s)."""
    # Em telas com vídeo/animação o dump falha ("could not get idle state"); apaga o arquivo
    # antes para não ler um dump velho.
    bater()
    try:  # 8 s no máximo: tela com vídeo trava o dump; quem chama cai na conferência por pixel
        xml = _exec([*ADB_CMD, 'shell', 'rm -f /sdcard/ui.xml; uiautomator dump /sdcard/ui.xml >/dev/null 2>&1; '
                     'cat /sdcard/ui.xml 2>/dev/null'], limite).stdout.decode('utf-8', 'ignore')
    except subprocess.TimeoutExpired:
        xml = ''
    bater()
    if '<hierarchy' not in xml:
        return [], ''
    return re.findall(r'(?:text|content-desc)="([^"]+)"', xml), xml


def achar(texto, xml):
    """Centro do elemento com esse texto, ou None."""
    m = re.search(r'(?:text|content-desc)="' + re.escape(texto) + r'"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)
    if not m:
        return None
    x1, y1, x2, y2 = map(int, m.groups())
    return (x1 + x2) // 2, (y1 + y2) // 2


def achar_parcial(trecho, xml):
    m = re.search(r'text="[^"]*' + re.escape(trecho) + r'[^"]*"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)
    if not m:
        return None
    x1, y1, x2, y2 = map(int, m.groups())
    return (x1 + x2) // 2, (y1 + y2) // 2


def coracao_vermelho(im, pos):
    x, y = pos
    for dx in range(-12, 13, 3):
        for dy in range(-12, 13, 3):
            if e_vermelho(im.getpixel((min(im.size[0] - 1, max(0, x + dx)), min(im.size[1] - 1, max(0, y + dy))))):
                return True
    return False


def pagina_parada(im_a, im_b, pos):
    """12/11: a faixa à esquerda do coração ("Vendido(s)", nome, preço) está igual nos dois prints = a página
    não rolou nem foi coberta, então o coração continua no mesmo lugar e dá para tocar de novo sem uiautomator."""
    if im_a is None or im_b is None or im_a.size != im_b.size:
        return False
    x, y = pos
    caixa = (max(0, x - 260), max(0, y - 60), max(1, x - 30), min(im_a.size[1], y + 60))
    a, b = im_a.crop(caixa).convert('L').tobytes(), im_b.crop(caixa).convert('L').tobytes()
    return sum(abs(p - q) for p, q in zip(a, b)) / max(1, len(a)) < 6


def acordar_e_desbloquear():
    sh('input keyevent KEYCODE_WAKEUP')
    time.sleep(1)
    def bloqueado():
        w = sh('dumpsys window')
        return 'mShowingLockscreen=true' in w or 'isStatusBarKeyguard=true' in w
    if bloqueado():
        sh('input swipe %d %d %d %d 300' % (*P('desbloq_de', 400, 1100), *P('desbloq_ate', 400, 300)))
        time.sleep(2)
        if bloqueado():
            print_tela('erro_bloqueio.png')
            raise Parou('tela bloqueada com PIN/padrão/senha — desbloqueie o celular ou remova o bloqueio')


FATOR = 0.65  # esperas fixas ~35% menores; as conferências de tela continuam por polling


def toque(x, y, espera=3.0):
    sh(f'input tap {x} {y}')
    # espera variável: 10% a 40% mais rápida que a base, sorteada a cada toque
    time.sleep(espera * FATOR * random.uniform(0.6, 0.9))


def cor(im, x, y):
    return im.getpixel((x, y))


def e_verde(c):
    r, g, b = c
    return g > 140 and r < 90 and b < 120


def e_vermelho(c):
    r, g, b = c
    return r > 200 and g < 110 and b < 90


def e_laranja(c):
    r, g, b = c
    return r > 210 and 50 < g < 120 and b < 90


def e_branco(c):
    return min(c) > 245


def tela_legenda(im):
    """Tela 'Adicionar legenda': cabeçalho branco + botão Postar laranja embaixo."""
    return (e_branco(cor(im, *PX('cab', 400, 62))) and e_laranja(cor(im, *PX('postar', 445, 1168)))
            and e_branco(cor(im, *PX('leg_rodape', 55, 1120))))


def tela_produtos(im):
    """Tela 'Adicionar Produto': cabeçalho branco + barra de pesquisa cinza clara."""
    c = cor(im, *PX('busca_prod', 400, 126))
    return e_branco(cor(im, *PX('cab', 400, 62))) and 235 <= c[0] <= 248 and abs(c[0] - c[2]) < 6


def aguardar_captcha(vis):
    """Captcha na tela: NÃO resolve. Print, bipe, espera o Kevin (até 30 min) e registra em
    captcha_log.csv. Devolve True se havia captcha (e ele sumiu)."""
    import datetime, captcha_log
    if not captcha_log.e_captcha(vis):
        return False
    global EM_CAPTCHA
    EM_CAPTCHA = True  # a vigia de passo não conta o tempo esperando o Kevin
    inicio = datetime.datetime.now()
    nome = f'captcha_{inicio:%m%d_%H%M%S}.png'
    print_tela(nome)
    print(f'  CAPTCHA {inicio:%H:%M:%S}: esperando o Kevin resolver no celular')
    fim = time.time() + 30 * 60
    while time.time() < fim:
        try:  # som "precisa de você" (sons\atencao.wav; máx. 1x/45 s; com a Central aberta, ela toca)
            from alerta import alerta_kevin
            alerta_kevin('CAPTCHA no celular (fila de postagem) — resolva à mão')
        except Exception:
            pass
        time.sleep(10)
        v, _ = textos_na_tela()
        if v and not captcha_log.e_captcha(v):
            captcha_log.registrar(inicio, datetime.datetime.now(), 'rodar_fila', os.path.join(PASTA, nome))
            EM_CAPTCHA = False
            return True
    captcha_log.registrar(inicio, None, 'rodar_fila', os.path.join(PASTA, nome), 'não resolvido em 30 min')
    raise Parou('captcha não resolvido em 30 min')


def esperar_pixel(passo, nome, teste, limite=25):
    fim = time.time() + limite
    prox = time.time() + 10
    while time.time() < fim:
        if teste(print_tela()):
            return
        if time.time() > prox:  # demorando: confere se é captcha (uiautomator é lento, só a cada 10 s)
            if aguardar_captcha(textos_na_tela()[0]):
                fim = time.time() + limite
            prox = time.time() + 10
        time.sleep(0.5)
    print_tela(f'erro_passo_{passo}.png')
    raise Parou(f'passo {passo}: não reconheci "{nome}" (print: erro_passo_{passo}.png)')


def esperar_texto(passo, textos, limite=25):
    """Espera até algum dos textos aparecer. Devolve (texto_encontrado, xml)."""
    fim = time.time() + limite
    while time.time() < fim:
        vis, xml = textos_na_tela()
        if passo == 1:  # página do produto: vendedor de férias / indisponível => pula o produto
            falhou = next((v for v in vis if re.search(r'falhou ao carregar|falha ao carregar', v, re.I)), None)
            if falhou:  # diálogo "Esse produto falhou ao carregar.": fecha pelo botão (bounds do dump) e deixa a fila tentar de novo
                for nome in ('Cancelar', 'Voltar', 'Fechar', 'OK'):
                    pos = achar(nome, xml or '')
                    if pos:
                        sh(f'input tap {pos[0]} {pos[1]}')
                        time.sleep(1.5)
                        break
                print_tela('erro_passo_1_falhou_carregar.png')
                raise Parou('passo 1: o produto falhou ao carregar (diálogo fechado; a fila tenta de novo e depois pula)')
            aviso = next((v for v in vis if FERIAS_RE.search(v)), None)
            if aviso:
                print_tela('erro_passo_1_ferias.png')
                raise ProdutoEsgotado(f'página do produto: "{aviso[:80]}" (vendedor de férias/indisponível)')
        for t in textos:
            if any(t in v for v in vis):
                return t, xml
        if aguardar_captcha(vis):
            fim = time.time() + limite
        time.sleep(0.5)
    print_tela(f'erro_passo_{passo}.png')
    raise Parou(f'passo {passo}: não achei {textos} na tela (print: erro_passo_{passo}.png)')


POS_CACHE = {}  # passo -> posição lida no 1º post desta execução (nos seguintes, sem uiautomator)


def foco():
    return sh('dumpsys window | grep mCurrentFocus')


def esperar_foco(nome, limite):
    """Espera a tela (Activity) mudar; bem mais barato que o uiautomator."""
    fim = time.time() + limite
    while time.time() < fim:
        if nome in foco():
            return True
        time.sleep(0.25)
    return False


def tocar_rapido(passo, texto, fallback, destino, espera=4, limite=25, botao_laranja=False):
    """Celular, do 2º post em diante: toca direto na posição já conhecida e confere pela Activity
    de destino. Se não mudar de tela, cai no caminho antigo (uiautomator), que também confere."""
    pos = POS_CACHE.get(passo)
    if PERFIL != 'tablet' and pos:
        for _ in range(2):
            sh(f'input tap {pos[0]} {pos[1]}')
            if esperar_foco(destino, 5):
                print(f'  [{passo}] "{texto}" direto em {pos}')
                return
        print(f'  [{passo}] toque direto não mudou de tela; lendo a tela')
    tocar_texto(passo, texto, fallback, espera=espera, limite=limite, botao_laranja=botao_laranja)


def tocar_texto(passo, texto, fallback, espera=4, limite=25, botao_laranja=False):
    try:
        _, xml = esperar_texto(passo, [texto], limite)
    except Parou:
        # Telas com vídeo tocando (prévia/editor): o uiautomator falha. Se o botão laranja
        # está na posição conhecida, toca nele mesmo assim.
        im = print_tela()
        fx, fy = fallback = P('fb_' + texto, *fallback)
        pontos = [(fx + dx, fy + dy) for dx in (-40, -30, 30, 40) for dy in (-12, 0, 12)]
        laranjas = sum(1 for p in pontos if e_laranja(cor(im, *p)) or e_vermelho(cor(im, *p)))
        # NUNCA na tela da legenda: lá o botão laranja nessa posição é o "Postar"
        tela_escura = not e_branco(cor(im, *PX('leg_rodape', 55, 1120))) and not tela_legenda(im)
        if not (botao_laranja and laranjas >= 6 and tela_escura):  # fundo do botão em volta do texto
            raise
        print(f'  [{passo}] uiautomator falhou; botão laranja visto em {fallback}, tocando')
        POS_CACHE[passo] = fallback
        toque(*fallback, espera=espera)
        return
    pos = achar(texto, xml) or P('fb_' + texto, *fallback)
    POS_CACHE[passo] = pos
    print(f'  [{passo}] tocando "{texto}" em {pos}')
    toque(*pos, espera=espera)


def digitar_legenda(texto):
    ims = sh('ime list -s')
    if 'com.android.adbkeyboard' not in ims:
        raise Parou('ADBKeyboard não instalado. Para digitar legenda com acento, instalar o APK '
                    'ADBKeyboard (github.com/senzhk/ADBKeyBoard) — precisa do OK do dono.')
    anterior = sh('settings get secure default_input_method').strip()
    sh('ime set com.android.adbkeyboard/.AdbIME')
    time.sleep(1)
    b64 = base64.b64encode(texto.encode('utf-8')).decode()
    sh(f'am broadcast -a ADB_INPUT_B64 --es msg {b64}')
    time.sleep(2)
    if anterior and anterior != 'null':
        sh(f'ime set {anterior}')


TOCOU_POSTAR = False


def postar(video, link, legenda, seco, favoritar=True, enviar_video=True):
    global TOCOU_POSTAR
    TOCOU_POSTAR = False
    if len(legenda) > 150:
        raise Parou(f'legenda tem {len(legenda)} caracteres; máximo 150')
    try:
        conectar()  # escolhe USB ou Wi-Fi (aparelhos.json); espera até RECONECTAR_MAX
    except Desconectado as e:
        raise Parou(f'celular não conectado no adb: {e}')
    print(f'[adb] usando o aparelho em {SERIAL} · perfil {detectar_perfil()} {TAM[0]}x{TAM[1]}')
    acordar_e_desbloquear()
    marca(None)

    if enviar_video:
        enviar(video)
    else:
        print('[0] pulando envio do vídeo (--sem-enviar)')
    marca('push')
    # 1-2. produto + favoritar
    if not favoritar:
        print('[1-2] pulando favoritar (--sem-favoritar)')
    else:
        favoritar_produto(link)
    marca('favoritar')
    postar_resto(legenda, seco)


TEMPOS = []


def marca(nome):
    """Mede cada etapa (rodar_fila grava no log). nome=None começa do zero."""
    if nome is None:
        TEMPOS.clear()
    TEMPOS.append((nome, time.time()))


def tempos():
    return ' · '.join(f'{b[0]} {b[1] - a[1]:.0f}s' for a, b in zip(TEMPOS, TEMPOS[1:]))


def tamanho_remoto(remoto):
    m = re.search(r'\d+', sh(f"stat -c %s '{remoto}' 2>/dev/null"))
    return int(m[0]) if m else -1


def enviar_arquivo(video, remoto, tam):
    """adb push uma vez. Se der timeout/queda, confere o tamanho no aparelho antes de repetir."""
    global OCUPADO
    for tentativa in range(2):
        OCUPADO = True
        try:
            _exec([*ADB_CMD, 'push', video, remoto], 900)
        except subprocess.TimeoutExpired:
            print('  [0] push passou do tempo; conferindo o tamanho no aparelho')
        finally:
            OCUPADO = False
        if tamanho_remoto(remoto) == tam:
            return
        if tentativa == 0:
            conectar()
            sh(f"rm -f '{remoto}'")
    raise Parou(f'passo 0: o vídeo não chegou inteiro ao aparelho ({tamanho_remoto(remoto)} de {tam} bytes)')


def enviar(video):
    # 0. vídeo na galeria
    # A galeria da Shopee ordena pela data do arquivo, e o adb push mantém a data do PC.
    # Por isso: 1) tira da galeria os vídeos anteriores, 2) envia o atual, 3) ajusta a data
    # dele para agora, 4) confere no MediaStore que ele é o mais novo.
    # Nunca duplica: nas novas tentativas do mesmo post o arquivo já está lá. Mover para
    # HorstAds_postados criava 2 cópias na galeria (a Shopee e a galeria do POCO enxergam essa
    # pasta também). Os vídeos ficam guardados no PC até o post sair, então apagar aqui é seguro.
    arquivo = os.path.basename(video).replace("'", '')
    remoto = f'{DESTINO}/{arquivo}'
    tam = os.path.getsize(video)
    sh(f'mkdir -p {DESTINO}')
    antigos = [l.strip() for pasta in (DESTINO, ARQUIVO_MORTO)
               for l in sh(f'ls {pasta} 2>/dev/null').splitlines() if l.strip().lower().endswith('.mp4')]
    for pasta in (DESTINO, ARQUIVO_MORTO):
        for v in [l.strip() for l in sh(f'ls {pasta} 2>/dev/null').splitlines() if l.strip().lower().endswith('.mp4')]:
            if pasta == DESTINO and v == arquivo and tamanho_remoto(remoto) == tam:
                continue  # já está inteiro no lugar certo: não envia de novo
            sh(f"rm -f '{pasta}/{v}'")
            sh(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d 'file://{pasta}/{v}'")
    if tamanho_remoto(remoto) == tam:
        print('[0] vídeo já estava no aparelho: não enviei de novo')
    else:
        enviar_arquivo(video, remoto, tam)
    sh(f"touch '{remoto}'")
    sh(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d 'file://{DESTINO}/{arquivo}'")
    fim = time.time() + 6  # espera a galeria indexar (antes: 4 s fixos)
    while True:
        linhas = sh('content query --uri content://media/external/video/media '
                    '--projection _display_name:date_modified').splitlines()
        vids = []
        for l in linhas:
            m = re.search(r'_display_name=(.*?), date_modified=(\d+)', l)
            if m:
                vids.append((int(m[2]), m[1]))
        if (vids and max(vids)[1] == arquivo) or time.time() > fim:
            break
        time.sleep(0.5)
    if not vids or max(vids)[1] != arquivo:
        raise Parou(f'passo 0: o vídeo mais novo da galeria não é {arquivo} (galeria: {sorted(vids)[-3:]})')
    if any(n in antigos and n != arquivo for _, n in vids):
        raise Parou('passo 0: vídeos antigos ainda aparecem na galeria')
    print('[0] vídeo enviado e conferido como o mais novo da galeria:', arquivo)


ITEM_ID = None  # 'shopid.itemid' do post (rodar_fila define); abre a página certa direto, sem link curto


def abrir_produto(link):
    """Abre o produto pelo ID (shopee.com.br/product/loja/item), não pelo link curto: o curto às vezes
    deixava na tela a página do post anterior. Confere no Android que foi esse ID que abriu."""
    if not ITEM_ID:
        raise PaginaErrada('sem itemId do link: não abro produto sem ID')
    loja, item = ITEM_ID.split('.')
    alvo = f'product/{loja}/{item}'
    print(f'[1] abrindo o produto pelo itemId {ITEM_ID} (shopee.com.br/{alvo})')
    sh(f'am start -a android.intent.action.VIEW -d https://shopee.com.br/{alvo} {PKG}')
    time.sleep(0.5)
    if alvo not in sh('dumpsys activity activities | grep -m3 dat=https'):
        raise PaginaErrada(f'o app não recebeu o ID {ITEM_ID}')


def favoritar_produto(link):
    abrir_produto(link)
    try:
        import captcha_log
        captcha_log.contar_aberto()
    except Exception:
        pass
    xml = ''
    try:
        _, xml = esperar_texto(1, ['Vendido'], limite=30)
    except Parou:
        # página "leve" com vídeo/animação: o uiautomator falha. Se o botão laranja
        # "Compre Agora" está na tela, toca na linha do nome (abre a página completa).
        im = print_tela()
        if e_laranja(cor(im, *PX('compre1', 300, 957))) and e_laranja(cor(im, *PX('compre2', 500, 957))):
            print('[1] uiautomator falhou na página leve; abrindo a página completa')
            toque(*P('nome_produto', 775, 858), espera=6)
        elif PERFIL != 'tablet':  # celular: app recém-aberto pode ignorar o link; manda de novo 1 vez
            print('[1] produto não abriu; mandando o link de novo')
            abrir_produto(link)
        else:
            raise
        _, xml = esperar_texto(1, ['Vendido'], limite=30)
    vis = re.findall(r'(?:text|content-desc)="([^"]+)"', xml)  # reaproveita o dump que achou "Vendido"
    if not any('Cupom' in v or 'Varia' in v or 'Avalia' in v or 'Escolhas Populares' in v for v in vis):
        time.sleep(0.7)  # página ainda montando: olha de novo só neste caso
        vis, xml = textos_na_tela()
    _fer = next((v for v in vis if FERIAS_RE.search(v)), None)
    if _fer:
        print_tela('erro_passo_1_ferias.png')
        raise ProdutoEsgotado(f'página do produto: "{_fer[:80]}" (vendedor de férias/indisponível)')
    if sair_de_tela_compra(vis):  # tela de compra por cima: Back e lê de novo (nunca toca nela)
        vis, xml = textos_na_tela()
    if (not e_pagina_completa(xml)
            and (any('Escolhas Populares' in v for v in vis) or not any('Cupom' in v or 'Varia' in v for v in vis))):
        # página "leve" (sem coração): tocar na linha do nome do produto abre a página completa.
        # 10/11: o toque em coordenada fixa caía em "Ou R$... em até 12x" (parcelamento) quando a página já
        # estava completa; agora só toca se NÃO há coração/nome da página completa no dump.
        print('[1] página leve: abrindo a página completa do produto')
        toque(*P('nome_produto', 775, 858), espera=6)
        sair_de_tela_compra()
        esperar_texto(1, ['Vendido'], limite=30)
        time.sleep(1)
        vis, xml = textos_na_tela()
        if sair_de_tela_compra(vis):
            vis, xml = textos_na_tela()
        # a página leve também tem "Vendido": espera ela sumir (página completa tem Cupom/Avaliações)
        leve = lambda v: (any('Escolhas Populares' in t for t in v)
                          or not any('Cupom' in t or 'Varia' in t or 'Avalia' in t for t in v))
        fim, proximo = time.time() + 30, time.time() + 8
        while time.time() < fim and leve(vis) and not e_pagina_completa(xml):
            if PERFIL != 'tablet' and time.time() > proximo:  # o toque às vezes não pega no celular
                if not sair_de_tela_compra(vis) and not e_pagina_completa(xml):
                    print('[1] ainda na página leve; tocando no nome de novo')
                    toque(*P('nome_produto', 775, 858), espera=4)
                    sair_de_tela_compra()
                proximo = time.time() + 8
            time.sleep(2)
            vis, xml = textos_na_tela()
        if PERFIL != 'tablet' and leve(vis):
            print_tela('erro_passo_1.png')
            raise Parou('passo 1: a página completa do produto não abriu (print: erro_passo_1.png)')
    # TRAVA: a página aberta tem que ser o produto DESTE post, antes de tocar no coração. O link às
    # vezes mostra ainda a página do post anterior (foi assim que 3 posts saíram com produto errado).
    if VALIDAR_PAGINA:
        motivo = VALIDAR_PAGINA(titulo_de(vis), vis)
        global PAGINA_DUVIDA
        PAGINA_DUVIDA = None
        if motivo:
            print_tela('erro_pagina_errada.png')
            if str(motivo).startswith('ainda é a página do post anterior'):
                raise PaginaErrada(f'página do link não é o produto do post: {motivo}')
            # nome da página sem nome/diferente: a página abriu pelo itemId (conferido no Android), então segue
            # favoritando; o passo 12 abre a lista Adicionar, captura print + nomes e manda para PENDENTES.
            PAGINA_DUVIDA = f'nome na página do link em dúvida: {motivo}'
            print(f'  [1] {PAGINA_DUVIDA}; vou capturar a lista Adicionar para o Kevin escolher')
    global PRODUTO_TEXTOS  # textos da página do produto do link (rodar_fila confere depois)
    PRODUTO_TEXTOS = list(vis)
    global TITULO_ESPERADO
    # nome aprovado pelo Kevin (linha da lista) > nome já confirmado antes > nome lido na página
    TITULO_ESPERADO = TITULO_APROVADO or TITULO_CACHE or titulo_de(vis)
    open(os.path.join(PASTA, 'produto_textos.txt'), 'w', encoding='utf-8').write('\n'.join(vis))
    with contextlib.suppress(Exception):  # placar: foto principal + preços + nome por itemId (tablet\cache_produto)
        import placar
        placar.salvar_cache(ITEM_ID, print_tela(), vis, TITULO_ESPERADO)
    pos_vendido = achar_parcial('Vendido', xml)
    coracao = (P('coracao', 775, 997)[0], pos_vendido[1]) if pos_vendido else P('coracao', 775, 997)
    mh = re.search(r'resource-id="buttonItemLiked"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)
    if mh:  # coração pelos limites reais do botão (nunca por coordenada fixa)
        a, b, c, d = map(int, mh.groups())
        coracao = ((a + c) // 2, (b + d) // 2)
    im_pagina = print_tela('p1_produto.png')
    inicial = coracao_vermelho(im_pagina, coracao)
    print(f'[2] coração em {coracao}: {"vermelho (já favoritado)" if inicial else "vazio"}')
    # Toca 1x e confere; se ficou "removido", toca de novo. Máx. 3 toques.
    # (Se já estava favoritado, isso desfavorita e favorita de novo -> sobe para o 1º em "Mais Recente".)
    foco_pagina = foco() if PERFIL != 'tablet' else ''
    ultimo_im = None
    for n in range(1, 4):
        if n > 1 and PERFIL != 'tablet' and pagina_parada(im_pagina, ultimo_im, coracao) and foco() == foco_pagina:
            # 12/11 (Kevin: "acelerar com cliques"): a página não mexeu desde o 1º print, então o coração está no
            # MESMO lugar: toca de novo direto, sem o uiautomator (cada dump custava 5-16 s). O resultado de cada
            # toque continua conferido pela cor do coração, igual antes.
            time.sleep(0.3)
        elif n > 1:  # depois do 1º toque a tela pode ter re-renderizado: acha o coração de novo pelos limites
            vis2, xml2 = textos_na_tela()
            if sair_de_tela_compra(vis2):
                vis2, xml2 = textos_na_tela()
            mh = re.search(r'resource-id="buttonItemLiked"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml2 or '')
            if mh:
                a, b, c, d = map(int, mh.groups())
                coracao = ((a + c) // 2, (b + d) // 2)
            elif xml2 and not e_pagina_completa(xml2):
                raise Parou('passo 2: coração sumiu da tela (não é mais a página completa do produto)')
        sh(f'input tap {coracao[0]} {coracao[1]}')
        # o coração muda na hora: confere por pixel (rápido) e só lê o aviso se não ficou vermelho.
        # Se já estava curtido, o 1º toque descurte (fica vazio) e o 2º curte de novo.
        descurtir = inicial and n == 1
        fim = time.time() + (1.5 if descurtir else 2.0)
        vermelho = not descurtir
        while time.time() < fim:  # 12/11: para assim que o coração muda (antes: 1 s fixo no descurtir)
            time.sleep(0.25)
            ultimo_im = print_tela(f'p2_favorito_{n}.png')
            vermelho = coracao_vermelho(ultimo_im, coracao)
            if vermelho != descurtir:
                break
        if inicial and n == 1:  # descurtir: precisa ver vazio antes de curtir de novo
            print(f'    toque {n}: coração={"vermelho" if vermelho else "vazio"}')
            continue
        aviso = None
        if not vermelho and PERFIL != 'tablet' and n == 1:
            # 20/11: o aviso "esgotado" aparece logo depois do toque no coração: lê a tela UMA vez antes do atalho
            try:
                vis_e, _ = textos_na_tela()
                esg = next((v for v in vis_e if ESGOTADO_RE.search(v) and len(v) < 90), None)
                if esg:
                    print_tela('erro_passo_2_esgotado.png')
                    raise ProdutoEsgotado(f'aviso ao favoritar: "{esg[:80]}" (esgotado)')
            except ProdutoEsgotado:
                raise
            except Exception:
                pass
        if not vermelho and PERFIL != 'tablet' and pagina_parada(im_pagina, ultimo_im, coracao):
            # 12/11: coração vazio com a página parada = este toque descurtiu (o anterior não tinha pegado).
            # Não precisa ler o aviso (uiautomator lento): o próximo toque curte de novo.
            print(f'    toque {n}: coração=vazio (página parada; curto de novo)')
            continue
        if not vermelho:
            vis, _ = textos_na_tela()
            if sair_de_tela_compra(vis):  # abriu parcelamento/compra: Back, sem tocar dentro
                time.sleep(0.5)
                continue
            aviso = next((v for v in vis if 'avorito' in v), None)
            esg = next((v for v in vis if ESGOTADO_RE.search(v) and len(v) < 90), None)
            if esg:
                print_tela('erro_passo_2_esgotado.png')
                raise ProdutoEsgotado(f'aviso ao favoritar: "{esg[:80]}" (esgotado)')
        print(f'    toque {n}: aviso={aviso!r} coração={"vermelho" if vermelho else "vazio"}')
        if vermelho or (aviso and 'Adicionado' in aviso):
            return
        time.sleep(0.5)
    raise Parou(f'passo 2: depois de 3 toques o coração em {coracao} não ficou favoritado — ver p2_favorito_3.png')


def e_folha_compra(vis):
    """Folha de compra/variação do produto (Cor, Quantidade, Estoque, Seguros + botão "Compre agora")."""
    t = ' | '.join(vis)
    if re.search(r'Parcelamento', t) and re.search(r'Aplicar|Cart[ãa]o de Cr[ée]dito', t):
        return True  # folha de parcelamento
    if re.search(r'Finalizar compra|Forma de pagamento|Meu carrinho|Resumo do pedido|Fazer pedido', t, re.I):
        return True  # carrinho / checkout / pagamento
    return bool(re.search(r'Compre agora', t, re.I)
                and re.search(r'Quantidade|Estoque|Seguros|Varia[çc][ãa]o', t))


def e_pagina_completa(xml):
    """Página completa do produto: tem o coração (buttonItemLiked) e o nome (labelProductPageProductName)."""
    return 'buttonItemLiked' in xml or 'labelProductPageProductName' in xml


def sair_de_tela_compra(vis=None, vezes=3):
    """Se uma tela de compra (parcelamento, Compre agora/variação, carrinho, checkout) abriu, aperta Back até
    sumir. NUNCA toca dentro dela. True se precisou fechar."""
    fechou = False
    for _ in range(vezes):
        if vis is None:
            vis, _x = textos_na_tela()
        if not e_folha_compra(vis):
            return fechou
        retry(3, 'tela de compra aberta: voltar')
        sh('input keyevent KEYCODE_BACK')
        time.sleep(1.2)
        fechou = True
        vis = None
    return fechou


def fechar_folha_compra():
    """Se a folha de compra estiver aberta, fecha com Back (NUNCA toca em Comprar). True se fechou."""
    vis, _ = textos_na_tela()
    if not e_folha_compra(vis):
        return False
    retry(3, 'folha de compra aberta: voltar')
    sh('input keyevent KEYCODE_BACK')
    time.sleep(1.2)
    return True


def ir_para_live():
    """Celular: a Home abre em "Início" e o 1º toque na aba às vezes não pega. Toca até a barra de
    baixo ficar preta (feed Live e Vídeo). No tablet não faz nada."""
    if PERFIL == 'tablet':
        return
    fora = 0
    for _ in range(8):
        if fechar_folha_compra():  # folha de variação/"Compre agora" por cima: Back e olha de novo
            continue
        if 'HomeActivity' not in foco():
            # página de produto (ReactActivity_) por cima: o am start não a tira; alterna Back e am start
            fora += 1
            retry(3, 'fora da Home: voltar')
            if fora % 2:
                sh('input keyevent KEYCODE_BACK')
                time.sleep(1.5)
            sh(f'am start -n {PKG}/com.shopee.app.ui.home.HomeActivity_')
            time.sleep(1.5)
            continue
        if max(cor(print_tela(), 130, 1440)) < 60:
            return
        sh('input tap %d %d' % P('aba_live', 400, 1190))
        fim = time.time() + 3
        while time.time() < fim:
            if max(cor(print_tela(), 130, 1440)) < 60:
                return
            time.sleep(0.3)
    print_tela('erro_passo_3.png')
    raise Parou('passo 3: a aba "Live e Vídeo" não abriu (print: erro_passo_3.png)')


def retry(etapa, motivo):
    """Registro único de nova tentativa (a Central conta "retry etapa" no log)."""
    print(f'retry etapa {etapa} motivo {motivo}')


def achar_proximo(im):
    """Centro do botão laranja/vermelho "Próximo" (canto inferior direito), sem uiautomator."""
    w, h = im.size
    pontos = [(x, y) for x in range(int(w * .6), w - 10, 6) for y in range(int(h * .8), h - 30, 6)
              if e_laranja(cor(im, x, y)) or e_vermelho(cor(im, x, y))]
    if len(pontos) < 40 or e_branco(cor(im, *PX('leg_rodape', 55, 1120))) or tela_legenda(im):
        return None  # na tela da legenda o botão laranja é o Postar: nunca tocar aqui
    return sum(p[0] for p in pontos) // len(pontos), sum(p[1] for p in pontos) // len(pontos)


POPUP_FECHAR = ('Agora não', 'Agora nao', 'Mais tarde', 'Pular', 'Fechar', 'Entendi', 'Continuar', 'Toque para continuar',
                'Cancelar', 'Não, obrigado')


def tratar_tela_desconhecida(etapa):
    """Popup conhecido: fecha. Permissão/captcha/login não são tocados. Senão, tecla voltar."""
    vis, xml = textos_na_tela()
    if aguardar_captcha(vis):
        return
    if any(re.search(r'Permitir|Fazer login|Entrar na conta|verifica', v, re.I) for v in vis):
        print_tela(f'erro_passo_{etapa}.png')
        raise Parou(f'etapa {etapa}: tela pede sua decisão (permissão ou login); print: erro_passo_{etapa}.png')
    for texto in POPUP_FECHAR:
        pos = achar(texto, xml)
        if pos:
            retry(etapa, f'popup "{texto}"')
            sh(f'input tap {pos[0]} {pos[1]}')
            time.sleep(1)
            return
    retry(etapa, 'tela desconhecida: voltar')
    sh('input keyevent KEYCODE_BACK')
    time.sleep(1.5)


def fluxo_ate_legenda(limite=70):
    """Celular: da câmera até a legenda, olhando a cada volta EM QUE TELA está e fazendo o passo dessa
    tela. Toque perdido repete com pequeno desvio; tela adiantada ou atrasada continua de onde está."""
    fim = time.time() + limite
    falhas = {}

    def falhou(etapa, motivo):
        falhas[etapa] = falhas.get(etapa, 0) + 1
        retry(etapa, motivo)

    while time.time() < fim:
        f = foco()
        if 'PublishVideoActivity' in f:
            return
        if 'SSZMultipleEditActivity' in f or 'SSZBasePreviewActivity' in f:
            editor = 'SSZMultipleEditActivity' in f
            etapa, destino = (8, 'PublishVideoActivity') if editor else (7, 'SSZMultipleEditActivity')
            n = falhas.get(etapa, 0)
            pos = achar_proximo(print_tela()) or POS_CACHE.get(etapa)
            if not pos:
                tocar_texto(etapa, 'Próximo', (721, 1165) if editor else (715, 1158), espera=2, botao_laranja=True)
                continue
            POS_CACHE[etapa] = pos
            x, y = pos[0] + (0, -14, 14, -24, 24)[n % 5], pos[1] + (0, 6, -6, 0, 0)[n % 5]
            sh(f'input tap {x} {y}')
            if not esperar_foco(destino, 4):
                if etapa == 8 and 'SSZBasePreviewActivity' in foco():
                    continue  # voltou uma tela: o laço refaz de onde está
                falhou(etapa, 'Próximo não mudou de tela')
            continue
        if 'SSZMediaActivity' in f:
            n = falhas.get(5, 0)
            if n or not POS_CACHE.get(5):  # olha a tela: se a galeria já abriu, não toca em Biblioteca
                vis, xml = textos_na_tela()
                if not any('Galeria' in v for v in vis):
                    pos = achar('Biblioteca', xml)
                    if not pos:
                        falhou(5, 'Biblioteca não apareceu')
                        time.sleep(1)
                        continue
                    POS_CACHE[5] = pos
                    sh(f'input tap {pos[0]} {pos[1]}')
                    time.sleep(1.2)
            else:
                # 12/11: espera curta e por tela (antes 1 s fixo antes e depois de tocar em Biblioteca)
                time.sleep(0.6)
                sh('input tap %d %d' % POS_CACHE[5])
                time.sleep(0.7)
            sh('input tap %d %d' % P('miniatura1', 100, 235))
            if not esperar_foco('SSZBasePreviewActivity', 3):
                falhou(5, 'prévia não abriu')
            continue
        tratar_tela_desconhecida(4)
    print_tela('erro_passo_8.png')
    raise Parou(f'não cheguei na legenda em {limite} s (falhas: {falhas}; print: erro_passo_8.png)')


def postar_resto(legenda, seco):

    # 3-4. feed -> perfil -> Postar vídeo
    # sair da página do produto e ir para a tela inicial da Shopee
    sh(f'am start -n {PKG}/com.shopee.app.ui.home.HomeActivity_')
    time.sleep(1.2)  # tocar no perfil logo que o feed abre, sem esperar lives carregarem
    # A Home costuma abrir direto na aba "Live e Vídeo" (feed com vídeo tocando, onde o
    # uiautomator não funciona). Toca no ícone de perfil (canto sup. esq.) e espera o perfil.
    ir_para_live()
    for tentativa in range(2):
        if tentativa:
            print('  [3] perfil não abriu; tocando na aba "Live e Vídeo" e tentando de novo')
            sh('input keyevent KEYCODE_BACK'); time.sleep(2)
            toque(*P('aba_live', 400, 1190), espera=6)
        toque(*P('icone_perfil', 35, 42), espera=3)
        try:
            if PERFIL != 'tablet' and POS_CACHE.get(4):  # botão laranja "+ Postar vídeo" já na tela?
                fim = time.time() + 8
                x, y = POS_CACHE[4]
                while time.time() < fim and not e_laranja(cor(print_tela(), x - 80, y)):
                    time.sleep(0.3)
            tocar_rapido(4, 'Postar vídeo', (688, 1156), 'SSZMediaActivity', espera=8, limite=15)
            break
        except Parou:
            if tentativa:
                raise
    marca('perfil+Postar vídeo')  # 12/11: separa o tempo do perfil do tempo da galeria no log ("tempos:")

    # 5-8. biblioteca -> 1º vídeo -> próximo x3
    # Tocar no MEIO da 1ª miniatura (abre a prévia). O círculo (179,154) seleciona e mostra
    # a barra "Selecionar/OneClip" -- não usar.
    if PERFIL != 'tablet':
        fluxo_ate_legenda()
    else:
        tocar_texto(5, 'Biblioteca', (638, 1070), espera=5)
        esperar_texto(6, ['Galeria'])
        toque(*P('miniatura1', 100, 235), espera=5)
        tocar_texto(7, 'Próximo', (715, 1158), espera=5, botao_laranja=True)
        tocar_texto(8, 'Próximo', (721, 1165), espera=8, botao_laranja=True)
    marca('galeria+próximo')

    postar_da_legenda(legenda, seco)


def postar_da_legenda(legenda, seco):
    # Nestas telas o uiautomator costuma falhar (miniatura animada), então a conferência
    # é por cor de pixel.
    # 9. legenda
    esperar_pixel(9, 'tela Adicionar legenda', tela_legenda, limite=40)
    # o touch às vezes não pega: confere que a legenda entrou antes de seguir (até 3 vezes)
    for tentativa in range(3):
        toque(*P('campo_legenda', 400, 140), espera=3)
        digitar_legenda(legenda)
        fim = time.time() + 2  # antes: 1,5 s fixo
        while not legenda_preenchida(print_tela()) and time.time() < fim:
            time.sleep(0.3)
        if legenda_preenchida(print_tela()):
            break
        print(f'  [9] legenda não entrou (tentativa {tentativa + 1}); tocando no campo de novo')
    else:
        print_tela('erro_passo_9.png')
        raise Parou('passo 9: a legenda não entrou no campo (print: erro_passo_9.png)')
    toque(*P('ok_teclado', 765, 62), espera=3)  # OK (fecha o teclado)
    if PERFIL != 'tablet':  # celular: o 1º OK só fecha o teclado; o 2º sai da edição da legenda
        toque(*P('ok_teclado', 765, 62), espera=3)
    print_tela('p9_legenda.png')
    marca('legenda')

    # 10-13. vincular o produto (1º de Minhas Curtidas > Mais Recente)
    for tentativa in range(3):  # linha "Adicionar produto"
        sh('input tap %d %d' % P('add_produto', 640, 345))
        fim = time.time() + 5
        while time.time() < fim and not tela_produtos(print_tela()):
            time.sleep(0.4)
        if tela_produtos(print_tela()):
            break
        retry(10, 'Adicionar produto não abriu')
    esperar_pixel(10, 'tela Adicionar Produto', tela_produtos, limite=10)
    toque(*P('curtidas', 300, 194), espera=4)  # Minhas Curtidas
    toque(*P('mais_recente', 300, 255), espera=5)  # Mais Recente
    for tentativa in range(3):  # toque perdido na aba: toca de novo antes de desistir
        fim = time.time() + 6
        while time.time() < fim:
            im = print_tela()
            if tela_produtos(im) and achar_adicionar(im):
                break
            time.sleep(0.5)
        else:
            retry(11, 'lista de Minhas Curtidas não apareceu')
            toque(*P('curtidas', 300, 194), espera=3)
            toque(*P('mais_recente', 300, 255), espera=3)
            continue
        break
    postar_da_lista(seco)


def legenda_preenchida(im):
    """Texto escuro na área da legenda (o texto de exemplo é cinza claro)."""
    (x1, y1), (x2, y2) = P('leg_area1', 171, 118), P('leg_area2', 790, 170)
    return sum(1 for x in range(x1, x2, 4) for y in range(y1, y2, 3) if max(cor(im, x, y)) < 70) >= 40


def achar_adicionar(im):
    """y do 1º botão laranja 'Adicionar' na coluna x=720 (a altura muda se o aviso amarelo
    de comissão estiver aberto ou fechado)."""
    xs = [P('add_x', x, 300)[0] for x in (680, 720, 760)]
    ya, yb = P('add_y1', 720, 290)[1], P('add_y2', 720, 620)[1]
    for y in range(ya, yb, 2):
        if all(e_laranja(cor(im, x, y)) for x in xs) and e_laranja(cor(im, xs[1], y + 8)):
            return y + 15
    return None


def postar_da_lista(seco):
    fim = time.time() + 30
    y_add = None
    while time.time() < fim and not y_add:
        im = print_tela('p12_lista_produtos.png')
        y_add = achar_adicionar(im) if tela_produtos(im) else None
        if not y_add:
            time.sleep(2)
    if not y_add:
        print_tela('erro_passo_12.png')
        raise Parou('passo 12: não achei o botão "Adicionar" do 1º produto (print: erro_passo_12.png)')
    print(f'  [12] lista carregada (1º Adicionar em y={y_add})')
    # 10/11 (Kevin): favoritar nem sempre põe o produto em 1º (indisponível, não listado, vende em live...).
    # Nunca escolhe por posição: só a linha cujo nome bate com o esperado (titulos.json/itemId), rolando a lista.
    global PRINT_LISTA
    LINHAS_VISTAS.clear()
    PRINT_LISTA = None
    if not TITULO_ESPERADO or (PAGINA_DUVIDA and not TITULO_APROVADO):
        # Kevin 10/11: todo pendente traz o print da lista Adicionar + os nomes das linhas. Sem nome seguro,
        # lê a lista (até 3 telas, sem tocar em nada) e entrega ao Kevin para escolher.
        achar_linha('\u0000sem nome esperado', paginas=3, ocr=True)
        print_tela('erro_passo_12_produto.png')
        raise ConfirmarNome(PAGINA_DUVIDA or 'sem nome esperado do produto (não escolho por posição)')
    # Kevin 10/11: 1ª tela + 1 rolagem; se não achar, o robô refavorita 1 vez (rodar_fila) e confere de novo
    PLACAR_LOG.clear()
    st, y_add, info = achar_linha(TITULO_ESPERADO, paginas=PAGINAS_LISTA)
    if st == 'ausente':
        print_tela('erro_passo_12_produto.png')
        raise ProdutoDaLista(f'{TITULO_ESPERADO!r} não está em Minhas Curtidas ({info})'
                             + (' | placar: ' + ' ; '.join(PLACAR_LOG[-4:]) if PLACAR_LOG else ''))
    if st != 'ok':
        print_tela('erro_passo_12_indisponivel.png')
        raise ProdutoIndisponivel(f'{TITULO_ESPERADO[:60]!r}: {info}')
    x_add = P('add_x', 720, 300)[0]
    janela = lambda im: e_laranja(cor(im, *PX('feito_cor', 200, 1160))) and not e_branco(cor(im, *PX('cab', 400, 62)))
    for tentativa in range(3):  # Adicionar: só toca de novo se ainda estiver na lista
        sh(f'input tap {x_add} {y_add}')
        fim = time.time() + 5
        while time.time() < fim and not janela(print_tela()):
            time.sleep(0.4)
        im = print_tela()
        if janela(im) or not tela_produtos(im):
            break
        vis, _x = textos_na_tela()
        aviso = next((v for v in vis if INDISPONIVEL_RE.search(v)), None)
        if aviso:  # o app recusou (toast/linha): não insiste, pula o produto
            print_tela('erro_passo_12_indisponivel.png')
            PRINT_LISTA = os.path.join(PASTA, 'erro_passo_12_indisponivel.png')
            raise ProdutoIndisponivel(f'{TITULO_ESPERADO[:60]!r}: o app recusou ao adicionar ({aviso[:80]})')
        retry(12, 'Adicionar não abriu a janela')
    else:
        print_tela('erro_passo_12_indisponivel.png')
        PRINT_LISTA = os.path.join(PASTA, 'erro_passo_12_indisponivel.png')
        raise ProdutoIndisponivel(f'{TITULO_ESPERADO[:60]!r}: Adicionar não abriu em 3 toques (não dá para adicionar)')
    postar_do_feito(seco)


def _norm_titulo(s):
    """minúsculas, sem acento, sem pontuação, espaços únicos; tira "..." do fim e o "0" que a
    leitura da tela às vezes cola no começo do nome."""
    import unicodedata
    s = re.sub('[\u200b-\u200d\ufeff]', '', s)  # a folha do vídeo traz o nome com caracteres invisíveis
    s = unicodedata.normalize('NFKD', s.replace('&amp;', '&'))
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'[^\w\s]', ' ', s.replace('…', ' ')).replace('_', ' ')
    return ' '.join(s.split()).lstrip('0')


def mesmo_nome(a, b):
    """Mesmo nome inteiro; só aceita diferença se um for o outro cortado no fim (o app trunca).
    Nunca compara só o começo: "...Linho BEGE" e "...Linho CINZA" são produtos diferentes."""
    a_bruto, b_bruto = a or '', b or ''
    a, b = _norm_titulo(a), _norm_titulo(b)
    if not a or not b:
        return False
    if a == b or (min(len(a), len(b)) >= 25 and (a.startswith(b) or b.startswith(a))):
        return True
    # 21/11 (Kevin, climatizador): a leitura do nome esperado às vezes traz UMA palavra a mais colada no começo
    # ("0WAP Climatizador..." x "Climatizador de Ar Wap..."). Tira só a 1ª palavra de um dos lados e compara de novo
    # (mesmas regras: igual ou um é o começo exato do outro, mín. 25 caracteres; "BEGE" x "CINZA" continua diferente).
    # RESTRITO (Kevin/coordenador 21/11, perfume árabe): só vale se a 1ª palavra for lixo de leitura (começa com dígito
    # colado em letras, tipo "0WAP", ou é um número solto) E o nome não for de perfume/fragrância. Marca na frente NUNCA é ignorada.
    risco = re.compile(r'perfum|fragr|colonia|col[oô]nia|parfum|eau de|deo ', re.I)
    for x, y, bruto in ((a, b, a_bruto), (b, a, b_bruto)):
        pt = bruto.strip().split(' ', 1)[0] if bruto.strip() else ''
        lixo = bool(re.match(r'^\d+[^\W\d_]+', pt)) or pt.isdigit()
        if lixo and ' ' in x and not risco.search(a_bruto) and not risco.search(b_bruto):
            x2 = x.split(' ', 1)[1]
            if x2 == y or (min(len(x2), len(y)) >= 25 and (x2.startswith(y) or y.startswith(x2))):
                return True
    # o OCR do cartão às vezes parte palavra/número ("SHAW TY", "1 57x170c" = 157x170c): sem espaços, mesmas regras
    # (igual ou um é o começo exato do outro, mín. 25 caracteres): continua não confundindo "BEGE" com "CINZA".
    sa, sb = a.replace(' ', ''), b.replace(' ', '')
    return sa == sb or (min(len(sa), len(sb)) >= 25 and (sa.startswith(sb) or sb.startswith(sa)))


def achar_na_lista(titulo, paginas=6, so_primeiro=False):
    """y do botão 'Adicionar' da linha do produto com esse nome em Minhas Curtidas, ou None.
    so_primeiro=True: só aceita se for o 1º produto da lista."""
    for pagina in range(paginas):
        for _ in range(3):
            _, xml = textos_na_tela()
            if xml:
                break
            time.sleep(1)
        im = print_tela()
        nomes = [m for m in re.finditer(r'text="([^"]{15,})"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)
                 if int(m[2]) > P('lista_x', 130, 0)[0] and int(m[3]) >= P('lista_y', 0, 270)[1]
                 and 'comiss' not in m[1].lower()]
        nomes.sort(key=lambda m: int(m[3]))
        if so_primeiro:
            nomes = nomes[:1]
        for m in nomes:
            x1, y1, y2 = int(m[2]), int(m[3]), int(m[5])
            if mesmo_nome(m[1], titulo):
                # botão laranja "Adicionar" da mesma linha: até ~150 px abaixo do topo do nome
                xs = [P('add_x', x, 300)[0] for x in (680, 720, 760)]
                for y in range(y1, min(im.size[1] - 80, y1 + 150), 2):
                    if all(e_laranja(cor(im, x, y)) for x in xs) and e_laranja(cor(im, xs[1], y + 8)):
                        print(f'  [12] produto achado na lista (tela {pagina + 1}): {m[1][:60]}')
                        return y + 15
        if pagina < paginas - 1:
            sh('input swipe %d %d %d %d 600' % (*P('lista_de', 400, 1000), *P('lista_ate', 400, 450)))  # rola a lista
            time.sleep(2.5)
    return None


def _parece_linha(a, b, limiar=0.75):
    """Nomes parecidos (ignora acento/pontuação e o corte "..." do app): compara o começo do maior com o menor."""
    import difflib
    x, y = _norm_titulo(a), _norm_titulo(b)
    if not x or not y:
        return False
    n = min(len(x), len(y))
    return difflib.SequenceMatcher(None, x[:n], y[:n]).ratio() >= limiar


def _ocr_primeira_linha(im):
    """OCR só do nome do 1º cartão da lista Adicionar (poco720: x 205-700, y 440-545), duas linhas juntas."""
    try:
        if im.size != (720, 1600):
            return ''
        rec = im.crop((205, 440, 700, 545)).resize((990, 210))
        caminho = os.path.join(PASTA, 'ocr_primeira_linha.png')
        rec.save(caminho)
        r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocr_tela.ps1'), caminho],
                           capture_output=True, timeout=60)
        linhas = [l.strip() for l in r.stdout.decode('utf-8', 'ignore').splitlines() if l.strip()]
        linhas = [l for l in linhas if not re.search(r'taxa de comiss|vendid|^r\$|comms|adicionar', l, re.I)]
        return ' '.join(linhas).strip(' ,.…')
    except Exception:
        return ''


REFRESH_LISTA = 0  # >0: segundos de espera + puxar a lista (pull-to-refresh) antes de ler (refação de "produto não achado")
PAGINAS_LISTA = 2  # telas lidas em Minhas Curtidas; as refações sobem para 8 (produto já favoritado antes pode estar mais abaixo)


def achar_linha(titulo, paginas=8, ocr=False):
    """Procura em Minhas Curtidas SÓ a linha cujo nome bate com `titulo` (rolando a lista).
    Devolve (estado, y_do_Adicionar, info):
      'ok'          -> y do botão laranja Adicionar daquela linha
      'indisponivel'-> a linha tem rótulo de indisponível/não listado/esgotado (info = rótulo)
      'sem_botao'   -> a linha não tem botão Adicionar laranja (não dá para adicionar)
      'ausente'     -> nenhuma linha com esse nome depois de rolar a lista
    Nunca devolve outra linha: posição na lista não conta.
    Guarda em LINHAS_VISTAS os nomes vistos e em PRINT_LISTA o print mais útil (1ª tela, ou a tela
    em que a linha foi achada) para o pendente de aprovação."""
    global PRINT_LISTA
    vistos_fim = None
    if REFRESH_LISTA:  # o favorito pode levar uns segundos para entrar em Minhas Curtidas: espera e puxa a lista
        time.sleep(REFRESH_LISTA)
        sh('input swipe %d %d %d %d 500' % (*P('lista_ate', 400, 450), *P('lista_de', 400, 1000)))  # puxa para baixo
        time.sleep(3)
    limite_busca = time.time() + 180  # 21/11: no máximo 3 min procurando; depois é "ausente" (vira pendente e a fila segue)
    for pagina in range(paginas):
        if pagina and time.time() > limite_busca:
            return 'ausente', None, f'tempo máximo de busca (3 min) após {pagina} telas' + _parecidos(titulo)
        xml = ''
        for _ in range(3):
            _, xml = textos_na_tela()
            if xml:
                break
            time.sleep(1)
        im = print_tela()
        alto = im.size[1]
        x_min, y_min = P('lista_x', 130, 0)[0], P('lista_y', 0, 270)[1]
        nos = [(m[1].replace('&amp;', '&'), int(m[2]), int(m[3]), int(m[5]))
               for m in re.finditer(r'text="([^"]{3,})"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml or '')
               if int(m[2]) > x_min and int(m[3]) >= y_min]
        rotulos = [n for n in nos if len(n[0]) <= 60 and INDISPONIVEL_RE.search(n[0])]
        nomes = sorted((n for n in nos if len(n[0]) >= 15 and 'comiss' not in n[0].lower()
                        and n not in rotulos), key=lambda n: n[2])
        for n in nomes:
            if n[0] not in LINHAS_VISTAS and not n[0].startswith('R$'):
                LINHAS_VISTAS.append(n[0])
        if ocr:  # o dump do uiautomator às vezes perde linhas (o monitor, 10/11): completa com OCR do print
            import difflib
            for l in ler_tela_ocr():
                if len(l) >= 15 and not re.search(r'taxa de comiss|vendid|^r\$|comms|adicionar|curtidas|pesquisar|relev|destaque', l, re.I) \
                        and not any(difflib.SequenceMatcher(None, _norm_titulo(l), _norm_titulo(v)).ratio() >= 0.7
                                    or _norm_titulo(l) in _norm_titulo(v) for v in LINHAS_VISTAS):
                    LINHAS_VISTAS.append('(OCR) ' + l)
        if pagina == 0:
            with contextlib.suppress(Exception):
                open(os.path.join(PASTA, 'p12_dump_pag1.xml'), 'w', encoding='utf-8').write(xml or '')
            # Kevin 10/11 (monitor gamer): a 1ª linha da lista às vezes NÃO sai no dump do uiautomator. Lê a 1ª linha
            # por OCR (recorte do cartão 1): entra nas opções do pendente e, se parece com o nome esperado, vale.
            prim = _ocr_primeira_linha(im)
            if prim and len(prim) >= 20 and not any(_parece_linha(prim, n[0]) for n in nomes):
                if prim not in LINHAS_VISTAS:
                    LINHAS_VISTAS.insert(0, '(OCR) ' + prim)
                y_primeira = achar_adicionar(im)
                if titulo and y_primeira and len(prim) >= 30 and _parece_linha(prim, titulo, 0.88):
                    with contextlib.suppress(Exception):
                        im.save(os.path.join(PASTA, 'p12_lista_achado.png'))
                        PRINT_LISTA = os.path.join(PASTA, 'p12_lista_achado.png')
                    print(f'  [12] produto achado na lista pela 1ª linha (OCR; o dump não trouxe): {prim[:60]}')
                    return 'ok', y_primeira, ''
            with contextlib.suppress(Exception):
                im.save(os.path.join(PASTA, 'p12_lista_pag1.png'))
                PRINT_LISTA = os.path.join(PASTA, 'p12_lista_pag1.png')
        for i, (txt, x1, y1, y2) in enumerate(nomes):
            if not mesmo_nome(txt, titulo):
                continue
            prox = next((n[2] for n in nomes[i + 1:] if n[2] > y2 + 10), None)
            fim_linha = prox if prox else y1 + 200
            if not prox and fim_linha > alto - 80 and pagina < paginas - 1:
                break  # linha cortada no pé da tela: rola e olha de novo
            with contextlib.suppress(Exception):
                im.save(os.path.join(PASTA, 'p12_lista_achado.png'))
                PRINT_LISTA = os.path.join(PASTA, 'p12_lista_achado.png')
            rot = next((n[0] for n in rotulos if y1 - 10 <= n[2] < fim_linha), None)
            if rot:
                print(f'  [12] produto achado mas indisponível (tela {pagina + 1}): {txt[:50]} · {rot[:40]}')
                return 'indisponivel', None, f'na lista como "{rot[:60]}"'
            xs = [P('add_x', x, 300)[0] for x in (680, 720, 760)]
            for y in range(y1, min(alto - 80, fim_linha), 2):
                if all(e_laranja(cor(im, x, y)) for x in xs) and e_laranja(cor(im, xs[1], y + 8)):
                    print(f'  [12] produto achado na lista (tela {pagina + 1}): {txt[:60]}')
                    return 'ok', y + 15, ''
            print(f'  [12] produto achado sem botão Adicionar (tela {pagina + 1}): {txt[:50]}')
            return 'sem_botao', None, 'na lista sem botão Adicionar (não dá para adicionar)'
        r_placar = _placar_lista(titulo, nomes, nos, rotulos, im, pagina, alto)
        if r_placar:
            return r_placar
        assinatura = tuple(n[0] for n in nomes)
        if assinatura and assinatura == vistos_fim:
            return 'ausente', None, f'fim da lista na tela {pagina + 1}' + _parecidos(titulo)
        vistos_fim = assinatura
        if pagina < paginas - 1:
            sh('input swipe %d %d %d %d 600' % (*P('lista_de', 400, 1000), *P('lista_ate', 400, 450)))  # rola a lista
            time.sleep(2.5)
    return 'ausente', None, f'{paginas} telas olhadas' + _parecidos(titulo)


PLACAR_LOG = []  # linhas do placar da última busca (vão para o motivo do pendente e para o log)
PLACAR_ATIVO = True


def _placar_lista(titulo, nomes, nos, rotulos, im, pagina, alto):
    """PLACAR (placar.py): várias provas por linha (posição, foto, nome distintivo, preço fraco) + vetos (marca/modelo/ml/cor).
    1ª linha + UMA 2ª confirmação (foto média/forte OU nome distintivo) = aceita; fora da 1ª: foto forte + nome; perfume/alto
    risco: 1ª + foto forte + nome. Nunca escolhe na dúvida (empate/veto -> None e o fluxo segue para o pendente)."""
    if not PLACAR_ATIVO or not titulo or not nomes:
        return None
    try:
        import placar
        cache = placar.ler_cache(ITEM_ID) if ITEM_ID else None
        linhas = []
        nomes = [n for n in nomes if not n[0].startswith('R$')]  # faixa de preço "R$10 - R$20" não é nome de produto
        for i, n in enumerate(nomes):
            prox = next((m[2] for m in nomes[i + 1:] if m[2] > n[3] + 10), None)
            fim_linha = prox if prox else n[2] + 200
            if fim_linha > alto - 80 and not prox:
                continue  # linha cortada no pé da tela: vê depois de rolar
            preco = next((placar.preco_da_linha(x[0]) for x in nos if n[2] <= x[2] < fim_linha and placar.preco_da_linha(x[0])), None)
            if preco is None:
                continue  # sem preço na linha = não é uma linha de produto (aba/rótulo)
            mini = im.crop((24, n[2], 196, min(alto, n[2] + 172)))
            pos = len(linhas) if pagina == 0 else len(linhas) + 1  # posição entre as linhas de produto (1ª = 0)
            linhas.append((n, fim_linha, placar.avaliar(titulo, n[0], preco, mini, cache, pos)))
        if not linhas:
            return None
        idx, log = placar.decidir([l[2] for l in linhas], titulo)
        for l, (ln, _f, _pl) in zip(log, linhas):
            print(f'  [placar] tela {pagina + 1} · {ln[0][:40]!r} · {l}')
        for l in log[len(linhas):]:
            print(f'  [placar] {l}')
        PLACAR_LOG[:] = (PLACAR_LOG + [f'tela {pagina + 1} {l}' for l in log])[-12:]
        if idx is None:
            return None
        (txt, x1, y1, y2), fim_linha, _p = linhas[idx]
        rot = next((n[0] for n in rotulos if y1 - 10 <= n[2] < fim_linha), None)
        if rot:
            return 'indisponivel', None, f'na lista como "{rot[:60]}"'
        xs = [P('add_x', x, 300)[0] for x in (680, 720, 760)]
        for y in range(y1, min(alto - 80, fim_linha), 2):
            if all(e_laranja(cor(im, x, y)) for x in xs) and e_laranja(cor(im, xs[1], y + 8)):
                with contextlib.suppress(Exception):
                    im.save(os.path.join(PASTA, 'p12_lista_achado.png'))
                global PRINT_LISTA
                PRINT_LISTA = os.path.join(PASTA, 'p12_lista_achado.png')
                print(f'  [12] produto achado pelo PLACAR (tela {pagina + 1}): {txt[:60]}')
                return 'ok', y + 15, ''
    except Exception as e:
        print(f'  [placar] erro (segue sem placar): {e}')
    return None


def _parecidos(titulo):
    """Linhas vistas com nome parecido (não igual): o Kevin decide se é o mesmo produto."""
    import difflib
    alvo = _norm_titulo(titulo)
    par = [v for v in LINHAS_VISTAS if difflib.SequenceMatcher(None, alvo, _norm_titulo(v)).ratio() >= 0.6]
    return f'; nome parecido: {par[0][:60]!r}' + (f' (+{len(par) - 1})' if len(par) > 1 else '') if par else ''


def produto_vinculado(im):
    """Cartão do produto (y 375-495): nome em texto escuro na linha y~400 e preço vermelho em y~470."""
    (a1, b1), (a2, b2) = P('card_nome1', 68, 388), P('card_nome2', 740, 418)
    (c1, d1), (c2, d2) = P('card_preco1', 68, 460), P('card_preco2', 200, 482)
    nome = sum(1 for x in range(a1, a2, 3) for y in range(b1, b2, 2) if max(cor(im, x, y)) < 100)
    preco = sum(1 for x in range(c1, c2, 2) for y in range(d1, d2, 2) if e_vermelho(cor(im, x, y)) or e_laranja(cor(im, x, y)))
    return nome >= 20 and preco >= 5


VIDEO_PELA_NOTIF = None  # {'t': hora em que o player abriu, 'thumb': miniatura do aviso} (rodar_fila lê)
AVISO_TOCADO = None  # 12/11: {'t': hora do toque, 'thumb': miniatura} quando tocou no aviso e o player NÃO abriu a tempo


def aviso_envio_visivel(im):
    """Cartão branco do aviso "Enviado com sucesso! / Clique aqui para ver seu vídeo." no topo (720x1600):
    x 24-696, y 180-296, quase todo branco, com texto escuro e a miniatura do vídeo à esquerda."""
    if im.size != (720, 1600):
        return False
    xs, ys = range(150, 690, 12), range(190, 290, 8)
    tot = len(xs) * len(ys)
    branco = sum(1 for x in xs for y in ys if min(im.getpixel((x, y))) > 236)
    escuro = sum(1 for x in range(146, 480, 6) for y in range(205, 272, 4) if max(im.getpixel((x, y))) < 120)
    # miniatura à esquerda: não é branca
    mini = sum(1 for x in range(44, 120, 8) for y in range(200, 276, 8) if min(im.getpixel((x, y))) < 200)
    # faixa logo abaixo do cartão NÃO é branca (o cartão acaba em y~296) e a acima (y 160-176) também não
    return branco >= 0.78 * tot and escuro >= 25 and mini >= 20


def aviso_carregando(im):
    """12/11: o MESMO cartão branco aparece durante o envio ("Carregando... 75%"), com a barra de progresso
    (laranja + trilho cinza) na linha y~292. O robô confundia esse cartão com "Enviado com sucesso!" e tocava
    nele (nada abria) ou desistia em 10 s antes do envio acabar (33 de 53 posts em 12/11)."""
    if im.size != (720, 1600):
        return False
    # 12/11 (post 1111A_03 esperou 90 s à toa): a linha y=292 de um vídeo do feed também pode parecer "barra".
    # Exige o CARTÃO BRANCO do aviso (mesma região do "Enviado com sucesso!") e só então a barra.
    xs, ys = range(150, 690, 12), range(190, 290, 8)
    branco = sum(1 for x in xs for y in ys if min(im.getpixel((x, y))) > 236)
    if branco < 0.78 * len(xs) * len(ys):
        return False
    pts = [im.getpixel((x, 292)) for x in range(30, 690, 10)]
    barra = sum(1 for c in pts if e_laranja(c) or (150 <= min(c) and max(c) <= 200 and max(c) - min(c) < 12))
    return barra >= 0.8 * len(pts)


def tocar_aviso_envio(segundos=10, teto=90):
    """PLANO A (Kevin 10/11): logo depois de sair da legenda, vigia o topo da tela; quando o cartão
    "Enviado com sucesso!" aparece, toca nele (no centro do cartão, só ali) e confere que o player do
    vídeo abriu em ~3 s. Devolve True se abriu; False = plano B (perfil). Nunca toca em outra coisa."""
    global VIDEO_PELA_NOTIF, AVISO_TOCADO
    VIDEO_PELA_NOTIF = AVISO_TOCADO = None
    if PERFIL == 'tablet':
        return False
    t0 = time.time()
    fim_espera, viu_carregando = t0 + segundos, False
    while time.time() < fim_espera:
        im = print_tela()
        if aviso_carregando(im):  # ainda enviando: espera o "Enviado com sucesso!" (até `teto` s no total)
            if not viu_carregando:
                print('  [aviso] envio em andamento ("Carregando..."): esperando terminar')
            viu_carregando = True
            fim_espera = min(t0 + teto, max(fim_espera, time.time() + 8))
            time.sleep(0.5)
            continue
        if aviso_envio_visivel(im):
            # 10/11: com o cartão já sumido o toque cai no feed de Live (x=400 = "+ Seguir"; x=480 = banner
            # "Maratona de Lives" que abriu uma WebPageActivity). Só toca se o cartão aparece em 2 prints seguidos.
            try:
                im2 = print_tela()
                if not aviso_envio_visivel(im2) or aviso_carregando(im2):
                    continue
            except Exception:
                continue
            thumb = im.crop((42, 198, 122, 278))
            try:
                os.makedirs(os.path.join(PASTA, 'aviso_envio'), exist_ok=True)
                im.crop((0, 0, 720, 520)).save(os.path.join(PASTA, 'aviso_envio', 'ultimo_visto.png'))
            except Exception:
                pass
            # 10/11 (cinta térmica): em 12 de 44 posts o toque não abriu o vídeo (1º toque perdido ou cartão já sumido,
            # e o toque caía no feed de Live). Agora: 1 toque; se não abriu e o cartão AINDA está na tela, repete
            # 1 vez; se o cartão já sumiu, não toca mais (não toca no feed) e vai pelo perfil. Toca em x=480 (longe
            # do botão "+ Seguir" que o feed de Live mostra em x 250-380).
            foco = ''
            for n_toque in range(2):
                sh('input tap 300 238')  # centro do cartão (texto "Enviado com sucesso!"), longe dos banners do feed
                t_toque = time.time()
                # 12/11: 2,8 s era pouco (o app ainda está terminando o envio): o player abria DEPOIS, tocava
                # sozinho e o robô ia pelo perfil e abria o vídeo de novo (Kevin: "assiste pela metade e depois
                # inteiro"). Agora espera até 5 s.
                fim = t_toque + 5.0
                while time.time() < fim:
                    time.sleep(0.3)
                    foco = sh('dumpsys window | grep mCurrentFocus')
                    # 10/11: o aviso abre o vídeo em ReactActivity_ (o perfil abre em NativePlayerActivity)
                    if 'NativePlayerActivity' in foco or 'ReactActivity' in foco:
                        VIDEO_PELA_NOTIF = {'t': t_toque + 1.0, 'thumb': thumb}
                        return True
                if n_toque == 0:
                    try:
                        if not aviso_envio_visivel(print_tela()):
                            break  # cartão já sumiu: não toca no feed
                    except Exception:
                        break
            try:
                print_tela('aviso_depois_do_toque.png')
            except Exception:
                pass
            if 'WebPageActivity' in foco:  # o toque abriu uma página web (banner): volta
                sh('input keyevent KEYCODE_BACK')
                time.sleep(1)
            else:  # o player pode abrir atrasado: rodar_fila confere o foco de novo antes de ir pelo perfil
                AVISO_TOCADO = {'t': t_toque, 'thumb': thumb}
            print(f'  [aviso] toquei no aviso mas o vídeo não abriu (foco: {foco.strip()[-80:]}): plano B (perfil)')
            return False
    print('  [aviso] "Enviado com sucesso!" não apareceu em %d s: plano B (perfil)' % (time.time() - t0))
    return False


CAPTURAS_AVISO = 0


def capturar_aviso_envio(max_posts=3, segundos=9):
    """SÓ OBSERVA (não toca em nada): logo depois de sair da legenda, tira prints a cada ~0.5 s e um dump
    no fim, em gravacao\\aviso_envio\\, para eu ver como/onde aparece "Enviado com sucesso!" e quanto tempo
    fica. Só nos primeiros posts de cada partida."""
    global CAPTURAS_AVISO
    if CAPTURAS_AVISO >= max_posts:
        return
    CAPTURAS_AVISO += 1
    try:
        pasta = os.path.join(PASTA, 'aviso_envio', f'post{CAPTURAS_AVISO}')
        os.makedirs(pasta, exist_ok=True)
        t0, n = time.time(), 0
        while time.time() - t0 < segundos:
            im = print_tela()
            im.crop((0, 0, im.size[0], 520)).save(os.path.join(pasta, f'q{n:02d}_{time.time() - t0:04.1f}s.png'))
            n += 1
            time.sleep(0.3)
        _v, xml = textos_na_tela(8)
        open(os.path.join(pasta, 'dump.xml'), 'w', encoding='utf-8').write(xml or '')
    except Exception as e:
        print(f'  (captura do aviso falhou: {e})')


def postar_confirmar_celular():
    """Celular: o 1º toque depois de tela parada pode se perder (05/11). Só repete enquanto a tela
    de legenda segue aberta (nada saiu). Saiu da tela = post aceito; a prova é a conferência no perfil."""
    global TOCOU_POSTAR
    def na_legenda():  # ainda na legenda OU com a folha "Editar informações" aberta = nada foi publicado
        if 'PublishVideoActivity' in sh('dumpsys window | grep mCurrentFocus'):
            return True
        try:
            im = print_tela()
            return tela_legenda(im) or _janela_editar(im)
        except Exception:
            return False
    for n in range(3):
        fim = time.time() + 10
        while time.time() < fim and na_legenda():
            time.sleep(1)
        if not na_legenda():
            break
        if n == 2:
            TOCOU_POSTAR = False  # a tela nunca saiu da legenda: nada foi publicado
            print_tela('erro_postar.png')
            raise Parou('Postar não reagiu a 3 toques (print: erro_postar.png)')
        print(f'  [16] Postar não reagiu; tocando de novo ({n + 2}/3)')
        toque(*P('postar_toque', 445, 1168), espera=3)
    if tocar_aviso_envio():  # plano A: aviso "Enviado com sucesso!" tocado, vídeo postado aberto
        print('[ok] vídeo postado (aviso "Enviado com sucesso!" visto e tocado)')
        return
    # 12/11: confirmar_postado(limite=4) gastava ~6-8 s por post sem nunca reconhecer nada no celular.
    # Agora 1 print só: se a janela do WhatsApp estiver aberta, fecha; a prova continua sendo a conferência no perfil.
    if janela_whatsapp(print_tela('p17_postado.png')):
        fechar_whatsapp()
        print('[ok] vídeo postado (confirmação vista)')
    else:
        print('[ok?] saiu da tela de legenda, sem confirmação visual: quem prova é a conferência no perfil')


def ler_tela_ocr():
    """Linhas de texto do print da tela (OCR do Windows, ocr_tela.ps1). Vazio se nao leu."""
    try:
        caminho = os.path.join(PASTA, 'ocr_cartao.png')
        print_tela('ocr_cartao.png')
        r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocr_tela.ps1'), caminho],
                           capture_output=True, timeout=60)
        return [l.strip() for l in r.stdout.decode('utf-8', 'ignore').splitlines() if l.strip()]
    except Exception:
        return []


class CartaoIlegivel(Parou):
    """O cartão do produto na legenda não pôde ser LIDO (dump vazio e OCR sem o nome). Nada foi publicado.
    Não é "nome diferente": rodar_fila manda o item para pendentes (com o print da lista Adicionar)."""


def ler_cartao_ocr_recorte():
    """OCR só do recorte do cartão do produto (poco720: y 585-700), ampliado 2x. O OCR da tela inteira
    lia o texto da capa do vídeo em vez do cartão (bike infantil, 10/11)."""
    try:
        im = print_tela()
        if im.size != (720, 1600):
            return []
        rec = im.crop((90, 585, 640, 700)).resize((1100, 230))
        caminho = os.path.join(PASTA, 'ocr_cartao_recorte.png')
        rec.save(caminho)
        r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocr_tela.ps1'), caminho],
                           capture_output=True, timeout=60)
        return [l.strip() for l in r.stdout.decode('utf-8', 'ignore').splitlines() if l.strip()]
    except Exception:
        return []


def _tem_palavras_do_nome(v, esperado):
    """A linha lida tem >= 2 palavras (>=5 letras) do nome esperado? (senão é outra coisa: capa, legenda...)"""
    pal = {p for p in re.findall(r'\w{5,}', _norm_titulo(esperado))}
    return len(pal & set(re.findall(r'\w{5,}', _norm_titulo(v)))) >= 2


def leitura_parcial_consistente(lida, esperado):
    """Só para produto JÁ APROVADO pelo Kevin (nome aprovado por itemId; a página abriu pelo itemId e a linha
    da lista bateu inteira): o OCR do cartão às vezes come um pedaço ("Tapetes Sisal Sintético e 2,50...").
    Vale se a leitura tem >= 20 caracteres e >= 4 palavras, TODAS as palavras lidas existem no nome aprovado
    e aparecem na mesma ordem (então nenhum número/cor trocado ou novo). Palavra a mais ou diferente = não vale."""
    a, b = _norm_titulo(lida), _norm_titulo(esperado)
    # 13/11 (carretilha, 3 pendentes): o OCR embaralha números ("10-25lbs" -> "1 0-251bs"). Para produto JÁ aprovado
    # pelo Kevin (achado na lista pelo nome aprovado), vale a leitura que é parecida (>= 0.88) com o começo do nome
    # aprovado, com >= 25 caracteres e >= 4 palavras.
    if len(a) >= 25 and len(a.split()) >= 4:
        import difflib
        n = min(len(a), len(b))
        if difflib.SequenceMatcher(None, a[:n], b[:n]).ratio() >= 0.88:
            return True
    # o OCR às vezes parte uma palavra ("SHAW TY" = SHAWTY): sem espaços, a leitura tem que ser o começo
    # exato do nome aprovado (mesma ordem, nada a mais) e ter >= 20 caracteres.
    sa, sb = a.replace(' ', ''), b.replace(' ', '')
    if len(sa) >= 20 and len(a.split()) >= 4 and sb.startswith(sa):
        return True
    ta, tb = a.split(), b.split()
    if len(a) < 20 or len(ta) < 4:
        return False
    i, casou, lixo = 0, 0, 0
    for k, w in enumerate(ta):
        j = i
        while j < len(tb) and tb[j] != w:
            j += 1
        if j < len(tb):  # palavra do nome aprovado, na ordem
            i, casou = j + 1, casou + 1
        elif k == len(ta) - 1 and len(w) >= 4 and any(t.startswith(w) for t in tb[i:]):
            casou += 1  # última palavra cortada pelo "..." do app ("emborra..." = emborrachamento)
        elif len(w) <= 3:  # sobra curta do OCR ("cki", "ox8", "1"): ruído, ignora (no máx. 3)
            lixo += 1
        else:  # palavra longa que não é do nome aprovado (outro modelo/cor): não vale
            return False
    return casou >= 4 and lixo <= 3 and casou >= lixo + 2


def conferir_cartao_antes_de_postar():
    """Última trava: lê o nome no cartão do produto na tela da legenda. Não leu ou não bate = não posta."""
    if not TITULO_ESPERADO:
        raise CartaoIlegivel('passo 15: sem nome esperado do produto; não posto às cegas')
    lidos = []
    dumps_vazios = 0
    # 12/11 (Kevin: "demora muito na tela de postar"): no celular o dump do uiautomator NUNCA sai com o vídeo
    # tocando na miniatura (log 12/11: 2 dumps vazios = 8 s + 20 s, ~24 s em todo post). Agora lê primeiro o
    # recorte do cartão pelo OCR (~2-4 s). A regra de aceitar é a MESMA (mesmo_nome / parcial aprovada);
    # se o OCR não bater, cai no caminho antigo (dump + OCR da tela inteira).
    if PERFIL != 'tablet':
        t_ocr = time.time()
        vis = ler_cartao_ocr_recorte()
        vis = [x for v in vis for x in (v, re.sub(r'^\S{1,2}\s+', '', v))]
        rapidos = [re.sub('[​-‍﻿]', '', v) for v in vis if len(v) >= 12]
        if any(mesmo_nome(v, TITULO_ESPERADO) for v in rapidos):
            print(f'  [15] cartão confere (OCR do cartão, {time.time() - t_ocr:.1f} s): {TITULO_ESPERADO[:50]}')
            return
        if TITULO_APROVADO:
            ok_p = next((v for v in rapidos if leitura_parcial_consistente(v, TITULO_ESPERADO)), None)
            if ok_p:
                print(f'  [15] cartão confere (OCR do cartão, leitura parcial de produto aprovado pelo Kevin, '
                      f'{time.time() - t_ocr:.1f} s): lido={ok_p[:60]!r} aprovado={TITULO_ESPERADO[:50]!r}')
                return
        print(f'  [15] OCR rápido do cartão não bateu ({rapidos[:2]}); lendo pelo caminho completo')
    # A tela da legenda toca o video na miniatura: o dump do uiautomator as vezes vem vazio ou estoura
    # os 8 s. Leitura vazia NUNCA passa; so tenta de novo com mais tempo (ate 6 vezes).
    for n in range(6):
        vis, xml = textos_na_tela(limite=8 if n == 0 else 20)
        if not xml:
            dumps_vazios += 1
            if dumps_vazios >= 2:  # dump nao sai com o video na tela: le o print com o OCR do Windows
                vis = ler_cartao_ocr_recorte() + ler_tela_ocr()  # recorte do cartão primeiro
                # o OCR cola o icone da sacola como 1-2 letras no comeco da linha ("O Aparador..."): tira so isso
                vis = [x for v in vis for x in (v, re.sub(r'^\S{1,2}\s+', '', v))]
                xml = 'ocr' if vis else ''
            if not xml:
                time.sleep(1.5)
                continue
        lidos = [re.sub('[\u200b-\u200d\ufeff]', '', v) for v in vis if len(v) >= 12]
        # o nome vem truncado no cartao ("...Buffet em MD\u2026"): mesmo_nome aceita o corte no fim, com no
        # minimo 25 caracteres, e so contra o nome COMPLETO esperado.
        if any(mesmo_nome(v, TITULO_ESPERADO) for v in lidos):
            print(f'  [15] cart\u00e3o confere: {TITULO_ESPERADO[:50]}')
            return
        if TITULO_APROVADO:  # aprova\u00e7\u00e3o do Kevin vale para sempre neste itemId: leitura parcial consistente passa
            ok_p = next((v for v in lidos if leitura_parcial_consistente(v, TITULO_ESPERADO)), None)
            if ok_p:
                print(f'  [15] cart\u00e3o confere (leitura parcial de produto aprovado pelo Kevin): lido={ok_p[:60]!r} '
                      f'aprovado={TITULO_ESPERADO[:50]!r}')
                return
        if lidos:
            break
        time.sleep(1)
    print_tela('erro_cartao_antes_postar.png')
    motivo = f'dump vazio {dumps_vazios}x' if not lidos else f'lido: {lidos[:4]}'
    msg = f'passo 15: cart\u00e3o do produto n\u00e3o confere com {TITULO_ESPERADO[:50]!r} ({motivo})'
    # Kevin 10/11: na d\u00favida N\u00c3O posta, vira pendente e a fila segue (nunca trava na tela de postar).
    # Vale para cart\u00e3o ileg\u00edvel (nada parecido com o nome) E para nome lido que n\u00e3o bate com certeza
    # (ex.: OCR comeu um peda\u00e7o). Nada \u00e9 publicado nos dois casos.
    raise CartaoIlegivel(msg)


def _janela_editar(im):
    """Folha "Editar informações do produto" (botão laranja Feito) aberta por cima da legenda."""
    return e_laranja(cor(im, *PX('feito_cor', 200, 1160))) and not e_branco(cor(im, *PX('cab', 400, 62)))


def postar_do_feito(seco):
    # (400,1176) cai em cima do texto branco "Feito"; conferir a cor em (200,1160)
    esperar_pixel(13, 'janela Editar informações (Feito)',
                  lambda im: e_laranja(cor(im, *PX('feito_cor', 200, 1160))) and not e_branco(cor(im, *PX('cab', 400, 62))),
                  limite=20)
    janela = lambda im: e_laranja(cor(im, *PX('feito_cor', 200, 1160))) and not e_branco(cor(im, *PX('cab', 400, 62)))
    pronto = lambda im: tela_legenda(im) and not e_branco(cor(im, *PX('reuso', 748, 560)))
    # ATENÇÃO: Feito fica quase em cima do Postar. Só toca de novo se a janela AINDA estiver aberta,
    # conferido no print logo antes do toque; na tela da legenda nunca toca aqui.
    for tentativa in range(3):
        im = print_tela()
        if pronto(im) or tela_legenda(im) or not janela(im):
            break
        if tentativa:
            retry(13, 'Feito não fechou a janela')
        sh('input tap %d %d' % P('feito', 400, 1176))
        fim = time.time() + 4
        while time.time() < fim and janela(print_tela()):
            time.sleep(0.4)

    # 14-15. botões: reutilização OFF, rótulo IA ON (posições com produto vinculado)
    # Rápido: 1 print por rodada, toca só o que falta, confere no print seguinte.
    t0 = time.time()
    esperar_pixel(14, 'tela da legenda com produto vinculado',
                  lambda im: tela_legenda(im) and not e_branco(cor(im, *PX('reuso', 748, 560))), limite=25)
    im = print_tela()
    for _ in range(5):
        reuso_on, ia_on = e_verde(cor(im, *PX('reuso', 748, 560))), e_verde(cor(im, *PX('ia', 748, 738)))
        if not reuso_on and ia_on:
            break
        if _:
            retry(15, f'botões reutilização={reuso_on} IA={ia_on}')
        if reuso_on:
            sh('input tap %d %d' % P('reuso', 748, 560)); time.sleep(0.8)
        if not ia_on:
            sh('input tap %d %d' % P('ia', 748, 738))
        time.sleep(1.2)
        im = print_tela()
    if e_verde(cor(im, *PX('reuso', 748, 560))) or not e_verde(cor(im, *PX('ia', 748, 738))):
        im.save(os.path.join(PASTA, 'p15_antes_postar.png'))
        raise Parou('passo 15: botões não ficaram (reutilização OFF / IA ON) — ver p15_antes_postar.png')
    if not legenda_preenchida(im):
        im.save(os.path.join(PASTA, 'p15_antes_postar.png'))
        raise Parou('passo 15: legenda parece vazia — ver p15_antes_postar.png')
    if not produto_vinculado(im):
        im.save(os.path.join(PASTA, 'p15_antes_postar.png'))
        raise CartaoIlegivel('passo 15: produto não aparece vinculado — ver p15_antes_postar.png')
    print(f'  [15] conferido em {time.time() - t0:.1f} s (botões, legenda, produto)')
    conferir_cartao_antes_de_postar()

    if seco:
        print_tela('seco_final.png')
        print('[--seco] parei antes de Postar. Print: gravacao\\seco_final.png')
        return

    # 10/11 (Cherry C): a folha "Editar informações do produto" pode abrir por cima da legenda e o toque em
    # Postar caía no "Feito" dela (o robô achava que tinha postado). Antes de Postar a folha TEM que estar
    # fechada e a tela tem que ser a da legenda limpa.
    for _t in range(4):
        im = print_tela()
        if tela_legenda(im) and not _janela_editar(im):
            break
        if _janela_editar(im):
            retry(16, 'folha Editar informações aberta antes de Postar: Feito')
            sh('input tap %d %d' % P('feito', 400, 1176))
        time.sleep(1.5)
    else:
        print_tela('erro_antes_postar_folha.png')
        raise Parou('antes de Postar: a tela não é a da legenda limpa (folha Editar informações aberta?) — ver erro_antes_postar_folha.png')
    global TOCOU_POSTAR
    TOCOU_POSTAR = True  # daqui em diante qualquer falha é "incerto" (pode ter publicado)
    marca('adicionar+nome+botoes')
    toque(*P('postar_toque', 445, 1168), espera=3)  # Postar (centro do botão; 'postar' é o ponto de cor)
    if PERFIL != 'tablet':
        return postar_confirmar_celular()
    if not confirmar_postado(limite=300):
        print_tela('erro_incerto.png')
        raise Incerto('não vi "Vídeo postado!/Enviado com sucesso!" em 300 s (print: erro_incerto.png)')
    print_tela('p17_postado.png')
    time.sleep(1)
    fechar_whatsapp()  # Cancelar na janela do WhatsApp (pode demorar a aparecer/fechar)
    print('[ok] vídeo postado (confirmação vista)')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('video'); p.add_argument('link'); p.add_argument('legenda')
    p.add_argument('--seco', action='store_true')
    p.add_argument('--sem-favoritar', action='store_true', help='produto já está no topo de Minhas Curtidas')
    p.add_argument('--sem-enviar', action='store_true', help='vídeo já está na galeria')
    p.add_argument('--da-legenda', action='store_true', help='retomar a partir da tela "Adicionar legenda" já aberta')
    p.add_argument('--da-lista', action='store_true', help='retomar na lista "Minhas Curtidas > Mais Recente" já aberta')
    p.add_argument('--do-feito', action='store_true', help='retomar na janela "Editar informações do produto"')
    p.add_argument('--doc', help='id do post para o postados.json (padrão: nome do vídeo)')
    a = p.parse_args()
    doc = a.doc or os.path.splitext(os.path.basename(a.video))[0]
    leg = a.legenda.replace('\\n', '\n')
    try:
        if a.do_feito:
            postar_do_feito(a.seco)
        elif a.da_lista:
            postar_da_lista(a.seco)
        elif a.da_legenda:
            postar_da_legenda(leg, a.seco)
        else:
            postar(a.video, a.link, leg, a.seco,
                   favoritar=not a.sem_favoritar, enviar_video=not a.sem_enviar)
    except Incerto as e:
        registrar(doc, 'incerto', str(e))
        print('INCERTO:', e)
        sys.exit(2)
    except Parou as e:
        print('PAROU (não postado):', e)
        sys.exit(1)
    if not a.seco:
        # só chega aqui se confirmar_postado() viu a confirmação
        registrar(doc, 'postado', 'confirmação vista; reutilização OFF, IA ON')
        # fim do ciclo: manda o vídeo do PC para a Lixeira (recuperável), só depois de postado
        if os.path.isfile(a.video):
            mandar_para_lixeira(a.video)
            print('[fim] vídeo do PC enviado para a Lixeira:', a.video)
