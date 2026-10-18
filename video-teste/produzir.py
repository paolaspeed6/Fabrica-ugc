"""Um comando para o lote inteiro: fotos do anúncio > cenas > 3 versões > legendas > folha de aprovação.

Uso:
    python3 produzir.py --preparar <link do anúncio> <nome>   # passo 0: baixa fotos e descrição em lote/<nome>-fotos/
    python3 produzir.py lote/banqueta.json [lote/outro_produto.json ...]

Passo 0 é grátis: o Claude olha a folha lote/<nome>-fotos/todas_as_fotos.jpg e o anuncio.json,
escolhe as fotos reais (descarta artes e erros do anúncio) e escreve lote/<nome>.json.

Cada produto.json (escrito pelo Claude a partir do anúncio):
{
  "nome": "banqueta",
  "link": "https://s.shopee.com.br/...",           # link de afiliado (vai nas legendas)
  "fotos": ["fotos/principal.jpg"],               # fotos reais do anúncio (URL ou arquivo)
  "cor_destaque": "auto",                         # ou hex; "auto" alterna pela PALETA
  (em "cenas", "lento": 1.4 desacelera um clipe com zoom forte em todas as versões)
  "cenas": [                                      # receita fiel: editar com Seedream ou animar foto
    {"editar": "...", "movimento": "...", "clipe": "cenas/cena1.mp4"},
    {"foto": 0, "movimento": "...", "clipe": "cenas/cena3.mp4"}
  ],
  "versoes": {                                    # um modelo aprovado por plataforma
    "shopee": {"cenas": [{"titulo": "...", "rotulo": "...", "chamadas": [...]}, ...]},
    "tiktok": {"cenas": [...]},
    "reels":  {"cenas": [...]}
  },
  "legendas": {"shopee": "...", "tiktok": "...", "reels": "..."},
  "hashtags": {"tiktok": "#casa #decor", "reels": "#decoracao"},
  "comentario": "🛒 Link do produto: {link}"         # opcional: 1º comentário fixado no Facebook
}

- Se o "clipe" de uma cena já existe, ela não é gerada de novo (custo zero); a imagem do Seedream fica em cenaN.png e também é reaproveitada.
- "--so-imagens" antes dos arquivos gera só as imagens, para conferir a fidelidade antes de pagar os vídeos.
- TETO_LOTE_USD=5 limita o gasto do lote inteiro.
  Senão, gera pelo WaveSpeed (precisa de WAVESPEED_API_KEY e do domínio liberado).
- Em cada versão, "cenas" segue a ordem das cenas geradas; use "ordem": [1, 0, 2]
  para reordenar e "ate"/"lento" por cena para ajustar o tempo.
- Cada "editar" ganha no fim a regra de composição (produto no centro, longe dos textos);
  use "composicao": false na cena para não acrescentar.
- As cenas de todos os produtos são geradas em paralelo, e a montagem roda 2 produtos por vez.
  Antes de gerar, confere se o saldo da WaveSpeed cobre o pior caso do lote.
- Saída em saida/<nome>/: um vídeo por versão, legendas.txt e, para o lote todo,
  saida/aprovacao.jpg com a foto do anúncio e um quadro de cada cena de cada versão.
"""
import json
import os
import subprocess
import sys
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import compor_embalagem  # noqa: E402
import gerar_video  # noqa: E402
from montar_video_pro import PALETA  # noqa: E402

# 3 cenas de 5 s com "lento" 1.1 dão exatamente 15 s em cada versão (medido no vídeo da placa)
ATE_PADRAO = {"shopee": [5.27] * 3, "tiktok": [5.08] * 3, "reels": [5.33] * 3,
              "reels_faixas": [5.33] * 3, "reels_cartao": [5.33] * 3}
GSAP = {"shopee", "reels_faixas", "reels_cartao"}  # estilos com texto animado (gsap/camada_<estilo>.html)
REELS = ["reels_faixas", "reels_cartao"]  # modelos 1 e 4 aprovados por a dona; alternam entre produtos
LENTO_PADRAO = 1.1
# Áreas de texto dos modelos: Shopee embaixo (73-92% da altura), TikTok em cima (8-22%) e CTA (62-68%),
# Reels embaixo à esquerda (63-90%). O produto fica entre 30% e 60% e nunca é coberto pelo texto.
COMPOSICAO = (" Composition: the product is placed in the CENTER of the frame, vertically between 30% and 60% "
              "of the image height, fully visible, with plain background (no important details) in the top 25% "
              "and the bottom 35% of the image, where on-screen text will go.")
