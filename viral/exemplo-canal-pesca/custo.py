"""Teto de gasto por chamada da WaveSpeed, calculado ANTES de enviar (2 estouros em 2026-10-17: vozes e Whisper).
Preços medidos pelo saldo. Modelo fora da tabela é recusado: medir 1 trecho curto antes (--medir) e anotar aqui."""
import json, subprocess

# modelo: (unidade, preço por unidade em US$, como medido)
PRECOS = {
    "google/veo3.1-lite/text-to-video":   ("segundo_video", 0.05, "4 s = 0,20 em 2026-10-17"),
    "google/veo3.1-lite/image-to-video":  ("segundo_video", 0.05, "4 s = 0,20; 6 s = 0,30"),
    "google/nano-banana-2.1/text-to-image": ("imagem", 0.036, "0,036 por imagem"),
    "google/nano-banana-2.1/edit":        ("imagem", 0.038, "0,0378 por imagem"),
    "minimax/speech-2.8-hd":              ("mil_caracteres", 0.11, "95 caracteres = 0,0103"),
    "google/nano-banana-pro/text-to-image": ("imagem", 0.126, "1k: 0,126 em 2026-10-17"),
    "google/veo3.1-fast/image-to-video":  ("segundo_video_1080", 0.15, "1080p 4 s = 0,60 em 2026-10-17"),
    "bytedance/seedream-v4":             ("imagem", 0.027, "0,027 por imagem em 2026-10-14"),
    "bytedance/seedream-v4/edit":        ("imagem", 0.027, "0,027 por imagem em 2026-10-14"),
    "wavespeed-ai/openai-whisper-turbo":  ("segundo_audio", 0.0007, "600 s = 0,42; corta em 600 s"),
}

def duracao(url_ou_arquivo):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", url_ou_arquivo],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def pior_caso(modelo, entrada):
    if modelo not in PRECOS:
        raise SystemExit(f"RECUSADO: {modelo} não tem preço medido. Rode 1 trecho curto com --medir e anote em custo.py.")
    unidade, preco, _ = PRECOS[modelo]
    if unidade == "segundo_video":
        q = float(entrada.get("duration", 8))  # sem duração = o maior valor do modelo
        if entrada.get("resolution", "720p") != "720p":
            raise SystemExit("RECUSADO: só 720p tem preço medido")
    elif unidade == "segundo_video_1080":
        q = float(entrada.get("duration", 8))
        if entrada.get("resolution", "1080p") != "1080p":
            raise SystemExit("RECUSADO: só 1080p tem preço medido neste modelo")
    elif unidade == "imagem":
        q = float(entrada.get("num_images", 1))
    elif unidade == "mil_caracteres":
        q = len(entrada["text"]) / 1000
    elif unidade == "segundo_audio":
        q = min(duracao(entrada["audio"]), 600)
    return round(q * preco * 1.05, 4)  # 5% de margem

def conferir(modelo, entrada, teto_chamada, gasto_lote, teto_lote):
    c = pior_caso(modelo, entrada)
    if c > teto_chamada:
        raise SystemExit(f"RECUSADO: pior caso US$ {c} passa do teto desta chamada US$ {teto_chamada}")
    if gasto_lote + c > teto_lote:
        raise SystemExit(f"RECUSADO: lote iria a US$ {gasto_lote + c:.3f}, teto aprovado US$ {teto_lote}")
    return c
