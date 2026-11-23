r"""PLACAR de reconhecimento do produto na lista "Adicionar produto / Minhas Curtidas" (Kevin 21/11).

Tudo local e grátis. Várias provas por linha da lista, nunca uma só:
  - POSIÇÃO: o produto recém-curtido costuma ser a 1ª linha (aba "Mais Recente").
  - FOTO: miniatura da linha x foto principal salva na página do produto (cache_produto\<itemId>.png).
  - PREÇO: preço da linha da lista x preços lidos na página do produto (±1%).
  - NOME DISTINTIVO: palavras raras (marca/linha/modelo) pesadas por IDF; palavras comuns (perfume, árabe, kit...) valem ~0.
  - VETO: números em conflito (ml, V, cm, kg, quantidade, códigos tipo PA335) ou marca/modelo distinto diferente.
Regras de decisão (ver decidir()): nunca escolhe na dúvida; empate = não aceita.
"""
import glob, json, math, os, re, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, 'cache_produto')

# palavras comuns que não distinguem produto (peso 0)
COMUNS = set('''de da do das dos e com para por em a o os as um uma ou na no nas nos ao sem sua seu
kit original novo nova importado importada importados premium pro super mega top oferta promocao frete gratis
perfume perfumes arabe arabes masculino feminino masculina feminina unissex fragrancia parfum eau toilette edp edt colonia deo
ml litros litro kg g cm mm m w v volts bivolt branco branca preto preta cinza azul vermelho rosa verde bege marrom dourado dourada prata
casa cozinha sala quarto banheiro escritorio home office multiuso moderno moderna resistente reforcado reforcada
tamanho cor conjunto jogo unidade unidades pecas peca cada lote promocional lancamento'''.split())

ALTO_RISCO = re.compile(r'perfum|fragr|parfum|colonia|eau de|\bedp\b|\bedt\b|deo |body splash|difusor|garrafa|squeeze|frasco|whisky|vinho|licor', re.I)


def norm(s):
    s = re.sub('[​-‍﻿]', '', s or '')
    s = unicodedata.normalize('NFKD', s.replace('&amp;', '&'))
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'[^\w\s]', ' ', s.replace('…', ' ')).replace('_', ' ')
    return ' '.join(s.split())


def tokens(nome):
    t = norm(nome).split()
    if t and re.match(r'^0+[^\W_]', t[0]) and not t[0].isdigit():  # lixo de leitura "0WAP"/"060x45" -> "wap"/"60x45"
        t[0] = t[0].lstrip('0')
    t = [_stem(x) for x in t]
    return [x for x in t if len(x) > 1 or x.isdigit()]


COR = set('branco preto cinza azul vermelho rosa verde bege marrom dourado prata amarelo laranja roxo nude off grafite cobre caramelo areia'.split())


def _stem(x):
    """curvo/curva, cadeiras/cadeira: tira o s final e a vogal de gênero (palavras com letras e ≥5 letras)."""
    if x.isalpha() and len(x) >= 5:
        if x.endswith('s'):
            x = x[:-1]
        if len(x) >= 5 and x[-1] in 'aoe':
            x = x[:-1]
    return x


_IDF = {}


def _corpus():
    nomes = []
    for p in glob.glob(os.path.join(BASE, 'filas', '*.json')) + [os.path.join(BASE, 'fila.json')]:
        try:
            for it in json.load(open(p, encoding='utf-8-sig')):
                for k in ('produto', 'titulo', 'nome'):
                    if it.get(k):
                        nomes.append(it[k])
        except Exception:
            pass
    for p in (os.path.join(BASE, 'feedback_aprovacoes.json'), os.path.join(BASE, 'pendentes_aprovacao.json')):
        try:
            d = json.load(open(p, encoding='utf-8-sig'))
            for it in (d if isinstance(d, list) else list(d.values())):
                if isinstance(it, dict):
                    nomes += [it.get(k) for k in ('esperado', 'escolhido', 'produto_video', 'produto') if it.get(k)]
                    nomes += [l for l in it.get('linhas_vistas', []) if isinstance(l, str)]
        except Exception:
            pass
    try:
        d = json.load(open(os.path.join(BASE, 'titulos.json'), encoding='utf-8-sig'))
        for v in d.values():
            if isinstance(v, str):
                nomes.append(v)
    except Exception:
        pass
    return nomes


