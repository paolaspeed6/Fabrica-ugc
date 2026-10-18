"""Gera a página de entrega de um lote (3 opções por produto) a partir de lote.json.
uso: python3 pagina_lote.py lote.json saida_dir   -> saida_dir/index.html + lista de arquivos para publicar"""
import json, sys, html
lote = json.load(open(sys.argv[1])); out = sys.argv[2]
OPS = [('A', 'Um dia com ela', 'a'), ('B', 'Faixas moderno', 'b'), ('C', 'Direto ao ponto', 'c')]
sec = []
for p in lote['produtos']:
    cards = ''.join(f'''
      <article class="op">
        <h3><span class="tag">Opção {L}</span> {nome}</h3>
        <video src="{p['id']}_{k}.mp4" poster="{p['id']}_{k}.jpg" controls playsinline preload="metadata"></video>
        <button class="dl" data-file="{p['id']}_{k}.mp4" data-name="{p['slug']}_{L}.mp4">Baixar opção {L}</button>
        <p class="msg" aria-live="polite"></p>
      </article>''' for L, nome, k in OPS)
    sec.append(f'''
  <section class="prod" aria-labelledby="{p['id']}">
    <h2 id="{p['id']}">{html.escape(p['nome'])}</h2>
    <div class="grid">{cards}
    </div>
    <div class="cap">
      <p id="cap-{p['id']}">{html.escape(p['legenda'])}</p>
      <button class="copy" data-target="cap-{p['id']}">Copiar legenda</button>
    </div>
  </section>''')
tpl = open(__file__.replace('pagina_lote.py', 'pagina_lote.html')).read()
open(f'{out}/index.html', 'w').write(tpl.replace('<!--TITULO-->', html.escape(lote['titulo'])).replace('<!--PRODUTOS-->', ''.join(sec))
                                     .replace('<!--N-->', str(len(lote['produtos']))))
