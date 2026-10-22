"""Lote 2026-10-21 (estilo novo da dona): sem gancho de horas, sem filtro (natural), transições whip/zoom,
cada vídeo abre com um take diferente. Rodar: LUXO_DIR=... python3 lote_1021.py p24
Anúncios da Shopee não abrem sem login (não automatizamos login): textos só com o que os takes mostram."""
import sys
from produto import *


def trio(X, Y, Z):
    """3 takes limpos: A abre com X, B com Y, C com Z."""
    return {'a': [[(X, 0.0, 1.0, 1.03)], [(Y, 2.0, 1.0, 1.03)], [(Z, 2.5, 1.0, 1.03)], [(X, 3.0, 1.0, 1.03)],
                  [(Y, 3.6, 1.0, 1.02, {'d': 2.0}), (Z, 0.5, 1.03, 1.0)]],
            'b': [[(Y, 0.0, 1.0, 1.03)], [(Z, 1.0, 1.0, 1.03, {'d': 2.5}), (X, 3.2, 1.0, 1.03)],
                  [(Y, 3.4, 1.0, 1.02, {'d': 2.4}), (X, 0.6, 1.03, 1.0)]],
            'c': [[(Z, 0.0, 1.0, 1.03)], [(X, 1.5, 1.0, 1.03, {'d': 2.9}), (Y, 1.0, 1.0, 1.03)], [(Z, 3.2, 1.0, 1.03)],
                  [(X, 4.4, 1.0, 1.02, {'d': 1.5}), (Y, 4.0, 1.03, 1.0)]]}


def duo(X, Y):
    """2 takes: A abre com X, B com Y, C com X mais adiante (produto ainda inteiro)."""
    return {'a': [[(X, 0.0, 1.0, 1.03)], [(Y, 1.0, 1.0, 1.03)], [(X, 3.0, 1.0, 1.03)], [(Y, 3.2, 1.0, 1.03)],
                  [(X, 1.2, 1.0, 1.02, {'d': 2.0}), (Y, 0.3, 1.03, 1.0)]],
            'b': [[(Y, 0.0, 1.0, 1.03)], [(X, 0.5, 1.0, 1.03, {'d': 2.6}), (Y, 3.0, 1.0, 1.03)],
                  [(X, 3.4, 1.0, 1.02, {'d': 2.4}), (Y, 1.5, 1.03, 1.0)]],
            'c': [[(X, 2.0, 1.0, 1.03)], [(Y, 0.4, 1.0, 1.03, {'d': 2.9}), (X, 0.3, 1.0, 1.03)], [(Y, 2.8, 1.0, 1.03)],
                  [(X, 4.0, 1.0, 1.02, {'d': 1.6}), (Y, 1.2, 1.03, 1.0)]]}


P = {}
# p24 motosserra Toyama: C tem mão 0,55–2,5 s; D tem mão 0,55–2,5 e logo distorcido pela IA (TOYAIMA) a partir de 3 s -> D só 0–0,55
P['p24'] = dict(id='p24', accent=(205, 45, 45), clips={'A': 6.0, 'B': 6.0, 'C': 6.0, 'D': 6.0}, leve='a sua',
  a=dict(eyebrow='Para quem tem sítio', gancho=['Lenha cortada', '*sem sofrimento.*'],
         momentos=[('Lenha', 'Para o fogão e a lareira'), ('Poda', 'Galhos grandes do quintal'), ('Sítio', 'O trabalho pesado do dia')]),
  b=dict(kicker='Motosserra Toyama', cenas=[('Chega de', 'machado', 'Corte de lenha e poda'),
                                           ('Sabre com', 'corrente', 'Empunhadura dupla'),
                                           ('Lenha, poda', 'e sítio', None)]),
  c=dict(eyebrow='Motosserra Toyama', gancho=['Cortando lenha', '*no machado?*'],
         itens=['Marca Toyama', 'Sabre com corrente', 'Empunhadura dupla'], onde=['Lenha, poda', '*e sítio.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03)], [('B', 2.5, 1.0, 1.03)], [('C', 3.4, 1.0, 1.03)], [('A', 3.0, 1.0, 1.03)],
                 [('B', 0.3, 1.0, 1.02, {'d': 2.2}), ('A', 1.0, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03)], [('A', 1.5, 1.0, 1.03, {'d': 2.5}), ('C', 3.4, 1.0, 1.03)],
                 [('A', 3.5, 1.0, 1.02, {'d': 2.0}), ('B', 3.0, 1.03, 1.0)]],
           'c': [[('D', 0.0, 1.0, 1.02, {'d': 0.55}), ('C', 3.4, 1.0, 1.03)], [('B', 1.5, 1.0, 1.03, {'d': 3.0}), ('A', 2.5, 1.0, 1.03)],
                 [('C', 3.3, 1.0, 1.03)], [('A', 4.2, 1.0, 1.02, {'d': 1.6}), ('B', 0.5, 1.03, 1.0)]]})

