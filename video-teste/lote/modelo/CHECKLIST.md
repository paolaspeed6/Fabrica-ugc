# Checklist do lote (copie junto com a pasta e marque cada passo; nenhum passo é opcional)

Antes de gastar
- [ ] OK da dona no chat com teto em dólar (quantos produtos, custo por produto, total)
- [ ] Tinder: produtos com status `produzindo` e campo `lote`
- [ ] links.txt ("NN https://shopee.com.br/product/<loja>/<item>")
- [ ] Fotos: `python3 -I produto-campeao/buscar_fotos.py <link> <lote>/pNN-fotos`
- [ ] Fichador: 1 ou 2 agentes `model: "sonnet"` (nunca 9), lendo só RESUMO_REGRAS.md + BRIEF_FICHADOR.md; descarta produto sem foto limpa ANTES de gastar
- [ ] Eu conferi cada ficha contra a foto 01 e cada texto contra o anúncio
- [ ] Links com Sub ID: `SHOPEE_APP_SECRET=... python3 -I gerar_links.py` → `python3 -I textos.py`

Geração (teto em TETO_USD; refazer só UMA vez) — fluxo econômico (a dona 26/10: economia sem perder qualidade)
- [ ] `TETO_USD=<teto> python3 -I gerar.py imagens p01,...`
- [ ] `python3 -I folha.py p01,...` (grátis: mede a borda e reprova sozinho; monta pNN-cenas/folha.jpg)
- [ ] `python3 -I fiscal_gemini.py <cenas sem veredito>` (grátis; 2 ou 3 filas em paralelo)
- [ ] Fiscal de confirmação: 1 agente Sonnet lendo só as folhas (PROMPT_FISCAL_SONNET.md)
- [ ] `python3 -I aplicar_fiscal.py p01,...` → refação única → folha.py + fiscal_gemini.py de novo nas refeitas
- [ ] `TETO_USD=<teto> python3 -I gerar.py clipes ...` só as liberadas
- [ ] `python3 -I fiscal_video_gemini.py ...` (grátis) → `python3 -I aprovar.py p01 ...` (o lote_auto usa só até 4 s de cada clipe)
- [ ] Perdas anotadas em `agentes/desperdicios.md`

Edição (grátis, layouts DA DONA)
- [ ] `cd video-teste/luxo/specs && python3 lote_auto.py <lote> <1º id> [pNN,...]` (monta os 3 layouts sozinho a partir dos trechos limpos)
- [ ] Lote grande: rodar solto (`setsid nohup bash cadeia.sh &`, sem limite de 2 h) + tarefa agendada de hora em hora que retoma e entrega (ver lista2510a/cadeia.sh e retomar.sh)
- [ ] Eu conferi capa e quadros (produto inteiro, sem mão, sem proibidos, take de abertura diferente nos 3)
- [ ] Produto `complexo`: foto 01 colada (`video-teste/foto_colada/`), ou motivo anotado se não der

Entrega (NUNCA pular; a dona 2026-10-24)
- [ ] Finais em `<lote>/final/DDMMX_NN_slug_A|B|C.mp4`
- [ ] Drive: `python3 video-teste/drive_backup.py <lote>/final --dia AAAA-MM-DD` (grava drive_links.json)
- [ ] `bash video-teste/lote/entregar.sh <lote> <PREFIXO> <dia> "Lista DD/MM X" 15 pNN ...` (auditor + Drive + conferir_docs, de 15 em 15)
- [ ] ArtifactData batch `conferir_docs/*.json` na coleção `conferir` da Conferência
- [ ] Tinder: status `pronto`
- [ ] Jogo: metas, Mural (o que aconteceu no lote) e Gasto
- [ ] Commit e push (mp4 finais em trabalhos/, spec, desperdícios, defeitos, vistos)
- [ ] (opcional) página com botão de baixar
- [ ] Depois da conferência dela: processar decisões, Postagens (agentes/postagens_formato.md), Melhorador
