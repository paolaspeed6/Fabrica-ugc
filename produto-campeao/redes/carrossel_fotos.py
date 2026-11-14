"""Fotos do carrossel: cada produto colocado no cenário fixo E_cozinha_branca (Nano Banana edit, US$ 0,0396 cada, teto em gasto_redes.json).
uso: TETO_USD=2.00 python3 -I carrossel_fotos.py carrosseis/<nome>.json
JSON: {"nome": "...", "itens": [{"id", "foto_url", "o_que": "descrição curta em inglês do produto", "onde": "como fica na cena"}]}"""
import base64, json, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
B = Path(__file__).resolve().parent
sys.path.insert(0, str(B.parents[1] / 'video-teste' / 'lote' / 'modelo')); sys.path.insert(0, str(B)); from api import api, baixar
from gerar_redes import cobrar, PRECO

M = 'google/nano-banana-2.1/edit'
CENA = 'data:image/jpeg;base64,' + base64.b64encode((B / 'cenarios' / 'E_cozinha_branca.jpg').read_bytes()).decode()
FIM = (" Keep the room of image 1 exactly (same cabinets, marble, peonies, light, camera angle); only add the product. "
       "The product must be identical to image 2 (same shape, color, pattern, number of pieces), realistic size, soft natural contact shadows, "
       "photorealistic smartphone photo, natural colors, no filter. No people, no hands, no text, no logos, no packaging, "
       "no bottles, no glasses, no drinks, no food.")

def baixa_foto(url):
    with urllib.request.urlopen(url, timeout=60) as r: return 'data:image/jpeg;base64,' + base64.b64encode(r.read()).decode()

def um(arg):
    pasta, it = arg; out = pasta / f"{it['id']}.jpg"
    if out.exists(): return f"{it['id']} já existe"
    txt = f"Image 1 is the room. Image 2 is the product: {it['o_que']}. Place it {it['onde']}." + FIM
    cobrar('carrossel ' + it['id'], PRECO[M])
    u = api(M, {'prompt': txt, 'images': [CENA, baixa_foto(it['foto_url'])], 'aspect_ratio': '4:5', 'resolution': '1k', 'output_format': 'jpeg'})
    baixar(u, out); return f"{it['id']} ok"

if __name__ == '__main__':
    c = json.load(open(sys.argv[1])); pasta = B / 'carrosseis' / c['nome']; pasta.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(3) as ex:
        for r in ex.map(um, [(pasta, it) for it in c['itens']]): print(r, flush=True)
    print('gasto total redes US$', json.loads((B / 'gasto_redes.json').read_text())['usd'])