def idf(tok):
    if not _IDF:
        nomes = set(norm(n) for n in _corpus() if isinstance(n, str))
        df = {}
        for n in nomes:
            for t in set(tokens(n)):
                df[t] = df.get(t, 0) + 1
        _IDF['_N'] = max(len(nomes), 1)
        _IDF.update(df)
    if tok in COMUNS:
        return 0.0
    df = _IDF.get(tok, 0)
    return max(0.2, math.log((_IDF['_N'] + 1) / (df + 1)))  # raro = alto


RARO = 2.0  # peso mínimo para ser "palavra distintiva"


def _num_conflito(E, R):
    """Números/códigos em conflito: mesma parte de letras ('ml', 'v', 'pa', '') com dígitos diferentes."""
    def par(t):
        m = re.match(r'^([^\d]*)(\d+)([^\d]*)$', t)
        return (m[1] + '|' + m[3], m[2]) if m else (t, '')
    # códigos de modelo (letras+dígitos, ≥5, não "100ml"/"220v"): SBD716B x SCD701B = produtos diferentes
    cod = lambda t: len(t) >= 5 and re.search(r'\d', t) and re.search(r'[^\W\d_]', t) and not re.match(r'^\d+[^\W\d_]{1,3}$', t)
    cE = {t for t in E if cod(t)}
    cR = {t for t in R if cod(t)}
    if cE - cR and cR - cE:
        return f'código de modelo diferente: {sorted(cE - cR)[0]} x {sorted(cR - cE)[0]}'
    nE = {t for t in E if re.search(r'\d', t)}
    nR = {t for t in R if re.search(r'\d', t)}
    for e in nE - nR:
        for r in nR - nE:
            (ke, de), (kr, dr) = par(e), par(r)
            if ke == kr and de != dr:
                return f'número diferente: {e} x {r}'
    return None


def prova_nome(esperado, linha, parcial=False):
    """(similaridade_distintiva 0..1, palavras_raras_em_comum, veto_ou_None).
    parcial=True: o 'esperado' é só o nome curto do vídeo (não o título completo do anúncio): então só vale veto de
    número com unidade (ml, V, cm...) e de palavra distintiva do esperado ausente na linha."""
    E, R = tokens(esperado), tokens(linha)
    if not E or not R:
        return 0.0, 0, None
    Ej, Rj = ''.join(E), ''.join(R)
    truncada = bool(re.search(r'(…|\.\.\.)\s*$', linha or ''))
    if truncada and len(R) < len(E):
        E_cmp = E[:len(R) + 2]
    else:
        E_cmp = E
    if parcial:
        veto = _num_conflito([t for t in E_cmp if re.search(r'\d\D|\D\d', t)], [t for t in R if re.search(r'\d\D|\D\d', t)])
    else:
        veto = _num_conflito(E_cmp, R)
    # cor diferente = variante diferente (BEGE x CINZA): se os dois citam cor e os conjuntos não se contêm, veta
    cE = {t for t in E_cmp if t in COR or _stem(t) in COR}
    cR = {t for t in R if t in COR or _stem(t) in COR}
    if cE and cR and not (cE <= cR or cR <= cE):
        veto = veto or f'cor diferente: {sorted(cE)} x {sorted(cR)}'
    # marca/modelo distinto: palavra rara de um lado que NÃO existe no outro (nem colada: "shaw ty" = "shawty")
    for t in ([] if parcial else R):
        if t not in E and not re.search(r'\d', t) and idf(t) >= RARO and t not in Ej:
            veto = veto or f'palavra distintiva só na linha da lista: "{t}"'
    for t in E_cmp:
        if t not in R and not re.search(r'\d', t) and idf(t) >= RARO and t not in Rj:
            veto = veto or f'palavra distintiva só no esperado: "{t}"'
    sw = lambda ts, ref, refj: (sum(idf(t) for t in ts if t in ref or t in refj), sum(idf(t) for t in ts))
    a, b = sw(R, set(E), Ej)
    c, d = sw(E_cmp, set(R), Rj)
    cob_r = a / b if b else 0.0
    cob_e = c / d if d else 0.0
    raras = sum(1 for t in set(R) & set(E) if idf(t) >= RARO)
    return min(cob_r, cob_e), raras, veto


def preco_igual(precos_pagina, preco_linha):
    if not preco_linha or not precos_pagina:
        return None
    return any(abs(p - preco_linha) <= 0.01 * preco_linha + 0.005 for p in precos_pagina)


