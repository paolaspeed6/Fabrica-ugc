# Modo Crescimento: vídeos virais para ganhar seguidores (Kevin, 2026-10-17)

Usar quando a conta ainda não tem o TikTok Shop liberado (Kevin: libera com 2.000 seguidores). O objetivo é **seguidor**, não venda: sem link, sem preço, sem CTA de compra. Ler junto com `principios.md` (os livros de venda continuam valendo para o ângulo), `manual_video_vencedor.md` e `regras_de_erros.md`. O roteirista anota, ao lado de cada decisão, o livro usado.

## Por que seguidor e não view
Viral que não vira seguidor não libera o Shop. O vídeo tem que prometer **mais do mesmo amanhã**: série, nicho claro e um motivo para seguir. Toda conta tem um nicho só (casa, tecnologia ou pet), o mesmo dos produtos que ela vai vender depois. Assim o público que chega já é comprador.

## Livros de internet, viralização e psicologia
| Livro | Regra que vira roteiro |
|---|---|
| **Brendan Kane — Hook Point / One Million Followers** | Os 3 primeiros segundos decidem tudo. Teste muitas variações do mesmo vídeo com ganchos diferentes e escale o que segura. Formato que dá certo vira série. |
| **Jimmy Donaldson (MrBeast) — guia de produção vazado** | Retenção acima de tudo: o que é prometido no gancho aparece no fim, a cada 3-5 s algo muda (corte, número, zoom), e nada de introdução. |
| **Jonah Berger — Contágio e Palavras Mágicas** | STEPPS: moeda social (“eu sabia disso”), gatilho do dia a dia, emoção de alta excitação (espanto, graça), utilidade prática. Palavras concretas e perguntas prendem mais que adjetivos. |
| **Chip e Dan Heath — Ideias que Colam** | Inesperado + concreto: quebre o que a pessoa espera no 1º segundo e mostre o objeto exato, nunca o genérico. |
| **George Loewenstein — Lacuna de Curiosidade** | O gancho abre uma pergunta que só o fim responde: “o 3º é o que ninguém conhece”. |
| **Nir Eyal — Hooked** | Gatilho, ação, recompensa variável, investimento: a série com número (“parte 4”) faz a pessoa voltar e seguir. |
| **Kahneman — Rápido e Devagar** e **Dan Ariely — Previsivelmente Irracional** | O feed é Sistema 1: imagem clara, 1 ideia por quadro, números redondos e comparação lado a lado (ancoragem). |
| **Austin Kleon — Mostre seu Trabalho** | Bastidor e processo prendem: “testei por 7 dias”, “montei em 2 min”. |
| **Malcolm Gladwell — O Ponto da Virada** | Fator de fixação: um bordão e um visual fixos por conta, para a pessoa reconhecer o perfil no 2º vídeo. |
| **Robert Cialdini — Pré-suasão** | O que aparece antes muda a leitura do que vem depois: abra com o problema, e o produto parece a resposta. |

## Liberado pelo Kevin (2026-10-17, cartão "Narração e mãos")
- **Narração por IA em PT-BR** nos vídeos de crescimento, pela WaveSpeed (MiniMax Speech 2.8 HD tem vozes `Portuguese_*`; ElevenLabs também está lá), sem conta nova. Antes de usar nos vídeos: testar 1 voz, medir o custo real e mostrar a ele.
- **Mãos geradas por IA** nos vídeos de crescimento, com risco de deformar: só com o OK do Kevin em cada cena, no máximo 2 tentativas por cena, conferindo dedos e produto num quadro por cena antes de entregar.
- Continuam valendo: sem rosto, fidelidade à foto 01 (a mão nunca muda forma, cor ou quantidade de peças), sem álcool e nada além do anúncio.

## Formatos para crescer (produto fiel à foto real, câmera em movimento; mãos de IA só com OK por cena)
1. **Top 3 / ranking** do nicho (“3 coisas de cozinha que parecem inúteis e não são”), com número grande na tela.
2. **Comparação “qual é melhor?”**: dois itens lado a lado e voto nos comentários. Os comentários empurram o alcance.
3. **Série numerada** (“Parte 1/5”) com promessa no fim: “segue pra ver a parte 2”.
4. **Satisfatório / ASMR visual**: close, câmera lenta e som limpo.
5. **Antes e depois** de um canto da casa, só com imagens reais do anúncio.
6. **Curiosidade útil**: “você usa isso errado” e “isso tem uma função escondida”, só com fatos verdadeiros.
7. **Pet humor** (contas de pet): legenda engraçada sobre um objeto, sem animal gerado por IA deformado.

