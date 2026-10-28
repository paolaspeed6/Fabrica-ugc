# Onde paramos (leia isto no começo de uma conversa nova; atualize no fim de cada lote)

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
## Último lote: Lista 27/10 C — ENTREGUE (27/10, 21h50 UTC)
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
