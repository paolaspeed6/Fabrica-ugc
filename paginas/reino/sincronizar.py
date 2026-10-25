#!/usr/bin/env python3
"""Monta o estado real do Reino (doc reino/estado do jogo) a partir dos dados das páginas.

Não muda nada na produção: só LÊ os dados exportados e escreve um JSON.

Uso (o Claude faz isso quando a dona pede "Atualiza o reino"):
  1. Exportar com ArtifactData (list, out_dir=<pasta>):
       Tinder      coleção candidatos  -> <pasta>/candidatos/*.json
       Conferência coleção conferir    -> <pasta>/conferir/*.json
       Postagens   coleção posts       -> <pasta>/posts/*.json
  2. python3 -I paginas/reino/sincronizar.py <pasta> [saida.json]
  3. ArtifactData set: coleção "reino", doc "estado", file_path=saida.json, na URL do jogo.

O que os dados não mostram (lote em produção, tarefas agendadas, erro) fica em
paginas/reino/manual.json, que o Claude atualiza a cada passo do lote.
"""
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BR = timezone(timedelta(hours=-3))
PRODUCAO = ["capataz", "fichador", "roteiro", "estudio", "fiscal_imagem", "camera", "fiscal_video", "edicao"]
VALIDOS = {"trabalhando", "sua_vez", "aguardando", "concluido", "erro"}
DECIDIDOS = {"ok", "editar", "descartar", "esgotado"}


