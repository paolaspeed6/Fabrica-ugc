"""Imagens para carrossel (Insta + TikTok): guarda no Drive SÓ os produtos estratégicos (a dona, 07/11: "apenas imagens de
produtos aesthetics, que chamem atenção; peça de carro não faz sentido guardar"). Grátis: Gemini decide + Drive.
uso: python3 -I salvar_imagens.py <lote> p01,p02,... [--dia AAAA-MM-DD] [--seco]
  Gemini olha a melhor cena aprovada + o nome e dá nota de 0 a 10 para "aesthetic que para o dedo no feed".
  Nota >= 8 (NOTA_MIN): sobe as cenas aprovadas (sem pessoa/mão) para <DRIVE_PASTA>/Carrossel/<dia>/<itemid>_<slug>/
  com info.txt (nome, ID do produto, link, 3 frases curtas). Registro em <lote>/carrossel.json (pula o que já foi)."""
import json, os, re, sys, base64
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # video-teste/
import drive_backup as D
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fiscal_gemini as G

NOTA_MIN = int(os.environ.get('NOTA_MIN', '8'))
PEDIDO = """Você escolhe produtos para CARROSSEL DE FOTOS no Instagram e no TikTok da loja Aguiiar Lar (casa, decoração, estilo de vida).
Só entram produtos ESTRATÉGICOS: bonitos, "aesthetic", que fazem a pessoa parar de rolar o feed e salvar o post
(decoração, organização bonita, cozinha/mesa posta elegante, iluminação, têxteis, móveis de design, cuidado pessoal bonito, gadgets fofos de casa).
NÃO entram (nota baixa): peça de carro/moto, ferramenta, ferragem, peça de reposição, material de construção, produto técnico ou feio,
coisa que só faz sentido funcional (amortecedor, filtro, cabo, parafuso, bomba), equipamento grande sem charme visual.
Produto: {nome}
Olhe a imagem (cena gerada do produto num ambiente). Responda SÓ JSON:
{{"nota": 0 a 10 (10 = muito aesthetic e chamativo para carrossel), "motivo": "curto, português",
"frases": ["3 frases curtas em português para os slides do carrossel, no máximo 7 palavras cada, sem preço, sem %, sem prometer entrega, sem nota/avaliações"]}}"""


def aprovadas(p, L):
    d = L / f'{p}-cenas'
    try: fi = json.loads((d / 'fiscal_imagem.json').read_text())
    except Exception: fi = {}
    return [d / f'{c}.jpg' for c in 'ABC' if (d / f'{c}.jpg').exists() and str(fi.get(c, {}).get('veredito', '')).upper().startswith('APROV')]


def main():
    a = sys.argv[1:]; seco = '--seco' in a; a = [x for x in a if x != '--seco']
    dia = None
    if '--dia' in a: i = a.index('--dia'); dia = a[i + 1]; del a[i:i + 2]
    L = Path(a[0]).resolve(); ps = a[1].split(',')
    import datetime; dia = dia or datetime.date.today().isoformat()
    reg_f = L / 'carrossel.json'; reg = json.loads(reg_f.read_text()) if reg_f.exists() else {}
    try: textos = json.loads((L / 'textos.json').read_text())
    except Exception: textos = {}
    tk = None
    for p in ps:
        if p in reg and (reg[p].get('enviado') or reg[p].get('nota', 0) < NOTA_MIN): print(p, 'já avaliado', reg[p].get('nota')); continue
        imgs = aprovadas(p, L)
        if not imgs: print(p, 'sem cena aprovada'); continue
        try: f = json.loads((L / f'{p}-ficha.json').read_text())
        except Exception: f = {}
        t = textos.get(p, {}); nome = t.get('nome') or f.get('nome_pt') or p
        link = t.get('link', ''); m = re.search(r'/(\d+)/?$', link) or re.search(r'i\.\d+\.(\d+)', link); iid = m.group(1) if m else p
        r = G.chamar([{'text': PEDIDO.format(nome=nome)}, {'inline_data': {'mime_type': 'image/jpeg', 'data': G.b64(imgs[0])}}])
        nota = int(r.get('nota', 0)); reg[p] = {'nome': nome, 'id': iid, 'link': link, 'nota': nota, 'motivo': r.get('motivo', ''), 'frases': r.get('frases', [])}
        print(p, nome, 'nota', nota, '-', r.get('motivo', ''))
        if nota >= NOTA_MIN and not seco:
            tk = tk or D.token()
            pai = D.pasta(tk, D.RAIZ, 'root')
            for parte in ('Carrossel', dia, f"{iid}_{t.get('slug') or p}"): pai = D.pasta(tk, parte, pai)
            info = L / f'{p}-cenas' / 'info.txt'
            info.write_text(f"{nome}\nID do produto: {iid}\nLink: {link}\nFrases:\n" + '\n'.join('- ' + x for x in reg[p]['frases']) + '\n')
            for im in imgs:
                c = L / f'{p}-cenas' / f'{iid}_{im.name}'; c.write_bytes(im.read_bytes()); D.enviar(tk, str(c), pai, 'image/jpeg')
            D.enviar(tk, str(info), pai, 'text/plain'); reg[p]['enviado'] = True
            print(p, 'no Drive:', len(imgs), 'imagens')
        reg_f.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
    n = sum(1 for v in reg.values() if v.get('enviado')); print(f'CARROSSEL {n} produtos estratégicos no Drive (nota mínima {NOTA_MIN})')


if __name__ == '__main__':
    main()
