"""Compara a 1ª miniatura do perfil com o vídeo (ffmpeg extrai quadros)."""
import os, subprocess, tempfile
from PIL import Image, ImageOps

# miniaturas do grid em "Vídeos" do perfil <SEU_PERFIL> (800x1280)
TILES = [(0, 540, 266, 892), (268, 540, 533, 892), (535, 540, 800, 892)]
TAM = (48, 64)


def _norm(im):
    return ImageOps.fit(im.convert('L'), TAM)


def quadros(video, tempos=(0, 0.5, 1.0, 2.0)):
    out = []
    for t in tempos:
        f = os.path.join(tempfile.gettempdir(), f'hq_{t}.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', video,
                        '-frames:v', '1', f], capture_output=True, timeout=60,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        if os.path.exists(f):
            out.append(_norm(Image.open(f)))
            os.remove(f)
    return out


def dist(a, b):
    pa, pb = a.tobytes(), b.tobytes()
    return sum(abs(x - y) for x, y in zip(pa, pb)) / len(pa)


def distancias(tela, video, qs=None):
    """Distância (0-255, menor = mais parecido) de cada miniatura ao melhor quadro do vídeo."""
    qs = qs or quadros(video)
    if not qs:
        raise RuntimeError('ffmpeg não extraiu quadros de ' + video)
    return [min(dist(_norm(tela.crop(t)), q) for q in qs) for t in TILES]


if __name__ == '__main__':
    import sys
    print(distancias(Image.open(sys.argv[1]).convert('RGB'), sys.argv[2]))
