"""Cena por CÓDIGO: movimento de câmera sobre a foto real do anúncio (US$ 0, letras e estampas intactas).

Uso:
    python3 mover_foto.py <foto.jpg> <saida.mp4> [--mov push] [--zoom 1.08] [--recorte x0,y0,x1,y1] [--dur 5.7]

Movimentos (regras_de_erros.md: nunca câmera travada, nunca girar para um lado que a foto não mostra):
  push     aproxima devagar          pull    afasta devagar (começa perto, termina mostrando tudo)
  pan_esq  desliza para a esquerda   pan_dir desliza para a direita
  sobe     sobe como uma grua        desce   desce revelando
Todos levam um leve balanço de câmera na mão (deslocamento e rotação mínimos) e easing suave.
Cena 1 (primeiro take, produto inteiro): use --mov push --zoom 1.05.
"""
import argparse
import math
import subprocess

from PIL import Image


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("foto"); a.add_argument("saida")
    a.add_argument("--mov", default="push")
    a.add_argument("--zoom", type=float, default=1.08)
    a.add_argument("--recorte", default="")
    a.add_argument("--dur", type=float, default=5.7)
    a.add_argument("--fps", type=int, default=30)
    o = a.parse_args()

    img = Image.open(o.foto).convert("RGB")
    if o.recorte:
        img = img.crop(tuple(int(v) for v in o.recorte.split(",")))
    w0, h0 = img.size
    k = 1080 / max(w0, h0)
    W, H = int(w0 * k) // 2 * 2, int(h0 * k) // 2 * 2
    src = img.resize((W * 2, H * 2), Image.LANCZOS)  # 2x para o zoom não serrilhar
    S = 2.0

    zmax = max(o.zoom, 1.04)
    zmin = 1.03  # margem para o balanço da mão nunca mostrar borda
    desl = (zmax - 1) * 0.42  # quanto o centro anda nos movimentos laterais (fração da largura)
    n = int(round(o.dur * o.fps))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(o.fps), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", o.saida],
                          stdin=subprocess.PIPE)
    for i in range(n):
        t = ease(i / (n - 1))
        cx, cy = 0.5, 0.5
        if o.mov == "push":
            z = zmin + (zmax - zmin) * t
        elif o.mov == "pull":
            z = zmax - (zmax - zmin) * t
        else:
            z = zmax
            d = desl * (t - 0.5)
            if o.mov == "pan_esq": cx = 0.5 + d
            elif o.mov == "pan_dir": cx = 0.5 - d
            elif o.mov == "sobe": cy = 0.5 + d
            elif o.mov == "desce": cy = 0.5 - d
        # câmera na mão: duas senoides lentas, amplitude mínima
        s = i / o.fps
        cx += 0.0022 * math.sin(2 * math.pi * 0.23 * s) + 0.0009 * math.sin(2 * math.pi * 0.61 * s + 1)
        cy += 0.0018 * math.sin(2 * math.pi * 0.19 * s + 2) + 0.0008 * math.sin(2 * math.pi * 0.53 * s)
        rot = math.radians(0.28 * math.sin(2 * math.pi * 0.17 * s + 0.5))
        # limita o centro para a janela nunca sair da foto
        mx, my = 0.5 / z + 0.004, 0.5 / z + 0.004
        cx, cy = min(max(cx, mx), 1 - mx), min(max(cy, my), 1 - my)
        # transformação: pixel de saída (x, y) -> pixel da fonte
        c, sn = math.cos(rot) / z * S, math.sin(rot) / z * S
        X0, Y0 = cx * W * S, cy * H * S
        coef = (c, -sn, X0 - c * W / 2 + sn * H / 2,
                sn, c, Y0 - sn * W / 2 - c * H / 2)
        quadro = src.transform((W, H), Image.AFFINE, coef, resample=Image.BICUBIC)
        ff.stdin.write(quadro.tobytes())
    ff.stdin.close()
    ff.wait()
    if ff.returncode:
        raise SystemExit("ffmpeg falhou")


if __name__ == "__main__":
    main()
