"""Varre o catálogo da API oficial Shopee Afiliados e escolhe os candidatos do dia
com cara de poucos afiliados (a API não dá o número; o Kevin confere no app).

Uso: python3 varrer.py [--top 60] [--preco-min 200] [--max-vendidos 2000]
Saídas: snapshots/<data>.json (base para vendas/dia) e candidatos-<data>.json.
Grátis (só a API oficial). Precisa de SHOPEE_APP_ID e SHOPEE_APP_SECRET.
"""
import argparse, hashlib, json, os, re, sys, time, unicodedata, urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
SNAP = BASE / "snapshots"
ENDPOINT = "https://open-api.affiliate.shopee.com.br/graphql"
QUERY = """query($l:Int,$s:Int,$p:Int,$k:String){productOfferV2(listType:$l,sortType:$s,page:$p,limit:50,keyword:$k){
nodes{itemId shopId productName shopName priceMin sales ratingStar commission commissionRate sellerCommissionRate
productLink offerLink imageUrl productCatIds} pageInfo{hasNextPage}}}"""
PROIBIDO = ["vinho", "cerveja", "whisky", "vodka", "cachaca", "gin ", "licor", "taca de",
            "adega", "chopeira", "abridor de vinho", "carrinho bar", "bar de bebidas", "cristaleira", "porta garrafa", "tabaco", "narguile", "vape", "pod "]
ITEM_ID_RECENTE = 50_000_000_000  # ids 5x bilhões = anúncios de 2026
# Aprendido com os 60 conferidos pelo Kevin em 21/10 (vídeos de criadores no app):
# marca famosa e estas categorias lotam de vídeo mesmo sem venda.
MARCAS_LOTADAS = ["jbl", "xiaomi", "samsung", "philips", "kingston", "alok", "waaw", "lg ", "sony",
                  "apple", "iphone", "motorola", "electrolux", "mondial", "britania", "philco", "gree"]
CATEGORIAS_LOTADAS = ["caixa de som", "boombox", "robo aspirador", "aspirador robo", "ar condicionado",
                      "ar-condicionado", "ssd", "fone", "smartwatch", "celular"]
VISTOS = BASE / "vistos.json"  # itemIds que o Kevin já conferiu: não voltam


def chamar(variaveis, tentativas=4):
    app_id, secret = os.environ["SHOPEE_APP_ID"], os.environ["SHOPEE_APP_SECRET"]
    for i in range(tentativas):
        try:
            corpo = json.dumps({"query": QUERY, "variables": variaveis}, separators=(",", ":"))
            ts = str(int(time.time()))
            sig = hashlib.sha256((app_id + ts + corpo + secret).encode()).hexdigest()
            req = urllib.request.Request(ENDPOINT, data=corpo.encode(), headers={
                "Content-Type": "application/json",
                "Authorization": f"SHA256 Credential={app_id}, Timestamp={ts}, Signature={sig}"})
            dados = json.load(urllib.request.urlopen(req, timeout=30))
            if dados.get("errors"):
                raise RuntimeError(dados["errors"])
            return dados["data"]["productOfferV2"]
        except Exception as e:
            if i == tentativas - 1:
                print("falhou:", variaveis, e, file=sys.stderr)
                return {"nodes": [], "pageInfo": {"hasNextPage": False}}
            time.sleep(2 ** (i + 1))


def plano(t):
    return unicodedata.normalize("NFKD", (t or "").lower()).encode("ascii", "ignore").decode()


def varrer(palavras):
    produtos = {}
    rodadas = [{"l": 0, "s": 2}, {"l": 2, "s": 2}] + [{"l": 0, "s": 2, "k": k} for k in palavras]
    for r in rodadas:
        for pagina in range(1, 201):
            res = chamar({**r, "p": pagina})
            for p in res["nodes"]:
                produtos[str(p["itemId"])] = p
            if not res["pageInfo"]["hasNextPage"]:
                break
            time.sleep(0.5)
        print(f"rodada {r}: {len(produtos)} produtos no total", flush=True)
    return produtos


def miniatura(url):
    """Foto em data URI (a página não carrega imagem de fora). Grátis."""
    try:
        import base64, io
        from PIL import Image
        arq = url.rsplit("/", 1)[-1]
        dados = urllib.request.urlopen(f"https://down-br.img.susercontent.com/file/{arq}", timeout=20).read()  # original, não a _tn borrada
        im = Image.open(io.BytesIO(dados)).convert("RGB")
        im.thumbnail((480, 480))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=72)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


STOP = set("de da do das dos e para com sem em a o as os p/ c/ kit 1 2 3 4 5 6 cm kg l w v un unidades novo nova original oficial premium".split())


def nucleo(nome, n=3):
    """As primeiras palavras que dizem o que o produto é (o que o afiliado digitaria na busca)."""
    pal = [w for w in re.findall(r"[a-z0-9]+", plano(nome)) if w not in STOP and len(w) > 1]
    return pal[:n]



