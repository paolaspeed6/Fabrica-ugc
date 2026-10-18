---
name: product-sniper
description: Tinder-style Product Sniper page (the owner 2026-10-17): where cards live, how the search runs, status flow into the factory, Sub ID per version
metadata:
  type: project
  modified: 2026-10-17T02:00:22.808Z
---

the owner (2026-10-17) asked to automate the factory like a YouTube video he liked: a Product Sniper finds products, he swipes cards on a Tinder-like page, approved ones flow through the factory.

- PAGE: (página do seu projeto) ("Product Sniper", pinned). Cards are docs in db collection `cartoes` (read/write with ArtifactData; never republish to change data). Source html: thread scratchpad only; read the artifact before republishing from another session.
- CARD FIELDS: nome, foto_data (jpeg ~500 px base64; move to assets before the db grows past a few hundred cards), preco, nota, avaliacoes, link, shopId, itemId, pasta (produto-campeao/sniper/produtos/<id>/ with photos + anuncio.json), tiktok{vendas_7d, criadores, comissao, lancado}, motivo, angulo (Blue Ocean, listing facts only), pontos (sort), status, decidido_em, versoes{<versao>:{sub_id, link}}.
- STATUS: novo → aprovado/descartado (the owner swipes; undo exists) → produzindo → pronto → postado (Claude sets produzindo/pronto; the owner's "Já postei" button deletes the version assets and sets postado).
- TABS (the owner 2026-10-17): Escolher, Fábrica (progress bar from field etapa 0-4 = Roteiro, Cenas, Checagens, Render, Pronto, plus etapa_nota; when pronto each versoes.<shopee|shopee2|shopee3|reels> = {video:"/_blob/<id>", asset_id, tam, legenda, sub_id, link} with Download via downloads capability), Descartados. Upload mp4s with Artifact publish asset:true to this page's url, ~5 MB each. Capabilities: db, assets, downloads. A posting tab (TikTok first) comes only after the creation model is validated (the owner). Sub ID format <produto>-<versao>-<AAMMDD>; see [[production-agents]] and agentes/orquestrador.md.
- SEARCH: produto-campeao/sniper.py <candidatos.json> <saida.json>. Candidates come from FastMoss product_search (region BR, categories 11/16/17, 7-day sales 100+, creators ≤50, commission 10%+, R$ 30-150); Kalodata (KaloPilot) is the other source. Shopee crawler search is loose: candidates need "precisa" words and still need a human-eye check of the match; a known listing goes in "shopee_link". First run 2026-10-17: 12 FastMoss hits, only 4 had a true Shopee match (moedor temperos, fone dormir, power bank 22,5 W, caneca térmica 1200 ml); pet category returned 0; wine opener dropped ([[no-alcohol-rule]]).
- No recurring run without the owner's OK ([[dono-step-by-step-minimal-cost]]).
- MANUAL (2026-10-17): agentes/manual_video_vencedor.md says TikTok Shop BR winners are cheap (median R$ 20, aim R$ 10-40 for TikTok picks, vs Shopee filter R$ 30-150) and orders per 1,000 views beat views; consider a separate TikTok price band when the owner next tunes the Sniper.
