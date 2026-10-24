# Brief do Fichador, Lista 24/10 A (2026-10-24)

Pasta: video-teste/lote/<pasta do lote>/ .
Para cada produto pNN que te deram: fotos em `pNN-fotos/` (01.jpg ... + anuncio.json com nome, descrição e preço).

Leia antes (obrigatório):
- agentes/setor_qualidade/fichador.md (o seu papel, campos da ficha)
- agentes/regras_de_erros.md (todas as regras; seções 9-15 em especial: 13 = prompt de vídeo só com o que está no quadro, 14 = posição de cada peça lida de TODAS as fotos + `complexo`, 15 = produto pequeno)
- Exemplo de ficha boa (aprovada pelo Kevin): exemplos/ficha-exemplo-poltronas.json
- Defeitos já vistos: agentes/aprendizado/defeitos.csv

Abra TODAS as fotos (mosaicos com PIL para ler rápido; abra em tamanho cheio as que têm letras, medidas ou detalhes funcionais).

## Saída 1: `pNN-ficha.json` (mesmos campos do exemplo)
`fotos_ref` com caminhos relativos à pasta do lote, ex. "pNN-fotos/01.jpg" (01 sempre primeiro; 2-4 fotos; nunca foto com pessoa, mão, colagem, texto grande de propaganda ou outra cor).
Cada cenário tem `id` (A, B, C), `texto`, `scale`, `camera`, `movimento`. Diretrizes novas (Kevin 2026-10-23):
1. **Sem zoom em letra pequena** (Kevin 11:18): a câmera nunca termina em close de painel, rótulo, logo pequeno ou tela. Termina em plano médio com o produto inteiro. Mas tem que ser vídeo UGC de verdade, agregando valor (ambiente de uso real, luz bonita, profundidade, câmera andando), não a foto do anúncio parada.
2. **Câmera só mostra o que a imagem de partida mostra**: nada de subir acima do topo, dar a volta, mostrar traseira ou lateral escondida. Arco só até 10-15° e nunca em produto redondo/giratório (o Seedance faz girar). Preferir: avanço reto lento de 20-30 cm na mesma altura, ou deslize lateral de 30-40 cm na mesma distância, ou leve descida (crane down) de 20 cm. Diga sempre ONDE a câmera para ("stops at a medium shot with the whole X still in frame, base on the floor"). Nunca "pull back" (o Seedance inverte).
3. **Enquadramento**: produto inteiro, 35-60% da altura do quadro, com folga em todos os lados (nunca encostando na borda; o cooktop do teste foi reprovado com 90% da largura). Produto grande/kit: câmera a 1,5-2,5 m com um objeto de tamanho conhecido encostado nele (regra 10); kit de N mostra as N unidades lado a lado na mesma distância e mesma altura (banquetas Gold foram descartadas por alturas diferentes).
4. **Cenários modernos** de classe média alta, de uso real (`uso`), variados entre si e contra as últimas linhas de agentes/aprendizado/cenarios_usados.csv (acrescente as suas 3 linhas no fim do csv com `>>`). Pisos e paredes de textura larga e calma. Produto que se fixa na parede ou se embute (micro-ondas/forno de embutir, monitor em suporte): parede/marcenaria contínua atrás de todos os pontos (regra 12).
5. **Detalhes funcionais** (Kevin 11:19): furos, grades, entradas de ar, botões, telas, tomadas, padrão de pneus: descreva-os em `partes` contando (fileiras, quantidade, forma), lidos das fotos de perto. Letra miúda ilegível: "tiny unreadable markings, keep them minimal, never invent words".
6. Nada proibido: pessoa, mão, bebida alcoólica, comida/objeto não vendido em cima do produto, líquidos, fumaça, faíscas. Ferramenta parada, desligada, sem disco girando, sem faísca. Nada de uso/demonstração.
7. Medidas: leia a foto de medidas e a descrição. A linha `scale` dá 2-3 comparações com objetos da cena (porta 2,1 m, bancada 90 cm, mesa 75 cm, assento 45 cm).
8. Se o anúncio mostra a variante da foto 01 diferente do título, vale a foto 01. Se o produto parecer réplica/falsificação de marca (ex.: "similar a Bosch"), ou se a foto 01 for colagem sem nenhuma foto limpa, escreva `"alerta": "..."` na ficha.

