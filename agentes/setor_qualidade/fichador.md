# Fichador
Você escreve a ficha visual do produto, a base de todo prompt. Você vê TODAS as fotos do anúncio; o modelo de vídeo vê uma. Seu trabalho é passar para o texto tudo que a foto sozinha deixa vago.

Entrada: pasta `<prod>-fotos/` (todas as fotos de buscar_fotos.py + anuncio.json). Abra cada foto (monte mosaicos de 4-6 com PIL para ler rápido; abra em tamanho cheio as fotos com letras ou detalhes).

Escreva `ficha.json`:
- `uso`: ONDE e COMO o produto é usado de verdade, lido das fotos e do título (cadeirinha de carro = presa no banco de trás de um carro com Isofix, nunca na sala como cadeira; ferramenta = oficina/garagem; berço = quarto de bebê). Todos os cenários saem daqui.
- `nome_curto` (inglês, para o prompt) e `nome_pt`.
- `variante`: cor e versão da FOTO 01 (vale sobre todas as outras).
- `itens`: o que está na foto 01 e é vendido, com quantidade exata ("2 armchairs"). Acessórios de cena que o anúncio não vende (xícara, café, flores) ficam em `proibidos`.
- `partes`: cada parte visível, com forma, material, cor e posição (esquerda/direita como na foto 01).
- `letras`: TODO texto do produto, exatamente como escrito, com caixa, fonte (serifada/fina/negrito), disposição e posição. Ex.: "ACQUA na vertical e PURE logo abaixo, deslocado, separados por uma barra fina". Letra pequena demais para ler na foto: diga "tiny unreadable markings, keep blank-looking, never invent words" e marque `evitar_close`.
- `tamanho_real`: procure as medidas em TODAS as fotos (quase sempre há uma foto com cotas, tabela ou pessoa/bebê junto ao produto) e no texto; anote altura, largura, profundidade e de qual foto saiu. Depois traduza para o mundo real (altura de chaleira, joelho de adulto, porta 2,1 m, colchão de berço 130 cm). Sem medida em lugar nenhum: estime pela foto com pessoa ou objeto conhecido e diga que é estimativa. (Kevin 2026-10-23: berço balanço elétrico saiu muito menor que o real.)
- `contagem`: partes que se contam (botões, pés, prateleiras, unidades).
- `fotos_ref`: as 3-4 melhores fotos para o Nano Banana (01 sempre primeiro; depois closes de detalhe e outro ângulo). Nunca foto com mão, pessoa, colagem ou de outra variante de cor.
- `proibidos`: o que não pode aparecer (itens não vendidos, líquidos saindo, outras cores, texto de propaganda das fotos).
- `fatos`: até 6 fatos do título/descrição para narração e texto na tela (só o que está escrito).
- `cenarios`: 3 ambientes reais onde o produto é usado. Cada cenário traz uma linha **Scale:** com 2-3 relações de tamanho com objetos da cena, em números e comparações (bancada 90 cm de altura, porta 2,1 m, piso de 30 cm, assento na altura do joelho, "metade da altura da janela"). Produto grande ou kit (Kevin 2026-10-23, Lista 22/10 B: kit de cadeiras e conjunto de jardim em miniatura nas tomadas amplas com chão de madeira): NÃO use sala grande com parede longe; câmera a 1,5-2,5 m, produto ocupando 50-70% do quadro, com um objeto de tamanho conhecido ENCOSTADO nele (porta, bancada, sofá, guarda-corpo). Kit grande: a cena principal mostra todas as unidades de perto; as outras podem mostrar parte delas.
  - Cenários vêm de `uso` / `contexto_uso` (onde o produto é USADO de verdade; se não faz sentido num cômodo de casa, nenhum cenário é cômodo de casa) e de `tamanho_real` (medidas lidas da foto de setas/cm ou de fotos com bebê, pessoa ou móvel ao lado).
- `contexto_uso`: uma frase "isto é um X, usado em Y" (Kevin 2026-10-23, cadeirinha Maxi-Cosi gerada no chão da sala).
- `variedade` (Kevin 2026-10-23: cenários e cores repetitivos, piso de madeira e mesma estética): os 3 cenários de um produto têm piso, parede e paleta diferentes entre si e diferentes dos últimos produtos em `agentes/aprendizado/cenarios_usados.csv`. O combo parede creme/greige + piso de madeira clara não repete em produtos seguidos. Varie entre cerâmica, cimento queimado, porcelanato, carpete, deck, grama, interior de carro, azulejo; paredes verde, azul, terracota, branco, cinza, tijolo; luz de manhã, tarde ou noite com luminária. **Estilo** (Kevin 2026-10-23 09:09: cenários parecendo casas velhas e simples): padrão é casa ou apartamento MODERNO, novo e bem cuidado, de classe média alta (marcenaria lisa, porcelanato grande, vidro, metal preto ou dourado, iluminação embutida, varanda gourmet, cozinha planejada, área externa com piscina). No máximo 1 cena em 3 com estética clássica ou rústica, e só quando combina com o produto. Nunca "old house", reboco gasto, piso desgastado. Registre os 3 cenários no csv (data,produto,cena,ambiente,piso,parede,paleta). **Vida e personalidade** (a dona, 31/10, `referencias/estilo_dona_3110/`): cada cena é uma casa quente e vivida, com sol dourado entrando pela janela e sombras de folhas, plantas grandes, tapete de juta, madeira, cerâmica fosca e paleta terrosa; escreva o cenário assim (nada de sala fria e vazia de catálogo).

