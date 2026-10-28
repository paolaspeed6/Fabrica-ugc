#!/usr/bin/env python3
"""Posta os vídeos da fábrica no Instagram (Reels), na Página do Facebook (Reels) e no Threads.

Uso:
  python3 postar.py conferir              confere os tokens (não posta nada)
  python3 postar.py plano.json --seco     mostra o que seria postado (não posta nem gera link)
  python3 postar.py plano.json            posta de verdade
  python3 postar.py fila.json --fila      posta da fila só o que falta e o ritmo deixa agora

plano.json = lista de vídeos, um por rede:
  [{"rede": "ig" | "fb" | "threads",
    "arquivo": "/caminho/2110_17_barraca-joyfox_Reels.mp4",
    "produto": "L0101Ap17", "versao": "R",
    "url_produto": "https://shopee.com.br/product/<loja>/<item>",
    "legenda": "2 quartos e 1 sala numa barraca só #barraca #camping",
    "link_fb": "ambos"}            só Facebook: "comentario", "legenda" ou "ambos" (padrão)

Regras (Kevin 2026-10-22):
- Link de afiliado sempre pela API (produto-campeao/vendas/link_subid.py), um Sub ID por vídeo e rede:
  <produto><versao><IG|FB|TH><AAMMDD>, ex. L0101Ap17RIG260101.
- Facebook: link no primeiro comentário, na legenda ou nos dois (link_fb), para comparar alcance. Instagram: link escrito na legenda (o vídeo Reels diz "Link na legenda"),
  mas não é clicável; a bio é o caminho clicável.
  Threads: link clicável na própria legenda.
- Kevin 2026-10-23: o mesmo Reels pode ir para Instagram, Facebook e Threads (uma vez em cada rede).
  postados.json guarda "rede|arquivo" e o script recusa repetir na mesma rede.
- Ritmo seguro (contas novas): no máximo MAX_DIA posts por rede por dia e INTERVALO_H horas entre posts da
  mesma rede. Aviso de spam/limite da Meta pausa só aquela rede por 24 h (pausas.json) e as outras seguem.
Tokens: META_PAGE_TOKEN (sua Página, também serve ao Instagram ligado) e THREADS_TOKEN. Nunca imprimir.
Vídeo do Threads precisa de URL pública: usa o arquivo do Drive (drive_links.json da pasta do vídeo),
abre o link só durante a postagem e fecha depois.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "produto-campeao", "vendas"))
sys.path.insert(0, os.path.join(AQUI, "..", "video-teste"))

GRAPH = "https://graph.facebook.com/v21.0"
THREADS = "https://graph.threads.net/v1.0"
PAGINA = os.environ.get("META_PAGE_ID", "")    # id da sua Página do Facebook
IG = os.environ.get("META_IG_ID", "")          # id do seu Instagram profissional ligado à Página
REGISTRO = os.path.join(AQUI, "postados.json")
CODIGO = {"ig": "IG", "fb": "FB", "threads": "TH"}
LIMITE_THREADS = 500
PAUSAS = os.path.join(AQUI, "pausas.json")
MAX_DIA = int(os.environ.get("MAX_DIA", "2"))
INTERVALO_H = float(os.environ.get("INTERVALO_H", "3"))
SPAM = ('"code":368', '"code":4,', '"code":32,', '"code":613', '"code":9,', "2207042", "spam", "Limitamos")


def pedir(metodo, url, token, dados=None, corpo=None, cab=None, tentativas=4):
    h = {"Authorization": ("OAuth " if "rupload" in url else "Bearer ") + token}
    h.update(cab or {})
    if dados is not None:
        corpo = urllib.parse.urlencode(dados).encode()
        h["Content-Type"] = "application/x-www-form-urlencoded"
    for i in range(tentativas):
        req = urllib.request.Request(url, data=corpo, headers=h, method=metodo)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            txt = e.read()[:500].decode(errors="replace")
            if e.code in (429, 500, 502, 503, 504) and i < tentativas - 1:
                time.sleep(2 ** (i + 2))
                continue
            raise RuntimeError(f"{metodo} {url.split('?')[0]} -> {e.code}: {txt}")
        except (urllib.error.URLError, TimeoutError):
            if i < tentativas - 1:
                time.sleep(2 ** (i + 2))
                continue
            raise


def esperar(checar, pronto, erro, limite=600):
    fim = time.time() + limite
    while time.time() < fim:
        st = checar()
        if pronto(st):
            return st
        if erro(st):
            raise RuntimeError(f"processamento falhou: {st}")
        time.sleep(10)
    raise RuntimeError("processamento passou de 10 min")


_pagina = {}


def tk(nome):
    v = os.environ.get(nome)
    if not v:
        sys.exit(f"falta a variável {nome}")
    if nome == "META_PAGE_TOKEN":  # a dona guardou o token do PERFIL (28/10): troca pelo da Página via me/accounts, sem pedir nada a ela
        if "t" not in _pagina:
            contas = pedir("GET", f"{GRAPH}/me/accounts?fields=id,access_token", v).get("data", [])
            alvo = os.environ.get("META_PAGE_ID")
            pg = next((c for c in contas if c.get("id") == alvo), None) or (contas[0] if contas else None)
            _pagina["t"] = pg["access_token"] if pg else v
        return _pagina["t"]
    return v


# ---------- redes ----------

def postar_ig(v, link):
    t = tk("META_PAGE_TOKEN")
    legenda = f"{v['legenda']}\n\nLink do produto: {link}"
    c = pedir("POST", f"{GRAPH}/{IG}/media", t, {
        "media_type": "REELS", "upload_type": "resumable", "caption": legenda, "share_to_feed": "true"})
    tam = os.path.getsize(v["arquivo"])
    with open(v["arquivo"], "rb") as f:
        pedir("POST", c["uri"], t, corpo=f.read(), cab={"offset": "0", "file_size": str(tam)})
    esperar(lambda: pedir("GET", f"{GRAPH}/{c['id']}?fields=status_code,status", t),
            lambda s: s.get("status_code") == "FINISHED", lambda s: s.get("status_code") in ("ERROR", "EXPIRED"))
    pub = pedir("POST", f"{GRAPH}/{IG}/media_publish", t, {"creation_id": c["id"]})
    perm = pedir("GET", f"{GRAPH}/{pub['id']}?fields=permalink", t).get("permalink")
    return {"id": pub["id"], "permalink": perm, "legenda": legenda}


def postar_fb(v, link):
    t = tk("META_PAGE_TOKEN")
    modo = v.get("link_fb", "ambos")   # "comentario", "legenda" ou "ambos" (teste de alcance, Kevin 2026-10-22)
    legenda = v["legenda"] + {"comentario": "\n\nLink no primeiro comentário 👇",
                              "legenda": f"\n\n🛒 Link do produto: {link}",
                              "ambos": f"\n\n🛒 Link do produto: {link}"}[modo]
    ini = pedir("POST", f"{GRAPH}/{PAGINA}/video_reels", t, {"upload_phase": "start"})
    vid = ini["video_id"]
    tam = os.path.getsize(v["arquivo"])
    with open(v["arquivo"], "rb") as f:
        pedir("POST", ini["upload_url"], t, corpo=f.read(), cab={"offset": "0", "file_size": str(tam)})
    pedir("POST", f"{GRAPH}/{PAGINA}/video_reels", t, {
        "upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED", "description": legenda})
    st = esperar(lambda: pedir("GET", f"{GRAPH}/{vid}?fields=status,post_id,permalink_url", t),
                 lambda s: s.get("status", {}).get("video_status") == "ready"
                 and s.get("status", {}).get("publishing_phase", {}).get("status") == "complete",
                 lambda s: s.get("status", {}).get("video_status") == "error")
    com = {}
    if modo != "legenda":
        alvo = st.get("post_id") or vid
        com = pedir("POST", f"{GRAPH}/{alvo}/comments", t, {"message": f"🛒 Link do produto: {link}"})
    perm = st.get("permalink_url")
    if perm and perm.startswith("/"):
        perm = "https://www.facebook.com" + perm
    return {"id": vid, "post_id": st.get("post_id"), "comentario": com.get("id"), "permalink": perm,
            "legenda": legenda}


def drive_publico(arquivo):
    """Abre o vídeo do Drive para qualquer pessoa com o link; devolve (url direta, fechar())."""
    import drive_backup as d
    links = json.load(open(os.path.join(os.path.dirname(arquivo), "drive_links.json")))
    url = links.get(os.path.basename(arquivo))
    if not url:
        raise RuntimeError("vídeo não está no drive_links.json; rode o drive_backup.py antes")
    fid = url.split("/d/")[1].split("/")[0]
    g = d.token()
    perm = json.loads(d.chamar(g, "POST", f"{d.API}/files/{fid}/permissions",
                               json.dumps({"role": "reader", "type": "anyone"}).encode(),
                               {"Content-Type": "application/json"})[2])["id"]

    def fechar():
        d.chamar(g, "DELETE", f"{d.API}/files/{fid}/permissions/{perm}")
    return f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t", fechar


def postar_threads(v, link):
    t = tk("THREADS_TOKEN")
    texto = f"{v['legenda']}\n\n🛒 {link}"
    if len(texto) > LIMITE_THREADS:
        raise RuntimeError(f"legenda do Threads com {len(texto)} caracteres (máx. {LIMITE_THREADS})")
    url, fechar = drive_publico(v["arquivo"])
    try:
        c = pedir("POST", f"{THREADS}/me/threads", t, {"media_type": "VIDEO", "video_url": url, "text": texto})
        esperar(lambda: pedir("GET", f"{THREADS}/{c['id']}?fields=status,error_message", t),
                lambda s: s.get("status") == "FINISHED", lambda s: s.get("status") in ("ERROR", "EXPIRED"))
        pub = pedir("POST", f"{THREADS}/me/threads_publish", t, {"creation_id": c["id"]})
    finally:
        fechar()
    perm = pedir("GET", f"{THREADS}/{pub['id']}?fields=permalink", t).get("permalink")
    return {"id": pub["id"], "permalink": perm, "legenda": texto}


POSTAR = {"ig": postar_ig, "fb": postar_fb, "threads": postar_threads}


# ---------- plano ----------

def ler_json(p):
    return json.load(open(p)) if os.path.exists(p) else {}


def ler_registro():
    reg = ler_json(REGISTRO)
    # entradas antigas (2026-10-22) usavam só o nome do arquivo como chave
    return {(k if "|" in k else f"{v['rede']}|{k}"): v for k, v in reg.items()}


def gravar(p, dados):
    with open(p, "w") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)


def pode_postar(rede, registro, pausas):
    """Devolve None se a rede pode postar agora, ou o motivo para esperar."""
    agora = datetime.now()
    if pausas.get(rede) and datetime.fromisoformat(pausas[rede]["ate"]) > agora:
        return f"pausada até {pausas[rede]['ate']} ({pausas[rede]['motivo'][:80]})"
    feitos = sorted(datetime.fromisoformat(v["quando"]) for v in registro.values() if v["rede"] == rede)
    hoje = [q for q in feitos if q.date() == agora.date()]
    if len(hoje) >= MAX_DIA:
        return f"já fez {len(hoje)} hoje (máx. {MAX_DIA})"
    if feitos and (agora - feitos[-1]).total_seconds() < INTERVALO_H * 3600:
        return f"último post há menos de {INTERVALO_H:g} h"
    return None


def checar_plano(plano, registro):
    erros, vistos = [], set()
    for i, v in enumerate(plano, 1):
        faltam = [k for k in ("rede", "arquivo", "produto", "versao", "url_produto", "legenda") if not v.get(k)]
        if faltam:
            erros.append(f"{i}: faltam {', '.join(faltam)}")
            continue
        nome = os.path.basename(v["arquivo"])
        if v["rede"] not in POSTAR:
            erros.append(f"{i}: rede '{v['rede']}' desconhecida (ig, fb, threads)")
        if not os.path.isfile(v["arquivo"]):
            erros.append(f"{i}: arquivo não existe: {v['arquivo']}")
        chave = f"{v['rede']}|{nome}"
        if chave in vistos:
            erros.append(f"{i}: {nome} aparece duas vezes para {v['rede']} no plano")
        if chave in registro:
            erros.append(f"{i}: {nome} já foi postado no {v['rede']} em {registro[chave]['quando']}")
        if "http" in v["legenda"]:
            erros.append(f"{i}: a legenda não leva link; o script põe o link certo de cada rede")
        vistos.add(chave)
    return erros


def conferir():
    t = tk("META_PAGE_TOKEN")
    p = pedir("GET", f"{GRAPH}/me?fields=id,name,instagram_business_account{{id,username}}", t)
    print("Página:", p.get("name"), "| Instagram:", p.get("instagram_business_account", {}).get("username"))
    th = pedir("GET", f"{THREADS}/me?fields=id,username", tk("THREADS_TOKEN"))
    print("Threads:", th.get("username"))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "conferir":
        return conferir()
    seco = "--seco" in sys.argv
    plano = json.load(open(sys.argv[1]))
    registro = ler_registro()
    # --fila: o plano é uma fila; posta só o que ainda falta e o ritmo permite agora
    if "--fila" in sys.argv:
        plano = [v for v in plano if f"{v['rede']}|{os.path.basename(v['arquivo'])}" not in registro]
    erros = checar_plano(plano, registro)
    if erros:
        sys.exit("plano recusado:\n" + "\n".join(erros))
    pausas = ler_json(PAUSAS)
    dia = format(date.today(), "%y%m%d")
    falhas = 0
    for v in plano:
        nome = os.path.basename(v["arquivo"])
        versao = v["versao"] + CODIGO[v["rede"]]
        espera = pode_postar(v["rede"], registro, pausas)
        if espera:
            print(f"espera {v['rede']}: {nome} ({espera})")
            continue
        if seco:
            print(f"[seco] {v['rede']}: {nome} | Sub ID {v['produto']}{versao}{dia} | {v['legenda']}")
            registro[f"{v['rede']}|{nome}"] = {"rede": v["rede"], "quando": datetime.now().isoformat()}
            continue
        from link_subid import link as gerar_link
        sub, link = gerar_link(v["url_produto"], v["produto"], versao, dia)
        try:
            res = POSTAR[v["rede"]](v, link)
        except Exception as e:
            falhas += 1
            msg = str(e)
            print(f"ERRO {v['rede']}: {nome}: {msg[:300]}", flush=True)
            if any(x in msg for x in SPAM):
                ate = datetime.fromtimestamp(time.time() + 24 * 3600).isoformat(timespec="seconds")
                pausas[v["rede"]] = {"ate": ate, "motivo": msg[:300]}
                gravar(PAUSAS, pausas)
                print(f"PAUSA {v['rede']} até {ate}", flush=True)
            continue
        registro[f"{v['rede']}|{nome}"] = {"rede": v["rede"], "quando": datetime.now().isoformat(timespec="seconds"),
                                           "subid": sub, "link": link, **res}
        gravar(REGISTRO, registro)   # grava a cada vídeo, para nunca repostar se cair no meio
        print(f"ok {v['rede']}: {nome} -> {res.get('permalink')}", flush=True)
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
