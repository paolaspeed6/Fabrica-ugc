"""K22 (a dona, 30/10): produto sem cena aprovada NÃO para mais em cartão de resgate. A fábrica monta A, B e C sozinha com as
imagens reprovadas SÓ por borda/largura (folha.py, "borda medida por código") ou com imagem aprovada e clipe reprovado,
com câmera por código (camera_codigo.py, grátis, nunca clipe IA: K19), e o produto vai para a Conferir com o aviso
"cenas reprovadas pela fiscal: confira". Ela descarta à mão se não servir.
Defeito grave (pessoa, mão, animal, bebida, garrafa/taça/copo, letra inventada, objeto proibido) continua fora: as imagens
que só a folha.py reprovou (nunca passaram na Fiscal) passam antes por uma checagem só de defeito grave no Gemini (grátis).
Sem nenhuma imagem aproveitável o produto segue para o descartadas.py (cartão resgate), como antes.
uso: python3 -I sem_cena.py p01,p02,...   (só mexe nos produtos sem aprovado.json; o produzir.sh roda depois do aprovar.py)"""
import json, shutil, subprocess, sys
from pathlib import Path
B = Path(__file__).resolve().parent
sys.path.insert(0, str(B))
AVISO = 'cenas reprovadas pela fiscal: confira'
GRAVE = """Você confere uma imagem de produto para um vídeo de loja (Shopee). A 1ª imagem é a foto do anúncio, a 2ª é a cena gerada.
Ignore enquadramento, borda, corte nas pontas e tamanho do produto: isso já é sabido. Responda GRAVE só se houver na 2ª imagem:
pessoa, mão, bebê, animal, bebida, garrafa, taça, copo, frasco, chama acesa, texto de propaganda/selo, letra legível inventada ou
errada no produto, objeto proibido em cima do produto, ou um produto claramente diferente do anúncio (outro modelo, cor, peças a menos).
Responda SÓ um JSON: {"grave": true ou false, "motivo": "curto, em português"}"""


def ler(p, padrao):
    return json.loads(p.read_text()) if p.exists() else padrao


def grave(p, img):
    from fiscal_gemini import chamar, b64, referencia
    f = ler(B / f'{p}-ficha.json', {})
    try:
        v = chamar([{'text': GRAVE}, {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(referencia(p, f))}},
                    {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(img)}}], tent=3)
    except Exception as e:
        return f'Gemini não respondeu ({e})'  # sem conferir, não entra
    return (v.get('motivo') or 'defeito grave') if v.get('grave') else ''


def candidatas(p):
    """{cena: imagem} aproveitáveis: imagem aprovada (clipe reprovado) ou a última versão reprovada só por borda."""
    d = B / f'{p}-cenas'; fi = ler(d / 'fiscal_imagem.json', {}); rr = ler(d / 'reprovacoes.json', []); out = {}
    for c in 'ABC':
        if (d / f'{c}.jpg').exists() and str((fi.get(c) or {}).get('veredito', '')).upper().startswith('APROV'):
            out[c] = d / f'{c}.jpg'; continue
        vers = sorted(B.glob(f'rejeitadas/{p}_{c}_v*.jpg'), key=lambda x: int(x.stem.rsplit('_v', 1)[1]), reverse=True)
        for img in vers:
            n = int(img.stem.rsplit('_v', 1)[1])
            mot = next((x['motivo'] for x in rr if x['cena'] == c and x.get('etapa') == f'imagem {n}ª'), '')
            if mot.startswith('borda medida'):
                g = grave(p, img); print(p, c, f'v{n}', 'GRAVE: ' + g if g else 'só borda: entra', flush=True)
                if not g: out[c] = img
                break  # a versão mais nova manda (a mais velha já foi trocada por um motivo)
    return out


if __name__ == '__main__':
    for p in sys.argv[1].split(','):
        d = B / f'{p}-cenas'
        if not d.exists() or (d / 'aprovado.json').exists(): continue
        cs = candidatas(p)
        if not cs: print(p, 'nenhuma imagem aproveitável: vai como resgate (descartadas.py)'); continue
        for c, img in cs.items():
            if img != d / f'{c}.jpg': shutil.copy(img, d / f'{c}.jpg')
        for c in 'ABC':
            if c not in cs: (d / f'{c}.jpg').unlink(missing_ok=True)
        subprocess.run([sys.executable, '-I', str(B / 'camera_codigo.py'), p, ','.join(cs)], check=True)
        av = ler(B / 'avisos.json', {}); av.setdefault(p, {})['geral'] = AVISO
        (B / 'avisos.json').write_text(json.dumps(av, ensure_ascii=False)); print(p, 'montado com', ','.join(cs), '+ aviso')