def sem_duplicatas(lista):
    """Kevin (23/10): mesma loja + mesmo núcleo do nome + mesmas medidas + preço até 5% = provável
    mesmo produto (ex.: ventilador de parede 76cm da IDEAL COMERCIO em 2 anúncios).
    Não remove nada (pode ser variação promissora): só marca "possivel_duplicata" com o id do
    anúncio de mais pontos, para o Tinder avisar. A lista já vem ordenada."""
    ficam, por_loja = [], {}
    for x in lista:
        pal = re.findall(r"[a-z0-9]+", plano(x["nome"]))
        chave = (tuple(nucleo(x["nome"])), frozenset(w for w in pal if re.fullmatch(r"\d+(cm|mm|m|l|ml|w|pol|kg|g|lt|litros)", w)))
        for y_id, y_chave, y_preco in por_loja.get(x["loja"], []):
            if chave == y_chave and abs(x["preco"] - y_preco) <= 0.05 * max(x["preco"], y_preco):
                x["possivel_duplicata"] = y_id
                break
        else:
            por_loja.setdefault(x["loja"], []).append((x["id"], chave, x["preco"]))
        ficam.append(x)
    return ficam

def contar_parecidos(produtos):
    """Quantos produtos do catálogo lido têm o mesmo núcleo de nome. Kevin (22/10): nome e produto
    incomuns = difícil de achar pela barra de busca = menos criadores."""
    titulos = [set(re.findall(r"[a-z0-9]+", plano(p["productName"]))) for p in produtos.values()]
    def conta(nome):
        nuc = nucleo(nome)
        return sum(1 for t in titulos if all(w in t for w in nuc)) if nuc else 0
    return conta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=100)
    ap.add_argument("--preco-min", type=float, default=200)
    ap.add_argument("--max-vendidos", type=int, default=30)
    ap.add_argument("--nota-min", type=float, default=4.6)
    ap.add_argument("--palavras", default=str(BASE / "palavras.txt"))
    a = ap.parse_args()

    palavras = [l.strip() for l in Path(a.palavras).read_text().splitlines()
                if l.strip() and not l.startswith("#")] if Path(a.palavras).exists() else []
    SNAP.mkdir(exist_ok=True)
    anteriores = sorted(SNAP.glob("*.json"))
    agora = datetime.now(timezone.utc)
    produtos = varrer(palavras)
    (SNAP / f"{agora:%Y%m%dT%H%M%SZ}.json").write_text(json.dumps(
        {k: [p["sales"], p["priceMin"], p["commission"]] for k, p in produtos.items()}))

    ant, horas = {}, None
    if anteriores:
        t0 = datetime.strptime(anteriores[-1].stem, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        h = (agora - t0).total_seconds() / 3600
        if h >= 12:
            ant, horas = json.loads(anteriores[-1].read_text()), h

    conta = contar_parecidos(produtos)
    vistos = set(json.loads(VISTOS.read_text())) if VISTOS.exists() else set()
    lista = []
    for k, p in produtos.items():
        if k in vistos:
            continue
        preco, vendidos = float(p["priceMin"] or 0), int(p["sales"] or 0)
        if preco < a.preco_min or vendidos > a.max_vendidos or float(p["ratingStar"] or 0) < a.nota_min:
            continue
        if any(w in plano(p["productName"]) for w in PROIBIDO):
            continue
        vdia = round((vendidos - int(ant[k][0])) * 24 / horas, 1) if horas and k in ant else None
        if vdia is None and vendidos < 5:
            continue  # sem prova de que vende
        com = float(p["commission"] or 0)
        n = min(com / 60, 1) * 3                                   # comissão em R$
        n += 2 if vendidos <= 300 else 1 if vendidos <= 1000 else 0  # pouco vendido = menos afiliados
        n += 1.5 if int(k) >= ITEM_ID_RECENTE else 0                # anúncio novo
        n += 1 if float(p["sellerCommissionRate"] or 0) > 0 else 0  # vendedor paga extra
        n += max(0, (float(p["ratingStar"]) - 4.6) / 0.4) * 0.5
        n += 1 if vendidos <= 10 else 0                             # até 10 vendidos: mediana 8 vídeos
        n += 0.5 if preco < 1000 else 0
        nome = plano(p["productName"])
        if any(m in nome for m in MARCAS_LOTADAS):
            n -= 3
        if any(c in nome for c in CATEGORIAS_LOTADAS):
            n -= 3
        parecidos = conta(p["productName"])
        n += 2 if parecidos <= 5 else 1 if parecidos <= 20 else -1 if parecidos > 100 else 0
        if vdia is not None:
            n += min(vdia / 3, 1) * 3                              # vendas subindo
        lista.append({"id": k, "nome": p["productName"], "loja": p["shopName"], "preco": preco,
                      "comissao_rs": round(com, 2), "comissao_pct": round(float(p["commissionRate"]) * 100, 1),
                      "extra_vendedor": float(p["sellerCommissionRate"] or 0) > 0,
                      "vendidos": vendidos, "vendas_dia": vdia, "novo": int(k) >= ITEM_ID_RECENTE,
                      "nota": float(p["ratingStar"]), "foto": p["imageUrl"], "link": p["productLink"],
                      "parecidos": parecidos, "pontos": round(n, 2)})
    lista.sort(key=lambda x: x["pontos"], reverse=True)
    lista = sem_duplicatas(lista)
    for x in lista[:a.top]:
        x["foto"] = miniatura(x["foto"])
    saida = BASE / f"candidatos-{agora:%Y-%m-%d}.json"
    saida.write_text(json.dumps(lista[:a.top], ensure_ascii=False, indent=1))
    print(f"{len(produtos)} lidos, {len(lista)} passaram no filtro, top {min(a.top, len(lista))} -> {saida}")
    if not horas:
        print("Primeira varredura: amanhã entra a medida de vendas por dia.")


if __name__ == "__main__":
    main()
