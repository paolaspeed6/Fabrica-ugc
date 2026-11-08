# Próximo lote: o essencial (leia só isto ao começar uma conversa nova)

Atualizado: 2026-11-08 manhã (Listas 08/11 A e B entregues, em conversas separadas). Histórico completo: memoria/historico_lotes.md. Regras: CLAUDE.md. Lições: memoria/licoes_da_fabrica.md.

## Como começar
- Conversa nova, no mesmo projeto. Ela não lembra de conversas antigas: só o que está nos arquivos.
- Lote novo: a dona manda "Lote do dia: 15 produtos da Fila, teto US$ 8". Crie a conversa com model claude-opus-5-5.
- Agentes de conferência (Fichador, fiscais): model sonnet.
- Pasta do lote: video-teste/lote/lista<DDMM><letra> (cópia de video-teste/lote/modelo). Passos: CHECKLIST.md.

## Regras que não podem falhar
- TESTE K24 (01/11): produto "largo" usa a guia (foto 01 na posição certa, só o cômodo muda). No aviso final: quantas cenas largas
  passaram de 1ª e se o Nano Banana manteve o produto igual à foto. Olhe a guia.jpg de 1 produto antes de gerar o resto.
- TESTE K23 (a dona, 31/10): o 1º lote com cenas "com vida" (sol, plantas, enfeites simples) conta no aviso final quantas cenas foram
  reprovadas por enfeite (surgiu/mudou no vídeo, vaso parecendo garrafa). Se der problema, a dona quer VOLTAR ao fundo vazio (git revert f9d1011).
- Nada pago sem OK da dona e teto em dólar. Refazer uma imagem ou clipe pago só UMA vez. Reprovou 2x: entender o motivo, não gerar de novo.
- Todo produto sai com A, B e C. Versão reprovada pelo auditor é refeita só na edição (grátis).
- Produto sem cena aprovada (K22, 30/10): a fábrica monta A, B e C sozinha com as imagens reprovadas só por borda (câmera por código,
  grátis, sem_cena.py no produzir.sh) e manda para a Conferir com o aviso "cenas reprovadas pela fiscal: confira". Defeito grave fica
  fora. Sem imagem aproveitável: cartão "resgate" (nunca descartar sem a dona ver).
- SEMPRE, em todo lote (a dona, 28/10): vídeo pronto vai para a Conferência (aba Conferir da Postagens, 7HYeG...). Só o Ok da dona libera para Postagens (automático, sem o Claude). A Conferência fixada antiga (6An95...) agora é só um botão para a certa.
- Edição: layouts A "Um dia com ela", B "Faixas", C "Direto ao ponto". Música animada (musicas/biblioteca). Assinatura "Aguiiar Lar" muda de lugar no vídeo.
- Nunca subir chave, token, link de afiliado ou Sub ID em repositório público (este é privado).

## Páginas (mesmo endereço)
- Postagens + Conferência: https://claude.ai/artifact/7HYeGG32XBtjXTcMMoffJt (botão "Conferência →").
- Tinder: https://claude.ai/artifact/U1eK13L3ufz213GvJcXkni
- Jogo (Reino Encantado): https://claude.ai/artifact/XZAgnZ6G94M1vYAqo8hFAd

## Lista 08/11 B (08/11 ~09h45 UTC; feita junto com a Lista 08/11 A, trabalhos p380-p386)
- 7 produtos com A, B e C (21 vídeos, 0811B-01..07, 12 s) na aba Conferir, pendentes. Gasto US$ 2,69 de 4 (25 imagens + 17 clipes).
  Nenhum pulado. Tinder: os 7 em `pronto`. Carrossel: 1 produto (p02 Impressora Y12, nota 9).
- K24: 4 largos (p01 Barraca, p03 Furadeira Bosch, p04 Kit DeWEN, p06 Anilhas) = 12 cenas; 9 passaram de 1ª. Guia em p01 (foto 05) 3/3
  e p04 (foto 06) 1/3; p03 e p06 do zero. p03: borda mediu a mesa, aprovei A/B/C à mão olhando a folha.
