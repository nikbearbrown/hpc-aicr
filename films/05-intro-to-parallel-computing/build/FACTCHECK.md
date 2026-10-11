# FACTCHECK — Intro to Parallel Computing (lecture)

**Sources.** S = the training document and repo code; the formulas are checked by computation. **Result.** 18 claims, all PASS. Checked 2026-10-06.

| # | Beat | Claim | Verdict | Source |
|---|---|---|---|---|
| 1 | B10 | serial 9 slots, pipelined 5, data-parallel 3 for three loads | PASS | S tables, counted |
| 2 | B20 | SISD/SIMD/MISD/MIMD definitions and examples | PASS | S |
| 3 | B30 | shared: one RAM, OpenMP, one-machine limit; distributed: own RAM, network, MPI; hybrid | PASS | S |
| 4 | B31 | ntasks = processes/ranks; cpus-per-task = cores per process; 4×5 = 20; pure OpenMP 1×20; pure MPI 20×1 | PASS | S |
| 5 | B40 | Speedup = 1/(S + P/N); S = 0.1 → ceiling 10×; strong scaling | PASS | S; limit N→∞ of 1/(0.1 + 0.9/N) = 10 |
| 6 | B41 | Speedup = S + P·N; 100 cores → 100× problem in the same time; weak scaling; plan first | PASS | S |
| 7 | B50 | each cell depends on its 8 neighbours; independent within a step | PASS | S |
| 8 | B51 B52 | the pragma; OpenMP job: 1 task, 20 cpus, OMP_NUM_THREADS from Slurm, 10000×10000×500 | PASS | S |
| 9 | B53 B54 | strips per rank; halo rows via MPI_Send/Recv; hybrid job 4×4×5 = 80 | PASS | S |
| 10 | B55 | the ten benchmark rows | PASS | S table verbatim |
| 11 | B60 | CPU latency / GPU throughput; tens vs thousands; chefs vs line cooks | PASS | S |
| 12 | B61 B62 | allocate, copy, launch, copy back; kernel computes one element; 1024² > a million threads | PASS | S (1,048,576) |
| 13 | B70 B71 | single-GPU and sharded code; gpu / multigpu partitions | PASS | S |
| 14 | B72 | nccl, world size, rank, local rank; all_reduce == world_size test | PASS | S |
| 15 | B73 | 11.73 s / 5.48 s (2.1×) / 5.08 s (2.3×); sync dominates at this size | PASS | S table |
| 16 | B80–B82 | mpi4py, R parallel/foreach, MATLAB parfor code | PASS | S (R's two snippets joined on one card) |
| 17 | B83 | the eight-row tool table | PASS | S |
| 18 | B90 B91 | four takeaways; three Slurm recipes | PASS | S |

## Stripped as datable
"Spring 2026"; the presenter's name (in the description).
