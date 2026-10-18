"""Montador 'luxo' 9:16 (conceito Zara Home e variações; memoria/colecao-luxo.md).
Serifa fina + itálico, rótulos em caixa alta espaçados, linha fina, color grade com grão,
sem moldura e sem botão de carrinho.  uso: python3 -I build_lux.py spec.json
(feito na sessão "Poltrona laranja" em 2026-10-18; fontes agora vêm de video-teste/fontes/)
"""
import json, sys, subprocess, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 24
SW, SH = 720, 1280
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fontes') + '/'
FONTS = {
    'serif': FD + 'Caladea-Regular.ttf',
    'serif_it': FD + 'Caladea-Italic.ttf',
    'serif_b': FD + 'Caladea-Bold.ttf',
    'sans': FD + 'LiberationSans-Regular.ttf',
    # opção B (shopee3 moderno) e opção C (revista), 2026-10-18
    'pop': FD + 'Poppins-Medium.ttf', 'pop_sb': FD + 'Poppins-SemiBold.ttf', 'pop_b': FD + 'Poppins-Bold.ttf',
    'pop_r': FD + 'Poppins-Regular.ttf',
    'dms': FD + 'DMSerifDisplay-Regular.ttf', 'dms_it': FD + 'DMSerifDisplay-Italic.ttf',
    'play': FD + 'PlayfairDisplay.ttf', 'play_it': FD + 'PlayfairDisplay-Italic.ttf', 'dm': FD + 'DMSans.ttf',
}
spec = json.load(open(sys.argv[1]))
SRC = spec['src']
INK = tuple(spec.get('ink', (255, 255, 255)))
ACC = tuple(spec.get('accent', (214, 168, 120)))  # cor de destaque das palavras entre [ ]
AUDIO_ONLY = os.environ.get('AUDIO_ONLY') == '1'


def font(n, s):
    return ImageFont.truetype(FONTS[n], s)


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def ease_io(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def lerp(a, b, t):
    return a + (b - a) * t


def tokens(line):
    """*itálico* e [destaque na cor ACC]; devolve (texto, italico, destaque)."""
    out, it, ac, buf = [], False, False, ''
    for ch in line:
        if ch in '*[]':
            if buf:
                out.append((buf, it, ac)); buf = ''
            if ch == '*': it = not it
            else: ac = ch == '['
        else:
            buf += ch
    if buf:
        out.append((buf, it, ac))
    return out


def soft_shadow(img, blur=14, alpha=120, dy=4):
    a = img.getchannel('A').point(lambda v: int(v * alpha / 255))
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.putalpha(a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, dy)); out.alpha_composite(img)
    return out


