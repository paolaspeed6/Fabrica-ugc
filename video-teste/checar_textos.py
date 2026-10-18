import json,glob,re,unicodedata
def norm(s): return unicodedata.normalize("NFKD",s.lower()).encode("ascii","ignore").decode()
for f in sorted(glob.glob("r[0-9][0-9].json")):
    p=json.load(open(f)); a=json.load(open(f[:3]+"-fotos/anuncio.json"))
    fonte=norm(a["nome"]+" "+a["descricao"]+" "+str(a["nota"])+" "+str(a["avaliacoes"]))
    fonte_num=re.sub(r"(\d)[.,](\d)",r"\1\2",fonte)
    txt=[]
    for k,v in p["versoes"].items():
        for c in v["cenas"]:
            for key in ("rotulo","titulo","sub","cta"):
                if c.get(key): txt.append(c[key])
            txt+=c.get("fichas",[]); ab=c.get("abertura")
            if ab: txt+= [ab["grande"],ab["texto"]]
    txt+=list(p["legendas"].values())+[p["selo"]["n"]+" "+p["selo"]["t"]]
    falta=set()
    for t in txt:
        t=re.sub(r"https?://\S+","",t)
        for n in re.findall(r"\d+(?:[.,]\d+)?",t):
            m=re.sub(r"[.,]","",n)
            if m not in fonte_num: falta.add(n)
    print(f[:3], "números fora do anúncio:", sorted(falta))
