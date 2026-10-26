# Onde paramos (leia isto no começo de uma conversa nova; atualize no fim de cada lote)

Atualizado: 2026-10-26.

## Último lote: Lista 25/10 A — ENTREGUE (26/10, 23h)
- 41 produtos na Conferência (106 vídeos: 41 A, 24 B, 41 C; 17 B reprovados no auditor por cena quase parada) e no Drive
  "Fabrica Videos/2026-10-26". Tinder: os 41 em `pronto`. Gasto US$ 18,69. Jogo: retomar (metas, mural, gasto) e perguntar à dona.
- No Drive ficaram cópias antigas cortadas (disco cheio) de 2510A_01 A/B, 25 A/B/C, 41 C, 43 A/B/C: a Conferência aponta para as boas.
- Antes do próximo lote: corrigir o layout B no lote_auto (tomadas de 5 s com clipe de 4 s = cena quase parada).

## Conferência do 25/10 A (a dona, 26/10 20h25) — FALTA PROCESSAR na conversa de produção (com as chaves e os clipes)
- OK (19): 01 02 03 04 06 07 13 17 18 19 20 23 29 32 41 42 43 44 45 → Postagens (agentes/postagens_formato.md).
- Editar, "letras muito grandes, saíram da tela" (21): 08 09 10 11 12 14 15 16 21 22 24 25 27 28 30 31 33 35 36 38 40.
  O build_lux.py já encolhe sozinho todo texto mais largo que a tela (margem 56 px, commit de 26/10). Basta renderizar de novo
  esses produtos (lote_auto + render, grátis) e trocar no Drive e na Conferência. Vídeo de resto aprovado: não mexer em cena.
- 26: "surgiu uma imagem do nada, quero vídeo fluido" → achar o corte/tomada com salto e refazer a montagem (grátis).
- A conversa do comentário (só app, sem chaves nem pasta do lote) não conseguiu processar; as decisões seguem salvas na página.

## Pendências da dona
- Segredos: renomear `shopee_APP_SECRET` para `SHOPEE_APP_SECRET`; token da Página em META_PAGE_TOKEN; THREADS_TOKEN novo;
  criar MARCA_NOME e DRIVE_PASTA.
- Tarefas agendadas do kit (varredura, contador, Reels) ainda não criadas.

## Próximo lote (fluxo econômico)
Seguir `video-teste/lote/modelo/CHECKLIST.md` e a seção "Economia de uso" do CLAUDE.md: Fichador Sonnet (1-2 agentes),
gerar.py → folha.py → fiscal_gemini.py → Fiscal Sonnet (1 agente, folhas) → clipes → fiscal_video_gemini.py → lote_auto.py →
render solto → entregar.sh → Conferência. Lote de 15 produtos de cada vez.

## Regra da dona (26/10): economia só se não prejudicar a qualidade
No 1º lote com o fluxo econômico, conferir 3 produtos TAMBÉM com uma Fiscal Opus (modelo padrão) e comparar com a Fiscal Sonnet.
Se o Sonnet deixar passar defeito que o Opus pegou, voltar a Fiscal de confirmação para o Opus (1 agente, só as folhas). Anotar o resultado aqui.
- Durante o render, musicas/usadas.json muda a cada vídeo: usar git update-index --assume-unchanged e desfazer no fim.
