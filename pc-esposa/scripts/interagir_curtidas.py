r"""Robô "interagir curtidas" (Kevin, 20/11/2026): para cada notificação de curtida num vídeo do Kevin, no Shopee:
abre o vídeo, assiste inteiro, copia o link (sem colar), toca na foto do produto vinculado, vê o produto, volta ao
vídeo, toca na foto de novo, volta. Carrinho é opcional e vem DESLIGADO (--carrinho).

Uso (um aparelho por vez; HORST_ADB_SERIAL escolhe o celular, como nos outros robôs):
    set HORST_ADB_SERIAL=<IP_DO_CELULAR1>:5555
    python interagir_curtidas.py                 # rodada normal (limite por rodada: --max, padrão 10)
    python interagir_curtidas.py --max 2         # teste com poucos itens
    python interagir_curtidas.py --listar        # só abre as notificações e lista as curtidas (não toca em nada)
    python interagir_curtidas.py --mapear        # salva o XML + print da tela atual em curtidas\mapa\ (calibração)
Parar: criar PARAR_curtidas (todos os celulares) ou PARAR_curtidas_<celular> aqui na pasta. Termina o item atual.

Regras (pedido do Kevin):
- Nenhum toque em posição fixa: todo toque vem dos bounds do uiautomator (ponto sorteado dentro do elemento).
  Os swipes de rolagem partem do tamanho da tela (wm size) com variação.
- Uma trava por aparelho (curtidas\interagir_curtidas_<id>.lock). Não sobe se a fila, o filtro de afiliados ou o
  assistir estão usando o mesmo celular.
- Captcha: NÃO resolve nem contorna. ps.aguardar_captcha() apita e espera o Kevin (até 30 min). Login: NÃO automatiza;
  tela de login = para e avisa. Sem esconder adb / sem spoof.
- Erro desconhecido em um item: print, registra em curtidas\erros.json (a Central mostra o aviso), PULA e continua.
  3 erros seguidos = para a rodada (algo mudou na tela). Celular sumiu do adb = para.
- Ritmo modesto: pausas sorteadas entre passos (1-3,5 s) e entre itens (25-80 s, às vezes 1,5-4 min);
  limite por rodada (--max; 0 = sem limite).
- Nunca lê nem grava o link copiado (só fica na área de transferência do celular, sem colar).
"""
import argparse, datetime, hashlib, html, json, os, random, re, subprocess, sys, time, traceback

BASE = r'C:\horst\tablet'
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, 'pylibs'))
import postar_shopee as ps  # noqa: E402
import aparelho_atual as ap  # noqa: E402

PASTA = os.path.join(BASE, 'curtidas')
MAPA = os.path.join(PASTA, 'mapa')
ESTADO = os.path.join(PASTA, 'estado.json')      # chaves de notificações já feitas (por aparelho)
ERROS = os.path.join(PASTA, 'erros.json')        # itens pulados (a Central lê)
LOG = os.path.join(PASTA, 'interagir_curtidas.log')
PRINTS_ATENCAO = os.path.join(BASE, 'central', 'prints_atencao')
ID = ap.id_aparelho()
if ID in ('', 'padrao'):
    ID = 'celular1'
LOCK = os.path.join(PASTA, f'interagir_curtidas_{ID}.lock')
STATUS = os.path.join(PASTA, f'status_{ID}.json')
PARAR_GERAL = os.path.join(BASE, 'PARAR_curtidas')
PARAR_MEU = os.path.join(BASE, f'PARAR_curtidas_{ID}')

# ------------------------------------------------------------------ ajustes (calibrar com --mapear / --listar)
MAX_RODADA = 10          # padrão do --max quando nada é informado (a Central manda o valor do campo; 0 = sem limite)
MAX_ACOES = 4            # teto de cópias de link / aberturas de produto por vídeo (sorteio de 1 a 4)
# (sem parada automática por dia: o número de itens por rodada vem de --max / do campo na Central; 0 = sem limite)
VIDEO_MIN_S, VIDEO_MAX_S = 6, 90   # assistir: no mínimo / no máximo (s)
PAUSA_CURTA = (0.2, 0.7)           # s entre cliques (Kevin: estava lento)
PAUSA_PASSO = (0.3, 1.0)           # s entre passos de um item
PAUSA_ITEM = (6, 20)              # s entre itens
PAUSA_LONGA = (40, 90)            # s, 15% das vezes
ERROS_SEGUIDOS_MAX = 3
# textos (regex, sem diferenciar maiúsculas). Ajustar se o Shopee mudar o texto:
ABA_NOTIF_RE = re.compile(r'^\s*Notifica[çc][õo]es?\b', re.I)
CATEGORIA_RE = re.compile(r'(Lives,\s*V[ií]deos|Shopee\s*V[ií]deo|Intera[çc][õo]es?|Atividade\s+social|Curtidas)', re.I)
MEU_PERFIL = os.environ.get('MEU_PERFIL','@<SEU_PERFIL>')   # o vídeo só vale se o autor na tela for este (descrição "video caption user")
CURTIDA_RE = re.compile(r'(curti(u|ram)\b|gostou|gostaram|reagiu|v[ií]deo alcan[çc]ou)', re.I)   # só TEXTO de notificação (nunca content-desc: "like btn")
COMPARTILHAR_RE = re.compile(r'^(Compartilhar|Share|Enviar)\b|compartilhar|video share icon', re.I)
ANCORA_RE = re.compile(r'video product icon', re.I)   # barra do produto vinculado no vídeo (foto à esquerda)
AUTOR_RE = re.compile(r'video caption user', re.I)
COPIAR_RE = re.compile(r'Copiar\s*(o\s*)?link|Copy\s*link|^Copiar$', re.I)
PRODUTO_ID_RE = re.compile(r'product|produto|item|goods|anchor|cart', re.I)
PAGINA_PRODUTO = ('buttonItemLiked', 'labelProductPageProductName')
PAGINA_PRODUTO_TXT = re.compile(r'Vendido|Adicionar ao carrinho|Compre Agora|Avalia[çc][õo]es do produto', re.I)
LOGIN_RE = re.compile(r'Esqueceu\s+(a\s+)?senha|Fa[çc]a\s+login|Fazer\s+login|Entre\s+ou\s+cadastre|Entrar\s+com\s+(Facebook|Google|Apple)', re.I)
CARRINHO_RE = re.compile(r'^(Adicionar ao carrinho|Adicionar ao Carrinho|Add to cart)$', re.I)
COMPRAR_RE = re.compile(r'Compre Agora|Comprar agora|Finalizar|Pagamento|Pedido', re.I)
VARIACAO_RE = re.compile(r'Selecione|Escolha|Varia[çc][ãa]o|Tamanho|Cor\b|Quantidade', re.I)


# botões que o robô NUNCA toca (curtir, comentar, seguir, comprar...). Erro real de 20/11: um regex largo tocou em "like btn".
PROIBIDO_RE = re.compile(r'like btn|like vide|comment|\bSeguir\b|follow|buynow|Compre?\s+Agora|Comprar|atc button', re.I)


class Pediram(Exception):
    """PARAR_curtidas criado: termina limpo."""


class ItemPulado(Exception):
    """Erro de um item: registra, pula, continua."""


class RodadaParou(Exception):
    """Tela de login / aparelho fora do adb / erros demais: para a rodada inteira."""


# ------------------------------------------------------------------ utilitários
def log(msg):
    linha = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} [{ID}] {msg}'
    try:
        print(linha, flush=True)
    except Exception:
        pass
    try:
        os.makedirs(PASTA, exist_ok=True)
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(linha + '\n')
    except Exception:
        pass


ps.print = lambda *a, **k: log('  ' + ' '.join(str(x) for x in a).strip())


def ler_json(caminho, padrao):
    try:
        return json.load(open(caminho, encoding='utf-8'))
    except Exception:
        return padrao


def gravar_json(caminho, dados):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    tmp = caminho + '.tmp'
    json.dump(dados, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, caminho)


def pedido_parar():
    return os.path.exists(PARAR_GERAL) or os.path.exists(PARAR_MEU)


def pausa(faixa=PAUSA_PASSO, parar_ok=True):
    """Pausa sorteada, em fatias de 1 s para o PARAR_curtidas valer na hora."""
    t = random.uniform(*faixa)
    fim = time.time() + t
    while time.time() < fim:
        if parar_ok and pedido_parar():
            raise Pediram()
        time.sleep(min(1.0, max(0.05, fim - time.time())))


def status(etapa, **extra):
    d = {'estado': extra.pop('estado', 'rodando'), 'etapa': etapa, 'aparelho': ID, 'pid': os.getpid(),
         'hora': f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}'}
    d.update(extra)
    try:
        gravar_json(STATUS, d)
    except Exception:
        pass


