# Lições da fábrica (memória do projeto original, out/2026, sem dados pessoais)

Tudo aqui foi aprendido na prática, quase sempre perdendo dinheiro. As regras detalhadas e numeradas estão em
`agentes/regras_de_erros.md`; este arquivo junta o "porquê" e o jeito de trabalhar que a dona da fábrica original pediu.
Leia uma vez no começo de cada conversa nova. Quando a dona der uma regra nova, grave aqui (data + regra + porquê).

## Jeito de trabalhar
- Um passo por vez, resposta curta, em português. Diga o próximo passo e o custo dele em R$.
- Nada pago sem pedido: nenhuma imagem, clipe, refação ou vídeo novo sem a dona pedir. Edição, checagem e código são grátis.
- Antes de gastar: teto duro em dólar, custo esperado e o OK dela. Modelo novo: medir 1 cena pelo saldo antes de orçar
  (o preço da lista do WaveSpeed às vezes é por SEGUNDO, não por clipe: um clipe que parecia US$ 0,11 custou US$ 0,56).
- Qualidade acima de economia: economizar nunca pode baixar a qualidade final. Cena simples não pode virar cena pobre.
- Toda cena é animação de IA de verdade. Câmera por código só onde o produto quebra na animação, e mesmo assim com o
  cenário animado por trás (produto parado colado por código), nunca foto parada com zoom.
- Na revisão, corrija SÓ o que ela marcar como "corrigir"/Editar. Comentário solto vira regra, não refação.
  Não reassista vídeos tentando adivinhar o que ela quis dizer: espere ela apontar.
- Lote liberado vai até o fim: trabalhos em segundo plano com tempo limite e nova tentativa, aviso curto a cada etapa.
- Registre toda refação paga e todo vídeo que não deu para postar em `agentes/desperdicios.md` (data, produto, lote, US$, motivo).
  Produto que não deu para postar volta para a Fila do Tinder.
- Corrija a dona quando um pedido puder prejudicar a fábrica (gasto, uso do plano Claude, qualidade). Diga em uma linha.
- Uso do plano Claude também é limite: lote numa conversa NOVA (15 a 20 produtos por conversa). Conversa longa gasta mais
  por mensagem: um vídeo já custou mais de US$ 5 de uso de Claude contra US$ 0,12 de WaveSpeed numa conversa comprida.
- Use o modelo Claude mais capaz para criação (roteiro, prompt, ficha). Subagentes separados para Fichador e fiscais são ok.
- Proteja a conta de afiliada: nunca burlar captcha, nunca automatizar login da Shopee, nunca robô no app.

## O que vende (busca de produtos)
- Regra de ouro: vendas recentes + 0 a 3 vídeos de criadores no app = venda quase certa (o vídeo dela aparece primeiro
  na busca). Menos de 10 vídeos com vendas recentes já vale. O número que importa é o de VÍDEOS de criadores, não de afiliados.
- Preferir produto caro (high ticket): comissão é % do preço; uma venda de R$ 400 vale umas 10 de R$ 20.
- Sinais: total vendido baixo (até ~30) tem menos vídeos; marca famosa lota mesmo sem vendas; nome difícil de buscar tem
  menos criadores. Lotadas: caixa de som bluetooth, robô aspirador, ar-condicionado. Vazias: purificador de água, cadeira de
  escritório, monitor sem marca, ventilador, gaiola, bebedouro, motor de popa. Móveis vendem mas lotam (fáceis de buscar).
- Nunca repetir anúncio: o controle é pelo itemId (`vistos.json`). Parecido da mesma loja só ganha o selo "possível
  duplicata"; a dona decide. A varredura nunca joga fora produto bom: soma tudo, sem limite.
- A API não dá data de avaliação nem número de afiliados; datas de avaliação no site são bloqueadas (não tentar burlar).

## Fidelidade ao anúncio (o que dá punição)
- Nunca gerar o produto a partir de texto: sempre partir das fotos reais do anúncio (Nano Banana Edit com as fotos).
- Cor, tecido, variante, detalhes e letras vêm da FOTO 01. Todos os itens da foto 01 aparecem em todo vídeo, na mesma
  quantidade e arrumação (relógio com 2 modelos na foto 01 saiu com 1 e o vídeo foi perdido).
