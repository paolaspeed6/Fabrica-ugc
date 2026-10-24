"""Método atual da fábrica (Lista 24/10 A do Kevin): ficha do Fichador -> Nano Banana 2.1 Edit (cena) ->
Fiscal de imagem -> Seedance 1.5 Pro Fast i2v 5 s -> Fiscal de vídeo. Teto duro TETO_USD sobre gasto.json (preços medidos: NB 0,0396; Seedance 0,10).
Kevin 2026-10-23 11:18: sem zoom em letras pequenas (a câmera para em plano médio), mas vídeo UGC de verdade, não print parada.
Regra 12 (2026-10-23): a câmera só mostra o que a imagem de partida já mostra (nada de passar por cima, por trás ou do lado).
câmera parada na IA (Seedance avança demais): FIXA=1 TETO_USD=... gerar.py clipes ...; o montar.py move a câmera por código.
uso: TETO_USD=8.50 python3 -I gerar.py imagens|clipes pNN [cenas]   (pula o que já existe; refazer = apagar o arquivo e
     pôr "fix_img"/"fix_vid" na cena da ficha, que entra no fim do prompt)"""
import json, os, sys, base64
try:
    import fcntl
except ImportError:  # Windows: a trava entre processos fica só a do próprio processo
    fcntl = None
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock
B = Path(__file__).resolve().parent
sys.path.insert(0, str(B)); from api import api, baixar
TETO = float(os.environ.get("TETO_USD", "0")); gf = B / "gasto.json"; trava = Lock()


def ref(f): return "data:image/jpeg;base64," + base64.b64encode((B / f).read_bytes()).decode()


def cobrar(nome, usd):
    with trava, open(B / "gasto.lock", "w") as lk:  # trava entre processos (2 processos corromperam o gasto.json em 2026-10-23)
        if fcntl: fcntl.flock(lk, fcntl.LOCK_EX)
        g = json.loads(gf.read_text()) if gf.exists() else {"usd": 0.0, "itens": []}
        if g["usd"] + usd > TETO + 1e-9: raise RuntimeError(f"TETO atingido antes de {nome}")
        g["usd"] = round(g["usd"] + usd, 4); g["itens"].append([nome, usd])
        tmp = gf.with_suffix(".tmp"); tmp.write_text(json.dumps(g, indent=1)); os.replace(tmp, gf)


FIM = (" Photorealistic full-frame vertical 9:16 photo taken by a person with a recent smartphone main camera, 26 mm lens, everything in natural focus. "
       "Modern, new, well-kept and aspirational space with clean contemporary finishes; motivated natural light with soft contrast and depth (foreground, product, background). "
       "True-to-life colors with neutral white balance; the product's colors match image 1 exactly. Calm wide textures. It contains only the objects described. Fine sensor grain. "
       "The whole product is in frame with clear space on every side, never touching the frame edges. "
       "Candid premium UGC photo, not a catalog shot, not a studio render. Ignore every advertising headline, badge, icon, arrow, measurement label and watermark printed on the reference images; they are not part of the product. "
       "No phone frame, no device bezel, no borders, no added text.")


def ficha(p): return json.loads((B / f"{p}-ficha.json").read_text())
def j(v): return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def descr(f):
    return (f"The product: {j(f['nome_curto'])}. Variant: {j(f['variante'])}. Items: {j(f['itens'])}. Parts: {j(f['partes'])}. "
            f"Lettering exactly: {j(f['letras'])}. Real size: {j(f['tamanho_real'])}. Count: {j(f.get('contagem', ''))}. Never show: {j(f['proibidos'])}.")


def vdescr(f):
    """descrição curta para o VÍDEO: o Seedance desenha tudo o que o prompt cita, até na lista do que não pode aparecer
    (p03 ganhou vinho e taças, p05 e p06 ganharam os gráficos e textos do anúncio; Lista 24/10 A). Só o que existe no quadro."""
    partes = [x for x in f['partes'] if not any(w in x.lower() for w in ('not to be shown', 'never', 'not shown', 'hidden', 'nunca', 'não aparece', 'traseira', 'back ('))]  # p06: "LED da traseira (não mostrar)" virou LED na tela
    # Lista 24/10 A p03: itens "(a mesa, vaso, xícara... da foto 01 não são vendidos)" e partes "Layout in photo 01: ... side table"
    # fizeram vaso, xícara e livros surgirem. Tira parênteses, menções a foto e partes de layout/conferência.
    import re
    def limpa(s):
        s = re.sub(r'\s*\([^)]*\)', '', s)
        s = re.sub(r'[;,]?\s*(?:no chairs|no table is sold|not sold)[^.;]*', '', s, flags=re.I)
        s = re.sub(r'(?:,\s*)?\s*(?:as\s+)?(?:seen\s+|read\s+)?(?:in|from)\s+(?:the\s+)?photos?\s+\d+(?:\s*(?:,|and)\s*\d+)*', '', s, flags=re.I)
        s = re.sub(r'[;,]?\s*not visible in the photos', '', s, flags=re.I)
        return re.sub(r'\s{2,}', ' ', s).strip()
    partes = [limpa(x) for x in partes if not re.match(r'\s*(layout|orientation|positions checked|proportions)', x, re.I)]
    return f"The product: {j(f['nome_curto'])}. Items: {j([limpa(x) for x in f['itens']])}. Parts: {j(partes)}."


