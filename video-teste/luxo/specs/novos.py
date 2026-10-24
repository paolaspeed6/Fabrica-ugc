"""Opções B e C do padrão de 3 vídeos por produto (a dona, 2026-10-18; memoria/colecao-luxo.md).
B = shopee3 do Kevin modernizado: cartão de vidro fosco embaixo, Poppins, palavra de destaque em [ ], CTA em pílula.
C = Revista: título "CASA" espaçado no topo, Playfair centralizado, detalhes como notas numeradas.
uso: from novos import opcao_b, opcao_c  (ver produtos.py)
"""
from common import *

FMT_B = dict(sat=0.92, warm=0.015, contrast=1.04, lift=0.02, vign=0.10, grain=0.010, top=0.10)
FMT_C = dict(sat=0.78, warm=0.04, contrast=0.96, lift=0.045, vign=0.22, grain=0.024, top=0.34)

BRANCO = (255, 255, 255)
SUAVE = (226, 222, 216)


def _txt(kind, lines, t0, t1, y, **k):
    return dict(kind=kind, lines=lines if isinstance(lines, list) else [lines], t0=t0, t1=t1, y=y, **k)


def opcao_b(nome, p, segs, narr, narr_at=0.4, bed=None, cuts=(0, 5, 10, 15), tempo=1.0):
    """p: kicker, cenas=[(titulo_linhas, sub)]*3 (a 3ª é o CTA), cta, accent. Cartão fixo; textos trocam a cada cena."""
    Y, Hc = 1400, 420
    tx = [dict(kind='glass', y=Y, h=Hc, t0=0, t1=15, out=False)]
    for i, (tit, sub) in enumerate(p['cenas']):
        a, b = cuts[i], cuts[i + 1]
        fim = i == 2
        tx += [
            _txt('eyebrow', p['kicker'], a, b, Y + 30, base='pop_sb', size=28, track=6, color=p['accent'], shadow=False, x=104, out=not fim),
            _txt('eyebrow', f'0{i + 1} / 03', a, b, Y + 30, base='pop', size=26, track=4, color=SUAVE, shadow=False, x=846, out=not fim),
            _txt('title', tit, a + (0 if i == 0 else 0.15), b, Y + 80, base='pop_b', it='pop_b', size=80, spacing=1.1,
                 shadow=False, x=104, out=not fim),
        ]
        if sub and not fim:
            tx.append(_txt('body', sub, a + (0 if i == 0 else 0.3), b, Y + 80 + len(tit) * 88 + 14, base='pop_r', it='pop_r', size=38,
                           color=SUAVE, shadow=False, x=104))
    tx.append(dict(kind='button', text=p['cta'], t0=cuts[2] + 0.35, t1=15, y=Y + 80 + len(p['cenas'][2][0]) * 88 + 22,
                   x=104, w=872, h=112, size=42, fill=p['accent'], anim='rise', out=False))
    save2(nome, narr=narr, narr_at=narr_at, tempo=tempo, bed=bed or [], grade=FMT_B, lift=260, accent=p['accent'], segs=segs, texts=tx)


def opcao_c(nome, p, segs, narr, narr_at=0.6, bed=None, tempo=1.0):
    """p: edicao, gancho=[linhas], notas=[(n, texto)]*3, cta. Tudo centralizado no topo (o produto fica livre)."""
    tx = [
        _txt('title', 'CASA', 0, 15, 70, base='play', it='play', size=96, align='center', x='c', track=38, out=False),
        dict(kind='line', len=150, t0=0, t1=15, y=196, x='c', out=False),
        _txt('eyebrow', p['edicao'], 0, 15, 236, base='dm', size=26, track=8, align='center', x='c', out=False),
        _txt('title', p['gancho'], 0, 4.6, 330, base='play', it='play_it', size=92, spacing=1.08, align='center', x='c'),
    ]
    t = [4.7, 7.3, 9.9]
    for (n, nota), a, b in zip(p['notas'], t, t[1:] + [12.0]):
        tx += [_txt('title', n, a, b, 330, base='play_it', it='play_it', size=120, align='center', x='c'),
               _txt('body', nota, a + 0.2, b, 486, base='play', it='play_it', size=64, spacing=1.12, align='center', x='c')]
    tx += [_txt('eyebrow', 'Disponível no link', 12.1, 15, 340, base='dm', size=30, track=9, align='center', x='c', out=False),
           _txt('title', p['cta'], 12.3, 15, 396, base='play', it='play_it', size=96, spacing=1.06, align='center', x='c',
                anim='wipe', out=False)]
    save2(nome, narr=narr, narr_at=narr_at, tempo=tempo, bed=bed or [], grade=FMT_C, segs=segs, texts=tx)


