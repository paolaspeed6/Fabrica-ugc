# Onde paramos (leia isto no começo de uma conversa nova; atualize no fim de cada lote)

Atualizado: 2026-10-26.

## Lote em andamento: Lista 25/10 A (`video-teste/lote/lista2510a`, pasta fora do Git)
- 45 produtos da Fila do Tinder (OK da dona, teto US$ 24). 3 descartados antes de gastar: p05 (pessoa em todas as fotos),
  p37 (réplica de Bosch), p39 (homem pedalando). Gasto em `gasto.json` (~US$ 18,7 com os clipes das refações).
- 42 produtos viram trabalhos/p67 em diante (`trabalhos_todos.json` = pNN do lote -> pasta em trabalhos/).
- Rodando solto: `cadeia.sh` (parte 1: 18 produtos; parte 2: 24 das refações). Se caiu: `setsid nohup bash retomar.sh &`.
- Tarefa agendada "Checar lote 25/10 A até concluir" (de hora em hora) entrega na Conferência de 15 em 15
  (conferir_docs/ -> ArtifactData coleção conferir; anotar em enviados_conferencia.txt), marca Tinder pronto (ids_tinder.json),
  sobe os finais com `git add -f` e apaga a tarefa no fim.
- Jogo pausado até o lote estar todo na Conferência (memoria/licoes_da_fabrica.md); depois atualizar metas/mural/gasto de uma vez.

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