# p25 toalheiro elétrico: a mão sentindo o calor faz parte (realista), nunca no 1º quadro
P['p25'] = dict(id='p25', accent=(70, 115, 195), scrim=0.62, clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Banheiro de hotel', gancho=['Toalha quentinha', '*todo dia.*'],
         momentos=[('Banho', 'Toalha quentinha na hora'), ('Parede', 'Fica fixo e ocupa pouco'), ('Tomada', 'É só ligar e usar')]),
  b=dict(kicker='Toalheiro elétrico', cenas=[('Toalha', 'quentinha', 'Aquece as toalhas'),
                                            ('Várias', 'barras', 'Toalha de banho e de rosto'),
                                            ('Banheiro', 'de hotel', None)]),
  c=dict(eyebrow='Toalheiro elétrico', gancho=['Toalha fria', '*depois do banho?*'],
         itens=['Aquece as toalhas', 'Várias barras', 'Fica na parede'], onde=['No seu banheiro,', '*todo dia.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.02)], [('C', 2.0, 1.0, 1.03)], [('B', 2.5, 1.0, 1.02)], [('C', 3.4, 1.0, 1.02)],
                 [('A', 3.6, 1.0, 1.02, {'d': 2.2}), ('C', 1.6, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.02)], [('C', 1.6, 1.0, 1.03, {'d': 2.6}), ('A', 2.4, 1.0, 1.02)],
                 [('C', 3.6, 1.0, 1.02, {'d': 2.2}), ('B', 3.0, 1.02, 1.0)]],
           'c': [[('C', 0.0, 1.0, 1.02, {'d': 1.2}), ('A', 0.6, 1.0, 1.02)], [('B', 1.0, 1.0, 1.02, {'d': 2.9}), ('C', 2.0, 1.0, 1.03)],
                 [('A', 3.2, 1.0, 1.02)], [('C', 4.2, 1.0, 1.02, {'d': 1.6}), ('B', 4.0, 1.02, 1.0)]]})

# p26 chinelos (branco, preto, rosa) com tira transparente
P['p26'] = dict(id='p26', accent=(225, 110, 170), clips={'A': 6.0, 'B': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Achado de verão', gancho=['Um par pra cada', '*momento.*'],
         momentos=[('Casa', 'Para ficar à vontade'), ('Piscina', 'Para o dia de sol'), ('Dia a dia', 'Combina com tudo')]),
  b=dict(kicker='Chinelo tira transparente', cenas=[('Branco, preto', 'ou rosa', 'Escolha a sua cor'),
                                                   ('Tira', 'transparente', 'Visual delicado'),
                                                   ('Piscina, casa', 'e passeio', None)]),
  c=dict(eyebrow='Chinelo de verão', gancho=['Qual cor', '*é a sua?*'],
         itens=['Tira transparente', 'Branco, preto e rosa', 'Visual delicado'], onde=['Piscina, casa', '*e passeio.*']),
  tomadas=duo('A', 'B'))

# p27 lavadora de alta pressão Eletroplas
P['p27'] = dict(id='p27', accent=(235, 120, 30), clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='a sua',
  a=dict(eyebrow='Para quem lava pesado', gancho=['Sujeira grossa?', '*Resolve aqui.*'],
         momentos=[('Quintal', 'Piso e calçada'), ('Carro', 'Lavagem completa'), ('Garagem', 'Limpeza pesada')]),
  b=dict(kicker='Lavadora Eletroplas', cenas=[('Lavadora de', 'alta pressão', 'Com carrinho e rodas'),
                                             ('Mangueira', 'no suporte', 'Fica tudo junto'),
                                             ('Quintal, carro', 'e garagem', None)]),
  c=dict(eyebrow='Lavadora Eletroplas', gancho=['Lavando o quintal', '*no balde?*'],
         itens=['Alta pressão', 'Carrinho com rodas', 'Mangueira no suporte'], onde=['Quintal, carro', '*e garagem.*']),
  tomadas=trio('A', 'B', 'C'))

# p28 cortador de piso (A: marca d'água do Hailuo cortada fora)
P['p28'] = dict(id='p28', accent=(230, 110, 30), clips={'A': 5.875, 'B': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para a sua obra', gancho=['Corte de piso', '*sem complicação.*'],
         momentos=[('Piso', 'Pisos e revestimentos'), ('Obra', 'Do começo ao acabamento'), ('Reforma', 'Faça você mesmo')]),
  b=dict(kicker='Cortador de piso', cenas=[('Corte', 'reto', 'Guia longa de metal'),
                                          ('Base', 'larga', 'Pés de apoio no chão'),
                                          ('Obra e', 'reforma', None)]),
  c=dict(eyebrow='Cortador de piso', gancho=['Vai reformar', '*a casa?*'],
         itens=['Guia longa de metal', 'Base larga de apoio', 'Alavanca de corte'], onde=['Obra e', '*reforma.*']),
  tomadas=duo('A', 'B'))

# p29 cortador de grama Tramontina
P['p29'] = dict(id='p29', accent=(235, 120, 25), clips={'A': 6.0, 'B': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para o seu jardim', gancho=['Grama alta?', '*Não mais.*'],
         momentos=[('Jardim', 'Grama sempre aparada'), ('Quintal', 'Quatro rodas'), ('Sábado', 'Jardim em ordem')]),
  b=dict(kicker='Cortador Tramontina', cenas=[('Grama', 'aparada', 'Jardim sempre bonito'),
                                             ('Quatro', 'rodas', 'Desliza pelo gramado'),
                                             ('Jardim e', 'quintal', None)]),
  c=dict(eyebrow='Cortador de grama', gancho=['Grama alta', '*no quintal?*'],
         itens=['Marca Tramontina', 'Quatro rodas', 'Cabo para empurrar'], onde=['Jardim e', '*quintal.*']),
  tomadas=duo('A', 'B'))

