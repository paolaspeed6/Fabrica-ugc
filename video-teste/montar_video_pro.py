"""Monta o vídeo final em 1080x1920 com tipografia profissional.

Uso:
    python3 montar_video_pro.py montagem.json

montagem.json:
{
  "nome": "banqueta_v1",
  "cor_destaque": "F2B66D",
  "cenas": [
    {"clipe": "cena1.mp4", "ate": 5.0, "titulo": "O detalhe que [muda] sua cozinha", "sub": ""},
    {"clipe": "cena2.mp4", "ate": 3.8, "titulo": "Courissimo + base de [ferro]", "sub": "Firme, elegante e fácil de limpar"},
    {"clipe": "cena3.mp4", "ate": 4.2, "titulo": "[93,5 cm] ideal para bancada", "sub": "", "cta": "Garanta a sua no link"}
  ]
}

- "estilo": "shopee" (padrão), "tiktok", "reels" ou "classico". Cada estilo tem
  fonte, layout, CTA e transição próprios:
    shopee: vitrine. Cartão de vidro fosco fixo embaixo (Montserrat), etiqueta,
            indicador de cena, fichas de especificação, chamadas apontando
            partes do produto, botão largo com seta, cenas deslizando de lado.
    classico: Inter Display no topo, botão arredondado, fade 0,3 s.
    tiktok: tipografia condensada grande (Bebas Neue) no centro, linhas em cascata,
            CTA branco minimalista, cortes rápidos com zoom.
    reels:  editorial, título serifado (DM Serif) embaixo à esquerda, rótulo em
            caixa alta, botão contornado, fades lentos.
- "rotulo": opcional por cena (reels e shopee), ex. "ÁREA GOURMET".
- "fichas": opcional (shopee), ex. ["93,5 cm", "Courissimo", "Ferro preto"].
- "chamadas": opcional (shopee), lista de {"texto", "x", "y", "lx", "ly"}: ponto no
  produto (x, y) e posição da etiqueta (lx, ly), em pixels de 1080x1920.
- "cor_destaque": hex, ou "auto" (padrão) para alternar entre vídeos pela PALETA.
- [palavra] entre colchetes sai na cor de destaque.
- "ate": segundos de tela de cada cena (corta o fim fraco).
- "lento": opcional, ex. 1.3 desacelera o clipe para reduzir zoom/movimento.
- Clipes 9:16 são recortados para preencher a tela; clipes quadrados ficam
  sobre um fundo de estúdio em degradê com a cor da própria foto.
- Transição suave de 0,3 s entre cenas; texto entra com fade e leve zoom.
"""
import json
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H, FPS, XF = 1080, 1920, 30, 0.3


def run(args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def dimensoes(clipe):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", str(clipe)],
                         capture_output=True, text=True, check=True).stdout.strip()
    w, h = map(int, out.split(","))
    return w, h


