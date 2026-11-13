"""Varredura de CARROSSEL (redes sociais), separada da varredura da Shopee Vídeo (a dona, 13/11).
Procura produto bonito/fofo para foto: Natal + estilo da casa dela (romântico, sofisticado, flores, rosa, americano).
Filtro da API (grátis) -> nota de beleza pelo Gemini olhando a foto (grátis) -> candidatos_carrossel-<data>.json.
Nunca pega produto do Kevin (excluidos.json). Rode DEPOIS da varredura diária (dividem o limite da API).
uso: python3 -I varrer_carrossel.py [--palavras palavras_natal.txt,palavras_romantico.txt] [--top 60]"""
import argparse, base64, json, math, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
B = Path(__file__).resolve().parent
AF = B.parent / 'afiliados'
sys.path.insert(0, str(AF)); import varrer as V
sys.path.insert(0, str(B.parents[1] / 'video-teste' / 'lote' / 'modelo')); import fiscal_gemini as G
CK = B / ('ck_carrossel_' + time.strftime('%Y-%m-%d') + os.environ.get('TAG', '')); CK.mkdir(exist_ok=True)
VISTOS = B / 'vistos_carrossel.json'

ESTILO = """Você escolhe produtos da Shopee para CARROSSEIS de foto no TikTok/Instagram da loja Aguiiar Lar.
Identidade da casa dela: romântica, sofisticada, base branca com madeira e plantas, flores, tons de rosa, laços, estilo casa americana; no Natal: vermelho, xadrez, dourado, fofo.
O que viraliza: item FOFO, BONITO na foto, diferente do comum (ex.: tigela em forma de flor, porta-ovos galinha, caneca boneco de neve).
Para cada foto numerada, devolva um JSON: lista de {"n": número, "beleza": 0-10 (quão fofo/bonito/fotogênico),
"estilo": 0-10 (quão combina com a identidade romântica (branco, madeira, plantas, rosa, flores) ou Natal fofo), "tema": um de ["Natal","Cozinha fofa","Café da manhã","Mesa posta","Quarto","Banheiro","Sala","Enxoval"],
"troque_isso": "o item comum e sem graça que este produto substitui, curto, em português (ex.: 'potinhos brancos lisos')",
"problema": "vazio, ou o que atrapalha (foto com texto/montagem, produto feio, não é de casa, parece barato)"}.
Cada foto vem com o PREÇO. Dê também "vale_o_preco": 0-10 (o que a pessoa leva pelo preço: kit com várias peças, uso o ano todo,
qualidade aparente, compra por impulso fácil; um papai noel de R$ 300 é inviável = nota baixa; até R$ 150 só se for kit grande ou peça que dura anos) e "beneficio": frase curta em português
com o benefício que vende (ex.: 'kit com 8 bolas pelo preço de 2', 'serve na mesa e na árvore'). Produto que não é de casa
(embalagem, folheto, lembrancinha, caixa de doces, festa infantil) = problema "não é de casa".
Notas altas só para o que uma garota de 25 anos salvaria E compraria sem pensar duas vezes."""

# a dona, 13/11 (3ª): "está tendo muitas xícaras que não têm nada a ver; gosto de coisas lindas e irresistíveis, uma casa bem das paty".
# Com --refs, as fotos dela vão junto e o Gemini compara cada produto com elas.
REFS = """ANTES das fotos numeradas vêm as FOTOS DE REFERÊNCIA da dona (o que ela AMA): casa "das paty" — rosa bebê, laços,
xadrez rosa e branco com dourado, vidro ondulado/bolha, cerâmica com bolinhas, palha e madeira com rosa, toalhas felpudas rosa,
peônias, tudo delicado, feminino e irresistível. Para cada foto numerada dê também "parece_refs": 0-10 (quanto parece que saiu
da mesma casa das referências; xícara comum, frase escrita, vermelho forte, rústico pesado, colorido infantil ou peça genérica = nota baixa)
e "tipo": o tipo de objeto em 1 ou 2 palavras (ex.: "xícara", "pote", "toalha", "prateleira", "copo")."""

def busca(i, k):
    f = CK / f'r{i:03d}.json'
    if f.exists(): return json.loads(f.read_text())
    prods = {}
    for pg in range(1, 6):
        res = V.chamar({'l': 0, 's': 2, 'k': k, 'p': pg})
        for p in res['nodes']: p['_k'] = k; prods[str(p['itemId'])] = p
        if not res['pageInfo']['hasNextPage']: break
        time.sleep(1.0)
    f.write_text(json.dumps(prods)); print(f'rodada {i} {k}: {len(prods)}', flush=True)
    return prods

