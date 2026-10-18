# Como importar o Modelo Aguiiar Lar em outra sessão do Claude

Mensagem para colar na sessão nova (junto com o zip `pacote-modelo-aguiiar-lar.zip`):

> Descompacte o zip na raiz do projeto (ele cria `MODELO_DE_CRIACAO.md`, `video-teste/luxo/`, `video-teste/fontes/`,
> `video-teste/auditar_video.py`, `memoria/`, `agentes/`, `referencias/` e `trabalhos/` de exemplo; se já existirem
> arquivos com o mesmo nome, compare antes de sobrescrever e me diga o que mudou).
> Leia `MODELO_DE_CRIACAO.md` inteiro, depois `memoria/colecao-luxo.md` e `agentes/regras_de_erros.md` (regras 8 a 13).
> A partir de agora, todo vídeo de produto sai nos 3 modelos de layout do PDF `referencias/modelos-layout/`, com as
> mesmas regras e o mesmo processo, sem voz e com música calma. Para testar, renderize o exemplo
> `trabalhos/p03-poltrona-terracota` (prévias primeiro) e compare com os vídeos prontos de `trabalhos/p01-cabideiro/out2/`.
> Se a sua fábrica já tem outros modelos, mantenha-os, mas use este visual (tipografia, cor, assinatura, CTA discreto,
> rodízio de abertura, produto inteiro na capa, só qualidades reais) como padrão de qualidade.

## Checklist depois de importar
1. `pip install --break-system-packages numpy pillow` e `ffmpeg -version` funcionando.
2. `cd video-teste/luxo/specs && LUXO_DIR=$(pwd)/../../../trabalhos/p03-poltrona-terracota python3 lote_1018.py p03`
3. `cd .. && LUXO_DIR=... PREVIEW=0,6,13 python3 -I build_lux.py $LUXO_DIR/specs/p03_c_direto.json` → abrir os JPGs em `trabalhos/p03-poltrona-terracota/out2/`.
4. `./render_lote.sh /caminho/absoluto/trabalhos/p03-poltrona-terracota` → os 3 vídeos devem sair APROVADOS na auditoria.
5. Se algo não bater com o PDF dos modelos, o PDF e `MODELO_DE_CRIACAO.md` mandam.

## O que tem no pacote
- `MODELO_DE_CRIACAO.md` — o modelo completo (layouts, regras, som, processo, instalação).
- `referencias/modelos-layout/Modelos_de_layout_Fabrica_UGC.pdf` — os 3 layouts com imagens (para mostrar a quem for criar).
- `referencias/exemplos-layout/` — JPGs de comparação usados na escolha (opção 1 "faixas" foi a escolhida para o B).
- `video-teste/luxo/` — montador, moldes, processo por produto, gerador de página, trilha calma, vozes (opcional).
- `video-teste/fontes/` — todas as fontes usadas.
- `video-teste/auditar_video.py` — auditoria automática.
- `memoria/colecao-luxo.md`, `agentes/regras_de_erros.md`, `agentes/licoes.md`, `agentes/prompts_da_dona.md` — decisões e regras.
- `trabalhos/p01-cabideiro/` — cenas, timelines e os 3 vídeos finais (exemplo real aprovado).
- `trabalhos/p03-poltrona-terracota/` — cenas e timelines para o teste.