# Órbita fez o Seedance girar o capacete e inventar a frente (2026-10-15): o produto só aparece pelos lados
# que o quadro inicial mostra. Use "push-in", "dolly lateral curto", "crane"; nunca "orbit" ou "rotate".
TRAVA_ANGULO = (" Realistic handheld smartphone camera feel. The camera may move in a short arc of at most 15-20 degrees, "
                "but no side of the product that is hidden in the first frame is ever shown. Lettering never changes "
                "or mirrors. No people, no reflections of people. Nothing new appears in the scene.")
# Cena que recebe a embalagem real por código (compor_embalagem.py): câmera parada na geração,
# o movimento é aplicado depois na imagem inteira
CAMERA_PARADA = (" Locked-off static camera on a tripod: no camera movement, no zoom, no pan. No people. "
                 "No bag or packaging, no text. Nothing new appears in the scene.")
# Regra fixa da dona (2026-10-15): os termos da Shopee proíbem bebida alcoólica. Citar garrafas no prompt, mesmo
# negando ("no wine bottles"), FEZ o Seedream desenhar garrafas 2 vezes: descreva só o que entra na cena
PROIBIDO = (" Minimalist, uncluttered scene: it contains ONLY the objects described above, nothing else on the floor, "
            "shelves or furniture.")
PARALELO_GERACAO = 12
PARALELO_MONTAGEM = 2
# Teto de gasto do lote (env TETO_LOTE_USD): cada chamada paga reserva seu preço antes de sair;
# passando do teto, a cena falha em vez de gastar. SO_IMAGENS para depois das edições do Seedream,
# para conferir a fidelidade das imagens (cenaN.png) antes de pagar a animação.
TETO_LOTE = float(os.environ.get("TETO_LOTE_USD", "inf"))
SO_IMAGENS = False
_gasto, _trava = [0.0], threading.Lock()


def api_paga(modelo, entrada):
    preco = gerar_video.CUSTO_CLIPE_USD if modelo == gerar_video.MODELO_VIDEO else gerar_video.CUSTO_IMAGEM_USD
    with _trava:
        if _gasto[0] + preco > TETO_LOTE + 1e-9:
            raise RuntimeError(f"teto do lote de US$ {TETO_LOTE:.2f} atingido")
        _gasto[0] += preco
    try:
        return gerar_video.api(modelo, entrada)
    except Exception:
        with _trava:  # tarefa que falhou na WaveSpeed não é cobrada
            _gasto[0] -= preco
        raise


REDES = {"shopee": "Shopee Vídeo", "tiktok": "TikTok", "reels": "Reels (Instagram/Facebook)"}


def destino_cena(p, base, i, c):
    return base / c.get("clipe", f"{p['nome']}-cenas/cena{i}.mp4")


def gerar_cena(p, base, i, c, fotos):
    """Gera uma cena (edição + animação). Devolve o custo em US$."""
    custo = 0.0
    destino = destino_cena(p, base, i, c)
    destino.parent.mkdir(parents=True, exist_ok=True)
    print(f"  {p['nome']}: gerando cena {i}")
    if "editar" in c:
        png = destino.with_suffix(".png")  # imagem do Seedream guardada: refazer só o vídeo não paga a imagem de novo
        if not png.exists():
            prompt = c["editar"] + (COMPOSICAO if c.get("composicao", True) else "") + PROIBIDO
            url, n = gerar_video.com_teto("imagem", lambda: api_paga(gerar_video.MODELO_IMAGEM, {
                "prompt": prompt, "images": fotos, "size": "720*1280"}))
            custo += n * gerar_video.CUSTO_IMAGEM_USD
            gerar_video.baixar(url, png)
        if SO_IMAGENS:
            return custo
        img = gerar_video.referencia(png.name, png.parent)
    elif SO_IMAGENS:
        return custo
    else:
        img = fotos[c["foto"]]
    vid, n = gerar_video.com_teto("vídeo", lambda: api_paga(gerar_video.MODELO_VIDEO, {
        "prompt": c["movimento"] + (CAMERA_PARADA if c.get("sobrepor") else TRAVA_ANGULO), "image": img, "resolution": gerar_video.RESOLUCAO, "duration": 5,
        **gerar_video.VIDEO_EXTRA}))
    custo += n * gerar_video.CUSTO_CLIPE_USD
    gerar_video.baixar(vid, destino)
    return custo