def save2(name, **sp):
    sp['src'] = SRC; sp['out'] = f'{S}/out2/{name}.mp4'; sp.setdefault('dur', 15.0)
    tot = sum(s['dur'] for s in sp['segs']); assert abs(tot - 15) < 1e-6, (name, tot)
    os.makedirs(f'{S}/specs', exist_ok=True); os.makedirs(f'{S}/out2', exist_ok=True)
    json.dump(sp, open(f'{S}/specs/{name}.json', 'w'), ensure_ascii=False, indent=1)


FMT_D = dict(sat=0.9, warm=0.025, contrast=1.02, lift=0.03, vign=0.18, grain=0.014, top=0.40)


def _sem_italico(linhas):
    """fontes sem itálico: *palavra* vira [palavra] (destaque na cor)."""
    return [l.replace('*', '\x00').replace('\x00', '[', 1).replace('\x00', ']', 1) if l.count('*') >= 2 else l for l in linhas]


CTA_MODERNO = dict(style='outline', icon='cart', text_color=(255, 255, 255), fill=(20, 18, 16, 70), lw=2,
                   base='dm_md', size=46, h=110)


def opcao_d(nome, p, segs, narr, narr_at=0.3, bed=None, tempo=1.0, cuts=(0, 3.2, 9.4, 12.0, 15), fonte=None):
    """"Direto ao ponto" (substitui a Revista, 2026-10-18: persuasivo e fácil para o público leigo).
    p: eyebrow, gancho=[linhas], itens=[3 textos], onde=[linhas], accent. Barrinhas tipo Stories no topo;
    frase simples -> "Olha o que ela tem:" + lista com ✓ -> onde usar -> "Toque no carrinho e veja o preço".
    fonte: None = DM Serif (1ª versão); 'dm' = DM Sans SemiBold (padrão aprovado: diferente da serifa da opção A).
    ITENS: só qualidades de verdade (regra 11 em agentes/regras_de_erros.md): nada de 'linhas retas' e afins."""
    a, b, c, d, e = cuts
    if fonte:
        big = dict(base=fonte + '_sb', it=fonte + '_sb', align='center', x='c', spacing=1.08)
        conv, tam = _sem_italico, 0.84
    else:
        big = dict(base='dms', it='dms_it', align='center', x='c', spacing=1.04)
        conv, tam = (lambda l: l), 1.0
    lado = dict(align='center', x='c')
    if p.get('esq'):  # produto alto deslocado para a direita (shiftx): texto alinhado à esquerda
        big.update(align='left', x=84); lado = dict(align='left', x=84); tam *= p.get('escala', 0.86)
    tem = p.get('tem', '*ela tem:*')
    tx = [dict(kind='bars', cuts=list(cuts), t0=0, t1=15, y=96, out=False),
          _txt('eyebrow', p['eyebrow'], a, b, 150, base=(fonte + '_md') if fonte else 'dm', size=30, track=7, **lado),
          _txt('title', conv(p['gancho']), a, b, 206, size=int(108 * tam), **big),
          _txt('title', conv(['Olha o que', tem]), b, c, 150, size=int(100 * tam), **big)]
    for i, item in enumerate(p['itens']):
        ti = p['itens_t'][i] if p.get('itens_t') else b + 1.2 + i * 1.5  # entra junto com a voz
        tx.append(dict(kind='check', text=item, t0=ti, t1=c, y=392 + i * 124, x=90, size=p.get('item_size', 58),
                       fill=p['accent'], base=(fonte + '_md') if fonte else 'dm'))
    tx += [_txt('title', conv(p['onde']), c, d, 206, size=int(104 * tam), **big),
           _txt('title', conv(['Toque no carrinho', '*e veja o preço.*']), d, e, 170, size=int(96 * tam), out=False, **big)]
    if fonte:
        tx.append(dict(kind='button', text='Ver o preço', t0=d + 0.4, t1=e, y=392, x='c', anim='fade', out=False, **CTA_MODERNO))
    else:
        tx.append(dict(kind='button', text='Ver o preço', t0=d + 0.4, t1=e, y=400, x=lado['x'], w=600, h=112, size=44,
                       fill=p['accent'], text_color=(255, 255, 255), anim='rise', out=False))
    save2(nome, narr=narr, narr_at=narr_at, tempo=tempo, bed=bed or [], grade=FMT_D, accent=p['accent'], segs=segs, texts=tx,
          **({'shiftx': p['shiftx']} if p.get('shiftx') else {}))


