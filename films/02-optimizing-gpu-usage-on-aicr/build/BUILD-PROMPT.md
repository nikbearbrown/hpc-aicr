# BUILD-PROMPT — Optimizing GPU Usage on AICR (lecture)

> lecture hpc/AICR-Optimizing-GPU-Usage/aicr-gpu-optimization.md — Liam persona, title "Optimizing GPU Usage on AICR". Same cast as the AICR Introduction film. Build into `hpc/youtube/claude-liam-lecture-aicr-optimizing-gpu-usage/`.

```bash
R=hpc/youtube/claude-liam-lecture-aicr-optimizing-gpu-usage
python3 $R/make_sheet.py
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R   # only if narration changed; re-pad BOUT 1.0 s; re-run make_sheet.py
cat $R/_kit.py $R/_scenes_partA.py $R/_scenes_partB.py $R/_scenes_partC.py $R/_scenes_partD.py $R/_scenes_tail.py > $R/scenes.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```
