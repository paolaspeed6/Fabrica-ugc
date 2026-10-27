"""Trilhas ANIMADAS e sofisticadas (a dona, 27/10: "mais animadas, ainda sofisticadas, menos melancólicas").
Estilo lounge/bossa/pop elegante: 104-120 bpm, tom maior com acordes de sétima, piano elétrico ou violão em levada
sincopada, baixo andando, bateria leve (aro, chimbal, bumbo macio) e melodia curta que volta (gancho).
Uso: python3 -I animadas.py SOUNDFONT.sf2 PASTA_SAIDA  (usa render() do compor.py; grátis, timbre GeneralUser GS)"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compor
from compor import n

ESC = [0, 2, 4, 5, 7, 9, 11]
PROGS = [[0, 5, 1, 4], [0, 2, 3, 4], [3, 4, 2, 5], [0, 4, 5, 3], [1, 4, 0, 5], [0, 3, 1, 4]]
# (nome, levada, baixo, melodia, pad)  presets GM do GeneralUser GS
TIMBRES = [('rhodes_vibrafone', 4, 33, 11, 89), ('violao_flauta', 24, 32, 73, 49), ('piano_sinos', 0, 33, 9, 89),
           ('rhodes_violao', 4, 33, 25, 49), ('piano_vibrafone', 0, 32, 11, 52), ('violao_celesta', 24, 33, 8, 89),
           ('rhodes_flauta', 5, 33, 73, 49), ('piano_marimba', 0, 33, 12, 89), ('guitarra_vibrafone', 26, 33, 11, 52),
           ('rhodes_sinos', 4, 32, 10, 89), ('piano_flauta', 0, 33, 73, 49), ('violao_vibrafone', 24, 33, 11, 89)]
LEVADAS = [[(0, .45), (1.5, .4), (2.5, .4), (3, .8)], [(0, .9), (1.5, .4), (2, .4), (3.5, .45)],
           [(.5, .4), (1.5, .4), (2.5, .4), (3.5, .4)], [(0, .4), (1, .4), (1.5, .4), (2.5, .9)]]
BAIXOS = [[(0, 0, 1), (1.5, 7, .4), (2, 12, .9), (3.5, 7, .4)], [(0, 0, 1.4), (1.5, 0, .4), (2.5, 7, .9), (3.5, 5, .4)],
          [(0, 0, .9), (1, 7, .9), (2, 12, .9), (3, 7, .9)]]


def acorde(ton, grau):  # tétrade (com sétima) da escala maior
    return [ton + ESC[(grau + i) % 7] + 12 * ((grau + i) // 7) for i in (0, 2, 4, 6)]


def peca(i):
    def f():
        r = random.Random(7000 + i)
        nome_t, p_lev, p_bx, p_mel, p_pad = TIMBRES[i % len(TIMBRES)]
        ton = [60, 62, 65, 67, 57, 64][i % 6]
        bpm = [108, 112, 116, 104, 120, 110][i % 6]
        prog = PROGS[i % len(PROGS)] * 2
        lev, bx = LEVADAS[i % len(LEVADAS)], BAIXOS[i % len(BAIXOS)]
        ev = []
        for b, g in enumerate(prog):
            t = b * 4; a = acorde(ton - 12, g)
            for tt, d in lev:  # levada sincopada
                for k in a[1:]:
                    n(ev, t + tt, d, 0, k, 50 + (8 if tt == 0 else 0))
            for tt, iv, d in bx:  # baixo
                n(ev, t + tt, d * .95, 1, a[0] - 12 + iv, 78)
            n(ev, t, 4.05, 3, a[1] + 12, 22); n(ev, t, 4.05, 3, a[3] + 12, 20)  # pad bem baixo
            for s in range(8):  # bateria: chimbal em colcheias, aro no 2 e 4, bumbo no 1 e no "e" do 3
                n(ev, t + s * .5, .2, 9, 42, 38 + (14 if s % 2 == 0 else 0))
            for tt in (1, 3):
                n(ev, t + tt, .2, 9, 37, 52)
            for tt in (0, 2.5):
                n(ev, t + tt, .3, 9, 36, 62)
            if b % 4 == 3:
                n(ev, t + 3.5, .2, 9, 46, 40)  # chimbal aberto no fim da frase
            n(ev, t, .2, 9, 70, 24)
        # gancho: motivo de 2 compassos repetido (com resposta) sobre a pentatônica maior
        pent = [0, 2, 4, 7, 9]
        rit = r.choice([[(0, .5), (.5, .5), (1.5, 1), (3, .5), (3.5, .5)], [(0, 1), (1.5, .5), (2, .5), (2.5, 1.5)],
                        [(.5, .5), (1, .5), (1.5, 1), (2.5, .5), (3, 1)]])
        alt = [r.choice(pent) + 12 * r.choice([1, 1, 2]) for _ in rit]
        for frase in range(4):
            t0 = frase * 8 + (4 if frase % 2 else 0) * 0
            for (tt, d), k in zip(rit, alt):
                kk = ton + k + (2 if frase == 2 else 0)
                while (kk - ton) % 12 not in pent: kk += 1
                n(ev, t0 + tt, d * .9, 2, min(88, max(67, kk)), 66)
            for (tt, d), k in zip(rit[:3], alt[::-1]):  # resposta no 2º compasso
                kk = ton + k
                n(ev, t0 + 4 + tt, d * .9, 2, min(88, max(67, kk)), 58)
        return f'animada_{i + 1:02d}_{nome_t}', bpm, {0: p_lev, 1: p_bx, 2: p_mel, 3: p_pad, 9: (128, 0)}, ev
    return f


PECAS = [peca(i) for i in range(12)]

if __name__ == '__main__':
    compor.SF, compor.OUT = sys.argv[1], sys.argv[2]
    os.makedirs(compor.OUT, exist_ok=True)
    for f in PECAS:
        compor.render(*f())
