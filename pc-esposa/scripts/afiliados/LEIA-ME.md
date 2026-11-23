# Afiliados (filtro automático)

Robô que confere produtos Shopee no tablet e conta os vídeos de afiliados.

| O quê | Onde |
|---|---|
| Script | `C:\horst\tablet\conferir_afiliados.py` |
| Resultado | `conferidos.csv` (abre no Excel; separador `;`) |
| Status para a Central | `status.json` (card "Afiliados (filtro automático)") |
| Log | `conferir_afiliados.log` |
| Prints de cada produto | `prints\` |
| Prints do mapeamento das telas | `prints\mapeamento\` |
| Tentativas de teste antigas | `testes\` |
| Gravação da demonstração manual | `demo\` (toques.txt + prints) |
| OCR do Windows | `ocr.ps1` |
| Parar entre produtos | criar o arquivo `PARAR` aqui |

Uso: `python conferir_afiliados.py LINKS.txt` (um link por linha), ou `--teste` (3 produtos já postados).
Não roda se a fila de postagem estiver rodando (é o mesmo tablet).

Regra do Kevin para bugs: **fechar e abrir de novo o app Shopee** (resolveu na prática em 05/11).
O robô faz isso sozinho: falhou um produto → `am force-stop com.shopee.br` → tenta de novo (máx. 2 tentativas, depois registra erro e segue).

Decisão (antiga, ver régua nova no script `decidir()`): vendas < 5 → descarta · 0 vídeos → aprovado_forte · até 10 → aprovado ·
11-15 → revisar · > 15 → descarta. A comissão é só registrada.

Situação (05/11 03:40): telas mapeadas, a contagem de vídeos funciona (Pétala = 11, conferido).
Falta deixar estável a passagem da página leve para a completa: o robô vai ser corrigido a partir da demonstração do Kevin.
