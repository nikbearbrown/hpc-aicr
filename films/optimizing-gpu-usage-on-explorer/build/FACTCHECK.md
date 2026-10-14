# FACTCHECK — Optimizing GPU Usage on Explorer

**What this is.** Every number and named claim in the film against its source. **Why.** Gate F. **Result.** All rows checked against the source files or the recorded login-node output; nothing was reproduced on a GPU node, and the film says so. Datable claims are attributed or stripped.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B11 | gpu-short and gpu-interactive 2 h, gpu 8 h, sharing 1 h | OK, recorded | `_real-outputs.md` sinfo -s | none |
| 2 | B11 | multigpu up to 24 h, needs an approved access request | OK, from source and HPC.md section 3 (not observed) | `training_main.md` 1.2; HPC.md | narration says "needs an approved access request" |
| 3 | B12 | three GPU partitions list the same 25 nodes | OK | sinfo -s T column 25 for gpu, gpu-short, gpu-interactive | none |
| 4 | B13 | five types on gpu: v100-sxm2, v100-pcie, a100, h200, t4; counts 4, 2, 3 or 4, 8, 4 | OK, recorded 2026-10-11 | `_real-outputs.md` gpu gres | "mostly four" for sxm2 (a node with 3 exists) |
| 5 | B13 | some written guides list only two types | OK | source table lists V100 and A100 only | worded "some written guides" |
| 6 | B14 | template lines as written | OK, verbatim | `slurm/v100_single_gpu.slurm` | read by sl() |
| 7 | B15 | --mem is CPU memory; raising it never fixes a GPU OOM | OK | source 1.1; HPC.md 6 | none |
| 8 | B15 | bare gpu:1 may land on a different card | OK | source 1.1 | none |
| 9 | B16 | PyTorch wheels carry their own CUDA runtime; no CUDA module | OK | source 1.1; setup_env.sh | none |
| 10 | B17 | gpu-logs and seff on PATH, nvidia-smi missing, python/3.13.5 module | OK, recorded | `_real-outputs.md` commands present; module avail | none |
| 11 | B18 | verify script checks five things; round trip proves use | OK | `01_gpu_verify.py` | none |
| 12 | B19 | CUDA_VISIBLE_DEVICES 0, 0,1, unset in interactive; never proof | OK (source says unset is normal; HPC.md says not proof either way) | source 1.4; HPC.md 6 | none |
| 13 | B20 | utilization = share of last second a kernel ran; below 50 wrong; example 87 percent, about a fifth memory | OK, example from source (87%, 18432 of 81920 MiB) | source 2.1 | labelled "example" |
| 14 | B21 | a coding agent should not run watch | OK | HPC.md section 1 | none |
| 15 | B22 | 2x2 readings; 15/75 is data starvation | OK | source 2.1, 2.2, 5.1 | none |
| 16 | B23 | bands 50/60/70/80; memory 60 to 90 healthy, under 40 room | OK, house rule | HPC.md section 6 | "use one set of bands" |
| 17 | B24 | Idle Bot: email after about 15 min, cancel after about an hour; no published percentage | OK, from HPC.md, not observed | HPC.md section 3 | "about"; "we found no published percentage" |
| 18 | B30-B35 | tool layers; profiler window; timeline patterns | OK | source section 3 | questionable nsys rows left out |
| 19 | B31 | under 30 min, skip batch queue | OK, source rule of thumb | source 3.2 | none |
| 20 | B33 | example table: loader 1.843 s CPU, 0 CUDA | OK, source illustration, labelled not our run | source 3.3 | on-screen tag |
| 21 | B34 | nsys on Explorer unconfirmed | OK | guide section III | stated |
| 22 | B35 | 15 ms burst, 50 ms gap | OK, source example | source 3.4 | tagged "example" |
| 23 | B40 | 25 ms compute, 60 ms loader, 35 idle of 60 = 58 percent | OK arithmetic 35/60 = 58.3 | source 4.1 callout | tagged "example" |
| 24 | B43-B44 | four settings; workers = cpus - 1; pin always; persistent when workers above 0; prefetch 2; cpus = workers + 1, at least 4 | OK | source 4.2; HPC.md 6 | none |
| 25 | B45 | benchmark has configs A to D | OK | `03_dataloader_benchmark.py` | not run by us |
| 26 | B46 | 10,000 samples pay overhead 10,000 times | OK | `02_naive_vs_batched.py` | none |
| 27 | B47 | home, scratch, projects are network filesystems; scratch purged | OK | source; HPC.md section 3 | none |
| 28 | B48 | 18, 55, 82 percent; about 420, 1300, 1950 images/s | OK, quoted illustration, no script behind it | source 4.3 | labelled, "no script produces these" |
| 29 | B50-B51 | doubling roughly doubles throughput until saturated; leave a margin | OK | source 5.2; guide | none |
| 30 | B52 | autocast around forward and loss, backward outside; weights, loss, normalization stay 32-bit | OK | source 5.3; guide | none |
| 31 | B53 | FP32 8/23, BF16 8/7, FP16 5/10 bits; BF16 on A100 and newer, FP16 + GradScaler on V100 and T4 | OK; H200 not named (inferred only) | source 5.3 table | H200 omitted |
| 32 | B54 | script 05 uses is_bf16_supported; script 06 picks by capability major 8 | OK, verbatim | scripts 05, 06 | none |
| 33 | B55 | total memory does not halve; "up to 8x" vs "1.5 to 3x" | OK | source 5.3; script 05 | none |
| 34 | B56 | 60 to 70 percent less activation memory, 30 percent more compute, uncited | OK, labelled "with no source" | source 5.4 | none |
| 35 | B60 | 20 percent on one card becomes four at 20; add cards above 80; under 60 fix first | OK | source 6.1 | none |
| 36 | B61-B63 | DDP rules, all-reduce | OK | source 6.2, 6.3 | none |
| 37 | B64 | three numbers must agree; one node | OK, rule from template and HPC.md | HPC.md section 6 | none |
| 38 | B65 | comment after trailing backslash breaks both templates | OK, stated in guide and HPC.md section 12, bash behaviour not run by us | guide; HPC.md | worded "ends the line there" |
| 39 | B66 | efficiency formula; above 80 pays, below 70 stop, 70 to 80 undescribed | OK | source 6.4; guide | none |
| 40 | B70-B74 | loop, decision guide, checklist | OK | source 7.1, 7.2, 7.4 | none |
| 41 | B72 | gpu-logs keeps about 7 days, public nodes only; not run by us | OK, from HPC.md | HPC.md section 6 | stated |
| 42 | B80-B81 | domains; Hugging Face flags bf16, gradient_checkpointing, dataloader_num_workers | OK | source section 8 | worker count "from your CPU count" |
| 43 | B82 | Explorer versus AICR differences | OK, recorded for both logins | guide table; `_real-outputs.md` | none |
| 44 | B83 | what was checked vs read | OK | guide "What we tested" | none |
| 45 | B84 | rchelp@northeastern.edu; office hours; consultation | OK | source | none |

Stripped: no date or version except the recorded python 3.13.5, labelled "recorded".
