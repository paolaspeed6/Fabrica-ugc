#!/usr/bin/env python3
"""Posta 1 vídeo por vez no Instagram, no Facebook e no Threads (a dona, 28/10): 6 posts por dia nos horários de pico,
alternando os layouts A e C (o B fica só para a Shopee), legenda boa com hashtags e o link de afiliada no 1º comentário
com a mensagem "Só copiar o link e colar no WhatsApp".

Uso:
  python3 -I redes_diario.py <pasta dos docs posts> --seco [N]   mostra os próximos N posts (padrão 6), não posta
  python3 -I redes_diario.py <pasta dos docs posts>              posta o próximo vídeo da fila nas 3 redes
  --estado F.json   registro + legendas num arquivo só (o doc redes/estado do banco da Postagens; a tarefa agendada
                    não consegue dar push no GitHub, 28/10), em vez de postados_redes.json / legendas_redes.json

<pasta dos docs posts> = saída do ArtifactData query (coleção posts, status pronto, out_dir) da página Postagens.
Fila: produtos na ordem do lote; 1ª volta A, C, A, C...; 2ª volta o layout que faltou de cada produto.
Registro: postados_redes.json (doc -> quando + resultado por rede). Legendas: legendas_redes.json (Gemini, grátis).
Link: o link_produto do doc (link curto de afiliada da dona, com Sub ID). Nunca imprimir chave.
"""
import glob, json, os, re, sys, tempfile, time, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "video-teste"))
import postar as P

BR = ZoneInfo("America/Sao_Paulo")
REG = os.path.join(AQUI, "postados_redes.json")
LEG = os.path.join(AQUI, "legendas_redes.json")
MAX_DIA = int(os.environ.get("MAX_DIA", "6"))
INTERVALO_MIN = int(os.environ.get("INTERVALO_MIN", "90"))  # nunca 2 posts colados se a tarefa disparar 2 vezes
REDES = os.environ.get("REDES", "ig,fb,threads").split(",")
COMENTARIO = "🛒 Gostou? Só copiar o link e colar no WhatsApp que abre direto na Shopee 👇\n{link}"
GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
MODELOS = ["gemini-3-flash-preview", "gemini-flash-latest", "gemini-flash-lite-latest"]


def ler(p):
    return json.load(open(p)) if os.path.exists(p) else {}


def gravar(p, d):
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)


def docs(pasta):
    out = {}
    for f in glob.glob(os.path.join(pasta, "**", "*.json"), recursive=True):
        d = json.load(open(f))
        d = d.get("data", d)
        nome = os.path.basename(f)[:-5]
        m = re.match(r"(\d{4})([A-Z]?)_(\d+)_.*_([AC])$", nome)
        if m and d.get("status") in ("pronto", "postado") and d.get("drive_url") and d.get("link_produto"):
            out[nome] = dict(d, id=nome, chave=(d.get("dia", ""), m[2], int(m[3])), layout=m[4])
    return out


def fila(ds, reg):
    prods = {}
    for d in ds.values():
        prods.setdefault(d["chave"], {})[d["layout"]] = d
    # lote mais novo primeiro (os da Shopee já postados também valem para as redes); dentro do lote, na ordem
    ordem, q = sorted(sorted(prods, key=lambda k: k[2]), key=lambda k: (k[0], k[1]), reverse=True), []
    for volta in (0, 1):
        for i, k in enumerate(ordem):
            quer = "AC"[(i + volta) % 2]
            d = prods[k].get(quer) or (prods[k].get("AC"[(i + volta + 1) % 2]) if volta == 0 else None)
            if d and d["id"] not in reg and d not in q:
                q.append(d)
    # alterna A e C de verdade, mesmo quando falta um layout
    a, c = [d for d in q if d["layout"] == "A"], [d for d in q if d["layout"] == "C"]
    ult = next((v["layout"] for _, v in sorted(reg.items(), key=lambda x: x[1]["quando"], reverse=True)), "C")
    res = []
    while a or c:
        lado = (c or a) if ult == "A" else (a or c)
        d = lado.pop(0)
        res.append(d)
        ult = d["layout"]
    return res


