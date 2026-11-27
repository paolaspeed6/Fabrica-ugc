#!/usr/bin/env python3
"""Fábrica (nuvem) <-> Central do PC da Paola, pela pasta "Central Esposa" do Google Drive (23/11/2026).

uso:
  python3 -I central_drive.py semear                  cria a pasta e os arquivos que o PC reescreve no lugar (1x; idempotente)
  python3 -I central_drive.py filtro [filtro_resultado.json baixado pelo conector]  filtro do PC -> Tinder (config/filtro_pc)
  python3 -I central_drive.py candidatos AAAA-MM-DD [tarde]   produtos da varredura -> filtro do PC (candidatos-<dia>[_tarde].json)
  python3 -I central_drive.py pular                   lista anti-repetido do filtro (produzidos, Kevin, descartados)
  python3 -I central_drive.py conferir <pasta_do_lote>      conferir_docs/*.json -> Central Esposa/conferir/ (aba Conferir do PC)
  python3 -I central_drive.py painel                  números da fábrica (gasto, lotes) para a Central do PC
  python3 -I central_drive.py ler                     imprime ordens de produção, decisões da Conferência e postados do PC
  python3 -I central_drive.py status <arquivo.json>   grava producao_status.json (andamento e gasto dos pedidos)

Arquivos que o PC reescreve (ordem_producao.json, decisoes_conferir.json, postados_pc_nuvem.json) são criados AQUI,
porque o acesso ao Drive (escopo drive.file) só enxerga arquivos criados por este app. O PC nunca apaga/recria esses.
"""
import glob, json, os, sys, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'video-teste'))
import drive_backup as d  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
UP = 'https://content.googleapis.com/upload/drive/v3/files'
NO_LUGAR = {'ordem_producao.json': {'pedidos': []}, 'decisoes_conferir.json': {'decisoes': {}, 'tinder': {}},
            'postados_pc_nuvem.json': {'postados': []}, 'producao_status.json': {'pedidos': [], 'produzidos': []},
            'pular_afiliados.json': {}, 'nuvem.json': {'cards': []}}


def _q(s):
    return s.replace("'", "\\'")


def central(tk):
    c = d.pasta(tk, 'Central Esposa', 'root')
    return c, d.pasta(tk, 'conferir', c)


def achar(tk, nome, pai):
    r = d.listar(tk, f"name = '{_q(nome)}' and '{pai}' in parents and trashed = false")
    return r[0]['id'] if r else None


def criar(tk, nome, pai, dados):
    meta = json.dumps({'name': nome, 'parents': [pai], 'mimeType': 'application/json'})
    corpo = json.dumps(dados, ensure_ascii=False)
    b = 'fronteira_central'
    pacote = (f'--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n'
              f'--{b}\r\nContent-Type: application/json\r\n\r\n{corpo}\r\n--{b}--').encode()
    return json.loads(d.chamar(tk, 'POST', UP + '?uploadType=multipart&fields=id', pacote,
                               {'Content-Type': f'multipart/related; boundary={b}'})[2])['id']


def gravar(tk, nome, pai, dados):
    """Atualiza NO LUGAR (mesmo id) se existe; senão cria."""
    fid = achar(tk, nome, pai)
    if not fid:
        return criar(tk, nome, pai, dados)
    d.chamar(tk, 'PATCH', f'{UP}/{fid}?uploadType=media', json.dumps(dados, ensure_ascii=False).encode(),
             {'Content-Type': 'application/json'})
    return fid


def baixar(tk, nome, pai, padrao):
    fid = achar(tk, nome, pai)
    if not fid:
        return padrao
    try:
        return json.loads(d.chamar(tk, 'GET', f'{d.API}/files/{fid}?alt=media')[2] or b'null') or padrao
    except Exception:
        return padrao


def semear(tk):
    c, _ = central(tk)
    for nome, vazio in NO_LUGAR.items():
        if not achar(tk, nome, c):
            criar(tk, nome, c, vazio)
            print('criado', nome)
    pular(tk)


