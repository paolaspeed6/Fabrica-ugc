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
- **Prompt que resolve (2026-10-18, imagem original do Nano Banana):** "The camera stays at the same distance the whole time and drifts very slowly a few centimeters to the right with a gentle natural hand sway. The whole <produto> stays fully visible in frame from <base> to <topo> for the entire clip. The <produto> and the room stay completely still... Nobody enters the frame." Deu 8 s limpos, sem avanço, sem pessoa, sem redesenho. Pedir "push-in" ou "close" faz o Pruna avançar até o detalhe e redesenhar.


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
13. **Produto inteiro no 1º take (capa/thumb)** (a dona, 2026-10-18): o primeiro quadro de TODO vídeo mostra o produto inteiro (sem cortar topo, pés ou laterais) e sem mão/pessoa. Close só depois. Conferir na prévia do t=0 antes de renderizar; vale junto com a regra 12 (cada opção abre com um take diferente, mas sempre com o produto inteiro).

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

## Regra 14 — logo distorcido pela IA e mão escondida no meio do take (2026-10-21)
Takes de IA (Veo/Hailuo) costumam deformar o LOGO no close (ex.: "TOYAIMA" em vez de "Toyama") e a mão pode
continuar no quadro mais tempo do que a tira de 1 quadro/s mostra. Antes do roteiro: tira a cada 0,5 s do
trecho de close, ler o logo; usar só trechos com logo certo e sem mão. Marca d'água "MiniMax/Hailuo" no canto
de baixo: cortar (crop 714x1270 + escala) antes de editar.

# Regras vindas do kit do Kevin (importadas em 2026-10-24; numeração com prefixo K)
Valem aqui também, quando o assunto aparecer (vídeo do zero, provador, Nano Banana, Wan, TikTok).

## K6. Vídeo com pessoa (TikTok Shop, provador IA, 2026-10-20)
- Seedance 1.5 imagem→vídeo com gestos de prova de roupa saiu com 3 braços e movimento só ~20% fiel (Kevin). Gesto de mão no tecido não sai de prompt: precisa de vídeo-guia (motion control).
- Antes de entregar qualquer vídeo com pessoa: contar braços, mãos e dedos em quadros a cada 0,5 s; giro de corpo muda o formato do corpo, cortar ou evitar.

- Vestir a modelo (Nano Banana, Kevin 2026-10-21): a 1ª geração afinou quadril, curvas e busto e afastou a câmera. Todo prompt de vestir leva: "exactly the same body proportions as image 1, pixel-aligned: same bust size and shape, same narrow waist, same wide curvy hips, same thighs and legs; do not slim, shrink or reshape any part of her body. Keep the exact same framing, zoom and camera distance as image 1". Saia/vestido: "not flared or puffy, follows the hip line of image 1". Antes de mostrar ao Kevin, comparar lado a lado com modelo_base_rosa.jpg (busto, cintura, quadril, coxas, altura dos pés); se mudou, não mostrar como pronto.

- Vídeo Wan (Kevin 2026-10-21): (a) inventou boca/queixo porque o guia enquadrava mais aberto que a foto base; antes de enviar, cortar e ampliar o guia para o mesmo enquadramento da base (pescoço no topo, sem cabeça) e conferir que nenhum quadro final mostra rosto; se aparecer, cortar o topo por código. (b) entortou a parede/batente da porta: paredes, batentes e colunas ficam retos; prompt pede "static background, perfectly straight vertical door frame and walls" e conferir linhas retas a cada 0,5 s. (c) Sem frase gravada no vídeo; frase só na página para copiar. (d) Alternar acessórios femininos e delicados entre produtos (pulseira fina, colar delicado, relógio fino dourado/prateado).

- Referência da roupa (Kevin 2026-10-21): NUNCA mandar a foto inteira da modelo do anúncio como imagem 2; o editor copia o corpo dela (o 12 perdeu coxas, busto e quadril). Recortar por código só a peça (close de cada parte, pouca pele) e dizer no prompt que a imagem 2 é só detalhe da peça e que o corpo dela deve ser ignorado. Biquíni: Nano Banana recusa vestir a partir da base; vestir no Seedream v4 edit (size 1152*2048) e depois corrigir o corpo no Nano Banana editando a vestida com a base como imagem 2 ("change only her bust size to match image 2"), que ele aceita. Base atual: tiktok-provador/modelo_base_cabelo_longo.jpg.

