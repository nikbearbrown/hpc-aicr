# BUILD-PROMPT — Intro to GPUs on Explorer (lecture)
> lecture hpc/Intro-to-GPUs-2026/training_main.md — Liam persona, title "Intro to GPUs on Explorer". Same cast as the series. Build into `hpc/youtube/claude-liam-lecture-intro-to-gpus/`.
```bash
R=hpc/youtube/claude-liam-lecture-intro-to-gpus
python3 $R/make_sheet.py
cat $R/_kit.py $R/_scenes_partA.py $R/_scenes_partB.py $R/_scenes_tail.py > $R/scenes.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```
