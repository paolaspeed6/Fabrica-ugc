# Cola o cartão da foto 01 em posição própria por cena (spec.json), sem cobrir produto, texto nem CTA.
# uso: aplicar2.py entrada.mp4 chave_spec prefixo_cartao(ed2/cNN) saida.mp4
import sys, json, subprocess, os
from PIL import Image
src, key, card, out = sys.argv[1:5]
segs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec.json')))[key]
tmp = os.path.dirname(os.path.abspath(out))
ws = sorted({s[4] for s in segs}); inp = ['-i', src]; idx = {}
for w in ws:
    for kind in ('mask', 'fg'):
        p = f'{tmp}/_{os.path.basename(card)}_{kind}_{w}.png'
        Image.open(f'{card}_{kind}.png').resize((w, w), Image.LANCZOS).save(p)
        inp += ['-loop', '1', '-i', p]; idx[(kind, w)] = len(inp) // 2 - 1 if False else None
# índices: 0 = vídeo; depois mask/fg de cada largura
n = 1; idx = {}
for w in ws: idx[('mask', w)] = n; idx[('fg', w)] = n + 1; n += 2
f = [f'[0:v]split={len(segs) + 1}[v0]' + ''.join(f'[b{i}]' for i in range(len(segs)))]
last = 'v0'
for i, (t0, t1, x, y, w) in enumerate(segs):
    en = f"between(t,{t0},{t1 - 0.001 if i < len(segs) - 1 else 99})"
    f.append(f"[b{i}]crop={w}:{w}:{x}:{y},gblur=sigma=22,eq=brightness=0.03:saturation=1.15,format=rgba[bl{i}]")
    f.append(f"[{idx[('mask', w)]}:v]format=gray[m{i}]")
    f.append(f"[bl{i}][m{i}]alphamerge[c{i}]")
    f.append(f"[{last}][c{i}]overlay={x}:{y}:shortest=1:enable='{en}'[o{i}a]")
    f.append(f"[o{i}a][{idx[('fg', w)]}:v]overlay={x}:{y}:shortest=1:enable='{en}'[o{i}]")
    last = f'o{i}'
cmd = ['ffmpeg', '-loglevel', 'error', '-y'] + inp + ['-filter_complex', ';'.join(f), '-map', f'[{last}]', '-map', '0:a?',
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True)
