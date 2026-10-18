"""Decisão do fiscal por cena, depois de ver sNN-cenas/pruna/conferencia.jpg.
Uso: python3 aprovar.py sNN K ok|codigo|<segundos>
  ok        mantém o clipe (primeiros 5,4 s do bruto)
  codigo    reprova o Pruna: apaga o clipe e marca "pruna_reprovado" (fazer_lista faz zoom por código na foto real)
  <seg>     usa só os primeiros <seg> s do bruto (antes de a câmera avançar demais), esticados para 5,4 s com interpolação
"""
import json, subprocess, sys
from pathlib import Path
L = Path(__file__).resolve().parent.parent / "lote" / "lista1017"
s, k, dec = sys.argv[1], int(sys.argv[2]), sys.argv[3]
js = L / f"{s}.json"; p = json.loads(js.read_text(encoding="utf-8")); c = p["cenas"][k - 1]
dst = L / c["clipe"]; raw = L / f"{s}-cenas" / "pruna" / f"cena{k}_raw.mp4"
if dec == "codigo":
    dst.unlink(missing_ok=True); c["pruna_reprovado"] = c.get("pruna"); c["pruna"] = None
elif dec != "ok":
    t = float(dec); f = 5.6 / t
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0", str(raw)], capture_output=True, text=True).stdout.strip().split(","))
    kk = 1080 / max(w, h); W, H = int(w * kk) // 2 * 2, int(h * kk) // 2 * 2
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(t), "-i", str(raw), "-an", "-vf",
                    f"setpts={f:.4f}*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,scale={W}:{H}:flags=lanczos",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)],
                   check=True, stdin=subprocess.DEVNULL)
    c["pruna_t"] = t
c["fiscal"] = dec
js.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
print(s, k, dec)