def gemini(texto):
    corpo = json.dumps({"contents": [{"parts": [{"text": texto}]}],
                        "generationConfig": {"temperature": 0.8, "responseMimeType": "application/json"}}).encode()
    for i in range(4):
        for m in MODELOS:
            try:
                r = urllib.request.Request(GEMINI.format(m), data=corpo, headers={
                    "Content-Type": "application/json", "x-goog-api-key": os.environ["GOOGLEAISTUDIO_API_KEY"]})
                d = json.load(urllib.request.urlopen(r, timeout=120))
                return json.loads(d["candidates"][0]["content"]["parts"][0]["text"])
            except Exception:
                pass
        time.sleep(20 * (i + 1))
    return None


REGRAS = """Escreva a legenda de um Reels da marca Aguiiar Lar (casa bonita e prática, achados da Shopee), em português do Brasil.
Produto: {produto}. Descrição curta: {base}.
Formato: 1ª linha = gancho curto que prende (pergunta ou situação do dia a dia, com 1 emoji);
2 a 3 linhas curtas com o benefício real para a casa, tom de amiga que indica, sem exagero;
1 linha "💬 Link nos comentários 👇"; por fim 8 a 12 hashtags em minúsculas, sem acento, misturando nicho
(#decoracao #casa #achadinhos #achadosshopee #shopee) e do produto.
Proibido: inventar medida, material ou função que não está na descrição; preço; % de desconto; prazo ou promessa de entrega;
nota ou número de avaliações; bebida; link; palavra "frete grátis"; dizer que comprou, ganhou ou usou
("comprei", "ganhei", "uso em casa"): fale do produto e de quem vai usar ("imagina...", "olha esse..."). Máximo 450 caracteres no total.
Responda JSON: {{"legenda": "..."}}"""


ESTADO = {}


def salvar(reg, cache):
    if ESTADO.get("arq"):
        gravar(ESTADO["arq"], {"registro": reg, "legendas": cache})
    else:
        gravar(REG, reg)
        gravar(LEG, cache)


def pode_comentar():
    """A chave da Meta precisa de pages_manage_engagement (fb) e instagram_manage_comments (ig) para o 1º comentário;
    sem elas (28/10) o link vai na legenda."""
    try:
        pm = P.pedir("GET", f"{P.GRAPH}/me/permissions", os.environ["META_PAGE_TOKEN"])["data"]
        ok = {x["permission"] for x in pm if x["status"] == "granted"}
    except Exception:
        ok = set()
    return {"fb": "pages_manage_engagement" in ok, "ig": "instagram_manage_comments" in ok, "threads": True}


def legenda(d, cache):
    if d["id"] in cache:
        return cache[d["id"]]
    base = re.sub(r"#\S+", "", d.get("legenda", "")).strip()
    tags = " ".join(re.findall(r"#\S+", d.get("legenda", "")))
    r = gemini(REGRAS.format(produto=d.get("produto", ""), base=base or d.get("produto", "")))
    txt = (r or {}).get("legenda", "").strip()
    if not txt or "http" in txt or len(txt) > 480:  # reserva sem Gemini
        txt = f"{base} ✨\n\n💬 Link nos comentários 👇\n\n{tags} #achadinhos #achadosshopee #casa #aguiiarlar".strip()
    cache[d["id"]] = txt
    salvar(ESTADO.get("reg", {}), cache)
    return txt


# ---------- vídeo do Drive ----------

def fid(d):
    return d["drive_url"].split("/d/")[1].split("/")[0]


def baixar(d, pasta):
    import drive_backup as g
    st, _, corpo = g.chamar(g.token(), "GET", f"{g.API}/files/{fid(d)}?alt=media")
    arq = os.path.join(pasta, d["id"] + ".mp4")
    open(arq, "wb").write(corpo)
    return arq


