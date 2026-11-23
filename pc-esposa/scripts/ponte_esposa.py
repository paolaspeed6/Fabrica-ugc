r"""Ponte da Paola (23/11/2026): liga os robôs do PC com a fábrica pelo Google Drive, sem precisar do Claude.

Pastas no Drive (Google Drive para desktop, X:\Meu Drive):
  Central Esposa\conferir\<LOTE-NN>.json   vídeos novos para conferir (a fábrica na nuvem grava)
  Central Esposa\ordem_producao.json        seus pedidos de produção (o PC reescreve NO LUGAR; a nuvem lê)
  Central Esposa\producao_status.json       andamento dos pedidos (a nuvem grava)
  Central Esposa\decisoes_conferir.json     suas decisões da Conferência (o PC reescreve NO LUGAR; a nuvem lê)
  Central Esposa\postados_pc_nuvem.json     o que o robô já postou (o rodar_fila.py reescreve NO LUGAR)
  Videos Esposa\AAAA-MM-DD\... ou Fabrica Videos\AAAA-MM-DD\...   os mp4

Fluxo automático:
  filtro aprova  -> aba Produção (espera a sua ordem) -> "Produzir" grava ordem_producao.json -> a fábrica produz
  fábrica entrega -> aba Conferir -> seu Ok -> entra sozinho no fila.json -> robô posta
  robô postou    -> sai sozinho do fila.json e da Conferência -> aba Postados
Arquivos "no lugar": nunca apagar/recriar no Drive (a nuvem perderia o acesso ao arquivo).
"""
import csv, datetime, glob, json, os, re, shutil, threading, time

TABLET = r'C:\horst\tablet'
LOCAL = os.path.join(TABLET, 'esposa')
FILA = os.path.join(TABLET, 'fila.json')
POSTADOS = os.path.join(TABLET, 'postados.json')
CONFERIDOS = os.path.join(TABLET, 'afiliados', 'conferidos.csv')
DECISOES = os.path.join(LOCAL, 'decisoes.json')
ENVIADOS = os.path.join(LOCAL, 'producao_enviados.json')
TINDER = os.path.join(LOCAL, 'tinder.json')  # itemId -> {'d': 'gostei'|'nao', 'em': ...}
LOG = os.path.join(LOCAL, 'ponte.log')
PASTAS_VIDEO = ('Videos Esposa', 'Fabrica Videos')
CUSTO_USD = 0.42        # 3 imagens + 3 clipes por produto (preço medido out/2026)
TETO_POR_PRODUTO = 0.60  # teto em dólar por produto (cobre 1 refação; ~R$ 3)
TRAVA = threading.Lock()
_IDX = {'t': 0, 'v': {}}