# ------------------------------------------------------------------ trava por aparelho + conflitos
def pid_vivo(pid):
    try:
        pid = int(str(pid).strip())
    except Exception:
        return False
    if os.name == 'nt':
        import ctypes
        k = ctypes.windll.kernel32
        k.OpenProcess.restype = ctypes.c_void_p
        k.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        k.CloseHandle.argtypes = [ctypes.c_void_p]
        h = k.OpenProcess(0x1000, False, pid)
        if not h:
            return False
        try:
            code = ctypes.c_ulong()
            return bool(k.GetExitCodeProcess(h, ctypes.byref(code))) and code.value == 259
        finally:
            k.CloseHandle(h)
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def lock_vivo(caminho):
    try:
        try:
            import pid_real  # 22/11: pid reaproveitado por outro programa não é robô vivo
            return pid_real.lock_vivo(caminho)
        except ImportError:
            pass
        return pid_vivo(open(caminho).read())
    except Exception:
        return False


def aparelho_ocupado():
    """Motivo (texto) se outro robô está no mesmo celular; None se está livre."""
    if lock_vivo(os.path.join(BASE, f'rodar_fila_{ID}.lock')) or (ID == 'celular1' and lock_vivo(os.path.join(BASE, 'rodar_fila.lock'))):
        return 'a fila de postagem está usando este celular'
    for pref in ('conferir', 'candidatos'):
        if lock_vivo(os.path.join(BASE, 'afiliados', f'{pref}_{ID}.lock')):
            return f'o robô de afiliados ({pref}) está usando este celular'
    try:
        import assistir_uso
        if assistir_uso.assistir_usa(ID):
            return 'o assistir está usando este celular'
    except Exception:
        pass
    return None


# ------------------------------------------------------------------ tela: nós do uiautomator
def nos_de(xml):
    out = []
    for m in re.finditer(r'<node\b([^>]*)>', xml or ''):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        b = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', a.get('bounds', ''))
        if not b:
            continue
        out.append({'text': html.unescape(a.get('text', '')), 'desc': html.unescape(a.get('content-desc', '')),
                    'rid': a.get('resource-id', ''), 'cls': a.get('class', ''),
                    'click': a.get('clickable') == 'true', 'b': tuple(map(int, b.groups()))})
    return out


def rotulo_no(n):
    return (n['text'] or n['desc'] or '').strip()


def tamanho_tela():
    try:
        m = re.search(r'(\d+)x(\d+)', ps.sh('wm size'))
        return int(m.group(1)), int(m.group(2))
    except Exception:
        return 720, 1600


_TELA = []


def tamanho_tela_cache():
    if not _TELA:
        _TELA.append(tamanho_tela())
    return _TELA[0]


def ler_tela(tentativas=3, espera=1.5):
    """(nós, xml, textos). Tela com vídeo às vezes falha no dump: tenta de novo e devolve vazio se não vier."""
    for i in range(tentativas):
        vis, xml = ps.textos_na_tela(limite=7)
        if xml:
            return nos_de(xml), xml, vis
        time.sleep(espera * random.uniform(0.7, 1.3))
    return [], '', []


def checar_telas_especiais(vis, xml=''):
    """Captcha: espera o Kevin (não resolve). Login: para a rodada (não automatiza)."""
    if vis and ps.aguardar_captcha(vis):
        log('captcha resolvido pelo Kevin; seguindo')
    if vis and any(LOGIN_RE.search(v) for v in vis):
        try:
            from alerta import alerta_kevin
            alerta_kevin('Shopee pediu login no celular (robô de curtidas parou)')
        except Exception:
            pass
        raise RodadaParou('tela de login do Shopee — faça o login à mão; o robô não automatiza login')


def tocar_no(n, etapa, folga=0.25):
    """Toca num ponto sorteado dentro do miolo do elemento (bounds do uiautomator). Nunca coordenada fixa."""
    if PROIBIDO_RE.search(n['desc'] + ' ' + n['rid'] + ' ' + n['text']):
        raise ItemPulado(f'recusei tocar em "{rotulo_no(n)[:40]}" ({n["rid"]}): botão que o robô nunca toca')
    x1, y1, x2, y2 = n['b']
    w, h = x2 - x1, y2 - y1
    x = random.randint(x1 + int(w * folga), max(x1 + int(w * folga), x2 - int(w * folga)))
    y = random.randint(y1 + int(h * folga), max(y1 + int(h * folga), y2 - int(h * folga)))
    log(f'  toque [{etapa}] em ({x},{y}) dentro de {n["b"]} "{rotulo_no(n)[:40]}"')
    ps.sh(f'input tap {x} {y}')
    return x, y


def voltar(vezes=1):
    for _ in range(vezes):
        ps.sh('input keyevent KEYCODE_BACK')
        time.sleep(random.uniform(0.3, 0.9))


def rolar(sentido=1, curto=False):
    """Rolagem da lista pelo tamanho da tela (com variação); sentido 1 = para baixo. curto = ~15% da tela."""
    w, h = tamanho_tela()
    x = int(w * random.uniform(0.45, 0.6))
    if curto:
        meio = random.uniform(0.48, 0.55)
        y1 = int(h * (meio + 0.075 if sentido > 0 else meio - 0.075))
        y2 = int(h * (meio - 0.075 if sentido > 0 else meio + 0.075))
    else:
        y1 = int(h * (random.uniform(0.68, 0.76) if sentido > 0 else random.uniform(0.28, 0.36)))
        y2 = int(h * (random.uniform(0.28, 0.36) if sentido > 0 else random.uniform(0.68, 0.76)))
    ps.sh(f'input swipe {x} {y1} {x + random.randint(-12, 12)} {y2} {random.randint(320, 520)}')
    time.sleep(random.uniform(0.5, 1.2))


def e_pagina_produto(xml, vis):
    return any(k in (xml or '') for k in PAGINA_PRODUTO) or (
        sum(1 for v in vis if PAGINA_PRODUTO_TXT.search(v)) >= 2)


def registrar_erro(chave, texto, erro, print_nome=None):
    """Aviso para a Central (curtidas\\erros.json + print estável em central\\prints_atencao)."""
    estavel = None
    try:
        nome = f'curtidas_{datetime.datetime.now():%Y%m%d_%H%M%S}.png'
        ps.print_tela(nome)
        os.makedirs(PRINTS_ATENCAO, exist_ok=True)
        import shutil
        shutil.copy2(os.path.join(ps.PASTA, nome), os.path.join(PRINTS_ATENCAO, nome))
        estavel = nome
    except Exception as e:
        log(f'  (sem print do erro: {e})')
    lista = ler_json(ERROS, [])
    lista.append({'hora': f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}', 'aparelho': ID, 'chave': chave,
                  'notificacao': (texto or '')[:120], 'erro': str(erro)[:300], 'print_estavel': estavel})
    gravar_json(ERROS, lista[-60:])


# ------------------------------------------------------------------ navegação
def abrir_shopee():
    ps.sh(f'monkey -p {ps.PKG} -c android.intent.category.LAUNCHER 1')
    time.sleep(random.uniform(2.5, 4))


def linhas_curtida(nos):
    """Notificações de curtida visíveis: [{chave, texto, no}] onde no = o texto da notificação (miolo da linha,
    longe do avatar, que abriria o perfil). A chave junta os textos da linha (nome + horário) para não repetir."""
    achados = []
    if e_video_do_kevin(nos):   # tela de vídeo: nunca é lista de notificações
        return []
    _w, _h = tamanho_tela_cache()
    for n in nos:
        t = n['text'].strip()
        # só linhas inteiramente na área visível da lista (abaixo das abas, acima da barra inferior); as que estão
        # recortadas pelo cabeçalho existem no dump mas o toque cairia nas abas
        if n['b'][1] < _h * 0.335 or n['b'][3] > _h * 0.875:
            continue
        if t and CURTIDA_RE.search(t) and len(t) < 300:
            # linha = menor nó clicável que contém este texto
            cont = [m for m in nos if m['click'] and m['b'][0] <= n['b'][0] and m['b'][1] <= n['b'][1]
                    and m['b'][2] >= n['b'][2] and m['b'][3] >= n['b'][3]]
            linha = min(cont, key=lambda m: (m['b'][2] - m['b'][0]) * (m['b'][3] - m['b'][1])) if cont else n
            lb = linha['b']
            # chave só com o texto da mensagem: o horário na linha ("01:16") muda a cada leitura e duplicaria o item.
            # (limite conhecido: a mesma pessoa curtindo outro vídeo depois tem a mesma chave e é pulada)
            chave = hashlib.sha1(' '.join(t.split()).lower().encode('utf-8')).hexdigest()[:16]
            achados.append({'chave': chave, 'texto': t, 'no': n, 'linha': linha})
    vistos, out = set(), []
    for a in achados:
        if a['chave'] not in vistos:
            vistos.add(a['chave'])
            out.append(a)
    return out


LAYOUT = os.path.join(PASTA, 'layout_video.json')


def salvar_layout(nos):
    """Guarda os bounds (lidos pelo uiautomator) de Compartilhar e da barra do produto na tela do vídeo.
    Com o vídeo tocando o uiautomator às vezes não responde; aí o robô usa o último layout lido neste mesmo
    tamanho de tela (e avisa no log). Nunca é coordenada digitada à mão."""
    w, h = tamanho_tela()
    pegos = [n for n in nos if COMPARTILHAR_RE.search(n['desc']) or ANCORA_RE.search(n['desc'])]
    if len(pegos) >= 2:
        try:
            gravar_json(LAYOUT, {'tela': [w, h], 'nos': pegos})
        except Exception:
            pass


