"""Trava o produto num clipe de câmera parada (Seedance camera_fixed): o produto e uma margem em volta vêm do
1º quadro, o resto do cenário (luz, folhas) segue animado pela IA. Resultado: produto 100% imóvel e fiel.
Depois o montar.py põe o movimento de câmera por código. Kevin 2026-10-22: "o produto não pode se mexer".
uso: python3 fixar.py <clipe.mp4> <saida.mp4> [margem_px] [--fonte img.jpg]
--fonte: o produto travado vem dessa imagem (mesma composição da cena), ex. <C>_orig.jpg com a marca que o sem_letras apagou."""
import sys, subprocess
import cv2, numpy as np


def mascara(img):
    """TODAS as partes grandes do produto (kit: microfones e controle; cadeira: encosto de cabeça solto), não só a maior.
    Kevin 2026-10-22: microfones e controle da p14 e o encosto da p10 bugaram porque ficaram fora da trava."""
    from rembg import remove, new_session
    from PIL import Image
    a = np.array(remove(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), session=new_session('isnet-general-use')))[..., 3]
    n, lab, st, _ = cv2.connectedComponentsWithStats((a > 128).astype(np.uint8))
    if n < 2:
        return None
    big = st[1:, 4].max()
    return np.isin(lab, [i for i in range(1, n) if st[i, 4] >= 0.02 * big]).astype(np.uint8) * 255


args = [x for x in sys.argv[1:] if not x.startswith('--')]
fonte = sys.argv[sys.argv.index('--fonte') + 1] if '--fonte' in sys.argv else None
if fonte:
    args.remove(fonte)
src, dst = args[0], args[1]; marg = int(args[2]) if len(args) > 2 else 40
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS) or 24
ok, f0 = cap.read(); assert ok
m = mascara(f0); assert m is not None, 'produto não achado'
if fonte:
    f0 = cv2.resize(cv2.imread(fonte), (f0.shape[1], f0.shape[0]), interpolation=cv2.INTER_AREA)
# sombra de contato e pés ficam dentro da margem; borda suave para não ver costura
m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * marg + 1, 2 * marg + 1)))
a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), marg / 2.5)[..., None]
h, w = f0.shape[:2]
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', str(fps),
                      '-i', '-', '-c:v', 'libx264', '-crf', '15', '-pix_fmt', 'yuv420p', dst], stdin=subprocess.PIPE)
fr, fora = f0, []
anel = (cv2.dilate(m, np.ones((61, 61))) > 0) & (m == 0)
perto = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (121, 121))) > 0  # 301 deixava um disco de luz congelada visível
# a luz do cenário muda: a parte travada acompanha o brilho/cor do entorno (ganho por canal, suavizado no tempo)
viz = (cv2.dilate(m, np.ones((241, 241))) > 0) & ~(cv2.dilate(m, np.ones((2 * marg + 41, 2 * marg + 41))) > 0)
ref = f0[viz].astype(np.float64).mean(0) + 1; ganho = np.ones(3)
while ok:
    ganho = 0.8 * ganho + 0.2 * np.clip((fr[viz].astype(np.float64).mean(0) + 1) / ref, 0.6, 1.6)
    # o que mudou muito perto do produto (peça girando, sombra dele) também volta ao 1º quadro
    d = (np.abs(fr.astype(np.float64) - f0 * ganho).max(2) > 40) & perto  # compara já com o brilho ajustado: só peça que mexeu
    d = cv2.dilate(cv2.morphologyEx(d.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((5, 5))), np.ones((25, 25)))
    b = np.maximum(a, cv2.GaussianBlur(d.astype(np.float32) / 255, (0, 0), 10)[..., None])
    out = (np.clip(f0 * ganho, 0, 255) * b + fr * (1 - b)).astype(np.uint8)
    fora.append(float(np.abs(fr.astype(int) - f0.astype(int)).max(2)[anel].mean()))
    p.stdin.write(out.tobytes()); ok, fr = cap.read()
p.stdin.close(); p.wait()
print(f'{dst}: {len(fora)} quadros; mudança média no anel em volta do produto {max(fora):.1f} (acima de ~12 = peça saindo da margem)')