- Vídeos Wan do lote 21/10 (Kevin): o Wan copia TUDO do guia, inclusive tapa, pisão, dancinha e giro rápido (2, 3, 8, 9, 10, 11). Antes de usar um guia, ver a 4 qps e cortar só trechos limpos (sem tapa, pisão, dança, giro rápido, aceleração). Guia com enquadramento mais fechado (legging, short_saia) dá zoom e esconde o conjunto: usar só guia de corpo inteiro na mesma distância da base. Trecho bugado: cortar na edição e fechar em loop (ida e volta). Fórmulas virais (agentes/viral.md) valem só para frase e legenda, nunca para o prompt da roupa.

- Edição dos vídeos do provador (Kevin 2026-10-21 08:11): NUNCA loop de ida e volta (reverse parece bugado). Trecho ruim (tapa, coçar, pisão, dança, giro rápido) sai com corte seco, só para frente. Corte de topo mínimo: 0% quando o rosto não aparece, 6% quando aparecem queixo ou boca; metade do pescoço e os ombros sempre visíveis (corte de 12% virou zoom e escondeu os ombros). Conferir faixa do topo a 1 qps antes de entregar.

## K7. Revisão da Lista 1020 (Kevin, 2026-10-21)
- **Sem demonstração de uso** (fatiar, cortar, parafusar) a não ser que a IA faça com perfeição; quase sempre buga.
- **Seedance:** o prompt pede produto parado e só movimento de câmera. Aproximação ou push-in sobre letras pequenas é só por código, nunca na geração.
- **Cortar todo trecho** em que o produto desliza, gira, se mexe sozinho ou em que surge objeto (queijo, presunto). Reaproveitar o começo limpo (ida e volta) ou outra cena boa do mesmo produto.
- **Letras pequenas** (autoclave, chaves de impacto, perfume, ar-condicionado): recorte da foto do anúncio sobre o ambiente gerado; só o ambiente passa pela IA.
- **"Um dia com ela" só quando o produto encaixa de verdade em manhã, tarde e noite** (deu certo no kit salão Dompel). Se não encaixar, plano B: o mesmo layout sem horários, com poucas palavras ou nada escrito. Nunca inventar horário sem sentido (gaiola "de manhã no bebedouro", fechadura "horário para abrir").
- **Filtro de cor mais leve:** a poltrona bege ficou mais amarela que o anúncio.
- **Take 1 mostra todos os itens inclusos da foto 01** (cesto e frasco da cuba, acessórios da gaiola), nem que seja ao lado, soltos.
- O produto segue a foto 01 em todo quadro (puxador da fechadura mudou entre quadros).

- (Kevin 2026-10-21) Todo vídeo do provador precisa ter o giro de quadril mostrando as costas da peça. Escolher só guias com "giro de costas" dentro da janela limpa (sem tapa, pisão, coçada). Se o defeito do guia cair justo no giro, trocar de guia antes de gerar, porque a edição não consegue criar o giro depois.

- (Kevin 2026-10-21, autoclave Liz) Produto com letras pequenas: NUNCA colar só o rótulo/letras da foto 01 sobre o produto gerado (desalinhou e bugou o vídeo). Recortar o PRODUTO INTEIRO da foto 01 (fundo removido com rembg isnet-general-use, só o maior pedaço) e colar sobre o produto gerado em todos os quadros: lista1020/correcoes/recorte_inteiro.py (SIFT + só escala/giro/deslocamento, suavizado). Usar só o trecho em que a câmera fica de frente; em arco lateral aparece o produto gerado por trás (fantasma) e é preciso cortar antes.

