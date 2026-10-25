/* =====================================================================
   TEMA: AGUIIAR CREATIVE, O REINO ENCANTADO DAS DIVAS  (só aparência)
   ---------------------------------------------------------------------
   Este arquivo só decide COMO cada etapa aparece: nome encantado,
   construção, cores, personagem e fala. Ele não decide nada da produção.

   - Trocar o visual inteiro: troque este arquivo (e, se quiser, arte.js).
   - Nova personagem: mude o bloco "personagem" de uma estação.
   - Nova área: acrescente em "areas" (com "abre": uma aba ou um link).
   - Etapa nova no fluxo.js sem entrada aqui: aparece com o nome real e
     uma casinha padrão. Nada quebra.

   As chaves de "estacoes" são os ids de fluxo.js. Nunca mude esses ids aqui.

   Personagem: tipo gnoma | fada | elfa | coruja
     cabelo: solto | coque | trancas | rabo | curto
     chapeu: pontudo | coroa | laco | tiara | flores | nenhum
     acessorio: oculos+bolsa | prancheta | livro | camera | varinha | fones | lupa
                | cartas | cristal | moeda | tesoura | lanterna | claquete | espelho
                | luneta | grafico | frasco | trofeu  (pode juntar dois com "+")
   Construção (predio): portal | vila | castelo | torre | biblioteca | atelie
     | estufa | cinema | inspecao | salao | espelho | correio | observatorio
     | numeros | laboratorio | cofre | trofeus | casinha | mural
   ===================================================================== */
