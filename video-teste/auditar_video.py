"""Auditoria automática do vídeo final (grátis, só ffmpeg). Roda antes de entregar à dona.
a dona 2026-10-18: a qualidade tem que SUPERAR as referências de referencias/; estas medidas pegam
o que passou nelas: cena quase parada, tela sem gancho no 1º quadro, transição fantasma, vídeo mudo.

uso: python3 auditar_video.py video.mp4 [mais.mp4 ...]   (sai com código 1 se algum reprovar)
"""
import json
import subprocess
import sys

import numpy as np

CENA_S = 5.0
MOV_MIN = 2.0      # média de diferença entre quadros (0-255, 10 fps, 108x192); abaixo disso a câmera está parada
FANTASMA_MAX = 0.4  # segundos de dupla exposição tolerados em cada troca de cena
TEXTO_MIN = 0.7    # letras no 1º quadro / letras em 1,2 s; abaixo disso o gancho ainda está entrando (refs 0,03-0,55; Luxo 0,87-1,0)


def sonda(v):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=codec_type,width,height", "-of", "json", v],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def diferencas(v):
    """diferença média entre quadros seguidos, a 10 fps."""
    cmd = ["ffmpeg", "-v", "error", "-i", v, "-vf",
           "scale=108:192,fps=10,tblend=all_mode=difference,signalstats,"
           "metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    return [float(l.split("=")[1]) for l in out.splitlines() if "YAVG=" in l]


def brilhos(v):
    """brilho médio de cada quadro, a 10 fps (para reconhecer mergulho ao preto, que é corte de propósito)."""
    cmd = ["ffmpeg", "-v", "error", "-i", v, "-vf",
           "scale=108:192,fps=10,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    return [float(l.split("=")[1]) for l in out.splitlines() if "YAVG=" in l]


def quadro_cinza(v, t):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t), "-i", v, "-frames:v", "1",
           "-vf", "scale=270:480,format=gray", "-f", "rawvideo", "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(480, 270).astype(int) if len(b) == 480 * 270 else None


def letras(a):
    """pixels de borda nítida de letra clara (vizinho bem mais escuro a 2 px); movimento de câmera quase não muda isso."""
    escuro = np.zeros(a.shape, bool)
    for dy, dx in ((0, 2), (0, -2), (2, 0), (-2, 0)):
        escuro |= np.roll(np.roll(a, dy, 0), dx, 1) < a - 90
    return int(((a > 200) & escuro).sum())


def auditar(v):
    falhas, info = [], {}
    s = sonda(v)
    dur = float(s["format"]["duration"])
    vid = next(x for x in s["streams"] if x["codec_type"] == "video")
    tem_audio = any(x["codec_type"] == "audio" for x in s["streams"])
    info["formato"] = f'{vid["width"]}x{vid["height"]} {dur:.2f}s audio={"sim" if tem_audio else "não"}'
    if (vid["width"], vid["height"]) != (1080, 1920):
        falhas.append("resolução diferente de 1080x1920")
    if not 14.9 <= dur <= 15.3:
        falhas.append(f"duração {dur:.2f}s (alvo 15 s)")
    if not tem_audio:
        falhas.append("vídeo mudo: sem trilha (ver memoria/reference-videos-quality-bar.md)")

    d = diferencas(v)
    for c in range(3):
        # ignora 0,6 s em volta de cada corte para medir só o movimento de câmera
        ini, fim = int((c * CENA_S + (0.6 if c else 0)) * 10), int(((c + 1) * CENA_S - 0.6) * 10)
        trecho = d[ini:fim] or [0]
        mov = sum(trecho) / len(trecho)
        info[f"movimento_cena{c + 1}"] = round(mov, 2)
        if mov < MOV_MIN:
            falhas.append(f"cena {c + 1} quase parada (movimento {mov:.2f} < {MOV_MIN})")

    luz = brilhos(v)
    for corte in (CENA_S, 2 * CENA_S):
        # troca seca = 1 pico; fusão longa = vários quadros médios seguidos (dupla exposição)
        janela = d[int((corte - 1) * 10):int((corte + 1) * 10)]
        base = sorted(janela)[len(janela) // 2] if janela else 0
        fantasma = sum(1 for x in janela if x > base + 3) / 10
        info[f"fusao_{int(corte)}s"] = fantasma
        # passou pelo preto (brilho < 35) = mergulho ao preto proposital, não dupla exposição
        if min(luz[int((corte - 1) * 10):int((corte + 1) * 10)] or [255]) < 35:
            info[f"fusao_{int(corte)}s"] = "preto"
        elif fantasma > FANTASMA_MAX:
            falhas.append(f"transição em {corte:.0f}s com {fantasma:.1f}s de dupla exposição")

    q0, q1 = quadro_cinza(v, 0), quadro_cinza(v, 1.2)
    if q0 is not None and q1 is not None:
        razao = letras(q0) / max(letras(q1), 1)
        info["gancho_1o_quadro"] = round(razao, 2)
        if razao < TEXTO_MIN:
            falhas.append("gancho ainda não aparece no 1º quadro (capa)")
    return falhas, info


if __name__ == "__main__":
    ruim = 0
    for v in sys.argv[1:]:
        falhas, info = auditar(v)
        print(("REPROVADO " if falhas else "APROVADO  ") + v, info)
        for f in falhas:
            print("   -", f)
        ruim += bool(falhas)
    sys.exit(1 if ruim else 0)
