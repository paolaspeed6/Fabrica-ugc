# Modelo de criação Aguiiar Lar (padrão aprovado em 2026-10-18)

Este é o modelo que a dona aprovou depois de várias rodadas. Qualquer sessão (nova, ou de outra pessoa) deve seguir
EXATAMENTE este layout, estas regras e este processo. Não invente outro visual sem pedido dela.

## 1. O que sai para cada produto
3 vídeos de 15 s, 9:16, 1080x1920, um em cada modelo de layout (PDF com imagens: `referencias/modelos-layout/Modelos_de_layout_Fabrica_UGC.pdf`):

| Opção | Nome | Visual | Onde está o molde |
|---|---|---|---|
| A | **Um dia com ela** (modelo padrão) | Serifa Caladea branca à esquerda, destaque em *itálico*; rótulo pequeno em caixa alta espaçada; 3 momentos com horário grande que rola (08:00 → 15:00 → 22:00) ou palavra curta (Café · Almoço · Jantar; Desenho · Leitura · Soneca); mergulho rápido ao preto em cada virada; a luz esquenta do dia para a noite; CTA "Disponível no link / Leve pra casa." com linha fina | `opcao_a` em `video-teste/luxo/specs/novos.py` |
| B | **Faixas moderno** (modelo Kevin "faixas" modernizado) | Embaixo: rótulo Poppins SemiBold espaçado + 2 faixas inclinadas 2° (1ª quase preta com letra branca, 2ª na cor do produto com letra escura, Poppins Bold) + subtítulo Poppins Regular; vídeo sobe 300 px para o produto ficar acima das faixas; CTA final = contorno fino branco com carrinho desenhado em traço + "Toque no carrinho" (sem pílula colorida, sem emoji) | `opcao_b_faixas` |
| C | **Direto ao ponto** (persuasivo, para o público leigo) | Barrinhas de progresso no topo (como Stories); DM Serif Display branca centralizada com *itálico*; gancho em frase simples → "Olha o que *ela tem:*" + 3 itens com ✓ desenhado num círculo na cor do produto → onde usar → "Toque no carrinho *e veja o preço.*" + botão "Ver o preço" | `opcao_d` (sem `fonte`) |

Em TODOS: assinatura **"Aguiiar Lar"** em Playfair itálico pequeno e translúcido que passeia devagar pelo meio do quadro
(não dá para cortar nem borrar um ponto fixo). Color grade suave com grão fino. Cortes secos (nunca fusão/dupla exposição).

## 2. Regras que nunca mudam (detalhe em `agentes/regras_de_erros.md`)
1. **Produto inteiro e sem mão/pessoa no 1º quadro** (é a capa/thumb). Close só depois.
2. **Cada uma das 3 opções abre com um take diferente** (rodízio).
3. **Texto nunca cobre o produto.** Produto alto e central (cabideiro, luminária, banqueta): `shiftx` empurra o vídeo para a direita (a sobra vira parede desfocada) e o texto vai à esquerda (`esq=True`, `escala`, `item_size`); dá para ajustar por cena (`{'shiftx': N}` na tomada).
4. **Só qualidades reais** que o comprador percebe e o anúncio comprova. Característica neutra NÃO é qualidade ("linhas retas", "formato quadrado", "cor bege", "tem 4 pés"). Na dúvida, simplifique ou fale de onde usar. Nada de nota/avaliação exata, % de desconto, promessa de entrega, bebida alcoólica.
5. **Cenas de IA (Veo/Gemini) muitas vezes têm MÃO inventada.** Conferir CADA cena a cada 0,1 s (tira de quadros) e usar só trechos limpos; tomadas com `{'d': x}` fixam a duração para não entrar na janela da mão.
6. **Prévia parada antes de renderizar** (`PREVIEW=0,6,13`): olhar capa, meio e CTA de cada opção.
7. **Auditoria obrigatória** (`video-teste/auditar_video.py`): movimento por cena, gancho visível no 1º quadro, sem fusão, som, 15 s, 1080x1920.
8. **Nada pago sem o OK dela** (diga o custo máximo antes).

## 3. Som
- **Atual (2026-10-18): SEM voz, só música calma** (`video-teste/luxo/trilha_piano.wav`, ou outra via `MUSICA=arquivo.wav`). A dona achou a voz Kokoro com sotaque estrangeiro; a do Gemini (Kore) era boa mas tem limite de 10 por dia por modelo.
- Para voltar a ter voz: `COM_VOZ=1` (gera frase por frase e alinha cortes e textos com a fala; `tts_kokoro.py` ou `tts_lux.py` do Gemini).

## 4. Processo (passo a passo)
1. Organizar as cenas do produto em `trabalhos/pNN-nome/src/A.mp4, B.mp4, C.mp4` (qualquer resolução vertical).
2. Olhar cada cena (tira de quadros) e anotar: onde o produto está inteiro, onde tem mão, onde é close.
3. Escrever o roteiro no `video-teste/luxo/specs/lote_*.py` (copiar um produto de `lote_1018.py`): textos das 3 opções, cor de destaque (tom do produto), tomadas por momento (com rodízio da abertura).
4. Gerar as timelines: `cd video-teste/luxo/specs && LUXO_DIR=/caminho/trabalhos/pNN-nome python3 lote_XXXX.py pNN`
5. Prévias paradas: `LUXO_DIR=... PREVIEW=0,6,13 python3 -I ../build_lux.py $LUXO_DIR/specs/pNN_a_umdia.json` (idem b_faixas, c_direto) e conferir.
6. Renderizar e auditar: `video-teste/luxo/render_lote.sh /caminho/trabalhos/pNN-nome ...` (3 em paralelo, ~6–8 min por produto).
7. Entregar numa página com botão de baixar (`video-teste/luxo/pagina_lote.py lote.json pasta`), legenda Shopee < 150 caracteres com 4 hashtags do nicho.
8. Erro novo → regra nova em `agentes/regras_de_erros.md` e `agentes/licoes.md`.

## 5. Instalação numa máquina nova
```
pip install --break-system-packages numpy pillow
# ffmpeg precisa estar instalado
# (só se for usar voz) pip install --break-system-packages kokoro-onnx soundfile  + modelos em /home/user/modelos-voz
```
Fontes ficam em `video-teste/fontes/` (Caladea, Liberation Sans, Poppins, DM Sans, DM Serif Display, Playfair Display, Montserrat, Bebas Neue).

## 6. Arquivos-chave
- `video-teste/luxo/build_lux.py` — montador (cor, textos, faixas, cartão, lista, barrinhas, relógio, assinatura, prévias).
- `video-teste/luxo/specs/novos.py` — os 3 moldes de layout (`opcao_a`, `opcao_b_faixas`, `opcao_d`).
- `video-teste/luxo/specs/produto.py` — processo de um produto (3 vídeos a partir de um cfg; com ou sem voz).
- `video-teste/luxo/specs/lote_1018.py` — 9 produtos reais de exemplo (roteiros, tomadas, janelas de mão anotadas).
- `memoria/colecao-luxo.md` — histórico das decisões da dona (o que foi aprovado, reprovado e por quê).
- `trabalhos/p01-cabideiro/out2/` — exemplo real final das 3 opções.
