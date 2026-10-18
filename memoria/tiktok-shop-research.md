---
name: tiktok-shop-research
description: the owner wants TikTok Shop best-sellers with many recent sales and few creators (2026-10-14); Kalodata has no Claude integration, FastMoss MCP is the candidate
metadata:
  type: project
---

the owner (2026-10-14) asked to integrate Kalodata so Claude can find TikTok Shop products with many recent sales and few creators.

Kalodata API alone is Enterprise-only (~US$570-600/month); see the 2026-10-17 KaloPilot line below. FastMoss MCP was the first route.

**Setup found (2026-10-15, from the official FastMoss CLI on GitHub, github.com/FastMoss/cli):** remote MCP URL https://mcp.fastmoss.com/mcp, with OAuth login (or an X-API-Key header). Tools include product_rank_top_selling, product_rank_new_listed (last 30 days), product_creator_analysis, product_sales_trend, product_search and credit_usage_summary; leaderboards take filter.region, filter.date_type and filter.date_value. Each call uses FastMoss credits, which are limited on the trial.
the owner created a FastMoss account on 2026-10-15. He was told to add a claude.ai custom connector named FastMoss with that URL and authorize it through OAuth (no key in chat). Connectors only reach thread sessions; if the running thread can't see it, start a new thread. Default chosen while the purpose question is unanswered: search TikTok Shop Brazil and flag which products also exist on Shopee.
2026-10-15: the claude.ai OAuth sign-in for the FastMoss connector returned a 404 page. Fallback sent to the owner: create an MCP API Key at developers.fastmoss.com, then re-add the custom connector with Authentication "No sign in" and the request header X-API-Key set to that key. Waiting on the owner to confirm it works.
2026-10-15: the FastMoss connector WORKS via the X-API-Key header and its tools reach this thread. Trial: 100 credits per day for 3 days (to 2026-10-18).
- the owner's first test filter: fewer than 50 affiliates and more than 100 recent sales.
- FastMoss covers TikTok Shop only, so "affiliates" means linked creators there. It has no Shopee affiliate counts; only the Shopee API gives those.
- What works: product_search with region BR, day7_units_sold_range, creator_count_range and commission_rate_range. Many results show 0% commission, meaning not open to affiliates.
- Delivered 10 products (top: pó desentupidor, óculos zoom, capa máquina de lavar).
- Shopee cross-check works free: shopee.com.br/search?keyword=... with the Googlebot UA returns item links (-i.<shop>.<item>). The script is in the session scratchpad only; it's simple enough to recreate.
- the owner interrupted a credit_usage_summary call: avoid extra credit checks.
- 2026-10-15 (thread "busca Shopee via Apify"): Apify token secret returns 401 even in a NEW session, so the token value itself is bad (or the "Shopee" secret, also injected on api.apify.com, overrides it); the owner must re-save it. Shopee's crawler pages show rating and review count but NO sold counts; /api/v4/search is blocked (403). Workaround used: FastMoss product_search by category (11 kitchen, 16 phones&electronics, 17 pet) + Shopee Googlebot search for the equivalent listing. Results: produto-campeao/busca-2026-10-15.md (top: fone para dormir de lado, 13 creators, Shopee listing with 81 reviews).
- 2026-10-17: Kalodata DOES have a Claude route: official KaloPilot skill (github.com/sailtonight/kalopilot-skill, MIT, copyright Kalodata). POST https://www.kalodata.com/api/pilot/skill/ext/v1/chat/async/submit with Authorization: Bearer <token> (token from kalodata.com/pilot > Connect OpenClaw), then poll /result; uses Kalodata credits, BR supported. the owner asked to set the token as a network secret for www.kalodata.com plus allowlist; first use: the 'Manual do Vídeo Vencedor' from top-selling BR videos.
- 2026-10-17 (thread "Manual do Vídeo Vencedor"): KaloPilot works; one 30-video analysis cost 18.29 credits and used up the owner's Kalodata credits, and the final report never arrived (the agent stops after its plan; follow-ups reuse task_id). Ask for the report in the same query. FastMoss video_script_info returned empty for BR videos; video_search by product_category_id (11/16/17) with orderby units_sold works. Manual v1: agentes/manual_video_vencedor.md (TikTok winners: median price R$ 20, small accounts sell, comparison and pain-question hooks).