## K8. Lista 2110 (Kevin, 2026-10-22)
- **Enquadramento:** o Nano Banana ignora "% da altura" no prompt. Usar a imagem-guia (`lista2110/layout.py`): recorte da foto do anúncio já no tamanho e lugar finais (y 0,37 a 0,67) e o NB só troca o fundo.
- **Produto se mexendo:** mesmo com "parado" no prompt, em 8 de 9 clipes do Seedance o produto se mexeu depois de 0,5-1,5 s (base da cadeira girou, cabo surgiu, tela mudou). Rodar `video-teste/checar_movimento.py` em todo clipe e usar só o trecho limpo. Câmera calma: sem arco, só avanço leve com pequeno deslize.
- **Letras miúdas:** o Seedance reescreve letra que não entende (ACQUAPURE virou letras aleatórias, marca Electrolux ilegível). Regra do Kevin: melhor nada escrito que letra errada. Apagar as letras miúdas da imagem ANTES de animar (`lista2110/sem_letras.py`). Não resolver colando recorte em todos os vídeos.
- **Sem uso do produto:** a IA gerou o purificador soltando água (aparência gelatinosa). Nada sai, escorre ou aparece; só a câmera se move.
- **Não inventar detalhes:** nenhuma peça, botão, cabo ou acessório que a foto 01 não mostra. Conferir cada imagem contra a foto 01 antes de animar.

### K8.1 Produto travado (2026-10-22)
- Prompt calmo, camera_fixed e last_image NÃO impedem o Seedance de girar ou deformar o produto (cadeira girou nos três). Padrão: seedance.py com FIXA=1 (câmera parada, luz constante, "nada novo aparece") + fixar.py (produto e margem vêm do 1º quadro em todos os quadros, com brilho ajustado ao entorno). O movimento de câmera vem do montar.py (aproximação + deslize).
- Conferir cada clipe travado por imagem: objeto novo surgindo no cenário (ex.: planta que nasce no fundo) reprova a cena.
- Produto alto (cadeira, gaiola): o Nano Banana às vezes ignora o tamanho do guia. Medir com caixa.py e olhar; refazer com "wide shot from across the room, product small in the middle of the frame".
- Ao refazer uma imagem de cena, APAGAR <cena>_orig.jpg e <cena>_letras.png antes de rodar o sem_letras.py de novo: ele parte do _orig e devolve a imagem antiga por cima da nova (Lista 2110: p12 B/C e p13 B foram animadas com a imagem errada).
- (Kevin 2026-10-22 05:54, revisão do grupo A) **Colar o produto do 1º quadro por cima (fixar.py) NÃO passa naturalidade**: sombras girando em ventilador parado, ferro vizinho acompanhando o giro da imagem, recorte "duro" sobre produto que já existe na cena. Ele prefere a versão original da IA. Padrão novo (seedance.py TRAVAR=0): câmera parada na IA, sem colagem; conferir 4 quadros e usar só o trecho limpo, ou outra cena do mesmo produto. Detalhes que bugam (controle, microfone, mouse que desliza) saem pelo corte.

### K8.2 Revisão do Kevin, Lista 21/10 A (2026-10-22 05:54)
- Recorte por código colado por cima de um produto que JÁ existe na cena não funciona: não fica natural (monitor 01 e purificador 09 voltaram aos clipes originais da IA e ficaram "mais postáveis"). Não usar recorte_inteiro.py por cima de cena gerada.
- Trava do produto (fixar.py): a máscara pega TODAS as partes grandes (kit com microfones e controle, encosto de cabeça). Peça fora da trava se deforma.
- Apagador de letras (sem_letras.py) em peças pequenas (microfone, controle) deixa a peça "bugada". Com o produto travado as letras não se deformam, então trave com a imagem original: fixar.py ... --fonte <C>_orig.jpg (as letras vêm da foto real pelo Nano Banana). Só apague se a letra do Nano Banana já sair errada.
- Marca do produto tem que aparecer no 1º take (monitor 11 ficou sem a marca HQ porque o apagador tirou).
- Ventilador travado com sombra das pás girando na parede fica incoerente: no prompt do ventilador, sem sombras de pás nem movimento de ar.
- (Kevin 2026-10-23, Lista 22/10 A) **Hélice girando é permitido nas próximas gerações** e melhora a estética: ventilador ligado com as pás girando pode ficar no trecho usado. Só o resto não pode bugar: grade, logo, formato, base e cor iguais à foto 01; corte o trecho quando a grade ou o logo deformarem. Vale para gerações novas, não para refazer vídeos já entregues.
- Ferro, cano ou objeto colado ao produto e fora da trava "acompanha" o produto de forma estranha: cenário sem objetos encostados no produto.
- (2026-10-22, grupo B) O prompt FIXA antigo citava "plant leaves or curtains" e "no sun patches"; sem o fixar.py por cima, o Seedance CRIOU plantas, cortinas e manchas de sol (p18, p21, p23). Regra 1 vale também para o prompt de vídeo: nunca citar objeto ou efeito que não está na imagem. Mesmo com o prompt limpo e camera_fixed, 3 de 3 testes giraram a cadeira, aproximaram a câmera ou criaram sol depois de ~1 s.
- Com a imagem-guia (layout.py), NÃO somar "wide shot from across the room": o produto saiu pequeno e baixo (p19, p25).
- (Kevin 2026-10-22 07:48) **Purificadores e produtos com letrinhas de marca: recorte da foto do anúncio colado por cima do produto gerado, um pouco MAIOR (~5%) para esconder as bordas** (lista2110/colar_recorte.py para clipe parado; lista2110/colar_anuncio.py quando a IA move a câmera: segue o produto por fluxo óptico. O SIFT do recorte_inteiro.py não casa com purificador preto e falhou). Fidelidade à 1ª imagem é a prioridade. Para os próximos: gerar o cenário já pensando no recorte.