## Regras do roteiro viral
- Gancho em até 1 s: texto ≤ 6 palavras + movimento de câmera forte. Escreva 5 ganchos por vídeo e escolha o que passa no teste “eu pararia o dedo?”.
- 7-15 s. Um vídeo curto que é visto até o fim e repetido vence um longo.
- Loop: o último quadro emenda no primeiro.
- Pedir o seguir com motivo: “segue que amanhã tem a parte 2”. Nunca “segue aí” solto.
- Pergunta na legenda para gerar comentário. 3-4 hashtags de nicho, nenhuma genérica.
- Som em alta: o Kevin escolhe no app, no rascunho. A API não coloca música em alta, e é ela que dá alcance.
- Nada de promessa falsa, “clickbait” que o vídeo não entrega, conteúdo de outra pessoa ou música com direitos embutida no arquivo.
- As regras fixas do projeto valem aqui também: sem álcool, sem rosto (mãos de IA só com OK por cena), fidelidade à foto 01 e produto parado com a câmera em movimento.

## Ritmo por conta nova
3 a 5 vídeos por dia nas 2 primeiras semanas, em horários diferentes, cada um com gancho próprio. Repetir o formato que passou de 3× a média da conta. O mesmo vídeo nunca vai para duas contas.

## Métrica (o Analista lê)
Seguidores ganhos por vídeo e por mil views, retenção em 3 s, % que assistiu até o fim, compartilhamentos e comentários. View sozinha é vaidade.

## Ferramentas (2026-10-17; preço só depois de medir 1 cena, regra do projeto)
| Para quê | Ferramenta | Situação |
|---|---|---|
| Movimento de câmera na foto real | `mover_foto.py` (código) | Já temos, US$ 0 |
| Cenário e luz de cinema ao redor do produto | Seedream v4 Edit + Seedance 1.5 Pro (WaveSpeed) | Já temos, ~US$ 0,10 por cena de 5 s |
| Cena mais realista, com som nativo | Kling e Veo 3 (pela WaveSpeed) | Testar 1 cena e medir o custo antes |
| Narração em português | MiniMax Speech 2.8 HD na WaveSpeed (vozes em português; ElevenLabs também lá) | Liberada pelo Kevin; testar 1 voz antes de usar |
| Legenda automática da narração | Whisper (roda aqui, grátis) | Instalar quando houver narração |
| Música em alta | App do TikTok, no rascunho | O Kevin escolhe; a API não coloca |
| Tendências e ganchos do momento | TikTok Creative Center, FastMoss e Kalodata | Creative Center grátis; os outros dependem de créditos |
| Medir seguidores e retenção | TikTok API (`video.list`, `user.info.stats`) | Pedir na revisão do app |

## Fator interrupção e estranheza enigmática (Kevin, 2026-10-17: "o verdadeiro oceano azul", nível Hollywood)
O polegar para sozinho quando o cérebro vê algo que não bate com o que ele sabe do mundo. Os primeiros 2,2 s decidem o vídeo.
1. **Quadro 0 já é estranho.** Nada de "clima" antes: o primeiro quadro mostra a coisa impossível. Por isso a cena 1 sai de imagem conferida (imagem → vídeo), nunca de texto puro.
2. **Contradição que dá vontade de saber mais** (Kevin corrigiu em 2026-10-17: não é física impossível). Dois fatos verdadeiros que não combinam e que só uma história escondida explica: "Meu avô pescou 50 anos nesse rio e nunca trouxe um peixe pra casa." O cérebro precisa fechar a lacuna (Loewenstein) e só fecha assistindo ou seguindo. Dita até 2,2 s e escrita na tela no quadro 0.
3. **Contraste:** calma x ameaça, escuro x um único feixe de luz, velho x intacto. Um som seco no 0,0 s (pancada metálica, estalo) antes da voz.
4. **Simbolismo:** um elemento principal que significa mais do que é (caixa = segredo, cadeado = alguém quis esconder, rio = quem guarda e devolve). Ele aparece em todas as cenas e em todas as partes da série.
5. **Escalada:** cada cena soma uma pista que aumenta a pergunta sem responder. A resposta fica para a próxima parte.
6. **Hollywood no prompt:** fonte de luz motivada e única, lente e câmera de cinema (anamórfica, Alexa), grão de 35 mm, névoa volumétrica, cor teal e âmbar, 1 ação e 1 movimento de câmera por cena, som nativo desenhado (silêncio antes do susto).
7. **Fácil para a IA:** objetos rígidos e simples (caixa, cadeado), sem vara, linha ou carretilha (a IA solta a vara no ar), sem animais; mãos só de luva e saindo de imagem conferida.

