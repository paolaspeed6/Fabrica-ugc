#!/bin/bash
# Entrega uma parte do lote: finais aprovados no auditor -> <lote>/final -> Drive -> docs da Conferência (conferir_docs/).
# uso: entregar.sh <lote> <PREFIXO> <AAAA-MM-DD> "<nome do lote>" <max> pNN pNN ...   (mapa pNN->trabalhos em <lote>/trabalhos_todos.json)
L=$1; PRE=$2; DIA=$3; NOME=$4; MAX=$5; shift 5; R=/home/user/fabrica-ugc; mkdir -p $L/final; n=0
for k in "$@"; do
  w=$(python3 -c "import json;print(json.load(open('$L/trabalhos_todos.json')).get('$k',''))"); [ -z "$w" ] && continue
  ls $L/final/${PRE}_${k#p}_* >/dev/null 2>&1 && continue
  id=${w%%-*}; o=$R/trabalhos/$w/out2; ok=1
  for v in a_umdia b_faixas c_direto; do [ -f $o/${id}_$v.mp4 ] || ok=0; done; [ $ok = 1 ] || continue
  slug=$(python3 -c "import json;print(json.load(open('$L/textos.json'))['$k']['slug'])"); boas=0
  for x in A:a_umdia B:b_faixas C:c_direto; do f=$o/${id}_${x#*:}.mp4  # auditor por vídeo: 1 reprovado não barra os outros 2 (26/10)
    python3 $R/video-teste/auditar_video.py $f | grep -q REPROVADO && { echo "$k ${x%%:*} reprovado no auditor"; continue; }
    [ $(stat -c%s $f) -gt 15500000 ] && bash $R/video-teste/luxo/recodificar.sh $f
    cp $f $L/final/${PRE}_${k#p}_${slug}_${x%%:*}.mp4 && ffprobe -v error $L/final/${PRE}_${k#p}_${slug}_${x%%:*}.mp4 || { rm -f $L/final/${PRE}_${k#p}_${slug}_${x%%:*}.mp4; echo "$k ${x%%:*} cópia falhou"; continue; }; boas=$((boas+1))
  done; [ $boas = 0 ] && continue
  echo "$k -> $w ok"; n=$((n+1)); [ $n -ge $MAX ] && break
done
python3 $R/video-teste/drive_backup.py $L/final --dia $DIA | tail -2
cd $L && python3 -I conferencia.py "$NOME" $DIA | tail -1; echo "ENTREGUES=$n"