## K6.x Penalidades do TikTok (Kevin 2026-10-22: conjunto azul lote1021 p01 e calça moletom lote1022 p04)
Diretriz do TikTok ("conteúdo sexualmente sugestivo"): proíbe "enquadramento sexualizado" e foco em partes íntimas (seios, nádegas, virilha). O que nossos dois vídeos tinham:
- Corte sem rosto que deixa o decote no topo do quadro, então o peito vira o assunto da cena (p01, 0-1 s).
- Mão alisando a barriga ou encostando no peito (p04, uns 6,5 s, mão sobre o seio).
- Perfil lateral lento que destaca o bumbum.
- Pessoa realista feita por IA postada sem o rótulo "Conteúdo gerado por IA".
Regras a partir de agora:
1. Ligar SEMPRE o rótulo "gerado por IA" ao postar (avisar o Kevin na página de cada lote).
2. Enquadramento de corpo inteiro, câmera na distância do provador; o topo do quadro corta no queixo ou no pescoço e nunca deixa o decote como primeira coisa da cena; sem zoom no peito ou no bumbum.
3. Guias: nada de mão no peito, barriga, quadril ou bumbum; nada de alisar o corpo. Só ajeitar a roupa (barra, alça, cós) e giro de costas rápido e natural, sem pose de perfil empinada.
4. Peças decotadas ou curtas: o prompt de vestir não aprofunda o decote; preferir o primeiro segundo com a roupa toda de frente.
5. Frase e legenda falam da roupa (tecido, caimento, ocasião), nunca do corpo.
Antes de entregar: conferir quadro a quadro (1 por 0,5 s) contra os itens 2 e 3.
Motivo real (Kevin 2026-10-22 22:06): "Promoção de produto inconsistente: seu vídeo parecia conter informações inconsistentes com os produtos vendidos." A punição veio logo após postar, pela revisão automática, e a apelação foi negada. Correções:
6. Mostrar só o que o anúncio vende. Peça complementar (top preto com a calça, short com o top) parece um conjunto vendido junto. Se for preciso cobrir o corpo, usar complemento discreto e neutro e deixar claro na legenda "vendido: só a calça", ou escolher anúncios de conjunto.
7. A peça tem de ser idêntica à foto 01: cor, altura da cintura (a calça do anúncio é cintura baixa com cordão e a nossa saiu cintura alta), largura da perna, barra, recortes e alças. Comparar lado a lado antes de animar.
8. Frase e legenda: só fatos do anúncio, com o mesmo nome da peça do título.
9. Rótulo de IA sempre ligado (pessoa realista feita por IA).

## K9. Quantidade de itens da foto 01 (Kevin 2026-10-23 04:54)
Erro: Zeblaze Stratos 4 Pro (Lista 21/10 B, p29). A foto 01 mostra 2 relógios (2 modelos) e o vídeo mostrou só 1. Kevin não pode postar; vídeo perdido e produto de volta à Fila.
Regra: se a foto 01 mostra 2 ou mais itens ou modelos, TODAS as cenas e versões mostram todos eles, na mesma quantidade e disposição. Antes de gerar, contar os itens da foto 01, escrever a contagem em "contagem" do produto e usar layout.py --todos (recorte de todos os itens). Antes de animar, conferir a imagem gerada contra essa contagem.
Toda regeneração paga e toda perda entra em agentes/desperdicios.md.

