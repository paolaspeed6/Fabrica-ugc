# Fábrica Shopee: comece aqui

A mesma fábrica do Kevin, na nuvem (claude.ai/code) ou no seu PC, com as suas contas e o seu dinheiro: Tinder de produtos, 4 vídeos de 15 s por produto,
página Conferência, backup no Drive, página Postagens e postagem automática no Instagram, Facebook e Threads.
O Claude faz tudo e pede o seu OK antes de qualquer gasto.

## Instalar (uma vez, uns 40 minutos)
1. **Python 3.10 ou mais novo** (python.org). No Windows marque "Add Python to PATH".
2. **ffmpeg**: Windows `winget install ffmpeg`; Mac `brew install ffmpeg`.
3. **Git for Windows** (só no Windows; git-scm.com). O Claude Code usa o Git Bash dele.
4. **Claude Code**: siga code.claude.com/docs e entre com a sua conta Claude (Pro ou Max).
5. Descompacte este kit numa pasta, por exemplo `Documentos/fabrica-shopee`.
6. Abra o terminal nessa pasta e rode `pip install -r requirements.txt` (baixa uns 2 GB na primeira vez; é normal).
7. Crie as contas e as chaves do `CONTAS.md`.
8. Na pasta do kit, rode `claude`. Ele lê o `CLAUDE.md` sozinho e já sabe o fluxo e todas as regras.

## Primeira conversa com o Claude
1. "Publique minhas páginas Tinder, Conferência e Postagens." Fixe no celular. (O Mapa da Fábrica é opcional: diga como quer o visual.)
   Mostre ao Claude os seus layouts de edição para ele usar os seus.
2. "Confira minhas chaves." Ele testa Shopee, WaveSpeed, Drive e Meta sem gastar.
3. "Faça a primeira varredura." Leva cerca de 1h45 e é grátis. Os produtos aparecem no Tinder.
4. Aprove alguns no Tinder e peça "teste com 1 produto". Ele diz o custo (uns US$ 0,42) e espera o seu OK.

## Dia a dia
- Varredura sozinha às 6h: agende `varredura.bat` no Agendador de Tarefas do Windows (ou peça ao Claude como fazer).
  Depois diga ao Claude "suba a varredura no Tinder".
- Arraste no Tinder: direita aprova, esquerda descarta.
- Fila cheia: o Claude avisa o custo do lote e espera o seu OK.
- Ele entrega uma página de revisão. Marque "corrigir" só no que quer mudar.
- Aprovados vão para o Drive e para a página Postagens (baixar, copiar legenda, Postei).
- Postagem automática: "poste o lote de hoje no Instagram, Facebook e Threads". Ele mostra o plano antes e posta só com o seu OK.

## O que tem aqui
- `CLAUDE.md`: o fluxo que o Claude segue.
- `CONTAS.md`: o que você cria e onde.
- `agentes/`: todas as regras e lições (`regras_de_erros.md` tem cada erro que já custou dinheiro).
- `produto-campeao/`: varredura do Tinder, fotos do anúncio e links de afiliado com Sub ID.
- `video-teste/`: montagem, render, revisão e backup no Drive. Modelo de lote em `video-teste/lote/modelo/`.
- `musicas/`: OPCIONAL. 30 trilhas livres de direitos, o gerador para criar as suas, ou nenhuma música. Você escolhe.
- `meta/postar.py`: postagem automática.
- `paginas/`: Tinder, Conferência, Postagens e o Mapa da Fábrica (o jogo; o visual você escolhe com o Claude).
- `memoria/licoes_da_fabrica.md`: todas as lições da fábrica original, sem dados pessoais.
- `TAREFAS_AGENDADAS.md`: varredura diária, contador e Reels automáticos.
- `skills/`: extras de design e animação (opcional).
- Edição: os seus layouts continuam sendo os seus. Os modelos do kit (`video-teste/luxo/`) ficam só como opção.

Custos medidos (out/2026): cerca de US$ 0,42 por produto (4 vídeos), uns R$ 2,40. Um lote de 15 produtos fica em torno de US$ 6,30.
