"""Gera trilhas próprias (obras em domínio público + composições originais) com o
timbre livre GeneralUser GS. Uso: python3 -I compor.py SOUNDFONT.sf2 PASTA_SAIDA"""
import sys, os, random, wave, subprocess
import numpy as np
import tinysoundfont

SR = 44100
SF = OUT = None

def n(ev, t, d, ch, key, vel):
    ev.append((t, d, ch, key, vel))

# ---------- peças: (nome, bpm, programas por canal, eventos em tempos) ----------
def canon():
    ev = []
    baixo = [50, 45, 47, 42, 43, 38, 43, 45]
    acordes = [(62, 66, 69), (57, 61, 64), (59, 62, 66), (54, 57, 61),
               (55, 59, 62), (54, 57, 62), (55, 59, 62), (57, 61, 64)]
    melodia = [78, 76, 74, 73, 71, 69, 71, 73]
    for i in range(8):
        t = i * 2
        n(ev, t, 2.1, 2, baixo[i], 70)
        for k in acordes[i]:
            n(ev, t, 2.1, 1, k, 42)
        a = acordes[i]
        for j, k in enumerate([a[0] - 12, a[1] - 12, a[2] - 12, a[1]]):
            n(ev, t + j * 0.5, 0.9, 0, k, 50)
        n(ev, t, 1.95, 3, melodia[i], 68)
    return 'classica_canon_pachelbel', 66, {0: 0, 1: 49, 2: 49, 3: 0}, ev

def gymnopedie():
    ev = []
    for b in range(6):
        t = b * 3
        if b % 2 == 0:
            n(ev, t, 3, 0, 43, 52); [n(ev, t + 1, 2, 0, k, 40) for k in (59, 62, 66)]
        else:
            n(ev, t, 3, 0, 38, 52); [n(ev, t + 1, 2, 0, k, 40) for k in (57, 61, 66)]
    mel = [(7, 1, 78), (8, 1, 81), (9, 1, 79), (10, 1, 78), (11, 1, 73),
           (12, 1, 71), (13, 1, 73), (14, 1, 74), (15, 3.5, 69)]
    for t, d, k in mel:
        n(ev, t, d, 0, k, 62)
    for b in range(6):
        n(ev, b * 3, 3, 1, 43 + 12 if b % 2 == 0 else 50, 30)
    return 'classica_gymnopedie_satie', 72, {0: 0, 1: 89}, ev

def prelude():
    ev = []
    compassos = [(60, 64, 67, 72, 76), (60, 62, 69, 74, 77), (59, 62, 67, 74, 77),
                 (60, 64, 67, 72, 76), (60, 64, 69, 76, 81)]
    for b, c in enumerate(compassos):
        t0 = b * 4
        for meio in (0, 2):
            t = t0 + meio
            n(ev, t, 2, 0, c[0], 48)
            n(ev, t + 0.25, 1.75, 0, c[1], 44)
            for j, k in enumerate([c[2], c[3], c[4], c[2], c[3], c[4]]):
                n(ev, t + 0.5 + j * 0.25, 0.6, 0, k, 46 + (6 if j % 3 == 0 else 0))
        n(ev, t0, 4, 1, c[0] - 12, 26)
    return 'classica_preludio_bach', 80, {0: 0, 1: 49}, ev

def calma():
    ev = []
    acordes = [(48, 55, 59, 64), (45, 52, 55, 60), (41, 48, 52, 57), (43, 50, 55, 62)]
    for i, a in enumerate(acordes):
        t = i * 4
        for k in a[1:]:
            n(ev, t, 4.1, 1, k + 12, 34)
        for j, k in enumerate([a[0], a[1], a[2], a[3], a[2] + 12, a[3], a[2], a[1]]):
            n(ev, t + j * 0.5, 1.2, 0, k, 38 + (8 if j == 0 else 0))
    mel = [(0, 2, 79), (2, 1, 76), (3, 1, 74), (4, 3, 76), (7, 1, 72),
           (8, 2, 69), (9.99, 1, 72), (11, 1, 76), (12, 4, 74)]
    for t, d, k in mel:
        n(ev, t, d, 2, k, 60)
    return 'calma_original_01', 64, {0: 0, 1: 89, 2: 0}, ev

def render(nome, bpm, progs, ev, dur_s=15.0, cauda=2.5):
    random.seed(nome)
    s = tinysoundfont.Synth(samplerate=SR)
    sf = s.sfload(SF)
    for ch, p in progs.items():  # p = preset (banco 0) ou (banco, preset); bateria = (128, 0) no canal 9
        b, p = p if isinstance(p, tuple) else (0, p)
        s.program_select(ch, sf, b, p, is_drums=(b == 128))
        s.control_change(ch, 7, 110)
    spb = 60.0 / bpm
    acoes = []
    for t, d, ch, k, v in ev:
        j = random.uniform(-0.012, 0.012) if ch == 0 else 0
        vv = max(1, min(127, v + random.randint(-5, 5)))
        acoes.append((max(0, t * spb + j), 1, ch, k, vv))
        acoes.append((max(0, (t + d) * spb + j), 0, ch, k, 0))
    acoes.sort(key=lambda a: (a[0], a[1]))
    total = int((dur_s + cauda) * SR)
    buf, pos = [], 0
    for tempo, liga, ch, k, v in acoes:
        alvo = min(int(tempo * SR), total)
        if alvo > pos:
            buf.append(np.frombuffer(s.generate(alvo - pos), dtype=np.float32).copy()); pos = alvo
        s.noteon(ch, k, v) if liga else s.noteoff(ch, k)
    if total > pos:
        buf.append(np.frombuffer(s.generate(total - pos), dtype=np.float32).copy())
    x = np.concatenate(buf).reshape(-1, 2)
    # reverb de sala por convolução (resposta ao impulso sintética)
    rng = np.random.default_rng(1)
    L = int(2.2 * SR)
    env = np.exp(-np.arange(L) / (0.45 * SR))
    ir = rng.standard_normal((L, 2)) * env[:, None]
    ir[:int(0.02 * SR)] = 0
    ir /= np.abs(ir).sum(axis=0) / 6
    m = len(x) + L - 1; nf = 1 << (m - 1).bit_length()
    wet = np.stack([np.fft.irfft(np.fft.rfft(x[:, c], nf) * np.fft.rfft(ir[:, c], nf), nf)[:len(x)]
                    for c in range(2)], axis=1)
    y = 0.78 * x + 0.32 * wet / (np.abs(wet).max() + 1e-9) * np.abs(x).max()
    y = y[:int(dur_s * SR)]
    y /= np.abs(y).max() + 1e-9
    tmp = os.path.join(OUT, nome + '_raw.wav')
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((y * 0.9 * 32767).astype('<i2').tobytes())
    final = os.path.join(OUT, nome + '.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-af',
                    f'afade=t=in:d=0.4,afade=t=out:st={dur_s - 1.8}:d=1.8,loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-ar', '44100', final], check=True)
    os.remove(tmp)
    print(final)

PECAS = [canon, gymnopedie, prelude, calma]

if __name__ == '__main__':
    SF, OUT = sys.argv[1], sys.argv[2]
    os.makedirs(OUT, exist_ok=True)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pecas
    for f in PECAS + pecas.PECAS:
        nome = f()[0]
        if not os.path.exists(os.path.join(OUT, nome + '.wav')):
            render(*f())