# p30 espreguiçadeira: A tem COPO com bebida na mesinha até ~4,6 s -> só A 4,7–6 (regra: nada de bebida/copo)
P['p30'] = dict(id='p30', accent=(196, 170, 130), clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='a sua',
  a=dict(eyebrow='Para a área externa', gancho=['Clima de', '*hotel em casa.*'],
         momentos=[('Jardim', 'Para ler e relaxar'), ('Piscina', 'Para tomar sol'), ('Varanda', 'Para descansar')]),
  b=dict(kicker='Espreguiçadeira', cenas=[('Clima de', 'hotel', 'Na beira da piscina'),
                                         ('Tela', 'clara', 'Estrutura preta'),
                                         ('Piscina, varanda', 'e jardim', None)]),
  c=dict(eyebrow='Espreguiçadeira', gancho=['Falta um lugar', '*pra relaxar?*'],
         itens=['Tela clara', 'Estrutura preta', 'Braços laterais'], onde=['Piscina, varanda', '*e jardim.*']),
  tomadas={'a': [[('B', 0.0, 1.0, 1.03)], [('C', 1.5, 1.0, 1.03)], [('A', 4.7, 1.0, 1.02, {'d': 1.25}), ('B', 3.5, 1.0, 1.02)],
                 [('B', 2.2, 1.0, 1.02)], [('C', 3.4, 1.0, 1.02, {'d': 2.0}), ('B', 0.3, 1.03, 1.0)]],
           'b': [[('C', 0.0, 1.0, 1.03)], [('B', 1.0, 1.0, 1.03, {'d': 2.6}), ('A', 4.7, 1.0, 1.02, {'d': 1.25}), ('C', 3.0, 1.0, 1.02)],
                 [('B', 3.4, 1.0, 1.02, {'d': 2.4}), ('C', 1.0, 1.03, 1.0)]],
           'c': [[('B', 2.5, 1.0, 1.03)], [('C', 0.5, 1.0, 1.03, {'d': 2.9}), ('B', 0.2, 1.0, 1.03)],
                 [('A', 4.7, 1.0, 1.02, {'d': 1.25}), ('C', 4.6, 1.0, 1.02)], [('C', 2.0, 1.0, 1.02, {'d': 1.6}), ('B', 4.0, 1.03, 1.0)]]})

# p31 gravador de vídeo (DVR) AGL: A/B/C sem a marca do Hailuo (cortada); E tem mão 1,2–4,8 s
P['p31'] = dict(id='p31', accent=(40, 110, 200), clips={'A': 5.875, 'B': 5.875, 'C': 5.875, 'D': 6.0, 'E': 6.0}, leve='o seu',
  tem='*ele tem:*',
  a=dict(eyebrow='Segurança em casa', gancho=['Sua casa', '*sempre de olho.*'],
         momentos=[('Casa', 'Câmeras no monitor'), ('Loja', 'Tudo gravado'), ('Escritório', 'Imagens na tela')]),
  b=dict(kicker='Gravador de vídeo AGL', cenas=[('Grave as', 'câmeras', 'Imagens no monitor'),
                                               ('Várias', 'entradas', 'Na parte de trás'),
                                               ('Casa, loja', 'e escritório', None)]),
  c=dict(eyebrow='Gravador de vídeo AGL', gancho=['Câmeras em casa?', '*Veja tudo.*'],
         itens=['Marca AGL', 'Várias entradas', 'Liga no monitor'], onde=['Casa, loja', '*e escritório.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.04)], [('B', 1.0, 1.0, 1.04)], [('D', 1.0, 1.0, 1.03)], [('C', 2.5, 1.0, 1.04)],
                 [('E', 4.9, 1.0, 1.02, {'d': 1.0}), ('A', 2.0, 1.04, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.12, {'d': 1.7}), ('D', 3.0, 1.0, 1.04, {'d': 1.6}), ('A', 1.0, 1.0, 1.08)], [('D', 2.5, 1.0, 1.03, {'d': 2.5}), ('A', 2.5, 1.0, 1.04)],
                 [('E', 0.0, 1.0, 1.02, {'d': 1.1}), ('C', 1.0, 1.04, 1.0)]],
           'c': [[('D', 0.0, 1.0, 1.03)], [('C', 0.2, 1.0, 1.04, {'d': 2.9}), ('E', 4.85, 1.0, 1.02, {'d': 1.0}), ('A', 3.0, 1.0, 1.04)],
                 [('B', 3.0, 1.0, 1.04)], [('D', 4.2, 1.0, 1.02, {'d': 1.6}), ('A', 0.5, 1.04, 1.0)]]})

# p32 kit microfone sem fio: A tem mão 1,1–4,0 s; C/D sem a marca do Hailuo
P['p32'] = dict(id='p32', accent=(210, 175, 90), clips={'A': 6.0, 'B': 6.0, 'C': 5.875, 'D': 5.875}, leve='o seu', tem='*o kit tem:*',
  a=dict(eyebrow='Para a sua festa', gancho=['Chega de fio', '*no palco.*'],
         momentos=[('Festa', 'Karaokê com a família'), ('Igreja', 'Louvor e eventos'), ('Estúdio', 'Gravação e live')]),
  b=dict(kicker='Microfone sem fio', cenas=[('Kit com', '2 microfones', 'E o receptor'),
                                           ('Sem', 'fio', 'Liberdade para cantar'),
                                           ('Festa, igreja', 'e estúdio', None)]),
  c=dict(eyebrow='Microfone sem fio', gancho=['Tropeçando', '*no fio?*'],
         itens=['2 microfones', 'Receptor com antenas', 'Sem fio'], onde=['Festa, igreja', '*e estúdio.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03, {'d': 1.05}), ('A', 4.1, 1.0, 1.03)], [('B', 1.0, 1.0, 1.03)], [('C', 2.0, 1.0, 1.03)],
                 [('B', 3.4, 1.0, 1.03)], [('D', 3.5, 1.0, 1.02, {'d': 2.2}), ('A', 4.3, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03)], [('C', 1.0, 1.0, 1.03, {'d': 2.5}), ('A', 4.1, 1.0, 1.03)],
                 [('D', 2.0, 1.0, 1.02, {'d': 2.4}), ('B', 2.0, 1.03, 1.0)]],
           'c': [[('C', 0.0, 1.0, 1.03)], [('B', 1.5, 1.0, 1.03, {'d': 2.9}), ('D', 0.5, 1.0, 1.03)], [('D', 3.0, 1.0, 1.03)],
                 [('B', 4.0, 1.0, 1.02, {'d': 1.6}), ('C', 3.5, 1.03, 1.0)]]})

