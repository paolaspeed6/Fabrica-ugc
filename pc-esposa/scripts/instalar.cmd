@echo off
rem Instala a Central Aguiiar Lar em C:\horst\tablet e cria o atalho na area de trabalho.
rem Rode com 2 cliques DENTRO da pasta "scripts" descompactada.
setlocal
set DEST=C:\horst\tablet
if not exist "%DEST%" mkdir "%DEST%"
echo Copiando arquivos para %DEST% ...
robocopy "%~dp0." "%DEST%" /E /XO /XF instalar.cmd aparelhos.json fila.json postados.json /NFL /NDL /NJH /NJS >nul
if not exist "%DEST%\aparelhos.json" copy "%~dp0aparelhos.json" "%DEST%\aparelhos.json" >nul
if not exist "%DEST%\esposa" mkdir "%DEST%\esposa"
if not exist "%DEST%\filas" mkdir "%DEST%\filas"
if not exist "%DEST%\fila.json" echo []> "%DEST%\fila.json"
if not exist "%DEST%\postados.json" echo []> "%DEST%\postados.json"
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Central Aguiiar Lar.lnk');$s.TargetPath='C:\horst\tablet\central\abrir_central.vbs';$s.WorkingDirectory='C:\horst\tablet\central';$s.Save()"
if not exist "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" (
  echo.
  echo FALTA o Python 3.12: baixe em python.org, instale "so para mim" e rode este arquivo de novo.
)
if not exist "%DEST%\platform-tools\adb.exe" (
  echo FALTA o adb: baixe "SDK Platform-Tools for Windows" e descompacte em %DEST%\platform-tools
)
echo.
echo Pronto. Abra "Central Aguiiar Lar" na area de trabalho.
pause
