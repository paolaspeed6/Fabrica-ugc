r"""Confere produtos Shopee no tablet e conta os vídeos de afiliados (filtro automático).

Uso:
  python conferir_afiliados.py LINKS.txt        (um link por linha)
  python conferir_afiliados.py LINKS.json       (lista de {"itemId": ..., "link": ...})
  python conferir_afiliados.py --teste          (3 produtos já postados da fila.json)

Fluxo por produto (o mesmo que o Kevin faz à mão):
  link -> página do produto (se abrir a "leve", toca no nome) -> Compartilhar (canto sup. dir.)
  -> faixa "Comissão de Afiliados x%, Estim. R$y" -> página de afiliado (nº de afiliados, vendas)
  -> seção "Aprenda Com Outros Criadores" > lista "Vídeos de Criadores" -> conta as miniaturas
  (rolando até o fim ou até 20). Sem a seção = 0 vídeos.

Navegação: conferida por cor de pixel (screencap). Leitura dos números: OCR do Windows
(afiliados\ocr.ps1) — o uiautomator neste tablet falha muito nessas telas.

Saída: afiliados\conferidos.csv, afiliados\status.json (card da Central), prints em afiliados\prints.
Em dúvida num produto: grava erro + print e segue para o próximo.
Captcha: pausa, bipe e espera o Kevin resolver (nunca resolve sozinho). Tela de login: para tudo.
Não favorita, não curte, não posta nada. Não roda junto com a fila de postagem (mesmo tablet).
Para parar entre um produto e outro: crie afiliados\PARAR.
"""
import argparse, csv, datetime, json, os, re, shutil, subprocess, sys, time, urllib.error, urllib.request

BASE = r'C:\horst\tablet'
sys.path.insert(0, BASE)
import postar_shopee as ps  # noqa: E402
import captcha_log  # noqa: E402

PASTA = os.path.join(BASE, 'afiliados')
PRINTS = os.path.join(PASTA, 'prints')
CSV = os.path.join(PASTA, 'conferidos.csv')
import aparelho_atual as ap  # noqa: E402
ID_APARELHO = ap.id_aparelho()  # um robô por aparelho (HORST_ADB_SERIAL)
STATUS = os.path.join(PASTA, f'status_{ID_APARELHO}.json')
STATUS_GERAL = os.path.join(PASTA, 'status.json')  # o card atual da Central lê este
LOG = os.path.join(PASTA, 'conferir_afiliados.log')
LOCK = os.path.join(PASTA, f'conferir_{ID_APARELHO}.lock')
PARAR = os.path.join(PASTA, 'PARAR')
OCR_PS1 = os.path.join(PASTA, 'ocr.ps1')
TMP_OCR = os.path.join(PASTA, f'_ocr_{ID_APARELHO}.png')  # 1 por aparelho: compartilhado os robôs liam a tela um do outro
LOCK_FILA = os.path.join(BASE, 'rodar_fila.lock')
CARDS = os.path.join(BASE, 'central', 'cards.json')
CAMPOS = ['data', 'itemId', 'link', 'nome', 'vendas', 'afiliados', 'videos', 'comissao_rs',
          'comissao_pct', 'print', 'decisao', 'motivo', 'segundos', 'prioridade', 'v7', 'primeira_vez', 'nossos_videos', 'views_max', 'views_mediana', 'views_total', 'v3', 'aparelho', 'zero_videos']  # novas colunas sempre no fim
# Régua (Kevin 10/11): limites em afiliados\regua_filtro.json, fácil de mudar
try:
    REGUA = json.load(open(os.path.join(PASTA, 'regua_filtro.json'), encoding='utf-8-sig'))
except Exception:
    REGUA = {}
# Perfis (Kevin 21/11): perfis_filtro.json; escolhe por HORST_PERFIL (ligar_perfil.cmd) ou pelo perfil_ativo
try:
    _PERFIS = json.load(open(os.path.join(PASTA, 'perfis_filtro.json'), encoding='utf-8-sig'))
except Exception:
    _PERFIS = {}
PERFIL_NOME = os.environ.get('HORST_PERFIL') or _PERFIS.get('perfil_ativo') or 'normal'
REGUA.update((_PERFIS.get('perfis') or {}).get(PERFIL_NOME) or {})
META_APROV = int(REGUA.get('meta_aprovados', 0) or 0)  # 0 = sem limite
EXIGIR_V7 = bool(REGUA.get('exigir_venda_semana', False))
MAX_APROV = int(REGUA.get('max_videos_aprovado', 4))
MAX_PRIO = int(REGUA.get('max_videos_prioridade', 1))
VIEWS_VENCEDOR = int(REGUA.get('views_video_vencedor', 10000))
VENDAS_MIN = int(REGUA.get('vendas_min', 10))
VALIDA_DESDE = str(REGUA.get('valida_desde', '2026-11-10 12:30'))
MAX_VIDEOS = MAX_APROV  # para de contar no (limite + 1)º vídeo: já é descarte, não precisa contar o resto
COMISSAO_MIN = float(REGUA.get('comissao_min', 20.0))  # R$ por venda (Kevin 05/11)
COMISSAO_MIN_TAXA_ALTA = float(REGUA.get('comissao_min_taxa_alta', 15.0))  # Kevin 10/11: taxa alta + venda recente
TAXA_ALTA_PCT = float(REGUA.get('taxa_alta_pct', 10))  # "taxa alta" = comissão > 10% do preço


def comissao_minima(pct, v7):
    """Mínimo em R$ (régua de 10/11): R$ 15 se taxa > 10% e venda na semana (v7 > 0), senão R$ 20."""
    if pct is not None and pct > TAXA_ALTA_PCT and v7 is not None and v7 > 0:
        return COMISSAO_MIN_TAXA_ALTA
    return COMISSAO_MIN
INTERVALO_PRODUTOS = 0  # s entre o INÍCIO de um produto e o próximo (Kevin 05/11: ritmo normal; 180 = lento);
                          # varia ±25% ao acaso. 0 = sem espera. Também por env HORST_INTERVALO.

ps.PASTA = PRINTS  # prints do postar_shopee (se usados) vão para a pasta daqui

# ---------------- perfis de tela (coordenadas por aparelho) ----------------
# tablet CM8800Ultra 800x1280 (mapeado 05/11) · POCO 25078PC3EG 720x1600 (mapeado 05/11 12:15)
PERFIS = {
    'tablet': dict(
        produto_verde=(150, 1170), produto_laranja=(450, 1165), produto_dir=(780, 1200),
        foto=(40, 780, 110, 740), voltar=(18, 44, 60, 82), leve=((300, 957), (500, 957)), leve_nome=(300, 858),
        painel_branco=(400, 770), painel_creme=(600, 870), painel_zap=(70, 955), faixa=(430, 848), faixa_y=(780, 900),
        af_branco=(200, 1135), af_laranja=(450, 1140), af_dir=(780, 1200), af_nao=(380, 1140),
        lista_branco=(400, 60), lista_vermelho=(767, 52), compartilhar=(650, 70),
        topo=90, fundo=1215, ver_x=(150, 320), topo_ver=(228, 250), chevron_x=762, secao_y=(80, 1100),
        sw_af='400 1000 400 450 900', sw_af1='400 1000 400 350 900', sw_lista='400 1100 400 350 1200',
        sw_topo='400 350 400 1100 300'),
    'poco720': dict(
        produto_verde=(150, 1458), produto_laranja=(540, 1440), produto_dir=(700, 1490),
        foto=(40, 680, 170, 700), voltar=(30, 64, 115, 145), leve=None, leve_nome=(300, 1190),
        painel_branco=(360, 790), painel_creme=(600, 980), painel_zap=(105, 1117), faixa=(380, 955), faixa_y=(900, 1010),
        af_branco=(200, 1425), af_laranja=(400, 1430), af_dir=(700, 1490), af_nao=(330, 1430),
        lista_branco=(400, 118), lista_vermelho=(660, 108), compartilhar=(496, 130),
        topo=170, fundo=1515, ver_x=(220, 420), topo_ver=(372, 392), chevron_x=687, secao_y=(150, 1400),
        sw_af='360 1200 360 550 900', sw_af1='360 1200 360 450 900', sw_lista='360 1250 360 650 1500',
        sw_topo='360 450 360 1350 300', espera_scroll=1.0, espera_fim=1.2),
}
P = dict(PERFIS['tablet'])


def escolher_perfil():
    """Escolhe o perfil pelo tamanho do screencap (chamado no início do main)."""
    w, h = ps.print_tela().size
    nome = 'poco720' if (w, h) == (720, 1600) else 'tablet'
    P.clear()
    P.update(PERFIS[nome])
    global TOPO, FUNDO
    TOPO, FUNDO = P['topo'], P['fundo']
    return nome, (w, h)



_print_original = ps.print_tela


