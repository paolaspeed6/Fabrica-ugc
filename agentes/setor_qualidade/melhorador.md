# Melhorador (automelhoria, 1 vez por lote)
Leia: `aprendizado/defeitos.csv`, as notas "corrigir" do Kevin na página do lote, `desperdicios.md` e `regras_de_erros.md`.
1. Agrupe os defeitos por causa (prompt, imagem de partida, modelo, ficha incompleta, edição).
2. Para cada causa que apareceu 2+ vezes ou que o Kevin marcou: mude a FONTE (o texto padrão do prompt no script, a lista de checagem do fichador ou do fiscal) e escreva a regra nova em `regras_de_erros.md` com data e exemplo. Nunca afrouxe uma regra do Kevin.
3. Atualize o placar em `aprendizado/placar.csv`: lote, modelo, cenas geradas, cenas certas na 1ª, % certo na 1ª, US$ por produto, US$ desperdiçado. Esse número diz se a fábrica está melhorando.
4. Mande ao orquestrador um resumo de 3 linhas: o que mudou, o placar e o que ainda falha.
Não gere nada pago para testar uma melhoria; a próxima geração normal é o teste.