def opcao_b_faixas(nome, p, segs, narr, narr_at=0.4, bed=None, cuts=(0, 5, 10, 15), tempo=1.0):
    """Opção 2, candidata "Faixas" do modelo Kevin, modernizada: 2 faixas levemente inclinadas (escura + cor do
    produto) com Poppins Bold, rótulo espaçado acima, subtítulo leve, CTA em contorno fino com carrinho em traço."""
    tx = []
    Y = p.get('y', 1300)  # 2026-10-20: 230 = faixas no topo, dentro da área livre da Shopee/Reels
    for i, (l1, l2, sub) in enumerate(p['cenas']):
        a, b = cuts[i], cuts[i + 1]; fim = i == 2
        tx += [_txt('eyebrow', p['kicker'], a, b, Y, base='pop_sb', size=28, track=7, x=78, out=not fim),
               dict(kind='band', text=l1, t0=a, t1=b, y=Y + 62, x=70, rotate=2, size=66, fill=(22, 20, 18, 238), out=not fim),
               dict(kind='band', text=l2, t0=a + (0 if i == 0 else 0.12), t1=b, y=Y + 166, x=70, rotate=2, size=66,
                    fill=tuple(p['accent']) + (255,), color=(26, 22, 18), out=not fim)]
        if sub and not fim:
            tx.append(_txt('body', sub, a + (0 if i == 0 else 0.3), b, Y + 300, base='pop_r', it='pop_r', size=38, x=82))
    tx.append(dict(kind='button', text=p['cta'], t0=cuts[2] + 0.4, t1=15, y=p.get('cta_y', Y + 304), x=p.get('cta_x', 70), anim='fade', out=False, **p.get('cta_estilo', CTA_MODERNO)))
    save2(nome, narr=narr, narr_at=narr_at, tempo=tempo, bed=bed or [], grade=FMT_B, lift=p.get('lift', 300), accent=p['accent'], segs=segs,
          texts=tx, **({'shiftx': p['shiftx']} if p.get('shiftx') else {}))


