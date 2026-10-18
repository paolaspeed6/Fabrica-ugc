# Manual do Vídeo Vencedor (TikTok Shop Brasil)
Versão 1, 2026-10-17. Fonte: FastMoss, os 30 vídeos que mais venderam de 17/09 a 16/10/2026 (10 em Casa/Cozinha, 10 em Tecnologia, 10 em Pet), e as 3 conclusões parciais do Kalodata (KaloPilot analisou os mesmos 30 roteiros, mas o relatório não chegou porque os créditos acabaram). Ler junto com `principios.md`, `regras_de_erros.md` e `analista.md`. Isto é "sinal", não "regra" (Annie Duke): 30 vídeos, 1 mês, sem os nossos números ainda.

## O que os números mostram
| Fato | Dado | O que fazemos |
|---|---|---|
| Produto barato, compra por impulso | preço mediano R$ 20; o mais caro, R$ 69 | No TikTok Shop priorizar R$ 10-40. Nossa faixa da Shopee (R$ 30-150) é cara para o TikTok |
| Conta pequena vende | 15 de 30 vídeos vêm de perfis com menos de 50 mil seguidores; perfis de 8 mil venderam 771 e 828 unidades | Conta nova pode vender desde o início |
| Volume de versões do mesmo produto | o fone para dormir Monster aparece 5 vezes no top 10; um único perfil postou 4 versões com o mesmo gancho | Confirma as 4 versões por produto; um produto que vende merece mais versões, não troca de produto |
| Quase todos são impulsionados | 23 de 30 marcados como anúncio (Spark Ads / GMV Max) | Separar o que é criativo do que é verba: comparar pedidos por mil views dentro do mesmo produto |
| Duração | mediana 36 s; 12 de 30 têm até 30 s; a garrafa térmica com 9 s vendeu 1.014 | 15 s continua certo; testar uma versão de 9-10 s |
| Conversão varia muito | de 0,1 a 28 pedidos por mil views | Viral não é venda: os vídeos com milhões de views converteram pior (0,1-0,3/mil) do que os de nicho (8-28/mil) |

## Kalodata (só as conclusões que chegaram)
1. Orgânico converteu cerca de 2× mais que anúncio pago.
2. Vídeo só com as mãos vendeu mais que vídeo com rosto. Rosto não é regra: a dona pode testar no TikTok.
3. O 2º vídeo que mais vendeu tinha 9 s.

## Ganchos que se repetem (legendas dos vencedores)
- **Pergunta da dor do dono** (Schwartz, consciente do problema): "Seu gato ama morder tudo pela casa?", "Seu cão se assusta com fogos?"
- **Comparação** (lacuna de curiosidade, Heath): "Qual é melhor?", "Qual o melhor carregador?". Foram 5 vídeos no top 10 de Tecnologia.
- **Risco escondido / autoridade** (Cialdini): "Muita gente usa, mas poucos sabem os riscos", de uma veterinária, sobre plástico contra inox.
- **Identidade / moeda social** (Berger): "A garrafa térmica das paty girls".
- **Rotina real** (história, StoryBrand): "Rotina real de casa".
- **Humor que se compartilha** (Contágio): fantasia Chucky para pet, 62 mil compartilhamentos.
- **CTA nativo:** "toque no carrinho laranja". Nenhum vencedor promete prazo de entrega.

## Como aplicar na fábrica
1. A versão Reels/TikTok abre com a pergunta da dor ou com a comparação, e nunca com "achadinho".
2. Testar uma versão de 9-10 s por produto (só o take 1 + CTA).
3. A prova vem na tela: número do anúncio, avaliações ou comparação lado a lado.
4. O produto continua parado e só a câmera se move, em 100% dos vídeos (regra da dona). Os vencedores com mãos mostram o produto em uso; aqui isso vira close de câmera, sem mão nem movimento do produto.
5. Nichos fortes agora: fone para dormir, garrafa térmica com canudo, utensílios de cozinha até R$ 20, cuidados pet (unha, brinquedo de gato, protetor de ouvido).

## Versão de oferta "fundo de funil" (do prompt "Máquina de 12 s", a dona 2026-10-17)
1. **Uma das versões por produto é de oferta:** fala com quem já quer comprar e leva uma headline de urgência por cima (OFERTA RELÂMPAGO NO CARRINHO LARANJA, CUPOM ATIVO HOJE, FRETE GRÁTIS, 2 PELO PREÇO DE 1, ÚLTIMAS UNIDADES). Só entra quando o anúncio mostra o fato no dia (cupom, frete grátis, leve 2, estoque baixo). Vale a regra 3.6, e o `checar_textos.py` confere.
2. **Proibido porcentagem e o símbolo %** no vídeo, na headline e na legenda. No TikTok Shop isso pode ser lido como alegação de desconto enganosa.
3. **Take "uso satisfatório":** vira uma categoria fixa de cena quando o anúncio tem foto real do produto em uso. É sempre sem rosto, mãos só com OK da dona, e o produto fica parado: só a câmera se move sobre a foto.
4. **Pacote por produto:** 5 headlines alternativas mais 1 legenda de oferta com 5 hashtags do nicho, para o teste A/B. Nenhuma cita outra marca.
5. **O que não entra, porque contraria regras aprovadas:** a câmera orbitando (slow orbit), o produto gerado no Veo, a montagem manual no CapCut e takes de 10 s. O formato continua 15 s em 3 cenas de 5 s, com a versão curta de 9-10 s em teste.

## Limites desta versão
- O `video_script_info` do FastMoss voltou vazio para os 6 vídeos BR testados, então gancho falado, cortes e câmera não foram medidos; os ganchos acima vêm das legendas.
- Falta a consulta 2 do Kalodata (produtos em alta com poucos criadores, ângulos que ninguém usa, objeções das avaliações), que depende de mais créditos.
