"""Monta o vídeo final: junta as cenas, põe em 9:16 e escreve o texto na tela.

Uso:
    python3 montar_video.py montagem.json

montagem.json:
{
  "nome": "banqueta_v1",
  "cenas": [
    {"clipe": "cena1.mp4", "texto": "Gancho aqui"},
    {"clipe": "cena2.mp4", "texto": "Benefício aqui"},
    {"clipe": "cena3.mp4", "texto": "CTA aqui"}
  ]
}

Caminhos dos clipes são relativos ao JSON. Clipes quadrados ou horizontais
ganham fundo desfocado para preencher o 9:16. Custo: zero (FFmpeg local).
"""
import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

FONTE = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
LARGURA, ALTURA = 720, 1280


def cena_com_texto(clipe, texto, saida, pasta_tmp):
    arq_texto = Path(pasta_tmp) / (saida.stem + ".txt")
    arq_texto.write_text("\n".join(textwrap.wrap(texto, width=22)), encoding="utf-8")
    filtro = (
        f"[0:v]split[a][b];"
        f"[a]scale={LARGURA}:{ALTURA}:force_original_aspect_ratio=increase,crop={LARGURA}:{ALTURA},boxblur=20:2[fundo];"
        f"[b]scale={LARGURA}:{ALTURA}:force_original_aspect_ratio=decrease[frente];"
        f"[fundo][frente]overlay=(W-w)/2:(H-h)/2,fps=24,"
        f"drawtext=fontfile={FONTE}:textfile={arq_texto}:fontsize=52:fontcolor=white:"
        f"borderw=4:bordercolor=black:line_spacing=10:x=(w-text_w)/2:y=h*0.14:"
        f"box=1:boxcolor=black@0.35:boxborderw=18[v]"
    )
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clipe), "-filter_complex", filtro,
                    "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                    "-pix_fmt", "yuv420p", str(saida)], check=True)


def main():
    arq = Path(sys.argv[1]).resolve()
    montagem = json.loads(arq.read_text(encoding="utf-8"))
    final = arq.parent / f"{montagem['nome']}.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        partes = []
        for i, cena in enumerate(montagem["cenas"], 1):
            saida = Path(tmp) / f"parte{i}.mp4"
            cena_com_texto(arq.parent / cena["clipe"], cena["texto"], saida, tmp)
            partes.append(saida)
        lista = Path(tmp) / "lista.txt"
        lista.write_text("".join(f"file '{p}'\n" for p in partes))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                        "-c", "copy", "-movflags", "+faststart", str(final)], check=True)
    print(f"Pronto: {final}")


if __name__ == "__main__":
    main()
