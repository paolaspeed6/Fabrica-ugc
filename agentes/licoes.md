# Lições (mais novas em cima)

- 2026-10-18 · Coleção Luxo aprovada (memoria/colecao-luxo.md). auditar_video.py dava falso alarme com câmera em movimento real (gancho) e com mergulho ao preto (fusão) → gancho agora mede bordas de letras (1º quadro / 1,2 s ≥ 0,7) e corte que passa pelo preto (brilho < 35) não conta como dupla exposição.
- 2026-10-18 · Poltrona (sessão de edição): edição sem a fábrica carregada (stickers, emoji) e recolor por máscara HSV (pixels bugados) reprovados → regras 9 e 10. Vídeos Veo com mão inventada: Camera_filming_green_lounge_chair ~0,75-5,75 s; Camera_filming_green_suede_chair ~0,75-3,5 s (limpo 3,75-6 s).
- 2026-10-18 · API Gemini grátis: imagem e Veo com cota 0; texto, visão e voz grátis (agentes/prompts_da_dona.md). Whisper não baixa modelo sem `*.hf.co` na rede (us.aws.cdn.hf.co, cas-server.xethub.hf.co).
- 2026-10-18 · Referências q09-q16: as cenas eram foto do anúncio com movimento por código (mover_foto.py), por isso quase paradas (movimento 0,5-1,6) e a capa sem gancho → criado `video-teste/auditar_video.py` (movimento por cena, gancho no 1º quadro, fusão fantasma, áudio, duração), ligado ao `fazer_lista.py`.
- 2026-10-16 · Lista1015 (revisão da dona): cenas de IA pagas trocadas por foto real em 15 produtos (desmonte de prateleira, planta andando, celular, parafusos inventados, letras tortas, pegador do lado errado) → o roteiro decide CÓDIGO ou IA por cena antes de gastar (regras_de_erros.md, seção 0).
- 2026-10-16 · Escrivaninha: close da "sapata niveladora" por IA inventou parafuso → close de mecanismo só com foto real.
- 2026-10-16 · 3 edições Shopee no mesmo layout → a dona quer 3 layouts diferentes (faixas, letras no topo, cartão com selo) para testar conversão.
- 2026-10-16 · Layout com título no topo: letra branca sumia em fundo claro → degradê do topo reforçado.
- 2026-10-16 · #achadinhosshopee genérica e saturada → 4 hashtags de nicho.
- 2026-10-16 · Botão de baixar gerava nome sem extensão para vídeos guardados como asset → nome = id + ".mp4".

- 2026-10-15 · Tapete v2: mudar o "nome" de um pNN.json sem apontar "clipe" para as cenas existentes faria o produzir.py gerar tudo de novo (pago) → sempre fixar "clipe" ao reaproveitar e rodar com TETO_LOTE_USD=0 quando o trabalho deve ser grátis.
- 2026-10-15 · Tapete v2 (QC): texto pequeno do Reels sem quebra de linha passava da borda de 1080 px; fichas da Shopee passavam do cartão com título de 2 linhas → medir textos antes de renderizar.

- 2026-10-15 · Poltrona: cena 3 veio com faixas brancas em cima e embaixo → corrigido cortando de graça; o portão A agora reprova faixas/bordas.
- 2026-10-15 · Poltrona: garrafas de vinho apareceram porque o prompt dizia "no bottles" → descrever só o que existe; produzir.py usa PROIBIDO positivo.
- 2026-10-15 · Poltrona: cor bege em vez do azul da foto 01 → a foto 01 é sempre a referência; checagem exige fotos[0] = 01.jpg.
- 2026-10-15 · Tapete: letras da embalagem tortas → embalagem real composta por código (compor_embalagem.py) com rastreio de câmera.
- 2026-10-15 · Capacete: giro inventou a frente → TRAVA_ANGULO; giro grande só com angulos_reais.
- 2026-10-15 · Vários: texto cobrindo o produto → conferir o último quadro; subir/escala por versão.
- 2026-10-21: motosserra p24 saiu com logo "TOYIAMA" (close de IA) e título encostando na borda; refeita. Ver regra 14.
