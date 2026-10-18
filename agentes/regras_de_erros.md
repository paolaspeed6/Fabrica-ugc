# Regras para não repetir erros. Ler antes de QUALQUER roteiro, prompt, geração ou edição.
a dona, 2026-10-15/16: "tenha certeza que não repetiremos nem os mesmos erros de geração, nem de edição". Atualizado em 2026-10-16 com a revisão dos 22 produtos da lista1015.

## 0. Decidir cena por cena ANTES de gastar (o erro que mais custou)
Na lista1015 muitas cenas de IA pagas foram jogadas fora e trocadas por foto real. No roteiro, cada cena já sai marcada:
- **CÓDIGO** (foto real do anúncio com zoom/pan por ffmpeg, US$ 0) é o padrão. Obrigatório para: produto com letras, logo, painel, botões ou números; produto estrutural (prateleira, mesa, estante, móvel, máquina, eletrodoméstico); tecido com estampa; close de mecanismo (sapata, dobradiça, parafuso, encaixe).
- **IA** (Seedream + Seedance) só para cenário sem o produto, ou produto liso e sem letras quando a foto 01 dá recorte limpo. Sempre com custo máximo dito antes e OK da dona. Antes de animar: `--so-imagens`, conferir contra a foto 01, `"imagens_conferidas": true`.
- Nunca pagar uma cena que o código consegue fazer. No máximo 2 tentativas por cena; corrigir o prompt antes de refazer.

**Produto parado, câmera em movimento (regra, 2026-10-17, vale para 100% dos vídeos):** o produto nunca se move, gira, abre, balança ou muda de lugar; quem se move é a câmera (aproximação, deslize lateral, subida, arco curto). Nas cenas por código o quadro inteiro se move junto, como uma câmera real. Nas cenas de IA o prompt descreve só o movimento da câmera e diz que o produto fica completamente parado no lugar; nenhuma ação física no produto (tecido balançando, gaveta abrindo, vapor saindo do produto). O que se mexe é só a luz ou o ambiente, e só se for natural.

## 1. Erros de geração que já aconteceram
| Erro | Onde | Regra |
|---|---|---|
| Letras tortas ou inventadas ao animar | Shopito, solda Coban, bike, capacete espelhado | Letras nunca passam por IA |
| Produto muda de forma, desmonta e remonta | Aço 30 cm, Metal Decore, kit prateleira, ZIG | Estrutura só por código |
| IA inventa peças | parafusos na mesa Yon e na sapata da escrivaninha, 2ª cabeça na escova, viseira camaleão | Close de detalhe só com foto real |
| Objetos que andam ou surgem | planta andando e celular no ZIG, garrafas atrás da poltrona | Cena sem objetos soltos; descrever só o que existe; nunca citar o proibido, nem negando |
| Lado errado | pegador da churrasqueira, frente inventada no capacete | Nunca espelhar foto; manter o lado da foto 01; arco de no máximo 15-20° e só para lados que o anúncio mostra |
| Cor ou variante errada | poltrona bege em vez de azul | Cor, tamanho e voltagem sempre da foto 01 |
| Mão, celular, pessoa ou texto grande na foto da galeria | seladora, solda Centurion, escrivaninha, estante | Não usar como cena; recortar só a parte limpa |
| Zoom cortando o produto no take 1 | areia, mesa | Take 1 com produto inteiro, zoom de no máximo 1.06 |
| Moldura de celular, faixas brancas | escova, poltrona | "Photorealistic full-frame photo"; conferir as bordas |
| Quantidade errada de partes (6 andares em vez de 5) | estante de aço 198 cm q19, cena de IA da garagem (regra, 2026-10-17: "tira nossa monetização") | Contagem obrigatória: ver seção 1.1 |
| Preço diferente da tabela | Kling cobrou por segundo (US$ 0,56 o clipe) | Medir 1 cena pelo saldo antes de usar modelo novo |
| Vara solta no ar e mão e pés que não foram pedidos | Veo 3.1 Lite texto→vídeo, cena 1 do canal de exemplo (2026-10-17) | Na IA, nada de vara, linha ou carretilha; cena com pessoa ou objeto fino sai de imagem conferida (imagem→vídeo) com negative_prompt; conferir 4 quadros antes de usar |
| Cobrança por segundo não medida | Whisper turbo da WaveSpeed: preço de tabela 0,0007 era POR SEGUNDO; 10 min de áudio custaram US$ 0,42 com máximo dito de US$ 0,05 (2026-10-17), e ele corta em 600 s | Antes de modelo novo, rodar um trecho curto (30 s) e medir pelo saldo; só então calcular o máximo |
| Recipiente aberto mostrou latas (parece bebida) | isopor da cena 4 do canal de exemplo (2026-10-17) | Recipiente sempre fechado na imagem (tampa fechada e amarrada); conferir o que aparece dentro de qualquer caixa, cesto ou isopor |
| Passou do máximo dito à dona | 3 vozes custaram US$ 0,057 com máximo de US$ 0,05 (texto mais longo que o previsto, 2026-10-17) | O máximo dito é teto duro: dimensionar texto, cenas e refações para não passar; se for passar, perguntar antes |

