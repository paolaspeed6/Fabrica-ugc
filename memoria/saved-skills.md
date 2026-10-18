---
name: saved-skills
description: the owner's motion/design skill packs (GSAP, motion-design, Design DNA, Genjutsu, Three.js) saved 2026-10-15 in skills/
metadata:
  type: reference
  modified: 2026-10-15T08:45:50.803Z
---

the owner asked on 2026-10-15 to save these skills and use them in the project. Copies live in skills/ (index in LEIA.md there):
- gsap/ from greensock/gsap-skills (MIT)
- motion-design/ from LottieFiles/motion-design-skill (MIT)
- design-dna/ from zanwei/design-dna (MIT)
- genjutsu/ from AThevon/genjutsu v4.1.1 (MIT)
- threejs/ from cloudai-x/threejs-skills

Rejected: SaeedAngiz1/Genjutsu-Skill (paid APIs, uploads media to public hosts) and mjcreations123/design-dna (proprietary license).

Network: git clone of github.com works from the container, but codeload, the github.com HTML pages and api.github.com return 403.

Plan: animated text overlays as an HTML page with a paused GSAP timeline, stepped frame by frame with tl.seek(t) in headless Chromium (Playwright), screenshots piped into ffmpeg over the product clips. Free to render. See [[edit-templates]].

2026-10-16: the owner asked to add the Emil Kowalski skill (emilkowal.ski/skill is blocked by the proxy; fetched the same content from GitHub emilkowalski/skill, MIT, Markdown only, reviewed). Saved in skills/emil-kowalski/ and listed in LEIA.md. Use for motion timing and easing of the GSAP text layers.

2026-10-16: the owner also asked for pbakaus/impeccable (Apache-2.0). Saved only its Markdown (SKILL.md + reference/) in skills/impeccable/; its browser scripts and CLI were not brought over. Use for layout, typography and color decisions of edit templates.
