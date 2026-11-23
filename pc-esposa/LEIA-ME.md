# Pacote de robôs Shopee (versão 23/11/2026)

Automações para **PC Windows + celular Android (adb)**:

| Parte | Arquivos | Conta / celular |
|---|---|---|
| Postar vídeos da fila | `rodar_fila.py`, `postar_shopee.py`, `pendentes.py`, `placar.py` | conta principal, celular 1 |
| Filtro de afiliados (só leitura) | `conferir_afiliados.py`, `afiliados\` | conta secundária, celular 2 |
| Interagir curtidas | `interagir_curtidas.py`, `curtidas.cmd` | conta principal |
| Assistir (versão antiga, opcional) | `assistir\` | conta secundária |
| Central (painel local 127.0.0.1:8765) | `central_horst.pyw`, `central\` | PC |

## Como usar
1. Abra o Claude numa pasta vazia no PC, descompacte este zip dentro e diga: **"Leia INSTRUCOES_PARA_CLAUDE.md e monte tudo."**
2. O Claude pergunta nome do perfil, @usuário, celulares e pasta do Drive e faz o resto.
3. Captcha e login são resolvidos **à mão**: os scripts nunca fazem isso.

## Requisitos
PC Windows, Python 3.12, adb (platform-tools), Google Drive para desktop, e **pelo menos 1 celular Android**. iPad/iPhone não rodam os scripts (há modo semi-manual nas instruções).

## Segurança
Sem chaves, tokens, links de afiliado, seriais, IPs ou dados de vendas. Tudo que é pessoal é placeholder `<...>`. Não suba para repositório público.
