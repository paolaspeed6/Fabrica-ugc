"""Trava Kevin (a dona, 25/11: "jamais sugira produtos repetidos para mim e para o Kevin").
Erro que motivou: de 10/11 a 25/11 a rotina procurava os excluidos_kevin_* com o token GDRIVE_* (escopo drive.file),
que NÃO enxerga arquivos do Kevin -> "nada novo" por 15 dias, 36 produtos dele no Tinder dela e 1 num lote pago.

uso:
  python3 trava_kevin.py registrar <titulos_vistos_no_drive.txt> [excluidos_kevin_*.json baixados...]
      Depois de listar a pasta do Drive COM O CONECTOR Google Drive (search_files parentId=1cYV-TSkE_cFpWPrItY5L65JD5s5rcDi6
      title contains 'kevin'): grava todos os títulos vistos (1 por linha) no .txt, baixa os que não estão em
      excluidos_juntados.txt e passa aqui. Junta no excluidos.json e grava kevin_checado.json (hora da checagem).
  python3 trava_kevin.py trava            -> sai com erro se a checagem tiver mais de 8 h ou faltar arquivo juntado
  python3 trava_kevin.py cruzar           -> ids do Tinder dela (listas/*.ids.json) que estão na lista do Kevin e ainda
                                             não foram tirados (grava kevin_no_tinder.json para marcar no Tinder)
  python3 trava_kevin.py lote <pasta do lote>   -> lista pNN do lote que são do Kevin (gerar.py já recusa sozinho)
"""
import glob, json, os, re, subprocess, sys, time
from datetime import datetime, timezone
A = os.path.dirname(os.path.abspath(__file__))
P = lambda f: os.path.join(A, f)
MAX_H = 8


def kevin_ids():
    E = json.load(open(P('excluidos.json')))
    return {str(i) for k, v in E.items() if k.startswith('kevin') for i in v}


def item_de_link(url):
    m = re.search(r'(?:product/\d+/|i\.\d+\.)(\d+)', url or '')
    return m.group(1) if m else None


def estado():
    try: c = json.load(open(P('kevin_checado.json')))
    except Exception: return False, 'nunca checado com o conector (rode trava_kevin.py registrar)'
    h = (time.time() - c['epoch']) / 3600
    juntados = set(open(P('excluidos_juntados.txt')).read().split())
    falta = [t for t in c['titulos'] if t not in juntados]
    if falta: return False, f'arquivos do Kevin vistos no Drive e NÃO juntados: {falta}'
    if h > MAX_H: return False, f'última checagem do Drive do Kevin há {h:.1f} h (máx {MAX_H} h): liste de novo com o conector'
    return True, f'ok (checado há {h:.1f} h, {len(c["titulos"])} arquivos do Kevin)'


def trava():
    ok, msg = estado()
    if not ok: sys.exit('TRAVA KEVIN: ' + msg)
    print('trava Kevin:', msg)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'registrar':
        titulos = [l.strip() for l in open(sys.argv[2]) if l.strip().startswith('excluidos_kevin')]
        novos = sys.argv[3:]
        if novos:
            subprocess.run([sys.executable, P('trocar_excluidos.py'), 'juntar', 'esposa', *novos], check=True, cwd=A)
            with open(P('excluidos_juntados.txt'), 'a') as f:
                for n in novos: f.write(os.path.basename(n) + '\n')
        json.dump({'quando': datetime.now(timezone.utc).isoformat(), 'epoch': time.time(), 'titulos': titulos},
                  open(P('kevin_checado.json'), 'w'), indent=1)
        trava()
    elif cmd == 'trava':
        trava()
    elif cmd == 'cruzar':
        k = kevin_ids(); feitos = set()
        try: feitos = set(json.load(open(P('kevin_tirados_do_tinder.json'))))
        except Exception: pass
        meus = set()
        for f in glob.glob(P('listas/*.ids.json')): meus |= set(map(str, json.load(open(f))))
        x = sorted((meus & k) - feitos)
        json.dump(x, open(P('kevin_no_tinder.json'), 'w'))
        print(len(x), 'do Kevin no Tinder dela a tirar -> kevin_no_tinder.json')
    elif cmd == 'lote':
        k = kevin_ids(); ruins = []
        for a in sorted(glob.glob(os.path.join(sys.argv[2], 'p*-fotos/anuncio.json'))):
            i = item_de_link(json.load(open(a)).get('link'))
            if i in k: ruins.append(os.path.basename(os.path.dirname(a))[:3] + ' ' + i)
        print('do Kevin no lote:', ruins or 'nenhum')
        sys.exit(1 if ruins else 0)
    else:
        sys.exit(__doc__)
