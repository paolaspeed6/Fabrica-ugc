# Prompts da dona (2026-10-18) — régua de qualidade das cenas

Ela gera hoje à mão: imagem no app Gemini ("gemini 2.1") e animação no Veo (low priority). Exemplos do resultado em
`referencias/gemini-veo/` (poltrona verde, 720x1280, 24 fps, 6-8 s, sem som). Meta dela: automático, NO MÍNIMO essa qualidade.

O que esses vídeos têm que os q09-q16 não têm (medido 2026-10-18):
- Parecem filmados no celular de verdade: sala real e cuidada (piso de pedra, taco espinha de peixe, tapete), luz de janela, plantas, sem "brilho de IA".
- Câmera contínua de verdade: push-in ou arco até o detalhe do tecido. Movimento 2,4 a 10 (auditar_video.py), contra 0,5-1,6 nos q09/q11.
- Cada cena em cenário e chão diferentes, produto idêntico.
- Defeito: em 2 dos 4 aparece uma MÃO apontando, mesmo com "no hands" no prompt → o QC reprova mão inventada (qualidade.md, Portão A, item 4).

## 1. Prompt de imagem (ela cola junto com a foto do produto)
Analise cuidadosamente a imagem do produto que estou enviando e crie 3 prompts diferentes para gerar imagens publicitárias ultra-realistas desse produto, extremamente realista 4k, estilo ugc, cada imagem chão e cenario diferente, cenarios reais mas bonitos e classicos, com texturas e sem iluminação de IA, minimo 16 linhas, sempre produtos novos e ambientes limpos. Criar imagens que pareçam fotos reais feitas por uma pessoa em um ambiente bonito e bem cuidado, com estética UGC premium, capazes de chamar atenção no feed e valorizar o produto sem parecer fotografia de catálogo, estúdio ou imagem gerada por IA.

## 2. Prompt base de animação
A POV UGC-style video showing the details of the bicycle; the bike remains stationary, with no hands or people visible, and no transitions—just a continuous shot of the bike.
(trocar "bicycle/bike" pelo produto)

## 3. Prompt de ganchos
Me de 40 ganchos criativos e atrativos para a shopee videos, quero 7 estilos de modelos de ganchos agressivos e atraentes, que façam despertar curiosidade e vontade de comprar, para esse produto e 10 ctas estrategicos e agressivos que incentivem a compra
(passar pelo filtro: só fatos do anúncio, sem nota exata, sem desconto, sem promessa de entrega — checar_textos.py e sem_nota.py)

## Teste da API Google AI Studio (chave GOOGLEAISTUDIO_API_KEY, 2026-10-18)
- Plano grátis: TODOS os modelos de imagem (gemini-2.5-flash-image, 3.1-flash-image, 3-pro-image, nano-banana-2.1, 3.1-flash-lite-image) = cota 0 (HTTP 429 "limit: 0"). Veo pela API não tem plano grátis. Nada foi cobrado.
- Grátis e funcionando: texto e análise de imagem/áudio (gemini-flash-latest) → escrever os 3 prompts de imagem e os 40 ganchos, conferir fidelidade das cenas, transcrever.
- Grátis e funcionando: narração PT-BR (gemini-2.5-flash-preview-tts, voz Kore; sotaque natural). gemini-3.8-flash-tts leu a instrução em voz alta: mandar só o texto a falar.
- O app Gemini/Flow da assinatura não pode ser automatizado (termos do Google; risco à conta).
