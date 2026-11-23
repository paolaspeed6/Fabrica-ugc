r"""Alerta sonoro "precisa de você" (captcha, PIN, login): som próprio, inconfundível.

    from alerta import alerta_kevin
    alerta_kevin('captcha')      # toca no máx. 1 vez a cada 45 s (chamar dentro do loop de espera)

O som (sons\atencao.wav) é gerado aqui mesmo, sem baixar nada: arpejo ascendente de videogame
(523-659-784-1047 Hz, onda quadrada suave + vibrato), mini-sirene e um "bloop" descendente.
"""
import math, os, struct, time, wave

BASE = r'C:\horst\tablet'
WAV = os.path.join(BASE, 'sons', 'atencao.wav')
INTERVALO = 45  # s entre repetições
TAXA = 44100
_ultimo = 0.0


def _onda_quadrada_suave(f, t):
    # soma das 3 primeiras harmônicas ímpares = quadrada "arredondada"
    return (math.sin(2 * math.pi * f * t) + math.sin(6 * math.pi * f * t) / 3 + math.sin(10 * math.pi * f * t) / 5) * 0.8


def gerar_wav(caminho=WAV):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    amostras = []

    def tom(freq_ini, freq_fim, dur, vib=6.0, prof=0.012, vol=0.45):
        n = int(TAXA * dur)
        fase = 0.0
        for i in range(n):
            t = i / TAXA
            f = freq_ini + (freq_fim - freq_ini) * (i / n)
            f *= 1 + prof * math.sin(2 * math.pi * vib * t)
            fase += f / TAXA
            env = min(1.0, i / (0.006 * TAXA)) * min(1.0, (n - i) / (0.02 * TAXA))
            v = (math.sin(2 * math.pi * fase) + math.sin(6 * math.pi * fase) / 3 + math.sin(10 * math.pi * fase) / 5) * 0.8
            amostras.append(v * env * vol)

    def silencio(d):
        amostras.extend([0.0] * int(TAXA * d))

    for f in (523, 659, 784, 1047):          # arpejo ascendente (90 ms cada)
        tom(f, f, 0.09)
        silencio(0.015)
    for _ in range(2):                        # mini-sirene de nave
        tom(880, 1320, 0.16, vib=11, prof=0.02, vol=0.38)
        tom(1320, 880, 0.16, vib=11, prof=0.02, vol=0.38)
    silencio(0.04)
    tom(1100, 180, 0.32, vib=4, prof=0.03, vol=0.5)   # "bloop" descendente
    with wave.open(caminho, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TAXA)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, a)) * 26000)) for a in amostras))
    return caminho


STATUS_PC = os.path.join(BASE, 'central', 'status_pc.json')  # a Central reescreve a cada ~30 s


def central_aberta(limite=90):
    try:
        return time.time() - os.path.getmtime(STATUS_PC) < limite
    except OSError:
        return False


def alerta_kevin(motivo='', status_path=None, forcar=False):
    """'Precisa de você' (captcha / PIN / login).
    1) Grava status_path (o status.json do card da automação) com state 'alerta' e detail = motivo:
       a Central mostra o aviso vermelho e toca o som ela mesma.
    2) Só toca o atencao.wav daqui se a Central estiver fechada (status_pc.json parado há > 90 s).
    No máx. 1 som a cada 45 s (chamar dentro do loop de espera), salvo forcar=True."""
    global _ultimo
    if status_path:
        try:
            import json
            try:
                st = json.load(open(status_path, encoding='utf-8'))
            except Exception:
                st = {}
            st.update(state='alerta', detail=motivo, quando=time.strftime('%H:%M:%S'))
            json.dump(st, open(status_path, 'w', encoding='utf-8'), ensure_ascii=False)
        except Exception:
            pass
    if not forcar and (central_aberta() or time.time() - _ultimo < INTERVALO):
        return False
    _ultimo = time.time()
    try:
        import winsound
        # som escolhido pelo Kevin (05/11): marimba C6-E6-G6 a 22% do volume (aprovado pelo Kevin; não mudar) (sons\opcao1.wav -> atencao.wav).
        # gerar_wav() é o som antigo (sirene) que ele NÃO quis: não usar.
        if not os.path.exists(WAV):
            return False
        winsound.PlaySound(WAV, winsound.SND_FILENAME | winsound.SND_ASYNC)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    gerar_wav()
    import winsound
    winsound.PlaySound(WAV, winsound.SND_FILENAME)
    print('ok', WAV)
