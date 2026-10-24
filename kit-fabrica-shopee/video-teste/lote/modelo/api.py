"""api() da WaveSpeed igual à do gerar_video.py, mas o log de ids pagos é à prova de falha (o pedidos.log compartilhado deu
Input/output error em 2026-10-20 e perdeu 2 imagens já cobradas) e a consulta do resultado tenta de novo em erro de rede."""
import json, time, urllib.request
from pathlib import Path
LOG = Path(__file__).resolve().parent / "pedidos.log"


def api(modelo, entrada):
    base = "https://api.wavespeed.ai/api/v3"; h = {"Content-Type": "application/json"}
    if __import__("os").environ.get("WAVESPEED_API_KEY"): h["Authorization"] = "Bearer " + __import__("os").environ["WAVESPEED_API_KEY"]
    req = urllib.request.Request(f"{base}/{modelo}", data=json.dumps(entrada).encode(), headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        tarefa = json.load(r)["data"]["id"]
    for _ in range(3):
        try:
            with open(LOG, "a") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {modelo} {tarefa}\n")
            break
        except OSError:
            time.sleep(1)
    fim = time.time() + 900
    while time.time() < fim:
        time.sleep(4)
        try:
            with urllib.request.urlopen(urllib.request.Request(f"{base}/predictions/{tarefa}/result", headers=h), timeout=60) as r:
                d = json.load(r)["data"]
        except Exception:
            continue
        if d["status"] == "completed":
            return d["outputs"][0]
        if d["status"] in ("failed", "cancelled", "timeout", "deleted"):
            raise RuntimeError(f"{modelo}: {d['status']} {d.get('error')}")
    raise RuntimeError(f"{modelo}: sem resultado em 15 min (id {tarefa})")


def baixar(url, destino):
    """baixa para a memória e grava com até 4 tentativas (a pasta do projeto é de rede)."""
    for t in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                dados = r.read()
            Path(destino).parent.mkdir(parents=True, exist_ok=True); Path(destino).write_bytes(dados)
            return destino
        except Exception:
            if t == 3:
                raise
            time.sleep(3 * (t + 1))
