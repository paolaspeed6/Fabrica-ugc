# Onde paramos (leia isto no começo de uma conversa nova; atualize no fim de cada lote)

## PARA A CONVERSA NOVA: o que está pendente (28/10)
Esta conversa nova NÃO lembra das conversas antigas. Tudo que importa está aqui e nas regras (CLAUDE.md, memoria/).
1. Redes sociais (Reels automático): Facebook e Instagram OK (postar.py conferir). Threads: testar com a chave nova (THREADS_TOKEN);
   se "Failed to decrypt", gerar de novo (Casos de uso > API do Threads > Gerador de token). Ainda não há Reels prontos nem agendamento.
   Só postar com OK da dona (qual produto, layout A ou C, legenda). Postagem automática: até 2 por dia por rede, 3 h entre posts.
2. Lote 27/10 D: pode estar em andamento na conversa "Lote 27/10 D". Conferir a aba Conferir antes de abrir outro.
3. Modelo: lote = Opus; agentes de conferência = Sonnet (CLAUDE.md, "Modelo de cada conversa").
4. Conferência e Postagens: mesmo endereço. Ok da dona libera sozinho. Edição pedida vira status editar.
5. Músicas animadas (biblioteca) e assinatura "Aguiiar Lar" mudando de lugar já valem.
6. Foto colada (produto complexo): só se a dona pedir. Não testada.
7. Pendências da dona: confirmar Tinder da importação de 27/10 (187 cartões) e a Fila (aprovados).


## Lista 30/10 A (2026-10-30)
- 10 produtos com A, B e C (30 vídeos, 3010A-01..09, 11) + 3010A-10 Bicicleta Infantil Aro 20 Triade 58214424772 como resgate (larga demais), aba Conferir. Gasto US$ 4,06 de 6 (47 imagens + 22 clipes).
- Com 1 cena só (os 3 layouts abrem no mesmo take): p02 Kit 4 Cadeiras Amis, p04 Espreguiçadeira Inflável. p04 B entregue com aviso (cena quase parada).
- 3010A-07 Cama Carro Stock Car: aviso no cartão, adesivo com chama/logo parecidos com Hot Wheels (a dona decide).
- Fotos: p05 Arara só tinha colagens → recorte limpo da foto 04 (p05-fotos/04c.jpg); p04 e p05 sem foto com pessoa/colagem nas referências.
- Chave Shopee está no ambiente como `shopee_APP_SECRET` (minúsculo): rodar `SHOPEE_APP_SECRET="$shopee_APP_SECRET" python3 -I gerar_links.py`.
- Fila: nenhum aprovado livre (só os 12 pulados). Próximo lote precisa de novos "aprovados" no Tinder.
## Lista 29/10 A (2026-10-29)
- 13 produtos com A, B e C (39 vídeos) + 2 resgates (2910A-09 Aparador Cerca Viva Tekna 55107980511, 2910A-10 Kit 2 Poltronas Opala + Puff 58204213844), aba Conferir. Gasto US$ 6,11 de 8.
- Pulado: Suporte lava-roupa 58203226664 (sem foto vazia). Entrou a reserva Tekna.
- Fila: só 23398536883 e 48318696775 livres.
## Modelos (28/10)
Lote novo: create_session com model claude-opus-5-5. Agentes de conferência: sonnet. Ver CLAUDE.md.

## Como a dona começa um lote (conversa nova, 15 produtos no máximo)
Mensagem: "Lote do dia: 15 produtos da Fila, teto US$ 8." O Claude: lê só este arquivo + CHECKLIST + RESUMO_REGRAS,
cria a pasta, fotos, 1 Fichador Sonnet, links/textos, `produzir.sh fase1` (segundo plano), 1 Fiscal Sonnet nas folhas,
`produzir.sh fase2` (segundo plano), Conferência + Tinder + commit. Cerca de 10 a 15 respostas do Claude por lote.

Atualizado: 2026-10-27 (21h50 UTC).