def precos_de_textos(textos):
    out = []
    for t in textos:
        for m in re.finditer(r'R\$\s?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})', t):
            out.append(float(m[1].replace('.', '').replace(',', '.')))
    return out


def preco_da_linha(txt):
    m = re.match(r'^R\$\s?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})(?:\s*-\s*R\$.*)?$', (txt or '').strip())  # aceita faixa "R$10,00 - R$20,00"
    return float(m[1].replace('.', '').replace(',', '.')) if m else None


# ------------------------------------------------------------------ foto
def _prep(img, lado=96):
    import numpy as np
    from PIL import Image
    im = img.convert('RGB')
    a = np.asarray(im).astype('int16')
    m = (np.abs(a - 255).max(axis=2) > 14)
    if m.sum() < 40:
        return None
    ys, xs = np.where(m)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    w, h = im.size
    s = max(w, h)
    q = Image.new('RGB', (s, s), (255, 255, 255))
    q.paste(im, ((s - w) // 2, (s - h) // 2))
    return q.resize((lado, lado), Image.LANCZOS)


def foto_score(foto_pagina, miniatura):
    """0..1: quanto a miniatura da lista parece a foto da página (dHash + cor + ORB). None se não deu para comparar."""
    try:
        import numpy as np
        import cv2
        a, b = _prep(foto_pagina), _prep(miniatura)
        if a is None or b is None:
            return None
        A, B = np.asarray(a), np.asarray(b)
        ga, gb = cv2.cvtColor(A, cv2.COLOR_RGB2GRAY), cv2.cvtColor(B, cv2.COLOR_RGB2GRAY)
        def dh(g):
            r = cv2.resize(g, (17, 16), interpolation=cv2.INTER_AREA)
            return (r[:, 1:] > r[:, :-1]).flatten()
        ham = float((dh(ga) != dh(gb)).mean())  # 0 igual .. 0.5 aleatório
        hs = []
        for X in (A, B):
            h = cv2.calcHist([cv2.cvtColor(X, cv2.COLOR_RGB2HSV)], [0, 1], None, [12, 6], [0, 180, 0, 256])
            hs.append(cv2.normalize(h, h).flatten())
        cor = max(0.0, float(cv2.compareHist(hs[0], hs[1], cv2.HISTCMP_CORREL)))
        orb = cv2.ORB_create(400)
        ka, da = orb.detectAndCompute(ga, None)
        kb, db = orb.detectAndCompute(gb, None)
        bons = 0
        if da is not None and db is not None and len(da) > 5 and len(db) > 5:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
            for par in bf.knnMatch(da, db, k=2):
                if len(par) == 2 and par[0].distance < 0.75 * par[1].distance:
                    bons += 1
        # SIFT + RANSAC (21/11): nº de pontos que coincidem GEOMETRICAMENTE entre a foto da página e a miniatura.
        # Mesmo produto/foto => dezenas; produtos diferentes => ~0-3 (dHash/histograma não separavam: calibrar_foto.py).
        sift = cv2.SIFT_create(400)
        ka, da = sift.detectAndCompute(cv2.cvtColor(np.asarray(_prep(foto_pagina, 256)), cv2.COLOR_RGB2GRAY), None)
        kb, db = sift.detectAndCompute(cv2.cvtColor(np.asarray(_prep(miniatura, 256)), cv2.COLOR_RGB2GRAY), None)
        if da is None or db is None or len(da) < 4 or len(db) < 4:
            return 0
        bons = [m for m, n in (p for p in cv2.BFMatcher().knnMatch(da, db, k=2) if len(p) == 2) if m.distance < 0.75 * n.distance]
        if len(bons) < 4:
            return 0
        pa = np.float32([ka[m.queryIdx].pt for m in bons])
        pb = np.float32([kb[m.trainIdx].pt for m in bons])
        _, mask = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=6)
        return int(mask.sum()) if mask is not None else 0
    except Exception:
        return None


# nº de pontos coincidentes (SIFT+RANSAC). calibrar_foto.py: entre ~2700 pares de produtos DIFERENTES o máximo foi 24
# (só 3 pares >= 20); miniaturas do mesmo produto simuladas >= 34. Limiares acima do máximo dos diferentes: 0 falsos positivos.
LIM_FORTE, LIM_MEDIA = 40, 25


def nivel_foto(f):
    if f is None:
        return 'sem'
    return 'forte' if f >= LIM_FORTE else ('media' if f >= LIM_MEDIA else 'fraca')


# ------------------------------------------------------------------ cache da página do produto
def salvar_cache(item_id, im_pagina, textos, nome=None):
    """Chamado no passo [1] (produto aberto): guarda a foto principal + preços + nome por itemId."""
    try:
        os.makedirs(CACHE, exist_ok=True)
        w, h = im_pagina.size
        foto = im_pagina.crop((int(w * 0.04), int(h * 0.09), int(w * 0.96), int(h * 0.43)))  # galeria (720x1600)
        foto.save(os.path.join(CACHE, f'{item_id}.png'))
        json.dump({'itemId': item_id, 'nome': nome, 'precos': precos_de_textos(textos)},
                  open(os.path.join(CACHE, f'{item_id}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception:
        pass


def ler_cache(item_id):
    from PIL import Image
    try:
        j = json.load(open(os.path.join(CACHE, f'{item_id}.json'), encoding='utf-8'))
        im = Image.open(os.path.join(CACHE, f'{item_id}.png')).convert('RGB')
        return {'foto': im, 'precos': j.get('precos', []), 'nome': j.get('nome')}
    except Exception:
        return None


# ------------------------------------------------------------------ decisão
def avaliar(esperado, linha_nome, linha_preco, miniatura, cache, posicao):
    """Placar de UMA linha."""
    sim, raras, veto = prova_nome(esperado, linha_nome)
    f = foto_score(cache['foto'], miniatura) if (cache and miniatura is not None) else None
    pi = preco_igual(cache['precos'], linha_preco) if cache else None
    return {'pos': posicao, 'nome': linha_nome, 'sim': round(sim, 2), 'raras': raras, 'veto': veto,
            'foto': f, 'nivel_foto': nivel_foto(f), 'preco_igual': pi, 'preco': linha_preco}


def decidir(placares, esperado, alto_risco=None):
    """Devolve (indice_aceito|None, [linhas de log]). Nunca escolhe na dúvida."""
    if alto_risco is None:
        alto_risco = bool(ALTO_RISCO.search(esperado or '') or any(ALTO_RISCO.search(p['nome'] or '') for p in placares))
    ok = []
    log = []
    for i, p in enumerate(placares):
        nome_ok = p['sim'] >= 0.60 and p['raras'] >= 2
        foto_m = p['nivel_foto'] in ('media', 'forte')
        foto_f = p['nivel_foto'] == 'forte'
        preco = p['preco_igual'] is True
        primeira = p['pos'] == 0
        # PREÇO é prova FRACA (Kevin: muda de uma hora pra outra): só aparece no log; NUNCA veta e NUNCA vale como 2ª confirmação.
        provas = [x for x, v in (('foto', foto_m), ('nome', nome_ok)) if v]
        if p['veto'] and str(p['veto']).startswith('palavra distintiva') and foto_f and primeira and not alto_risco:
            # anúncio renomeado: mesmas fotos (>=40 pontos SIFT, 0 falsos em ~2700 pares) = mesmo produto; só números/códigos/cor/marca-ml vetam de verdade
            r = 'ACEITA (foto forte supera nome escrito diferente)'
            ok.append(i)
        elif p['veto']:
            r = f'VETO ({p["veto"]})'
        elif alto_risco:
            r = 'ACEITA' if (primeira and foto_f and nome_ok) else 'não (alto risco: 1ª + foto forte + nome distintivo)'
            if r == 'ACEITA':
                ok.append(i)
        elif primeira:
            r = 'ACEITA' if provas else 'não (1ª linha sem 2ª confirmação: foto média/forte ou nome distintivo)'
            if provas:
                ok.append(i)
        else:
            r = 'ACEITA' if (foto_f and nome_ok) else 'não (fora da 1ª: só foto forte + nome distintivo)'
            if foto_f and nome_ok:
                ok.append(i)
        log.append(f'linha {p["pos"] + 1}: foto={p["foto"]} ({p["nivel_foto"]}) preço={"=" if preco else ("≠" if p["preco_igual"] is False else "?")} '
                   f'nome={p["sim"]} (raras {p["raras"]}) → {r}')
    if len(ok) > 1:
        log.append('EMPATE entre linhas: não escolho (pendente)')
        return None, log
    return (ok[0] if ok else None), log
