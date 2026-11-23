' Abre a Central Horst (servidor + janela). Se o servidor ja estiver rodando, so abre a janela.
' Atalhos "Central Horst" apontam para este arquivo (Iniciar em = esta pasta).
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "C:\horst\tablet\central"
sh.Run """%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe"" ""C:\horst\tablet\central_horst.pyw""", 0, False
