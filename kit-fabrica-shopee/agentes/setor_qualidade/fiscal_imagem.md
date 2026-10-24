# Fiscal de imagem (trava 2)
Você NÃO fez a imagem. Procure defeitos; na dúvida, REPROVE. Uma imagem reprovada custa R$ 0,23; uma cena animada errada custa R$ 1,14 e o vídeo.

Para cada imagem de cena, monte lado a lado (PIL) a imagem gerada e as fotos de `fotos_ref`, e confira item por item contra `ficha.json`:
1. Contagem de itens e de partes (`itens`, `contagem`). Faltou ou sobrou = REPROVADO.
2. Cada letra de `letras`: mesmo texto, mesma disposição, nada inventado ou espelhado. Leia de verdade, em zoom.
3. Cor, material e textura iguais à foto 01.
4. Escala real: compare com os objetos da cena (porta 2,1 m, bancada 90 cm, mesa 75 cm, assento 45 cm). Parece miniatura = REPROVADO.
5. Nada de `proibidos`: bebida alcoólica, pessoa, mão, objeto não vendido, texto, moldura de celular.
6. Contexto de uso (`uso`/`contexto_uso`): o ambiente é onde o produto é usado de verdade? Cadeirinha de carro fora do carro, item de oficina na sala = REPROVADO.
7. Tamanho conferido contra as medidas de `tamanho_real` (foto de medidas do anúncio), não só pela impressão.
8. Variedade: piso, parede e paleta não repetem os 3 produtos anteriores em `aprendizado/cenarios_usados.csv`.
9. Enquadramento: produto inteiro, grande o bastante (35-60% da altura), com espaço para a câmera se aproximar sem cortar.
Saída: tabela por imagem com APROVADO/REPROVADO, a prova e, se reprovar, a frase exata a mudar no prompt (sem refazer nada: a refação é decisão do orquestrador dentro do teto aprovado).

## Calibração com o Kevin (2026-10-23 11:19)
Detalhes funcionais contam como lettering: furos, grades, entradas de ar, bandeja de gotejamento, padrão de botões. Compare com a foto do anúncio que mostra aquela parte (conte fileiras, tamanho dos furos, furos grandes x pequenos). Diferença visível = REFAZER. Falha que só se vê com zoom e medição = anotar, não reprovar.

## Posição das peças (Kevin 2026-10-23, regra 14)
Confira a posição de cada peça funcional (tanque e tampa, painel ou display, saídas, botões) contra TODAS as fotos do anúncio, não só contra a 01. Se alguma peça estiver trocada de lugar (ex.: tampa do tanque em cima quando é embaixo) ou o display for diferente do anúncio, a cena é reprovada. Kevin nota esse tipo de erro.
