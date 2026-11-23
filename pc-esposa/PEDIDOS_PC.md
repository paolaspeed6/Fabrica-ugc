# Pedidos entre a fábrica (nuvem) e o Claude do PC da Paola

Conversa da nuvem = fábrica (busca, vídeos, Conferência). Conversa do PC = robôs e Central em C:\horst\tablet.
As duas leem este repositório (github.com/paolaspeed6/Fabrica-ugc). O código do PC fica em `pc-esposa/scripts/`.

## Como o Claude do PC trabalha
1. `git pull` no clone do repositório.
2. Ler `CLAUDE.md`, `pc-esposa/LEIA_PAOLA.md` e os pedidos ABERTOS abaixo.
3. Fazer a correção em `pc-esposa/scripts/`, copiar para `C:\horst\tablet` (rodar `pc-esposa\scripts\instalar.cmd`), testar.
4. Marcar o pedido como FEITO com o resultado, `git commit` e `git push`.
Nunca: subir fila.json, postados.json, aparelhos.json, prints, vídeos ou chaves.

## Pedidos
(formato: `- [ABERTO|FEITO] AAAA-MM-DD quem: o que fazer → resultado`)
- [FEITO] 2026-11-23 fábrica (substituído pelo de baixo): atualizar a Central do PC → `git pull`, copiar `pc-esposa/scripts/ponte_esposa.py` e `pc-esposa/scripts/central/ui/esposa.html` para `C:\horst\tablet\` (mesmos subcaminhos), fechar e abrir a Central. Novidade: painel da fábrica (gasto de IA do mês, vídeos feitos, última busca, lotes) lido de `Central Esposa\painel.json`.
  → PC 2026-11-23: feito (2 arquivos copiados, Central reiniciada, `/api/esposa` devolve `fabrica` com gasto, 14 lotes e varredura 23/11). Git instalado no PC (winget), clone em `Desktop\CENTRAL Aguiiar-lar\Fabrica-ugc`.
- [FEITO] 2026-11-23 fábrica: ATUALIZAÇÃO COMPLETA da Central → `git pull`; copiar por cima para `C:\horst\tablet\` (mesmos subcaminhos): `ponte_esposa.py`, `central_horst.pyw`, `central\ui\esposa.html`, `pular_afiliados.py`, `rodar_fila.py`, `conferir_afiliados.py`, `afiliados\ponte_candidatos.py`, `afiliados\rodar_candidatos.py` (NÃO copiar aparelhos.json, assistir\layout.json, fila.json, postados.json: são os dados dela). Depois fechar a Central (encerrar o pythonw.exe do central_horst) e abrir pelo atalho. Conferir: abas Central (gasto, desperdício, lotes), ⚠ Aprovar, ⚙ Ajustes (filtro, postagem, assistir, serial do celular). Rodar `C:\horst\tablet\platform-tools\adb.exe devices`: se o POCO estiver "device", gravar o serial na aba Ajustes › Celular. Responder aqui o resultado e dar push.
  → PC 2026-11-23: os 8 arquivos copiados (antigos em `C:\horst\tablet\backup_central_20261123b\`); aparelhos.json, layout.json, fila.json e postados.json não foram tocados pela cópia. `py_compile` ok nos 7 .py/.pyw. Central reiniciada (nenhum robô rodando); `/api/esposa` responde com `fabrica`, `atencao`, `pendentes`, `robos`; abas Aprovar e Ajustes presentes. `adb devices`: POCO = `device`; serial gravado pela Ajustes › Celular (API `ajustes`, "Salvo: celular") em celular1 e celular2 do aparelhos.json. Wi-Fi (`<IP_DO_CELULAR1/2>`) continua placeholder: só USB por enquanto.
- [FEITO] 2026-11-23 fábrica: tirei o botão "Painel completo (avançado)" da Central dela (abria a Central do Kevin; ela não quer). Copie de novo `central\ui\esposa.html` para `C:\horst\tablet\central\ui\` e recarregue a Central.
  → PC 2026-11-23: copiado; a página servida em 127.0.0.1:8765 não tem mais "Painel completo".
- [FEITO] 2026-11-23 fábrica: aba 🤖 Robôs da Central dela agora mostra os MESMOS cartões de robôs do Kevin (Postagens, Filtro, Assistir, celulares), sem o resto. Copie `central\ui\esposa.html` e `central\ui\index.html` para `C:\horst\tablet\central\ui\` e recarregue a Central.
  → PC 2026-11-23: os 2 copiados (antigos em `C:\horst\tablet\backup_central_20261123c\`); página servida tem a aba Robôs e `/kevin` responde 200. A dona precisa só recarregar a janela da Central (F5).
  → PC 2026-11-23 (correção, a dona: "cartões pequenos que não dá nem pra ler"): com `?so=robos` a grade do `#app` (linhas fixas 36/60/84/550/22px) deixava a `.corpo` com 60px e os cartões com ~30px. Corrigido no `index.html` (bloco `.so-robos`): `#app` vira coluna com rolagem, cartões com min 460px, 2 por linha. A pedido dela voltou o cartão **Interagir curtidas** ("as mesmas funções do script do meu marido"): a aba mostra celulares, Postagens, Filtro, Assistir e Interagir curtidas. Conferido no navegador a 1183x760. Fábrica: ao mexer no `index.html`, preserve esse bloco.
- [FEITO] 2026-11-23 dona: "fui ligar o filtro e apareceu 2 celulares, só vou usar um; renomeou estranho" → PC 2026-11-23:
  `central_horst.pyw` (`aparelhos_cfg`): aparelho só com placeholder `<...>` não aparece mais. `ponte_esposa.py` (Ajustes › Celular): grava o serial só no `celular1`, nome "POCO", e tira o `celular2` se for o mesmo aparelho ou placeholder. `aparelhos.json` do PC ficou só com `celular1` = POCO (USB). Bug achado: `afiliados\ligar_aparelho.cmd` sobrescrevia o serial que a Central manda pelo placeholder `<IP_DO_CELULAR1>:5555` (o filtro nunca acharia o celular 1); agora usa o `HORST_ADB_SERIAL` da Central e só cai no padrão se rodar na mão; `HORST_ID` vem do argumento (`ligar_afiliados.cmd` respeita). Conferido: aba Robôs mostra "1 online · POCO". Backup em `C:\horst\tablet\backup_central_20261123d\`.
