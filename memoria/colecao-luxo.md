---
name: colecao-luxo
description: conceito "Coleção Luxo" (Zara Home + Galeria + Um dia com ela) aprovado pela dona em 2026-10-18 — receita de tipografia, cor, som, câmera e ganchos
metadata:
  type: feedback
  modified: 2026-10-18
---

A dona pediu (2026-10-18): "conceito zara home, regras de design que já aprendemos, fonte do layout 3 mas sem moldura e sem a parte de carrinho, sofisticado, elaborado, 3 opções de vídeo com layout e ganchos diferentes, todos luxuosos e elegantes, um no estilo Zara Home, os outros com criatividade". Feito na sessão "Poltrona laranja" para a cadeira trançada e a poltrona capitonê bege; ela aprovou e mandou absorver o conceito. Vídeos e página: `trabalhos/cadeira-poltrona-bege/` (`*_lux1_zarahome`, `*_lux2_galeria`, `*_lux3_umdia`).

**PADRÃO NOVO (a dona, 2026-10-18): 3 opções de vídeo para CADA produto.**
- Opção A = "Um dia com ela" (conceito 3 abaixo): "ficou perfeita, salve como modelo padrão dos próximos". Sempre presente.
- Opção B = shopee3 do Kevin (cartão escuro embaixo, gancho com palavra de destaque, CTA cheio) com toque modernizado. Substitui o Zara Home ("ficou boa, porém quero outra versão, também moderna").
- Opção C = "Direto ao ponto" (a dona, 2026-10-18: "um dos modelos, quero que seja bem persuasivo, capa de revista não me pegou muito, quero algo que o público leigo também entenda"). Barrinhas tipo Stories no topo, gancho em frase simples (DM Serif Display centralizada), "Olha o que *ela tem:*" + 3 itens com ✓ desenhado (DM Sans) aparecendo junto com a voz, onde usar, "Toque no carrinho *e veja o preço.*" + botão "Ver o preço". Voz calorosa de amiga recomendando. `opcao_d` em specs/novos.py. A Galeria e a Revista foram DESCARTADAS (a Revista fica em trabalhos/ só como histórico).

**Como as opções B e C foram feitas (2026-10-18, `video-teste/luxo/specs/novos.py`, exemplo em `cadeira_poltrona.py`):**
- B (shopee3 moderno): cartão de vidro fosco (o vídeo desfocado por trás, tinta escura 62%, borda branca fina, raio 44) fixo embaixo em y=1400, h=420; vídeo sobe 260 px (`lift`) para o produto ficar acima do cartão. Rótulo Poppins SemiBold em CAIXA ALTA na cor de destaque + contador "01 / 03"; título Poppins Bold 80 px com palavra entre [ ] na cor de destaque (tom do produto: areia/caramelo); subtítulo Poppins Regular; CTA = pílula cheia na cor de destaque com seta desenhada (sem emoji) que sobe na última cena. Cor limpa (sat 0,92, grão 0,01). Voz confiante e moderna.
- (descartada) Revista: "CASA" em Playfair espaçada no topo + linha fina + "EDIÇÃO Nº 07 · A PEÇA DO MÊS" em DM Sans; gancho em Playfair centralizado; detalhes como "01 / 02 / 03" em Playfair itálico grande + nota curta; CTA "Disponível no link / Leve essa peça *pra casa.*". Tudo no topo, centralizado (produto livre embaixo); fechar voltando ao plano da abertura. Cor matte quente com grão.
- Narração: gemini-2.5-flash-preview-tts só dá 10 por dia grátis; usar `MODELO=gemini-3.1-flash-tts-preview PREFIXO=1` (lê só o texto, testado por transcrição).
- Sempre gerar prévias paradas (`PREVIEW=0,6,13`) e conferir texto cortado e texto sobre o produto antes de renderizar.

