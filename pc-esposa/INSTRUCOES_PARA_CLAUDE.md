# Instruções para o Claude da esposa do Kevin

Você vai instalar, adaptar e operar as automações Shopee (postar, filtro de afiliados, interagir curtidas, assistir e Central) neste PC (Windows). Fale com ela em português, curto e direto. O código veio do PC do Kevin; os caminhos foram padronizados para `C:\horst\tablet`.

## 0. Regras que valem sempre (não negociáveis)
- **Nunca** burlar captcha, nunca automatizar login/senha/PIN da Shopee, nunca falsificar aparelho nem esconder o adb. Captcha/login: o script pausa e apita; ela resolve à mão.
- **Um aparelho por conta, uma tarefa por vez** por conta. Conta principal = postagens. Conta secundária = filtro de afiliados e assistir (revezam no mesmo celular; nunca juntos).
- Nunca escreva chave de API, token, link de afiliado ou senha em arquivo do pacote nem em repositório. Use variáveis de ambiente. Pasta com dados dela nunca vai para GitHub público.
- Gasto de API paga (Anthropic, WaveSpeed etc.): **pergunte a ela antes**, com teto e estimativa.
- Não aumente volume de postagens para além do ritmo do script (8-12 min por post, 08:00-22:00). Ban de postagem já aconteceu por produto errado; as travas existem por isso. Nunca as remova sem ela pedir explicitamente e ciente do risco.

## 0b. Aparelho dela
Ela usa **um único celular Android: um POCO C85 (Android 15, 720x1600) que era do Kevin**. Use-o como `celular1` no `aparelhos.json` dela e **revezem** tarefas (postar, filtro, curtidas) nele, nunca duas ao mesmo tempo. Esse POCO já esteve preso na permissão de câmera do Android e só aparece no adb por USB: pergunte se está com depuração USB (+ "Depuração USB (Configurações de segurança)" no Xiaomi) ligada. As coordenadas do pacote foram feitas nesse modelo, então devem servir quase direto; mesmo assim, teste com 1 post / 3 itens.

## 1. Perguntas iniciais (faça de uma vez só)
1. Nome exibido do perfil de postagem (conta principal) e @usuário.
2. Nome exibido e @usuário do perfil da conta secundária (usado no "assistir").
3. Qual celular Android é de cada conta (marca/modelo, tamanho de tela, Android). Ela só tem iPad/iPhone? Então vá ao **modo semi-manual** (seção 8).
4. Letra do Google Drive no PC (ex. `G:`) e nome das pastas (padrão: `Central Esposa` e `Videos Esposa`).
5. Ela tem credencial da API de afiliados Shopee? (opcional, só para o varredor diário que gera `candidatos_afiliados.json`; guardar em variáveis de ambiente `SHOPEE_APP_ID` / `SHOPEE_APP_SECRET` no PC dela, nunca no pacote).

