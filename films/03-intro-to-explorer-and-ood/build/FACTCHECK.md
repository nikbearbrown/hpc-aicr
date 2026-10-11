# FACTCHECK — Intro to Explorer and OOD (lecture)

**Sources.** S = the training document; its screenshots (SS); R = rc-docs.northeastern.edu pages the source links. **Result.** 24 claims: 23 PASS, 1 CORRECTED. Checked 2026-10-06.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B10 | login node for light work; compute nodes via the Slurm scheduler | PASS | S §What is an HPC | |
| 2 | B11 | Explorer replaced Discovery; 45,000 CPU cores; 525+ GPUs; free to NU faculty and students; at MGHPCC, Holyoke | PASS | S §What is Explorer | |
| 3 | B12 | 10 GbE to campus; 6 PB storage; 10 GbE or InfiniBand 100/200 Gbps between nodes | PASS | S | |
| 4 | B20 | PI/staff storage space required; free up to 35 TB; project command or access form; storage request form; classroom form by the instructor | PASS | S §How to get an account | |
| 5 | B31 | ssh login.explorer.northeastern.edu; password cursor doesn't move; Windows: MobaXterm/PuTTY, port 22 | PASS | S; banner text from SS | |
| 6 | B32 | ood.explorer.northeastern.edu; Northeastern credentials + Duo; dashboard | PASS | S; SS | |
| 7 | B40 | /home, /scratch, /projects, /courses/coursename.code; course users may lack /projects; absolute paths | PASS | S §file paths | |
| 8 | B41 | home 75 GB; scratch 50 TB purged first Tuesday monthly; projects long-term; courses 1–5 TB shared; "quota exceeded" | PASS | S §Transferring Data | |
| 9 | B42 | the ls listing and the cat output | PASS | S verbatim (ls truncated with …) | |
| 10 | B50 | scp via xfer.discovery.neu.edu; zip/tar many small files | PASS | S | |
| 11 | B51 B52 | Files app: Home Directory, Change directory, Upload; 10 GB limit; scp or Globus beyond | PASS | S; SS | |
| 12 | B60 | no software, big transfers or computation on login nodes | PASS | S §Running Jobs | |
| 13 | B61 | srun defaults 4 h, 1 node, 1 task, 2 GB, 2 CPUs, short; flags and short flags | CORRECTED | S | S's short-flag line reads `--m 50GB --n 16` (typos); the film shows the valid `--mem 50GB -n 16` |
| 14 | B62 | partitions: short (default), sharing; gpu, sharing, gpu-interactive, gpu-short; long, multigpu by application; courses, courses-gpu | PASS | S table | |
| 15 | B63 | which partition | PASS | S | |
| 16 | B64 | GPU definition; the two srun GPU commands; record which GPU | PASS | S | |
| 17 | B65 B66 | OOD RStudio form fields; Queued → Starting → Running; time starts when running; cancel when done | PASS | S; SS | |
| 18 | B67 | the sbatch script | PASS | S verbatim; presenter's email and home path → `username` | |
| 19 | B68 | `Submitted batch job 3719393`; slurm-3719393.out contents; less, q; start small and scale up | PASS | S | |
| 20 | B70 | squeue output rows; `squeue -p short | wc -l` → 518; --start | PASS | S (user column shows `username`) | |
| 21 | B71 B72 | Active Jobs; My Interactive Sessions; Host; 7-digit job id 3468842; Session ID link; output.log | PASS | S; SS | |
| 22 | B80 | seff 371441: 12 cores, 8.29% CPU eff, 10.44% of 50 GB, 00:17:19; seff 2612438: 8 cores, 83.83%, 3.56% of 15.62 GB, 00:25:57 | PASS | S verbatim | |
| 23 | B90 | module avail / load; exact case; not in .bashrc (OOD interference, reproducibility) | PASS | S §Software | |
| 24 | B91 | conda (not only Python), containers, from source; rchelp, office hours, consultation | PASS | S | |

## Stripped as datable
"Spring 2026", "Intro to Linux recording", "next training session", "Discovery" kept only as "the older Discovery cluster" (the transfer host still carries the name).