def text_block(lines, size, align='left', spacing=1.06, color=INK, base='serif', it='serif_it', track=0, shadow=True):
    fr, fi = font(base, size), font(it, size)
    def wlen(t, f):
        return f.getlength(t) + track * len(t)
    widths = [sum(wlen(t, fi if i else fr) for t, i, _ in tokens(ln)) for ln in lines]
    lh = int(size * spacing)
    pad = 40
    img = Image.new('RGBA', (int(max(widths)) + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for k, ln in enumerate(lines):
        x = pad + ((max(widths) - widths[k]) / 2 if align == 'center' else 0)
        y = pad + k * lh
        for t, i, a in tokens(ln):
            f = fi if i else fr
            cor = ACC if a else color
            if track:
                for ch in t:
                    d.text((x, y), ch, font=f, fill=cor); x += f.getlength(ch) + track
            else:
                d.text((x, y), t, font=f, fill=cor); x += f.getlength(t)
    return (soft_shadow(img) if shadow else img), pad


def make(el):
    k = el['kind']; al = el.get('align', 'left')
    fb, fit = el.get('base', 'serif'), el.get('it', el.get('base_it', 'serif_it'))
    cor = tuple(el.get('color', INK)); sh = el.get('shadow', True)
    if k == 'title':
        return text_block(el['lines'], el.get('size', 118), al, el.get('spacing', 1.02), cor, fb, fit, el.get('track', 0), sh)
    if k == 'body':
        return text_block(el['lines'], el.get('size', 88), al, el.get('spacing', 1.08), cor, fb, fit, el.get('track', 0), sh)
    if k == 'eyebrow':
        f = el.get('base', 'sans')
        return text_block([l.upper() for l in el['lines']], el.get('size', 34), al, 1.6, cor, f, f, el.get('track', 11), sh)
    if k == 'button':  # pílula cheia com texto e seta (CTA do shopee3 moderno)
        f = font(el.get('base', 'pop_sb'), el.get('size', 46))
        txt = el['text']; w = el.get('w', 820); h = el.get('h', 116)
        img = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
        b = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=tuple(el.get('fill', ACC)) + (255,))
        tc = tuple(el.get('text_color', (22, 20, 18)))
        tw = f.getlength(txt); arrow = el.get('arrow', True)
        x0 = (w - tw - (64 if arrow else 0)) / 2
        d.text((x0, h / 2), txt, font=f, fill=tc, anchor='lm')
        if arrow:  # seta desenhada (sem emoji)
            ax = x0 + tw + 26; ay = h / 2
            d.line([(ax, ay), (ax + 36, ay)], fill=tc, width=5)
            d.line([(ax + 22, ay - 14), (ax + 36, ay), (ax + 22, ay + 14)], fill=tc, width=5, joint='curve')
        img.alpha_composite(b, (40, 40))
        return soft_shadow(img, 18, 90, 8), 40
    if k == 'check':  # item de lista com ✓ desenhado num círculo (opção "Direto ao ponto")
        f = font(el.get('base', 'dm'), el.get('size', 52)); txt = el['text']
        r = int(el.get('size', 52) * 0.62); w = int(2 * r + 28 + f.getlength(txt)) + 80
        img = Image.new('RGBA', (w, 2 * r + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        cx, cy = 40 + r, 40 + r
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(el.get('fill', ACC)) + (255,))
        d.line([(cx - r * .45, cy + r * .02), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)],
               fill=(255, 255, 255), width=max(4, r // 5), joint='curve')
        d.text((40 + 2 * r + 28, cy), txt, font=f, fill=tuple(el.get('color', INK)), anchor='lm')
        return soft_shadow(img, 12, 120), 40
    if k == 'bars':  # barrinhas de progresso no topo, como nos Stories (desenhadas por quadro)
        return None, 0
    if k == 'glass':  # cartão de vidro fosco: desenhado por quadro em cima do vídeo (ver glass_on)
        return None, 0
    if k == 'line':
        L = el.get('len', 220)
        img = Image.new('RGBA', (L + 80, 84), (0, 0, 0, 0))
        ImageDraw.Draw(img).line([(40, 42), (40 + L, 42)], fill=INK, width=3)
        return soft_shadow(img, 8, 90), 40
    if k == 'placard':  # etiqueta de museu (galeria)
        wcard = 640
        lines = el['lines']
        img = Image.new('RGBA', (wcard + 80, 420), (0, 0, 0, 0))
        card = Image.new('RGBA', (wcard, 300), (246, 243, 237, 238))
        d = ImageDraw.Draw(card)
        d.text((44, 40), lines[0].upper(), font=font('sans', 26), fill=(110, 104, 96))
        d.text((44, 84), lines[1], font=font('serif', 56), fill=(28, 26, 24))
        d.text((44, 152), lines[2], font=font('serif_it', 42), fill=(70, 66, 60))
        d.line([(44, 216), (140, 216)], fill=(28, 26, 24), width=2)
        d.text((44, 236), lines[3], font=font('sans', 28), fill=(90, 86, 80))
        img.alpha_composite(card, (40, 40))
        return soft_shadow(img, 22, 110, 10), 40
    if k == 'clock':
        return None, 0
    raise ValueError(k)


def bars_on(base, el, t):
    """segmentos finos que enchem conforme o vídeo avança (cada um = um momento do roteiro)."""
    cuts = el['cuts']; n = len(cuts) - 1; x0, y, gap = 60, el.get('y', 96), 12
    w = (W - 2 * x0 - gap * (n - 1)) / n
    ov = Image.new('RGBA', (W, y + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)  # camada à parte: o branco translúcido mistura com o vídeo
    for i in range(n):
        a, b = cuts[i], cuts[i + 1]; fill = min(1, max(0, (t - a) / (b - a)))
        xa = x0 + i * (w + gap)
        d.rounded_rectangle([xa, y, xa + w, y + 6], radius=3, fill=(255, 255, 255, 90))
        if fill > 0:
            d.rounded_rectangle([xa, y, xa + max(6, w * fill), y + 6], radius=3, fill=(255, 255, 255, 235))
    base.alpha_composite(ov)


def glass_on(base, el, alpha, dy):
    """desfoca o vídeo atrás do cartão, escurece e põe borda fina: vidro fosco moderno."""
    x, y, w, h, r = el.get('x', 56), int(el['y'] + dy), el.get('w', W - 112), el['h'], el.get('r', 44)
    reg = base.crop((x, y, x + w, y + h)).convert('RGB').filter(ImageFilter.GaussianBlur(el.get('blur', 28)))
    tint = Image.new('RGB', (w, h), tuple(el.get('tint', (18, 16, 15))))
    reg = Image.blend(reg, tint, el.get('dark', 0.62)).convert('RGBA')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=int(255 * alpha))
    reg.putalpha(m)
    edge = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle([1, 1, w - 2, h - 2], radius=r, outline=(255, 255, 255, int(54 * alpha)), width=2)
    reg.alpha_composite(edge)
    base.alpha_composite(reg, (x, y))


def clock_img(txt, size):
    img, _ = text_block([txt], size, 'left', 1.0, base='serif')
    return img


# ---------- vídeo ----------
def read_seg(src, ss, n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', SRC[src], '-frames:v', str(n),
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3)
    while len(fr) < n:
        fr = np.concatenate([fr, fr[-1:]])
    return fr


LIFT = spec.get('lift', 0)  # sobe o vídeo N px; a faixa de baixo vira o próprio vídeo desfocado (fica atrás do cartão)


def render_src(frame, z, cx, cy):
    w, h = SW / z, SH / z
    x0 = min(max(cx - w / 2, 0), SW - w); y0 = min(max(cy - h / 2, 0), SH - h)
    img = Image.fromarray(frame).resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h))
    if not LIFT:
        return img
    out = Image.new('RGB', (W, H))
    out.paste(img, (0, -LIFT))
    # faixa de baixo: o fim do quadro esticado e desfocado, com emenda em degradê
    fundo = img.crop((0, H - LIFT - 260, W, H)).resize((W, LIFT + 260)).filter(ImageFilter.GaussianBlur(40))
    out.paste(fundo.crop((0, 260, W, LIFT + 260)), (0, H - LIFT))
    out.paste(fundo.crop((0, 0, W, 260)), (0, H - LIFT - 260), Image.linear_gradient('L').resize((W, 260)))
    return out


G = spec.get('grade', {})
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = 1 - G.get('vign', 0.15) * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.55) / (H * 0.62)) ** 2, 0, 1.6)
TOPG = 1 - G.get('top', 0.28) * np.clip(1 - yy / 900, 0, 1) ** 1.5  # escurece o topo p/ o texto
SHADE = (VIG * TOPG)[..., None]
rng = np.random.default_rng(7)