def drive_publico(d):
    import drive_backup as g
    t, f = g.token(), fid(d)
    perm = json.loads(g.chamar(t, "POST", f"{g.API}/files/{f}/permissions",
                               json.dumps({"role": "reader", "type": "anyone"}).encode(),
                               {"Content-Type": "application/json"})[2])["id"]
    return (f"https://drive.usercontent.google.com/download?id={f}&export=download&confirm=t",
            lambda: g.chamar(t, "DELETE", f"{g.API}/files/{f}/permissions/{perm}"))


# ---------- redes (link sempre no 1º comentário) ----------

def ig(arq, leg, com):
    t = P.tk("META_PAGE_TOKEN")
    c = P.pedir("POST", f"{P.GRAPH}/{P.IG}/media", t, {
        "media_type": "REELS", "upload_type": "resumable", "caption": leg, "share_to_feed": "true"})
    with open(arq, "rb") as f:
        P.pedir("POST", c["uri"], t, corpo=f.read(), cab={"offset": "0", "file_size": str(os.path.getsize(arq))})
    P.esperar(lambda: P.pedir("GET", f"{P.GRAPH}/{c['id']}?fields=status_code", t),
              lambda s: s.get("status_code") == "FINISHED", lambda s: s.get("status_code") in ("ERROR", "EXPIRED"))
    pub = P.pedir("POST", f"{P.GRAPH}/{P.IG}/media_publish", t, {"creation_id": c["id"]})
    r = {"id": pub["id"], "permalink": P.pedir("GET", f"{P.GRAPH}/{pub['id']}?fields=permalink", t).get("permalink")}
    try:
        if com:
            r["comentario"] = P.pedir("POST", f"{P.GRAPH}/{pub['id']}/comments", t, {"message": com}).get("id")
    except Exception as e:
        r["comentario_erro"] = str(e)[:200]
    return r


def fb(arq, leg, com):
    t = P.tk("META_PAGE_TOKEN")
    ini = P.pedir("POST", f"{P.GRAPH}/{P.PAGINA}/video_reels", t, {"upload_phase": "start"})
    vid = ini["video_id"]
    with open(arq, "rb") as f:
        P.pedir("POST", ini["upload_url"], t, corpo=f.read(), cab={"offset": "0", "file_size": str(os.path.getsize(arq))})
    P.pedir("POST", f"{P.GRAPH}/{P.PAGINA}/video_reels", t, {
        "upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED", "description": leg})
    st = P.esperar(lambda: P.pedir("GET", f"{P.GRAPH}/{vid}?fields=status,post_id,permalink_url", t),
                   lambda s: s.get("status", {}).get("video_status") == "ready"
                   and s.get("status", {}).get("publishing_phase", {}).get("status") == "complete",
                   lambda s: s.get("status", {}).get("video_status") == "error")
    perm = st.get("permalink_url") or ""
    r = {"id": vid, "permalink": ("https://www.facebook.com" + perm) if perm.startswith("/") else perm}
    try:  # comentário no id do vídeo (no post_id a API recusa, 28/10)
        if com:
            r["comentario"] = P.pedir("POST", f"{P.GRAPH}/{vid}/comments", t, {"message": com}).get("id")
    except Exception as e:
        r["comentario_erro"] = str(e)[:200]
    return r


