"""Narração luxo grátis (Gemini TTS, voz Kore). uso: [ESTILO="..."] python3 -I tts_lux.py "texto" saida.wav
Rodar uma de cada vez: várias em paralelo deram HTTP 429."""
import os,sys,json,base64,urllib.request,subprocess
text,out=sys.argv[1],sys.argv[2]
ESTILO=os.environ.get("ESTILO","voz calma, elegante e sofisticada, ritmo pausado, como comercial de marca de decoração de luxo")
# 2.5 = só 10 grátis por dia (2026-10-18); os outros recebem o estilo como instrução de sistema (senão leem a instrução em voz alta)
MODELO=os.environ.get("MODELO","gemini-2.5-flash-preview-tts")
cfg={"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":os.environ.get("VOZ","Kore")}}}}
if MODELO.startswith("gemini-2.5") or os.environ.get("PREFIXO"):
    body={"contents":[{"parts":[{"text":"Fale em português do Brasil com "+ESTILO+": "+text}]}],"generationConfig":cfg}
else:  # texto puro, sem instrução (systemInstruction dá 400 nos modelos de voz; o 3.8 lê instrução em voz alta)
    body={"contents":[{"parts":[{"text":text}]}],"generationConfig":cfg}
req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent",
 data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":os.environ["GOOGLEAISTUDIO_API_KEY"]})
r=json.load(urllib.request.urlopen(req,timeout=120))
pcm=base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
open(out+".pcm","wb").write(pcm)
subprocess.run(["ffmpeg","-v","error","-y","-f","s16le","-ar","24000","-ac","1","-i",out+".pcm",out],check=True)
