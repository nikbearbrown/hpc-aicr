---
name: film-on-explorer
description: Plan and scripts for rendering a narrated lecture film on Northeastern's Explorer cluster (not AICR): pack the film and the brutalist.art toolkit, stage them in a job-scoped scratch folder, run a one-time toolchain setup and a render with Slurm, fetch the master back, and delete only the job folder after a yes. Use when a professor or an agent wants to render lecture films on the HPC cluster instead of a laptop, or asks how to package the toolkit for the cluster. Loads on top of the hpc skill.
version: 2026-10-11
---

# film-on-explorer: read `FILM-ON-EXPLORER.md`, and `HPC.md`, first

This skill is a pointer. The plan, the pilot, and the rules are in [FILM-ON-EXPLORER.md](./FILM-ON-EXPLORER.md); the scripts are in `scripts/`. Read the `hpc` skill's `HPC.md` first: **ask before every `sbatch`, never compute on a login node, never type or read a password or key, delete only what you can list.**

Nothing here has been run on a compute node yet. The first job is a pilot, and its first check (can a compute node reach PyPI and npm?) decides whether the rest is possible. This is for Explorer, not AICR.