def layout_salvo():
    d = ler_json(LAYOUT, {})
    try:
        if d.get('tela') == list(tamanho_tela()):
            return [{**n, 'b': tuple(n['b'])} for n in d['nos']]
    except Exception:
        pass
    return []


def e_video_do_kevin(nos):
    return any(n['text'].strip() == MEU_PERFIL for n in nos) and any(COMPARTILHAR_RE.search(n['desc']) for n in nos)


def lista_visivel(nos, vis):
    if e_pagina_produto('', vis):
        return False
    cab = any(ABA_NOTIF_RE.search(rotulo_no(n)) and n['b'][1] < 350 for n in nos)
    return cab or bool(linhas_curtida(nos))


def abrir_notificacoes():
    """Shopee aberto -> lista de notificações com as curtidas à vista. Levanta ItemPulado/RodadaParou se não achar."""
    status('abrindo notificações')
    ps.acordar_e_desbloquear()
    voltar_ate_barra()
    _w, h = tamanho_tela()
    cat_tocada, rolagens_busca = False, 0
    for tentativa in range(18):
        nos, xml, vis = ler_tela(tentativas=2, espera=1.0)
        if not nos:  # vídeo/live na tela trava o uiautomator: recomeça o app do zero (regra do Kevin: fechar e abrir)
            log('  dump vazio (vídeo/live na tela?): reabrindo o Shopee')
            ps.sh(f'am force-stop {ps.PKG}')
            time.sleep(random.uniform(1.2, 2.2))
            abrir_shopee()
            continue
        checar_telas_especiais(vis, xml)
        if nos and linhas_curtida(nos):
            return nos
        # categoria (Shopee Vídeo / Interações) dentro das notificações
        if nos and any(ABA_NOTIF_RE.search(rotulo_no(n)) and n['b'][1] < 350 for n in nos):
            cat = next((n for n in nos if CATEGORIA_RE.search(rotulo_no(n)) and n['click'] or
                        (CATEGORIA_RE.search(rotulo_no(n)) and n['b'][1] > 300)), None)
            if cat and not cat_tocada:
                tocar_no(cat, 'categoria de notificação')
                cat_tocada = True
                pausa((1.5, 2.5))
                continue
            if cat_tocada:
                # categoria já aberta e nenhuma curtida na parte visível: as novas notificações empurraram as curtidas
                # para baixo (causa dos "não achei as notificações" de 20/11): rola a lista procurando
                rolagens_busca += 1
                if rolagens_busca <= 6:
                    rolar(1)
                    continue
                if rolagens_busca <= 8:
                    rolar(-1)
                    continue
        aba = [n for n in nos if ABA_NOTIF_RE.search(rotulo_no(n))]
        aba = sorted(aba, key=lambda n: -n['b'][1])  # a aba do rodapé (y maior) vem primeiro; sino do topo é o plano B
        if aba:
            tocar_no(aba[0], 'aba/sino Notificações')
            pausa((1.5, 2.5))
            continue
        voltar()
    ps.print_tela('erro_curtidas_notificacoes.png')
    raise RodadaParou('não achei as notificações de curtida (use --mapear na tela de notificações para ajustar os textos)')


def voltar_para_lista():
    """Depois de um item: BACK até a lista de notificações aparecer; se não der, reabre o app."""
    for _ in range(6):
        if progresso(ps.print_tela()) is not None:   # ainda no vídeo (dump nem adianta): só BACK
            voltar()
            continue
        nos, xml, vis = ler_tela(tentativas=1)
        if nos and lista_visivel(nos, vis):
            return nos
        voltar()
    log('  lista não voltou com BACK: reabrindo o Shopee')
    ps.sh(f'am force-stop {ps.PKG}')
    time.sleep(random.uniform(1.2, 2.2))
    return abrir_notificacoes()


# ------------------------------------------------------------------ passos de um item
def assinatura(im):
    w, h = im.size
    return im.crop((0, int(h * 0.12), w, int(h * 0.62))).convert('L').resize((36, 48))


def diferenca(a, b):
    pa, pb = a.tobytes(), b.tobytes()
    return sum(abs(x - y) for x, y in zip(pa, pb)) / max(1, len(pa))


def progresso(im):
    """Barra de progresso do vídeo (faixa azul fina logo abaixo das abas, y ~11% da tela): fração 0..1 ou None."""
    w, h = im.size
    melhor, y_melhor = 0, None
    for y in range(int(h * 0.09), int(h * 0.15), 2):
        n = sum(1 for x in range(0, w, 4) if (lambda p: p[2] > 150 and p[2] > p[0] + 40)(im.getpixel((x, y))))
        if n > melhor:
            melhor, y_melhor = n, y
    if y_melhor is None or melhor < 3:
        return None
    xs = [x for x in range(0, w, 4) if (lambda p: p[2] > 150 and p[2] > p[0] + 40)(im.getpixel((x, y_melhor)))]
    return max(xs) / w


def estimar_duracao():
    """Duração do vídeo pela velocidade da barra de progresso (leituras por ~4 s). None se a barra não aparece
    ou está parada. Conta de 0%: se a 1ª leitura já passa de 60% espera o vídeo reiniciar (máx 20 s)."""
    leituras = []
    t0 = time.time()
    while time.time() - t0 < 24:
        p = progresso(ps.print_tela())
        if p is None:
            return None
        if leituras and p < leituras[-1][1] - 0.3:   # reiniciou: recomeça a medir do zero
            leituras = []
        leituras.append((time.time(), p))
        if len(leituras) >= 3 and leituras[-1][1] - leituras[0][1] >= 0.08:
            (ta, pa), (tb, pb) = leituras[0], leituras[-1]
            return max(3.0, (tb - ta) / (pb - pa))
        time.sleep(random.uniform(0.6, 1.0))
    return None


def assistir_inteiro():
    """Assiste o vídeo inteiro. Pela barra de progresso: terminou quando ela volta ao começo (loop) ou chega a ~100%.
    Sem barra visível, cai na comparação com o 1º segundo. Teto VIDEO_MAX_S."""
    t0 = time.time()
    ref, moveu, prox_checagem = None, False, t0 + 12
    pmax = 0.0
    while True:
        dec = time.time() - t0
        if pedido_parar() and dec > VIDEO_MAX_S:
            raise Pediram()
        if dec >= VIDEO_MAX_S:
            log(f'  vídeo passou de {VIDEO_MAX_S}s: segui sem esperar a volta')
            return round(dec)
        im = ps.print_tela()
        p = progresso(im)
        if p is not None:
            pmax = max(pmax, p)
            if (pmax > 0.5 and p < pmax - 0.4 and dec > 4) or (p > 0.985 and dec > 4):
                log(f'  vídeo terminou em ~{round(dec)}s (barra {round(pmax * 100)}%)')
                return round(dec)
        sig = assinatura(im)
        if ref is None and dec >= 1.0:
            ref = sig
        elif ref is not None:
            d = diferenca(sig, ref)
            if d > 14:
                moveu = True
            elif moveu and d < 6 and dec >= VIDEO_MIN_S:
                log(f'  vídeo deu a volta em ~{round(dec)}s')
                return round(dec)
        time.sleep(random.uniform(0.6, 1.0))  # (sem dump durante o vídeo: o uiautomator não consegue com vídeo tocando)


def copiar_link(nos):
    """Compartilhar > Copiar link. Só copia; nunca cola e nunca lê a área de transferência. Aviso (não erro) se não achar."""
    comp = [n for n in nos if COMPARTILHAR_RE.search(rotulo_no(n)) and n['click']] or \
           [n for n in nos if COMPARTILHAR_RE.search(rotulo_no(n))]
    if not comp:
        log('  AVISO: botão Compartilhar não achado; link não copiado')
        return False
    tocar_no(comp[0], 'compartilhar')
    pausa((0.8, 1.8))
    nos2, xml2, vis2 = ler_tela()
    checar_telas_especiais(vis2, xml2)
    cop = [n for n in nos2 if COPIAR_RE.search(rotulo_no(n))]
    if not cop:
        log('  AVISO: "Copiar link" não achado na folha de compartilhar; fechando a folha')
        voltar()
        return False
    tocar_no(sorted(cop, key=lambda n: -n['b'][1])[0], 'copiar link')
    pausa((0.6, 1.2))
    nos3, xml3, vis3 = ler_tela(tentativas=1)
    if nos3 and any(COPIAR_RE.search(rotulo_no(n)) for n in nos3):  # folha ainda aberta
        voltar()
    return True


def achar_foto_produto(nos):
    """Miniatura do produto vinculado ao vídeo: imagem clicável pequena e (quase) quadrada, de preferência com
    id/descrição de produto, na metade de baixo da tela. Devolve o nó ou None."""
    for n in nos:  # tela real (20/11): barra "video product icon"; a foto é o trecho da esquerda
        if ANCORA_RE.search(n['desc']) and n['click']:
            x1, y1, x2, y2 = n['b']
            return {**n, 'b': (x1, y1, min(x2, x1 + 80), y2)}
    _w, h = tamanho_tela()
    cand = []
    for n in nos:
        x1, y1, x2, y2 = n['b']
        w_, h_ = x2 - x1, y2 - y1
        if not (50 <= w_ <= 420 and 50 <= h_ <= 420):
            continue
        quadrado = 0.7 <= w_ / max(1, h_) <= 1.4
        imagem = 'Image' in n['cls'] or bool(re.search(r'image|img|cover|thumb|photo', n['rid'], re.I))
        pontos = (3 if PRODUTO_ID_RE.search(n['rid'] + ' ' + n['desc']) else 0) + (2 if imagem else 0) \
            + (1 if quadrado else 0) + (1 if n['click'] else 0) + (1 if y1 > h * 0.5 else 0)
        if pontos >= 5 and (imagem or n['click']):
            cand.append((pontos, y1, n))
    if not cand:
        return None
    cand.sort(key=lambda c: (-c[0], -c[1]))
    return cand[0][2]