def _print_robusto(nome=None):
    """screencap às vezes vem cortado/vazio quando o cabo USB oscila: tenta de novo e, se o
    tablet sumiu do adb, espera ele voltar (até 20 min) em vez de derrubar o lote."""
    for tentativa in range(4):
        try:
            return _print_original(nome)
        except Exception:
            time.sleep(1.5)
            if 'device' not in ps.adb('get-state', timeout=15):
                status('alerta', 'tablet desconectou do USB — confira o cabo; o robô espera')
                log('  tablet sumiu do adb: esperando voltar (até 20 min)')
                fim = time.time() + 20 * 60
                while time.time() < fim and 'device' not in ps.adb('get-state', timeout=15):
                    try:  # tenta religar o adb Wi-Fi (IP do aparelhos.json) a cada ~30 s
                        _, ip = ps.enderecos_tablet()
                        if ip:
                            subprocess.run([ps.ADB, 'connect', ip], capture_output=True, timeout=20,
                                           creationflags=ps.SEM_JANELA)
                            if ps._estado(ip) == 'device':
                                ps._usar(ip)
                                break
                    except Exception:
                        pass
                    time.sleep(30)  # sem som: desconexão o robô resolve sozinho (aviso só no card)
                if 'device' not in ps.adb('get-state', timeout=15):
                    raise PararTudo('tablet desconectado por mais de 20 min')
                log('  tablet voltou')
                status('rodando')
    return _print_original(nome)


ps.print_tela = _print_robusto


class Pular(Exception):
    """Problema neste produto: registra e segue para o próximo."""


class FalhaCarregar(Pular):
    """Tela "Este produto falhou ao carregar" (ou parecida): recarrega 1 vez; se persistir, registra erro
    'falha_carregar' (volta para recheck depois), pula SEM reabrir o app 3x e segue (Kevin 10/11)."""


FALHA_CARREGAR_RE = re.compile(r'falhou ao carregar|falha ao carregar|erro ao carregar|n[ãa]o foi poss[ií]vel carregar|'
                               r'problema ao carregar|por favor,? recarregue|'
                               r'produto n[ãa]o encontrado|produto indispon[ií]vel|n[ãa]o est[áa] mais dispon', re.I)


def fechar_dialogo_falha():
    """Toca no botão do diálogo "falhou ao carregar" pelo BOUNDS lido do dump (Cancelar > Voltar > Fechar > OK),
    nunca por coordenada fixa. Se a tela não sair em ~3 s, fecha e reabre o app (sem login, sem limpar dados).
    Devolve True se saiu do diálogo."""
    try:
        _vis, xml = ps.textos_na_tela(6)
        for nome in ('Cancelar', 'Voltar', 'Fechar', 'OK'):
            pos = ps.achar(nome, xml or '')
            if pos:
                log(f'  diálogo de falha: tocando em "{nome}" {pos}')
                ps.sh(f'input tap {pos[0]} {pos[1]}')
                break
        fim = time.time() + 3
        while time.time() < fim:
            time.sleep(1)
            if not falha_de_carregamento():
                return True
    except Exception as e:
        log(f'  (fechar diálogo de falha: {e!r})')
    log('  diálogo de falha não saiu em 3 s: fechando e reabrindo a Shopee')
    recuperar_app()
    return not falha_de_carregamento()


def falha_de_carregamento():
    """Texto da tela de falha de carregamento, ou ''."""
    try:
        vis, _x = ps.textos_na_tela(6)
        return next((v for v in vis if FALHA_CARREGAR_RE.search(v)), '')
    except Exception:
        return ''


class PararTudo(Exception):
    pass


class Esgotado(Pular):
    """Kevin 20/11: produto "não listado", "indisponível" ou "esgotado" -> decisão 'esgotado' na hora
    (não é aprovado nem erro, não volta para a fila), sem reabrir o app."""


class TelaFalha(Pular):
    """A tela mostrou "falhou ao carregar" enquanto o robô esperava (detecta na hora, sem esperar 58 s)."""


class ErroCarregar(Pular):
    """Kevin 21/11: falhou ao carregar 2x seguidas -> decisão 'erro_carregar' e vai para o próximo."""


def tocar_tentar_novamente():
    """Toca em "Tentar novamente" (ou "Recarregar") pelo bounds lido na tela. True se achou o botão."""
    try:
        _vis, xml = ps.textos_na_tela(6)
        for nome in ('Tentar novamente', 'Tentar de novo', 'Recarregar', 'RECARREGAR', 'Recarregue'):
            pos = ps.achar(nome, xml or '') or ps.achar_parcial(nome, xml or '')
            if pos:
                log(f'  tocando em "{nome}" {pos}')
                for _ in range(2):  # o 1º toque depois de tela parada às vezes se perde
                    ps.sh(f'input tap {pos[0]} {pos[1]}')
                    time.sleep(1.5)
                    if not falha_de_carregamento():
                        break
                return True
    except Exception as e:
        log(f'  (tentar novamente: {e!r})')
    return False


ESGOTADO_RE = re.compile(r'n[ãa]o\s+(?:est[áa]\s+)?(?:mais\s+)?listad|indispon[ií]vel|esgotad', re.I)


# ---------------- utilidades ----------------

def log(msg):
    linha = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}'
    print(linha, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(linha + '\n')


LOTE = {'feito': None, 'total': None}  # progresso do lote atual (para o card)


def status(state, aviso=None):
    """Card da Central: rodando | parado | alerta (captcha/erro). Números vêm do CSV (status_card)."""
    state = {'ok': 'parado', 'erro': 'alerta'}.get(state, state)
    try:
        sys.path.insert(0, PASTA)
        import status_card
        status_card.escrever(state, LOTE['feito'], LOTE['total'], aviso)
    except Exception as e:  # o card nunca derruba o robô
        json.dump({'state': state, 'detail': aviso or f'(status: {e})'}, open(STATUS, 'w', encoding='utf-8'),
                  ensure_ascii=False)


def bipe(motivo='precisa de você no tablet'):
    """'Precisa de você' (só captcha, tela com PIN, login da Shopee): som próprio sons\\atencao.wav
    via alerta.alerta_kevin (máx. 1x/45 s; se a Central estiver aberta, ela mesma toca)."""
    try:
        from alerta import alerta_kevin
        alerta_kevin(motivo)
    except Exception:
        pass


def vivo(pid):
    try:
        os.kill(pid, 0)
    except Exception:
        return False
    try:  # 22/11: existe mas não é um robô (pid reaproveitado, ex.: audiodg.exe) = não está vivo
        import pid_real
        if not pid_real.e_robo(pid):
            return False
    except ImportError:
        pass
    try:  # 13/11: PID reaproveitado por outro programa (chrome) não é robô vivo
        s = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'], capture_output=True, text=True, timeout=15,
                           creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
        return any(str(pid) in l and 'python' in l.lower() for l in s.splitlines())
    except Exception:
        return True


def num(s):
    """'67' -> 67, '1,2mil' -> 1200, '10mil+' -> 10000."""
    if not s:
        return None
    s = s.strip().lower().replace('+', '').replace(' ', '')
    m = re.fullmatch(r'(\d[\d.,]*)(mil|k)?', s)
    if not m:
        return None
    n, mil = m.groups()
    if mil:
        return int(float(n.replace('.', '').replace(',', '.')) * 1000)
    return int(n.replace('.', '').replace(',', ''))


def reais(s):
    m = re.search(r'R\$\s*(\d[\d.]*,\d{2})', s or '')
    return float(m[1].replace('.', '').replace(',', '.')) if m else None


def item_id(link):
    """shopid.itemid do link curto (segue só o 1º redirecionamento, sem abrir a página)."""
    padrao = r'(?:-i\.|/product/|/)(\d{6,})[./](\d{6,})'
    m = re.search(padrao, link)
    if m:
        return f'{m[1]}.{m[2]}'

    class SemSeguir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    try:
        urllib.request.build_opener(SemSeguir).open(link, timeout=15)
    except urllib.error.HTTPError as e:
        m = re.search(padrao, e.headers.get('Location', ''))
        if m:
            return f'{m[1]}.{m[2]}'
    except Exception:
        pass
    return ''


# ---------------- OCR (Windows.Media.Ocr) ----------------

def ocr(im=None):
    """Palavras da tela: lista de (texto, x, y, w, h, linha). ~1 s."""
    (im or ps.print_tela()).save(TMP_OCR)
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', OCR_PS1, TMP_OCR],
                       capture_output=True, timeout=60, creationflags=ps.SEM_JANELA)
    out = []
    for l in r.stdout.decode('utf-8', 'ignore').splitlines():
        p = l.split('\t')
        if len(p) == 6:
            out.append((p[0], *map(int, p[1:])))
    return out


def linhas(pal):
    """[(texto da linha, y)] em ordem de cima para baixo."""
    por = {}
    for t, x, y, w, h, n in pal:
        por.setdefault(n, []).append((x, y, t))
    res = [(' '.join(t for _, _, t in sorted(v)), min(y for _, y, _ in v)) for v in por.values()]
    return sorted(res, key=lambda a: a[1])


def antes_de(pal, palavra):
    """Número escrito logo à esquerda da palavra, na mesma altura (ex.: '97' de '97 Afiliados')."""
    alvo = next((p for p in pal if p[0].startswith(palavra)), None)
    if not alvo:  # OCR às vezes cola o número na palavra ("298Afiliados")
        colado = next((p for p in pal if re.fullmatch(r'[\d.,]+(mil|k)?\+?' + palavra + r'.*', p[0], re.I)), None)
        return num(re.match(r'[\d.,]+(?:mil|k)?\+?', colado[0], re.I)[0]) if colado else None
    _, ax, ay = alvo[:3]
    # palavras numéricas encostadas à esquerda (da direita para a esquerda, folga < 16 px)
    viz = sorted((p for p in pal if abs(p[2] - ay) <= 8 and p[1] < ax), key=lambda p: -p[1])
    partes, borda = [], ax
    for t, x, y, w, h, _ in viz:
        if borda - (x + w) > 16 or not re.fullmatch(r'[\d.,]+(mil|k)?\+?', t.lower()):
            break
        partes.insert(0, t)
        borda = x
    return num(''.join(partes))


