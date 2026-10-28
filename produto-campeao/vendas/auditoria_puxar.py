"""Auditoria: puxa 90 dias do conversionReport (3 janelas de 30 dias) para conv90.json. Grátis. Não commitar o conv90.json."""
import json, sys, time
sys.path.insert(0, "/home/user/Fabrica-ugc/produto-campeao/vendas")
from api import chamar
CAMPOS = """clickTime purchaseTime conversionId conversionStatus totalCommission netCommission estimatedTotalCommission buyerType utmContent device productType referrer
orders{orderId orderStatus items{shopId shopName completeTime itemId itemName itemPrice displayItemStatus actualAmount refundAmount qty itemTotalCommission itemSellerCommissionRate itemShopeeCommissionRate categoryLv1Name categoryLv2Name fraudStatus attributionType channelType campaignType}}"""
Q = "query($a:Int64,$b:Int64%%s){conversionReport(purchaseTimeStart:$a,purchaseTimeEnd:$b,limit:500%%s){nodes{%s} pageInfo{hasNextPage scrollId}}}" % CAMPOS
fim = int(time.time()); nos = []
for k in range(3):  # 3 janelas de 30 dias
    b = fim - k*30*86400; a = b - 30*86400; s = None
    while True:
        v = {"a": str(a), "b": str(b)}
        if s: v["s"] = s
        try:
            r = chamar(Q % ((",$s:String!", ",scrollId:$s") if s else ("", "")), v)["conversionReport"]
        except Exception as e:
            print("janela", k, "erro:", str(e)[:300]); break
        nos += r["nodes"]; print("janela", k, len(r["nodes"]))
        if not r["pageInfo"]["hasNextPage"]: break
        s = r["pageInfo"]["scrollId"]; time.sleep(1)
    time.sleep(1)
json.dump(nos, open("conv90.json", "w"), ensure_ascii=False)
print("total", len(nos))