## 2. Instalação
1. Copie `scripts\` (todo o conteúdo) para `C:\horst\tablet\` (ou use outra pasta e rode substituição de `C:\horst\tablet` nos .py/.cmd; confira com `grep`).
2. Instale Python 3.12 (python.org), adb (Android platform-tools em `C:\horst\tablet\platform-tools\`), e as libs que os scripts importarem (`pip install pillow` etc.; leia os imports; opcionais ficam em `C:\horst\tablet\pylibs`). OCR usa o Windows (`ocr_tela.ps1`, `afiliados\ocr.ps1`), sem instalar nada.
3. No celular: ativar Opções do desenvolvedor, Depuração USB; em Xiaomi/POCO ligar também **"Depuração USB (Configurações de segurança)"** e reiniciar (sem isso os toques falham com INJECT_EVENTS). Tela não pode apagar durante o trabalho (`tela_apagada.py` ajuda). Dados móveis desligados, Wi-Fi ligado. Login na Shopee feito por ela, à mão.
4. `adb devices` → anote o serial de cada celular e preencha `aparelhos.json` (`celular1` = principal/postagens, `celular2` = secundário). Os `.cmd` usam `HORST_ADB_SERIAL`; ajuste os placeholders `<IP_DO_CELULAR1>`, `<SERIAL_CELULAR2>` etc. em todos os `.cmd`, `.py` e `.pyw` (`grep -rn "<" ` para achar). O caminho do Python nos `.py` aparece como `C:\horst\python\python.exe`: troque pelo real.
5. Crie no Drive as pastas `Central Esposa` e `Videos Esposa\AAAA-MM-DD` e confira a letra do drive nos arquivos: `afiliados\rodar_candidatos.py` (LISTA), `conferir_afiliados.py` (VENDAS_RECENTES), `pular_afiliados.py` (ARQ), `rodar_fila.py` (`pasta_videos_do_dia`, `PASTA_DRIVE`).
6. Rode `python -m py_compile` em todos os .py e faça testes **sem postar**: `adb devices`, captura de tela, `teste_trava.py` (teste seco da trava de produto), `python conferir_afiliados.py --teste`.

## 3. Postagens (conta principal, celular 1)
Arquivos: `rodar_fila.py`, `postar_shopee.py`, `conferir.py`, `pendentes.py`, `vigia_postagem.py`, `aparelho_atual.py`, `tela_apagada.py`, `captcha_log.py`, `alerta.py`, `rodar_fila.cmd`.

Dados que ela fornece (você cria os arquivos):
- `fila.json`: lista de `{"doc": "DDMMX_NN_nome_A", "produto": "...", "link": "<link do produto dela>", "legenda": "<até 150 caracteres, sem links>"}`. O `doc` é o nome do mp4 (`DDMM` no início decide a pasta do dia no Drive). Links de afiliado são **dela**, nunca os do Kevin.
- Vídeos em `Videos Esposa\AAAA-MM-DD\<doc>.mp4` no Drive.

Fluxo que o script já implementa (preserve; só mude coordenadas/textos se a tela dela for diferente):
1. Abre o produto pelo **itemId** (não só pelo link curto), confirma ID, nome e preço por OCR; o título lido nunca pode ser o do post anterior.
2. Favorita/curte o produto, abre o perfil, "+ Postar vídeo", Biblioteca, escolhe o vídeo, legenda, "Adicionar produto" > Minhas Curtidas > pega a linha pelo **nome esperado** (rola até 8 telas).
3. Antes de **Postar**, confere o cartão do produto no editor. Dúvida = **não posta**: grava em `pendentes_aprovacao.json` com print e segue para o próximo item (outras versões A/B/C do mesmo produto ficam retidas).
4. Depois de "Enviado com sucesso!", toca a notificação (plano A; perfil = plano B), assiste o vídeo inteiro, confere o produto em "Ver Produtos" durante a reprodução; se o produto não aparecer em Minhas Curtidas após 1 rolagem, descurte e curte de novo. Check pós-post bloqueante.
5. Tela de compra/parcelamento aberta por engano: botão **Voltar** (nunca toques em posição fixa; toques só por bounds do dump).
6. **Uma versão (A/B/C) por produto por dia.** Ritmo 8-12 min, 08:00-22:00.
7. Parar com calma: criar o arquivo `C:\horst\tablet\PARAR`. Se existir `erro.txt`, a fila não roda até ela olhar.

A primeira execução é **um post só** (`python rodar_fila.py --um`), com ela olhando o celular. Só depois liga a fila.

## 4. Filtro de afiliados (conta secundária, celular 2)
Arquivos: `conferir_afiliados.py`, `afiliados\` (rodar_candidatos.py, vigia_conferencia.py, status_card.py, `regua_filtro.json`, `ocr.ps1`, `ligar_aparelho.cmd`, `ligar_afiliados.cmd`), `pular_afiliados.py`.

Somente leitura: não curte, não favorita, não posta. Régua em `afiliados\regua_filtro.json` (editável):
- Aprova só produto com **até 6 vídeos de criadores** e **sem vídeo vencedor** (prioridade 0-1); **7 ou mais = descarta**. (Kevin, 10/11: subiu de 4 para 6.)
- Qualquer vídeo de criador com **10 mil views ou mais** = descarta ("já tem vídeo vencedor").
- Venda na semana e pelo menos **10 vendas no total** para aprovar; menos de 10 vendas = descarta.
- Comissão mínima **R$ 20**. Exceção: se a taxa de comissão for **maior que 10%** do preço **e houver venda recente na semana**, aceita comissão menor, a partir de **R$ 15** (até R$ 15 de comissão já serve nesse caso). Valores em `comissao_min`, `comissao_min_taxa_alta`, `taxa_alta_pct` no `regua_filtro.json`.

Entradas no Drive (`Central Esposa\`): `candidatos_afiliados.json` (lista de `{itemId, link, nome, comissao_rs}` ordenada por vendas recentes), `vendas_recentes.json` (`{"itens": {"<itemId>": {...vendas total, 7 dias, 3 dias}}}`, ver `vendas_recentes()` no código) e `pular_afiliados.json` (ids já produzidos/descartados). Se ela não tiver o varredor diário (API de afiliados), ofereça criar um com a API oficial dela (credenciais só em variáveis de ambiente) ou alimentar `candidatos` por lista de links (`python conferir_afiliados.py LINKS.txt`).
Perfis em `afiliados\perfis_filtro.json` (normal = até 6 vídeos; zero_videos = aprova até 3 vídeos e separa os de 0 em `aprovados_zero_videos.csv`; `meta_aprovados` para após N aprovados); troque `perfil_ativo` ou use `ligar_perfil.cmd`. Produto não listado/indisponível/esgotado = decisão `esgotado`; "Falhou ao carregar" = tenta de novo, pula na 2ª falha.
Saída: `afiliados\conferidos.csv`, `status.json`, prints. Captcha/login: pausa e espera ela. Rodar com `afiliados\ligar_aparelho.cmd celular2`; parar com `afiliados\PARAR` (ou `PARAR_celular2`).

## 4b. Interagir curtidas (conta principal, celular 1; versão 23/11)
Arquivos: `interagir_curtidas.py`, `curtidas.cmd`. Para cada notificação de curtida / "seu vídeo alcançou N views" nos vídeos DELA: abre o vídeo pelo perfil, assiste inteiro, copia o link 1-4x e toca a foto do produto vinculado 1-4x (volta ao vídeo), com pausas aleatórias. **Nunca curte, comenta nem segue.** Modos: Misto (padrão), Só notificações, Só perfil; `--parar-apos N` (0 = sem limite).
- Defina a variável de ambiente `MEU_PERFIL` com o @ exato do perfil dela (ex. `@minha_loja`); o robô só age em vídeos cujo autor na tela seja esse.
- Os textos das telas (regex no topo do arquivo) e coordenadas de fallback são do celular do Kevin (POCO, 720x1600, Shopee em português): confira em prints da tela dela. Tela com vídeo tocando trava o uiautomator; o robô pula o item e segue (3 erros seguidos param a rodada).
- No Kevin ainda não foi validado em volume: primeiro teste com **3 itens** (`curtidas.cmd celular1 --max 3`, veja o `--help`), ela olhando o celular.
- Risco de conta: interação repetitiva pode ser vista como automação pela Shopee. Avise-a uma vez e deixe a decisão com ela.
- `destravar_fila.py/.bat`: destrava a fila de postagem (arquiva erro, tira PARAR, limpa locks mortos). `placar.py`, `calibrar_*.py`: reconhecimento do produto na lista "Adicionar produto" e calibração; só rode as calibrações com prints dela.

## 5. Assistir (conta secundária, celular 2) — versão antiga, opcional
Pasta `scripts\assistir\`. Abre o perfil dela e assiste cada vídeo do grid (15 a 32 s) passando para o próximo. **Só use quando o celular 2 não estiver no filtro nem postando.**
- Edite `assistir\layout.json`: `profile_name` = nome exibido do **perfil dela**, `search_query` = **@usuário dela** (sem arroba). No código original a busca era por outro nome; agora tudo vem desses dois campos.
- Em `phones`, troque a chave pelo serial real (`adb shell getprop ro.serialno`); `mode`: `perfil_conectado` (a conta tem perfil próprio e abre pelo ícone) ou `buscar_nome` (digita o usuário na busca da aba "Live e Vídeo"). `grade_baixa: true` se o cabeçalho do perfil for alto.
- **Recalibre** com prints do celular dela: `cells`, `oldest_cells`, `profile_icon`, `search_icon`, `live_tab`, `caption`. As coordenadas do pacote são de uma tela 720x1600 do Kevin.
- Rodar: `assistir\assistir.bat` ou `python assistir.py [fim_comeco|comeco_fim|meio_comeco|meio_fim]`. Parar: arquivo `PARAR` na pasta. Verifique `HORST_ADB` ou `platform-tools` no caminho padrão.

## 6. Central (interface local)
O pacote traz a Central pronta: `central_horst.pyw` (servidor em `127.0.0.1:8765`) + `central\ui\index.html` + `central\abrir_central.vbs`. Ela lê/escreve a pasta `Central Esposa` do Drive (letra `G:` ou outra: ajuste em `central_horst.pyw`, classe `Drive`). A sugestão por IA (Claude CLI) vem DESLIGADA (`SUGESTAO_HAIKU = False`); só ligue com ordem dela. Pode simplificar o visual a pedido dela. Se preferir criar uma própria do zero, o desenho sugerido abaixo continua valendo. Se for criar do zero, construa uma Central local para ela (HTML + pequeno servidor Python em `127.0.0.1:8765`, atalho `.vbs`/`.lnk` na área de trabalho), em português e simples. O desenho (ela escolhe o visual):
- **Painel**: status de cada robô (postagens, filtro, assistir) lido dos arquivos `rodar_fila.log`, `afiliados\status*.json`, `assistir\status\estado.json`; botões Ligar/Parar (criam/removem `PARAR`).
- **Fila / Postagens**: lista `fila.json` x `postados.json` (postados hoje, pendentes, pulados, erros com print).
- **Pendentes de aprovação**: mostra `pendentes_aprovacao.json` com o print; ela escolhe a linha certa (grava em `titulos.json`, `_aprovados`) ou recusa (vai para `pulados.json`). IA pode **sugerir**, nunca aprovar nem postar.
- **Afiliados**: aprovados/descartados do `conferidos.csv`, com motivo, e a régua editável.
- **Alertas**: captcha, login, erro, bateria. Som já existe em `alerta.py` / `sons\`.
- **Drive**: lê/escreve JSONs em `Central Esposa\` (Drive Desktop sincroniza; sem upload de vídeos grandes e sem backup constante, para não pesar a internet dela).
O iPad dela serve para acompanhar essa Central pela rede local (IP do PC:8765) ou por uma página no Drive; não roda os scripts.

## 7. Drive e arquivos
- Instale Google Drive para desktop; pastas `Central Esposa` (JSONs) e `Videos Esposa\AAAA-MM-DD\` (mp4). Nada de vídeo duplicado no PC; apague o vídeo local após post confirmado (o script já faz).
- Guarde um relatório de erros em `erros.md` e leia-o antes de mudar qualquer script.

## 8. Modo semi-manual (só iPad/iPhone, sem Android)
Os scripts não rodam. Faça: (a) a Central no PC mostra, por produto, vídeo, legenda e link; (b) ela posta à mão no app pelo iPad e marca "postado" (grava em `postados.json`); (c) o filtro de afiliados é conferido à mão seguindo a régua da seção 4, com a Central só registrando aprovados/descartados. Quando ela comprar um Android, volte às seções 2 a 5.

## 9. Ao terminar
Teste curto de cada parte, um relatório do que funcionou e do que ela precisa fazer à mão, e a lista de placeholders ainda abertos. Não tente "melhorar" travas de segurança sem ela pedir.
