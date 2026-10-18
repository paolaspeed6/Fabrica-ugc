---
name: video-length-15s
description: the owner's rule (2026-10-13) - every video must run the full 15 seconds; replaces the earlier 13-15 s range
metadata:
  type: feedback
  modified: 2026-10-13T09:23:28.291Z
---

the owner (2026-10-13): "os vídeos todos deverão ter os 15 segundos completos". Every finished video, on every platform version, must be exactly 15 s.

**Why:** the owner's standing instruction after the bike test, whose versions came out at 13.6-14 s. It replaces the earlier "13-15 s, try short vs long" note.

**How to apply:** in produzir.py product files, set per-scene "ate" so each version totals 15.0 s (scenes overlap about 0.3 s per cut, so 3 scenes need about 15.6 s of "ate" in total, e.g. 5.2/5.2/5.2; generated clips are 5 s, so use "lento" or a 4th scene when "ate" exceeds the clip). Check the length with ffprobe before delivering. Related: [[one-command-pipeline]], [[edit-templates]].
