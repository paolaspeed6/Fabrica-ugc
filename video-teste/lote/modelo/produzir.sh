#!/bin/bash
# Lote inteiro sem o Claude no meio (a dona, 27/10: economizar uso). Rode com o Bash do Claude em segundo plano
# (run_in_background, timeout 7200000): a máquina fica ligada e o Claude recebe 1 aviso só no fim de cada fase.
#   fase1 <lote> p01,p02,...    imagens -> borda (folha.py) -> Fiscal Gemini -> 1 refação -> borda + Gemini de novo
#   (o Claude roda 1 agente Sonnet só nas folhas: PROMPT_FISCAL_SONNET.md)
#   fase2 <lote> p01,... <PRE> <AAAA-MM-DD> "<Lista DD/MM X>"   aplica -> clipes -> Fiscal de vídeo Gemini -> edição -> render -> entrega
# Teto: TETO_USD no ambiente (gerar.py para sozinho). Log: <lote>/produzir.log
set -u; F=$1; L=$(cd "$2" && pwd); P=$3; R=/home/user/fabrica-ugc; S=$R/video-teste/luxo/specs
log(){ echo "$(date -u +%H:%M) $*" | tee -a $L/produzir.log; }
cd $L
sem_veredito(){ python3 -c "
import json,os,sys
r=[]
for p in '$P'.split(','):
    try: fi=json.load(open(p+'-cenas/fiscal_imagem.json'))
    except Exception: fi={}
    r+=[p+c for c in 'ABC' if os.path.exists(p+'-cenas/'+c+'.jpg') and c not in fi]
print(','.join(r))"; }
gemini(){ x=$(sem_veredito); [ -n "$x" ] || return 0
  python3 -I folha.py $P >> produzir.log 2>&1   # borda medida por código: reprova sozinho
  x=$(sem_veredito); [ -n "$x" ] && python3 -I fiscal_gemini.py $x >> produzir.log 2>&1
  python3 -I folha.py $P >> produzir.log 2>&1; }  # folha final com os vereditos
if [ "$F" = fase1 ]; then
  log "fase1 $P"; python3 -I gerar.py imagens $P >> produzir.log 2>&1; gemini
  python3 -I aplicar_fiscal.py $P | tee -a produzir.log
  python3 -I gerar.py imagens $P >> produzir.log 2>&1; gemini   # refação única
  log "FASE1_PRONTA gasto=$(python3 -c "import json;print(json.load(open('gasto.json'))['usd'])")"
  exit 0
fi
PRE=$4; DIA=$5; NOME=$6
log "fase2 $P"; python3 -I aplicar_fiscal.py $P | tee -a produzir.log
python3 -c "  # Sonnet reprovou cena já liberada: fica 'falhou' (não gera 3ª imagem)
import json
for p in '$P'.split(','):
    f=json.load(open(p+'-ficha.json')); fi=json.load(open(p+'-cenas/fiscal_imagem.json'))
    for c in f['cenarios']:
        if c.get('estado')=='animar' and not fi.get(c['id'],{}).get('veredito','').upper().startswith('APROV'): c['estado']='falhou'
    json.dump(f,open(p+'-ficha.json','w'),ensure_ascii=False,indent=1)"
an=$(python3 -c "
import json,os
r=[]
for p in '$P'.split(','):
    for c in json.load(open(p+'-ficha.json'))['cenarios']:
        if c.get('estado')=='animar' and not os.path.exists(p+'-cenas/'+c['id']+'.mp4'): r.append(p+c['id'])
print(','.join(r))")
[ -n "$an" ] && python3 -I gerar.py clipes $an >> produzir.log 2>&1
vs=$(python3 -c "
import json,os
r=[]
for p in '$P'.split(','):
    try: fv=json.load(open(p+'-cenas/fiscal_video.json'))
    except Exception: fv={}
    r+=[p+c for c in 'ABC' if os.path.exists(p+'-cenas/'+c+'.mp4') and c not in fv]
print(','.join(r))")
[ -n "$vs" ] && python3 -I fiscal_video_gemini.py $vs >> produzir.log 2>&1
python3 -I aprovar.py $(echo $P | tr , ' ') >> produzir.log 2>&1
python3 -I descartadas.py "$NOME" $DIA >> produzir.log 2>&1   # produto sem cena aprovada: a dona confere as reprovadas (27/10)
n0=$(ls $R/trabalhos | sed -n 's/^p\([0-9]*\)-.*/\1/p' | sort -n | tail -1); n0=$((n0+1))
(cd $S && python3 lote_auto.py $L $n0 $P) >> produzir.log 2>&1
python3 -c "
import json,os
a=json.load(open('trabalhos_todos.json')) if os.path.exists('trabalhos_todos.json') else {}
a.update(json.load(open('trabalhos.json'))); json.dump(a,open('trabalhos_todos.json','w'),indent=1)"
bash $R/video-teste/luxo/render_lote.sh $(python3 -c "import json;print(' '.join('$R/trabalhos/'+v for v in json.load(open('trabalhos.json')).values()))") >> produzir.log 2>&1
find $R/trabalhos -name "*.video.mp4" -delete   # intermediários enchem o disco (26/10)
bash $R/video-teste/lote/entregar.sh $L $PRE $DIA "$NOME" 99 $(echo $P | tr , ' ') >> produzir.log 2>&1
log "FASE2_PRONTA gasto=$(python3 -c "import json;print(json.load(open('gasto.json'))['usd'])") conferir_docs=$(ls conferir_docs 2>/dev/null | wc -l)"
