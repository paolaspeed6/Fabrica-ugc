"""Lote 2026-10-24 A (teste do método do kit: criado do zero com Nano Banana + Seedance, editado nos layouts da dona).
Estilo natural (sem filtro, whip/zoom), sem voz + música calma, cada vídeo abre com um take diferente.
clips = fim do trecho limpo do Fiscal de vídeo (o _segs nunca passa desse ponto). Textos: pNN-textos.json do Fichador (só fatos do anúncio).
Rodar: LUXO_DIR=trabalhos/p65-banquetas-baixas python3 lote_2410.py p65"""
import sys
from produto import *

P = {}
# p65 Kit 2 Banquetas Baixas (lista2410a p01): A = cena B do lote (0–4,8 s limpo; pratos no nicho do fundo depois de 1 s, sem bebida),
# B = cena C do lote (0–5,0 s limpo). A cena A do lote foi descartada pelo Fiscal de imagem.
P['p65'] = dict(id='p65', accent=(205, 118, 58), clips={'A': 4.8, 'B': 5.0}, leve='o seu', tem='*o kit tem:*',
  a=dict(eyebrow='Cozinha e área gourmet', gancho=['Ilha sem banqueta?', '*Agora tem duas.*'],
         momentos=[('Café', 'Assento em corino'), ('Almoço', 'Estrutura em madeira'), ('Jantar', 'Base firme e estável')]),
  b=dict(kicker='Kit 2 Banquetas Baixas', cenas=[('Kit com', '2 banquetas', 'Para cozinha, balcão e ilha'),
                                                ('Assento', 'em corino', 'Estofado e confortável'),
                                                ('Estrutura', 'em madeira', None)]),
  c=dict(eyebrow='Kit 2 Banquetas Baixas', gancho=['Balcão sem lugar', '*pra sentar?*'],
         itens=['Kit com 2 banquetas', 'Assento em corino', 'Estrutura em madeira'], onde=['Cozinha, ilha', '*e área gourmet.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03)], [('B', 0.0, 1.0, 1.03)], [('A', 2.0, 1.0, 1.03)], [('B', 2.2, 1.0, 1.03)],
                 [('A', 0.5, 1.0, 1.02, {'d': 2.1}), ('B', 0.4, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03, {'d': 2.6}), ('A', 2.0, 1.0, 1.03)], [('A', 0.0, 1.0, 1.03, {'d': 2.4}), ('B', 2.4, 1.0, 1.03)],
                 [('B', 0.3, 1.0, 1.02, {'d': 2.4}), ('A', 2.0, 1.03, 1.0)]],
           'c': [[('A', 2.6, 1.0, 1.03, {'d': 1.6}), ('B', 3.0, 1.0, 1.03)], [('B', 0.0, 1.0, 1.03, {'d': 2.9}), ('A', 0.2, 1.0, 1.03)],
                 [('A', 2.0, 1.0, 1.03)], [('B', 3.2, 1.0, 1.02, {'d': 1.6}), ('A', 0.6, 1.03, 1.0)]]})

# p66 Bicicleta Spinning 150 kg (lista2410a p02): A 0–3,0 s (depois a letra do garfo varia), B 0–4,5 s, C 0–2,0 s (brilho verde
# na roda 2,1–2,8 s), D = C de 3,0 a 5,0 s. Suporte de garrafa vazio em todos. Inércia fora dos textos (título 15 kg x descrição 20 kg).
P['p66'] = dict(id='p66', accent=(241, 204, 77), clips={'A': 3.0, 'B': 4.5, 'C': 2.0, 'D': 2.0}, leve='a sua', tem='*ela tem:*',
  a=dict(eyebrow='Treino em casa', gancho=['Academia longe?', '*Pedale em casa.*'],
         momentos=[('Treino', 'Suporta até 150 kg'), ('Ajuste', 'Banco e guidão ajustáveis'), ('Painel', 'Painel digital')]),
  b=dict(kicker='Bicicleta Spinning Profissional', cenas=[('Até', '150 kg', 'Metal, ABS e borracha'),
                                                         ('Painel', 'digital', 'Velocidade, tempo e calorias'),
                                                         ('Banco', 'ajustável', None)]),
  c=dict(eyebrow='Bicicleta Spinning', gancho=['Sem tempo pra', '*academia?*'],
         itens=['Suporta até 150 kg', 'Painel digital', 'Banco e guidão ajustáveis'], onde=['Treino', '*em casa.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03)], [('B', 0.5, 1.0, 1.03)], [('D', 0.0, 1.0, 1.03, {'d': 1.3}), ('C', 0.0, 1.0, 1.03)],
                 [('B', 1.8, 1.0, 1.03)], [('A', 0.6, 1.0, 1.02, {'d': 2.2}), ('D', 0.0, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03, {'d': 2.8}), ('A', 0.6, 1.0, 1.03)], [('C', 0.0, 1.0, 1.03, {'d': 1.9}), ('B', 1.4, 1.0, 1.03)],
                 [('D', 0.0, 1.0, 1.03, {'d': 2.0}), ('A', 0.0, 1.03, 1.0)]],
           'c': [[('C', 0.0, 1.0, 1.03, {'d': 1.95}), ('B', 2.5, 1.0, 1.03)], [('A', 0.0, 1.0, 1.03, {'d': 2.9}), ('B', 0.2, 1.0, 1.03)],
                 [('D', 0.0, 1.0, 1.03, {'d': 1.9}), ('A', 2.0, 1.0, 1.03)], [('B', 3.2, 1.0, 1.02, {'d': 1.2}), ('A', 0.3, 1.03, 1.0)]]})

if __name__ == '__main__':
    for pid in sys.argv[1:]:
        print(fazer_produto(P[pid]))
