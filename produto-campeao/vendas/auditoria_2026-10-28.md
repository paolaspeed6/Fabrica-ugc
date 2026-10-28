# Auditoria de performance Shopee (afiliada Aguiiar Lar), 28/10/2026

Fonte: API oficial Shopee Afiliados (`conversionReport`), compras de 30/07 a 27/10/2026, 1.621 pedidos e 208 produtos.
A API **não tem** visualizações, curtidas, comentários, compartilhamentos, cliques, ID do vídeo nem data de postagem.
Ela só tem pedidos, comissões, produtos, lojas, horário do clique e horário da compra.
Comissão = concluída + pendente (a API zera a comissão dos pedidos cancelados).

## 1. Resumo executivo
1. **Quase tudo vem do Shopee Vídeo:** 98,6% dos pedidos e 96,8% da comissão. Instagram e redes somam 23 pedidos e R$ 661 em 90 dias.
2. **Renda estável, sem crescimento:** cerca de R$ 230 a R$ 260 por dia há 3 meses (de R$ 1,0 mil a R$ 2,3 mil por semana).
3. **Os produtos novos quase pararam de vender:** produtos com a 1ª venda na semana caíram de 16 a 35 por semana (ago/set)
   para 3 a 13 (out). 62% da comissão de out vem de produtos que já vendiam há mais de 60 dias.
4. **A taxa do vendedor decide o dinheiro:** pedido com "Comissão extra" do vendedor (SELLER_OPEN_CAMPAIGN) paga R$ 24,93,
   e o pedido sem ela paga R$ 5,28. Os produtos sem taxa extra são 36% dos pedidos e só 11% da comissão.
5. **27% dos pedidos são cancelados** (437 pedidos, R$ 156 mil em produtos). Bicicleta é o pior caso: 37% no geral,
   77% na Cripto Aro 29 e 67% na GTS Aro 29. Na faixa de R$ 800 a R$ 1.500 o cancelamento chega a 48%.

## 2. Painel de indicadores
| Período | Pedidos | Cancelados | Comissão (concl. + pend.) | R$/dia | Produtos com venda | vs. período anterior |
|---|---|---|---|---|---|---|
| 7 dias | 149 | 28% | R$ 1.838 | 263 | 54 | +27% (R$ 1.451) |
| 14 dias | 269 | 24% | R$ 3.289 | 235 | 71 | −20% (R$ 4.096) |
| 30 dias | 611 | 27% | R$ 7.851 | 262 | 114 | +10% (R$ 7.160; 129 produtos) |
| 60 dias | 1.209 | 27% | R$ 15.011 | 250 | 170 | — |
| 90 dias | 1.621 | 27% | R$ 20.940 | 233 | 208 | — |

Em 90 dias foram R$ 373 mil em vendas válidas, com comissão média de 5,6%. Comissão concluída: R$ 17.979. Pendente: R$ 2.961.
Os pendentes são quase todos dos últimos 30 dias e ainda podem cancelar. 99% dos compradores já eram clientes Shopee.

## 3. Evolução (proxy: pedidos e comissão por semana; a API não tem visualizações)
Comissão por semana: ago entre R$ 1,0 mil e R$ 1,8 mil, set entre R$ 1,7 mil e R$ 2,2 mil, out entre R$ 1,6 mil e R$ 2,3 mil.
O melhor pico foi a semana de 05/10 (173 pedidos, R$ 2.296). O platô veio em setembro.
Produtos com a 1ª venda, por semana: 35 · 19 · 19 · 21 · 9 · 17 · 16 · 17 · 9 · 13 · **3 · 7** · 3 (semana parcial).
Hipótese, sem prova: em outubro entraram menos vídeos novos com produto vendável, ou os vídeos novos não converteram.
Para confirmar, seria preciso a lista de vídeos postados com data.

## 4. Vendas e comissões: o que gera dinheiro
- **Faixa de preço:** de R$ 100 a R$ 400 fica o volume (1.070 pedidos, R$ 11,2 mil, 54%).
  De R$ 400 a R$ 1.500 fica o valor por pedido (R$ 29 a R$ 68), mas com mais cancelamento. Abaixo de R$ 100 quase não paga (R$ 1,50 a R$ 3,83 por pedido).
- **Taxa do vendedor:** de 10% a 20% paga R$ 70 por pedido válido. A taxa 0% paga R$ 5. O mesmo esforço de vídeo rende até 13 vezes mais.
- **Categoria:** cadeira R$ 5,3 mil, bicicleta R$ 4,2 mil (R$ 42 por pedido, mas 37% de cancelamento),
  banqueta/banco R$ 3,3 mil (R$ 13 por pedido), mesa R$ 1,1 mil.
