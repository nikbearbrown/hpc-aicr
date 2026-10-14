# ACTS — Optimizing GPU Usage on Explorer (lecture)

**What this is.** Coverage map for the lecture film of Northeastern Research Computing's training on GPU profiling and optimization on Explorer (`training_main.md`, six demo scripts, two Slurm templates, `setup_env.sh`), checked against our written guide and rule file. **Why.** A lecture covers the whole source; every section lands in an act or is listed as left out. **Result.** All eight numbered sections, the opening, the quick reference and the help section are covered in eight acts, 55 body beats, about 15 min 2 s of narration.

| Source section | Act | Beats |
|---|---|---|
| Opening: the question nobody asks; measure first | BIDEA, BVDT | BIDEA |
| Prerequisites (ssh, srun, clone, setup_env) | folded: venv and pip in B16; the interactive session in B31 | B16, B31 |
| 1 Do you even have the GPU (silent failures, Slurm request, partitions, verify script, CUDA_VISIBLE_DEVICES) | I | B10-B19 |
| (added, not in the source: Idle Bot; recorded login-node facts) | I, II | B17, B24 |
| 2 Seeing your GPU live (nvidia-smi, the quiz, two axes, nvitop, bands) | II | B20-B24 |
| 3 The profiling toolchain (layers, interactive profiling, PyTorch profiler, reading it, Nsight Systems) | III | B30-B35 |
| 4 Data starvation (factory analogy, stopwatch tests, four knobs, batching, storage, illustrative table) | IV | B40-B48 |
| 5 Memory versus utilization (batch size, mixed precision, formats, checkpointing, memory monitor) | V | B50-B57 |
| 6 Multi-GPU (80 percent rule, data parallel, DDP code, Slurm request, template trap, scaling efficiency) | VI | B60-B66 |
| 7 The workflow (loop, decision guide, gpu-logs, checklist, hygiene) | VII | B70-B74 |
| 8 Connecting to your work; how to get help; Explorer reference | VIII | B80-B84 |
| Quick reference card; Explorer at a glance | BVDT; corrected in B13, B82 | — |

## LEFT OUT
- **Presenter notes in HTML comments and the "question for audience" prompts as such.** Production notes; the answers are taught (B22, B33).
- **The nsys 'timeline patterns' rows on `.to(device)` in the DataLoader worker, `--nproc_per_node` tuning and `find_unused_parameters`, and 'two GPU streams alternate'.** Questionable or not actionable (see FACTCHECK rows 31-32); B35 teaches the three patterns that are sound.
- **`scripts/05` and `scripts/06` full bodies, `01_gpu_verify.py` print blocks.** Shown by excerpt only where the idea needs it (B18, B54).
- **The missing `scripts/07_gpu_logs_guide.py`.** It is not in the repository; B72 shows the command only.
- **The original's `train.py` / `train_ddp.py` flags.** Not provided; B65 says to supply your own.

## Order
The source's order is kept. IdleBot is added to Act II (the consequence of low utilization), recorded login-node facts to Act I, and the Explorer-versus-AICR comparison to Act VIII, all from our guide and rule file.

## Cast
| Object | Picture | Beats |
|---|---|---|
| a GPU | dark card, ghost light (terracotta when busy) | B10 B15 B19 B24 B40 B60 B61 |
| a job | small kraft box with one terracotta tape | B10 B24 B40 B70 |
| the processor | dark chip with kraft pins | B10 B19 |
| VRAM | open white tank | B15 B50 |
| a person | Professor Bear portrait | B84 |

## Self-contained check
The narration never says 'the guide', 'the lesson', 'the training' or a section number; Research Computing is named as the source of facts only where a fact needs it (B14, B33, B48, B55, B65, B84). The second cluster is introduced in one sentence in B82. The presenter is credited in the description, not in the film. Six prerequisite terms are in BDEFS. No video number appears anywhere.
