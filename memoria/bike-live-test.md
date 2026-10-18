---
name: bike-live-test
description: First live WaveSpeed test (Krow Blaze aro 29 bike, 2026-10-13) - what failed, composite recipe the owner rejected as static, costs, model options, Apify plan
metadata:
  type: project
  modified: 2026-10-13T09:26:28.377Z
---

Product: Krow Blaze aro 29 bike (Shopee 901067314/58253674993), main photo only (white bg) in video-teste/bike-fotos/A_principal.png; script lote/bike.json; outputs saida/bike/.

**Failures (text/logo products):** Seedream v4 edit with a part-by-part description turned the bike to 3/4 and wrote "KROI". Seedance animating the bike (composite or listing photo) pushed in hard despite "very slow" and rewrote BLAZE as "ELRM". A better description doesn't fix it: cheap models redraw small letters every frame.

**Composite recipe** (details in [[product-fidelity-rule]]): 100% faithful, but the owner rejected the result as "estático, amador", unlikely to convert. the owner wants cinema realism: near-360 orbit around the product, beautiful location, realistic light. Limit: one photo shows one side, so 360 invents the other sides.

**Costs:** US$0.381 total on the bike (0.174 used, 0.207 discarded tests); plus US$0.027 brush edit (it added a fake second brush head) and an unexplained US$0.06. saldo: veja no painel.

**OpenCV tracking test** (free, on a discarded Seedance clip): global SIFT homography to paste the real KROW/BLAZE patches failed on close zoom frames (still "ELRM", line artifacts). Might work on gentle moves; unproven. Prototype only in a scratchpad, not saved.

**WaveSpeed GET /api/v3/models** lists every model with price and schema. Options: Kling v3 turbo std i2v US$0.112/5s at 720p; pixverse v6 transition (start+end frame) from US$0.025; vidu q2-pro start-end-fast US$0.08; bria/embed-product US$0.04; Seedance v1 pro fast has camera_fixed and 480p/720p/1080p. Idea offered to the owner (not chosen yet): anchor both first and last frame with the real product; or a 30-45° half orbit on Kling v3 720p, about R$0.64 per scene.

**the owner chose:** don't generate; find all listing photos. Shopee hosts (shopee.com.br, down-br.img.susercontent.com) are blocked by the proxy. Apify Shopee BR scrapers (lergassy, xtracto, khadinakbar) cost ~US$5-7 per 1000 products, pay per result; free plan US$5/month, no card. Open: does the full gallery come back for BR listings (one scraper warns many return only card data)? Next step given to the owner: Apify account, token as network secret (api.apify.com), allow api.apify.com + down-br.img.susercontent.com together, then test with the bike. Video length rule: [[video-length-15s]].
