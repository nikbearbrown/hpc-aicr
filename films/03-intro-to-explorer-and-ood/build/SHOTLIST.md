# SHOTLIST — Intro to Explorer and OOD (lecture)

**What this is.** One row per body beat: about, lane, runner-up, why (BEST-BEAT LAW). **Result.** 29 body beats: 11 Manim (8 cast scenes, 3 tables/trees/reports), 7 real captures of the Open OnDemand site (the training's own screenshots), 10 real-command terminals, 1 large-icon row. No text-only cards.

| Beat | About | Lane | Runner-up | Why |
|---|---|---|---|---|
| B10 | cluster shape: login node, Slurm, compute | cast scene | the source's SVG diagram | the source's own figure, drawn with the series cast |
| B11 | 45,000 cores, 525+ GPUs, free, Holyoke | counters over unit grids | photo of MGHPCC | the numbers are the claim |
| B12 | 10 GbE, 6 PB, InfiniBand | pipes between racks | table | bandwidth is a pipe |
| B20 | research vs classroom accounts | two doors, cabinet, tokens | flowchart | an access path is a door |
| B30 | terminal or website | two windows cabled to one node | icon row | "same cluster" is the cable |
| B31 | ssh login | **real session** (CCPlainShell): the command, the password prompt, the welcome banner from the training's screenshot | the screenshot in a browser frame | a terminal is not a browser; the banner text is real |
| B32 | OOD dashboard | **real capture** (BrowserCapture) | drawing | rung 1 |
| B40 | four places, absolute paths | cast containers with real paths | table | film 1's grammar |
| B41 | quotas and purge | cast containers filling / sweeping | table | the first-Tuesday purge is a motion |
| B42 | ls and cat | **real commands + the source's outputs** | — | commands |
| B50 | scp | **real commands** | drawing of two machines | commands |
| B51 B52 | OOD Files app | **real captures** | drawing | rung 1 |
| B60 | leave the login node | cast scene with X | text | the move is the claim |
| B61 B64 | srun forms | **real commands** | — | commands |
| B62 | partitions | drawn table | text table | the source's table, drawn |
| B63 | which partition | decision tree | prose | a choice is a tree |
| B65 B66 | OOD RStudio form, running card | **real captures** | drawing | rung 1 |
| B67 B68 | sbatch script, submit, output | **real script and the source's real outputs** | code card | the header is all #SBATCH comments (type gate §8.12); the terminal shows it verbatim |
| B70 | squeue | **real commands + the source's outputs** | — | commands |
| B71 B72 | OOD jobs pages | **real captures** | drawing | rung 1 |
| B80 | seff | **the source's two real reports**, re-composed with bars | the source text as a shell | bars make 8% vs 84% visible |
| B90 | modules | **real commands** | — | commands |
| B91 | conda / containers / source | large library icons | FormBCard | three named routes |

## Tool beats and their rung

Captures B32 B51 B52 B65 B66 B71 B72: the training's own screenshots of ood.explorer.northeastern.edu (rung 1, human-supplied), copied into `captures/` and `runtime/remotion/public/lecture-explorer-ood/`. Terminal beats: commands from the source; outputs only where the source shows them (B42, B68, B70) or the training's screenshot shows them (B31). No Explorer session was run by this build (no account access from here).
