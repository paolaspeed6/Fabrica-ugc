"""Busca produtos HIGH TICKET na API oficial do Shopee Afiliados (Brasil).

Uso:
    python3 buscar_produtos.py                       # palavras de palavras_high_ticket.txt
    python3 buscar_produtos.py "cadeira gamer" --paginas 2
    python3 buscar_produtos.py --teste               # 1 chamada pequena, só mostra os campos

Precisa das variáveis SHOPEE_APP_ID e SHOPEE_APP_SECRET (nunca gravar a senha em arquivo).

Regra do Kevin (2026-10-18): alto ticket (preço >= R$ 200), ranqueado pela comissão em
R$ por venda (campo commission), vendas recentes, menos de 15 afiliados e anúncios pagos.
- Anúncio pago: a API não mostra Shopee Ads; usa sellerCommissionRate > 0 (o vendedor paga
  comissão extra aos afiliados), sinal de que ele está investindo no produto.
- Vendas recentes: diferença do total vendido entre snapshots diários (snapshots/).
  A primeira execução só cria a linha de base.
- Afiliados: a API não informa. Aproximação: poucas vendas totais, anúncio recente
  (itemId alto) e vendas subindo. A contagem real vem do Konkur, só nos finalistas.

Saídas: ranking.csv (todos que passaram) e sniper/cartoes-api-<data>.json (os melhores,
no formato dos cartões do Product Sniper).
"""
import argparse
import csv
import hashlib
import json
import os
import time
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ENDPOINT = "https://open-api.affiliate.shopee.com.br/graphql"
BASE = Path(__file__).resolve().parent
SNAPSHOTS = BASE / "snapshots"

QUERY = """
query($keyword: String, $sortType: Int, $page: Int, $limit: Int) {
  productOfferV2(keyword: $keyword, sortType: $sortType, page: $page, limit: $limit) {
    nodes {
      itemId shopId productName shopName price priceMin priceMax
      sales ratingStar commissionRate commission sellerCommissionRate shopeeCommissionRate
      shopType periodStartTime periodEndTime
      productLink offerLink imageUrl
    }
    pageInfo { page limit hasNextPage }
  }
}
"""

PRECO_MIN = 200.0
NOTA_MIN = 4.6
VENDAS_TOTAIS_MAX = 2000      # acima disso já tem muito afiliado, quase certo
ITEM_ID_RECENTE = 50_000_000_000  # ids 5x bilhões = anúncios de 2026
PROIBIDO = ["vinho", "cerveja", "whisky", "vodka", "cachaca", "gin ", "licor", "taca de",
            "adega", "chopeira", "abridor de vinho"]


