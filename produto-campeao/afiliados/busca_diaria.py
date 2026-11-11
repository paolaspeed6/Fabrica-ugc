"""Varredura diaria: varrer.py com checkpoint por rodada (sobrevive ao limite de tempo) e 3 rodadas em paralelo. Apague ck_diaria_<data>/ depois."""
import json, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import varrer as V

CK = Path(__file__).resolve().parent / ("ck_diaria_" + time.strftime("%Y-%m-%d"))
CK.mkdir(exist_ok=True)

def uma(i, r):
    f = CK / f"r{i:03d}.json"
    if f.exists():
        return json.loads(f.read_text())
    prods = {}
    for pagina in range(1, 201):
        res = V.chamar({**r, "p": pagina})
        for p in res["nodes"]:
            prods[str(p["itemId"])] = p
        if not res["pageInfo"]["hasNextPage"]:
            break
        time.sleep(1.0)
    f.write_text(json.dumps(prods))
    print(f"rodada {i} {r.get('k','geral')}: {len(prods)}", flush=True)
    return prods

def varrer_ck(palavras):
    rodadas = [{"l": 0, "s": 2}, {"l": 2, "s": 2}] + [{"l": 0, "s": 2, "k": k} for k in palavras]
    produtos = {}
    with ThreadPoolExecutor(2) as ex:
        for prods in ex.map(lambda a: uma(*a), enumerate(rodadas)):
            produtos.update(prods)
    print(f"total {len(produtos)}", flush=True)
    return produtos

V.varrer = varrer_ck
sys.argv = ["varrer.py"]  # top 100 e palavras.txt (padrao do varrer.py)
V.main()
