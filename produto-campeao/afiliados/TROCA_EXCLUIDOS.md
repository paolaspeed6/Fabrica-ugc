# Troca automática de excluídos com o Kevin (pasta do Drive "Horst Ads Excluídos")

**Pasta: "Horst Ads Excluídos", id `1cYV-TSkE_cFpWPrItY5L65JD5s5rcDi6`** (https://drive.google.com/drive/folders/1cYV-TSkE_cFpWPrItY5L65JD5s5rcDi6), do Kevin, compartilhada com ela como editora (10/11).
Ler/baixar com o conector Google Drive (search_files parentId = esse id); o GDRIVE_* da fábrica (escopo drive.file) não enxerga os arquivos do Kevin.
Já juntados: `excluidos_juntados.txt`. 1ª troca feita em 10/11 (subido excluidos_esposa_2026-11-10_inicial.json, 1250 ids).

O Kevin compartilha com ela a pasta "Horst Ads Excluídos" no Google Drive, como editora. Cada um sobe ali os produtos que pegou, e a rotina de cada um lê os do outro. Assim nenhum produto aparece pros dois.

Na rotina diária dela, com o conector Google Drive ligado:

**Antes de varrer**
1. Procure na pasta "Horst Ads Excluídos" (compartilhada com ela) os arquivos com título `excluidos_kevin_*.json`. Baixe só os que ainda não foram juntados; anote os títulos já juntados em `excluidos_juntados.txt`.
2. Rode `python3 trocar_excluidos.py juntar esposa <arquivos baixados>` e acrescente os títulos ao `excluidos_juntados.txt`.

**Depois de semear o Tinder**
3. Rode `python3 trocar_excluidos.py gerar esposa candidatos-<data>.json excluidos_esposa_<data>.json`, com os ids que ela semeou hoje.
4. Suba o arquivo na pasta como **arquivo novo**, título `excluidos_esposa_<data>.json`, tipo application/json, sem converter pra formato Google. Nunca apague nem edite os arquivos do Kevin.

Primeira vez: suba também um `excluidos_esposa_<data>_inicial.json` com todos os ids do vistos.json dela, no formato {"de":"esposa","data":"AAAA-MM-DD","tipo":"inicial","ids":[...]}.
