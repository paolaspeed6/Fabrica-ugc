"""Fiscal de imagem (trava 2) pelo Gemini, grátis (GOOGLEAISTUDIO_API_KEY), para não gastar o uso do Claude (a dona, 26/10:
"de um jeito de nosso projeto economizar tokens"). Mesmo formato de saída da Fiscal subagente: pNN-cenas/fiscal_imagem.json
{"A": {"veredito": "APROVADO|REPROVADO", "provas", "corrigir_prompt", "risco_animacao"}} (mescla: só as cenas pedidas mudam).
uso: python3 -I fiscal_gemini.py p01A,p03B,...      -> imprime uma linha por cena; depois rode aplicar_fiscal.py
     padrão gemini-3-flash-preview (o único liberado na chave grátis em 26/10; o 2.5 saiu e o Pro pede plano pago)."""
import base64, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path
B = Path(__file__).resolve().parent
# só estes respondem na chave grátis (26/10); se um estiver congestionado (503), tenta o próximo
MODELOS = os.environ.get('MODELO', 'gemini-3-flash-preview,gemini-flash-lite-latest,gemini-flash-latest').split(',')
MOD = MODELOS[0]
URL = 'https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent'
REGRAS = (B.parents[2] / 'agentes' / 'regras_de_erros.md')

PEDIDO = """Você é a FISCAL DE IMAGEM de uma fábrica de vídeos de produtos da Shopee (loja Aguiiar Lar). Compare a IMAGEM GERADA (2ª imagem)
com a FOTO DO ANÚNCIO (1ª imagem) e com a ficha abaixo. Reprove só o que uma cliente veria no celular. Reprove se houver:
- produto diferente da foto do anúncio: forma, proporção, cor (desbotada ou outro tom), peças a mais ou a menos, contagem errada
  (kit de N = N itens inteiros; pernas, travessas, botões, rodas, acessórios), item virado de costas ou fora da posição da foto;
- tamanho irreal em relação ao cômodo (gigante ou miniatura);
- produto cortado ou encostando na borda (menos de ~5% de folga de cada lado), ou de borda a borda;
- letra inventada ou torta LEGÍVEL no produto (logo errado);
- PROIBIDOS em qualquer lugar: pessoa, mão, bebê, animal, garrafa, taça, copo, frasco, pote de vidro, bebida, chama acesa,
  tela/painel aceso (exceto se a foto do anúncio mostra assim), texto de propaganda, selos, objetos que a ficha proíbe;
- fundo bagunçado (muitos objetos pequenos soltos) ou decoração encostando/em cima do produto. Decoração simples no fundo é PERMITIDA e desejada
  (a dona, 31/10: plantas, tapete, cerâmica fosca larga, galhos secos, tábua de madeira, quadro sem texto, sol com sombras de folhas).
Responda SÓ um JSON: {"veredito": "APROVADO" ou "REPROVADO", "provas": "o que você conferiu e o motivo, em português, curto",
"corrigir_prompt": "se reprovado: frase em INGLÊS dizendo como a imagem deve ser (nunca cite o objeto proibido, descreva o certo, ex.: 'every surface is bare'); se aprovado: vazio",
"risco_animacao": "se aprovado: aviso curto em português + uma frase em INGLÊS entre aspas duplas para o vídeo, ex.: \\"the camera stays at the same distance and drifts slowly a few centimeters to the left\\" (sem avanço se a folga for pequena); se reprovado: vazio"}"""


def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()


def chamar(partes, tent=6):
    global MOD
    corpo = json.dumps({'contents': [{'parts': partes}], 'generationConfig': {'temperature': 0.1, 'responseMimeType': 'application/json'}}).encode()
    for i in range(tent):
        for m in MODELOS:
            try:
                r = urllib.request.Request(URL.format(m), data=corpo, headers={'Content-Type': 'application/json', 'x-goog-api-key': os.environ['GOOGLEAISTUDIO_API_KEY']})
                d = json.load(urllib.request.urlopen(r, timeout=240))
                MOD = m
                return json.loads(d['candidates'][0]['content']['parts'][0]['text'])
            except urllib.error.HTTPError as e:
                if e.code not in (429, 500, 503): raise
            except (KeyError, IndexError, json.JSONDecodeError, TimeoutError, urllib.error.URLError, ConnectionError):
                pass
        time.sleep(30 * (i + 1))
    raise RuntimeError('Gemini não respondeu')


def referencia(p, f):
    for r in (f.get('fotos_ref') or []):
        q = B / f'{p}-fotos' / (r if str(r).endswith('.jpg') else f'{r}.jpg')
        if q.exists(): return q
    for n in ('01_limpa.jpg', '01.jpg'):
        if (B / f'{p}-fotos' / n).exists(): return B / f'{p}-fotos' / n


def fiscal(p, k):
    f = json.loads((B / f'{p}-ficha.json').read_text())
    cena = next((c for c in f['cenarios'] if c['id'] == k), {})
    campos = {x: f.get(x) for x in ('nome_curto', 'itens', 'partes', 'letras', 'contagem', 'tamanho_real', 'proibidos', 'riscos', 'evitar_close')}
    texto = PEDIDO + '\n\nFICHA DO PRODUTO:\n' + json.dumps(campos, ensure_ascii=False) + '\n\nCENA PEDIDA:\n' + json.dumps(cena, ensure_ascii=False)[:3000]
    ref = referencia(p, f); img = B / f'{p}-cenas/{k}.jpg'
    return chamar([{'text': texto}, {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(ref)}},
                   {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(img)}}])


if __name__ == '__main__':
    for pk in sys.argv[1].split(','):
        p, k = pk[:3], pk[3:]
        if not (B / f'{p}-cenas/{k}.jpg').exists(): print(pk, 'SEM IMAGEM'); continue
        try: v = fiscal(p, k)
        except Exception as e: print(pk, 'FALHOU', e, flush=True); continue
        fj = B / f'{p}-cenas/fiscal_imagem.json'; d = json.loads(fj.read_text()) if fj.exists() else {}
        v['fiscal'] = f'gemini ({MOD})'; d[k] = v; fj.write_text(json.dumps(d, ensure_ascii=False, indent=1))
        print(pk, v['veredito'], '|', v.get('provas', '')[:160].replace('\n', ' '), flush=True)
