"""K31, última trava antes da Conferir (grátis, Gemini): compara 3 quadros de cada vídeo final (uma por cena) com a FOTO 01 do anúncio.
Produto diferente (outra variante, detalhe inventado, forma/cor errada) vira AVISO no cartão da Conferir (avisos.json), com a cena e o motivo,
para a dona descartar ou pedir edição antes de postar. Não gasta nada pago.
uso: python3 -I conferir_produto.py <pasta do lote>   (o entregar.sh já roda, antes do Drive e da conferencia.py)"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fiscal_gemini import b64, chamar

L = Path(sys.argv[1]).resolve()
PEDIDO = """Fiscal RIGOROSA. Imagem 1 = FOTO 01 do anúncio da Shopee (o produto que a cliente recebe). Imagens 2, 3 e 4 = quadros de 3 cenas
de um vídeo do produto (ignore textos e legendas por cima). O produto de cada cena é o MESMO da foto 01, detalhe por detalhe? Confira forma,
proporção, cor e tom, cor dos pés/base/metal, material e textura, costuras, braços, puxadores, gavetas, nichos, peças a mais ou a menos.
Responda só JSON: {"cenas": [{"cena": 2, "igual": true/false, "diferenca": "curta, em português"}, {"cena": 3, ...}, {"cena": 4, ...}],
"gravidade": 0-10 (0 = idêntico; 10 = claramente outro produto)}"""
avp = L / 'avisos.json'; av = json.loads(avp.read_text()) if avp.exists() else {}
res = {}
for mp4 in sorted((L / 'final').glob('*_[ABC].mp4')):
    m = re.match(r'[^_]+_(\d+)_.*_([ABC])\.mp4', mp4.name)
    if not m: continue
    p, v = 'p' + m.group(1), m.group(2)
    f = json.loads((L / f'{p}-ficha.json').read_text()) if (L / f'{p}-ficha.json').exists() else {}
    um = next((L / (x if '/' in x else f'{p}-fotos/{x}') for x in (f.get('fotos_ref') or []) if Path(x).name in ('01_limpa.jpg', '01.jpg')), L / f'{p}-fotos/01.jpg')
    if not um.exists(): continue
    with tempfile.TemporaryDirectory() as td:
        qs = []
        for i, t in enumerate((2.0, 5.5, 9.0)):
            q = Path(td) / f'{i}.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(mp4), '-frames:v', '1', '-vf', 'scale=540:-2', str(q)])
            if q.exists(): qs.append(q)
        # folha para a Fiscal final (Sonnet): foto 01 + 3 cenas, lado a lado (o Gemini sozinho deixou passar exaustor quadrado e tapete errado, 15/11)
        from PIL import Image
        ims = [Image.open(x).convert('RGB') for x in [um] + qs]; H = 640
        ims = [i.resize((max(1, int(i.width * H / i.height)), H)) for i in ims]
        fo = Image.new('RGB', (sum(i.width for i in ims) + 8 * len(ims), H), 'white'); x0 = 0
        for i in ims: fo.paste(i, (x0, 0)); x0 += i.width + 8
        (L / 'folhas_finais').mkdir(exist_ok=True); fo.save(L / 'folhas_finais' / f'{p}{v}.jpg', quality=85)
        try:
            r = chamar([{'text': PEDIDO}, {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(um)}}] +
                       [{'inline_data': {'mime_type': 'image/jpeg', 'data': b64(q)}} for q in qs])
            if isinstance(r, list): r = r[0]
        except Exception as e: print(mp4.name, 'FALHOU', e); continue
    res[mp4.name] = r
    ruins = [c for c in r.get('cenas', []) if not c.get('igual')]
    if ruins and (r.get('gravidade') or 0) >= 4:
        msg = '⚠ produto diferente da foto 01: ' + '; '.join(c.get('diferenca', '') for c in ruins)[:180]
        av.setdefault(p, {})[v] = (av.get(p, {}).get(v, '') + ' ' + msg).strip()
    print(mp4.name, 'grav', r.get('gravidade'), '|', '; '.join(c.get('diferenca', '') for c in ruins)[:150], flush=True)
avp.write_text(json.dumps(av, ensure_ascii=False)); (L / 'conferir_produto.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
