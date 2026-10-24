"""Detector automático de produto que se mexe ou deforma num clipe gerado (Kevin 2026-10-22: "mesmo dando a instrução
pro produto ficar parado, ele se mexeu"). Grátis, roda antes de montar e decide o trecho limpo de cada cena.

Como: acha o produto no 1º quadro (rembg), segue pontos do produto e do resto da cena com fluxo óptico.
Com os pontos do cenário calcula a geometria da câmera (matriz fundamental, aceita arco, deslize e aproximação
com paralaxe). Se o produto só está parado e a câmera se mexe, os pontos dele obedecem à mesma geometria.
Se o produto gira, desliza, muda de forma ou ganha peça, os pontos dele saem dessa geometria.
Validado em 2026-10-22: pegou a base giratória da cadeira p05 cena C girando sozinha a partir de 1,25 s
e deixou passar a cena A (só câmera) até 4,5 s.

uso: python3 checar_movimento.py <clipe.mp4> [--json]   (LIMITE padrão 2,5 = erro do produto / erro do cenário)"""
import json, os, sys
import cv2, numpy as np

LIMITE = float(os.environ.get('LIMITE', '2.5')); PISO = float(os.environ.get('PISO', '1.0'))  # px; abaixo disso é ruído


def mascara(img):
    from rembg import remove, new_session
    from PIL import Image
    a = np.array(remove(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), session=new_session('isnet-general-use')))[..., 3]
    n, lab, st, _ = cv2.connectedComponentsWithStats((a > 128).astype(np.uint8))
    if n < 2:
        return None
    return (lab == 1 + int(np.argmax(st[1:, 4]))).astype(np.uint8) * 255


def sampson(F, p0, p1):
    x0 = np.c_[p0, np.ones(len(p0))]; x1 = np.c_[p1, np.ones(len(p1))]
    a = x0 @ F.T; b = x1 @ F
    return np.sqrt(np.sum(x1 * a, 1) ** 2 / (a[:, 0] ** 2 + a[:, 1] ** 2 + b[:, 0] ** 2 + b[:, 1] ** 2 + 1e-9))


def checar(clip, passo=3):
    cap = cv2.VideoCapture(clip); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    ok, f0 = cap.read(); assert ok, clip
    m = mascara(f0)
    if m is None:
        return dict(clip=clip, erro='produto não achado', limpo=0.0)
    g0 = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY)
    pp = cv2.goodFeaturesToTrack(g0, 400, 0.01, 6, mask=cv2.erode(m, np.ones((9, 9))))
    pf = cv2.goodFeaturesToTrack(g0, 600, 0.005, 8, mask=255 - cv2.dilate(m, np.ones((31, 31))))
    if pp is None or pf is None or len(pp) < 12 or len(pf) < 20:
        return dict(clip=clip, erro='poucos pontos para medir', limpo=0.0)
    pp, pf = pp.reshape(-1, 2), pf.reshape(-1, 2)
    cp, cf, prev = pp.copy(), pf.copy(), g0; vp = np.ones(len(pp), bool); vf = np.ones(len(pf), bool)
    serie, i = [], 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        i += 1; g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        a, sa, _ = cv2.calcOpticalFlowPyrLK(prev, g, cp.reshape(-1, 1, 2), None, winSize=(21, 21), maxLevel=3)
        b, sb, _ = cv2.calcOpticalFlowPyrLK(prev, g, cf.reshape(-1, 1, 2), None, winSize=(21, 21), maxLevel=3)
        cp, cf = a.reshape(-1, 2), b.reshape(-1, 2); vp &= sa.ravel() == 1; vf &= sb.ravel() == 1; prev = g
        if i % passo:
            continue
        if vp.sum() < 12 or vf.sum() < 20:
            serie.append((round(i / fps, 2), 99.0, 1.0)); continue
        F, _ = cv2.findFundamentalMat(pf[vf], cf[vf], cv2.FM_RANSAC, 1.0, 0.999)
        if F is None or F.shape != (3, 3):
            continue
        ep = float(np.median(sampson(F, pp[vp], cp[vp]))); eb = float(np.median(sampson(F, pf[vf], cf[vf])))
        serie.append((round(i / fps, 2), round(ep, 2), round(eb, 2)))
    ruim = next((t for t, ep, eb in serie if ep > max(PISO, LIMITE * eb)), None)
    dur = round(i / fps, 2)
    limpo = round(max(0.0, ruim - 0.15) if ruim is not None else dur, 2)
    return dict(clip=clip, limpo=limpo, duracao=dur, primeiro_problema=ruim,
                pior=max(serie, key=lambda x: x[1] / max(x[2], 0.2)) if serie else None)


if __name__ == '__main__':
    r = checar([a for a in sys.argv[1:] if not a.startswith('--')][0])
    print(json.dumps(r, ensure_ascii=False) if '--json' in sys.argv else
          f"{r['clip']}: trecho limpo {r['limpo']} s de {r.get('duracao')} s (1º problema em {r.get('primeiro_problema')} s)")
