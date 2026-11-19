"""Varredura de Natal (a dona, 19/11): decorações bonitas com comissão >= R$ 20, para o topo do Tinder.
uso: python3 natal.py [--com-min 20]  -> candidatos-natal-<data>.json (mesmo formato do varrer.py, campo natal=True)."""
import argparse, json, sys, time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import varrer as V
from largo import largo

PALAVRAS = ["arvore de natal", "arvore de natal grande", "arvore de natal luxo", "arvore de natal nevada", "arvore de natal 2,10",
            "arvore de natal 1,80", "arvore natal pinheiro", "decoracao de natal", "decoracao natalina luxo", "enfeite de natal",
            "kit bolas de natal", "bolas de natal luxo", "guirlanda de natal", "guirlanda natalina", "festao natalino",
            "papai noel decorativo", "papai noel grande", "boneco de neve decorativo", "rena decorativa", "rena iluminada",
            "presepio", "presepio completo", "pisca pisca", "pisca pisca led cascata", "cortina de led natal", "luzes de natal",
            "cascata led natal", "estrela ponteira arvore", "ponteira de natal", "saia para arvore de natal", "meia de natal",
            "trilho de mesa natal", "toalha de mesa natal", "centro de mesa natal", "caminho de mesa natalino", "jogo americano natal",
            "almofada natal", "capa de almofada natal", "tapete natal", "enfeite porta natal", "arranjo natalino", "vela decorativa natal",
            "luminaria natal", "casinha de natal led", "vila de natal", "quebra nozes decorativo", "anjo decorativo natal",
            "laco de natal", "kit decoracao arvore natal", "arvore de natal com led", "arvore de natal branca", "arvore de natal rose",
            "arvore de natal dourada", "boneco papai noel", "noel escalador", "painel de natal", "cesta natalina decorativa",
            "pelucia natal", "galhos nevados decorativos", "pinha decorativa natal", "sino decorativo natal", "globo de neve"]
NATAL = ["natal", "natalin", "noel", "papai", "rena", "presepio", "pisca", "guirland", "festao", "neve", "nevad", "pinheiro",
         "arvore", "christmas", "xmas", "quebra nozes", "trenó", "treno", "estrela", "led", "anjo", "sino", "pinha", "bolas", "enfeite"]
NAO_DECOR = ["fantasia", "roupa", "camiseta", "pijama", "vestido", "chinelo", "brinquedo infantil", "panetone", "chocolate",
             "cesta basica", "kit beleza", "perfume", "maquiagem", "caneca", "bone ", "gorro", "meia calca"]

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
        if not any(w in nome for w in NATAL) or any(w in nome for w in NAO_DECOR + V.PROIBIDO + ["taca", "garrafa", "copo", "bebida"]): continue
        if any(m in nome for m in V.MARCAS_LOTADAS): continue
        par = conta(p["productName"])
        n = min(com / 60, 1) * 4 + (2 if 5 <= vend <= 500 else 1 if vend <= 2000 else 0)
        n += 1.5 if int(k) >= V.ITEM_ID_RECENTE else 0
        n += 1 if float(p["sellerCommissionRate"] or 0) > 0 else 0
        n += max(0, (nota - 4.5) / 0.5)
        n += 2 if "natal" in nome or "natalin" in nome or "noel" in nome else 0
        n += 1 if par <= 20 else 0
        lista.append({"id": k, "nome": p["productName"], "loja": p["shopName"], "preco": preco, "comissao_rs": round(com, 2),
                      "comissao_pct": round(float(p["commissionRate"]) * 100, 1), "extra_vendedor": float(p["sellerCommissionRate"] or 0) > 0,
                      "largo": largo(p["productName"]), "vendidos": vend, "vendas_dia": None, "novo": int(k) >= V.ITEM_ID_RECENTE,
                      "nota": nota, "foto": p["imageUrl"], "link": p["productLink"], "parecidos": par, "pontos": round(n, 2), "natal": True})
    lista.sort(key=lambda x: x["pontos"], reverse=True)
    lista = V.sem_duplicatas(lista)
    lista = [x for x in lista if not x.get("possivel_duplicata")][:a.top]
    for x in lista: x["foto"] = V.miniatura(x["foto"])
    saida = BASE / f"candidatos-natal-{datetime.now():%Y-%m-%d}.json"
    saida.write_text(json.dumps(lista, ensure_ascii=False, indent=1))
    print(len(prods), "lidos;", len(lista), "->", saida)

if __name__ == "__main__":
    main()