def candidatos(tk, dia, tarde):
    c, _ = central(tk)
    dd, mm = dia[8:10], dia[5:7]
    ids = json.load(open(os.path.join(AQUI, 'listas', f'{dd}{mm}_varredura_docs{"_tarde" if tarde else ""}.ids.json')))
    pasta = os.path.join(AQUI, 'listas', f'{dd}{mm}_varredura_docs')
    out = []
    for i in map(str, ids):
        p = os.path.join(pasta, i + '.json')
        if not os.path.exists(p):
            continue
        x = json.load(open(p))
        out.append({'itemId': i, 'link': x.get('link'), 'nome': x.get('nome', ''), 'comissao_rs': x.get('comissao_rs'),
                    'comissao_pct': x.get('comissao_pct'), 'pontos': x.get('pontos'), 'vendidos': x.get('vendidos'),
                    'vendas_dia': x.get('vendas_dia')})
    out.sort(key=lambda x: float(x.get('pontos') or 0), reverse=True)
    nome = f'candidatos-{dia}{"_tarde" if tarde else ""}.json'
    if not out:  # 27/11: pasta _varredura_docs movida antes da hora -> subiu lista vazia; nunca subir vazio
        sys.exit(f'{nome}: 0 produtos (a pasta listas/{dd}{mm}_varredura_docs sumiu?) — nada enviado')
    if len(sys.argv) > 4 and sys.argv[4] == 'regravar':
        gravar(tk, nome, c, out)
        print(nome, len(out), 'produtos regravados no Drive')
        return
    if achar(tk, nome, c):
        print(nome, 'já está no Drive')
        return
    criar(tk, nome, c, out)
    print(nome, len(out), 'produtos para o filtro do PC')
    # Drive limpo (a dona, 23/11): listas de candidatos com mais de 3 dias saem (o PC já importou)
    import datetime
    limite = (datetime.date.fromisoformat(dia) - datetime.timedelta(days=3)).isoformat()
    for f in d.listar(tk, f"name contains 'candidatos-' and '{c}' in parents and trashed = false"):
        if f['name'][11:21] < limite:
            d.chamar(tk, 'DELETE', f"{d.API}/files/{f['id']}")
            print('apagado do Drive:', f['name'])


def pular(tk):
    """Ids que o filtro do PC não confere: já produzidos/aprovados por ela, os do Kevin e os descartados no Tinder."""
    c, _ = central(tk)
    dec = json.load(open(os.path.join(AQUI, 'decididos.json')))
    kevin = set()
    for v in json.load(open(os.path.join(AQUI, 'excluidos.json'))).values():
        kevin |= set(map(str, v))
    desc = set(json.load(open(os.path.join(AQUI, 'listas', 'tinder_descartados_apagados.json'))))
    st = baixar(tk, 'producao_status.json', c, {})
    prod = set(map(str, dec)) | set(map(str, st.get('produzidos') or []))
    dados = {'produzidos': sorted(prod), 'kevin': sorted(kevin), 'descartados_tinder': sorted(desc)}
    gravar(tk, 'pular_afiliados.json', c, dados)
    print('pular_afiliados.json:', len(prod), 'produzidos,', len(kevin), 'do Kevin,', len(desc), 'descartados')


def conferir(tk, lote):
    _, pc = central(tk)
    ja = {f['name'] for f in d.listar(tk, f"'{pc}' in parents and trashed = false")}
    n = 0
    for f in sorted(glob.glob(os.path.join(lote, 'conferir_docs', '*.json'))):
        nome = os.path.basename(f)
        if nome in ja:
            continue
        criar(tk, nome, pc, json.load(open(f)))
        n += 1
    print(n, 'produto(s) na aba Conferir do PC')


def desperdicio(arq):
    """Soma o agentes/desperdicios.md: linhas da tabela (coluna US$) e "refações de imagem (US$ x)" das seções de lote."""
    import re, datetime
    mes_atual = datetime.date.today().isoformat()[:7]
    tot = mes = 0.0
    casos, sec_data, sec = [], None, ''
    for l in open(arq, encoding='utf-8').read().splitlines():
        m = re.match(r'\| (\d{4}-\d\d-\d\d) \| ([^|]*)\| ([^|]*)\| ([\d,]+) \|[^|]*\|([^|]*)\|', l)
        if m:
            v = float(m[4].replace(',', '.'))
            tot += v
            mes += v if m[1][:7] == mes_atual else 0
            casos.append({'data': m[1], 'lote': m[3].strip(), 'usd': v, 'motivo': m[5].strip()[:120]})
            continue
        h = re.match(r'## (.*) \((\d\d)/(\d\d)\)', l)
        if h:
            sec_data, sec = f'{mes_atual[:4]}-{h[3]}-{h[2]}', h[1]
            continue
        for x in re.findall(r'refa\w+ de \w+ \(US\$ ([\d,]+)\)', l):
            v = float(x.replace(',', '.'))
            tot += v
            mes += v if (sec_data or '')[:7] == mes_atual else 0
            casos.append({'data': sec_data, 'lote': sec, 'usd': v, 'motivo': l.strip('- ')[:120]})
    return {'total_usd': round(tot, 2), 'mes_usd': round(mes, 2), 'ultimos': casos[-6:][::-1]}


