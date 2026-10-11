---
name: aicr
description: Best-practice rules for an agent helping a researcher use the AICR GPU cluster (the shared AI Compute Resource at MGHPCC, login.aicr.ai, B200 and RTX PRO 6000 GPUs), written for researchers who are not experts in parallel computing. Use whenever a task involves AICR, ssh aicr, ood.aicr.ai, b200-batch, b200-devel, rtx-batch, rtx-devel, jobstats, or running GPU jobs there. Covers getting in with a key and certificate, partitions and GPU requests, the develop-then-batch workflow, idle-GPU cancellation, storage and the 30-day scratch purge, transfers, lessons from real AICR jobs, and ending a project. Builds on the hpc skill: load that first.
version: 2026-10-11
---

# AICR: read `HPC.md`, then `AICR.md`, before you touch the cluster

This skill is only a pointer. The rules are in two files:

```
HPC.md     ← the general rules (the hpc skill's file); read it first
AICR.md    ← in this folder; what is different or stricter on AICR, plus lessons from real jobs
```

Load the `hpc` skill's `HPC.md` first if you have not, then load [AICR.md](./AICR.md) in full, and follow both. AICR is **not** Explorer: usernames, partitions, storage and policy differ, and `AICR.md` says how.

The things to keep in mind even before you have read it:

1. **AICR is for production runs of code that already works.** Test on Explorer or locally; debug on a `*-devel` partition; submit `*-batch` only a tuned, unattended job.
2. **Every GPU you hold must be running kernels.** Idle GPUs are cancelled automatically. Verify the GPU in the first seconds of a job and fail the job yourself if CUDA is missing.
3. **One GPU, one node, until you have measured.** Over 80% utilisation on one GPU and DDP-ready code before you ask for more.
4. **No backups.** Scratch is purged after 30 days and AICR keeps no off-site copy: keep originals elsewhere.
5. **Never do the human-only login steps** (OnDemand sign-in, key download, passphrase, unlocking the key) and never read or print a key.
