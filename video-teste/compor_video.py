"""Cena com o produto 100% fiel: cenário animado (vídeo sem o produto) + foto real do anúncio por cima.

Uso:
    python3 compor_video.py fundo.mp4 foto_anuncio.png saida.mp4 [y_chao=0.73] [largura=0.94] [zoom=1.10]

A IA nunca redesenha o produto: escritas, logos e cores ficam idênticos ao anúncio.
A foto precisa ter fundo branco (padrão da foto principal da Shopee). O zoom lento
("câmera se aproximando") é feito por código no quadro inteiro, então não deforma nada.
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1920, 24


def recorte(foto, larg):
    a = np.asarray(Image.open(foto).convert("RGB")).astype(float)
    m = 24  # marcas de borda de algumas fotos de anúncio
    a[:m] = 255; a[-m:] = 255; a[:, :m] = 255; a[:, -m:] = 255
    x0, y0, x1, y1 = Image.fromarray(((255 - a.min(axis=2)) > 40).astype("uint8") * 255).getbbox()
    a = a[y0:min(a.shape[0], y1 + 25), x0:x1]  # inclui a sombra no chão
    alt = int(a.shape[0] * larg / a.shape[1])
    a = np.asarray(Image.fromarray(a.astype("uint8")).resize((larg, alt), Image.LANCZOS)).astype(float)
    alfa = np.clip((255 - a.min(axis=2) - 110) / 60, 0, 1)[..., None]  # sólido = pixel original
    return a, alfa


def main():
    fundo, foto, saida = sys.argv[1:4]
    y_chao = float(sys.argv[4]) if len(sys.argv) > 4 else 0.73
    larg = int(W * (float(sys.argv[5]) if len(sys.argv) > 5 else 0.94))
    zoom = float(sys.argv[6]) if len(sys.argv) > 6 else 1.10
    a, alfa = recorte(foto, larg)
    alt = a.shape[0]
    x, y = (W - larg) // 2, int(H * y_chao) - alt
    sombra = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sombra).ellipse([x + 30, y + alt - 60, x + larg - 30, y + alt - 12], fill=70)
    sombra = (np.asarray(sombra.filter(ImageFilter.GaussianBlur(18))).astype(float) / 255)[..., None]
    cx, cy = W / 2, y + alt / 2  # o zoom aproxima do centro do produto
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fundo],
                               capture_output=True, text=True).stdout)
    n = int(dur * FPS)
    ler = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", fundo, "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    gravar = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                               "-pix_fmt", "yuv420p", saida], stdin=subprocess.PIPE)
    i = 0
    while True:
        buf = ler.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        q = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(float)
        q = q * (1 - sombra) + np.array([20, 15, 10]) * sombra
        reg = q[y:y + alt, x:x + larg]
        reg[:] = alfa * a + (1 - alfa) * reg * a / 255  # branco some, sombra escurece
        t = min(i / max(n - 1, 1), 1)
        z = 1 + (zoom - 1) * (t * t * (3 - 2 * t))  # suave no começo e no fim
        cw, ch = W / z, H / z
        l = min(max(cx - cw / 2, 0), W - cw); tp = min(max(cy - ch / 2, 0), H - ch)
        img = Image.fromarray(q.astype("uint8")).resize((W, H), Image.BICUBIC, box=(l, tp, l + cw, tp + ch))
        gravar.stdin.write(img.tobytes())
        i += 1
    gravar.stdin.close(); gravar.wait(); ler.wait()
    print(f"{saida}: {i} quadros")


if __name__ == "__main__":
    main()