# ---------------- telas (cor de pixel; 800x1280) ----------------

def cor(im, x, y):
    return im.getpixel((x, y))


def pagina_completa(im):
    """Página completa: barra de baixo verde (chat/carrinho) à esquerda e laranja à direita.
    Loja 'Oficial': barra branca à esquerda e botão vermelho escuro (208,1,27) à direita."""
    r, g, b = cor(im, *P['produto_verde'])
    normal = 20 < r < 80 and 140 < g < 200 and 130 < b < 190 and ps.e_laranja(cor(im, *P['produto_laranja']))
    r2, g2, b2 = cor(im, *P['produto_laranja'])
    oficial = (ps.e_branco(cor(im, *P['produto_verde'])) and r2 > 170 and g2 < 40 and b2 < 60
               and cor(im, *P['produto_dir']) == cor(im, *P['produto_laranja']))
    return normal or oficial


def foto_carregada(im):
    """A foto do produto (y 100-740) já apareceu: enquanto carrega, essa área fica toda branca
    e o toque no nome é ignorado."""
    x0, x1, y0, y1 = P['foto']
    pts = [(x, y) for x in range(x0, x1, 40) for y in range(y0, y1, 40)]
    return sum(1 for p in pts if min(cor(im, *p)) < 225) > len(pts) * 0.08


def pagina_leve(im):
    """Página leve: botão laranja largo "Compre Agora" (y~957), sem a barra verde embaixo."""
    if not P['leve']:
        return False  # no celular o link abre direto a página completa
    return ps.e_laranja(cor(im, *P['leve'][0])) and ps.e_laranja(cor(im, *P['leve'][1])) and not pagina_completa(im)


def icones_carregados(im):
    """Seta de voltar (canto sup. esq.) desenhada em branco: só aparece quando a página carregou
    (no esqueleto de carregamento é um círculo cinza liso). Vale para produto branco em fundo branco."""
    x0, x1, y0, y1 = P['voltar']
    return sum(1 for x in range(x0, x1) for y in range(y0, y1) if min(cor(im, x, y)) > 245) >= 40


def leve_pronta(im):
    return pagina_leve(im) and (foto_carregada(im) or icones_carregados(im))


def painel_compartilhar(im):
    """Painel 'Compartilhe Links para Ganhar Comissão': título branco (y~782), faixa creme
    da comissão (y~848) e o ícone verde do WhatsApp (70,955)."""
    r, g, b = cor(im, *P['painel_creme'])
    creme = r > 245 and g > 240 and 225 < b < 250 and r - b > 5
    zx, zy = P['painel_zap']
    zap = any(ps.e_verde(cor(im, zx + dx, zy + dy)) for dx in (-15, 0, 15) for dy in (-15, 0, 15))
    return ps.e_branco(cor(im, *P['painel_branco'])) and creme and zap


def pagina_afiliado(im):
    """Página de afiliado: barra de baixo branca (Chat/Favoritar) + laranja 'Compartilhe para Ganhar'."""
    return (ps.e_branco(cor(im, *P['af_branco'])) and ps.e_laranja(cor(im, *P['af_laranja']))
            and ps.e_laranja(cor(im, *P['af_dir'])) and not ps.e_laranja(cor(im, *P['af_nao'])))


def lista_videos(im):
    """'Vídeos de Criadores': cabeçalho branco, ícone vermelho (+) no canto, miniaturas à esquerda."""
    return ps.e_branco(cor(im, *P['lista_branco'])) and ps.e_vermelho(cor(im, *P['lista_vermelho'])) and len(botoes_ver(im)) >= 1


def esperar(teste, limite):
    """Espera a tela. Se demorar, confere a cada ~8 s se é captcha (aí espera o Kevin e
    dá mais tempo depois que ele resolver)."""
    fim = time.time() + limite
    prox_ocr = time.time() + 8
    assin, desde, esq_desde = None, time.time(), None
    while time.time() < fim:
        im = ps.print_tela()
        if teste(im):
            return im
        if time.time() > prox_ocr:
            pal = ocr(im)
            if captcha_log.e_captcha([t for t, *_ in pal]) and checar_bloqueios(pal):
                fim = time.time() + limite  # pausa proposital (captcha): não conta como travamento
                assin, desde, esq_desde = None, time.time(), None
            elif any(k in ' '.join(t for t, *_ in pal).lower() for k in (
                    'conta restrita', 'conta suspensa', 'conta bloqueada', 'atividade incomum',
                    'atividade suspeita', 'acesso restrito', 'temporariamente bloquead')):
                ps.print_tela(f'bloqueio_{datetime.datetime.now():%m%d_%H%M%S}.png')
                raise PararTudo('Shopee mostrou BLOQUEIO/CONTA RESTRITA (não é captcha) — parei tudo')
            elif ESGOTADO_RE.search(' '.join(t for t, *_ in pal)):  # antes era lido como "sem internet"
                raise Esgotado(ESGOTADO_RE.search(' '.join(t for t, *_ in pal))[0])
            elif FALHA_CARREGAR_RE.search(' '.join(t for t, *_ in pal)):
                raise TelaFalha(FALHA_CARREGAR_RE.search(' '.join(t for t, *_ in pal))[0])
            elif any(t.lower() == 'unavailable' for t, *_ in pal):
                raise Pular('Shopee sem internet (Network Unavailable)')
            prox_ocr = time.time() + 8
        # vigia de travamento (Kevin 05/11): tela igual por 60 s ou esqueleto cinza por 45 s
        a = im.convert('L').resize((40, 64)).tobytes()
        if assin is None or sum(abs(x - y) for x, y in zip(a, assin)) / len(a) > 2:
            assin, desde = a, time.time()
        elif time.time() - desde > 60:
            raise Pular('tela parada por 60 s (travou)')
        if esqueleto(im):
            esq_desde = esq_desde or time.time()
            if time.time() - esq_desde > 45:
                raise Pular('Shopee presa no carregamento (esqueleto cinza) por 45 s')
        else:
            esq_desde = None
        time.sleep(0.5)
    return None


def esqueleto(im):
    """Tela de carregamento da Shopee: quase toda cinza-clara lisa (com o 'presente' ou a sacola S)."""
    w, h = im.size
    pts = [cor(im, x, y) for x in range(40, w - 20, 60) for y in range(120, h - 80, 60)]
    claros = sum(1 for c in pts if 236 <= min(c) and max(c) - min(c) < 8)
    return claros > len(pts) * 0.85


def tocar_e_esperar(pos, teste, origem, limite, tentativas=3):
    """Toque com conferência: toca e espera a tela nova. Só toca de novo se ainda estiver
    na tela de origem (evita tocar em outra coisa se a tela mudou)."""
    for n in range(tentativas):
        ps.sh(f'input tap {pos[0]} {pos[1]}')
        im = esperar(teste, limite)
        if im:
            return im
        atual = ps.print_tela()
        if not origem(atual):
            checar_bloqueios()
            return esperar(teste, 5)
    return None


def dormir_ate_resolver(inicio, nome, suspender):
    """Captcha sem resposta à noite: põe o PC em espera; ao acordar espera o Kevin resolver
    (sem limite de tempo), reconectando o adb se cair, e continua do mesmo produto."""
    hora = datetime.datetime.now()
    status('alerta', f'CAPTCHA sem resposta: PC em espera desde {hora:%H:%M}. Resolva o captcha no celular '
                     'que o robô continua sozinho')
    log(f'CAPTCHA sem resposta em 15 min: colocando o PC em espera ({hora:%H:%M})')
    res = suspender.suspender()
    acordou = datetime.datetime.now()
    log(f'PC voltou da espera ({res}) às {acordou:%H:%M}: esperando o captcha ser resolvido')
    status('alerta', f'CAPTCHA: PC acordou às {acordou:%H:%M} — resolva o captcha no celular que o robô continua')
    ultimo_bipe = 0
    while True:
        if os.path.exists(PARAR):
            raise PararTudo('PARAR durante a espera do captcha')
        try:
            textos = [t for t, *_ in ocr()]
        except Exception as e:
            log(f'  adb sem resposta depois da espera ({e}); reconectando')
            if ':' in (ps.SERIAL or ''):
                subprocess.run([ps.ADB, 'connect', ps.SERIAL], capture_output=True, timeout=20)
            time.sleep(30)
            continue
        if not captcha_log.e_captcha(textos):
            captcha_log.registrar(inicio, datetime.datetime.now(), 'conferir_afiliados', os.path.join(PRINTS, nome),
                                  f'sem resposta 15 min; PC em espera {hora:%H:%M}, acordou {acordou:%H:%M}')
            log('captcha resolvido depois da espera: continuando do mesmo produto')
            status('rodando')
            return True
        if time.time() - ultimo_bipe > 300:
            bipe('CAPTCHA no celular — resolva à mão')
            ultimo_bipe = time.time()
        time.sleep(10)


