---
name: edit-layout-checks
description: the owner 2026-10-15 defects found in the 22-product batch and the checks that must run on every finished video
metadata:
  type: feedback
---

the owner found these after the batch (he said he thought they were already saved):
1. Text card over the product in Reels (seladora scenes 1-2): square listing-photo scenes sat under the card. Fixed: Reels styles now lift square scenes by default (ESTILOS desloc -320 in montar_video_pro.py). Check EVERY scene, not one frame.
2. Overlapping letters in the Shopee card (Padliz scene 3): the highlight padding made the title wrap to 2 lines while the code counted 1, so the chips landed on the title. Fixed in gsap/camada_shopee.html (safer wrap width, chips placed under the real title height).
3. Small lettering garbled when the angle changes (Shopito and any lettered package/panel): Seedance distorts small print when animating a listing photo. NOT yet fixed; planned fix after the owner lists all defects: motion done by code (zoom/pan) on the real photo for lettered products, no AI animation.
4. AI scenes inventing parts (mesa Yon scene 3: screws and hinges on the legs): replace with the animated listing photo or code motion; decision card posted (US$ 0.50 for 5 scenes).

**Why:** fidelity to the listing and readable text are the owner's hard rules ([[listing-match-rules]], [[product-fidelity-rule]]).
**How to apply:** before delivering, sample frames at 1 s, mid and end of every scene in all 3 versions; the same checklist is in agentes/ficha_rapida.md. the owner wants to list all defects first, then a more precise process ([[lote-22-produtos-1015]]).

5. FIRST TAKE RULE (the owner 2026-10-15 19:58): the product must show COMPLETE in take 1, clean and clear, with no zoom that crops it and nothing (objects, text) covering it. Desk q09 scene 1 was replaced by a code-made slow zoom (ffmpeg zoompan) on the full listing photo: lote/lista1015/mesa_yon_120-cenas/cena1_codigo.mp4, free. A scene `clipe` pointing at an existing mp4 skips generation, so code-made clips can replace AI clips. Many other first takes still use a Seedance push-in on a crop; to audit and fix with the general precision pass.