**Ajustes da dona (2026-10-18, depois da 1ª entrega das 3 opções):**
- Textos e escritas: "perfeitos". Layouts 2 e 3 ainda vão mudar; mostrar JPEG de exemplo antes de editar o vídeo.
- Opção 2: o cartão com selo já é um dos modelos do Kevin; ela quer a OUTRA opção do modelo Kevin (letras grandes no topo ou faixas), modernizada.
- Voz: estava agressiva; quer calma, sedutora, suave.
- CTA de carrinho no fim estava "brega" (pílula cheia colorida com seta): fazer algo moderno e discreto.
- "Linhas retas" não é qualidade: ver regra 11 em agentes/regras_de_erros.md. Rodízio do take inicial: regra 12.

**Tipografia:** serifa Caladea Regular (título ~118 px, corpo ~88 px); destaque em *itálico* (Caladea Italic), NÃO em cor. Rótulo "eyebrow" em sans (Liberation Sans) CAIXA ALTA 34 px, espaçamento ~11 px. Texto branco com sombra suave (blur 14, alpha 120). Alinhado à esquerda em x=84, faixa do topo y≈200–620, nunca sobre o produto. Sem moldura, sem pílula, sem ícone de carrinho, sem emoji.

**Animação:** linha fina de 3 px que se desenha (0,9 s); textos entram com fade + subida de 26 px (0,55 s) ou wipe da esquerda com borda suave (CTA). Gancho JÁ visível no 1º quadro (sem animação em t=0).

**CTA elegante:** eyebrow "DISPONÍVEL NO LINK" + "Leve pra casa." ou "Leve essa peça *pra casa.*" + linha fina. Narração: "Toque no link e leve pra casa."

**Cor (por quadro):** saturação 0,72–0,86, lift 0,02–0,04, contraste 0,94–1,08, leve aquecido, vinheta, topo escurecido para leitura, grão fino (σ≈0,022, 2x2 px).

**Som:** voz Kore (gemini-2.5-flash-preview-tts) com estilo "voz calma, elegante e sofisticada, ritmo pausado, comercial de decoração de luxo"; pausas encurtadas para no máx. 0,5 s para caber em 15 s; trilha = piano do áudio das próprias cenas Veo em crossfade de 1,5 s, volume 0,3; loudnorm −14 LUFS. Rodar TTS em série (em paralelo deu 429).

**Câmera e corte:** zoom lento contínuo 1,0→1,06–1,10 com easing; cortes secos no ritmo da narração (sem dupla exposição); closes por recorte de 1,5–2,0x.

**Os 3 conceitos (gancho diferente em cada):**
1. Zara Home — "NOVA COLEÇÃO — CASA" / "O trançado *que faltava.*" · "A poltrona *que acolhe.*"; "DETALHE 01/02/03" numerados como catálogo.
2. Galeria — produto como obra: vinheta forte (spot), "PEÇA Nº 01" / "Não é só uma *cadeira.*" · "Elegância não faz *barulho.*"; detalhe criativo = etiqueta de museu (cartão off-white: "Peça nº 02 / Poltrona capitonê / estudo em tom areia / Sala · Quarto · Leitura").
3. Um dia com ela — "DAS 8H ÀS 22H" / "Um dia inteiro *com ela.*" · "Do café ao *último capítulo.*"; relógio serifado de 200 px que rola 08:00→15:00→22:00, mergulho rápido ao preto (0,17 s) nas viradas, cor que esquenta e escurece do dia para a noite.

**Auditoria (2026-10-18):** os 6 passam em movimento (3,3–13), gancho na capa (0,87–1,0), som e 15 s. O auditor foi corrigido: medir letras (não diferença de quadro) e aceitar mergulho ao preto.

**Atenção:** os textos usam só o que se vê (trançado, capitonê, visual aveludado, pés escuros) porque a Shopee bloqueou a leitura dos anúncios; material e tecido não confirmados — confirmar com a dona antes de postar.
