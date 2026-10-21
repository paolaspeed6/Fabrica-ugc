#!/bin/bash
# Refaz o mp4 final (≤16 MB, limite da página) a partir do mestre .video.mp4 + áudio do final. uso: recodificar.sh arquivo.mp4 ...
for f in "$@"; do
  ffmpeg -v error -y -i "$f.video.mp4" -i "$f" -map 0:v -map 1:a -c:v libx264 -b:v 7.5M -maxrate 10M -bufsize 15M -preset slow \
    -pix_fmt yuv420p -c:a copy -movflags +faststart -t 15 "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f"
done
