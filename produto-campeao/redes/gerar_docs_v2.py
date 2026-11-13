import json,sys,time,os
sys.path.insert(0,'/home/user/fabrica-ugc/produto-campeao/vendas'); sys.path.insert(0,'/home/user/fabrica-ugc/produto-campeao/afiliados')
from link_subid import link
d=json.load(open('candidatos_carrossel-2026-11-13_v2.json'))
exc=set(); E=json.load(open('../afiliados/excluidos.json'))
for v in (E.values() if isinstance(E,dict) else [E]): exc|=set(map(str,v))
vis=set(map(str,json.load(open('vistos_carrossel.json'))))
os.makedirs('listas/1311_v2_docs',exist_ok=True)
n=40; ok=[]
for x in d:
    if str(x['id']) in exc or str(x['id']) in vis: print('fora',x['id']); continue
    n+=1; sub=f'Cr{n:03d}'
    for t in range(6):
        try: s,url=link(x['link'],sub,'','261113'); break
        except Exception as e: time.sleep(10*(t+1)); url=None
    if not url: print('sem link',x['id']); n-=1; continue
    doc={k:v for k,v in x.items()}; doc.update(link_afiliado=url,sub_id=s,dia='2026-11-13',ordem=n,origem='varredura_carrossel',busca_lista='natal rosa + natal + romântico (v2, filtro R$ 10)')
    json.dump(doc,open(f'listas/1311_v2_docs/{x["id"]}.json','w'),ensure_ascii=False); ok.append(str(x['id']))
json.dump(sorted(vis|set(ok)),open('vistos_carrossel.json','w'))
print(len(ok),'ok')
