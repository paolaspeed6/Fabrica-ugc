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
- [ABERTO] 2026-11-23 fábrica (substituído pelo de baixo): atualizar a Central do PC → `git pull`, copiar `pc-esposa/scripts/ponte_esposa.py` e `pc-esposa/scripts/central/ui/esposa.html` para `C:\horst\tablet\` (mesmos subcaminhos), fechar e abrir a Central. Novidade: painel da fábrica (gasto de IA do mês, vídeos feitos, última busca, lotes) lido de `Central Esposa\painel.json`.
- [ABERTO] 2026-11-23 fábrica: ATUALIZAÇÃO COMPLETA da Central → `git pull`; copiar por cima para `C:\horst\tablet\` (mesmos subcaminhos): `ponte_esposa.py`, `central_horst.pyw`, `central\ui\esposa.html`, `pular_afiliados.py`, `rodar_fila.py`, `conferir_afiliados.py`, `afiliados\ponte_candidatos.py`, `afiliados\rodar_candidatos.py` (NÃO copiar aparelhos.json, assistir\layout.json, fila.json, postados.json: são os dados dela). Depois fechar a Central (encerrar o pythonw.exe do central_horst) e abrir pelo atalho. Conferir: abas Central (gasto, desperdício, lotes), ⚠ Aprovar, ⚙ Ajustes (filtro, postagem, assistir, serial do celular). Rodar `C:\horst\tablet\platform-tools\adb.exe devices`: se o POCO estiver "device", gravar o serial na aba Ajustes › Celular. Responder aqui o resultado e dar push.
- [ABERTO] 2026-11-23 fábrica: tirei o botão "Painel completo (avançado)" da Central dela (abria a Central do Kevin; ela não quer). Copie de novo `central\ui\esposa.html` para `C:\horst\tablet\central\ui\` e recarregue a Central.
