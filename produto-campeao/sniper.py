"""Product Sniper: cruza os achados do TikTok Shop (FastMoss) com o anúncio equivalente na Shopee.

Uso:
    python3 sniper.py <candidatos.json> <saida_cartoes.json>

candidatos.json: lista de {"id", "busca" (termos para a Shopee), "tiktok": {vendas_7d, criadores,
comissao, lancado, preco, titulo}, "precisa": [palavras que o nome do anúncio tem que ter, sem acento],
opcional "evitar": [palavras que descartam um anúncio].
Para cada um, busca na Shopee (página servida a buscadores, grátis), lê os 12 primeiros anúncios
e escolhe o que melhor bate com a regra da dona: nota 4,7+, R$ 30-150, poucas avaliações
(anúncio novo, menos afiliados) e id de item alto (anúncio recente).
"""
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"


def abrir(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def anuncio(loja, item):
    h = abrir(f"https://shopee.com.br/product/{loja}/{item}")
    for bloco in re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(bloco)
        except ValueError:
            continue
        if d.get("@type") == "Product":
            r = d.get("aggregateRating") or {}
            o = d.get("offers") or {}
            preco = o.get("price") or o.get("lowPrice")
            return {
                "nome": d.get("name"), "foto": d.get("image"),
                "preco": float(preco) if preco else None,
                "nota": float(r["ratingValue"]) if r.get("ratingValue") else None,
                "avaliacoes": int(r["ratingCount"]) if r.get("ratingCount") else 0,
                "loja": (o.get("seller") or {}).get("name"),
                "link": f"https://shopee.com.br/product/{loja}/{item}", "shopId": loja, "itemId": item,
            }
    return None


def plano(t):
    return unicodedata.normalize("NFKD", (t or "").lower()).encode("ascii", "ignore").decode()


def pontos(a):
    if not a or not a["nota"] or a["nota"] < 4.7 or not a["preco"] or not 30 <= a["preco"] <= 150:
        return -1
    p = 0
    p += 3 if 5 <= a["avaliacoes"] <= 300 else 1 if a["avaliacoes"] <= 1500 else 0
    p += 2 if int(a["itemId"]) >= 50_000_000_000 else 0  # ids 5x bilhões = anúncios de 2026
    p += (a["nota"] - 4.7) * 5
    return p


def main():
    cands = json.load(open(sys.argv[1], encoding="utf-8"))
    saida = []
    for c in cands:
        if c.get("shopee_link"):  # anúncio já conhecido (busca anterior)
            loja, item = re.search(r"/(\d+)/(\d+)", c["shopee_link"]).groups()
            a = anuncio(loja, item)
            saida.append({**c, "shopee": a if pontos(a) >= 0 else None})
            print(c["id"], "->", a and a["nome"][:60])
            continue
        h = abrir("https://shopee.com.br/search?keyword=" + urllib.parse.quote(c["busca"]))
        vistos, achados = set(), []
        for loja, item in re.findall(r'href="/[^"]*-i\.(\d+)\.(\d+)', h):
            if (loja, item) in vistos:
                continue
            vistos.add((loja, item))
            if len(vistos) > 12:
                break
            try:
                a = anuncio(loja, item)
            except Exception:
                a = None
            nome = plano(a and a["nome"])
            if a and all(w in nome for w in c.get("precisa", [])) \
                    and not any(w in nome for w in c.get("evitar", [])):
                achados.append(a)
            time.sleep(0.5)
        melhor = max(achados, key=pontos, default=None)
        if melhor is not None and pontos(melhor) < 0:
            melhor = None
        if melhor is None:
            print("   sem anúncio bom; vistos:", [(x["nome"][:40], x["preco"], x["nota"]) for x in achados])
        saida.append({**c, "shopee": melhor})
        print(c["id"], "->", melhor and f'{melhor["nome"][:60]} | R$ {melhor["preco"]} | {melhor["nota"]} | {melhor["avaliacoes"]} aval.')
    json.dump(saida, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