def saldo_usd():
    with urllib.request.urlopen("https://api.wavespeed.ai/api/v3/balance", timeout=30) as r:
        return json.load(r)["data"]["balance"]


def checar_antes_de_gastar(p, base, so_imagens):
    """Travas das regras da dona (2026-10-15): qualquer erro aqui impede gastar crédito."""
    erros = []
    principal = p["fotos"][0] if p.get("fotos") else ""
    if not principal.endswith("01.jpg"):  # cor/variante sempre a da 1ª foto do anúncio
        erros.append(f"a 1ª referência precisa ser a foto principal do anúncio (01.jpg), está {principal}")
    for i, c in enumerate(p["cenas"], 1):
        txt = (c.get("editar", "") + " " + c.get("movimento", "")).lower()
        # arco curto (15-20 graus) e câmera na mão são liberados; giro grande só com "angulos_reais": true
        # (anúncio com fotos dos lados que o giro mostra), senão o modelo inventa o lado escondido
        if not p.get("angulos_reais"):
            for ruim in ("orbit", "rotate", "360", "spin", "turntable"):
                if ruim in txt.replace("does not rotate", "").replace("not rotate", ""):
                    erros.append(f"cena {i}: giro '{ruim}' sem fotos desses ângulos; use arco curto de 15-20 graus")
        for ruim in ("wine", "beer", "liquor", "cocktail", "champagne"):
            if ruim in txt and "no " + ruim not in txt:
                erros.append(f"cena {i}: bebida alcoólica no prompt ({ruim})")
        if p.get("embalagem_com_letras") and "editar" in c and "package" in c["editar"].lower():
            erros.append(f"cena {i}: embalagem com letras não pode ser redesenhada pela IA; use a foto real por código")
        if not so_imagens and "editar" in c and not destino_cena(p, base, i, c).exists():
            if not destino_cena(p, base, i, c).with_suffix(".png").exists():
                erros.append(f"cena {i}: gere e confira as imagens antes (--so-imagens)")
    if not so_imagens and not p.get("imagens_conferidas"):
        erros.append('marque "imagens_conferidas": true só depois de comparar cor, tecido, letras e forma com a 1ª foto')
    return erros


def gerar_lote(produtos):
    """Gera em paralelo todas as cenas que faltam. Devolve (custo, nomes dos produtos que falharam)."""
    tarefas = []
    problemas = []
    for p, base in produtos:
        if any(not destino_cena(p, base, i, c).exists() for i, c in enumerate(p["cenas"], 1)):
            problemas += [f"{p['nome']}: {e}" for e in checar_antes_de_gastar(p, base, SO_IMAGENS)]
    if problemas:
        raise SystemExit("Nada foi gerado. Corrija antes de gastar:\n  " + "\n  ".join(problemas))
    for p, base in produtos:
        fotos = None
        for i, c in enumerate(p["cenas"], 1):
            if destino_cena(p, base, i, c).exists():
                continue
            if fotos is None:
                fotos = [gerar_video.referencia(f, base) for f in p["fotos"]]
            tarefas.append((p, base, i, c, fotos))
    if not tarefas:
        return 0.0, set()
    def preco(t, tentativas):
        c = t[3]
        img = "editar" in c and not destino_cena(t[0], t[1], t[2], c).with_suffix(".png").exists()
        return tentativas * ((not SO_IMAGENS) * gerar_video.CUSTO_CLIPE_USD + img * gerar_video.CUSTO_IMAGEM_USD)
    esperado = sum(preco(t, 1) for t in tarefas)
    pior = min(sum(preco(t, gerar_video.MAX_TENTATIVAS) for t in tarefas), TETO_LOTE)
    saldo = saldo_usd()
    print(f"{len(tarefas)} cenas; esperado US$ {esperado:.2f}, pior caso US$ {pior:.2f}, saldo US$ {saldo:.2f}")
    if saldo < pior:
        raise SystemExit("saldo da WaveSpeed não cobre o pior caso do lote: recarregue, divida o lote ou use TETO_LOTE_USD")
    custo, falhas = 0.0, set()
    with ThreadPoolExecutor(PARALELO_GERACAO) as ex:
        futuros = {ex.submit(gerar_cena, *t): t[0]["nome"] for t in tarefas}
        for f, nome in futuros.items():
            try:
                custo += f.result()
            except Exception as e:  # noqa: BLE001  um produto com problema não para o lote
                print(f"  {nome}: {e}")
                falhas.add(nome)
    return custo, falhas


