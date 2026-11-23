# Central Aguiiar Lar no seu PC (23/11/2026)

Tudo roda no seu PC, sem o Claude. Só a criação dos vídeos (IA) acontece na fábrica, na nuvem, e começa sozinha quando você dá a ordem.

## O caminho de cada produto (tudo automático)
1. **Busca** (nuvem, 05:41 e 16:41): manda os produtos novos para o Drive (`Central Esposa\candidatos-...json`).
2. **Filtro** (robô no celular, conta que já está conectada): confere vídeos, vendas e comissão pela régua (`afiliados\regua_filtro.json`).
3. **Produção** (aba da Central): o que o filtro aprova entra sozinho na fila. Você toca **Iniciar produção** (máx. 15, teto em dólar aparece no botão) = sua ordem.
4. **Fábrica** (nuvem) produz e entrega na aba **Conferir**.
5. **Conferir**: você assiste e toca **Ok** → entra sozinho na **Fila de postagem**.
6. **Postagem** (robô, conta NOVA): posta 1 por produto por dia, 8-12 min entre posts, 08h-22h.
7. Postou → sai sozinho da fila e da Conferência → aparece em **Postados** e a fábrica fica sabendo.

## Sem repetidos
- A busca tira os produtos que o Kevin já pegou e os que você já viu, e manda os seus para ele.
- O filtro pula os já produzidos, os do Kevin e os descartados (`Central Esposa\pular_afiliados.json`, a nuvem atualiza).

## Limpeza automática (1x por dia)
- Vídeos no Drive: apagados 2 dias depois de postados, e os recusados ou as versões que você não escolheu (vão para a lixeira do Drive).
- Prints de tela com mais de 15 dias; cópias de segurança com mais de 7 dias; fichas da Conferência já resolvidas com mais de 30 dias.
- Nunca apaga a fila, os postados, as suas decisões ou um vídeo ainda não postado.

## Instalar (1 vez)
1. Instale o **Google Drive para desktop** e entre na sua conta (a pasta `Central Esposa` já foi criada).
2. Instale o **Python 3.12** (python.org) e baixe o **adb** (SDK Platform-Tools) em `C:\horst\tablet\platform-tools`.
3. Descompacte este pacote e dê 2 cliques em `scripts\instalar.cmd`.
4. No celular: Depuração USB ligada (+ "Depuração USB (Configurações de segurança)" no POCO) e o cabo no PC.
5. Preencha o `C:\horst\tablet\aparelhos.json` com o serial do celular (`adb devices` mostra).
6. Abra **Central Aguiiar Lar** na área de trabalho.

## Robôs
- **Postagem**: só na conta nova. Se o celular for o mesmo do filtro, troque a conta à mão no app antes de ligar (o robô nunca faz login).
- **Filtro**: na conta que já está conectada. Só olha, não curte nem posta.
- **Assistir meus vídeos**: só assiste os seus vídeos (edite `assistir\layout.json` com o nome e o @ do seu perfil).
- Um robô por vez no celular. Captcha ou login: o robô para e apita; você resolve com a mão.
- Primeiro teste da postagem: 1 post só, olhando o celular (`rodar_fila.py --um`).

O painel completo do Kevin continua em `http://127.0.0.1:8765/kevin` (avançado).
