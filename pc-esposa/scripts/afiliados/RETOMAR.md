# Filtro de afiliados: onde estamos e como retomar (atualizado 20/11 12:40)

O progresso fica salvo sozinho em `conferidos.csv` (1 linha por produto conferido). Parar e religar não perde nada:
o robô pula tudo que já tem resultado (menos "erro", que é reconferido).

## Agora
- Fila: `afiliados\fila_filtro.json` (3.811 produtos, buscas de 10, 15, 17 e 19/11 + restos). Faltam ~2.877.
- Rodando: Poco azul (celular1) desde 20/11 12:33. Poco verde (celular2) fora do adb (plugar no PC).
- Régua (`regua_filtro.json`): até 6 vídeos; prioridade 0-1; vídeo com 10 mil+ views = descarta;
  comissão mínima R$ 20 (R$ 15 se taxa > 10% e venda na semana); "não listado/indisponível/esgotado" = esgotado.

## Religar
- Um aparelho: `C:\horst\tablet\afiliados\ligar_aparelho.cmd celular1` (ou `celular2`) — ou o botão da Central.
- Vigia (religa sozinho quem cair): apagar `afiliados\VIGIA_PARAR` e rodar
  `%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe C:\horst\tablet\afiliados\vigia_conferencia.py`
- Parar um aparelho: criar `afiliados\PARAR_celular1` / `PARAR_celular2`. Os dois: `afiliados\PARAR`.
