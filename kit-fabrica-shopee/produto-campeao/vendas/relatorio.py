"""Puxa as vendas dos últimos N dias e soma por Sub ID e por produto (grátis, API oficial).

Uso: python3 relatorio.py [dias=30]
Saída: vendas_<data>.json e um resumo na tela. Base para o filtro aprender o que vende de verdade.
"""
import json, sys, time
from collections import defaultdict
from datetime import date
from pathlib import Path
from api import chamar

Q = """query($a:Int64,$b:Int64%s){conversionReport(purchaseTimeStart:$a,purchaseTimeEnd:$b,limit:50%s){
nodes{purchaseTime utmContent totalCommission orders{orderStatus items{itemId itemName qty actualAmount itemTotalCommission}}}
pageInfo{hasNextPage scrollId}}}"""


def main():
    dias = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    fim = int(time.time()); ini = fim - dias * 86400
    nos, scroll = [], None
    while True:
        v = {"a": str(ini), "b": str(fim)}
        if scroll:
            v["s"] = scroll
        r = chamar(Q % ((",$s:String!", ",scrollId:$s") if scroll else ("", "")), v)["conversionReport"]
        nos += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]:
            break
        scroll = r["pageInfo"]["scrollId"]
    por_sub, por_item = defaultdict(lambda: [0, 0.0]), defaultdict(lambda: [0, 0.0, ""])
    for n in nos:
        sub = (n.get("utmContent") or "").strip("-") or "(sem sub id)"
        for o in n["orders"] or []:
            for it in o["items"] or []:
                c = float(it.get("itemTotalCommission") or 0)
                por_sub[sub][0] += int(it["qty"] or 0); por_sub[sub][1] += c
                k = str(it["itemId"]); por_item[k][0] += int(it["qty"] or 0); por_item[k][1] += c; por_item[k][2] = it["itemName"]
    saida = Path(__file__).parent / f"vendas_{date.today():%Y-%m-%d}.json"
    saida.write_text(json.dumps({"dias": dias, "por_sub": por_sub, "por_item": por_item}, ensure_ascii=False, indent=1))
    print(f"{len(nos)} conversões em {dias} dias -> {saida}")
    for sub, (q, c) in sorted(por_sub.items(), key=lambda x: -x[1][1])[:15]:
        print(f"{q:4d} itens  R$ {c:8.2f}  {sub}")


if __name__ == "__main__":
    main()