## Saída 2: `pNN-textos.json` (roteiro das 4 versões; formato do exemplo abaixo)
Só fatos ESCRITOS no título ou na descrição (números, materiais, recursos). Sem preço, prazo, %, nota exata, frete. Gancho de até 6 palavras. Legendas Shopee (`leg_a`, `leg_b`, `leg_c`): nome + 2 fatos + 4 hashtags de nicho, < 150 caracteres, sem link. `leg_r`: gancho + fatos + 4 hashtags, termine a frase com ". #" antes das hashtags (o link entra depois). `a.momentos` = 3 linhas; use `sem_horario: true` salvo se manhã/tarde/noite fizer sentido real. `b.cenas`/`r.cenas` = 3 trios [grande1, grande2, linha pequena ou null]. `c.itens` = 3 motivos de até ~26 caracteres. `ac` = cor de destaque RGB que combine com o produto. `en` = nome curto em inglês; `ext` = "from the X to the Y" (extensão do produto).
Exemplo (Lista 22/10 B p01): exemplos/textos-exemplo.json chave "p01" (ignore `links`, `link`; não precisa `leg_r` com link).
Inclua `slug` (kebab-case curto) e `nome` (nome curto em PT, até ~35 caracteres).

Ao terminar cada produto, releia a foto 01 e confira a ficha contra ela. Responda no fim com 1 linha por produto: pNN, nome, alertas (se houver).

## Notas por tipo de produto (aprendidas nos lotes do Kevin)
### Móveis: cadeiras, poltronas, banquetas, sofá, mesa (Lista 24/10 A)
- Posição de cada peça funcional em `partes` (encosto, braços, base giratória, pés, rodízios, alavancas, costuras/nervuras) conferida em TODAS as fotos. Marque `"complexo": true` só se for máquina/eletrônico/muitas letras (aqui quase nunca).
- Kits: a contagem da foto 01 vale em todas as cenas; unidades lado a lado na mesma distância e mesma altura do assento.
- Kit de cadeiras já saiu em miniatura: cadeira de 80-85 cm, assento a ~45 cm, 6 unidades em tamanho real em volta de uma mesa de jantar de 75 cm, câmera a 2-2,5 m.
- O Seedance avança mesmo quando se pede deslize (Lista 23/10 C): planeje cenas em que um avanço de 20 cm ainda deixa o produto inteiro no quadro.

### Bebê, casa, fitness, perfume (Lista 24/10 C)
- Regra 14: descreva a POSIÇÃO de cada peça funcional (em cima/embaixo, frente/trás, esquerda/direita) usando TODAS as fotos; copie texto de display/painel/rótulo legível em qualquer foto. Marque `"complexo": true` (foto 01 colada no vídeo) em bike com monitor, carrinho de bebê/travel system com muitas peças, cozinha infantil com muitos itens, e em qualquer produto com muitas letras ou peças. Produto simples (tapete, mesa, prateleira, berço simples): `"complexo": false`.
- Regra 15 (produto pequeno, perfumes 80-100 ml): siga a seção "Produto pequeno" do fichador.md AO PÉ DA LETRA (câmera 70-90 cm, produto 35-45% da largura, objeto bem maior encostado, sem "large in frame"/"close"). O frasco e a caixa (se a foto 01 mostrar a caixa, ela aparece) com as letras exatas do rótulo; letra miúda = "tiny markings, keep as in image 1".
- Regra 13: nos campos `movimento` nada de proibidos nem textos de propaganda.
- Carrinho de bebê, berço, cozinha infantil: NUNCA bebê ou criança na cena (nada de pessoa); carrinho parado, sem dobrar/abrir. Kit (carrinho + bebê conforto, 3 em 1 com moisés): todos os itens da foto 01, na posição da foto 01.
- Tapetes: o tapete é o piso, mostre a medida real (300x400 / 300x300) com sofá e mesa de centro em cima/ao redor para escala; sem textura que cintile (trama baixa calma, câmera não rasante).
- Prateleiras suspensas/de parede: fixação só em parede/teto liso contínuo (regra 12); poucos objetos neutros nelas, nada de comida ou bebida alcoólica.

### Ferramentas, máquinas, eletrônicos (Lista 24/10 B)
- Detalhes funcionais (grades, furos, ventilação, painel, botões, discos, lâminas, brocas): forma e padrão exatos em partes (contagem quando visível); o fiscal confere isso.
- Cenários: modernos, onde o produto é usado de verdade (oficina/garagem moderna ou bancada para ferramentas; obra/área de serviço para cortador de piso; cozinha profissional/gourmet para forno industrial; cozinha planejada para coifa; galpão/academia/área gourmet para ventilador industrial; caminhão/motorhome/área externa para gerador; escritório gamer/quarto para PC; pulso não, relógio fica sobre superfície). Pisos de textura larga e calma. Os 3 cenários com piso/parede/paleta diferentes entre si e de agentes/aprendizado/cenarios_usados.csv.
- Produto preso em parede/teto (coifa, ventilador de parede): só parede lisa contínua atrás de todos os pontos de fixação; coifa sobre cooktop/fogão, na altura certa.
