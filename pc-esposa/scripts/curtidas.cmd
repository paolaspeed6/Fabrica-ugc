@echo off
rem Liga o robo de curtidas num aparelho: curtidas.cmd celular1  (ou celular2)
rem A Central chama com HORST_ADB_SERIAL ja definido. Parar: criar PARAR_curtidas (todos) ou PARAR_curtidas_celular1.
cd /d C:\horst\tablet
set PYTHONPATH=C:\horst\tablet\pylibs
set PYTHONIOENCODING=utf-8
rem A Central ja manda HORST_ADB_SERIAL; o argumento so vale quando rodar na mao
if not defined HORST_ADB_SERIAL if /i "%~1"=="celular2" set HORST_ADB_SERIAL=<SERIAL_CELULAR2>
if not defined HORST_ADB_SERIAL set HORST_ADB_SERIAL=<IP_DO_CELULAR1>:5555
if exist PARAR_curtidas del /q PARAR_curtidas
if /i "%~1"=="celular1" if exist PARAR_curtidas_celular1 del /q PARAR_curtidas_celular1
if /i "%~1"=="celular2" if exist PARAR_curtidas_celular2 del /q PARAR_curtidas_celular2
echo %HORST_ADB_SERIAL% | find ":" >nul && C:\horst\tablet\platform-tools\adb.exe connect %HORST_ADB_SERIAL% >nul 2>&1
if not exist curtidas mkdir curtidas
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -X utf8 interagir_curtidas.py %2 %3 %4 %5 %6 >> curtidas\saida.out 2>&1
