"""Chamada assinada à API oficial Shopee Afiliados (usa SHOPEE_APP_ID e SHOPEE_APP_SECRET)."""
import hashlib, json, os, time, urllib.request


def chamar(query, variaveis=None):
    app_id, secret = os.environ["SHOPEE_APP_ID"], (os.environ.get("SHOPEE_APP_SECRET") or os.environ["shopee_APP_SECRET"])
    corpo = json.dumps({"query": query, "variables": variaveis or {}}, separators=(",", ":"))
    ts = str(int(time.time()))
    sig = hashlib.sha256((app_id + ts + corpo + secret).encode()).hexdigest()
    req = urllib.request.Request("https://open-api.affiliate.shopee.com.br/graphql", data=corpo.encode(), headers={
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={app_id}, Timestamp={ts}, Signature={sig}"})
    dados = json.load(urllib.request.urlopen(req, timeout=30))
    if dados.get("errors"):
        raise RuntimeError(dados["errors"])
    return dados["data"]
