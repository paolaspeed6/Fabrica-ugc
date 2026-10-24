# Estética "vídeos da esposa" (Veo 3) — prompts universais

Estudo de 2026-10-18 sobre 7 vídeos enviados pelo Kevin (2 finais 1080x1920 24 fps da esposa: cadeira de corda e poltrona capitonê; 5 de 720x1280 30 fps: bancada preta, bancada branca, mesinha infantil). Todos já vinham com texto; nenhuma geração crua chegou ainda.

## O que faz parecer real
- Luz: só luz do dia difusa de janela fora do quadro, céu meio nublado, sombra de contato suave, cantos mais escuros. Sem rim light, sem softbox, sem brilho de IA.
- Cor: paleta quente-neutra e um pouco apagada (creme, verde sálvia, terracota, carvalho). Balanço de branco neutro.
- Cenário: casas clássicas europeias bem cuidadas: boiserie (molduras na parede), parquet espinha de peixe, ladrilho hidráulico estampado, piso de terracota, travertino, arcos de cal com oliveiras. Poucos objetos, todos de textura real (vime, linho, cerâmica, plantas).
- Câmera: lente grande-angular de celular (~26 mm), na altura do produto, quase todo o quadro em foco (sem bokeh de lente 85 mm). Plano contínuo, aproximação lenta até o detalhe do material, balanço leve de mão.
- Estrutura: o mesmo produto em 2-3 cômodos diferentes, um cômodo por cena.
- Edição (só nos 2 finais dela): história "um dia inteiro com ela" com horários 08:00 / 15:00 / 22:00, tipografia serifada fina, sem faixas.

## Onde está a diferença para o nosso padrão
- produtor.md manda "commercial product cinematography", "golden hour backlight with rim light", "softbox key light", "85 mm creamy bokeh", "high dynamic range". Isso é exatamente a cara de catálogo/IA que ela evita.
- A estética vem quase toda da IMAGEM, não do modelo de vídeo.
- Veo 3 dá movimento de mão mais natural e 24 fps; Seedance 1.5 Fast é bem mais barato. Não testado lado a lado.

## Prompt de imagem (Seedream v4 Edit ou Nano Banana; referência = foto 01 do anúncio)
Trocar {CENARIO} por um dos cenários abaixo; um cenário por cena.

```
Use the product from the reference image exactly as it is: same shape, proportions, colors, materials, texture, number of parts and every detail; any lettering reads left to right, never mirrored. The product is brand new and spotless, resting naturally the way it is really used, centered and fully visible, filling about half of the frame height.
Setting: {CENARIO}
Photorealistic full-frame vertical 9:16 photo taken by a person with a recent smartphone main camera: 26 mm wide lens, held slightly below eye level at the product's height, everything from the product to the back wall in natural focus.
Lighting comes only from soft, diffuse daylight through a large window out of frame on one side, a slightly overcast day, gentle natural falloff across the room, soft real contact shadows under the product and slightly darker corners.
True-to-life, slightly muted warm-neutral colors with neutral white balance; the product's color matches the reference exactly.
Real textures everywhere: wood grain, fabric weave, tile grout, lime-plaster walls, small natural imperfections of an old, well-kept house.
The room is clean, tidy and calm, minimalist, only the objects described, a few classic decor pieces softly placed in the background.
Natural phone-camera rendering: fine sensor grain, mild vignetting, highlights near the window, realistic dynamic range.
It looks like a candid photo a customer with good taste took at home and posted, premium UGC, not a catalog shot and not a studio render.
No phone frame, no device bezel, no borders, no text.
```

### Cenários (escolher pelo produto)
1. `a classic Parisian living room with cream wall panels and boiserie moulding, light oak herringbone parquet floor, sheer linen curtains, a small potted olive tree`
2. `a classic room with sage green wall panels and moulding, a patterned encaustic cement tile floor in cream, terracotta and charcoal, a brass wall sconce, a woven wicker basket`
3. `a Mediterranean veranda with white lime-plaster arches, a worn terracotta tile floor, potted plants and olive trees in the garden outside`
4. `a quiet reading corner with a pale travertine stone floor, built-in wooden bookshelves holding only books and ceramics, tall window with linen curtains`
5. Banheiro: `a classic bathroom with sage green wall panels and moulding, patterned encaustic cement tile floor, a brass oval mirror and wall sconce, folded white towels`
6. Cozinha: `a classic kitchen with a white marble countertop, cream wooden cabinets with brass handles, a terracotta tile floor, a linen cloth and a small herb pot`

## Prompt de animação — Veo 3 (base da esposa, reforçado)
```
A POV UGC-style video filmed handheld on a smartphone, one continuous shot with no cuts and no transitions. The camera slowly walks toward the {PRODUTO} with a gentle, natural handheld sway, then glides closer to show the texture and finish of its {DETALHE}. The {PRODUTO} stays completely still in its place and keeps its exact shape, colors and every detail. The room stays calm and empty, nobody in frame, the soft window daylight stays constant. Quiet ambient room sound only.
```

## Prompt de animação — Seedance 1.5 Pro Fast (produzir.py já acrescenta a trava de ângulo)
```
Handheld smartphone POV video, one continuous shot. The camera slowly pushes in toward the {PRODUTO} with subtle natural hand shake and a small 15-degree arc to one side, ending on a close view of the texture of its {DETALHE}. The {PRODUTO} stays perfectly still with the same shape, colors and details as the first frame. The soft daylight from the window stays constant. Realistic phone footage with natural motion blur.
```

## Não confirmado
- Gerações cruas: ainda não chegaram; todos os 7 vídeos têm texto.
- Qual modelo de imagem ela usa e se o áudio do Veo fica no vídeo final.
- Se o Seedance chega no mesmo visual: precisa de teste de 1 cena (imagem US$ 0,027 + clipe US$ 0,10).
- Num vídeo de bancada branca aparece uma mão entrando no quadro, mesmo com "no hands": falha do próprio Veo, checar frames.