def threads(d, leg, com):
    t = P.tk("THREADS_TOKEN")
    if len(leg) > P.LIMITE_THREADS:
        leg = leg[:P.LIMITE_THREADS - 1].rsplit("\n", 1)[0]
    url, fechar = drive_publico(d)
    try:
        c = P.pedir("POST", f"{P.THREADS}/me/threads", t, {"media_type": "VIDEO", "video_url": url, "text": leg})
        P.esperar(lambda: P.pedir("GET", f"{P.THREADS}/{c['id']}?fields=status,error_message", t),
                  lambda s: s.get("status") == "FINISHED", lambda s: s.get("status") in ("ERROR", "EXPIRED"))
        pub = P.pedir("POST", f"{P.THREADS}/me/threads_publish", t, {"creation_id": c["id"]})
    finally:
        fechar()
    r = {"id": pub["id"], "permalink": P.pedir("GET", f"{P.THREADS}/{pub['id']}?fields=permalink", t).get("permalink")}
    try:  # o "comentário" no Threads é uma resposta ao próprio post
        if not com:
            return r
        rc = P.pedir("POST", f"{P.THREADS}/me/threads", t, {"media_type": "TEXT", "text": com, "reply_to_id": pub["id"]})
        time.sleep(5)
        r["comentario"] = P.pedir("POST", f"{P.THREADS}/me/threads_publish", t, {"creation_id": rc["id"]}).get("id")
    except Exception as e:
        r["comentario_erro"] = str(e)[:200]
    return r


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if "--estado" in sys.argv:
        ESTADO["arq"] = sys.argv[sys.argv.index("--estado") + 1]
        e = ler(ESTADO["arq"])
        e = e.get("data", e)
        reg, cache = e.get("registro", {}), e.get("legendas", {})
    else:
        reg, cache = ler(REG), ler(LEG)
    ESTADO["reg"] = reg
    pausas = ler(P.PAUSAS)
    q = fila(docs(sys.argv[1]), reg)
    if "--seco" in sys.argv:
        n = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 6
        print(f"{len(q)} vídeos na fila (A e C); {MAX_DIA} por dia = {-(-len(q) // MAX_DIA)} dias")
        for d in q[:n]:
            print(f"\n=== {d['id']} ({d['layout']}) ===\n{legenda(d, cache)}\n--- 1º comentário ---\n"
                  + COMENTARIO.format(link=d["link_produto"]))
        return
    agora = datetime.now(BR)
    feitos = sorted(datetime.fromisoformat(v["quando"]) for v in reg.values())
    hoje = [x for x in feitos if x.astimezone(BR).date() == agora.date()]
    if len(hoje) >= MAX_DIA:
        return print(f"já postou {len(hoje)} hoje (máx. {MAX_DIA})")
    if feitos and agora - feitos[-1] < timedelta(minutes=INTERVALO_MIN):
        return print("último post há pouco tempo; espera o próximo horário")
    if not q:
        return print("fila vazia: nenhum vídeo A ou C pronto sem postar")
    d = q[0]
    leg, com = legenda(d, cache), COMENTARIO.format(link=d["link_produto"])
    ent = {"quando": agora.isoformat(timespec="seconds"), "layout": d["layout"], "produto": d.get("produto"),
           "link": d["link_produto"]}
    reg[d["id"]] = ent
    salvar(reg, cache)  # grava antes, para nunca repostar se cair no meio
    comenta = pode_comentar()
    link_leg = leg.replace("💬 Link nos comentários 👇", com)
    with tempfile.TemporaryDirectory() as tmp:
        arq = baixar(d, tmp)
        for rede in REDES:
            pz = pausas.get(rede)
            if pz and datetime.fromisoformat(pz["ate"]) > datetime.now():
                ent[rede] = {"pulado": f"pausada até {pz['ate']}"}
                continue
            try:
                lg = leg if comenta[rede] else link_leg  # sem permissão de comentar: link na legenda
                cm = com if comenta[rede] else None
                ent[rede] = {"ig": lambda: ig(arq, lg, cm), "fb": lambda: fb(arq, lg, cm),
                             "threads": lambda: threads(d, lg, cm)}[rede]()
                if not comenta[rede]:
                    ent[rede]["link_na_legenda"] = True
                print(f"ok {rede}: {ent[rede].get('permalink')}"
                      + (" (comentário falhou)" if "comentario_erro" in ent[rede] else ""), flush=True)
            except Exception as e:
                msg = str(e)
                ent[rede] = {"erro": msg[:300]}
                print(f"ERRO {rede}: {msg[:200]}", flush=True)
                if any(x in msg for x in P.SPAM):
                    pausas[rede] = {"ate": (datetime.now() + timedelta(hours=24)).isoformat(timespec="seconds"),
                                    "motivo": msg[:300]}
                    P.gravar(P.PAUSAS, pausas)
            salvar(reg, cache)
    print(f"postado {d['id']} ({d['layout']}); faltam {len(q) - 1} na fila")


if __name__ == "__main__":
    main()
