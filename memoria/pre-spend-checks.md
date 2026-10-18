---
name: pre-spend-checks
description: produzir.py refuses to spend WaveSpeed credit until the owner's 2026-10-15 rules pass (main photo first, no orbit, no alcohol, no AI-drawn packaging, images checked)
metadata:
  type: project
---

After the 2026-10-15 batch wasted credits, the owner asked that the same errors never repeat ("é muito importante essa economia de créditos"). the owner isn't yet sure the videos will convert, so spend must stay minimal while scaling starts.

video-teste/produzir.py runs checar_antes_de_gastar() on every product with scenes still to generate, and stops the whole batch before any paid call if any check fails:
- fotos[0] must be the listing's main photo (01.jpg): color and variant come from it.
- No "orbit", "rotate", "360", "spin" or "turntable" in a prompt.
- No alcohol words in a prompt unless negated.
- "embalagem_com_letras": true forbids AI edits that show the package (use the real photo by code).
- Paid video generation needs the Seedream images first (--so-imagens) AND "imagens_conferidas": true in the product JSON. Claude sets that flag only after comparing color, fabric, lettering and shape of every part with photo 01.

Also: TETO_LOTE_USD caps a batch's spend, and nothing is generated without the owner's request ([[no-generation-without-request]], [[listing-match-rules]]).
