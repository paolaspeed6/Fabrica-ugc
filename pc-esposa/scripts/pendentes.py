r"""Pendentes de aprovação (10/11, Kevin): produto que não deu para vincular com certeza.

A fila NÃO espera: grava o item aqui (com print da lista Adicionar e os nomes das linhas vistas),
sai do editor sem postar e segue para o próximo. As outras versões (A/B/C) do mesmo produto ficam
fora da fila enquanto o produto estiver pendente.

Na Central o Kevin:
  - Aprova: escolhe qual linha (nome) é o produto certo. O nome vai para titulos.json["_aprovados"]
    [itemId] com approved_by "kevin" e o item volta para a fila (sai daqui).
  - Recusa: as versões vão para pulados.json com motivo "recusado_kevin".
Sugestão do Haiku (opcional) é só texto no cartão: nunca aprova nem posta.
"""
import contextlib, datetime, json, os, re, shutil, time

BASE = r'C:\horst\tablet'
ARQ = os.path.join(BASE, 'pendentes_aprovacao.json')
PULADOS = os.path.join(BASE, 'pulados.json')
TITULOS = os.path.join(BASE, 'titulos.json')
GRAV = os.path.join(BASE, 'gravacao')
TRAVA = os.path.join(BASE, 'postados.json.trava')  # a mesma trava do rodar_fila (postados/pulados)


def _agora():
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')


def _ler(caminho, padrao):
    try:
        return json.load(open(caminho, encoding='utf-8-sig'))
    except Exception:
        return padrao


def _gravar(caminho, dados):
    tmp = caminho + '.tmp'
    json.dump(dados, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, caminho)