FOLHA_CACHE = []   # bounds da foto do 1º item da folha "Ver Produtos" (lidos por dump nesta execução)


def abrir_produto_pela_foto(rotulo_passo, nos_cache):
    """Acha a foto nos bounds do vídeo -> toca -> espera a página do produto. Devolve (nos, xml, vis) da página.
    Com vídeo tocando o uiautomator não responde; por isso os bounds vêm do dump feito quando o vídeo abriu
    (a tela do vídeo tem sempre o mesmo layout), e só se esse cache faltar tenta um dump novo."""
    nos = nos_cache
    if not nos:
        nos, xml, vis = ler_tela(tentativas=2, espera=1.5)
        if not nos:
            raise ItemPulado(f'{rotulo_passo}: dump da tela do vídeo falhou (uiautomator sem resposta)')
        checar_telas_especiais(vis, xml)
    foto = achar_foto_produto(nos)
    if not foto:
        ps.print_tela('erro_curtidas_sem_foto.png')
        raise ItemPulado(f'{rotulo_passo}: foto do produto vinculado não achada na tela do vídeo')
    tocar_no(foto, rotulo_passo + ' (barra do produto)')
    # Caminho rápido (Kevin: menos parado entre cliques): depois da 1ª abertura confirmada por dump, a folha tem o mesmo
    # layout; usa os bounds lidos naquela vez, sem dumps (3-4 s cada). Folha aberta = a barra do vídeo some da tela.
    if FOLHA_CACHE:
        pausa((0.5, 0.9), parar_ok=False)
        if progresso(ps.print_tela()) is None:
            tocar_no(FOLHA_CACHE[0], rotulo_passo + ' (foto do 1º item, bounds já lidos)')
            pausa((1.3, 2.0), parar_ok=False)
            return [], '', []
        log('  (caminho rápido: a folha não abriu; sigo pelo caminho com dump)')
    # Tela real (20/11): a barra do produto abre a folha "Ver Produtos (N)"; a foto do 1º item da folha abre o produto.
    fim_folha = time.time() + 12
    folha = None
    while time.time() < fim_folha and folha is None:
        pausa((0.7, 1.3))
        nf, xf, vf = ler_tela(tentativas=1)
        if vf:
            checar_telas_especiais(vf, xf)
        if nf and e_pagina_produto(xf, vf):
            return nf, xf, vf   # (abriu direto a página do produto)
        itens = [n for n in nf if 'list item panel' in n['rid'] or 'list item panel' in n['desc']]
        if itens:
            folha = min(itens, key=lambda n: n['b'][1])
    if folha is None:
        log(f'  AVISO: folha "Ver Produtos" não apareceu ({rotulo_passo}); sigo e volto')
        return [], '', []
    x1, y1, x2, y2 = folha['b']
    foto_item = {**folha, 'b': (x1, y1, min(x2, x1 + 190), y2)}
    FOLHA_CACHE[:] = [foto_item]
    tocar_no(foto_item, rotulo_passo + ' (foto do 1º item)')
    fim = time.time() + 14
    while time.time() < fim:
        pausa((0.7, 1.3))
        n2, x2, v2 = ler_tela(tentativas=1)
        if v2:
            checar_telas_especiais(v2, x2)
        if v2 and e_pagina_produto(x2, v2):
            return n2, x2, v2
    log(f'  AVISO: página do produto não confirmou depois do toque ({rotulo_passo}); sigo e volto')
    return [], '', []


def voltar_ao_video():
    """BACK até a tela do vídeo (fecha página do produto e a folha 'Ver Produtos'). Com o vídeo tocando o dump falha:
    dump vazio logo depois de um BACK = estamos no vídeo."""
    for _ in range(4):
        voltar()
        pausa((0.6, 1.0))
        if progresso(ps.print_tela()) is not None:   # barra do vídeo à vista = estamos no vídeo (rápido, sem dump)
            return
        nos, xml, vis = ler_tela(tentativas=1)
        if not nos or e_video_do_kevin(nos):
            return
        if lista_visivel(nos, vis):
            raise ItemPulado('voltei demais: caí na lista de notificações em vez do vídeo')
    log('  AVISO: não confirmei a volta ao vídeo')


def carrinho(nos, vis):
    """OPCIONAL (--carrinho). Toca em 'Adicionar ao carrinho'; se abrir seleção de variação, fecha (não escolhe).
    Nunca toca em Compre Agora/pagamento."""
    alvo = next((n for n in nos if CARRINHO_RE.match(rotulo_no(n))), None)
    if not alvo:
        log('  carrinho: botão não achado; pulei')
        return
    tocar_no(alvo, 'adicionar ao carrinho')
    pausa((0.8, 1.8))
    n2, x2, v2 = ler_tela(tentativas=2)
    if any(COMPRAR_RE.search(v) for v in v2) and not e_pagina_produto(x2, v2):
        log('  carrinho: caí numa tela de compra; voltando (nada confirmado)')
        voltar()
    elif any(VARIACAO_RE.search(v) for v in v2) and any(CARRINHO_RE.match(v) or 'Confirmar' in v for v in v2):
        log('  carrinho: pede variação; fechei sem escolher')
        voltar()


def processar(item, usar_carrinho):
    """Um item completo. Levanta ItemPulado em erro de tela conhecido; qualquer outro erro o chamador também pula."""
    # 1. abrir o vídeo
    FOLHA_CACHE.clear()   # a folha de um produto novo pode ter outro tamanho: 1ª abertura de cada item é por dump
    status('abrindo vídeo', texto=item['texto'][:60])
    # a lista pode ter rolado/recolhido o cabeçalho desde o dump: relê e acha a linha de novo antes de tocar
    nos0, xml0, vis0 = ler_tela()
    checar_telas_especiais(vis0, xml0)
    atual = next((a for a in linhas_curtida(nos0) if a['chave'] == item['chave']), None)
    if not atual:
        raise ItemPulado('a linha da notificação sumiu da tela antes do toque')
    tocar_no(atual['no'], 'notificação de curtida')
    # o toque passa pela aba Live e Vídeo (às vezes mostra uma live antes): só vale quando o autor na tela é o Kevin
    fim = time.time() + 22
    nos = []
    while time.time() < fim:
        pausa((0.7, 1.3))
        nos, xml, vis = ler_tela(tentativas=1)
        if vis:
            checar_telas_especiais(vis, xml)
        if nos and e_video_do_kevin(nos):
            break
        if nos and e_pagina_produto(xml, vis):
            voltar()
            raise ItemPulado('a notificação abriu uma página de produto, não um vídeo')
    else:
        # Kevin (20/11): sem fallback de layout salvo. uiautomator falhou = pula o item, avisa e continua.
        raise ItemPulado(f'o vídeo de {MEU_PERFIL} não foi lido pelo uiautomator em ~20 s depois do toque (item pulado)')
    acoes_no_video(nos, usar_carrinho, item['texto'][:60])


def acoes_no_video(nos, usar_carrinho, texto):
    """Passos 2-4 com o vídeo do Kevin já aberto e lido (nos = dump da tela do vídeo): assistir (medindo a duração),
    copiar link 1-3x e abrir o produto 1-3x durante a reprodução, esperar o fim. Nunca curte, comenta nem segue."""
    status('assistindo o vídeo', texto=texto)
    t_video = time.time()
    nos_video = nos  # bounds lidos quando o vídeo abriu (com o vídeo tocando o uiautomator não responde)
    n_copias, n_produto = random.randint(1, MAX_ACOES), random.randint(1, MAX_ACOES)   # Kevin: 1 a 4 vezes cada (teto 4)
    log(f'  plano do item: copiar link {n_copias}x, abrir produto {n_produto}x')
    # Kevin: começar LOGO por Compartilhar > Copiar link (a 1ª cópia vem antes de medir a duração)
    marca_t = {}
    status(f'copiando o link (1/{n_copias})')
    copiar_link(nos_video)
    marca_t['1a copia'] = time.time() - t_video
    pausa(PAUSA_CURTA)
    dur = estimar_duracao()   # lê a barra por ~4 s; None se não achar a barra
    sequencial = dur is None
    # teto de tempo por item: duração do vídeo + 25 s (sem barra: 30 s + 25 s); passou, pula o resto e segue
    limite_item = t_video + (dur if dur else 30) + 25
    if sequencial:
        log('  AVISO: barra de progresso não vista; assisto depois das ações')
    else:
        log(f'  vídeo dura ~{round(dur)}s; as ações acontecem com ele rodando e só termino depois dele acabar')
    for i in range(1, n_copias):
        if time.time() > limite_item:
            log('  teto de tempo do item: pulando as cópias que faltam')
            break
        status(f'copiando o link ({i + 1}/{n_copias})')
        copiar_link(nos_video)
        pausa(PAUSA_CURTA)
    # 4. foto do produto -> produto -> volta ao vídeo, n vezes
    for i in range(n_produto):
        if time.time() > limite_item:
            log('  teto de tempo do item: pulando as aberturas de produto que faltam')
            break
        status(f'abrindo o produto ({i + 1}/{n_produto})')
        n_prod, x_prod, v_prod = abrir_produto_pela_foto(f'foto do produto ({i + 1}/{n_produto})', nos_video)
        pausa(PAUSA_CURTA)
        if usar_carrinho and n_prod and i == 0:
            carrinho(n_prod, v_prod)
            pausa(PAUSA_CURTA)
        voltar_ao_video()
        pausa(PAUSA_CURTA)
    if not sequencial:  # requisito do Kevin: assistir o vídeo inteiro (as ações rodaram durante a reprodução)
        falta = dur + 1.5 - (time.time() - t_video)
        if falta > 0:
            log(f'  faltam ~{round(falta)}s para o vídeo acabar; esperando')
            pausa((falta, falta + 0.5), parar_ok=False)
        seg = round(time.time() - t_video)
    else:
        seg = assistir_inteiro()
    log(f'  item ok (vídeo ~{seg}s, total {round(time.time() - t_video)}s)')


