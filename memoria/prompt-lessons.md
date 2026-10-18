---
name: prompt-lessons
description: Prompt wording lessons for Seedream and Seedance product scenes (phone frames, impossible poses, product placement)
metadata:
  type: feedback
  modified: 2026-10-14T05:11:23.153Z
---

- "Smartphone photo" in a Seedream prompt drew a phone frame around the image. Use "Photorealistic full-frame photo" plus "No phone frame, no device bezel, no borders, no text".
- A pose the product can't hold on its own ("standing on its base") made a Seedream edit invent a part (a second bristle head on the cleaning brush). Show the product resting the way it really can.
- Since 2026-10-14, every scene is generated with the product centered, at 30-65% of frame height, clear of the templates' text areas, so text never covers it.

- 2026-10-15 batch (helmet, armchair, dog pads): Seedream mirrored helmet lettering (SPARK read backwards) and turned a second clear visor into a chameleon one; say "lettering reads left to right, never mirrored", name the reference photo's view, and spell out which kit part looks how. Living-room and reading-corner scenes got wine bottles on shelves ([[no-alcohol-rule]]); ask for plain walls and no shelves. A "top-down" shot came out inside a phone frame; say "DSLR photo filling the frame, not a screen".
- Seedance "orbit" turned a side-view helmet to face the camera and invented a front graphic plus a person-like reflection in the visor. produzir.py now appends TRAVA_ANGULO (same angle as frame 1, never rotate or show hidden sides) to every motion prompt; use push-in, short lateral dolly or crane only.
- Check the Seedream images (produzir.py --so-imagens) before paying for animation, then check 5 frames per clip before rendering.

**Why:** these errors break the product fidelity rule ([[product-fidelity-rule]]) and the owner's layout rules ([[edit-templates]]).
**How to apply:** use these phrasings and this placement in every scene prompt.
