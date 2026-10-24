# Brief do Fiscal de imagem, Lista 24/10 A (2026-10-23)

Pasta: video-teste/lote/<pasta do lote>/ .
Leia antes: agentes/setor_qualidade/fiscal_imagem.md (inclusive "Calibração com o Kevin") e as seções 9-15 de agentes/regras_de_erros.md.
Para cada produto pNN seu: imagens `pNN-cenas/A.jpg`, `B.jpg`, `C.jpg`; ficha `pNN-ficha.json`; fotos do anúncio `pNN-fotos/` (compare com `fotos_ref` e com as fotos de detalhe).
Monte com PIL lado a lado imagem gerada + fotos de referência; dê zoom (crop ampliado) em letras e detalhes funcionais.

Critério extra do Kevin (2026-10-23): a câmera vai fazer um avanço reto curto e parar em plano médio. Então a imagem precisa de folga em volta do produto (não encostar na borda). Letra pequena ilegível é aceitável se não forma palavra inventada legível; palavra inventada legível ou logo errado = REPROVADO. Pergunta-guia para defeitos pequenos: o Kevin veria isso no iPhone? Se não, APROVADO com nota.
Também reprove: produto encostado/preso em coisa sem nexo (regra 12), kit com unidades em alturas/distâncias incoerentes, miniatura, objeto proibido (pessoa, mão, bebida, comida em cima, item não vendido), contexto de uso errado, variante/cor errada.

Grave `pNN-cenas/fiscal_imagem.json`: {"A": {"veredito": "APROVADO"|"REPROVADO", "provas": "...", "corrigir_prompt": "frase exata a acrescentar no prompt da imagem se reprovar", "risco_animacao": "o que pode bugar ao animar e uma frase para o prompt de vídeo"}, "B": ..., "C": ...}
Não gere nada, não chame API. Responda com 1 linha por produto: pNN A/B/C vereditos e motivo curto das reprovações.

Novidade 2026-10-24: confira a POSIÇÃO de cada peça (braços, base giratória, pés, alças, apoio de pés) contra TODAS as fotos do anúncio da mesma variante (regra 14), e a escala real contra a linha scale da ficha (regra 10; nada de miniatura nem de gigante).