- K23: 2 cenas reprovadas por enfeite (p04 B planta encostando na maleta; p07 B vaso encostando + oficina bagunçada). Nenhum clipe com enfeite mudando.
- Cenas que restaram: p04 só A; p05 A e C; p07 A e C.
- Avisos para a dona: p01 fotos não mostram "2 ambientes"/"2-16 pessoas" (textos sem número); p03 é Bosch de verdade (peso discorda, sem peso);
  p04 marca DeWEN com visual parecido com DeWalt (sem marca nem "original"; 30 x 20 peças, sem número); p05 sem medidas no anúncio;
  p06 nenhuma foto mostra as 6 anilhas (feito 2 grupos de 3); p07 só a caixa, sem gerador.
- O produzir.sh da lista B usou n0+51 para não colidir com a lista A.
## Lista 08/11 A (08/11 ~09h50 UTC)
- 7 produtos com A, B e C (21 vídeos, 0811A-01..07, trabalhos p330-p336, 12 s) na aba Conferir, pendentes.
  Gasto US$ 2,91 de 4 (23 imagens = 21 + 2 refações; 20 clipes). Nenhum pulado. Tinder: os 7 em `pronto`.
- Carrossel: 5 produtos no Drive (p01-p05, nota >= 8); fora p06 Base (1) e p07 Halteres (7).
- K24: 3 largos (p02 Banquetas e p03 Baú com guia; p04 Cortina do zero, sem foto limpa) = 9 cenas; 9 passaram de 1ª. Produto igual à foto.
- K23: nenhuma cena reprovada por enfeite. Nenhum clipe com enfeite mudando. p06 A e C reprovadas pela Sonnet (cadeira/banquinho
  ao fundo); refeitas 1x: A aprovada, C repetiu o banquinho = falhou (p06 usa A e B).
- O rembg não baixou o modelo (504 do GitHub) e a fase 1 rodou sem borda: baixei à mão (`mkdir -p ~/.u2net && curl -L -o ~/.u2net/u2net.onnx ...`)
  e conferi a borda olhando. Sub ID: gerar_links.py usa AAMMDD com o ano 26 (261108), não 25.
- Avisos para a dona: p01 anúncio com ~20 cores (fiz verde-sálvia, perto da foto 01); p04 largura 4 m ou 6 m não dita (textos sem
  largura); p05 3 cores (fiz freijó/off-white da foto 01); p06 alturas discordam (textos sem altura); p07 descrição 4 anilhas de cada
  peso x foto 3 por lado (fiz como a foto).

## Lista 07/11 A (07/11 ~06h40 UTC)
- 11 produtos com A, B e C (33 vídeos, 0711A-01..08, 10..12, trabalhos p319-p329, 12 s) na aba Conferir, pendentes.
  Gasto US$ 4,24 de 8 (49 imagens = 33 + 16 refações; 23 clipes). Tinder: os 11 em `pronto`.
- Pulados pelo Fichador (Tinder volta a `aprovado` + `pulado`): p09 Tapete degrau 52462303951 (bebê e cachorro nas fotos limpas),
  p13 Capas de cadeira 23497764752 (20 kits, cor não dita), p14 Papel fotográfico 58268060894 (foto 01 banner, 1000 folhas sem foto limpa).
- K24: 4 largos (p04 Carrinho, p06 Barraca, p11 Base hidráulica, p12 Amortecedores) = 12 cenas; 5 passaram de 1ª.
  Guia só no p11 (único largo com foto 01 boa): A e B de 1ª, produto igual à foto. p04, p06, p12 do zero (foto 01 com texto).
- K23: 4 cenas reprovadas por enfeite encostando (Sonnet: p02 B, p10 A, p11 C, p12 C); refeitas 1 vez (p02 B e p10 A aprovadas;
  p10 A aprovada à mão, a borda mediu o fio). Nenhum clipe com enfeite mudando.
- Cenas que restaram: p04, p06 e p12 com 1 cena só; p01, p05, p08, p11 com 2.
- Avisos para a dona: p05 é Lattafa Afeef (não parece réplica; foto 03 diz "feminino", descrição unissex: textos sem gênero);
  p06 anúncio "2 ambientes" x foto "3" (textos sem número); p12 título 2002-2016 x descrição 2004-2016 (sem anos), peças revisadas
  (sem "original"); p01, p02, p03 foto 01 com cena de bar/abajur/caixa: referência foi outra foto limpa.

