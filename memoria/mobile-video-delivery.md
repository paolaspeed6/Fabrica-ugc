---
name: mobile-video-delivery
description: the owner can't download attached mp4 files on his phone (2026-10-14); deliver videos via an Artifact page with a downloads-capability save button
metadata:
  type: feedback
---

the owner (2026-10-14): "Não estou conseguindo baixar pelo celular" — the mp4 files attached in the thread could not be downloaded on his phone.

**Why:** the owner reviews and posts from his phone; plain file attachments (and `<a download>` links in artifacts, which the sandbox blocks) don't work for him.

**How to apply:** when delivering finished videos, also publish an Artifact page with the mp4s as supporting files (each under 15 MB), a `<video>` preview, a "Baixar vídeo" button using the `downloads` capability (fetch the relative file as a Blob, then `downloads.save`), and the caption with a copy button. First one: (página do seu projeto) (SOYO RX580). For batches, one page per batch. Related: [[one-command-pipeline]].
