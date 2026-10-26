# Fábrica de vídeos UGC Aguiiar Lar (afiliada Shopee) + método do kit Fábrica Shopee (24/10/2026)

Responda sempre em português do Brasil, curto e simples, um passo por vez (a dona usa o celular). Diga sempre o que mudou e quanto custou.

Esta fábrica faz duas coisas:
1. **Editar** os takes que a dona manda (Veo/Hailuo), nos 3 layouts DELA: `MODELO_DE_CRIACAO.md`.
2. **Criar do zero** (método do kit, a mesma fábrica do Kevin): Tinder de produtos → fotos do anúncio → setor de qualidade →
   imagens (Nano Banana) e clipes (Seedance/Veo) na WaveSpeed → edição nos layouts DELA → Conferência → Drive → Postagens → Reels automáticos.

## Antes de QUALQUER roteiro, prompt, geração ou edição, leia
- `MODELO_DE_CRIACAO.md` (o padrão atual: 3 layouts, regras, processo, sem voz + música calma, estilo natural sem filtro)
- `agentes/regras_de_erros.md` inteiro (regras da dona 1-14 e as do kit com prefixo K; cada uma custou dinheiro)
- `agentes/setor_qualidade/LEIA.md` e o papel de cada agente (fichador, fiscal_imagem, fiscal_video, melhorador)
- `agentes/principios.md`, `agentes/produtor.md`, `agentes/desperdicios.md`, `agentes/LEIA.md`, `agentes/orquestrador.md`
- `memoria/LEIA.md`, `memoria/colecao-luxo.md` e `memoria/licoes_da_fabrica.md` (o porquê de cada regra). Regra nova da dona: grave na hora.
- `agentes/prompts_da_dona.md` (prompts dela e régua de qualidade Gemini/Veo); vídeo viral: `agentes/viral.md`
- `INSTRUCOES_DO_PROJETO.md` (regras gerais, custos, padrões de vídeo)
Skills de animação e design em `skills/` (leia `skills/LEIA.md` e o SKILL.md certo antes de mexer em texto animado, layout ou movimento).
Não repita nenhum erro listado.

## Dinheiro (regra dura)
- Nada pago sem o OK da dona no chat, com teto em dólar: quantos produtos, custo por produto e total.
- Preços medidos (WaveSpeed, out/2026): Nano Banana 2.1 Edit US$ 0,0396 por imagem; Seedance 1.5 Pro Fast i2v 5 s 720p sem áudio
  US$ 0,10 por clipe; Veo 3.1 Lite 4 s US$ 0,20. Por produto: 3 imagens + 3 clipes = ~US$ 0,42 (+ refações). Teto: R$ 3 por produto.
- O `video-teste/lote/modelo/gerar.py` para sozinho no teto (`TETO_USD`, gasto em `gasto.json`). Refazer só UMA vez; reprovou de novo = outra cena.
- Edição, busca, fotos, links, fichas, fiscais, montagem, render, Drive e postagem são grátis. Modelo novo: medir 1 cena antes de orçar.
- Toda refação paga ou vídeo perdido vai em `agentes/desperdicios.md`.

## Chaves (a dona cria; nunca peça para colar chave no chat, nunca grave chave em arquivo)
Segredos do ambiente (claude.ai/code > ambiente > engrenagem): WAVESPEED_API_KEY (já injetada pela rede), GOOGLEAISTUDIO_API_KEY
(header `x-goog-api-key`; texto, visão e voz grátis), SHOPEE_APP_ID, SHOPEE_APP_SECRET, GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET,
GDRIVE_REFRESH_TOKEN, META_PAGE_TOKEN, META_PAGE_ID, META_IG_ID, THREADS_TOKEN, MARCA_NOME (= "Aguiiar Lar"), DRIVE_PASTA.
Se faltar uma, diga qual e aponte `CONTAS.md`. Rede liberada necessária: lista em `CONTAS.md` / guia do kit.

## Edição (vale para os dois modos)
Sempre os layouts DELA (`MODELO_DE_CRIACAO.md`, `video-teste/luxo/specs/novos.py` + `produto.py`, lotes em `specs/lote_*.py`):
A "Um dia com ela", B "Faixas moderno", C "Direto ao ponto"; estilo natural (sem filtro, transições whip/zoom), gancho sem horário
quando não combina, assinatura "Aguiiar Lar" fixa no topo, sem voz + música calma (agora alternando a biblioteca `musicas/`).
Os modelos do kit (`video-teste/luxo/specs/padrao_app.py`, `opcao_c.py` "Checklist", Reels, `montar.py`) são só opção, se ela pedir.
Todo vídeo final passa em `video-teste/auditar_video.py`; a meta é SUPERAR `referencias/`. Entrega por página com botão de baixar
(`video-teste/luxo/pagina_lote.py`) ou Drive. Arquivo final ≤ 15,5 MB (`video-teste/luxo/recodificar.sh`).