**ABRAhub Studio (YouTube, títulos lidos em 2026-10-17; os vídeos pedem login, não foram assistidos):** os maiores são histórias com protagonista absurdo ("Esse Porco Me Gerou 1.311.213 Milhões De Views", "Como Fiz 4.649.232 Milhões de Views Com IA em 17 Dias"); títulos de contradição ("Essa Influencer Não Existe e Mesmo Assim Vende", "Isso Custa Milhões e Eu Faço Sozinho No Meu Quarto", "Disseram Que IA Não Faz Zoom. Então Eu Fiz Isso"); reação inesperada ("Essa Barista Não Esperava Por Isso"); cultura pop recriada (GTA, Backrooms, Copa 2026 "Vazou"); séries ("GTA V | A Série"). Ele também tem "Tik Tok Shop: O Jeito Mais Rápido De Conseguir 2.000 Seguidores". **O Farol** (@ofarolhub) tem só 3 shorts com menos de 1 mil views: nada para copiar ainda.

### Livros do fator interrupção (Kevin, 2026-10-17)
- **Tim Wu, The Attention Merchants:** atenção se colhe com novidade e com história em capítulos (folhetim, "continua amanhã"); o hábito de voltar vale mais que o susto. Uso: série com gancho no fim e horário fixo de postagem.
- **Martin Lindstrom, Buyology:** a decisão é inconsciente; neurônios-espelho (a câmera nos olhos de quem vive a cena), marcadores somáticos (um som que o corpo reconhece: lampião chiando, remo na água), rituais e mistério colam na memória mais que imagem bonita; susto vazio não fica. Uso: POV, 1 som-assinatura por série, 1 ritual repetido.
- **Robert Cialdini, As Armas da Persuasão:** autoridade (50 anos no rio), prova social, escassez de informação (só ele sabia, ninguém foi junto), afinidade e unidade (família, avô, rio nosso), compromisso (comentar o palpite prende à parte 2). Uso: 1 pergunta de palpite na legenda e na tela final.

## Como produzimos o vídeo viral 1 (Seu Barranco, Regra nº 1, 2026-10-17; modelo para os próximos canais)
- **Roteiro:** Kevin recusou contradição de física impossível (v2) e mistério lento (v3). Aprovou a v4: série de regras com uma regra contraditória dita em 2 s, autoridade, uma história com perda, um símbolo fixo (lampião aceso) e "regra 2 amanhã". Arquivo: `viral/pesca/roteiro_parte1.md`. Aula do ABRAhub (Protocolo Viral): fator de interrupção em menos de 2 s; estranheza só funciona com motivo; contradição = dois significados opostos no mesmo quadro (noiva de véu + trator na lama). Notas em `viral/abrahub/`.
- **Imagens:** Nano Banana 2.1 texto→imagem, US$ 0,036 cada, 9:16, base de prompt de cinema (Alexa, anamórfica, grão, névoa, teal e âmbar). Conferir cada imagem antes de animar; corrigir com Nano Banana edit (US$ 0,038) mandando a imagem como data URI.
- **Vídeo:** Veo 3.1 Lite imagem→vídeo, 720p, US$ 0,05 por segundo, som nativo, negative_prompt. Imagem como data URI funciona.
- **Voz:** MiniMax speech-2.8-hd, voz Portuguese_SereneElder, emoção neutral, cerca de US$ 0,11 por mil caracteres; 1 arquivo por cena. As reticências viram pausas longas: o montador encurta para 0,3 s (0,6 s nas dramáticas) e acelera 1,08×.
- **Edição (US$ 0):** `viral/pesca/edicao/montar_regras.py <roteiro.json> <saida.mp4>` (push-in por código, cor de cinema, grão, pancada grave no quadro 0, legenda palavra por palavra e carimbos em GSAP `camada_regras.html`, tela final no preto). Depois comprimir a cerca de 2,3 Mbps (8 MB) e entregar numa página com botão "Baixar vídeo".
- **Teto de gasto em código:** toda chamada paga passa por `viral/pesca/gerar.py ... --teto <lote aprovado> --max <chamada>`, que calcula o pior caso em `custo.py` (preço medido, unidade e tamanho da entrada) e recusa se passar. Modelo sem preço medido é recusado: medir antes um trecho curto com `--medir`.
- **Transcrição de graça:** faster-whisper (modelo small) roda aqui; hosts liberados: huggingface.co, us.aws.cdn.hf.co (usar `HF_HUB_DISABLE_XET=1`). Passar o áudio já decodificado (numpy), porque o PyAV instalado quebra.

