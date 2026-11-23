r"""Teste a seco da trava de produto. NUNCA toca em Postar.

Vai até logo antes de Postar com um produto da fila, confere que o cartão certo é aceito e que um nome
errado é recusado, fecha o app sem publicar e tira o vídeo de teste da galeria. Só grava trava_ok.json
(o que libera o Desbloquear da Central) se os dois lados passarem.

Uso, com um celular livre (sem robô e sem fila):
    set HORST_ADB_SERIAL=<IP_DO_CELULAR1>:5555
    set PYTHONPATH=C:\horst\tablet\pylibs
    python teste_trava.py
"""
import datetime, json, os, sys, time
sys.path.insert(0, r'C:\horst\tablet')
import postar_shopee as ps, rodar_fila as r

DOC = sys.argv[1] if len(sys.argv) > 1 else '0411F_14_perfume-hawas-thunder_B'
ERRADO = 'Lona Plástica Azul CK100 10x8 M 100 Micras Impermeável para Cobertura Temporária Telhados Obras Camping Barracas'
TRAVA_OK = os.path.join(r.BASE, 'trava_ok.json')

item = next(i for i in r.carregar_filas() if i['doc'] == DOC)
if r.estado().get(DOC, '').startswith('postado'):
    sys.exit('esse post já saiu: escolha outro DOC')
video = r.baixar(item)
leg = item['legenda'].replace('\\n', '\n')
iid = r.itemid_de(item['link'], r.carregar(r.ITEMIDS, {}))
ps.ITEM_ID = iid
ps.TITULO_CACHE = r.carregar(r.TITULOS, {}).get(iid)
ps.PRODUTO_TEXTOS = ps.TITULO_ESPERADO = None
r.ULTIMO_PRODUTO = None
ps.VALIDAR_PAGINA = r.validador_de_pagina(item, ps.TITULO_CACHE)
aceitou = recusou = False
t0 = time.time()
try:
    ps.postar(video, item['link'], leg, seco=True, favoritar=True)
    aceitou = ps.TOCOU_POSTAR is False
    print('cartão certo aceito em', round(time.time() - t0), 's', flush=True)
    certo, ps.TITULO_ESPERADO = ps.TITULO_ESPERADO, ERRADO
    try:
        ps.conferir_cartao_antes_de_postar()
        print('FALHOU: o cartão aceitou um nome errado', flush=True)
    except ps.Parou as e:
        recusou = True
        print('nome errado recusado:', str(e)[:160], flush=True)
    ps.TITULO_ESPERADO = certo
except Exception as e:
    print('PAROU:', type(e).__name__, e, 'foco', ps.foco().strip()[-60:], flush=True)
finally:
    tocou = ps.TOCOU_POSTAR
    print('TOCOU_POSTAR', tocou, flush=True)
    # sair sem publicar: fecha o app à força, sem voltar por cima dos botões
    ps.sh(f'am force-stop {ps.PKG}')
    time.sleep(1)
    n = os.path.basename(video)
    ps.sh(f"rm -f '{ps.DESTINO}/{n}'")
    ps.sh(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d 'file://{ps.DESTINO}/{n}'")
    ps.sh('input keyevent KEYCODE_HOME')
    print('galeria:', repr(ps.sh(f'ls {ps.DESTINO} 2>/dev/null').strip()), flush=True)
if aceitou and recusou and not tocou:
    json.dump({'ok': True, 'por': 'teste_trava', 'doc': DOC, 'aparelho': ps.SERIAL,
               'quando': datetime.datetime.now().astimezone().isoformat(timespec='seconds')},
              open(TRAVA_OK, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('PASSOU: trava_ok.json gravado', flush=True)
else:
    print('NÃO passou: trava_ok.json não foi gravado', flush=True)
    sys.exit(1)
