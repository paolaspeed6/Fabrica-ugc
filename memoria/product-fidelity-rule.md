---
name: product-fidelity-rule
description: Hard rule - product in generated videos must be identical to the Shopee listing; never generate the product from a text prompt
metadata:
  type: feedback
  modified: 2026-10-13T07:52:07.739Z
---

Product shown in every video must match the ad/listing exactly. Ad platforms (Shopee, Meta, TikTok) punish severely when the video shows a different product than the listing.

**Why:** the owner's first WaveSpeed test (2026-10-13, Z Image Turbo text-to-image + Seedance V1 Pro Fast, prompts in video-teste/teste1_prompts.md) had good quality but scenes 1 and 2 showed a completely different product than the listing, because text-to-image invents its own product.

**How to apply:** never create the product from text. Start every product scene from the real listing photos: either animate the listing photo directly (image-to-video, zero image cost) or use a reference-image edit model (WaveSpeed Seedream v4 edit ~$0.027/image, up to 10 reference images; Qwen Image Edit ~$0.02) to place the exact product in a scene (a room or a new angle). No people in generated scenes; product-only. Motion prompts must be low-motion and say the product keeps its exact shape, color and logo; avoid rotating/close morphing shots. QC step: compare a frame of each scene to the listing photo before publishing. Cost impact (WaveSpeed recipe, all 480p: 2 Seedream edits anchored on the listing's main photo + 3 Seedance animations): R$1.33 first try, ~R$1.73 with discard margin, R$2.66 worst case; a third edit to extend the square main photo to 9:16 makes it ~R$1.93 / R$2.97. 720p scenes break the R$3 cap ([[dono-baseline-cost-and-pipeline]]).

**Composite recipe (proven 2026-10-13 on the Krow Blaze bike, products with text/logos):** never let AI render the product. Seedream v4 text-to-image (bytedance/seedream-v4) makes an EMPTY side-view background; Seedance animates it with a locked camera; video-teste/compor_video.py overlays the real white-background listing photo (multiply blend, contact shadow, slow zoom by code, 1080x1920). Scene 3 = same photo on a code-made gray studio backdrop (free). ~US$0.174 = ~R$0.99/video. Failures that led here: Seedream edit turned the bike to 3/4 and wrote "KROI"; Seedance animating the bike pushed in hard despite "very slow" and rewrote BLAZE as "ELRM"; Seedream edit of the brush added a second brush head ("stands upright on its base" prompt). Needs a clean white-background main photo (badges/collages break the cutout).