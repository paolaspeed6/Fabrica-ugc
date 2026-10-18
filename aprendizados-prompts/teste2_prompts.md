# Teste 2: Escova de Limpeza Elétrica 5 em 1 (fiel ao anúncio)

Anúncio: https://shopee.com.br/Escova-de-Limpeza-El%C3%A9trica-Lava-Lou%C3%A7as-5-em-1-Kit-Completo-Recarreg%C3%A1vel-Usb-Cozinha-Banheiro-Sapatos-i.1524383764.58220091550

Regra: nenhuma imagem cria o produto do zero. Toda cena parte das fotos reais do anúncio, que estão em `escova-fotos/`:

- `A_kit_completo.png`: escova + 5 cabeças + cabo USB (foto principal)
- `B_medidas.png`: escova com medidas (173 x 235 mm)
- `C1_fogao_esponja.png`: em uso, esponja amarela no cooktop (recortada da foto "Multi Funções")
- `C2_pia_escova.png`: em uso, cerdas brancas na pia
- `C3_vidro.png` e `C4_sofa.png`: outros usos, para variações

Descrição fiel do produto (vai em todos os prompts):
white handheld electric spin scrubber shaped like an L: a vertical white cylindrical handle with one round gray power button with a power symbol on the front and a ribbed white ring at the bottom; on top, a horizontal white cylindrical motor head with a ribbed light-gray ring at the back; a round white bristle brush head attached at the front.

Custo no WaveSpeed: 1 edição Seedream (US$ 0,027) + 3 cenas em 480p (US$ 0,06 cada) = US$ 0,21, cerca de R$ 1,20. No máximo 2 tentativas por cena.

## Cena 1, hook: pessoa segurando o produto real

Passo 1, **Seedream V4 Edit**, enviando `A_kit_completo.png`, `B_medidas.png` e `C2_pia_escova.png`, tamanho 720x1280:

```text
Use only the electric cleaning brush from the reference images, keeping it exactly identical: a white handheld electric spin scrubber shaped like an L, vertical white cylindrical handle with one round gray power button with a power symbol on the front and a ribbed white ring at the bottom, a horizontal white cylindrical motor head with a ribbed light-gray ring at the back, and a round white bristle brush head at the front. Proportions as in the reference: about 17 cm wide and 23 cm tall, fits in one hand. A Brazilian woman around 30, casual t-shirt, holds this exact brush by the handle in her right hand next to her face, smiling, in a simple home kitchen beside a sink with dirty pans. Photorealistic full-frame photo, natural window light, vertical 9:16. No phone frame, no device bezel, no borders. Do not redesign, recolor, add or remove any part of the product. No text, no logos added.
```

Confira: formato em L, botão cinza redondo, anel cinza atrás da cabeça, cerdas brancas, tamanho de uma mão. Se algo mudou, gere de novo uma vez.

Passo 2, **Seedance V1 Pro Fast Image-to-Video**, 480p, 5s, com a imagem do passo 1:

```text
She lifts the brush slightly toward the camera and smiles, very small movement, handheld phone with slight shake. The brush stays rigid and keeps exactly the same shape, color and button the whole time; it does not rotate or deform.
```

Texto na tela: "Lavar louça nunca foi tão fácil"

## Cena 2, demonstração na pia: foto real

**Seedance V1 Pro Fast Image-to-Video**, 480p, 5s, direto com `C2_pia_escova.png`:

```text
The white bristle brush head spins fast and scrubs the sink surface with a little soap foam, the hand holds it steady, slow subtle camera push-in. The device body stays rigid and unchanged; only the bristle head rotates.
```

Texto na tela: "Gira sozinha e tira a sujeira pesada"

## Cena 3, outra função: foto real no cooktop

**Seedance V1 Pro Fast Image-to-Video**, 480p, 5s, direto com `C1_fogao_esponja.png`:

```text
The yellow sponge head spins and polishes the black glass cooktop, soap foam spreading, the hand holds it steady, slow subtle camera push-in. The device body stays rigid and unchanged; only the sponge head rotates.
```

Texto na tela: "5 cabeças: louça, fogão, vidro, sofá. Link aqui embaixo"

## Conferência antes de usar

Pause cada cena no começo, no meio e no fim e compare com as fotos do anúncio: formato em L, cor, botão, anel cinza e tipo de cabeça. Se mudou, descarte a cena.
