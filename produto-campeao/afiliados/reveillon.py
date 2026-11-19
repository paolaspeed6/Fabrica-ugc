"""Varredura de Réveillon (a dona, 19/11): decoração de festa de Ano Novo (mesa, painel, luzes, balões), comissão >= R$ 20,
logo depois do Natal no Tinder. Sem bebida/taça/garrafa/fogos.
uso: python3 reveillon.py [--com-min 20]  -> candidatos-reveillon-<data>.json (campo reveillon=True)."""
import argparse, json, sys, time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import varrer as V
from largo import largo

PALAVRAS = ["decoracao reveillon", "decoracao ano novo", "kit decoracao ano novo", "painel ano novo", "painel reveillon",
            "cortina metalizada", "cortina de franja metalizada", "cortina brilhante festa", "baloes ano novo", "kit baloes dourado",
            "arco de baloes dourado", "balao numero 2027", "balao metalizado dourado", "faixa feliz ano novo", "letreiro feliz ano novo",
            "topo de bolo ano novo", "centro de mesa reveillon", "toalha de mesa branca festa", "trilho de mesa dourado",
            "caminho de mesa dourado", "sousplat dourado", "sousplat prata", "guardanapo de tecido branco", "porta guardanapo dourado",
            "jogo americano dourado", "castical dourado", "candelabro decorativo", "vela decorativa dourada", "lanterna marroquina",
            "cordao de luz led", "fio de fada led", "cortina de led", "luminaria estrela led", "letreiro neon led", "globo espelhado",
            "bola espelhada decorativa", "estrela decorativa dourada", "arranjo de flores brancas", "flores artificiais brancas",
            "vaso decorativo dourado", "bandeja espelhada", "bandeja dourada decorativa", "boleira de vidro", "suporte de doces festa",
            "kit pegue e monte", "painel redondo festa", "capa painel redondo", "cilindro decorativo festa", "pompom de papel",
            "guirlanda metalizada", "confete metalizado mesa", "kit festa ano novo", "decoracao festa dourada", "decoracao festa prata"]
FESTA = ["reveillon", "ano novo", "2027", "festa", "balao", "baloes", "metaliz", "dourad", "prata", "led", "neon", "brilh",
         "espelhad", "estrela", "vela", "castical", "candelabro", "sousplat", "guardanapo", "toalha", "trilho", "caminho de mesa",
         "jogo americano", "painel", "cortina", "pompom", "confete", "boleira", "bandeja", "centro de mesa", "arranjo", "flores", "lanterna",
         "letreiro", "globo", "guirlanda", "cilindro", "pegue e monte", "topo de bolo", "vaso"]
NAO_DECOR = ["fantasia", "roupa", "camiseta", "pijama", "vestido", "chinelo", "brinquedo", "chocolate", "kit beleza", "perfume",
             "maquiagem", "caneca", "bone ", "gorro", "meia calca", "champanhe", "champagne", "espumante", "vinho", "cerveja", "drink",
             "whisky", "balde de gelo", "brinde", "fogos", "rojao", "bombinha", "oculos", "colar", "brinco", "pulseira", "unha",
             "cabelo", "natal", "natalin", "noel", "presepio", "infantil", "cha de bebe", "aniversario infantil"]

def uma(r):
    out = {}
    for p in range(1, 6):
        res = V.chamar({**r, "p": p})
        for x in res["nodes"]:
            out[str(x["itemId"])] = x
        if not res["pageInfo"]["hasNextPage"]:
            break
        time.sleep(1.0)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--com-min", type=float, default=20); ap.add_argument("--top", type=int, default=80)
    a = ap.parse_args()
    rodadas = [{"l": 0, "s": s, "k": k} for k in PALAVRAS for s in (2, 5)]
    prods = {}
    with ThreadPoolExecutor(2) as ex:
        for i, r in enumerate(ex.map(uma, rodadas)):
            prods.update(r)
            if i % 10 == 0: print(i, len(prods), flush=True)
    vistos = set(json.loads(V.VISTOS.read_text()))
    vistos |= {str(i) for ids in json.loads(V.EXCLUIDOS.read_text()).values() for i in ids}
    conta = V.contar_parecidos(prods)
    lista = []
    for k, p in prods.items():
        nome = V.plano(p["productName"]); com = float(p["commission"] or 0)
        preco, vend, nota = float(p["priceMin"] or 0), int(p["sales"] or 0), float(p["ratingStar"] or 0)
        if k in vistos or com < a.com_min or (nota and nota < 4.5) or vend < 1: continue
        if not any(w in nome for w in FESTA) or any(w in nome for w in NAO_DECOR + V.PROIBIDO + ["taca", "tacas", "garrafa", "copo", "bebida", "cooler"]): continue
        if any(m in nome for m in V.MARCAS_LOTADAS): continue
        par = conta(p["productName"])
        n = min(com / 60, 1) * 4 + (2 if 5 <= vend <= 500 else 1 if vend <= 2000 else 0)
        n += 1.5 if int(k) >= V.ITEM_ID_RECENTE else 0
        n += 1 if float(p["sellerCommissionRate"] or 0) > 0 else 0
        n += max(0, (nota - 4.5) / 0.5)
        n += 2 if "reveillon" in nome or "ano novo" in nome else 0
        n += 1 if par <= 20 else 0
        lista.append({"id": k, "nome": p["productName"], "loja": p["shopName"], "preco": preco, "comissao_rs": round(com, 2),
                      "comissao_pct": round(float(p["commissionRate"]) * 100, 1), "extra_vendedor": float(p["sellerCommissionRate"] or 0) > 0,
                      "largo": largo(p["productName"]), "vendidos": vend, "vendas_dia": None, "novo": int(k) >= V.ITEM_ID_RECENTE,
                      "nota": nota, "foto": p["imageUrl"], "link": p["productLink"], "parecidos": par, "pontos": round(n, 2), "reveillon": True})
    lista.sort(key=lambda x: x["pontos"], reverse=True)
    lista = V.sem_duplicatas(lista)
    lista = [x for x in lista if not x.get("possivel_duplicata")][:a.top]
    for x in lista: x["foto"] = V.miniatura(x["foto"])
    saida = BASE / f"candidatos-reveillon-{datetime.now():%Y-%m-%d}.json"
    saida.write_text(json.dumps(lista, ensure_ascii=False, indent=1))
    print(len(prods), "lidos;", len(lista), "->", saida)

if __name__ == "__main__":
    main()
