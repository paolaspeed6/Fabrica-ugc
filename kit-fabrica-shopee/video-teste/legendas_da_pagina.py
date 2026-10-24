#!/usr/bin/env python3
"""Tira as legendas de uma página de vídeos prontos (index.html) para um .txt.

Uso: python3 legendas_da_pagina.py index.html [mais.html...] -o legendas.txt
Entende os dois formatos de página: <p id="cap-gNN-versao"> e PRODUTOS = [...].
"""
import argparse, html, json, re

ap = argparse.ArgumentParser()
ap.add_argument("paginas", nargs="+")
ap.add_argument("-o", required=True)
a = ap.parse_args()
linhas = []
for p in a.paginas:
    t = open(p, encoding="utf-8").read()
    m = re.search(r"PRODUTOS\s*=\s*(\[.*?\]);\s*\n", t, re.S)
    if m:
        for prod in json.loads(m.group(1)):
            linhas.append(f"== g{prod['n']} · {prod['nome']} · {prod.get('link', '')}")
            for v in prod["videos"]:
                linhas.append(f"[{v['nome']}] {v['legenda']}")
            linhas.append("")
        continue
    for g, ver, leg in re.findall(r'<p id="cap-(g\d+)-(\w+)">(.*?)</p>', t, re.S):
        linhas.append(f"[{g}_{ver}.mp4] {html.unescape(re.sub(r'<[^>]+>', '', leg)).strip()}")
open(a.o, "w", encoding="utf-8").write("\n".join(linhas) + "\n")
print(f"{a.o}: {len(linhas)} linhas")
