"""Conta os vídeos Shopee postados (hoje, semana, mês) para o contador do Mapa da Fábrica.

Uso: python3 resumo_postados.py <pasta com os JSON dos docs posts com status postado>
Imprime o JSON para gravar em postagens_resumo/atual no banco do Mapa.
"""
import datetime as dt
import glob
import json
import sys
from zoneinfo import ZoneInfo

tz = ZoneInfo("America/Sao_Paulo")
hoje = dt.datetime.now(tz).date()
segunda = hoje - dt.timedelta(days=hoje.weekday())
c = {"hoje": 0, "semana": 0, "mes": 0, "total": 0}
dias = {}
for f in glob.glob(sys.argv[1].rstrip("/") + "/**/*.json", recursive=True):
    d = json.load(open(f))
    d = d.get("data", d)
    if d.get("status") != "postado" or d.get("auto") or d.get("versao") == "Reels" or f.endswith("_Reels.json"):
        continue
    pe = d.get("postado_em")
    if not pe:
        continue
    t = dt.datetime.fromisoformat(pe.replace("Z", "+00:00")).astimezone(tz).date()
    c["total"] += 1
    dias[str(t)] = dias.get(str(t), 0) + 1
    c["hoje"] += t == hoje
    c["semana"] += t >= segunda
    c["mes"] += (t.year, t.month) == (hoje.year, hoje.month)
corte = str(hoje - dt.timedelta(days=13))
c["dias"] = {k: v for k, v in sorted(dias.items()) if k >= corte}
c["dia_ref"] = str(hoje)
c["atualizado_em"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
print(json.dumps(c, ensure_ascii=False))
