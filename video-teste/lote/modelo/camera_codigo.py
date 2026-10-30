"""Câmera por código sobre a imagem (K19/K22, grátis): resgate e produto sem cena aprovada nunca viram clipe de IA.
Avanço lento e suave (zoom 1,00 -> 1,05 em 5 s, centro da imagem): corta só 2,5% de cada lado, as pontas do produto ficam.
Grava pNN-cenas/<X>.mp4 (720x1280, 25 fps, 5 s) e fiscal_video.json "usar 0.0-5.0", depois roda aprovar.py.
uso: python3 -I camera_codigo.py pNN [A,B,C]   (cenas na ordem da escolha da dona: a 1ª vira A, a 2ª B, a 3ª C)
     a imagem de origem é pNN-cenas/<X>.jpg; com a ordem trocada, as originais vão antes para pNN-cenas/orig_<X>.jpg."""
import json, shutil, subprocess, sys
from pathlib import Path
B = Path(__file__).resolve().parent
ZOOM = 1.05; DUR = 5; FPS = 25


def clipe(img, mp4):
    n = DUR * FPS
    # sobe a resolução antes do zoompan: sem isso o zoom anda em degraus de 1 px (tremido)
    vf = (f"scale=2880:5120,zoompan=z='1+{ZOOM - 1}*(on/{n - 1})*(on/{n - 1})*(3-2*on/{n - 1})':"
          f"x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s=720x1280:fps={FPS},format=yuv420p")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', str(img), '-vf', vf, '-frames:v', str(n),
                    '-c:v', 'libx264', '-crf', '15', str(mp4)], check=True)


if __name__ == '__main__':
    k = sys.argv[1]; d = B / f'{k}-cenas'
    ordem = sys.argv[2].split(',') if len(sys.argv) > 2 else [c for c in 'ABC' if (d / f'{c}.jpg').exists()]
    for c in 'ABC':
        if (d / f'{c}.jpg').exists() and not (d / f'orig_{c}.jpg').exists(): shutil.copy(d / f'{c}.jpg', d / f'orig_{c}.jpg')
    for f in list(d.glob('[ABC].jpg')) + list(d.glob('[ABC].mp4')) + list(d.glob('[ABC]_*.mp4')): f.unlink()
    fv = {}
    for novo, c in zip('ABC', ordem):
        shutil.copy(d / f'orig_{c}.jpg', d / f'{novo}.jpg'); clipe(d / f'{novo}.jpg', d / f'{novo}.mp4')
        fv[novo] = dict(veredito='usar 0.0-5.0', inicio=0.0, fim=float(DUR), defeitos=[], origem=f'imagem {c}, câmera por código (K19/K22)')
    (d / 'fiscal_video.json').write_text(json.dumps(fv, ensure_ascii=False, indent=1))
    (d / 'aprovado.json').unlink(missing_ok=True)
    subprocess.run([sys.executable, '-I', str(B / 'aprovar.py'), k], check=True)
