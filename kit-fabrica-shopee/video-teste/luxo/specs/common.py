import json, os, sys
# pasta de trabalho de um produto: src/A.mp4..F.mp4 (cenas), tts2/ (narrações), out2/ e specs/ (saídas)
S = os.environ.get('LUXO_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trabalho'))
SRC = {k: f'{S}/src/{k}.mp4' for k in 'ABCDEF'}
def seg(src,ss,dur,z=(1.0,1.08),c0=None,c1=None,**kw):
    d=dict(src=src,ss=ss,dur=dur,z=list(z),**kw)
    if c0: d['c0']=list(c0)
    if c1: d['c1']=list(c1)
    return d
