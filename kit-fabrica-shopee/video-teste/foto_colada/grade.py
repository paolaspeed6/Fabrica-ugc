# Folha de prévia: por cena, 3 quadros (início, meio, fim) com grade de 100 px e o cartão proposto.
import sys, json, subprocess, numpy as np
from PIL import Image, ImageDraw
vid, segs, out = sys.argv[1], json.loads(sys.argv[2]), sys.argv[3]
k = 5  # 1080x1920 -> 216x384
tiles = []
for s in segs:
    for t in (s['t0'] + 0.3, (s['t0'] + s['t1']) / 2, s['t1'] - 0.3):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', vid, '-frames:v', '1', '-vf', 'scale=216:384', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        im = Image.fromarray(np.frombuffer(raw, np.uint8).reshape(384, 216, 3).copy()); d = ImageDraw.Draw(im)
        for g in range(100, 1920, 100):
            c = (0, 255, 255) if g % 500 == 0 else (90, 90, 90)
            d.line((0, g // k, 216, g // k), fill=c); d.line((g // k, 0, g // k, 384), fill=c) if g < 1080 else None
        if 'x' in s: d.rectangle((s['x'] // k, s['y'] // k, (s['x'] + s['w']) // k, (s['y'] + s['w']) // k), outline=(255, 0, 255), width=2)
        tiles.append(im)
C = 6; R = (len(tiles) + C - 1) // C
sh = Image.new('RGB', (216 * C, 384 * R), 'black')
for i, t in enumerate(tiles): sh.paste(t, (216 * (i % C), 384 * (i // C)))
sh.save(out, quality=82)
