---
name: reference-videos-quality-bar
description: the owner's 14 reference videos (2026-10-14) defining the minimum quality bar - photoreal handheld product videos, 2 rooms, native captions
metadata:
  type: feedback
  modified: 2026-10-14T01:26:25.001Z
---

the owner sent 14 reference videos on 2026-10-14: "quero que fique com no mínimo essa qualidade". If WaveSpeed can't reach it, the owner is open to another tool. Copies: referencias/ (os 14 vídeos de referência que ela anexar).

What they share (checked frame by frame):
- Products: home/furniture (bar stools, armchairs, dining chairs, manicure chair, office chair, burlap bags) and one sneaker with an "IRON" logo that stays consistent. Usually 2 units of the product in the scene.
- 720x1280 (or 720x1296), 30 fps, 6 to 18 s, almost all with audio.
- Structure: 2 scenes of about 6 s each, each in a DIFFERENT photoreal room (Scandi or Mediterranean interior, natural window light, wood or terracotta floor, plants, ceramics). Product identical in both.
- Camera: realistic handheld smartphone feel. Slow push-in, a lateral arc or orbit around the product, a close pass over details. Never static. Looks shot on an iPhone, not CGI.
- Text: one short line per scene in the native TikTok caption style (small white bold text, thin black outline, centered in the upper third, a letter-scatter animation). Scene 1 is the hook ("POV: finalmente encontrou...", "Manicure, você PRECISA ver isso"). Scene 2 is the CTA ("Clica no carrinho e confere quanto tá saindo"). There are NO designed templates; the look is native UGC.

**Update (the owner, same day):** the references are the owner's OLD 2-scene videos. the owner now makes 3-scene videos and noticed those become winning ads ("anúncio campeão") more easily. Use 3 scenes of about 5 s each (= 15 s, [[video-length-15s]]) with the same look.

**Text decision (the owner, same day):** keep OUR approved text templates ([[edit-templates]]: shopee vitrine, tiktok v3, reels), not the native caption style. Only the scenes and the image quality must match the references.

**720p models on WaveSpeed (GET /api/v3/models, base price per 5 s):** Kling v3 turbo std US$0.112 (~R$2.40 per 3-scene video with 3 Seedream edits); Seedance v1 pro fast at 720p ~US$0.12 (~R$2.50); hailuo-02 fast US$0.10; Seedance 1.5 pro fast US$0.20, Kling 2.5 turbo std US$0.21, Veo 3.1 lite US$0.30, Seedance 2.0 US$0.50+ (all over the R$3 cap at 3 scenes). Little room for redos under the cap.

**PRICE TRAP (verified 2026-10-14 by saldo: veja no painel.56. Always verify a model's real charge with one short call and the balance before quoting. Seedance pro fast 480p really is US$0.06 per 5 s clip.

**First 720p video (2026-10-14, SOYO RX580 graphics card, the owner approved production):** 4 Seedream edits (1 redo) + 3 Kling v3 turbo std 5 s clips = US$1.79 (~R$10.2), OVER the R$3 cap. Quality looked faithful and realistic (handheld arcs, fans spinning in the case). Files: video-teste/placa-cenas/, lote/placa.json, saida/placa/. To hit exactly 15 s with 5 s clips: "lento" 1.1 and per-version "ate" shopee 5.27 / tiktok 5.08 / reels 5.33.

**CHOSEN 720p MODEL (2026-10-14, measured by balance):** Seedance 1.5 pro fast (bytedance), 720p, 9:16, generate_audio false = US$0.10 per 5 s clip; good handheld look, product faithful. Seedance v1 pro fast 720p = US$0.12, bad (over-zoom, ghost person). Recipe: 3 Seedream v4 edits + 3 Seedance 1.5 fast clips = US$0.381, about R$2.17 per video (R$2.74 with one redo). Note: the /models list price for 1.5 fast (US$0.20) did not match the real charge; always measure.

**APPROVED (the owner, 2026-10-14 03:22, "esse modelo ficou ótimo"):** Seedance 1.5 pro fast 720p is the production video model.

**COMPOSITION AND TEXT RULES (the owner, 2026-10-14, after the SOYO video):** on-screen text must never cover the product, especially at the start. In Seedream edits, put the product in the center (about 30-65% of frame height), clear of the template text zones: Shopee card at the bottom (73-92%), TikTok title at the top (8-22%) plus CTA (62-68%), Reels at bottom-left (63-90%). Check the first frames of every version. Scene 1 text must show the product NAME and MODEL clearly (e.g. "SOYO RX580 8GB"), because electronics buyers want to confirm the model.

**How to apply:** this replaces the 3-scene 480p plan and the static composite recipe. Likely needs 720p plus a stronger image-to-video model fed with a photoreal product-in-room start image. Check cost against the R$3 cap. Related: [[bike-live-test]], [[product-fidelity-rule]], [[edit-templates]], [[video-length-15s]].

**New references (the owner, 2026-10-18): 16 finished factory videos in referencias/** (q09 mesa Yon, q10 fogão industrial 6 bocas, q11 prateleira industrial kit, q12 kit roll-on Tropfen, q15 prateleira 5 tábuas, q16 mesa quadrada 80). All 1080x1920, 30 fps, 15 s (some 15.77 s), 3 scenes of 5 s, our templates:
- shopee: hook on dark gradient band at the bottom, 2-tone bold text (white + colored highlight box: orange, purple or red), small kicker line above (brand · model or size).
- shopee2: big condensed letters at the top (white + one colored word), small spaced subline, white "Toque no carrinho" pill at the end.
- shopee3: dark rounded card at the bottom, kicker + bold sentence with a colored keyword, final card has a colored CTA button.
- reels: same bottom band as shopee, CTA "Link na legenda".
- Scene 2 is usually a closer view or a different angle of the same product scene; scene 3 returns to the hero shot. Product never covered by text. Highlight color matches the product/scene (orange for the stove, purple for the lavender oils, gold for wood).
- WARNING: these videos show exact ratings and review counts ("Nota 4,83", "415 avaliações", "254 avaliações · Nota 4,88"). They predate rule 7 in agentes/regras_de_erros.md (2026-10-17). Copy the look, NOT those texts: use "bem avaliado" / "nota alta" instead.
