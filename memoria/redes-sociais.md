# Redes sociais (TikTok e Instagram): linha própria, separada da Shopee Vídeo (a dona, 13/11/2026)

## Por quê
- Repostar o vídeo da Shopee nas redes não funciona: TikTok @aguiiar_lar 86 vídeos, 60 seguidores, ~8 curtidas/vídeo;
  Instagram @_aguiiar_lar 82 posts em 3 semanas (6 por dia automáticos), 8 seguidores, 2 curtidas no total.
- Referências que ela mandou (TikTok, carrossel de fotos, contas pequenas de 197 a 17,9 mil seguidores com 94 mil a 1,6 milhão de views):
  "Troque isso… / Por isso!" (item comum x versão fofa da Shopee, em pares), "favs do enxoval versão cozinha", Natal.
  Mesmo cenário em todas as fotos, texto minúsculo pequeno, música brasileira conhecida escolhida no app,
  última foto com CTA "grupo/link na bio" ou "comenta que eu envio".

## Identidade visual da casa Aguiiar Lar (regra da dona)
- Estilo ROMÂNTICO e SOFISTICADO, com FLORES, coisas ROSAS, estilo casa AMERICANA, base BRANCA com MADEIRA e PLANTAS. Manter sempre.
- No Natal: o mesmo estilo romântico com vermelho, xadrez, laços, dourado, fofo.
- Itens bonitos e fofos (o que viraliza).

## O que ela quer
1. Aba "REDES SOCIAIS" no topo da página do Tinder.
2. Varredura própria só para carrossel: produtos estratégicos, bonitos, com boa comissão; agora Natal.
   Script: produto-campeao/redes/varrer_carrossel.py (palavras_natal.txt, palavras_romantico.txt; nota de beleza pelo Gemini, grátis).
3. Vídeos com vários produtos: usam os NOSSOS vídeos já feitos, escolhendo os produtos mais estratégicos.
4. Instagram automático pode postar carrossel; TikTok ela posta no app (música em alta só pelo app).

## Letra das capas (a dona escolheu em 13/11)
- Estilo 1 "Elegante": branco com sombra suave; linha pequena em Cormorant Garamond itálico, linha principal em Cormorant
  Garamond 600 MAIÚSCULA grande, fecho em Great Vibes cursiva (ex.: "Parece de / LOJA CARA, / mas é da Shopee").
  Assinatura "aguiiar lar" pequena embaixo. Modelo: produto-campeao/redes/capas/teste.html (#c1). Fontes em video-teste/fontes/redes/.

## Referência de casa que ela mandou (13/11): "esse é o estilo de casa que eu gosto"
Cozinha americana clássica: armários brancos ou off-white estilo shaker com puxadores pretos ou dourados, armários de vidro,
bancada de MADEIRA (butcher block) ou mármore branco, azulejo metrô branco, flores rosa (tulipas, peônias, rosas) em vaso branco,
tapete xadrez bege ou floral rosa, cesta de vime, banquinho de madeira, chaleira esmaltada branca, tábuas de madeira, luz quente e suave.
Cenários e imagens do carrossel seguem isso.

## Cenário fixo (a dona escolheu em 13/11)
- E_cozinha_branca (produto-campeao/redes/cenarios/E_cozinha_branca.jpg): cozinha branca romântica, bancada de mármore branco,
  vaso branco com peônias rosa, armários creme com puxador dourado, janela em arco, lustre de cristal, tapete floral rosa.
  Toda foto de produto do carrossel nasce desse cenário (mesma bancada, mesma luz).

## Filtro estratégico da varredura de carrossel (a dona, 13/11)
"Quero produtos estratégicos, com bons preços e benefícios; um papai noel de 300 reais é inviável."
- Preço R$ 15 a R$ 90 (pontua mais até R$ 50), nota ≥ 4,7, 50+ vendidos, comissão ≥ 10% e ≥ R$ 2.
- Gemini recebe o preço e dá "vale_o_preco" (≥ 7 para entrar) e o "benefício" que vende; tira o que não é de casa
  (folheto, embalagem, caixa de doces, lembrancinha).

## Filtro estratégico da varredura de carrossel (a dona, 13/11)
"Quero produtos estratégicos, com bons preços e benefícios; um papai noel de 300 reais é inviável."
- Preço R$ 30 a R$ 150 (pontua mais até R$ 80), nota >= 4,7, 50+ vendidos, comissão >= 10% e NO MÍNIMO R$ 10 por venda (a dona, 13/11).
- Gemini recebe o preço e dá "vale_o_preco" (>= 7 para entrar) e o "benefício" que vende; tira o que não é de casa
  (folheto, embalagem, caixa de doces, lembrancinha).

## Aba "🎬 Montar vídeo" (Tinder > REDES SOCIAIS, 13/11)
- A dona: "quero criar com os vídeos já criados, ganchos estratégicos, produtos bons" + "uma aba onde eu possa escolher os vídeos".
- Coleção `videos` (Tinder): 1 doc por produto já aprovado na Conferir (id = id da Conferir, ex. 1211A-03), com poster, drive_urls A/B/C,
  links, tema e charme (Gemini), preço/comissão quando conhecidos. Gerado por `produto-campeao/redes/montar_videos_docs.py`.
- Ela toca 3 a 5 vídeos (ordem do toque = ordem no vídeo), escolhe gancho e voz (voz bonita / minha voz / só música) e pede.
  O pedido vai para a coleção `montagens` {videos, produtos, gancho, voz, status: pedido|montando|conferir}.
- Montagem: grátis (edição). Trechos dos vídeos já prontos + gancho com as letras do estilo 1 + CTA "comenta EU QUERO". Sempre para a Conferir.
- A dona (13/11): quer narrar os vídeos ou usar "uma voz bem bonita".

## Filtro "casa das paty" (13/11, 3ª conversa de estilo)
- A dona: "está tendo muitas xícaras que não têm nada a ver; gosto de coisas lindas e irresistíveis, quero uma casa bem das paty".
- Fotos dela em `produto-campeao/redes/referencias_paty/` (armário branco com louça rosa e caneca de bolinhas, escada de madeira
  com toalhas rosa e cesto de palha, estante clara com caixas rosa, potes xadrez rosa com dourado, copo fosco de gatinho).
- `varrer_carrossel.py --refs referencias_paty --max-tipo 2`: o Gemini vê as referências, dá "parece_refs" (precisa >= 7) e o "tipo";
  no máximo 2 do mesmo tipo (chega de 10 xícaras). Palavras em `palavras_paty.txt`. Varreduras pequenas (20) até achar o filtro certo.
- Móveis no mesmo estilo (a dona, 13/11): penteadeira, banquetas, racks… `palavras_paty_moveis.txt`, `--preco-max 600` (comissão ≥ R$ 10 continua).
- A dona (13/11): "pode" R$ 5 de comissão mínima para OBJETOS (móveis seguem R$ 10). Ganchos escolhidos por ela estão na aba (tinder.html GANCHOS).
- A dona (13/11): quer TUDO para casa no estilo paty (cozinha, panelas, pratos, banheiro, quarto, sala) para fazer "achadinhos que mudaram meu banheiro/quarto/sala". `palavras_paty_casa.txt`; fila em `fila_paty.sh`.
