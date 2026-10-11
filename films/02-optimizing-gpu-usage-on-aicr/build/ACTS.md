# ACTS — Optimizing GPU Usage on AICR (lecture)

**What this is.** Coverage map for the lecture film of `hpc/AICR-Optimizing-GPU-Usage/aicr-gpu-optimization.md` (AICR Training Workshop 2). **Why.** A lecture covers the whole source; every section lands in an act or is listed as left out. **Result.** All eight numbered sections plus the opening question, the quick reference and the help section are covered in eight acts, 38 body beats, 14 min 29 s. Two parts of the source are left out, both for the reason the source itself gives.

| Source section | Act | Beats |
|---|---|---|
| The Question Nobody Asks; "measure before you change" | BIDEA, BVDT | BIDEA |
| Prerequisites (OOD login, srun into b200-devel, modules, clone, setup_env) | folded: the srun/devel habit is Act III B31; username and OOD were the first film's subject | — |
| 1 Do you even have the GPU (silent failures, partitions, minimal script, mem vs VRAM, verify script, CUDA_VISIBLE_DEVICES, idle cancellation) | I | B10–B16 |
| 2 Seeing your GPU live (nvidia-smi, the quiz, two axes, nvitop) | II | B20–B23 |
| 3 The profiling toolchain (layers, devel→batch workflow, PyTorch Profiler, reading it, nsys) | III | B30–B34 |
| 4 Data starvation (factory, diagnostic, the quiz, four knobs, biggest win) | IV | B40–B44 |
| 5 Memory vs utilization (two metrics, decision table, batch size, BF16, precision table and trade-offs, checkpointing) | V | B50–B56 |
| 6 Multi-GPU (80% rule, DDP all-reduce, checking DDP, scaling efficiency) | VI | B60–B63 |
| 7 The workflow (loop, decision guide, jobstats, checklist, hygiene) | VII | B70–B73 |
| 8 Your research domain; How to get help | VIII | B80 B81 |
| Quick reference card; AICR at a glance | BVDT (recap) | BVDT |

## LEFT OUT

- **Section 4.2 "AICR Storage: Where Your Data Lives Matters" and the `$TMPDIR` rsync block.** The source has this whole section inside an HTML comment ("commented out — kept for reference") and removed its rows from the checklist, decision guide and reference table. The film follows the source's own decision.
- **Prerequisites step-by-step (clone the repo, run setup_env.sh).** Procedure for the live workshop room, not a teaching point; the devel-session habit it introduces is taught in B31.
- **Presenter notes and "image prompt for slide" HTML comments.** Production notes, not content.
- **"An idle B200 is roughly 2.5× more expensive to waste than an idle A100."** Unsourced in the document; stripped (FACTCHECK row 2).
- **"Consider vLLM (covered in Workshop 3)."** Datable cross-reference to a session that does not exist in this film; stripped.
- **nvidia-smi 2.1 note "GPU-Util 84% … Below 50%? We need to check something!"** Kept. The 2.2 ASCII diagram is redrawn as B22.

## Order

The source's order is kept. The hygiene points of 7.5 are spoken inside B70 (one change at a time, baselines) and B73 (cancel the devel session).

## Cast (continued from film 1, same kit)

| Object | Picture | Beats |
|---|---|---|
| a GPU | dark block, light turns terracotta when busy | B10 B13 B14 B15 B16 B21 B22 B60 B61 |
| a job | small kraft box, one terracotta tape | B10 B16 B21 B22 B31 B73 |
| the racks | dark server stacks | B10 |
| meters / gauges | ink arc with needle, terracotta only at the mark | B21 B50 B51 B60 |

## Self-contained check

The source leans on Workshop 1 ("logging in, storage, partitions, submitting your first job"), on Explorer, and on A100/V100 comparisons. The film never says "Workshop 1" or "the previous session"; B11 re-states the partitions it needs; "the cards you may be used to" replaces named older GPUs except where the source's own numbers need them (B52 says only "a B200 with 192 GB"). Six prerequisite terms are defined in BDEFS. The presenter is credited in the description, not in the film.
