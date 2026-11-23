# OCR do Windows (Windows.Media.Ocr, já vem no Windows). Uso: ocr.ps1 imagem.png
# Saída: uma linha por palavra: texto<TAB>x<TAB>y<TAB>largura<TAB>altura<TAB>nº da linha
param([string]$img)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType = WindowsRuntime]
$null = [Windows.Globalization.Language, Windows.Globalization, ContentType = WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Esperar($op, [Type]$t) {
    $task = $asTask.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait(-1) | Out-Null; $task.Result }
$file = Esperar ([Windows.Storage.StorageFile]::GetFileFromPathAsync($img)) ([Windows.Storage.StorageFile])
$stream = Esperar ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$dec = Esperar ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bmp = Esperar ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
$lang = [Windows.Globalization.Language]::new('pt-BR')
$eng = if ([Windows.Media.Ocr.OcrEngine]::IsLanguageSupported($lang)) { [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang) } else { [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages() }
$res = Esperar ($eng.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
$n = 0
foreach ($l in $res.Lines) {
    foreach ($w in $l.Words) { $r = $w.BoundingRect; "{0}`t{1}`t{2}`t{3}`t{4}`t{5}" -f $w.Text, [int]$r.X, [int]$r.Y, [int]$r.Width, [int]$r.Height, $n }
    $n++
}
