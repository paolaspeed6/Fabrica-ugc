"""PADRÃO APROVADO para produção em massa (Kevin 2026-10-20 18:40, "salve o padrão").
3 versões por link: Shopee A "Um dia com ela", Shopee B "Faixas", Reels "Faixas".
- Gancho/faixas no topo, entre y 230 e 650 (abaixo da barra do app).
- CTA embaixo, LOGO ACIMA do botão real do app, nunca em cima dele, com seta para baixo:
  Shopee "Toque no carrinho" em y 1350 (acima do card do produto); Reels "Link na legenda" em y 1310 (acima da legenda).
- Nada de texto em y > 1440 nem na coluna da direita (x > 940): é a área do app.
- lift 250 (vídeo sobe; o produto fica entre o texto e o card).
- Clipes do Pruna: use preparar_clipe() (ida e volta só do trecho com o produto inteiro), porque o Pruna aproxima até cortar.
uso: from padrao_app import fazer_app, preparar_clipe ; fazer_app(cfg) com o mesmo cfg de horst.fazer (id, accent, clips, a, b, r, tomadas)."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from produto import _segs, MUSICA, trilha
from novos import opcao_a, opcao_b_faixas, CTA_MODERNO
from horst import _ajusta, _a

TOPO, LIFT, CTA_Y_SHOPEE, CTA_Y_REELS = 230, 250, 1350, 1310
CTA_SHOPEE = dict(CTA_MODERNO, icon='down')
CTA_REELS = dict(style='solid', fill=(255, 255, 255), text_color=(22, 20, 18), icon='down', base='pop_sb', size=44, h=104)


def preparar_clipe(orig, dest, ate, lento=1.0):
    """ida e volta de orig[0:ate] (s), opcionalmente desacelerada; dura 2*ate*lento."""
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', orig, '-filter_complex',
                    f'[0:v]trim=0:{ate},setpts={lento}*(PTS-STARTPTS),fps=24,split[f][r0];[r0]reverse[r];[f][r]concat=n=2:v=1[v]',
                    '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', dest], check=True)
    return round(2 * ate * lento, 2)


def _a_cta(sp):
    _a(sp); sp.update(lift=LIFT)
    fim = [el for el in sp['texts'] if el['kind'] == 'eyebrow' and el['lines'] == ['Toque no carrinho']][0]
    sp['texts'].remove(fim)
    sp['texts'].append(dict(kind='button', text='Toque no carrinho', t0=fim['t0'] + 0.6, t1=15, y=CTA_Y_SHOPEE, x='c', anim='fade',
                            out=False, **CTA_SHOPEE))


def fazer_app(cfg):
    pid, ac, A, B, R, tm = cfg['id'], cfg['accent'], cfg['a'], cfg['b'], cfg['r'], cfg['tomadas']
    cuts = (0, 3.0, 5.6, 8.2, 10.8)
    opcao_a(f'{pid}_a_umdia', dict(eyebrow=A['eyebrow'], gancho=A['gancho'], momentos=A['momentos'], cta=A['cta'], accent=ac, sem_horario=A.get('sem_horario')),
            _segs(cuts + (15,), tm['a'], cfg['clips']), None, bed=[trilha(f'{pid}_a_umdia')], cuts=cuts)
    _ajusta(f'{pid}_a_umdia', _a_cta)
    cuts = (0, 5.0, 10.0, 15)
    opcao_b_faixas(f'{pid}_b_faixas', dict(kicker=B['kicker'], cenas=B['cenas'], cta='Toque no carrinho', y=TOPO, lift=LIFT,
                   cta_y=CTA_Y_SHOPEE, accent=ac, cta_estilo=CTA_SHOPEE), _segs(cuts, tm['b'], cfg['clips']), None, bed=[trilha(f'{pid}_b_faixas')], cuts=cuts)
    _ajusta(f'{pid}_b_faixas', lambda sp: None)
    opcao_b_faixas(f'{pid}_r_reels', dict(kicker=R['kicker'], cenas=R['cenas'], cta='Link na legenda', y=TOPO, lift=LIFT,
                   cta_y=CTA_Y_REELS, accent=ac, cta_estilo=CTA_REELS), _segs(cuts, tm['r'], cfg['clips']), None, bed=[trilha(f'{pid}_r_reels', 'reels')], cuts=cuts)
    _ajusta(f'{pid}_r_reels', lambda sp: None)
    return [f'{pid}_a_umdia', f'{pid}_b_faixas', f'{pid}_r_reels']
