# Checklist do lote (copie junto com a pasta e marque cada passo; nenhum passo é opcional)

Antes de gastar
- [ ] OK da dona no chat com teto em dólar (quantos produtos, custo por produto, total)
- [ ] Tinder: produtos com status `produzindo` e campo `lote`
- [ ] links.txt ("NN https://shopee.com.br/product/<loja>/<item>")
- [ ] Fotos: `python3 -I produto-campeao/buscar_fotos.py <link> <lote>/pNN-fotos`
- [ ] Fichador (subagente separado, ficha com cada mínimo detalhe, regra 15) → pNN-ficha.json e pNN-textos.json
- [ ] Eu conferi cada ficha contra a foto 01 e cada texto contra o anúncio
- [ ] Links com Sub ID: `SHOPEE_APP_SECRET=... python3 -I gerar_links.py` → `python3 -I textos.py`

Geração (teto em TETO_USD; refazer só UMA vez)
- [ ] `TETO_USD=<teto> python3 -I gerar.py imagens p01,...`
- [ ] Fiscal de imagem (subagente separado) → `python3 -I aplicar_fiscal.py p01,...` → refação única → fiscal de novo
- [ ] `TETO_USD=<teto> python3 -I gerar.py clipes ...` só as liberadas
- [ ] Fiscal de vídeo (subagente separado) → trechos limpos → `python3 -I aprovar.py p01 ...`
- [ ] Perdas anotadas em `agentes/desperdicios.md`

Edição (grátis, layouts DA DONA)
- [ ] `trabalhos/pNN-slug/src` com os clipes limpos + `video-teste/luxo/specs/lote_DDMM.py` (clips = fim do trecho limpo)
- [ ] `bash video-teste/luxo/render_lote.sh trabalhos/pNN-...` (em segundo plano) → APROVADO no auditor, ≤ 15,5 MB
- [ ] Eu conferi capa e quadros (produto inteiro, sem mão, sem proibidos, take de abertura diferente nos 3)
- [ ] Produto `complexo`: foto 01 colada (`video-teste/foto_colada/`), ou motivo anotado se não der

Entrega (NUNCA pular; a dona 2026-10-24)
- [ ] Finais em `<lote>/final/DDMMX_NN_slug_A|B|C.mp4`
- [ ] Drive: `python3 video-teste/drive_backup.py <lote>/final --dia AAAA-MM-DD` (grava drive_links.json)
- [ ] Conferência: `python3 -I conferencia.py "Lista DD/MM X" AAAA-MM-DD` → ArtifactData batch `conferir_docs/*.json` na coleção `conferir`
- [ ] Tinder: status `pronto`
- [ ] Jogo: metas, Mural (o que aconteceu no lote) e Gasto
- [ ] Commit e push (mp4 finais em trabalhos/, spec, desperdícios, defeitos, vistos)
- [ ] (opcional) página com botão de baixar
- [ ] Depois da conferência dela: processar decisões, Postagens (agentes/postagens_formato.md), Melhorador
