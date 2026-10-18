"""Cena grátis no Pruna p-video (demo.pruna.ai): foto real do anúncio + prompt de câmera -> clipe 8 s 720p.
Uso: python3 -I pruna_cena.py <foto> <saida.mp4> "<prompt>"   (grava também <saida>.json com o prompt reescrito)
"""
import json, shutil, sys, time
from gradio_client import Client, handle_file

foto, saida, prompt = sys.argv[1], sys.argv[2], sys.argv[3]
erro = None
for tent in range(3):
    try:
        c = Client("https://demo.pruna.ai/", verbose=False)
        img, vid, ip, vp, err = c.predict(p=prompt, img=handle_file(foto), a="9:16", api_name="/handler")
        if not vid:
            raise RuntimeError(err or "sem vídeo")
        shutil.copy(vid if isinstance(vid, str) else vid["video"], saida)
        ipath = img["path"] if isinstance(img, dict) else img
        if ipath:
            shutil.copy(ipath, saida[:-4] + "_img" + ipath[ipath.rfind("."):])
        json.dump({"prompt": prompt, "image_prompt": ip, "video_prompt": vp, "erro": err}, open(saida[:-4] + ".json", "w"), ensure_ascii=False, indent=1)
        print("ok", saida); sys.exit(0)
    except Exception as e:
        erro = e; print("falhou", tent, e, file=sys.stderr); time.sleep(20 * (tent + 1))
print("ERRO", erro); sys.exit(1)
