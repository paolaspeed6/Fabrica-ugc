# Setor de Qualidade (Kevin, 2026-10-23)
Meta: vídeo certo na PRIMEIRA geração, com cara de pessoa real filmando, produto idêntico ao anúncio.
Cada agente é um subagente separado (Agent tool, modelo opus), com contexto limpo. Kevin aprovou o uso (plano 20x, 2026-10-23).
Quem reprova não criou: o fiscal nunca é o mesmo agente que escreveu o prompt.

| Trava | Agente | Quando | Saída |
|---|---|---|---|
| 1 | [fichador.md](fichador.md) | antes de qualquer gasto | `ficha.json` do produto |
| 2 | [fiscal_imagem.md](fiscal_imagem.md) | depois do Nano Banana, antes do Veo | APROVADO/REPROVADO por imagem |
| 3 | [fiscal_video.md](fiscal_video.md) | depois do Veo, antes da edição | trecho limpo por cena ou REFAZER |
| 4 | [melhorador.md](melhorador.md) | 1 vez por lote, depois da revisão do Kevin | regras e prompts corrigidos + placar |

Receita atual de cena (teste 2026-10-23): Nano Banana 2.1 Edit (US$ 0,0396) com as melhores 3-4 fotos + Veo 3.1 Lite image-to-video 4 s 720p (US$ 0,20 medido), prompt UGC com ficha e narração em PT-BR.
Toda regra antiga de regras_de_erros.md continua valendo.
