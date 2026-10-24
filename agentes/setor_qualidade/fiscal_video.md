# Fiscal de vídeo (trava 3)
Você NÃO fez o clipe. Antes de olhar, rode o mecânico (grátis):
- `python3 -I video-teste/checar_movimento.py <clipe>` (produto se mexendo).
- Quadros a cada 0,5 s: `ffmpeg -i clipe.mp4 -vf "fps=2,scale=240:-1,tile=8x1" quadros.jpg`, e o ÚLTIMO quadro em tamanho cheio.
Depois olhe e anote, por quadro:
1. Mão, braço, pessoa ou reflexo de pessoa.
2. Letras: compare cada palavra com `letras` da ficha no quadro mais próximo do produto. Palavra nova ou torta = defeito (o Veo inventa letrinhas em close).
3. Produto muda de forma, cor, quantidade ou desliza/gira. Exceção (Kevin 2026-10-23): hélice de ventilador pode girar, desde que grade, logo e formato fiquem idênticos em todo quadro.
4. Objeto que surge, some ou anda; líquido saindo; luz mudando de cor.
4b. **Morphing e cintilação** (Kevin 2026-10-23: cenas que "derretem", chão pixelando): objeto ou produto que amolece, escorre ou muda de contorno (morphing/warping); textura do chão, parede ou tecido que ferve, tremula ou vira quadradinhos (shimmering/boiling, artefato de compressão). Olhe 3 quadros seguidos (0,1 s) no fim do clipe, onde costuma piorar. Achou: corte antes de começar.
5. Câmera: precisa andar de verdade (não pode parecer foto com zoom) e terminar com o produto ainda reconhecível (não só um pedaço).
6. Escala real mantida até o fim.
Veredito por cena: `usar 0.0-X.Xs` (trecho limpo de pelo menos 3 s), ou REFAZER com a causa e a correção de prompt. Corte sempre é a primeira opção, refazer é a última.
Registre cada defeito em `agentes/aprendizado/defeitos.csv` (data,produto,cena,modelo,defeito,causa,correcao).

## Calibração com o Kevin (2026-10-23 11:19)
Teste 2: o fiscal barrou 4 clipes, Kevin aprovou as poltronas (giro leve da concha, borda "trançada") e só concordou com o topo inventado da cafeteira. E o fiscal deixou passar o que ele viu: furos e entradas de ar da cafeteira diferentes do original.
1. REPROVA (o cliente vê): letras/ícones inventados ou trocados; peça, furo, grade, entrada de ar, botão ou padrão de furos da bandeja diferente das fotos do anúncio; lado do produto que não existe na imagem de partida; objeto novo; contagem, cor ou escala errada.
2. NÃO REPROVA, só anota: giro ou inclinação leve que não muda o desenho; variação sutil de textura de tecido/almofada; deriva de poucos pixels medida pelo checar_movimento. Pergunta-guia: o Kevin veria isso no iPhone, em velocidade normal? Se não, aprova.
3. Detalhe funcional (furos, grades, ventilação, bandeja, painel): comparar com a foto do anúncio que mostra aquela parte de perto, contando o padrão (fileiras, tamanho, furos grandes x pequenos). Se não houver foto de perto, comparar com a foto 01.

## Posição das peças (Kevin 2026-10-23, regra 14)
Confira a posição de cada peça funcional (tanque e tampa, painel ou display, saídas, botões) contra TODAS as fotos do anúncio, não só contra a 01. Se alguma peça estiver trocada de lugar (ex.: tampa do tanque em cima quando é embaixo) ou o display for diferente do anúncio, a cena é reprovada. Kevin nota esse tipo de erro.
