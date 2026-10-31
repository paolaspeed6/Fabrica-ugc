# Resumo das regras para os agentes (1 página; economia de uso, a dona 26/10)
Agentes do setor de qualidade (Fichador, Fiscais) leem SÓ este resumo + o BRIEF da função. O arquivo completo
(`agentes/regras_de_erros.md`) é para o orquestrador e para o Melhorador.

## Produto igual ao anúncio
- Foto 01 manda: cor por parte (tom hex), forma, proporção, lado/orientação, posição de cada item, número exato de cada peça
  (pernas, travessas, botões, rodas, voltas de mangueira, acessórios). Kit de N = N inteiros. Medidas de cada parte.
- Letra no produto copiada letra por letra; miúda ou difícil = câmera longe (sem close). Propaganda da foto nunca é produto.
- Produto parado; quem se mexe é a câmera. Avanço curto (15-20 cm) só se houver folga; folga pequena = deriva lateral curta ou descida.
- Tamanho real: comparar com portas, bancadas, camas; produto pequeno ganha objeto de escala com tamanho real.

## Enquadramento (motivo nº 1 de reprovação)
- Produto inteiro (todos os itens) em no máximo 60% da largura, 12% de folga de cada lado. `folha.py` mede e reprova sozinho (< 3% ou > 88%).
- Produto largo, comprido ou kit = câmera mais longe. Capa (1º quadro) com o produto inteiro, sem mão nem pessoa.

## Proibidos (em qualquer lugar da cena)
Pessoa, mão, bebê, animal, garrafa, taça, copo, frasco, pote de vidro, bebida, chama acesa, tela/painel aceso (salvo se a foto 01 mostra),
texto de propaganda, selos, cotas/medidas desenhadas. Fundo com VIDA (a dona, 31/10): sol dourado com sombras de folhas, plantas, tapete,
no máximo 2-3 peças de decoração simples e grandes (cerâmica fosca larga, galhos secos, tábua, quadro sem texto); reprovar só fundo bagunçado,
decoração encostando no produto ou vaso com gargalo fino que pareça garrafa.
Nunca citar o proibido no prompt (nem negando): descrever o certo.

## Textos (vídeo e legenda)
Só o que está ESCRITO no título/descrição. Número que discorda entre título e descrição = fora. Sem prazo de entrega, %, nota,
número de avaliações, bebida. Cor, formato, "linhas retas" não são qualidade. Gancho: pergunta ou problema; horário só se combinar.
Legendas < 150 caracteres, 4 hashtags de nicho.

## Produto que não dá para fazer (Fichador descarta ANTES de gastar)
Nenhuma foto com o produto limpo (pessoa/bebê cobrindo peças), réplica de marca ("Original" com outro nome no corpo),
variações misturadas sem foto da escolhida. Marque `"pular": true` com o motivo.

## Refação
Só UMA. Reprovou de novo = cena "falhou" e o produto usa outra cena aprovada. Toda perda vai em `agentes/desperdicios.md`.

## Entrega
Todo produto sai com A, B e C (versão reprovada é refeita, não pulada). Produto sem cena aprovada (K22, 30/10): a fábrica monta A, B e C com as imagens reprovadas só por borda (câmera por código) e manda com aviso; defeito grave fica fora. Sem imagem aproveitável = "resgate", nunca descartado direto.