# p33 ventilador (sem a marca do Hailuo)
P['p33'] = dict(id='p33', accent=(90, 150, 210), clips={'A': 5.875, 'B': 5.875, 'C': 5.875}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para dias quentes', gancho=['Calor no', '*galpão?*'],
         momentos=[('Galpão', 'Ar circulando'), ('Oficina', 'Ambiente mais fresco'), ('Garagem', 'Para o dia todo')]),
  b=dict(kicker='Ventilador', cenas=[('Ar', 'circulando', 'Grade de proteção'),
                                    ('Hélice', 'larga', 'Corpo preto'),
                                    ('Galpão, oficina', 'e garagem', None)]),
  c=dict(eyebrow='Ventilador', gancho=['Calor no', '*trabalho?*'],
         itens=['Grade de proteção', 'Hélice larga', 'Corpo preto'], onde=['Galpão, oficina', '*e garagem.*']),
  tomadas=trio('A', 'B', 'C'))

# p34 kit esmerilhadeira + chave de impacto: B tem mão mostrando o kit a partir de 0,6 s (realista, nunca no 1º quadro)
P['p34'] = dict(id='p34', accent=(240, 190, 20), clips={'A': 6.0, 'B': 6.0}, leve='o seu', tem='*o kit tem:*',
  a=dict(eyebrow='Para a sua oficina', gancho=['Duas ferramentas,', '*uma maleta.*'],
         momentos=[('Obra', 'Corte e desbaste'), ('Oficina', 'Aperto de porcas'), ('Casa', 'Reparos do dia a dia')]),
  b=dict(kicker='Kit sem fio', cenas=[('Esmerilhadeira', 'e chave de impacto', 'Com baterias e carregador'),
                                     ('Tudo na', 'maleta', 'Fácil de guardar'),
                                     ('Obra, oficina', 'e casa', None)]),
  c=dict(eyebrow='Kit sem fio', gancho=['Ainda preso', '*na tomada?*'],
         itens=['Esmerilhadeira', 'Chave de impacto', 'Maleta com baterias'], onde=['Obra, oficina', '*e casa.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.04)], [('B', 3.4, 1.0, 1.02)], [('A', 3.0, 1.0, 1.04)], [('B', 2.5, 1.0, 1.02)],
                 [('A', 1.0, 1.0, 1.03, {'d': 2.2}), ('B', 3.5, 1.02, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.02, {'d': 1.3}), ('A', 1.0, 1.0, 1.04)], [('B', 3.0, 1.0, 1.02, {'d': 2.5}), ('A', 3.0, 1.0, 1.04)],
                 [('B', 4.0, 1.0, 1.02, {'d': 1.95}), ('A', 0.5, 1.04, 1.0)]],
           'c': [[('A', 2.5, 1.04, 1.08)], [('B', 2.8, 1.0, 1.02, {'d': 2.9}), ('A', 0.5, 1.0, 1.04)], [('B', 3.3, 1.0, 1.02)],
                 [('A', 4.0, 1.0, 1.03, {'d': 1.6}), ('B', 4.1, 1.02, 1.0)]]})

# p35 manifold digital: B tem mão a partir de 1,3 s
P['p35'] = dict(id='p35', accent=(40, 120, 220), clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para o técnico', gancho=['Medição', '*sem adivinhação.*'],
         momentos=[('Instalação', 'Ar-condicionado'), ('Carga', 'Leitura na tela'), ('Manutenção', 'Mangueiras coloridas')]),
  b=dict(kicker='Manifold digital', cenas=[('Leitura', 'na tela', 'Display digital'),
                                          ('Mangueiras', 'coloridas', 'Azul, vermelha e amarela'),
                                          ('Ar-condicionado', 'e refrigeração', None)]),
  c=dict(eyebrow='Manifold digital', gancho=['Leitura difícil', '*no ponteiro?*'],
         itens=['Display digital', 'Mangueiras coloridas', 'Vem na caixa'], onde=['Ar-condicionado', '*e refrigeração.*']),
  tomadas=trio('A', 'B', 'C'))

# p36 perfurador de solo (sem a marca do Hailuo)
P['p36'] = dict(id='p36', accent=(240, 110, 30), clips={'A': 5.875, 'B': 5.875}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para o seu sítio', gancho=['Buraco pra cerca', '*sem cavadeira.*'],
         momentos=[('Cerca', 'Buraco para mourão'), ('Plantio', 'Covas para mudas'), ('Sítio', 'Trabalho mais rápido')]),
  b=dict(kicker='Perfurador de solo', cenas=[('Chega de', 'cavadeira', 'Broca em espiral'),
                                            ('Cerca e', 'plantio', 'Buracos no chão'),
                                            ('Sítio, chácara', 'e fazenda', None)]),
  c=dict(eyebrow='Perfurador de solo', gancho=['Ainda furando', '*na cavadeira?*'],
         itens=['Broca em espiral', 'Motor portátil', 'Duas alças'], onde=['Cerca e', '*plantio.*']),
  tomadas=duo('A', 'B'))

