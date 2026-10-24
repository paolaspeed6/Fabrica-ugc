# Montador Luxo (memoria/colecao-luxo.md)
1. Cenas do produto em `trabalho/src/A.mp4 ... F.mp4` (720x1280, Veo/Gemini) ou `LUXO_DIR=/pasta`.
2. Narração: `python3 -I tts_lux.py "texto" trabalho/tts2/x.wav` (uma de cada vez) e `python3 -I tighten.py x.wav x_t.wav 0.5`.
3. Timeline: copiar um bloco de `specs/lux.py` (molde), ajustar cortes/textos, rodar `cd specs && python3 lux.py` (gera os .json).
4. Render: `python3 -I build_lux.py trabalho/specs/NOME.json` (~3,5 min) e `python3 ../auditar_video.py saida.mp4`.

## Padrão aprovado para produção em massa (2026-10-20)
Use `specs/padrao_app.py` (`fazer_app(cfg)` e `preparar_clipe()`): gancho no topo, CTA com seta ↓ logo acima do card da Shopee / da legenda do Reels, nada na área do app. Exemplo: `specs/u01s_cfg.py`. No Reels, `cenas` usa o mesmo formato da B: (linha1, linha2 na cor, subtítulo).
