# Página Postagens (para quem posta: Kevin ou o irmão dele)

Página fixa: (sua página Postagens, veja paginas/) (um vídeo por vez, 4 passos: abrir produto e favoritar, baixar do Drive, copiar legenda, Postei).
Os vídeos NUNCA entram na página: ficam no Google Drive "<DRIVE_PASTA>/<AAAA-MM-DD>/". A página só guarda texto e miniatura.

No fim de cada lote, a thread de produção:
1. Envia os finais ao Drive: python3 video-teste/drive_backup.py <pasta dos finais> --dia AAAA-MM-DD
   Ele grava drive_links.json (nome do arquivo -> link do Drive) na pasta dos finais.
2. Só depois que o Kevin aprovar o vídeo na revisão, grava um documento por vídeo com ArtifactData (batch de até 50) na coleção "posts" da página:
   doc_id = nome do arquivo sem .mp4 (ex.: 2310_01_cadeira_A)
   {produto, versao ("Shopee A" | "Shopee B" | "Shopee C" | "Reels"), conta (onde postar), legenda,
    link_produto (link curto com Sub ID, vendas/link_subid.py), drive_url (de drive_links.json),
    poster (miniatura jpg 320 px em data URI, ~10 KB), dia (AAAA-MM-DD do lote), ordem (número), status: "pronto"}
3. Nunca o mesmo vídeo em duas contas. Vídeos postados ficam com status "postado" e postado_em.

Regra do Kevin (22/10 10:34): o link de afiliado de cada vídeo é SEMPRE gerado pela API (link_subid.py, grátis), com um Sub ID por vídeo, a partir do link do produto aprovado no Tinder (campo link: shopee.com.br/product/<loja>/<item>). Nunca usar link copiado à mão. Gerar todos de uma vez quando a fila fechar 45 e o lote for liberado, nunca a cada aprovação.

## Reels automáticos (Kevin 23/10)
O Kevin não posta mais Reels à mão. Na página Postagens, os Reels ficam só na aba "Reels auto" (somente leitura). Eles nunca aparecem em "Para postar".
- Ao gravar posts de um lote, o vídeo Reels leva `auto: true` e `status: "pronto"` (na fila). Também entra na fila do Postador Meta (meta/, fila_reels_<data>.json; postar.py e rodar_fila.sh).
- Depois de cada rodada do postador, quem rodou atualiza o doc posts/<arquivo sem .mp4> com status "postado", postado_em e redes {ig, fb, threads: permalink}, usando os dados de meta/postados.json.

## Esgotados (Kevin 2026-10-23)
- Coleção `esgotados/<dia-produto>`: produto, lote, link_produto, poster, drive_urls {A,B,C,Reels}, posts (cópia dos docs de posts não postados), marcado_em, conferir_em (+30 dias).
- Na Postagens: botão "Esgotado" ao lado de "Abrir e favoritar" (só no vídeo A) move todos os vídeos não postados do produto (inclusive o Reels da fila) para `esgotados`.
- Aba "Esgotados": ordenada por conferir_em; "Voltou ao estoque" recria os posts com status pronto (usa `posts` ou, se faltar, drive_urls) e apaga o esgotado; "Ainda esgotado" adia +30 dias.
- Páginas de revisão de lote gravam só em `esgotados`, nunca em posts.
