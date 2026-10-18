"""Narração luxo grátis (Gemini TTS, voz Kore). uso: python3 -I tts_lux.py "texto" saida.wav
Rodar uma de cada vez: várias em paralelo deram HTTP 429."""
import os,sys,json,base64,urllib.request,subprocess
text,out=sys.argv[1],sys.argv[2]
body={"contents":[{"parts":[{"text":"Fale em português do Brasil com voz calma, elegante e sofisticada, ritmo pausado, como comercial de marca de decoração de luxo: "+text}]}],
 "generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Kore"}}}}}
req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent",
 data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":os.environ["GOOGLEAISTUDIO_API_KEY"]})
r=json.load(urllib.request.urlopen(req,timeout=120))
pcm=base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
open(out+".pcm","wb").write(pcm)
subprocess.run(["ffmpeg","-v","error","-y","-f","s16le","-ar","24000","-ac","1","-i",out+".pcm",out],check=True)
