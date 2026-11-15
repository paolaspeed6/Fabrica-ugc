# Fiscal final (Sonnet) — K31, a dona 15/11: "produtos muito diferentes das imagens de referência… estou queimando dinheiro"
Obrigatória em todo lote, DEPOIS do entregar.sh (que gera `folhas_finais/pNNX.jpg`: foto 01 do anúncio + 3 cenas do vídeo final) e ANTES de avisar a dona.
O Gemini grátis deixou passar defeitos graves (exaustor redondo virou quadrado, tapete virou outro, painel ganhou ripado que não existe,
cadeira com pés pretos quando a foto 01 tem pés dourados). Por isso a última palavra é desta fiscal.
Use o Agent tool com `model: "sonnet"`, UM agente para o lote inteiro. Texto para o agente:

---
Você é a FISCAL FINAL da fábrica Aguiiar Lar. Leia só /home/user/fabrica-ugc/agentes/setor_qualidade/RESUMO_REGRAS.md (K30 e K31).
Lote: <PASTA DO LOTE>. Abra cada `folhas_finais/pNNX.jpg` (1ª imagem = FOTO 01 do anúncio; as outras 3 = cenas do vídeo final; ignore os textos).
Para cada cena, compare o produto com a foto 01 como cliente que vai receber a caixa: formato geral, proporção, cor e tom, cor dos pés/base/metal,
material/estampa/textura, costuras, braços, puxadores, gavetas, nichos, ripados, LEDs, nº de peças. Em dúvida, amplie (recorte com PIL).
Classifique cada vídeo: OK | AVISO (diferença pequena que a cliente notaria) | DESCARTAR (outro produto, outra variante, peça inventada ou faltando).
Grave `fiscal_final.json` na pasta do lote: {"pNNX": {"veredito": "OK|AVISO|DESCARTAR", "motivo": "curto, em português"}}. Não gaste nada pago, não faça commit.
Responda uma linha por vídeo que não for OK.
---
Depois: para cada AVISO/DESCARTAR, atualize o doc `conferir/<PRE>-<NN>` na Postagens (ArtifactData update, campo `aviso`, acrescentando
"A: ⚠ <motivo>"; DESCARTAR começa com "🗑️ descartar:"). A dona decide no Ok. No aviso final do lote: quantos OK, AVISO e DESCARTAR.