## Aula do ABRAhub (Protocolo Viral), aplicada (resumo em `viral/abrahub/resumo_aula.md`)
- Quadro 0 = **contradição visual**: dois significados opostos na mesma imagem (noiva de véu + trator). Junto: **contraste** de sentimentos (fofo + perigoso, sagrado + comercial, luxo + decadência) e **símbolo** que aponta para uma emoção conhecida (poder, solidão, desejo, raiva). Estranheza sem significado = "mais um vídeo zoado de IA".
- **Estética travada por canal:** um bloco fixo de prompt (paleta, textura, lente, grão, luz) usado em toda imagem do canal, para o público reconhecer o perfil. Seu Barranco: o bloco base do roteiro v4 (Alexa, anamórfica, grão 35 mm, névoa, teal e âmbar, lampião).
- **Conceito com carona:** procurar o assunto do momento no nicho (FastMoss, Creative Center) e chegar com ângulo próprio.
- Nada de grupo de engajamento.

## Realismo extremo (Kevin, 2026-10-17)
"Cinematic film still, anamorphic, teal and amber" deixa a imagem bonita demais e com cara de IA. Usar o **código estético documental** de cada conta (câmera e lente reais, ISO alto com ruído, foco imperfeito, cor sem tratamento, enquadramento torto, luz só da fonte que existe na cena). O do Seu Barranco está em `viral/pesca/roteiro_v5_noiva.md`. Sempre mostrar as imagens paradas com a voz e a legenda ao Kevin antes de pagar a animação.

