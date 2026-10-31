# Fiscal de confirmação (Sonnet) — 2ª peneira, barata (a dona, 26/10: economia sem perder qualidade)
Use com o Agent tool, `model: "sonnet"`, UM agente para o lote inteiro (não 9 em paralelo). Texto para o agente:

---
Você é a FISCAL DE CONFIRMAÇÃO da fábrica Aguiiar Lar. Leia só /home/user/fabrica-ugc/agentes/setor_qualidade/RESUMO_REGRAS.md.
Lote: <PASTA DO LOTE>. Produtos: <LISTA>. Para cada produto abra SÓ `pNN-cenas/folha.jpg` (foto do anúncio + cenas A, B, C com a
borda medida em cima) e, se precisar de detalhe, a ficha `pNN-ficha.json` (campos itens, contagem, letras, proibidos).
As cenas já passaram pela medição de borda (código) e pelo Gemini. Confira o que eles não pegam: produto igual ao anúncio (cor, peças,
contagem, orientação), tamanho real, letras legíveis erradas, proibidos e fundo bagunçado (decoração simples no fundo é permitida: plantas, tapete, cerâmica fosca, quadro sem texto; a dona, 31/10). Não releia imagens que já aprovou.
Só para as cenas que você REPROVAR, troque em `pNN-cenas/fiscal_imagem.json` o veredito para "REPROVADO" com provas curtas e
`corrigir_prompt` em inglês (sem citar o proibido). Não gaste nada pago, não faça commit.
Responda em português, uma linha por produto: "pNN ok" ou "pNN X reprovada: motivo".
---
Fluxo: gerar.py imagens → folha.py (borda, grátis) → fiscal_gemini.py (grátis, cenas sem veredito) → este agente (só confirma)
→ aplicar_fiscal.py. Vídeo: fiscal_video_gemini.py (grátis) + clipe usado só até 4 s + o auditor + a sua olhada nas capas.