## Lista 06/11 A (06/11 ~08h UTC)
- 15 produtos com A, B e C (45 vídeos, 0611A-01..15, trabalhos p304-p318, 12 s) na aba Conferir, pendentes.
  Gasto US$ 5,19 de 8 (63 imagens = 45 + 18 refações; 27 clipes). Nenhum pulado; reservas 58218204570, 58254802142, 58216811643 seguem livres.
  Tinder: os 15 em `pronto`.
- K24: 5 largos (p01 Gangorra, p02 Cadeiras Trida, p09 Poltronas Opalla, p12 Pneus, p14 Cômoda) = 15 cenas; 7 passaram de 1ª.
  Guia conferida no p09: produto igual à foto. p02 sem cena aprovada (borda 94-97%) → K22 com aviso.
- K23: nenhuma cena reprovada por enfeite. Nenhum clipe com enfeite mudando.
- Fiscal Sonnet: p15 B reprovada (rótulo com letras erradas, falhou); p08 C reprovada pela cor, aprovei à mão (mesmo tom da A, luz quente).
- Cenas que restaram: p07 e p09 com 1 cena só (C); p14 só A; p06 A e C. p03 A e p11 A usam só 2 s (deformação depois).
- Avisos para a dona: p03 Kit MTG e p04 Chave ZRF só tinham fotos de propaganda; p06 Bosch vendida sem bateria (não parece réplica);
  p14 Cômoda referência foto 05 (a 01 tem pelúcia/trocador); p11 Mesa "Taça" chamada de torneada; p12 etiqueta de eficiência discorda (não citada).

## Lista 05/11 A (05/11 ~23h20 UTC)
- 15 produtos com A, B e C (45 vídeos, 0511A-01..15, trabalhos p289-p303, 1º lote com vídeos de 12 s) na aba Conferir, pendentes.
  Gasto US$ 5,74 de 8 (54 imagens + 36 clipes). Tinder: os 15 em `pronto`.
- Pulado: p09 Desumidificador Komeco 58219853250 (a Shopee não entregou o anúncio; Tinder volta a `aprovado` + `pulado`).
  Entrou a reserva 58250028195 Banco de jardim (p09). Reservas 58263107666 e 58258967475 seguem livres.
- K24: 6 produtos largos (p02, p06, p08, p09, p10, p12) = 18 cenas; 10 passaram de 1ª (+ p09 A reprovada por engano na borda, aprovada
  à mão). Guia conferida no p09: produto igual à foto. p10 Anilhas (foto ruim): só C aprovada.
- K23: 1 cena reprovada por enfeite (p14 A tigela no balcão, Sonnet; refeita e aprovada). Nenhum clipe com enfeite mudando.
- Fiscal de vídeo: p15 A hélice pode girar (aviso no cartão). Quase todos os clipes "câmera parada" (a câmera por código compensa).
- Avisos para a dona (nos cartões): p02 Bike (descrição "vermelha", fotos azuis); p08 Furadeira (foto 01 com 2 ferramentas, fiz 1);
  p10 1 cena só; p15 capa com gancho em cima do ventilador; p07 Kappesberg medidas discordam (fotos 03 x 04).
- Container reiniciou no meio da fase 2: os arquivos ficaram; re-render só dos que faltavam (render_lote.sh + entregar.sh à mão).
  ffprobe falhando no entregar = mp4 cortado pelo reinício: apague e renderize de novo.

## Lista 02/11 D (03/11 ~01h50 UTC)
- 15 produtos com A, B e C (45 vídeos, 0211D-01..15) na aba Conferir, pendentes. Gasto US$ 5,01 de 8 (66 imagens + 24 clipes).
  Nenhum pulado (reservas 58216420941, 58218876924, 58267293734 seguem `aprovado`, livres). Tinder: os 15 em `pronto`.
- K24: 12 produtos largos = 36 cenas; 14 passaram de 1ª. Com guia (foto 01 boa, 9 produtos): 12 de 27 de 1ª (p08 Mangueira 3/3;
  p02, p06, p13 2/3; p05 Cadeira Pétala 0/3 e foi K22 com aviso). Do zero (p04, p11, p12): 2 de 9. Produto igual à foto nas cenas com guia.
