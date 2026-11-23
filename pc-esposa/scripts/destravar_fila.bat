@echo off
chcp 65001 >nul
cd /d C:\horst\tablet
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   DESTRAVAR A FILA DE POSTAGEM  (nao depende da Central)
echo ============================================================
echo.
echo Qual celular vai postar?
echo   A = Poco azul   (padrao: so aperte Enter)
echo   V = Poco verde
set /p ESC="Escolha [A/V]: "
set ALVO=azul
if /i "%ESC%"=="V" set ALVO=verde
echo.
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" destravar_fila.py %ALVO%
echo.
echo Pronto. Pode fechar esta janela.
pause
