#!/bin/bash
# Refaz UMA versão (a|b|c) de um produto com zoom maior quando o auditor acusa cena quase parada (a dona 27/10: nunca faltar versão).
# uso: refazer_versao.sh <trabalhos/pXX-slug> <a|b|c> <zoom, ex. 1.18>   (não pega o lock: quem chama já está na fila ou fora do render)
W=$(cd "$1" && pwd); V=$2; Z=$3; D=$(cd "$(dirname "$0")" && pwd); id=$(basename $W | cut -d- -f1)
declare -A N=([a]=a_umdia [b]=b_faixas [c]=c_direto)
(cd $D && LUXO_DIR=$W python3 -c "
import json,sys; sys.argv=['x','$D','1']
src=open('lote_auto.py').read(); ns={}; exec(src[src.index('CUTS ='):src.index('def cfg(')], ns)
p='$W/specs/_cfg.json'; c=json.load(open(p)); c['tomadas']['$V']=ns['tomadas'](list(c['clips']),c['clips'],{'$V':$Z})['$V']; json.dump(c,open(p,'w'),ensure_ascii=False)
from produto import fazer_produto; fazer_produto(c)") >/dev/null || exit 1
cd $D/.. && LUXO_DIR=$W python3 -I build_lux.py $W/specs/${id}_${N[$V]}.json >/dev/null
