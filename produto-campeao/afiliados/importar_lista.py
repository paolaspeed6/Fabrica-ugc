"""Importa uma lista de links da dona para o Tinder (a dona, 27/10: "adicione os links ao tinder e salve internamente").
Lê listas/<nome>.txt (o texto que ela cola: "N. nome / R$ ..., X vendidos, Y vendas/dia, nota Z / https://shopee.com.br/product/<loja>/<item>"),
busca cada produto na API oficial de afiliados (grátis), gera o link de afiliado DELA (Sub ID T<AAMMDD>p<NNN>) e a foto,
e grava listas/<nome>_docs/<itemId>.json no formato do Tinder (coleção candidatos, sem status = cartão novo em "Escolher").
Ordem da lista = mais promissor primeiro (pontos maiores). Pula itemId que já está no Tinder (passe a pasta da listagem).
uso: SHOPEE_APP_SECRET=... python3 -I importar_lista.py listas/2710.txt AAAA-MM-DD [pasta_com_candidatos_existentes]"""
import json, re, sys, time
from pathlib import Path
B = Path(__file__).resolve().parent
sys.path.insert(0, str(B)); sys.path.insert(0, str(B.parent / 'vendas'))
from varrer import miniatura
from api import chamar
from link_subid import link

arq, dia = Path(sys.argv[1]), sys.argv[2]
ja = {p.stem for p in Path(sys.argv[3]).glob('*.json')} if len(sys.argv) > 3 else set()
txt = arq.read_text(); out = arq.with_name(arq.stem + '_docs'); out.mkdir(exist_ok=True)
# formato compacto, uma linha por produto: N|preço|vendidos|vendas_dia|nota|link (o nome vem da API)
itens = [(n, '', pr, ve, vd, no, u, *re.search(r'product/(\d+)/(\d+)', u).groups())
         for n, pr, ve, vd, no, u in (l.split('|') for l in txt.splitlines() if l.count('|') == 5 and not l.startswith('#'))]
print(len(itens), 'produtos na lista')
Q = 'query{productOfferV2(itemId:%s,shopId:%s,limit:1){nodes{itemId productName shopName priceMin sales ratingStar commission commissionRate imageUrl}}}'
for n, nome, preco, vend, vdia, nota, url, loja, item in itens:
    if item in ja: print(n, item, 'já está no Tinder'); continue
    if (out / f'{item}.json').exists(): continue
    try:
        nd = (chamar(Q % (item, loja))['productOfferV2']['nodes'] or [{}])[0]
        sub, curto = link(url, f'Tp{int(n):03d}', '', dia[2:].replace('-', ''))
    except Exception as e:
        print(n, item, 'FALHOU', e, flush=True); time.sleep(3); continue
    pr = float(preco.replace('.', '').replace(',', '.'))
    cpct = round(float(nd.get('commissionRate') or 0) * 100, 1)
    doc = dict(nome=nd.get('productName') or nome.strip(), loja=nd.get('shopName') or '', preco=pr, vendidos=int(vend),
               vendas_dia=float(vdia or 0), nota=float(nota), link=url, link_afiliado=curto, sub_id=sub,
               comissao_pct=cpct, comissao_rs=round(float(nd.get('commission') or pr * cpct / 100), 2),
               foto=miniatura(nd['imageUrl']) if nd.get('imageUrl') else '', dia=dia, ordem=int(n),
               pontos=round(10 - int(n) * 0.04, 2), novo=True, origem='lista da dona')
    (out / f'{item}.json').write_text(json.dumps(doc, ensure_ascii=False)); print(n, item, curto, flush=True)
