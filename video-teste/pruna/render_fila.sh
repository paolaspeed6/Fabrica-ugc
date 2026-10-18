#!/bin/bash
# Renderiza (2 por vez) cada sNN com a marca lote/lista1017/sNN.aprovado; para depois de 90 min sem nada novo.
cd "$(dirname "$0")/.."
L=lote/lista1017; ocioso=0
while [ $ocioso -lt 180 ]; do
  novo=0
  for a in $L/s[0-9][0-9].aprovado; do
    [ -e "$a" ] || continue
    s=$(basename $a .aprovado); [ -e $L/$s.render ] && continue
    while [ $(jobs -rp | wc -l) -ge 2 ]; do sleep 5; done
    touch $L/$s.render; novo=1
    ( timeout -s KILL 1200 python3 fazer_lista.py $L/$s.json < /dev/null > $L/$s-cenas/render.log 2>&1
      echo "$(date +%H:%M:%S) $s $(tail -1 $L/$s-cenas/render.log)" >> pruna/render.log ) &
  done
  [ $novo = 1 ] && ocioso=0 || ocioso=$((ocioso+1))
  sleep 30
done
wait; echo "$(date +%H:%M:%S) FIM" >> pruna/render.log
