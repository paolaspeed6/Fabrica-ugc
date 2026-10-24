"""Shopee C (Kevin 2026-10-22: 4ª versão, o "C dos vídeos da esposa", no layout app-safe e na estética da marca).
Duas candidatas para o Kevin escolher pelo print:
- 'revista': o C da esposa (novos.opcao_c): CASA espaçado, Playfair centralizado, detalhes como notas numeradas.
- 'zara': o "Zara Home" (lux.py cadeira_lux1_zarahome): rótulo + título serifado com itálico, "Detalhe 01/02", lugares de uso.
Tudo entre y 230 e 650 (abaixo da barra do app); CTA "Toque no carrinho" com seta em y 1350, logo acima do card do produto.
p: rotulo, gancho=[2 linhas com *itálico*], notas=[3 frases curtas com *itálico*], lugares ('Sala · Escritório'), cta=[2 linhas]."""
from novos import _txt, save2
from padrao_app import CTA_SHOPEE, CTA_Y_SHOPEE
from horst import _ajusta

FMT_CZ = dict(sat=0.88, warm=0.015, contrast=0.96, lift=0.04, vign=0.14, grain=0.02, top=0.30)  # filtro leve (regra 7: nada amarelado)


def _cta(t0):
    return dict(kind='button', text='Toque no carrinho', t0=t0, t1=15, y=CTA_Y_SHOPEE, x='c', anim='fade', out=False, **CTA_SHOPEE)


def opcao_c(nome, p, segs, estilo='zara', bed=None, accent=(255, 255, 255)):
    t = [0, 3.4, 6.0, 8.6, 11.2]
    if estilo == 'revista':
        tx = [_txt('title', 'CASA', 0, 15, 230, base='play', it='play', size=64, align='center', x='c', track=30, out=False),
              dict(kind='line', len=120, t0=0, t1=15, y=318, x='c', out=False, color=list(accent)),
              _txt('title', p['gancho'], 0, t[1] - 0.1, 350, base='play', it='play_it', size=80, spacing=1.06, align='center', x='c')]
        for i, nota in enumerate(p['notas']):
            a, b = t[i + 1], t[i + 2]
            tx += [_txt('title', f'0{i + 1}', a, b, 340, base='play_it', it='play_it', size=96, align='center', x='c'),
                   _txt('body', nota, a + 0.2, b - 0.05, 470, base='play', it='play_it', size=58, spacing=1.1, align='center', x='c')]
        tx += [_txt('eyebrow', p['rotulo'], t[4] + 0.1, 15, 350, base='dm', size=26, track=8, align='center', x='c', out=False),
               _txt('title', p['cta'], t[4] + 0.3, 15, 400, base='play', it='play_it', size=84, spacing=1.06, align='center', x='c', anim='wipe', out=False)]
    elif estilo == 'lista':  # criação nova (Kevin 2026-10-22): checklist que se monta cena a cena, fica inteira no fim
        LAR = (238, 77, 45)  # laranja da Shopee: parece nativo do app
        tx = [dict(kind='band', text=p.get('selo', '3 motivos pra levar').upper(), t0=0, t1=15, y=230, x=70, size=30, base='pop_b',
                   fill=LAR + (255,), color=(255, 255, 255), px=22, py=12, r=30, out=False),
              _txt('title', [l.replace('*', '') for l in p['gancho']], 0, t[1] - 0.05, 320, base='pop_b', it='pop_b', size=78, spacing=1.04)]
        for i, item in enumerate(p['itens']):
            y = 318 + i * 100
            tx += [dict(kind='rect', w=880, h=84, r=42, fill=(255, 255, 255, 242), t0=t[i + 1], t1=15, y=y, x=62, anim='fade', out=False, shadow=True),
                   dict(kind='check', text=item, t0=t[i + 1] + 0.12, t1=15, y=y + 17, x=74, size=40, shadow=False, base='pop_sb', fill=LAR,
                        color=(28, 24, 22), anim='fade', out=False)]
    else:
        tx = [_txt('eyebrow', p['rotulo'], 0, t[1] - 0.1, 250, base='dm_md'),
              _txt('title', p['gancho'], 0, t[1] - 0.1, 300, base='dms', it='dms_it', size=104),
              dict(kind='line', len=220, t0=0.4, t1=t[1] - 0.1, y=560, anim='draw', color=list(accent))]
        for i, nota in enumerate(p['notas']):
            a, b = t[i + 1], t[i + 2]
            tx += [_txt('eyebrow', f'Detalhe 0{i + 1}', a, b - 0.05, 250, base='dm_md'),
                   _txt('body', nota, a + 0.1, b - 0.05, 300, base='dms', it='dms_it', size=84)]
        tx += [_txt('eyebrow', p['lugares'], t[3] + 0.2, t[4] - 0.05, 470, base='dm_md', size=28),
               _txt('eyebrow', 'Toque no carrinho', t[4] + 0.1, 15, 250, base='dm_md', out=False),
               _txt('title', p['cta'], t[4] + 0.35, 15, 300, base='dms', it='dms_it', size=104, anim='wipe', out=False),
               dict(kind='line', len=220, t0=t[4] + 0.7, t1=15, y=300 + len(p['cta']) * 108 + 30, anim='draw', out=False, color=list(accent))]
    tx.append(_cta(t[4] + 0.6))
    save2(nome, bed=bed or [], grade=FMT_CZ, segs=segs, texts=tx, accent=list(accent), lift=0, dips=[t[1], t[2], t[3], t[4]])
    _ajusta(nome, lambda sp: None)
