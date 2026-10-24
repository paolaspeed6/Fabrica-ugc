# Skills salvas (Kevin, 2026-10-15)
Pacotes de instruções para o Claude (só Markdown e alguns scripts locais; nada aqui roda sozinho nem precisa de chave).
- gsap/ (greensock/gsap-skills, MIT): animação GSAP; timeline com seek determinístico, base do texto animado nos vídeos.
- motion-design/ (LottieFiles/motion-design-skill, MIT): tempo, easing, coreografia de entrada e saída.
- design-dna/ (zanwei/design-dna, MIT): extrai cores, fontes e estilo de imagens de referência em tokens JSON.
- genjutsu/ (AThevon/genjutsu v4.1.1, MIT): skills cast, paint, bunshin e sub-skills (_jutsu) de GSAP, Three.js, canvas.
- threejs/ (cloudai-x/threejs-skills): Three.js para cenas 3D.
- emil-kowalski/ (emilkowalski/skill, MIT, 2026-10-16): filosofia de animação de UI (easing, duração, vocabulário de movimento, performance, revisão e auditoria de animações). Só Markdown. Útil para o timing dos textos GSAP; ler skills/animation-vocabulary, animate e emil-design-eng antes de mudar a camada de texto.
- impeccable/ (pbakaus/impeccable, Apache-2.0, 2026-10-16): guia de design de interface (tipografia, cor, layout, movimento, anti-padrões). Copiei só os .md (SKILL.md e reference/); os scripts do navegador e o CLI NÃO foram trazidos. Ler antes de desenhar novos modelos de texto/layout.
Descartados: SaeedAngiz1/Genjutsu-Skill (APIs pagas, sobe mídia para hosts públicos) e mjcreations123/design-dna (licença proprietária).
Uso: antes de editar a camada de texto/motion dos vídeos, ler o SKILL.md relevante aqui.

No kit, as skills vêm compactadas em `skills/skills.zip` (são mais de 300 arquivos; assim cabem num upload só no GitHub).
Quando precisar de uma: `python3 -c "import zipfile;zipfile.ZipFile('skills/skills.zip').extractall('skills')"`.
Nada aqui é obrigatório para a fábrica Shopee: servem para quem for desenhar modelos novos de texto e animação.
