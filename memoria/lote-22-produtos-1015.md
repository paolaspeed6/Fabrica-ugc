---
name: lote-22-produtos-1015
description: Result of the owner's 2026-10-15 list of 22 products (66 videos): where files and pages are, cost, open issues
metadata:
  type: project
---

the owner's second batch (23 links, 22 products) was produced 2026-10-15 in lean mode: JSONs in video-teste/lote/lista1015/qNN.json, outputs in video-teste/saida/qNN_*/ (3 videos each), summary in lote/lista1015/LISTA.md.

Cost: Seedream images US$ 0.84 + animation US$ 6.60 (66 clips) = about US$ 7.44, about US$ 0.34 per product ([[dono-baseline-cost-and-pipeline]]). 7 AI scenes that came out unfaithful (q03, q05, q14, q15, q16, q18) were replaced by the animated listing photo. WaveSpeed saldo: veja no painel

Delivery (updated 19:30): all 66 videos are on the ONE pinned page (página do seu projeto), newest first. They are stored as artifact ASSETS (capability assets, 20 MiB each, 25 per upload call, urls /_blob/<id>) because 533 MB do not fit the 256 MB page limit; the page keeps its older videos as page files. the owner did not want separate pages. The 3 earlier part pages (8tiDCjd4mj7B51aNCQgNmm, KPixFyDMuufWwCoAgnM7op, 5jmZpxfSHRU5msAkopt6zA) are obsolete and had a JS syntax bug; delete them only with the owner's OK. To add videos later: upload as assets to the pinned url, add entries at the top of VIDEOS in scratchpad hoje-page/index.html with arq set to the /_blob url, republish.

Fixes made: cor_destaque must not start with "#"; dark accent colors are lightened; `subir` now also lifts square (foto) scenes in montar_video_pro.py (used to keep the product above the Reels card); the Reels badge subtitle shrank to 17 px so "NNN AVALIAÇÕES" fits.

Open issues (free to fix, new clips cost US$ 0.10 each, ask the owner first): q23 scene 2 uses a listing photo with baked-in text that clashes with our title; q03 scene 2 likewise; q09 shopee scene 1 crop too tight; q22 shopee2 scene 2 cuts the machine at the edge; q06 pad scene shows a phone; q08 listing photo shows a hand.
the owner's rules: no paid API for now, ask before any quality-lowering or extra-cost action ([[ask-before-quality-or-cost-change]]).