- K23: 1 cena reprovada por enfeite (p12B pote branco na janela, Fiscal Sonnet). Nenhum clipe com enfeite mudando.
- Sonnet reprovou p10B e p12C já liberadas (aplicar_fiscal pula cena em estado `animar`: refiz à mão, 1 vez). p12C aprovada (aço claro);
  p10B saiu 2x com laterais fechadas = falhou (p10 com 1 cena só).
- Avisos para a dona: p06 Base de mesa (só a base, sem tampo; a Lista 02/11 B teve outra base parecida); p04 Cadeiras Alicia (foto 01
  com cotas, medidas discordam, textos sem número); p03 Impressora (marca GENAI x "Tattoo Printer"); p01 Colchão (tamanho não dito,
  queen estimado); p11 título "Similar a Makita" (corpo SONGHE); p14 foto 01 com 4 cadeiras, kit é de 2.

## Lista 02/11 C (02/11 ~05h40 UTC)
- 15 produtos com A, B e C (45 vídeos, 0211C-01..15) na aba Conferir, pendentes. Gasto US$ 5,48 de 8 (55 imagens + 33 clipes).
  Nenhum pulado (reservas 58254629841, 58215886048, 58267293734 seguem `aprovado`, livres). Tinder: os 15 em `pronto`.
- K24: 6 produtos largos (p01 cadeiras, p05 cômoda, p08 penteadeira, p10 banco baú, p11 rack, p12 escrivaninha) = 18 cenas; 7 passaram
  de 1ª. Com guia (foto 01 boa) só p05 e p12: p05 0 de 3 de 1ª (1 aprovada na refação), p12 2 de 3. Os outros 4 foram do zero.
- K23: nenhuma cena reprovada por enfeite. p09 B reprovada pela Fiscal Sonnet (brinquedos inventados na cadeirinha).
- Emoji no gancho (K26): saiu ☒ em 8 produtos; tirei e re-renderizei (grátis). Cuidado: lote_auto.py com subconjunto renumera as pastas
  (p05 virou p262) e o entregar.sh usa trabalhos_todos.json (mapa velho): atualize o trabalhos_todos.json antes de entregar de novo.
