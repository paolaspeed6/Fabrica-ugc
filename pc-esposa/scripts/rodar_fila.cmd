@echo off
cd /d C:\horst\tablet
rem numpy e Pillow estao na pasta virtual do app Claude; fora dele o Python nao as enxerga
set PYTHONPATH=C:\horst\tablet\pylibs
rem ..........................................................................
set PYTHONIOENCODING=utf-8
rem Kevin 05/11: tablet aposentado; a fila roda no Celular 1 (a Central pode passar outro aparelho)
if not defined HORST_ADB_SERIAL set HORST_ADB_SERIAL=<IP_DO_CELULAR1>:5555
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" rodar_fila.py --seguido --ignorar-horario
echo.
echo ===== A fila parou. Veja C:\horst\tablet\erro.txt e rodar_fila.log =====
pause
