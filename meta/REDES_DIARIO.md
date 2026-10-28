# Postagem nas redes, 6 por dia (a dona, 28/10)

- Vídeos: os da aba "Para postar" da Postagens (coleção `posts`, status `pronto`), só layouts **A e C**, alternando A, C, A, C.
  O B fica só para a Shopee. Postar nas redes NÃO muda o status do doc (ela ainda posta na Shopee à mão).
- Redes: Instagram (Reels), Facebook (Reels da Página) e Threads, o mesmo vídeo nas 3.
- Horários (Brasília, pico): 08:07, 11:07, 13:07, 17:07, 19:07, 21:07. 1 vídeo por horário, máximo 6 por dia.
- Legenda: Gemini (grátis) com gancho, benefício real, "💬 Link nos comentários 👇" e 8 a 12 hashtags; cache em
  `legendas_redes.json` (a do `--seco` é a mesma que vai ao ar).
- 1º comentário: "🛒 Gostou? Só copiar o link e colar no WhatsApp que abre direto na Shopee 👇" + link de afiliada da dona
  (`link_produto` do doc). No Threads o comentário é uma resposta ao próprio post.
- Registro: `postados_redes.json` (nunca reposta). Aviso de spam pausa a rede 24 h (`pausas.json`).

## Cada disparo da tarefa agendada (conversa nova, gastar o mínimo)
1. ArtifactData query na Postagens (https://claude.ai/artifact/7HYeGG32XBtjXTcMMoffJt), coleção `posts`,
   where status == pronto, limit 1000, out_dir `<scratchpad>/posts`.
2. `cd meta && python3 -I redes_diario.py <scratchpad>/posts` (Bash, timeout 600000).
3. `git add meta/postados_redes.json meta/legendas_redes.json meta/pausas.json; git commit; git push origin main`.
4. Resposta de 1 linha: o que postou ou por que não postou. Não ler outros arquivos, não mexer em mais nada.
