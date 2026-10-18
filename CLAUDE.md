# Fábrica de vídeos UGC (afiliada Shopee)

Responda sempre em português do Brasil, curto e simples (a dona usa o celular).

Antes de qualquer roteiro, prompt, geração ou edição, leia:
- `INSTRUCOES_DO_PROJETO.md` (regras gerais, custos, padrões de vídeo)
- `agentes/LEIA.md`, `agentes/orquestrador.md`, `agentes/principios.md`, `agentes/regras_de_erros.md`
- `agentes/prompts_da_dona.md` (prompts dela e régua de qualidade Gemini/Veo)
- `memoria/LEIA.md` e os arquivos de `memoria/` do assunto (o que a fábrica já aprendeu)
- Vídeo viral: `agentes/viral.md`

Skills de animação e design ficam em `skills/` (GSAP, motion design, Design DNA, Genjutsu, Three.js, Emil Kowalski, Impeccable): leia `skills/LEIA.md` e o SKILL.md certo antes de mexer em texto animado, layout ou movimento.

Regras que nunca mudam:
- Nada pago sem o OK da dona: diga o custo máximo antes.
- Todo vídeo final passa em `video-teste/auditar_video.py`; a meta é SUPERAR `referencias/`, não igualar.
- Erro novo vira regra em `agentes/regras_de_erros.md` e `agentes/licoes.md`.
- Chaves: WaveSpeed (injetada pela rede / `WAVESPEED_API_KEY`), Google AI Studio (`GOOGLEAISTUDIO_API_KEY`, header `x-goog-api-key`; texto, visão e voz grátis, imagem e Veo não).
- A cada sessão o setup script instala `gradio_client` e `faster-whisper`; o Whisper precisa de `*.hf.co` liberado na rede.
