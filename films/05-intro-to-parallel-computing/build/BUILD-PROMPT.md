# BUILD-PROMPT — Intro to Parallel Computing (lecture)
> lecture hpc/Intro-to-HPC-Scaling-Parallel-Computing-2026/intro_to_parallel_computing.md — Liam persona, title "Intro to Parallel Computing". Build into `hpc/youtube/claude-liam-lecture-intro-to-parallel-computing/`.
```bash
R=hpc/youtube/claude-liam-lecture-intro-to-parallel-computing
python3 $R/make_sheet.py
cat $R/_kit.py $R/_scenes_partA.py $R/_scenes_partB.py $R/_scenes_partC.py $R/_scenes_tail.py > $R/scenes.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```
