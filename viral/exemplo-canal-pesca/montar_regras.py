"""Monta o vídeo "As Regras do Rio" (canal de exemplo) a partir das cenas do Veo e da narração, custo zero.
Uso: python3 montar_regras.py roteiro.json saida.mp4
- câmera nunca travada: push-in leve por código em cima do movimento do Veo
- cor de cinema igual em todas as cenas (teal e âmbar, vinheta, grão)
- som: pancada grave no quadro 0 (interrupção), som nativo baixo, narração por cima, "sopro" quando o lampião apaga
- legenda palavra por palavra e carimbos na camada GSAP (camada_regras.html)
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FPS = 30

def sh(*a, saida=False):
    r = subprocess.run(a, check=True, capture_output=True, text=True)
    return r.stdout + r.stderr if saida else None

def dur(p):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p), saida=True).strip())

def falas(audio, n_frases):
    """Trechos com voz (início, fim). Junta trechos até sobrar n_frases (as pausas <#x#> do texto)."""
    log = sh("ffmpeg", "-i", str(audio), "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-", saida=True)
    ini = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    fim = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    total = dur(audio)
    starts = [0.0] + ini if not fim or fim[0] > 0.05 else ini
    ends = fim if len(fim) >= len(starts) else fim + [total]
    seg = [(s, e) for s, e in zip(starts, ends) if e - s > 0.12]
    while len(seg) > n_frases:  # junta a menor pausa
        k = min(range(len(seg) - 1), key=lambda i: seg[i + 1][0] - seg[i][1])
        seg[k:k + 2] = [(seg[k][0], seg[k + 1][1])]
    return seg

def trechos(audio):
    log = sh("ffmpeg", "-i", str(audio), "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-", saida=True)
    ini = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    fim = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    total = dur(audio)
    starts = ([0.0] if not fim or fim[0] > 0.05 else []) + ini
    ends = [f for f in fim if f > 0.05] + [total]
    return [(a, b) for a, b in zip(starts, ends) if b - a > 0.08]

def apertar(audio, saida, tempo=1.08):
    """Encurta as pausas da voz (o TTS estica as reticências): pausa normal vira 0,3 s, pausa dramática 0,6 s."""
    seg = trechos(audio)
    partes = []
    for k, (a, b) in enumerate(seg):
        partes.append(f"[0:a]atrim={max(0, a - 0.04)}:{b + 0.06},asetpts=PTS-STARTPTS[s{k}]")
        if k + 1 < len(seg):
            gap = 0.6 if seg[k + 1][0] - b > 0.9 else 0.3
            partes.append(f"anullsrc=r=44100:cl=mono,atrim=duration={gap}[g{k}]")
    ordem = "".join(f"[s{k}]" + (f"[g{k}]" if k + 1 < len(seg) else "") for k in range(len(seg)))
    n = 2 * len(seg) - 1
    sh("ffmpeg", "-y", "-i", str(audio), "-filter_complex",
       ";".join(partes) + f";{ordem}concat=n={n}:v=0:a=1,atempo={tempo}[a]", "-map", "[a]", "-ar", "44100", "-ac", "1", str(saida))
    return saida

def palavras_com_tempo(texto, audio, desloc):
    frases = [f.strip() for f in re.split(r"<#[\d.]+#>", texto) if f.strip()]
    seg = falas(audio, len(frases))
    if len(seg) < len(frases):  # não achou todas as pausas: trata tudo como 1 trecho
        frases, seg = [" ".join(frases)], [(seg[0][0], seg[-1][1])]
    out = []
    for f, (s, e) in zip(frases, seg):
        ws = f.split()
        pesos = [len(re.sub(r"\W", "", w)) + 2 for w in ws]
        t = s
        for w, p in zip(ws, pesos):
            d = (e - s) * p / sum(pesos)
            out.append({"t": w, "ini": round(desloc + t, 3), "fim": round(desloc + t + d, 3), "frase_fim": w is ws[-1]})
            t += d
    return out

def grupos(ps, maximo=3, chars=0):
    g, atual = [], []
    for p in ps:
        atual.append(p)
        cheio = (len(" ".join(x["t"] for x in atual)) >= chars) if chars else len(atual) == maximo
        if cheio or p["frase_fim"]:
            g.append(atual); atual = []
    if atual: g.append(atual)
    res = []
    for i, a in enumerate(g):
        fim = a[-1]["fim"] + 0.25
        if i + 1 < len(g): fim = min(fim, g[i + 1][0]["ini"])
        res.append({"ini": a[0]["ini"], "fim": round(fim, 3), "palavras": [{"t": p["t"], "ini": p["ini"], "fim": p["fim"]} for p in a]})
    return res

def main():
    R = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    saida = Path(sys.argv[2]).resolve()
    base = AQUI.parent
    tmp = Path(tempfile.mkdtemp(dir=AQUI))
    for c in R["cenas"] + [R["fim"]]:
        c["voz"] = str(apertar(base / c["voz"], tmp / (Path(c["voz"]).stem + "_a.wav"), R.get("tempo_voz", 1.08)))
    t, partes, vozes, todas = 0.0, [], [], []
    for i, c in enumerate(R["cenas"]):
        clipe, voz = base / c["clipe"], base / c["voz"]
        dv, dc = dur(voz), dur(clipe)
        alvo = max(dc, dv + c.get("desloc", 0.3) + c.get("folga", 0.35))
        if c.get("flex"):  # clipe feito por código: dura o tempo da fala
            alvo = min(dc, dv + c.get("desloc", 0.3) + c.get("folga", 0.35))
        lento = alvo / dc  # se a fala for maior que o clipe, o clipe desacelera um pouco
        if lento > 1.45: sys.exit(f"cena {i+1}: fala de {dv:.1f}s não cabe no clipe de {dc:.1f}s")
        z = c.get("zoom", 0.06)
        n = round(alvo * FPS)
        p = tmp / f"c{i}.mp4"
        sh("ffmpeg", "-y", "-i", str(clipe), "-filter_complex",
           f"[0:v]setpts={lento}*PTS,fps={FPS},scale=1080:1920:flags=lanczos,"
           f"zoompan=z='1+{z}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},"
           f"eq=contrast=1.06:saturation=0.92,colorbalance=bs=0.05:gs=0.02:rh=0.04:gh=0.02,"
           f"vignette=PI/4.5,noise=alls=7:allf=t,trim=duration={alvo},setpts=PTS-STARTPTS[v];"
           f"[0:a]atempo={1/lento},volume={c.get('vol_amb', 0.45)},apad,atrim=duration={alvo}[a]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-ar", "44100", str(p))
        partes.append(p)
        d = t + c.get("desloc", 0.3)
        vozes.append((voz, d))
        ps = palavras_com_tempo(c["texto"], voz, d)
        todas.append(ps)
        c["_ini"], c["_fim"] = t, t + alvo
        t += alvo
    # tela final preta
    fim_ini, fim_dur = t, R["fim"]["dur"]
    vf = R["fim"]["voz"]  # já é caminho absoluto
    preto = tmp / "preto.mp4"
    if R["fim"].get("clipe"):  # tela final em cima de uma cena (loop com o começo), não no preto
        sh("ffmpeg", "-y", "-i", str(base / R["fim"]["clipe"]), "-filter_complex",
           f"[0:v]fps={FPS},scale=1080:1920,eq=contrast=1.04:saturation=0.95,vignette=PI/4.5,noise=alls=7:allf=t,trim=duration={fim_dur},setpts=PTS-STARTPTS[v];[0:a]volume=0.4,apad,atrim=duration={fim_dur}[a]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-ar", "44100", "-ac", "2", str(preto))
    else:
        sh("ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}:d={fim_dur}", "-f", "lavfi", "-i",
           f"anullsrc=r=44100:cl=stereo", "-t", str(fim_dur), "-c:v", "libx264", "-crf", "16", "-c:a", "aac", str(preto))
    partes.append(preto)
    vozes.append((base / vf, fim_ini + R["fim"].get("desloc", 0.35)))
    ps_fim = palavras_com_tempo(R["fim"]["texto"], base / vf, fim_ini + R["fim"].get("desloc", 0.35))
    fim_clipe = R["fim"].get("clipe")
    total = fim_ini + fim_dur
    lista = tmp / "lista.txt"
    lista.write_text("".join(f"file '{p}'\n" for p in partes))
    junto = tmp / "junto.mp4"
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-ar", "44100", "-ac", "2", str(junto))

    # carimbos: tempo da palavra-chave
    def quando(palavra, depois=0.0):
        for ps in todas + [ps_fim]:
            for p in ps:
                if p["ini"] >= depois and re.sub(r"\W", "", p["t"]).lower().startswith(palavra.lower()): return p["ini"]
        raise SystemExit(f"palavra-chave não achada: {palavra}")
    carimbos = []
    for c in R["carimbos"]:
        ini = quando(c["em"])
        cena = next(x for x in R["cenas"] if x["_ini"] <= ini < x["_fim"])
        passo = (quando(c["passo_em"], ini) - ini) if c.get("passo_em") else c.get("passo", .15)
        carimbos.append({"linhas": c["linhas"], "ini": ini, "fim": cena["_fim"] if not c.get("ate") else quando(c["ate"], ini + 0.01), "passo": passo, "tremer": c.get("tremer", False)})
    gs = [g for ps in todas + ([ps_fim] if R.get("legenda_no_fim") else []) for g in grupos(ps, chars=R.get("legenda_chars", 0))]  # sem legenda na tela final: ela já tem o texto grande
    dados = {"fim": total, "hook_fim": R["cenas"][0]["_fim"], "carimbos": carimbos, "grupos": gs,
             "fim_ini": fim_ini, "prox_atraso": (quando(R["fim"]["prox_em"]) - fim_ini) if R["fim"].get("prox_em") else 0.0}
    (tmp / "dados.json").write_text(json.dumps(dados, ensure_ascii=False))
    camada = tmp / "camada.mov"
    dados_extra = R.get("camada_dados", {})
    d2 = json.loads((tmp / "dados.json").read_text()); d2.update(dados_extra); (tmp / "dados.json").write_text(json.dumps(d2, ensure_ascii=False))
    subprocess.run(["node", str(AQUI / "render_regras.js"), str(AQUI / R.get("camada", "camada_regras.html")), str(tmp / "dados.json"), str(camada), str(FPS)], check=True)

    # som: pancada grave no 0, sopro do lampião no preto, vozes
    ent = ["-i", str(junto), "-i", str(camada),
           "-f", "lavfi", "-t", "1.6", "-i", "sine=f=48:r=44100",
           "-f", "lavfi", "-t", "0.5", "-i", "anoisesrc=r=44100:a=0.6:c=brown"]
    filt = ["[2:a]afade=t=out:st=0.02:d=1.5,volume=2.4,aformat=channel_layouts=stereo[boom]",
            f"[3:a]lowpass=f=900,afade=t=in:d=0.04,afade=t=out:st=0.08:d=0.4,volume=1.2,adelay={int(fim_ini*1000)}|{int(fim_ini*1000)},aformat=channel_layouts=stereo[sopro]"]
    mix = ["[0:a]", "[boom]", "[sopro]"]
    for k, (v, d) in enumerate(vozes):
        ent += ["-i", str(v)]
        filt.append(f"[{4+k}:a]volume={R.get('vol_voz', 1.6)},aformat=channel_layouts=stereo,adelay={int(d*1000)}|{int(d*1000)}[v{k}]")
        mix.append(f"[v{k}]")
    filt.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.95,atrim=duration={total}[a]")
    filt.append("[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]")
    sh("ffmpeg", "-y", *ent, "-filter_complex", ";".join(filt), "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", str(saida))
    (saida.with_suffix(".tempos.json")).write_text(json.dumps(dados, ensure_ascii=False, indent=1))
    subprocess.run(["rm", "-rf", str(tmp)])
    print(f"Pronto: {saida} ({total:.1f}s)")

main()