# ------------------------------------------------------------------ rodada
def hoje_str():
    return f'{datetime.date.today():%Y-%m-%d}'


def arquivar_erros():
    """Cada rodada começa com a lista de avisos limpa (os antigos vão para curtidas\\erros_arquivo\\): a Central mostrava
    avisos de testes velhos somados (20 em 20/11) junto com a rodada atual."""
    try:
        if ler_json(ERROS, []):
            pasta = os.path.join(PASTA, 'erros_arquivo')
            os.makedirs(pasta, exist_ok=True)
            os.replace(ERROS, os.path.join(pasta, f'erros_{datetime.datetime.now():%Y%m%d_%H%M%S}.json'))
    except Exception as e:
        log(f'  (não arquivei os avisos antigos: {e})')


def garantir_pronto():
    """Antes de cada item: tela acesa e destravada, Shopee em primeiro plano, bateria ok, ninguém mais no celular.
    Devolve True se precisou reabrir o Shopee (quem chama recomeça a lista). Levanta RodadaParou com motivo claro."""
    motivo = aparelho_ocupado()
    if motivo:
        raise RodadaParou(f'parei: {motivo} (o celular é de outro robô agora)')
    try:
        ps.acordar_e_desbloquear()
    except ps.Parou as e:
        raise RodadaParou(f'parei: {e}')
    try:
        bat = ps.sh('dumpsys battery')
        nivel = int(re.search(r'level:\s*(\d+)', bat).group(1))
        carregando = re.search(r'status:\s*(\d+)', bat) and re.search(r'status:\s*(\d+)', bat).group(1) in ('2', '5')
        if nivel < 10 and not carregando:
            raise RodadaParou(f'parei: bateria em {nivel}% e sem carregar')
    except RodadaParou:
        raise
    except Exception:
        pass
    foco = ps.sh('dumpsys window | grep mCurrentFocus')
    if ps.PKG not in foco:
        log('  Shopee fora do primeiro plano: reabrindo')
        abrir_shopee()
        return True
    return False


def rodada(args):
    est = ler_json(ESTADO, {})
    meus = est.setdefault(ID, {'feitos': {}, 'dia': hoje_str(), 'hoje': 0})
    if meus.get('dia') != hoje_str():
        meus['dia'], meus['hoje'] = hoje_str(), 0
    feitos = meus['feitos']
    limite = args.max
    feitos_rodada = erros_rodada = erros_seguidos = 0
    nos = abrir_notificacoes()
    if args.listar:
        for a in linhas_curtida(nos):
            log(f'  curtida: {a["texto"][:100]} (chave {a["chave"]}){" [já feita]" if a["chave"] in feitos else ""}')
        return 0, 0
    rolagens = 0
    while feitos_rodada + erros_rodada < limite:
        if pedido_parar():
            log('PARAR_curtidas encontrado — parando')
            break
        novas = [a for a in linhas_curtida(nos) if a['chave'] not in feitos]
        if not novas:
            if rolagens >= 4:
                log('sem curtidas novas à vista')
                break
            rolar(1)
            rolagens += 1
            nos, xml, vis = ler_tela()
            checar_telas_especiais(vis, xml)
            continue
        item = novas[0]
        log(f'item {feitos_rodada + erros_rodada + 1}/{limite}: "{item["texto"][:90]}"')
        try:
            if garantir_pronto():   # app tinha saído do primeiro plano / tela apagou: recomeça a lista
                nos = abrir_notificacoes()
                novas = [a for a in linhas_curtida(nos) if a['chave'] not in feitos]
                if not novas:
                    log('sem curtidas novas depois de reabrir')
                    break
                item = novas[0]
            processar(item, args.carrinho)
            feitos[item['chave']] = f'{datetime.datetime.now():%Y-%m-%d %H:%M}'
            meus['hoje'] += 1
            feitos_rodada += 1
            erros_seguidos = 0
        except Pediram:
            raise
        except (RodadaParou, ps.Desconectado):
            raise
        except Exception as e:  # erro desconhecido ou ItemPulado: pula, registra, continua
            erros_rodada += 1
            erros_seguidos += 1
            feitos[item['chave']] = f'pulado {datetime.datetime.now():%Y-%m-%d %H:%M}'  # não insiste no mesmo item
            if not isinstance(e, ItemPulado):
                log('  erro inesperado:\n' + traceback.format_exc())
            log(f'  PULEI o item: {e}')
            registrar_erro(item['chave'], item['texto'], e)
            if erros_seguidos >= ERROS_SEGUIDOS_MAX:
                raise RodadaParou(f'parei depois de {erros_seguidos} itens seguidos com erro (último: {str(e)[:120]}). '
                                  f'Confira a tela do celular; o robô não gera mais avisos nesta rodada.')
        meus['feitos'] = dict(sorted(feitos.items(), key=lambda kv: kv[1])[-500:])
        gravar_json(ESTADO, est)
        status('entre itens', feitos=feitos_rodada, erros=erros_rodada, hoje=meus['hoje'])
        if feitos_rodada + erros_rodada >= limite:
            break
        pausa(PAUSA_LONGA if random.random() < 0.15 else PAUSA_ITEM)
        try:
            if erros_seguidos >= 2:   # 2 erros seguidos: reabre o Shopee e recomeça a lista antes de tentar de novo
                log('  2 erros seguidos: reabrindo o Shopee e recomeçando a lista')
                ps.sh(f'am force-stop {ps.PKG}')
                time.sleep(random.uniform(0.5, 1.2))
                nos = abrir_notificacoes()
            else:
                nos = voltar_para_lista()
        except ItemPulado as e:
            raise RodadaParou(str(e))
    return feitos_rodada, erros_rodada


# ------------------------------------------------------------------ fonte 2: Eu > Criadores & Afiliados > Conversões
FEED_MAX_VIDEOS = 8           # vídeos do feed "Vídeo em Destaque" olhados à procura de @<SEU_PERFIL>
OCR_PS1 = os.path.join(BASE, 'ocr_tela.ps1')


def visivel(n, topo=0.095, base=0.875):
    _w, h = tamanho_tela_cache()
    return n['b'][1] >= h * topo and n['b'][3] <= h * base


def tocar_texto(regex, etapa, rolagens=0, so_visivel=True):
    """Acha pelo uiautomator um nó com esse texto (inteiro na tela) e toca. Rola até `rolagens` vezes se não achar."""
    rx = re.compile(regex, re.I)
    for i in range(rolagens + 1):
        nos, xml, vis = ler_tela()
        checar_telas_especiais(vis, xml)
        c = [n for n in nos if rx.search(rotulo_no(n)) and (visivel(n) or not so_visivel)]
        if c:
            tocar_no(c[0], etapa)
            return nos
        if i < rolagens:
            # achado mas cortado pelo topo: rola na direção contrária; senão segue rolando para baixo
            fora = [n for n in nos if rx.search(rotulo_no(n)) and not visivel(n)]
            cortado_no_topo = bool(fora) and fora[0]['b'][1] < tamanho_tela_cache()[1] * 0.095
            rolar(-1, curto=True) if cortado_no_topo else rolar(1, curto=bool(fora))
    raise ItemPulado(f'não achei "{regex}" na tela ({etapa})')


def ocr_faixa(caixa=(0.0, 0.60, 0.80, 0.86)):
    """OCR (leitura, sem tocar) de uma faixa da tela: onde o feed mostra "@autor". Devolve as linhas lidas."""
    im = ps.print_tela()
    w, h = im.size
    recorte = im.crop((int(w * caixa[0]), int(h * caixa[1]), int(w * caixa[2]), int(h * caixa[3])))
    recorte = recorte.resize((recorte.size[0] * 2, recorte.size[1] * 2))
    caminho = os.path.join(ps.PASTA, 'ocr_autor_curtidas.png')
    recorte.save(caminho)
    try:
        r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', OCR_PS1, caminho],
                           capture_output=True, timeout=60, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        return [l.strip() for l in r.stdout.decode('utf-8', 'ignore').splitlines() if l.strip()]
    except Exception:
        return []


