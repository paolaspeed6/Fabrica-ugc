---
name: no-repeat-errors-rules
description: the owner 2026-10-15/16 - never repeat generation or edit errors; full checklist in agentes/regras_de_erros.md; per-scene CODE vs AI decision before spending; 3 different Shopee layouts
metadata:
  type: feedback
  modified: 2026-10-16T08:54:22.818Z
---

the owner (2026-10-15 22:56, again 2026-10-16 06:56 for the next list: cortina, lava e seca...): never repeat generation or edit errors; get maximum quality from scripts and prompts. Full checklist: agentes/regras_de_erros.md (read before any script, prompt, generation or edit); roteirista.md and produtor.md point to it; dated lessons in agentes/licoes.md. Builds on [[code-motion-on-real-photo]], [[edit-layout-checks]], [[ask-before-quality-or-cost-change]], [[listing-match-rules]].

**Biggest lesson (lista1015):** many paid AI scenes were later thrown away and replaced by code zoom on the real photo. The script now marks each scene CODE (default; mandatory for lettering, panels, structure, printed fabric, mechanism close-ups) or AI (only empty settings or plain products with a clean cutout, with max cost and the owner's OK).

**Layouts (the owner 2026-10-16 03:43, "layouts variados para testar o que mais converte"):** Shopee 1 = faixas (reels_faixas), Shopee 2 = big letters on top with the product between title and button (tiktok_b, strong top gradient), Shopee 3 = dark card with badge (reels_cartao); Reels = faixas with the link in the caption. Builder video-teste/fazer_b.py. Vitrine retired.

**Captions (2026-10-16):** no generic #achadinhosshopee; 4 niche hashtags.

**Claims (the owner 2026-10-16 08:54, "erros custam dinheiro"):** every on-screen or caption claim (number, material, feature, color) must be WRITTEN in the listing title or description; a model name is not a feature ("Starry" became "projeta estrelas"). Run video-teste/checar_textos.py plus a term check against anuncio.json before rendering. Rule 3.6 in regras_de_erros.md.

**Part counts (the owner 2026-10-17, "tira nossa monetização"):** the q19 steel shelf (5 shelves) came out with 6 in an AI scene. Every countable part (shelves, tiers, drawers, rings, kit pieces) goes in the JSON as "contagem" from the listing and photo 01. Products with repeated parts are CODE only; gallery photos must show the same count. Count the parts in one frame per scene per version before delivery. Section 1.1 of regras_de_erros.md.

**Static product, moving camera (the owner 2026-10-17, 100% of videos):** what converts is the product standing still while the camera moves. The product never moves, turns, opens or sways. AI prompts describe only camera motion with the product perfectly still. Code motion (the whole frame moving like a camera) already follows this. Rule in regras_de_erros.md and produtor.md.

**No exact rating or review count (the owner 2026-10-17):** they change over time; use "bem avaliado", "nota alta", "milhares de avaliações"; the selo becomes a word (TOP avaliado). video-teste/sem_nota.py, called by fazer_lista.py, blocks the render if one appears. Rule 3.7.

**Why:** wasted generations and edits cost the owner money and trust.
**How to apply:** before delivering, view a contact sheet of every scene of all 4 versions; run long renders with Bash run_in_background (nohup workers died between turns).
