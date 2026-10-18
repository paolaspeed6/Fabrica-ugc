---
name: no-alcohol-rule
description: Never put wine bottles, beer or any alcoholic drink in generated scenes or decoration (Shopee terms)
metadata:
  type: feedback
  modified: 2026-10-15T06:52:42.422Z
---

Never add wine bottles, wine glasses, beer, liquor, cocktails or any other alcoholic drink to a generated scene, background or decoration (the owner, 2026-10-15).

**Why:** Shopee's terms are strict about alcohol, and a video showing it can be removed or get the account penalized.
**How to apply:** video-teste/produzir.py appends a PROIBIDO clause to every Seedream prompt and a no-alcohol line to every Seedance prompt. Also check every scene image for drinks before animating, especially in barbecue, living-room and dining scenes ([[prompt-lessons]], [[product-fidelity-rule]]).
