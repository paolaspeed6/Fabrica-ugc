# Estado da configuração (2026-10-17)

## Decisão da dona (2026-10-17)
O provedor é a WaveSpeed. Não usar Higgsfield, nem como alternativa.

## Já salvo no projeto
Os 58 arquivos de texto do fabrica-ugc.zip (agentes/, video-teste/, produto-campeao/, modelos-edicao/*.md, skills/LEIA.md, viral/), com a mesma estrutura de pastas do pacote. Os 3 arquivos da raiz (LEIA-PRIMEIRO.md, COMO_USAR.md e INSTRUCOES_DO_PROJETO.md) ficaram em claude/.
Não cabem como documento do projeto (arquivos binários): video-teste/fontes/*.ttf (14 fontes do Google Fonts) e modelos-edicao/3-modelos-shopee.jpg. Para usá-los, anexe o zip de novo na conversa ou baixe as fontes do GitHub google/fonts.

## Ajustes feitos no pacote
- render_fila.sh agora entra na própria pasta video-teste, em vez de usar /mnt/project-files.
- Os .md de agentes/ citam agentes/licoes.md por caminho relativo.

## Pendente (ela configura no ambiente)
- As conversas do projeto do chat rodam no ambiente padrão (Default), que só libera instaladores de pacotes e GitHub e não tem tela de edição. A WaveSpeed, a Shopee e a Pruna ficam bloqueadas (testado em 2026-10-17).
- Caminho: criar o ambiente "Fábrica UGC" em claude.ai/code (botão do ambiente embaixo da caixa de mensagem › New environment) e rodar a fábrica numa conversa iniciada lá com esse ambiente.
- Rede Custom com os domínios: api.wavespeed.ai, *.wavespeed.ai, shopee.com.br, *.shopee.com.br, *.susercontent.com, open-api.affiliate.shopee.com.br, demo.pruna.ai, huggingface.co, *.hf.space (e a lista padrão marcada).
- Chave da WaveSpeed: network secret para o host api.wavespeed.ai (Authorization: Bearer). Como alternativa, a variável WAVESPEED_API_KEY.
- Opcional: SHOPEE_APP_ID e SHOPEE_APP_SECRET, só para o buscar_produtos.py.

## A cada sessão nova (grátis)
pip install --break-system-packages gradio_client faster-whisper
Isso pode ir para o setup script do ambiente.
