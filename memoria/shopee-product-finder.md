---
name: shopee-product-finder
description: Automated Shopee product research via official Shopee Affiliate Open API; script at produto-campeao, blocked on network + credentials
metadata:
  type: project
  modified: 2026-10-13T07:53:30.753Z
---

the owner wants product research automated and done by Claude; the owner doesn't search by hand or send candidate lists (per-product manual work doesn't scale for the owner). Route chosen 2026-10-13: free official Shopee Affiliate Open API (GraphQL, https://open-api.affiliate.shopee.com.br/graphql, productOfferV2, SHA256 signature of AppId+timestamp+payload+secret). Returns sales total, ratingStar, commissionRate, price, offerLink. Does NOT return listing creation date, affiliate count or review dates; those are checked only on finalists. Recent sales = delta of total sales between daily snapshots.

Script: produto-campeao/buscar_produtos.py (untested against the live API). Filters: rating 4.7+, 100+ sold, commission 10%+, price R$30-150; score 0-10; writes ranking.csv and snapshots/.

**Blockers (as of 2026-10-13):** the owner requested Open API access in the Shopee Afiliados panel (manual approval); waiting for Shopee to approve it is the current next step. Project ran on the built-in cloud env, which denied shopee hosts (403 at proxy); the owner must add a cloud environment allowing open-api.affiliate.shopee.com.br and shopee.com.br, storing keys as env vars SHOPEE_APP_ID / SHOPEE_APP_SECRET. Never take keys in chat. Related: [[dono-step-by-step-minimal-cost]].

Update 2026-10-13: Niches: casa, tecnologia, pet (starter keywords in produto-campeao/palavras.txt). Video test script at video-teste/gerar_video.py (ffmpeg concat; untested live).

Update 2026-10-13 05:20: the owner rejected fal ($10 minimum top-up too expensive for a test). Switched video provider to WaveSpeed: $1 free credits on signup, no card; Seedance V1 Pro Fast i2v $0.06 (480p) / $0.12 (720p) per 5s, Seedream v4 Edit $0.027/image (Z Image Turbo, $0.005, is text-to-image: not for products). API: POST https://api.wavespeed.ai/api/v3/<model>, Bearer WAVESPEED_API_KEY, poll /predictions/<id>/result. gerar_video.py now targets WaveSpeed (cloud env must also allow its API host; key as env var). First test (manual on the WaveSpeed site, prompts in video-teste/teste1_prompts.md, escova elétrica de limpeza, ~R$1.45) used text-to-image and showed a different product, see [[product-fidelity-rule]]. WaveSpeed is ~15% pricier per clip than fal; current recipe and costs: [[dono-baseline-cost-and-pipeline]].

**the owner's winning filter (2026-10-13, the owner asked to save it for every future product search):** products RECENTLY ADDED to Shopee that already have RECENT, POSITIVE reviews have few competing affiliates. Prioritize them in every search, alongside few affiliates and recent sales. How to apply: the API has no listing creation date, so treat as "new" the items that first appear in our daily snapshots with low total sold but fast-growing sales delta; then confirm listing age and review dates/sentiment on the finalists. Score these higher in buscar_produtos.py once the API is live.

**Full listing photos, free (2026-10-14, works):** produto-campeao/buscar_fotos.py <link incl. s.shopee short link> <folder> fetches the server-rendered page Shopee serves to crawlers (Googlebot UA; same route the Apify actor lergassy/shopee-scraper uses) and saves main photo + gallery + description images (01.jpg...) and anuncio.json (name, full description, price, rating, shop). Allowed hosts now: s.shopee.com.br, shopee.com.br, down-br.img.susercontent.com, api.apify.com, apify.com. the owner also saved an Apify token secret, but it returned 401 in the session that was already running (secrets reach only new sessions); Apify is only a fallback. First run: SOYO RX580 8GB graphics card (the owner's next product to promote), 12 images in video-teste/placa-fotos/.

**Affiliate count per Shopee product is not public (checked 2026-10-15):** no tool shows it, paid ones included. Proxies told to the owner:
- new listing, few reviews and fast-rising sales;
- FastMoss creator count for the same product on TikTok ([[tiktok-shop-research]]).

Recent-sales sources:
- the Shopee Affiliate API (daily delta of total sold; still pending);
- Apify Shopee BR scrapers, about US$2-5 per 1000 products; sold-count precision not verified;
- free: the bot-served product page has aggregateRating ratingCount (no sold count), so a daily delta of ratingCount is a proxy.

Recommended combo: FastMoss spots TikTok winners with few creators, then a Shopee match plus rating-count growth. An Apify test (at most ~US$0.25 for 50 products) is offered, waiting on the owner's OK.
