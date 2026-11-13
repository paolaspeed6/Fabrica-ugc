"""Vídeo com vários produtos (aba 🎬 Montar vídeo do Tinder > Redes Sociais). Grátis: só edição.

Usa a versão A de cada vídeo já aprovado (o texto antigo dela fica sempre no topo, até ~30% da altura).
A faixa de cima (0-650 px) vira o painel da Aguiiar Lar (letras do estilo 1 que a dona escolheu) e cobre esse texto;
o produto continua aparecendo embaixo, sem mudar de tamanho.

Uso: python3 montar.py pedido.json saida.mp4
pedido.json = {"gancho": "...", "fim": ["Comenta", "EU QUERO", "que eu te mando o link"],
               "itens": [{"mp4": ".../X_A.mp4", "ini": 1.0, "dur": 4.8, "nome": "Banqueta bouclê"}, ...],
               "musica": ".../trilha.wav", "voz": null | ".../voz.wav"}
"""
import json, subprocess, sys, os, tempfile, html
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
FONTES = RAIZ / 'video-teste/fontes/redes'
TOPO = 650           # altura do painel
W, H = 1080, 1920
HOOK = 2.6           # segundos do gancho sobre o 1º produto
FIM = 3.0            # segundos do convite no fim (sobre o último produto)

CSS = f"""
@font-face{{font-family:Vibes;src:url({FONTES}/great-vibes-latin-400-normal.woff)}}
@font-face{{font-family:Corm;font-weight:600;src:url({FONTES}/cormorant-garamond-latin-600-normal.woff)}}
@font-face{{font-family:Corm;font-style:italic;font-weight:500;src:url({FONTES}/cormorant-garamond-latin-500-italic.woff)}}
body{{margin:0}}
.p{{width:{W}px;height:{TOPO}px;background:#f8f2ec;position:relative;overflow:hidden;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;color:#3b2a2e;box-sizing:border-box;padding:40px 60px 30px}}
.p::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:6px;background:linear-gradient(90deg,#e9c9d3,#c9748f,#e9c9d3)}}
.ass{{position:absolute;top:34px;left:0;right:0;font:500 italic 30px Corm;letter-spacing:.32em;color:#a3868c}}
.it{{font:500 italic 74px/1 Corm;color:#6d5056}}
.cx{{font:600 116px/1.02 Corm;letter-spacing:.04em;text-transform:uppercase;margin:6px 0}}
.sc{{font:400 104px/1.05 Vibes;color:#c4587f}}
.num{{font:400 92px/1 Vibes;color:#c4587f}}
.nome{{font:600 84px/1.05 Corm;letter-spacing:.03em;text-transform:uppercase;margin-top:8px}}
.de{{font:500 italic 46px Corm;color:#a3868c;margin-top:16px}}
"""


def gancho_partes(g):
    """'Parece de loja cara, mas é da Shopee' -> pequeno / CAIXA ALTA / cursiva (estilo 1)."""
    if ',' in g:
        a, c = g.split(',', 1)
        pal = a.split()
        if len(pal) >= 3:
            return ' '.join(pal[:-2]), ' '.join(pal[-2:]) + ',', c.strip()
        return '', a + ',', c.strip()
    pal = g.split()
    t = len(pal)
    return ' '.join(pal[:t // 3]), ' '.join(pal[t // 3:2 * t // 3]), ' '.join(pal[2 * t // 3:])


def painel(corpo):
    return f'<div class="p"><div class="ass">aguiiar lar</div>{corpo}</div>'


def renderizar(paineis, pasta):
    doc = f"<html><head><style>{CSS}</style></head><body>" + ''.join(paineis) + "</body></html>"
    f = Path(pasta) / 'paineis.html'; f.write_text(doc)
    subprocess.run(['node', str(Path(__file__).with_name('foto_paineis.js')), str(f), str(pasta), str(W), str(TOPO)],
                   check=True, capture_output=True)
    return [str(Path(pasta) / f'painel{i}.png') for i in range(len(paineis))]


def main(pedido, saida):
    P = json.load(open(pedido))
    itens = P['itens']; n = len(itens)
    tmp = tempfile.mkdtemp()
    e = html.escape
    pq, cx, sc = gancho_partes(P['gancho'])
    corpos = [painel(f'<div class="it">{e(pq)}</div><div class="cx">{e(cx)}</div><div class="sc">{e(sc)}</div>')]
    for i, it in enumerate(itens):
        corpos.append(painel(f'<div class="num">nº {i + 1}</div><div class="nome">{e(it["nome"])}</div>'
                             f'<div class="de">achadinho {i + 1} de {n}</div>'))
    f1, f2, f3 = P.get('fim') or ['Comenta', 'EU QUERO', 'que eu te mando o link']
    corpos.append(painel(f'<div class="it">{e(f1)}</div><div class="cx">{e(f2)}</div><div class="sc">{e(f3)}</div>'))
    png = renderizar(corpos, tmp)

    # trechos dos vídeos (só a parte de baixo, sem o texto antigo)
    trechos = []
    for i, it in enumerate(itens):
        o = f'{tmp}/t{i}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(it['ini']), '-t', str(it['dur']), '-i', it['mp4'],
                        '-vf', f'crop={W}:{H - TOPO}:0:{TOPO},fps=30,setsar=1', '-an', '-c:v', 'libx264', '-preset', 'fast',
                        '-crf', '16', o], check=True)
        trechos.append(o)
    lista = f'{tmp}/l.txt'; Path(lista).write_text(''.join(f"file '{t}'\n" for t in trechos))
    base = f'{tmp}/base.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', base], check=True)
    total = sum(it['dur'] for it in itens)

    # quando cada painel aparece
    janelas = [(0, HOOK)]
    t = 0
    for i, it in enumerate(itens):
        a = HOOK if i == 0 else t
        b = t + it['dur'] - (FIM if i == n - 1 else 0)
        janelas.append((a, b)); t += it['dur']
    janelas.append((total - FIM, total))

    ent = ['-f', 'lavfi', '-i', f'color=c=#f8f2ec:s={W}x{H}:r=30:d={total}', '-i', base]
    for p_ in png: ent += ['-i', p_]
    filtro = '[0][1]overlay=0:%d[v0]' % TOPO
    for k, (a, b) in enumerate(janelas):
        filtro += f';[v{k}][{k + 2}]overlay=0:0:enable=\'between(t,{a:.2f},{b - 0.001:.3f})\'[v{k + 1}]'
    ult = f'v{len(janelas)}'
    # áudio: música baixa (+ voz por cima, se tiver)
    musica = P.get('musica') or str(RAIZ / 'musicas/silencio.wav')
    ent += ['-stream_loop', '-1', '-i', musica]
    ia = len(png) + 2
    vol = 0.35 if P.get('voz') else 1.0
    filtro += f';[{ia}:a]atrim=0:{total},volume={vol},afade=t=in:d=0.8,afade=t=out:st={total - 1.2}:d=1.2[m]'
    if P.get('voz'):
        ent += ['-i', P['voz']]
        filtro += f';[{ia + 1}:a]adelay=300|300,apad[vz];[m][vz]amix=inputs=2:duration=first:normalize=0[a]'
    else:
        filtro += ';[m]anull[a]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ent, '-filter_complex', filtro, '-map', f'[{ult}]', '-map', '[a]',
                    '-t', str(total), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', saida], check=True)
    print(saida, f'{total:.1f}s', f'{os.path.getsize(saida) / 1e6:.1f} MB')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
