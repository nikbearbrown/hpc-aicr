# FACTCHECK — Intro to GPUs on Explorer (lecture)

**Sources.** S = the training document and its repo scripts; SS = its screenshots. **Result.** 17 claims, all PASS. Checked 2026-10-06.

| # | Beat | Claim | Verdict | Source |
|---|---|---|---|---|
| 1 | B10 | gpu 8 h; gpu-interactive 2 h; gpu-short 2 h, prioritised; multigpu 24 h; courses-gpu 24 h; sharing 1 h, GPUs lent by PIs | PASS | S §partitions |
| 2 | B11 | the GRES list for gpu | PASS | S verbatim |
| 3 | B12 | NodeList/Gres/GresUsed command; per-node command; MIXED is CPU state | PASS | S |
| 4 | B13 | GPU Monitor app: idle/mixed/allocated nodes; pending GPU jobs by type | PASS | SS gpu-monitor2 |
| 5 | B20 | core definition; few complex vs thousands simple | PASS | S |
| 6 | B21 | Ferraris/bicycles; professors/stadium; matrix multiply; ML, simulation, data analysis | PASS | S |
| 7 | B30 | three ways | PASS | S |
| 8 | B31 | ssh; cd /scratch/$USER; git clone | PASS | S |
| 9 | B40 B41 | Standard Apps → VSCode Server; password, sharing, 1 GPU, Launch | PASS | S; SS |
| 10 | B42 | chmod, setup_python_env.sh, which python, gpu_simple.py prints CUDA_VISIBLE_DEVICES = 0 and the allocated line | PASS | S; gpu_simple.py |
| 11 | B50 B51 | srun --partition=sharing --gres=gpu:1 --pty bash; gpu_test_torch.py contents; vi + nvidia-smi | PASS | S; example1/ |
| 12 | B52 | submit_job.sh contents; sbatch | PASS | example1/submit_job.sh (comment lines omitted) |
| 13 | B60 | gpu-logs record values and times | PASS | S verbatim |
| 14 | B70 B71 | naive and batched code; 50,000 | PASS | S (import/device lines omitted to fit the card) |
| 15 | B72 | overhead per request vs one request | PASS | S |
| 16 | B73 | num_workers=0 vs 2, pin_memory, non_blocking | PASS | S (dataset line omitted) |
| 17 | B80 | four best practices; seff; CUDA/cuDNN; rchelp, office hours | PASS | S |
