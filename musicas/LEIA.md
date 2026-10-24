# Músicas (OPCIONAL: a dona decide)


O kit vem em partes de até 30 MB: `1-fabrica-shopee-principal.zip` (obrigatório) não traz as trilhas. As 30 trilhas vêm em
`2-musicas-a/b/c.zip` e o timbre do gerador em `3-gerador-musicas-1/2.zip`. Só suba esses se ela quiser música; descompacte por cima
da mesma pasta `fabrica-shopee` (as pastas já batem).
Pergunte à dona na primeira vez que for renderizar: quer música de fundo? Quais? Grave a resposta em `memoria/licoes_da_fabrica.md`.
- **Sem música:** renderize com `MUSICA=<raiz do kit>/musicas/silencio.wav` (15 s de silêncio).
- **Usar as 30 do kit:** já funciona sozinho. `biblioteca/` tem 30 trilhas de 15 s (11 clássicas em domínio público com arranjo
  próprio + 19 calmas originais), a -20 LUFS. Sem custo, sem crédito, sem Content ID. Apague as que ela não quiser.
- **Criar as dela (grátis):** junte o timbre e gere novas peças:
  `cat gerador/GeneralUser-GS.sf2.parte0* > gerador/GeneralUser-GS.sf2` (está em 3 partes porque o GitHub do navegador só aceita arquivos de até 25 MB),
  `pip install --no-deps tinysoundfont`, `python3 -I gerador/compor.py gerador/GeneralUser-GS.sf2 PASTA_SAIDA`.
  As peças ficam em `gerador/compor.py` e `gerador/pecas.py` (dá para pedir ao Claude estilos novos: mais delicado, harpa, piano...).
  Depois normalize a -20 LUFS e ponha em `biblioteca/`. Timbre GeneralUser GS v2.0.3: uso comercial liberado.
- **Uma trilha fixa:** `MUSICA=/caminho/da/trilha.wav`.

Como alterna: `escolher.py` (o mesmo vídeo sempre recebe a mesma trilha; senão a usada há mais tempo, sem repetir as últimas 15
na mesma conta; registro em `usadas.json`). Ligado em video-teste/luxo/specs/produto.py (`trilha()`).
Volume nos vídeos sem voz: baixo (-22 LUFS), agudos -3 dB acima de 6 kHz, fade-in 1,2 s (luxo/build_lux.py).
Música de app (TikTok/Instagram) não entra em postagem automática; por isso as trilhas próprias.
