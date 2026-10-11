# BUILD-PROMPT — Intro to Linux (lecture)
> lecture hpc/Intro-to-Linux-2026/intro_to_linux.md — Liam persona, title "Intro to Linux". Build into `hpc/youtube/claude-liam-lecture-intro-to-linux/`.
```bash
R=hpc/youtube/claude-liam-lecture-intro-to-linux
python3 $R/make_sheet.py
cat $R/_kit.py $R/_scenes_partA.py $R/_scenes_partB.py $R/_scenes_tail.py > $R/scenes.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```
