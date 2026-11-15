"""Monta o doc central/painel da aba Central (página Tinder).
Uso: python3 -I paginas/central/montar.py <pasta com posts/*.json baixados da Postagens> > central.json
Depois: ArtifactData set no Tinder, coleção central, doc painel, file_path=central.json.
Números só do que é medido: lotes (memoria/historico_lotes.md), posts (Postagens), varredura (listas/)."""
import json, glob, re, sys, os, collections, datetime
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pasta = sys.argv[1]

# Lotes e gasto (do histórico de lotes)
t = open(os.path.join(RAIZ, "memoria/historico_lotes.md")).read()
lotes, vistos = [], set()
for m in re.finditer(r'(?:Lista|Lote) (\d\d/\d\d) ([A-D])\b[^\n]*\n?(?:[^\n]*\n){0,3}?[^\n]*?(\d+) produtos[^\n]*?\((\d+) vídeos', t):
    k = m.group(1) + " " + m.group(2)
    if k in vistos: continue
    vistos.add(k); g = re.search(r'Gasto US\$ ([\d,]+)', t[m.start():m.start() + 900])
    lotes.append({"nome": k, "produtos": int(m.group(3)), "videos": int(m.group(4)),
                  "usd": float(g.group(1).replace(",", ".")) if g else None})
if "30/10 B" not in vistos:
    lotes.append({"nome": "30/10 B", "produtos": 15, "videos": 45, "usd": 5.44})
chave = lambda l: (int(l["nome"][3:5]) < 10 and 1 or 0, l["nome"][3:5], l["nome"][:2], l["nome"][-1])
lotes.sort(key=lambda l: ("2026-%s-%s" % (l["nome"][3:5], l["nome"][:2]), l["nome"][-1]))

# Posts (Postagens)
st = collections.Counter(); por_dia = collections.Counter(); por_lote = {}
pronto_mod = collections.Counter(); ultimos = []
for f in glob.glob(os.path.join(pasta, "posts", "*.json")):
    j = json.load(open(f)); j = j.get("data", j); s = j.get("status"); st[s] += 1
    cod = os.path.basename(f)[:5]  # ex. 1211B
    nome = cod[:2] + "/" + cod[2:4] + " " + cod[4]
    pl = por_lote.setdefault(nome, {"liberados": 0, "postados": 0})
    pl["liberados"] += 1
    if s == "postado":
        pl["postados"] += 1; por_dia[str(j.get("postado_em", ""))[:10]] += 1
        ultimos.append((str(j.get("postado_em", "")), j.get("produto", ""), (j.get("versao") or "?")[0], j.get("poster", "")))
    elif s == "pronto":
        pronto_mod[(j.get("versao") or "?")[0]] += 1
for l in lotes:
    l.update(por_lote.get(l["nome"], {"liberados": 0, "postados": 0}))

hoje = datetime.date.today()
dias = [(hoje - datetime.timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
mes = hoje.strftime("%m")
ultimos.sort(reverse=True)
ult = [{"em": u[0], "produto": u[1][:60], "modelo": u[2], "poster": u[3] if len(u[3]) < 40000 else ""} for u in ultimos[:8]]
sem = sum(n for d, n in por_dia.items() if d >= (hoje - datetime.timedelta(days=6)).isoformat())
mesp = sum(n for d, n in por_dia.items() if d[5:7] == hoje.strftime("%m") and d[:4] == str(hoje.year))
usd_mes = round(sum(l["usd"] or 0 for l in lotes if l["nome"][3:5] == mes), 2)

# Varredura (último arquivo de ids semeados)
ids = sorted(glob.glob(os.path.join(RAIZ, "produto-campeao/afiliados/listas/*_varredura_docs.ids.json")))
varr = None
if ids:
    u = ids[-1]; n = os.path.basename(u)[:4]
    try: q = len(json.load(open(u)))
    except Exception: q = None
    varr = {"dia": n[:2] + "/" + n[2:], "novos": q}

out = {
    "atualizado_em": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "gasto": {"total_usd": round(sum(l["usd"] or 0 for l in lotes), 2), "mes_usd": usd_mes,
              "teto_lote_usd": 8, "teto_produto_brl": 3},
    "videos": {"produzidos": sum(l["videos"] for l in lotes), "liberados": sum(st.values()),
               "para_postar": st.get("pronto", 0), "postados": st.get("postado", 0),
               "para_postar_modelo": dict(pronto_mod), "semana": sem, "mes": mesp},
    "ultimos": ult,
    "postados_dia": [[d, por_dia.get(d, 0)] for d in dias],
    "lotes": lotes[-14:][::-1],
    "varredura": varr,
    "agenda": [["05:41 e 16:41", "Varredura do Tinder (produtos novos)"], ["23:55", "Contador de postados"]],
    "nao_medido": ["Comissão e vendas (falta ligar o relatório de conversões da Shopee)", "Saldo da WaveSpeed"],
}
print(json.dumps(out, ensure_ascii=False))