# p37 pneu XBRI Brutus T/A: A tem mão 0,55–2,0 s
P['p37'] = dict(id='p37', accent=(240, 170, 40), clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para a sua picape', gancho=['Pneu careca?', '*Hora de trocar.*'],
         momentos=[('Cidade', 'No asfalto do dia a dia'), ('Estrada', 'Para pegar a estrada'), ('Terra', 'Para estrada de chão')]),
  b=dict(kicker='Pneu XBRI Brutus T/A', cenas=[('Letras', 'brancas', 'Visual off-road'),
                                              ('Cravos', 'largos', 'Para asfalto e terra'),
                                              ('Asfalto', 'e terra', None)]),
  c=dict(eyebrow='Pneu XBRI Brutus', gancho=['Pneu careca', '*no seu carro?*'],
         itens=['Letras brancas', 'Cravos largos', 'Asfalto e terra'], onde=['Cidade, estrada', '*e terra.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03, {'d': 0.5}), ('A', 2.1, 1.0, 1.03)], [('B', 2.0, 1.0, 1.03)], [('C', 2.5, 1.0, 1.03)],
                 [('B', 3.4, 1.0, 1.03)], [('C', 3.6, 1.0, 1.02, {'d': 2.0}), ('A', 3.5, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03)], [('C', 1.0, 1.0, 1.03, {'d': 2.5}), ('A', 3.2, 1.0, 1.03)],
                 [('B', 3.4, 1.0, 1.02, {'d': 2.4}), ('A', 2.1, 1.03, 1.0)]],
           'c': [[('C', 0.0, 1.0, 1.03)], [('A', 2.2, 1.0, 1.03, {'d': 2.9}), ('B', 1.0, 1.0, 1.03)], [('C', 3.2, 1.0, 1.03)],
                 [('A', 4.4, 1.0, 1.02, {'d': 1.5}), ('B', 4.0, 1.03, 1.0)]]})

# p38 petisco Dreamies sabor carne: A tem mão segurando o pacote a partir de ~1,9 s; B quase parado (zoom 1,1)
P['p38'] = dict(id='p38', accent=(215, 35, 45), clips={'A': 6.0, 'B': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para o seu gato', gancho=['Hora do', '*petisco.*'],
         momentos=[('Mimo', 'Um agrado no dia'), ('Treino', 'Recompensa na hora'), ('Carinho', 'Hora de agradar')]),
  b=dict(kicker='Petisco Dreamies', cenas=[('Sabor', 'carne', 'Petisco para gatos'),
                                          ('Pacote', 'prático', 'Fácil de guardar'),
                                          ('Mimo pro', 'seu gato', None)]),
  c=dict(eyebrow='Petisco para gatos', gancho=['Seu gato', '*merece um mimo?*'],
         itens=['Marca Dreamies', 'Sabor carne', 'Pacote prático'], onde=['Um mimo', '*todo dia.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.04)], [('B', 0.5, 1.0, 1.1)], [('A', 3.0, 1.0, 1.03)], [('B', 3.0, 1.0, 1.1)],
                 [('A', 4.0, 1.0, 1.02, {'d': 1.95}), ('B', 1.5, 1.1, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.12, {'d': 2.5}), ('A', 3.5, 1.0, 1.04)], [('A', 0.5, 1.0, 1.04, {'d': 2.6}), ('B', 3.0, 1.0, 1.1)],
                 [('A', 3.4, 1.0, 1.02, {'d': 2.4}), ('B', 1.5, 1.1, 1.0)]],
           'c': [[('A', 1.0, 1.0, 1.05, {'d': 0.9}), ('B', 2.0, 1.0, 1.1)], [('A', 2.0, 1.0, 1.03, {'d': 2.9}), ('B', 0.4, 1.0, 1.1)],
                 [('A', 3.5, 1.0, 1.03)], [('B', 4.0, 1.1, 1.0, {'d': 1.6}), ('A', 4.2, 1.03, 1.0)]]})

# p39 tela de sombreamento: a dona pediu que a tela dobrada na bancada (take C) SEMPRE abra os 3 vídeos
P['p39'] = dict(id='p39', accent=(90, 140, 70), clips={'A': 8.0, 'B': 8.0, 'C': 6.0}, leve='a sua', tem='*ela tem:*',
  a=dict(eyebrow='Para a sua horta', gancho=['Sol forte', '*na horta?*'],
         momentos=[('Horta', 'Proteção do sol forte'), ('Canteiro', 'Sombra para as mudas'), ('Viveiro', 'Plantas mais protegidas')]),
  b=dict(kicker='Tela de sombreamento', cenas=[('Sombra', 'na horta', 'Protege do sol forte'),
                                              ('Tela', 'preta', 'Cobre canteiros'),
                                              ('Horta, viveiro', 'e jardim', None)]),
  c=dict(eyebrow='Tela de sombreamento', gancho=['Sol queimando', '*suas plantas?*'],
         itens=['Sombra na horta', 'Tela preta', 'Vem dobrada'], onde=['Horta, viveiro', '*e jardim.*']),
  tomadas={'a': [[('C', 0.0, 1.0, 1.03)], [('A', 2.0, 1.0, 1.03)], [('B', 2.5, 1.0, 1.03)], [('A', 5.0, 1.0, 1.03)],
                 [('B', 5.0, 1.0, 1.02, {'d': 2.2}), ('C', 3.0, 1.03, 1.0)]],
           'b': [[('C', 1.5, 1.0, 1.04, {'d': 2.5}), ('A', 0.5, 1.0, 1.03)], [('B', 1.0, 1.0, 1.03, {'d': 2.5}), ('A', 4.0, 1.0, 1.03)],
                 [('C', 3.6, 1.0, 1.02, {'d': 2.0}), ('B', 5.0, 1.03, 1.0)]],
           'c': [[('C', 3.0, 1.0, 1.04, {'d': 1.6}), ('A', 0.0, 1.0, 1.03)], [('B', 2.0, 1.0, 1.03, {'d': 2.9}), ('A', 3.0, 1.0, 1.03)],
                 [('B', 5.0, 1.0, 1.03)], [('A', 6.0, 1.0, 1.02, {'d': 1.6}), ('C', 4.2, 1.03, 1.0)]]})

