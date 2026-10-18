---
name: edit-templates
description: Video edit templates per platform in montar_video_pro.py - all three approved by the owner (Shopee vitrine, TikTok v3, Reels), rejected looks, color rotation, fonts, files
metadata:
  type: project
---

Main editor: video-teste/montar_video_pro.py (montar_video.py is the old amateur version, don't use). Driven by a montagem.json; "estilo" picks the template. Zero cost, under 1 min per render, no Claude tokens. Fonts (OFL) in video-teste/fontes.

- **shopee** (v2 "vitrine", 2026-10-13, APPROVED by the owner): frosted-glass card fixed at the bottom (Montserrat), accent label chip, scene indicator dots, spec chips, callouts (dot + line + dark pill) pointing at product parts, wide accent CTA button with arrow, scenes slide sideways, square main-photo clip shifted up so the whole product stays above the card. Callouts need x/y per scene: place them only on scenes where the product barely moves (camera pans break them). Demo banqueta-cenas/banqueta_shopee_v2.mp4.
- **classico** (old Shopee v1, Inter Display top + pill CTA): approved earlier, but the owner said the TikTok and Reels templates are better than it; keep only as an option.
- **reels** (Instagram/Facebook) — APPROVED by the owner 2026-10-13 ("ficou ótima, salve esse modelo para futuras solicitações"): DM Serif Display title bottom-left with italic accent keyword, small uppercase letter-spaced label with accent underline, outlined white CTA pill, bottom dark gradient, slow 0.5 s fades. Demo banqueta-cenas/banqueta_reels_v1.mp4.
- **tiktok** — v2 (white caption boxes, Poppins, highlighter keyword) REJECTED as "muito amador"; never use that look. v3 (2026-10-13, APPROVED by the owner): Bebas Neue big uppercase centered near top, lines cascade in, small letter-spaced Poppins subtitle, minimal white CTA with accent dash, quick cuts with punch zoom. Demo banqueta-cenas/banqueta_tiktok_v3.mp4.

**2026-10-15 updates (the owner):** Shopee vitrine now renders with a GSAP animated text layer (gsap/montar_gsap.py, big "abertura" number in the first 1.8 s); a 2nd Shopee edit "shopee2" uses the tiktok v3 look (big letters on top) and the owner called it "perfeito". Reels letters were too small: title now 124 px, white label 44 px, sub 56 px, CTA 52 px, soft shadow; the text block starts around y 950, so scene 2 often needs escala about 0.5. Punctuation after a [highlight] is glued to it.

**Reels models (the owner, 2026-10-15 10:17):** the owner approved preview models 1 and 4 and asked to alternate between them. The old editorial reels look is retired. The models are gsap/camada_reels_faixas.html ("reels_faixas": two tilted bands, accent and black, plus a white CTA pill) and gsap/camada_reels_cartao.html ("reels_cartao": dark card, accent label, big title, full accent CTA, round badge from product "selo" {n,t}). produzir.py alternates them by product name unless versoes.reels.estilo is set. Both Shopee edits stay (shopee GSAP vitrine + shopee2 tiktok look). Previews: video-teste/previas/reels_opcoes.jpg. Per product, the researcher picks the model by retention, CTA, visual impact and proof ([[production-agents]]).

Each version gets its own original hook and CTA ([[scale-first-reuse-rule]]). Scene generation: gerar_video.py, rewritten 2026-10-13 to the fidelity recipe ([[product-fidelity-rule]]); untested live.

**Variety rule (the owner, 2026-10-13):** alternate font accent colors and edit variations from time to time so videos don't all look the same. montar_video_pro.py has PALETA (caramel, mint, coral, lilac, yellow, ice blue) and "cor_destaque": "auto" rotates it per video; prefer a color that suits the product. Also vary hook angle, label wording and which approved template a product gets, while keeping each platform's approved look.

**Facebook link placement (2026-10-14, the owner asked):** organic Facebook posts use the s.shopee.com.br affiliate link as is (no bit.ly or other shortener) in the first pinned comment; the caption says "Link no primeiro comentário 👇". produzir.py writes a "Comentário fixado (Facebook)" line under Reels in legendas.txt (product.json key "comentario", default "🛒 Link do produto: {link}"). Paid Meta ads put the link in the "Comprar agora" button. This is market practice, not a Meta rule; compare reach on the first posts.