### 1.1 Contagem de partes (regra, 2026-10-17)
Produto diferente do anúncio derruba a monetização. Toda parte que se conta é conferida pelo número, não pelo "parece igual".
1. **Antes do roteiro:** escrever no JSON `"contagem": {"prateleiras": 5}` (andares, prateleiras, tábuas, gavetas, portas, nichos, pés, rodas, anéis, lâmpadas, peças do kit, unidades), tirada do título, da descrição e da foto 01. Se os três discordam, vale a foto 01 e o número sai do texto da tela.
2. **Produto com partes repetidas (prateleiras, gavetas, anéis, kits) é CÓDIGO sempre**, nunca imagem nem animação de IA, porque a IA soma ou tira níveis. Cena de IA só pode mostrar o cenário vazio, sem o produto.
3. **Foto da galeria só entra se mostrar a mesma contagem da 01** (galerias misturam variações de 4, 5 e 6 andares).
4. **Conferência:** em 1 quadro de cada cena de cada versão, contar as partes e anotar na folha "cena N: 5 prateleiras, ok". Qualquer diferença reprova o vídeo antes da entrega.

### 1.2 Pruna p-video (animação grátis, lista1017, 2026-10-17)
Em 57 cenas: a câmera avança rápido (em 3-4 s já corta o produto) e o LLM do Pruna reescreve o prompt por conta própria. Erros vistos: apresentadora ou pessoa entrando na cena (8 cenas, quase sempre em foto de fundo branco), corte ou fusão para outro produto ou objeto (vaso, outro lustre, outra mesa), luz do produto mudando de cor, tecido balançando, bordado e estampa redesenhados no close, 4º pé no tripé, purpurina dourada no ar, "luz do sol" deixando cortina branca dourada depois de uns 3,5 s (s26 cena 3, cortada em 3,0 s).
- Foto de fundo branco ou estúdio: não usar no Pruna (vira comercial com pessoa). Só foto de ambiente real.
- Conferir 4 quadros por cena (0,1 / 1,8 / 3,6 / 5,3 s) contra a foto 01 e contar as partes; usar só o trecho limpo do início com `video-teste/pruna/aprovar.py sNN K <segundos>` (estica com interpolação para 5,6 s), `ok` ou `codigo` (volta para zoom na foto real).
- Cena 1 com produto inteiro: quase sempre só os primeiros 1,6-2,2 s servem.


