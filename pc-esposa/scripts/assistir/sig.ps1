param(
  [string]$Image,
  [int]$X = 8,
  [int]$Y = 1268,
  [int]$W = 560,
  [int]$H = 60,
  [int]$WX = -1,
  [int]$WY = 0,
  [int]$WW = 0,
  [int]$WH = 0
)
Add-Type -AssemblyName System.Drawing
$b = [System.Drawing.Bitmap]::FromFile($Image)
$x = $X; $y = $Y; $w = $W; $h = $H
if ($y + $h -gt $b.Height) { $y = [Math]::Max(0, $b.Height - $h - 1) }
$hash = 17
for ($yy = $y; $yy -lt ($y + $h); $yy += 8) {
  for ($xx = $x; $xx -lt ([Math]::Min($x + $w, $b.Width)); $xx += 8) {
    $p = $b.GetPixel($xx, $yy)
    $hash = (($hash * 33) -bxor $p.ToArgb()) -band 2147483647
  }
}
$branco = -1
if ($WX -ge 0 -and $WH -gt 0) {
  $total = 0
  $claros = 0
  $y2 = [Math]::Min($WY + $WH, $b.Height)
  $x2 = [Math]::Min($WX + $WW, $b.Width)
  for ($yy = $WY; $yy -lt $y2; $yy += 12) {
    for ($xx = $WX; $xx -lt $x2; $xx += 12) {
      $p = $b.GetPixel($xx, $yy)
      $total++
      if ($p.R -gt 242 -and $p.G -gt 242 -and $p.B -gt 242) { $claros++ }
    }
  }
  if ($total -gt 0) {
    $branco = [Math]::Round($claros / $total, 3).ToString([System.Globalization.CultureInfo]::InvariantCulture)
  }
}
$b.Dispose()
Write-Output $hash
Write-Output $branco
