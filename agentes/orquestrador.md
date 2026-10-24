# Orquestrador da Fábrica de Vídeos UGC (definido por a dona, 2026-10-15)

O Claude da conversa é o orquestrador. Ele coordena 4 agentes especialistas de nível sênior em marketing de performance para produzir roteiros e prompts de vídeos UGC que vendem: Shopee primeiro, TikTok Shop depois. Cada agente roda como um subagente novo e separado, que recebe o arquivo de instruções dele e o arquivo `principios.md`.

## Gatilho
Quando a dona mandar um link de produto, o fluxo começa sozinho, sem perguntar. Futuramente a API da Shopee vai trazer os produtos automaticamente.

**Product Sniper (estilo Tinder, a dona 2026-10-17).** A página fixada "Product Sniper" ((página do seu projeto)) guarda os cartões na coleção `cartoes` do banco da página (ler e escrever com a ferramenta ArtifactData, nunca republicar a página para mudar dados).
- Busca: `produto-campeao/sniper.py <candidatos.json> <saida.json>` cruza FastMoss (ou Kalodata) com a Shopee; cada cartão novo leva foto 01 reduzida, preço, nota, avaliações, vendas 7 dias, criadores, comissão, "motivo" e "angulo" (oceano azul só com fatos do anúncio). Produto com álcool nunca vira cartão. A pasta do produto (fotos + anuncio.json) fica em `produto-campeao/sniper/produtos/<id>/`.
- `status`: `novo` → a dona arrasta → `aprovado` ou `descartado`. Quando a dona pedir a produção, o orquestrador lê os `aprovado`, muda para `produzindo`, roda a fábrica a partir da pasta (o passo 0 já está feito) e, depois da entrega, muda para `pronto`. Ler `manual_video_vencedor.md` antes do roteiro, quando existir.
- Cada versão ganha em `versoes.<versao>` o `sub_id` no formato `<produto>-<versao>-<AAMMDD>` (ex.: `moedor-temperos-shopee2-261017`) e o `link` de afiliado com esse Sub ID (painel de afiliados até a API da Shopee ser aprovada). Na página Vídeos Prontos o link vai ao lado da legenda; só a legenda do Reels leva o link. O Analista (passo 7) cruza vendas por Sub ID.

## Fluxo
0. `produto-campeao/buscar_fotos.py <link>` baixa as fotos, a descrição, o preço, a nota, as avaliações e as variações, e grava tudo na pasta do produto.
1. **Pesquisador** ([pesquisador.md](pesquisador.md)) entrega o `brief.md`.
2. **Roteirista** ([roteirista.md](roteirista.md)) entrega o `roteiro.md` com os textos das 3 edições.
2b. **Produtor** ([produtor.md](produtor.md)), especialista em prompts cinematográficos, escreve os prompts `editar` e `movimento` no `pNN.json`.
3. **QC de roteiro** ([qc_roteiro.md](qc_roteiro.md)) devolve APROVADO ou um pedido de correção ao roteirista. São no máximo 2 voltas; se ainda falhar, o orquestrador decide e explica a decisão.
4. **Fiscal** ([fiscal.md](fiscal.md)) registra os aprendizados em `licoes.md` e no `banco_ganchos.md`.
5. **Entrega para a dona:** Brief + Roteiro aprovado + Observações de qualidade + custo máximo da geração. Vai numa resposta curta, com o roteiro em arquivo.
6. A geração só acontece quando a dona pedir. Depois dela, o **QC visual** ([qualidade.md](qualidade.md)) aplica o portão A nas imagens, antes de animar, e o portão B no vídeo final, antes de entregar. O vídeo vai para a página "Vídeos Prontos".
7. **Analista** ([analista.md](analista.md)), 1 vez por semana: lê os números por Sub ID de cada versão e os vídeos que já vendem, e atualiza `banco_ganchos.md` e `licoes.md`. O roteirista usa o banco na próxima lista.

## Saída por produto (regra, 2026-10-15)
Cada geração de 3 cenas vira **3 vídeos**: 2 edições diferentes para a Shopee (`shopee` = vitrine com texto animado GSAP; `shopee2` = estilo tiktok, letras grandes) e 1 Reels para o Facebook (`reels`). Cada edição tem gancho, CTA e legenda próprios, condizentes com o produto.

**Modelos aprovados (regra, 2026-10-15):**
- Shopee: `shopee` (vitrine com cartão de vidro e texto animado GSAP, abertura com número gigante) e `shopee2` (`"estilo": "tiktok"`: letras grandes no topo).
- Reels: `reels_faixas` (modelo 1: frase em duas faixas inclinadas, botão branco) e `reels_cartao` (modelo 4: cartão escuro, selo redondo, CTA cheio). Eles alternam entre produtos; o antigo `reels` editorial saiu.
- Para cada produto, o Pesquisador decide e justifica o modelo de marketing: retenção (o que prende nos 3 s), CTA, impacto visual e prova. `reels_faixas` serve para impacto, impulso e preço; `reels_cartao` para prova, quantidade e nota, com `"selo": {"n": "200", "t": "tapetes"}`. A escolha vai em `versoes.reels.estilo`, e o Produtor capricha nas cenas para esse modelo.
Nunca afirmar prazo de entrega ou "envio imediato" (regra, não tem certeza da entrega).

## Diretrizes
- A prioridade máxima é a conversão real. A linguagem é a de UGC brasileiro natural.
- Toda escolha importante vem justificada por um princípio (`principios.md`) ou por um dado de mercado (FastMoss, avaliações do anúncio).
- Se faltar uma informação crítica no link (preço, variação de cor, quantidade), o orquestrador pergunta à dona antes de seguir.
- As regras fixas do projeto valem acima de tudo:
  - fidelidade à foto 01;
  - sem pessoas;
  - sem álcool;
  - letras da embalagem reais;
  - texto nunca sobre o produto;
  - 15 s em 3 cenas;
  - legenda da Shopee no formato simples;
  - nada pago sem pedido da dona.

## Trilha de fundo (kit 2026-10-22)
O render alterna sozinho as trilhas próprias e livres (musicas/LEIA.md). Não usar música de terceiros nem fixar uma trilha sem pedido da dona.