- **Compra por impulso:** 70% compram em menos de 1 hora depois do clique e 85% em menos de 24 h. Só 6% passam de 3 dias.
  O dinheiro vem da hora em que o vídeo é assistido, não de cookie longo.
- **Horário da compra (Brasília):** de 9h às 24h, com pico das 12h às 18h. Os dias da semana são parecidos (sem dia campeão).
  Isso é horário de compra, não de postagem.
- 153 lojas, sem dependência de uma só. A maior (WJ Móveis) tem 13%.

## 5. Ranking (90 dias)
Os 10 produtos do topo fazem 40% da comissão, e os 50 do topo fazem 79%. 76 produtos (37%) venderam só 1 vez e somam R$ 1.405.

| # | Produto | Preço | Pedidos | Cancel. | Comissão | Taxa vend. |
|---|---|---|---|---|---|---|
| 1 | Banqueta balcão/churrasco | 159 | 221 | 32% | R$ 2.595 | 10% |
| 2 | Bicicleta Aro 29 Ksw 24v hidráulico | 1.108 | 11 | 27% | R$ 1.112 | 12% |
| 3 | Jogo 4 Banquetas Katrina 85 cm | 380 | 57 | 26% | R$ 822 | 4% |
| 4 | Banqueta Country c/ encosto 70 cm | 150 | 80 | 34% | R$ 695 | 4% |
| 5 | Bicicleta Aro 29 Cripto 21v | 839 | 26 | **77%** | R$ 603 | 11% |
| 6 | Kit 2 Cadeiras Lunna linho | 777 | 15 | 20% | R$ 581 | 5% |
| 7 | Lixeira 12 L rosê/dourada inox | 261 | 37 | **3%** | R$ 580 | 6% |
| 8 | Kit 2 Cadeiras madeira maciça linho | 950 | 7 | 43% | R$ 479 | 10%+3% |
| 9 | Conjunto 4 Cadeiras madeira maciça | 799 | 13 | 15% | R$ 435 | 4% |
| 10 | Bicicleta infantil Aro 20 BMX | 649 | 15 | 13% | R$ 417 | 0% |

- **Vencedores para repetir:** a Banqueta nº 1 vendeu em 59 dos 88 dias e ainda faz de R$ 250 a R$ 300 por semana em outubro.
  Lixeira (3% de cancelamento) e Banco Namoradeira (75 pedidos, 8% de cancelamento) são estáveis.
- **Oportunidades:** produtos com taxa de 10% ou mais e poucos pedidos (Poltrona Presidente com 4 pedidos e R$ 275,
  Estante Livreiro, Mesa Sensorial Montessori com 15%). Eles merecem um 2º vídeo.
- **Atenção:** Bicicleta Cripto e GTS (cancelam mais do que entregam) e a Namoradeira (75 pedidos com taxa do vendedor 0%,
  só R$ 4 por pedido). Na Namoradeira vale procurar o mesmo item numa loja com comissão extra.

## 6. Gargalos
Confirmados pelos dados:
- O catálogo está envelhecendo, porque a entrada de produtos novos que vendem caiu em outubro.
- 36% dos pedidos estão em produtos sem comissão extra.
- O cancelamento de 27% é alto em bicicleta e na faixa de R$ 800 a R$ 1.500.
- **Não há Sub ID:** em 90 dias, nenhum pedido veio com Sub ID (`utmContent` vazio). Por isso não dá para saber qual vídeo vendeu.

Hipóteses (precisam de dado que a API não dá):
- Os vídeos novos têm menos visualização (falta o painel do Shopee Vídeo).
- O cancelamento da bicicleta pode vir de frete, prazo ou loja.

## 7. Plano de 30 dias (em ordem)
1. **Filtro de taxa no Tinder:** só aceitar produto com comissão extra do vendedor (`sellerCommCoveRatio` / taxa de 7% ou mais).
   Para os campeões com 0%, procurar a mesma peça numa loja com taxa.
2. **Repetir o vencedor:** de 2 a 3 vídeos novos por semana dos campeões ativos (Banqueta nº 1, Katrina, Country, Lixeira, cadeiras de linho),
   com ganchos diferentes.