- Tamanho real sempre: kit de N mostra N unidades inteiras; nada de miniatura (cadeiras, PC, berço saíram de brinquedo).
  Linha de escala em todo prompt com 2-3 comparações; produto grande com câmera a 1,5-2,5 m e um objeto de tamanho
  conhecido encostado; produto pequeno (até ~20 cm) com câmera a 70-90 cm e um objeto bem maior ao lado.
- Peças contáveis (prateleiras, gavetas, níveis) com a contagem do anúncio: estante de 5 prateleiras já saiu com 6.
- Letra miúda a IA redesenha errado: texto exato só onde dá para ler; letra ilegível = "tiny markings, keep as in image 1"
  e nada de close nela. Produto com muitas letras/peças (máquina, motor, painel): foto 01 colada num canto (regra 14).
- Posição de cada peça lida de TODAS as fotos (tampa de combustível em cima quando é embaixo = vídeo errado).
- Só fatos do anúncio: todo número, material, recurso e cor no texto tem que estar escrito no título ou na descrição.
  Nome de modelo não é recurso. Sem nota exata nem número de avaliações (mudam), sem % de desconto, sem prazo de entrega,
  urgência só se o anúncio provar.
- Nada de bebida alcoólica em cena (taças e garrafas aparecem sozinhas em sala e churrasqueira: conferir).
- Nada de pessoa, mão ou bebê na cena. Produto parado, só a câmera anda (o que converte é produto parado com câmera viva).
- Cenário do uso real (cadeirinha de carro não vai no chão da sala), casas MODERNAS de classe média alta, cenários
  diferentes entre as 3 cenas e entre produtos (`agentes/aprendizado/cenarios_usados.csv`).
- Conteúdo original: a Shopee prefere cena nova de IA a zoom na foto do anúncio (zoom na foto parece básico e igual aos rivais).

## Prompts (o que já deu errado)
- O prompt de VÍDEO leva só nome, itens, peças e escala. Citar o que NÃO pode aparecer faz o modelo desenhar exatamente
  isso (taças, vasos, 3ª cadeira, texto na parede). Nada de "(não vendido)", "Layout in photo 01" ou textos do anúncio no vídeo.
- "Smartphone photo" desenhou moldura de celular: use "Photorealistic full-frame photo" e "no phone frame, no borders, no text".
- Pose que o produto não aguenta sozinho faz a IA inventar peça. Mostre o produto apoiado do jeito real.
- Órbita/giro faz a IA virar o produto e inventar o lado escondido: só aproximação curta, deslize lateral ou subida leve.
  A câmera só mostra o que a imagem de partida já mostra (passar por cima inventou o topo de uma cafeteira).
- O Seedance avança mesmo quando se pede deslize: planeje cenas em que um avanço de 20 cm ainda deixa o produto inteiro.
  Se ele insistir em mexer o produto: `FIXA=1` (câmera parada na IA) e o movimento vem por código.
- Pisos de textura fina cintilam/pixelam: piso de textura larga e calma, câmera não rasante.
- Letras espelhadas: escreva "lettering reads left to right, never mirrored".

## Edição e entrega
- 15 s exatos, 3 cenas, 9:16, gancho no primeiro segundo; o produto aparece inteiro, limpo e sem nada por cima na 1ª cena.
- Texto nunca cobre o produto (confira o ÚLTIMO quadro de cada cena: a aproximação aumenta o produto).
- Fora da área do app: barra de cima, legenda e cartão do produto embaixo, ícones à direita. Chamada com ↓ logo acima do
  botão do app, nunca em cima dele.
- Cada versão com gancho, chamada e modelo próprios: só trocar a ordem das cenas não vale como versão nova.
- Ganchos e chamadas bem elaborados, específicos do produto (nada genérico). Detalhe de compra (quantidade, medida) grande na tela.
- Legenda Shopee: nome + 2 fatos do anúncio + 4 hashtags de nicho, menos de 150 caracteres, sem link, sem emoji.
  Reels: gancho + fatos + hashtags + o link de afiliada dela.
