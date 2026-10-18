"""a dona 2026-10-17: nota e numero de avaliacoes mudam com o tempo, entao nunca aparecem exatos no video nem na legenda.
Use frases como "bem avaliado", "nota alta", "milhares de avaliacoes" (so se o anuncio tiver mais de 1.000).
checar(p, anuncio) devolve a lista de textos proibidos; vazia = ok."""
import re

PADROES = [
    r"\b[1-5][.,]\d{1,2}\s*(de\s+)?(nota|estrela|★|⭐)",  # 4,8 de nota
    r"\bnota\s*\d",                                 # nota 5
    r"\d[\d.]*\s*(mil\s+)?(avalia|review|estrela)",  # 2.104 avaliacoes, 5 estrelas
]


def textos(p):
    out = []
    for v in p.get("versoes", {}).values():
        for c in v.get("cenas", []):
            for k in ("rotulo", "titulo", "sub", "cta"):
                if c.get(k):
                    out.append(c[k])
            out += c.get("fichas", [])
            ab = c.get("abertura")
            if ab:
                out += [ab.get("grande", ""), ab.get("texto", "")]
    out += list(p.get("legendas", {}).values())
    if p.get("selo"):
        out.append(f'{p["selo"].get("n", "")} {p["selo"].get("t", "")}')
    return out


def checar(p, anuncio=None):
    ruins = []
    exatos = []
    if anuncio:
        for k in ("nota", "avaliacoes"):
            if anuncio.get(k):
                s = str(anuncio[k])
                if k == "nota":
                    exatos += [s.replace(".", ","), s]
                else:
                    n = int(float(s))
                    exatos += [f"{n:,}".replace(",", "."), str(n)] if n >= 100 else []
    for t in textos(p):
        limpo = re.sub(r"https?://\S+", "", t)
        if any(re.search(r, limpo, re.I) for r in PADROES) or any(e and re.search(r'(?<![\d.,])' + re.escape(e) + r'(?![\d]|[.,]\d|\s*(m|cm|mm|kg|x)\b)', limpo) for e in exatos):
            ruins.append(t)
    return ruins
