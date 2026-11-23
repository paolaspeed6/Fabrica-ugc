@echo off
cd /d C:\horst\tablet
if not defined HORST_ADB_SERIAL set HORST_ADB_SERIAL=<IP_DO_CELULAR1>:5555
if not defined HORST_ID if "%HORST_ADB_SERIAL%"=="<SERIAL_CELULAR2>" (set HORST_ID=celular2) else set HORST_ID=celular1
if not defined HORST_ID set HORST_ID=celular1
set PYTHONPATH=C:\horst\tablet\pylibs
set HORST_INTERVALO=0
if exist afiliados\PARAR del /q afiliados\PARAR
echo %HORST_ADB_SERIAL% | find ":" >nul && C:\horst\tablet\platform-tools\adb.exe connect %HORST_ADB_SERIAL% >nul 2>&1
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" afiliados\rodar_candidatos.py >> afiliados\rodar_candidatos_%HORST_ID%.out 2>&1
