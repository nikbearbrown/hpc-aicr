# BUILD-PROMPT — Scientific Reproducibility (lecture)
> lecture hpc/Intro-to-Scientific-Reproducibility-2026/scientific_repoducibility_main.md — Liam persona, title "Scientific Reproducibility". Build into `hpc/youtube/claude-liam-lecture-scientific-reproducibility/`.
```bash
R=hpc/youtube/claude-liam-lecture-scientific-reproducibility
python3 $R/make_sheet.py
cat $R/_kit.py $R/_scenes_partA.py $R/_scenes_partB.py $R/_scenes_tail.py > $R/scenes.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```
