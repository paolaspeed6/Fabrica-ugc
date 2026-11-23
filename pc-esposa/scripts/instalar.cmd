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
rem Paola 23/11: os robos procuram o Python na pasta Python312; se ela instalou outra versao (3.13, 3.14...),
rem cria um atalho de pasta (juncao) com esse nome apontando para a versao instalada. Nao precisa de administrador.
set PYBASE=%LOCALAPPDATA%\Programs\Python
if not exist "%PYBASE%\Python312\pythonw.exe" (
  rem 1o: pergunta ao proprio Python onde ele esta (serve para qualquer instalacao: python.org, gerenciador novo, Store)
  for %%C in (py python) do (
    if not exist "%PYBASE%\Python312\pythonw.exe" (
      for /f "delims=" %%D in ('%%C -c "import sys;print(sys.base_prefix)" 2^>nul') do (
        if exist "%%D\pythonw.exe" (
          if not exist "%PYBASE%" mkdir "%PYBASE%"
          if exist "%PYBASE%\Python312" rmdir "%PYBASE%\Python312" 2>nul
          mklink /J "%PYBASE%\Python312" "%%D" >nul && echo Python encontrado: %%D
        )
      )
    )
  )
  for /f "delims=" %%P in ('dir /b /ad /o-n "%PYBASE%\Python3*" 2^>nul') do (
    if not exist "%PYBASE%\Python312\pythonw.exe" if exist "%PYBASE%\%%P\pythonw.exe" (
      if exist "%PYBASE%\Python312" rmdir "%PYBASE%\Python312" 2>nul
      mklink /J "%PYBASE%\Python312" "%PYBASE%\%%P" >nul && echo Python encontrado: %%P
    )
  )
)
if not exist "C:\horst\python\python.exe" if exist "%PYBASE%\Python312\python.exe" mklink /J "C:\horst\python" "%PYBASE%\Python312" >nul
if not exist "%PYBASE%\Python312\pythonw.exe" (
  echo.
  echo FALTA o Python: baixe em python.org, instale e rode este arquivo de novo.
) else (
  echo Instalando as bibliotecas dos robos ^(pode levar uns minutos^)...
  "%PYBASE%\Python312\python.exe" -m pip install --quiet --upgrade pillow numpy opencv-python
)
if not exist "%DEST%\platform-tools\adb.exe" (
  echo FALTA o adb: baixe "SDK Platform-Tools for Windows" e descompacte em %DEST%\platform-tools
)
echo.
echo Pronto. Abra "Central Aguiiar Lar" na area de trabalho.
pause