def log(m):
    os.makedirs(LOCAL, exist_ok=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {m}\n')


def ler(caminho, padrao):
    try:
        return json.load(open(caminho, encoding='utf-8-sig'))
    except Exception:
        return padrao


def gravar(caminho, dados):
    """Arquivo LOCAL: grava atômico (tmp + replace)."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    tmp = caminho + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    json.load(open(tmp, encoding='utf-8'))
    os.replace(tmp, caminho)


def raiz_drive():
    for letra in 'GHIJKLMNOPQRSTUVWXYZDEF':
        for r in ('Meu Drive', 'My Drive'):
            p = f'{letra}:\\{r}'
            if os.path.isdir(os.path.join(p, 'Central Esposa')):
                return p
    return None


def central():
    r = raiz_drive()
    return os.path.join(r, 'Central Esposa') if r else None


def no_lugar(nome, dados):
    """Arquivo do DRIVE criado pela nuvem: reescreve o conteúdo sem apagar (mantém o id). False se não existe."""
    c = central()
    p = os.path.join(c, nome) if c else None
    if not p or not os.path.isfile(p):
        return False
    with open(p, 'r+', encoding='utf-8') as f:
        f.seek(0)
        f.write(json.dumps(dados, ensure_ascii=False))
        f.truncate()
    return True


def _id(x):
    return str(x or '').strip().split('.')[-1]


# ------------------------------------------------------------------ vídeos

def indice_mp4():
    if time.time() - _IDX['t'] < 120:
        return _IDX['v']
    ind = {}
    r = raiz_drive()
    for nome in PASTAS_VIDEO if r else ():
        base = os.path.join(r, nome)
        if not os.path.isdir(base):
            continue
        hoje = datetime.date.today()
        for dia in os.listdir(base):
            try:
                if (hoje - datetime.date.fromisoformat(dia[:10])).days > 30:
                    continue
            except ValueError:
                continue
            for raiz, _d, ns in os.walk(os.path.join(base, dia)):
                for n in ns:
                    if n.lower().endswith('.mp4'):
                        ind.setdefault(n[:-4], os.path.join(raiz, n))
    _IDX.update(t=time.time(), v=ind)
    return ind


def video(doc):
    return indice_mp4().get(os.path.basename(str(doc)))


# ------------------------------------------------------------------ postados

def postados():
    """doc -> {'em': utc, 'produto': ...} dos que o robô postou (resultado começa com 'postado')."""
    out = {}
    for e in ler(POSTADOS, []):
        r = e.get('resultado') or e.get('status') or ''
        if e.get('doc') and r.startswith('postado') and e['doc'] not in out:
            out[e['doc']] = {'em': e.get('utc') or e.get('postado_em') or '', 'produto': e.get('produto') or ''}
    return out


# ------------------------------------------------------------------ Conferência

def docs_conferir():
    c = central()
    pasta = os.path.join(c, 'conferir') if c else None
    out = {}
    for p in sorted(glob.glob(os.path.join(pasta, '*.json'))) if pasta else ():
        d = ler(p, None)
        if isinstance(d, dict):
            out[os.path.basename(p)[:-5]] = d
    return out


def conferir_lista():
    dec = ler(DECISOES, {})
    post = postados()
    pend, aceitos = [], []
    for did, d in docs_conferir().items():
        posts = []
        for k, p in sorted((d.get('posts') or {}).items()):
            posts.append({'doc': k, 'versao': p.get('versao') or k[-1], 'legenda': p.get('legenda') or '',
                          'link': p.get('link_produto') or d.get('link_anuncio') or '', 'tem_video': bool(video(k)),
                          'postado': k in post})
        item = {'id': did, 'lote': d.get('lote') or '', 'produto': d.get('produto') or did, 'aviso': d.get('aviso') or '',
                'posts': posts}
        x = dec.get(did)
        if not x:
            pend.append(item)
        elif x.get('status') == 'ok':
            item['aceitas'] = x.get('versoes') or []
            if not all(p['postado'] for p in posts if p['doc'] in item['aceitas']):
                aceitos.append(item)  # saiu da Conferência; fica em "Na fila" até postar todas as versões aceitas
    return {'pendentes': pend, 'na_fila': aceitos}


def decidir(did, versoes=None, recusar=False):
    with TRAVA:
        d = docs_conferir().get(did)
        if not d:
            return False, 'Esse vídeo sumiu da pasta conferir do Drive.'
        dec = ler(DECISOES, {})
        if dec.get(did):
            return False, 'Esse produto já foi decidido.'
        agora = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        if recusar:
            dec[did] = {'status': 'recusado', 'em': agora}
            gravar(DECISOES, dec)
            _espelhar_decisoes(dec)
            return True, f'Recusado: {d.get("produto", did)[:50]}'
        posts = d.get('posts') or {}
        versoes = [v for v in (versoes or list(posts)) if v in posts]
        if not versoes:
            return False, 'Marque ao menos uma versão (A, B ou C).'
        fila = ler(FILA, [])
        na_fila = {i.get('doc') for i in fila}
        novos = []
        for k in versoes:
            p = posts[k]
            link = p.get('link_produto') or d.get('link_anuncio') or ''
            if k in na_fila or not link:
                continue
            novos.append({'doc': k, 'produto': p.get('produto') or d.get('produto') or '', 'link': link,
                          'legenda': (p.get('legenda') or '')[:150], 'origem': f'conferencia {d.get("lote", "")}'})
        if novos:
            if os.path.exists(FILA):
                shutil.copy2(FILA, FILA + '.antes_conferencia')
            gravar(FILA, fila + novos)
        dec[did] = {'status': 'ok', 'versoes': versoes, 'em': agora}
        gravar(DECISOES, dec)
        _espelhar_decisoes(dec)
        log(f'conferencia ok {did}: +{len(novos)} na fila')
        return True, f'{len(novos)} vídeo(s) foram para a fila de postagem.'


def _espelhar_decisoes(dec):
    try:
        no_lugar('decisoes_conferir.json', {'atualizado_em': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                                            'decisoes': dec, 'tinder': ler(TINDER, {})})
    except Exception as e:
        log(f'decisoes_conferir.json não atualizado: {e!r}')


# ------------------------------------------------------------------ limpeza automática

def limpar_postados():
    """Tira do fila.json o que o robô já postou (com cópia fila.json.antes_limpeza). Devolve quantos saíram."""
    with TRAVA:
        post = postados()
        fila = ler(FILA, None)
        if not isinstance(fila, list):
            return 0
        resto = [i for i in fila if i.get('doc') not in post]
        if len(resto) == len(fila):
            return 0
        shutil.copy2(FILA, FILA + '.antes_limpeza')
        gravar(FILA, resto)
        log(f'fila: {len(fila) - len(resto)} postado(s) removido(s)')
        return len(fila) - len(resto)


# ------------------------------------------------------------------ Produção

def aprovados_filtro():
    try:
        linhas = list(csv.DictReader(open(CONFERIDOS, encoding='utf-8-sig'), delimiter=';'))
    except Exception:
        return []
    linhas.sort(key=lambda l: (l.get('data') or '').strip())
    ult = {}
    for l in linhas:
        k = _id(l.get('itemId'))
        if k:
            ult[k] = l
    env = ler(ENVIADOS, {})
    tin = ler(TINDER, {})
    c = central()
    prod = ler(os.path.join(c, 'producao_status.json'), {}) if c else {}
    feitos = {_id(i) for i in (prod.get('produzidos') or [])}
    try:  # sem produto repetido: já produzidos (seus e do Kevin), descartados no Tinder etc. (lista no Drive)
        import pular_afiliados
        feitos |= pular_afiliados.ids()
    except Exception as e:
        log(f'pular_afiliados.json não lido: {e!r}')
    out = []
    for k, l in ult.items():
        if l.get('decisao') != 'aprovado' or k in env or k in feitos:
            continue
        if (tin.get(k) or {}).get('d') == 'nao':
            continue
        out.append({'itemId': k, 'tinder': 'gostei',  # Paola 23/11: aprovado pelo filtro entra direto na fila de produção
                    'nome': l.get('nome') or '', 'link': l.get('link') or '', 'videos': l.get('videos') or '',
                    'vendas': l.get('vendas') or '', 'comissao_rs': l.get('comissao_rs') or '', 'data': l.get('data') or '',
                    'motivo': l.get('motivo') or ''})
    out.sort(key=lambda x: x['data'], reverse=True)
    return out


def tinder(item_id, gostei):
    """Swipe no Tinder da Central: gostei = entra na fila de produção; não = some da lista."""
    with TRAVA:
        t = ler(TINDER, {})
        t[_id(item_id)] = {'d': 'gostei' if gostei else 'nao', 'em': datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
        gravar(TINDER, t)
    _espelhar_decisoes(ler(DECISOES, {}))
    return True, 'Foi para a fila de produção.' if gostei else 'Descartado.'


def desfazer_tinder(item_id):
    with TRAVA:
        t = ler(TINDER, {})
        t.pop(_id(item_id), None)
        gravar(TINDER, t)
    return True, 'Voltou para o Tinder.'


def produzir(ids=None):
    with TRAVA:
        disp = {x['itemId']: x for x in aprovados_filtro()}
        if not ids:
            ids = [k for k, x in disp.items() if x['tinder'] == 'gostei']
        itens = [disp[i] for i in dict.fromkeys(_id(i) for i in ids or []) if i in disp][:15]
        if not itens:
            return False, 'A fila de produção está vazia: dê ❤ no Tinder primeiro.'
        c = central()
        arq = os.path.join(c, 'ordem_producao.json') if c else None
        if not arq or not os.path.isfile(arq):
            return False, 'Falta o arquivo ordem_producao.json no Drive (Central Esposa). Peça à fábrica para criar.'
        ordem = ler(arq, {})
        ordem = ordem if isinstance(ordem, dict) else {}
        agora = datetime.datetime.now().astimezone()
        teto = round(len(itens) * TETO_POR_PRODUTO, 2)
        pedido = {'id': f'{agora:%Y%m%d-%H%M%S}', 'em': agora.isoformat(timespec='seconds'), 'teto_usd': teto,
                  'custo_estimado_usd': round(len(itens) * CUSTO_USD, 2), 'itens': itens}
        ordem['pedidos'] = (ordem.get('pedidos') or []) + [pedido]
        if not no_lugar('ordem_producao.json', ordem):
            return False, 'Não consegui gravar no Drive.'
        env = ler(ENVIADOS, {})
        for x in itens:
            env[x['itemId']] = {'pedido': pedido['id'], 'em': pedido['em']}
        gravar(ENVIADOS, env)
        log(f'produção: pedido {pedido["id"]} com {len(itens)} produtos, teto US$ {teto}')
        return True, f'Pedido enviado: {len(itens)} produto(s), teto US$ {teto:.2f}. A fábrica começa sozinha.'


def producao_estado():
    c = central()
    st = ler(os.path.join(c, 'producao_status.json'), {}) if c else {}
    ordem = ler(os.path.join(c, 'ordem_producao.json'), {}) if c else {}
    feitos = {p.get('id'): p for p in (st.get('pedidos') or []) if isinstance(p, dict)}
    pedidos = []
    for p in reversed((ordem.get('pedidos') or [])[-10:]):
        s = feitos.get(p.get('id'), {})
        pedidos.append({'id': p.get('id'), 'em': p.get('em'), 'n': len(p.get('itens') or []), 'teto_usd': p.get('teto_usd'),
                        'estado': s.get('estado') or 'na fila da fábrica', 'gasto_usd': s.get('gasto_usd')})
    return {'aprovados': aprovados_filtro(), 'pedidos': pedidos}


# ------------------------------------------------------------------ resumo para a tela

def estado():
    post = postados()
    fila = ler(FILA, [])
    lista = conferir_lista()
    ult = sorted(post.items(), key=lambda kv: kv[1]['em'], reverse=True)[:60]
    hoje = datetime.date.today()
    por_dia = {}
    for v in post.values():
        try:
            d = datetime.datetime.strptime(v['em'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc).astimezone().date()
        except Exception:
            continue
        por_dia[d.isoformat()] = por_dia.get(d.isoformat(), 0) + 1
    dias = [(hoje - datetime.timedelta(days=i)).isoformat() for i in range(13, -1, -1)]
    return {'drive': bool(central()), 'conferir': lista['pendentes'], 'na_fila_conferidos': lista['na_fila'],
            'fila': [{'doc': i.get('doc'), 'produto': i.get('produto') or ''} for i in fila if i.get('doc') not in post][:200],
            'postados': [{'doc': d, **v} for d, v in ult], 'postados_total': len(post),
            'postados_dia': [[d, por_dia.get(d, 0)] for d in dias],
            'producao': producao_estado(),
            'fabrica': ler(os.path.join(central(), 'painel.json'), {}) if central() else {}}


def faxina():
    """Limpeza automática (1x por dia): apaga só o que não serve mais. Nunca mexe em fila, postados, decisões ou vídeos
    ainda não postados.
    - prints de tela com mais de 15 dias (gravacao, afiliados/prints);
    - cópias de segurança (.antes_) com mais de 7 dias;
    - na pasta conferir do Drive: produtos recusados, ou aceitos com todas as versões já postadas, há mais de 30 dias."""
    agora = time.time()
    n = 0
    for pasta, dias, padrao in ((os.path.join(TABLET, 'gravacao'), 15, '*.png'), (os.path.join(TABLET, 'afiliados', 'prints'), 15, '*.png'),
                                (TABLET, 7, '*.antes_*'), (os.path.join(TABLET, 'afiliados'), 7, '*.antes_*')):
        for f in glob.glob(os.path.join(pasta, padrao)):
            try:
                if agora - os.path.getmtime(f) > dias * 86400:
                    os.remove(f)
                    n += 1
            except OSError:
                pass
    c = central()
    dec, post = ler(DECISOES, {}), postados()
    for did, d in docs_conferir().items() if c else ():
        x = dec.get(did) or {}
        try:
            velho = (datetime.datetime.now().astimezone() - datetime.datetime.fromisoformat(x.get('em'))).days > 30
        except Exception:
            continue
        acabou = x.get('status') == 'recusado' or all(v in post for v in (x.get('versoes') or []))
        if velho and acabou:
            try:
                os.remove(os.path.join(c, 'conferir', did + '.json'))
                n += 1
            except OSError:
                pass
    # vídeos no Drive (o que mais ocupa espaço): apaga 2 dias depois de postado, e os de produto recusado ou versão não
    # escolhida. Vão para a lixeira do Drive (some de vez em 30 dias).
    sobra = set()
    for did, d in docs_conferir().items() if c else ():
        x = dec.get(did) or {}
        if not x:
            continue
        for k in (d.get('posts') or {}):
            if x.get('status') == 'recusado' or k not in (x.get('versoes') or []):
                sobra.add(k)
    for k, v in post.items():
        try:
            em = datetime.datetime.strptime(v['em'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc)
            if (datetime.datetime.now(datetime.timezone.utc) - em).days >= 2:
                sobra.add(k)
        except Exception:
            pass
    for k in sobra:
        f = video(k)
        if f and os.path.isfile(f):
            try:
                os.remove(f)
                n += 1
            except OSError:
                pass
    if n:
        _IDX['t'] = 0
        log(f'faxina: {n} arquivo(s) inútil(eis) apagado(s)')
    return n


def loop():
    ult_faxina = 0
    while True:
        try:
            limpar_postados()
            if time.time() - ult_faxina > 86400:
                ult_faxina = time.time()
                faxina()
        except Exception as e:
            log(f'loop: {e!r}')
        time.sleep(60)


def iniciar():
    threading.Thread(target=loop, daemon=True).start()


# ------------------------------------------------------------------ Ajustes (a dona, 23/11: configurar sem o Claude)
REGUA = os.path.join(TABLET, 'afiliados', 'regua_filtro.json')
PERFIS = os.path.join(TABLET, 'afiliados', 'perfis_filtro.json')
LAYOUT = os.path.join(TABLET, 'assistir', 'layout.json')
APARELHOS = os.path.join(TABLET, 'aparelhos.json')
CONFIG_FILA = os.path.join(TABLET, 'config_fila.json')
CAMPOS_REGUA = {  # campo: (tipo, mínimo, máximo, texto)
    'max_videos_aprovado': (int, 0, 30, 'Máximo de vídeos de criadores no produto'),
    'views_video_vencedor': (int, 0, 10_000_000, 'Descarta se algum vídeo tiver estas views ou mais'),
    'comissao_min': (float, 0, 1000, 'Comissão mínima (R$)'),
    'comissao_min_taxa_alta': (float, 0, 1000, 'Comissão mínima quando a taxa é alta (R$)'),
    'taxa_alta_pct': (float, 0, 100, 'Taxa alta = comissão acima de (% do preço)'),
    'vendas_min': (int, 0, 100000, 'Vendas mínimas no total'),
    'exigir_venda_semana': (bool, 0, 1, 'Exigir venda nesta semana'),
    'meta_aprovados': (int, 0, 5000, 'Parar o filtro após N aprovados (0 = sem limite)'),
}
NO_PERFIL = ('max_videos_aprovado', 'meta_aprovados', 'exigir_venda_semana')  # o perfil ativo vence a régua


def _gravar_json(caminho, dados):
    tmp = caminho + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    json.load(open(tmp, encoding='utf-8'))
    os.replace(tmp, caminho)


def ajustes():
    rg, pf = ler(REGUA, {}), ler(PERFIS, {})
    perfis = pf.get('perfis') or {}
    ativo = pf.get('perfil_ativo') if pf.get('perfil_ativo') in perfis else (next(iter(perfis), ''))
    ef = {**rg, **(perfis.get(ativo) or {})}
    lay, ap, cf = ler(LAYOUT, {}), ler(APARELHOS, {}), ler(CONFIG_FILA, {})
    serial = (ap.get('celular1') or {}).get('usb', '')
    return {'filtro': {'perfil_ativo': ativo, 'perfis': list(perfis),
                       'campos': [{'k': k, 'tipo': t.__name__, 'min': a, 'max': b, 'txt': x, 'v': ef.get(k)}
                                  for k, (t, a, b, x) in CAMPOS_REGUA.items()]},
            'postagem': {'meta_posts': int(cf.get('meta_posts', 0) or 0)},
            'assistir': {'profile_name': lay.get('profile_name', ''), 'search_query': lay.get('search_query', ''),
                         'watch_min': lay.get('watch_min', 15), 'watch_max': lay.get('watch_max', 32)},
            'celular': {'serial': '' if serial.startswith('<') else serial}}


def gravar_ajustes(d):
    d = d if isinstance(d, dict) else {}
    msgs = []
    with TRAVA:
        f = d.get('filtro')
        if isinstance(f, dict):
            rg, pf = ler(REGUA, {}), ler(PERFIS, {})
            perfis = pf.setdefault('perfis', {})
            if f.get('perfil_ativo') in perfis:
                pf['perfil_ativo'] = f['perfil_ativo']
            alvo = perfis.setdefault(pf.get('perfil_ativo') or 'normal', {})
            for k, (t, a, b, _x) in CAMPOS_REGUA.items():
                if k not in f:
                    continue
                try:
                    v = (str(f[k]).lower() in ('1', 'true', 'sim', 'on')) if t is bool else t(str(f[k]).replace(',', '.'))
                except ValueError:
                    return False, f'Valor inválido em "{CAMPOS_REGUA[k][3]}".'
                if t is not bool and not a <= v <= b:
                    return False, f'"{CAMPOS_REGUA[k][3]}" deve ficar entre {a} e {b}.'
                (alvo if k in NO_PERFIL else rg)[k] = v
            rg['valida_desde'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            _gravar_json(REGUA, rg)
            _gravar_json(PERFIS, pf)
            msgs.append('filtro (vale na próxima vez que ligar o filtro)')
        p = d.get('postagem')
        if isinstance(p, dict) and 'meta_posts' in p:
            try:
                n = int(p['meta_posts'])
                assert 0 <= n <= 5000
            except Exception:
                return False, 'Quantidade de posts: um número de 0 a 5000 (0 = sem limite).'
            cf = ler(CONFIG_FILA, {})
            cf['meta_posts'] = n
            _gravar_json(CONFIG_FILA, cf)
            msgs.append('postagem')
        a = d.get('assistir')
        if isinstance(a, dict):
            lay = ler(LAYOUT, None)
            if not isinstance(lay, dict):
                return False, 'Não achei assistir\\layout.json.'
            for k in ('profile_name', 'search_query'):
                if k in a:
                    lay[k] = str(a[k]).strip().lstrip('@')[:80]
            for k in ('watch_min', 'watch_max'):
                if k in a:
                    lay[k] = max(3, min(300, int(a[k])))
            _gravar_json(LAYOUT, lay)
            msgs.append('assistir')
        c = d.get('celular')
        if isinstance(c, dict) and str(c.get('serial', '')).strip():
            s = re.sub(r'[^A-Za-z0-9:._-]', '', str(c['serial']))[:64]
            ap = ler(APARELHOS, {})
            # um celular só (POCO): fica como celular1; as contas revezam no mesmo aparelho (PC 23/11)
            c1 = ap.setdefault('celular1', {})
            c1['usb'] = s
            if not c1.get('nome') or c1['nome'].startswith('Celular 1 ('):
                c1['nome'] = 'POCO'
            c2 = ap.get('celular2') or {}
            if str(c2.get('usb') or '') in (s, '') or str(c2.get('usb') or '').startswith('<'):
                ap.pop('celular2', None)
            _gravar_json(APARELHOS, ap)
            lay = ler(LAYOUT, None)
            if isinstance(lay, dict):
                ph = {k: v for k, v in (lay.get('phones') or {}).items() if not k.startswith('<')}
                ph[s] = {'label': 'POCO', 'mode': (lay.get('phones') or {}).get(s, {}).get('mode', 'buscar_nome'), 'id_central': 'celular1'}
                lay['phones'] = ph
                _gravar_json(LAYOUT, lay)
            msgs.append('celular')
    return (True, 'Salvo: ' + ', '.join(msgs) + '.') if msgs else (False, 'Nada para salvar.')
