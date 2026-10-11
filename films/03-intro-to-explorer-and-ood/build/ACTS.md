# ACTS — Intro to Explorer and OOD (lecture)

**What this is.** Coverage map for the lecture film of `hpc/Intro-to-Explorer-OOD-2026/Intro_explorer_ood.md`. **Why.** A lecture covers the whole source; every section lands in an act or is listed as left out. **Result.** All eight agenda items of the training plus the account section are covered in nine acts, 29 body beats, about 9 min. Nothing of substance left out.

| Source section | Act | Beats |
|---|---|---|
| What is an HPC | I · What A Cluster Is | B10 |
| What is Explorer | I | B11 B12 |
| How to get an account | II · Getting An Account | B20 |
| How to access Explorer; logging in via terminal (Mac, Windows); via OOD | III · Logging In | B30 B31 B32 |
| Welcome to file paths | IV · Where Files Live | B40 B42 |
| Transferring data (space limits) | IV | B41 |
| Transfer with scp; with the OOD Files app; limits, Globus | V · Moving Data | B50 B51 B52 |
| Running jobs; srun and sbatch; partitions; which partition; GPU resources; OOD interactive jobs; sbatch script; output | VI · Running Jobs | B60–B68 |
| Checking job status (squeue; OOD Jobs / My Interactive Sessions; output.log) | VII · Checking On A Job | B70 B71 B72 |
| How to become a super user (seff) | VIII · Right-Sizing | B80 |
| Software (modules, conda, containers, source); How to get help | IX · Software | B90 B91 |

## LEFT OUT

- The presenter's name and the "Spring 2026 Training Series" framing (credited in the description; datable in the film).
- Cross-references to other sessions ("Intro to Linux recording", "next training: Intro to GPUs"): datable, and the film stands alone.
- The MGHPCC photograph and the two SVG diagrams in `images/`: the diagrams are redrawn as B10/B60; the photo is not evidence for any claim.
- The full 18-entry `ls /projects/seedpod/rawdata` listing is shown as its first entries plus an ellipsis (B42); the `cat` example is verbatim.
- The `squeue --start` output (the source shows none).

## Order

The source's order, with one fold: the storage quotas (source §Transferring Data) are taught in Act IV beside the paths they describe, before the transfer commands.

## Cast (series kit)

| Object | Picture | Beats |
|---|---|---|
| compute racks | dark server stacks | B10 B12 B60 |
| login node | one dark slab | B10 B30 B60 |
| a job | kraft box, one terracotta tape | B10 B60 |
| home / scratch / projects / courses | kraft box / open bin / white cabinet / kraft cabinet | B40 B41 |
| Slurm | a gate on the belt | B10 B60 |

## Self-contained check

The source assumes the live training room (links, "we will cover"). The film defines six terms up front, never says "this training" or "recording", and names Northeastern and Explorer because they are the subject. The presenter's username in the source's commands is replaced by `username` where the source itself says to substitute your own; it is kept where it is part of a real output (B42's `cat` path, the seff reports' user line is not shown).