## K10. Escala real do produto (Kevin 2026-10-23 05:25)
Erro (Lista 21/10 B): Kit 6 Cadeiras Roma (p30) saiu com cadeiras em miniatura e o PC Gamer Ryzen 5 completo (p32) saiu em miniatura; os dois foram descartados e voltaram à Fila. O Bebedouro Industrial HIZA 25 L (p33) também saiu pequeno demais (Kevin postou mesmo assim).
Causa: layout.py encaixa o recorte na faixa fixa y 0.38-0.66 do quadro. Com vários itens (--todos) ou produto grande, isso encolhe tudo e o cenário em volta vira de brinquedo (mesa, porta e piso fora de escala).
Regra: o produto aparece no tamanho real do mundo. Uma cadeira tem tamanho de cadeira, um gabinete de PC tem tamanho de gabinete e um bebedouro industrial é alto (chega perto da altura de uma pessoa). Um kit de N mostra N unidades em tamanho real. O enquadramento nunca encolhe um produto grande até parecer miniatura: para produto grande ou kit, afastar a câmera e mostrar o ambiente em escala (porta, mesa, piso, tomada como referência), ou mostrar parte das unidades por cena, sempre com a contagem certa na cena principal.
Antes de animar: conferir a imagem contra objetos de referência da cena (porta cerca de 2,1 m, mesa cerca de 75 cm, assento de cadeira cerca de 45 cm). Se o produto parecer de brinquedo, não animar.
Ferramentas e aparelhos pequenos também (Kevin 2026-10-23, Lista 22/10 A): o martelete do Combo Stanley saiu menor do que é em cima da mesa, e o berço balanço elétrico saiu pequeno (descartado). Produto pequeno sobre mesa/bancada encolhe porque a mesa ocupa o quadro e o layout coloca o produto numa faixa fixa. Regra: dar a medida em cm no prompt (martelete SDS cerca de 35-40 cm de comprimento, quase o antebraço de um adulto; parafusadeira cerca de 20-25 cm) e uma comparação com algo da cena (largura da mesa, um caderno A4 = 30 cm, uma caneca = 10 cm). Kit com itens de tamanhos diferentes: cada item no seu tamanho relativo da foto 01 (o martelete bem maior que a parafusadeira). Conferir antes de animar com a mesma régua.

## K11. Morphing e chão pixelando (Kevin 2026-10-23 09:02)
Erro: cenas que "derretem" (objeto muda de contorno, morphing/warping) e chão ou parede que tremula ou vira quadradinhos (shimmering/boiling).
Regra: no prompt, pisos e paredes de textura larga e calma (cimento queimado, porcelanato grande, terracota 30 cm, tábua larga); nada de espinha de peixe, ladrilho estampado, carpete listrado ou grama densa quando a câmera anda. Câmera lenta, clipe de 4 s, nada de close extremo em superfície lisa. Prompt de vídeo: "stable textures, solid objects keep their exact shape, no morphing". Antes de entregar, conferir 3 quadros seguidos no fim de cada clipe e cortar antes do defeito (setor_qualidade/fiscal_video.md item 4b).

## K6.y Corpo da modelo do provador encolhe no vestir (Kevin 2026-10-23 09:21, lote TikTok 23/10)
Erro: Nano Banana reduziu o busto em várias fotos, sobretudo nos biquínis (p01 camuflado, p10 pink); o cropped saiu largo e comprido; o short jeans básico saiu folgado.
Causa: a peça do anúncio está numa modelo de busto pequeno, e o editor copia o tamanho da peça junto. Na modelo do Kevin (extremamente encorpada, busto grande) a mesma peça fica menor e mais justa.
Regra para TODO prompt de vestir:
1. Toda roupa é JUSTA no corpo dela: "skin-tight, stretched over her body"; cropped termina acima do umbigo e abraça o busto, nunca solto nem comprido.
2. Biquíni: triângulos do tamanho do anúncio, esticados sobre o busto grande dela ("the small triangles stretch over her large full bust, her bust volume exactly as image 1"); nunca aumentar a peça para cobrir mais nem reduzir o busto.
3. Complemento básico (short jeans, legging, top) também é justo e marca o corpo, como roupa de rua/praia.
4. Calçado com vida e variado: chinelo colorido/estampado ou rasteira com detalhe; tênis variando (branco chunky, bege, preto e branco, colorido de corrida, cano baixo retrô). Nunca o mesmo chinelo branco da base.
Conferir lado a lado com a base o volume do busto antes de mostrar; se diminuiu, não mostrar como pronto.