### 1.3 Seedream: cenas originais (lista1017b, 2026-10-17)
- Tapete largo (3 x 2 m) em foto vertical 9:16 virou passadeira comprida e estreita duas vezes, mesmo com "3:2, never a narrow runner". Tapete largo: cena de cima (top-down) ou o tapete só em parte do quadro, e conferir a proporção contra a foto 01.
- Preço medido: US$ 0,027 por foto (11 fotos = US$ 0,297 no saldo).
- Medida em número no prompt ("25 cm", "80 cm") faz o Seedream desenhar linhas e rótulos de medida na foto (t09, t16, t18). Escreva o tamanho só por comparação ("do tamanho de um prato", "mais estreito que a mesa") e diga "no measurement lines, no dimension labels".
- "straw-beige" (cor palha) virou cúpula de juta/palha trançada duas vezes (t03): use a cor sem a palavra do material ("pale sand-beige smooth fabric").
- Tapete largo continua virando passadeira em 9:16 mesmo de cima ou atravessado: gerar tapete em formato quadrado (1440*1440) e montar como foto quadrada.
- Lustre plafon (preso no teto) ganhou haste/cabo; diga "mounted flush directly against the ceiling, no rod, stem or cable". Kit de 1 peça virou 2: "Only ONE single chandelier".
- 3ª tentativa (2026-10-17 20:27, US$ 0,43): cenas 1 e 2 em quadrado 1440 saíram certas (tapete largo, cúpula lisa, espiral). As CENAS DE USO de tapete voltaram a virar passadeira e algumas saíram em fundo branco infinito (sem cômodo); lustre plafon ganhou haste de novo; kit de 2 plafons ganhou 2 arandelas; cortina branca virou bege; uma cena saiu dentro de moldura de celular. Regra: cena de uso só para produto em pé ou pendurado que a pessoa toca (luminária, cortina); tapete e plafon ficam sem pessoa. Após 2 falhas, recorte grátis de uma foto aprovada do mesmo produto, nunca 3ª geração.
- Conferir também o pescoço/haste das luminárias de pé contra a foto 01 (t03: cena de uso com haste cromada longa passou na 1ª conferência e estava errada).

## 2. Produtos novos (cortina, lava e seca e afins)
- **Cortina, tecido estampado, roupa de cama, tapete:** cor, transparência (voil x blackout), estampa, ilhós ou varão e barra iguais à foto 01. A IA redesenha estampa e muda o caimento, então as cenas são por código. Movimento de tecido por IA só com OK, só em tecido liso. "Blackout", medidas e "corta luz" só se o anúncio diz; medida que se contradiz entre título e descrição não entra.
- **Lava e seca, máquina, eletrodoméstico, eletrônico:** painel, marca, botões e números são letras, então só código. Nada de roupa, água ou espuma gerada no tambor. Porta abrindo para o lado da foto. Capacidade (kg) e voltagem só se o anúncio confirma para a variação da foto 01.
- **Qualquer produto com variações:** só a variação da foto 01.

