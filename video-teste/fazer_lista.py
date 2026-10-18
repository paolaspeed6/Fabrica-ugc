"""Lote sem gasto: cenas por código (mover_foto.py) + 4 versões do modelo B (fazer_b.py) + legendas + folha de conferência.

Uso: python3 fazer_lista.py lote/lista1016/r01.json [...]
Cada produto: saida/<nome>/<nome>_{shopee,shopee2,shopee3,reels}.mp4, legendas.txt e conferencia.jpg
(5 instantes de cada versão: 0,5 s, meio de cada cena e fim). Nenhuma API paga é chamada.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from auditar_video import auditar
from sem_nota import checar as checar_nota

AQUI = Path(__file__).resolve().parent
VERS = ["shopee", "shopee2", "shopee3", "reels"]
ROT = {"shopee": "Shopee Vídeo (edição 1, faixas)", "shopee2": "Shopee Vídeo (edição 2, letras no topo)",
       "shopee3": "Shopee Vídeo (edição 3, cartão)", "reels": "Reels (Instagram/Facebook), link na legenda"}


def clipes(p, base):
    out = []
    for c in p["cenas"]:
        dst = base / c["clipe"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            cmd = [sys.executable, str(AQUI / "mover_foto.py"), str(base / p["fotos"][c["foto"]]), str(dst),
                   "--mov", c.get("codigo", "push"), "--zoom", str(c.get("zoom", 1.08))]
            if c.get("recorte"):
                cmd += ["--recorte", ",".join(str(int(v)) for v in c["recorte"])]
            subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)
        out.append(dst)
    return out


def legendas(p, saida):
    L = p["legendas"]
    txt = []
    for v in VERS:
        corpo = L.get(v, "")
        if v == "reels":
            if "Link do produto" not in corpo:
                corpo += f"\nLink do produto: {p['link']}"
            if p.get("hashtags", {}).get("reels"):
                corpo += "\n" + p["hashtags"]["reels"]
        txt.append(f"== {ROT[v]} ==\n{corpo}\n")
    (saida / "legendas.txt").write_text("\n".join(txt), encoding="utf-8")


def conferencia(p, saida):
    larg = 200
    fonte = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf", 18)
    tempos = [0.5, 2.6, 7.5, 12.4, 14.6]
    linhas = []
    for v in VERS:
        mp4 = saida / f"{p['nome']}_{v}.mp4"
        qs = []
        for t in tempos:
            png = saida / f"_q{t}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(mp4), "-frames:v", "1",
                            "-vf", f"scale={larg}:-2", str(png)], check=True, stdin=subprocess.DEVNULL)
            qs.append(Image.open(png).convert("RGB"))
            png.unlink()
        linhas.append((v, qs))
    alt = linhas[0][1][0].height
    folha = Image.new("RGB", (larg * 5 + 40, (alt + 26) * 4), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for k, (v, qs) in enumerate(linhas):
        y = k * (alt + 26)
        d.text((4, y + 2), f"{p['nome']} · {v}", font=fonte, fill=(0, 0, 0))
        for j, q in enumerate(qs):
            folha.paste(q, (j * (larg + 10), y + 24))
    folha.save(saida / "conferencia.jpg", quality=80)


def main():
    for arq in sys.argv[1:]:
        arq = Path(arq).resolve()
        p = json.loads(arq.read_text(encoding="utf-8"))
        base = arq.parent
        anuncio = base / Path(p["fotos"][0]).parent / "anuncio.json"
        ruins = checar_nota(p, json.loads(anuncio.read_text(encoding="utf-8")) if anuncio.exists() else None)
        if ruins:  # a dona 2026-10-17: nota e avaliacoes mudam; nunca o numero exato
            print("BLOQUEADO (nota/avaliações exatas):", p["nome"], ruins)
            continue
        saida = AQUI / "saida" / p["nome"]
        saida.mkdir(parents=True, exist_ok=True)
        cs = clipes(p, base)
        cenas = [{"clipe": str(c), "ate": 5.33, "lento": p["cenas"][i].get("lento", 1.0),
                  "subir": p["cenas"][i].get("subir", 0), "escala": p["cenas"][i].get("escala", 1.0)}
                 for i, c in enumerate(cs)]
        (saida / "montagem_reels_antigo.json").write_text(
            json.dumps({"nome": p["nome"], "estilo": "base", "cenas": cenas}, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(AQUI / "fazer_b.py"), str(arq), str(saida), "--render"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        print(r.stdout.strip(), r.stderr.strip()[-300:])
        legendas(p, saida)
        if all((saida / f"{p['nome']}_{v}.mp4").exists() for v in VERS):
            conferencia(p, saida)
            # a dona 2026-10-18: superar as referências; o que reprovar aqui não vai para ela sem correção
            linhas = []
            for v in VERS:
                falhas, info = auditar(str(saida / f"{p['nome']}_{v}.mp4"))
                linhas.append(("REPROVADO " if falhas else "APROVADO  ") + v + " " + str(info))
                linhas += ["   - " + f for f in falhas]
            (saida / "auditoria.txt").write_text("\n".join(linhas), encoding="utf-8")
            print("\n".join(linhas))
            print("PRONTO", p["nome"])
        else:
            print("FALTOU VÍDEO", p["nome"])


if __name__ == "__main__":
    main()
