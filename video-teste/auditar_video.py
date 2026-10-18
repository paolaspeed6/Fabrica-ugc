"""Auditoria automática do vídeo final (grátis, só ffmpeg). Roda antes de entregar à dona.
a dona 2026-10-18: a qualidade tem que SUPERAR as referências de referencias/; estas medidas pegam
o que passou nelas: cena quase parada, tela sem gancho no 1º quadro, transição fantasma, vídeo mudo.

uso: python3 auditar_video.py video.mp4 [mais.mp4 ...]   (sai com código 1 se algum reprovar)
"""
import json
import subprocess
import sys

CENA_S = 5.0
MOV_MIN = 2.0      # média de diferença entre quadros (0-255, 10 fps, 108x192); abaixo disso a câmera está parada
FANTASMA_MAX = 0.4  # segundos de dupla exposição tolerados em cada troca de cena
TEXTO_MIN = 6.0    # contraste mínimo do 1º quadro contra o quadro de 1 s na área do texto (gancho já visível)


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


def quadro_cinza(v, t):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t), "-i", v, "-frames:v", "1",
           "-vf", "scale=54:96,format=gray", "-f", "rawvideo", "-"]
    return subprocess.run(cmd, capture_output=True).stdout


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

    for corte in (CENA_S, 2 * CENA_S):
        # troca seca = 1 pico; fusão longa = vários quadros médios seguidos (dupla exposição)
        janela = d[int((corte - 1) * 10):int((corte + 1) * 10)]
        base = sorted(janela)[len(janela) // 2] if janela else 0
        fantasma = sum(1 for x in janela if x > base + 3) / 10
        info[f"fusao_{int(corte)}s"] = fantasma
        if fantasma > FANTASMA_MAX:
            falhas.append(f"transição em {corte:.0f}s com {fantasma:.1f}s de dupla exposição")

    q0, q1 = quadro_cinza(v, 0), quadro_cinza(v, 1.0)
    if q0 and q1:
        dif = sum(abs(a - b) for a, b in zip(q0, q1)) / len(q0)
        info["gancho_1o_quadro"] = round(dif, 2)
        if dif > TEXTO_MIN:
            falhas.append("1º quadro diferente do quadro de 1 s: gancho ainda não aparece na capa")
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
