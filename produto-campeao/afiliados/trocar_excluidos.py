"""Troca de excluídos entre Kevin e esposa pela pasta do Drive "Horst Ads Excluídos".
O Claude da rotina baixa/sobe os arquivos com o conector Google Drive; este script só mexe nos JSON locais.

  python3 trocar_excluidos.py juntar <eu> <arquivo_baixado.json> [...]
      junta os ids dos arquivos do OUTRO no excluidos.json (chave "<de>_<data>_<tipo>"). Ignora arquivos com "de" == <eu>.
  python3 trocar_excluidos.py gerar <eu> <ids_semeados.json|candidatos-<data>.json> <saida.json>
      gera o arquivo do dia (só os ids novos que EU semeei hoje) para subir no Drive como excluidos_<eu>_<data>.json.
Formato: {"de": "kevin"|"esposa", "data": "AAAA-MM-DD", "tipo": "inicial"|"dia", "ids": [...]}
"""
import json, sys, time
from pathlib import Path
B = Path(__file__).resolve().parent
EXC = B / "excluidos.json"

def ler_ids(f):
    d = json.loads(Path(f).read_text())
    if isinstance(d, dict) and "ids" in d: return [str(i) for i in d["ids"]]
    return [str(x["id"]) if isinstance(x, dict) else str(x) for x in d]

cmd, eu = sys.argv[1], sys.argv[2]
if cmd == "juntar":
    exc = json.loads(EXC.read_text()) if EXC.exists() else {}
    for f in sys.argv[3:]:
        d = json.loads(Path(f).read_text())
        if d.get("de") == eu:
            continue
        chave = f'{d["de"]}_{d["data"]}_{d.get("tipo","dia")}'
        exc[chave] = sorted(set(map(str, d["ids"])))
        print(f"{chave}: {len(exc[chave])} ids")
    EXC.write_text(json.dumps(exc))
elif cmd == "gerar":
    ids = sorted(set(ler_ids(sys.argv[3])))
    Path(sys.argv[4]).write_text(json.dumps({"de": eu, "data": time.strftime("%Y-%m-%d"), "tipo": "dia", "ids": ids}))
    print(f"{len(ids)} ids -> {sys.argv[4]}")
