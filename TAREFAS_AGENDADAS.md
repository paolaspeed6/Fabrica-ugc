# Tarefas agendadas (criar uma vez)

Na nuvem (claude.ai/code): peça ao Claude "crie as tarefas agendadas do TAREFAS_AGENDADAS.md". Ele cria cada uma como
tarefa agendada (rotina) do projeto, rodando numa conversa nova a cada vez, no mesmo ambiente com os segredos.
No PC: Agendador de Tarefas do Windows com `varredura.bat` (só a varredura; o resto você pede no chat).
Antes de criar, troque as URLs entre <> pelas suas (estão em `MINHAS_PAGINAS.md`).

## 1. Varredura diária do Tinder (todo dia 6:47, America/Sao_Paulo)
Texto da tarefa:
> Varredura diária do Tinder Shopee. Leia o CLAUDE.md e a memoria/licoes_da_fabrica.md.
> 1. Leia o banco da página Tinder (<URL do Tinder>, coleção candidatos). Se houver 10 ou mais decisões novas
>    (aprovado/descartado desde a última rodada, ver produto-campeao/afiliados/ultima_rodada.json), compare aprovados x
>    descartados, ajuste varrer.py/palavras.txt e anote o aprendizado em agentes/busca_poucos_videos.md.
> 2. Rode a varredura destacada (pode passar de 2 h):
>    `cd produto-campeao/afiliados && setsid nohup bash -c 'timeout 10800 python3 varrer.py > varredura_diaria.log 2>&1; echo "exit=$?" > varredura_diaria.fim' &`
>    e espere o arquivo .fim (laço em segundo plano, no máximo 2 h por espera, rearmando). Apague o .fim no fim.
> 3. Some TODOS os bons resultados novos no Tinder (status novo, campo dia = hoje), em lotes de no máximo 25 documentos.
>    Nunca repita itemId (vistos.json); parecido da mesma loja só ganha possivel_duplicata. Atualize vistos.json e ultima_rodada.json.
> 4. Se a Fila (status aprovado) chegou ao lote_min de config/geral: avise "Lote DD/MM pronto, N produtos, custo estimado US$ X"
>    e espere o OK. Nada pago nesta tarefa.

## 2. Contador de postados do Mapa (todo dia 23:55, America/Sao_Paulo)
> Leia a coleção posts da página Postagens (<URL das Postagens>) e salve cada doc com status postado como JSON numa pasta
> temporária. Rode `python3 mapa/resumo_postados.py <pasta>` e grave o JSON impresso em postagens_resumo/atual no banco da
> página Mapa (<URL do Mapa>). Não mude mais nada.

## 3. Fila dos Reels automáticos (opcional, 2 vezes por dia, ex. 10:00 e 19:00)
> Monte a fila dos Reels com status pronto e auto true da página Postagens (formato em agentes/postagens_formato.md e no topo de
> meta/postar.py), rode `MAX_DIA=2 INTERVALO_H=3 bash meta/rodar_fila.sh fila.json` e sincronize os docs posts com
> meta/postados.json (status, permalinks em redes). Aviso de spam: a rede fica pausada 24 h (pausas.json); nunca insista.
Só crie esta depois de a dona aprovar o primeiro plano de postagem com `--seco`.

## Dicas
- Uma conversa nova por rodada gasta menos uso do plano Claude que uma conversa longa.
- Se a varredura começar a passar de 3 h (palavras.txt muito grande), limite as páginas por palavra no varrer.py.
- O banco do Tinder guarda miniaturas (~35 KB por produto; limite 100 MB): com umas 2.500 cartas, limpe os descartados antigos.
