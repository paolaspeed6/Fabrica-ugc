"""Opções B e C da cadeira trançada e da poltrona capitonê bege (2026-10-18). Opção A = lux3_umdia em lux.py.
LUXO_DIR=trabalhos/cadeira-poltrona-bege. Narrações: tts2/{cb,pb,cc,pc}_t.wav (gemini-3.1-flash-tts-preview, PREFIXO=1)."""
from novos import *
N = f'{S}/tts2/'
PIANO = ['D', 'F', 'D']
AREIA = (201, 160, 112)
CARAMELO = (208, 164, 116)

opcao_b('cadeira_b_shopee3', dict(kicker='Cadeira trançada', accent=AREIA, cta='Toque no carrinho',
  cenas=[(['O [trançado] que a', 'varanda pedia'], 'Encosto e assento trançados'),
         (['Textura [natural]', 'de pertinho'], 'Linhas retas · visual leve'),
         (['Combina com', '[qualquer canto]'], None)]),
  [seg('A', 0.0, 4.6, (1.0, 1.08)), seg('B', 3.6, 2.4, (1.0, 1.06)), seg('C', 2.4, 2.0, (1.02, 1.08)),
   seg('B', 0.0, 3.0, (1.0, 1.06)), seg('C', 0.0, 3.0, (1.0, 1.06))],
  N + 'cb_t.wav', narr_at=0.4, bed=PIANO, cuts=(0, 4.6, 9.0, 15))

opcao_b('poltrona_b_shopee3', dict(kicker='Poltrona capitonê', accent=CARAMELO, cta='Toque no carrinho',
  cenas=[(['A poltrona que deixa', 'a sala [pronta]'], 'Encosto capitonê · visual aveludado'),
         (['Capitonê que', '[valoriza] o ambiente'], 'Pés escuros de linha clássica'),
         (['Sala, quarto', 'ou [leitura]'], None)]),
  [seg('D', 0.0, 2.8, (1.0, 1.14)), seg('E', 3.2, 2.2, (1.0, 1.12)), seg('D', 3.0, 2.5, (1.6, 1.7), c0=(360, 700)), seg('E', 0.0, 2.5, (1.45, 1.5), c0=(400, 820)),
   seg('F', 1.0, 5.0, (1.0, 1.07))],
  N + 'pb_t.wav', narr_at=0.4, bed=PIANO, tempo=1.04)

opcao_c('cadeira_c_revista', dict(edicao='Edição nº 07 · A peça do mês', gancho=['A peça do mês', '*é trançada.*'],
  notas=[('01', 'Trançado *no encosto.*'), ('02', 'Linhas *retas.*'), ('03', 'Da varanda *à sala.*')],
  cta=['Leve essa peça', '*pra casa.*']),
  [seg('A', 0.0, 4.6, (1.0, 1.07)), seg('C', 0.0, 2.7, (1.0, 1.06)), seg('B', 0.5, 2.6, (1.0, 1.05)),
   seg('A', 2.4, 2.1, (1.0, 1.04)), seg('A', 0.6, 3.0, (1.06, 1.0))],
  N + 'cc_t.wav', narr_at=0.5, bed=PIANO, tempo=1.06)

opcao_c('poltrona_c_revista', dict(edicao='Edição nº 08 · A peça do mês', gancho=['O conforto', '*virou tendência.*'],
  notas=[('01', 'Encosto *capitonê.*'), ('02', 'Visual *aveludado.*'), ('03', 'Pés de *linha clássica.*')],
  cta=['Leve essa peça', '*pra casa.*']),
  [seg('E', 0.0, 4.6, (1.0, 1.07)), seg('D', 0.0, 2.7, (1.0, 1.06)), seg('F', 0.0, 2.6, (1.0, 1.06)),
   seg('E', 3.0, 2.1, (1.05, 1.1)), seg('D', 2.5, 3.0, (1.0, 1.06))],
  N + 'pc_t.wav', narr_at=0.6, bed=PIANO)

# opção C nova "Direto ao ponto" (a Revista não convenceu a dona: quer persuasivo e fácil para o público leigo)
opcao_d('cadeira_c_direto', dict(eyebrow='Para a sua varanda', gancho=['Falta *uma peça*', 'na sua varanda.'],
  itens=['Encosto trançado', 'Assento trançado', 'Linhas retas'], onde=['Varanda, sala', '*ou leitura.*'], accent=AREIA),
  [seg('A', 0.0, 2.8, (1.0, 1.08)), seg('C', 0.0, 3.0, (1.0, 1.07)), seg('B', 0.0, 3.1, (1.0, 1.06)),
   seg('A', 2.4, 2.1, (1.0, 1.05)), seg('A', 0.6, 4.0, (1.08, 1.0))],
  N + 'cd_t.wav', narr_at=0.3, bed=PIANO, cuts=(0, 2.8, 8.9, 11.0, 15))

opcao_d('poltrona_c_direto', dict(eyebrow='Para a sua sala', gancho=['Sua sala merece', '*mais conforto.*'],
  itens=['Encosto capitonê', 'Visual aveludado', 'Pés clássicos'], onde=['Sala, quarto', '*ou leitura.*'], accent=CARAMELO),
  [seg('D', 0.0, 3.3, (1.0, 1.12)), seg('E', 0.0, 3.0, (1.0, 1.08)), seg('F', 0.0, 2.9, (1.0, 1.08)),
   seg('E', 3.0, 2.65, (1.04, 1.12)), seg('D', 2.2, 3.15, (1.12, 1.0))],
  N + 'pd_t.wav', narr_at=0.3, bed=PIANO, cuts=(0, 3.3, 9.2, 11.85, 15))
