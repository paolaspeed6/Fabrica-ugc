"""Busca produtos campeões na API oficial do Shopee Afiliados (Brasil).

Uso:
    export SHOPEE_APP_ID=...  SHOPEE_APP_SECRET=...
    python3 buscar_produtos.py "organizador" "escova secadora" --paginas 3

Cada execução salva um snapshot em snapshots/. A partir da segunda execução
(idealmente 24h depois), o script calcula as vendas recentes de cada produto
pela diferença do total de vendidos entre os snapshots.

A API não informa número de afiliados nem data das avaliações; o ranking usa
vendas recentes, nota, comissão e preço. Concorrência de afiliados é checada
depois, só nos finalistas.
"""
import argparse
import csv
import hashlib
import json
import os
import time
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
      sales ratingStar commissionRate commission
      productLink offerLink imageUrl
    }
    pageInfo { page limit hasNextPage }
  }
}
"""

# Filtros do produto campeão
NOTA_MIN = 4.7
VENDAS_TOTAIS_MIN = 100
PRECO_MIN, PRECO_MAX = 30.0, 150.0
COMISSAO_MIN = 0.10


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


def buscar(palavras, paginas):
    produtos = {}
    for palavra in palavras:
        for pagina in range(1, paginas + 1):
            # sortType 2 = mais vendidos
            res = chamar_api({"keyword": palavra, "sortType": 2, "page": pagina, "limit": 50})
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


def nota(p, vendas_dia):
    preco = float(p.get("priceMin") or p.get("price") or 0)
    comissao = float(p.get("commissionRate") or 0)
    estrelas = float(p.get("ratingStar") or 0)
    pontos = 0.0
    pontos += min(vendas_dia / 20, 1) * 4 if vendas_dia is not None else min(int(p["sales"]) / 2000, 1) * 2
    pontos += max(0, (estrelas - 4.5) / 0.5) * 2
    pontos += min(comissao / 0.20, 1) * 2
    pontos += 2 if PRECO_MIN <= preco <= PRECO_MAX else 0
    return round(pontos, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("palavras", nargs="+")
    ap.add_argument("--paginas", type=int, default=2)
    args = ap.parse_args()

    SNAPSHOTS.mkdir(exist_ok=True)
    arquivo_ant, anterior = ultimo_snapshot()
    produtos = buscar(args.palavras, args.paginas)
    agora = datetime.now(timezone.utc)

    horas = None
    if arquivo_ant:
        t_ant = datetime.strptime(arquivo_ant.stem, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        horas = max((agora - t_ant).total_seconds() / 3600, 1)

    linhas = []
    for item_id, p in produtos.items():
        preco = float(p.get("priceMin") or p.get("price") or 0)
        if float(p.get("ratingStar") or 0) < NOTA_MIN or int(p.get("sales") or 0) < VENDAS_TOTAIS_MIN:
            continue
        if float(p.get("commissionRate") or 0) < COMISSAO_MIN:
            continue
        vendas_dia = None
        if horas and item_id in anterior:
            vendas_dia = round((int(p["sales"]) - int(anterior[item_id]["sales"])) * 24 / horas, 1)
        linhas.append({
            "nota": nota(p, vendas_dia),
            "produto": p["productName"],
            "preco": preco,
            "vendidos_total": p["sales"],
            "vendas_por_dia": "" if vendas_dia is None else vendas_dia,
            "estrelas": p["ratingStar"],
            "comissao_%": round(float(p["commissionRate"]) * 100, 1),
            "loja": p["shopName"],
            "palavra": p["palavra"],
            "link_afiliado": p["offerLink"],
            "link": p["productLink"],
        })

    (SNAPSHOTS / f"{agora:%Y%m%dT%H%M%SZ}.json").write_text(json.dumps(produtos, ensure_ascii=False))
    linhas.sort(key=lambda l: l["nota"], reverse=True)
    saida = BASE / "ranking.csv"
    with saida.open("w", newline="", encoding="utf-8") as f:
        if linhas:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
            w.writeheader()
            w.writerows(linhas)
    print(f"{len(produtos)} produtos lidos, {len(linhas)} passaram nos filtros -> {saida}")
    if not horas:
        print("Primeira execução: rode de novo em ~24h para medir vendas recentes.")


if __name__ == "__main__":
    main()