- Avisos para a dona: p02 Eames (foto 1 cadeira, descrição "conjunto de 2"); p11 Rack (foto do anúncio com TV SONY, não vendida);
  p15 Armário (anúncio vende 4, 5 ou 6 camadas; fiz 5); p06 Luminária (fotos com marca d'água LUZORA).

## Lista 02/11 B (02/11 ~02h UTC)
- 15 produtos com A, B e C (45 vídeos, 0211B-01..10, 12..16) na aba Conferir, pendentes. Gasto US$ 5,06 de 8 (57 imagens + 28 clipes).
  Tinder: os 15 em `pronto`.
- Pulado pelo Fichador: p11 Kit Camping 12 itens 58268825392 (só colagem, kit com frascos de cal). Tinder: `aprovado` + `pulado`.
  Entrou a reserva 58269823326 Estante VONDER (p16). Reservas 58216811643 e 58270305535 (perfume Afeef) seguem livres.
- K24: guia em p04 Banquetas (3 de 3 de 1ª) e p05 Bike infantil (1 de 3; A e C com 88-89% da largura: foto quadrada a 75% da guia
  enche o quadro). 4 de 6 cenas com guia de 1ª; produto igual à foto nos dois. p13 Cabeceira e p14 Penteadeira: guia não usada
  (cabeceira cortada na foto; pincéis em cima). p13 sem cena aprovada (borda) → K22 com aviso.
- K23: 1 cena reprovada por enfeite (p12B caneca na mesinha, Fiscal Sonnet). Nenhum clipe com enfeite mudando.
- Perfume Armaf Maleka (p09): não parece réplica (frasco/caixa Armaf), loja revendedora genérica.
- Avisos para a dona: p10 é só a base (sem tampo); p07 título "Creality 10 kg" x foto 1 rolo Soleyin 1 kg (textos sem peso/marca);
  p03 título "Marrom" x foto branca (fiz branca); p02 e p08 sem foto 100% limpa.
- Os lotes A e B usaram os mesmos números de trabalho (p259-p273) com nomes diferentes: sem colisão de arquivo.
- Atenção: `pgrep -f build_lux` dentro do mesmo comando acha a si mesmo (laço infinito); rodar 2 build_lux no mesmo vídeo corrompe o mp4.

## Lista 02/11 A (02/11 ~01h50 UTC)
- 15 produtos com A, B e C (45 vídeos, 0211A-02..16) na aba Conferir, pendentes. Gasto US$ 5,86 de 8 (57 imagens + 36 clipes).
  Tinder: os 15 em `pronto`.
- Pulado pelo Fichador: p01 Mesa Colméia 13843468905 (foto 01 com 3 cores, sem dizer qual é vendida). Tinder: `aprovado` + `pulado`.
  Entrou a reserva 58267850781 Cadeira de balanço 4 molas (p16). Reservas 58215062273 e 58216676221 seguem livres.
- 1º lote com K24 (guia) e K25 (ganchos). Largos com guia: p09 Poltronas (1 de 3 de 1ª) e p15 Kit 3 Poltronas (3 de 3 de 1ª):
  4 de 6 cenas largas passaram de 1ª. O Nano Banana manteve o produto igual (cor, peças), mas no p15 espalhou as 3 poltronas
  em vez de manter a posição da guia. p03 Balcão (foto ruim, do zero): 1 de 3 de 1ª. A medição de borda (rembg) reprovou por engano
  p09A e p03B (mediu planta/parede junto): aprovei à mão olhando a folha.
- K23: 1 cena reprovada por enfeite (p05C cesto encostado na lixeira). Nenhum clipe com enfeite mudando.
- Emoji no gancho saiu como quadradinho (5 vídeos A): refeito na edição; o textos.py agora tira emoji sozinho.
- Avisos para a dona: p11 título diz "elétrica sem fio" mas a foto é só a chave de catraca com extensor; p10 foto 01 tinha carro
  (não entrou); p05 Lixeira e p06 Poltrona com 1 cena só aprovada (vídeo repete a cena).
- Os números de trabalhos/ (p259-p273) podem coincidir com os dos lotes B/C feitos ao mesmo tempo (nomes diferentes, sem conflito).

## Estado anterior (01/11, manhã)
- Lote 01/11 A (01/11 ~06h40 UTC): 15 produtos com A, B e C (45 vídeos, 0111A-01..15) na aba Conferir, pendentes. Gasto US$ 5,33 de 8
  (69 imagens + 26 clipes). Tinder: os 15 em `pronto`. Nenhum pulado; reserva 13843468905 Mesa Colméia segue `aprovado` (livre).
- K22 (câmera por código + aviso): p04 Churrasqueira, p10 Kit 2 Mesas de Cabeceira, p13 Mesa em L.
- Teste K23 (2º lote): 1 cena reprovada por enfeite/fundo bagunçado (p12C ferramentas soltas). Nenhum clipe com enfeite mudando.
- Avisos para a dona: p08 GM Bear é chave de catraca (título diz impacto); p14 Maldivas x Ibiza; p11 sem medidas.
- Fila: aprovados livres só a Mesa Colméia + os 13 já pulados. Próximo lote precisa de mais "aprovados" no Tinder. Nenhum lote aberto.
- O push para main: a conversa nova pode abrir em HEAD solto; use `git checkout -B main HEAD` antes do push.

## Estado anterior (31/10, noite)
- Lote 31/10 A (31/10 ~21h UTC): 8 produtos com A, B e C (24 vídeos, 3110A-02..09) na aba Conferir, pendentes. Gasto US$ 3,23 de 5
  (36 imagens + 18 clipes). Tinder: os 8 em `pronto`.
- Pulado pelo Fichador: p01 Filamento 3D SUNLU 58217392854 (logo de outra marca na foto 01, sem foto dos 10 rolos). Tinder: `aprovado` + campo `pulado`.
- 1º lote com K23 (cena com vida). p02 Cortina e p06 Cadeiras de praia com 1 cena só aprovada (vídeo repete a cena).
- Avisos para a dona: p05 Gabinete (foto mostra PC montado, não vendido); p08 Estante preta (foto 01 do anúncio é azul); p07 "75 cm" ambíguo.
- O produzir.sh usa /home/user/fabrica-ugc (minúsculo): numa conversa nova crie o atalho `ln -s /home/user/Fabrica-ugc /home/user/fabrica-ugc`.
- Fila: aprovados livres agora só os 12 já pulados + p01 Filamento (pulado). Próximo lote precisa de mais "aprovados" no Tinder. Nenhum lote aberto.

## Estado anterior (31/10, madrugada)
- Lote 30/10 B (31/10 ~02h30 UTC): 15 produtos com A, B e C (45 vídeos, 3010B-01..15) na aba Conferir, pendentes. Gasto US$ 5,44 de 8
  (54 imagens + 33 clipes). Nenhum pulado (reservas não usadas). Tinder: os 15 em `pronto`.
- 1º lote real do sem_cena.py (K22): funcionou. 3010B-13 Lustre Corsalle (clipe A acendeu as lâmpadas; B era outro modelo e ficou fora:
  vídeos com A e C) e 3010B-15 Kit 2 Estantes (A, B e C só por borda) foram montados com câmera por código e foram com o aviso
  "cenas reprovadas pela fiscal: confira". A dona decide/descarta à mão.
- Avisos para a dona: p04 Batedeira só tinha 1 foto (ambiente); p06 Hotend "ORIGINAL Creality" (foto 01 com logo, peça sem nome);
  p02 Painel TV e p13 Lustre com 1 cena só aprovada (vídeo repete a cena).
- Drive: a 1ª subida caiu (Connection reset) e o entregar.sh saiu sem conferir_docs; rodei drive_backup.py + entregar.sh de novo à mão.
- Fila: aprovados livres agora são só as reservas 58217392854, 58215204667, 58203555197, 53018045160, 49217644309 (+ os 12 já pulados
  e os outros aprovados do Tinder). Nenhum lote aberto.

## Estado anterior (30/10, noite)
- Resgates processados (30/10, US$ 0): 2810A-13 Colchão, 2810B-06 Cabeceira + Recamier, 2910A-09 Aparador Tekna, 2910A-10 Kit Poltronas
  Opala, 3010A-10 Bicicleta Tríade: 15 vídeos (A, B e C) na aba Conferir, pendentes, nos mesmos cartões (resgate_processado: true).
  Imagens do histórico da WaveSpeed (casadas pelo poster), textos refeitos do anúncio (pastas antigas não estavam no disco), câmera
  por código (camera_codigo.py). B do colchão, cabeceira e poltronas vai com aviso (zoom suave; o auditor achou quase parada).
  Tinder: os 5 em `pronto`. Ainda em `produzindo` no Tinder (de lotes antigos, não mexi): 52916448186, 54418096324, 54661666510, 56166664405.
- Nenhum resgate pendente. Nenhum lote aberto.

## Estado anterior (30/10, manhã)
- Lote 30/10 A (30/10 09h50 UTC): 10 produtos com A, B e C (30 vídeos, 3010A-01..09, 11) + 3010A-10 Bicicleta Infantil Aro 20 Triade
  como resgate (larga demais), na aba Conferir. Gasto US$ 4,06 de 6 (47 imagens + 22 clipes). Tinder: 10 em `pronto`; 58214424772 (resgate) segue `produzindo`.
- 3010A-07 Cama Carro: aviso de adesivo parecido com Hot Wheels (a dona decide). p02 e p04 com 1 cena só.
- Fila: nenhum aprovado livre (só os 12 já pulados). Próximo lote precisa de mais "aprovados" no Tinder.
- Chave Shopee no ambiente se chama `shopee_APP_SECRET` (minúsculo): `SHOPEE_APP_SECRET="$shopee_APP_SECRET" python3 -I gerar_links.py <AAMMDD>`.
- Copie a pasta modelo DEPOIS do git pull (no 30/10 a cópia saiu antes e faltavam K20/K21; corrigido a tempo).

## Estado anterior (29/10)
- Lote 29/10 A (29/10 22h05 UTC): 13 produtos com A, B e C (39 vídeos, 2910A-01..08, 11..15) + 2910A-09 Aparador Cerca Viva Tekna
  e 2910A-10 Kit 2 Poltronas Opala + Puff como resgate (largos demais), na aba Conferir. Gasto US$ 6,11 de 8 (66 imagens + 35 clipes).
  Tinder: 13 em `pronto`; 55107980511 e 58204213844 (resgates) seguem `produzindo`.
- Pulado pelo Orquestrador: Suporte lava-roupa 58203226664 (nenhuma foto vazia, sempre com máquina em cima; volta a `aprovado`).
- Fila: aprovados livres só Exaustor Ventisol 60 cm 23398536883 e Kit 4 Cadeiras Amis Rattan 48318696775 (+ os 12 já pulados).
  Próximo lote precisa de mais "aprovados" no Tinder.
- Regra nova K20: rodar textos.py antes da fase2 (o produzir.sh agora para sozinho antes dos clipes se faltar).

## Estado anterior (28/10)
- Lote 28/10 B (28/10 22h35 UTC): 12 produtos com A, B e C (36 vídeos, 2810B-01..05, 07..13) + 2810B-06 Cabeceira Itália + Recamier
  como resgate, na aba Conferir. Gasto US$ 4,56 de 8 (52 imagens + 25 clipes). Só 13 aprovados livres na Fila (nenhum pulado).
- FILA VAZIA: todos os aprovados restantes são os 11 já pulados pelo Fichador. Próximo lote precisa de novos "aprovados" no Tinder
  (187 em "Escolher").
- Lote 28/10 A (28/10 20h40 UTC): 14 produtos com A, B e C (42 vídeos, 2810A-02..20) + 2810A-13 Colchão Ortho Flex como resgate,
  na aba Conferir. Gasto US$ 6,18 de 8 (60 imagens + 38 clipes). Pulados pelo Fichador (Tinder segue `aprovado`): Kit Cooktop+Balcão
  58254841155 (colagem), Viveiro 58265685456 (sem foto limpa), Radiador Kombi 58211200606 (colagem), Banco Kulmai 58209960104
  (modelos misturados), Chave de impacto 1200 N.m 58263626567 (só colagens).
- Lotes 27/10 A, B, C e D entregues na Conferir (gasto US$ 4,98 + 5,58 + 6,26 + 6,72).
- Lote 27/10 D (28/10 02h45): 15 produtos (2710D-01..15) + os 2 resgates (2710A-12 panelas, 2710C-01 espreguiçadeiras) com A, B e C,
  pendentes para a dona. Nenhum resgate nem pedido de edição pendente. Detalhes: memoria/historico_lotes.md.
- Resgate: imagens aceitas pela dona vêm do histórico da WaveSpeed (grátis) + câmera por código (zoompan), nunca clipe IA (regra K19).
- Fila: sem aprovados novos (só os 11 pulados). A dona precisa aprovar mais no Tinder antes do próximo lote.
- Tinder: 187 produtos novos da lista da dona (busca 27/10) em "Escolher". Fila = aprovados.
- Pedidos da dona já valendo: músicas animadas; assinatura "Aguiiar Lar" mudando de lugar.
- Foto colada (produto complexo): só se a dona pedir. Não testada.

## Redes sociais (Reels automático): PENDENTE
- Facebook e Instagram: funcionando (postar.py conferir).
- Threads: "Failed to decrypt". A dona trocou THREADS_TOKEN. Testar numa conversa nova; se falhar, gerar outra chave (developers.facebook.com > app > Casos de uso > API do Threads > Gerador de token).
- Reels: layouts A e C alternando (B fica só na Shopee). Ainda não há Reels prontos.
- Postagem automática: até 2 por dia por rede, 3 horas entre posts. Só posta com o OK da dona (produto, layout, legenda).
- Não postar nada sem a dona aprovar.

## Lembretes para a sessão nova (o que o Claude precisa fazer ao começar)
1. Ler este arquivo. Não reler o histórico inteiro.
2. Se a dona falar de redes: rodar `cd meta && python3 -I postar.py conferir` (não imprime tokens).
3. Se falar de lote: conferir a aba Conferir antes de criar outro lote.
