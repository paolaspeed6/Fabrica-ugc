# Checklist do lote (copie junto com a pasta e marque cada passo; nenhum passo é opcional)

Antes de gastar
- [ ] OK da dona no chat com teto em dólar (quantos produtos, custo por produto, total)
- [ ] Tinder: produtos com status `produzindo` e campo `lote`
- [ ] links.txt ("NN https://shopee.com.br/product/<loja>/<item>")
- [ ] Fotos: `python3 -I produto-campeao/buscar_fotos.py <link> <lote>/pNN-fotos`
- [ ] Fichador: 1 ou 2 agentes `model: "sonnet"` (nunca 9), lendo só RESUMO_REGRAS.md + BRIEF_FICHADOR.md; descarta produto sem foto limpa ANTES de gastar
- [ ] Eu conferi cada ficha contra a foto 01 e cada texto contra o anúncio
- [ ] Links com Sub ID: `SHOPEE_APP_SECRET=... python3 -I gerar_links.py` → `python3 -I textos.py`

Geração + edição + entrega num comando (a dona 27/10): Bash em segundo plano, timeout 7200000, 1 aviso por fase
- [ ] `TETO_USD=<teto> bash produzir.sh fase1 <lote> p01,...` (imagens, borda, Gemini, 1 refação)
- [ ] 1 agente Sonnet nas folhas (PROMPT_FISCAL_SONNET.md)
- [ ] `TETO_USD=<teto> bash produzir.sh fase2 <lote> p01,... <PRE> <AAAA-MM-DD> "Lista DD/MM X"` (clipes, Fiscal de vídeo, edição, render, Drive, conferir_docs)
- [ ] ArtifactData batch dos conferir_docs na coleção `conferir` da página POSTAGENS (aba Conferir) + Tinder `pronto` + commit — e pronto
O que o produzir.sh faz por dentro (só para conferir/consertar):
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
- [ ] ArtifactData batch `conferir_docs/*.json` na coleção `conferir` da página POSTAGENS (a dona 27/10: o Ok dela cria os posts sozinho)
- [ ] Tinder: status `pronto`
- [ ] Jogo: metas, Mural (o que aconteceu no lote) e Gasto
- [ ] Commit e push (mp4 finais em trabalhos/, spec, desperdícios, defeitos, vistos)
- [ ] (opcional) página com botão de baixar
- [ ] Nenhum produto sem versão: o entregar.sh refaz a versão reprovada com zoom maior (2x) e, se ainda falhar, entrega com `aviso` para a dona decidir
- [ ] Produto sem cena aprovada (K22): `sem_cena.py` (o produzir.sh já roda) monta A, B e C com as reprovadas só por borda, câmera por código, aviso "cenas reprovadas pela fiscal: confira"; defeito grave fica fora. Sem imagem aproveitável: `descartadas.py` (o produzir.sh já roda) manda as cenas reprovadas para a aba Conferir (cartão "resgate"); nunca descartar sem ela ver
- [ ] Começo do lote seguinte: `conferir` com status `resgatar` (campo escolha = cenas que ela aceitou) → imagens do histórico da WaveSpeed (grátis) → `camera_codigo.py pNN <escolha>` (K19) → lote_auto → render → entregar;
- [ ] Começo do lote seguinte: ler `conferir` da Postagens com status `editar` (nota dela), refazer, gravar de novo como `pendente`; Melhorador
