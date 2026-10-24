#!/bin/bash
# Roda a fila de postagem a cada hora (ritmo seguro), até acabar ou passar ~110 min.
# Uso: MAX_DIA=10 INTERVALO_H=0.95 bash rodar_fila.sh fila.json
cd "$(dirname "$0")"
fim=$(( $(date +%s) + 6600 ))
while :; do
  date -u +%FT%TZ
  python3 postar.py "$1" --fila 2>&1 | grep -v '^espera'
  falta=$(python3 -c "
import json,os,sys;sys.path.insert(0,'.');import postar
r=postar.ler_registro();p=json.load(open('$1'))
print(sum(1 for v in p if f\"{v['rede']}|{os.path.basename(v['arquivo'])}\" not in r))")
  echo "faltam $falta"
  [ "$falta" = 0 ] && break
  [ $(( $(date +%s) + 3600 )) -gt $fim ] && break
  sleep 3600
done