## Vídeo 2 "As moedas do meu avô" (2026-10-17)
- Página: (página do Kevin, não incluída) · 44 s · tela final "HISTÓRIAS DE PESCADOR TODOS OS DIAS" (Kevin: série diária, não semanal) · US$ 2,02 (pirarucu em Veo 3.1 Fast US$ 0,60, 2 cenas Veo Lite, 4 imagens Nano Banana Pro, voz MiniMax). Roteiro: viral/pesca/roteiro_v6_moedas.md; edição: viral/pesca/edicao/roteiro_moedas.json + camada_historia.html (legenda de 2 linhas: legenda_chars 30).
- GRÁTIS: Pruna demo (https://demo.pruna.ai, modelo p-video, Gradio). Imagem + prompt -> clipe de 8 s 720p sem custo: `gradio_client` -> Client("https://demo.pruna.ai/").predict(p=prompt, img=handle_file(png), a="9:16", api_name="/handler"). Termos (docs.api.pruna.ai/terms 6.1 e 11): o resultado é nosso, uso comercial ok; não apagar marca d'água/selo de origem (o p-video não traz nenhum). Pode sair do ar ou ter limite: teste, não dependência.
- Voz Senhor sereno é lenta: o roteiro de 22 s virou 44 s. Contar ~2,3 palavras/s ao escrever.
- Camada de texto: qtrle corrompia legenda com muitas mudanças (legenda presa/duplicada); render_regras.js agora usa -c:v png. Conferir sempre a folha de quadros.
- Ao alongar clipe por código com imagem: `-loop 1 -t N` + zoompan d=1 por quadro (d=96 por quadro de entrada gerou clipe de 406 s).
- PRÓXIMOS VÍDEOS TIKTOK (Kevin 2026-10-17 10:23): mais efeitos sonoros (som-assinatura, impactos, ambiente nos cortes) e mais elementos virais.

## REGRA DO DIRETOR E DO EDITOR (Kevin 2026-10-17 20:10, após o vídeo das moedas)
Kevin: "ainda está muito simples, falta animação, falta gatilho pra prender a atenção visualmente, falta movimento como filme real; está claramente uma foto encaixada em cima da outra, as cenas não encaixam; o barco parado no fundo não tem impacto."
1. Nada de foto parada com zoom em vídeo viral. Toda cena tem movimento real dentro do quadro (água correndo, linha esticando, objeto ou bicho em ação, chuva, luz que pisca) e câmera de filme (travelling, drone, câmera na linha d'água, seguindo a ação). Zoom por código só como último recurso, e nunca na abertura.
2. Os 2 primeiros segundos são o quadro mais extraordinário do vídeo: ação em andamento, algo que o espectador nunca viu e precisa decifrar (a contradição está NA IMAGEM, não só na fala).
3. As cenas encaixam como um filme: o mesmo personagem (de costas), a mesma canoa, a mesma luz e hora, e a mesma tempestade em toda a sequência; a direção do movimento continua de um corte para o outro (raccord). Cortes no movimento, não em quadros parados.
4. O roteiro nasce da imagem: primeiro a sequência de planos com ação, depois a fala que encaixa nela. A história tem que pedir movimento (perseguição, fuga, algo puxando, algo surgindo).
5. Design de som em toda cena (Kevin 10:23): água, vento, trovão, madeira rangendo, carretilha gritando, pancada grave nos cortes de impacto, silêncio antes da virada.
6. Antes de entregar, o diretor assiste à folha de quadros e pergunta: "algum plano parece foto?" Se sim, refaz.
- Pruna só com texto (sem imagem) NÃO serve para ação: o modelo de texto dele reescreve o pedido para "static camera, subtle movement" e trocou a noite e a canoa arrastada por um homem remando de dia (teste v7/p1.mp4, 2026-10-17). Use o Pruna só animando uma imagem nossa; ação forte vai no Veo.

## FÓRMULA FIXA DO SEU BARRANCO (Kevin 2026-10-17 20:51: "essa será nossa arma")
Todo roteiro junta três coisas: **mulher bonita e atraente** (Luana e outras personagens IA, roupa de rio e biquíni), **pesca** e **história de pescador ou lenda** (Nego d'Água, Poço do Velho, avô Seu Barranco). Objetivo: dopamina contínua do primeiro ao último segundo.
Mecânica da dopamina (livros):
- Antecipação > recompensa (Lindstrom, Buyology; Sapolsky): prometer algo no 1º segundo e entregar aos poucos.
- Recompensa variável (Eyal, Hooked; Wu): a cada 3-5 s um pico novo e imprevisível (beleza, ação, susto, achado, risada da lenda).
- Lacuna de curiosidade (Loewenstein) e Zeigarnik: um laço aberto que só a parte 2 fecha; séries numeradas.
- Atração e simpatia (Cialdini): olhar e fala direto para a câmera, intimidade ("você aí", "fica comigo").
- Carona de conceito (ABRAhub): lendas e temas já virais no TikTok, com o nome no 1º segundo e nas hashtags.
- Virada de expectativa (Heath): o espectador espera uma coisa, recebe outra e comenta.
Limites que mantêm o alcance e a conta: câmera na ação e no rosto, nunca zoom ou câmera lenta no corpo; nada de nudez nem promessa de tirar a roupa; rótulo de IA ligado; personagens adultas; sem álcool.
Roteiros de referência: viral/pesca/roteiro_v10_mergulho.md (aprovado), pesquisa de realismo em viral/pesca/pesquisa_realismo_luana.md.

## Custo: travar o visual antes das cenas (Kevin 2026-10-18, "custo bem alto, à toa")
O mergulho proibido gastou US$ 2,00 só em imagens: 6 rodadas de 8 cenas porque corpo, pele e roupa mudaram a cada revisão. Regra: primeiro 1 retrato com rosto, corpo E roupa final aprovados (US$ 0,03 por tentativa), só depois as cenas. Animação: Pruna grátis primeiro; pago só com OK dele na hora.