def cena(f, c): return next(x for x in f["cenarios"] if x["id"] == c)


def imagem(p, c):
    d = B / f"{p}-cenas"; d.mkdir(exist_ok=True); out = d / f"{c}.jpg"
    if out.exists(): return f"{p} {c}.jpg já existe"
    f = ficha(p); s = cena(f, c); cobrar(f"img {p}{c}", 0.0396)
    txt = descr(f) + f" Image 1 is the exact product and color. Setting: {s['texto']} {s['scale']} {s['camera']}" + FIM + (" " + s["fix_img"] if s.get("fix_img") else "")
    u = api("google/nano-banana-2.1/edit", {"prompt": txt, "images": [ref(f"{p}-fotos/{x}" if "/" not in x else x) for x in f["fotos_ref"]],
                                             "aspect_ratio": "9:16", "resolution": "1k", "output_format": "jpeg"})
    baixar(u, out); (d / f"{c}.img.txt").write_text(txt); return f"{p} {c}.jpg ok"


FIXA = os.environ.get("FIXA") == "1"  # Seedance avança mesmo pedindo "sem avanço" -> camera_fixed; montar.py põe a câmera por código


def clipe_fixo(p, c):
    """câmera parada na IA (camera_fixed): cenário vivo, produto parado; nunca cita objeto que não existe (regra 1)."""
    d = B / f"{p}-cenas"; out = d / f"{c}_fixa.mp4"
    if out.exists(): return f"{p} {c}_fixa.mp4 já existe"
    f = ficha(p); cobrar(f"clipe fixo {p}{c}", 0.10)
    t = (f"Locked-off tripod shot of the exact scene in the image: the framing stays identical for the whole clip. "
         f"The {f['nome_curto']} stays perfectly still and unchanged, with exactly the same shape, colors, logo and lettering as in the first frame. "
         "The room, the objects and the light stay exactly as they are in the image; only a very faint, natural shimmer of light and air keeps it alive, "
         "like a real video of a quiet room. Photorealistic, true-to-life colors.")
    u = api("bytedance/seedance-v1.5-pro/image-to-video-fast", {"prompt": t, "image": ref(f"{p}-cenas/{c}.jpg"), "resolution": "720p", "duration": 5,
                                                                 "generate_audio": False, "aspect_ratio": "9:16", "camera_fixed": True})
    baixar(u, out); (d / f"{c}_fixa.prompt.txt").write_text(t); return f"{p} {c}_fixa.mp4 ok"


def clipe(p, c):
    if FIXA: return clipe_fixo(p, c)


def clipe(p, c):
    d = B / f"{p}-cenas"; out = d / f"{c}.mp4"
    if out.exists(): return f"{p} {c}.mp4 já existe"
    f = ficha(p); s = cena(f, c); cobrar(f"clipe {p}{c}", 0.10)
    t = (f"Handheld smartphone UGC video, one continuous shot with no cuts, filmed by a real person. {s['movimento']} Gentle natural hand sway, slow and steady speed. "
         f"The camera only reveals what is already visible in the first frame: it never rises above the top of the product, never goes behind or around it, "
         f"and stops at a medium shot where the whole product is still in frame; no close-up on small lettering. "
         f"{vdescr(f)} {s['scale']} The product stays perfectly still, rigid and solid, exactly as in the first frame: same shape, size, count, colors, logo and lettering; "
         f"no part of it rotates, tilts, opens or slides; only the camera moves. "
         "Plain real camera footage of only what is in the first frame; every surface keeps exactly what it shows in the first frame. Stable textures, solid objects keep their exact shape. The light stays constant."
         + (" " + s["fix_vid"] if s.get("fix_vid") else ""))
    u = api("bytedance/seedance-v1.5-pro/image-to-video-fast", {"prompt": t, "image": ref(f"{p}-cenas/{c}.jpg"), "resolution": "720p", "duration": 5,
                                                                 "generate_audio": False, "aspect_ratio": "9:16"})
    baixar(u, out); (d / f"{c}.prompt.txt").write_text(t); return f"{p} {c}.mp4 ok"


if __name__ == "__main__":
    fn = imagem if sys.argv[1] == "imagens" else clipe
    ps = sys.argv[2].replace(" ", ",").split(","); cenas = sys.argv[3] if len(sys.argv) > 3 else "ABC"
    tarefas = [(p[:3], p[3]) if len(p) == 4 else None for p in ps if p]  # "p01A,p02B" ou "p01,p02" + cenas
    tarefas = [t for t in tarefas if t] or [(p, c) for p in ps for c in cenas]
    tarefas = [t for t in tarefas if t[1]] if all(len(p) == 4 for p in ps if p) else [(p, c) for p in ps for c in cenas]

    def run(pc):
        try: return fn(*pc)
        except Exception as e: return f"{pc} ERRO {e}"
    with ThreadPoolExecutor(6) as ex:
        for r in ex.map(run, tarefas): print(r, flush=True)
    print("gasto", json.loads(gf.read_text())["usd"] if gf.exists() else 0)