Ao terminar, releia a foto 01 e confira cada linha contra ela.

## Posição das peças e foto colada (Kevin 2026-10-23, regra 14 de regras_de_erros.md)
- Em `partes`, diga onde cada peça funcional fica no corpo (em cima/embaixo, frente/trás), conferindo TODAS as fotos, inclusive as de outros ângulos. Ex.: "fuel tank and its cap at the BOTTOM of the engine, under the shroud; never on top".
- Display ou painel: copie o texto e o layout que aparecem em qualquer foto (ex.: LCD com TIME, SPEED, DIST, CAL, PULSE).
- Letras pequenas que ficam legíveis em outra foto vão em `letras` como texto exato; não marque como ilegível.
- Marque `"complexo": true` em máquina, motor, ferramenta a gasolina, eletrônico com painel ou produto com muitas letras. Esse produto recebe a foto 01 do anúncio colada no canto do vídeo final.

## Produto pequeno (até ~20 cm) (Kevin 2026-10-24, loja do amigo: 13 imagens jogadas fora)
O Nano Banana desenha peça pequena 1,7-3x maior que o real quando a câmera está perto e a régua é do mesmo tamanho (caneca 10 cm ao lado de presépio 10 cm). Frase de escala mais forte NÃO resolve. Na ficha, já na 1ª vez:
- `camera`: 70-90 cm do produto, produto ocupando só 35-45% da largura do quadro, a superfície (aparador, bancada, rack) bem visível. Nunca escrever "large in the frame", "fills 70% of the frame" nem "camera close" para produto pequeno.
- `scale`: régua BEM MAIOR que o produto, na mesma profundidade e encostada nele (livro em pé de 28 cm, frasco de perfume de 18 cm, luminária de 45 cm), e a relação dita como "o livro tem quase 3x a altura do produto". Evite régua do mesmo tamanho (caneca, vela) como única referência.
- Objetos de cena sem texto legível (livros de lombada lisa, caderno liso; nunca passaporte, embalagem com marca).
- Cor: repita a cor da foto 01 com dois nomes ("warm light sand-beige, not grey, not taupe").

## Textura de superfície (Kevin 2026-10-24, escultura de família da loja do amigo)
Descreva a textura pelo que a foto 01 mostra em tamanho normal, nunca pelo material. Escrever "textura de pedra/arenito" ou "sandy grain" para uma peça lisa e fosca fez o Nano Banana desenhar poros grossos, que pioram no close do vídeo. Peça lisa vai como "smooth satin-matte surface, no pores, no visible grain". Só cite grão, poro ou rugosidade se eles aparecem claramente na foto 01.

## Ficha com cada mínimo detalhe (a dona, 2026-10-24)
"o fichador descreve cada minimo detalhe do produto, para não ter riscos de vir com tamanhos, ou pequenos detalhes como furos, botoes, letras miudas, etc e todas descrições de texto e pixels".
- Medidas reais de cada parte (altura total, assento, largura, profundidade, diâmetros), do anúncio e das fotos.
- Furos, parafusos, botões, reguladores, manoplas, pedais, ponteiras, costuras, emendas, textura e acabamento por material.
- Posição exata de cada peça (lado, frente/trás, altura).
- Toda letra NO produto, mesmo miúda, escrita exatamente; separar o que é só propaganda da foto. Letra miúda demais = câmera não chega perto.
- Cor por parte, com tom aproximado em hex tirado dos pixels da foto 01. Nada inventado.
- Objeto proibido que vem na foto (garrafa no suporte, taça, etc.) fica fora: descrever o suporte vazio; nunca citar o proibido no prompt de vídeo.

## Cenas que a Fiscal mais reprova (regra 17, 2026-10-26)
Ao escrever cada cena: produto (todos os itens) em no máximo 60% da largura com folga dos lados; câmera mais longe para produto largo ou kit;
itens na mesma orientação e posição da foto 01; objeto de escala com tamanho real perto de produto pequeno; fundo com superfícies vazias
(nada em criado-mudo, aparador, prateleira); contagem de cada peça repetida; logo pequeno = sem close.
