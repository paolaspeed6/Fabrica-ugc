@echo off
rem Varredura diaria do Tinder (gratis, ~1h45). Agende no "Agendador de Tarefas" do Windows para as 6h.
cd /d "%~dp0"
python produto-campeao\afiliados\varrer.py >> produto-campeao\afiliados\varredura.log 2>&1