def checar_bloqueios(pal=None):
    """Captcha -> registra, avisa e espera o Kevin (nunca resolve). Login -> para tudo."""
    textos = [t for t, *_ in (pal if pal is not None else ocr())]
    junto = ' '.join(textos).lower()
    if captcha_log.e_captcha(textos):
        inicio = datetime.datetime.now()
        nome = f'captcha_{inicio:%m%d_%H%M%S}.png'
        ps.print_tela(nome)
        status('alerta', f'CAPTCHA no tablet desde {inicio:%H:%M} — resolva à mão; o robô espera')
        log('CAPTCHA: pausado esperando o Kevin resolver no tablet')
        # Kevin (05/11): sem resposta em 15 min (a qualquer hora) -> PC em ESPERA e continua sozinho
        # quando ele resolver ao acordar. De dia (ou com outra tarefa no PC) espera 30 min e para.
        sys.path.insert(0, os.path.join(BASE, 'afiliados'))
        import suspender
        noite = suspender.no_horario() and not os.path.exists(suspender.CHAVE)
        limite = time.time() + (15 if noite else 30) * 60
        while time.time() < limite:
            bipe('CAPTCHA no tablet — resolva à mão')
            time.sleep(10)
            if not captcha_log.e_captcha([t for t, *_ in ocr()]):
                captcha_log.registrar(inicio, datetime.datetime.now(), 'conferir_afiliados',
                                      os.path.join(PRINTS, nome))
                log('captcha sumiu: continuando')
                status('rodando')
                return True
        espera_min = 15 if noite else 30
        ok, motivo = suspender.pode_suspender() if noite else (False, 'fora do horário configurado')
        if not ok:
            captcha_log.registrar(inicio, None, 'conferir_afiliados', os.path.join(PRINTS, nome),
                                  f'não resolvido em {espera_min} min; PC não suspenso: {motivo}')
            raise PararTudo(f'captcha não resolvido em {espera_min} min (PC não suspenso: {motivo})')
        return dormir_ate_resolver(inicio, nome, suspender)
    shopee_na_frente = 'com.shopee.br' in ps.sh('dumpsys window | grep mCurrentFocus')
    if shopee_na_frente and (('entrar' in junto and 'senha' in junto) or 'faça login' in junto or 'fazer login' in junto):
        ps.print_tela('login.png')
        raise PararTudo('Shopee pediu login no tablet — faça login à mão e rode de novo')


# ---------------- contagem de miniaturas ----------------

def miniaturas(im):
    """Topos (y) das miniaturas inteiras na coluna da esquerda (x 16-136, 160 px de altura)."""
    corridas, ini = [], None
    for y in range(90, 1216):
        escura = any(min(cor(im, x, y)) < 235 for x in range(22, 132, 4))
        if escura and ini is None:
            ini = y
        elif not escura and ini is not None:
            corridas.append((ini, y))
            ini = None
    return [a for a, b in corridas if 150 <= b - a <= 175]


TOPO, FUNDO = 90, 1215  # área da lista (abaixo do cabeçalho, acima da barra do Android)


def _cinza(im):
    import numpy as np
    return np.asarray(im.convert('L').crop((0, TOPO, im.size[0], FUNDO)), dtype=np.int16)[:, ::4]


def deslocamento(antes, depois):
    """Quantos px a lista subiu entre dois prints (alinha as faixas da tela; não depende de
    as miniaturas serem parecidas)."""
    import numpy as np
    # imagem reduzida (1 linha a cada 2) para ficar rápido; o resultado volta em px da tela
    a, b = _cinza(antes)[::2], _cinza(depois)[::2]
    h = a.shape[0]
    melhor, dmelhor = None, 0
    for d in range(0, h - 60):
        diff = np.abs(a[d:] - b[:h - d]).mean()
        if melhor is None or diff < melhor:
            melhor, dmelhor = diff, d
    return dmelhor * 2 if melhor is not None and melhor < 12 else None


def botoes_ver(im):
    """y dos botões amarelos 'Ver' (um por vídeo, ~150 px abaixo do topo da miniatura).
    Mais confiável que a miniatura, que às vezes tem borda branca/preta."""
    def amarelo(c):
        return c[0] >= 250 and 240 <= c[1] <= 252 and 215 <= c[2] <= 236
    linhas_ok = [y for y in range(TOPO, FUNDO) if sum(1 for x in range(P['ver_x'][0], P['ver_x'][1], 2) if amarelo(cor(im, x, y))) >= 6]
    res, ini, prev = [], None, None
    for y in linhas_ok + [None]:
        if y is not None and prev is not None and y == prev + 1:
            prev = y
            continue
        if ini is not None and 14 <= prev - ini <= 40 and ini > TOPO + 2 and prev < FUNDO - 2:
            res.append(ini)
        ini = prev = y
    return res


VIEWS = []  # views de cada vídeo contado na última lista (só registro)
ULTIMA_TELA = [None]  # última tela da lista de vídeos (main salva como prints\<itemId>_fim.jpg)


def views_da_tela(pal, botoes):
    """Número escrito à esquerda de cada botão 'Ver' (ex.: '1,7mil' / '930'). {y_botão: views}."""
    res = {}
    vers = [p for p in pal if p[0].lower() == 'ver']
    for y in botoes:
        w = min(vers, key=lambda p: abs(p[2] - (y + 6)), default=None)
        if not w or abs(w[2] - (y + 6)) > 14:
            continue
        esq = [p for p in pal if abs(p[2] - w[2]) <= 8 and p[1] + p[3] <= w[1] + 2 and w[1] - (p[1] + p[3]) < 30]
        if esq:  # o número fica ~17 px à esquerda do "Ver"
            res[y] = num(max(esq, key=lambda p: p[1])[0])
    return res


def contar_videos(nome_print):
    """Conta as miniaturas pela posição absoluta na lista: posição na tela + quanto já rolou."""
    # a lista às vezes abre um pouco rolada (1º vídeo cortado no topo): volta ao topo antes
    # (só 1 arrasto, e só se não abriu no topo: no topo o 1º botão 'Ver' fica em y~238)
    vs0 = botoes_ver(ps.print_tela())
    if not vs0 or not P['topo_ver'][0] <= vs0[0] <= P['topo_ver'][1]:
        ps.sh(f"input swipe {P['sw_topo']}")
        time.sleep(1.5)
    # espera a lista assentar (spinner de "carregando mais" no fim muda a tela e desalinha a contagem)
    ultima, fim_espera = None, time.time() + 12
    while time.time() < fim_espera:
        atual = ps.print_tela().convert('L').resize((40, 64)).tobytes()
        if ultima is not None and sum(abs(x - y) for x, y in zip(atual, ultima)) / len(atual) < 1.5:
            break
        ultima = atual
        time.sleep(1.5)
    topos, rolado, anterior = [], 0, None
    VIEWS.clear()
    ULTIMA_TELA[0] = None
    os.makedirs(os.path.join(PRINTS, f'_rolagem_{ID_APARELHO}'), exist_ok=True)
    for n in os.listdir(os.path.join(PRINTS, f'_rolagem_{ID_APARELHO}')):
        os.remove(os.path.join(PRINTS, f'_rolagem_{ID_APARELHO}', n))
    rastro = []
    parado = 0
    for rolagem in range(20):
        im = ps.print_tela()
        if rolagem == 0:
            im.save(os.path.join(PRINTS, nome_print))
        im.save(os.path.join(PRINTS, f'_rolagem_{ID_APARELHO}', f'{rolagem:02d}.png'))  # só os da última contagem
        if anterior is not None:
            d = deslocamento(anterior, im)
            if d is None:  # lista ainda carregando/animando: espera e tenta alinhar de novo (2x)
                for _ in range(2):
                    time.sleep(2)
                    im = ps.print_tela()
                    d = deslocamento(anterior, im)
                    if d is not None:
                        break
            if d is None:
                im.save(os.path.join(PRINTS, nome_print.replace('.png', '_desalinhado.png')))
                raise Pular('contagem: não consegui alinhar a rolagem da lista')
            if d < 10:
                # Kevin (05/11): a lista pode ainda estar carregando mais vídeos no fim. Só é fim
                # quando DUAS rolagens seguidas não movem nada (espera ~2,5 s e tenta de novo).
                parado += 1
                if parado >= 2:
                    break
                time.sleep(P.get('espera_fim', 2.5))
                ps.sh(f"input swipe {P['sw_lista']}")
                time.sleep(P.get('espera_scroll', 2))
                continue
            parado = 0
            rolado += d
        vs = botoes_ver(im)
        rastro.append((rolado, vs))
        try:
            # OCR só na faixa das views (à esquerda dos botões "Ver"): bem mais rápido que a tela toda
            vw = views_da_tela(ocr(im.crop((0, 0, P['ver_x'][1] + 80, im.size[1]))), vs)
        except Exception:
            vw = {}
        for y in vs:
            pos = y + rolado
            if not any(abs(pos - t) < 40 for t in topos):
                topos.append(pos)
                if vw.get(y) is not None:
                    VIEWS.append(vw[y])
        log(f'    rolagem {rolagem}: rolado={rolado} botões={vs} total={len(topos)}')
        if len(topos) > MAX_VIDEOS:
            return MAX_VIDEOS + 1
        anterior = im
        ULTIMA_TELA[0] = im
        ps.sh(f"input swipe {P['sw_lista']}")  # devagar: quase sem embalo
        time.sleep(P.get('espera_scroll', 2))  # ~2 s para a lista carregar mais vídeos
    return len(topos)


# ---------------- um produto ----------------

