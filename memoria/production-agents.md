---
name: production-agents
description: the owner's UGC video factory (2026-10-15) - orchestrator + researcher, scriptwriter, pre-generation QC, prompt fiscal; instructions in agentes/
metadata:
  type: project
  modified: 2026-10-15T09:25:16.680Z
---

On 2026-10-15 the owner defined the "Fábrica de Vídeos UGC". The Claude in the conversation is the orchestrator. Each specialist runs as a fresh subagent (Agent tool), given its own instruction file plus principios.md. All files are in agentes/ (start with orquestrador.md).

**Agents**
- pesquisador.md: writes brief.md, covering angle, awareness level, strongest proof, objection, hook pattern and CTA elements.
- roteirista.md: writes roteiro.md and pNN.json, with 5 ranked hook options per platform and an "abertura" big animated opening.
- qc_roteiro.md: scores every item 0-10 and releases only at 8 or above. It fixes the problems itself or sends the roteiro back, at most 2 rounds.
- produtor.md: cinematic prompt specialist (DoP vocabulary, fixed prompt structure, positive-only wording) who writes the editar/movimento prompts.
- fiscal.md: keeps licoes.md and banco_ganchos.md (hooks, CTAs and results).
- analista.md (the owner 2026-10-17): weekly; learns what converts from per-version Sub ID sales and top-selling TikTok videos (FastMoss), updates banco_ganchos.md and licoes.md. Uses principios.md plus Lean Analytics, Kohavi (A/B tests), Hubbard, Annie Duke, Kahneman, Knaflic.
- qualidade.md: visual QC after generation. Gate A checks images before animation; gate B checks the final frames.

principios.md applies Kim & Mauborgne's Blue Ocean (the owner 2026-10-17: "criar algo que vai se destacar no meio de outros anúncios parecidos"; an ERRC grid per product, at least 1 of the 4 versions on a new angle or non-obvious buyer, and a hook must not fit a competitor), Schwartz (awareness levels, mechanism), Hopkins (specificity, proof), Cialdini, Halbert, Ogilvy and PAS, with low-friction CTAs native to each platform.

**Output per product (the owner, 2026-10-15 09:47):** each 3-scene generation becomes 3 videos: 2 different Shopee edits (versoes "shopee" = GSAP vitrine, "shopee2" with "estilo": "tiktok" = big letters) + 1 Facebook Reels. Each gets its own hook, CTA and caption, matching the product and readable on a phone. Never claim delivery speed ("envio imediato"); the owner isn't sure of it.

**Trigger:** when the owner sends a product link, the flow starts automatically, without asking. The delivery is Brief + approved Roteiro + quality notes + maximum generation cost. Paid generation runs only when the owner asks. Ask the owner only when critical info is missing from the listing.

**Watch out:** a p*.json whose "nome" changes must point "clipe" at the existing clips, or produzir.py regenerates them and charges for it.

See [[listing-match-rules]], [[no-generation-without-request]], [[videos-prontos-page]].
- GROWTH MODE (the owner 2026-10-17): TikTok accounts need 2,000 followers before TikTok Shop, so first videos aim at followers, not sales. Roteirista follows agentes/viral.md (viral/psychology books, formats, cadence 3-5/day per new account, tools table). Self-learning loop in analista.md: agentes/aprendizado/videos.csv per video + Sniper swipe stats in aprendizado/sniper.md. the owner chose (2026-10-17 03:42) "Narração e mãos": AI PT-BR narration allowed (test 1 voice and measure cost first) and AI hands allowed in viral growth videos, with his OK per scene; product fidelity rules unchanged.
