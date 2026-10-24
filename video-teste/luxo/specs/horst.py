"""Identidade da marca (fábrica original, 2026-10-18): inspirada no modelo da esposa, mas não igual.
Shopee A = "Um dia com ela" com DM Serif Display, CTA "Toque no carrinho" e linha na cor do produto;
Shopee B = "Faixas moderno"; Reels = cartão de vidro (o nosso cartão escuro) com CTA "Link na legenda".
Assinatura pequena (MARCA_NOME), deslizando devagar no topo (nunca sobre o produto).
uso: from horst import fazer  ->  fazer(cfg) grava specs/<id>_a_umdia.json, _b_faixas.json, _r_reels.json"""
import json
from produto import _segs, MUSICA
from novos import *

import os
# assinatura pequena no topo: o nome da loja de quem usa a fábrica (variável MARCA_NOME; vazia = sem assinatura)
MARCA = dict(marca=os.environ.get('MARCA_NOME', ''), marca_fonte='dms_it', marca_size=34, marca_y=(128, 168), clock_base='dms')


def _ajusta(nome, fn):
    f = f'{S}/specs/{nome}.json'; sp = json.load(open(f)); sp.update(MARCA); fn(sp); json.dump(sp, open(f, 'w'), ensure_ascii=False, indent=1)


def _a(sp):
    for el in sp['texts']:
        if el['kind'] == 'title':
            el['base'], el['it'] = 'dms', 'dms_it'
        if el['kind'] == 'eyebrow':
            el['base'] = 'dm_md'
            if el['lines'] == ['Disponível no link']:
                el['lines'] = ['Toque no carrinho']
        if el['kind'] == 'line':
            el['color'] = list(sp.get('accent', (255, 255, 255)))


def fazer(cfg):
    pid = cfg['id']; comum = dict(accent=cfg['accent'], **({'shiftx': cfg['shiftx']} if cfg.get('shiftx') else {}))
    A, B, R = cfg['a'], cfg['b'], cfg['r']
    cuts = (0, 3.0, 5.6, 8.2, 10.8)
    opcao_a(f'{pid}_a_umdia', dict(eyebrow=A['eyebrow'], gancho=A['gancho'], momentos=A['momentos'], cta=A['cta'], **comum),
            _segs(cuts + (15,), cfg['tomadas']['a'], cfg['clips']), None, bed=[MUSICA], cuts=cuts)
    _ajusta(f'{pid}_a_umdia', _a)
    cuts = (0, 5.0, 10.0, 15)
    opcao_b_faixas(f'{pid}_b_faixas', dict(kicker=B['kicker'], cenas=B['cenas'], cta='Toque no carrinho', lift=cfg.get('lift', 300), **comum),
                   _segs(cuts, cfg['tomadas']['b'], cfg['clips']), None, bed=[MUSICA], cuts=cuts)
    _ajusta(f'{pid}_b_faixas', lambda sp: None)
    opcao_b(f'{pid}_r_reels', dict(kicker=R['kicker'], cenas=R['cenas'], cta='Link na legenda', accent=cfg['accent']),
            _segs(cuts, cfg['tomadas']['r'], cfg['clips']), None, bed=[MUSICA], cuts=cuts)
    _ajusta(f'{pid}_r_reels', lambda sp: None)
    return [f'{pid}_a_umdia', f'{pid}_b_faixas', f'{pid}_r_reels']