def normalizar(clipe, ate, saida, lento=1.0, soco=False, desloc=130, subir=0, escala=1.0):
    """lento > 1 desacelera o clipe (menos zoom/movimento no mesmo tempo de tela).
    soco=True dá um zoom rápido na entrada da cena (corte estilo TikTok).
    subir (px, clipe vertical; negativo desce): sobe a cena para o produto ficar acima da área de texto; a faixa
    que sobra embaixo recebe a própria cena desfocada, que fica sob o degradê e o cartão.
    escala < 1 reduz a cena (sobre o mesmo fundo desfocado) quando o produto é alto demais para só subir."""
    w, h = dimensoes(clipe)
    pts = f"setpts={lento}*PTS,"
    zoom = (f",scale=w='trunc({W}*(1+0.1*max(0\\,1-t/0.3))/2)*2':h=-2:eval=frame:flags=bicubic,"
            f"crop={W}:{H}" if soco else "")
    if w / h < 0.7:  # vertical: preenche a tela
        cheio = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
        if subir or escala != 1.0:
            lw = int(W * escala) // 2 * 2
            fc = (f"[0:v]{pts}{cheio},split[a][b];[b]gblur=sigma=40,eq=brightness=-0.12[fundo];"
                  f"[a]scale={lw}:-2:flags=lanczos,unsharp=5:5:0.6[c];"
                  f"[fundo][c]overlay=(W-w)/2:{-int(subir)},fps={FPS}{zoom},format=yuv420p[v]")
            args = ["-i", str(clipe), "-t", str(ate), "-filter_complex", fc, "-map", "[v]"]
        else:
            vf = f"{pts}{cheio},unsharp=5:5:0.6,fps={FPS}{zoom},format=yuv420p"
            args = ["-i", str(clipe), "-t", str(ate), "-vf", vf]
    else:  # quadrado/horizontal: estende o fundo de estúdio com degradê e bordas bem suaves
        desloc -= subir  # cena quadrada: subir também levanta o produto acima do cartão
        fundo, mascara, quadro = (saida.with_suffix(x) for x in (".fundo.png", ".mask.png", ".q.png"))
        run(["-i", str(clipe), "-frames:v", "1", str(quadro)])
        im = Image.open(quadro).convert("RGB")
        topo = im.crop((0, 0, im.width, 8)).resize((1, 1)).getpixel((0, 0))
        base = im.crop((0, im.height - 8, im.width, im.height)).resize((1, 1)).getpixel((0, 0))
        g = Image.new("RGB", (1, H))
        for y in range(H):
            k = y / (H - 1)
            g.putpixel((0, y), tuple(int(topo[i] * (1 - k) + base[i] * k) for i in range(3)))
        g.resize((W, H)).save(fundo)
        ph = round(W * h / w)
        m = Image.new("L", (W, ph), 255)
        borda = 200
        for y in range(borda):
            a = int(255 * (y / borda) ** 1.5)
            for yy in (y, ph - 1 - y):
                m.paste(a, (0, yy, W, yy + 1))
        m.save(mascara)
        fc = (f"[0:v]{pts}scale={W}:{ph}:flags=lanczos,unsharp=5:5:0.6,format=rgba[c];[2:v]format=gray[m];"
              f"[c][m]alphamerge[cm];[1:v][cm]overlay=0:(H-h)/2+{desloc}:shortest=1,fps={FPS}{zoom},format=yuv420p[v]")
        args = ["-i", str(clipe), "-loop", "1", "-i", str(fundo), "-loop", "1", "-i", str(mascara),
                "-t", str(ate), "-filter_complex", fc, "-map", "[v]"]
    run([*args, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(saida)])


def ts(seg):
    h, r = divmod(seg, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def destaque(texto, cor):
    bgr = cor[4:6] + cor[2:4] + cor[0:2]
    return re.sub(r"\[(.+?)\]", rf"{{\\c&H{bgr}&}}\1{{\\c&HFFFFFF&}}", texto)


def legenda_ass(cenas, inicios, cor, arq):
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Inter Display ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,-1,0,1,0,4,8,110,110,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    linhas = []
    anim = r"{\fad(220,160)\fscx94\fscy94\t(0,260,\fscx100\fscy100)}"
    for c, ini in zip(cenas, inicios):
        a, b = ini + 0.15, ini + c["ate"] - 0.1
        texto = destaque(c["titulo"], cor)
        if c.get("sub"):
            texto += r"\N{\fs24}\N{\fnInter Display SemiBold\fs54\c&HF2F2F2&}" + c["sub"]
        linhas.append(f"Dialogue: 1,{ts(a)},{ts(b)},Titulo,,0,0,0,,{anim}{texto}")
    arq.write_text(cab + "\n".join(linhas) + "\n", encoding="utf-8")


def degrade_topo(arq):
    g = Image.new("RGBA", (W, 900), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    for y in range(900):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * (1 - y / 900) ** 1.6)))
    g.save(arq)


