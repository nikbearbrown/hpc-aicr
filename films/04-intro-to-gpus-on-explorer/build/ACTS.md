# ACTS — Intro to GPUs on Explorer (lecture)

**What this is.** Coverage map for the lecture film of `hpc/Intro-to-GPUs-2026/training_main.md`. **Result.** All thirteen agenda items are covered in eight acts, 21 body beats, about 6 min 45 s.

| Source section | Act | Beats |
|---|---|---|
| Accessing Explorer | III (B31) | B31 |
| Which GPU partitions | I | B10 |
| Which GPU types (sinfo %G; GresUsed; GPU Monitor app; MIXED) | I | B11 B12 B13 |
| What are GPUs, anyway (cores; Ferraris/bicycles; professors/stadium; uses) | II | B20 B21 |
| How do I use them (three ways) | III | B30 |
| Prerequisite (clone) | III | B31 |
| Open OnDemand (VS Code Server form; setup script; gpu_simple.py) | IV | B40 B41 B42 |
| Interactive GPU sessions (srun; gpu_test_torch.py; vi) | V | B50 B51 |
| Batch jobs with SLURM (submit_job.sh; sbatch) | V | B52 |
| Monitoring (nvidia-smi in script; gpu-logs) | VI | B60 |
| Using GPUs efficiently (batching; data loading) | VII | B70 B71 B72 B73 |
| Best practices; How to get help | VIII | B80 |

## LEFT OUT
- The presenter's name and "Spring 2026 Training Series" (credited in the description; datable).
- The two audience questions about the `sharing` partition (live-room prompts; the command they point to is shown in B12).
- The NVIDIA CPU-vs-GPU diagram and the pizza-delivery image: redrawn as B20/B21; the originals are not evidence.
- `vscode.png` (the dark VS Code window): not shown; its grey-on-dark UI text fails the type gate's local-contrast rule and the step it illustrates is spoken over B42.
- The `cd` into the repo and `which python` lines are kept; the optional "run gpu_test_torch.py too" step in the OOD demo is folded into B50/B51.

## Order
The source's order, with the ssh/clone prerequisite moved to Act III beside the three ways (it serves all three).

## Cast (series kit)
GPU block (B20 B72), job box / crates (B21 B72 B80), the drawn table grammar (B10), gpu-logs re-composed (B60).

## Self-contained check
Defines core, GPU, partition, GRES, srun, sbatch up front. Never says "this training", "recording" or "Spring 2026". Names Explorer and Northeastern because they are the subject. The source's `username` placeholder is kept as `username`.
