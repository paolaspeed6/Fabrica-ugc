#!/bin/bash
# fila das varreduras paty (uma de cada vez: dividem o limite da API de afiliados)
cd "$(dirname "$0")"
TAG=_patymoveis timeout 5400 python3 varrer_carrossel.py --palavras palavras_paty_moveis.txt --top 20 --refs referencias_paty --max-tipo 2 --preco-max 600 > patymoveis.log 2>&1
TAG=_patycasa timeout 7200 python3 varrer_carrossel.py --palavras palavras_paty_casa.txt --top 40 --refs referencias_paty --max-tipo 3 --preco-max 200 --com-min 5 > patycasa.log 2>&1
touch fila_paty.fim
