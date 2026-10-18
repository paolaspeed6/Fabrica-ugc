# Pesquisa: realismo da Luana com ~US$ 2 (2026-10-17, nada gerado)

## 1. Preços WaveSpeed (GET /api/v3/models; saldo 5,26)
base_price = config padrão, sem unidade. ? = não confirmado.

| Modelo (imagem) | base | Obs. |
|---|---|---|
| seedream-v4 / v4/edit | 0,027/img | medido; ByteDance, biquíni ok |
| seedream-v5.0-lite (/edit) | 0,035/img | pele/rosto melhor que 4.5 |
| seedream-v4.5 /edit | 0,04/img | até 14 refs, forte em consistência |
| qwen-image/edit-2511, flux-kontext-dev | 0,02-0,025 | realismo médio, pele lisa |
| nano-banana-2.1 /edit | 0,036-0,038 | medido; filtra biquíni às vezes |
| nano-banana-pro | 0,126-0,14 | melhor pele; caro, filtra |
| pruna p-image / edit | 0,005 / 0,01 | rascunho |

| Modelo (imagem->vídeo) | base | Unidade |
|---|---|---|
| seedance-v1.5-pro/i2v-fast | 0,20 | medido 0,10/5 s 720p sem áudio |
| seedance-v1.5-pro/i2v | 0,26 | 5 s 720p com áudio (0,13 sem) |
| wan-2.6/i2v-flash | 0,125 | ? 5 s 720p c/ áudio |
| hailuo-02/fast ; 2.3/fast | 0,10 ; 0,19 | por clipe 6 s (512p ; 768p) |
| kling-v2.5-turbo-std / v2.6-std | 0,21 | ? provável por 5 s |
| kling-v3-turbo-std | 0,112 | POR SEGUNDO (0,56/5 s) |
| minimax-h3 (open) | 0,20 | ? por segundo |
| pruna p-video / p-video-2 | 0,02 / 0,025 | ? por segundo |
| veo3.1-lite / fast | 0,05/s / 0,15/s | medido; filtra biquíni |

Política: Google (Nano Banana, Veo) bloqueia em parte moda praia desde jan/2026. Kling é PG-13; contexto amplo (rio, canoa, plano médio) passa melhor. Seedance: sem regra oficial, tolerante. Evitar close de corpo.

## 2. Grátis: demo.pruna.ai (acessível)
- `/handler` (p, img, a=9:16, g=p-image|z-image-turbo|flux-2-klein-4b) : o reescritor deixa a câmera parada.
- Melhor: `/generate_both_for_slider` com **p-image-photos-realism-lora** (0,5-0,8).
- `/generate_next_scene` = p-image-edit (rosto); `/regenerate_video_only` aceita `camera_movement` (pan, dolly...). Tremor na pós.
- Avaliação: com o LoRA, o p-image chega a foto de Instagram, mas a pele fica lisa e o rosto oscila. Serve para rascunho e fallback, não para close.

## 3. Técnicas de realismo
- **Prompt:** "shot on iPhone 15, 24mm, candid, handheld", poros visíveis, sardas, pele oleosa ou molhada, fios soltos (flyaway), assimetria, sombras irregulares, leve ruído digital, realces um pouco estourados. Evitar "flawless, glass skin, studio, cinematic bokeh, 8k".
- **Consistência:** herói, depois folha ref (frente, 3/4, perfil) em edit-sequential. Toda cena é edit da ref ("same woman, same face") e o vídeo é sempre i2v do quadro-chave.
- **Movimento:** 1 ação física por clipe, microgestos (piscar, respirar, cabelo), 4-5 s, sem slow motion, "handheld phone, slight sway". Mãos e água deformam: cortar antes.
- **Pós (ffmpeg, grátis):** 30 fps, grão 2-3% (`noise=alls=6:allf=t`), menos nitidez, `lenscorrection` leve, tremor (crop + seno), uma gradação, H.264 8 Mbps.

**Prompts prontos**
1. Herói: `Candid iPhone photo, 24mm, of a 25-year-old Brazilian riverside fisherwoman standing in a wooden canoe on an Amazon river at golden sunset, tanned skin with visible pores, faint freckles, light sweat sheen, dark wavy hair with flyaway strands, red bikini top, short frayed denim shorts, relaxed smile, uneven warm side light, blown highlights on water, mild noise, medium shot, not posed`
2. Por cima do ombro (edit com ref): `Same woman, same face. Seen from behind at the edge of the canoe, pulling a white cropped shirt over her head, glancing back over her shoulder at the camera with a playful smile, wet strands on her neck, golden backlight, handheld phone, slight motion blur, medium shot`
3. Subaquático (edit com ref): `Same woman, same face, swimming underwater toward the riverbed in murky green Amazon water, sun rays piercing from the surface, suspended particles, small bubbles from her nose, hair floating, red bikini top, low contrast, action-camera look, slight distortion`

