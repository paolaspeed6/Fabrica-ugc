"""Baixa todas as fotos e a descrição de um anúncio da Shopee (grátis, sem API).

Uso:
    python3 buscar_fotos.py <link do anúncio ou link curto s.shopee.com.br> <pasta_destino>

Lê a versão da página que a Shopee entrega a buscadores (a mesma rota que os coletores
pagos do Apify usam). Salva em <pasta_destino>:
  - 01.jpg ... : foto principal, galeria e imagens da descrição, na ordem do anúncio
  - anuncio.json: nome, descrição completa, preço, nota, link, lista de fotos (origem de cada uma)
Se a Shopee mudar a página e nada vier, o fallback é o coletor lergassy/shopee-scraper no Apify.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
IMG = "https://down-br.img.susercontent.com/file/"


def abrir(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.geturl(), r.read().decode("utf-8", "replace")


def ids(url):
    m = re.search(r"/product/(\d+)/(\d+)", url) or re.search(r"i\.(\d+)\.(\d+)", url) \
        or re.search(r"/(\d{5,})/(\d{6,})", url)
    if not m:
        raise SystemExit(f"não achei loja/item no link: {url}")
    return m.group(1), m.group(2)


def main():
    link, destino = sys.argv[1], Path(sys.argv[2])
    final = link
    if "s.shopee" in link:  # link curto de afiliado: segue o redirecionamento
        req = urllib.request.Request(link, headers={"User-Agent": UA}, method="HEAD")
        with urllib.request.urlopen(req, timeout=60) as r:
            final = r.geturl()
    loja, item = ids(final)
    _, h = abrir(f"https://shopee.com.br/product/{loja}/{item}")

    prod = {}
    for bloco in re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(bloco)
        except ValueError:
            continue
        if d.get("@type") == "Product":
            prod = d
    if not prod:
        raise SystemExit("a Shopee não entregou o registro do produto (tente o Apify)")

    # ordem: foto principal, galeria (miniaturas do topo), imagens da descrição
    fotos = [(prod["image"].rsplit("/", 1)[-1], "principal")]
    # galeria, variações e imagens da descrição; o contexto antes de cada imagem diz de onde ela é
    # (os nomes de classe da Shopee mudam, então não dependemos deles; rodapé e loja ficam de fora)
    galeria, descricao = [], []
    for m in re.finditer(re.escape(IMG) + r'([A-Za-z0-9_-]+)', h):
        ctx = h[max(0, m.start() - 250):m.start()]
        if "thumbnail" in ctx or "selection-box" in ctx:
            galeria.append(m.group(1))
        elif re.search(r'padding-bottom:[\d.]+%"><picture', ctx):
            descricao.append(m.group(1))
    for lista, origem in ((galeria, "galeria"), (descricao, "descricao")):
        for f in lista:
            if f not in [x for x, _ in fotos]:
                fotos.append((f, origem))

    destino.mkdir(parents=True, exist_ok=True)
    salvas = []
    for i, (f, origem) in enumerate(fotos, 1):
        arq = destino / f"{i:02d}.jpg"
        urllib.request.urlretrieve(IMG + f, arq)
        salvas.append({"arquivo": arq.name, "origem": origem, "url": IMG + f})
    info = {
        "nome": prod.get("name"), "descricao": prod.get("description"),
        "preco": prod.get("offers", {}).get("price"), "nota": prod.get("aggregateRating", {}).get("ratingValue"),
        "avaliacoes": prod.get("aggregateRating", {}).get("ratingCount"),
        "loja": prod.get("offers", {}).get("seller", {}).get("name"),
        "link": link, "url": prod.get("url"), "shopId": loja, "itemId": item, "fotos": salvas,
    }
    (destino / "anuncio.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{info['nome']}\n{len(salvas)} fotos em {destino}")


if __name__ == "__main__":
    main()