def foto(url):
    try:
        return base64.b64encode(urllib.request.urlopen(url + '_tn', timeout=30).read()).decode()
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--palavras', default='palavras_natal.txt,palavras_romantico.txt')
    ap.add_argument('--top', type=int, default=60)
    ap.add_argument('--refs', help='pasta com as fotos de referência da dona (ex.: referencias_paty)')
    ap.add_argument('--max-tipo', type=int, default=0, help='no máximo N produtos do mesmo tipo (0 = sem limite)')
    ap.add_argument('--preco-max', type=float, default=150, help='móveis (a dona, 13/11): até R$ 600')
    a = ap.parse_args()
    refs = []
    if a.refs:
        for f in sorted((B / a.refs).glob('*.jpg')):
            refs += [{'text': 'Referência da dona:'}, {'inline_data': {'mime_type': 'image/jpeg', 'data': base64.b64encode(f.read_bytes()).decode()}}]
    pal = [l.strip() for f in a.palavras.split(',') for l in (B / f).read_text().splitlines() if l.strip() and not l.startswith('#')]
    prods = {}
    with ThreadPoolExecutor(2) as ex:
        for d in ex.map(lambda x: busca(*x), enumerate(pal)): prods.update(d)
    fora = set()
    if V.EXCLUIDOS.exists(): fora |= {str(i) for ids in json.loads(V.EXCLUIDOS.read_text()).values() for i in ids}  # Kevin etc.
    if VISTOS.exists(): fora |= set(json.loads(VISTOS.read_text()))
    lista = []
    for k, p in prods.items():
        preco, vend, nota = float(p['priceMin'] or 0), int(p['sales'] or 0), float(p['ratingStar'] or 0)
        com = float(p['commission'] or 0)
        # a dona, 13/11: "produtos estratégicos, com bons preços e benefícios; um papai noel de 300 reais é inviável".
        # a dona, 13/11 (2ª): "e que também tenha no mínimo 10 reais de comissão" -> preço sobe para até R$ 150 (R$ 10 a 15% = R$ 67+).
        if k in fora or not (30 <= preco <= a.preco_max) or nota < 4.7 or vend < 50: continue
        if float(p['commissionRate']) < 0.10 or com < 10: continue
        if any(w in V.plano(p['productName']) for w in V.PROIBIDO): continue
        n = min(com / 8, 1) * 3 + min(float(p['commissionRate']) / 0.2, 1) * 2 + min(math.log10(vend + 1) / 4, 1) * 3 + (1.5 if preco <= a.preco_max * 0.53 else 0.5 if preco <= a.preco_max * 0.73 else 0) + min((com - 10) / 15, 1) * 2
        n += 1 if float(p['sellerCommissionRate'] or 0) > 0 else 0
        lista.append((n, k, p))
    lista.sort(reverse=True); lista = lista[:a.top * 3]
    print(len(prods), 'lidos;', len(lista), 'vão para a nota de beleza', flush=True)
    saida = []
    for i in range(0, len(lista), 12):
        bloco = lista[i:i + 12]; fotos = [foto(p['imageUrl']) for _, _, p in bloco]
        partes = [{'text': ESTILO + ('\n' + REFS if refs else '')}] + refs
        for j, ((_, k, p), f) in enumerate(zip(bloco, fotos)):
            if f: partes += [{'text': f'Foto {j}: {p["productName"][:90]} | preço R$ {float(p["priceMin"]):.2f}'}, {'inline_data': {'mime_type': 'image/jpeg', 'data': f}}]
        try: notas = {int(x['n']): x for x in G.chamar(partes)}
        except Exception as e: print('gemini falhou', e); continue
        for j, (n, k, p) in enumerate(bloco):
            x = notas.get(j)
            if not x or x.get('problema') or x['beleza'] < 7 or x['estilo'] < 6 or x.get('vale_o_preco', 0) < 7: continue
            if refs and x.get('parece_refs', 0) < 7: continue
            com = float(p['commission'] or 0)
            saida.append({'id': k, 'nome': p['productName'], 'loja': p['shopName'], 'preco': float(p['priceMin']),
                          'comissao_rs': round(com, 2), 'comissao_pct': round(float(p['commissionRate']) * 100, 1),
                          'vendidos': int(p['sales']), 'nota': float(p['ratingStar']), 'link': p['productLink'], 'foto_url': p['imageUrl'],
                          'tema': x['tema'], 'beleza': x['beleza'], 'estilo': x['estilo'], 'troque_isso': x.get('troque_isso', ''), 'vale_o_preco': x.get('vale_o_preco'), 'beneficio': x.get('beneficio', ''),
                          'busca': p['_k'], 'tipo': x.get('tipo', ''), 'parece_refs': x.get('parece_refs'),
                          'pontos': round(n + x['beleza'] * 0.5 + x['estilo'] * 0.5 + x.get('vale_o_preco', 0) * 0.6 + x.get('parece_refs', 0) * 0.8, 2)})
        print(f'beleza {i + len(bloco)}/{len(lista)}: {len(saida)} aprovados', flush=True)
    saida.sort(key=lambda x: x['pontos'], reverse=True)
    if a.max_tipo:
        cont, filt = {}, []
        for x in saida:
            t = V.plano(x.get('tipo') or '').strip()
            if cont.get(t, 0) < a.max_tipo: filt.append(x); cont[t] = cont.get(t, 0) + 1
        saida = filt
    saida = saida[:a.top]
    for x in saida: x['foto'] = V.miniatura(x['foto_url'])
    out = B / f'candidatos_carrossel-{time.strftime("%Y-%m-%d")}{os.environ.get("TAG", "")}.json'
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=1))
    from collections import Counter
    print(len(saida), '->', out, dict(Counter(x['tema'] for x in saida)))

if __name__ == '__main__':
    main()
