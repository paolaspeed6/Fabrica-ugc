/* =====================================================================
   FLUXO REAL DA FÁBRICA  (dados, sem nada de aparência)
   ---------------------------------------------------------------------
   Aqui ficam as etapas de verdade, na ordem da produção, com o nome real,
   o que cada uma faz, o que entra, o que sai, o custo e os links.
   O visual (nomes encantados, personagens, construções) fica em tema.js.
   Trocar o tema NUNCA muda este arquivo. Mudar a produção = mudar aqui
   (e nos scripts da fábrica), nunca no tema.

   Cada etapa tem um "id" fixo. O tema e o banco (reino/estado) usam esse id.
   quem: "claude" = o Claude faz sozinho | "voce" = depende de você.
   ===================================================================== */
window.FLUXO = (() => {
  const L = {
    tinder: "https://claude.ai/artifact/U1eK13L3ufz213GvJcXkni",
    post: "https://claude.ai/artifact/7HYeGG32XBtjXTcMMoffJt",
    conf: "https://claude.ai/artifact/6An95qPxcauMJb3p1umWXk"
  };

  const etapas = [
    { id: "tinder", nome: "Ilha do Tinder", papel: "Caçadora de produtos", quem: "voce",
      faz: "Todo dia de manhã a varredura procura na Shopee produtos bons com poucos vídeos de criadores e coloca os cartões no Tinder. Você arrasta para a direita o que quer em vídeo.",
      entra: "Busca diária na Shopee", sai: "Produtos aprovados vão para a Fila", custo: "Grátis",
      acao: [["Abrir Tinder", L.tinder]] },
    { id: "fila", nome: "Fila", papel: "Porteiro do lote", quem: "voce",
      faz: "Quando a Fila junta 15 produtos, eu te digo o custo do lote: quantos produtos, custo por produto e total. Só depois do seu OK a máquina liga.",
      entra: "Produtos aprovados", sai: "Lote liberado", custo: "Teto por lote, aprovado por você",
      acao: [["Abrir Tinder", L.tinder]], comando: "Pode produzir o lote da Fila" },
    { id: "capataz", nome: "Capataz", papel: "Orquestradora", quem: "claude",
      faz: "Divide o lote em grupos de 3 a 5 produtos e põe os agentes para trabalhar ao mesmo tempo, cada um num agente separado. Também cria os links de afiliado com Sub ID de cada vídeo.",
      entra: "Lote liberado", sai: "Grupos trabalhando juntos", custo: "Grátis" },
    { id: "fichador", nome: "Fichador", papel: "Trava 1", quem: "claude",
      faz: "Lê TODAS as fotos do anúncio e monta a ficha: cor da foto 01, quantos itens, letras exatas da marca, tamanho real pelas medidas e onde fica cada peça. Ninguém gasta antes da ficha pronta.",
      entra: "Link do produto", sai: "Ficha do produto", custo: "Grátis" },
    { id: "roteiro", nome: "Sala de roteiro", papel: "Roteirista", quem: "claude",
      faz: "Acha o ângulo que vende, escreve o gancho (pergunta ou problema, nunca o de horas quando não combina) e a chamada de cada versão, e os comandos de cena. Só qualidades reais.",
      entra: "Ficha + regras da fábrica", sai: "Roteiro e comandos de cena", custo: "Grátis" },
    { id: "estudio", nome: "Estúdio de foto", papel: "Nano Banana", quem: "claude",
      faz: "Cria as cenas novas usando as fotos reais do anúncio como base, nunca inventando o produto do zero. Luz de janela, casa elegante, nada de cara de catálogo.",
      entra: "Fotos do anúncio + comando", sai: "Imagens das 3 cenas", custo: "US$ 0,04 por imagem" },
    { id: "fiscal_imagem", nome: "Fiscal de imagem", papel: "Trava 2", quem: "claude",
      faz: "Compara cada imagem com a ficha e as fotos do anúncio. Reprova cor, letra, tamanho errado ou peça fora do lugar antes de gastar com vídeo.",
      entra: "Imagens", sai: "Aprovada ou reprovada", custo: "Grátis" },
    { id: "camera", nome: "Câmera", papel: "Animador", quem: "claude",
      faz: "Câmera andando devagar, avanço curto, produto parado em tamanho real. O comando leva só nome, itens, peças e escala.",
      entra: "Imagens aprovadas", sai: "Cenas em vídeo", custo: "Seedance US$ 0,10 por 5 s; Veo 3.1 Lite US$ 0,20 por 4 s só se precisar" },
    { id: "fiscal_video", nome: "Fiscal de vídeo", papel: "Trava 3", quem: "claude",
      faz: "Assiste cada cena e corta trechos onde o produto escorrega, gira, derrete, muda de peça, ganha objeto novo ou aparece mão. Se não salvar, pede para refazer só uma vez.",
      entra: "Cenas em vídeo", sai: "Trechos limpos", custo: "Grátis" },
    { id: "edicao", nome: "Ilha de edição", papel: "Editora", quem: "claude",
      faz: "Monta os vídeos de 15 s nos seus 3 layouts: A Um dia com ela, B Faixas moderno, C Direto ao ponto. Estilo natural sem filtro, transições whip e zoom, só os melhores momentos, sem voz e com música calma. Aguiiar Lar fixo no topo. Depois: Drive e Conferência, sempre.",
      entra: "Trechos limpos + roteiro", sai: "3 vídeos prontos por produto", custo: "Grátis" },
    { id: "conferencia", nome: "Conferência", papel: "Você confere", quem: "voce",
      faz: "Uma página só com o que falta conferir, de todos os lotes. Cada produto mostra o vídeo A. Toque OK, Editar, Descartar ou Esgotado e já fica salvo. Depois toque Avisar o Claude.",
      entra: "Vídeos prontos", sai: "OK vai para Postagens. Editar volta corrigido. Descartar volta para a Fila", custo: "Grátis",
      acao: [["Abrir Conferência", L.conf]], comando: "Terminei a Conferência, processa" },
    { id: "postagens", nome: "Postagens", papel: "Você posta", quem: "voce",
      faz: "Os vídeos aprovados vão para o Drive e para a página Postagens. Lá você salva o vídeo, copia a legenda, posta na Shopee e toca em Postei. Produto que esgotou fica separado.",
      entra: "Vídeos aprovados", sai: "Vídeos postados na Shopee", custo: "Grátis",
      acao: [["Abrir Postagens", L.post]] },
    { id: "postador_meta", nome: "Postador Meta", papel: "Robô das redes", quem: "claude",
      faz: "Pega o Reels de cada produto e publica no Instagram, no Facebook e no Threads, num ritmo seguro para conta nova: até 2 por dia, 3 horas entre eles. Aviso de spam pausa aquela rede por 24 h.",
      entra: "Reels prontos", sai: "Reels no Instagram, Facebook e Threads", custo: "Grátis" },
    { id: "analista", nome: "Analista", papel: "Contador de vendas", quem: "claude",
      faz: "Lê as vendas e cliques por Sub ID e descobre qual versão e qual gancho vendem mais. Os vencedores vão para o banco de ganchos. Liga junto com a chave da Shopee.",
      entra: "Vendas por Sub ID", sai: "Ganchos e lições novas", custo: "Grátis" },
    { id: "melhorador", nome: "Melhorador", papel: "Trava 4", quem: "claude",
      faz: "Uma vez por lote, depois da sua conferência, corrige as regras e os comandos para o erro não se repetir. Aí a estrada volta para o começo, mais esperta.",
      entra: "Sua conferência + defeitos", sai: "Regras melhores para o próximo lote", custo: "Grátis" }
  ];

  /* Áreas fora da estrada. "aba" abre uma aba desta página; "acao" abre outra página. */
  const areas = [
    { id: "painel", nome: "Painel da fábrica", papel: "Indicadores e missões", aba: "castelo",
      faz: "O resumo do dia: vídeos postados, produtos andando, o que espera o seu OK, gastos, etapas rodando e metas." },
    { id: "cofre", nome: "Gasto total", papel: "Gastos, orçamento e teto", aba: "cofre",
      faz: "Teto de R$ 3 por produto. Cada gasto pago tem teto antes e o seu OK. Todo vídeo refeito ou perdido entra no registro de desperdícios.",
      entra: "Seu OK", sai: "Gasto controlado", custo: "WaveSpeed, recarga feita por você" },
    { id: "metas", nome: "Metas", papel: "Troféus e nível", aba: "conquistas",
      faz: "Cada meta cumprida vale um troféu e sobe o seu nível." },
    { id: "takes", nome: "Ateliê dos takes", papel: "Seus takes", quem: "voce",
      faz: "Você manda os takes (Veo, Hailuo) e o link do produto aqui no chat. Eu edito nos seus 3 layouts, só com os melhores momentos, e entrego numa página com botão de baixar.",
      entra: "Seus takes + link", sai: "3 vídeos por produto", custo: "Grátis" },
    { id: "mural", nome: "Mural das correções", papel: "Avisos e atividades", aba: "mural",
      faz: "Tudo o que já foi corrigido e o que ainda vai ser, com a data." }
  ];

  /* Tarefas que rodam sozinhas (fora da estrada) */
  const automaticas = [
    { id: "varredura", nome: "Varredura do Tinder", quando: "todo dia de manhã" },
    { id: "reels", nome: "Reels automáticos", quando: "Instagram, Facebook e Threads" },
    { id: "contador", nome: "Contador de postados", quando: "todo dia às 23:55" }
  ];

  const missoes = [
    { id: "takes", n: "Mandar takes para editar", agora: "Quando quiser",
      t: "Mande os takes e o link do produto aqui no chat. Eu edito nos seus 3 layouts e entrego com botão de baixar." },
    { id: "tinder", n: "Escolher produtos", agora: "Quando a varredura trouxer cartões",
      t: "Arraste para a direita o que merece vídeo. Com 15 na Fila, eu te mando o custo do lote e espero o seu OK.", acao: [["Abrir Tinder", L.tinder]] },
    { id: "conferencia", n: "Conferir vídeos", agora: "Quando eu avisar que um lote ficou pronto",
      t: "Veja o vídeo A de cada produto e toque OK, Editar, Descartar ou Esgotado. No fim, toque Avisar o Claude.", acao: [["Abrir Conferência", L.conf]] },
    { id: "postagens", n: "Postar na Shopee", agora: "Depois do seu OK na Conferência",
      t: "Salve o vídeo, copie a legenda, poste no app e toque Postei.", acao: [["Abrir Postagens", L.post]] }
  ];

  const comandos = [
    ["Pode produzir o lote da Fila", "libera o próximo lote"],
    ["Terminei a Conferência, processa", "OK vai para Postagens"],
    ["Roda a varredura do Tinder agora", "cartões novos"],
    ["Quanto gastei até agora?", "placar do dinheiro"],
    ["Atualiza o reino", "estados, metas e mural"],
    ["Anota no mural: ", "correção nova com data"]
  ];

  const paginas = [
    ["Tinder", "escolher produtos", L.tinder],
    ["Conferência", "OK, Editar, Descartar, Esgotado", L.conf],
    ["Postagens", "postar e ver esgotados", L.post]
  ];

  const leis = [
    "Nada pago sem o seu OK, sempre com teto de gasto antes.",
    "Produto igual à foto 01 do anúncio: cor, peças, letras e todos os itens.",
    "Só qualidades reais do anúncio. Sem prazo de entrega, sem %, sem nota exata, sem bebida.",
    "Produto inteiro na capa, sem mão. Cada vídeo começa com um take diferente.",
    "15 segundos, estilo natural sem filtro, sem voz e com música calma. \"Aguiiar Lar\" fixo no topo.",
    "Vídeo que não dá pra postar vira perda no registro e volta para a Fila."
  ];

  /* Números da regra de dinheiro (CLAUDE.md). Mudou lá, mude aqui. */
  const teto = { porProduto: 3, moeda: "BRL", custoMedioUSD: 0.42, cambio: 5.69, travas: 4, layouts: 3 };

  /* Etapas que contam como "produto andando" (entre o OK do lote e a Conferência) */
  const producao = ["capataz", "fichador", "roteiro", "estudio", "fiscal_imagem", "camera", "fiscal_video", "edicao"];

  const monstros = [
    { n: "Encolhedor", usd: "4,48", o: "Cadeiras, PC gamer, cozinha, arara, berço e banquetas saíram em miniatura. A faixa fixa do layout encolhia produto grande.",
      r: "Tamanho real sempre: linha de escala em todo comando, kit de N com N unidades inteiras, medidas lidas em todas as fotos." },
    { n: "Fantasma do prompt", usd: "3,64", o: "O comando de vídeo citava a lista do que não pode aparecer. O modelo desenhou exatamente isso: taças, vasos, cotas, 3ª cadeira, texto na parede.",
      r: "Comando de vídeo leva só nome, itens, peças e escala. Nada de proibidos, textos do anúncio ou outras cores." },
    { n: "Barrados na porta", usd: "3,57", o: "Imagens e clipes com letra errada, produto encostando na borda, peça girando. Os fiscais pegaram antes de virar vídeo ruim.",
      r: "Fiscal de imagem antes de animar e fiscal de vídeo antes de editar." },
    { n: "Torto do quadro", usd: "2,81", o: "Produto grande ou pequeno demais, fora do espaço entre o texto e a chamada.",
      r: "Prévia de enquadramento em código antes de gerar." },
    { n: "Eco do lote", usd: "0,92", o: "Clipes a mais, imagens refeitas por enquadramento e imagens perdidas por erro de gravação do registro.",
      r: "Um contador de gasto por lote e o registro salvo antes de cada pedido pago." },
    { n: "Sumidor de itens", usd: "0,92", o: "O relógio tinha 2 modelos na foto 01 e o vídeo mostrou 1. O monitor duplo saiu com 1 tela.",
      r: "Se a foto 01 mostra 2 ou mais itens, todo vídeo mostra todos, na mesma quantidade e arrumação." },
    { n: "Fora de lugar", usd: "0,42", o: "A cadeirinha de carro apareceu no chão da sala, como se fosse cadeira de casa.",
      r: "Cenário do uso real do produto e cenários variados entre as versões." }
  ];
  const testes = [
    ["Receita nova de qualidade (2 testes, Nano Banana + Veo e Seedance)", "0,97", "mostrou que com câmera andando de verdade o Seedance deforma o produto e criou os fiscais"],
    ["Primeiro teste", "0,12", "provou a fábrica de ponta a ponta"]
  ];
  const aprender = [
    ["Ficha antes de tudo.", "Contar os itens da foto 01, ler as medidas e as letras da marca. Grátis."],
    ["Prévia de enquadramento em código.", "Mostra se o produto cabe entre o texto e a chamada antes de gerar. Grátis."],
    ["Ler as regras de erros", "antes de cada roteiro, comando ou geração. Grátis."],
    ["Checar textos:", "só fatos do anúncio, nada de %, prazo ou nota. Grátis."],
    ["Fiscal de imagem antes de animar.", "Uma imagem errada custa US$ 0,04; o vídeo dela custaria US$ 0,10 a 0,20."],
    ["Teste de 1 cena", "antes de um modelo novo ou de um lote com regra nova."],
    ["Teto no script.", "Todo gasto roda com limite em dólar e para sozinho."],
    ["Comparar com os vídeos de referência", "antes de entregar. Grátis."],
    ["Sua marcação \"Editar\"", "vira regra nova pelo Melhorador, para o erro não voltar."]
  ];

  return { links: L, etapas, areas, automaticas, missoes, comandos, paginas, leis, teto, producao, monstros, testes, aprender };
})();
