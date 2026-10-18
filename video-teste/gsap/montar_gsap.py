"""Monta um vídeo com a camada de texto animada em GSAP.
Uso: python3 gsap/montar_gsap.py <montagem.json> [saida.mp4]
1) montar_video_pro.py faz o fundo (cenas, degradê, vidro) sem texto;
2) render.js anima o texto da mesma montagem quadro a quadro em Chromium;
3) o ffmpeg sobrepõe a camada transparente. Nada é gerado por IA: custo zero."""
import json, subprocess, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import montar_video_pro as mvp

arq = Path(sys.argv[1]).resolve()
m = json.loads(arq.read_text(encoding="utf-8"))
est = mvp.ESTILOS[m.get("estilo", "shopee")]
cor = m.get("cor_destaque", "auto")
if cor == "auto":
    cor = mvp.PALETA[sum(map(ord, m["nome"])) % len(mvp.PALETA)]
saida = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else arq.parent / f"{m['nome']}_gsap.mp4"

# mesmos inícios de cena que o montar_video_pro (transição de XF segundos)
xf, inicios, t = est["xf"], [], 0.0
for i, c in enumerate(m["cenas"]):
    inicios.append(max(0.0, t - (xf if i else 0)))
    t = (t - xf + c["ate"]) if i else c["ate"]
fins = [inicios[i + 1] + xf / 2 for i in range(len(inicios) - 1)] + [t]

with tempfile.TemporaryDirectory(dir=arq.parent) as tmp:
    tmp = Path(tmp)
    base_json = tmp / "base.json"
    base_json.write_text(json.dumps({**m, "nome": "base", "sem_texto": True, "cenas": [
        {**c, "clipe": str((arq.parent / c["clipe"]).resolve())} for c in m["cenas"]]}, ensure_ascii=False))
    subprocess.run([sys.executable, str(AQUI.parent / "montar_video_pro.py"), str(base_json)], check=True)
    dados = tmp / "dados.json"
    dados.write_text(json.dumps({"cor": cor, "total": len(m["cenas"]), "fim": t, "selo": m.get("selo"), "inclina": m.get("inclina"), "ordem": m.get("ordem"), "alinha": m.get("alinha"), "cenas": [
        {k: c.get(k) for k in ("rotulo", "titulo", "fichas", "cta", "abertura", "sub", "selo")} | {"ini": ini, "fim": fim}
        for c, ini, fim in zip(m["cenas"], inicios, fins)]}, ensure_ascii=False))
    camada = tmp / "camada.mov"
    subprocess.run(["node", str(AQUI / "render.js"), str(AQUI / f"camada_{m.get('estilo', 'shopee')}.html"),
                    str(dados), str(camada), str(mvp.FPS)], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp / "base.mp4"), "-i", str(camada),
                    "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]", "-map", "[v]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-r", str(mvp.FPS),
                    "-movflags", "+faststart", str(saida)], check=True)
print(f"Pronto: {saida}")