def montar_versoes(p, clipes, saida):
    cor = p.get("cor_destaque", "auto")
    if cor == "auto":  # uma cor por produto, alternando entre produtos
        cor = PALETA[sum(map(ord, p["nome"])) % len(PALETA)]
    videos = {}
    for chave, v in p["versoes"].items():
        estilo = v.get("estilo", chave)  # ex.: "shopee2": {"estilo": "tiktok", ...} = 2ª edição Shopee
        if chave == "reels" and "estilo" not in v:  # alterna os modelos de Reels entre produtos
            estilo = REELS[sum(map(ord, p["nome"])) % len(REELS)]
        ordem = v.get("ordem", list(range(len(v["cenas"]))))
        cenas = []
        for pos, (idx, txt) in enumerate(zip(ordem, v["cenas"])):
            cena = {"clipe": str(clipes[idx]), "ate": ATE_PADRAO[estilo][min(pos, 2)], **txt}
            cena.setdefault("lento", p["cenas"][idx].get("lento", LENTO_PADRAO))  # 5 s x 1.1 cobre o "ate"
            cena.setdefault("subir", p["cenas"][idx].get("subir", 0))  # px: tira o produto de baixo do texto
            cena.setdefault("escala", p["cenas"][idx].get("escala", 1.0))
            cenas.append(cena)
        nome = f"{p['nome']}_{chave}"
        m = {"nome": nome, "estilo": estilo, "cor_destaque": cor, "cenas": cenas, "selo": p.get("selo")}
        arq = saida / f"montagem_{chave}.json"
        arq.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  montando {chave} ({estilo})")
        if estilo in GSAP and p.get("gsap", True):  # texto animado em GSAP (custo zero)
            cmd = [sys.executable, str(AQUI / "gsap" / "montar_gsap.py"), str(arq), str(saida / f"{nome}.mp4")]
        else:
            cmd = [sys.executable, str(AQUI / "montar_video_pro.py"), str(arq)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        videos[chave] = (saida / f"{nome}.mp4", [c["ate"] for c in cenas])
    return videos


def escrever_legendas(p, saida):
    linhas = []
    for estilo in p.get("legendas", {}):
        rede = REDES.get(estilo, REDES.get(estilo.rstrip("0123456789"), estilo) + " (2ª edição)")
        linhas += [f"== {rede} ==", p["legendas"][estilo].replace("{link}", p.get("link", "")),
                   p.get("hashtags", {}).get(estilo, "")]
        if estilo == "reels":  # no Facebook o link vai no 1º comentário, fixado (link na legenda perde alcance)
            linhas += ["-- Comentário fixado (Facebook) --",
                       p.get("comentario", "🛒 Link do produto: {link}").replace("{link}", p.get("link", ""))]
        linhas.append("")
    (saida / "legendas.txt").write_text("\n".join(linhas), encoding="utf-8")


def quadro(video, t, larg):
    png = video.with_suffix(f".{t:.1f}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
                    "-frames:v", "1", "-vf", f"scale={larg}:-2", str(png)], check=True)
    img = Image.open(png).convert("RGB")
    png.unlink()
    return img


