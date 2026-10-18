"""Gera uma cena do vídeo viral de pesca na WaveSpeed, com teto de gasto.

Uso: python3 gerar.py <nome> <modelo> <json_entrada> --teto USD_LOTE --max USD_CHAMADA [--medir]
Para antes de chamar se o gasto desde o início do lote (arquivo gasto.json) já passa do teto.
"""
import json, sys, time, urllib.request
import custo
from pathlib import Path

API = "https://api.wavespeed.ai/api/v3/"
AQUI = Path(__file__).resolve().parent
CENAS = AQUI / "cenas"; CENAS.mkdir(exist_ok=True)
GASTO = AQUI / "gasto.json"

def req(url, dados=None):
    r = urllib.request.Request(url, data=json.dumps(dados).encode() if dados else None,
                               headers={"Content-Type": "application/json"}, method="POST" if dados else "GET")
    with urllib.request.urlopen(r, timeout=120) as f:
        return json.load(f)

def saldo(): return req(API + "balance")["data"]["balance"]

nome, modelo, entrada = sys.argv[1], sys.argv[2], json.loads(Path(sys.argv[3]).read_text())
if "--teto" not in sys.argv or "--max" not in sys.argv:
    sys.exit("PARADO: diga --teto (máximo aprovado do lote) e --max (máximo desta chamada)")
teto = float(sys.argv[sys.argv.index("--teto") + 1])
maximo = float(sys.argv[sys.argv.index("--max") + 1])
g = json.loads(GASTO.read_text()) if GASTO.exists() else {"inicio": saldo(), "itens": []}
antes = saldo()
gasto = g["inicio"] - antes
if gasto >= teto:
    sys.exit(f"PARADO: gasto do lote US$ {gasto:.3f} já chegou ao teto US$ {teto}")
if "--medir" in sys.argv:  # modelo novo: só um trecho curto, e o teto da chamada ainda vale
    previsto = maximo
    print(f"MEDINDO {modelo} com teto de US$ {maximo}")
else:
    previsto = custo.conferir(modelo, entrada, maximo, gasto, teto)
    print(f"pior caso US$ {previsto}")
d = req(API + modelo, entrada)["data"]
for _ in range(200):
    time.sleep(5)
    r = req(d["urls"]["get"])["data"]
    if r["status"] in ("completed", "failed"): break
if r["status"] != "completed":
    sys.exit(f"FALHOU: {r.get('error')}")
url = r["outputs"][0]
ext = url.rsplit(".", 1)[-1].split("?")[0]
destino = CENAS / f"{nome}.{ext}"
urllib.request.urlretrieve(url, destino)
time.sleep(3)
depois = saldo()
g["itens"].append({"nome": nome, "modelo": modelo, "custo": round(antes - depois, 4)})
GASTO.write_text(json.dumps(g, indent=1))
if antes - depois > maximo:
    print(f"ALERTA: custou US$ {antes - depois:.4f}, acima do máximo US$ {maximo}: corrigir custo.py")
print(f"OK {destino} custo US$ {antes - depois:.4f} | lote US$ {g['inicio'] - depois:.4f} de {teto}")
