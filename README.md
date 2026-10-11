# HPC and AICR: films, guides, and agent rules

**What this is.** A repository for researchers who are new to Northeastern University's research computing: the **Explorer** cluster and the shared **AICR** GPU cluster. It holds (1) the **films**: short narrated lectures, each with a written **guide** that follows the film and the files that built it, and (2) **agent rules**: two files that make a coding agent (Claude Code, Codex) follow cluster best practice on a researcher's behalf.

**Why it exists.** Most cluster trouble is not hard computer science: a request that is too big, a GPU left idle, work run on a login node, data left on a disk that gets wiped. The films and guides teach the habits; the agent rules make an AI assistant keep them.

**How it relates to Northeastern Research Computing's training.** Most guides are **our own rewrite of their lessons**, based on https://github.com/northeastern-rc-training and citing each original. They are not copies: the structure follows our films, the wording and exercises are ours, and we added what we learned using the clusters (real read-only output, corrections, gaps). Each guide says what we tested ourselves and what we only read. The originals remain the authority and belong to their authors.

**What is inside.** Two folders only.

| Folder | What it holds |
|---|---|
| [`films/`](films/) | one subfolder per film: the film link, `guide.md` (our written lesson), `build/` (beat sheet, scenes, fact-check) and a README saying where it comes from. [`films/REAL-OUTPUTS.md`](films/REAL-OUTPUTS.md) is the read-only output we captured on both clusters |
| [`skills/`](skills/) | `hpc/HPC.md` and `aicr/AICR.md`, the agent rules, plus `film-on-explorer/` (a plan and scripts for rendering a lecture film on Explorer) and thin `SKILL.md` wrappers with Codex metadata. [How to use them](skills/README.md) |

## The films

Playlist: https://www.youtube.com/playlist?list=PLX28mAL5_hLk (the first eight are published; links are unlisted).

| # | Film | Watch | Status | Folder |
|---|---|---|---|---|
| 1 | AICR Introduction | [film](https://youtu.be/TY1xixqUZ_0) | published | [`films/01-aicr-introduction`](films/01-aicr-introduction) |
| 2 | Optimizing GPU Usage on AICR | [film](https://youtu.be/8oinGvzgzgc) | published | [`films/02-optimizing-gpu-usage-on-aicr`](films/02-optimizing-gpu-usage-on-aicr) |
| 3 | Intro to Explorer and OOD | [film](https://youtu.be/LIjhb1dokME) | published | [`films/03-intro-to-explorer-and-ood`](films/03-intro-to-explorer-and-ood) |
| 4 | Intro to GPUs on Explorer | [film](https://youtu.be/vqe1ILbAuRc) | published | [`films/04-intro-to-gpus-on-explorer`](films/04-intro-to-gpus-on-explorer) |
| 5 | Intro to Parallel Computing | [film](https://youtu.be/IEIEL4jZhjQ) | published | [`films/05-intro-to-parallel-computing`](films/05-intro-to-parallel-computing) |
| 6 | Intro to Linux | [film](https://youtu.be/Q70HTMmL6oQ) | published | [`films/06-intro-to-linux`](films/06-intro-to-linux) |
| 7 | Scientific Reproducibility | [film](https://youtu.be/68LPUyZrRYs) | published | [`films/07-scientific-reproducibility`](films/07-scientific-reproducibility) |
| 8 | Installing Software on an HPC Cluster | [film](https://youtu.be/l2RwXl8W-sA) | published | [`films/08-installing-software-on-an-hpc-cluster`](films/08-installing-software-on-an-hpc-cluster) |
| 9 | Logging into AICR with Claude | – | built or building at the time of writing; not yet published | [`films/09-logging-into-aicr-with-claude`](films/09-logging-into-aicr-with-claude) |
| 10 | Requesting Access to Explorer | – | laid out (script, scenes, fact-check); not yet rendered | [`films/10-requesting-access-to-explorer`](films/10-requesting-access-to-explorer) |
|  | Managing /projects on Explorer | – | built; not in the published playlist | [`films/managing-projects-on-explorer`](films/managing-projects-on-explorer) |
|  | Logging into Explorer with Claude | – | evidence recorded (a real, tested key login); film not yet laid out | [`films/logging-into-explorer-with-claude`](films/logging-into-explorer-with-claude) |
|  | Optimizing GPU Usage on Explorer | – | source material only; no film built | [`films/optimizing-gpu-usage-on-explorer`](films/optimizing-gpu-usage-on-explorer) |
|  | Running a Local LLM on Explorer and Pointing Coding Agents at It | – | source material only; no film built | [`films/running-a-local-llm-on-explorer`](films/running-a-local-llm-on-explorer) |
|  | Scientific Reproducibility II (version control) | – | source material only; no film built | [`films/scientific-reproducibility-ii`](films/scientific-reproducibility-ii) |
|  | Scientific Reproducibility III (containers) | – | source material only; no film built | [`films/scientific-reproducibility-iii`](films/scientific-reproducibility-iii) |

## Use the agent rules

Do not paste them into your `CLAUDE.md` or `AGENTS.md`. Point to them: "when a task involves Explorer, Slurm, or HPC, read `skills/hpc/HPC.md` first; for AICR also read `skills/aicr/AICR.md`." Details and a ready snippet are in [`skills/README.md`](skills/README.md).

## Redo a film

Each `films/<film>/build/` folder holds the plan and scenes, not the rendered video. The films are built with the [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit. Rendered video, audio and large files are deliberately not in this repository (see `.gitignore`).

## Credits and licensing

The lessons these guides are based on are by Northeastern University Research Computing staff (https://github.com/northeastern-rc-training); each film's README credits the presenter where the original names one. Those repositories carry no license, so **we do not reproduce their text, code or images**: only our own rewrites, with citations, are here. The films, guides, scripts, scenes, fact-checks and agent rules written for this repository are by Nik Bear Brown. The narration is an AI voice (Liam, in for the author). Two items are not derived from Research Computing's lessons: the local-LLM tutorial and the login and access guides.

## What is and is not verified

The agent rules and guides were fact-checked against their sources, and the facts marked "tested by us" were read from real, read-only sessions on both clusters on 2026-10-11 (nothing was submitted or changed). Anything needing a compute node, a job or Open OnDemand is marked "from the source, not run by us". Partition limits and quotas change, so every rule says "confirm live". Some quotas are described differently in different sources (for example the scratch quota); the guides and rules list every such conflict. Whether Research Computing permits automated agent access is not addressed by any source: ask rchelp@northeastern.edu.

Usernames, Slurm accounts and local paths in the records are replaced with placeholders such as `<aicr-username>`.
