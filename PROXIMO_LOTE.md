# Próximo lote: o essencial (leia só isto ao começar uma conversa nova)

Atualizado: 2026-11-09 madrugada (Lista 09/11 A entregue). Histórico completo: memoria/historico_lotes.md. Regras: CLAUDE.md. Lições: memoria/licoes_da_fabrica.md.

## Como começar
- Conversa nova, no mesmo projeto. Ela não lembra de conversas antigas: só o que está nos arquivos.
- Lote novo: a dona manda "Lote do dia: 15 produtos da Fila, teto US$ 8". Crie a conversa com model claude-opus-5-5.
- Agentes de conferência (Fichador, fiscais): model sonnet.
- Pasta do lote: video-teste/lote/lista<DDMM><letra> (cópia de video-teste/lote/modelo). Passos: CHECKLIST.md.
- No fim do lote: atualize só a seção "Estado atual" daqui (curta). O detalhe do lote (pulados, avisos, K22-K25) vai no TOPO de memoria/historico_lotes.md, não aqui (a dona, 10/11: menos contexto).

## Regras que não podem falhar
- TESTE K24 (01/11): produto "largo" usa a guia (foto 01 na posição certa, só o cômodo muda). No aviso final: quantas cenas largas
  passaram de 1ª e se o Nano Banana manteve o produto igual à foto. Olhe a guia.jpg de 1 produto antes de gerar o resto.
- TESTE K23 (a dona, 31/10): o 1º lote com cenas "com vida" (sol, plantas, enfeites simples) conta no aviso final quantas cenas foram
  reprovadas por enfeite (surgiu/mudou no vídeo, vaso parecendo garrafa). Se der problema, a dona quer VOLTAR ao fundo vazio (git revert f9d1011).
- Nada pago sem OK da dona e teto em dólar. Refazer uma imagem ou clipe pago só UMA vez. Reprovou 2x: entender o motivo, não gerar de novo.
- Todo produto sai com A, B e C. Versão reprovada pelo auditor é refeita só na edição (grátis).
- Produto sem cena aprovada (K22, 30/10): a fábrica monta A, B e C sozinha com as imagens reprovadas só por borda (câmera por código,
  grátis, sem_cena.py no produzir.sh) e manda para a Conferir com o aviso "cenas reprovadas pela fiscal: confira". Defeito grave fica
  fora. Sem imagem aproveitável: cartão "resgate" (nunca descartar sem a dona ver).
- SEMPRE, em todo lote (a dona, 28/10): vídeo pronto vai para a Conferência (aba Conferir da Postagens, 7HYeG...). Só o Ok da dona libera para Postagens (automático, sem o Claude). A Conferência fixada antiga (6An95...) agora é só um botão para a certa.
- Edição: layouts A "Um dia com ela", B "Faixas", C "Direto ao ponto". Música animada (musicas/biblioteca). Assinatura "Aguiiar Lar" muda de lugar no vídeo.
- Nunca subir chave, token, link de afiliado ou Sub ID em repositório público (este é privado).

## Páginas (mesmo endereço)
- Postagens + Conferência: https://claude.ai/artifact/7HYeGG32XBtjXTcMMoffJt (botão "Conferência →").
- Tinder: https://claude.ai/artifact/U1eK13L3ufz213GvJcXkni
- Jogo (Reino Encantado): https://claude.ai/artifact/XZAgnZ6G94M1vYAqo8hFAd

## Estado atual (10/11)
- Último lote: Lista 09/11 A (39 vídeos na Conferir, US$ 4,42). Fila do Tinder vazia: a dona aprova mais e pede o lote.
- Saldo WaveSpeed: confira com `curl -s https://api.wavespeed.ai/api/v3/balance` (~US$ 31 em 09/11).
- Varredura diária nova (10/11): produto-campeao/afiliados/busca_diaria.py + troca de excluídos com o Kevin (TROCA_EXCLUIDOS.md).
- Carrossel: salvar_imagens.py (fim da fase2) manda só produtos aesthetic (nota >= 8) ao Drive, Carrossel/<dia>/.
- O que cada lote anterior fez (pulados, avisos, K22-K25): memoria/historico_lotes.md (topo). Só leia se precisar.

## Redes sociais (Reels automático): PENDENTE
- Facebook e Instagram: funcionando (postar.py conferir).
- Threads: "Failed to decrypt". A dona trocou THREADS_TOKEN. Testar numa conversa nova; se falhar, gerar outra chave (developers.facebook.com > app > Casos de uso > API do Threads > Gerador de token).
- Reels: layouts A e C alternando (B fica só na Shopee). Ainda não há Reels prontos.
- Postagem automática: até 2 por dia por rede, 3 horas entre posts. Só posta com o OK da dona (produto, layout, legenda).
- Não postar nada sem a dona aprovar.

## Lembretes para a sessão nova (o que o Claude precisa fazer ao começar)
1. Ler este arquivo. Não reler o histórico inteiro.
2. Se a dona falar de redes: rodar `cd meta && python3 -I postar.py conferir` (não imprime tokens).
3. Se falar de lote: conferir a aba Conferir antes de criar outro lote.
