#!/usr/bin/env python3
"""Backup dos vídeos finais no Google Drive da dona, sem passar pela conversa.

Uso:
  python3 drive_backup.py <pasta_ou_arquivos...> [--dia AAAA-MM-DD] [--legendas arquivo.txt]

Envia cada .mp4 para "<DRIVE_PASTA>/<dia>/" (padrão "Fabrica Videos") (cria as pastas se faltarem),
pula arquivos que já estão lá com o mesmo nome e tamanho, e envia o arquivo
de legendas junto. Lê GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET e
GDRIVE_REFRESH_TOKEN do ambiente (escopo drive.file).
"""
import argparse, datetime, json, os, sys, time, urllib.parse, urllib.request, urllib.error

RAIZ = os.environ.get("DRIVE_PASTA", "Fabrica Videos")
API = "https://content.googleapis.com/drive/v3"
UPLOAD = "https://content.googleapis.com/upload/drive/v3/files?uploadType=resumable&fields=id,name,size"
PEDACO = 16 * 1024 * 1024
PASTA_MIME = "application/vnd.google-apps.folder"


def token():
    faltam = [v for v in ("GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET", "GDRIVE_REFRESH_TOKEN") if not os.environ.get(v)]
    if faltam:
        sys.exit("faltam variáveis: " + ", ".join(faltam))
    dados = urllib.parse.urlencode({
        "client_id": os.environ["GDRIVE_CLIENT_ID"],
        "client_secret": os.environ["GDRIVE_CLIENT_SECRET"],
        "refresh_token": os.environ["GDRIVE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    # oauth2.googleapis.com às vezes é bloqueado pela rede da sessão (2026-10-23); www.googleapis.com/oauth2/v4/token é o mesmo serviço
    for url in ("https://oauth2.googleapis.com/token", "https://www.googleapis.com/oauth2/v4/token", "https://accounts.google.com/o/oauth2/token"):
        try:
            with urllib.request.urlopen(url, dados, timeout=30) as r:
                return json.load(r)["access_token"]
        except urllib.error.HTTPError as e:
            erro = e
    raise erro


def chamar(tk, metodo, url, corpo=None, cab=None, tentativas=5):
    for i in range(tentativas):
        h = {"Authorization": "Bearer " + tk}
        h.update(cab or {})
        req = urllib.request.Request(url, data=corpo, headers=h, method=metodo)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            if e.code == 308:
                return 308, dict(e.headers), b""
            if e.code in (429, 500, 502, 503, 504) and i < tentativas - 1:
                time.sleep(2 ** (i + 1))
                continue
            raise RuntimeError(f"{metodo} {url} -> {e.code}: {e.read()[:300]!r}")
        except (urllib.error.URLError, TimeoutError):
            if i < tentativas - 1:
                time.sleep(2 ** (i + 1))
                continue
            raise


def listar(tk, q):
    url = API + "/files?" + urllib.parse.urlencode({"q": q, "fields": "files(id,name,size)", "pageSize": 1000})
    return json.loads(chamar(tk, "GET", url)[2])["files"]


def pasta(tk, nome, pai):
    nome_q = nome.replace("'", "\\'")
    q = f"name = '{nome_q}' and mimeType = '{PASTA_MIME}' and trashed = false and '{pai}' in parents"
    achou = listar(tk, q)
    if achou:
        return achou[0]["id"]
    corpo = json.dumps({"name": nome, "mimeType": PASTA_MIME, "parents": [pai]}).encode()
    return json.loads(chamar(tk, "POST", API + "/files", corpo, {"Content-Type": "application/json"})[2])["id"]


def enviar(tk, caminho, pai, mime):
    tam = os.path.getsize(caminho)
    meta = json.dumps({"name": os.path.basename(caminho), "parents": [pai]}).encode()
    _, h, _ = chamar(tk, "POST", UPLOAD, meta, {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": mime, "X-Upload-Content-Length": str(tam)})
    sessao = h.get("Location") or h.get("location")
    with open(caminho, "rb") as f:
        ini = 0
        while ini < tam:
            f.seek(ini)
            bloco = f.read(PEDACO)
            fim = ini + len(bloco) - 1
            st, h, _ = chamar(tk, "PUT", sessao, bloco, {"Content-Range": f"bytes {ini}-{fim}/{tam}"})
            if st == 308:
                faixa = h.get("Range") or h.get("range")
                ini = int(faixa.split("-")[1]) + 1 if faixa else 0
            else:
                ini = tam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entradas", nargs="+")
    ap.add_argument("--dia", default=datetime.date.today().isoformat())
    ap.add_argument("--legendas")
    ap.add_argument("--reordenar", action="store_true", help="só ajusta a data dos vídeos da pasta do dia para o 01 A ficar no topo")
    a = ap.parse_args()

    if a.reordenar:
        tk = token()
        dia = pasta(tk, a.dia, pasta(tk, RAIZ, "root"))
        vids = sorted((f for f in listar(tk, f"'{dia}' in parents and trashed = false") if f["name"].endswith(".mp4")),
                      key=lambda f: f["name"], reverse=True)
        base = time.time() - len(vids)
        for n, f in enumerate(vids):
            quando = datetime.datetime.fromtimestamp(base + n, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            chamar(tk, "PATCH", API + "/files/" + f["id"], json.dumps({"modifiedTime": quando}).encode(),
                   {"Content-Type": "application/json"})
        print(f"reordenados {len(vids)} vídeos em {RAIZ}/{a.dia}")
        return

    arquivos = []
    for e in a.entradas:
        if os.path.isdir(e):
            arquivos += sorted(os.path.join(e, n) for n in os.listdir(e) if n.lower().endswith(".mp4"))
        elif e.lower().endswith(".mp4"):
            arquivos.append(e)

    # sobe de trás para frente: o Drive mostra primeiro o último enviado, então o 01 A fica no topo das Sugestões
    arquivos.sort(key=os.path.basename, reverse=True)
    tk = token()
    dia = pasta(tk, RAIZ, "root")
    for parte in a.dia.split("/"):  # --dia "2026-10-23/Lista 23-10 A" cria subpasta (2026-10-23)
        dia = pasta(tk, parte, dia)
    print(f"pasta https://drive.google.com/drive/folders/{dia}", flush=True)
    lista = listar(tk, f"'{dia}' in parents and trashed = false")
    ja = {f["name"]: int(f.get("size", -1)) for f in lista}
    ids = {}
    for f in lista:
        ids.setdefault(f["name"], []).append(f["id"])

    def trocar(c):
        # versão reeditada (tamanho diferente): apaga a antiga antes de enviar
        for i in ids.get(os.path.basename(c), []):
            chamar(tk, "DELETE", API + "/files/" + i)

    enviados = pulados = 0
    for c in arquivos:
        if ja.get(os.path.basename(c)) == os.path.getsize(c):
            pulados += 1
            continue
        trocar(c)
        enviar(tk, c, dia, "video/mp4")
        enviados += 1
        print("ok", os.path.basename(c), flush=True)
    if a.legendas and ja.get(os.path.basename(a.legendas)) != os.path.getsize(a.legendas):
        trocar(a.legendas)
        enviar(tk, a.legendas, dia, "text/plain")
    print(f"fim: {enviados} enviados, {pulados} já estavam lá, pasta {RAIZ}/{a.dia}")
    # links de cada vídeo para a página Postagens (nome do arquivo -> link do Drive)
    links = {f["name"]: f"https://drive.google.com/file/d/{f['id']}/view"
             for f in listar(tk, f"'{dia}' in parents and trashed = false")}
    saida = os.path.join(os.path.dirname(arquivos[0]) if arquivos else ".", "drive_links.json")
    with open(saida, "w") as f:
        json.dump(links, f, ensure_ascii=False, indent=1)
    print("links:", saida)


if __name__ == "__main__":
    main()
