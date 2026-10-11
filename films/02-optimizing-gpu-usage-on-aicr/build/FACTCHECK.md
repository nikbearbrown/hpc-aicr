# FACTCHECK — Optimizing GPU Usage on AICR (lecture)

**What this is.** Every factual claim in the narration and on screen, checked. **Sources.** S = the workshop document; D = the saved AICR documentation pages in `aicr/`; C = the live cluster, read-only (`SESSION.md`); N = NVIDIA's published B200 / RTX PRO 6000 specifications (as restated by S). **Result.** 30 claims: 27 PASS, 2 CORRECTED, 1 STRIPPED. Checked 2026-10-06.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | many GPU jobs leave the GPU idle much of the time; measure before you change | PASS | S "The Question Nobody Asks" | |
| 2 | — | "an idle B200 is roughly 2.5× more expensive to waste than an idle A100" | STRIPPED | S, unsourced | not spoken |
| 3 | B10 | unloaded CUDA module → PyTorch runs on CPU with no error; --gres typo → wrong node; stale CUDA_VISIBLE_DEVICES | PASS | S §1 | |
| 4 | B11 | four GPU partitions; B200 192 GB; RTX PRO 6000 96 GB; devel 4 h, batch 24 h | PASS (note) | S §1.1; C (partitions, walltimes) | D's hardware page says 180 GB HBM3e per B200; S says 192 GB throughout and its nvidia-smi sample reads 196608 MiB; the film follows S, the training the film is of |
| 5 | B12 | the minimal script | PASS | S §1.2 verbatim; comments shortened | `cuda/13.1` resolves on C |
| 6 | B13 | --mem is CPU RAM not VRAM; DataLoader workers use the cpus-per-task cores | PASS | S §1.2 | "eight cores means seven workers and one main" follows S's `num_workers = cpus-per-task − 1` |
| 7 | B14 | the verify script's five checks; is_available() vs a round trip | PASS | S §1.3 and `scripts/01_gpu_verify.py` | |
| 8 | B15 | CUDA_VISIBLE_DEVICES values and meanings; never override | PASS | S §1.4 | |
| 9 | B16 | idle GPU jobs are cancelled; profile in devel | PASS | S §1.5; the first film | |
| 10 | B20 | nvidia-smi sample rows; 84% healthy, below 50% check; 24576/196608 MiB = 12% | PASS | S §2.1 (12.5%, S says 12%) | |
| 11 | B21 | 12% util + 91% memory = data starvation | PASS | S §2.1 quiz | |
| 12 | B22 | the two-axes model and target zone 80–100% util, 70–90% memory | PASS | S §2.2 | |
| 13 | B23 | nvitop shows per-process use, memory trend, power, temperature | PASS | S §2.3 | |
| 14 | B30 | four layers and their tools/questions | PASS | S §3.1 | |
| 15 | B31 | devel → batch workflow; 50–100 steps; > 70% | PASS | S §3.2 | |
| 16 | B32–B34 | profiler code; reading order; nsys flags; 50–100 steps | PASS | S §3.3–3.4 verbatim | scp line generalized to USER@login.aicr.ai (S has placeholders) |
| 17 | B40 | 8 ms vs 50 ms factory analogy; B200 much faster than older cards | PASS | S §4.1 | "A100" not named; "the cards you may be used to" |
| 18 | B41–B42 | diagnostic code; 45 ms / 9 ms → 80% wasted | PASS | S §4.1 | |
| 19 | B43–B44 | four knobs, start values; num_workers 0 → 4 often 20% → 60–80% | PASS | S §4.2 | |
| 20 | B50–B51 | metric meanings; decision table | PASS | S §5.1 | |
| 21 | B52 | doubling batch ≈ doubles throughput if not saturated; 15–20% memory → 4–8× room; binary search; 70–85% | PASS | S §5.2 | |
| 22 | B53–B55 | autocast BF16; halves activation memory; 2–4× matmuls; no GradScaler; master weights/loss/softmax/norm stay FP32 | PASS | S §5.3 | |
| 23 | B54 | bit splits FP32 8/23, BF16 8/7, FP16 5/10, FP8 4/3 | PASS | S §5.3 table; IEEE 754 / bfloat16 definitions | |
| 24 | B56 | checkpointing: −60–70% activation memory, ~+30% compute; when to use | PASS | S §5.4 | |
| 25 | B60 | 80% rule; < 60% fix first; I/O-bound gets worse | PASS | S §6.1 | |
| 26 | B61 | DDP all-reduce; NVLink in-node fast, across nodes slower | PASS | S §6.2 | |
| 27 | B62–B63 | DDP checks; torchrun; efficiency bands > 80 / 70–80 / < 70 | PASS | S §6.3–6.4 | |
| 28 | B70–B71 | the seven-step loop; the decision tree thresholds | PASS | S §7.1–7.2 | |
| 29 | B72 | jobstats from Princeton RC runs on AICR; the report's values 13/25/80/17, 55:09 run, 08:00 limit, 11% note | PASS | S §7.3; C verbatim | the film says "an RTX card" (rtx-batch, 95.6 GB total) |
| 30 | B73, B80 | checklist items; devel limit 4 running jobs; domain mapping; rchelp@northeastern.edu | CORRECTED | S §7.4–8 | "Consider vLLM (Workshop 3)" dropped as datable; "Molecular dynamics: copy inputs to fast storage" dropped because S commented its storage section out |

## Stripped as datable or unsourced

Row 2 (2.5× cost claim); "Workshop 1/3" cross-references; the A100/V100 comparisons except as S's own numbers inside B52's "192 GB" statement.

## Pronunciation note

"AICR" is voiced "acre" as in the earlier AICR films.