def opcao_b_topo(nome, p, segs, narr, narr_at=0.4, bed=None, cuts=(0, 5, 10, 15), tempo=1.0):
    """Opção 2, candidata "Letras grandes no topo" do modelo Kevin, modernizada: Bebas Neue grande centralizada
    (linha 2 na cor do produto), linha fina, subtítulo DM Sans espaçado, CTA em link sublinhado com carrinho em traço."""
    tx = []
    for i, (l1, l2, sub) in enumerate(p['cenas']):
        a, b = cuts[i], cuts[i + 1]; fim = i == 2
        tx += [_txt('title', [l1.upper(), '[' + l2.upper() + ']'], a, b, 150, base='bebas', it='bebas', size=128, spacing=0.94,
                    align='center', x='c', out=not fim),
               dict(kind='line', len=120, t0=a, t1=b, y=412, x='c', out=not fim)]
        if sub and not fim:
            tx.append(_txt('eyebrow', sub, a + (0 if i == 0 else 0.25), b, 450, base='dm_md', size=30, track=6, align='center', x='c'))
    tx.append(dict(kind='button', text=p['cta'], t0=cuts[2] + 0.4, t1=15, y=440, x='c', anim='fade', out=False,
                   style='link', icon='cart', text_color=(255, 255, 255), base='dm_md', size=48, h=100, shadow=True))
    save2(nome, narr=narr, narr_at=narr_at, tempo=tempo, bed=bed or [], grade=FMT_B, accent=p['accent'], segs=segs, texts=tx)


FMT_A = dict(sat=0.92, contrast=0.98, lift=0.03, vign=0.22, grain=0.02, top=0.30)  # filtro mais leve (kit 2026-10-21)


def opcao_a(nome, p, segs, narr, narr_at=0.5, bed=None, tempo=1.0, cuts=(0, 2.9, 5.6, 7.9, 10.6)):
    """Opção A padrão "Um dia com ele/ela" (aprovada 2026-10-18; molde = poltrona_lux3_umdia em lux.py).
    p: eyebrow ('Das 8h às 22h'), gancho=[linhas com *itálico*], momentos=[(rótulo grande, legenda)]*3, cta.
    Rótulo grande: horário 'HH:MM' (rola entre eles) OU palavra curta para produtos sem manhã/tarde/noite
    ('Café', 'Almoço', 'Jantar'). Mergulho ao preto na virada de cada momento e luz que esquenta até a noite."""
    a, b, c, d, e = cuts
    ramp = [(0, -0.01, 1.02), (c - 0.2, -0.01, 1.02), (c + 0.2, 0.025, 1.0), (d - 0.2, 0.025, 1.0), (d + 0.2, 0.05, 0.93), (15, 0.05, 0.93)]
    tx = [_txt('eyebrow', p['eyebrow'], a, b - 0.1, 250), _txt('title', p['gancho'], a, b - 0.1, 300)]
    if p.get('sem_horario'):  # plano B (kit 2026-10-21): produto que não encaixa em manhã/tarde/noite, só 1 frase curta por cena
        ramp = [(0, 0.0, 1.0), (15, 0.0, 1.0)]
        for (rot, leg), t0, t1 in zip(p['momentos'], (b + 0.2, c + 0.1, d + 0.1), (c - 0.1, d - 0.1, e - 0.1)):
            tx.append(_txt('title', leg, t0, t1, 280, size=84))
    else:
        tx.append(dict(kind='clock', keys=[(b, p['momentos'][0][0]), (c, p['momentos'][1][0]), (d, p['momentos'][2][0])],
                       t0=b, t1=e - 0.1, y=230, size=200 if ':' in p['momentos'][0][0] else 150, anim='fade'))
        for (rot, leg), t0, t1 in zip(p['momentos'], (b + 0.2, c + 0.1, d + 0.1), (c - 0.1, d - 0.1, e - 0.1)):
            tx.append(_txt('eyebrow', leg, t0, t1, 470))
    head = p.get('cta', 'Leve pra casa.')
    lines = head if isinstance(head, list) else [head]
    tx += [_txt('eyebrow', 'Disponível no link', e + 0.1, 15, 250, out=False),
           _txt('title', lines, e + 0.35, 15, 300, out=False, anim='wipe'),
           dict(kind='line', len=220, t0=e + 0.7, t1=15, y=300 + len(lines) * 122 + 30, anim='draw', out=False)]
    save2(nome, narr=narr, narr_at=narr_at, tempo=tempo, bed=bed or [], dips=[c, d],
          grade=dict(FMT_A, warm_ramp=ramp), segs=segs, texts=tx, **({'shiftx': p['shiftx']} if p.get('shiftx') else {}))
