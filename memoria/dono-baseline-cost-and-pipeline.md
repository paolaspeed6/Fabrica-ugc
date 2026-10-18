---
name: dono-baseline-cost-and-pipeline
description: the owner's current UGC method costs ~R$1.50/video (image per scene -> image-to-video, ~3 scenes); all recommendations must be compared to that
metadata:
  type: project
  modified: 2026-10-13T07:51:44.163Z
---

As of 2026-10-13 the owner already produces UGC semi-manually at ~R$1.50 per video: generates one image per scene, animates each with image-to-video, ~3 scenes per video, edits and finishes by hand. Sells via Shopee shop, Meta Ads, TikTok, Reels. Wants to scale (next target: about 50 videos per day) without the cost rising much; will pay more only for real productivity gains.

**Why:** avatar UGC tools (Creatify R$9-21, Arcads ~R$60, HeyGen ~R$1.30-2.70 per 15-30s) are mostly above the owner's baseline, so the plan centers on automating the owner's own hybrid pipeline via pay-per-use APIs. the owner set a hard ceiling of R$3 per finished video (2026-10-13). Provider: WaveSpeed (wavespeed.ai, US$1 free credit, no card); the owner rejected fal.ai over its US$10 minimum deposit, so fal recipes and prices are not the plan. Recipe per video: 2 Seedream v4 Edit images anchored on the Shopee listing's main photo (US$0.027 each) + 3 Seedance 1.0 Pro Fast animations of 5 s at 480p (US$0.06 each). Everything stays 480p; 720p scenes break the ceiling. At R$5.50 + 3.5% IOF = R$5.69 per US$: R$1.33 per finished video if everything succeeds first try, ~R$1.73 with a fair discard margin (redo ~1 in 3), R$2.66 worst case (every item made twice, the cap). With a third edit to extend the square main photo to 9:16: ~R$1.93 with margin, R$2.97 worst case. Editing, on-screen text and CTA are free (video-teste/montar_video.py). Seedance 2.0, MiniMax H3, Kling, Veo are too expensive for the cap. the owner's current tools come from a bundled "box" of AI tool access that can't be automated, which is why the API route matters.

**How to apply:** always quote costs per finished video incl. discards, side by side with R$1.50. Plan doc: (página do seu projeto) (thread "Stack e plano de UGC com IA"). Niches (casa, tecnologia, pet), volume target and format (13-15 s vertical, product-only scenes with no people, on-screen text, no voice-over yet) are known now, not open questions. Never generate the product from a text prompt; see [[product-fidelity-rule]].

**Counting rule (the owner, 2026-10-15 11:58):** the 3 edits from one 3-scene generation (2 Shopee + 1 Reels/TikTok) count as ONE video, so always quote cost per product/generation (about US$ 0.34 = R$ 1.92 on the 22-product list), never divided by 3. "50-100 vídeos por dia" means 50-100 products a day.
