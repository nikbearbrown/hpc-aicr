# BUILD-PROMPT — Installing Software on an HPC Cluster (lecture)
> lecture hpc/Intro-to-Software-Installation-2026/intro_to_sw_installation.md — Liam persona, title "Installing Software on an HPC Cluster". Build into `hpc/youtube/claude-liam-lecture-software-installation/`.
```bash
R=hpc/youtube/claude-liam-lecture-software-installation
python3 $R/make_sheet.py
cat $R/_kit.py $R/_scenes_partA.py $R/_scenes_partB.py $R/_scenes_partC.py $R/_scenes_tail.py > $R/scenes.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```
