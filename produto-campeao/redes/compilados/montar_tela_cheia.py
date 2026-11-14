"""Vídeo de vários produtos em TELA CHEIA (a dona, 14/11: "faça um vídeo com tela limpa"). Grátis: só edição.
Usa os clipes LIMPOS (sem texto) de <lote>/pNN-cenas/X.mp4; o texto (estilo 1) fica por cima do vídeo, no topo,
com uma sombra suave em degradê, igual ao carrossel. Sem painel creme.
Uso: python3 montar_tela_cheia.py pedido.json saida.mp4   (mesmo pedido.json do montar.py)"""
import json, subprocess, sys, os, tempfile, html
from pathlib import Path
from montar import gancho_partes, FONTES, HOOK, FIM, RAIZ

W, H, FAIXA = 1080, 1920, 760
CSS = f"""
@font-face{{font-family:Vibes;src:url({FONTES}/great-vibes-latin-400-normal.woff)}}
@font-face{{font-family:Corm;font-weight:600;src:url({FONTES}/cormorant-garamond-latin-600-normal.woff)}}
@font-face{{font-family:Corm;font-style:italic;font-weight:500;src:url({FONTES}/cormorant-garamond-latin-500-italic.woff)}}
html,body{{margin:0;background:transparent}}
.p{{width:{W}px;height:{FAIXA}px;position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
  text-align:center;color:#fff;box-sizing:border-box;padding:150px 50px 0;
  background:linear-gradient(180deg,rgba(40,20,28,.62),rgba(40,20,28,.30) 55%,rgba(40,20,28,0));
  text-shadow:0 2px 6px rgba(40,15,25,.45),0 4px 28px rgba(40,15,25,.55)}}
.ass{{position:absolute;top:70px;left:0;right:0;font:500 italic 30px Corm;letter-spacing:.32em;opacity:.9}}
.it{{font:500 italic 72px/1 Corm}}
.cx{{font:600 112px/1.02 Corm;letter-spacing:.04em;text-transform:uppercase;margin:6px 0}}
.sc{{font:400 104px/1.05 Vibes;color:#ffd9e6}}
.num{{font:400 88px/1 Vibes;color:#ffd9e6}}
.nome{{font:600 84px/1.05 Corm;letter-spacing:.03em;text-transform:uppercase;margin-top:8px}}
.de{{font:500 italic 44px Corm;margin-top:14px;opacity:.92}}
"""


def renderizar(corpos, pasta):
    f = Path(pasta) / 'paineis.html'
    f.write_text(f"<html><head><style>{CSS}</style></head><body>" + ''.join(f'<div class="p"><div class="ass">aguiiar lar</div>{c}</div>' for c in corpos) + "</body></html>")
    js = Path(pasta) / 'foto.js'
    js.write_text("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
                  f"const p=await b.newPage({{viewport:{{width:{W},height:{FAIXA}}}}});await p.goto('file://{f}');"
                  "await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);const els=await p.$$('.p');"
                  f"for(let i=0;i<els.length;i++) await els[i].screenshot({{path:'{pasta}/painel'+i+'.png',omitBackground:true}});await b.close();}})();")
    subprocess.run(['node', str(js)], check=True, capture_output=True)
    return [f'{pasta}/painel{i}.png' for i in range(len(corpos))]


def main(pedido, saida):
    P = json.load(open(pedido)); itens = P['itens']; n = len(itens); tmp = tempfile.mkdtemp(); e = html.escape
    pq, cx, sc = gancho_partes(P['gancho'])
    corpos = [f'<div class="it">{e(pq)}</div><div class="cx">{e(cx)}</div><div class="sc">{e(sc)}</div>']
    for i, it in enumerate(itens):
        corpos.append(f'<div class="num">nº {i + 1}</div><div class="nome">{e(it["nome"])}</div><div class="de">achadinho {i + 1} de {n}</div>')
    f1, f2, f3 = P.get('fim') or ['Comenta', 'EU QUERO', 'que eu te mando o link']
    corpos.append(f'<div class="it">{e(f1)}</div><div class="cx">{e(f2)}</div><div class="sc">{e(f3)}</div>')
    png = renderizar(corpos, tmp)
    trechos = []
    for i, it in enumerate(itens):
        o = f'{tmp}/t{i}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(it['ini']), '-t', str(it['dur']), '-i', it['mp4'],
                        '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1', '-an',
                        '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', o], check=True)
        trechos.append(o)
    lista = f'{tmp}/l.txt'; Path(lista).write_text(''.join(f"file '{t}'\n" for t in trechos))
    base = f'{tmp}/base.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', base], check=True)
    total = sum(it['dur'] for it in itens)
    janelas = [(0, HOOK)]; t = 0
    for i, it in enumerate(itens):
        janelas.append((HOOK if i == 0 else t, t + it['dur'] - (FIM if i == n - 1 else 0))); t += it['dur']
    janelas.append((total - FIM, total))
    ent = ['-i', base]
    for p_ in png: ent += ['-i', p_]
    filtro = '[0]null[v0]'
    for k, (a, b) in enumerate(janelas):
        filtro += f';[v{k}][{k + 1}]overlay=0:0:enable=\'between(t,{a:.2f},{b - 0.001:.3f})\'[v{k + 1}]'
    ult = f'v{len(janelas)}'
    ent += ['-stream_loop', '-1', '-i', P.get('musica') or str(RAIZ / 'musicas/silencio.wav')]
    ia = len(png) + 1
    filtro += f';[{ia}:a]atrim=0:{total},afade=t=in:d=0.8,afade=t=out:st={total - 1.2}:d=1.2[a]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ent, '-filter_complex', filtro, '-map', f'[{ult}]', '-map', '[a]',
                    '-t', str(total), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', saida], check=True)
    print(saida, f'{total:.1f}s', f'{os.path.getsize(saida) / 1e6:.1f} MB')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
