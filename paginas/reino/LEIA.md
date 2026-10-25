# Reino Encantado das Divas (o jogo da fábrica)

Página publicada no MESMO link do jogo antigo (veja `MINHAS_PAGINAS.md`). Banco da página: capabilities `{db: {}, user: {}}`.
Substitui `paginas/mapa.html` (que fica só como versão antiga, para voltar se precisar).

## As peças (aparência separada da produção)

| Arquivo | O que tem | Pode mudar sem medo? |
|---|---|---|
| `fluxo.js` | As 15 etapas REAIS (nome, o que faz, entra, sai, custo, links), áreas, missões, comandos, leis, teto | Só quando a produção mudar de verdade |
| `tema.js` | Nomes encantados, construção, cores, personagem e fala de cada etapa; nomes das abas e dos estados | Sim. É o visual |
| `arte.js` | Desenhos em SVG: personagens, construções, floresta, encomendas | Sim. Só desenho |
| `motor.js` | Lê o banco e liga cada etapa à sua casinha pelo estado real | Só para mudar comportamento da página |
| `jogos.js` | Os 3 jogos (Pode ou não pode, Memória, Poço dos ganchos) | Sim |
| `sincronizar.py` + `manual.json` | Montam o estado real de cada etapa | `manual.json` sim, a cada passo do lote |

Nenhum desses arquivos é usado pelos scripts de produção (gerar.py, fiscais, edição, Drive, Conferência, postagem).
Trocar o tema nunca muda a produção. O elo entre os dois é só o `id` de cada etapa (`tinder`, `fila`, `capataz`, `fichador`,
`roteiro`, `estudio`, `fiscal_imagem`, `camera`, `fiscal_video`, `edicao`, `conferencia`, `postagens`, `postador_meta`,
`analista`, `melhorador`). Nunca renomeie um id só por causa do visual.

## Receitas
- **Nova personagem ou roupa:** em `tema.js`, mude o bloco `personagem` da estação (tipo gnoma/fada/elfa/coruja, cabelo, cores,
  chapéu, acessório). Os nomes aceitos estão no topo do arquivo. Acessório novo = desenhar em `arte.js` (NA_MAO ou NO_CORPO).
- **Nova construção:** desenhe uma função em `ARTE.PREDIOS` e use o nome em `predio` no tema.
- **Nova área especial:** acrescente em `TEMA.areas` com `abre: {aba: "..."}` ou `abre: {link: "https://..."}`
  (e, se for coisa real da fábrica, a descrição em `FLUXO.areas` com o mesmo `id`).
- **Etapa nova na produção:** primeiro na fábrica de verdade; depois em `fluxo.js`. Sem tema, ela aparece com o nome real
  e a casinha padrão. Depois, se quiser, dê um visual em `tema.js`.
- **Trocar o tema inteiro:** faça outro `tema.js` (e `arte.js` se quiser outros desenhos). `fluxo.js` e `motor.js` ficam.

## Estado real das casinhas (doc `reino/estado`)
Estados: `trabalhando` (Claude fazendo), `sua_vez` (precisa da dona), `aguardando`, `concluido`, `erro`.
Formato: `{atualizado_em, fonte, etapas: {<id>: {estado, texto, qtd, itens[]}}, automaticas: {varredura|reels|contador: {ligada, texto}}, recentes: [{quando, etapa, texto}]}`.
Sem o doc, a página mostra "sem notícia" (nunca inventa estado). `qtd` = produtos reais naquela etapa (viram encomendas no mapa;
quando a etapa está `trabalhando`, uma encomenda anda pela trilha até a próxima).

**"Atualiza o reino"** (grátis, só leitura das outras páginas):
1. ArtifactData `list` com `out_dir=<pasta>`: Tinder `candidatos` (paginar com cursor até o fim), Conferência `conferir`,
   Postagens `posts`. Coleção vazia: crie a pasta vazia (`mkdir <pasta>/posts`) para contar como "zero", não "sem notícia".
2. `python3 -I paginas/reino/sincronizar.py <pasta> <pasta>/reino_estado.json`
3. ArtifactData `set` coleção `reino`, doc `estado`, `file_path=<pasta>/reino_estado.json` (pinar `if_version` se já existir).

Durante um lote (opcional, não é etapa obrigatória da produção): ao trocar de etapa, ponha em `manual.json`
`"lote": {"nome": "Lista DD/MM X", "etapa": "<id>", "produtos": [...], "erro": null}` e rode os passos acima.
Fim do lote: `"lote": null` e `"ultimo_lote": "Lista DD/MM X"`. Tarefa agendada ligada/desligada: `automaticas` no `manual.json`.
Algo parou: `"etapas": {"<id>": {"estado": "erro", "texto": "o que parou e como resolver"}}` (some quando resolver).

## Publicar
Artifact `publish` com `url` do jogo, `file_path` = `paginas/reino/index.html` e
`files` = `{"fluxo.js","tema.js","arte.js","motor.js","jogos.js"}` (mesmos nomes). Não passar `capabilities` (mantém db e user).
Antes, ler a versão publicada (`action: read`).
