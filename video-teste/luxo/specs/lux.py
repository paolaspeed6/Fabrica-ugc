"""Timelines da Coleção Luxo (cadeira trançada + poltrona capitonê bege, 2026-10-18). Molde para novos produtos.
Fontes: A=varanda(cadeira, ghosting 4.8–6.4s), B=sala(cadeira; áudio tem passos → não usar), C=leitura(cadeira),
D=sala(poltrona, piano), E=quarto(poltrona, sem áudio), F=leitura(poltrona, piano).
Narrações: tts_lux.py → tighten.py X.wav X_t.wav 0.5. Render ~3,5 min/vídeo.
Textos: c1 "O trançado que faltava na sua casa. Linhas simples, textura natural... e aquele toque que transforma qualquer canto. Toque no link e leve pra casa."
 c2 "Não é só uma cadeira. É uma peça para ser vista. O trançado chama o olhar, as linhas são limpas... e o ambiente inteiro muda. Toque no link e leve essa peça pra casa."
 c3 "Um dia inteiro com ela. De manhã, café na varanda. À tarde, a sala. À noite, o cantinho de leitura. Toque no link e leve pra casa."
 p1 "A poltrona que acolhe. Encosto capitonê, visual aveludado, pezinhos escuros de linha clássica. Toque no link e leve pra casa."
 p2 "Elegância não faz barulho. Ela só ocupa o lugar certo. Capitonê no encosto, visual aveludado, linhas clássicas. Toque no link e leve essa peça pra casa."
 p3 "Do café ao último capítulo. De manhã, no quarto. À tarde, na sala. E à noite, no cantinho de leitura. Toque no link e leve pra casa."
"""
from common import *
import json
N=f'{S}/tts2/'
def save2(name, **sp):
    sp['src']=SRC; sp['out']=f'{S}/out2/{name}.mp4'; sp.setdefault('dur',15.0)
    tot=sum(s['dur'] for s in sp['segs']); assert abs(tot-15)<1e-6,(name,tot)
    os.makedirs(f'{S}/specs', exist_ok=True); os.makedirs(f'{S}/out2', exist_ok=True)
    json.dump(sp,open(f'{S}/specs/{name}.json','w'),ensure_ascii=False,indent=1)
def eb(txt,t0,t1,y=250,**k): return dict(kind='eyebrow',lines=[txt],t0=t0,t1=t1,y=y,**k)
def ti(lines,t0,t1,y=300,**k): return dict(kind='title',lines=lines,t0=t0,t1=t1,y=y,**k)
def bo(lines,t0,t1,y=300,**k): return dict(kind='body',lines=lines,t0=t0,t1=t1,y=y,**k)
def ln(t0,t1,y,L=220,**k): return dict(kind='line',len=L,t0=t0,t1=t1,y=y,anim='draw',**k)
def cta(t0,head='Leve pra casa.',eyebrow='Disponível no link'):
    lines=head if isinstance(head,list) else [head]
    return [eb(eyebrow,t0,15,y=250,out=False), ti(lines,t0+0.25,15,y=300,out=False,anim='wipe'),
            ln(t0+0.6,15,300+len(lines)*122+30,out=False)]
ZARA=dict(sat=0.82,warm=0.035,contrast=0.94,lift=0.04,vign=0.12,grain=0.02,top=0.30)
GAL=dict(sat=0.72,warm=0.0,contrast=1.08,lift=0.02,vign=0.55,grain=0.026,top=0.32)
DIA=dict(sat=0.86,contrast=0.98,lift=0.035,vign=0.25,grain=0.022,top=0.30)
PIANO=['D','F','D']

# CADEIRA
save2('cadeira_lux1_zarahome', narr=N+'c1_t.wav', narr_at=0.5, bed=PIANO, grade=ZARA,
 segs=[seg('A',0.0,3.9,(1.0,1.08)), seg('B',5.0,1.6,(1.0,1.05)), seg('C',2.8,1.4,(1.04,1.1)),
       seg('B',0.3,2.0,(1.0,1.06)), seg('C',5.4,2.0,(1.0,1.06)), seg('A',6.5,1.5,(1.0,1.04)), seg('B',2.3,2.6,(1.02,1.1))],
 texts=[eb('Nova coleção — Casa',0,3.8), ti(['O trançado','*que faltava.*'],0,3.8), ln(0.4,3.8,580),
        eb('Detalhe 01',3.9,5.5), bo(['Linhas *simples.*'],4.0,5.5),
        eb('Detalhe 02',5.5,6.9), bo(['Textura *natural.*'],5.6,6.9),
        bo(['Transforma','*qualquer canto.*'],7.2,10.9),
        eb('Varanda · Sala · Leitura',9.0,10.9,y=520)] + cta(11.3))

save2('cadeira_lux2_galeria', narr=N+'c2_t.wav', narr_at=0.5, tempo=1.08, bed=PIANO, grade=GAL,
 segs=[seg('C',0.0,2.6,(1.0,1.06)), seg('A',0.6,2.0,(1.0,1.05)), seg('B',5.0,2.0,(1.0,1.04)), seg('C',2.6,1.8,(1.03,1.08)),
       seg('A',6.5,1.5,(1.0,1.04)), seg('B',0.0,2.4,(1.0,1.06)), seg('C',5.3,2.7,(1.0,1.06))],
 texts=[eb('Peça nº 01',0,2.5), ti(['Não é só','uma *cadeira.*'],0,2.5),
        ti(['É uma peça','*para ser vista.*'],2.6,4.6),
        bo(['O trançado','*chama o olhar.*'],4.7,6.6),
        bo(['Linhas *limpas.*'],6.7,8.4),
        dict(kind='placard',lines=['Peça nº 01','Cadeira trançada','estudo em textura e luz','Varanda · Sala · Leitura'],t0=8.5,t1=11.0,y=230,anim='fade')]
       + cta(11.1,['Leve essa peça','*pra casa.*']))