# p40 tubo de cobre com isolamento: B tem mão 1,5–4,0 s; a dona: "só os melhores momentos" (closes dos rolos)
P['p40'] = dict(id='p40', accent=(200, 110, 60), clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='o seu', tem='*o kit tem:*',
  a=dict(eyebrow='Para o instalador', gancho=['Instalação', '*sem improviso.*'],
         momentos=[('Split', 'Ar-condicionado'), ('Obra', 'Instalação nova'), ('Troca', 'Manutenção do ar')]),
  b=dict(kicker='Tubo de cobre', cenas=[('Rolo de', 'cobre', 'Com isolamento branco'),
                                       ('Com', 'isolamento', 'Tubo branco por fora'),
                                       ('Ar-condicionado', 'e refrigeração', None)]),
  c=dict(eyebrow='Tubo de cobre', gancho=['Vai instalar', '*o ar?*'],
         itens=['Rolo de cobre', 'Isolamento branco', 'Para ar-condicionado'], onde=['Ar-condicionado', '*e refrigeração.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03)], [('C', 3.5, 1.0, 1.03)], [('B', 4.2, 1.0, 1.03, {'d': 1.75}), ('A', 4.5, 1.0, 1.03)],
                 [('C', 2.5, 1.0, 1.03)], [('A', 3.0, 1.0, 1.02, {'d': 2.2}), ('B', 0.2, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03, {'d': 1.4}), ('A', 2.5, 1.0, 1.03)], [('C', 4.0, 1.0, 1.03, {'d': 1.9}), ('A', 4.0, 1.0, 1.03)],
                 [('B', 4.2, 1.0, 1.02, {'d': 1.75}), ('C', 2.0, 1.03, 1.0)]],
           'c': [[('C', 0.0, 1.0, 1.03)], [('A', 3.2, 1.0, 1.03, {'d': 2.7}), ('C', 3.5, 1.0, 1.03)],
                 [('B', 4.2, 1.0, 1.03, {'d': 1.75}), ('A', 5.0, 1.0, 1.02)], [('C', 4.4, 1.0, 1.02, {'d': 1.55}), ('A', 1.5, 1.03, 1.0)]]})

# p41 martelete Bosch Professional: mão segurando a ferramenta a partir de ~1,0 s nos dois takes (natural, nunca na capa)
P['p41'] = dict(id='p41', accent=(0, 95, 170), clips={'A': 6.0, 'B': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para a sua obra', gancho=['Furar concreto', '*sem sofrer.*'],
         momentos=[('Concreto', 'Furos na parede'), ('Obra', 'Do começo ao fim'), ('Reforma', 'Faça você mesmo')]),
  b=dict(kicker='Martelete Bosch', cenas=[('Bosch', 'Professional', 'Linha profissional'),
                                         ('Com', 'maleta', 'Fácil de guardar'),
                                         ('Obra e', 'reforma', None)]),
  c=dict(eyebrow='Martelete Bosch', gancho=['Parede de', '*concreto?*'],
         itens=['Bosch Professional', 'Empunhadura lateral', 'Vem na maleta'], onde=['Obra e', '*reforma.*']),
  tomadas={'a': duo('A', 'B')['a'], 'b': duo('A', 'B')['b'],
           'c': [[('A', 0.3, 1.0, 1.05, {'d': 1.3}), ('B', 3.0, 1.0, 1.03)], [('B', 0.4, 1.0, 1.03, {'d': 2.9}), ('A', 1.5, 1.0, 1.03)],
                 [('B', 4.0, 1.0, 1.03)], [('A', 4.0, 1.0, 1.02, {'d': 1.6}), ('B', 1.2, 1.03, 1.0)]]})

# p42 kit reparo hidráulico (lataria)
P['p42'] = dict(id='p42', accent=(210, 30, 30), clips={'A': 6.0, 'B': 6.0}, leve='o seu', tem='*o kit tem:*',
  a=dict(eyebrow='Para a sua oficina', gancho=['Lataria amassada?', '*Desamassa aqui.*'],
         momentos=[('Lataria', 'Desempeno de amassados'), ('Oficina', 'Força hidráulica'), ('Garagem', 'Tudo na maleta')]),
  b=dict(kicker='Kit reparo hidráulico', cenas=[('Bomba', 'hidráulica', 'Com mangueira'),
                                               ('Várias', 'peças', 'Extensões e ponteiras'),
                                               ('Oficina e', 'funilaria', None)]),
  c=dict(eyebrow='Kit reparo hidráulico', gancho=['Lataria', '*amassada?*'],
         itens=['Bomba hidráulica', 'Várias extensões', 'Vem na maleta'], onde=['Oficina e', '*funilaria.*']),
  tomadas=duo('A', 'B'))

# p43 centrífuga de mel manual: B tem mão 0,9–2,4 s
P['p43'] = dict(id='p43', accent=(220, 160, 40), clips={'A': 6.0, 'B': 6.0}, leve='a sua', tem='*ela tem:*',
  a=dict(eyebrow='Para o apicultor', gancho=['Colheita do mel', '*mais fácil.*'],
         momentos=[('Colheita', 'Mel direto dos quadros'), ('Manivela', 'Funciona na mão'), ('Torneira', 'Mel sai por baixo')]),
  b=dict(kicker='Centrífuga de mel', cenas=[('Aço', 'inox', 'Corpo brilhante'),
                                           ('Manivela', 'manual', 'Sem energia elétrica'),
                                           ('Apiário e', 'sítio', None)]),
  c=dict(eyebrow='Centrífuga de mel', gancho=['Ainda espremendo', '*os favos?*'],
         itens=['Corpo em inox', 'Manivela manual', 'Torneira de saída'], onde=['Apiário e', '*sítio.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03)], [('B', 2.5, 1.0, 1.03)], [('A', 3.0, 1.0, 1.03)], [('B', 3.3, 1.0, 1.03)],
                 [('A', 1.2, 1.0, 1.02, {'d': 2.0}), ('B', 3.8, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03, {'d': 1.3}), ('A', 1.0, 1.0, 1.03)], [('A', 0.5, 1.0, 1.03, {'d': 2.6}), ('B', 2.5, 1.0, 1.03)],
                 [('A', 3.4, 1.0, 1.02, {'d': 2.4}), ('B', 3.4, 1.03, 1.0)]],
           'c': [[('A', 2.0, 1.0, 1.03)], [('B', 2.5, 1.0, 1.03, {'d': 2.9}), ('A', 0.3, 1.0, 1.03)], [('B', 3.2, 1.0, 1.03)],
                 [('A', 4.0, 1.0, 1.02, {'d': 1.6}), ('B', 4.0, 1.03, 1.0)]]})

