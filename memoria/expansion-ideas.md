---
name: expansion-ideas
description: the owner's expansion questions (2026-10-14) - reuse videos in other countries, faceless ("dark") YouTube channel; answers given, nothing started
metadata:
  type: project
---

the owner asked on 2026-10-14 about two expansions. Nothing has been started on either.

**Other countries.** Answer: yes, at almost no cost. Scenes have no people and no voice, and the on-screen text is drawn by code, so a new language only needs translated texts and a re-render. Conditions:
- the identical product must be sold in that country ([[product-fidelity-rule]]);
- an affiliate account and link for each country;
- local currency and units, and never reuse a text that quotes a price;
- the fonts cover Spanish and English but not Thai or Vietnamese.
Suggested first market: Spanish (Shopee Mexico or Colombia).

**Faceless "dark" YouTube.** Answer: possible with the same base (script, generated scenes, AI narration, assembly in code). The cost is different:
- a 10-minute video made only of clips would be about 120 clips, roughly R$68;
- the viable mix is mostly stills with camera moves done in code plus a few clips, an estimated R$10-20 per video, not measured.
YouTube does not monetize "inautêntico" mass-produced repetitive content, and realistic AI content must be disclosed. Shorts made from the product videos are a shortcut; a YouTube Shopping affiliate program with Shopee in Brazil was recalled but not verified.

2026-10-15: the owner wants several faceless channels posting daily, 100% original scripts, and will invest in tools and APIs ("não me limite"). Planning moved to the thread "YouTube dark" (started 13:11). Plan given: channel 1 is built as the full factory (topic, script, narration, scenes, edit, thumbnail, upload via the official YouTube Data API; unverified API apps upload as private until Google's audit, so request it early); channels 2-3 open in different niches once channel 1 ships daily with no manual work; each channel has its own niche, voice, look and scriptwriter so it doesn't read as a copy network. Own lean agent team. Waiting on the owner's niche choice (card; recommended: histórias e mistérios). Nothing spent.

Niche method (the owner 13:13 asked for professional tools and reference books): score candidates on Schwartz existing mass desire (rising 12-month demand), Blue Ocean (outliers: small new channels with videos at 10x their average), Berger STEPPS shareability, Heath story retention, and our viability (RPM, AI cost, policy risk). Tools offered on a card: free YouTube Data API outlier finder built by Claude (recommended; the owner needs a free Google API key and googleapis.com on the allowlist), NexLev (~US$42/mo, web only, the owner sends prints), or both. Prices came from competitor sites; confirm on official sites before any purchase.

YouTube key: env var YOUTUBE_API_KEY (the owner saved 2026-10-15; reaches new sessions). Finder: youtube-dark/cacador_outliers.py + nichos.txt (Portuguese-audio only, ~4,000 of 10,000 daily quota units per run). the owner prefers no new tools unless necessary. First run 2026-10-15 (outliers-2026-10-15.md): História best for long-form (19 channels under 1 year with outliers); curiosidades high but 89% Shorts; geografia/abandonados and psicologia/estoicismo next; histórias e mistérios near last. the owner confirmed História for channel 1 (13:36). Rerun weekly to see what is rising.
Cost estimate 10-min video (WaveSpeed list, unmeasured): voice ~8,500 chars US$0.85-1.70 (ElevenLabs/MiniMax HD; list price and description disagree), ~60 Seedream stills US$1.62, 6 Seedance clips US$0.60, thumbnail US$0.08; total US$3-4 (R$17-23), ~R$600/month per daily channel. Script uses the owner's Claude plan. Next: 3-voice 30 s test, max US$0.15, awaiting the owner's OK.
