"""Peças extras: clássicas em domínio público (arranjo nosso) + calmas originais geradas por regra."""
import random
from compor import n

# ---------------- clássicas ----------------
def fur_elise():
    ev = []
    u = 0.5  # semicolcheia em tempos
    n(ev, 0, u, 0, 76, 58); n(ev, u, u, 0, 75, 52)
    compassos = [
        ('mel', [76, 75, 76, 71, 74, 72]),
        ('arp', 69, (45, 52, 57), (60, 64, 69)),
        ('arp', 71, (40, 52, 56), (64, 68, 71)),
        ('arp', 72, (45, 52, 57), (64, 76, 75)),
        ('mel', [76, 75, 76, 71, 74, 72]),
        ('arp', 69, (45, 52, 57), (60, 64, 69)),
        ('arp', 71, (40, 52, 56), (64, 72, 71)),
        ('fim', 69, (45, 52, 57)),
    ]
    t = 2 * u
    for c in compassos:
        if c[0] == 'mel':
            for i, k in enumerate(c[1]):
                n(ev, t + i * u, u * 1.1, 0, k, 56)
        elif c[0] == 'arp':
            n(ev, t, 2 * u, 0, c[1], 60)
            for i, k in enumerate(c[2]):
                n(ev, t + i * u, 3 * u, 0, k, 44)
            for i, k in enumerate(c[3]):
                n(ev, t + (3 + i) * u, u * 1.2, 0, k, 50)
        else:
            n(ev, t, 6 * u, 0, c[1], 58)
            for i, k in enumerate(c[2]):
                n(ev, t + i * u, 6 * u, 0, k, 42)
        t += 6 * u
    return 'classica_fur_elise_beethoven', 62, {0: 0}, ev

def moonlight():
    ev = []
    b = [(37, 49, (56, 61, 64), (56, 61, 64)), (35, 47, (56, 61, 64), (56, 61, 64)),
         (33, 45, (57, 61, 64), (57, 62, 66)), (32, 44, (56, 60, 66), (56, 60, 63)),
         (37, 49, (56, 61, 64), (56, 61, 64))]
    tri = 1 / 3
    for i, (b1, b2, x, y) in enumerate(b):
        t0 = i * 4
        n(ev, t0, 4, 0, b1, 50); n(ev, t0, 4, 0, b2, 48)
        for q in range(4):
            tr = x if q < 2 else y
            for j, k in enumerate(tr):
                n(ev, t0 + q + j * tri, 0.9, 0, k, 40 + (4 if j == 0 else 0))
    n(ev, 16 + 0.75, 0.25, 0, 68, 58); n(ev, 17, 3, 0, 68, 62)
    n(ev, 0, 20, 1, 49, 22)
    return 'classica_ao_luar_beethoven', 64, {0: 0, 1: 49}, ev

def ode():
    ev = []
    mel = [66, 66, 67, 69, 69, 67, 66, 64, 62, 62, 64, 66, 66, 64, 64,
           66, 66, 67, 69, 69, 67, 66, 64, 62, 62, 64, 66, 64, 62, 62]
    dur = [1] * 12 + [1.5, 0.5, 2] + [1] * 12 + [1.5, 0.5, 2]
    t = 0
    for k, d in zip(mel, dur):
        n(ev, t, d * 0.95, 0, k + 12, 60); t += d
    acordes = [(50, 54, 57), (45, 49, 52), (50, 54, 57), (45, 49, 52),
               (50, 54, 57), (45, 49, 52), (50, 54, 57), (45, 50, 54)]
    for i, a in enumerate(acordes):
        for k in a:
            n(ev, i * 4, 4.05, 1, k + 12, 36)
        n(ev, i * 4, 4, 2, a[0] - 12, 50)
        for j in range(4):
            n(ev, i * 4 + j, 0.9, 3, a[j % 3] + 12, 34)
    return 'classica_ode_alegria_beethoven', 118, {0: 46, 1: 49, 2: 42, 3: 45}, ev