window.TEMA = {
  marca: "Aguiiar Creative",
  titulo: "O Reino Encantado das Divas",
  rodape: "Aguiiar Lar · fábrica de vídeos",

  /* Nomes das abas (a chave é fixa; o texto é livre) */
  abas: {
    castelo: "Castelo", floresta: "Floresta", conquistas: "Conquistas",
    mural: "Mural", cofre: "Cofre", brincar: "Brincar", perdas: "Desperdício"
  },

  /* Como cada estado real aparece */
  estados: {
    trabalhando: { rotulo: "Trabalhando", dica: "Fazendo sozinha, com faísca" },
    sua_vez:     { rotulo: "Sua vez",     dica: "Brilho rosa: precisa de você" },
    aguardando:  { rotulo: "Aguardando",  dica: "Descansando até chegar trabalho" },
    concluido:   { rotulo: "Concluído",   dica: "Estrelas e flores: tudo certo" },
    erro:        { rotulo: "Erro",        dica: "Nuvem de chuva: algo parou" }
  },

  niveis: [["Aprendiz", 0], ["Ajudante", .2], ["Gerente", .4], ["Chefona", .6], ["Rainha do Reino", .85]],

  estacoes: {
    tinder: { nome: "Portal das Descobertas", predio: "portal",
      cores: { parede: "#cfc1e6", telhado: "#9f86c8", detalhe: "#e8a7bd" },
      personagem: { nome: "Flora", titulo: "Gnoma caçadora", tipo: "gnoma", pele: "#f6d3bf", cabelo: "rabo", corCabelo: "#8a5a3c",
        roupa: "#8fae86", chapeu: "pontudo", corChapeu: "#6f8f63", acessorio: "oculos+bolsa" },
      fala: "Achei produtos com poucos vídeos. Venha escolher!" },

    fila: { nome: "Vila das Encomendas", predio: "vila",
      cores: { parede: "#f4e6d4", telhado: "#d98ba0", detalhe: "#c9a35b" },
      personagem: { nome: "Dália", titulo: "Gnoma guardiã", tipo: "gnoma", pele: "#e9bfa4", cabelo: "trancas", corCabelo: "#c27b4e",
        roupa: "#c97f95", chapeu: "pontudo", corChapeu: "#b56a82", acessorio: "lanterna" },
      fala: "As encomendas só saem da vila com o seu OK." },

    capataz: { nome: "Castelo da Diretora", predio: "castelo",
      cores: { parede: "#f6ede2", telhado: "#d792a7", detalhe: "#c9a35b" },
      personagem: { nome: "Rosa", titulo: "Gnoma diretora", tipo: "gnoma", pele: "#f3cdb6", cabelo: "solto", corCabelo: "#5a3527",
        roupa: "#b77fc2", chapeu: "coroa", corChapeu: "#d8b45e", acessorio: "prancheta" },
      fala: "Cada uma no seu posto, todas juntas!" },

    fichador: { nome: "Torre da Conferência", predio: "torre",
      cores: { parede: "#e7dccf", telhado: "#9f86c8", detalhe: "#a8bfa0" },
      personagem: { nome: "Íris", titulo: "Fada fiscal", tipo: "fada", pele: "#f7dccb", cabelo: "coque", corCabelo: "#d9b16a",
        roupa: "#a7c4d9", chapeu: "tiara", corChapeu: "#d8b45e", acessorio: "lupa" },
      fala: "Leio todas as fotos antes de qualquer gasto." },

    roteiro: { nome: "Biblioteca dos Encantos", predio: "biblioteca",
      cores: { parede: "#a67a5b", telhado: "#8fae86", detalhe: "#e8a7bd" },
      personagem: { nome: "Bela", titulo: "Gnoma roteirista", tipo: "gnoma", pele: "#d9a585", cabelo: "solto", corCabelo: "#2f1f1a",
        roupa: "#e8a7bd", chapeu: "laco", corChapeu: "#c26a86", acessorio: "livro" },
      fala: "Pergunta curta prende o dedo!" },

    estudio: { nome: "Ateliê das Imagens", predio: "atelie",
      cores: { parede: "#f6ede2", telhado: "#e3a0b4", detalhe: "#ffffff" },
      personagem: { nome: "Celeste", titulo: "Fada fotógrafa", tipo: "fada", pele: "#f6d3bf", cabelo: "curto", corCabelo: "#b9a4d8",
        roupa: "#f0c6d3", chapeu: "flores", corChapeu: "#e8a7bd", acessorio: "camera" },
      fala: "Casa linda, produto igualzinho." },

    fiscal_imagem: { nome: "Jardim da Qualidade", predio: "estufa",
      cores: { parede: "#d6e6d2", telhado: "#a8bfa0", detalhe: "#e8a7bd" },
      personagem: { nome: "Violeta", titulo: "Fada fiscal", tipo: "fada", pele: "#e9bfa4", cabelo: "trancas", corCabelo: "#6b3f5e",
        roupa: "#b9a4d8", chapeu: "flores", corChapeu: "#f2d27a", acessorio: "lupa" },
      fala: "Cor errada não passa do meu jardim." },

    camera: { nome: "Cinema das Fadas", predio: "cinema",
      cores: { parede: "#efe2f2", telhado: "#c97f95", detalhe: "#f2d27a" },
      personagem: { nome: "Aurora", titulo: "Elfa animadora", tipo: "elfa", pele: "#f3cdb6", cabelo: "solto", corCabelo: "#e9c77b",
        roupa: "#9f86c8", chapeu: "nenhum", corChapeu: "#f2d27a", acessorio: "varinha" },
      fala: "Ação! Bem devagarinho." },

    fiscal_video: { nome: "Torre da Inspeção", predio: "inspecao",
      cores: { parede: "#e4d9ec", telhado: "#6f8f63", detalhe: "#c9a35b" },
      personagem: { nome: "Safira", titulo: "Gnoma inspetora", tipo: "gnoma", pele: "#c98f6e", cabelo: "coque", corCabelo: "#1f1714",
        roupa: "#7fa2b8", chapeu: "pontudo", corChapeu: "#5f7a52", acessorio: "claquete" },
      fala: "Produto derreteu? Corta!" },

    edicao: { nome: "Salão da Edição", predio: "salao",
      cores: { parede: "#f4e6d4", telhado: "#9f86c8", detalhe: "#e8a7bd" },
      personagem: { nome: "Mel", titulo: "Gnoma editora", tipo: "gnoma", pele: "#f6d3bf", cabelo: "rabo", corCabelo: "#b5651d",
        roupa: "#e3a0b4", chapeu: "nenhum", corChapeu: "#c26a86", acessorio: "fones" },
      fala: "Corte no ritmo da música calma." },

    conferencia: { nome: "Espelho da Perfeição", predio: "espelho",
      cores: { parede: "#f6ede2", telhado: "#d8b45e", detalhe: "#e8a7bd" },
      personagem: { nome: "Você", titulo: "A dona do reino", tipo: "gnoma", pele: "#e9bfa4", cabelo: "solto", corCabelo: "#3a2420",
        roupa: "#d792a7", chapeu: "tiara", corChapeu: "#d8b45e", acessorio: "espelho" },
      fala: "Agora é com você, chefa. O espelho mostra o vídeo A." },

    postagens: { nome: "Correio das Estrelas", predio: "correio",
      cores: { parede: "#f4e6d4", telhado: "#7f9fc4", detalhe: "#f2d27a" },
      personagem: { nome: "Estela", titulo: "Gnoma carteira", tipo: "gnoma", pele: "#d9a585", cabelo: "trancas", corCabelo: "#5a3527",
        roupa: "#8fa7d0", chapeu: "pontudo", corChapeu: "#c97f95", acessorio: "cartas" },
      fala: "Vídeo na vitrine, venda chegando!" },

    postador_meta: { nome: "Observatório das Redes", predio: "observatorio",
      cores: { parede: "#e7dccf", telhado: "#9f86c8", detalhe: "#f2d27a" },
      personagem: { nome: "Lyra", titulo: "Elfa das redes", tipo: "elfa", pele: "#f7dccb", cabelo: "rabo", corCabelo: "#2f1f1a",
        roupa: "#8fae86", chapeu: "nenhum", corChapeu: "#d8b45e", acessorio: "luneta" },
      fala: "Espero minhas chaves novas para postar os Reels." },

    analista: { nome: "Torre dos Números", predio: "numeros",
      cores: { parede: "#efe2f2", telhado: "#7f9fc4", detalhe: "#b9a4d8" },
      personagem: { nome: "Clara", titulo: "Fada analista", tipo: "fada", pele: "#f3cdb6", cabelo: "coque", corCabelo: "#8a5a3c",
        roupa: "#a8bfa0", chapeu: "tiara", corChapeu: "#b9a4d8", acessorio: "grafico" },
      fala: "Quero saber qual gancho vende mais." },

    melhorador: { nome: "Laboratório dos Encantos", predio: "laboratorio",
      cores: { parede: "#f4e6d4", telhado: "#8fae86", detalhe: "#b9a4d8" },
      personagem: { nome: "Jade", titulo: "Gnoma alquimista", tipo: "gnoma", pele: "#e9bfa4", cabelo: "curto", corCabelo: "#6b3f5e",
        roupa: "#a8bfa0", chapeu: "pontudo", corChapeu: "#9f86c8", acessorio: "frasco" },
      fala: "O erro de hoje vira regra amanhã." }
  },

  /* Áreas especiais. "id" liga ao fluxo.js (áreas) quando existir lá. */
  areas: [
    { id: "painel", nome: "Castelo da Diretora", predio: "castelo", abre: { aba: "castelo" },
      cores: { parede: "#f6ede2", telhado: "#d792a7", detalhe: "#c9a35b" },
      personagem: { nome: "Rosa", titulo: "Gnoma diretora", tipo: "gnoma", pele: "#f3cdb6", cabelo: "solto", corCabelo: "#5a3527",
        roupa: "#b77fc2", chapeu: "coroa", corChapeu: "#d8b45e", acessorio: "prancheta" },
      fala: "Aqui você vê o reino inteiro de uma vez." },
    { id: "cofre", nome: "Cofre das Moedas", predio: "cofre", abre: { aba: "cofre" },
      cores: { parede: "#a67a5b", telhado: "#8fae86", detalhe: "#d8b45e" },
      personagem: { nome: "Dourada", titulo: "Gnoma tesoureira", tipo: "gnoma", pele: "#f6d3bf", cabelo: "coque", corCabelo: "#b5651d",
        roupa: "#d8b45e", chapeu: "pontudo", corChapeu: "#8fae86", acessorio: "moeda" },
      fala: "Nenhum centavo sai sem o seu OK." },
    { id: "metas", nome: "Jardim das Conquistas", predio: "trofeus", abre: { aba: "conquistas" },
      cores: { parede: "#f6ede2", telhado: "#a8bfa0", detalhe: "#d8b45e" },
      personagem: { nome: "Glória", titulo: "Fada dos troféus", tipo: "fada", pele: "#e9bfa4", cabelo: "solto", corCabelo: "#c27b4e",
        roupa: "#f2d27a", chapeu: "flores", corChapeu: "#e8a7bd", acessorio: "trofeu" },
      fala: "Cada meta cumprida floresce aqui." },
    { id: "takes", nome: "Ateliê dos Takes", predio: "casinha", abre: { folha: true },
      cores: { parede: "#f4e6d4", telhado: "#c97f95", detalhe: "#9f86c8" },
      personagem: { nome: "Lua", titulo: "Gnoma costureira", tipo: "gnoma", pele: "#c98f6e", cabelo: "trancas", corCabelo: "#1f1714",
        roupa: "#c8b6e2", chapeu: "laco", corChapeu: "#c97f95", acessorio: "tesoura" },
      fala: "Manda os takes que eu deixo lindo!" },
    { id: "mural", nome: "Mural Encantado", predio: "mural", abre: { aba: "mural" },
      cores: { parede: "#a67a5b", telhado: "#8fae86", detalhe: "#f4e6d4" },
      personagem: { nome: "Pena", titulo: "Corujinha mensageira", tipo: "coruja", roupa: "#b89a7a", corChapeu: "#e8a7bd", acessorio: "cartas" },
      fala: "Uh-uh! Trago as novidades do reino." }
  ],

  /* Casinha usada por qualquer etapa nova que ainda não tem tema */
  padrao: { predio: "casinha", cores: { parede: "#f4e6d4", telhado: "#b9a4d8", detalhe: "#e8a7bd" },
    personagem: { nome: "Ajudante", titulo: "Gnoma ajudante", tipo: "gnoma", pele: "#f3cdb6", cabelo: "solto", corCabelo: "#8a5a3c",
      roupa: "#c8b6e2", chapeu: "pontudo", corChapeu: "#9f86c8", acessorio: "prancheta" },
    fala: "Nova por aqui! Já estou trabalhando." }
};
