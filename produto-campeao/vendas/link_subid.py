"""Gera o link de afiliado de um vídeo com Sub ID, para saber depois qual vídeo vendeu.

Uso: python3 link_subid.py <link do produto> <produto> <versao> [AAMMDD]
Ex.:  python3 link_subid.py https://shopee.com.br/product/1/2 L0101Ap01 A
Sub ID = <produto><versao><AAMMDD>, só letras e números (a Shopee recusa hífen e _ ; testado 22/10).
Ex.: L0101Ap01A260101 = Lista 01/01 A, produto 01, versão A (Shopee A; B = Shopee B; R = Reels). Grátis.
"""
import re
import sys
from datetime import date
from api import chamar

M = "mutation($u:String!,$s:[String!]){generateShortLink(input:{originUrl:$u,subIds:$s}){shortLink}}"


def link(url, produto, versao, dia=None):
    sub = re.sub(r"[^A-Za-z0-9]", "", f"{produto}{versao}{dia or format(date.today(), '%y%m%d')}")
    return sub, chamar(M, {"u": url, "s": [sub]})["generateShortLink"]["shortLink"]


if __name__ == "__main__":
    print(*link(*sys.argv[1:5]))