- Música própria livre de direitos, alternando sozinha (`musicas/`). Volume baixo nos vídeos sem voz.
- Celular: vídeo anexado no chat não baixa no iPhone; entregue por página com botão de baixar ou link do Drive.
- Os layouts de edição da dona são os dela: use os modelos dela. Os modelos do kit (`video-teste/luxo/`) são só opção.

## Postagem automática
- Reels no Instagram, Facebook e Threads pela API da Meta (app em modo Desenvolvimento, sem revisão).
- Conta nova: ritmo seguro (MAX_DIA=2, INTERVALO_H=3). O Facebook já recusou com aviso anti-spam (código 368) em página
  nova: a rede fica pausada 24 h e tenta de novo 1 vez por dia, nunca em laço.
- No Instagram link não é clicável: use o link da bio. No Facebook, o link vai num primeiro comentário. No Threads o link é clicável.
- Pessoa realista feita por IA = rótulo de IA ligado.

## Modelos e preços medidos (out/2026, WaveSpeed)
- Nano Banana 2.1 Edit: US$ 0,0396 por imagem (1k, 9:16). Seedance 1.5 Pro Fast i2v 720p 5 s sem áudio: US$ 0,10.
  Veo 3.1 Lite: US$ 0,20 por clipe de 4 s (melhor caminhada de câmera, mas pôs mão no produto e inventou letrinha; só se o Seedance não der).
- Seedance v1 Pro Fast 720p foi ruim (zoom demais, pessoa fantasma). Kling v3 turbo std custa por segundo (caro).
- Candidatos a comparar um dia (1 cena cada): Seedance 2.0 Mini Turbo, Kling 2.6 Std, Vidu Q3 Turbo, Wan 2.6 Flash.
- Teto por produto: R$ 3 (todas as versões). Câmbio usado: R$ 5,69 por US$.

## Limite de uso do Claude (a dona, 2026-10-24)
Em 24/10 o limite de uso parou a Fiscal de vídeo às ~06:30 UTC (volta 8:20 UTC) e nada retomou sozinho até a dona escrever às 20:18.
Regra: ao ver "session limit · resets HH:MM", agende na hora um lembrete (send_later) para alguns minutos depois do reset,
com o passo exato para retomar (ex.: SendMessage ao agente parado). Sem isso a fábrica fica parada até a dona voltar.

## Conferência e Fila (a dona, 2026-10-25)
- Produto em produção sai da Fila do Tinder (status produzindo → aba Produção; pronto quando terminar).
- Na Conferência, ao tocar "Avisar o Claude" os decididos saem de "Para conferir": Editar → "Em edição", OK/Descartar/Esgotado → "Conferidos". "Para conferir" fica só com vídeo novo.

## Jogo pausado (a dona, 2026-10-26)
"Pause o jogo até terminar os vídeos, depois voltamos": não atualizar o jogo (reino, metas, mural, gastos) até o lote 25/10 A estar na Conferência. Depois, atualizar tudo de uma vez e perguntar como seguir com o jogo.

## Não encerrar antes de concluir (a dona, 2026-10-26)
"Tenha certeza que não irá mais encerrar a tarefa antes de concluí-la". Lote longo: rodar solto (setsid nohup, sem limite de 2 h), script de retomada que pula o que já está pronto, e tarefa agendada de hora em hora que retoma e entrega até o fim. Só apagar a tarefa agendada quando tudo estiver na Conferência.

