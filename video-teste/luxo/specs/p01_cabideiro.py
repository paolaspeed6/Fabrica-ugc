"""Cabideiro de madeira (2026-10-18): 3 opções do padrão. Cenas: A entrada (aparador + espelho), B quarto,
C sala (MÃO até 2,4 s: usar só depois de 2,6 s). Produto alto e central -> shiftx 250 e texto à esquerda."""
from novos import *
N = f'{S}/tts/'
TRILHA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trilha_piano.wav')
MEL = (196, 132, 82)  # tom da madeira
opcao_a('p01_a_umdia', dict(eyebrow='Das 7h às 22h', gancho=['Um dia inteiro', '*organizado.*'], shiftx=310,
  momentos=[('07:30', 'Na saída'), ('15:00', 'Na sala'), ('22:00', 'No quarto')]),
  [seg('A', 0.0, 2.85, (1.0, 1.06)), seg('A', 3.0, 2.25, (1.0, 1.05)), seg('C', 2.6, 2.05, (1.0, 1.05)),
   seg('B', 0.0, 2.35, (1.0, 1.06)), seg('B', 2.4, 3.0, (1.0, 1.05)), seg('A', 5.0, 2.5, (1.04, 1.0))],
  N + 'a_t.wav', narr_at=0.4, bed=[TRILHA], cuts=(0, 2.85, 5.1, 7.15, 9.5))
opcao_b_faixas('p01_b_faixas', dict(kicker='Cabideiro de madeira', accent=MEL, cta='Toque no carrinho', shiftx=310, lift=0,
  cenas=[('Chega de casaco', 'jogado na cadeira', 'Casacos, bolsas e chapéus'),
         ('Ganchos em', 'vários níveis', 'Madeira torneada'),
         ('Entrada, sala', 'ou quarto', None)]),
  [seg('B', 0.0, 5.0, (1.0, 1.08)), seg('A', 4.0, 3.3, (1.0, 1.06)), seg('C', 3.0, 3.5, (1.0, 1.05)), seg('A', 0.5, 3.2, (1.0, 1.05))],
  N + 'b_t.wav', narr_at=0.4, bed=[TRILHA], cuts=(0, 5.0, 8.3, 15))
opcao_d('p01_c_direto', dict(eyebrow='Para a sua entrada', gancho=['Falta *um lugar*', 'para os casacos.'], tem='*ele tem:*',
  itens=['Ganchos em vários níveis', 'Madeira torneada', 'Ocupa pouco espaço'], itens_t=[3.45, 4.7, 5.6],
  onde=['Entrada, sala', '*ou quarto.*'], accent=MEL, shiftx=310, esq=True, item_size=44, escala=0.74),
  [seg('C', 0.0, 0.7, (1.0, 1.02), shiftx=40), seg('C', 2.6, 1.8, (1.0, 1.06), shiftx=330), seg('B', 0.0, 2.0, (1.0, 1.02)), seg('A', 0.0, 1.95, (1.0, 1.02)),
   seg('C', 6.0, 1.85, (1.0, 1.04), shiftx=120), seg('A', 1.3, 6.7, (1.05, 1.0))],
  N + 'c_t.wav', narr_at=0.35, bed=[TRILHA], cuts=(0, 2.5, 6.45, 8.3, 15))
