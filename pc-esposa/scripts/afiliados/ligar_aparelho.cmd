@echo off
rem Liga o filtro de afiliados em um aparelho: ligar_aparelho.cmd celular1  (ou celular2)
rem Parar so um aparelho: criar afiliados\PARAR_celular1 ou PARAR_celular2. afiliados\PARAR para os dois.
rem Saida do robo por aparelho: afiliados\rodar_candidatos_celular1.out / _celular2.out (ligar_afiliados.cmd)
rem PC Paola 23/11: a Central manda HORST_ADB_SERIAL (aparelhos.json); so usa o padrao se rodar na mao.
if /i not "%~1"=="celular1" if /i not "%~1"=="celular2" (
  echo Use: ligar_aparelho.cmd celular1 ou celular2
  exit /b 1
)
if not defined HORST_ADB_SERIAL if /i "%~1"=="celular1" set "HORST_ADB_SERIAL=<IP_DO_CELULAR1>:5555"
if not defined HORST_ADB_SERIAL if /i "%~1"=="celular2" set "HORST_ADB_SERIAL=<SERIAL_CELULAR2>"
set HORST_ID=%~1
if exist C:\horst\tablet\afiliados\PARAR_%~1 del /q C:\horst\tablet\afiliados\PARAR_%~1
call C:\horst\tablet\afiliados\ligar_afiliados.cmd
