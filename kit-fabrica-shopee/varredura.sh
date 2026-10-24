#!/bin/bash
# Varredura diária do Tinder (grátis, ~1h45). Mac/Linux: agende com crontab -e:  0 6 * * * bash /caminho/varredura.sh
cd "$(dirname "$0")" && python3 produto-campeao/afiliados/varrer.py >> produto-campeao/afiliados/varredura.log 2>&1