## Criar do zero: produção de um lote (só depois do OK com teto)
Pasta `video-teste/lote/listaDDMMx` (copie `video-teste/lote/modelo`). Passos completos no CLAUDE.md do kit (`kit-fabrica-shopee/CLAUDE.md`):
1. Fotos (grátis): `python3 produto-campeao/buscar_fotos.py <link> <lote>/pNN-fotos`.
2. **Fichador** (trava 1, subagente, antes de gastar): `BRIEF_FICHADOR.md` + `agentes/setor_qualidade/fichador.md` → `pNN-ficha.json`, `pNN-textos.json`.
3. Links com Sub ID: `gerar_links.py` → `textos.py` (legendas < 150).
4. Imagens: `TETO_USD=<teto> python3 -I gerar.py imagens p01,...`
5. **Fiscal de imagem** (trava 2, subagente SEPARADO de quem escreveu): `BRIEF_FISCAL_IMAGEM.md` → `aplicar_fiscal.py`.
6. Clipes: `TETO_USD=<teto> python3 -I gerar.py clipes p01A,...` (só os liberados; `FIXA=1` se o produto se mexer).
7. **Fiscal de vídeo** (trava 3, subagente separado): `BRIEF_FISCAL_VIDEO.md` → `aprovar.py`.
8. Edição nos layouts DELA (acima). Produto `complexo`: foto 01 colada num canto (`video-teste/foto_colada/`).
9. **Obrigatório, nunca pular** (a dona, 24/10: o teste foi entregue só na página de baixar e não foi para a Conferência):
   finais em `<lote>/final/` com o nome `DDMMX_NN_slug_A|B|C.mp4` → `python3 video-teste/drive_backup.py <lote>/final --dia AAAA-MM-DD`
   → `python3 -I conferencia.py "Lista DD/MM X" AAAA-MM-DD` → ArtifactData batch dos `conferir_docs/*.json` na coleção `conferir`
   da Conferência (URL em `MINHAS_PAGINAS.md`) → Tinder status `pronto`. Página de baixar é extra, nunca no lugar da Conferência.
   Siga `video-teste/lote/modelo/CHECKLIST.md` e marque cada passo no `<lote>/CHECKLIST.md`.
   Depois da conferência dela: processar as decisões e o **Melhorador** (trava 4, 1 vez por lote).
Os agentes do setor de qualidade são subagentes separados (ferramenta Agent).

## Economia de uso do Claude sem perder qualidade (a dona, 26/10: o lote 25/10 A esgotou o limite 3 vezes)
- **Uma conversa nova por lote.** Comece lendo `PROXIMO_LOTE.md` (o resumo do ponto em que paramos), não o histórico.
- **Agentes no Sonnet** (`model: "sonnet"` no Agent tool), 1 ou 2 por etapa, NUNCA 9 em paralelo. Eles leem só
  `agentes/setor_qualidade/RESUMO_REGRAS.md` + o BRIEF da função; o `regras_de_erros.md` inteiro é só para o orquestrador.
- **Código e Gemini antes do Claude (grátis):** `folha.py` (borda medida por rembg, reprova sozinho, monta 1 folha por produto),
  `fiscal_gemini.py` e `fiscal_video_gemini.py` (GOOGLEAISTUDIO_API_KEY; modelo gemini-3-flash-preview com reserva automática);
  a Fiscal Sonnet só confirma olhando a folha (`video-teste/lote/modelo/PROMPT_FISCAL_SONNET.md`).
- **Edição sozinha:** `video-teste/luxo/specs/lote_auto.py` (3 layouts da dona a partir dos trechos limpos, clipe só até 4 s).
- **Lote longo roda solto** (`setsid nohup`, sem o limite de 2 h) com `retomar.sh` + tarefa agendada de hora em hora até tudo estar na Conferência.
- Respostas curtas; não reler arquivos grandes nem imagens já conferidas; olhar 1 folha de quadros por produto, não vídeo por vídeo.

## Páginas do kit (publicar uma vez, quando ela pedir) — capabilities {db: {}, user: {}}
`paginas/tinder.html` (Tinder Shopee), `paginas/conferencia.html` (+comments), `paginas/postagens.html` (formato em `agentes/postagens_formato.md`),
e o jogo "Reino Encantado das Divas" em `paginas/reino/` (ler `paginas/reino/LEIA.md`: aparência em tema.js/arte.js, etapas reais em
fluxo.js; "Atualiza o reino" = sincronizar.py + doc reino/estado). URLs em `MINHAS_PAGINAS.md`. Dados só via ArtifactData.
Varredura diária: `produto-campeao/afiliados/varrer.py` (precisa da API de afiliados). Tarefas agendadas: `TAREFAS_AGENDADAS.md`.
Postagem automática: `meta/postar.py` (conferir, plano com `--seco`, fila `meta/rodar_fila.sh` com MAX_DIA=2 INTERVALO_H=3).

## Onde ficam os dados na nuvem
Cada conversa começa de um clone novo. No fim de cada tarefa: commit e push dos registros (vistos.json, ultima_rodada.json, postados.json,
pausas.json, usadas.json, desperdicios.md, defeitos.csv, MINHAS_PAGINAS.md, memoria/) e dos mp4 finais aprovados (os da dona ficam no Git
até o Drive estar ligado). Nada de intermediários (*.video.mp4, prévias) no Git.

## Nunca
- Burlar captcha, automatizar login da Shopee ou usar robô no app (a conta de afiliada é renda da família).
- Bebida alcoólica, taças ou garrafas em cena; promessa de entrega, % de desconto, nota exata ou número de avaliações.
- Mão ou pessoa na capa; produto se mexendo; objeto sem nexo; detalhe, letra ou qualidade inventada ("linhas retas" não é qualidade).
- Subir chave, token, link de afiliado ou Sub ID para repositório público (este é privado).
- Erro novo vira regra em `agentes/regras_de_erros.md` e `agentes/licoes.md`.

O kit original, intacto, está em `kit-fabrica-shopee/` (referência; não editar lá).
A cada sessão o setup script instala `gradio_client` e `faster-whisper`; o Whisper precisa de `*.hf.co` liberado na rede.
