"""Voz PADRÃO da fábrica (a dona, 2026-10-18): Kokoro local, mistura "dora_nicole" = 75% pf_dora + 25% af_nicole,
velocidade 0,9. Grátis e sem limite. uso: python3 -I tts_kokoro.py "texto" saida.wav
Modelo: KOKORO_DIR (padrão /home/user/modelos-voz) com kokoro-v1.0.onnx e voices-v1.0.bin
(baixar de https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 ; pip install kokoro-onnx soundfile)."""
import os, sys
import soundfile as sf
from kokoro_onnx import Kokoro

D = os.environ.get('KOKORO_DIR', '/home/user/modelos-voz')
text, out = sys.argv[1], sys.argv[2]
k = Kokoro(f'{D}/kokoro-v1.0.onnx', f'{D}/voices-v1.0.bin')
voz = k.get_voice_style('pf_dora') * 0.75 + k.get_voice_style('af_nicole') * 0.25
a, sr = k.create(text, voice=voz, speed=float(os.environ.get('VELOCIDADE', 0.9)), lang='pt-br')
sf.write(out, a, sr)
