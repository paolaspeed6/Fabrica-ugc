"""Roda a lista de candidatos do Drive em lotes de 50 até passar de 150 aprovados no dia.

- Lista: G:\\Meu Drive\\Central Esposa\\candidatos_afiliados.json (ordem de v7 decrescente)
- Pula itemIds já em conferidos.csv. Espera um lote que esteja rodando terminar antes.
- Para: aprovados do dia > META, lista acabou, arquivo afiliados\\PARAR, ou o robô parou por
  captcha não resolvido/login (código de saída 1).
- Entre lotes reclassifica o CSV com a régua atual (decidir()).
"""
import csv, datetime, json, os, subprocess, sys, time

BASE = r'C:\horst\tablet'
PASTA = os.path.join(BASE, 'afiliados')
LISTA = next((f'{l}:\\{r}\\Central Esposa\\candidatos_afiliados.json' for l in 'GHIJKLMNOPQRSTUVWXYZDEF' for r in ('Meu Drive', 'My Drive')
                 if __import__('os').path.isdir(f'{l}:\\{r}\\Central Esposa')), r'G:\Meu Drive\Central Esposa\candidatos_afiliados.json')  # Paola: letra do Drive automática
FILA_LOCAL = r'C:\horst\tablet\afiliados\fila_filtro.json'  # 10/11: busca de hoje + restantes; tem prioridade sobre a lista do Drive
CSV = os.path.join(PASTA, 'conferidos.csv')
PARAR = os.path.join(PASTA, 'PARAR')
META, LOTE = 150, 50
sys.path.insert(0, BASE)
import aparelho_atual as ap  # noqa: E402
ID_APARELHO = ap.id_aparelho()  # um robô por aparelho (HORST_ADB_SERIAL)
LOCK = os.path.join(PASTA, f'conferir_{ID_APARELHO}.lock')
LOCK_SEQ = os.path.join(PASTA, f'candidatos_{ID_APARELHO}.lock')
PARAR_ID = f'{PARAR}_{ID_APARELHO}'


def log(m):
    linha = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} [candidatos] {m}'
    print(linha, flush=True)
    open(os.path.join(PASTA, 'conferir_afiliados.log'), 'a', encoding='utf-8').write(linha + '\n')


def linhas():
    try:
        return list(csv.DictReader(open(CSV, encoding='utf-8-sig'), delimiter=';'))
    except Exception:
        return []


def reclassificar():
    import conferir_afiliados as c
    with ap.trava_csv():  # 2 robôs: ninguém grava enquanto o CSV é reescrito
        ls = linhas()
        for l in ls:
            c.completar_recentes(l)
            if l['decisao'] in ('ja_produzido', 'esgotado', 'erro_carregar'):  # decisões fixas: não reclassificar
                continue
            if l['decisao'] != 'erro':
                l['decisao'], l['motivo'] = c.decidir(l)
            l['prioridade'] = c.prioridade(l)
            l['zero_videos'] = 'sim' if l.get('decisao') == 'aprovado' and str(l.get('videos')).strip() == '0' else ''
        tmp = CSV + f'.{ID_APARELHO}.tmp'
        with open(tmp, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=c.CAMPOS, delimiter=';', extrasaction='ignore')
            w.writeheader()
            w.writerows(ls)
        for tentativa in range(20):  # alguém pode estar só lendo o CSV: tenta de novo
            try:
                os.replace(tmp, CSV)
                break
            except PermissionError:
                time.sleep(0.5)
    c.gerar_aprovados_zero()
    sys.path.insert(0, PASTA)
    import status_card
    status_card.escrever('parado')


ADB = [os.path.join(BASE, 'platform-tools', 'adb.exe'), '-s', '<SERIAL_TABLET>']


def conectado():
    """USB ou Wi-Fi (aparelhos.json), tentando 'adb connect' no Wi-Fi — via postar_shopee."""
    try:
        import postar_shopee as ps
        ps.conectar_rapido = ps.escolher_tablet(reconectar=False)
        return True
    except Exception:
        return False


def wifi_do_tablet():
    if os.environ.get('HORST_ADB_SERIAL'):  # aparelho escolhido por variável
        return ap.wifi_de()
    try:
        d = json.load(open(os.path.join(BASE, 'aparelhos.json'), encoding='utf-8-sig'))
        return (d.get('tablet') or {}).get('wifi')
    except Exception:
        return None