def e_autor_kevin(linhas):
    return any(re.search(re.escape(MEU_PERFIL.lstrip('@')).replace('\\ ','\\s*'), l, re.I) for l in linhas)


def voltar_a_conversoes():
    for _ in range(8):
        nos, xml, vis = ler_tela(tentativas=1)
        if nos and any('Minhas Convers' in rotulo_no(n) for n in nos):
            return
        voltar()
        pausa((0.4, 0.9))
    raise RodadaParou('não consegui voltar para Minhas Conversões')


def abrir_conversoes():
    status('abrindo Conversões')
    ps.acordar_e_desbloquear()
    for t in range(3):   # logo depois de abrir o app o dump às vezes falha (vídeo/animação): reabre e tenta de novo
        ps.sh(f'am force-stop {ps.PKG}')
        time.sleep(random.uniform(0.5, 1.2))
        abrir_shopee()
        try:
            tocar_texto(r'^Eu$', 'aba Eu', so_visivel=False)
            break
        except ItemPulado:
            if t == 2:
                raise
            log('  aba Eu não lida; reabrindo o Shopee')
    pausa((1.5, 2.5))
    tocar_texto(r'^Criadores\s*&\s*Afiliados$', 'Criadores & Afiliados', rolagens=3)
    pausa((2.0, 3.0))
    tocar_texto(r'^Convers[ãa]o$', 'aba Conversão', so_visivel=False)
    pausa((1.5, 2.5))
    tocar_texto(r'^Conclu[ií]do$', 'filtro Concluído')
    pausa((1.5, 2.5))


def produtos_concluidos(nos):
    """Nomes de produto das linhas de pedido (texto longo, inteiro na tela, fora dos rótulos fixos)."""
    ign = re.compile(r'^(ID do Pedido|Pedido realizado|Comiss|Ver mais|Minhas Convers|Todos|N[aã]o pago|Pendente|Conclu|Cancelado|Filtro|\d+ Produtos)', re.I)
    out = []
    for n in nos:
        t = n['text'].strip()
        if len(t) >= 25 and not ign.search(t) and visivel(n):
            out.append(n)
    return out


def procurar_video_do_kevin():
    """No feed "Vídeo em Destaque": olha até FEED_MAX_VIDEOS vídeos, lendo "@autor" por OCR. Nos de outros só desliza."""
    for i in range(FEED_MAX_VIDEOS):
        time.sleep(random.uniform(1.2, 2.0))
        linhas = ocr_faixa()
        log(f'  feed {i + 1}/{FEED_MAX_VIDEOS}: autor lido = {" | ".join(linhas)[:70]!r}')
        if e_autor_kevin(linhas):
            return True
        rolar(1)   # só desliza para o próximo vídeo; nenhuma ação em vídeo de outra pessoa
        pausa((0.5, 1.2))
    return False


def norm_titulo(s):
    return re.sub(r'[^a-z0-9]+', ' ', (s or '').lower().replace('…', ' ').replace('...', ' ')).strip()


def mesmo_produto(titulo_card, nome_pedido):
    """Card do perfil vem truncado com '…': casa se o começo do card (normalizado, mín. 14 letras) é o começo do pedido."""
    a, b = norm_titulo(titulo_card), norm_titulo(nome_pedido)
    a = a[:max(14, min(len(a), 30))]
    return len(a) >= 14 and b.startswith(a[:min(len(a), 24)])


def cards_do_perfil(nos):
    """[(titulo, chip_videos_ou_None, bounds)] dos cards 'product item card' visíveis."""
    out = []
    for c in nos:
        if 'product item card' in c['rid'] or 'product item card' in c['desc']:
            x1, y1, x2, y2 = c['b']
            dentro = [n for n in nos if n['b'][0] >= x1 and n['b'][1] >= y1 and n['b'][2] <= x2 and n['b'][3] <= y2]
            tit = next((n['text'] for n in dentro if len(n['text']) >= 15 and not n['text'].startswith('R$')), '')
            chip = next((n for n in dentro if re.match(r'^\d+ v[ií]deos?$', n['text'].strip(), re.I)), None)
            out.append((tit, chip, c['b']))
    return out


def video_no_perfil(nome_pedido):
    """Eu do Kevin (Live e Vídeo > ícone do perfil > aba Produtos): acha o card do produto do pedido, toca em 'N vídeos'
    e devolve o dump da tela do vídeo do Kevin (@<SEU_PERFIL>). None se o produto não está no perfil / sem vídeo."""
    status('procurando o vídeo no perfil do Kevin')
    voltar_ate_barra()
    tocar_texto(r'^Live e V[ií]deo$', 'aba Live e Vídeo', so_visivel=False)
    pausa((1.5, 2.5))
    for t in range(4):   # com o feed tocando o dump falha: tenta de novo
        try:
            tocar_texto(r'me page icon', 'ícone do perfil', so_visivel=False)
            break
        except ItemPulado:
            if t == 3:
                raise
            pausa((1.0, 2.0))
    pausa((2.0, 3.0))
    tocar_texto(r'^Produtos$', 'aba Produtos do perfil', so_visivel=False)
    pausa((1.5, 2.5))
    achado = None
    for passo in range(2):
        for rol in range(8 if passo else 1):
            nos, xml, vis = ler_tela()
            for tit, chip, b in cards_do_perfil(nos):
                if mesmo_produto(tit, nome_pedido) and chip is not None:
                    achado = chip
                    break
            if achado:
                break
            if passo:
                rolar(1)
        if achado:
            break
        if passo == 0:   # só 2 cards na aba: abre "Ver Todos os Produtos" e procura lá
            try:
                tocar_texto(r'^Ver Todos os Produtos$', 'Ver Todos os Produtos', rolagens=1)
            except ItemPulado:
                return None
            pausa((2.0, 3.0))
    if not achado:
        log('  produto não está nos produtos do perfil do Kevin')
        return None
    tocar_no(achado, 'N vídeos do produto (perfil)')
    fim = time.time() + 20
    while time.time() < fim:
        pausa((0.6, 1.0))
        nos, xml, vis = ler_tela(tentativas=1)
        if nos and e_video_do_kevin(nos):
            return nos
    raise ItemPulado('o vídeo do Kevin não abriu pelo "N vídeos" do perfil')


def processar_produto(no_produto, usar_carrinho):
    nos_v = video_no_perfil(no_produto['text'])
    if nos_v:
        acoes_no_video(nos_v, usar_carrinho, no_produto['text'][:60])
        return
    if not FEED_LIGADO:   # decisão do Kevin: sem dump não há ação; o feed fica desligado (use --feed para ligar)
        raise ItemPulado('produto não está no perfil do Kevin (feed "Vídeos em Destaque" desligado)')
    # fallback: feed "Vídeos em Destaque" da página do produto (só se o perfil não achou)
    log('  perfil não achou: tentando o feed "Vídeos em Destaque" (fallback)')
    abrir_conversoes()
    nos0, _x, _v = ler_tela()
    reencontro = [n for n in produtos_concluidos(nos0) if n['text'].strip()[:25] == no_produto['text'].strip()[:25]]
    if not reencontro:
        raise ItemPulado('não reencontrei o produto na lista de Conversões para o fallback')
    no_produto = reencontro[0]
    tocar_no(no_produto, 'produto do pedido (lista)')
    pausa((1.5, 2.5))
    nos, xml, vis = ler_tela()
    nome = no_produto['text'][:20]
    cand = [n for n in nos if n['text'].strip().startswith(nome) and visivel(n)]
    if not cand:
        raise ItemPulado('detalhe do pedido não mostrou o produto para abrir')
    tocar_no(cand[0], 'produto (detalhe do pedido)')
    pausa((2.0, 3.0))
    tocar_texto(r'^V[ií]deos em Destaque$', 'Vídeos em Destaque', rolagens=6)
    pausa((2.0, 3.0))
    if not procurar_video_do_kevin():
        raise ItemPulado(f'@<SEU_PERFIL> não apareceu nos {FEED_MAX_VIDEOS} primeiros vídeos do feed (produto pulado)')
    # vídeo do Kevin na tela: lê o layout (dump logo que possível) e faz as mesmas ações indiretas
    nos_v, xml_v, vis_v = ler_tela(tentativas=3, espera=1.0)
    if not nos_v:
        raise ItemPulado('uiautomator não leu a tela do vídeo do Kevin no feed (produto pulado)')
    acoes_no_video(nos_v, usar_carrinho, no_produto['text'][:60])


