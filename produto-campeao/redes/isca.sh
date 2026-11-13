#!/bin/bash
cd "$(dirname "$0")"
until [ -f fila_paty.fim ]; do sleep 30; done

# iscas (a dona, 13/11 "sim"): reaproveita as buscas paty já salvas
TAG=_paty timeout 3600 python3 varrer_carrossel.py --palavras palavras_paty.txt --top 15 --refs referencias_paty --max-tipo 2 --isca > isca1.log 2>&1
TAG=_patycasa timeout 3600 python3 varrer_carrossel.py --palavras palavras_paty_casa.txt --top 15 --refs referencias_paty --max-tipo 2 --isca > isca2.log 2>&1
touch isca.fim