@contextlib.contextmanager
def trava(limite=30):
    fim = time.time() + limite
    while True:
        try:
            fd = os.open(TRAVA, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(TRAVA) > 60:
                    os.remove(TRAVA)
                    continue
            except OSError:
                pass
            if time.time() > fim:
                raise TimeoutError('arquivos da fila travados')
            time.sleep(0.2)
    try:
        yield
    finally:
        os.close(fd)
        with contextlib.suppress(OSError):
            os.remove(TRAVA)


def listar():
    return [p for p in _ler(ARQ, []) if isinstance(p, dict) and p.get('id')]


def docs_pendentes():
    """Todos os docs fora da fila por estarem pendentes (o item e as outras versões do produto)."""
    out = set()
    for p in listar():
        out.update(p.get('docs') or [p.get('doc')])
    out.discard(None)
    return out


def codigo(doc):
    s = str(doc or '').rsplit('_', 1)
    return s[1] if len(s) == 2 and len(s[1]) <= 2 else ''


def adicionar(item, docs, item_id, motivo, tipo, linhas, print_origem=None, video=None, aparelho=None,
              esperado=None):
    """Grava o item como pendente (um registro por produto; versões já pendentes entram no mesmo)."""
    doc = item['doc']
    os.makedirs(GRAV, exist_ok=True)
    img = ''
    if print_origem and os.path.isfile(print_origem):
        img = os.path.join(GRAV, f'pend_{doc}.png')
        try:
            shutil.copyfile(print_origem, img)
        except Exception:
            img = ''
    linhas = [str(l)[:200] for l in dict.fromkeys(l for l in (linhas or []) if l)][:30]
    with trava():
        lista = listar()
        reg = next((p for p in lista if doc in (p.get('docs') or []) or p.get('doc') == doc), None)
        novo = {
            'id': doc, 'doc': doc, 'codigo': codigo(doc), 'docs': list(dict.fromkeys([doc, *(docs or [])])),
            'video': video or '', 'produto': item.get('produto') or '', 'esperado': esperado or '',
            'itemId': item_id or '', 'link': item.get('link') or '', 'motivo': str(motivo)[:400], 'tipo': tipo,
            'hora': _agora(), 'print': os.path.basename(img) if img else '', 'linhas_vistas': linhas,
            'aparelho': aparelho or '',
        }
        if reg:
            reg.update({k: v for k, v in novo.items() if k not in ('id',)})
            reg.pop('sugestao', None)
            reg.pop('sugestao_tentada', None)
        else:
            lista.append(novo)
            reg = novo
        _gravar(ARQ, lista)
    return reg


def definir(pid, **campos):
    with trava():
        lista = listar()
        for p in lista:
            if p['id'] == pid:
                p.update(campos)
                _gravar(ARQ, lista)
                return True
    return False


def _chave_aprov(p):
    return p.get('itemId') or ('produto:' + ' '.join(str(p.get('produto') or '').lower().split()))


def base_do_doc(doc):
    """doc sem a versão (_A/_B/_C/_Reels): '1111G_04_kit-vara..._A' -> '1111G_04_kit-vara...' (o mesmo produto)."""
    s = str(doc or '')
    return re.sub(r'_(A|B|C|Reels)$', '', s)


def aprovado(item_id, produto, doc=None):
    """Nome aprovado pelo Kevin para este itemId, para o produto-base do doc (todas as versões A/B/C) ou para o
    nome do produto (sem itemId), ou None. Kevin 13/11: aprovou uma versão, vale para todas."""
    ap = _ler(TITULOS, {}).get('_aprovados') or {}
    chaves = [item_id, ('base:' + base_do_doc(doc)) if doc else None,
              'produto:' + ' '.join(str(produto or '').lower().split())]
    for k in chaves:
        if k and isinstance(ap.get(k), dict) and ap[k].get('nome'):
            return ap[k]['nome']
    return None


def aprovar(escolhas):
    """escolhas: {id_pendente: nome_da_linha}. Guarda o nome exato aprovado e devolve o item à fila."""
    feitos, erros = [], []
    with trava():
        lista = listar()
        titulos = _ler(TITULOS, {})
        ap = titulos.setdefault('_aprovados', {})
        for pid, nome in (escolhas or {}).items():
            p = next((x for x in lista if x['id'] == pid), None)
            nome = re.sub(r'^\((?:OCR(?: do print)?|nome na página do link)\)\s*', '', str(nome or '').strip())
            if not p:
                erros.append(f'{pid}: não está mais pendente')
                continue
            if len(nome) < 5:
                erros.append(f'{pid}: escolha a linha certa')
                continue
            reg_ap = {'nome': nome, 'approved_by': 'kevin', 'hora': _agora(), 'doc': p['doc'],
                      'esperado': p.get('esperado') or p.get('produto') or ''}
            ap[_chave_aprov(p)] = reg_ap
            # 13/11 (Kevin: "aprovou uma versão, todas as mesmas também"): grava também pelo produto-base de CADA doc
            # do pendente (A/B/C) e pelo nome do produto, e aprova junto qualquer pendente irmão.
            for d in (p.get('docs') or [p['doc']]):
                ap['base:' + base_do_doc(d)] = reg_ap
            if p.get('produto'):
                ap['produto:' + ' '.join(str(p['produto']).lower().split())] = reg_ap
            _registrar_feedback('aprovado', p, nome)
            lista.remove(p)
            feitos.append(pid)
            irmaos = [x for x in lista if x is not p and (
                (p.get('itemId') and x.get('itemId') == p.get('itemId')) or
                {base_do_doc(d) for d in (x.get('docs') or [x['doc']])} & {base_do_doc(d) for d in (p.get('docs') or [p['doc']])})]
            for x in irmaos:  # pendente irmão (mesmo itemId ou mesmo produto-base): aprovado junto
                _registrar_feedback('aprovado_irmao', x, nome)
                lista.remove(x)
                feitos.append(x['id'])
        if feitos:
            _gravar(TITULOS, titulos)
            _gravar(ARQ, lista)
    return feitos, erros


FEEDBACK_JSON = os.path.join(BASE, 'feedback_aprovacoes.json')
FEEDBACK_MD = os.path.join(BASE, 'feedback_aprovacoes.md')


def _registrar_feedback(decisao, p, escolhido=''):
    """Aprendizado com o Kevin (10/11): guarda a decisão (nome do vídeo/produto, nome esperado, linhas vistas, linha
    escolhida, itemId) em feedback_aprovacoes.json e num resumo legível (.md) com os padrões de divergência de nome.
    A aprovação por itemId já impede o mesmo produto de voltar a pendente (titulos.json _aprovados)."""
    try:
        reg = {'hora': _agora(), 'decisao': decisao, 'doc': p.get('doc'), 'itemId': p.get('itemId') or '',
               'produto_video': p.get('produto') or '', 'esperado': p.get('esperado') or '',
               'escolhido': escolhido, 'tipo': p.get('tipo') or '', 'motivo': (p.get('motivo') or '')[:200],
               'linhas_vistas': (p.get('linhas_vistas') or [])[:30]}
        dados = _ler(FEEDBACK_JSON, [])
        dados.append(reg)
        _gravar(FEEDBACK_JSON, dados)
        linhas = ['# Feedback do Kevin nas aprovações (gerado automaticamente)', '',
                  'Cada linha: o que o robô esperava/via x o que o Kevin escolheu. Padrões = divergências de nome já aceitas.', '']
        for r in dados[-200:]:
            esc = r['escolhido'] or '(recusado)'
            linhas.append(f"- {r['hora'][:16]} · {r['decisao']} · {r['doc']} · vídeo: {r['produto_video']} · "
                          f"esperado: {r['esperado'] or '—'} · escolhido: {esc} · itemId {r['itemId'] or '—'} · tipo {r['tipo']}")
        with open(FEEDBACK_MD, 'w', encoding='utf-8') as f:
            f.write('\n'.join(linhas) + '\n')
    except Exception:
        pass


def recusar(ids):
    feitos = []
    with trava():
        lista = listar()
        pul = _ler(PULADOS, [])
        ja = {x.get('doc') for x in pul if isinstance(x, dict)}
        for pid in ids or []:
            p = next((x for x in lista if x['id'] == pid), None)
            if not p:
                continue
            for d in p.get('docs') or [p['doc']]:
                if d not in ja:
                    pul.append({'doc': d, 'hora': _agora(), 'motivo': 'recusado_kevin', 'por': 'central',
                                'detalhe': (p.get('motivo') or '')[:200]})
                    ja.add(d)
            lista.remove(p)
            feitos.append(pid)
        if feitos:
            _gravar(PULADOS, pul)
            _gravar(ARQ, lista)
    return feitos