def ler(pasta, nome):
    p = Path(pasta) / nome
    if not p.is_dir():
        return None  # não exportado: a etapa fica sem notícia (não inventa)
    out = []
    for f in sorted(p.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            d["_id"] = f.stem
            out.append(d)
        except (OSError, ValueError):
            pass
    return out


def dia_br(iso):
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(str(iso).replace("Z", "+00:00")).astimezone(BR).strftime("%Y-%m-%d")
    except ValueError:
        return str(iso)[:10]


def curto(nome, n=46):
    nome = " ".join(str(nome or "").split())
    return nome if len(nome) <= n else nome[: n - 1].rstrip() + "…"


def plural(n, um, varios):
    return f"{n} {um if n == 1 else varios}"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pasta = sys.argv[1]
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(pasta) / "reino_estado.json"
    manual = json.loads((AQUI / "manual.json").read_text(encoding="utf-8"))
    cand, conf, posts = ler(pasta, "candidatos"), ler(pasta, "conferir"), ler(pasta, "posts")
    etapas, recentes = {}, []
    auto = manual.get("automaticas", {})
    lote = manual.get("lote") or None
    lote_min = int(manual.get("lote_min", 15))

    # 1 Tinder e 2 Fila
    if cand is not None:
        escolher = [c for c in cand if c.get("status") not in ("aprovado", "descartado", "pronto", "produzindo")]
        aprovados = [c for c in cand if c.get("status") == "aprovado"]
        if escolher:
            etapas["tinder"] = {"estado": "sua_vez", "qtd": len(escolher),
                                "texto": plural(len(escolher), "cartão novo", "cartões novos") + " esperando você arrastar.",
                                "itens": [curto(c.get("nome")) for c in escolher[:6]]}
        else:
            v = auto.get("varredura", {})
            etapas["tinder"] = {"estado": "aguardando", "qtd": 0,
                                "texto": "Nenhum cartão novo. " + ("A varredura traz mais amanhã cedo." if v.get("ligada") else "A varredura diária ainda não está ligada.")}
        if lote:
            etapas["fila"] = {"estado": "concluido", "qtd": len(aprovados),
                              "texto": f"Lote liberado. {plural(len(aprovados), 'produto continua', 'produtos continuam')} na fila para o próximo."}
        elif len(aprovados) >= lote_min:
            etapas["fila"] = {"estado": "sua_vez", "qtd": len(aprovados),
                              "texto": f"{len(aprovados)} produtos aprovados esperando o seu OK. Peça o custo do lote antes (teto por produto).",
                              "itens": [curto(c.get("nome")) for c in aprovados[:6]]}
        else:
            etapas["fila"] = {"estado": "aguardando", "qtd": len(aprovados),
                              "texto": f"{plural(len(aprovados), 'produto', 'produtos')} na fila. O lote abre com {lote_min}."}
        por_dia = defaultdict(lambda: [0, 0])
        for c in cand:
            d = dia_br(c.get("decidido_em"))
            if d and c.get("status") in ("aprovado", "descartado", "pronto"):
                por_dia[d][0 if c.get("status") != "descartado" else 1] += 1
        for d, (a, x) in por_dia.items():
            recentes.append({"quando": d, "etapa": "tinder", "texto": f"No Tinder você aprovou {a} e descartou {x} produtos."})

    # 3-10 Produção
    if lote:
        atual = lote.get("etapa")
        idx = PRODUCAO.index(atual) if atual in PRODUCAO else -1
        prods = [curto(p) for p in lote.get("produtos", [])]
        for i, eid in enumerate(PRODUCAO):
            if i < idx:
                etapas[eid] = {"estado": "concluido", "qtd": 0, "texto": f"{lote.get('nome', 'Lote')}: etapa feita."}
            elif i == idx:
                erro = lote.get("erro")
                etapas[eid] = {"estado": "erro" if erro else "trabalhando", "qtd": len(prods), "itens": prods[:6],
                               "texto": erro or f"{lote.get('nome', 'Lote')}: trabalhando em {plural(len(prods), 'produto', 'produtos')}."}
            else:
                etapas[eid] = {"estado": "aguardando", "qtd": 0, "texto": f"Espera a etapa anterior do {lote.get('nome', 'lote')}."}
    else:
        ult = manual.get("ultimo_lote")
        for eid in PRODUCAO:
            etapas[eid] = {"estado": "aguardando", "qtd": 0,
                           "texto": "Sem lote em produção agora." + (f" Último: {ult}." if ult else "")}

    # 11 Conferência e 15 Melhorador
    if conf is not None:
        pend = [c for c in conf if c.get("status") in (None, "", "pendente")]
        nao_proc = [c for c in conf if c.get("status") in DECIDIDOS and not c.get("processado")]
        if pend:
            etapas["conferencia"] = {"estado": "sua_vez", "qtd": len(pend),
                                     "texto": plural(len(pend), "vídeo esperando", "vídeos esperando") + " a sua conferência.",
                                     "itens": [curto(c.get("produto")) for c in pend[:6]]}
        elif nao_proc:
            etapas["conferencia"] = {"estado": "concluido", "qtd": 0,
                                     "texto": f"Você decidiu {plural(len(nao_proc), 'vídeo', 'vídeos')}. Falta o Claude processar: peça \"Terminei a Conferência, processa\".",
                                     "itens": [f"{curto(c.get('produto'), 38)}: {c.get('status')}" for c in nao_proc[:6]]}
        else:
            etapas["conferencia"] = {"estado": "aguardando", "qtd": 0, "texto": "Nada para conferir agora."}
        etapas["melhorador"] = {"estado": "aguardando", "qtd": 0,
                                "texto": "Roda uma vez por lote, depois que o Claude processar a sua Conferência."}
        por_dia = defaultdict(int)
        for c in conf:
            if c.get("status") in DECIDIDOS:
                por_dia[(dia_br(c.get("decidido_em")), c.get("lote", ""))] += 1
        for (d, lt), n in por_dia.items():
            if d:
                recentes.append({"quando": d, "etapa": "conferencia", "texto": f"Você conferiu {plural(n, 'vídeo', 'vídeos')} da {lt or 'lista'}."})

    # 12 Postagens
    if posts is not None:
        fila = [p for p in posts if p.get("status") != "postado" and not p.get("auto")]
        if fila:
            etapas["postagens"] = {"estado": "sua_vez", "qtd": len(fila),
                                   "texto": plural(len(fila), "vídeo pronto", "vídeos prontos") + " para você postar na Shopee.",
                                   "itens": [curto(p.get("produto")) for p in fila[:6]]}
        else:
            etapas["postagens"] = {"estado": "aguardando", "qtd": 0, "texto": "Nenhum vídeo na fila de postagem agora."}
        por_dia = defaultdict(int)
        for p in posts:
            if p.get("status") == "postado":
                por_dia[dia_br(p.get("postado_em"))] += 1
        for d, n in por_dia.items():
            if d:
                recentes.append({"quando": d, "etapa": "postagens", "texto": f"{plural(n, 'vídeo postado', 'vídeos postados')}."})

    # 13 Postador Meta e 14 Analista
    r = auto.get("reels", {})
    etapas["postador_meta"] = {"estado": "trabalhando" if r.get("ligada") else "aguardando", "qtd": 0,
                               "texto": r.get("texto") or ("Postando os Reels no ritmo seguro." if r.get("ligada") else "Parado.")}
    etapas["analista"] = {"estado": "aguardando", "qtd": 0, "texto": manual.get("analista", "Liga junto com a leitura de vendas por Sub ID.")}

    # Correções manuais (erro, pausa) ganham de tudo
    for eid, e in (manual.get("etapas") or {}).items():
        if e.get("estado") in VALIDOS:
            etapas[eid] = {**etapas.get(eid, {"qtd": 0}), **e}

    recentes += manual.get("recentes", [])
    recentes.sort(key=lambda x: x.get("quando", ""), reverse=True)
    doc = {
        "atualizado_em": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "fonte": "paginas/reino/sincronizar.py",
        "etapas": etapas,
        "automaticas": {k: {"ligada": bool(v.get("ligada")), "texto": v.get("texto", "")} for k, v in auto.items()},
        "recentes": recentes[:12],
    }
    saida.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok: {saida}  ({len(etapas)} etapas, {len(doc['recentes'])} novidades)")
    for k, v in etapas.items():
        print(f"  {k:14} {v['estado']:11} {v.get('qtd', 0):>3}  {v['texto'][:70]}")


if __name__ == "__main__":
    main()
