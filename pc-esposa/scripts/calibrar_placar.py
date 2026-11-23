r"""Validação OFFLINE do placar (placar.py) com os casos reais de feedback_aprovacoes.json + perfumes.
Uso: python calibrar_placar.py   (não toca em celular nem em fila; só lê arquivos)
"""
import itertools, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import placar as P

BASE = os.path.dirname(os.path.abspath(__file__))
fb = json.load(open(os.path.join(BASE, 'feedback_aprovacoes.json'), encoding='utf-8-sig'))
lim = lambda s: re.sub(r'^\(OCR\)\s*', '', s or '')

# ---------- 1) aprovados pelo Kevin: a linha escolhida NÃO pode levar veto; conta quantos têm prova de nome
aprov = [x for x in fb if x['decisao'] == 'aprovado' and x.get('escolhido') and x.get('linhas_vistas')]
sem_veto = nome_ok = 0
for x in aprov:
    boa = len(x.get('esperado', '')) > 25 and not re.match(r'(Compre|Economize|Classificado)', x['esperado'])
    esp = x['esperado'] if boa else x['produto_video']
    esc = x['escolhido']
    sim, raras, veto = P.prova_nome(esp, esc, parcial=not boa)
    if veto:
        print(f'  ! aprovado com VETO: esp={esp[:55]!r} esc={esc[:55]!r} -> {veto}')
    else:
        sem_veto += 1
    if sim >= 0.6 and raras >= 2:
        nome_ok += 1
print(f'[1] aprovados: {len(aprov)} | sem veto: {sem_veto} | com prova de nome sozinha: {nome_ok}')

# ---------- 2) falsos positivos de nome: esperado x TODAS as outras linhas vistas (produto diferente) não pode virar "nome ok"
fp = tot = 0
for x in fb:
    esp = x.get('esperado') or ''
    if len(esp) < 25 or re.match(r'(Compre|Economize|Classificado)', esp):
        esp = x.get('produto_video') or ''
    esc = lim(x.get('escolhido') or '')
    for l in x.get('linhas_vistas', []):
        l = lim(l)
        if not esc and True or P.norm(l)[:25] != P.norm(esc)[:25]:
            # linha diferente da escolhida (ou caso sem escolhida: nenhuma linha é o produto)
            if esc and P.norm(l)[:20] == P.norm(esc)[:20]:
                continue
            tot += 1
            sim, raras, veto = P.prova_nome(esp, l)
            if not veto and sim >= 0.6 and raras >= 2:
                fp += 1
                print(f'  ! FALSO POSITIVO de nome: esp={esp[:50]!r} linha={l[:50]!r} sim={sim:.2f}')
print(f'[2] pares produto-diferente testados: {tot} | falsos positivos de nome: {fp}')

# ---------- 3) perfumes: nenhum perfume pode "casar" com outro perfume diferente
perf = ['Perfume Árabe Lattafa Victoria Eau de Parfum 100ml Original', 'Perfume Árabe Lattafa Pisa Eau de Parfum 100ml Original',
        'Perfume Khamrah Qahwa Lattafa Eau de Parfum 100ml Masculino Importado', 'Perfume Árabe Afeef Lattafa 100ml Eau de Parfum Unissex',
        'Perfume Árabe Hawas Thunder Eau de Parfum 100ml Original', 'Perfume Cherry in the Woods Eau de Parfum 100ml',
        'Perfume Odyssey Mandarin Sky Armaf Eau de Parfum 100ml', 'Perfume Pink Eclipse Maison Alhambra Eau de Parfum 100ml',
        'Perfume Árabe Masculino Al Wataniah Khamrah Qahwa 100ml', 'Perfume Árabe Masculino Lattafa Khamrah Qahwa 50ml', 'Perfume Hawas Thunder Eau de Parfum 50ml Original']
pfp = 0
for a, b in itertools.permutations(range(len(perf)), 2):
    sim, raras, veto = P.prova_nome(perf[a], perf[b])
    if not veto and sim >= 0.6 and raras >= 2:
        pfp += 1
        print(f'  ! PERFUME casou: {perf[a][:50]!r} x {perf[b][:50]!r} sim={sim:.2f}')
mesmo = [P.prova_nome(p, p) for p in perf]
print(f'[3] perfumes: pares diferentes que casariam: {pfp} de {len(perf) * (len(perf) - 1)} | iguais com veto: {sum(1 for m in mesmo if m[2])}')
# ---------- 4) variantes: nomes que começam igual mas são produtos diferentes (cor, modelo "Acqua", tamanho)
todos = set()
for x in fb:
    for k in ('esperado', 'escolhido'):
        if x.get(k) and len(x[k]) > 25:
            todos.add(lim(x[k]))
    todos.update(lim(l) for l in x.get('linhas_vistas', []))
todos = sorted(todos)
var = vfp = 0
for a, b in itertools.combinations(todos, 2):
    na, nb = P.norm(a), P.norm(b)
    if na[:20] == nb[:20] and na != nb and not (na.startswith(nb) or nb.startswith(na)):
        var += 1
        sim, raras, veto = P.prova_nome(a, b)
        if not veto and sim >= 0.6 and raras >= 2:
            vfp += 1
            print(f'  ! VARIANTE casou: {a[:60]!r} x {b[:60]!r} sim={sim:.2f}')
extra = [('Cadeira Escritório Gamer Preta 120kg Reclinável Ergonômica', 'Cadeira Escritório Gamer Rosa 120kg Reclinável Ergonômica'),
         ('Kit 2 Cadeiras Malaga Linho Bege Sala de Jantar Estofada', 'Kit 2 Cadeiras Malaga Linho Cinza Sala de Jantar Estofada'),
         ('Kit 4 Cadeiras Malaga Linho Bege Sala de Jantar', 'Kit 2 Cadeiras Malaga Linho Bege Sala de Jantar'),
         ('Ventilador de Mesa Mallory 30cm 127V Preto Silencioso', 'Ventilador de Mesa Mallory 40cm 127V Preto Silencioso'),
         ('Ventilador de Mesa Mallory 30cm 127V Preto Silencioso', 'Ventilador de Mesa Mallory 30cm 220V Preto Silencioso'),
         ('Kit Vara Carretilha JP PRO 10-25lbs + Carretilha 7', 'Kit Vara Carretilha JP PRO Acqua 10-25lbs + Carretilha 7'),
         ('Parafusadeira e Furadeira STANLEY SBD716B 13mm 20V', 'Parafusadeira e Furadeira STANLEY SCD701B 13mm 20V')]
for a, b in extra:
    var += 1
    sim, raras, veto = P.prova_nome(a, b)
    if not veto and sim >= 0.6 and raras >= 2:
        vfp += 1
        print(f'  ! VARIANTE (sintética) casou: {a[:50]!r} x {b[:50]!r}')
print(f'[4] variantes testadas: {var} | casariam por engano: {vfp}')
print('RESULTADO NOME:', 'OK (0 falsos positivos)' if (fp == 0 and pfp == 0 and vfp == 0 and sem_veto == len(aprov)) else 'REVISAR')