def chamar_api(variables):
    app_id = os.environ["SHOPEE_APP_ID"]
    secret = os.environ["SHOPEE_APP_SECRET"]
    payload = json.dumps({"query": QUERY, "variables": variables}, separators=(",", ":"))
    ts = str(int(time.time()))
    assinatura = hashlib.sha256((app_id + ts + payload + secret).encode()).hexdigest()
    req = urllib.request.Request(
        ENDPOINT,
        data=payload.encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"SHA256 Credential={app_id}, Timestamp={ts}, Signature={assinatura}",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        dados = json.load(resp)
    if dados.get("errors"):
        raise RuntimeError(dados["errors"])
    return dados["data"]["productOfferV2"]


def plano(t):
    return unicodedata.normalize("NFKD", (t or "").lower()).encode("ascii", "ignore").decode()


def buscar(palavras, paginas, sort):
    produtos = {}
    for palavra in palavras:
        for pagina in range(1, paginas + 1):
            res = chamar_api({"keyword": palavra, "sortType": sort, "page": pagina, "limit": 50})
            for p in res["nodes"]:
                p["palavra"] = palavra
                produtos[str(p["itemId"])] = p
            if not res["pageInfo"]["hasNextPage"]:
                break
            time.sleep(1)
    return produtos


def ultimo_snapshot():
    arquivos = sorted(SNAPSHOTS.glob("*.json"))
    if not arquivos:
        return None, {}
    return arquivos[-1], json.loads(arquivos[-1].read_text())


def pontos(p, vendas_dia):
    """0-10: comissão em R$ pesa mais; depois poucos afiliados (aproximação) e vendas recentes."""
    comissao = float(p.get("commission") or 0)
    vendas = int(p.get("sales") or 0)
    n = min(comissao / 60, 1) * 4                         # R$ 60+ por venda = nota cheia
    # Vendedor pagando comissão extra (campanha de afiliados paga) = anúncio sendo impulsionado
    n += 2 if float(p.get("sellerCommissionRate") or 0) > 0 else 0
    n += 2 if vendas <= 300 else 1 if vendas <= 1000 else 0
    n += 1 if int(p["itemId"]) >= ITEM_ID_RECENTE else 0
    n += max(0, (float(p.get("ratingStar") or 0) - 4.6) / 0.4)
    if vendas_dia is not None:
        n += min(vendas_dia / 5, 1) * 2                   # 5+ vendas/dia = nota cheia
    return round(n, 1)


def ler_palavras(arquivo):
    return [l.strip() for l in Path(arquivo).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("palavras", nargs="*")
    ap.add_argument("--arquivo", default=str(BASE / "palavras_high_ticket.txt"))
    ap.add_argument("--paginas", type=int, default=1)
    ap.add_argument("--sort", type=int, default=2, help="sortType da API (2 = mais vendidos)")
    ap.add_argument("--cartoes", type=int, default=0, help="Sniper em pausa (Kevin 2026-10-18)")
    ap.add_argument("--preco-min", type=float, default=PRECO_MIN)
    ap.add_argument("--teste", action="store_true")
    args = ap.parse_args()

    if args.teste:
        res = chamar_api({"keyword": args.palavras[0] if args.palavras else "cadeira gamer",
                          "sortType": args.sort, "page": 1, "limit": 3})
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return

    palavras = args.palavras or ler_palavras(args.arquivo)
    SNAPSHOTS.mkdir(exist_ok=True)
    arquivo_ant, anterior = ultimo_snapshot()
    produtos = buscar(palavras, args.paginas, args.sort)
    agora = datetime.now(timezone.utc)

    horas = None
    if arquivo_ant:
        t_ant = datetime.strptime(arquivo_ant.stem, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        horas = (agora - t_ant).total_seconds() / 3600
        if horas < 12:
            horas = None  # snapshot muito próximo: não mede venda recente

    linhas = []
    for item_id, p in produtos.items():
        preco = float(p.get("priceMin") or p.get("price") or 0)
        if preco < args.preco_min or float(p.get("ratingStar") or 0) < NOTA_MIN:
            continue
        if int(p.get("sales") or 0) > VENDAS_TOTAIS_MAX:
            continue
        if any(w in plano(p["productName"]) for w in PROIBIDO):
            continue
        vendas_dia = None
        if horas and item_id in anterior:
            vendas_dia = round((int(p["sales"]) - int(anterior[item_id]["sales"])) * 24 / horas, 1)
        linhas.append({
            "pontos": pontos(p, vendas_dia),
            "produto": p["productName"],
            "preco": preco,
            "comissao_rs": round(float(p.get("commission") or 0), 2),
            "comissao_%": round(float(p.get("commissionRate") or 0) * 100, 1),
            "extra_vendedor_%": round(float(p.get("sellerCommissionRate") or 0) * 100, 1),
            "vendidos_total": p["sales"],
            "vendas_por_dia": "" if vendas_dia is None else vendas_dia,
            "anuncio_recente": int(item_id) >= ITEM_ID_RECENTE,
            "estrelas": p["ratingStar"],
            "loja": p["shopName"],
            "palavra": p["palavra"],
            "itemId": item_id,
            "shopId": p["shopId"],
            "foto": p["imageUrl"],
            "link_afiliado": p["offerLink"],
            "link": p["productLink"],
        })

    (SNAPSHOTS / f"{agora:%Y%m%dT%H%M%SZ}.json").write_text(json.dumps(produtos, ensure_ascii=False))
    linhas.sort(key=lambda l: (l["pontos"], l["comissao_rs"]), reverse=True)
    saida = BASE / "ranking.csv"
    with saida.open("w", newline="", encoding="utf-8") as f:
        if linhas:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
            w.writeheader()
            w.writerows(linhas)

    cartoes = [{
        "id": f"api-{l['itemId']}",
        "nome": l["produto"], "foto": l["foto"], "preco": l["preco"], "nota": l["estrelas"],
        "link": l["link"], "link_afiliado": l["link_afiliado"], "shopId": str(l["shopId"]),
        "itemId": l["itemId"], "comissao_rs": l["comissao_rs"], "comissao_pct": l["comissao_%"],
        "vendidos_total": l["vendidos_total"], "vendas_por_dia": l["vendas_por_dia"],
        "pontos": l["pontos"], "status": "novo",
    } for l in linhas[:args.cartoes]]
    if not cartoes:
        print(f"{len(produtos)} produtos lidos, {len(linhas)} passaram -> {saida}")
        return
    arq_cartoes = BASE / "sniper" / f"cartoes-api-{agora:%Y-%m-%d}.json"
    arq_cartoes.write_text(json.dumps(cartoes, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{len(produtos)} produtos lidos, {len(linhas)} passaram -> {saida}, {len(cartoes)} cartões -> {arq_cartoes}")
    if not horas:
        print("Linha de base criada: rode de novo daqui a ~24h para medir vendas recentes.")


if __name__ == "__main__":
    main()