def rodada_conversoes(args):
    est = ler_json(ESTADO, {})
    meus = est.setdefault(ID, {'feitos': {}, 'dia': hoje_str(), 'hoje': 0})
    feitos = meus['feitos']
    abrir_conversoes()
    feitos_rodada = erros_rodada = erros_seguidos = 0
    rolagens = 0
    while feitos_rodada + erros_rodada < args.max:
        if pedido_parar():
            log('PARAR_curtidas encontrado — parando')
            break
        nos, xml, vis = ler_tela()
        checar_telas_especiais(vis, xml)
        novos = [n for n in produtos_concluidos(nos)
                 if 'conv:' + hashlib.sha1(n['text'].strip().lower().encode('utf-8')).hexdigest()[:16] not in feitos]
        if not novos:
            if rolagens >= 4:
                log('sem produtos concluídos novos à vista')
                break
            rolar(1)
            rolagens += 1
            continue
        n = novos[0]
        chave = 'conv:' + hashlib.sha1(n['text'].strip().lower().encode('utf-8')).hexdigest()[:16]
        log(f'produto {feitos_rodada + erros_rodada + 1}/{args.max}: "{n["text"][:70]}"')
        try:
            garantir_pronto()
            processar_produto(n, args.carrinho)
            feitos[chave] = f'{datetime.datetime.now():%Y-%m-%d %H:%M}'
            feitos_rodada += 1
            erros_seguidos = 0
        except (Pediram, RodadaParou, ps.Desconectado):
            raise
        except Exception as e:
            erros_rodada += 1
            erros_seguidos += 1
            feitos[chave] = f'pulado {datetime.datetime.now():%Y-%m-%d %H:%M}'
            if not isinstance(e, ItemPulado):
                log('  erro inesperado:\n' + traceback.format_exc())
            log(f'  PULEI o produto: {e}')
            registrar_erro(chave, 'Conversões: ' + n['text'], e)
            if erros_seguidos >= ERROS_SEGUIDOS_MAX:
                raise RodadaParou(f'{erros_seguidos} produtos seguidos com erro — parei a rodada')
        meus['feitos'] = dict(sorted(feitos.items(), key=lambda kv: kv[1])[-500:])
        gravar_json(ESTADO, est)
        if feitos_rodada + erros_rodada >= args.max:
            break
        pausa(PAUSA_LONGA if random.random() < 0.15 else PAUSA_ITEM)
        try:
            abrir_conversoes()   # recomeça do zero: o perfil/feed deixam o app em outra tela
        except ItemPulado as e:
            raise RodadaParou(str(e))
    return feitos_rodada, erros_rodada


FEED_LIGADO = False


# ------------------------------------------------------------------ fonte: MEUS VÍDEOS pelo perfil (aba Vídeos) + modo misto
def abrir_perfil_videos():
    """Live e Vídeo > ícone do perfil > aba Vídeos (a grade com os vídeos do Kevin; NÃO a aba Produtos)."""
    voltar_ate_barra()
    tocar_texto(r'^Live e V[ií]deo$', 'aba Live e Vídeo', so_visivel=False)
    pausa((1.0, 2.0))
    for t in range(4):   # com o feed tocando o dump falha: tenta de novo
        try:
            tocar_texto(r'me page icon', 'ícone do perfil', so_visivel=False)
            break
        except ItemPulado:
            if t == 3:
                raise
            pausa((0.6, 1.2))
    pausa((1.5, 2.5))
    try:
        tocar_texto(r'^V[ií]deos$', 'aba Vídeos do perfil', so_visivel=False)
        pausa((0.8, 1.5))
    except ItemPulado:
        pass   # a aba Vídeos já vem selecionada


def abrir_video_do_perfil(meus):
    """Abre um vídeo da grade do perfil (revezando entre os visíveis: o próximo índice fica no estado) e devolve o dump
    da tela do vídeo. Só abre vídeo do Kevin (@<SEU_PERFIL>) lido pelo uiautomator; senão ItemPulado."""
    status('abrindo um vídeo do meu perfil')
    abrir_perfil_videos()
    nos, xml, vis = ler_tela()
    checar_telas_especiais(vis, xml)
    grade = sorted([n for n in nos if re.match(r'^click video \d+$', n['desc'].strip())
                    and visivel(n, base=0.93)], key=lambda n: (n['b'][1], n['b'][0]))
    if not grade:
        raise ItemPulado('a aba Vídeos do perfil não mostrou vídeos (grade vazia ou tela diferente)')
    idx = int(meus.get('perfil_idx', 0)) % len(grade)
    meus['perfil_idx'] = idx + 1
    tocar_no(grade[idx], f'vídeo {idx + 1} da grade do perfil')
    fim = time.time() + 20
    while time.time() < fim:
        pausa((0.6, 1.0))
        nv, xv, vv = ler_tela(tentativas=1)
        if vv:
            checar_telas_especiais(vv, xv)
        if nv and e_video_do_kevin(nv):
            return nv
    raise ItemPulado('o vídeo do perfil não abriu / não foi lido pelo uiautomator em ~20 s (item pulado)')


def proxima_notificacao(feitos):
    """Abre as notificações e devolve a próxima curtida/aviso ainda não feito (rola até 5x). None se não há mais."""
    nos = abrir_notificacoes()
    for i in range(6):
        novas = [a for a in linhas_curtida(nos) if a['chave'] not in feitos]
        if novas:
            return novas[0]
        if i == 5:
            break
        rolar(1)
        nos, xml, vis = ler_tela()
        checar_telas_especiais(vis, xml)
    return None


def rodada_mista(args, modo):
    """modo 'misto': alterna notificações e vídeos do perfil (uma fonte por item). 'notificacoes' / 'perfil': só uma.
    Mesmo teto de 4 e mesmas ações indiretas nos dois (copiar link, produto, terminar o vídeo). Sem limite diário;
    o total vem de --max (0 = sem limite)."""
    est = ler_json(ESTADO, {})
    meus = est.setdefault(ID, {'feitos': {}, 'dia': hoje_str(), 'hoje': 0})
    if meus.get('dia') != hoje_str():
        meus['dia'], meus['hoje'] = hoje_str(), 0
    feitos = meus['feitos']
    fontes = {'misto': ['notificacao', 'perfil'], 'notificacoes': ['notificacao'], 'perfil': ['perfil']}[modo]
    sem_novo, turno = set(), 0
    feitos_rodada = erros_rodada = erros_seguidos = 0
    log(f'modo {modo}: fontes {" + ".join(fontes)}')
    while feitos_rodada + erros_rodada < args.max:
        if pedido_parar():
            log('PARAR_curtidas encontrado — parando')
            break
        ativas = [f for f in fontes if f not in sem_novo]
        if not ativas:
            log('nenhuma fonte tem itens novos; encerrando a rodada')
            break
        fonte = ativas[turno % len(ativas)]
        turno += 1
        rotulo_item = fonte
        chave = None
        try:
            garantir_pronto()
            if fonte == 'notificacao':
                item = proxima_notificacao(feitos)
                if item is None:
                    log('sem notificações novas à vista')
                    sem_novo.add('notificacao')
                    continue
                chave, rotulo_item = item['chave'], item['texto']
                log(f'item {feitos_rodada + erros_rodada + 1} [notificação]: "{item["texto"][:80]}"')
                processar(item, args.carrinho)
                feitos[chave] = f'{datetime.datetime.now():%Y-%m-%d %H:%M}'
            else:
                log(f'item {feitos_rodada + erros_rodada + 1} [vídeo do perfil]')
                nos_v = abrir_video_do_perfil(meus)
                acoes_no_video(nos_v, args.carrinho, 'vídeo do perfil')
            meus['hoje'] += 1
            feitos_rodada += 1
            erros_seguidos = 0
        except (Pediram, RodadaParou, ps.Desconectado):
            raise
        except Exception as e:
            erros_rodada += 1
            erros_seguidos += 1
            if chave:
                feitos[chave] = f'pulado {datetime.datetime.now():%Y-%m-%d %H:%M}'
            if not isinstance(e, ItemPulado):
                log('  erro inesperado:\n' + traceback.format_exc())
            log(f'  PULEI o item [{fonte}]: {e}')
            registrar_erro(chave or 'perfil', f'[{fonte}] {rotulo_item}', e)
            if erros_seguidos >= ERROS_SEGUIDOS_MAX:
                raise RodadaParou(f'parei depois de {erros_seguidos} itens seguidos com erro (último: {str(e)[:120]}). '
                                  f'Confira a tela do celular; o robô não gera mais avisos nesta rodada.')
            if erros_seguidos >= 2:
                log('  2 erros seguidos: reabrindo o Shopee e recomeçando')
                ps.sh(f'am force-stop {ps.PKG}')
                time.sleep(random.uniform(1.0, 2.0))
        meus['feitos'] = dict(sorted(feitos.items(), key=lambda kv: kv[1])[-500:])
        gravar_json(ESTADO, est)
        status('entre itens', feitos=feitos_rodada, erros=erros_rodada, hoje=meus['hoje'])
        if feitos_rodada + erros_rodada >= args.max:
            break
        pausa(PAUSA_LONGA if random.random() < 0.15 else PAUSA_ITEM)
    return feitos_rodada, erros_rodada