save2('cadeira_lux3_umdia', narr=N+'c3_t.wav', narr_at=0.5, bed=PIANO, dips=[5.6,7.9],
 grade=dict(DIA, warm_ramp=[(0,-0.02,1.03),(5.4,-0.02,1.03),(5.8,0.05,1.0),(7.7,0.05,1.0),(8.1,0.11,0.86),(15,0.11,0.86)]),
 segs=[seg('A',0.0,4.6,(1.0,1.1)), seg('A',6.6,1.0,(1.04,1.08)), seg('B',0.0,2.3,(1.0,1.06)),
       seg('C',0.0,2.5,(1.0,1.06)), seg('C',2.6,2.0,(1.03,1.08)), seg('B',4.8,2.6,(1.0,1.05))],
 texts=[eb('Das 8h às 22h',0,2.8), ti(['Um dia inteiro','*com ela.*'],0,2.8),
        dict(kind='clock',keys=[(2.9,'08:00'),(5.6,'15:00'),(7.9,'22:00')],t0=2.9,t1=10.5,y=230,size=200,anim='fade'),
        eb('Café na varanda',3.1,5.5,y=470), eb('A sala',5.7,7.8,y=470), eb('O cantinho de leitura',8.0,10.5,y=470)]
       + cta(10.7))

# POLTRONA
save2('poltrona_lux1_zarahome', narr=N+'p1_t.wav', narr_at=1.2, bed=PIANO, grade=ZARA,
 segs=[seg('D',0.0,3.3,(1.0,1.07)), seg('F',0.0,1.6,(1.9,2.0),c0=(380,700)), seg('E',0.0,1.6,(1.5,1.55),c0=(400,900)),
       seg('D',3.3,2.0,(1.6,1.5),c0=(360,1000)), seg('E',1.6,2.4,(1.0,1.06)), seg('F',1.6,4.1,(1.0,1.08))],
 texts=[eb('Nova coleção — Casa',0,3.2), ti(['A poltrona','*que acolhe.*'],0,3.2), ln(0.4,3.2,580),
        eb('Detalhe 01',3.3,4.9,y=200), bo(['Encosto *capitonê.*'],3.4,4.9,y=250),
        eb('Detalhe 02',4.9,6.5,y=200), bo(['Visual *aveludado.*'],5.0,6.5,y=250),
        eb('Detalhe 03',6.5,8.5,y=200), bo(['Linha *clássica.*'],6.6,8.5,y=250),
        eb('Sala · Quarto · Leitura',8.6,9.8)] + cta(9.9))

save2('poltrona_lux2_galeria', narr=N+'p2_t.wav', narr_at=0.5, bed=PIANO, grade=GAL,
 segs=[seg('F',0.0,2.7,(1.0,1.06)), seg('D',0.0,2.6,(1.0,1.06)), seg('F',2.7,1.6,(1.8,1.9),c0=(420,700)),
       seg('E',0.0,1.8,(1.5,1.55),c0=(400,900)), seg('D',2.6,2.0,(1.5,1.4),c0=(360,950)), seg('E',1.7,4.3,(1.0,1.08))],
 texts=[eb('Peça nº 02',0,2.6), ti(['Elegância não','faz *barulho.*'],0,2.6),
        ti(['Ela só ocupa','*o lugar certo.*'],2.7,5.2),
        bo(['Capitonê','*no encosto.*'],5.3,6.9,y=220),
        bo(['Visual *aveludado.*'],7.0,8.7,y=220),
        dict(kind='placard',lines=['Peça nº 02','Poltrona capitonê','estudo em tom areia','Sala · Quarto · Leitura'],t0=8.8,t1=11.1,y=200,anim='fade')]
       + cta(11.2,['Leve essa peça','*pra casa.*']))

save2('poltrona_lux3_umdia', narr=N+'p3_t.wav', narr_at=0.8, bed=PIANO, dips=[5.6,7.8],
 grade=dict(DIA, warm_ramp=[(0,-0.02,1.03),(5.4,-0.02,1.03),(5.8,0.05,1.0),(7.6,0.05,1.0),(8.0,0.11,0.86),(15,0.11,0.86)]),
 segs=[seg('E',0.0,3.6,(1.0,1.07)), seg('E',3.6,2.0,(1.25,1.3)), seg('D',0.0,2.2,(1.0,1.06)),
       seg('F',0.0,2.8,(1.0,1.07)), seg('F',2.8,2.2,(1.05,1.1)), seg('D',2.2,2.2,(1.0,1.06))],
 texts=[eb('Das 8h às 22h',0,3.4), ti(['Do café ao','*último capítulo.*'],0,3.4),
        dict(kind='clock',keys=[(3.6,'08:00'),(5.6,'15:00'),(7.8,'22:00')],t0=3.6,t1=10.5,y=230,size=200,anim='fade'),
        eb('No quarto',3.8,5.5,y=470), eb('Na sala',5.7,7.7,y=470), eb('No cantinho de leitura',7.9,10.5,y=470)]
       + cta(10.7))
