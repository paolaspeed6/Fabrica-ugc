# Postagem nas redes, 6 por dia (a dona, 28/10)

- Vídeos: coleção `posts` da Postagens com status `pronto` ou `postado` (já postado na Shopee também vale), só layouts **A e C**,
  alternando A, C, A, C, lote mais novo primeiro.
  O B fica só para a Shopee. Postar nas redes NÃO muda o status do doc (ela ainda posta na Shopee à mão).
- Redes: Instagram (Reels), Facebook (Reels da Página) e Threads, o mesmo vídeo nas 3.
- Horários (Brasília, pico): 08:07, 11:07, 13:07, 17:07, 19:07, 21:07. 1 vídeo por horário, máximo 6 por dia.
- Legenda: Gemini (grátis) com gancho, benefício real, "💬 Link nos comentários 👇" e 8 a 12 hashtags; cache em
  `legendas_redes.json` (a do `--seco` é a mesma que vai ao ar).
- Link: a chave da Meta NÃO tem `pages_manage_engagement` nem `instagram_manage_comments` (28/10); enquanto faltar, o script põe
  a mensagem + link na legenda do Facebook e do Instagram (no lugar de "Link nos comentários"). No Threads o comentário funciona.
- 1º comentário: "🛒 Gostou? Só copiar o link e colar no WhatsApp que abre direto na Shopee 👇" + link de afiliada da dona
  (`link_produto` do doc). No Threads o comentário é uma resposta ao próprio post.
- Registro + legendas: doc `redes/estado` do banco da Postagens (a tarefa agendada não tem push no GitHub, 28/10). Nunca reposta. Aviso de spam pausa a rede 24 h (`pausas.json`).

## Cada disparo da tarefa agendada (trig_01SbdhGUDGc1uRG5H4x7aehs)
O passo a passo está no prompt da própria tarefa: query posts (com cursor) → get redes/estado → redes_diario.py --estado → set redes/estado.
