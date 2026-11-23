r"""Posta a fila do Shopee Vídeo no tablet, um post por vez (não precisa do Claude).

Uso:  python rodar_fila.py            (roda até 22:00 ou até a fila acabar)
      python rodar_fila.py --um       (posta só o próximo e sai)

- Fila: fila.json (ordem do arquivo). Pula o que já está "postado" no postados.json.
- Cada ciclo: baixa o vídeo pelo navegador (Downloads), posta com postar_shopee.py,
  confere no perfil (1ª miniatura = vídeo novo, toca ~15 s, print local),
  e só então apaga o vídeo do PC e do tablet.
- Qualquer erro ou "incerto": print + erro.txt e PARA tudo. Enquanto erro.txt existir,
  o script não roda (apague depois de conferir o que houve).
- Para parar com calma: crie o arquivo C:\horst\tablet\PARAR (para antes do próximo post).
- Ritmo: um post a cada 8-12 min (sorteado), só entre 08:00 e 22:00 (hora do PC).
"""
import argparse, contextlib, datetime, json, os, random, re, shutil, sys, threading, time, traceback

BASE = r'C:\horst\tablet'
sys.path.insert(0, BASE)
import postar_shopee as ps  # noqa: E402
import conferir  # noqa: E402
import aparelho_atual as ap  # noqa: E402
import pendentes  # noqa: E402


def _print_no_log(*a, **k):
    """As mensagens do postar_shopee (cada passo, caminho direto ou não) também vão pro log."""
    log('  ' + ' '.join(str(x) for x in a).strip())


ps.print = _print_no_log

FILA = os.path.join(BASE, 'fila.json')
POSTADOS = os.path.join(BASE, 'postados.json')
SYNC = os.path.join(BASE, 'postados_para_sync.json')
ERRO = os.path.join(BASE, 'erro.txt')
PARAR = os.path.join(BASE, 'PARAR')
ID_FILA = ap.id_aparelho()
if ID_FILA in ('', 'padrao'):
    ID_FILA = 'celular1'  # sem serial continua sendo o aparelho padrão
LOCK = os.path.join(BASE, f'rodar_fila_{ID_FILA}.lock')
LOCK_LEGADO = os.path.join(BASE, 'rodar_fila.lock')  # o vigia olha este; só o celular1 segura
PARAR_MEU = os.path.join(BASE, f'PARAR_{ID_FILA}')
CLAIMS = os.path.join(BASE, 'fila_claims')
LOG = os.path.join(BASE, 'rodar_fila.log')
VIDEOS = os.path.join(BASE, 'videos')
DOWNLOADS = os.path.join(os.path.expanduser('~'), 'Downloads')
HORA_INI, HORA_FIM = 8, 22


ULTIMO_PRODUTO = None  # (chave, título, textos) do último post com produto conferido nesta execução
SEMPRE_FAVORITAR = False  # False = pula o favoritar quando é o mesmo produto do post anterior
FILAS = os.path.join(BASE, 'filas')  # filas extras (fila_*.json) somadas depois da fila.json


def chave_produto(item):
    """Identifica o produto entre versões/dias: nome da fila normalizado (fallback: doc sem _A/_B/_C)."""
    nome = ' '.join(str(item.get('produto') or '').lower().split())
    return nome or item['doc'].rsplit('_', 1)[0]


TITULOS = os.path.join(BASE, 'titulos.json')           # itemId -> nome real, já confirmado
PULADOS = os.path.join(BASE, 'pulados.json')         # {doc, hora, motivo}: escrito pela Central
ITEMIDS = os.path.join(BASE, 'itemids.json')          # cache link -> "shopid.itemid"
CONFERIDOS = os.path.join(BASE, 'afiliados', 'conferidos.csv')  # do robô de afiliados (só leitura)
ORDEM = os.path.join(BASE, 'proxima_ordem.json')       # próximos posts com prioridade (para a Central)


