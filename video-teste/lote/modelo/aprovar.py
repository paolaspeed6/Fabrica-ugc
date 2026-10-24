"""pNN-cenas/fiscal_video.json -> pNN-cenas/aprovado.json para o montar.py. Cena com "inicio" > 0 vira X_ini.mp4 (cortada por ffmpeg).
Cena reprovada (fim < 2,0 s ou sem clipe) usa a cena aprovada mais longa do mesmo produto. uso: python3 -I aprovar.py p01 p02 ..."""
import json, re, subprocess, sys
from pathlib import Path
B = Path(__file__).resolve().parent
for k in sys.argv[1:]:
    d = B / f'{k}-cenas'; fv = json.loads((d / 'fiscal_video.json').read_text()) if (d / 'fiscal_video.json').exists() else {}
    seg = {}
    for c in 'ABC':
        v = fv.get(c); mp4 = d / f'{c}_fixa.mp4' if (d / f'{c}_fixa.mp4').exists() else d / f'{c}.mp4'
        if not v or not mp4.exists(): continue
        fim = float(v.get('fim') or 0); ini = float(v.get('inicio') or 0)
        if not fim:
            m = re.search(r'usar\s+([\d.]+)\s*-\s*([\d.]+)', v.get('veredito', ''))
            if m: ini, fim = float(m.group(1)), float(m.group(2))
        if fim - ini < 1.5: continue
        if ini > 0:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ini), '-i', str(mp4), '-an', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', str(d / f'{c}_ini.mp4')], check=True)
        seg[c] = round(min(fim - ini, 5.0), 2)
    if not seg: print(k, 'SEM CENA APROVADA'); continue
    melhor = max(seg, key=seg.get)
    ok = {c: seg.get(c, melhor) for c in 'ABC'}
    (d / 'aprovado.json').write_text(json.dumps(ok)); print(k, ok)
