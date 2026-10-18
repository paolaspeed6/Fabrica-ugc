"""Anima as cenas da lista1017 no Pruna (grátis) assim que cada sNN.json aparece.
Uso: python3 -I gerar_lote.py [paralelo=3]
Cena com "pruna": null fica para o código (mover_foto). Bruto em sNN-cenas/pruna/, clipe final sNN-cenas/cenaK.mp4
(primeiros 5,4 s, lado maior 1080, 30 fps) e folha sNN-cenas/pruna/conferencia.jpg (foto 01 + 4 quadros por cena)."""
import json, subprocess, sys, threading, time, queue
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).resolve().parent
LOTE = AQUI.parent / "lote" / "lista1017"
PAR = int(sys.argv[1]) if len(sys.argv) > 1 else 3
LOG = AQUI / "progresso.log"
fila, vistos, lock = queue.Queue(), set(), threading.Lock()
pend = {}

def log(*a):
    with lock, open(LOG, "a") as f:
        f.write(time.strftime("%H:%M:%S ") + " ".join(map(str, a)) + "\n")

def normalizar(raw, dst):
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0", str(raw)], capture_output=True, text=True).stdout.strip().split(","))
    k = 1080 / max(w, h); W, H = int(w * k) // 2 * 2, int(h * k) // 2 * 2
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-t", "5.4", "-an", "-vf",
                    f"scale={W}:{H}:flags=lanczos,fps=30", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)], check=True, stdin=subprocess.DEVNULL)

def folha(js, p):
    base = js.parent
    pdir = base / f"{js.stem}-cenas" / "pruna"
    f01 = Image.open(base / p["fotos"][0]).convert("RGB"); f01.thumbnail((300, 300))
    linhas = []
    for k, c in enumerate(p["cenas"], 1):
        clip = base / c["clipe"]
        if not clip.exists() or not c.get("pruna"):
            continue
        qs = []
        for t in (0.1, 1.8, 3.6, 5.3):
            out = pdir / f"_f{k}_{t}.jpg"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(clip), "-frames:v", "1",
                            "-vf", "scale=300:300:force_original_aspect_ratio=decrease", str(out)], stdin=subprocess.DEVNULL)
            if out.exists():
                qs.append(Image.open(out).convert("RGB")); out.unlink()
        linhas.append(qs)
    if not linhas:
        return
    sheet = Image.new("RGB", (310 * 5, 310 * len(linhas)), "white")
    for i, qs in enumerate(linhas):
        sheet.paste(f01, (0, i * 310))
        for j, q in enumerate(qs):
            sheet.paste(q, (310 * (j + 1), i * 310))
    sheet.save(pdir / "conferencia.jpg", quality=82)

def trabalhador():
    while True:
        js, k, c = fila.get()
        base = js.parent; pdir = base / f"{js.stem}-cenas" / "pruna"; pdir.mkdir(parents=True, exist_ok=True)
        dst = base / c["clipe"]; raw = pdir / f"cena{k}_raw.mp4"
        try:
            p = json.loads(js.read_text(encoding="utf-8"))
            foto = base / p["fotos"][c["foto"]]
            if c.get("recorte"):
                inp = pdir / f"cena{k}_in.png"
                Image.open(foto).convert("RGB").crop(tuple(int(v) for v in c["recorte"])).save(inp)
            else:
                inp = foto
            if not raw.exists():
                r = subprocess.run([sys.executable, "-I", str(AQUI / "pruna_cena.py"), str(inp), str(raw), c["pruna"]],
                                   capture_output=True, text=True, timeout=1500, stdin=subprocess.DEVNULL)
                if not raw.exists():
                    raise RuntimeError((r.stdout + r.stderr)[-300:])
            normalizar(raw, dst)
            log("ok", js.stem, f"cena{k}")
        except Exception as e:
            log("FALHOU", js.stem, f"cena{k}", repr(e)[:300])
        with lock:
            pend[js.stem] -= 1; fim = pend[js.stem] == 0
        if fim:
            try:
                folha(js, json.loads(js.read_text(encoding="utf-8"))); log("PRODUTO", js.stem)
            except Exception as e:
                log("folha falhou", js.stem, repr(e)[:200])
        fila.task_done()

for _ in range(PAR):
    threading.Thread(target=trabalhador, daemon=True).start()
ocioso = 0
while True:
    novos = 0
    for js in sorted(LOTE.glob("s[0-9][0-9].json")):
        if js.stem in vistos:
            continue
        try:
            p = json.loads(js.read_text(encoding="utf-8"))
        except Exception:
            continue  # ainda sendo gravado
        vistos.add(js.stem); novos += 1
        cenas = [(k, c) for k, c in enumerate(p["cenas"], 1) if c.get("pruna") and not (js.parent / c["clipe"]).exists()]
        with lock:
            pend[js.stem] = len(cenas)
        log("fila", js.stem, len(cenas), "cenas")
        for k, c in cenas:
            fila.put((js, k, c))
    ocioso = 0 if (novos or fila.unfinished_tasks) else ocioso + 1
    if (len(vistos) >= 27 and not fila.unfinished_tasks) or ocioso > 120:  # 120 x 30 s sem nada
        break
    time.sleep(30)
log("FIM")