def folha_aprovacao(itens, arq):
    """Uma linha por vídeo: foto do anúncio + 1 quadro do meio de cada cena."""
    larg, alt, rot = 240, 427, 44
    fonte = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf", 24)
    linhas = []
    for nome, foto, video, ates in itens:
        meios, t = [], 0.0
        for i, a in enumerate(ates):
            meios.append(t + a / 2)
            t += a - 0.3
        quadros = [quadro(video, m, larg) for m in meios]
        if foto.startswith("http"):
            import io
            import urllib.request
            foto = io.BytesIO(urllib.request.urlopen(foto, timeout=60).read())
        ref = Image.open(foto).convert("RGB")
        ref.thumbnail((larg, alt))
        linha = Image.new("RGB", (larg * (len(quadros) + 1) + 10 * len(quadros), alt + rot), (245, 245, 245))
        d = ImageDraw.Draw(linha)
        d.text((10, 8), f"{nome}  |  anúncio  vs  cenas", font=fonte, fill=(30, 30, 30))
        linha.paste(ref, (0, rot + (alt - ref.height) // 2))
        for i, q in enumerate(quadros, 1):
            linha.paste(q, (i * (larg + 10), rot))
        linhas.append(linha)
    folha = Image.new("RGB", (max(l.width for l in linhas), sum(l.height + 12 for l in linhas)), (255, 255, 255))
    y = 0
    for l in linhas:
        folha.paste(l, (0, y))
        y += l.height + 12
    folha.save(arq, quality=88)


def preparar(link, nome):
    """Passo 0: baixa todas as fotos e a descrição do anúncio e monta uma folha para escolher as fotos."""
    pasta = AQUI / "lote" / f"{nome}-fotos"
    subprocess.run([sys.executable, str(AQUI.parent / "produto-campeao" / "buscar_fotos.py"), link, str(pasta)],
                   check=True)
    fotos = sorted(pasta.glob("[0-9][0-9].jpg"))
    larg, colunas = 300, 4
    folha = Image.new("RGB", (larg * colunas, larg * -(-len(fotos) // colunas)), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for k, f in enumerate(fotos):
        img = Image.open(f).convert("RGB")
        img.thumbnail((larg - 10, larg - 10))
        x, y = (k % colunas) * larg, (k // colunas) * larg
        folha.paste(img, (x + 5, y + 5))
        d.rectangle([x + 5, y + 5, x + 45, y + 35], fill=(0, 0, 0))
        d.text((x + 12, y + 10), f.stem, fill=(255, 255, 255))
    folha.save(pasta / "todas_as_fotos.jpg", quality=85)
    print(f"Folha para escolher as fotos: {pasta / 'todas_as_fotos.jpg'}")


def produzir_produto(p, base, raiz):
    print(f"Montando: {p['nome']}")
    saida = raiz / p["nome"]
    saida.mkdir(parents=True, exist_ok=True)
    clipes = []
    for i, c in enumerate(p["cenas"], 1):
        clipe = destino_cena(p, base, i, c)
        if c.get("sobrepor"):  # embalagem real colada por código; letras idênticas ao anúncio
            comp = clipe.with_name(clipe.stem + "_emb.mp4")
            if not comp.exists():
                compor_embalagem.compor(clipe, c["sobrepor"], base, comp)
            clipe = comp
        clipes.append(clipe)
    videos = montar_versoes(p, clipes, saida)
    escrever_legendas(p, saida)
    foto = p["fotos"][0]
    foto = foto if foto.startswith("http") else str(base / foto)
    return [(f"{p['nome']} · {estilo}", foto, video, ates) for estilo, (video, ates) in videos.items()]


def main():
    global SO_IMAGENS
    if sys.argv[1] == "--preparar":
        return preparar(sys.argv[2], sys.argv[3])
    args = sys.argv[1:]
    if args[0] == "--so-imagens":
        SO_IMAGENS, args = True, args[1:]
    raiz = AQUI / "saida"
    produtos = []
    for arq in args:
        arq = Path(arq).resolve()
        produtos.append((json.loads(arq.read_text(encoding="utf-8")), arq.parent))
    custo_total, falhas = gerar_lote(produtos)
    if SO_IMAGENS:
        print(f"Imagens prontas (cenaN.png ao lado dos clipes). Custo: US$ {custo_total:.3f}. Falharam: {sorted(falhas)}")
        return
    prontos = [(p, base) for p, base in produtos if p["nome"] not in falhas]
    itens = []
    with ThreadPoolExecutor(PARALELO_MONTAGEM) as ex:
        for linhas in ex.map(lambda pb: produzir_produto(*pb, raiz), prontos):
            itens += linhas
    if falhas:
        print(f"Ficaram de fora (geração falhou 2 vezes): {', '.join(sorted(falhas))}")
    folha_aprovacao(itens, raiz / "aprovacao.jpg")
    print(f"Pronto: {len(itens)} vídeos em {raiz}")
    print(f"Folha de aprovação: {raiz / 'aprovacao.jpg'}")
    print(f"Custo de geração: US$ {custo_total:.3f} (cerca de R$ {custo_total * 5.69:.2f})")


if __name__ == "__main__":
    main()
