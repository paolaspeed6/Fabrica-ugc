@echo off
rem Liga o filtro num aparelho com um perfil de perfis_filtro.json: ligar_perfil.cmd celular1 zero_videos
rem Sem perfil: usa o "perfil_ativo" do perfis_filtro.json.
if not "%~2"=="" set HORST_PERFIL=%~2
call C:\horst\tablet\afiliados\ligar_aparelho.cmd %~1
