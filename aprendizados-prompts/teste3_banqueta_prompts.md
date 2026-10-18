# Teste 3: Banqueta Alta com Encosto, base de ferro, courissimo

Anúncio: https://shopee.com.br/Banqueta-Alta-Com-Encosto-Para-Area-Gourmet-Banqueta-Base-De-Ferro-Em-Courissimo-Luxo-i.1281485491.58267016519

Fotos reais do anúncio em `banqueta-fotos/`:
- `A_banqueta_caramelo.png`: banqueta sozinha, cor caramelo
- `B_medidas_creme.png`: medidas (altura 93,5 cm, largura 40 cm, profundidade 42 cm), cor creme
- `C_area_gourmet.png`: mulher sentada numa área gourmet com 2 banquetas

Descrição fiel do produto (vai nos prompts):
bar stool with a square upholstered seat and a low rectangular upholstered backrest in smooth caramel-brown faux leather, a thin matte black square-tube iron frame with four straight vertical legs, and an H-shaped footrest made of two side bars joined by one center crossbar. Height 93.5 cm, seat about 40 x 42 cm. No armrests, no swivel, no wheels, no stitching patterns.

Custo no WaveSpeed: 1 edição Seedream (US$ 0,027) + 3 cenas em 480p (US$ 0,06 cada) = US$ 0,21, cerca de R$ 1,20. No máximo 2 tentativas por cena.

Ordem no vídeo (atualizada): gancho = cena do Seedream (seção "Cena 2" abaixo, com pessoa) > ambiente = foto real da área gourmet (seção "Cena 1") > CTA = foto principal (seção "Cena 3"). Na montagem, use o texto do gancho na primeira cena.

## Cena 1, gancho: foto real da área gourmet

**Seedance V1 Pro Fast Image-to-Video**, 480p, 5s, direto com `C_area_gourmet.png`:

```text
The woman sitting on the bar stool smiles and turns her head slightly toward the camera, relaxed, gentle breeze in the plants, very slow camera push-in. The bar stools stay completely still and unchanged in shape and color; the woman does not stand up.
```

Texto na tela: "A banqueta que deixou minha área gourmet com cara de restaurante"

## Cena 2, detalhe: banqueta real numa cozinha de apartamento

Passo 1, **Seedream V4 Edit**, enviando `A_banqueta_caramelo.png` e `B_medidas_creme.png`, tamanho 720x1280:

```text
Use only the bar stool from the reference images, in the caramel-brown color of the first image, keeping it exactly identical: square upholstered seat and low rectangular upholstered backrest in smooth caramel-brown faux leather, thin matte black square-tube iron frame with four straight vertical legs, H-shaped footrest with two side bars joined by one center crossbar, 93.5 cm tall. Place one of this exact stool at a white kitchen island counter in a modern Brazilian apartment, warm afternoon light, a coffee mug on the counter, photorealistic full-frame photo taken at eye level, vertical 9:16. No phone frame, no device bezel, no borders. Do not add armrests, stitching, wheels or a swivel base; do not change the frame or the footrest. No text.
```

Confira: encosto baixo e reto, assento quadrado, 4 pernas retas pretas, apoio de pés em H, cor caramelo. Se algo mudou, gere de novo uma vez.

Passo 2, **Seedance V1 Pro Fast Image-to-Video**, 480p, 5s, com a imagem do passo 1:

```text
A woman's hand slowly slides across the leather seat of the stool, steam rises from the coffee mug, handheld phone with slight natural shake. The stool stays still, rigid and identical in shape, color and frame.
```

Texto na tela: "Courissimo fácil de limpar + base de ferro firme"

## Cena 3, produto e CTA: foto real da banqueta

**Seedance V1 Pro Fast Image-to-Video**, 480p, 5s, direto com `A_banqueta_caramelo.png`:

```text
Very slow camera push-in toward the stool, soft studio light, subtle light reflection moving on the leather. The stool does not move or change shape.
```

Texto na tela: "93,5 cm, ideal para bancada. Link aqui embaixo"

## Conferência antes de usar

Pause cada cena no começo, no meio e no fim e compare com as fotos do anúncio: encosto, assento, 4 pernas, apoio de pés em H, cor. Se mudou, descarte a cena.

Observação: na foto da área gourmet o tom das banquetas é mais avermelhado que na foto principal. Use a cor da foto principal (caramelo) na cena 2 e escolha no anúncio a variação de cor que vai divulgar.
