---
name: claude-usage-budget
description: the owner 2026-10-15 - the 4-agents-per-product factory burned his Claude plan usage; use the lean one-pass mode (ficha_rapida.md)
metadata:
  type: feedback
  modified: 2026-10-15T11:52:04.860Z
---

On 2026-10-15 at 11:50 the owner stopped the full factory. In his words: "desse jeito a fábrica não vai rodar, está consumindo todo uso do meu claude... pretendia fazer mais de 50 por dia".

The full mode ran 4 separate agents per product (researcher, scriptwriter, producer, QC). Each agent re-read about 10 rule files plus the photos, so 22 products needed about 88 full reads.

**Why:** Claude plan usage is a hard limit, just like WaveSpeed credit. The target is 50+ videos a day.

**How to apply:**
- Use the lean mode by default. One agent (model opus for creative work since the owner 2026-10-17, see [[creative-principles-and-model]]; sonnet only for mechanical tasks) handles 4-5 products in a single pass.
- That agent reads only agentes/ficha_rapida.md, one example JSON, anuncio.json, photo 01 and at most 2 more photos.
- QC is done by code: checar_antes_de_gastar plus frame grids. Don't use separate QC agents.
- Avoid Workflow fan-outs and long agent chains.
- A proposed next step is running the factory through the owner's own Anthropic API key (pay per use), so his plan isn't consumed. That's waiting on the owner's choice.

See [[production-agents]].
