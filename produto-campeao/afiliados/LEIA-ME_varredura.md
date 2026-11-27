# Atualização da varredura diária (10/11/2026)

Instrução para a sessão do Claude que roda a varredura. Aplique os passos na ordem.

## O que muda
1. **busca_diaria.py (novo):** roda a mesma varredura do varrer.py, mas salva cada rodada em `ck_diaria_<data>/` e faz 3 rodadas em paralelo. Cai de mais de 2 h para ~65 min, e se a sessão cair ela continua de onde parou. Use sempre este, não o varrer.py direto.
2. **varrer.py atualizado:**
   - comissão ≤ 7% do preço perde 1 ponto;
   - lê `excluidos.json` ({motivo: [itemIds]}) e nunca mostra esses produtos;
   - `POUCO_ESCOLHIDOS` começa vazio (é aprendido com os descartes dela, veja "Aprender").
3. **excluidos_kevin.json:** produtos que já foram do Kevin. Assim os dois não pegam o mesmo produto.
4. **palavras_grande.txt:** 94 palavras extras para os dias em que ela quiser muitos links (modo triplo).

## Troca com o Kevin
Veja TROCA_EXCLUIDOS.md (pasta do Drive compartilhada; substitui o excluidos_kevin.json nas próximas vezes).

## Instalar
1. Faça backup de `varrer.py` e, se existir, de `excluidos.json` na pasta atual da varredura.
2. Copie `varrer.py`, `busca_diaria.py` e `palavras_grande.txt` para essa pasta. Se ela já tiver mudado o `palavras.txt` dela, mantenha o dela.
3. Junte `excluidos_kevin.json` ao `excluidos.json` dela, como uma chave nova. **Não apague as chaves que já existem** nem o `vistos.json` dela.
4. Variáveis de ambiente: `SHOPEE_APP_ID` e `SHOPEE_APP_SECRET` com a API de afiliados **dela**. Se a sessão roda na nuvem do Claude, o host `open-api.affiliate.shopee.com.br` precisa estar liberado **sem injeção** de credencial (a injeção quebra a assinatura).

## Rodar (rotina diária)
- Normal (top 100): `timeout 10800 python3 busca_diaria.py > varredura_diaria.log 2>&1`
- Rode destacado do terminal (por exemplo `setsid nohup ... &`) e espere o arquivo de fim, porque pode passar de 1 h.
- **Modo triplo (top 300):** junte `palavras.txt` com as palavras de `palavras_grande.txt` que ainda não estão nele num `palavras_triplo.txt`. No fim do `busca_diaria.py`, troque `sys.argv = ["varrer.py"]` por `sys.argv = ["varrer.py", "--top", "300", "--palavras", "palavras_triplo.txt"]`.
- Se a API devolver muitos `System Error` ou `Rate limit`, rode com 2 em paralelo e `sleep 1.0`. As rodadas já salvas são puladas.
- Antes de rodar, confira se não tem outra varredura do mesmo dia rodando: as duas dividem o limite da API.
- Depois de semear no Tinder: ponha os ids semeados no `vistos.json` e apague `ck_diaria_<data>/`.

## Aprender (toda semana ou a cada ~50 decisões)
1. Leia as decisões dela no Tinder (aprovado ou descartado).
2. Se ≥ 70% dos descartes de uma categoria se repetem (ex.: 5 de 7 berços), ponha a palavra sem acento em `POUCO_ESCOLHIDOS` (-1 ponto, continua na busca).
3. Se um padrão numérico aparece nos descartes (ex.: comissão baixa), ajuste o peso no varrer.py, com um comentário dizendo a data e o motivo.
4. Nunca use decisões de outra pessoa como se fossem dela.

## Espaço do Tinder (a dona, 21/11: "pode apagar produtos que já recusei")
O banco do Tinder tem limite de 100 MB (cada produto guarda a foto). Em TODA rodada, antes do batch dos novos:
1. ArtifactData query na coleção `candidatos` com `where status == "descartado"`, `limit 1000`, `out_dir` no scratchpad (vem ~75 por página).
2. Guarde nome/link/loja de cada um em `listas/tinder_descartados_apagados.json` (backup leve, sem foto).
3. ArtifactData batch `delete` (até 50 por batch, `if_version` = versão listada). Apague 2 páginas por rodada.
Os ids continuam em `vistos.json`, então não voltam para o Tinder. Nunca apague status novo/aprovado/producao/pronto.
Se o batch dos novos der `quota_exceeded`, apague mais uma página de descartados e tente de novo.

## 27/11: Tinder desligado (a dona)
Quem escolhe os produtos agora é só a Central do PC (o celular confere a lista da busca). A rotina NÃO semeia mais no Tinder
(ele encheu: 100 MB). A busca continua 2x por dia mandando candidatos-<data>[_tarde].json para o Drive (Central Esposa).
