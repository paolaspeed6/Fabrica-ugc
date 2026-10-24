"""Links de afiliado com Sub ID de TODOS os produtos do lote, de uma vez (grátis, API oficial Shopee Afiliados, conta da dona).
Lê links.txt ("NN https://shopee.com.br/product/<loja>/<item>" por linha) e grava links_afiliado.json:
{"pNN": {"a": link, "sub_a": SubID, "b": ..., "c": ..., "r": ...}}. Sub ID = L<PREFIXO>p<NN><A|B|C|R><AAMMDD>, só letras e números.
uso: python3 -I gerar_links.py [AAMMDD]"""
import json, os, sys
from pathlib import Path
B = Path(__file__).resolve().parent
sys.path.insert(0, str(B.parents[2] / 'produto-campeao' / 'vendas'))
from link_subid import link
PRE = os.environ.get('PREFIXO') or B.name.replace('lista', '').upper()
dia = sys.argv[1] if len(sys.argv) > 1 else None
saida = B / 'links_afiliado.json'; L = json.loads(saida.read_text()) if saida.exists() else {}
for linha in (B / 'links.txt').read_text().splitlines():
    if not linha.strip() or '<loja>' in linha:
        continue
    n, url = linha.split()[:2]; k = f'p{n}'
    if len(L.get(k, {})) == 8:
        continue
    d = {}
    for v, cod in (('a', 'A'), ('b', 'B'), ('c', 'C'), ('r', 'R')):
        sub, curto = link(url, f'L{PRE}p{n}', cod, dia); d[v] = curto; d['sub_' + v] = sub
    L[k] = d; saida.write_text(json.dumps(L, ensure_ascii=False, indent=1)); print(k, d['sub_a'], d['a'])
