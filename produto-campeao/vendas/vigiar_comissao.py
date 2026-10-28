"""Confere se os 20 produtos que mais deram comissão ainda pagam a mesma taxa (grátis, só leitura).

Uso: python3 auditoria_puxar.py && python3 vigiar_comissao.py   (lê o conv90.json)
Taxa que caiu = trocar o produto do vídeo por um equivalente com comissão extra.
"""
import json, time, collections as C
from api import chamar

F = "itemId productName price commissionRate sellerCommissionRate sales ratingStar"
com, info = C.defaultdict(float), {}
for x in json.load(open("conv90.json")):
    for o in x["orders"]:
        for i in o["items"]:
            if o["orderStatus"] != "CANCELLED":
                com[i["itemId"]] += float(i["itemTotalCommission"] or 0)
            info[i["itemId"]] = (i["itemName"][:45], i["itemSellerCommissionRate"])
for item, c in sorted(com.items(), key=lambda kv: -kv[1])[:20]:
    nos = chamar("query($i:Int64){productOfferV2(itemId:$i,limit:1){nodes{%s}}}" % F, {"i": str(item)})["productOfferV2"]["nodes"]
    nome, antes = info[item]
    hoje = f"{float(nos[0]['sellerCommissionRate']) * 100:.0f}%" if nos else "fora do ar"
    alerta = "  <-- MUDOU" if not nos or abs(float(antes.strip('%') or 0) - float(nos[0]["sellerCommissionRate"]) * 100) > 0.5 else ""
    print(f"R$ {c:7.0f}  {nome:45} vendedor antes {antes:>6} hoje {hoje:>10}{alerta}")
    time.sleep(0.5)
