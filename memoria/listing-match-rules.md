---
name: listing-match-rules
description: the owner 2026-10-15 - color from the listing's FIRST photo, packaging lettering pixel-exact, text never over the product, hooks and CTAs extremely elaborate
metadata:
  type: feedback
  modified: 2026-10-15T07:29:02.018Z
---

the owner's rules after the 2026-10-15 batch. the owner discarded the armchair and dog-pad videos because of these errors.

1. **Color and variant come from the listing's MAIN (first) photo, always.** The Poltrona Lara listing opens with the BLUE chair; Claude used beige (photo 15), and the owner won't use it. Fabric color, texture and details must match that first photo 100%.
2. **Packaging with lots of lettering must match exactly.** Seedream and Seedance redraw small print: the Espaço de Bicho bag came out wobbly and garbled ("ESPAÇO BICHO", "60x30"), which looks like AI and risks penalties. Plan for this kind of product: never let AI redraw the package. Either composite the real listing photo of the package by code onto the AI scene (camera locked in Seedance; code applies the same push-in to the whole frame so the package moves with the scene), or keep the package out of the AI scene and show only unprinted parts (the pad, absorption). A scene with AI-drawn lettering fails the check.
3. **Text never covers the product.** Check the LAST frame of each clip (push-ins grow the product). montar_video_pro.py takes per-scene "subir" (px, moves the scene up over a blurred fill) and "escala" (<1, shrinks it); produzir.py reads them from p["cenas"][i] or a version's scene. Text zones: Shopee card y 1300-1640 of 1920, Reels text from about 1150.
4. **Hooks and CTAs always extremely elaborate** (the owner: "Extremamente Elaborados"). No generic lines. Each one is built from the product's strongest proof and a proven pattern (price shock, curiosity, pain, POV, quantity plus price), specific to the product.

5. **Key buying details always big and easy to read on screen** (the owner, 07:30): unit count (200 unidades, kit 10), size, weight, number of visors. They go in the headline or a large badge, not only in the small spec chips, so viewers grasp the product at a glance and the caption is easier to write.

**How to apply:** check all four before showing the owner anything, and generate nothing without the owner's request ([[no-generation-without-request]], [[product-fidelity-rule]], [[edit-templates]]).