3. **Volume de produto novo:** voltar a ter de 15 a 20 produtos novos testados por semana, que era o ritmo de ago/set, na faixa de R$ 150 a R$ 800.
4. **Cortar o que cancela:** pausar Bicicleta Cripto e GTS. Antes de um vídeo de produto acima de R$ 800, olhar a nota da loja e o prazo.
5. **Medir por vídeo:** toda semana, exportar do app (Central de Afiliados > Shopee Vídeo) as visualizações e os cliques por vídeo,
   e salvar o arquivo aqui. Assim dá para cruzar visualização, clique e venda.
6. Rodar esta auditoria a cada 7 dias (`auditoria_puxar.py`, grátis) e comparar com esta.

---
## Atualização: painel do app Shopee Vídeo (prints de 28/10, dados até 26/10)
Dados salvos em `painel_app_2026-10-26.json`. Bate com a API: 30 dias = 604 pedidos no app e 611 na API.
O valor de "Vendas" do app inclui pedidos cancelados (R$ 218 mil, contra R$ 147 mil válidos na API).

**Funil (30 dias):** cerca de 250 mil visualizações (estimativa: 4 × 62,7 mil), depois 44,3 mil cliques (cerca de 18% de quem vê clica, número muito bom),
depois 604 pedidos (**1,4% de quem clica compra**), e por fim 27% de cancelamento.
O gargalo não é atenção nem clique: é o produto, o preço e a loja depois do clique.

**Descobertas novas**
1. **Os vídeos novos quase não são vistos.** Em 15 dias entraram cerca de 194 vídeos (eram 57 nos 15 dias anteriores), mas o melhor deles teve 496 visualizações
   e a maioria ficou entre 120 e 280. As cerca de 64 mil visualizações por semana vêm dos vídeos antigos:
   a Banqueta (postada em 24/06) trouxe sozinha +7,3 mil espectadores na semana, e a Mesa 8 lugares (28/05) trouxe +R$ 1,2 mil de GMV.
   Explica por que "produtos com 1ª venda" caiu em outubro: **o volume de postagem subiu, mas o alcance de cada vídeo novo é perto de zero.**
2. **O público é mulher (72%) e tem 45 anos ou mais (61%).** Vários vídeos novos fogem desse público: inversor de camping, DVR de câmeras,
   adaptador de furadeira para motosserra e caixa de som. Casa, cozinha e móveis conversam com quem já assiste.
3. **Compartilhar é a reação principal:** 816 compartilhamentos contra 249 curtidas e 15 comentários. Ela manda o vídeo para alguém (marido ou filha)
   antes de comprar. Ganchos que pedem isso ("mostra pra quem vai montar com você") têm base nos dados.
4. **Horário:** a audiência tem pico às 21h, depois às 12h e às 18h, e um vale entre 3h e 6h.
   Vários vídeos novos foram postados entre 1h55 e 2h57, ou seja, no vale. Hipótese: isso piora o empurrão inicial. O efeito não está provado.
5. **Foz do Iguaçu com 19,6% das visualizações** é fora do normal para o tamanho da cidade (SP tem 19,9%).
   Hipóteses: visualizações da própria conta ou de aparelhos da casa, ou público de fronteira. Vale conferir; se for visualização própria, os números reais são cerca de 20% menores.
6. **A última semana caiu:** de 20 a 26/10 foram 124 pedidos (−44) e R$ 41 mil (−R$ 24,9 mil), com cliques estáveis (−2%).
   A queda está na conversão (de 0,3% para 0,2%), não no alcance. Isso combina com o fato de que os vídeos com receita caíram de 66 para 50.

**Plano de 30 dias revisado (substitui a seção 7)**
1. **Menos vídeos e mais certeiros:** parar a enxurrada (cerca de 13 por dia). Postar de 3 a 5 por dia, só de casa, cozinha e móveis,
   com comissão extra de 7% ou mais, na faixa de R$ 150 a R$ 800.
2. **Reaproveitar os campeões:** fazer variações dos vídeos da Banqueta, da Mesa 8 lugares e da Namoradeira (mesmo produto, novo gancho, nova capa),
   e procurar produtos "irmãos" (banquetas, mesas e bancos de madeira em lojas com taxa).
3. **Postar no pico:** entre 11h e 12h e entre 18h e 21h. Testar 2 semanas e comparar a visualização média dos vídeos novos (meta: passar de 500).
4. **Cortar o fora do público:** eletrônico, ferramenta e camping saem, a não ser que um teste prove o contrário.
5. **Cortar o que cancela:** bicicletas Cripto e GTS.
6. **Medir toda semana:** mandar os mesmos prints (Vendas 7 dias + lista de vídeos novos). Eu comparo com este arquivo.