def voltar_ate_barra(max_backs=5):
    """Sai do vídeo/perfil com BACK até a barra inferior do Shopee (abas Início...Eu) aparecer, sem reabrir o app
    (reabrir custava ~25 s por produto). App fora do primeiro plano: abre. Dump vazio = vídeo tocando: só BACK."""
    foco = ps.sh('dumpsys window | grep mCurrentFocus')
    if ps.PKG not in foco:
        abrir_shopee()
    for _ in range(max_backs + 1):
        nos, xml, vis = ler_tela(tentativas=1, espera=0.2)
        if nos and any('tab_bar_button' in n['rid'] or 'tab_bar_button' in n['desc'] or n['rid'].endswith('title') for n in nos):
            return
        voltar()
    log('  barra inferior não apareceu com BACK; reabrindo o Shopee')
    ps.sh(f'am force-stop {ps.PKG}')
    time.sleep(random.uniform(0.5, 1.2))
    abrir_shopee()


def nomes_conversoes(maximo_rolagens=3):
    """Nomes de produto dos pedidos Concluídos (só leitura), para dar prioridade no perfil."""
    nomes = []
    abrir_conversoes()
    for i in range(maximo_rolagens + 1):
        nos, xml, vis = ler_tela()
        for n in produtos_concluidos(nos):
            t = n['text'].strip()
            if t not in nomes:
                nomes.append(t)
        if i < maximo_rolagens:
            rolar(1)
    log(f'  {len(nomes)} produto(s) de pedidos Concluídos lidos para priorizar')
    return nomes


def listar_cards_perfil():
    """Perfil do Kevin > Produtos > Ver Todos: [{titulo, chip}] dos cards com 'N vídeos'."""
    voltar_ate_barra()
    tocar_texto(r'^Live e V[ií]deo$', 'aba Live e Vídeo', so_visivel=False)
    pausa((1.5, 2.5))
    for t in range(4):
        try:
            tocar_texto(r'me page icon', 'ícone do perfil', so_visivel=False)
            break
        except ItemPulado:
            if t == 3:
                raise
            pausa((1.0, 2.0))
    pausa((2.0, 3.0))
    tocar_texto(r'^Produtos$', 'aba Produtos do perfil', so_visivel=False)
    pausa((1.5, 2.5))
    try:
        tocar_texto(r'^Ver Todos os Produtos$', 'Ver Todos os Produtos', rolagens=1)
        pausa((2.0, 3.0))
    except ItemPulado:
        pass
    vistos, lista = set(), []
    for rol in range(10):
        nos, xml, vis = ler_tela()
        novos = 0
        for tit, chip, b in cards_do_perfil(nos):
            k = norm_titulo(tit)[:40]
            if tit and chip is not None and k not in vistos:
                vistos.add(k)
                lista.append({'titulo': tit, 'chave': 'perfil:' + hashlib.sha1(k.encode('utf-8')).hexdigest()[:16]})
                novos += 1
        if rol >= 1 and not novos:
            break
        rolar(1)
    log(f'  {len(lista)} produto(s) com vídeo no perfil do Kevin')
    return lista


def rodada_perfil(args):
    est = ler_json(ESTADO, {})
    meus = est.setdefault(ID, {'feitos': {}, 'dia': hoje_str(), 'hoje': 0})
    feitos = meus['feitos']
    prioridade = []
    if not args.sem_prioridade:
        try:
            prioridade = nomes_conversoes()
        except (Pediram, RodadaParou, ps.Desconectado):
            raise
        except Exception as e:
            log(f'  (sem prioridade de Conversões: {e})')
    cards = listar_cards_perfil()
    cards.sort(key=lambda c: 0 if any(mesmo_produto(c['titulo'], p) for p in prioridade) else 1)
    for c in cards:
        c['prioritario'] = any(mesmo_produto(c['titulo'], p) for p in prioridade)
    log('  ordem: ' + ' | '.join(('★ ' if c['prioritario'] else '') + c['titulo'][:28] for c in cards[:8]))
    feitos_rodada = erros_rodada = erros_seguidos = 0
    for c in cards:
        if feitos_rodada + erros_rodada >= args.max:
            break
        if c['chave'] in feitos:
            continue
        if pedido_parar():
            log('PARAR_curtidas encontrado — parando')
            break
        log(f'produto {feitos_rodada + erros_rodada + 1}/{args.max}: "{c["titulo"][:70]}"{" (Conversões)" if c["prioritario"] else ""}')
        try:
            garantir_pronto()
            nos_v = video_no_perfil(c['titulo'])
            if not nos_v:
                raise ItemPulado('card do perfil não reencontrado')
            acoes_no_video(nos_v, args.carrinho, c['titulo'][:60])
            feitos[c['chave']] = f'{datetime.datetime.now():%Y-%m-%d %H:%M}'
            feitos_rodada += 1
            erros_seguidos = 0
        except (Pediram, RodadaParou, ps.Desconectado):
            raise
        except Exception as e:
            erros_rodada += 1
            erros_seguidos += 1
            feitos[c['chave']] = f'pulado {datetime.datetime.now():%Y-%m-%d %H:%M}'
            if not isinstance(e, ItemPulado):
                log('  erro inesperado:\n' + traceback.format_exc())
            log(f'  PULEI o produto: {e}')
            registrar_erro(c['chave'], 'Perfil: ' + c['titulo'], e)
            if erros_seguidos >= ERROS_SEGUIDOS_MAX:
                raise RodadaParou(f'{erros_seguidos} produtos seguidos com erro — parei a rodada')
        meus['feitos'] = dict(sorted(feitos.items(), key=lambda kv: kv[1])[-500:])
        gravar_json(ESTADO, est)
        pausa(PAUSA_LONGA if random.random() < 0.15 else PAUSA_ITEM)
    return feitos_rodada, erros_rodada


def mapear():
    os.makedirs(MAPA, exist_ok=True)
    base = os.path.join(MAPA, f'{datetime.datetime.now():%Y%m%d_%H%M%S}')
    vis, xml = ps.textos_na_tela(limite=20)
    open(base + '.xml', 'w', encoding='utf-8').write(xml or '')
    ps.print_tela(f'curtidas_mapa_{os.path.basename(base)}.png')
    log(f'mapa salvo: {base}.xml e gravacao\\curtidas_mapa_{os.path.basename(base)}.png ({len(vis)} textos)')
    for t in vis[:60]:
        log('   ' + t[:100])


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--max', type=int, default=MAX_RODADA, help='itens por rodada (0 = sem limite)')
    a.add_argument('--modo', choices=('misto', 'notificacoes', 'perfil', 'produtos'), default='misto', help='misto = notificações e meus vídeos do perfil, alternando (padrão); produtos = antigo fluxo pela aba Produtos')
    a.add_argument('--carrinho', action='store_true', help='tenta adicionar ao carrinho (desligado por padrão)')
    a.add_argument('--listar', action='store_true', help='só lista as curtidas (não toca nelas)')
    a.add_argument('--mapear', action='store_true', help='salva XML + print da tela atual')
    a.add_argument('--conversoes', action='store_true', help='fonte: Eu > Criadores & Afiliados > Conversões > Concluído (--max = produtos)')
    a.add_argument('--perfil', action='store_true', help='(antigo) = --modo produtos')
    a.add_argument('--sem-prioridade', action='store_true', help='com --perfil: não lê Conversões')
    a.add_argument('--feed', action='store_true', help='liga o fallback do feed Vídeos em Destaque (desligado por padrão)')
    args = a.parse_args()
    os.makedirs(PASTA, exist_ok=True)
    if args.mapear:
        ps.conectar()
        mapear()
        return 0
    if lock_vivo(LOCK):
        log('já está rodando neste celular')
        return 0
    motivo = aparelho_ocupado()
    if motivo:
        log(f'não subo: {motivo}')
        return 1
    open(LOCK, 'w').write(str(os.getpid()))
    codigo = 0
    try:
        log(f'interagir_curtidas no {ID} (máx {args.max}/rodada{", carrinho LIGADO" if args.carrinho else ""})')
        ps.conectar()
        arquivar_erros()
        global FEED_LIGADO
        FEED_LIGADO = args.feed
        if args.max <= 0:
            args.max = 10 ** 9
            log('  sem limite de itens (--max 0): só PARAR_curtidas, a fila acabar ou erros seguidos param a rodada')
        modo = 'produtos' if args.perfil else args.modo
        if args.conversoes:
            f, e = rodada_conversoes(args)
        elif modo == 'produtos':
            f, e = rodada_perfil(args)
        elif args.listar:
            f, e = rodada(args)
        else:
            f, e = rodada_mista(args, modo)
        log(f'rodada terminou: {f} item(ns) feitos, {e} pulado(s)')
        status('parado', estado='parado', feitos=f, erros=e)
    except Pediram:
        log('parado pelo PARAR_curtidas')
        status('parado (PARAR)', estado='parado')
    except RodadaParou as e:
        log(f'RODADA PARADA: {e}')
        registrar_erro('rodada', 'rodada parada', e)
        status(f'parou: {e}', estado='erro')
        codigo = 2
    except ps.Desconectado as e:
        log(f'celular fora do adb: {e}')
        status('celular fora do adb', estado='erro')
        codigo = 3
    except Exception as e:
        log('ERRO NÃO TRATADO:\n' + traceback.format_exc())
        registrar_erro('rodada', 'erro geral', e)
        status(f'erro: {e}', estado='erro')
        codigo = 4
    finally:
        try:
            if open(LOCK).read().strip() == str(os.getpid()):
                os.remove(LOCK)
        except Exception:
            pass
    return codigo


if __name__ == '__main__':
    sys.exit(main())
