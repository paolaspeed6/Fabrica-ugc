"""Gera referencias/modelos-layout/Modelos_de_layout_Fabrica_UGC.pdf (os 3 modelos aprovados em 2026-10-18).
Rodar da raiz do repo depois de mudar um modelo: python3 video-teste/luxo/gerar_pdf_modelos.py"""
import subprocess, tempfile, os
from PIL import Image, ImageDraw, ImageFont
F = 'video-teste/fontes/'
P = 'trabalhos/cadeira-poltrona-bege'
S = tempfile.mkdtemp() + '/'
for t in (0.3, 6, 13):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f'{P}/poltrona_lux3_umdia.mp4', '-frames:v', '1', '-vf', 'scale=360:640', f'{S}a_{t}.png'], check=True)
for t in (0.3, 7, 13.5):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f'{P}/out2/poltrona_c_direto.mp4', '-frames:v', '1', '-vf', 'scale=360:640', f'{S}c_{t}.png'], check=True)


def fnt(n, s, w=None):
    f = ImageFont.truetype(F + n, s)
    if w:
        f.set_variation_by_name(w)
    return f


SER = lambda s: fnt('DMSerifDisplay-Regular.ttf', s)
SUB = fnt('DMSans.ttf', 30, 'Medium'); TX = fnt('DMSans.ttf', 26, 'Regular'); EB = fnt('DMSans.ttf', 22, 'SemiBold')
W, H = 1240, 1754; BG = (246, 243, 238); INK = (30, 26, 22); MUT = (110, 100, 90); ACC = (150, 98, 52)


def wrap(d, txt, f, x, y, maxw, cor=INK, lh=1.45):
    for par in txt.split('\n'):
        line = ''
        for w in par.split(' '):
            t = (line + ' ' + w).strip()
            if d.textlength(t, font=f) > maxw and line:
                d.text((x, y), line, font=f, fill=cor); y += int(f.size * lh); line = w
            else:
                line = t
        d.text((x, y), line, font=f, fill=cor); y += int(f.size * lh)
    return y


def strip(paths, h=560):
    ims = [Image.open(p).convert('RGB') for p in paths]
    ims = [i.resize((int(i.width * h / i.height), h)) for i in ims]
    out = Image.new('RGB', (sum(i.width for i in ims) + 24 * (len(ims) - 1), h), BG); x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + 24
    return out


def page(n, nome, apelido, img, itens):
    pg = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(pg)
    d.text((80, 80), f'MODELO {n}', font=EB, fill=ACC)
    d.text((80, 116), nome, font=SER(64), fill=INK)
    d.text((80, 200), apelido, font=SUB, fill=MUT)
    if img.width > W - 160:
        img = img.resize((W - 160, int(img.height * (W - 160) / img.width)))
    pg.paste(img, ((W - img.width) // 2, 270)); y = 270 + img.height + 50
    for k, v in itens:
        d.text((80, y), k.upper(), font=EB, fill=ACC); y += 36
        y = wrap(d, v, TX, 80, y, W - 160) + 18
    return pg


capa = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(capa)
d.text((80, 140), 'FÁBRICA UGC · PADRÃO 2026-10-18', font=EB, fill=ACC)
d.text((80, 190), 'Modelos de layout', font=SER(96), fill=INK)
y = wrap(d, 'Cada produto sai em 3 vídeos de 15 s (9:16, 1080x1920), um em cada modelo abaixo. As 3 versões começam cada uma com '
         'um take diferente. Textos só com qualidades reais do produto (na dúvida, simplificar). Gancho já visível no 1º quadro. '
         'Narração calma na voz Kore (Gemini) + trilha de piano.', SUB, 80, 340, W - 160) + 30
for n, t, dsc in [(1, 'Um dia com ela', 'serifa elegante, relógio ou momentos que rolam, luz do dia virando noite'),
                  (2, 'Faixas moderno', 'faixas levemente inclinadas embaixo, escura + cor do produto'),
                  (3, 'Direto ao ponto', 'frase simples, "Olha o que ela tem:" com lista de checks, ver o preço')]:
    d.text((80, y), f'{n}.  {t}', font=SER(48), fill=INK); y += 62
    y = wrap(d, dsc, TX, 128, y, W - 220, MUT) + 22
pags = [capa,
 page(1, 'Um dia com ela', 'Opção A · modelo padrão', strip([S + 'a_0.3.png', S + 'a_6.png', S + 'a_13.png']), [
  ('Tipografia', 'Caladea (serifa) branca; destaque em itálico, não em cor. Rótulos pequenos em caixa alta espaçada (Liberation Sans). Texto à esquerda (x=84), faixa do topo; nunca sobre o produto.'),
  ('Roteiro', 'Gancho (0–2,9 s) → 3 momentos com horário grande que rola (08:00 → 15:00 → 22:00) ou palavra curta para produtos sem manhã/tarde/noite (Café · Almoço · Jantar; Ao sair · Ao chegar) → CTA "Disponível no link / Leve pra casa." com linha fina.'),
  ('Movimento e cor', 'Mergulho rápido ao preto (0,17 s) em cada virada; a luz esquenta e escurece do dia para a noite; zoom lento contínuo; grão fino.'),
  ('Produto alto', 'Vídeo deslocado para o lado (a sobra vira parede desfocada) para o texto não cobrir o produto.')]),
 page(2, 'Faixas moderno', 'Opção B · modelo Kevin "faixas" modernizado', Image.open('referencias/exemplos-layout/ex_2a_faixas.jpg').convert('RGB'), [
  ('Tipografia', 'Poppins Bold dentro de 2 faixas inclinadas 2°: a 1ª escura (quase preta), a 2ª na cor do produto com letra escura. Rótulo acima em Poppins SemiBold caixa alta espaçada; subtítulo Poppins Regular.'),
  ('Posição', 'Embaixo; o vídeo sobe 300 px para o produto ficar acima das faixas (a faixa de baixo vira o próprio vídeo desfocado).'),
  ('Roteiro', '3 cenas (gancho, detalhe, onde usar), cada uma com suas duas linhas; na última, CTA moderno.'),
  ('CTA', 'Contorno fino branco sobre fundo levemente escuro, ícone de carrinho desenhado em traço e "Toque no carrinho" (DM Sans). Sem pílula colorida, sem seta grossa, sem emoji.')]),
 page(3, 'Direto ao ponto', 'Opção C · persuasivo e fácil para o público leigo', strip([S + 'c_0.3.png', S + 'c_7.png', S + 'c_13.5.png']), [
  ('Tipografia', 'DM Serif Display branca centralizada (destaque em itálico); lista e rótulos em DM Sans.'),
  ('Roteiro', 'Barrinhas de progresso no topo (como Stories) → gancho em frase simples → "Olha o que ela tem:" + 3 itens com check desenhado entrando junto com a voz → onde usar → "Toque no carrinho e veja o preço." + botão "Ver o preço".'),
  ('Regra dos itens', 'Só qualidades reais e comprovadas pelo anúncio. Característica neutra (ex.: "linhas retas") não entra. Na dúvida, simplificar.'),
  ('Voz', 'Calma e calorosa, como uma amiga recomendando; nada agressivo.')]),
]
out = 'referencias/modelos-layout/Modelos_de_layout_Fabrica_UGC.pdf'
pags[0].save(out, save_all=True, append_images=pags[1:], resolution=150)
print(out)