## K12. Objeto preso em coisa sem nexo (Kevin 2026-10-23 09:35, Lista 22/10 C p44 prateleira aerofólio)
Erro: na cena com cortina, um dos suportes da prateleira de parede ficou "parafusado" na cortina. A IA pôs uma cortina logo atrás de onde o produto se fixa.
Regra: produto que se fixa (prateleira, suporte, TV, nicho, espelho, luminária de parede) só em parede lisa e contínua atrás de TODOS os pontos de fixação; o prompt não pede nem deixa espaço para cortina, janela, porta, quina ou móvel atrás dele. Na conferência da imagem antes de animar: cada suporte ou parafuso toca a parede? Se algo estiver apoiado ou preso em coisa que não aguenta (cortina, vidro, ar), a cena é reprovada.
Começo de cada versão (Kevin 09:37): a regra do produto exato nos primeiros segundos vale para o início de TODAS as versões (A, B, C e Reels), não só da primeira cena gerada. Cena reaproveitada no lugar de uma reprovada também abre com o produto idêntico à foto 01.

### K6.z Padrão do provador TikTok (Kevin 2026-10-23 09:48, aprovado nas fotos v3 do lote 23/10)
- Complemento de peça (anúncio só de cima ou só de baixo) é sempre SENSUAL e combinando com o nicho: ex. short de cetim tipo pijaminha com renda, saia curta moderna, top justo moderno. Nunca jeans básico ou camiseta básica sem graça.
- Calçado combina com o look (salto/sandália de tira com peça sensual; chinelo colorido com biquíni; tênis variados no fitness). Nunca tênis preto.
- Biquíni: triângulos no tamanho real do anúncio, ficando visivelmente pequenos no busto grande dela.
- Corpo: malhado, cinturinha, barriga e coxas naturais de mulher comum, busto/quadril/glúteos grandes; toda roupa justa.
- Limites que continuam: sem contorno de mamilo ou virilha (pedir bojo liso / tecido grosso), sem rosto.

### K6.w Parede deformando no Wan (Kevin 2026-10-23 11:00, lote 23/10)
Quase todos os vídeos do lote 23/10 (takes A vestido 2-5.5 + C babydoll 7.4-9.8) entortaram a parede/batente nos giros; o prompt "static background, straight door frame" não basta. Kevin postou porque a modelo ficou boa, mas é defeito. Próximo lote: testar de graça a troca de fundo por código (recortar a modelo quadro a quadro e colar sobre o fundo parado da foto vestida) antes de entregar; conferir paredes a cada 0,5 s.

## K12. Câmera nunca mostra lado que a imagem de partida não mostra (2026-10-23)
Cafeteira teste 2 cena C: o prompt pediu "tilt para cima" e a câmera passou por cima da máquina. O modelo de vídeo só recebe a imagem de partida, não as outras fotos, então inventou a tampa. Regra: o movimento só pode revelar o que já aparece na imagem de partida. Se a cena precisa mostrar o topo (ou outro lado), a imagem de partida já tem que mostrá-lo, feita a partir da foto que mostra esse lado.

### K6.v TikTok "imagens estáticas / quadro fixo" (Kevin 2026-10-23 11:32, biquíni camuflado lote 23/10)
TikTok Shop puniu o vídeo p01 (visibilidade reduzida + produtos removidos) por "imagens estáticas / quadro fixo". Medição: o vídeo tem movimento contínuo em todos os segundos (diferença média 2-5 por quadro, nenhum trecho parado), então o provável gatilho é o conjunto câmera travada + fundo 100% parado + o mesmo take repetido (A+C+A+C) + texto fixo na tela o vídeo todo. Recurso recomendado. Prevenção nos próximos: não repetir take na edição (pedir takes diferentes ou um trecho contínuo mais longo), câmera de celular na mão com leve balanço real vinda da guia, texto da tela só nos primeiros segundos, e conferir com o medidor de movimento antes de entregar.