def minueto():
    ev = []
    mel = [(74, 1), (67, .5), (69, .5), (71, .5), (72, .5), (74, 1), (67, 1), (67, 1),
           (76, 1), (72, .5), (74, .5), (76, .5), (78, .5), (79, 1), (67, 1), (67, 1),
           (72, 1), (74, .5), (72, .5), (71, .5), (69, .5), (71, 1), (72, .5), (71, .5), (69, .5), (67, .5),
           (66, 1), (67, .5), (69, .5), (71, .5), (67, .5), (69, 3)]
    t = 0
    for k, d in mel:
        n(ev, t, d * 0.9, 0, k, 58); t += d
    lh = [(55, 3), (59, 3), (60, 3), (59, 3), (57, 3), (55, 3), (62, 1), (59, 1), (55, 1), (50, 3)]
    t = 0
    for k, d in lh:
        n(ev, t, d * 0.95, 0, k - 12, 46); t += d
    return 'classica_minueto_sol_bach', 100, {0: 6}, ev

def greensleeves():
    ev = []
    mel = [(69, 1), (72, 2), (74, 1), (76, 1.5), (77, .5), (76, 1), (74, 2), (71, 1),
           (67, 1.5), (69, .5), (71, 1), (72, 2), (69, 1), (69, 1.5), (68, .5), (69, 1),
           (71, 2), (68, 1), (64, 2), (69, 1)]
    t = 0
    for k, d in mel:
        n(ev, t, d * 0.95, 0, k, 62); t += d
    acordes = [(45, 52, 57), (48, 55, 60), (43, 50, 55), (40, 47, 52), (45, 52, 57), (40, 47, 56), (40, 47, 56), (40, 47, 56)]
    for i, a in enumerate(acordes):
        t0 = 1 + i * 3
        n(ev, t0, 3, 1, a[0], 50)
        for j, k in enumerate((a[1], a[2], a[1] + 12)):
            n(ev, t0 + j, 1.8, 1, k, 40)
    return 'classica_greensleeves_tradicional', 96, {0: 73, 1: 24}, ev

def largo():
    ev = []
    mel = [(76, 1.5), (79, .5), (79, 2), (76, 1.5), (74, .5), (72, 2), (74, 1), (76, 1), (79, 1), (76, 1), (74, 4),
           (76, 1.5), (79, .5), (79, 2), (76, 1.5), (74, .5), (72, 2), (74, 1), (76, 1), (74, 1.5), (72, .5), (72, 4)]
    t = 0
    for k, d in mel:
        n(ev, t, d * 0.98, 0, k - 12, 64); t += d
    acordes = [(48, 52, 55), (53, 57, 60), (43, 47, 50), (43, 47, 53), (48, 52, 55), (53, 57, 60), (43, 47, 53), (48, 52, 55)]
    for i, a in enumerate(acordes):
        for k in a:
            n(ev, i * 4, 4.05, 1, k, 38)
        n(ev, i * 4, 4, 2, a[0] - 12, 46)
    return 'classica_largo_novo_mundo_dvorak', 84, {0: 69, 1: 49, 2: 42}, ev

def canon_harpa():
    ev = []
    baixo = [50, 45, 47, 42, 43, 38, 43, 45]
    acordes = [(62, 66, 69), (57, 61, 64), (59, 62, 66), (54, 57, 61),
               (55, 59, 62), (54, 57, 62), (55, 59, 62), (57, 61, 64)]
    linha2 = [74, 73, 71, 69, 67, 66, 67, 64]
    for i in range(8):
        t = i * 2
        n(ev, t, 2.1, 1, baixo[i], 60)
        a = acordes[i]
        for j, k in enumerate([a[0], a[1], a[2], a[0] + 12, a[2], a[1], a[0] + 12, a[2]]):
            n(ev, t + j * 0.25, 1.0, 0, k, 46)
        n(ev, t, 1.95, 2, linha2[i] + 12, 54)
    return 'classica_canon_harpa_pachelbel', 66, {0: 46, 1: 42, 2: 40}, ev

