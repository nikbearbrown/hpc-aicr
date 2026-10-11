# BUILD-PROMPT — Intro to Explorer and OOD (lecture)

> lecture hpc/Intro-to-Explorer-OOD-2026/Intro_explorer_ood.md — Liam persona, title "Intro to Explorer and OOD". Same cast as the AICR films. Build into `hpc/youtube/claude-liam-lecture-intro-to-explorer-ood/`.

```bash
R=hpc/youtube/claude-liam-lecture-intro-to-explorer-ood
python3 $R/make_sheet.py
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R   # only if narration changed; re-pad BOUT 1.0 s; re-run make_sheet.py
cat $R/_kit.py $R/_scenes_partA.py $R/_scenes_partB.py $R/_scenes_tail.py > $R/scenes.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```