def painel(tk):
    """Números da fábrica para a Central do PC: gasto do mês/total, lotes (vídeos e US$), última busca."""
    import subprocess, tempfile
    raiz = os.path.join(AQUI, '..', '..')
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, 'posts'))
        out = subprocess.run([sys.executable, '-I', os.path.join(raiz, 'paginas', 'central', 'montar.py'), t],
                             capture_output=True, text=True, check=True).stdout
    p = json.loads(out)
    dados = {k: p.get(k) for k in ('gasto', 'lotes', 'varredura', 'atualizado_em', 'nao_medido')}
    dados['lotes'] = [{k: l.get(k) for k in ('nome', 'produtos', 'videos', 'usd')} for l in (dados['lotes'] or [])]
    dados['desperdicio'] = desperdicio(os.path.join(raiz, 'agentes', 'desperdicios.md'))
    c, _ = central(tk)
    gravar(tk, 'painel.json', c, dados)
    print('painel.json: mês US$', dados['gasto'].get('mes_usd'), '·', len(dados['lotes']), 'lotes')


def ler(tk):
    c, _ = central(tk)
    print(json.dumps({k: baixar(tk, k, c, {}) for k in ('ordem_producao.json', 'producao_status.json',
                                                         'decisoes_conferir.json', 'postados_pc_nuvem.json')},
                     ensure_ascii=False, indent=1))


def filtro(tk, arq=None):
    """25/11 (a dona): resultado do filtro do PC -> Tinder. O PC grava filtro_resultado.json na Central Esposa
    (afiliados\\resultado_drive.py). Arquivo criado pelo PC: o token drive.file pode não enxergar -> baixe com o
    CONECTOR Google Drive e passe o caminho. Grava filtro_pc_doc.json = doc config/filtro_pc do Tinder
    {r: só ids do Tinder, k: ids do Kevin que estão no Tinder} (a página tira "descarta" e os do Kevin, sobe os aprovados)."""
    import glob
    if arq:
        dados = json.load(open(arq, encoding='utf-8-sig'))
    else:
        c, _ = central(tk)
        dados = baixar(tk, 'filtro_resultado.json', c, {})
    meus = set()
    for f in glob.glob(os.path.join(AQUI, 'listas', '*.ids.json')):
        meus |= set(map(str, json.load(open(f))))
    r = {i: v[:4] for i, v in (dados.get('r') or {}).items() if i in meus}
    sys.path.insert(0, AQUI); import trava_kevin
    k = sorted(meus & trava_kevin.kevin_ids())
    doc = {'quando': dados.get('quando', ''), 'r': r, 'k': k}
    json.dump(doc, open(os.path.join(AQUI, 'filtro_pc_doc.json'), 'w'), ensure_ascii=False)
    n = lambda x: sum(1 for v in r.values() if v[0] == x)
    print(f"filtro do PC ({doc['quando'] or 'sem arquivo'}): {n('aprovado')} aprovados, {n('descarta')} fora, "
          f"{n('revisar')} revisar no Tinder; {len(k)} do Kevin escondidos -> filtro_pc_doc.json (ArtifactData set config/filtro_pc)")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    tk = d.token()
    if a[0] == 'semear':
        semear(tk)
    elif a[0] == 'candidatos':
        candidatos(tk, a[1], len(a) > 2 and a[2] == 'tarde')
    elif a[0] == 'pular':
        pular(tk)
    elif a[0] == 'conferir':
        conferir(tk, a[1])
    elif a[0] == 'filtro':
        filtro(tk, a[1] if len(a) > 1 else None)
    elif a[0] == 'painel':
        painel(tk)
    elif a[0] == 'ler':
        ler(tk)
    elif a[0] == 'status':
        c, _ = central(tk)
        gravar(tk, 'producao_status.json', c, json.load(open(a[1])))
        print('producao_status.json atualizado')
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