def manha():
    ev = []
    frases = [[79, 76, 74, 72, 74, 76], [79, 76, 74, 72, 74, 76, 74, 76],
              [79, 76, 79, 81, 76, 81], [79, 76, 74, 72]]
    t = 0
    for f, fr in enumerate(frases):
        for i, k in enumerate(fr):
            d = 0.5 if i < len(fr) - 1 else (1.5 if f < 3 else 3)
            n(ev, t, d * 0.95, 0, k, 62); t += d if i == len(fr) - 1 else 0.5
    for i, a in enumerate([(48, 55, 64), (48, 55, 64), (45, 52, 60), (48, 55, 64)]):
        for k in a:
            n(ev, i * 4.5, 4.6, 1, k, 40)
    return 'classica_manha_peer_gynt_grieg', 70, {0: 73, 1: 49}, ev

# ---------------- calmas originais (regras + semente) ----------------
TONS = [60, 62, 63, 65, 67, 57, 58]
PROG_MAIOR = [[0, 5, 3, 4], [0, 4, 5, 3], [3, 0, 4, 5], [0, 3, 5, 4], [5, 3, 0, 4], [0, 2, 3, 4]]
PROG_MENOR = [[0, 5, 2, 6], [0, 3, 6, 2], [0, 6, 5, 4], [5, 6, 0, 0]]
ESCALA_MAIOR = [0, 2, 4, 5, 7, 9, 11]
ESCALA_MENOR = [0, 2, 3, 5, 7, 8, 10]
TIMBRES = [  # (nome, arpejo, fundo, melodia)
    ('piano', 0, 89, 0), ('harpa', 46, 49, 73), ('eletrico', 4, 94, 4), ('vibrafone', 11, 49, 11),
    ('violao', 24, 49, 73), ('celesta', 8, 89, 0), ('piano_coro', 0, 53, 0), ('marimba', 12, 89, 75),
    ('piano_cordas', 0, 49, 40), ('caixinha', 10, 94, 10),
]
RITMOS = [[2, 1, 1], [3, 1], [1, 1, 2], [4], [1.5, .5, 2], [1, 1, 1, 1], [2, 2]]
PADROES = [[0, 1, 2, 3, 2, 1, 2, 3], [0, 2, 1, 3, 2, 3, 1, 2], [0, 1, 2, 3, 4, 3, 2, 1], [0, 3, 2, 3, 1, 3, 2, 3]]

def _acorde(tonica, escala, grau):
    g = [escala[(grau + i) % 7] + 12 * ((grau + i) // 7) for i in (0, 2, 4, 6)]
    return [tonica + x for x in g]

def original(i):
    def f():
        r = random.Random(1000 + i)
        menor = i % 4 == 3
        ton = TONS[i % len(TONS)] - (3 if menor else 0)
        esc = ESCALA_MENOR if menor else ESCALA_MAIOR
        prog = r.choice(PROG_MENOR if menor else PROG_MAIOR)
        nome_t, p_arp, p_fundo, p_mel = TIMBRES[i % len(TIMBRES)]
        bpm = r.choice([60, 64, 68, 72, 76])
        pad = r.choice(PADROES)
        sem_melodia = i % 5 == 4
        ev = []
        rep = prog * 2
        for b, grau in enumerate(rep):
            t = b * 4
            a = _acorde(ton - 12, esc, grau)
            n(ev, t, 4, 0, a[0] - 12, 46)
            for k in a[1:3]:
                n(ev, t, 4.1, 1, k + 12, 30)
            notas = a + [a[0] + 12]
            for j, idx in enumerate(pad):
                n(ev, t + j * 0.5, 1.3, 0, notas[idx], 40 + (6 if j == 0 else 0))
            if sem_melodia:
                continue
            alvo = sorted(k + 24 for k in a[:3])
            k = r.choice(alvo)
            tt = t
            for d in r.choice(RITMOS):
                k = min(84, max(64, k))
                n(ev, tt, d * 0.95, 2, k, 58)
                tt += d
                passo = r.choice([-2, -1, 1, 2, 0])
                pos = [x for x in esc]
                k = k + {-2: -3, -1: -2, 0: 0, 1: 2, 2: 4}[passo]
                while (k - ton) % 12 not in pos:
                    k += 1
        nome = f'calma_original_{i + 2:02d}_{nome_t}'
        return nome, bpm, {0: p_arp, 1: p_fundo, 2: p_mel}, ev
    return f

PECAS = [fur_elise, moonlight, ode, minueto, greensleeves, largo, canon_harpa, manha] + [original(i) for i in range(18)]
