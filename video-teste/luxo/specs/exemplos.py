"""Exemplos JPEG para a dona escolher (2026-10-18): opção C com fonte nova + candidatas da opção 2. Poltrona."""
from novos import *
N = f'{S}/tts2/'
CARAMELO = (208, 164, 116)
B_TEXTOS = dict(kicker='Poltrona capitonê', accent=CARAMELO, cta='Toque no carrinho',
  cenas=[('A poltrona que deixa', 'a sala pronta', 'Encosto capitonê · visual aveludado'),
         ('Capitonê que', 'valoriza o ambiente', 'Pés escuros de linha clássica'),
         ('Sala, quarto', 'ou leitura', None)])
SEG_B = [seg('F', 0.0, 2.8, (1.0, 1.12)), seg('E', 3.2, 2.2, (1.0, 1.12)), seg('D', 3.0, 2.5, (1.6, 1.7), c0=(360, 700)),
         seg('E', 0.0, 2.5, (1.45, 1.5), c0=(400, 820)), seg('D', 0.0, 5.0, (1.0, 1.07))]
opcao_b_faixas('ex_2a_faixas', B_TEXTOS, SEG_B, N + 'pb_t.wav')
opcao_b_topo('ex_2b_topo', B_TEXTOS, SEG_B, N + 'pb_t.wav')
D_TEXTOS = dict(eyebrow='Para a sua sala', gancho=['Sua sala merece', '*mais conforto.*'],
  itens=['Encosto capitonê', 'Visual aveludado', 'Pés clássicos'], onde=['Sala, quarto', '*ou leitura.*'], accent=CARAMELO)
SEG_D = [seg('E', 0.0, 3.3, (1.0, 1.12)), seg('D', 0.0, 3.0, (1.0, 1.08)), seg('F', 0.0, 2.9, (1.0, 1.08)),
         seg('E', 3.0, 2.65, (1.04, 1.12)), seg('D', 2.2, 3.15, (1.12, 1.0))]
opcao_d('ex_3_dmsans', D_TEXTOS, SEG_D, N + 'pd_t.wav', cuts=(0, 3.3, 9.2, 11.85, 15), fonte='dm')
opcao_d('ex_3_montserrat', D_TEXTOS, SEG_D, N + 'pd_t.wav', cuts=(0, 3.3, 9.2, 11.85, 15), fonte='mont')
