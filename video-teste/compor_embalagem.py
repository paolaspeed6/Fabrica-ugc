"""Cola a embalagem REAL do anúncio (recorte da foto) sobre uma cena gerada com câmera parada
e aplica o movimento de câmera por código na imagem inteira, para a embalagem andar junto com a cena.
Regra da dona (2026-10-15): letras de embalagem nunca são redesenhadas pela IA.

"sobrepor" na cena do produto.json:
  {"foto": "p11-fotos/04.jpg", "recorte": [450, 180, 940, 860],   # caixa da embalagem na foto (px)
   "x": 0.72, "base": 0.62, "altura": 0.30}                        # centro x, linha do chão e altura (fração do quadro)
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def recortar(foto, caixa, limite=236):
    """Tira o fundo branco ligado às bordas do recorte (flood fill), mantendo brancos internos."""
    im = Image.open(foto).convert("RGB").crop(caixa)
    w, h = im.size
    claro = Image.new("L", (w, h), 0)
    px, cl = im.load(), claro.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            cl[x, y] = 255 if min(r, g, b) >= limite else 0
    fundo = claro.copy()
    for semente in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if fundo.getpixel(semente) == 255:
            ImageDraw.floodfill(fundo, semente, 128)
    alfa = fundo.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA")
    out.putalpha(alfa)
    return out.crop(alfa.getbbox())


def camada(cfg, base, larg, alt, arq):
    emb = recortar(base / cfg["foto"], cfg["recorte"])
    eh = int(alt * cfg["altura"])
    emb = emb.resize((int(emb.width * eh / emb.height), eh), Image.LANCZOS)
    tela = Image.new("RGBA", (larg, alt), (0, 0, 0, 0))
    cx, chao = int(larg * cfg["x"]), int(alt * cfg["base"])
    sombra = Image.new("L", (larg, alt), 0)
    ImageDraw.Draw(sombra).ellipse((cx - emb.width * 0.62, chao - 16, cx + emb.width * 0.62, chao + 22), fill=150)
    sombra = sombra.filter(ImageFilter.GaussianBlur(14))
    tela.paste(Image.new("RGBA", (larg, alt), (20, 15, 10, 255)), (0, 0), sombra)
    tela.alpha_composite(emb, (cx - emb.width // 2, chao - emb.height))
    tela.save(arq)


def compor(clipe, cfg, base, saida):
    """Rastreia o movimento do chão/cenário (fluxo óptico) e move a embalagem junto, quadro a quadro.
    Assim ela fica "apoiada" no chão mesmo quando o modelo mexe a câmera."""
    import cv2
    import numpy as np
    cap = cv2.VideoCapture(str(clipe))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    ok, q0 = cap.read()
    h, w = q0.shape[:2]
    png = Path(saida).with_suffix(".camada.png")
    camada(cfg, base, w, h, png)
    lay = cv2.imread(str(png), cv2.IMREAD_UNCHANGED).astype(np.float32)
    png.unlink()
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                           "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-t", "5", "-an", "-c:v", "libx264",
                           "-crf", "16", "-pix_fmt", "yuv420p", str(saida)], stdin=subprocess.PIPE)
    M = np.eye(3)
    ant = cv2.cvtColor(q0, cv2.COLOR_BGR2GRAY)
    q = q0
    while True:
        A = M[:2]
        cam = cv2.warpAffine(lay, A, (w, h), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        a = cam[:, :, 3:4] / 255.0
        out = (q.astype(np.float32) * (1 - a) + cam[:, :, :3] * a).clip(0, 255).astype(np.uint8)
        ff.stdin.write(out.tobytes())
        ok, q = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(q, cv2.COLOR_BGR2GRAY)
        pts = cv2.goodFeaturesToTrack(ant, 400, 0.01, 8)
        if pts is not None:
            nov, st, _ = cv2.calcOpticalFlowPyrLK(ant, g, pts, None)
            bons = st.ravel() == 1
            if bons.sum() >= 12:
                T, _ = cv2.estimateAffinePartial2D(pts[bons], nov[bons], method=cv2.RANSAC, ransacReprojThreshold=2.0)
                if T is not None:
                    M = np.vstack([T, [0, 0, 1]]) @ M
        ant = g
    ff.stdin.close()
    ff.wait()
    cap.release()


def compor_parado(clipe, cfg, base, saida):
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=width,height", "-of", "csv=p=0", str(clipe)],
                                   capture_output=True, text=True, check=True).stdout.strip().split(","))
    png = Path(saida).with_suffix(".camada.png")
    camada(cfg, base, w, h, png)
    zoom = cfg.get("zoom", 0.10)  # aproximação por código ao longo de 5 s, com leve balanço de câmera na mão
    fc = (f"[0:v][1:v]overlay=0:0,scale=w='trunc({w}*(1+{zoom}*t/5)/2)*2':h=-2:eval=frame:flags=bicubic,"
          f"crop={w}:{h}:'(iw-{w})/2+6*sin(t*1.3)':'(ih-{h})/2+5*sin(t*0.9+1)',format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(clipe), "-loop", "1", "-i", str(png),
                    "-filter_complex", fc, "-map", "[v]", "-t", "5", "-an", "-c:v", "libx264", "-crf", "16",
                    str(saida)], check=True)
    png.unlink()


if __name__ == "__main__":
    import json
    compor(sys.argv[1], json.loads(sys.argv[2]), Path(sys.argv[3]), sys.argv[4])