## K13. Prompt de vídeo não cita proibidos nem textos de propaganda (Lista 23/10 A, 2026-10-23)
Erro: o prompt do Seedance levava a ficha inteira, com "Never show: bowls, fruit, plants..." e "Lettering: o texto 'MELHOR ESCOLHA' da foto é propaganda". Resultado: vaso, fruteira e torneira surgiram na bancada (p03 B, C) e um corte de cena com "MELHOR ESCOLHA" e "VS" na tela (p02 C). É a regra 1 valendo também para a ficha.
Regra: o prompt de VÍDEO leva só o que existe (nome, variante, itens, partes, contagem, Scale) e "every surface stays as bare as in the first frame". Nada de lista de proibidos, nada de texto de propaganda citado (gerar.py descr_video na lista2310a).
Enquadramento: produto que já começa de borda a borda não aguenta aproximação; use deriva lateral curta na mesma distância.

## K6.zz Biquíni: mostrar elasticidade (Kevin 2026-10-23 12:04)
Pode mostrar a elasticidade do biquíni com a peça nas mãos ou puxando de leve a alça lateral no quadril, SEM baixar a peça e sem nada que pareça tirar a roupa. Só com um vídeo-guia limpo que tenha esse movimento (Wan copia o guia).

### K6.u Guia com rosto em close faz o Wan desenhar o rosto (2026-10-23, mix do biquíni)
babydoll_3.mp4 (5-7,5 s) é close de selfie com o rosto visível: o Wan gerou o rosto inteiro da modelo, mesmo com a imagem base sem rosto. Nunca usar trechos de guia em que o rosto da pessoa aparece no quadro. Narração: ElevenLabs multilingual-v2 (voz Jessica) sai ~30% mais longa que o vídeo; escrever ~2,3 palavras por segundo de vídeo.

## K13. O prompt de vídeo só descreve o que está no quadro (Lista 23/10 B, 2026-10-23)
Erro: o prompt do Seedance levava a ficha inteira (variante "foto 01", medidas, letras de propaganda, lista "Never show" com vinho, taças, comida, LED da traseira). O Seedance desenhou exatamente isso: vinho e taças no balcão das banquetas (p03), bolinhas de massagem, cotas e "Preta foto 01" sobre a cadeira (p05), texto "165HZ" e robô na tela do monitor (p06), texto de propaganda na parede do monitor 49" (p12), LED vermelho na borda da tela (p06 C). 14 clipes refeitos.
Regra: o prompt de VÍDEO leva só nome curto, itens e partes visíveis (sem partes "não mostrar"), a linha Scale e o movimento. Nada de lista de proibidos, variante, medidas em número de foto, textos de propaganda. Correção de clipe também em frase positiva ("o balcão fica exatamente como no 1º quadro, vazio e liso"), nunca nomeando o objeto indesejado. lista2310b/gerar.py (vdescr) já faz isso.
Também visto: seladora acende a fenda em vermelho (dizer "desligada, fenda escura"); vidro preto de forno de frente reflete a pessoa filmando (filmar 10-15° de lado); Seedance troca deslize/descida por aproximação e termina em close de letras (autoclave, micro-ondas): cortar antes do close.

