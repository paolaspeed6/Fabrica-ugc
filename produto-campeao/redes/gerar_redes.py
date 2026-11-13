"""Imagens das REDES SOCIAIS (carrossel) pela WaveSpeed, com teto duro em gasto_redes.json (a dona, 13/11: teto US$ 2,00 no teste).
uso: TETO_USD=2.00 python3 -I gerar_redes.py cenarios"""
import json, os, sys, fcntl
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
B = Path(__file__).resolve().parent
sys.path.insert(0, str(B.parents[1] / 'video-teste' / 'lote' / 'modelo')); from api import api, baixar
TETO = float(os.environ.get('TETO_USD', '0')); GF = B / 'gasto_redes.json'
PRECO = {'google/nano-banana-2.1/text-to-image': 0.0396, 'google/nano-banana-2.1/edit': 0.0396}

def cobrar(nome, usd):
    with open(B / 'gasto.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        g = json.loads(GF.read_text()) if GF.exists() else {'usd': 0.0, 'itens': []}
        if g['usd'] + usd > TETO + 1e-9: raise RuntimeError(f'TETO atingido antes de {nome}')
        g['usd'] = round(g['usd'] + usd, 4); g['itens'].append([nome, usd]); GF.write_text(json.dumps(g, indent=1))

# Identidade da casa Aguiiar Lar (a dona, 13/11): romântica, sofisticada, branco com madeira e plantas, flores, rosa, estilo americano.
CASA = ("Photorealistic vertical 9:16 smartphone photo, 26 mm lens, natural focus, fine grain, candid lifestyle post of a real home. "
        "Romantic and sophisticated American-style home: white walls and white cabinetry, warm natural wood, green plants, fresh pink and blush flowers, "
        "soft warm daylight, airy, clean and cozy. The center of the surface is EMPTY and clear, ready to place one product there later. "
        "No people, no hands, no text, no logos, no bottles, no glasses, no drinks. ")
CENARIOS = {
 'A_bancada': CASA + "Kitchen corner: white marble countertop seen at a slight high angle, light wood open shelf and white subway-tile backsplash behind, "
              "a small vase of pink peonies at the far left back, a trailing green plant on the shelf, warm under-cabinet light.",
 'B_aparador': CASA + "Living-room corner: a white painted wooden console table with brass details in front of a white wall with classic wall molding, "
              "a pink rose bouquet at the back left, a large potted olive tree to the right on the floor, soft window light from the left.",
 'C_mesa': CASA + "Dining nook: a light oak wooden table with a white linen tablecloth corner, a window with sheer white curtains behind, "
              "a small ceramic vase with pink garden roses at the back, eucalyptus sprigs, soft morning light.",
}

def cenario(n):
    out = B / 'cenarios' / f'{n}.jpg'
    if out.exists(): return f'{n} já existe'
    m = 'google/nano-banana-2.1/text-to-image'; cobrar('cenario ' + n, PRECO[m])
    u = api(m, {'prompt': CENARIOS[n], 'aspect_ratio': '9:16', 'resolution': '1k', 'output_format': 'jpeg'})
    baixar(u, out); return f'{n} ok'

if __name__ == '__main__':
    if sys.argv[1] == 'cenarios':
        with ThreadPoolExecutor(3) as ex:
            for r in ex.map(cenario, CENARIOS): print(r)
    print('gasto', json.loads(GF.read_text())['usd'] if GF.exists() else 0)
