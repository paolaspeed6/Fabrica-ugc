"""10 ESTILOS de trilha (a dona 27/11: "dez tipos de músicas diferentes, alegres, comerciais, sons bonitos; está muito repetitivo").
O estilo 'lounge' são as 12 animadas que já existem (animadas.py). Aqui ficam os outros 9, com 4 trilhas cada.
Arquivo: <estilo>_NN_<timbre>.wav; o escolher.py lê o estilo pelo prefixo e não repete estilo seguido.
Uso: python3 -I estilos.py SOUNDFONT.sf2 PASTA_SAIDA  (grátis, timbre GeneralUser GS, uso comercial liberado)"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compor
from compor import n

MAIOR = [0, 2, 4, 5, 7, 9, 11]
PENT = [0, 2, 4, 7, 9]


def acorde(ton, grau, notas=4):
    return [ton + MAIOR[(grau + i) % 7] + 12 * ((grau + i) // 7) for i in range(0, 2 * notas, 2)]


# Cada estilo: bpm, progressões (graus), tons, variações de timbre (nome, {canal: preset}), comp, baixo, bateria, melodia.
# comp: lista de (tempo, duração) dentro do compasso; 'arp' = arpejo em semicolcheias/colcheias.
# canais: 0 acompanhamento, 1 baixo, 2 melodia, 3 pad/cordas, 4 enfeite, 9 bateria
ESTILOS = {
    'pop_alegre': dict(
        bpm=[120, 124, 118, 122], tons=[60, 62, 65, 67],
        progs=[[0, 4, 5, 3], [0, 3, 4, 4], [5, 3, 0, 4], [0, 4, 3, 4]],
        timbres=[('piano_sintetizador', {0: 0, 1: 38, 2: 80, 3: 89}), ('guitarra_sinos', {0: 25, 1: 33, 2: 9, 3: 49}),
                 ('piano_assobio', {0: 1, 1: 34, 2: 78, 3: 89}), ('violao_glock', {0: 25, 1: 33, 2: 9, 3: 50})],
        comp=[(0, .4), (.5, .4), (1.5, .4), (2, .4), (2.5, .4), (3.5, .4)], baixo='oitava',
        bateria='pop', mel='alegre'),
    'comercial': dict(
        bpm=[116, 112, 120, 114], tons=[62, 64, 60, 65],
        progs=[[0, 4, 5, 3], [5, 3, 0, 4], [3, 0, 4, 5], [0, 5, 3, 4]],
        timbres=[('piano_cordas', {0: 0, 1: 33, 2: 0, 3: 48, 4: 45}), ('piano_pizzicato', {0: 0, 1: 33, 2: 45, 3: 49}),
                 ('piano_eletrico_cordas', {0: 4, 1: 33, 2: 11, 3: 48}), ('violao_cordas', {0: 25, 1: 32, 2: 0, 3: 48})],
        comp='arp8', baixo='pulsado', bateria='comercial', mel='inspira'),
    'tropical': dict(
        bpm=[106, 108, 110, 104], tons=[65, 62, 67, 60],
        progs=[[5, 3, 0, 4], [0, 4, 5, 3], [5, 4, 3, 4], [3, 4, 5, 0]],
        timbres=[('marimba_flauta', {0: 12, 1: 38, 2: 75, 3: 89}), ('steel_drum', {0: 114, 1: 38, 2: 114, 3: 89}),
                 ('kalimba_sintetizador', {0: 108, 1: 39, 2: 81, 3: 90}), ('marimba_pan', {0: 12, 1: 38, 2: 75, 3: 52})],
        comp=[(.5, .3), (1.5, .3), (2.5, .3), (3.5, .3), (2.75, .25)], baixo='house', bateria='tropical', mel='tropical'),
    'ukulele_feliz': dict(
        bpm=[126, 130, 124, 128], tons=[67, 60, 65, 62],
        progs=[[0, 3, 4, 0], [0, 5, 3, 4], [0, 3, 0, 4], [3, 4, 0, 5]],
        timbres=[('violao_assobio', {0: 24, 1: 32, 2: 78, 4: 9}), ('violao_glock', {0: 24, 1: 32, 2: 9, 4: 13}),
                 ('violao_xilofone', {0: 24, 1: 32, 2: 13, 4: 9}), ('violao_flautim', {0: 24, 1: 32, 2: 72, 4: 9})],
        comp=[(0, .3), (.5, .2), (1, .3), (1.5, .2), (2, .3), (2.5, .2), (3, .3), (3.5, .2)], baixo='saltado',
        bateria='palmas', mel='saltitante'),
    'funk_groove': dict(
        bpm=[100, 104, 98, 102], tons=[64, 62, 65, 60],
        progs=[[1, 4, 1, 4], [0, 3, 0, 3], [5, 1, 4, 0], [1, 4, 0, 5]],
        timbres=[('clavinete_metais', {0: 7, 1: 36, 2: 61, 3: 89}), ('guitarra_metais', {0: 28, 1: 36, 2: 61, 3: 89}),
                 ('rhodes_sax', {0: 4, 1: 37, 2: 65, 3: 89}), ('clavinete_sintetizador', {0: 7, 1: 36, 2: 81, 3: 52})],
        comp=[(0, .2), (.75, .2), (1.5, .2), (2.25, .2), (2.5, .2), (3.25, .2)], baixo='funk', bateria='funk', mel='curta'),
    'bossa_nova': dict(
        bpm=[132, 136, 128, 140], tons=[62, 60, 65, 57],
        progs=[[1, 4, 0, 0], [0, 5, 1, 4], [3, 2, 1, 4], [0, 3, 1, 4]],
        timbres=[('violao_flauta', {0: 24, 1: 32, 2: 73, 3: 52}), ('violao_vibrafone', {0: 24, 1: 32, 2: 11, 3: 49}),
                 ('violao_sax', {0: 24, 1: 32, 2: 66, 3: 52}), ('violao_piano', {0: 24, 1: 32, 2: 0, 3: 49})],
        comp=[(0, .4), (.75, .4), (1.5, .4), (2.5, .4), (3.25, .4)], baixo='bossa', bateria='bossa', mel='suave'),
    'piano_bonito': dict(
        bpm=[92, 96, 88, 100], tons=[60, 65, 62, 67],
        progs=[[0, 4, 5, 3], [3, 4, 0, 5], [0, 5, 3, 4], [5, 3, 0, 4]],
        timbres=[('piano_cordas', {0: 0, 2: 0, 3: 49, 1: 0}), ('piano_harpa', {0: 46, 2: 0, 3: 49, 1: 0}),
                 ('piano_celesta', {0: 0, 2: 8, 3: 89, 1: 0}), ('piano_coro', {0: 0, 2: 0, 3: 52, 1: 0})],
        comp='arp16', baixo='longo', bateria=None, mel='bonita'),
    'cinematico': dict(
        bpm=[96, 100, 92, 104], tons=[62, 60, 64, 57],
        progs=[[5, 3, 0, 4], [0, 4, 5, 3], [5, 4, 3, 4], [3, 0, 4, 5]],
        timbres=[('cordas_trompas', {0: 48, 1: 43, 2: 60, 3: 48, 4: 46}), ('cordas_piano', {0: 48, 1: 43, 2: 0, 3: 49, 4: 46}),
                 ('cordas_violino', {0: 48, 1: 43, 2: 40, 3: 49, 4: 46}), ('cordas_coro', {0: 48, 1: 43, 2: 52, 3: 48, 4: 46})],
        comp='ostinato', baixo='longo', bateria='epico', mel='epica'),
    'eletronico_chill': dict(
        bpm=[86, 90, 84, 88], tons=[64, 62, 65, 60],
        progs=[[0, 5, 3, 4], [5, 3, 0, 4], [3, 4, 5, 5], [0, 2, 3, 4]],
        timbres=[('pad_rhodes', {0: 4, 1: 38, 2: 81, 3: 88}), ('pad_sinos', {0: 88, 1: 38, 2: 10, 3: 89}),
                 ('pad_pluck', {0: 4, 1: 39, 2: 84, 3: 91}), ('pad_vibrafone', {0: 89, 1: 38, 2: 11, 3: 88})],
        comp=[(0, 1.4), (1.5, .4), (2.5, 1.2)], baixo='lofi', bateria='lofi', mel='chill'),
}

DRUM = {
    'pop': lambda t, b: ([(t, 36, 80), (t + 2, 36, 78), (t + 2.5, 36, 55)] + [(t + 1, 39, 70), (t + 3, 39, 72)]
                         + [(t + s * .5, 42, 40 + 12 * (s % 2 == 0)) for s in range(8)] + ([(t, 49, 60)] if b == 0 else [])),
    'comercial': lambda t, b: ([(t + i, 36, 70) for i in range(4)] + [(t + 1, 39, 55), (t + 3, 39, 58)]
                               + [(t + s * .5 + .5, 42, 36) for s in range(0, 8, 2)] + [(t + s * .25, 54, 22) for s in range(16)]),
    'tropical': lambda t, b: ([(t + i, 36, 78) for i in range(4)] + [(t + i + .5, 46, 42) for i in range(4)]
                              + [(t + 1, 39, 50), (t + 3, 39, 52)] + [(t + s * .25, 70, 26) for s in range(16)]),
    'palmas': lambda t, b: ([(t, 36, 60), (t + 2, 36, 58), (t + 1, 39, 66), (t + 3, 39, 66)] + [(t + s * .5, 54, 34) for s in range(8)]),
    'funk': lambda t, b: ([(t, 36, 82), (t + .75, 36, 60), (t + 2.5, 36, 70), (t + 1, 38, 76), (t + 3, 38, 78), (t + 3.75, 38, 30)]
                          + [(t + s * .25, 42, 30 + 14 * (s % 2 == 0)) for s in range(16)]),
    'bossa': lambda t, b: ([(t, 36, 50), (t + 1.5, 36, 40), (t + 2, 36, 50), (t + 3.5, 36, 40)]
                           + [(t + tt, 37, 46) for tt in (0, .75, 1.5, 2.5, 3.25)] + [(t + s * .5, 69, 26) for s in range(8)]),
    'epico': lambda t, b: ([(t, 41, 70), (t + 1.5, 41, 50), (t + 2, 43, 62), (t + 3.5, 41, 50)] + ([(t, 49, 55)] if b % 4 == 0 else [])
                           + ([(t + 3 + s * .25, 38, 30 + s * 8) for s in range(4)] if b % 4 == 3 else [])),
    'lofi': lambda t, b: ([(t, 36, 70), (t + 1.75, 36, 50), (t + 2.5, 36, 62), (t + 1, 38, 56), (t + 3, 38, 58)]
                          + [(t + s * .5 + (.06 if s % 2 else 0), 42, 32) for s in range(8)]),
}


def baixo(ev, est, t, raiz, r):
    k = raiz - 24
    if est == 'oitava':
        for tt in (0, .5, 1, 1.5, 2, 2.5, 3, 3.5):
            n(ev, t + tt, .4, 1, k + (12 if tt % 1 else 0), 74)
    elif est == 'pulsado':
        for s in range(8):
            n(ev, t + s * .5, .42, 1, k, 70 + 8 * (s % 2 == 0))
    elif est == 'house':
        for tt in (.5, 1.5, 2.5, 3.5):
            n(ev, t + tt, .4, 1, k + 12, 80)
    elif est == 'saltado':
        for tt, iv in ((0, 0), (1, 7), (2, 0), (3, 7)):
            n(ev, t + tt, .5, 1, k + iv, 72)
    elif est == 'funk':
        for tt, iv, d in ((0, 0, .3), (.75, 12, .2), (1.5, 0, .2), (2, 7, .3), (2.75, 10, .2), (3.25, 12, .2), (3.5, 0, .3)):
            n(ev, t + tt, d, 1, k + iv, 84)
    elif est == 'bossa':
        for tt, iv in ((0, 0), (1.5, 7), (2, 7), (3.5, 0)):
            n(ev, t + tt, .45, 1, k + iv, 74)
    elif est == 'lofi':
        n(ev, t, 1.4, 1, k, 76); n(ev, t + 2.5, 1.2, 1, k + 7, 66)
    else:  # longo (piano/cinematico)
        n(ev, t, 4.05, 1, k + 12, 58); n(ev, t + 2, 2, 1, k + 19, 40)


def comp(ev, est, t, a, r):
    vozes = a[1:]
    if est == 'arp8':
        seq = [a[0], a[1], a[2], a[3], a[2] + 12, a[3], a[2], a[1]]
        for j, k in enumerate(seq):
            n(ev, t + j * .5, .45, 0, k, 46 + 8 * (j % 4 == 0))
    elif est == 'arp16':
        seq = [a[0], a[2], a[3], a[1] + 12, a[2] + 12, a[1] + 12, a[3], a[2]] * 2
        for j, k in enumerate(seq):
            n(ev, t + j * .25, .6, 0, k, 38 + 10 * (j % 4 == 0))
    elif est == 'ostinato':
        for j in range(8):
            n(ev, t + j * .5, .4, 0, a[(0, 2, 1, 2)[j % 4]], 52 + 10 * (j % 2 == 0))
        n(ev, t, 4.05, 4, a[0] - 12, 34)
    else:
        for tt, d in est:
            for k in vozes:
                n(ev, t + tt, d, 0, k, 50 + 8 * (tt == 0))


def melodia(ev, est, ton, prog, r, compassos):
    """Gancho de 1 compasso repetido com variação (pergunta e resposta), notas do acorde nos tempos fortes."""
    ritmos = {
        'alegre': [[(0, .5), (.5, .5), (1, .5), (1.5, 1), (3, .5), (3.5, .5)], [(0, .75), (.75, .75), (1.5, .5), (2, 1), (3, 1)]],
        'inspira': [[(0, 1), (1, .5), (1.5, .5), (2, 2)], [(0, .5), (.5, .5), (1, 1), (2, .5), (2.5, 1.5)]],
        'tropical': [[(0, .5), (.75, .25), (1, .5), (1.75, .75), (2.5, .5), (3, 1)], [(.5, .5), (1, .5), (2, .5), (2.5, .5), (3, .75)]],
        'saltitante': [[(0, .5), (.5, .25), (.75, .25), (1, .5), (2, .5), (2.5, .5), (3, .5)], [(0, .25), (.25, .25), (.5, .5), (1.5, .5), (2, 1)]],
        'curta': [[(0, .25), (.5, .25), (.75, .5), (2, .25), (2.5, .5)], [(0, .5), (1, .25), (1.25, .25), (2.5, .25), (3, .5)]],
        'suave': [[(0, 1.5), (1.5, .5), (2, 1), (3, 1)], [(.5, 1), (1.5, 1), (2.5, 1.5)]],
        'bonita': [[(0, 1.5), (1.5, .5), (2, 2)], [(0, 1), (1, 1), (2, 1.5), (3.5, .5)]],
        'epica': [[(0, 2), (2, 1), (3, 1)], [(0, 1.5), (1.5, .5), (2, 2)]],
        'chill': [[(.5, .5), (1, 1), (2.5, .5), (3, 1)], [(0, 1.5), (2, .5), (2.5, 1.5)]],
    }[est]
    rit = r.choice(ritmos)
    base = ton + 12
    for b in range(compassos):
        if b % 4 == 0 and b // 4 >= 1 and est in ('bonita', 'epica', 'chill'):
            base = ton + 12  # volta ao centro a cada frase
        a = acorde(base, prog[b % len(prog)], 3)
        resposta = b % 2 == 1
        for j, (tt, d) in enumerate(rit if not resposta else rit[:max(2, len(rit) - 1)]):
            if tt in (0, 2) or j == 0:
                k = a[(j + b) % 3]
            else:
                k = base + PENT[r.randrange(5)] + (12 if r.random() < .25 else 0)
            while k < ton + 7: k += 12
            while k > ton + 26: k -= 12
            n(ev, b * 4 + tt, d * .92, 2, k, 70 - 8 * resposta)


def peca(estilo, i):
    def f():
        cfg = ESTILOS[estilo]
        r = random.Random(f'{estilo}{i}')
        nome_t, progs = cfg['timbres'][i]
        bpm, ton, prog = cfg['bpm'][i], cfg['tons'][i], cfg['progs'][i]
        compassos = math.ceil(15 * bpm / 240) + 1
        ev = []
        for b in range(compassos):
            t = b * 4
            a = acorde(ton - 12, prog[b % len(prog)])
            comp(ev, cfg['comp'], t, a, r)
            baixo(ev, cfg['baixo'], t, a[0], r)
            if 3 in progs:
                n(ev, t, 4.05, 3, a[1] + 12, 24); n(ev, t, 4.05, 3, a[2] + 12, 22)
            if 4 in progs and cfg['comp'] != 'ostinato' and b % 2 == 1:
                n(ev, t + 3.5, .3, 4, a[3] + 24, 40)
            if cfg['bateria']:
                for tt, k, v in DRUM[cfg['bateria']](t, b):
                    n(ev, tt, .2, 9, k, v)
        melodia(ev, cfg['mel'], ton, prog, r, compassos)
        if cfg['bateria']:
            progs = dict(progs); progs[9] = (128, 0)
        return f'{estilo}_{i + 1:02d}_{nome_t}', bpm, progs, ev
    return f


PECAS = [peca(e, i) for e in ESTILOS for i in range(4)]

if __name__ == '__main__':
    compor.SF, compor.OUT = sys.argv[1], sys.argv[2]
    os.makedirs(compor.OUT, exist_ok=True)
    so = sys.argv[3] if len(sys.argv) > 3 else ''
    for f in PECAS:
        nome = f()[0]
        if so and not nome.startswith(so):
            continue
        compor.render(*f())