def acordado():
    """Celular no bateria: o scrcpy -w só mantém acordado na tomada. Se dormiu, acorda e tira a
    tela de bloqueio SEM PIN (com PIN o robô para e espera o Kevin, como antes)."""
    try:
        if 'mWakefulness=Awake' not in ps.sh('dumpsys power | grep mWakefulness=', timeout=20) or \
                'showing=true' in ps.sh('dumpsys window policy | grep showing=', timeout=20):
            log('  celular dormiu/bloqueou: acordando e desbloqueando (sem PIN)')
            ps.sh('input keyevent KEYCODE_WAKEUP')
            time.sleep(1)
            ps.sh('wm dismiss-keyguard')
            time.sleep(1.5)
            if 'showing=true' in ps.sh('dumpsys window policy | grep showing=', timeout=20):
                ps.acordar_e_desbloquear()
    except ps.Parou:
        raise
    except Exception as e:
        log(f'  acordar: {e!r}')


def conferir(link, tag, marcas):
    r = {'link': link}
    acordado()

    def marca(etapa):
        marcas.append((etapa, time.time()))
        fase({'produto': 'Compartilhar / comissão', 'compartilhar': 'página de afiliado',
              'afiliado': 'abrindo vídeos de criadores', 'lista': 'contando vídeos',
              'contagem': 'salvando'}.get(etapa, etapa), link)

    fase('abrindo o produto', link)

    # Tela inicial antes do link: senão a página do produto anterior ainda aparece por alguns
    # segundos e engana a conferência. Depois exige a mesma tela em 2 prints seguidos.
    def abrir_link():
        ps.sh('input keyevent KEYCODE_HOME')
        time.sleep(1)
        ps.sh(f'am start -a android.intent.action.VIEW -d {link} {ps.PKG}')
        time.sleep(2.5)

    abrir_link()
    captcha_log.contar_aberto()
    abriu = lambda i: pagina_leve(i) or pagina_completa(i)  # noqa: E731
    # Kevin 21/11: "falhou ao carregar" -> tenta de novo NA HORA; 2x o mesmo erro -> pula (erro_carregar)
    for vez in (1, 2):
        try:
            im = esperar(abriu, 40) and esperar(abriu, 3)
            if not im:
                checar_bloqueios()
                im = esperar(abriu, 15)
            falha = None if im else falha_de_carregamento()
        except TelaFalha as e:
            im, falha = None, str(e)
        if im:
            break
        if not falha:
            raise Pular('página do produto não abriu')
        if vez == 1:
            log(f'  tela de falha: "{falha[:60]}"; tentando de novo na hora')
            if not tocar_tentar_novamente():
                ps.sh('input keyevent KEYCODE_BACK')
                abrir_link()
            continue
        ps.sh('input keyevent KEYCODE_BACK')  # o próximo produto começa pela tela inicial: não precisa reabrir o app
        raise ErroCarregar(f'erro_carregar: "{falha[:80]}" 2x seguidas')
    if pagina_leve(im):
        # como o Kevin faz: espera a foto aparecer e toca no TEXTO do nome (com nome comprido a
        # setinha da direita some). A página completa demora até ~30 s (mostra um "presente" cinza).
        if not esperar(leve_pronta, 30):
            raise Pular('página leve não terminou de carregar (foto) em 30 s')
        time.sleep(1)
        if not tocar_e_esperar(P['leve_nome'], pagina_completa, pagina_leve, 30):
            raise Pular('página leve: tocar no nome não abriu a página completa')
    if not esperar(lambda i: pagina_completa(i) and (foto_carregada(i) or icones_carregados(i)), 20):
        raise Pular('página completa não terminou de carregar')
    marca('produto')

    # Compartilhar -> painel com a faixa da comissão
    time.sleep(1.5)
    im = tocar_e_esperar(P['compartilhar'], painel_compartilhar, pagina_completa, 10)
    if not im:
        raise Pular('botão Compartilhar não abriu o painel')
    time.sleep(0.8)
    for _leitura in range(2):  # se a comissão não vier, lê de novo 1x
        pal = ocr()
        for t, y in linhas(pal):
            if 'Estim' in t or 'Comissão de Afiliados' in t:
                r['comissao_rs'] = reais(t) or reais(' '.join(p[0] for p in pal if abs(p[2] - y) < 12))
                break
        if r.get('comissao_rs') is not None:
            break
        time.sleep(1)
    y_faixa = next((p[2] + 6 for p in pal if p[0] == 'Afiliados' and P['faixa_y'][0] < p[2] < P['faixa_y'][1]), P['faixa'][1])
    marca('compartilhar')
    # Kevin (05/11): comissão baixa já descarta aqui, sem abrir a página de afiliado (~40 s a menos)
    corte = min(COMISSAO_MIN, COMISSAO_MIN_TAXA_ALTA)  # 15-20: a régua decide com a taxa e o v7
    if r.get('comissao_rs') is not None and r['comissao_rs'] < corte:
        r['nome'] = r.get('nome') or ''
        r['decisao_pronta'] = ('descarta', f'comissão baixa (R$ {r["comissao_rs"]:.2f} < {corte:.0f})'.replace('.', ','))
        ps.sh('input keyevent KEYCODE_BACK')
        return r

    # Kevin (05/11): depois de tocar na faixa, a página de afiliado (presente cinza) pode demorar.
    # Espera até 45 s, checando a cada 3 s, SEM vigia de "tela parada"/esqueleto nesse passo;
    # só depois disso a recuperação completa (fechar/reabrir) e refaz o produto.
    ps.sh(f"input tap {P['faixa'][0]} {y_faixa}")
    fim_af, carregou = time.time() + 45, False
    while time.time() < fim_af:
        im = ps.print_tela()
        if pagina_afiliado(im) and not esqueleto(im):
            carregou = True
            break
        if painel_compartilhar(im) and time.time() > fim_af - 40:  # o toque não pegou: toca de novo 1x
            ps.sh(f"input tap {P['faixa'][0]} {y_faixa}")
        time.sleep(3)
    if not carregou:
        raise Pular('página de afiliado não carregou em 45 s')
    marca('afiliado')
    time.sleep(1.5)
    preco = None
    secao, fim_pagina = None, False
    for rolagem in range(4):
        pal = ocr()
        lin = linhas(pal)
        if r.get('afiliados') is None:
            r['afiliados'] = antes_de(pal, 'Afiliados')
        if r.get('vendas') is None:
            r['vendas'] = antes_de(pal, 'Vendido')
        if preco is None:
            precos = [reais(t) for t, y in lin if t.startswith('R$') and reais(t)]
            preco = precos[0] if precos else None
        if not r.get('nome'):  # linhas entre o preço e a linha dos afiliados
            y_pr = next((y for t, y in lin if t.startswith('R$')), None)
            y_af = next((y for t, y in lin if 'Afiliados' in t), None)
            if y_pr is not None and y_af is not None:
                r['nome'] = ' '.join(t for t, y in lin if y_pr + 20 < y < y_af - 10)
        s = next((p for p in pal if p[0] == 'Aprenda'), None)
        if s:
            secao = s[2] + s[4] // 2
        fim_pagina = any(k in ' '.join(t for t, _ in lin) for k in ('mesma loja', 'similares'))
        if (secao and P['secao_y'][0] < secao < P['secao_y'][1]) or fim_pagina:
            break
        ps.sh(f"input swipe {P['sw_af']}")
        time.sleep(1.5)
        secao = None
    nome_print = f'{tag}_afiliado.png'
    ps.print_tela(nome_print)
    r['print'] = os.path.join(PRINTS, nome_print)
    if preco and r.get('comissao_rs'):
        r['comissao_pct'] = round(r['comissao_rs'] / preco * 100, 1)
    if secao and P['secao_y'][0] < secao < P['secao_y'][1]:
        if not tocar_e_esperar((P['chevron_x'], secao), lista_videos, pagina_afiliado, 15):
            raise Pular('seção de vídeos achada, mas a lista "Vídeos de Criadores" não abriu')
        marca('lista')
        time.sleep(1.2)
        r['videos'] = contar_videos(f'{tag}_videos.png')
        if VIEWS:  # a régua de 10/11 usa views_max (vídeo vencedor)
            vv = sorted(VIEWS)
            r.update(views_max=vv[-1], views_mediana=vv[len(vv) // 2], views_total=sum(vv))
        r['print'] = os.path.join(PRINTS, f'{tag}_videos.png')
        marca('contagem')
    elif fim_pagina:
        r['videos'] = 0  # página toda carregada e sem a seção "Aprenda Com Outros Criadores"
    else:
        raise Pular('não achei a seção de vídeos nem o fim da página de afiliado')
    return r


VENDAS_RECENTES = next((f'{l}:\\{r}\\Central Esposa\\vendas_recentes.json' for l in 'GHIJKLMNOPQRSTUVWXYZDEF' for r in ('Meu Drive', 'My Drive')
                 if __import__('os').path.isdir(f'{l}:\\{r}\\Central Esposa')), r'G:\Meu Drive\Central Esposa\vendas_recentes.json')  # Paola: letra do Drive automática  # Drive sincronizado no PC
_VR = None


def vendas_recentes(item):
    """(total, v7, v3, primeira_vez) das varreduras diárias, pelo itemId (sem o shopid), ou None."""
    global _VR
    if _VR is None:
        try:
            _VR = json.load(open(VENDAS_RECENTES, encoding='utf-8')).get('itens', {})
        except Exception as e:
            log(f'  vendas_recentes.json não lido: {e}')
            _VR = {}
    chave = str(item or '').split('.')[-1]
    return _VR.get(chave)


def _int(x):
    return int(x) if str(x).lstrip('-').isdigit() else None


def regua_nova(r):
    """Linhas conferidas a partir de VALIDA_DESDE usam a régua de 10/11; as antigas mantêm a de 05/11."""
    d = str(r.get('data') or '')
    return not d or d >= VALIDA_DESDE


def decidir(r):
    if regua_nova(r):
        return decidir_1011(r)
    return decidir_0511(r)


def decidir_1011(r):
    """Régua do Kevin (10/11): "produtos com menos vídeos ainda, que ainda não têm um vídeo vencedor".
    comissão < mín descarta · vendas < mín descarta (anúncio < 7 dias com >= 2: revisar) ·
    vídeos > MAX_APROV descarta · algum vídeo com >= VIEWS_VENCEDOR views descarta ("já tem vídeo vencedor") ·
    semana parada (v7 = 0): aprovado só com >= 50 vendas no total, senão revisar · senão aprovado.
    Prioridade: aprovado com <= MAX_PRIO vídeos. A lista não mostra vendas por vídeo: só views."""
    v, vendas, v7 = _int(r.get('videos')), _int(r.get('vendas')), _int(r.get('v7'))
    com = r.get('comissao_rs')
    try:
        com = float(str(com).replace(',', '.')) if com not in (None, '') else None
    except ValueError:
        com = None
    pct = r.get('comissao_pct')
    try:
        pct = float(str(pct).replace(',', '.')) if pct not in (None, '') else None
    except ValueError:
        pct = None
    minimo = comissao_minima(pct, v7)
    if com is not None and com < minimo:
        por = '' if minimo == COMISSAO_MIN_TAXA_ALTA else (
            f' · taxa {pct:.1f}%'.replace('.', ',') if pct is not None else ' · taxa não lida') + (
            '' if pct is None or pct <= TAXA_ALTA_PCT else (' · sem venda na semana' if not v7 else ''))
        return 'descarta', f'comissão baixa (R$ {com:.2f} < {minimo:.0f}){por}'.replace('.', ',', 1)
    if vendas is None:
        return 'revisar', 'vendas não lidas'
    idade = None
    try:
        idade = (datetime.date.today() - datetime.date.fromisoformat(r.get('primeira_vez'))).days
    except Exception:
        pass
    if vendas < VENDAS_MIN:
        if idade is not None and idade < 7 and vendas >= 2:
            return 'revisar', f'anúncio novo ({idade} dias) com {vendas} vendas'
        return 'descarta', f'só {vendas} vendas (< {VENDAS_MIN})'
    if v is None:
        return 'revisar', 'vídeos não contados'
    if v > MAX_APROV:
        return 'descarta', f'{f"{MAX_APROV + 1}+" if v > MAX_VIDEOS else v} vídeos (> {MAX_APROV})'
    vmax = _int(r.get('views_max'))
    if vmax is not None and vmax >= VIEWS_VENCEDOR:
        return 'descarta', f'já tem vídeo vencedor ({vmax} visualizações)'
    sem_views = ' · views não lidas' if v > 0 and vmax is None else ''
    sem_fonte_v7 = v7 is None and not _VR  # PC Paola 23/11: sem vendas_recentes.json não há como exigir; decide pelo resto
    if EXIGIR_V7 and not (v7 or 0) > 0 and not sem_fonte_v7:  # perfil exige venda na semana
        if v7 is None:
            return 'revisar', f'{v} vídeos · venda da semana desconhecida (perfil {PERFIL_NOME} exige)'
        return 'descarta', f'{v} vídeos · sem venda na semana (perfil {PERFIL_NOME} exige)'
    if v7 == 0:
        if vendas >= 50:
            return 'aprovado', f'{v} vídeos, {vendas} vendas no total (semana parada, mas histórico bom){sem_views}'
        return 'revisar', f'{v} vídeos · parado na semana (v7 = 0){sem_views}'
    extra = ' · sem dado da semana' if v7 is None else f', v7={v7}'
    prio = f' · prioridade (<= {MAX_PRIO} vídeo)' if v <= MAX_PRIO else ''
    return 'aprovado', f'{v} vídeos, {vendas} vendas{extra}{prio}{sem_views}'


def decidir_0511(r):
    """Decisão por produto (ver a régua logo abaixo)."""
    # Régua do Kevin (05/11 09:20, "só o lógico"; sem a regra "v7 > vídeos" nem "vendas > 10"):
    #  comissão < 20 descarta · total < 10 descarta (anúncio < 7 dias com >= 2 vendas: revisar)
    #  > 15 vídeos descarta · 10-15 aprovado só se v7 >= 3x vídeos (senão revisar)
    #  < 10 vídeos: aprovado se v7 >= 1 ou v7 desconhecido; v7 = 0: revisar · < 5 vídeos aprovado = prioridade
    v, vendas, v7 = _int(r.get('videos')), _int(r.get('vendas')), _int(r.get('v7'))
    com = r.get('comissao_rs')
    try:
        com = float(str(com).replace(',', '.')) if com not in (None, '') else None
    except ValueError:
        com = None
    if com is not None and com < COMISSAO_MIN:
        return 'descarta', f'comissão baixa (R$ {com:.2f} < {COMISSAO_MIN:.0f})'.replace('.', ',')
    if vendas is None:
        return 'revisar', 'vendas não lidas'
    idade = None
    try:
        idade = (datetime.date.today() - datetime.date.fromisoformat(r.get('primeira_vez'))).days
    except Exception:
        pass
    if vendas < 10:
        if idade is not None and idade < 7 and vendas >= 2:
            return 'revisar', f'anúncio novo ({idade} dias) com {vendas} vendas'
        return 'descarta', f'só {vendas} vendas (< 10)'
    if v is None:
        return 'revisar', 'vídeos não contados'
    if v > 15:
        return 'descarta', f'{"16+" if v >= 16 else v} vídeos (> 15)'
    if v >= 10:
        if v7 is not None and v7 >= 3 * v:
            return 'aprovado', f'{v} vídeos, mas v7={v7} (>= 3x vídeos)'
        # Kevin (05/11): "aprove os que valem" e mantenha a lógica: comissão alta compensa a concorrência
        if com is not None and com >= 60:
            return 'aprovado', f'{v} vídeos e v7 fraco, mas comissão alta (R$ {com:.2f} >= 60)'.replace('.', ',')
        return 'revisar', f'{v} vídeos (10-15) e v7={v7 if v7 is not None else "?"} (< 3x = {3 * v})'
    if v7 == 0:
        # poucos vídeos e bom histórico: pode ser só uma semana fraca
        if v <= 5 and vendas >= 50:
            return 'aprovado', f'{v} vídeos, {vendas} vendas no total (semana parada, mas histórico bom)'
        return 'revisar', f'{v} vídeos · parado na semana (v7 = 0)'
    extra = ' · sem dado da semana' if v7 is None else f', v7={v7}'
    return 'aprovado', f'{v} vídeos, {vendas} vendas{extra}' + (' · prioridade (< 5 vídeos)' if v < 5 else '')


FALHAS_SEGUIDAS = [0]
INICIO_ULTIMO = [0.0]


ZERO_CSV = os.path.join(PASTA, 'aprovados_zero_videos.csv')


def gerar_aprovados_zero():
    """Kevin 21/11: aprovados com 0 vídeos separados para ele escolher o que produzir (última linha de cada produto)."""
    try:
        ult = {}
        for l in csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';'):
            ult[(l.get('itemId') or '').split('.')[-1]] = l
        try:  # 22/11: nunca listar produto já produzido / da lista de pular
            import pular_afiliados
            pular = pular_afiliados.ids()
        except Exception:
            pular = set()
        zs = [l for l in ult.values() if l.get('decisao') == 'aprovado' and str(l.get('videos')).strip() == '0'
              and (l.get('itemId') or '').split('.')[-1] not in pular]
        zs.sort(key=lambda l: l.get('data') or '', reverse=True)
        tmp = ZERO_CSV + f'.{ID_APARELHO}.tmp'
        with open(tmp, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(['data', 'nome', 'link', 'vendas', 'v7', 'comissao_rs', 'comissao_pct', 'itemId', 'aparelho'])
            for l in zs:
                w.writerow([l.get('data'), l.get('nome'), l.get('link'), l.get('vendas'), l.get('v7'), l.get('comissao_rs'),
                            l.get('comissao_pct'), l.get('itemId'), l.get('aparelho')])
        os.replace(tmp, ZERO_CSV)
    except Exception as e:
        log(f'  (aprovados_zero_videos.csv não atualizado: {e!r})')


def aprovados_da_sequencia():
    """Aprovados (dos 2 aparelhos) desde o início da sequência (HORST_INICIO_SEQ 'AAAA-MM-DD HH:MM'), senão do dia."""
    desde = os.environ.get('HORST_INICIO_SEQ') or f'{datetime.date.today():%Y-%m-%d}'
    ult = {}
    try:
        for l in csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';'):
            ult[(l.get('itemId') or '').split('.')[-1]] = l
    except Exception:
        return 0
    return sum(1 for l in ult.values() if l.get('decisao') == 'aprovado' and (l.get('data') or '') >= desde)


def fase(texto, link=''):
    """Etapa atual no status.json (a Central relê a cada 3 s): mostra ao vivo o que o robô está fazendo."""
    try:
        st = json.load(open(STATUS, encoding='utf-8'))
        agora = f'{datetime.datetime.now():%H:%M:%S}'
        st.update(etapa=texto, etapa_link=link, quando=agora)
        # a Central já mostra as "linhas" do card: a 1ª vira "Agora: <etapa> · hora · lote x/50"
        pr = st.get('progresso') or {}
        lote = f" · lote {pr.get('feito', 0) + 1}/{pr['total']}" if pr.get('total') else ''
        st['linhas'] = [f'Agora: {texto} · {agora}{lote}'] + [l for l in (st.get('linhas') or [])
                                                             if not str(l).startswith('Agora:')]
        tmp = STATUS + '.tmp'
        json.dump(st, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
        os.replace(tmp, STATUS)
        shutil.copyfile(STATUS, STATUS_GERAL)
    except Exception:
        pass


def recuperar_app():
    """Recuperação completa (igual ao Kevin fechar e abrir à mão): force-stop, 5 s, tela inicial,
    abrir a Shopee pelo launcher e esperar a home dela carregar. NUNCA pm clear (desloga)."""
    ps.sh(f'am force-stop {ps.PKG}')
    time.sleep(5)
    acordado()
    ps.sh('input keyevent KEYCODE_HOME')
    time.sleep(1)
    ps.sh(f'monkey -p {ps.PKG} -c android.intent.category.LAUNCHER 1')
    fim = time.time() + 30
    anterior = None
    while time.time() < fim:  # app aberto e parado (sem esqueleto e fora da tela de abertura laranja)
        im = ps.print_tela()
        w, h = im.size
        abertura = ps.e_laranja(cor(im, w // 2, h // 2)) and ps.e_laranja(cor(im, w // 2, h // 5))
        atual = im.convert('L').resize((40, 64)).tobytes()
        parada = anterior is not None and sum(abs(x - y) for x, y in zip(atual, anterior)) / len(atual) < 3
        if not esqueleto(im) and not abertura and parada:
            break
        anterior = atual
        time.sleep(1.5)
    time.sleep(2)


def bateria():
    """Nível da bateria do tablet (%), ou None se não conseguir ler."""
    try:
        m = re.search(r'level: (\d+)', ps.sh('dumpsys battery'))
        return int(m[1]) if m else None
    except Exception:
        return None


def salvar_fim(item):
    """Print reduzido (jpg ~50 KB) da última tela da lista de vídeos, para conferir depois.
    Apaga os *_fim.jpg com mais de 7 dias."""
    im = ULTIMA_TELA[0]
    ULTIMA_TELA[0] = None
    try:
        if im is not None and item:
            im.convert('RGB').resize((400, 640)).save(os.path.join(PRINTS, f'{item}_fim.jpg'), quality=60)
        limite = time.time() - 7 * 86400
        for n in os.listdir(PRINTS):
            p = os.path.join(PRINTS, n)
            if n.endswith('_fim.jpg') and os.path.getmtime(p) < limite:
                os.remove(p)
    except Exception as e:
        log(f'  (print do fim não salvo: {e})')


def prioridade(r):
    v = _int(r.get('videos'))
    limite = MAX_PRIO if regua_nova(r) else 4  # 10/11: 0 a 1 vídeo; antes de 10/11: < 5
    return 'sim' if r.get('decisao') == 'aprovado' and v is not None and v <= limite else 'não'


def nossos_videos(link):
    """Quantos vídeos NÓS já publicamos desse produto (postados.json + filas; casa pelo nome do
    produto do link na fila, porque cada versão A/B/C tem um link curto diferente)."""
    import glob
    try:
        fila = json.load(open(os.path.join(BASE, 'fila.json'), encoding='utf-8'))
        for p in glob.glob(os.path.join(BASE, 'filas', 'fila_*.json')):
            fila += json.load(open(p, encoding='utf-8'))
        post = {e['doc'] for e in json.load(open(os.path.join(BASE, 'postados.json'), encoding='utf-8'))
                if str(e.get('resultado', '')).startswith('postado')}
    except Exception:
        return ''
    produto = next((i.get('produto') for i in fila if i.get('link') == link), None)
    if not produto:
        return 0
    return len({i['doc'] for i in fila if i.get('produto') == produto and i['doc'] in post})


def completar_recentes(r):
    vr = vendas_recentes(r.get('itemId'))
    r['v7'] = vr[1] if vr and vr[1] is not None else ''
    r['primeira_vez'] = vr[3] if vr and len(vr) > 3 and vr[3] else ''
    r['v3'] = vr[2] if vr and len(vr) > 2 and vr[2] is not None else ''
    r['nossos_videos'] = nossos_videos(r.get('link'))


# ---------------- entrada / saída ----------------

def ler_entrada(caminho):
    texto = open(caminho, encoding='utf-8-sig').read().strip()
    if texto.startswith('['):
        return [{'itemId': str(i.get('itemId') or i.get('item_id') or ''), 'link': i['link'], 'nome': i.get('nome', '')}
                for i in json.loads(texto) if i.get('link')]
    return [{'itemId': '', 'link': l.strip()} for l in texto.splitlines() if l.strip().startswith('http')]


def links_teste():
    fila = json.load(open(os.path.join(BASE, 'fila.json'), encoding='utf-8'))
    postados = {e['doc'] for e in json.load(open(os.path.join(BASE, 'postados.json'), encoding='utf-8'))
                if str(e.get('resultado', '')).startswith('postado')}
    vistos, out = set(), []
    for i in fila:
        if i['doc'] in postados and i.get('produto') not in vistos:
            vistos.add(i.get('produto'))
            out.append({'itemId': '', 'link': i['link']})
    return out[-3:]


def gravar(r):
    r['aparelho'] = ID_APARELHO
    r['zero_videos'] = 'sim' if r.get('decisao') == 'aprovado' and _int(r.get('videos')) == 0 else ''
    linha = {k: ('' if r.get(k) is None else r.get(k)) for k in CAMPOS}
    for k in ('comissao_rs', 'comissao_pct'):  # vírgula decimal (Excel em português)
        if isinstance(r.get(k), float):
            linha[k] = f'{r[k]:.2f}'.replace('.', ',')
    with ap.trava_csv():  # 2 robôs: um escreve de cada vez
        novo = not os.path.exists(CSV)
        with open(CSV, 'a', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=';', extrasaction='ignore')
            if novo:
                w.writeheader()
            w.writerow(linha)


def resumo_hoje():
    hoje = f'{datetime.date.today():%Y-%m-%d}'
    try:
        lin = [l for l in csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';')
               if l['data'].startswith(hoje)]
    except Exception:
        lin = []
    bons = sum(1 for l in lin if l['decisao'].startswith('aprovado'))
    vids = [int(l['videos']) for l in lin if l['videos'].isdigit()]
    media = f'{sum(vids) / len(vids):.1f}' if vids else '-'
    return f'{len(lin)} checados hoje, {bons} bons, média {media} vídeos'


def registrar_card():
    try:
        cards = json.load(open(CARDS, encoding='utf-8'))
    except Exception:
        return
    novo = {'id': 'afiliados', 'title': 'Afiliados (filtro automático)', 'tipo': 'generico',
            'status': STATUS_GERAL, 'parar': PARAR, 'detail': 'Robô de checagem de afiliados'}
    for c in cards:
        if c.get('id') == 'afiliados':
            c.pop('state', None)
            c.update(novo)
            break
    else:
        cards.append(novo)
    json.dump(cards, open(CARDS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ---------------- principal ----------------

def main():
    a = argparse.ArgumentParser()
    a.add_argument('entrada', nargs='?')
    a.add_argument('--teste', action='store_true', help='3 produtos já postados da fila.json')
    args = a.parse_args()
    if not args.teste and not args.entrada:
        a.error('passe o arquivo de links ou --teste')
    os.makedirs(PRINTS, exist_ok=True)
    registrar_card()

    lock_meu = os.path.join(BASE, f'rodar_fila_{ID_APARELHO}.lock')
    fila_aqui = False
    for caminho in (lock_meu, LOCK_FILA if ID_APARELHO == 'celular1' else None):
        if not caminho or not os.path.exists(caminho):
            continue
        try:
            if vivo(int(open(caminho).read())):
                fila_aqui = True
        except ValueError:
            pass
    if fila_aqui:
        status('parado', 'fila de postagem neste aparelho — não rodei')
        log(f'a fila de postagem está no {ID_APARELHO}: não vou mexer neste aparelho')
        sys.exit(1)
    try:  # 11/11: o "assistir" do Kevin usa este celular: não rodo em cima dele
        import assistir_uso
        if assistir_uso.assistir_usa(ID_APARELHO):
            status('parado', 'assistir neste aparelho — não rodei')
            log(f'o assistir está rodando no {ID_APARELHO}: não vou mexer neste aparelho')
            sys.exit(1)
    except ImportError:
        pass
    if os.path.exists(LOCK):
        try:
            pid = int(open(LOCK).read())
            if vivo(pid):
                log(f'já está rodando (pid {pid})')
                sys.exit(0)
        except ValueError:
            pass
    open(LOCK, 'w').write(str(os.getpid()))
    try:
        itens = links_teste() if args.teste else ler_entrada(args.entrada)
        if not args.teste:
            import pular_afiliados
            itens = pular_afiliados.tirar(itens, log)
        if 'device' not in ps.adb('get-state'):
            raise PararTudo('tablet não conectado no adb')
        fim_pin = time.time() + 30 * 60
        while True:  # tela com PIN: nunca digita senha; bipa e espera o Kevin desbloquear
            try:
                ps.acordar_e_desbloquear()
                break
            except ps.Parou as e:
                if time.time() > fim_pin:
                    raise PararTudo(f'tela bloqueada com PIN por 30 min: {e}')
                status('alerta', 'tablet bloqueado com PIN — desbloqueie; o robô espera')
                bipe('tablet bloqueado com PIN — desbloqueie')
                time.sleep(15)
        perfil, tam = escolher_perfil()
        log(f'== {len(itens)} produto(s) para conferir · aparelho {ps.SERIAL} · perfil {perfil} {tam[0]}x{tam[1]} · '
            f'régua {PERFIL_NOME} (até {MAX_APROV} vídeos, meta {META_APROV or "sem"}, venda semana {"sim" if EXIGIR_V7 else "não"})')
        for n, it in enumerate(itens, 1):
            if os.path.exists(PARAR) or os.path.exists(f'{PARAR}_{ID_APARELHO}'):
                log('arquivo PARAR encontrado — parando')
                break
            ident = it.get('itemId') or ''
            if ident and (ap.ja_conferido(ident) or not ap.reservar(ident, ID_APARELHO)):
                log(f'  {ident}: já conferido ou reservado pelo outro aparelho, pulando')
                continue
            try:  # tela física apagada durante o trabalho (screencap/toques continuam funcionando)
                import tela_apagada
                tela_apagada.garantir(ps.SERIAL)
            except Exception:
                pass
            nivel = bateria()
            log(f'  bateria do tablet: {nivel}%')
            if nivel is not None and nivel < 15:  # pausa entre produtos até carregar (sem som)
                log(f'  bateria {nivel}% < 15%: pausado carregando')
                anterior = nivel
                while nivel is not None and nivel < 40:
                    tomada = 'AC powered: true' in ps.sh('dumpsys battery')
                    fonte = 'tomada' if tomada else 'só USB do PC (não carrega)'
                    status('alerta', f'pausado: carregando (bateria {nivel}%, {fonte})')
                    time.sleep(180)
                    try:  # captcha aparecendo durante a pausa: registra e espera o Kevin do mesmo jeito
                        checar_bloqueios()
                    except PararTudo:
                        raise
                    except Exception:
                        pass
                    nivel = bateria()
                    # na tomada, volta com >= 20% subindo; só no USB do PC ou caindo, espera 40%
                    if tomada and nivel is not None and nivel >= 20 and nivel > anterior:
                        break
                    anterior = nivel
                log(f'  bateria {nivel}%: retomando')
            # ritmo mais lento entre produtos (conta não "esquenta"): espera o que falta do intervalo
            intervalo = float(os.environ.get('HORST_INTERVALO', INTERVALO_PRODUTOS))
            if n > 1 and intervalo > 0:
                import random
                alvo = INICIO_ULTIMO[0] + intervalo * random.uniform(0.75, 1.25)
                espera = alvo - time.time()
                if espera > 0:
                    status('rodando', f'esperando {espera:.0f} s entre produtos (ritmo lento, evita captcha)')
                    while time.time() < alvo and not os.path.exists(PARAR):
                        time.sleep(5)
                    if os.path.exists(PARAR):
                        log('arquivo PARAR encontrado — parando')
                        break
            INICIO_ULTIMO[0] = time.time()
            # Kevin: reabrir o app a cada 5 produtos (a cada 3 se os últimos produtos estão falhando)
            cada = 3 if FALHAS_SEGUIDAS[0] >= 2 else 5
            if n > 1 and (n - 1) % cada == 0:
                log(f'  a cada {cada} produtos: fechando e reabrindo a Shopee')
                recuperar_app()
            LOTE.update(feito=n - 1, total=len(itens))
            status('rodando')
            t0 = time.time()
            tag = f'{datetime.datetime.now():%m%d_%H%M%S}'
            marcas = [('início', t0)]
            r = {'link': it['link']}
            # regra do Kevin: qualquer problema de carregamento -> fechar e reabrir o app e tentar de novo,
            # até 3 tentativas por produto; só depois registra erro e segue
            for tentativa in (1, 2, 3):
                try:
                    r = conferir(it['link'], tag, marcas)
                    r['itemId'] = it.get('itemId') or item_id(it['link'])
                    completar_recentes(r)
                    if r.get('v7') in (None, '') and it.get('v7') is not None:  # busca nova (10/11): v7 vem da fila
                        r['v7'] = it['v7']
                    if not r.get('primeira_vez') and it.get('primeira_vez'):
                        r['primeira_vez'] = it['primeira_vez']
                    r['decisao'], r['motivo'] = r.pop('decisao_pronta', None) or decidir(r)
                    break
                except Pular as e:
                    if isinstance(e, ErroCarregar):
                        r = {'link': it['link'], 'decisao': 'erro_carregar', 'motivo': str(e)}
                        log(f'  {e} — pulando para o próximo')
                        break
                    if isinstance(e, Esgotado) or ESGOTADO_RE.search(str(e)):
                        nome = f'{tag}_esgotado.png'
                        ps.print_tela(nome)
                        r = {'link': it['link'], 'decisao': 'esgotado', 'motivo': f'produto {e}'.strip(),
                             'print': os.path.join(PRINTS, nome)}
                        log(f'  esgotado/indisponível/não listado: {e} — segue sem esperar comissão')
                        break
                    nome = f'{tag}_erro{tentativa}.png'
                    ps.print_tela(nome)
                    r = {'link': it['link'], 'decisao': 'erro', 'motivo': f'{e} (tentativa {tentativa})',
                         'print': os.path.join(PRINTS, nome)}
                    log(f'  falhou (tentativa {tentativa}): {e}')
                    if isinstance(e, FalhaCarregar):  # já recarregou 1x: registra (recheck depois) e segue
                        r['motivo'] = str(e)
                        break
                    if tentativa < 3:
                        log('  recuperação: fechando e reabrindo a Shopee pelo launcher')
                        recuperar_app()
                        marcas[:] = [('início', time.time())]
            FALHAS_SEGUIDAS[0] = (FALHAS_SEGUIDAS[0] + 1 if r.get('decisao') == 'erro'
                                  and not str(r.get('motivo', '')).startswith('falha_carregar') else 0)
            if FALHAS_SEGUIDAS[0] >= 3:
                raise PararTudo(f'{FALHAS_SEGUIDAS[0]} produtos seguidos com erro mesmo reabrindo a Shopee 3x '
                                f'(último: {r.get("motivo")})')
            r['data'] = f'{datetime.datetime.now():%Y-%m-%d %H:%M}'
            r['itemId'] = it.get('itemId') or item_id(it['link'])
            r['segundos'] = round(time.time() - t0)
            if not str(r.get('nome') or '').strip() or str(r.get('nome')).replace('.', '').isdigit():
                r['nome'] = it.get('nome') or r.get('nome') or ''  # OCR não leu: usa o nome da lista
            r['prioridade'] = prioridade(r)
            salvar_fim(r.get('itemId'))
            gravar(r)
            try:  # 25/11 (a dona): resultado do filtro vai para o Drive -> Tinder
                sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'afiliados'))
                import resultado_drive; resultado_drive.exportar()
            except Exception as e:
                log(f'(resultado para o Tinder falhou: {e!r})')
            if r.get('decisao') in ('erro', 'erro_carregar'):
                ap.liberar(r.get('itemId'))  # libera a reserva (Kevin 21/11)
            if r.get('decisao') == 'aprovado':
                gerar_aprovados_zero()
            if META_APROV and aprovados_da_sequencia() >= META_APROV:
                log(f'meta do perfil {PERFIL_NOME} batida: {META_APROV} aprovados nesta sequência — parando limpo')
                ap.gravar_parada(ID_APARELHO, f'normal: META batida ({META_APROV} aprovados, perfil {PERFIL_NOME})')
                break
            LOTE['feito'] = n
            status('rodando')
            etapas = ' '.join(f'{e}={b - a:.0f}s' for (_, a), (e, b) in zip(marcas, marcas[1:]))
            log(f'  {r["itemId"]} vendas={r.get("vendas")} afiliados={r.get("afiliados")} '
                f'vídeos={r.get("videos")} comissão=R${r.get("comissao_rs")} -> {r["decisao"]} '
                f'({r.get("motivo")}) [{r["segundos"]} s: {etapas}]')
        LOTE.update(feito=None, total=None)
        status('parado')
    except PararTudo as e:
        status('erro', str(e))
        log(f'PAROU: {e}')
        ap.gravar_parada(ID_APARELHO, f'PAROU: {e}')
        if any(k in str(e).lower() for k in ('captcha', 'login', 'bloquead', 'pin')):
            bipe(str(e))  # só quando precisa do Kevin
        sys.exit(1)
    except Exception as e:
        status('erro', f'erro inesperado: {e!r}')
        log(f'erro inesperado: {e!r}')
        ap.gravar_parada(ID_APARELHO, f'erro inesperado: {e!r}')
        raise
    finally:
        try:
            import tela_apagada
            tela_apagada.parar()
        except Exception:
            pass
        try:
            os.remove(LOCK)
        except Exception:
            pass


if __name__ == '__main__':
    main()