def warm_at(t):
    ramp = G.get('warm_ramp')
    if not ramp:
        return G.get('warm', 0.03), G.get('expo', 1.0)
    for (t0, w0, e0), (t1, w1, e1) in zip(ramp, ramp[1:]):
        if t0 <= t <= t1:
            u = ease_io((t - t0) / max(1e-3, t1 - t0)); return lerp(w0, w1, u), lerp(e0, e1, u)
    return ramp[-1][1], ramp[-1][2]


def grade(img, t):
    a = np.asarray(img, np.float32) / 255
    warm, expo = warm_at(t)
    lum = (a * [0.2126, 0.7152, 0.0722]).sum(-1, keepdims=True)
    a = lum + (a - lum) * G.get('sat', 0.85)
    c = G.get('contrast', 0.95)
    a = (a - 0.5) * c + 0.5
    a = a * [1 + warm, 1 + warm * 0.35, 1 - warm * 0.9]
    lift = G.get('lift', 0.035)
    a = lift + a * (1 - lift)
    a = a * SHADE * expo
    # dip (preto) nas viradas de capítulo
    for dt in spec.get('dips', []):
        d = abs(t - dt)
        if d < 0.17:
            a = a * (d / 0.17) ** 1.2
    g = G.get('grain', 0.022)
    if g:
        n = rng.standard_normal((H // 2, W // 2, 1)).astype(np.float32)
        n = np.repeat(np.repeat(n, 2, 0), 2, 1)
        a = a + n * g
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


layers = []
YT = spec.get('ytop', 0)
for el in spec['texts']:
    el['img'], el['pad'] = make(el)
    layers.append(el)

segs = spec['segs']
clock_cache = {}
def compose(base, t):
    """põe textos, cartão e botão sobre o quadro já com cor."""
    for el in layers:
        if not (el['t0'] <= t < el['t1']):
            continue
        dt, rem = t - el['t0'], el['t1'] - t
        anim = el.get('anim', 'fade')
        img = el['img']
        if el['kind'] == 'clock':  # relógio que rola entre horários
            keys = el['keys']; txt = keys[0][1]
            for (ta, sa), (tb, sb) in zip(keys, keys[1:]):
                if t >= tb: txt = sb
                elif t >= ta and t > tb - 0.6:
                    ha = int(sa[:2]) * 60; hb = int(sb[:2]) * 60
                    m = int(lerp(ha, hb, ease((t - (tb - 0.6)) / 0.6)))
                    txt = f'{m // 60:02d}:{(m % 60) // 5 * 5:02d}'
                elif t >= ta: txt = sa
            if txt not in clock_cache:
                clock_cache[txt] = clock_img(txt, el.get('size', 190))
            img = clock_cache[txt]
            pad = 40
        else:
            pad = el['pad']
        alpha, dy, wipe = 1.0, 0, 1.0
        if el['t0'] > 0:
            if anim == 'fade':
                alpha = ease(dt / 0.55); dy = 26 * (1 - ease(dt / 0.7))
            elif anim == 'rise':  # cartão sobe de baixo
                alpha = ease(dt / 0.4); dy = 120 * (1 - ease(dt / 0.6))
            elif anim == 'wipe':
                wipe = ease_io(dt / 0.8)
            elif anim == 'draw':
                wipe = ease_io(dt / 0.9)
        if el.get('out', True) and rem < 0.35 and t < spec['dur'] - 0.05:
            alpha *= rem / 0.35
        if el['kind'] == 'glass':
            glass_on(base, el, alpha, dy + YT)
            continue
        if el['kind'] == 'bars':
            bars_on(base, el, t)
            continue
        im = img
        if wipe < 0.999:
            cw = int(im.width * wipe)
            m = Image.new('L', im.size, 0)
            ImageDraw.Draw(m).rectangle([0, 0, max(0, cw - 40), im.height], fill=255)
            for j in range(40):
                x = cw - 40 + j
                if 0 <= x < im.width:
                    ImageDraw.Draw(m).line([(x, 0), (x, im.height)], fill=int(255 * (1 - j / 40)))
            a = Image.composite(im.getchannel('A'), Image.new('L', im.size, 0), m)
            im = im.copy(); im.putalpha(a)
        if alpha < 0.999:
            a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
        x = el.get('x', 84)
        x = (W - im.width) // 2 if x == 'c' else x - pad
        base.alpha_composite(im, (int(x), int(el['y'] + YT - pad + dy)))


def preview(tempos):
    """prévias paradas (regra: aprovar com imagem antes de renderizar): PREVIEW=0,4.5,12 salva PNGs."""
    for t in tempos:
        t0 = 0.0
        for sg in segs:
            if t < t0 + sg['dur'] or sg is segs[-1]:
                k = int((t - t0) * FPS); n = max(1, int(sg['dur'] * FPS))
                fr = read_seg(sg['src'], sg['ss'] + k / FPS, 1)[0]
                u = ease_io(k / max(1, n - 1)) * 0.6 + (k / max(1, n - 1)) * 0.4
                z0, z1 = sg.get('z', [1.0, 1.06]); c0 = sg.get('c0', [SW / 2, SH / 2]); c1 = sg.get('c1', c0)
                base = grade(render_src(fr, lerp(z0, z1, u), lerp(c0[0], c1[0], u), lerp(c0[1], c1[1], u)), t).convert('RGBA')
                compose(base, t)
                base.convert('RGB').save(f"{spec['out']}_t{t:05.2f}.jpg", quality=88)
                break
            t0 += sg['dur']


if os.environ.get('PREVIEW'):
    preview([float(x) for x in os.environ['PREVIEW'].split(',')]); sys.exit(0)
enc = None if AUDIO_ONLY else subprocess.Popen(
    ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
     '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', spec['out'] + '.video.mp4'],
    stdin=subprocess.PIPE)
t_cur = 0.0; fi = 0
for sg in ([] if AUDIO_ONLY else segs):
    n = int(round((t_cur + sg['dur']) * FPS)) - int(round(t_cur * FPS))
    frames = read_seg(sg['src'], sg['ss'], n)
    z0, z1 = sg.get('z', [1.0, 1.06]); c0 = sg.get('c0', [SW / 2, SH / 2]); c1 = sg.get('c1', c0)
    for k in range(n):
        u = ease_io(k / max(1, n - 1)) * 0.6 + (k / max(1, n - 1)) * 0.4
        t = fi / FPS
        base = grade(render_src(frames[k], lerp(z0, z1, u), lerp(c0[0], c1[0], u), lerp(c0[1], c1[1], u)), t).convert('RGBA')
        compose(base, t)
        enc.stdin.write(base.convert('RGB').tobytes())
        fi += 1
    t_cur += sg['dur']
if enc:
    enc.stdin.close(); enc.wait()

# ---------- áudio: narração + trilha (piano das cenas) ----------
bed = spec['bed']
inputs = ['-i', spec['out'] + '.video.mp4', '-i', spec['narr']]
for b in bed:
    inputs += ['-i', SRC[b]]
fc = [f'[{i + 2}:a]aresample=48000,aformat=channel_layouts=stereo[b{i}]' for i in range(len(bed))]
cur = 'b0'
for i in range(1, len(bed)):
    fc.append(f'[{cur}][b{i}]acrossfade=d={spec.get("xf", 1.5)}[x{i}]'); cur = f'x{i}'
fc.append(f'[{cur}]afade=t=in:d=0.6,afade=t=out:st={spec["dur"] - 1.6}:d=1.6,volume={spec.get("amb_vol", 0.3)}[amb]')
fc.append(f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atempo={spec.get("tempo", 1.0)},'
          f'adelay={int(spec["narr_at"] * 1000)}:all=1,highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:makeup=2[nar]')
fc.append(f'[amb][nar]amix=inputs=2:normalize=0:duration=longest,apad,atrim=0:{spec["dur"]},'
          'loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '0:v', '-map', '[aout]',
                '-c:v', 'libx264', '-b:v', '5M', '-maxrate', '6.5M', '-bufsize', '9M', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(spec['dur']), spec['out']], check=True)
print('ok', spec['out'])
