---
name: film-on-explorer
description: Plan and scripts for rendering a narrated lecture film on Northeastern's Explorer cluster (not AICR): pack the film and the brutalist.art toolkit, stage them in a job-scoped scratch folder, run a one-time toolchain setup and a render with Slurm, fetch the master back, and delete only the job folder after a yes. Use when a professor or an agent wants to render lecture films on the HPC cluster instead of a laptop, or asks how to package the toolkit for the cluster. Loads on top of the hpc skill.
version: 2026-10-11
---

# film-on-explorer: read `FILM-ON-EXPLORER.md`, and `HPC.md`, first

This skill is a pointer. The plan, the pilot, and the rules are in [FILM-ON-EXPLORER.md](./FILM-ON-EXPLORER.md); the scripts are in `scripts/`. Read the `hpc` skill's `HPC.md` first: **ask before every `sbatch`, never compute on a login node, never type or read a password or key, delete only what you can list.**

Piloted once, on 2026-10-11, with one finished film: it rendered on a compute node and matched the Mac's master (same size, frame rate and duration; sampled frames scored 0.948 to 0.9999 on a similarity scale where 1 is identical). Rendering needs no internet; the one-time install uses the cluster's proxy, which `module purge` removes (the setup script loads `explorer/1.0` first to keep it). The install is one idempotent script (`scripts/bootstrap_toolkit.sh`, read-only unless `--sync-code` or `--sync-scripts`). The heavy rendering runs on a compute node, everything else on the researcher's computer. **Caveat:** Gate T (typography) failed two beats on the cluster that passed at home, so a film rendered here is checked again at home before it is posted. This is for Explorer, not AICR.
