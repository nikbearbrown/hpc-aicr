# ACTS — Intro to Parallel Computing (lecture)

**What this is.** Coverage map for the lecture film of `hpc/Intro-to-HPC-Scaling-Parallel-Computing-2026/intro_to_parallel_computing.md`. **Result.** All nine agenda sections are covered in nine acts, 26 body beats, about 9 min 50 s.

| Source section | Act | Beats |
|---|---|---|
| 1 Why parallel (pipelining tables) | I | B10 |
| 2 Flynn's taxonomy | II | B20 |
| 3 Shared vs distributed; hybrid; Slurm ntasks vs cpus-per-task | III | B30 B31 |
| 4 Amdahl's law; Gustafson's law; programming tip | IV | B40 B41 |
| 5 Game of Life: serial, OpenMP (+ job), MPI+OpenMP (decomposition, halo, job), benchmark | V | B50 B51 B52 B53 B54 B55 |
| 6 GPU computing: CPU vs GPU; CUDA steps; kernel | VI | B60 B61 B62 |
| 7 PyTorch: single GPU, multi-GPU, DDP, benchmark | VII | B70 B71 B72 B73 |
| 8 Python mpi4py; R; MATLAB; choosing the tool | VIII | B80 B81 B82 B83 |
| 9 Takeaways; Slurm recipes; help | IX | B90 B91 |

## LEFT OUT
- Presenter and "Spring 2026" framing (credited in the description; datable).
- The source's PNG charts (`amdahls_law.png`, `gustafsons_law.png`, `time_comparison.png`, `speedup_comparison.png`, `gpu_time_comparison.png`, `mpi_halo_exchange.png`, Game of Life GIFs): redrawn as B40, B41, B55, B73, B53, B50 from the source's own tables and formulas (WHOLE-SOURCE LAW 5).
- The single-GPU and multi-GPU sbatch headers (§7.1, §7.2): spoken in B70/B71 ("one GPU on the gpu partition"; "two GPUs on multigpu"); the recipes beat B91 carries the GPU header.
- "Other Python parallel tools": named in B80 narration only.

## Order
The source's order.

## Cast
Node plinths and core pads (B30 B31 B53), CPU/GPU blocks (B20 B60 B61), kraft blocks (B10), the series' drawn-table and chart grammar.

## Self-contained check
Defines core, node, thread, process, MPI, speedup up front. Explorer is not the subject here; Slurm is named because the recipes are Slurm. Never says "this training" or "the session".