## K14. Produto complexo leva a foto do anúncio colada + posição de cada peça (Kevin 2026-10-23 20:56-20:59, Lista 23/10 C)
Erro: na roçadeira p40 a IA pôs a tampa do tanque de gasolina em cima, mas no anúncio ela fica embaixo (a ficha até dizia "tanque embaixo", e o fiscal deixou passar). Na bike p32 o 2º take mostrou um monitor diferente do anúncio, que aparece em outras fotos com descrição do display.
Regras:
- Produto complexo (máquina, motor, ferramenta a gasolina, eletrônico com painel, muitas peças ou muitas letras pequenas) leva a FOTO 01 DO ANÚNCIO colada durante o vídeo inteiro. Estilo aprovado pelo Kevin (21:25): SEM fundo branco (recorta o branco, mantendo todos os itens pequenos), SEM o texto "Foto do anúncio", sobre um cartão arredondado com o próprio vídeo desfocado atrás (vidro fosco). NUNCA em cima do produto (Kevin 2026-10-23 20:31, 2ª revisão: a posição fixa embaixo à esquerda cobriu o produto em B09, B13, C39 e C40). A posição é escolhida CENA POR CENA, olhando o início, o meio e o fim de cada cena (a câmera aproxima e o produto cresce): o lugar livre mais comum é à direita, acima do produto, logo abaixo do texto; em cena com espaço embaixo à direita, ali. Também não cobre texto, o selo marca, nem o botão CTA (Shopee A/C: x 260-820; B/Reels: x 70-620; y 1325-1385). Limites: y 230 a 1440, x até 940 da metade da tela para baixo. Tamanho: o MAIOR que couber no espaço realmente livre, em geral 240 a 320 px (Kevin 2026-10-24 01:58, p32: 190 px ficou pequeno; "um pouquinho maior, e no espaço realmente livre"). Piso livre na frente do produto é bom lugar, mas só acima de y 1440 (abaixo disso o card do produto do app cobre). Se a cena não tiver nenhum espaço livre (motor que ocupa a tela toda), usa o canto onde cobre menos e avisa o Kevin. Ferramenta: video-teste/foto_colada/ (spec.json com [início, fim, x, y, largura] por cena, grade.py para prévia com grade e retângulo, aplicar2.py para renderizar). Se a foto 01 tiver fundo de cena (não branco), usa a foto inteira com cantos arredondados no mesmo cartão. Ferramenta: scratchpad ed2/card.py + aplicar.sh do thread Lista 23/10 C. Pode ser a foto inteira ou recortada, desde que tenha todos os elementos. Isso evita punição injusta mesmo quando o vídeo ficou fiel. Ferramenta: video-teste/lote/lista2310c (scratchpad ed/inset.py + overlay ffmpeg). Produto simples não precisa.
- Fichador: além das peças, descreve a POSIÇÃO de cada peça funcional em relação ao corpo (em cima/embaixo, frente/trás, esquerda/direita), usando TODAS as fotos (outros ângulos), e copia o texto do display/painel quando aparece em alguma foto.
- Fiscal de imagem e de vídeo: conferem a posição das peças funcionais (tanque, tampa, painel, saídas) contra todas as fotos, não só contra a foto 01; peça trocada de lugar reprova a cena.
- Letras pequenas legíveis em outras fotos do anúncio (Kevin, p35) devem ir para a ficha como texto exato.

- Pneus e produtos com escrita grande no corpo (Kevin, Lista 23/10 B p14): as escritas aparecem bem visíveis em outras fotos do anúncio e no vídeo ficaram fracas. A ficha copia essas escritas como texto exato e o fiscal confere se ficaram legíveis.
- Seja fiel à primeira imagem: se a foto 01 mostra acessórios junto (ex.: rolos de fita da seladora, Lista 23/10 B p09), eles aparecem no vídeo ou na foto colada.

## K15. Produto pequeno sai gigante no Nano Banana (Kevin 2026-10-24, loja do amigo)
Erro: presépio de 5-13 cm, escultura de 15 cm e caixinha de 7 cm saíram 1,7-3x maiores que o real; 13 imagens descartadas (US$ 0,51) em 3 rodadas. Só passou com câmera a 80-90 cm, produto em 35-45% da largura e régua bem maior encostada (livro 28 cm, perfume 18 cm).
Regra: o Fichador escreve isso na ficha ANTES da 1ª imagem (setor_qualidade/fichador.md, "Produto pequeno"). Desperdício de imagem por escala é falha da ficha, não do fiscal.

## K13.b Ficha com "(não vendido)" e "Layout in photo 01" vaza para o vídeo (Lista 24/10 A, 2026-10-24)
Erro: itens "2 dining chairs (the side table, vase, cup, books, plant and rug of photo 01 are not sold)" e a parte "Layout in photo 01: ... side table" iam inteiros no prompt do Seedance (o vdescr só filtrava partes com "never/hidden"). Vaso, xícara, livros e tapete surgiram do nada em p03 A e B; cadeira giratória girou em p05 C e p07 C.
Regra: o prompt de vídeo tira parênteses dos itens, frases "not sold / no table is sold", menções "photo 0X" e as partes que começam com Layout/Orientation/Positions checked/Proportions (lista2410a/gerar.py vdescr). Cadeira/poltrona giratória: frase "seat, backrest and headrest keep facing exactly the same direction in every frame; the chair is locked in place" e câmera quase parada.
