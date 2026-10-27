#!/bin/bash
# Produto `complexo` (regra K14): cola o cartão da foto 01 num canto livre, o vídeo todo. Automático para o lote_auto/produzir.sh.
# A e C: canto de baixo à direita (textos ficam em cima); B: canto de cima à direita (textos ficam embaixo).
# uso: colar_auto.sh <foto01.jpg> <video.mp4> <a|b|c>   (troca o vídeo no lugar)
F=$1; V=$2; LAY=$3; D=$(dirname "$0"); T=$(mktemp -d)
python3 -I $D/card.py "$F" $T/c 270 >/dev/null || exit 1
[ "$LAY" = b ] && Y=150 || Y=1480
ffmpeg -v error -y -i "$V" -i $T/c_fg.png -filter_complex "[1]format=rgba,fade=in:st=0:d=0.4:alpha=1[c];[0][c]overlay=W-w-40:$Y" \
  -map 0:a? -c:a copy -c:v libx264 -crf 19 -preset medium -pix_fmt yuv420p -movflags +faststart $T/o.mp4 && mv $T/o.mp4 "$V"
rm -rf $T
