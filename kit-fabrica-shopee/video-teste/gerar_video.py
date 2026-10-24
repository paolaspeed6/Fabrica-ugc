"""Gera as cenas de 1 vídeo pela receita fiel ao anúncio (WaveSpeed: Seedream v4 Edit + Seedance 1.5 Pro Fast 720p).

Uso:
    (chave: segredo de rede "Bearer" para api.wavespeed.ai nas configurações do projeto,
     ou a variável WAVESPEED_API_KEY)
    python3 gerar_video.py roteiro.json

roteiro.json:
{
  "nome": "banqueta",
  "fotos": ["https://.../foto_principal.jpg"],
  "cenas": [
    {"editar": "prompt do Seedream: coloque ESTE produto numa cozinha...", "movimento": "..."},
    {"editar": "prompt do Seedream: outro ambiente/ângulo...", "movimento": "..."},
    {"foto": 0, "movimento": "câmera lenta se aproximando; o produto não muda"}
  ]
}

Regra de fidelidade: o produto nunca é criado só por texto. Cada cena ou anima
uma foto real do anúncio ("foto": índice em "fotos") ou parte de uma edição do
Seedream V4 Edit que usa as fotos do anúncio como referência ("editar").
Sem pessoas nas cenas. 720p, 5 s por cena, no máximo 2 tentativas por
etapa (teto de R$ 3 por vídeo). Os clipes saem em <nome>/cenaN.mp4; a edição
final é feita por montar_video_pro.py (um estilo por plataforma).

"fotos" aceita URLs (como as que a API da Shopee devolve) ou arquivos locais,
enviados como data URI. Não testado ao vivo: confira na primeira execução os
nomes dos campos do Seedream V4 Edit e se a WaveSpeed aceita data URI.
"""
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.request
from pathlib import Path

MODELO_IMAGEM = "bytedance/seedream-v4/edit"
MODELO_VIDEO = "bytedance/seedance-v1.5-pro/image-to-video-fast"  # aprovado pelo Kevin em 2026-10-14
RESOLUCAO = "720p"
VIDEO_EXTRA = {"generate_audio": False, "aspect_ratio": "9:16"}  # com áudio o preço dobra
CUSTO_CLIPE_USD = 0.10  # medido pelo saldo: US$ 0,10 por cena de 5 s em 720p sem áudio
CUSTO_IMAGEM_USD = 0.027
MAX_TENTATIVAS = 2


def api(modelo, entrada):
    headers = {"Content-Type": "application/json"}
    if os.environ.get("WAVESPEED_API_KEY"):  # sem a variável, o segredo de rede do projeto injeta o cabeçalho
        headers["Authorization"] = f"Bearer {os.environ['WAVESPEED_API_KEY']}"
    base = "https://api.wavespeed.ai/api/v3"
    req = urllib.request.Request(f"{base}/{modelo}", data=json.dumps(entrada).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        tarefa = json.load(r)["data"]["id"]
    with open(Path(__file__).resolve().parent / "pedidos.log", "a") as log:  # ids pagos, para recuperar se o script parar
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {modelo} {tarefa}\n")
    while True:
        time.sleep(3)
        req = urllib.request.Request(f"{base}/predictions/{tarefa}/result", headers=headers)
        with urllib.request.urlopen(req, timeout=60) as r:
            dados = json.load(r)["data"]
        if dados["status"] == "completed":
            return dados["outputs"][0]
        if dados["status"] in ("failed", "cancelled", "timeout", "deleted"):
            raise RuntimeError(f"{modelo}: {dados['status']} {dados.get('error')}")


def com_teto(etapa, func):
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            return func(), tentativa
        except Exception as e:  # noqa: BLE001
            print(f"  {etapa}: tentativa {tentativa} falhou ({e})")
    raise RuntimeError(f"{etapa}: {MAX_TENTATIVAS} tentativas falharam, vídeo descartado")


def baixar(url, destino):
    urllib.request.urlretrieve(url, destino)
    return destino


def referencia(foto, base):
    if foto.startswith("http"):
        return foto
    arq = (base / foto).read_bytes()
    tipo = mimetypes.guess_type(foto)[0] or "image/png"
    return f"data:{tipo};base64,{base64.b64encode(arq).decode()}"


def main():
    arq = Path(sys.argv[1]).resolve()
    roteiro = json.loads(arq.read_text(encoding="utf-8"))
    pasta = arq.parent / roteiro["nome"]
    pasta.mkdir(exist_ok=True)
    fotos = [referencia(f, arq.parent) for f in roteiro["fotos"]]
    custo = 0.0
    for i, cena in enumerate(roteiro["cenas"], 1):
        print(f"Cena {i}")
        if "editar" in cena:
            img, n = com_teto("imagem", lambda: api(MODELO_IMAGEM, {
                "prompt": cena["editar"], "images": fotos, "size": "720*1280",
            }))
            custo += n * CUSTO_IMAGEM_USD
        else:
            img = fotos[cena["foto"]]
        vid, n = com_teto("vídeo", lambda: api(MODELO_VIDEO, {
            "prompt": cena["movimento"], "image": img, "resolution": RESOLUCAO, "duration": 5, **VIDEO_EXTRA,
        }))
        custo += n * CUSTO_CLIPE_USD
        baixar(vid, pasta / f"cena{i}.mp4")
    print(f"Cenas prontas em {pasta}. Confira 1 quadro de cada cena contra a foto do anúncio.")
    print(f"Custo de API: US$ {custo:.3f} (cerca de R$ {custo * 5.69:.2f})")


if __name__ == "__main__":
    main()
