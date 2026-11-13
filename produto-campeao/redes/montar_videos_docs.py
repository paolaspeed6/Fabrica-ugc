import json,glob,re,os,base64,io,sys
from PIL import Image
S=sys.argv[1]; R='/home/user/fabrica-ugc/produto-campeao'
info={}
for f in glob.glob(R+'/**/*.json',recursive=True):
    if os.path.getsize(f)>60e6: continue
    try: d=json.load(open(f))
    except: continue
    L=d if isinstance(d,list) else (list(d.values()) if isinstance(d,dict) else [])
    for x in L:
        if isinstance(x,dict) and (x.get('id') or x.get('itemId')) and 'comissao_rs' in x:
            info[str(x.get('id') or x.get('itemId'))]={'preco':x.get('preco'),'comissao_rs':x.get('comissao_rs'),'vendidos':x.get('vendidos')}
out=[]
for f in sorted(glob.glob(S+'/post_db/conferir/*.json')):
    d=json.load(open(f)); did=os.path.basename(f)[:-5]
    m=re.search(r'/(\d+)$',d.get('link_anuncio','').split('?')[0]); iid=m.group(1) if m else ''
    p=d.get('poster','')
    try:
        im=Image.open(io.BytesIO(base64.b64decode(p.split(',',1)[1]))).convert('RGB'); im.thumbnail((240,427))
        b=io.BytesIO(); im.save(b,'JPEG',quality=70); p='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    except Exception as e: p=''
    links={k.rsplit('_',1)[-1]:v.get('link_produto') for k,v in (d.get('posts') or {}).items()}
    doc={'produto':d.get('produto',''),'lote':d.get('lote',''),'dia':d.get('dia',''),'item_id':iid,'poster':p,
         'drive_urls':d.get('drive_urls',{}),'link_anuncio':d.get('link_anuncio',''),'links':links,**info.get(iid,{})}
    out.append((did,doc))
json.dump(out,open(S+'/vid/docs.json','w'),ensure_ascii=False)
print(len(out),sum(1 for _,d in out if d.get('comissao_rs')), sum(len(d['poster']) for _,d in out)/1e6,'MB')