- Regra da dona (27/10 19h, confirmada): vídeos ficam na aba Conferir esperando o Ok dela; só o Ok leva para "Para postar". Nada de para_postar.py.
- 2710B-03 Mesa em L: resgate PROCESSADO (27/10 21h): as 3 imagens aceitas foram recuperadas do histórico da WaveSpeed
  (POST https://api.wavespeed.ai/api/v3/predictions {"page":1,"page_size":100} lista as gerações com o link do resultado; grátis),
  animadas com câmera fixa (FIXA=1, US$ 0,30) e voltaram à aba Conferir como pendente com A, B e C. Tinder: pronto.
## Último lote: Lista 28/10 B — ENTREGUE (28/10, 22h35 UTC)
- 12 produtos com A, B e C (36 vídeos) na aba Conferir da Postagens (2810B-01..05, 07..13) + 2810B-06 Cabeceira Itália + Recamier Baú
  como "resgate" (as 3 cenas reprovadas nas 2 rodadas: conjunto largo). Drive "Fabrica Videos/2026-10-28". Tinder: 12 em `pronto`;
  cabeceira+recamier (58209326162) segue `produzindo`. Gasto US$ 4,56 de 8 (52 imagens + 25 clipes).
- Só havia 13 aprovados livres na Fila; nenhum pulado pelo Fichador. A Fila ficou só com os 11 já pulados.
- Fiscal Sonnet pegou p07C (7 botões em vez de 10), p08C (cabos pendurados inventados), p09C (manchas de luz no chão), p11A (painel com luz/TV).
## Lote anterior: Lista 28/10 A — ENTREGUE (28/10, 20h40 UTC)
- 14 produtos com A, B e C (42 vídeos) na aba Conferir da Postagens (2810A-02,03,05..10,14,16..20) + 2810A-13 Colchão casal Ortho Flex
  como "resgate" (as 3 cenas reprovadas nas 2 rodadas). Drive "Fabrica Videos/2026-10-28". Tinder: 14 em `pronto`; colchão segue `produzindo`.
  Gasto US$ 6,18 de 8 (60 imagens + 38 clipes, nenhuma refação de clipe).
- Pulados pelo Fichador: Kit Cooktop+Balcão, Viveiro, Radiador Kombi, Banco Kulmai, Chave de impacto 1200 N.m (sem foto limpa/colagem).
  Entraram as reservas Mesa Moema, Purificador ALKA, Caixa de areia, Barraca pop-up e Monitor Concórdia (p16-p20).
- Segredo do ambiente ainda com nome minúsculo `shopee_APP_SECRET`: rodei gerar_links com SHOPEE_APP_SECRET="$shopee_APP_SECRET".
  Pedir à dona para renomear para SHOPEE_APP_SECRET.
## Lista 27/10 C — ENTREGUE (27/10, 21h50 UTC)
- 14 produtos com A, B e C (42 vídeos) na aba Conferir (2710C-02..13, 15, 16) + 2710C-01 Kit 2 Espreguiçadeiras como "resgate"
  (91-96% da largura nas 2 rodadas). Drive "Fabrica Videos/2026-10-27". Tinder: 14 em `pronto`; p01 segue `produzindo`.
  Gasto US$ 5,96 (52 imagens + 39 clipes) + US$ 0,30 do resgate da Mesa = US$ 6,26 de 8.
- Pulado pelo Orquestrador: Aparador Industrial 160 cm 58268219197 (nenhuma foto limpa; garrafas e taças nas fotos 01/02; status
  segue `aprovado`). Entrou Poltrona Bouclé Opally 58265861538 (p16).
- Fiscal Sonnet pegou p06C (LED inventado) e p07C (vaso parecendo garrafa); cena liberada e depois reprovada fica "falhou" (sem 3ª imagem).
- A dica "whole X under 40% of frame width" NÃO segurou o kit comprido de espreguiçadeiras (Nano Banana enche o quadro).
  Produto comprido deitado ainda é risco: próximo passo a testar = cena vista de ponta/diagonal ou outpaint.
- Consertos: gerar.py FIXA=1 era ignorado (2 "def clipe"); produzir.sh não via clipe `_fixa` (sem Fiscal de vídeo).
- Atenção: p07 e p09 são o mesmo filamento Soleyin Ultra PLA branco de 2 lojas (vídeos parecidos); títulos dizem 12 kg mas é 1 carretel (textos sem peso).
- Fila: próximos aprovados a partir de 58218778773 (Cadeira de Balanço Bebê) e 56166165783.
## Lote anterior: Lista 27/10 B — ENTREGUE (27/10, 13h UTC)
- 14 produtos com A, B e C (42 vídeos) na aba Conferir da Postagens (2710B-01,02,04,05,07..13,15,16,17) + 2710B-03 (Mesa em L Lisboa)
  como "resgate" (as 3 cenas largas demais, 90-100% da largura, mesmo na refação). Drive "Fabrica Videos/2026-10-27".
  Tinder: 14 em `pronto`; Mesa em L segue `produzindo` (resgate). Gasto US$ 5,58 (teto 8): 60 imagens + 32 clipes.
- Pulados pelo Fichador (status voltou a `aprovado`): Furadeira Bosch GSB 16 RE 23294968042 (sem foto limpa, suspeita de réplica)
  e Cama Infantil Carro 58260559338 (8 variações de personagens licenciados, foto 01 só colchão). Entraram Furadeira ZOWSBB
  47968128312 (p16) e Monitor Gamer 27" 58211778615 (p17).
- Fiscal Sonnet pegou na p16 letras espelhadas (A) e caixote na bancada (B); o resto passou.
- Ainda largos: mesa em L, forno (A), banquetas (A, C), poltrona amamentação (A, C). Próximo Fichador: produto largo/L/kit
  "whole X under 40% of frame width", piso vazio em volta.
- Fila: próximos aprovados a partir de 58212612080 (decidido 25/10 02:50) e 58255199042.

## Lote mais antigo: Lista 27/10 A — ENTREGUE (27/10, 11h20 UTC)
- 12 produtos com A, B e C (36 vídeos) na aba Conferir da Postagens (2710A-01..11, 14) + 2710A-12 (Caçarolas) como "resgate".
  Drive "Fabrica Videos/2026-10-27". Tinder: 12 em `pronto`; p12 segue `produzindo` (resgate). Gasto US$ 4,98 (teto 8).
- Pulados pelo Fichador (sem gasto, status no Tinder intocado = `aprovado`): Poltrona Orgânica Redonda (foto 01 de outro modelo)
  e Kit Halteres 30 kg (foto 01 colagem). Bicicleta ergométrica silenciosa 58268085829 saiu da Shopee (404).
- Consertos: produzir.sh instala rembg (sem ele a borda não era medida); aplicar_fiscal apaga o veredito velho da cena refeita.
- Fiscal Sonnet x Opus (p05, p09, p11): fora de borda, a Sonnet achou o mesmo que a Opus (e mais: abajur aceso, armário espelhado).
  As 2 que só a Opus pegou (p05B, p09B) eram borda larga, que o folha.py reprova sozinho quando o rembg está instalado.
  Decisão: manter a Fiscal Sonnet, mas só depois do folha.py (conferir que pNN-cenas/folha.jpg existe).
- Atenção: produto pequeno (panelas) e kits largos ainda saem largos demais mesmo na refação; Fichador deve pedir câmera mais longe.
- Nota: a legenda B do balcão (05) diz "Pia e cooktop" (vem do título "p/Pia/Cooktop"); se a dona achar que confunde, trocar.

## Lote mais antigo: Lista 25/10 A — ENTREGUE (26/10, 23h)
- 41 produtos na Conferência (106 vídeos: 41 A, 24 B, 41 C; 17 B reprovados no auditor por cena quase parada) e no Drive
  "Fabrica Videos/2026-10-26". Tinder: os 41 em `pronto`. Gasto US$ 18,69. Jogo: retomar (metas, mural, gasto) e perguntar à dona.
- No Drive ficaram cópias antigas cortadas (disco cheio) de 2510A_01 A/B, 25 A/B/C, 41 C, 43 A/B/C: a Conferência aponta para as boas.
- Antes do próximo lote: corrigir o layout B no lote_auto (tomadas de 5 s com clipe de 4 s = cena quase parada).

## Conferência do 25/10 A (a dona, 26/10 20h25) — FALTA PROCESSAR na conversa de produção (com as chaves e os clipes)
- OK (19): 01 02 03 04 06 07 13 17 18 19 20 23 29 32 41 42 43 44 45 → Postagens (agentes/postagens_formato.md).
- Editar, "letras muito grandes, saíram da tela" (21): 08 09 10 11 12 14 15 16 21 22 24 25 27 28 30 31 33 35 36 38 40.
  O build_lux.py já encolhe sozinho todo texto mais largo que a tela (margem 56 px, commit de 26/10). Basta renderizar de novo
  esses produtos (lote_auto + render, grátis) e trocar no Drive e na Conferência. Vídeo de resto aprovado: não mexer em cena.
- 26: "surgiu uma imagem do nada, quero vídeo fluido" → achar o corte/tomada com salto e refazer a montagem (grátis).
- A conversa do comentário (só app, sem chaves nem pasta do lote) não conseguiu processar; as decisões seguem salvas na página.

## Lista 25/10 A — situação em 27/10
- Postagens (Para postar): 19 produtos aprovados, cada um com A, B e C (57 vídeos).
- Conferência (https://claude.ai/artifact/7HYeGG32XBtjXTcMMoffJt → "Conferência →"): 22 refeitos (letras + solda) com A/B/C, pendentes;
  2510A-34 (Kit 4 Cadeiras) como "resgate". Ao abrir a próxima conversa: ler `conferir` com status editar/resgatar e processar.

## Foto colada (produto complexo, K14) — só quando a dona pedir (27/10)
`video-teste/foto_colada/colar_auto.sh <foto01> <video> <a|b|c>` cola o cartão num canto (A/C embaixo à direita, B em cima).
AINDA NÃO TESTADO: testar em 1 produto e mostrar a ela antes de usar no lote.

## Redes sociais (28/10)
- A dona escolheu: Reels = layout A e C alternando (B só Shopee). Ligar postagem só depois de `meta/postar.py conferir` passar.
- 28/10: Meta respondeu "API access blocked" (app bloqueado/restrito) e Threads "Failed to decrypt" (token colado errado). Dona vai corrigir.

## Pendências da dona
- Segredos: renomear `shopee_APP_SECRET` para `SHOPEE_APP_SECRET`; token da Página em META_PAGE_TOKEN; THREADS_TOKEN novo;
  criar MARCA_NOME e DRIVE_PASTA.
- Tarefas agendadas do kit (varredura, contador, Reels) ainda não criadas.

## Próximo lote (fluxo econômico)
Seguir `video-teste/lote/modelo/CHECKLIST.md` e a seção "Economia de uso" do CLAUDE.md: Fichador Sonnet (1-2 agentes),
gerar.py → folha.py → fiscal_gemini.py → Fiscal Sonnet (1 agente, folhas) → clipes → fiscal_video_gemini.py → lote_auto.py →
render solto → entregar.sh → Conferência. Lote de 15 produtos de cada vez.

## Regra da dona (26/10): economia só se não prejudicar a qualidade
No 1º lote com o fluxo econômico, conferir 3 produtos TAMBÉM com uma Fiscal Opus (modelo padrão) e comparar com a Fiscal Sonnet.
Se o Sonnet deixar passar defeito que o Opus pegou, voltar a Fiscal de confirmação para o Opus (1 agente, só as folhas). Anotar o resultado aqui.
- Durante o render, musicas/usadas.json muda a cada vídeo: usar git update-index --assume-unchanged e desfazer no fim.

## Lote: Lista 27/10 D — ENTREGUE (28/10, 02h45 UTC)
- 15 produtos novos com A, B e C (45 vídeos) na aba Conferir (2710D-01..15) + os 2 resgates processados com A, B e C, pendentes
  nos cartões antigos: 2710A-12 (Jogo 3 Panelas) e 2710C-01 (Kit 2 Espreguiçadeiras Fita Náutica). Drive "Fabrica Videos/2026-10-28"
  (dos 2 resgates ficaram no Drive também as cópias velhas com o mesmo nome; a Conferir aponta para as novas).
  Tinder: os 17 em `pronto`. Gasto US$ 6,72 de 8 (61 imagens + 37 clipes + 6 clipes fixos jogados fora).
- Resgates: imagens recuperadas do histórico da WaveSpeed (grátis, comparando com o poster do cartão). O clipe de câmera fixa da IA
  inventou cachorro, vapor e marca d'água (o Gemini deixou passar a marca) → regra K19: resgate = câmera por código (ffmpeg zoompan) sobre a imagem.
- Fichador: só p01 tem foto limpa na 07 (foto 01 com bebê); p06 estante tem taças em todas as fotos (cenas saíram limpas);
  p14 foto 01 é arte de propaganda (cena A saiu limpa). Fiscal Sonnet pegou abajur aceso (p01C, p15C).
- Com 1 cena só: p11 espreguiçadeiras marrom e p14 kit camping (as outras falharam 2x; os 3 layouts usam a cena boa).
  A dica "eixo comprido para o fundo" salvou 1 de 3 cenas no kit de espreguiçadeiras.
- Fila: próximos aprovados a partir de 58254841155 (Kit Cooktop + Balcão) e 58256198377 (Kit Anilhas).
