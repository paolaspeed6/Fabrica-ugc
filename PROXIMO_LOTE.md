# Próximo lote: o essencial (leia só isto ao começar uma conversa nova)

Atualizado: 2026-10-31 (Lista 30/10 B entregue). Histórico completo: memoria/historico_lotes.md. Regras: CLAUDE.md. Lições: memoria/licoes_da_fabrica.md.

## Como começar
- Conversa nova, no mesmo projeto. Ela não lembra de conversas antigas: só o que está nos arquivos.
- Lote novo: a dona manda "Lote do dia: 15 produtos da Fila, teto US$ 8". Crie a conversa com model claude-opus-5-5.
- Agentes de conferência (Fichador, fiscais): model sonnet.
- Pasta do lote: video-teste/lote/lista<DDMM><letra> (cópia de video-teste/lote/modelo). Passos: CHECKLIST.md.

## Regras que não podem falhar
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

## Estado atual (31/10, madrugada)
- Lote 30/10 B (31/10 ~02h30 UTC): 15 produtos com A, B e C (45 vídeos, 3010B-01..15) na aba Conferir, pendentes. Gasto US$ 5,44 de 8
  (54 imagens + 33 clipes). Nenhum pulado (reservas não usadas). Tinder: os 15 em `pronto`.
- 1º lote real do sem_cena.py (K22): funcionou. 3010B-13 Lustre Corsalle (clipe A acendeu as lâmpadas; B era outro modelo e ficou fora:
  vídeos com A e C) e 3010B-15 Kit 2 Estantes (A, B e C só por borda) foram montados com câmera por código e foram com o aviso
  "cenas reprovadas pela fiscal: confira". A dona decide/descarta à mão.
- Avisos para a dona: p04 Batedeira só tinha 1 foto (ambiente); p06 Hotend "ORIGINAL Creality" (foto 01 com logo, peça sem nome);
  p02 Painel TV e p13 Lustre com 1 cena só aprovada (vídeo repete a cena).
- Drive: a 1ª subida caiu (Connection reset) e o entregar.sh saiu sem conferir_docs; rodei drive_backup.py + entregar.sh de novo à mão.
- Fila: aprovados livres agora são só as reservas 58217392854, 58215204667, 58203555197, 53018045160, 49217644309 (+ os 12 já pulados
  e os outros aprovados do Tinder). Nenhum lote aberto.

## Estado anterior (30/10, noite)
- Resgates processados (30/10, US$ 0): 2810A-13 Colchão, 2810B-06 Cabeceira + Recamier, 2910A-09 Aparador Tekna, 2910A-10 Kit Poltronas
  Opala, 3010A-10 Bicicleta Tríade: 15 vídeos (A, B e C) na aba Conferir, pendentes, nos mesmos cartões (resgate_processado: true).
  Imagens do histórico da WaveSpeed (casadas pelo poster), textos refeitos do anúncio (pastas antigas não estavam no disco), câmera
  por código (camera_codigo.py). B do colchão, cabeceira e poltronas vai com aviso (zoom suave; o auditor achou quase parada).
  Tinder: os 5 em `pronto`. Ainda em `produzindo` no Tinder (de lotes antigos, não mexi): 52916448186, 54418096324, 54661666510, 56166664405.
- Nenhum resgate pendente. Nenhum lote aberto.

## Estado anterior (30/10, manhã)
- Lote 30/10 A (30/10 09h50 UTC): 10 produtos com A, B e C (30 vídeos, 3010A-01..09, 11) + 3010A-10 Bicicleta Infantil Aro 20 Triade
  como resgate (larga demais), na aba Conferir. Gasto US$ 4,06 de 6 (47 imagens + 22 clipes). Tinder: 10 em `pronto`; 58214424772 (resgate) segue `produzindo`.
- 3010A-07 Cama Carro: aviso de adesivo parecido com Hot Wheels (a dona decide). p02 e p04 com 1 cena só.
- Fila: nenhum aprovado livre (só os 12 já pulados). Próximo lote precisa de mais "aprovados" no Tinder.
- Chave Shopee no ambiente se chama `shopee_APP_SECRET` (minúsculo): `SHOPEE_APP_SECRET="$shopee_APP_SECRET" python3 -I gerar_links.py <AAMMDD>`.
- Copie a pasta modelo DEPOIS do git pull (no 30/10 a cópia saiu antes e faltavam K20/K21; corrigido a tempo).

## Estado anterior (29/10)
- Lote 29/10 A (29/10 22h05 UTC): 13 produtos com A, B e C (39 vídeos, 2910A-01..08, 11..15) + 2910A-09 Aparador Cerca Viva Tekna
  e 2910A-10 Kit 2 Poltronas Opala + Puff como resgate (largos demais), na aba Conferir. Gasto US$ 6,11 de 8 (66 imagens + 35 clipes).
  Tinder: 13 em `pronto`; 55107980511 e 58204213844 (resgates) seguem `produzindo`.
- Pulado pelo Orquestrador: Suporte lava-roupa 58203226664 (nenhuma foto vazia, sempre com máquina em cima; volta a `aprovado`).
- Fila: aprovados livres só Exaustor Ventisol 60 cm 23398536883 e Kit 4 Cadeiras Amis Rattan 48318696775 (+ os 12 já pulados).
  Próximo lote precisa de mais "aprovados" no Tinder.
- Regra nova K20: rodar textos.py antes da fase2 (o produzir.sh agora para sozinho antes dos clipes se faltar).

## Estado anterior (28/10)
- Lote 28/10 B (28/10 22h35 UTC): 12 produtos com A, B e C (36 vídeos, 2810B-01..05, 07..13) + 2810B-06 Cabeceira Itália + Recamier
  como resgate, na aba Conferir. Gasto US$ 4,56 de 8 (52 imagens + 25 clipes). Só 13 aprovados livres na Fila (nenhum pulado).
- FILA VAZIA: todos os aprovados restantes são os 11 já pulados pelo Fichador. Próximo lote precisa de novos "aprovados" no Tinder
  (187 em "Escolher").
- Lote 28/10 A (28/10 20h40 UTC): 14 produtos com A, B e C (42 vídeos, 2810A-02..20) + 2810A-13 Colchão Ortho Flex como resgate,
  na aba Conferir. Gasto US$ 6,18 de 8 (60 imagens + 38 clipes). Pulados pelo Fichador (Tinder segue `aprovado`): Kit Cooktop+Balcão
  58254841155 (colagem), Viveiro 58265685456 (sem foto limpa), Radiador Kombi 58211200606 (colagem), Banco Kulmai 58209960104
  (modelos misturados), Chave de impacto 1200 N.m 58263626567 (só colagens).
- Lotes 27/10 A, B, C e D entregues na Conferir (gasto US$ 4,98 + 5,58 + 6,26 + 6,72).
- Lote 27/10 D (28/10 02h45): 15 produtos (2710D-01..15) + os 2 resgates (2710A-12 panelas, 2710C-01 espreguiçadeiras) com A, B e C,
  pendentes para a dona. Nenhum resgate nem pedido de edição pendente. Detalhes: memoria/historico_lotes.md.
- Resgate: imagens aceitas pela dona vêm do histórico da WaveSpeed (grátis) + câmera por código (zoompan), nunca clipe IA (regra K19).
- Fila: sem aprovados novos (só os 11 pulados). A dona precisa aprovar mais no Tinder antes do próximo lote.
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
