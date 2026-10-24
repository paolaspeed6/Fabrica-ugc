# Busca automática de produtos Shopee com poucos vídeos de criadores

Atualizado em 22/10/2026. Cada lição tem data e de onde veio. Script: produto-campeao/afiliados/varrer.py.
Página onde o Kevin confere: "Caça Poucos Afiliados" ((sua página Tinder Shopee, veja paginas/)).

## A métrica
- O que importa é o número de VÍDEOS DE CRIADORES do produto, visto só no app (Kevin, 21/10). Afiliados não importam.
- Regra de ouro (Kevin, 21/10): vendas recentes + 0 a 3 vídeos = venda quase certa, porque o nosso vídeo aparece primeiro na busca. Até 10 vídeos + vendas recentes = vale criar.
- Nenhuma API, página pública ou ferramenta paga mostra esse número (pesquisado em 21/10). Nunca usar robô no app, captcha pago ou login automático (risco de perder a conta de afiliado).

## O que separa produto vazio de produto lotado (60 conferidos em 21/10)
1. Total vendido: até 10 vendidos teve mediana de 8 vídeos; de 11 a 30, 14; acima de 30, 21.
2. Marca famosa lota mesmo sem venda: JBL 39, Xiaomi 33 e 34, Alok/Waaw 12 e 30, Kingston 1.200, Philips Evnia 1.600.
3. Categorias lotadas: caixa de som, robô aspirador, ar-condicionado. Vazias: purificador, cadeira de escritório, monitor de marca pequena, ventilador, gaiola, bebedouro, motor de popa.
4. Preço abaixo de R$ 1.000: mediana de 7 vídeos, contra 12 acima.
5. Comissão extra do vendedor não separou nada (todos os 60 tinham). A API não mostra anúncio pago.
6. Nome incomum (Kevin, 22/10): a maioria dos afiliados acha produto pela barra de busca, então nome e produto pouco comuns têm menos criadores. No script, isso vira "parecidos": quantos produtos do catálogo lido têm as mesmas 3 primeiras palavras do nome.

## Exemplos positivos
- Lista 2110: os 33 com até 10 vídeos (listas/lista2110.md).
- Os ~130 produtos que o Kevin mandou em listas antes de 21/10 (afiliados/exemplos_kevin.json), todos com poucos criadores. As palavras deles entraram em afiliados/palavras.txt.

## Ajustes já feitos no script
- 21/10: até 30 vendidos, marcas e categorias lotadas no fim, bônus para até 10 vendidos e preço abaixo de R$ 1.000, 100 candidatos por dia, ids já conferidos não voltam (vistos.json).
- 22/10: pontuação por nome incomum; palavras dos exemplos do Kevin.

## Próximos aprendizados
- Vendas por dia: precisa de duas varreduras com 12 h ou mais entre elas.
- A cada lote que o Kevin conferir, comparar os vazios com os lotados e anotar aqui.
- Depois que o filtro estiver afiado: ajustar o visual e a organização do fluxo (Kevin, 22/10).

## Aprender com venda real (22/10)
- Cada vídeo leva um link com Sub ID: produto-campeao/vendas/link_subid.py. A Shopee só aceita letras e números no Sub ID.
  Formato: L0101Ap01A260101 = lista 01/01 A, produto 01, versão A (B = Shopee B, R = Reels), data AAMMDD.
- Vendas por Sub ID e por produto: produto-campeao/vendas/relatorio.py [dias]. Em 22/10 a API mostrou 0 conversões nos últimos 90 dias.
- Página de conferência: campo "Vídeos" (obrigatório) e "Afil." (afiliados, opcional, para estudo).

## Móveis (Kevin, 22/10)
- O que mais vende na conta da esposa: móveis e casa (poltrona, cadeira, armário, guarda-roupa, banqueta, mesa, lixeira, espreguiçadeira, bicicleta, decoração, cadeira de jardim, puff, cama, beliche, mesa infantil, rack, reposição de cadeira). Daí a estética Zara Home.
- São fáceis de buscar, então lotam. Estratégia: nomes de cauda longa dentro de móveis (variações e usos específicos) e deixar a pontuação de nome incomum filtrar.

## 22/10 tarde: varredura 3 (primeira com vendas por dia)
- 163.982 produtos lidos, 20.495 passaram no filtro. A varredura completa leva cerca de 1 h 45 min (a tarefa diária usa limite de 2 h).
- Nenhum dos 76 produtos não escolhidos do Tinder vendeu nas 15 h entre as duas fotos do catálogo. Produtos com poucas vendas totais vendem devagar, então "vendas por dia" só vira sinal útil com uma janela de vários dias. Até lá, o cartão continua mostrando o total vendido.
- Entraram 6 produtos novos para completar 100 esperando escolha (regra do Kevin: não acumular além disso).

## 23/10: varredura diária (aprendizado)
- 197 decisões novas desde a rodada anterior, mas 191 aprovações caíram no mesmo minuto (22/10 22:02, "Aprovar todos") e só 1 descarte (furadeira Bosch, marca famosa, já penalizada). Sem contraste entre aprovados e descartados, então nenhum peso nem palavra mudou hoje.
