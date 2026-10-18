#!/bin/bash
# Renderiza os 3 vídeos de cada produto (3 em paralelo) e audita. uso: render_lote.sh trabalhos/pNN-nome ...
cd "$(dirname "$0")"
exec 9>/tmp/fabrica_render.lock; flock 9  # uma fila só: lotes esperam a vez
for d in "$@"; do
  id=$(basename "$d" | cut -d- -f1)
  for o in a_umdia b_faixas c_direto; do LUXO_DIR=$d python3 -I build_lux.py $d/specs/${id}_$o.json >/dev/null & done; wait
  python3 ../auditar_video.py $d/out2/${id}_a_umdia.mp4 $d/out2/${id}_b_faixas.mp4 $d/out2/${id}_c_direto.mp4 | cut -c1-110
done