## 3. Roteiro e texto
1. Gancho de até 6 palavras, condizente com o produto e provado pelo anúncio; número grande quando houver.
2. Nunca prazo de entrega. Preço só se conferido no dia da postagem.
3. Detalhes-chave (unidades, medida, kg, voltagem) grandes na tela.
4. Por produto: 3 Shopee + 1 Reels, cada um com gancho e CTA próprios, sem repetir frase.
5. Legenda Shopee: 1 linha (nome + 2 fatos do anúncio) + 4 hashtags de nicho, nenhuma genérica (#achadinhosshopee saiu em 2026-10-16). Reels: gancho + "Link do produto: <link>" na própria legenda.

6. Cada afirmação na tela ou na legenda (número, material, recurso, cor) tem que estar ESCRITA no título ou na descrição do anúncio; nome de modelo não é recurso ("Starry" virou "projeta estrelas" na lista1016, a dona 2026-10-16). Cor só a que a descrição confirma, nunca deduzida de foto com luz colorida. Antes de renderizar, rodar a checagem de números e termos contra o anuncio.json.
7. **Nota e avaliações nunca em número exato** (regra, 2026-10-17: mudam com o tempo). Use "bem avaliado", "nota alta", "aprovado por quem comprou", "milhares de avaliações" (só se o anúncio tiver mais de 1.000). Vale para a tela, o selo e as legendas. O selo do cartão vira palavra, ex.: `{"n": "TOP", "t": "avaliado"}`. O `fazer_lista.py` bloqueia o render se achar nota ou avaliação exata (`video-teste/sem_nota.py`).
8. **Superar as referências, não igualar** (a dona, 2026-10-18: "deverá ser superior a essa qualidade, com pensamento próprio na edição, criatividade e auto aprimoramento"). Os 16 vídeos de `referencias/` reprovaram em `video-teste/auditar_video.py`: capa (1º quadro) sem gancho nos 16; cenas quase paradas (zoom de foto); fusão com dupla exposição de 0,5 a 0,7 s; todos mudos. Todo vídeo novo passa nessa auditoria (o `fazer_lista.py` grava `auditoria.txt`) e o QC olha também: um detalhe criativo próprio do produto por vídeo (não só trocar a cor do mesmo molde), corte seco ou transição com motivo, nada de repetir o mesmo gancho entre produtos.
9. **Nunca editar sem a fábrica carregada** (a dona, 2026-10-18: edição da poltrona feita sem as regras saiu com texto estilo sticker, pílulas e emoji, reprovada). Antes de editar: CLAUDE.md, regras e `memoria/edit-templates.md`; usar os layouts da fábrica.
10. **Nunca recolorir o produto por máscara de cor** (HSV + ffmpeg): a poltrona verde→laranja saiu com pixels bugados, reprovada. Trocar cor só editando a imagem a partir da foto do anúncio na cor certa (custo dito antes).
11. **Só qualidades de verdade nos ganchos, listas e narração** (a dona, 2026-10-18: "fala sobre linhas retas, mas isso não é uma qualidade exatamente"). Característica neutra não é benefício: "linhas retas", "formato quadrado", "cor bege", "tem 4 pés" etc. NÃO entram como qualidade. Use só o que o comprador percebe como vantagem e o anúncio comprova (conforto, material, acabamento, medida útil, facilidade de montar/limpar, versatilidade de uso). Na dúvida, troque por onde usar ou pelo efeito no ambiente. O roteirista e o QC conferem item por item antes de gerar a voz.
12. **Rodízio do take inicial** (a dona, 2026-10-18): as 3 opções de um mesmo produto começam cada uma com um take DIFERENTE (outra cena/ângulo no 1º quadro). Conferir na timeline antes de renderizar.

## 4. Edição
1. Take 1: produto inteiro, limpo, nada cobrindo.
2. Texto nunca cobre o produto: contact sheet com início, meio e fim de cada cena das 4 versões, olhar um por um antes de dizer que está pronto.
3. Letras não se sobrepõem; vírgula decimal (4,87) não quebra a linha.
4. Layouts (regra, 2026-10-16): Shopee 1 = faixas (`reels_faixas`); Shopee 2 = letras grandes no topo, produto entre título e botão (`tiktok_b`); Shopee 3 = cartão escuro com selo (`reels_cartao`); Reels = faixas com "Link na legenda". Vitrine aposentada. Builder: `video-teste/fazer_b.py <qNN.json> <saida> --render`.
5. Título branco em fundo claro some: o `tiktok_b` usa degradê do topo forte (950 px, alfa 225); conferir legibilidade em produto branco.

## 5. Operação
1. Render longo: Bash com run_in_background (o sistema acompanha). nohup/setsid morreram entre turnos em 2026-10-16 e perderam 1 hora.
2. Loop `while read`: `read -u 3 ... 3< lista` e `< /dev/null` no comando, senão o ffmpeg come a lista.
3. `timeout -s KILL` por produto; conferir progresso a cada poucos minutos. 2 renders por vez (4 CPUs), cerca de 4 min por produto.
4. Não usar `pkill -f`; `TETO_LOTE_USD=0` quando só renderizar.
5. Página Vídeos Prontos: armazenamento de 1 GB; apagar as versões substituídas (com OK da dona) antes de subir as novas. O nome do arquivo baixado precisa terminar em `.mp4`.
