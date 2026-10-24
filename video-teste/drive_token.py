"""Gera o GDRIVE_REFRESH_TOKEN uma única vez, no seu PC (grátis).
Antes: crie o cliente OAuth "App para computador" no Google Cloud (passo a passo em CONTAS.md) e defina
GDRIVE_CLIENT_ID e GDRIVE_CLIENT_SECRET. Depois rode: python3 drive_token.py
O navegador abre, você entra na SUA conta Google e autoriza. O token aparece no terminal: guarde como variável
de ambiente GDRIVE_REFRESH_TOKEN (nunca em arquivo nem no chat). Escopo drive.file: o app só vê os arquivos que ele mesmo criou."""
import http.server, json, os, urllib.parse, urllib.request, webbrowser

ID, SEGREDO = os.environ["GDRIVE_CLIENT_ID"], os.environ["GDRIVE_CLIENT_SECRET"]
PORTA = 8765; VOLTA = f"http://127.0.0.1:{PORTA}"
codigo = {}


class Recebe(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        codigo["c"] = (q.get("code") or [None])[0]
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write("Pronto, pode fechar esta aba e voltar ao terminal.".encode())

    def log_message(self, *a):
        pass


url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": ID, "redirect_uri": VOLTA, "response_type": "code", "access_type": "offline", "prompt": "consent",
    "scope": "https://www.googleapis.com/auth/drive.file"})
print("Abrindo o navegador. Se não abrir, copie este endereço:\n" + url)
webbrowser.open(url)
srv = http.server.HTTPServer(("127.0.0.1", PORTA), Recebe)
while "c" not in codigo:
    srv.handle_request()
if not codigo["c"]:
    raise SystemExit("autorização recusada")
dados = urllib.parse.urlencode({"code": codigo["c"], "client_id": ID, "client_secret": SEGREDO,
                                "redirect_uri": VOLTA, "grant_type": "authorization_code"}).encode()
r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", dados, timeout=30))
if os.name == "nt":  # Windows: grava direto como variável do usuário, sem mostrar na tela
    import subprocess
    subprocess.run(["setx", "GDRIVE_REFRESH_TOKEN", r["refresh_token"]], check=True, capture_output=True)
    print("\nGDRIVE_REFRESH_TOKEN gravado. Feche e abra o terminal.")
else:
    print('\nAcrescente ao fim do ~/.zshrc ou ~/.bashrc e abra um terminal novo:\nexport GDRIVE_REFRESH_TOKEN="' + r["refresh_token"] + '"')
