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
    'dm_md': (FD + 'DMSans.ttf', 'Medium'), 'dm_sb': (FD + 'DMSans.ttf', 'SemiBold'), 'dm_b': (FD + 'DMSans.ttf', 'Bold'),
    'mont_md': (FD + 'Montserrat.ttf', 'Medium'), 'mont_sb': (FD + 'Montserrat.ttf', 'SemiBold'), 'mont_b': (FD + 'Montserrat.ttf', 'Bold'), 'mont_xb': (FD + 'Montserrat.ttf', 'ExtraBold'),
    'bebas': FD + 'BebasNeue-Regular.ttf',
    'play': FD + 'PlayfairDisplay.ttf', 'play_it': FD + 'PlayfairDisplay-Italic.ttf', 'dm': FD + 'DMSans.ttf',
}
spec = json.load(open(sys.argv[1]))
# modo natural (a dona, 2026-10-21): sem filtro/grão/vinheta, take lido em resolução cheia, bitrate alto,
# transições profissionais nos cortes (spec['trans'] = [[t, 'whip'|'zoom'|'whipv'], ...])
NATURAL = bool(spec.get('natural'))
RS = 1.5 if NATURAL else 1.0  # leitura em 1080x1920; coordenadas continuam no espaço 720x1280
VBR = ['-b:v', '14M', '-maxrate', '18M', '-bufsize', '24M'] if NATURAL else ['-b:v', '5M', '-maxrate', '6.5M', '-bufsize', '9M']
SRC = spec['src']
INK = tuple(spec.get('ink', (255, 255, 255)))
ACC = tuple(spec.get('accent', (214, 168, 120)))  # cor de destaque das palavras entre [ ]
AUDIO_ONLY = os.environ.get('AUDIO_ONLY') == '1'


_fcache = {}