## 2026-10-26 (Lista 25/10 A)
- O container é reclamado quando a conversa fica parada: processo solto morre. Durante render longo, manter um Monitor ligado (30 min, re-armar) na conversa.
- Apagar trabalhos/*/out2/*.video.mp4 depois de cada render (enchem o disco).
- Auditor por vídeo: 1 vídeo reprovado não barra os outros 2 do produto.

## 2026-10-27 Conferência dentro da Postagens (a dona: "tenha certeza que não vou precisar falar sobre isso novamente")
- A dona confere na aba "Conferir" da página Postagens. Ok = os vídeos do produto vão sozinhos para "Para postar" (a página grava os posts). Pedir edição = status `editar` + nota; o Claude refaz no começo da conversa seguinte e grava de novo como `pendente`.
- A página Conferência antiga não recebe mais lotes. Nunca gravar posts à mão um por um nem esperar autorização produto a produto.

- 27/10: corte para peça gigante em kit = prompt de vídeo com detalhe de UMA peça (regra K18). Vídeo só com nome + itens + tomada travada.
- 27/10 (19h): a dona confirmou que os vídeos ficam na aba Conferir esperando o Ok dela antes de ir para "Para postar" (ela tinha pedido o automático por engano). Nunca colocar em "Para postar" sem o Ok dela.
- 27/10 (19h): ao desfazer o envio automático, o Claude apagou posts que a dona tinha acabado de aprovar (o Ok dela regrava o post e muda a versão). Antes de apagar/mexer em posts, ler o status do conferir: status "ok" sem auto = Ok dela, não mexer.

## 27/10 (a dona)
- Músicas mais animadas e sofisticadas, menos melancólicas: biblioteca = 12 trilhas animadas (gerador/animadas.py); calmas fora do rodízio.
- "Aguiiar Lar" com a mesma fonte, mas mudando de lugar no vídeo (topo e cantos livres, a cada 2,5-4 s) para não dar para cortar só a faixa de cima (build_lux.py _marca_plano).
- 27/10 C: histórico da WaveSpeed (POST /api/v3/predictions) devolve as imagens já pagas: resgate sem pagar de novo. Kit comprido (espreguiçadeiras) sai largo mesmo pedindo 40% da largura.
- 28/10 D: resgate = imagem aceita + câmera por código (zoompan), nunca clipe IA (inventou cachorro, vapor, marca d'água). Gemini pode anotar defeito e ainda dizer "usar": conferir 1 folha de quadros.

## 28/10 (a dona): Reels das redes sociais
- Para Instagram, Facebook e Threads: usar os layouts A ("Um dia com ela") e C ("Direto ao ponto"), alternando entre os produtos. B fica só para a Shopee.

## 28/10 – Conferência sempre antes de Postagens (a dona: "a partir de agora sempre faça assim em todos os lotes")
Todo lote: vídeos prontos vão para a Conferência (aba Conferir da Postagens). Só o Ok dela leva para "Para postar".
Ela abria a "Conferência" fixada antiga (outro banco, sem os lotes novos) e achava que os vídeos não chegavam; essa página virou um atalho.

## 28/10 – Redes automáticas: 1º disparo
- Postou nas 3 redes (mesa em L, A). Comentário com link falhou no IG e no FB: a chave da Meta não tem pages_manage_engagement /
  instagram_manage_comments. Agora o link vai na legenda até a dona gerar uma chave com essas permissões.
- A conversa da tarefa agendada não tem push no GitHub (403): o registro dos posts mora no banco da Postagens (redes/estado).
- A query do banco pagina (next_cursor): sempre seguir o cursor.
- 28/10: a dona quer nas redes SEMPRE primeiro os produtos bonitos e funcionais (puffs, poltronas, penteadeira): chamam mais
  atenção. Listas ESTRELAS / BONITOS / FIM no meta/redes_diario.py; produto novo de decoração entra sozinho na frente.
- 29/10: o segredo da Shopee está gravado como `shopee_APP_SECRET` (minúsculas). api.py aceita os dois nomes; nunca dizer
  "falta a chave" sem olhar `env | cut -d= -f1`. Lista 29/10: 200 links, 17 já existiam, 183 cartões novos no Tinder.
- 30/10: a dona viu muito desperdício na Conferência. Pediu "manter a qualidade e reduzir o desperdício". ~US$ 0,90 por lote
  (15%) vai em refação de produto largo que falha de novo. Regra K21: selo "largo" no Tinder + sem refação de borda com 2 cenas boas.
  Ideia em espera (precisa OK com teto ~US$ 0,05): imagem horizontal para produto largo e vídeo vertical montado dela.
- (30/10, a dona, K22) Produto sem cena aprovada não para mais em resgate: a fábrica monta A, B e C com as imagens reprovadas só por
  borda/largura (câmera por código, grátis) e manda para a Conferir com "cenas reprovadas pela fiscal: confira"; ela descarta à mão.
  Defeito grave (pessoa, bebida, letra inventada, objeto proibido) continua fora. Os 5 resgates de 28-30/10 eram todos assim e ela aceitou todos.