## 3b. Nego d'Água (cenas 6 e 7)
- **Imagem:** Seedream v4/v4.5 (edit do quadro da cena 4) faz criatura e água turva sem recusa; Nano Banana pode recusar terror + biquíni.
- **Vídeo:** sem teste direto publicado. Seedance 1.5 lidera i2v em consistência; Kling e Wan são fortes em física e água. Criatura quase parada (olhos acendem, bolhas), silhueta escura: deforma menos. Cena 7: quadro-chave já com a mão no tornozelo, prompt só "pulls her down", 4 s, corte seco. Alternativa: veo3.1-lite start-end (0,40, risco de filtro).
- **Sem caricatura:** espírito do rio (pele de pedra molhada cinza-esverdeada, membranas); nunca traços étnicos ou de pessoa real.

Prompt da criatura: `Underwater in murky green Amazon river at dusk, behind mossy boulders on the riverbed, a tall bald humanoid river spirit stands motionless, slick dark grey-green skin like wet river stone, faint scales, webbed fingers, two small glowing amber eyes, mostly in shadow, silt and thin sun rays, woman in red bikini top swimming upward in foreground out of focus, action-camera look, grain, not a cartoon`

## 4. Recomendação: Seedream v4 + Seedance 1.5 Pro Fast
| Item | Modelo | Qtde | US$ |
|---|---|---|---|
| Herói + folha ref | seedream-v4 / edit-sequential | 4 img | 0,108 |
| 7 quadros-chave (cenas 1-7), 2 tentativas | seedream-v4/edit e t2i | 14 img | 0,378 |
| Cenas 1, 2, 3, 5, 6, 7 (4 s) | seedance-v1.5-pro i2v-fast 720p, sem áudio | 24 s | 0,48 |
| Cena 4 subaquática (6 s) | idem | 6 s | 0,12 |
| 3 refações | idem | 12 s | 0,24 |
| Opcional: mergulho no Kling | kling-v2.5-turbo-std 5 s (?) | 1 | 0,21 |
| Sussurro final | minimax speech-2.8-hd | ~60 caracteres | 0,01 |
| Subtotal | | | 1,546 |
| **Máximo com 10%** | | | **1,70** |

- Cena 8 = preto; risada e música da biblioteca. Seedance/s extrapolado de 0,10/5 s: medir 1 clipe de 4 s (custo.py). Herói plástico: refazer só ele no Nano Banana 2.1.

**Fallback:** demo Pruna (LoRA + p-image-edit + `/regenerate_video_only`) = US$ 0; ou WaveSpeed p-image/edit (10 × 0,01) + p-video (~26 s × 0,02 ?) ≈ 0,62. Realismo menor.

## Lição rodada 4 (2026-10-18)
- Edit do retrato mudando a pose (sentada para em pé) trocou o rosto e trouxe moldura de celular de volta ("candid photo taken by a friend" puxa moldura). Não usar essa frase.
- Para mudar corpo e pele de verdade, edit em cima do retrato antigo quase não muda nada (rodada 3). Funcionou: retrato NOVO em texto (bytedance/seedream-v4), "Photorealistic full-frame DSLR photo", "no freckles, no moles", "flat toned stomach with no belly", "No phone frame, no device bezel, no screen". Arquivo v10d/heroi_luana.jpg; prompt em v10d/json/heroi2.json.
- Rodada 5: mandar a foto de referência do short (vista de costas) como 2ª imagem no edit fez o Seedream virar a Luana de costas nas cenas 1 e 5 (bunda em foco, aliança foi parar no dedo). Nunca mandar referência de roupa com pose; descrever a peça só em texto.
- Funcionou: cena 4 simples (vista lateral, ela na borda da canoa prestes a pular), cena 7 com a criatura AGACHADA atrás da pedra ("crouches like an animal, not standing like a man"), cena 8 com câmera embaixo e a mão descrita dedo por dedo (4 dedos na frente do tornozelo, polegar atrás do calcanhar).
- Rodada 5 final (v10f): gerar tudo a partir do retrato com a roupa descrita em texto funcionou (biquíni vermelho combinando, canoa "completely DRY... clearly INSIDE it"). Falhas: k5 com corpo duplicado; refação k5b trouxe o short jeans de volta (o retrato tem short: dizer "no shorts" quando ela já tirou); k8b soltou a mão do tornozelo. Saída barata: recorte do fundo (aliança + iscas) da k5 como cena de inserto.