def botao_cta(texto, cor, arq):
    fonte = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", 52)
    caixa = fonte.getbbox(texto)
    tw, th = caixa[2] - caixa[0], caixa[3] - caixa[1]
    pw, ph = tw + 120, 112
    img = Image.new("RGBA", (pw + 20, ph + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((10, 18, pw + 10, ph + 18), radius=ph // 2, fill=(0, 0, 0, 70))
    d.rounded_rectangle((10, 10, pw + 10, ph + 10), radius=ph // 2,
                        fill=tuple(int(cor[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    d.text((10 + (pw - tw) / 2 - caixa[0], 10 + (ph - th) / 2 - caixa[1]), texto, font=fonte, fill=(22, 22, 22))
    img.save(arq)


# Cores de destaque testadas sobre fundo escuro e claro (caramelo, menta, coral, lilás, amarelo, azul-gelo)
PALETA = ["F2B66D", "7FD8BE", "FF8A65", "C7B8FF", "FFD54F", "8FD3FF"]

FONTES = Path(__file__).parent / "fontes"


def fonte(nome, tam):
    return ImageFont.truetype(str(FONTES / nome), tam)


def rgb(cor):
    return tuple(int(cor[i:i + 2], 16) for i in (0, 2, 4))


def tokens(texto):
    """'O [ferro] preto' -> [('O', False), ('ferro', True), ('preto', False)]"""
    out = []
    for parte in re.split(r"(\[.+?\])", texto):
        for p in parte.strip("[]").split():
            if out and not parte.startswith("[") and p[0] in ",.!?;:" and out[-1][1]:
                out[-1] = (out[-1][0] + p[0], True)  # pontuação colada no destaque: "seco," sem espaço
                p = p[1:]
                if not p:
                    continue
            out.append((p, parte.startswith("[")))
    return out


def quebrar(toks, f, largura):
    linhas, atual = [], []
    for t in toks:
        if atual and f.getlength(" ".join(w for w, _ in atual + [t])) > largura:
            linhas.append(atual)
            atual = [t]
        else:
            atual.append(t)
    return linhas + ([atual] if atual else [])


def quadro_tiktok(c, cor, arq):
    """Tipografia display condensada (Bebas Neue) centralizada, linhas entrando em cascata,
    rótulo pequeno espaçado e CTA branco minimalista. Devolve camadas [(png, atraso)]."""
    camadas = []
    ft = fonte("BebasNeue-Regular.ttf", 140)
    fs = fonte("Poppins-Medium.ttf", 38)

    def camada(desenhar, atraso):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        desenhar(ImageDraw.Draw(img), ImageDraw.Draw(sombra))
        from PIL import ImageFilter
        sombra = sombra.filter(ImageFilter.GaussianBlur(14))
        final = Image.alpha_composite(sombra, img)
        png = arq.with_name(f"{arq.stem}_{len(camadas)}.png")
        final.save(png)
        camadas.append((png, atraso))

    def espacado(d, y, texto, f, fill, esp=8):
        larg = sum(f.getlength(ch) + esp for ch in texto) - esp
        x = (W - larg) / 2
        for ch in texto:
            d.text((x, y), ch, font=f, fill=fill)
            x += f.getlength(ch) + esp

    y = 290
    linhas = quebrar(tokens(c.get("titulo", "").upper()), ft, 920)
    for i, linha in enumerate(linhas):
        def lin(d, ds, linha=linha, y=y):
            lw = ft.getlength(" ".join(w for w, _ in linha))
            x = (W - lw) / 2
            for w, dest in linha:
                ds.text((x, y + 6), w, font=ft, fill=(0, 0, 0, 170))
                d.text((x, y), w, font=ft, fill=rgb(cor) if dest else (255, 255, 255))
                x += ft.getlength(w + " ")
        camada(lin, 0.09 * i)
        y += 134
    if c.get("sub"):
        def sub(d, ds, y=y):
            ds.rectangle((W / 2 - 300, y + 20, W / 2 + 300, y + 80), fill=(0, 0, 0, 120))
            d.rectangle((W / 2 - 40, y + 14, W / 2 + 40, y + 18), fill=rgb(cor))
            espacado(d, y + 34, c["sub"].upper(), fs, (255, 255, 255))
        camada(sub, 0.09 * len(linhas) + 0.05)
    if c.get("cta"):
        fc = fonte("Poppins-SemiBold.ttf", 44)
        def cta(d, ds):
            tw = fc.getlength(c["cta"])
            x0, y0, bh = (W - tw) / 2 - 60, c.get("cta_y", H - 600), 108
            ds.rounded_rectangle((x0, y0 + 10, x0 + tw + 120, y0 + bh + 10), radius=16, fill=(0, 0, 0, 150))
            d.rounded_rectangle((x0, y0, x0 + tw + 120, y0 + bh), radius=16, fill=(255, 255, 255, 255))
            d.rectangle((x0 + 28, y0 + bh / 2 - 3, x0 + 44, y0 + bh / 2 + 3), fill=rgb(cor))
            asc, desc = fc.getmetrics()
            d.text((x0 + 60, y0 + (bh - asc - desc) / 2 + 3), c["cta"], font=fc, fill=(18, 18, 18))
        camada(cta, 0.5)
    return camadas


def quadro_reels(c, cor, arq):
    """Editorial: rótulo em caixa alta, título serifado à esquerda, botão contornado; bloco embaixo."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # letras grandes (regra, 2026-10-15: "a letra está muito pequena"), com sombra para ler em qualquer fundo
    x, base, larg = 70, H - 400, 940
    ft, fi = fonte("DMSerifDisplay-Regular.ttf", 124), fonte("DMSerifDisplay-Italic.ttf", 124)
    fs, fr = fonte("Poppins-Medium.ttf", 56), fonte("Poppins-SemiBold.ttf", 44)
    blocos = []  # (altura, desenhar(y))
    if c.get("rotulo"):
        def rot(y, t=c["rotulo"].upper()):
            xx = x
            for ch in t:
                d.text((xx, y), ch, font=fr, fill=(255, 255, 255))  # branco: legível em fundo claro
                xx += fr.getlength(ch) + 6
            d.rectangle((x, y + 74, x + 110, y + 80), fill=rgb(cor))
        blocos.append((116, rot))
    linhas = quebrar(tokens(c.get("titulo", "")), ft, larg)
    def tit(y):
        for linha in linhas:
            xx = x
            for w, dest in linha:
                f = fi if dest else ft
                d.text((xx, y), w, font=f, fill=rgb(cor) if dest else (255, 255, 255))
                xx += f.getlength(w + " ")
            y += 132
    blocos.append((132 * len(linhas) + 10, tit))
    if c.get("sub"):
        for ls in quebrar(tokens(c["sub"]), fs, larg):
            blocos.append((72, lambda y, ls=ls: d.text((x, y + 6), " ".join(w for w, _ in ls), font=fs, fill=(245, 245, 245))))
    if c.get("cta"):
        fc = fonte("Poppins-SemiBold.ttf", 52)
        def cta(y):
            tw = fc.getlength(c["cta"])
            d.rounded_rectangle((x, y + 30, x + tw + 110, y + 150), radius=60, fill=(0, 0, 0, 90), outline=(255, 255, 255), width=5)
            asc, desc = fc.getmetrics()
            d.text((x + 55, y + 30 + (120 - asc - desc) / 2 + 2), c["cta"], font=fc, fill=(255, 255, 255))
        blocos.append((160, cta))
    y = base - sum(h for h, _ in blocos)
    for h, desenhar in blocos:
        desenhar(y)
        y += h
    from PIL import ImageFilter
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sombra.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda a: int(a * 0.75)))
    img = Image.alpha_composite(sombra, img)
    img.save(arq)
    return [(arq, 0)]


def montserrat(peso, tam):
    f = fonte("Montserrat.ttf", tam)
    f.set_variation_by_axes([peso])
    return f


CARD = (60, 1300, W - 60, 1640)  # x0, y0, x1, y1 do cartão de vidro (estilo shopee)


def vidro(arq_mascara, arq_borda):
    x0, y0, x1, y1 = CARD
    m = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=40, fill=255)
    m.save(arq_mascara)
    b = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.rounded_rectangle(CARD, radius=40, fill=(255, 255, 255, 22), outline=(255, 255, 255, 70), width=2)
    b.save(arq_borda)


def quadro_shopee(c, cor, arq, idx=0, total=1):
    """Vitrine: cartão de vidro fosco fixo embaixo, com etiqueta, título, indicador de
    cena e fichas de especificação; chamadas com linha apontando partes do produto."""
    camadas = []
    x0, y0, x1, y1 = CARD

    def nova():
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def salvar(img, atraso):
        png = arq.with_name(f"{arq.stem}_{len(camadas)}.png")
        img.save(png)
        camadas.append((png, atraso))

    img = nova()
    d = ImageDraw.Draw(img)
    fe, ft = montserrat(700, 28), montserrat(800, 66)
    y = y0 + 44
    if c.get("rotulo"):
        t = c["rotulo"].upper()
        lw = sum(fe.getlength(ch) + 3 for ch in t) + 40
        d.rounded_rectangle((x0 + 50, y, x0 + 50 + lw, y + 50), radius=25, fill=rgb(cor) + (255,))
        xx = x0 + 70
        for ch in t:
            d.text((xx, y + 9), ch, font=fe, fill=(24, 24, 24))
            xx += fe.getlength(ch) + 3
    # indicador de cena (bolinhas), à direita
    for i in range(total):
        cx = x1 - 60 - (total - 1 - i) * 30
        cor_b = rgb(cor) + (255,) if i == idx else (255, 255, 255, 110)
        largura = 26 if i == idx else 10
        d.rounded_rectangle((cx - largura, y + 20, cx, y + 30), radius=5, fill=cor_b)
    y += 78
    for linha in quebrar(tokens(c.get("titulo", "")), ft, x1 - x0 - 100):
        xx = x0 + 50
        for w, dest in linha:
            d.text((xx, y), w, font=ft, fill=rgb(cor) if dest else (255, 255, 255))
            xx += ft.getlength(w + " ")
        y += 80
    if c.get("fichas"):
        ff = montserrat(600, 32)
        xx, y = x0 + 50, y + 14
        for f in c["fichas"]:
            fw = ff.getlength(f) + 48
            d.rounded_rectangle((xx, y, xx + fw, y + 58), radius=29, outline=(255, 255, 255, 200), width=2)
            d.text((xx + 24, y + 11), f, font=ff, fill=(255, 255, 255))
            xx += fw + 14
    salvar(img, 0)

    for ch in c.get("chamadas", []):
        img = nova()
        d = ImageDraw.Draw(img)
        px, py, lx, ly = ch["x"], ch["y"], ch["lx"], ch["ly"]
        fc = montserrat(700, 34)
        tw = fc.getlength(ch["texto"])
        esquerda = lx < px
        bx0 = lx - tw - 56 if esquerda else lx
        d.line((px, py, lx, ly), fill=(255, 255, 255, 230), width=3)
        d.ellipse((px - 22, py - 22, px + 22, py + 22), outline=(255, 255, 255, 160), width=3)
        d.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(255, 255, 255, 255))
        d.rounded_rectangle((bx0, ly - 34, bx0 + tw + 56, ly + 34), radius=34, fill=(20, 20, 20, 200))
        d.text((bx0 + 28, ly - 22), ch["texto"], font=fc, fill=(255, 255, 255))
        salvar(img, 0.35)

    if c.get("cta"):
        img = nova()
        d = ImageDraw.Draw(img)
        fc = montserrat(800, 44)
        tw = fc.getlength(c["cta"])
        by0, bh = y1 + 26, 104
        d.rounded_rectangle((x0, by0 + 8, x1, by0 + bh + 8), radius=30, fill=(0, 0, 0, 90))
        d.rounded_rectangle((x0, by0, x1, by0 + bh), radius=30, fill=rgb(cor) + (255,))
        asc, desc = fc.getmetrics()
        tx = (W - tw - 50) / 2
        d.text((tx, by0 + (bh - asc - desc) / 2 + 2), c["cta"], font=fc, fill=(20, 20, 20))
        ax, ay = tx + tw + 22, by0 + bh / 2  # seta
        d.line((ax, ay, ax + 28, ay), fill=(20, 20, 20), width=5)
        d.line((ax + 16, ay - 12, ax + 28, ay), fill=(20, 20, 20), width=5)
        d.line((ax + 16, ay + 12, ax + 28, ay), fill=(20, 20, 20), width=5)
        salvar(img, 0.55)
    return camadas


def degrade(arq, lado, altura, alfa):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(g)
    for i in range(altura):
        a = int(alfa * (1 - i / altura) ** 1.6)
        y = i if lado == "topo" else H - 1 - i
        dr.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    g.save(arq)


ESTILOS = {
    "classico": {"xf": 0.3, "soco": False},
    "shopee": {"xf": 0.4, "soco": False, "quadro": quadro_shopee, "vidro": True,
               "transicao": "slideleft", "degrade": ("base", 900, 150), "desloc": -150},
    "tiktok": {"xf": 0.12, "soco": True, "quadro": quadro_tiktok, "degrade": ("topo", 1100, 170)},
    # tiktok com o produto abaixo do título e acima do botão (nada por cima do produto); cta_y por cena
    "tiktok_b": {"xf": 0.12, "soco": True, "quadro": quadro_tiktok, "degrade": ("topo", 950, 225), "desloc": 300},
    "reels": {"xf": 0.5, "soco": False, "quadro": quadro_reels, "degrade": ("base", 1100, 190), "desloc": -320},
    # modelos de Reels com texto em GSAP (gsap/camada_<estilo>.html); aqui só o fundo
    "reels_faixas": {"xf": 0.5, "soco": False, "quadro": quadro_reels, "degrade": ("base", 1100, 190), "desloc": -320},
    "reels_cartao": {"xf": 0.5, "soco": False, "quadro": quadro_reels, "degrade": ("base", 1100, 190), "desloc": -320},
}


def main():
    arq = Path(sys.argv[1]).resolve()
    m = json.loads(arq.read_text(encoding="utf-8"))
    cenas, cor = m["cenas"], m.get("cor_destaque", "auto")
    if cor == "auto":  # alterna a cor de destaque entre vídeos, sempre da mesma paleta profissional
        cor = PALETA[sum(map(ord, m["nome"])) % len(PALETA)]
    est = ESTILOS[m.get("estilo", "shopee")]
    XF = est["xf"]
    final = arq.parent / f"{m['nome']}.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        partes = []
        for i, c in enumerate(cenas):
            p = tmp / f"p{i}.mp4"
            normalizar(arq.parent / c["clipe"], c["ate"], p, c.get("lento", 1.0), est["soco"], est.get("desloc", 130),
                       c.get("subir", 0), c.get("escala", 1.0))
            partes.append(p)
        # transições suaves entre cenas
        inicios, t, fc, ult = [], 0.0, "", "[0:v]"
        for i, c in enumerate(cenas):
            inicios.append(max(0.0, t - (XF if i else 0)))
            if i:
                off = t - XF
                fc += f"{ult}[{i}:v]xfade=transition={est.get('transicao', 'fade')}:duration={XF}:offset={off:.3f}[x{i}];"
                ult = f"[x{i}]"
                t = off + c["ate"]
            else:
                t = c["ate"]
        n = len(partes)
        if "quadro" not in est:  # estilo clássico: legenda ASS + botão
            ass = tmp / "texto.ass"
            legenda_ass(cenas, inicios, cor, ass)
            grad = tmp / "grad.png"
            degrade_topo(grad)
            extras = ["-loop", "1", "-i", str(grad)]
            fc += f"{ult}[{n}:v]overlay=0:0:shortest=1[g];[g]subtitles={ass}[s]"
            ult, k = "[s]", n + 1
            for c, ini in zip(cenas, inicios):
                if c.get("cta"):
                    png = tmp / f"cta{k}.png"
                    botao_cta(c["cta"], cor, png)
                    t0 = ini + 0.6
                    extras += ["-loop", "1", "-i", str(png)]
                    fc += (f";[{k}:v]format=rgba,fade=in:st={t0:.2f}:d=0.3:alpha=1[b{k}];"
                           f"{ult}[b{k}]overlay=(W-w)/2:H-560:shortest=1:enable='gte(t,{t0:.2f})'[o{k}]")
                    ult, k = f"[o{k}]", k + 1
        else:  # estilos com quadro de texto desenhado (tiktok, reels)
            extras, k = [], n
            if est.get("degrade"):
                grad = tmp / "grad.png"
                degrade(grad, *est["degrade"])
                extras += ["-loop", "1", "-i", str(grad)]
                fc += f"{ult}[{k}:v]overlay=0:0:shortest=1[g]"
                ult, k = "[g]", k + 1
            else:
                fc += f"{ult}null[g]"
                ult = "[g]"
            if est.get("vidro"):
                x0, y0, x1, y1 = CARD
                masc, borda = tmp / "vidro_m.png", tmp / "vidro_b.png"
                vidro(masc, borda)
                extras += ["-loop", "1", "-i", str(masc), "-loop", "1", "-i", str(borda)]
                fc += (f";{ult}split[va][vb];[vb]crop={x1 - x0}:{y1 - y0}:{x0}:{y0},gblur=sigma=28,"
                       f"eq=brightness=-0.16:saturation=1.1,format=rgba[vc];[{k}:v]format=gray[vm];"
                       f"[vc][vm]alphamerge[vd];[va][vd]overlay={x0}:{y0}:shortest=1[ve];"
                       f"[ve][{k + 1}:v]overlay=0:0:shortest=1[vf]")
                ult, k = "[vf]", k + 2
            # sem_texto: só cenas, degradê e vidro; o texto vem da camada GSAP (gsap/montar_gsap.py)
            for i, (c, ini) in enumerate([] if m.get("sem_texto") else zip(cenas, inicios)):
                t1 = ini + c["ate"] - (0.05 if est["soco"] else 0.2)
                d = 0.25 if est["soco"] else 0.45
                sobe = 28 if est["soco"] else 40
                kw = {"idx": i, "total": len(cenas)} if est["quadro"] is quadro_shopee else {}
                for png, atraso in est["quadro"](c, cor, tmp / f"q{i}.png", **kw):
                    t0 = ini + (0.12 if est["soco"] else 0.25) + atraso
                    extras += ["-loop", "1", "-i", str(png)]
                    fc += (f";[{k}:v]format=rgba,fade=in:st={t0:.2f}:d={d}:alpha=1[t{k}];"
                           f"{ult}[t{k}]overlay=0:'{sobe}*pow(max(0,1-(t-{t0:.2f})/{d}),2)':eval=frame:shortest=1:"
                           f"enable='between(t,{t0:.2f},{t1:.2f})'[o{k}]")
                    ult, k = f"[o{k}]", k + 1
        fc += f";{ult}null[v]"
        entradas = [a for p in partes for a in ("-i", str(p))] + extras
        run([*entradas, "-filter_complex", fc, "-map", "[v]", "-t", f"{t:.3f}", "-c:v", "libx264",
             "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
             "-movflags", "+faststart", str(final)])
    print(f"Pronto: {final}")


if __name__ == "__main__":
    main()