def font(n, s):
    """nome -> fonte; entradas (arquivo, 'Peso') escolhem o peso de uma fonte variável."""
    if (n, s) not in _fcache:
        v = FONTS[n]
        if isinstance(v, tuple):
            f = ImageFont.truetype(v[0], s); f.set_variation_by_name(v[1])
        else:
            f = ImageFont.truetype(v, s)
        _fcache[(n, s)] = f
    return _fcache[(n, s)]


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
    if k == 'button':  # CTA: 'solid' (cheio), 'outline' (contorno fino) ou 'link' (só texto sublinhado); ícone 'cart'/'arrow'
        f = font(el.get('base', 'pop_sb'), el.get('size', 46))
        txt = el['text']; h = el.get('h', 116); estilo = el.get('style', 'solid'); icon = el.get('icon', 'arrow')
        tc = tuple(el.get('text_color', (22, 20, 18)))
        tw = f.getlength(txt); iw = 0 if not icon else (int(h * 0.42) + 22)
        w = el.get('w') or int(tw + iw + (0 if estilo == 'link' else h))
        img = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
        b = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        if estilo == 'solid':
            d.rounded_rectangle([0, 0, w - 1, h - 1], radius=el.get('r', h // 2), fill=tuple(el.get('fill', ACC)) + (255,))
        elif estilo == 'outline':
            if el.get('fill'):
                d.rounded_rectangle([0, 0, w - 1, h - 1], radius=el.get('r', h // 2), fill=tuple(el['fill']))
            d.rounded_rectangle([1, 1, w - 2, h - 2], radius=el.get('r', h // 2), outline=tc, width=el.get('lw', 3))
        x0 = (w - tw - iw) / 2 if estilo != 'link' else 0
        if icon == 'cart':  # carrinho em traço fino, desenhado (sem emoji)
            s_ = int(h * 0.42); cx, cy = x0, h / 2 - s_ / 2; lw = max(3, s_ // 9)
            d.line([(cx, cy + s_ * .08), (cx + s_ * .2, cy + s_ * .08), (cx + s_ * .34, cy + s_ * .66), (cx + s_ * .9, cy + s_ * .66),
                    (cx + s_, cy + s_ * .24), (cx + s_ * .27, cy + s_ * .24)], fill=tc, width=lw, joint='curve')
            for wx in (.42, .82):
                r_ = s_ * .07; d.ellipse([cx + s_ * wx - r_, cy + s_ * .86 - r_, cx + s_ * wx + r_, cy + s_ * .86 + r_], fill=tc)
            x0 += iw
        d.text((x0, h / 2), txt, font=f, fill=tc, anchor='lm')
        if icon == 'arrow':
            ax = x0 + tw + 22; ay = h / 2; lw = max(3, h // 30)
            d.line([(ax, ay), (ax + 30, ay)], fill=tc, width=lw)
            d.line([(ax + 18, ay - 11), (ax + 30, ay), (ax + 18, ay + 11)], fill=tc, width=lw, joint='curve')
        if estilo == 'link':  # sublinhado fino
            d.line([(0, h / 2 + el.get('size', 46) * .72), (w - (0 if icon != 'arrow' else 0), h / 2 + el.get('size', 46) * .72)], fill=tc, width=2)
        img.alpha_composite(b, (40, 40))
        return (soft_shadow(img, 18, 90, 8) if el.get('shadow', True) else img), 40
    if k == 'band':  # faixa: texto sobre fundo colorido, cantos levemente arredondados (gira com 'rotate')
        f = font(el.get('base', 'pop_b'), el.get('size', 76)); txt = el['text']
        px, py = el.get('px', 30), el.get('py', 14)
        bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w, h = tw + 2 * px, th + 2 * py
        img = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        d.rounded_rectangle([40, 40, 40 + w, 40 + h], radius=el.get('r', 10), fill=tuple(el.get('fill', ACC)))
        d.text((40 + px - bb[0], 40 + py - bb[1]), txt, font=f, fill=tuple(el.get('color', (255, 255, 255))))
        return soft_shadow(img, 16, 80, 6), 40
    if k == 'rect':  # painel/faixa sólida (cor com alfa), cantos 'all'/'top'/'none'; aceita 'rotate'
        w, h, r = el['w'], el['h'], el.get('r', 0)
        img = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        fill = tuple(el.get('fill', (20, 18, 16, 235)))
        cantos = el.get('corners', 'all')
        if r and cantos == 'top':
            d.rounded_rectangle([40, 40, 40 + w - 1, 40 + h + r], radius=r, fill=fill)
            img = img.crop((0, 0, w + 80, h + 80))
        elif r:
            d.rounded_rectangle([40, 40, 40 + w - 1, 40 + h - 1], radius=r, fill=fill)
        else:
            d.rectangle([40, 40, 40 + w - 1, 40 + h - 1], fill=fill)
        return (soft_shadow(img, el.get('blur', 24), el.get('sh', 70), 6) if el.get('shadow', False) else img), 40
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
    c = tuple(el.get('color', (255, 255, 255)))
    for i in range(n):
        a, b = cuts[i], cuts[i + 1]; fill = min(1, max(0, (t - a) / (b - a)))
        xa = x0 + i * (w + gap)
        d.rounded_rectangle([xa, y, xa + w, y + 6], radius=3, fill=c + (70,))
        if fill > 0:
            d.rounded_rectangle([xa, y, xa + max(6, w * fill), y + 6], radius=3, fill=c + (235,))
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
                          '-vf', f'scale={int(SW*RS)}:{int(SH*RS)}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],  # qualquer resolução vira 720x1280
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, int(SH*RS), int(SW*RS), 3)
    while len(fr) < n:
        fr = np.concatenate([fr, fr[-1:]])
    return fr


SHIFTX = spec.get('shiftx', 0)
LIFT = spec.get('lift', 0)  # sobe o vídeo N px; a faixa de baixo vira o próprio vídeo desfocado (fica atrás do cartão)


def render_src(frame, z, cx, cy, sx=None):
    w, h = SW / z, SH / z
    x0 = min(max(cx - w / 2, 0), SW - w); y0 = min(max(cy - h / 2, 0), SH - h)
    img = Image.fromarray(frame).resize((W, H), Image.LANCZOS, box=(x0 * RS, y0 * RS, (x0 + w) * RS, (y0 + h) * RS))
    SHIFTX = globals()['SHIFTX'] if sx is None else sx
    if SHIFTX:  # produto alto no meio: empurra o vídeo para o lado; a sobra vira a borda desfocada (parede)
        out = Image.new('RGB', (W, H)); out.paste(img, (SHIFTX, 0))
        faixa = abs(SHIFTX)
        borda = img.crop((0, 0, 120, H) if SHIFTX > 0 else (W - 120, 0, W, H)).resize((faixa + 120, H)).filter(ImageFilter.GaussianBlur(30))
        if SHIFTX > 0:
            out.paste(borda.crop((0, 0, faixa, H)), (0, 0))
            out.paste(borda.crop((faixa, 0, faixa + 120, H)), (faixa, 0), Image.linear_gradient('L').rotate(-90).resize((120, H)))
        else:
            out.paste(borda.crop((120, 0, faixa + 120, H)), (W - faixa, 0))
        img = out
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


def trans_fx(img, t):
    """transição no corte: chicote (whip) com borrão de movimento ou zoom punch; o vídeo de saída sai, o de entrada chega."""
    for tc, kind in spec.get('trans', []):
        d = t - tc; R = 0.16
        if abs(d) >= R: continue
        u = 1 - abs(d) / R; u = u * u  # força máxima no corte
        sgn = -1 if d < 0 else 1  # antes do corte sai, depois entra
        a = np.asarray(img, np.float32)
        if kind in ('whip', 'whipv'):
            ax = 1 if kind == 'whip' else 0
            off = int((W if ax else H) * 0.35 * u) * (1 if d < 0 else -1) * -1
            k = max(1, int(70 * u))
            acc = np.zeros_like(a)
            for i in range(8):
                acc += np.roll(a, off + int((i - 3.5) / 3.5 * k), axis=ax)
            a = acc / 8
        else:  # zoom punch: sai crescendo, entra encolhendo, com borrão radial
            z = 1 + 0.22 * u
            acc = np.zeros_like(a)
            for i in range(6):
                zi = z * (1 + 0.018 * u * i)
                ww, hh = W / zi, H / zi
                acc += np.asarray(img.resize((W, H), Image.BILINEAR, box=((W - ww) / 2, (H - hh) / 2, (W + ww) / 2, (H + hh) / 2)), np.float32)
            a = acc / 6
        img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return img


def grade(img, t):
    img = trans_fx(img, t)
    if NATURAL:  # sem filtro: só os mergulhos ao preto, se houver
        dd = [abs(t - dt) for dt in spec.get('dips', []) if abs(t - dt) < 0.17]
        if not dd: return img
        return Image.fromarray((np.asarray(img, np.float32) * (min(dd) / 0.17) ** 1.2).astype(np.uint8))
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
            rola = all(len(k[1]) == 5 and k[1][2] == ':' for k in keys)  # horários rolam; palavras só trocam
            for (ta, sa), (tb, sb) in zip(keys, keys[1:]):
                if not rola:
                    if t >= tb: txt = sb
                    continue
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
        if el.get('rotate'):  # faixas inclinadas (modelo Kevin 'faixas')
            im = im.rotate(el['rotate'], resample=Image.BICUBIC, expand=True)
        x = el.get('x', 84)
        x = (W - im.width) // 2 if x == 'c' else x - pad
        base.alpha_composite(im, (int(x), int(el['y'] + YT - pad + dy)))


MARCA = spec.get('marca', 'Aguiiar Lar')  # marca d'água da conta da dona (2026-10-18); '' desliga
_marca_cache = {}


def marca_on(base, t):
    """assinatura "Aguiiar Lar" fixa, centralizada no topo, igual em todos os vídeos (a dona, 2026-10-18):
    Playfair itálico pequeno, branco translúcido com sombra suave, acima das barrinhas e dos textos."""
    if not MARCA:
        return
    if 'p' not in _marca_cache:
        f = font('play_it', 36)
        tw = int(f.getlength(MARCA)) + 40
        pq = Image.new('RGBA', (tw, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(pq)
        d.text((20, 35), MARCA, font=f, fill=(255, 255, 255, 170), anchor='lm')
        _marca_cache['p'] = soft_shadow(pq, 8, 90, 2)
    m = _marca_cache['p']
    base.alpha_composite(m, ((W - m.width) // 2, spec.get('marca_y', 30)))


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
                base = grade(render_src(fr, lerp(z0, z1, u), lerp(c0[0], c1[0], u), lerp(c0[1], c1[1], u), sg.get('shiftx')), t).convert('RGBA')
                compose(base, t); marca_on(base, t)
                base.convert('RGB').save(f"{spec['out']}_t{t:05.2f}.jpg", quality=88)
                break
            t0 += sg['dur']


if os.environ.get('PREVIEW'):
    preview([float(x) for x in os.environ['PREVIEW'].split(',')]); sys.exit(0)
enc = None if AUDIO_ONLY else subprocess.Popen(
    ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
     '-c:v', 'libx264', '-crf', '12' if NATURAL else '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', spec['out'] + '.video.mp4'],
    stdin=subprocess.PIPE)
t_cur = 0.0; fi = 0
for sg in ([] if AUDIO_ONLY else segs):
    n = int(round((t_cur + sg['dur']) * FPS)) - int(round(t_cur * FPS))
    frames = read_seg(sg['src'], sg['ss'], n)
    z0, z1 = sg.get('z', [1.0, 1.06]); c0 = sg.get('c0', [SW / 2, SH / 2]); c1 = sg.get('c1', c0)
    for k in range(n):
        u = ease_io(k / max(1, n - 1)) * 0.6 + (k / max(1, n - 1)) * 0.4
        t = fi / FPS
        base = grade(render_src(frames[k], lerp(z0, z1, u), lerp(c0[0], c1[0], u), lerp(c0[1], c1[1], u), sg.get('shiftx')), t).convert('RGBA')
        compose(base, t); marca_on(base, t)
        enc.stdin.write(base.convert('RGB').tobytes())
        fi += 1
    t_cur += sg['dur']
if enc:
    enc.stdin.close(); enc.wait()

# ---------- áudio: narração + trilha (piano das cenas) ----------
bed = spec['bed']
if not spec.get('narr'):  # sem voz (a dona, 2026-10-18): só a música calma, mais alta, com fade
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', spec['out'] + '.video.mp4', '-i', SRC.get(bed[0], bed[0]), '-filter_complex',
                    f'[1:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.8,afade=t=out:st={spec["dur"] - 1.8}:d=1.8,'
                    f'apad,atrim=0:{spec["dur"]},loudnorm=I=-16:TP=-1.5:LRA=11[aout]', '-map', '0:v', '-map', '[aout]',
                    '-c:v', 'libx264', *VBR, '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(spec['dur']), spec['out']], check=True)
    print('ok', spec['out']); sys.exit(0)
inputs = ['-i', spec['out'] + '.video.mp4', '-i', spec['narr']]
for b in bed:  # cena do próprio produto (letra) ou arquivo de trilha (caminho)
    inputs += ['-i', SRC.get(b, b)]
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
                '-c:v', 'libx264', *VBR, '-preset', 'slow', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(spec['dur']), spec['out']], check=True)
print('ok', spec['out'])