# p44 cadeira de escritório: mão nos 3 takes de ~0,7 a 2,1 s -> só 0–0,65 e depois de 2,2 s
P['p44'] = dict(id='p44', accent=(190, 190, 195), clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='a sua', tem='*ela tem:*',
  a=dict(eyebrow='Para o seu escritório', gancho=['Reunião', '*com estilo.*'],
         momentos=[('Reunião', 'Sala de reunião'), ('Recepção', 'Para receber clientes'), ('Estudo', 'Mesa de estudo')]),
  b=dict(kicker='Cadeira de escritório', cenas=[('Encosto', 'alto', 'Estofado preto'),
                                               ('Base', 'cromada', 'Com braços'),
                                               ('Escritório', 'e reunião', None)]),
  c=dict(eyebrow='Cadeira de escritório', gancho=['Cadeira feia', '*na reunião?*'],
         itens=['Encosto alto', 'Base cromada', 'Braços laterais'], onde=['Escritório', '*e reunião.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03, {'d': 0.65}), ('A', 2.2, 1.0, 1.03)], [('B', 2.2, 1.0, 1.03)], [('C', 2.5, 1.0, 1.03)],
                 [('A', 3.4, 1.0, 1.03)], [('B', 3.6, 1.0, 1.02, {'d': 2.2}), ('C', 4.0, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03, {'d': 0.7}), ('B', 2.2, 1.0, 1.03, {'d': 2.3}), ('C', 3.5, 1.0, 1.03)],
                 [('C', 2.2, 1.0, 1.03, {'d': 2.5}), ('A', 3.4, 1.0, 1.03)], [('B', 3.6, 1.0, 1.02, {'d': 2.4}), ('A', 2.4, 1.03, 1.0)]],
           'c': [[('C', 0.0, 1.0, 1.03, {'d': 0.8}), ('C', 2.2, 1.0, 1.03)], [('A', 2.4, 1.0, 1.03, {'d': 2.9}), ('B', 2.6, 1.0, 1.03)],
                 [('C', 3.3, 1.0, 1.03)], [('A', 4.4, 1.0, 1.02, {'d': 1.5}), ('B', 4.1, 1.03, 1.0)]]})

# p45 fone sem fio esportivo (gancho na orelha + estojo): mão A 1,0–3,0 s, B 0,5–3,0 s
P['p45'] = dict(id='p45', accent=(60, 170, 220), clips={'A': 6.0, 'B': 6.0}, leve='o seu', tem='*ele tem:*',
  a=dict(eyebrow='Para treinar', gancho=['Fone caindo', '*no treino?*'],
         momentos=[('Treino', 'Gancho na orelha'), ('Corrida', 'Sem fio'), ('Dia a dia', 'Estojo de carga')]),
  b=dict(kicker='Fone sem fio esportivo', cenas=[('Gancho', 'na orelha', 'Feito para o esporte'),
                                                ('Estojo', 'de carga', 'Guarda e carrega'),
                                                ('Treino, corrida', 'e dia a dia', None)]),
  c=dict(eyebrow='Fone sem fio', gancho=['Fone caindo', '*na corrida?*'],
         itens=['Gancho na orelha', 'Estojo de carga', 'Sem fio'], onde=['Treino, corrida', '*e dia a dia.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.04, {'d': 0.9}), ('A', 3.1, 1.0, 1.05)], [('B', 3.1, 1.0, 1.04)], [('A', 3.3, 1.0, 1.06)],
                 [('B', 3.3, 1.05, 1.0)], [('A', 3.6, 1.0, 1.03, {'d': 2.2}), ('B', 3.5, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.04, {'d': 0.45}), ('B', 3.1, 1.0, 1.05, {'d': 2.8}), ('A', 3.2, 1.0, 1.04)],
                 [('A', 3.1, 1.0, 1.05, {'d': 2.5}), ('B', 3.2, 1.0, 1.04)], [('B', 3.4, 1.0, 1.02, {'d': 2.4}), ('A', 3.3, 1.03, 1.0)]],
           'c': [[('A', 3.1, 1.06, 1.02, {'d': 2.8}), ('B', 5.5, 1.0, 1.02)], [('B', 3.1, 1.0, 1.05, {'d': 2.0}), ('A', 3.1, 1.0, 1.04, {'d': 2.0}), ('B', 5.0, 1.03, 1.0)],
                 [('B', 3.3, 1.0, 1.03)], [('A', 4.3, 1.0, 1.02, {'d': 1.6}), ('B', 4.1, 1.03, 1.0)]]})