def itemid_de(link, cache):
    """Segue o redirect do link curto s.shopee uma vez e tira o 'shopid.itemid' (com cache)."""
    if link in cache:
        return cache[link]
    import re, urllib.request

    class SemRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    alvo = ''
    try:
        req = urllib.request.Request(link, method='GET', headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.build_opener(SemRedirect).open(req, timeout=10)
    except urllib.error.HTTPError as e:
        alvo = e.headers.get('Location', '') or ''
    except Exception:
        return None
    caminho = alvo.split('?', 1)[0]
    m = (re.search(r'i\.(\d+)\.(\d+)', caminho) or re.search(r'/product/(\d+)/(\d+)', caminho)
         or re.search(r'/(\d{5,})/(\d{6,})/?$', caminho))  # ex.: shopee.com.br/opaanlp/SHOP/ITEM
    if not m:
        return None
    cache[link] = f'{m[1]}.{m[2]}'
    return cache[link]


def ranks_conferidos():
    """item (parte depois do ponto do itemId) -> 0 prioridade (<5 vídeos ou prioridade=sim),
    2 descartado (decisao descartado ou >15 vídeos), 1 normal."""
    import csv
    out = {}
    try:
        # formato do robô: data;itemId;link;nome;vendas;afiliados;videos;...;decisao;motivo;segundos;
        # prioridade;v7;primeira_vez;nossos_videos — decisao aprovado|revisar|descarta|erro,
        # prioridade sim|não. Vários registros do mesmo produto: vale o mais recente (por data).
        linhas = list(csv.DictReader(open(CONFERIDOS, encoding='utf-8-sig'), delimiter=';'))
        linhas.sort(key=lambda l: (l.get('data') or '').strip())
        for l in linhas:
            iid = (l.get('itemId') or '').strip()
            if not iid:
                continue
            # só as colunas do robô (ele já aplica a regra completa do Kevin, incluindo vendas)
            dec = (l.get('decisao') or '').strip().lower()
            pri = (l.get('prioridade') or '').strip().lower() == 'sim'
            if pri:
                r = 0
            elif dec.startswith('descart'):
                r = 2
            else:
                r = 1
            out[iid.split('.')[-1]] = r
    except Exception:
        pass
    return out


def ordenar_por_prioridade(pend, comecados=()):
    """Kevin 05/11: 1 vídeo de cada produto antes de repetir produto. Em rodadas: produtos com menos
    versões postadas vêm primeiro; dentro da rodada, por prioridade (0 primeiro, 2 por último; sem
    dado do robô = 1). comecados: {produto: versões já postadas}."""
    comecados = dict(comecados) if isinstance(comecados, dict) else {}
    ranks = ranks_conferidos()
    cache = carregar(ITEMIDS, {})
    grupos, ordem_grupos = {}, []
    for i in pend:
        k = chave_produto(i)
        if k not in grupos:
            grupos[k] = []
            ordem_grupos.append(k)
        grupos[k].append(i)
    rank_grupo = {}
    for k in ordem_grupos:
        r = 1
        if ranks:
            for i in grupos[k]:
                iid = itemid_de(i.get('link', ''), cache)
                if iid:
                    r = ranks.get(iid.split('.')[-1], 1)
                    break
        rank_grupo[k] = r
    try:
        json.dump(cache, open(ITEMIDS, 'w', encoding='utf-8'), indent=1)
    except Exception:
        pass
    pos = {k: n for n, k in enumerate(ordem_grupos)}
    linhas = [(comecados.get(k, 0) + n, rank_grupo[k], pos[k], n, i)
              for k in ordem_grupos for n, i in enumerate(grupos[k])]
    linhas.sort(key=lambda t: t[:4])
    saida = [t[4] for t in linhas]
    try:
        json.dump([{'doc': i['doc'], 'produto': i.get('produto'), 'rank': rank_grupo[chave_produto(i)]}
                   for i in saida[:12]], open(ORDEM, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    except Exception:
        pass
    return saida, rank_grupo


FILA_MANUAL = os.path.join(BASE, 'fila_manual.txt')
FILA_MANUAL_OK = os.path.join(BASE, 'fila_manual_importados.txt')
FILA_MANUAL_JSON = os.path.join(FILAS, 'fila_manual_auto.json')  # entra pela mesma mesclagem de fila_*.json (dedup por doc)
CABECALHO_MANUAL = """# FILA MANUAL (Kevin 21/11). Uma linha por vídeo, campos separados por |
#   VÍDEO | LINK DO PRODUTO | LEGENDA (opcional)
# VÍDEO = caminho de um .mp4 neste PC (ex.: C:\\\\Users\\\\<USUARIO>\\\\Videos\\\\meu_video.mp4) OU link do arquivo no Google Drive
#         (https://drive.google.com/file/d/XXXX/view). LINK DO PRODUTO = link da Shopee (s.shopee.com.br/... ou shopee.com.br/product/...).
# Exemplo:
#   C:\\\\Users\\\\<USUARIO>\\\\Videos\\\\cadeira.mp4 | https://s.shopee.com.br/AbCdEf123 | Cadeira linda #cadeira #casa
# Linhas começadas com # são ignoradas. A fila lê este arquivo a cada ciclo: linha boa vai para a fila e é movida para
# fila_manual_importados.txt; linha com problema fica aqui com "# ERRO: motivo" por cima. Nada trava.
"""


def _linha_manual(txt):
    """Valida UMA linha da fila manual. Devolve (item_dict, None) ou (None, motivo)."""
    partes = [p.strip() for p in txt.split('|')]
    if len(partes) < 2 or not partes[0] or not partes[1]:
        return None, 'use: VÍDEO | LINK DO PRODUTO | LEGENDA (opcional)'
    video, link = partes[0].strip('"'), partes[1]
    legenda = partes[2] if len(partes) > 2 else ''
    if not re.match(r'^https?://(s\.shopee\.com\.br/|shopee\.com\.br/)', link):
        return None, 'o link do produto precisa ser da Shopee (s.shopee.com.br/... ou shopee.com.br/product/...)'
    drive_id, local = '', ''
    m = re.search(r'drive\.google\.com/(?:file/d/|open\?id=|uc\?(?:[^ ]*&)?id=)([A-Za-z0-9_-]{20,})', video)
    if m:
        drive_id = m[1]
    elif re.match(r'^[A-Za-z]:\\', video) or video.startswith('\\\\'):
        if not video.lower().endswith('.mp4'):
            return None, 'o vídeo local precisa ser um arquivo .mp4'
        if not os.path.isfile(video):
            return None, 'não achei o arquivo de vídeo neste PC'
        local = video
    else:
        return None, 'o vídeo precisa ser um caminho do PC (C:\\...\\arquivo.mp4) ou um link do Google Drive'
    base = os.path.splitext(os.path.basename(local))[0] if local else drive_id[:10]
    slug = re.sub(r'[^a-z0-9]+', '-', ps._norm_titulo(base)).strip('-')[:40] or 'video'
    doc = f'MANUAL{datetime.date.today():%d%m}_{slug}_A'
    return {'doc': doc, 'dia': f'{datetime.date.today():%Y-%m-%d}', 'ordem': 1, 'versao': 'Shopee A',
            'produto': slug.replace('-', ' ').title(), 'drive_id': drive_id, 'link': link, 'legenda': legenda or slug.replace('-', ' '),
            '_local': local}, None


def importar_fila_manual():
    """Lê tablet\\fila_manual.txt a cada ciclo, valida, põe os itens bons em filas\\fila_manual_auto.json (mesma mesclagem/dedup
    de qualquer fila_*.json) e move as linhas importadas para fila_manual_importados.txt. Linha inválida fica com '# ERRO'."""
    if not os.path.isfile(FILA_MANUAL):
        return
    try:
        linhas = open(FILA_MANUAL, encoding='utf-8-sig').read().splitlines()
    except OSError:
        return
    if not any(l.strip() and not l.lstrip().startswith('#') for l in linhas):
        return
    atuais = carregar(FILA_MANUAL_JSON, [])
    docs = {i['doc'] for i in atuais if isinstance(i, dict)}
    novas, ficam, importadas = [], [], []
    erro_anterior = False
    for l in linhas:
        s = l.strip()
        if s.startswith('# ERRO:'):  # erro de uma passada anterior: descarta (será refeito se a linha continuar ruim)
            erro_anterior = True
            continue
        if not s or s.startswith('#'):
            ficam.append(l)
            continue
        item, motivo = _linha_manual(s)
        if item is None:
            ficam.append(f'# ERRO: {motivo}')
            ficam.append(l)
            continue
        local = item.pop('_local')
        if item['doc'] in docs:  # mesma linha já importada antes
            importadas.append(l + '   # (já estava na fila)')
            continue
        try:
            if local:
                os.makedirs(VIDEOS, exist_ok=True)
                destino = os.path.join(VIDEOS, item['doc'] + '.mp4')
                if not os.path.isfile(destino):
                    shutil.copyfile(local, destino)
        except OSError as e:
            ficam.append(f'# ERRO: não consegui copiar o vídeo ({e})')
            ficam.append(l)
            continue
        docs.add(item['doc'])
        novas.append(item)
        importadas.append(l)
    if not novas and not importadas and not erro_anterior and len(ficam) == len(linhas):
        return
    if novas:
        os.makedirs(FILAS, exist_ok=True)
        tmp = FILA_MANUAL_JSON + '.tmp'
        json.dump(atuais + novas, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, FILA_MANUAL_JSON)
    if importadas:
        with open(FILA_MANUAL_OK, 'a', encoding='utf-8') as f:
            for l in importadas:
                f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M}  {l}\n')
    tmp = FILA_MANUAL + '.tmp'
    open(tmp, 'w', encoding='utf-8').write('\n'.join(ficam) + '\n')
    os.replace(tmp, FILA_MANUAL)
    if novas:
        log(f'fila manual: {len(novas)} item(ns) importado(s) de fila_manual.txt')


def sincronizar_filas_drive():
    """Kevin 10/11: lote novo vai sozinho para a fila. Copia filas fila_*.json NOVOS/alterados de
    <Drive>\\Central Esposa para filas\\ (só se for uma lista JSON válida de itens com doc e link)."""
    try:
        origem = None
        for letra in 'GHIJKLMNOPQRSTUVWXYZDEF':
            p = f'{letra}:\\Meu Drive\\Central Esposa'
            if os.path.isdir(p):
                origem = p
                break
        if not origem:
            return
        os.makedirs(FILAS, exist_ok=True)
        for n in os.listdir(origem):
            if not (n.startswith('fila_') and n.endswith('.json')):
                continue
            src, dst = os.path.join(origem, n), os.path.join(FILAS, n)
            if os.path.isfile(dst) and os.path.getsize(dst) == os.path.getsize(src):
                continue
            dados = json.load(open(src, encoding='utf-8-sig'))
            if not (isinstance(dados, list) and dados and all(isinstance(i, dict) and i.get('doc') and i.get('link')
                                                               for i in dados)):
                log(f'  (fila nova {n} do Drive ignorada: formato inválido)')
                continue
            tmp = dst + '.tmp'
            shutil.copyfile(src, tmp)
            os.replace(tmp, dst)
            log(f'  fila nova do Drive: {n} ({len(dados)} itens) copiada para filas\\')
    except Exception as e:
        log(f'  (sincronizar filas do Drive falhou: {e})')


def carregar_filas():
    """fila.json + filas\\fila_*.json (em ordem de nome), sem repetir doc."""
    todas, vistos = [], set()
    # 16/11: "fila_<lote>_v2.json" (edições refeitas) vale ANTES da versão antiga do mesmo lote: o doc repetido fica
    # com o drive_id novo (a ordem decide quem ganha, pois o 1º doc visto vence).
    extras = sorted((os.path.join(FILAS, n) for n in os.listdir(FILAS)
                     if n.startswith('fila_') and n.endswith('.json')),
                    key=lambda c: (0 if re.search(r'_v\d+\.json$', c) else 1, os.path.basename(c))) if os.path.isdir(FILAS) else []
    for caminho in [FILA, *extras]:
        for i in carregar(caminho, []):
            if i.get('doc') and i['doc'] not in vistos:
                vistos.add(i['doc'])
                todas.append(i)
    return todas


class Erro(Exception):
    pass


def log(msg):
    linha = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}'
    PASSO['t'] = time.time()
    with open(LOG, 'a', encoding='utf-8') as f:  # arquivo primeiro: a janela pode travar o print
        f.write(linha + '\n')
    print(linha, flush=True)


# Vigia de passo (dentro da fila). Um passo parado mais de 90 s antes de Postar: fecha a Shopee e
# encerra com erro comum (o vigia_postagem religa e refaz o post do zero, 1 vez). Na 2ª trava do mesmo
# post, ou parada longa depois de Postar, encerra sem religar. Clicar na janela preta congelava o print
# (seleção do console); desligar_quickedit() evita isso.
PASSO = {'ativo': False, 'doc': None, 't': 0.0}
TRAVOU = os.path.join(BASE, 'travou.json')
LIMITE_PASSO, LIMITE_POS_POSTAR, LIMITE_SEM_MUDANCA = 90, 1020, 20


def desligar_quickedit():
    try:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.GetStdHandle(-10)
        modo = ctypes.c_uint32()
        if k.GetConsoleMode(h, ctypes.byref(modo)):
            k.SetConsoleMode(h, (modo.value | 0x80) & ~0x40)
    except Exception:
        pass


def fechar_shopee():
    try:
        ps._exec([*ps.ADB_CMD, 'shell', f'am force-stop {ps.PKG}'], 15)
    except Exception:
        pass


def travou_e_sai():
    doc, tocou = PASSO['doc'], ps.TOCOU_POSTAR
    try:
        ps.print_tela('erro_travou.png')  # mostra em que tela parou
    except Exception:
        pass
    cont = carregar(TRAVOU, {})
    cont[doc] = cont.get(doc, 0) + 1
    json.dump(cont, open(TRAVOU, 'w', encoding='utf-8'))
    if tocou:
        ps.registrar(doc, 'incerto', 'travou depois de tocar em Postar')
        txt = f'INCERTO: travou depois de tocar em Postar (pode ter postado); confira no perfil'
    elif cont[doc] >= 2:
        fechar_shopee()
        txt = 'não postado: travou 2x no mesmo post; bloqueado até você olhar'
    else:
        fechar_shopee()
        txt = f'não postado: sem progresso há {LIMITE_SEM_MUDANCA} s; Shopee fechada, refazer o post'
    with open(ERRO, 'w', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\ndoc: {doc}\n{txt}\n')
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} PAROU: {txt}\n')
    os._exit(3)


def assinatura_tela():
    """Tela reduzida, sem a barra de status (o relógio muda sozinho). None se não der para ler."""
    import io
    raw = ps._exec([*ps.ADB_CMD, 'exec-out', 'screencap', '-p'], 10).stdout
    im = ps.Image.open(io.BytesIO(raw)).convert('L')
    w, h = im.size
    return im.crop((0, 90, w, h - 110)).resize((32, 56)).tobytes()


def vigia_de_passo():
    """Kevin 06/11: sem passo novo no log E sem a tela mudar por 20 s = travou. Tela mudando (vídeo,
    carregamento, upload) espera até o limite maior. Captcha/login/PIN e envio do vídeo não contam."""
    anterior, tela_mudou = None, time.time()
    while True:
        time.sleep(4)
        if not PASSO['ativo'] or ps.EM_CAPTCHA or ps.OCUPADO:
            anterior, tela_mudou = None, time.time()
            continue
        agora = time.time()
        try:
            sig = assinatura_tela()
            if anterior is None or sum(abs(a - b) for a, b in zip(sig, anterior)) / len(sig) > 1.5:
                tela_mudou = agora
            anterior = sig
        except Exception:
            tela_mudou = agora  # sem leitura não conclui que travou (o limite maior vale)
        if ps.TOCOU_POSTAR:  # upload pode segurar a mesma tela: nunca chama de incerto por 20 s
            if agora - PASSO['t'] > LIMITE_POS_POSTAR:
                travou_e_sai()
        # trava = sem nenhum sinal de vida (adb/leitura/log) E tela parada por 20 s
        elif agora - max(PASSO['t'], tela_mudou, ps.BATIMENTO) > LIMITE_SEM_MUDANCA:
            travou_e_sai()
        elif agora - PASSO['t'] > LIMITE_PASSO and agora - tela_mudou > LIMITE_SEM_MUDANCA:
            travou_e_sai()  # script rodando em círculo: sem passo novo há 90 s e tela parada


def carregar(caminho, padrao):
    try:
        return json.load(open(caminho, encoding='utf-8'))
    except Exception:
        return padrao


def estado():
    """doc -> último resultado no postados.json."""
    est = {}
    for e in carregar(POSTADOS, []):
        r = e.get('resultado') or e.get('status') or ''
        if est.get(e['doc'], '').startswith('postado'):
            continue  # postado nunca é rebaixado
        est[e['doc']] = r
    return est


def escrever_sync():
    vistos, out = set(), []
    for e in carregar(POSTADOS, []):
        r = e.get('resultado') or e.get('status') or ''
        if r.startswith('postado') and e['doc'] not in vistos:
            vistos.add(e['doc'])
            out.append({'doc': e['doc'], 'postado_em': e.get('utc')})
    json.dump(out, open(SYNC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    escrever_postados_nuvem(out)


NUVEM_POSTADOS = None  # caminho do postados_pc_nuvem.json no Drive (achado 1x)
_APARELHO_DOC = {}     # doc -> celular que postou (preenchido aqui; o que já estava no arquivo é mantido)


def escrever_postados_nuvem(postados):
    """22/11 (retorno PC->nuvem): SOBRESCREVE NO LUGAR (open 'w', sem apagar/recriar/os.replace: mantém o id do Drive)
    G:\\Meu Drive\\Central Esposa\\postados_pc_nuvem.json com todos os docs postados. Falha só vai para o log, nunca trava a fila."""
    global NUVEM_POSTADOS
    try:
        if not NUVEM_POSTADOS:
            for letra in 'GHIJKLMNOPQRSTUVWXYZDEF':
                p = f'{letra}:\\Meu Drive\\Central Esposa\\postados_pc_nuvem.json'
                if os.path.isfile(p):
                    NUVEM_POSTADOS = p
                    break
        if not NUVEM_POSTADOS:
            return
        if not _APARELHO_DOC:  # aparelho já gravado em versões anteriores do arquivo
            with contextlib.suppress(Exception):
                for x in json.load(open(NUVEM_POSTADOS, encoding='utf-8-sig')).get('postados', []):
                    if x.get('doc') and x.get('aparelho'):
                        _APARELHO_DOC[x['doc']] = x['aparelho']
        lista = [{'doc': x['doc'], 'postado_em': x.get('postado_em'), 'aparelho': _APARELHO_DOC.get(x['doc'])} for x in postados]
        doc = {'atualizado_em': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'postados': lista}
        txt = json.dumps(doc, ensure_ascii=False)
        with open(NUVEM_POSTADOS, 'w', encoding='utf-8') as f:
            f.write(txt)
    except Exception as e:
        log(f'  (postados_pc_nuvem.json não atualizado: {e})')


def alertar(msg):
    """Som só quando precisa do Kevin (captcha, PIN/tela bloqueada, login): sons\\atencao.wav via
    alerta.alerta_kevin. Demais erros: sem som, só o aviso visual no painel/Central."""
    if not any(k in str(msg).lower() for k in ('captcha', 'bloquead', 'pin/', 'login')):
        return
    try:
        from alerta import alerta_kevin
        alerta_kevin(str(msg).split('\n')[0])
    except Exception:
        pass


def arquivo_erro():
    """Celular 1 continua no erro.txt (vigia e Central). O outro celular não derruba o primeiro."""
    if ID_FILA == 'celular1':
        return ERRO
    return os.path.join(BASE, f'erro_{ID_FILA}.txt')


def parar_com_erro(msg, doc=None):
    try:
        nome = f'erro_fila_{doc or "geral"}.png'
        ps.print_tela(nome)
        msg += f'\nprint: {os.path.join(ps.PASTA, nome)}'
    except Exception as e:
        msg += f'\n(sem print: {e})'
    with open(arquivo_erro(), 'w', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\ndoc: {doc}\n{msg}\n')
    log('PAROU: ' + msg.replace('\n', ' | '))
    alertar(f'Post: {doc}\n\n{msg.split(chr(10) + "Traceback")[0]}')
    sys.exit(1)


# ---------- download ----------

def mp4s():
    return {n: os.path.getsize(os.path.join(DOWNLOADS, n)) for n in os.listdir(DOWNLOADS)
            if n.lower().endswith('.mp4')}


PASTA_DRIVE = ('Meu Drive', 'My Drive')
INDICE_DRIVE = {}  # pasta do dia -> {nome.mp4: caminho}


def video_valido(caminho):
    """Tamanho mínimo e cabeçalho de mp4 (ftyp)."""
    try:
        if os.path.getsize(caminho) < 100 * 1024:
            return False
        with open(caminho, 'rb') as f:
            return f.read(12)[4:8] == b'ftyp'
    except OSError:
        return False


def pasta_videos_do_dia(doc):
    """doc 0411B_... -> ...\\Videos Esposa\\2026-11-04 (DDMM do início do nome)."""
    m = re.match(r'(\d\d)(\d\d)', doc)
    if not m:
        return None
    ano = datetime.date.today().year
    for letra in 'GHIJKLMNOPQRSTUVWXYZDEF':
        for raiz in PASTA_DRIVE:
            for nome in ('Videos Esposa', 'Fabrica Videos'):  # Paola 23/11: a fábrica dela sobe em "Fabrica Videos"
                p = f'{letra}:\\{raiz}\\{nome}\\{ano}-{m[2]}-{m[1]}'
                if os.path.isdir(p):
                    return p
    return None


def copiar_do_drive(item, destino):
    """Copia o vídeo pela pasta do Google Drive para computador. False se não achar."""
    pasta = pasta_videos_do_dia(item['doc'])
    if not pasta:
        return False
    if pasta not in INDICE_DRIVE:  # lista a pasta do dia uma vez por execução
        ind = {}
        for raiz, _, nomes in os.walk(pasta):
            for n in nomes:
                if n.lower().endswith('.mp4'):
                    ind.setdefault(n, os.path.join(raiz, n))
        INDICE_DRIVE[pasta] = ind
    origem = INDICE_DRIVE[pasta].get(item['doc'] + '.mp4')
    if not origem:
        return False
    os.makedirs(VIDEOS, exist_ok=True)
    temp = destino + '.parte'
    shutil.copyfile(origem, temp)
    if os.path.getsize(temp) != os.path.getsize(origem) or not video_valido(temp):
        os.remove(temp)
        raise Erro(f'cópia do Drive inválida: {origem}')
    os.replace(temp, destino)
    return True


def abrir_navegador_escondido(url):
    """Reserva: abre minimizado e fora da tela, sem roubar o foco."""
    opera = os.path.expandvars(r'%LOCALAPPDATA%\Programs\Opera GX\opera.exe')
    try:
        import subprocess
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = 7  # SW_SHOWMINNOACTIVE
        subprocess.Popen([opera, '--window-position=-32000,-32000', url], startupinfo=info)
    except Exception:
        os.startfile(url)


def baixar_quieto(item):
    """Download adiantado: se falhar, o ciclo desse post baixa de novo (e aí sim avisa)."""
    try:
        baixar(item, 'próximo: ')
    except Exception as e:
        log(f'  (download adiantado falhou: {e})')


def baixar(item, rotulo=''):
    pronto = os.path.join(VIDEOS, item['doc'] + '.mp4')
    if os.path.isfile(pronto) and os.path.getsize(pronto) > 0:
        log(f'  vídeo já baixado: {pronto}')
        return pronto
    # 1º: Google Drive para computador (sem navegador). Só cai no navegador se não achar.
    try:
        copia = copiar_do_drive(item, pronto)
        if copia:
            log(f'  {rotulo}baixado via Drive: {os.path.basename(pronto)} ({os.path.getsize(pronto) // 1024} KB)')
            return pronto
    except Exception as e:
        log(f'  (Drive falhou: {e}; indo pelo navegador)')
    antes = set(mp4s())
    url = (f'https://drive.usercontent.google.com/download?id={item["drive_id"]}'
           f'&export=download&confirm=t')
    abrir_navegador_escondido(url)
    fim = time.time() + 600
    novo, tam, estavel = None, -1, 0
    while time.time() < fim:
        time.sleep(3)
        baixando = any(n.endswith(('.crdownload', '.part', '.tmp')) for n in os.listdir(DOWNLOADS))
        agora = mp4s()
        novos = [n for n in agora if n not in antes]
        if not novos:
            continue
        novo = max(novos, key=lambda n: os.path.getmtime(os.path.join(DOWNLOADS, n)))
        if agora[novo] == tam and agora[novo] > 0 and not baixando:
            estavel += 1
            if estavel >= 3:
                break
        else:
            estavel, tam = 0, agora[novo]
    else:
        raise Erro(f'download não terminou em 10 min (drive_id {item["drive_id"]})')
    os.makedirs(VIDEOS, exist_ok=True)
    destino = os.path.join(VIDEOS, item['doc'] + '.mp4')
    shutil.move(os.path.join(DOWNLOADS, novo), destino)
    if not video_valido(destino):
        os.remove(destino)
        raise Erro(f'o vídeo baixado pelo navegador não é um mp4 válido: {novo}')
    log(f'  {rotulo}baixado pelo navegador: {novo} ({tam // 1024} KB) -> {destino}')
    return destino


# ---------- conferência no perfil ----------

def tela_perfil(im):
    """Perfil da conta principal: fundo branco na área do nome e botão laranja '+ Postar vídeo' embaixo."""
    return (ps.e_branco(ps.cor(im, *ps.P('perfil_br1', 400, 300))) and ps.e_branco(ps.cor(im, *ps.P('perfil_br2', 400, 100)))
            and ps.e_laranja(ps.cor(im, *ps.P('perfil_lar1', 600, 1140))) and ps.e_laranja(ps.cor(im, *ps.P('perfil_lar2', 750, 1156))))


def abrir_perfil():
    # O toque no ícone de perfil sobre uma live às vezes não pega: confere por pixel e repete.
    for tentativa in range(6):
        if tela_perfil(ps.print_tela()):  # pode ter aberto atrasado na tentativa anterior
            time.sleep(2)
            return
        if tentativa % 3 == 0:
            ps.sh(f'am start -n {ps.PKG}/com.shopee.app.ui.home.HomeActivity_')
            time.sleep(2)
            ps.ir_para_live()
        x, y = ps.P('icone_perfil', 35, 42)
        ps.sh(f'input swipe {x} {y} {x} {y} 120')
        fim = time.time() + 15
        while time.time() < fim:
            if tela_perfil(ps.print_tela()):
                return
            time.sleep(0.5)
    raise Erro('conferência: não consegui abrir o perfil <SEU_PERFIL>')


def _conferir_pelo_perfil(video, doc):
    ps.detectar_perfil()
    if ps.PERFIL != 'tablet':  # miniaturas da 1ª linha da grade no celular (720x1600)
        conferir.TILES = [(0, 748, 239, 1064), (241, 748, 479, 1064), (481, 748, 720, 1064)]
    abrir_perfil()

    def grade_carregada(fim_s=8):  # espera a 1ª miniatura sair do branco, em vez de espera fixa
        fim = time.time() + fim_s
        while True:
            tela = ps.print_tela(f'conf_grid_{doc}.png')
            mini = tela.crop(conferir.TILES[0]).convert('L').resize((16, 16)).tobytes()
            if sum(mini) / len(mini) < 235 or time.time() > fim:
                return tela
            time.sleep(0.4)

    qs = conferir.quadros(video)  # extrai os quadros uma vez só
    for n in range(45):  # ~1 s por rodada; sem reabrir o perfil. Puxa para atualizar a cada 8 s
        tela = grade_carregada()
        d = conferir.distancias(tela, video, qs)
        if d[0] < 15 and d[0] < d[1]:
            log(f'  conferência ({n + 1} leituras): distâncias das miniaturas = {[round(x, 1) for x in d]}')
            break
        if n % 8 == 7:
            ps.sh('input swipe %d %d %d %d 400' % (*ps.P('puxar_de', 400, 650), *ps.P('puxar_ate', 400, 1100)))
        time.sleep(0.7)
    else:
        log(f'  conferência: distâncias finais = {[round(x, 1) for x in d]}')
        raise Erro('conferência: a 1ª miniatura do perfil não bate com o vídeo novo '
                   f'(ver gravacao\\conf_grid_{doc}.png)')
    ps.toque(*ps.P('video1', 133, 715), espera=1)  # abre o vídeo novo
    if ps.PERFIL != 'tablet':  # o 1º toque pode se perder: repete até o player abrir
        for _ in range(6):
            time.sleep(1.5)
            if 'NativePlayerActivity' in ps.sh('dumpsys window | grep mCurrentFocus'):
                break
            if _ % 2 == 1:
                ps.toque(*ps.P('video1', 133, 715), espera=1)
        else:
            raise Erro('conferência: o vídeo não abriu no player')
    log('  conferência ok: vídeo novo é o 1º do perfil')
    _conferir_aberto(video, doc, time.time())  # o player abriu: daqui conta a reprodução


def conferir_no_perfil(video, doc):
    """Plano A: o vídeo já foi aberto tocando no aviso "Enviado com sucesso!" (ps.VIDEO_PELA_NOTIF).
    Plano B (aviso não pegou ou miniatura não bate): abre pelo perfil."""
    ps.detectar_perfil()
    via, ps.VIDEO_PELA_NOTIF = ps.VIDEO_PELA_NOTIF, None
    if via:
        try:
            qs = conferir.quadros(video)
            d = min(conferir.dist(conferir._norm(via['thumb']), q) for q in qs) if qs else 999
            log(f'  PLANO A (aviso "Enviado com sucesso!"): miniatura do aviso x vídeo = {d:.1f}')
            if d < 70:  # 10/11: a capa do aviso tem texto por cima (51 num vídeo certo); o produto é conferido a seguir
                return _conferir_aberto(video, doc, via['t'])
            log('  miniatura do aviso não bate com o vídeo: saindo do player e indo pelo perfil (plano B)')
        except (ProdutoErrado, ProdutoIncerto):  # 12/11: produto ilegível NÃO reabre o vídeo pelo perfil
            raise
        except Exception as e:
            log(f'  plano A falhou ({e}); indo pelo perfil (plano B)')
        for _ in range(2):
            f = ps.sh('dumpsys window | grep mCurrentFocus')
            if 'NativePlayerActivity' not in f and 'ReactActivity' not in f:
                break
            ps.sh('input keyevent KEYCODE_BACK')
            time.sleep(1.2)
    else:
        tocado, ps.AVISO_TOCADO = getattr(ps, 'AVISO_TOCADO', None), None
        if tocado:
            # 12/11 (Kevin: "abre o vídeo, assiste pela metade, volta e assiste inteiro"): o toque no aviso às
            # vezes abre o player DEPOIS da janela de espera. Antes de ir pelo perfil, olha se ele abriu; se
            # abriu, segue a conferência nele mesmo (mesma regra do plano A: miniatura do aviso x vídeo).
            fim, f = time.time() + 3, ''
            while time.time() < fim:
                f = ps.foco()
                if 'NativePlayerActivity' in f or 'ReactActivity_' in f:
                    break
                time.sleep(0.4)
            if 'NativePlayerActivity' in f or 'ReactActivity_' in f:
                try:
                    qs = conferir.quadros(video)
                    d = min(conferir.dist(conferir._norm(tocado['thumb']), q) for q in qs) if qs else 999
                    log(f'  PLANO A (atrasado): o vídeo abriu depois do toque no aviso; miniatura x vídeo = {d:.1f}')
                    if d < 70:
                        return _conferir_aberto(video, doc, max(tocado['t'] + 1.0, time.time() - 6))
                except (ProdutoErrado, ProdutoIncerto):
                    raise
                except Exception as e:
                    log(f'  plano A atrasado falhou ({e})')
                for _ in range(2):  # não é o vídeo certo / falhou: sai do player antes de ir pelo perfil
                    f = ps.foco()
                    if 'NativePlayerActivity' not in f and 'ReactActivity' not in f:
                        break
                    ps.sh('input keyevent KEYCODE_BACK')
                    time.sleep(1.2)
        log('  PLANO B: aviso "Enviado com sucesso!" não pegou; abrindo pelo perfil')
    return _conferir_pelo_perfil(video, doc)


def _conferir_aberto(video, doc, t_abriu):
    # Kevin 10/11: confere "Ver Produtos" durante o play (o vídeo continua rodando), mas só sai do vídeo
    # quando o tempo todo desde a abertura do player (duração + 1 s) tiver passado.
    ps.print_tela(f'conf_tocando_{doc}.png')
    # 12/11 (Kevin: "assistir e conferir o produto no mesmo clique"): a conferência do produto acontece com o
    # vídeo aberto e, dê certo ou errado, o robô termina de assistir NESTE player (nada de voltar e abrir de novo).
    erro_produto = None
    try:
        conferir_produto(doc)
    except (ProdutoErrado, ProdutoIncerto) as e:
        erro_produto = e
    try:
        r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'default=nw=1:nk=1', video], capture_output=True, text=True, timeout=20,
                           creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        dur = float((r.stdout or '0').strip() or 0)
    except Exception:
        dur = 15.0
    # Kevin 10/11 ("sapateira: não terminou de assistir e fechou"): a conferência do produto abre o painel por cima
    # do vídeo (pausa/cobre a reprodução), então contar desde a abertura do player cortava o final. Agora a espera
    # é a duração inteira + 1,5 s a partir do FIM da conferência (painel fechado, vídeo à vista), e só sai se o
    # player ainda estiver aberto; nenhum watchdog/regra corta essa espera.
    PASSO['t'] = time.time()
    # 12/11: antes esperava a duração INTEIRA depois da conferência, além do que já tinha tocado antes do painel
    # abrir (o vídeo era visto 1,5 vez). Agora desconta o que tocou entre abrir o player e tocar no produto (o
    # painel cobre/pausa o vídeo, regra de 10/11 da sapateira): no total o vídeo passa 1 vez inteira.
    ja_tocou = max(0.0, min(CONF_PRODUTO.get('t_toque') or t_abriu, time.time()) - t_abriu)
    ja_tocou = max(ja_tocou, CONF_PRODUTO.get('play_s') or 0.0)  # 20/11: tempo de reprodução medido (vídeo se movendo)
    # Kevin 12/11 05:43: +3 s de folga no desconto (o player demora um pouco a começar a tocar de verdade)
    total = max(1.0, min(48.0, (dur or 15.0) + 1.5 + 3.0 - ja_tocou))
    log(f'  assistindo até o fim: mais {total:.0f} s (vídeo de {dur:.0f} s; já tocou {ja_tocou:.0f} s antes do painel)')
    fim = time.time() + total
    while time.time() < fim:
        time.sleep(min(2.0, max(0.1, fim - time.time())))
        PASSO['t'] = time.time()  # mantém o vigia de passo satisfeito durante a reprodução
        manter_tela_acesa()
    foco_fim = ps.sh('dumpsys window | grep mCurrentFocus')
    log(f'  assistiu até o fim (foco: {foco_fim.strip()[-60:]})')
    if erro_produto:
        raise erro_produto


class ProdutoIncerto(Exception):
    """Pós-post: não deu para LER o nome do produto vinculado (≠ produto errado). Não para a fila: vira pendência
    "Conferir produto vinculado" na Central para o Kevin olhar no perfil (regra 10/11: na dúvida, avisa e segue)."""


class ProdutoErrado(Exception):
    pass


def _norm_txt(s):
    return ' '.join(s.replace('&amp;', '&').split()).lower()


def titulo_do_painel(vis):
    return ps.titulo_de(vis)


def mesmo_titulo(a, b):
    return ps.mesmo_nome(a, b)  # mesma regra da lista "Minhas Curtidas"


def faixa_produto(im):
    """Faixa do produto vinculado no vídeo: sacolinha laranja à esquerda (celular, y~1188)."""
    return sum(1 for x in range(32, 74, 3) for y in range(1166, 1208, 3) if ps.e_laranja(ps.cor(im, x, y))) >= 25


ATENCAO = os.path.join(BASE, 'central', 'prints_atencao')  # prints dos registros que pedem atenção: nenhuma limpeza apaga


def guardar_print(doc, *nomes):
    """Copia o 1º print que existir (nomes dentro de gravacao\\) para central\\prints_atencao\\<doc>_<hora>.png e devolve
    o caminho estável ('' se nenhum existir). Kevin 14/11: "ver print" dava {"erro":"não encontrado"}."""
    try:
        os.makedirs(ATENCAO, exist_ok=True)
        for n in nomes:
            src = n if os.path.isabs(n) else os.path.join(ps.PASTA, n)
            if os.path.isfile(src) and os.path.getsize(src) > 0:
                dst = os.path.join(ATENCAO, f'{doc}_{datetime.datetime.now():%Y%m%d_%H%M%S}.png')
                shutil.copyfile(src, dst)
                return dst
    except Exception as e:
        log(f'  (guardar print falhou: {e})')
    return ''


PRINT_CHECK = {}  # doc -> caminho estável da print tirada NO MOMENTO da leitura do painel "Ver Produtos"


def print_util(im):
    """False para frame preto/quase uniforme (desvio padrão baixo)."""
    try:
        from PIL import ImageStat
        return ImageStat.Stat(im.convert('L')).stddev[0] > 12
    except Exception:
        return True


def capturar_bom(doc):
    """Print da tela do pós-check (a mesma tela lida pelo painel/OCR). Até 3 capturas: descarta frame preto/uniforme.
    Salva em gravacao\\conf_produto_<doc>.png e guarda a cópia estável em central\\prints_atencao (PRINT_CHECK)."""
    im = None
    for _ in range(3):
        try:
            im = ps.print_tela(f'conf_produto_{doc}.png')
        except Exception:
            im = None
        if im is not None and print_util(im):
            break
        time.sleep(0.7)
    PRINT_CHECK[doc] = guardar_print(doc, f'conf_produto_{doc}.png')
    return im


def nome_compativel(lida, esperado):
    """Nome lido (parcial/truncado/com outra redação) COMPATÍVEL com o título esperado: >= 75% das palavras próprias
    da leitura existem no título esperado (ou >= 88% de semelhança no começo). Só 'claramente diferente' alarma."""
    import difflib
    a, b = ps._norm_titulo(lida or ''), ps._norm_titulo(esperado or '')
    if not a or not b:
        return False
    stop = {'para', 'com', 'modelo', 'de', 'do', 'da', 'em', 'e', 'a', 'o', 'por'}
    pa = [w for w in a.split() if len(w) >= 3 and w not in stop]
    pb = {w[:5] for w in b.split() if len(w) >= 3}
    if len(pa) >= 3 and sum(1 for w in pa if w[:5] in pb) / len(pa) >= 0.75:
        return True
    n = min(len(a), len(b))
    return n >= 25 and difflib.SequenceMatcher(None, a[:n], b[:n]).ratio() >= 0.88


def pendencia_vinculo(doc, motivo, tipo='incerto'):
    """Post publicado cujo produto não deu para confirmar. SÓ o produto claramente errado (tipo='errado') vira aviso
    vermelho na Central; leitura vazia/incerta/falha de conferência vai em silêncio para pos_check_nao_confirmado.csv
    (Kevin 18/11: avisos demais, a maioria falso alarme)."""
    silencioso = tipo != 'errado'
    caminho = os.path.join(BASE, 'pos_check_nao_confirmado.csv' if silencioso else 'conferir_vinculo.csv')
    novo = not os.path.exists(caminho)
    estavel = PRINT_CHECK.pop(doc, '') or guardar_print(doc, f'conf_produto_{doc}.png', f'conf_tocando_{doc}.png',
                                                         f'conf_grid_{doc}.png', f'erro_fila_{doc}.png')
    with open(caminho, 'a', encoding='utf-8') as f:
        if novo:
            f.write('hora;doc;motivo;print\n')
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S};{doc};{motivo.replace(';', ',')[:200]};"
                f"{estavel or os.path.join(ps.PASTA, f'conf_produto_{doc}.png')}\n")
    log(f'  {"pós-check não confirmado (silencioso)" if silencioso else "pendência para o Kevin: conferir produto vinculado"} '
        f'de {doc} ({motivo[:120]})')


LIXO_CARTAO = re.compile(r'(@|Adicionar um coment|Identificado como|Pesquisar)|.*Veja mais'
                         # 12/11: cabeçalho dos recomendados lido como "nome do produto" (monitor, gabinete):
                         r'|(voc[eê] tamb[eé]m pode gostar|produtos? (similares|semelhantes|relacionados)|recomendad)', re.I)
RE_ROTULO = re.compile(r'(ver produtos|click video|gasto m[ií]nimo)', re.I)
RE_PROMO = re.compile(r'\d+\s*%|desconto|cupom|frete|r\$\s*\d|\bvendid|avalia|oferta', re.I)
CONF_PRODUTO = {'t_toque': None, 'play_s': 0.0}  # hora do toque na faixa do produto (o painel cobre o vídeo a partir daí)


_QUADRO = {'im': None}


def _quadro_mudou(im):
    """20/11: True se o centro da tela mudou desde o print anterior (= o vídeo está tocando; carregando fica parado)."""
    try:
        a = im.crop((60, 250, 660, 1050)).convert('L').resize((60, 80))
        ant, _QUADRO['im'] = _QUADRO['im'], a
        if ant is None:
            return False
        pa, pb = list(a.getdata()), list(ant.getdata())
        return sum(abs(x - y) for x, y in zip(pa, pb)) / len(pa) > 2.5
    except Exception:
        return False


def manter_tela_acesa():
    """20/11: a conferência fica 1 min sem tocar na tela e o celular apagava: acorda (inofensivo com a tela acesa)."""
    try:
        ps.sh('input keyevent KEYCODE_WAKEUP')
    except Exception:
        pass


def ler_cartao(doc):
    """Celular: lê SÓ o produto vinculado ao vídeo. Toca na faixa do produto: abre a folha do
    vídeo, onde o uiautomator lê o nome. Não rola nada (rolando aparecem os recomendados).
    Se abrir a página do produto, usa só o nome ao lado de "Vendido". Tenta 2x; ilegível = []."""
    CONF_PRODUTO['play_s'] = 0.0
    _QUADRO['im'] = None
    t_fim_total = time.time() + 45  # 20/11: orçamento TOTAL (antes 3x20 s = 60 s parado + 20 s assistindo = ~4 voltas do vídeo)
    t_acordou = 0.0
    for tentativa in range(3):  # 18/11: 3 tentativas (antes 2): "faixa não apareceu em 20 s" era a causa de 11 de 30 avisos
        if tentativa and time.time() >= t_fim_total:
            break
        fim = min(time.time() + 20, max(t_fim_total, time.time() + 6))  # faixa com a sacolinha laranja: 0,5 s por vez
        faixa = False
        while time.time() < fim and not faixa:
            t_p = time.time()
            im_p = ps.print_tela()
            faixa = faixa_produto(im_p)
            if _quadro_mudou(im_p):  # só conta como "assistindo" o tempo em que o vídeo realmente se move
                CONF_PRODUTO['play_s'] += min(1.5, time.time() - t_p + 0.5)
            PASSO['t'] = time.time()
            if time.time() - t_acordou > 8:
                manter_tela_acesa()
                t_acordou = time.time()
            if not faixa:
                time.sleep(0.5)
        log(f'  faixa do produto {"apareceu" if faixa else "não apareceu"}'
            f' (vídeo tocou ~{CONF_PRODUTO["play_s"]:.0f} s até aqui)')
        if not faixa:  # sem a faixa não toca: poderia abrir outra tela
            continue
        if not CONF_PRODUTO.get('t_toque'):
            CONF_PRODUTO['t_toque'] = time.time()
        ps.sh('input tap 300 1188')
        fim, f = time.time() + 6, ''
        while time.time() < fim:
            f = ps.foco()
            if 'ReactTransparentActivity' in f or 'HalfPdpActivity' in f:
                break
            time.sleep(0.3)
        time.sleep(0.8)
        vis, _ = ps.textos_na_tela()
        vis = [re.sub('[​-‍﻿]', '', v) for v in vis]
        capturar_bom(doc)  # 18/11: a print do aviso é a tela real da leitura (painel aberto), sem frame preto
        if 'HalfPdpActivity' in f:
            t = ps.titulo_de(vis) if any('Vendido' in v for v in vis) else None
            nomes = [t] if t else []
        elif 'ReactTransparentActivity' not in f:
            nomes = []  # abriu outra tela: não lê nome nenhum daqui
        else:
            nomes = [v for v in vis if len(v) >= 15 and not ps.UI_NAO_E_NOME.match(v.strip())
                     and not LIXO_CARTAO.match(v.strip())]
        if 'ReactTransparentActivity' in f and ps.TITULO_ESPERADO and not any(
                ps.mesmo_nome(n, ps.TITULO_ESPERADO) for n in nomes):
            # 12/11: o dump às vezes não traz o nome do produto vinculado: lê o print com o OCR do Windows
            # e fica só com linhas que têm >= 2 palavras do nome esperado (a comparação depois é a mesma).
            ocr = [x for v in ps.ler_tela_ocr() for x in (v, re.sub(r'^\S{1,2}\s+', '', v))]
            extra = [v for v in ocr if ps._tem_palavras_do_nome(v, ps.TITULO_ESPERADO)]
            if extra:
                log(f'  cartão do vídeo pelo OCR: {extra[:2]}')
                nomes = extra + nomes
        log(f'  cartão do vídeo ({f.split("/")[-1].strip(" }")[:28]}): {nomes[:3]}')
        # 12/11: só rótulos ("Ver Produtos (1)", "click video...", promoção) não contam como leitura: tenta a 2ª vez
        if any(not RE_ROTULO.match(n.strip()) and not RE_PROMO.search(n) for n in nomes):
            return nomes
        ps.sh('input keyevent KEYCODE_BACK')
        time.sleep(1.5)
    return []


GENERICAS = set('para com sala kit jantar cadeira cadeiras mesa perfume arabe conjunto'.split())


def palavras(texto):
    return [w for w in ps._norm_titulo(texto).split() if len(w) >= 4]


def distintivas(item, fila):
    """Palavras que só este produto tem na fila ("cherry", "hawas"): evita "Perfume Árabe X" passar por Y."""
    outras = set()
    k = chave_produto(item)
    for i in fila:
        if chave_produto(i) != k:
            outras.update(palavras(str(i.get('produto') or '')))
    return [w for w in palavras(str(item.get('produto') or '')) if w not in outras and w not in GENERICAS]


def produto_bate(item, titulo, fila):
    """None se o título da loja é deste item da fila; senão o motivo."""
    t = ps._norm_titulo(titulo or '')
    if not t:
        return 'sem nome na página'
    base = palavras(str(item.get('produto') or ''))
    chaves = [w for w in base if w not in GENERICAS] or base
    if chaves and sum(1 for w in chaves if w[:5] in t) / len(chaves) < 0.34:
        return f'{titulo[:50]!r} não parece {item.get("produto")!r}'
    dist = distintivas(item, fila)
    if dist and not any(w[:5] in t for w in dist):
        return f'{titulo[:50]!r} não tem {dist[:3]} de {item.get("produto")!r}'
    return None


def parece(item, titulo):
    """Conferência folgada (o nome da loja difere do da fila): pelo menos 1/4 das palavras próprias."""
    t = ps._norm_titulo(titulo or '')
    base = palavras(str(item.get('produto') or ''))
    chaves = [w for w in base if w not in GENERICAS] or base
    return bool(t) and (not chaves or sum(1 for w in chaves if w[:5] in t) / len(chaves) >= 0.25)


def validador_de_pagina(item, cache):
    fila = carregar_filas()
    anterior = ULTIMO_PRODUTO[1] if ULTIMO_PRODUTO and ULTIMO_PRODUTO[0] != chave_produto(item) else None

    def validar(titulo, vis):
        if anterior and titulo and ps.mesmo_nome(titulo, anterior):
            return f'ainda é a página do post anterior ({titulo[:50]!r})'
        if ps.TITULO_APROVADO:  # Kevin já aprovou este itemId (página abriu pelo ID): não reprova o nome de novo
            return None
        if cache:
            return None if ps.mesmo_nome(titulo or '', cache) else \
                f'{(titulo or "")[:50]!r} difere do nome confirmado {cache[:50]!r}'
        if not titulo:
            return 'sem nome na página'
        return None if parece(item, titulo) else f'{titulo[:50]!r} não parece {item.get("produto")!r}'
    return validar


def fechar_painel_produto():
    """12/11: fecha só o painel do produto e PARA no player (antes eram 2 BACK fixos: o 2º saía do vídeo e a
    "espera assistindo" acontecia no feed/perfil)."""
    for _ in range(3):
        f = ps.foco()
        if not any(k in f for k in ('ReactTransparentActivity', 'HalfPdpActivity', 'ProductDetail', 'WebPageActivity')):
            return
        ps.sh('input keyevent KEYCODE_BACK')
        time.sleep(0.8)


def conferir_produto(doc):
    """No vídeo tocando: abre o produto vinculado e compara o nome com a página do link."""
    CONF_PRODUTO['t_toque'] = None
    esperado = ps.PRODUTO_TEXTOS
    if not esperado:
        raise ProdutoErrado('não guardei os textos da página do produto do link')
    titulo_link = ps.TITULO_ESPERADO or titulo_do_painel(esperado)
    if not titulo_link:
        raise Erro('não achei o nome do produto na página do link (gravacao\\produto_textos.txt)')

    def painel_aberto(im):  # barra de baixo do painel do produto: botão laranja de compra à direita
        def lar(c):  # laranja normal ou escurecido pelo tutorial "Arraste para cima"
            r, g, b = c
            return ps.e_laranja(c) or (80 < r < 130 and 20 < g < 45 and b < 30)
        if ps.PERFIL != 'tablet':
            return 'HalfPdpActivity' in ps.sh('dumpsys window | grep mCurrentFocus')
        return lar(ps.cor(im, 600, 1170)) and lar(ps.cor(im, 750, 1200))

    if ps.PERFIL != 'tablet':
        nomes = ler_cartao(doc)
        # rótulos do cartão que NÃO são nome de produto ("Ver Produtos (1)", "click video more...", "Gasto mínimo...")
        nomes = [n for n in nomes if not RE_ROTULO.match(n.strip()) and not RE_PROMO.search(n)]  # promoção não é nome
        if not nomes:  # sem leitura: vira pendência para o Kevin, não "produto errado" confirmado
            fechar_painel_produto()  # 12/11: volta ao player para terminar de assistir sem o painel por cima
            raise ProdutoIncerto('incerto: não consegui ler o nome do produto vinculado no vídeo (só o rótulo "Ver Produtos")')
        certo = next((n for n in nomes if mesmo_titulo(n, titulo_link)), None)
        if not certo:  # 18/11: leitura parcial/outra redação do MESMO produto não é "produto errado"
            certo = next((n for n in nomes if nome_compativel(n, titulo_link)), None)
        if not certo and ps.TITULO_APROVADO:  # mesma regra da trava antes de Postar (nome aprovado pelo Kevin)
            certo = next((n for n in nomes if ps.leitura_parcial_consistente(n, titulo_link)), None)
        fechar_painel_produto()
        if not certo:
            raise ProdutoErrado(f'produto no vídeo: {nomes[0]!r} ≠ produto do link: {titulo_link!r}')
        log(f'  produto conferido: {certo}')
        return certo
    aberto = False
    posicoes = [(290, 840), (240, 993), (240, 1018)]  # cartão do produto / faixa / carrinho
    for pos in posicoes:
        ps.sh('input tap %d %d' % pos)
        fim = time.time() + 6
        while time.time() < fim and not aberto:
            aberto = painel_aberto(None)if ps.PERFIL != 'tablet' else painel_aberto(ps.print_tela())
            if not aberto:
                time.sleep(0.3)
        if aberto:
            log(f'  produto aberto pelo toque em {pos}')
            break
    if not aberto:
        ps.print_tela(f'conf_produto_{doc}.png')
        raise ProdutoErrado('não abriu produto nenhum no vídeo (sem produto vinculado?)')
    # O painel abre com o vídeo do produto tocando (uiautomator falha) e o nome fica embaixo:
    # arrasta o painel para cima ("Arraste para cima para ver os detalhes") e lê de novo.
    titulo = None
    for _ in range(4):
        vis, _ = ps.textos_na_tela()
        titulo = titulo_do_painel(vis) or titulo
        if titulo and mesmo_titulo(titulo, titulo_link):
            break
        ps.sh('input swipe %d %d %d %d 500' % (*ps.P('painel_de', 400, 900), *ps.P('painel_ate', 400, 300)))
        time.sleep(3)
    ps.print_tela(f'conf_produto_{doc}.png')
    if not titulo or not mesmo_titulo(titulo, titulo_link):
        raise ProdutoErrado(f'produto no vídeo: {titulo!r} ≠ produto do link: {titulo_link!r}')
    log(f'  produto conferido: {titulo}')
    ps.sh('input keyevent KEYCODE_BACK'); time.sleep(2)
    ps.sh('input keyevent KEYCODE_BACK'); time.sleep(2)
    return titulo


@contextlib.contextmanager
def trava_json(limite=30):
    """Dois celulares gravando postados.json ao mesmo tempo não se apagam."""
    arq = POSTADOS + '.trava'
    fim = time.time() + limite
    while True:
        try:
            fd = os.open(arq, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(arq) > 60:
                    os.remove(arq)
                    continue
            except OSError:
                pass
            if time.time() > fim:
                raise TimeoutError('postados.json travado')
            time.sleep(0.2)
    try:
        yield
    finally:
        os.close(fd)
        with contextlib.suppress(OSError):
            os.remove(arq)


def pular_produto(item, motivo):
    """Põe em pulados.json este doc e as outras versões (A/B/C) do mesmo produto ainda não postadas."""
    with trava_json():
        lista = carregar(PULADOS, [])
        ja = {p.get('doc') for p in lista if isinstance(p, dict)}
        est = estado()
        chave = chave_produto(item)
        try:
            docs = [i['doc'] for i in carregar_filas() if chave_produto(i) == chave]
        except Exception:
            docs = []
        docs = [d for d in dict.fromkeys([item['doc'], *docs])
                if d not in ja and not est.get(d, '').startswith('postado')]
        hora = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        for d in docs:
            lista.append({'doc': d, 'hora': hora, 'motivo': motivo[:300], 'por': 'rodar_fila'})
        tmp = PULADOS + '.tmp'
        json.dump(lista, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, PULADOS)
    return len(docs)


def pular_com_motivo(item, motivo, detalhe='', so_este=False):
    """pulados.json com motivo curto (ex.: 'vendedor_de_ferias', 'erro_revisar') + detalhe. so_este=False pula também
    as outras versões A/B/C ainda não postadas do mesmo produto (erro do PRODUTO); True só este doc (erro do item)."""
    with trava_json():
        lista = carregar(PULADOS, [])
        ja = {p.get('doc') for p in lista if isinstance(p, dict)}
        est = estado()
        docs = [item['doc']]
        if not so_este:
            try:
                chave = chave_produto(item)
                docs += [i['doc'] for i in carregar_filas() if chave_produto(i) == chave]
            except Exception:
                pass
        docs = [d for d in dict.fromkeys(docs) if d not in ja and not est.get(d, '').startswith('postado')]
        hora = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        for d in docs:
            lista.append({'doc': d, 'hora': hora, 'motivo': motivo, 'por': 'rodar_fila', 'detalhe': detalhe[:300]})
        tmp = PULADOS + '.tmp'
        json.dump(lista, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, PULADOS)
    return len(docs)


ERROS_REVISAR = os.path.join(BASE, 'erros_revisar.json')
ERROS_SEGUIDOS = []  # docs (distintos) com erro desconhecido seguidos, sem post bem-sucedido no meio
# Kevin 10/11: o que continua PARANDO e chamando (captcha, login/PIN, diálogo de permissão, aparelho desconectado)
BLOQUEIA_RE = re.compile(r'captcha|login|\bPIN\b|senha|bloquead|permiss|tela pede sua decis|desconect|n[ãa]o conectad|'
                         r'adb|ADBKeyboard|tela bloqueada', re.I)


def erro_para_revisar(item, doc, msg):
    """Erro sem tratamento (antes de Postar, nada publicado): print + log + erros_revisar.json (a Central mostra em
    "Erros para revisar", sem som), pula SÓ este item e segue. 3 seguidos em itens diferentes = problema geral: para."""
    resumo = str(msg).split('\n')[0][:300]
    nome_print = f'erro_fila_{doc}.png'
    try:
        ps.print_tela(nome_print)
    except Exception:
        nome_print = ''
    lista = carregar(ERROS_REVISAR, [])
    lista.append({'doc': doc, 'produto': item.get('produto') or '', 'hora': datetime.datetime.now().astimezone().isoformat(
        timespec='seconds'), 'erro': resumo, 'print': nome_print, 'detalhe': str(msg)[:1500],
        'print_estavel': guardar_print(doc, nome_print) if nome_print else ''})
    json.dump(lista[-200:], open(ERROS_REVISAR, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    pular_com_motivo(item, 'erro_revisar', resumo, so_este=True)
    log(f'  ERRO PARA REVISAR (item pulado, a fila segue): {resumo}')
    if doc not in ERROS_SEGUIDOS:
        ERROS_SEGUIDOS.append(doc)
    if len(ERROS_SEGUIDOS) >= 3:
        parar_com_erro(f'3 erros seguidos em itens diferentes ({", ".join(ERROS_SEGUIDOS[-3:])}): problema geral; '
                       f'último: {resumo}', doc)
    liberar_claim(doc)


def pendente_produto(item, iid, motivo, tipo, video=None):
    """10/11 (Kevin): produto que não deu para vincular com certeza vira PENDENTE DE APROVAÇÃO
    (pendentes_aprovacao.json, com print da lista Adicionar e os nomes das linhas vistas).
    As outras versões A/B/C ainda não postadas do mesmo produto ficam fora da fila junto.
    Nada é publicado e a fila não espera: segue para o próximo item."""
    est = estado()
    chave = chave_produto(item)
    try:
        docs = [i['doc'] for i in carregar_filas() if chave_produto(i) == chave]
    except Exception:
        docs = []
    ja = {p.get('doc') for p in carregar(PULADOS, []) if isinstance(p, dict)}
    docs = [d for d in dict.fromkeys([item['doc'], *docs])
            if d not in ja and not est.get(d, '').startswith('postado')]
    reg = pendentes.adicionar(item, docs, iid, motivo, tipo, list(ps.LINHAS_VISTAS),
                              print_origem=ps.PRINT_LISTA, video=video, aparelho=ID_FILA,
                              esperado=ps.TITULO_ESPERADO or ps.TITULO_CACHE or '')
    return len(reg.get('docs') or [])


def marcar(doc, **campos):
    with trava_json():
        dados = carregar(POSTADOS, [])
        for e in reversed(dados):
            if e['doc'] == doc:
                e.update(campos)
                break
        json.dump(dados, open(POSTADOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ---------- limpeza ----------

def limpar(postados):
    """Apaga do PC e do tablet os vídeos de posts confirmados."""
    for n in os.listdir(VIDEOS) if os.path.isdir(VIDEOS) else []:
        if n.lower().endswith('.mp4') and os.path.splitext(n)[0] in postados:
            ps.mandar_para_lixeira(os.path.join(VIDEOS, n))
            log(f'  apagado do PC (Lixeira): {n}')
    for pasta in (ps.DESTINO, ps.ARQUIVO_MORTO):
        for n in ps.sh(f'ls {pasta} 2>/dev/null').split():
            if n.lower().endswith('.mp4') and os.path.splitext(n)[0] in postados:
                ps.sh(f"rm -f '{pasta}/{n}'")
                ps.sh(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d 'file://{pasta}/{n}'")
                log(f'  apagado do celular: {pasta}/{n}')


# ---------- ciclo ----------

def ciclo(item):
    try:  # tela física apagada durante o post (economiza bateria; screencap/toques seguem funcionando)
        import tela_apagada
        tela_apagada.garantir(ps.SERIAL)
    except Exception:
        pass
    doc = item['doc']
    log(f'== {doc} ({item.get("produto")})')
    video = baixar(item)
    leg = item['legenda'].replace('\\n', '\n')
    # Mesmo produto do post anterior bem-sucedido (A->B->C em sequência): ele já é o 1º de
    # "Minhas Curtidas > Mais Recente", então não favorita de novo (o nome é conferido na lista).
    # Senão: abre o link e favorita (se já curtido, descurte e curte para subir ao topo).
    global ULTIMO_PRODUTO
    chave = chave_produto(item)
    # Kevin (05/11): favoritar na hora de postar CADA versão (mais simples e garante o topo).
    favoritar = True if SEMPRE_FAVORITAR else not (ULTIMO_PRODUTO and ULTIMO_PRODUTO[0] == chave)
    if favoritar:
        ps.PRODUTO_TEXTOS = ps.TITULO_ESPERADO = None
    else:
        ps.TITULO_ESPERADO, ps.PRODUTO_TEXTOS = ULTIMO_PRODUTO[1], ULTIMO_PRODUTO[2]
        log('  mesmo produto do post anterior: pulando o favoritar')
    # Nome já confirmado deste produto (titulos.json, por itemId): evita reler o nome da página.
    cache_ids = carregar(ITEMIDS, {})
    iid = itemid_de(item.get('link', ''), cache_ids)
    titulos = carregar(TITULOS, {})
    ps.TITULO_CACHE = titulos.get(iid) if iid else None
    ps.TITULO_APROVADO = pendentes.aprovado(iid, item.get('produto'), doc)  # linha aprovada pelo Kevin (itemId, produto-base ou nome)
    if ps.TITULO_APROVADO:
        log(f'  nome aprovado pelo Kevin: {ps.TITULO_APROVADO[:60]}')
    ps.ITEM_ID = iid
    ps.PAGINA_DUVIDA = None  # dúvida de nome da página é por item
    if iid and cache_ids.get(item.get('link')) == iid:
        json.dump(cache_ids, open(ITEMIDS, 'w', encoding='utf-8'), indent=1)
    PASSO.update(ativo=True, doc=doc, t=time.time())
    ps.VALIDAR_PAGINA = validador_de_pagina(item, ps.TITULO_CACHE)
    try:
        try:
            t_item = time.time()
            for tentativa in range(3):  # Kevin: bug = fechar e reabrir o app (só antes de tocar em Postar)
                if tentativa and time.time() - t_item > 360 and not ps.TOCOU_POSTAR:
                    # limite de 6 min por item (antes de Postar): vira pendente e a fila segue
                    raise ps.CartaoIlegivel(f'limite de 6 min neste item sem conseguir postar com segurança')
                try:
                    ps.postar(video, item['link'], leg, seco=False, favoritar=favoritar)
                    break
                except (ps.ProdutoDaLista, ps.ProdutoIndisponivel):
                    raise
                except ps.Parou as e:
                    bloqueio = re.search(r'captcha|login|PIN|senha|bloque', str(e), re.I)
                    # cartão ilegível: no máx. 2 tentativas na mesma tela, depois vira pendente (não trava a fila)
                    if (tentativa == 2 or ps.TOCOU_POSTAR or bloqueio
                            or (isinstance(e, (ps.CartaoIlegivel, ps.NomeDiferente)) and tentativa >= 1)):
                        raise
                    log(f'  bug ({e}); fechando e reabrindo a Shopee ({tentativa + 1}/2)')
                    ps.sh(f'am force-stop {ps.PKG}')
                    time.sleep(4)
                    ps.sh(f'monkey -p {ps.PKG} -c android.intent.category.LAUNCHER 1')
                    time.sleep(10)
        except ps.ProdutoDaLista as e:
            # antes de Postar (nada publicado): refaz o post do zero, favoritando o produto
            # 12/11 (arranhador: favoritou, o coração ficou vermelho, mas o produto não apareceu em Minhas Curtidas):
            # até 2 refações; em cada uma espera o favorito propagar e puxa a lista para atualizar antes de procurar.
            for refacao in (1, 2):
                log(f'  produto não achado em Minhas Curtidas ({e}); refazendo com favoritar ({refacao}/2, com refresh da lista)')
                ps.sh(f'am force-stop {ps.PKG}')
                time.sleep(3)
                ps.REFRESH_LISTA = 3 + 5 * refacao  # segundos de espera + puxar a lista antes de ler
                ps.PAGINAS_LISTA = 2  # 21/11 (Kevin): nada de rolar 8 telas; o PLACAR olha a 1ª tela (+1) e, sem certeza, vira pendente
                try:
                    ps.postar(video, item['link'], leg, seco=False, favoritar=True)
                    break
                except ps.ProdutoDaLista as e2:
                    e = e2
                    if refacao == 2:
                        raise
                finally:
                    ps.REFRESH_LISTA = 0
                    ps.PAGINAS_LISTA = 2
    except (ps.ProdutoDaLista, ps.ProdutoIndisponivel, ps.CartaoIlegivel, ps.NomeDiferente) as e:
        # 10/11 (Kevin): produto que não dá para vincular com certeza não trava a fila: nada publicado,
        # sai do editor, vira PENDENTE DE APROVAÇÃO na Central (print + linhas vistas) e segue.
        PASSO['ativo'] = False
        ps.sh(f'am force-stop {ps.PKG}')
        if isinstance(e, ps.ConfirmarNome):
            tipo, txt = 'parecido', 'precisa confirmar o nome (print da lista Adicionar e nomes anexados)'
        elif isinstance(e, ps.NomeDiferente):
            tipo, txt = 'parecido', 'o nome na página do link não bate com o esperado (nada publicado)'
        elif isinstance(e, ps.CartaoIlegivel):
            tipo, txt = 'ausente', 'não deu para confirmar o produto no cartão da legenda (ilegível ou nome não bate com certeza)'
        elif isinstance(e, ps.ProdutoDaLista):
            tipo = 'parecido' if 'nome parecido' in str(e) else 'ausente'
            txt = 'não achado em Minhas Curtidas mesmo após favoritar'
        else:
            tipo, txt = 'indisponivel', 'indisponível / não dá para adicionar'
        try:
            n = pendente_produto(item, iid, f'produto {txt}: {e}', tipo, video=video)
            log(f'  PENDENTE DE APROVAÇÃO ({n} versões): produto {txt}: {e}')
        except Exception as e2:  # sem conseguir gravar o pendente: o jeito antigo (pulados.json)
            n = pular_produto(item, f'não postado: produto {txt}: {e} (pendente falhou: {e2})')
            log(f'  PULADO ({n} versões; pendente falhou: {e2}): produto {txt}: {e}')
        liberar_claim(doc)
        return
    except ps.ProdutoEsgotado as e:
        # Kevin 10/11: vendedor de férias / produto indisponível na página: pula o produto (todas as versões),
        # vai para esgotados (Central) e segue para o próximo.
        PASSO['ativo'] = False
        n = pular_com_motivo(item, 'vendedor_de_ferias', str(e))
        log(f'  PRODUTO PULADO ({n} versões) e marcado como esgotado: {e}')
        liberar_claim(doc)
        return
    except ps.Parou as e:
        if ps.TOCOU_POSTAR or BLOQUEIA_RE.search(str(e)):
            parar_com_erro(f'não postado: {e}', doc)
        PASSO['ativo'] = False
        erro_para_revisar(item, doc, f'não postado: {e}')
        return
    except Exception as e:
        if not ps.TOCOU_POSTAR and not isinstance(e, ps.Desconectado) and not BLOQUEIA_RE.search(str(e)):
            PASSO['ativo'] = False
            erro_para_revisar(item, doc, f'não postado: {e!r}')
            return
        if not ps.TOCOU_POSTAR:  # caiu antes de tocar em Postar (ex.: tablet desconectou): nada publicado
            parar_com_erro(f'não postado: {e!r}\n{traceback.format_exc()}', doc)
        # Incerto ou falha depois de tocar em Postar
        ps.registrar(doc, 'incerto', str(e))
        parar_com_erro(f'INCERTO (pode ter postado; confira no perfil): {e}\n{traceback.format_exc()}', doc)
    PASSO['ativo'] = False
    cont = carregar(TRAVOU, {})
    if cont.pop(doc, None):
        json.dump(cont, open(TRAVOU, 'w', encoding='utf-8'))
    ps.registrar(doc, 'postado', 'confirmação vista; reutilização OFF, IA ON')
    ERROS_SEGUIDOS.clear()  # post bem-sucedido: zera a contagem de erros seguidos
    POSTS_SESSAO[0] += 1  # Kevin 21/11: posts concluídos desde que a fila foi ligada (para "parar após N posts")
    escrever_progresso('rodando')
    _APARELHO_DOC[doc] = ID_FILA
    escrever_sync()
    ps.marca('postar')
    log('  postado (confirmação vista)')
    log('  tempos: ' + ps.tempos())
    # Kevin 06/11: a conferência do produto no vídeo NÃO bloqueia. Se não bater ou não der para ler,
    # reabre o vídeo 1 vez; se continuar, avisa na Central (conferir_vinculo.csv) e segue a fila.
    vinculo_ok = True
    # 12/11: saiu o dump de diagnóstico logo após o post (uiautomator de até 6 s em todo post; o aviso
    # "Enviado com sucesso!" já é conhecido). E não reabre mais o vídeo quando o produto não confere: a leitura
    # já tenta 2 vezes no mesmo player (+ OCR) e o vídeo é assistido 1 vez só (Kevin 12/11).
    try:
        conferir_no_perfil(video, doc)
    except ProdutoIncerto as e:  # 10/11 (Kevin): não deu para LER o produto: avisa na Central e SEGUE (não para a fila)
        vinculo_ok = False
        marcar(doc, produto_conferido=f'incerto: {e}')
        pendencia_vinculo(doc, str(e), 'incerto')
        log(f'  pós-check incerto (silencioso, a fila segue): {e}')
    except ProdutoErrado as e:
        # Kevin 11/11 ("o aviso travou a tela? pode prosseguir"): aviso pós-post NUNCA trava a fila. O post já saiu;
        # registra a pendência "Conferir produto vinculado" na Central (para o Kevin olhar no perfil) e segue.
        vinculo_ok = False
        marcar(doc, produto_conferido=f'produto_errado?: {e}')
        pendencia_vinculo(doc, str(e), 'errado')
        log(f'  CONFERIR NO PERFIL (aviso, a fila segue): {e}')
    except Exception as e:
        marcar(doc, produto_conferido=f'nao conferido: {e}')
        if BLOQUEIA_RE.search(str(e)) or isinstance(e, ps.Desconectado):
            parar_com_erro(f'postado, mas a conferência falhou (vídeo mantido): {e}', doc)
        # 10/11 (Kevin): falha de conferência sem bloqueio = o post JÁ saiu; avisa para conferir e segue
        vinculo_ok = False
        pendencia_vinculo(doc, f'conferência falhou: {str(e)[:200]}', 'incerto')  # "pós-check não confirmado": silencioso
        log(f'  CONFERÊNCIA FALHOU (post mantido; conferir no perfil; a fila segue): {e}')
    if vinculo_ok:
        marcar(doc, produto_conferido='ok')
    ULTIMO_PRODUTO = (chave, ps.TITULO_ESPERADO, ps.PRODUTO_TEXTOS) if ps.TITULO_ESPERADO else None
    # guarda o nome só depois de bater na lista E no vídeo publicado; nada de texto de promoção
    tit = ps.TITULO_ESPERADO
    if vinculo_ok and iid and tit and not ps.TITULO_APROVADO and len(tit) >= 15 and not re.search(
            r'\bleve\b|desconto|%|frete|cupom|avalia[çc]|busque', tit, re.I):
        with pendentes.trava():  # relê: a Central pode ter gravado uma aprovação durante o post
            titulos = carregar(TITULOS, {})
            if iid not in titulos:
                titulos[iid] = tit
                json.dump(titulos, open(TITULOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    limpar({d for d, r in estado().items() if r.startswith('postado')})


def produtos_postados_hoje(fila):
    """(chaves de produto, itemIds) dos posts publicados HOJE (hora local) em postados.json."""
    hoje = datetime.date.today()
    docs = set()
    for e in carregar(POSTADOS, []):
        if not isinstance(e, dict) or not str(e.get('resultado', '')).startswith('postado'):
            continue
        try:
            t = datetime.datetime.strptime(str(e.get('utc', '')), '%Y-%m-%dT%H:%M:%SZ').replace(
                tzinfo=datetime.timezone.utc).astimezone()
        except Exception:
            continue
        if t.date() == hoje:
            docs.add(e.get('doc'))
    cache = carregar(ITEMIDS, {})
    chaves, ids = set(), set()
    for i in fila:
        if i['doc'] in docs:
            chaves.add(chave_produto(i))
            iid = itemid_de(i.get('link', ''), cache)
            if iid:
                ids.add(iid)
    return chaves, ids


def no_horario():
    return HORA_INI <= datetime.datetime.now().hour < HORA_FIM


def pid_vivo(pid):
    """12/11: no Windows, os.kill(pid, 0) NÃO é um teste: 0 == CTRL_C_EVENT e manda Ctrl+C para o grupo do
    processo (ou falha). Agora pergunta ao Windows se o processo ainda está ativo, sem mexer nele."""
    try:
        pid = int(str(pid).strip())
    except Exception:
        return False
    try:
        import pid_real
        if not pid_real.e_robo(pid):  # 22/11: existe mas não é um robô (pid reaproveitado)
            return False
    except ImportError:
        pass
    if os.name == 'nt':
        import ctypes
        k = ctypes.windll.kernel32
        k.OpenProcess.restype = ctypes.c_void_p
        k.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        k.CloseHandle.argtypes = [ctypes.c_void_p]
        h = k.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        try:
            codigo = ctypes.c_ulong()
            return bool(k.GetExitCodeProcess(h, ctypes.byref(codigo))) and codigo.value == 259  # STILL_ACTIVE
        finally:
            k.CloseHandle(h)
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def lock_vivo(caminho):
    # 22/11: pid reaproveitado pelo Windows (ex.: audiodg.exe) não conta: pid_real exige python + script do robô +
    # processo criado antes do lock; lock que falha é removido com log.
    try:
        import pid_real
        return pid_real.lock_vivo(caminho, log=log)
    except ImportError:
        pass
    try:
        return pid_vivo(open(caminho).read())
    except Exception:
        return False


def pedido_parar():
    return os.path.exists(PARAR) or os.path.exists(PARAR_MEU)


def _arq_claim(doc):
    return os.path.join(CLAIMS, re.sub(r'\W+', '_', str(doc)) + '.txt')


def erro_prende(doc):
    if not doc:
        return False
    for nome in ('erro.txt', 'erro_celular1.txt', 'erro_celular2.txt'):
        try:
            if doc in open(os.path.join(BASE, nome), encoding='utf-8').read():
                return True
        except Exception:
            pass
    return False


def reivindicar(doc):
    """True se este celular pode postar o doc. O outro, no mesmo instante, recebe False."""
    os.makedirs(CLAIMS, exist_ok=True)
    arq = _arq_claim(doc)
    for _ in range(2):
        try:
            fd = os.open(arq, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, ID_FILA.encode())
            os.close(fd)
            return True
        except FileExistsError:
            try:
                dono = open(arq, encoding='utf-8').read().strip()
            except OSError:
                return False
            if dono == ID_FILA:
                return True
            lock_dono = os.path.join(BASE, f'rodar_fila_{dono}.lock')
            if lock_vivo(lock_dono) or erro_prende(doc):
                return False
            if time.time() - os.path.getmtime(arq) < 45 * 60:
                return False
            try:
                os.remove(arq)
            except OSError:
                return False
    return False


def liberar_claim(doc):
    arq = _arq_claim(doc)
    try:
        if open(arq, encoding='utf-8').read().strip() == ID_FILA:
            os.remove(arq)
    except OSError:
        pass


def outro_postando():
    for nome in ('celular1', 'celular2'):
        if nome != ID_FILA and lock_vivo(os.path.join(BASE, f'rodar_fila_{nome}.lock')):
            return True
    if ID_FILA != 'celular1' and lock_vivo(LOCK_LEGADO):
        return True
    return False


CONFIG_FILA = os.path.join(BASE, 'config_fila.json')
PROGRESSO = os.path.join(BASE, 'fila_progresso.json')
POSTS_SESSAO = [0]
T_INICIO = [time.time()]


def meta_posts():
    """"Parar após N posts" (0 = sem limite): relido a cada ciclo de tablet\\config_fila.json."""
    try:
        return max(0, int(json.load(open(CONFIG_FILA, encoding='utf-8-sig')).get('meta_posts', 0) or 0))
    except Exception:
        return 0


def escrever_progresso(estado):
    """tablet\\fila_progresso.json: a Central mostra "x / N" e o estado ("concluído: N posts")."""
    try:
        tmp = PROGRESSO + '.tmp'
        json.dump({'pid': os.getpid(), 'aparelho': ID_FILA, 'estado': estado, 'concluidos': POSTS_SESSAO[0],
                   'meta_posts': meta_posts(), 'desde': datetime.datetime.fromtimestamp(T_INICIO[0]).astimezone().isoformat(
                       timespec='seconds'), 'atualizado': datetime.datetime.now().astimezone().isoformat(timespec='seconds')},
                  open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
        os.replace(tmp, PROGRESSO)
    except Exception:
        pass


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--um', action='store_true', help='posta só o próximo e sai')
    a.add_argument('--ignorar-horario', action='store_true')
    a.add_argument('--seguido', action='store_true', help='sem espera entre posts (um logo após o outro)')
    a.add_argument('--so-conferir', metavar='DOC', help='refaz só a conferência de um post já postado')
    args = a.parse_args()

    if args.so_conferir:
        doc = args.so_conferir
        ps.PRODUTO_TEXTOS = open(os.path.join(ps.PASTA, 'produto_textos.txt'), encoding='utf-8').read().splitlines()
        video = os.path.join(VIDEOS, doc + '.mp4')
        ps.fechar_whatsapp()
        conferir_no_perfil(video, doc)
        if not estado().get(doc, '').startswith('postado'):
            # era "incerto": a confirmação no perfil (miniatura + produto) prova que saiu
            ps.registrar(doc, 'postado', 'confirmado no perfil depois de incerto')
            escrever_sync()
        marcar(doc, produto_conferido='ok')
        limpar({d for d, r in estado().items() if r.startswith('postado')})
        log(f'  conferência refeita ok: {doc}')
        return

    if os.path.exists(os.path.join(BASE, 'FILA_BLOQUEADA')):
        log('bloqueada: aguardando trava + OK do Kevin (FILA_BLOQUEADA)')
        sys.exit(1)
    if os.path.exists(ERRO):
        log('erro.txt existe — não vou rodar. Confira o problema e apague erro.txt.')
        sys.exit(1)
    meu_erro = arquivo_erro()
    if meu_erro != ERRO and os.path.exists(meu_erro):
        log(f'{os.path.basename(meu_erro)} existe — não vou rodar neste celular.')
        sys.exit(1)
    # 10/11: um aparelho = uma tarefa. Se o robô de afiliados (conferir/candidatos) está vivo neste celular,
    # a fila não sobe nele (antes subia por cima do filtro e travava na tela de permissão/câmera).
    try:  # 11/11: o "assistir" do Kevin usa o celular: não sobe em cima dele
        import assistir_uso
        if assistir_uso.assistir_usa(ID_FILA):
            log(f'o assistir está usando o {ID_FILA}: a fila não sobe neste aparelho (desligue o assistir)')
            sys.exit(1)
    except ImportError:
        pass
    if lock_vivo(os.path.join(BASE, 'curtidas', f'interagir_curtidas_{ID_FILA}.lock')):  # 20/11: robô de curtidas
        log(f'o robô de curtidas está usando o {ID_FILA}: a fila não sobe neste aparelho')
        sys.exit(1)
    for _pref in ('conferir', 'candidatos'):
        _l = os.path.join(BASE, 'afiliados', f'{_pref}_{ID_FILA}.lock')
        if lock_vivo(_l):
            log(f'o robô de afiliados ({_pref}) está usando o {ID_FILA}: a fila não sobe neste aparelho')
            sys.exit(1)
    if lock_vivo(LOCK) or (ID_FILA == 'celular1' and lock_vivo(LOCK_LEGADO)):
        log(f'já está rodando neste celular ({ID_FILA})')
        sys.exit(0)
    open(LOCK, 'w').write(str(os.getpid()))
    if ID_FILA == 'celular1':
        open(LOCK_LEGADO, 'w').write(str(os.getpid()))
    log(f'fila no {ID_FILA}')
    desligar_quickedit()
    threading.Thread(target=vigia_de_passo, daemon=True).start()
    try:
        escrever_sync()
        prefetch = None
        proximo = time.time()
        avisou_hoje = None
        escrever_progresso('rodando')
        while True:
            # Kevin 21/11: "parar após N posts": ao chegar em N posts concluídos desde que foi ligada, termina LIMPO, entre posts
            _meta = meta_posts()
            if _meta and POSTS_SESSAO[0] >= _meta:
                log(f'concluído: {POSTS_SESSAO[0]} posts (meta {_meta}); a fila termina sozinha, entre posts')
                escrever_progresso(f'concluído: {POSTS_SESSAO[0]} posts')
                return
            escrever_progresso('rodando')
            sincronizar_filas_drive()  # lote novo do Drive entra sozinho
            try:
                importar_fila_manual()  # Kevin 21/11: itens colocados à mão em fila_manual.txt
            except Exception as e:
                log(f'  (fila manual ignorada neste ciclo: {e})')
            fila = carregar_filas()  # relê a cada post: filas novas entram sem reiniciar
            est = estado()
            postados = {d for d, r in est.items() if r.startswith('postado')}
            limpar(postados)
            hoje = f'{datetime.date.today():%Y-%m-%d}'
            # pulados.json: posts que o Kevin mandou pular pela Central (relido a cada post)
            pulados = {p.get('doc') for p in carregar(PULADOS, []) if isinstance(p, dict)}
            pulados |= pendentes.docs_pendentes()  # pendentes de aprovação: a fila não espera por eles
            restantes = [i for i in fila if i['doc'] not in postados and i['doc'] not in pulados]
            # "dia_post" (opcional): só posta a partir desse dia; sem o campo, posta já
            pend = [i for i in restantes if not i.get('dia_post') or str(i['dia_post']) <= hoje]
            # Regra do Kevin: A/B/C do mesmo produto NUNCA no mesmo dia. Produto com irmão postado hoje
            # (mesmo produto-base ou mesmo itemId) fica para outro dia.
            ate_amanha_n = 0
            try:
                chaves_hoje, ids_hoje = produtos_postados_hoje(fila)
                ate_amanha = [i for i in restantes if chave_produto(i) in chaves_hoje
                              or (itemid_de(i.get('link', ''), carregar(ITEMIDS, {})) or '#') in ids_hoje]
                if ate_amanha:
                    ids_adiados = {i['doc'] for i in ate_amanha}
                    ate_amanha_n = len(ids_adiados)
                    if ids_adiados != getattr(sys.modules[__name__], '_ULT_ADIADOS', None):
                        log(f'  irmãos já postados hoje: adiando {len(ids_adiados)} item(ns) para outro dia')
                        sys.modules[__name__]._ULT_ADIADOS = ids_adiados
                    restantes = [i for i in restantes if i['doc'] not in ids_adiados]
                    pend = [i for i in restantes if not i.get('dia_post') or str(i['dia_post']) <= hoje]  # BUG 10/11: pend já tinha sido calculado antes
            except Exception as e:
                log(f'  (regra do mesmo dia ignorada neste ciclo: {e})')
            if not restantes:
                # 16/11 (Kevin): a fila NUNCA sai sozinha (às 03:08 saiu com "fila terminou" e ninguém copiou as filas
                # novas do Drive). Sem item elegível (nada sobrou OU só sobrou o que fica para outro dia) ela aguarda,
                # relê filas/Drive a cada 10 min (sincronizar no topo do laço) e só o arquivo PARAR encerra.
                if avisou_hoje != hoje:
                    if ate_amanha_n:
                        log(f'fila de hoje terminou; {ate_amanha_n} item(ns) ficam para amanhã — aguardando (sem sair)')
                    else:
                        log('fila vazia: nenhum item elegível — aguardando lote novo no Drive (sem sair; só PARAR encerra)')
                    avisou_hoje = hoje
                for _ in range(60):  # 10 min; PARAR continua valendo; relê filas/Drive ao voltar
                    if pedido_parar():
                        log('arquivo PARAR encontrado — parando')
                        return
                    time.sleep(10)
                continue
            if not pend:
                if avisou_hoje != hoje:
                    prox = min(str(i['dia_post']) for i in restantes)
                    log(f'concluído hoje, próximo amanhã (próximo dia_post: {prox}; faltam {len(restantes)})')
                    avisou_hoje = hoje
                for _ in range(60):  # espera 10 min e confere de novo (PARAR continua valendo)
                    if pedido_parar():
                        log('arquivo PARAR encontrado — parando')
                        return
                    time.sleep(10)
                continue
            # prioridade do robô de afiliados (relida a cada post); A/B/C do mesmo produto juntos.
            # Um produto já começado (A postado) termina antes de trocar de produto.
            try:
                comecados = {}
                for i in fila:
                    if i['doc'] in postados:
                        k = chave_produto(i)
                        comecados[k] = comecados.get(k, 0) + 1
                pend, rank_grupo = ordenar_por_prioridade(pend, comecados)
            except Exception as e:
                log(f'  (prioridade ignorada neste ciclo: {e})')
            item = None
            for cand in pend:
                if reivindicar(cand['doc']):
                    item = cand
                    break
            if item is None:
                log('os próximos vídeos estão com o outro celular — espero')
                time.sleep(20)
                continue
            if est.get(item['doc']) == 'incerto':
                parar_com_erro('o último registro deste post é "incerto"; confira no perfil e '
                               'marque no postados.json antes de continuar', item['doc'])
            if pedido_parar():
                liberar_claim(item['doc'])
                log('arquivo PARAR encontrado — parando')
                return
            espera = proximo - time.time()
            if espera > 0:
                log(f'próximo post em {espera / 60:.1f} min')
                time.sleep(espera)
            if not args.ignorar_horario and not no_horario():
                liberar_claim(item['doc'])
                log('fora do horário 08:00-22:00 — parando')
                return
            inicio = time.time()
            try:
                # adianta o download do PRÓXIMO vídeo enquanto este posta (um download por vez)
                if prefetch and prefetch.is_alive():
                    prefetch.join(600)
                baixar(item)
                if pedido_parar():
                    liberar_claim(item['doc'])
                    log('arquivo PARAR encontrado — parando')
                    return
                if (not outro_postando() and len(pend) > 1
                        and not os.path.isfile(os.path.join(VIDEOS, pend[1]['doc'] + '.mp4'))):
                    prefetch = threading.Thread(target=baixar_quieto, args=(pend[1],), daemon=True)
                    prefetch.start()
                ciclo(item)
            except SystemExit:
                raise
            except Exception as e:
                parar_com_erro(f'erro: {e}\n{traceback.format_exc()}', item['doc'])
            if args.um:
                return
            proximo = time.time() + random.uniform(5, 20) if args.seguido else inicio + random.uniform(8, 12) * 60
    finally:
        try:
            import tela_apagada
            tela_apagada.parar()
        except Exception:
            pass
        for caminho in (LOCK, LOCK_LEGADO if ID_FILA == 'celular1' else None):
            if not caminho:
                continue
            try:
                if open(caminho).read().strip() == str(os.getpid()):
                    os.remove(caminho)
            except Exception:
                pass


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except BaseException as e:  # qualquer falha inesperada também avisa e grava erro.txt
        parar_com_erro(f'erro inesperado: {e!r}\n{traceback.format_exc()}')
