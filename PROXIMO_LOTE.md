# Próximo lote: o essencial (leia só isto ao começar uma conversa nova)

Atualizado: 2026-10-28 (20h45 UTC). Histórico completo: memoria/historico_lotes.md. Regras: CLAUDE.md. Lições: memoria/licoes_da_fabrica.md.

## Como começar
- Conversa nova, no mesmo projeto. Ela não lembra de conversas antigas: só o que está nos arquivos.
- Lote novo: a dona manda "Lote do dia: 15 produtos da Fila, teto US$ 8". Crie a conversa com model claude-opus-5-5.
- Agentes de conferência (Fichador, fiscais): model sonnet.
- Pasta do lote: video-teste/lote/lista<DDMM><letra> (cópia de video-teste/lote/modelo). Passos: CHECKLIST.md.

## Regras que não podem falhar
- Nada pago sem OK da dona e teto em dólar. Refazer uma imagem ou clipe pago só UMA vez. Reprovou 2x: entender o motivo, não gerar de novo.
- Todo produto sai com A, B e C. Versão reprovada pelo auditor é refeita só na edição (grátis).
- Produto sem cena aprovada vira "resgate" na aba Conferir. Nunca descartar sem a dona ver.
- SEMPRE, em todo lote (a dona, 28/10): vídeo pronto vai para a Conferência (aba Conferir da Postagens, 7HYeG...). Só o Ok da dona libera para Postagens (automático, sem o Claude). A Conferência fixada antiga (6An95...) agora é só um botão para a certa.
- Edição: layouts A "Um dia com ela", B "Faixas", C "Direto ao ponto". Música animada (musicas/biblioteca). Assinatura "Aguiiar Lar" muda de lugar no vídeo.
- Nunca subir chave, token, link de afiliado ou Sub ID em repositório público (este é privado).

## Páginas (mesmo endereço)
- Postagens + Conferência: https://claude.ai/artifact/7HYeGG32XBtjXTcMMoffJt (botão "Conferência →").
- Tinder: https://claude.ai/artifact/U1eK13L3ufz213GvJcXkni
- Jogo (Reino Encantado): https://claude.ai/artifact/XZAgnZ6G94M1vYAqo8hFAd

## Estado atual (28/10)
- Lote 28/10 A (28/10 20h40 UTC): 14 produtos com A, B e C (42 vídeos, 2810A-02..20) + 2810A-13 Colchão Ortho Flex como resgate,
  na aba Conferir. Gasto US$ 6,18 de 8 (60 imagens + 38 clipes). Pulados pelo Fichador (Tinder segue `aprovado`): Kit Cooktop+Balcão
  58254841155 (colagem), Viveiro 58265685456 (sem foto limpa), Radiador Kombi 58211200606 (colagem), Banco Kulmai 58209960104
  (modelos misturados), Chave de impacto 1200 N.m 58263626567 (só colagens).
- Lotes 27/10 A, B, C e D entregues na Conferir (gasto US$ 4,98 + 5,58 + 6,26 + 6,72).
- Lote 27/10 D (28/10 02h45): 15 produtos (2710D-01..15) + os 2 resgates (2710A-12 panelas, 2710C-01 espreguiçadeiras) com A, B e C,
  pendentes para a dona. Nenhum resgate nem pedido de edição pendente. Detalhes: memoria/historico_lotes.md.
- Resgate: imagens aceitas pela dona vêm do histórico da WaveSpeed (grátis) + câmera por código (zoompan), nunca clipe IA (regra K19).
- Fila: próximos aprovados a partir de 54514950462 (Banqueta Tulipa) e 58263622580 (Cortina Blackout). Pular os já pulados (ver histórico).
- Tinder: 187 produtos novos da lista da dona (busca 27/10) em "Escolher". Fila = aprovados.
- Pedidos da dona já valendo: músicas animadas; assinatura "Aguiiar Lar" mudando de lugar.
- Foto colada (produto complexo): só se a dona pedir. Não testada.

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