# p46 banqueta estofada caramelo (matelassê, alavanca de altura, apoio de pés), takes Hailuo sem marca d'água
P['p46'] = dict(id='p46', accent=(190, 110, 60), clips={'A': 5.875, 'B': 5.875, 'C': 5.875}, leve='a sua', tem='*ela tem:*',
  a=dict(eyebrow='Para a sua cozinha', gancho=['Seu balcão', '*pede charme.*'],
         momentos=[('Café', 'Manhã no balcão'), ('Almoço', 'Rápido na cozinha'), ('Visita', 'Conversa na ilha')]),
  b=dict(kicker='Banqueta estofada', cenas=[('Estofado', 'matelassê', 'Cor caramelo'),
                                           ('Altura', 'regulável', 'Alavanca embaixo do assento'),
                                           ('Cozinha, ilha', 'e balcão', None)]),
  c=dict(eyebrow='Banqueta estofada', gancho=['Balcão sem', '*banqueta?*'],
         itens=['Estofado matelassê', 'Altura regulável', 'Apoio para os pés'], onde=['Cozinha, ilha', '*e balcão.*']),
  tomadas=trio('A', 'B', 'C'))

# p47 quadro decorativo (3 telas com moldura de madeira): takes B–E (sala, aparador, buffet, quarto); o take A é uma
# cadeira de escritório (outro produto?) e ficou de fora
P['p47'] = dict(id='p47', accent=(200, 140, 70), clips={'B': 5.875, 'C': 5.875, 'D': 5.875, 'E': 5.875}, leve='o seu', scrim=0.6,
  tem='*o conjunto tem:*',
  a=dict(eyebrow='Para a sua parede', gancho=['Parede vazia?', '*Fé e beleza.*'],
         momentos=[('Sala', 'Acima do sofá'), ('Entrada', 'No aparador'), ('Quarto', 'Acima da cama')]),
  b=dict(kicker='Quadro decorativo', cenas=[('Conjunto de', '3 quadros', 'Moldura de madeira'),
                                           ('Fé na', 'sua parede', 'Tons quentes e suaves'),
                                           ('Sala, quarto', 'e entrada', None)]),
  c=dict(eyebrow='Quadro decorativo', gancho=['Parede vazia', '*na sala?*'],
         itens=['3 quadros', 'Moldura de madeira', 'Tons quentes'], onde=['Sala, quarto', '*e entrada.*']),
  tomadas={'a': [[('B', 0.0, 1.0, 1.03)], [('B', 2.0, 1.0, 1.03)], [('C', 2.5, 1.0, 1.03)], [('E', 2.5, 1.0, 1.03)],
                 [('D', 3.0, 1.0, 1.02, {'d': 2.2}), ('B', 1.0, 1.03, 1.0)]],
           'b': [[('C', 0.0, 1.0, 1.03)], [('D', 1.0, 1.0, 1.03, {'d': 2.5}), ('B', 3.2, 1.0, 1.03)],
                 [('E', 3.0, 1.0, 1.02, {'d': 2.4}), ('C', 3.0, 1.03, 1.0)]],
           'c': [[('E', 0.0, 1.0, 1.03)], [('B', 1.5, 1.0, 1.03, {'d': 2.9}), ('D', 2.0, 1.0, 1.03)], [('C', 3.2, 1.0, 1.03)],
                 [('D', 4.2, 1.0, 1.02, {'d': 1.5}), ('E', 3.8, 1.03, 1.0)]]})

# p48 fritadeira elétrica 3 cubas inox: mão A 0,5–3,4 s; B 0,5–5,5 s (só B 0–0,45); C limpo
P['p48'] = dict(id='p48', accent=(230, 150, 40), clips={'A': 6.0, 'B': 6.0, 'C': 6.0}, leve='a sua', tem='*ela tem:*',
  a=dict(eyebrow='Para o seu negócio', gancho=['Fila na', '*lanchonete?*'],
         momentos=[('Batata', 'Cestos separados'), ('Pastel', 'Três cubas'), ('Salgado', 'Tudo ao mesmo tempo')]),
  b=dict(kicker='Fritadeira elétrica', cenas=[('Três', 'cubas', 'Cestos com cabo'),
                                             ('Corpo em', 'inox', 'Para cozinha profissional'),
                                             ('Lanchonete', 'e restaurante', None)]),
  c=dict(eyebrow='Fritadeira elétrica', gancho=['Uma fritadeira', '*só não dá?*'],
         itens=['Três cubas', 'Cestos com cabo', 'Corpo em inox'], onde=['Lanchonete', '*e restaurante.*']),
  tomadas={'a': [[('A', 0.0, 1.0, 1.03, {'d': 0.45}), ('A', 3.5, 1.0, 1.03, {'d': 2.4}), ('C', 0.5, 1.0, 1.03)],
                 [('C', 2.0, 1.0, 1.03)], [('A', 3.4, 1.0, 1.04)], [('C', 3.4, 1.0, 1.03)],
                 [('A', 3.6, 1.0, 1.02, {'d': 2.2}), ('C', 4.0, 1.03, 1.0)]],
           'b': [[('B', 0.0, 1.0, 1.03, {'d': 0.45}), ('C', 1.0, 1.0, 1.04, {'d': 2.6}), ('A', 3.6, 1.0, 1.03)],
                 [('C', 3.0, 1.0, 1.03, {'d': 2.5}), ('A', 3.4, 1.0, 1.04)], [('C', 3.6, 1.0, 1.02, {'d': 2.4}), ('A', 3.5, 1.03, 1.0)]],
           'c': [[('C', 0.0, 1.0, 1.03)], [('A', 3.4, 1.0, 1.03, {'d': 2.5}), ('C', 2.6, 1.0, 1.04)], [('A', 3.6, 1.0, 1.05)],
                 [('C', 4.2, 1.0, 1.02, {'d': 1.6}), ('A', 4.0, 1.03, 1.0)]]})

if __name__ == '__main__':
    for pid in sys.argv[1:]:
        print(fazer_produto(P[pid]))
