"""Fotos originais (Seedream v4 Edit) das cenas da lista1017b, com teto de gasto travado.
Uso: python3 -I fotos_ia.py TETO_USD [tNN ...]   (sem tNN: todos os tNN.json da pasta)
Cena com "editar" e sem tNN-cenas/cenaK.png é gerada a partir das fotos reais em "refs".
Cada chamada reserva US$ 0,027 antes de sair; passando do teto, para. Folha por produto em folhas/tNN.jpg
(foto 01 do anúncio + as 3 fotos novas)."""
import base64, json, mimetypes, sys, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import gerar_video  # noqa: E402
from produzir import COMPOSICAO, PROIBIDO  # noqa: E402

L = AQUI.parent / "lote" / "lista1017b"
TETO = float(sys.argv[1])
PRECO = gerar_video.CUSTO_IMAGEM_USD
gasto, lock = [0.0], threading.Lock()
LOG = L / "fotos.log"


def log(*a):
    with lock, open(LOG, "a") as f:
        f.write(time.strftime("%H:%M:%S ") + " ".join(map(str, a)) + "\n")


def ref(p):
    tipo = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return f"data:{tipo};base64,{base64.b64encode(p.read_bytes()).decode()}"


def gerar(js, k, c, fotos):
    out = js.parent / f"{js.stem}-cenas" / f"cena{k}.png"
    with lock:
        if gasto[0] + PRECO > TETO + 1e-9:
            log("TETO", js.stem, k); return
        gasto[0] += PRECO
    try:
        url = gerar_video.api(gerar_video.MODELO_IMAGEM, {
            "prompt": c["editar"] + COMPOSICAO + PROIBIDO,
            "images": [ref(js.parent / fotos[i]) for i in c.get("refs", [0])],
            "size": c.get("tamanho", "1080*1920")})
        out.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, out)
        log("ok", js.stem, k)
    except Exception as e:  # noqa: BLE001
        log("FALHOU", js.stem, k, repr(e)[:200])


def folha(js, p):
    base = js.parent
    ims = [base / p["fotos"][0]] + [base / f"{js.stem}-cenas/cena{k}.png" for k in (1, 2, 3)]
    W, H = 360, 640
    sheet = Image.new("RGB", (W * 4 + 30, H + 40), "white")
    d = ImageDraw.Draw(sheet); d.text((8, 8), f"{js.stem} · anúncio | cena 1 | cena 2 | cena 3", fill="black")
    for i, f in enumerate(ims):
        if f.exists():
            im = Image.open(f).convert("RGB"); im.thumbnail((W, H)); sheet.paste(im, (i * (W + 10), 36))
    (L / "folhas").mkdir(exist_ok=True)
    sheet.save(L / "folhas" / f"{js.stem}.jpg", quality=80)


def main():
    alvo = sys.argv[2:]
    arqs = [L / f"{t}.json" for t in alvo] if alvo else sorted(L.glob("t[0-9][0-9].json"))
    tarefas = []
    for js in arqs:
        p = json.loads(js.read_text(encoding="utf-8"))
        for k, c in enumerate(p["cenas"], 1):
            if c.get("editar") and not (js.parent / f"{js.stem}-cenas/cena{k}.png").exists():
                tarefas.append((js, k, c, p["fotos"]))
    log("inicio", len(tarefas), "fotos, teto", TETO)
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda t: gerar(*t), tarefas))
    for js in arqs:
        folha(js, json.loads(js.read_text(encoding="utf-8")))
    log("fim, reservado US$", f"{gasto[0]:.3f}")
    print(f"{len(tarefas)} pedidas, reservado US$ {gasto[0]:.3f}")


if __name__ == "__main__":
    main()
