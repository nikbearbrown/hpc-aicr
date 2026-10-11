---
name: hpc
description: Best-practice rules for an agent helping a researcher use Northeastern's Explorer cluster or any shared Slurm HPC cluster, written for researchers who are not experts in parallel computing. Use whenever a task involves Explorer, HPC, Slurm, sbatch, srun, salloc, squeue, job arrays, GPUs or CPUs on a cluster, modules, conda or containers on a cluster, scratch or projects storage, or "my job is slow or too big". Covers what the agent must never do, whether parallel is even the answer, sizing a request, GPUs, storage, software, reproducibility, and how an agent logs in safely. For the AICR GPU cluster also load the aicr skill.
version: 2026-10-11
---

# HPC: read `HPC.md` before you touch the cluster

This skill is only a pointer. The rules are in one file:

```
HPC.md     ← in this folder; read it completely before running any cluster command
```

Load [HPC.md](./HPC.md) now, in full, and follow it. Do not work from memory of general Slurm advice: the file holds limits, traps and decisions specific to Northeastern's Explorer cluster, and it marks every unconfirmed item.

The three things to keep in mind even before you have read it:

1. **Look before you act.** Read-only commands first. Measure before you change. Ask before you spend, delete, or change who can see data.
2. **Never compute on a login node**, never hold an idle GPU, never type or read a password, passphrase or key, and never use `ssh` from an agent without `-o BatchMode=yes`.
3. **Say what you did not confirm.** If a limit, quota or policy is not in `HPC.md` or confirmed live, tell the researcher to ask Research Computing (rchelp@northeastern.edu).

If the task is on the AICR cluster (`login.aicr.ai`, B200 or RTX PRO 6000 GPUs), also load the `aicr` skill and read `AICR.md` after `HPC.md`.
