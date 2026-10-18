"""Modelo B (faixas) em 4 versoes: 3 Shopee (principal + 2 variacoes) e 1 Reels com link na legenda.
Uso: python3 fazer_b.py <lote/qNN.json> <saida/dir> [--render]
Le o JSON do produto e a montagem_reels.json (clipes, ate, subir, escala) e grava montagem_b{1,2,3,r}.json."""
import json, sys, subprocess
from pathlib import Path
AQUI = Path(__file__).resolve().parent
pj = Path(sys.argv[1]); d = Path(sys.argv[2]); p = json.loads(pj.read_text(encoding="utf-8"))
base = json.loads((d / "montagem_reels.json").read_text(encoding="utf-8")) if (d / "montagem_reels.json").exists() else None
bak = d / "montagem_reels_antigo.json"
if base and base.get("estilo") != "reels_faixas_b":
    if not bak.exists(): bak.write_text(json.dumps(base, ensure_ascii=False))
base = json.loads(bak.read_text(encoding="utf-8"))
V = p["versoes"]; n = p["nome"]
QUENTES = ["E8743B", "F5B82E", "E04F39", "D8A868", "F28C28"]
c0 = (p.get("cor_destaque") or "E8743B").lstrip("#")
if c0 == "auto" or len(c0) != 6: c0 = "E8743B"
outras = [c for c in QUENTES if c.lower() != c0.lower()]
cores = {"b1": c0, "b2": outras[0], "b3": outras[1], "r": outras[2]}
def cena(i, **t):
    b = base["cenas"][i]
    keep = {k: b[k] for k in ("clipe", "ate", "lento", "subir", "escala") if k in b}
    return {**keep, **{k: v for k, v in t.items() if v}}
sh, s2, rl = V["shopee"]["cenas"], V["shopee2"]["cenas"], V["reels"]["cenas"]
def fichas(c): return " · ".join(c.get("fichas") or [])
CTA = "Toque no carrinho"
vers = {}
vers["b1"] = [cena(i, rotulo=sh[i].get("rotulo"), titulo=sh[i]["titulo"], sub=fichas(sh[i]) if i == 2 else None,
                   cta=sh[i].get("cta") if i == 2 else None) for i in range(3)]
vers["b2"] = [cena(i, rotulo=rl[i].get("rotulo") if i == 0 else None, titulo=s2[i]["titulo"], sub=s2[i].get("sub"),
                   cta=CTA if i == 2 else None) for i in range(3)]
ab = sh[0].get("abertura") or {}
t3 = f"[{ab['grande']}] {ab['texto']}" if ab.get("grande") else sh[0]["titulo"]
vers["b3"] = [cena(0, rotulo=sh[0].get("rotulo"), titulo=t3),
              cena(1, rotulo=sh[1].get("rotulo"), titulo=rl[1]["titulo"], sub=rl[1].get("sub")),
              cena(2, rotulo=sh[2].get("rotulo"), titulo=rl[2]["titulo"], sub=fichas(sh[2]), cta=CTA)]
vers["r"] = [cena(i, rotulo=rl[i].get("rotulo"), titulo=rl[i]["titulo"], sub=rl[i].get("sub"),
                  cta="Link na legenda" if i == 2 else None) for i in range(3)]
var = {"b1": dict(inclina=-2, ordem="cor", alinha="esq"), "b2": dict(inclina=2, ordem="preto", alinha="dir"),
       "b3": dict(inclina=-3, ordem="preto", alinha="esq"), "r": dict(inclina=-2, ordem="cor", alinha="esq")}
nome_arq = {"b1": "shopee", "b2": "shopee2", "b3": "shopee3", "r": "reels"}
# 3 layouts Shopee diferentes (regra, 2026-10-16): b1 faixas, b2 tiktok (letras no topo), b3 cartao com selo; reels = faixas
estilo = {"b1": "reels_faixas", "b2": "tiktok_b", "b3": "reels_cartao", "r": "reels_faixas"}
def dims(clipe):
    q = Path(clipe) if Path(clipe).is_absolute() else d / clipe
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(q)],
                       capture_output=True, text=True).stdout.strip().split(",")
    return int(o[0]), int(o[1])
for c in vers["b2"]:  # tiktok_b: quadrado ja fica entre titulo e botao; vertical encolhe para caber ali
    w, h = dims(c["clipe"]); c["subir"], c["escala"] = (-700, 0.56) if w / h < 0.7 else (0, 1.0)
    if c.get("cta"): c["cta_y"] = 1740
for k, cs in vers.items():
    m = {"nome": f"{n}_{nome_arq[k]}", "estilo": estilo[k], "cor_destaque": cores[k], "cenas": cs, "selo": p.get("selo") if k == "b3" else None, **var[k]}
    (d / f"montagem_{nome_arq[k]}.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print("montagens ok", n)
if "--render" in sys.argv:
    so = [x.split("=")[1] for x in sys.argv if x.startswith("--so=")]
    for k in vers:
        a = nome_arq[k]
        if so and a not in so[0].split(","): continue
        prog = [str(AQUI / "montar_video_pro.py"), str(d / f"montagem_{a}.json")] if k == "b2" else \
               [str(AQUI / "gsap" / "montar_gsap.py"), str(d / f"montagem_{a}.json"), str(d / f"{n}_{a}.mp4")]
        for _ in range(2):  # uma nova tentativa se o Chromium falhar
            r = subprocess.run([sys.executable, *prog], capture_output=True, stdin=subprocess.DEVNULL)
            if r.returncode == 0: break
        if r.returncode: print(r.stderr.decode()[-400:])
        print(a, "ok" if r.returncode == 0 else "FALHOU")
