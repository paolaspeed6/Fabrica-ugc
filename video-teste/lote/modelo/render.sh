#!/bin/bash
# monta e renderiza as 3 versões de cada produto (3 em paralelo) no scratchpad, audita e copia só os finais para final/
# com nome fácil de achar: <PREFIXO>_NN_<slug>_A.mp4 (Shopee Um dia), _B.mp4 (Faixas), _C.mp4 (Checklist), _Reels.mp4.
# uso: RENDER_DIR=<scratchpad> bash render.sh p05 p09 ...
cd "$(dirname "$0")"; PRE=${PREFIXO:-$(basename "$PWD" | sed s/lista// | tr a-z A-Z)}; VT=$(cd ../.. && pwd); R=${RENDER_DIR:?defina RENDER_DIR}; mkdir -p final $R
for k in "$@"; do
  d=$R/$k-luxo; LUXO_DIR=$d python3 -I montar.py $k > $R/$k-montar.log 2>&1 < /dev/null || { echo "$k montar FALHOU"; continue; }
  for o in a_umdia b_faixas c_lista r_reels; do LUXO_DIR=$d timeout -s KILL 2700 python3 -I $VT/luxo/build_lux.py $d/specs/${k}_$o.json > $d/render_$o.log 2>&1 < /dev/null & done; wait
  python3 -I $VT/auditar_video.py $d/out2/${k}_a_umdia.mp4 $d/out2/${k}_b_faixas.mp4 $d/out2/${k}_c_lista.mp4 $d/out2/${k}_r_reels.mp4 < /dev/null 2>&1 | cut -c1-140
  s=$(python3 -c "import json;print(json.load(open('textos.json'))['$k']['slug'])"); n=${k#p}
  for o in a_umdia:A b_faixas:B c_lista:C r_reels:Reels; do f=$d/out2/${k}_${o%%:*}.mp4; [ -f $f ] && cp $f final/${PRE}_${n}_${s}_${o##*:}.mp4; done
  echo "$k pronto"
done