def esperar_tablet(limite=30 * 60):
    """Tablet sumiu: tenta 'adb connect' no IP do aparelhos.json a cada 30 s (até 30 min).
    Só pede o cabo se o connect responder 'refused' (o tablet reiniciou e perdeu o adb Wi-Fi)."""
    if conectado():
        return
    ip = wifi_do_tablet()
    log(f'tablet sumiu do adb: tentando reconectar no Wi-Fi {ip} a cada 30 s (até 30 min)')
    fim = time.time() + limite
    avisou_cabo = False
    while time.time() < fim:
        saida = ''
        if ip:
            try:
                saida = subprocess.run([ADB[0], 'connect', ip], capture_output=True, text=True, timeout=20,
                                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout.lower()
            except Exception as e:
                saida = str(e).lower()
        if conectado():
            log('tablet voltou')
            time.sleep(5)
            return
        if 'refused' in saida and not avisou_cabo:
            avisou_cabo = True
            log('adb connect recusado: o tablet reiniciou — precisa do cabo USB 1 minuto para religar o Wi-Fi')
            try:
                sys.path.insert(0, PASTA)
                import status_card
                status_card.escrever('alerta', aviso='tablet reiniciou: ligue o cabo USB 1 min para religar o Wi-Fi')
            except Exception:
                pass
        time.sleep(30)
    log('tablet não voltou em 30 min — parando')
    sys.exit(1)


def aprovados_hoje():
    hoje = f'{datetime.date.today():%Y-%m-%d}'
    ult = {}
    for l in linhas():  # histórico: vale a última linha de cada produto
        ult[l['itemId'] or l['link']] = l
    return sum(1 for l in ult.values() if l['data'].startswith(hoje) and l['decisao'] == 'aprovado')


def vivo(arq):
    try:  # 22/11: pid_real = python + script do robô + criado antes do lock (pid reaproveitado = lock morto, removido)
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import pid_real
        return pid_real.lock_vivo(arq)
    except ImportError:
        pass
    try:
        pid = int(open(arq).read())
        saida = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'], capture_output=True, text=True,
                               timeout=15, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
        return any(str(pid) in l and 'python' in l.lower() for l in saida.splitlines())  # 13/11: PID reaproveitado por outro programa (chrome) não é robô vivo
    except Exception:
        return False


def carregar_cand():
    """Lê a lista de candidatos e tira comissão baixa e os já produzidos/esposa/etc. (usado no início e quando a lista muda)."""
    cand = json.load(open(FILA_LOCAL if os.path.exists(FILA_LOCAL) else LISTA, encoding='utf-8'))
    log(f'lista: {FILA_LOCAL if os.path.exists(FILA_LOCAL) else LISTA} ({len(cand)} produtos)')
    # Kevin (05/11): comissão abaixo do mínimo nem abre no tablet; só lista em pulados_comissao.txt
    import conferir_afiliados as _c
    minimo = min(getattr(_c, 'COMISSAO_MIN', 20.0), getattr(_c, 'COMISSAO_MIN_TAXA_ALTA', 20.0))  # 15-20: o robô decide
    baixos = [c for c in cand if c.get('comissao_rs') is not None and float(c['comissao_rs']) < minimo]
    if baixos:
        with open(os.path.join(PASTA, 'pulados_comissao.txt'), 'w', encoding='utf-8') as f:
            f.write('itemId;comissao_rs\n' + ''.join(f'{c["itemId"]};{c["comissao_rs"]}\n' for c in baixos))
        log(f'{len(baixos)} candidatos pulados por comissão < R$ {minimo:.0f} (pulados_comissao.txt)')
    cand = [c for c in cand if c not in baixos]
    import pular_afiliados
    return pular_afiliados.tirar(cand, log)  # produzidos, tinder, esposa, reaprovados (lista no Drive)


def main():
    try:  # 11/11: o "assistir" do Kevin usa o celular: não sobe em cima dele
        import assistir_uso
        if assistir_uso.assistir_usa(ID_APARELHO):
            log(f'{ID_APARELHO}: o assistir está rodando neste celular — não subo o filtro (desligue o assistir)')
            return
    except ImportError:
        pass
    if vivo(LOCK_SEQ):
        log(f'{ID_APARELHO}: já tem uma sequência rodando neste aparelho')
        return
    open(LOCK_SEQ, 'w').write(str(os.getpid()))
    ap.limpar_parada(ID_APARELHO)
    os.environ.setdefault('HORST_INICIO_SEQ', f'{datetime.datetime.now():%Y-%m-%d %H:%M}')  # meta do perfil conta daqui
    while vivo(LOCK):  # lote anterior ainda rodando (lock de processo morto não prende mais)
        time.sleep(15)
    try:  # 14/11: ao rodar, puxa candidatos novos do Drive para a fila (sem vigia)
        sys.path.insert(0, PASTA)
        import ponte_candidatos
        ponte_candidatos.importar()
    except Exception as e:
        log(f'(ponte do Drive falhou: {e!r})')
    reclassificar()
    cand = carregar_cand()
    mtime_lista = os.path.getmtime(FILA_LOCAL if os.path.exists(FILA_LOCAL) else LISTA)
    n_lote = 0
    while True:
        if os.path.exists(PARAR) or os.path.exists(PARAR_ID):
            log(f'{ID_APARELHO}: PARAR encontrado — parando')
            return
        try:  # Kevin 10/11: lista nova (busca/extras/faltantes) entra sem religar: relê quando o arquivo muda
            m = os.path.getmtime(FILA_LOCAL if os.path.exists(FILA_LOCAL) else LISTA)
            if m != mtime_lista:
                mtime_lista = m
                cand = carregar_cand()
        except Exception as e:
            log(f'(releitura da lista falhou: {e})')
        try:  # 22/11: pular_afiliados.json (produzidos etc.) relido a CADA lote, em todos os perfis
            import pular_afiliados
            cand = pular_afiliados.tirar(cand, log)
        except Exception as e:
            log(f'(releitura do pular_afiliados falhou: {e})')
        qtd = aprovados_hoje()
        import conferir_afiliados as _cm
        if _cm.META_APROV and _cm.aprovados_da_sequencia() >= _cm.META_APROV:
            log(f'META do perfil {_cm.PERFIL_NOME} batida: {_cm.META_APROV} aprovados nesta sequência')
            ap.gravar_parada(ID_APARELHO, f'normal: META batida (perfil {_cm.PERFIL_NOME})')
            return
        if not _cm.META_APROV and False and qtd > META:  # 21/11: meta 0 = sem limite (o teto de 150/dia saiu)
            log(f'META batida: {qtd} aprovados hoje (> {META})')
            ap.gravar_parada(ID_APARELHO, 'normal: META batida')
            try:
                import status_card
                status_card.escrever('parado', aviso=f'Meta do dia batida: {qtd} aprovados hoje (> {META}).')
            except Exception:
                pass
            return
        feitos = {str(l['itemId']).split('.')[-1] for l in linhas() if l['decisao'] != 'erro'}
        # Kevin 10/11: produto que deu erro (ex.: "falhou ao carregar") 2x HOJE não volta no mesmo dia: sem isso o
        # último item da lista ficava em laço infinito na mesma tela. Fica para o recheck de amanhã.
        _hoje, _erros = f'{datetime.date.today():%Y-%m-%d}', {}
        for l in linhas():
            if l['decisao'] == 'erro' and str(l.get('data', '')).startswith(_hoje):
                k = str(l['itemId']).split('.')[-1]
                _erros[k] = _erros.get(k, 0) + 1
        feitos |= {k for k, n in _erros.items() if n >= 2}
        resto = [c for c in cand if str(c['itemId']) not in feitos]
        if not resto:
            log(f'lista acabou ({qtd} aprovados hoje)')
            ap.gravar_parada(ID_APARELHO, 'normal: lista acabou')
            try:  # 10/11 (Kevin): "Ligar" não fazia nada e a Central não dizia por quê
                import status_card
                status_card.escrever('parado', aviso=f'Lista do dia acabou: sem produtos novos para conferir ({qtd} aprovados hoje). '
                                                     'Novos candidatos só na próxima busca (veja "Busca" na Linha do dia).')
            except Exception:
                pass
            return
        n_lote += 1
        arq = os.path.join(PASTA, f'lote_cand_{ID_APARELHO}_{n_lote:02d}.json')
        json.dump([{'itemId': c['itemId'], 'link': c['link'], 'nome': c.get('nome', ''), 'v7': c.get('v7'),
                    'primeira_vez': c.get('primeira_vez')} for c in resto[:LOTE]],
                  open(arq, 'w', encoding='utf-8'), ensure_ascii=False)
        log(f'{ID_APARELHO} lote {n_lote}: {min(LOTE, len(resto))} produtos (faltam {len(resto)}; aprovados hoje {qtd})')
        esperar_tablet()
        r = subprocess.run([sys.executable, os.path.join(BASE, 'conferir_afiliados.py'), arq], cwd=BASE)
        reclassificar()
        if r.returncode != 0 and not conectado():
            log('robô parou com o tablet desconectado — espero voltar e continuo')
            continue
        if r.returncode != 0:
            log(f'robô saiu com código {r.returncode} (captcha/login/erro) — parando a sequência')
            return


if __name__ == '__main__':
    main()
