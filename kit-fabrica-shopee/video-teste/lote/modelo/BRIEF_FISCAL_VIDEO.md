# Brief do Fiscal de vídeo, Lista 24/10 A (2026-10-23)

Pasta: video-teste/lote/<pasta do lote>/ .
Leia antes: agentes/setor_qualidade/fiscal_video.md (inteiro, com "Calibração com o Kevin") e as seções 11-15 de agentes/regras_de_erros.md.
Clipes: `pNN-cenas/X.mp4` (Seedance, 5 s, câmera de mão real); imagem de partida `pNN-cenas/X.jpg`; ficha `pNN-ficha.json`; fotos do anúncio `pNN-fotos/`.
Rode `python3 -I video-teste/checar_movimento.py <clipe>` (grátis) e monte as folhas de quadros (fps=4 em zoom e o último quadro em tamanho cheio); trabalhe numa pasta sua no /tmp, não suje a pasta do lote.

Calibração (Kevin aprovou as poltronas que o fiscal anterior barrou): REPROVA o que o Kevin vê no iPhone em velocidade normal: letra/logo inventado legível, peça/furo/grade diferente, produto que gira/desliza de forma visível, objeto que surge, mão/pessoa, lado inventado, contagem/escala/cor errada, morphing ou chão fervendo. Deriva de poucos pixels, giro levíssimo, textura de tecido variando = só anota.
Corte é sempre a primeira opção: dê o trecho limpo do início. Trecho limpo de 2,0 s ou mais serve (a edição desacelera com interpolação). Menos de 2,0 s = REFAZER, com a causa e a frase exata a acrescentar no prompt de vídeo.

Grave `pNN-cenas/fiscal_video.json` (se já existir, acrescente/atualize só as suas cenas): {"X": {"veredito": "usar 0.0-3.5s" | "REFAZER: causa", "fim": 3.5 (0 se refazer), "defeitos": [...], "corrigir_prompt": "...", "nota_estetica": "0-10 e por quê"}}
Registre os defeitos em agentes/aprendizado/defeitos.csv (data,produto,cena,modelo,defeito,causa,correcao) com `>>`.
Não gere nada pago. Responda 1 linha por clipe: pNN X veredito.
