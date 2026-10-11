# SHOTLIST — Optimizing GPU Usage on AICR (lecture)

**What this is.** One row per body beat: what the sentence is about, the lane picked, the runner-up, why (BEST-BEAT LAW). **Result.** 38 body beats: 27 Manim (6 isometric/cast scenes, 21 charts, tables, meters, diagrams), 9 real code listings, 2 real-command terminals, 1 large-icon row. No text-only cards in the body. Real evidence: Bear's own job 318592 read with `jobstats` (B72); the workshop's own nvidia-smi sample (B20).

| Beat | About | Lane | Runner-up | Why |
|---|---|---|---|---|
| B10 | three silent failures | cast scenes: job lands on CPU, wrong rack, stale tag | text list | "silent" is the point: a job landing on the wrong block with no alarm shows it |
| B11 | four GPU partitions, VRAM, walltime | drawn table + VRAM bars | real sinfo (film 1) | the source's table is the figure; bars make 192 vs 96 visible |
| B12 | minimal job script, the request | **the real script** in a plain terminal (`cat`) | ClaudeCodeBeat | a header of #SBATCH lines is all comments to the type gate (§8.12); the terminal shows it verbatim, as film 1 does |
| B12B | the work lines | **the real commands** in a plain terminal | ClaudeCodeBeat | same |
| B13 | CPU RAM vs VRAM; cores → workers | cast: RAM box on CPU side, VRAM slab on GPU; 8 core pads | two-column card | a spatial confusion ("which memory?") answered spatially |
| B14 | five checks of the verify script | checklist landing + tensor round trip | code listing of 01_gpu_verify.py | the round trip is a motion (CPU → GPU → CPU); the script's 132 lines would be unreadable |
| B15 | CUDA_VISIBLE_DEVICES values | mono rows + GPU blocks lit per value | table | the value maps to a count of lit cards |
| B16 | idle GPU cancellation | re-use of film 1's idle-cancel scene | — | same fact, same picture (cast continuity across the series) |
| B20 | nvidia-smi: the two numbers | drawn dark terminal with the workshop's exact sample rows; rings | CCPlainShell | the sample is 75 chars wide; CCPlainShell would ellipsize it; the drawing keeps the text verbatim and can ring the two numbers |
| B21 | 12% util + 91% memory | two gauges + starved GPU | 2×2 (next beat) | the quiz is two readings; two gauges |
| B22 | the two-axes model | 2×2 grid with cast miniatures | the source's ASCII diagram as text | the source's own figure, redrawn (WHOLE-SOURCE LAW 5) |
| B23 | nvitop | **real commands** (CCPlainShell) | drawn TUI | no capture possible (needs a GPU session); a drawn TUI would invent content; the commands and the source's own description are real |
| B30 | four profiling layers | ladder, rung by rung | table | layers are a ladder |
| B31 | profile in devel, run in batch | two lanes, belt across | flowchart card | the job's journey; same belt grammar as film 1 |
| B32 | profiler code | **real code** | — | it is code |
| B33 | how to read the profile | kernel timeline with gaps + bars | table of columns | "gaps between kernels" is a picture; the table of column names is not |
| B34 | Nsight Systems | **real commands** | — | commands |
| B40 | factory analogy | isometric press + truck with timers | bar chart | the source's own analogy, drawn; the chart comes next |
| B41 | the two-timing diagnostic | **real code** | — | it is code |
| B42 | 45 ms vs 9 ms → 80% | two bars on one time axis | stat card | the waiting span IS the 80% |
| B43 | DataLoader four knobs | **real code** | — | it is code |
| B44 | knob start values; 0 → 4 workers | four dials + utilization bar | table | dials turn; the bar jumps on the one-line change |
| B50 | two metrics, independent | two meters moving independently | table | independence is shown by needles not moving together |
| B51 | decision table | drawn table with gauge icons | text table | the source's table, icons instead of the words low/high |
| B52 | batch size, binary search | VRAM bar + search marker jumping | code listing of the search | the search IS halving a gap; show the gap halving (the code is in the source, shown as its idea) |
| B53 | BF16 autocast | **real code** before/after | — | it is code |
| B54 | exponent vs mantissa | four bit-bars 8|23 · 8|7 · 5|10 · 4|3 | precision table | the bits are the argument; same-length exponent segments show why BF16 needs no scaler |
| B55 | what BF16 buys; what stays FP32 | model blocks: shrink, speed tag, four stay FP32 | bullet card | "mixed" is shown as some blocks changing and some not |
| B56 | gradient checkpointing | **real code** | recompute diagram | one call in HF, one wrapper in PyTorch: the code is the lesson |
| B60 | the 80% rule | one GPU splitting into four; waste ×4 | table | multiplication of waste is a picture |
| B61 | DDP all-reduce | three GPUs, gradients merge and return | the source's ASCII diagram | the source's figure, drawn with the cast |
| B62 | checking DDP, torchrun | **real code** | — | it is code |
| B63 | scaling efficiency | measured vs ideal bars, three bands | formula card | the shortfall from ideal is the efficiency |
| B70 | the optimization loop | seven-step ring; second fix pushed out | table | a loop is a ring; "one change" is a motion |
| B71 | decision guide | tree lighting up | the source's ASCII tree as text | the source's figure, drawn |
| B72 | jobstats | **real report** (job 318592) re-composed with bars at the real values | the demo script's simulated report | a real report beats a simulated one; SHOW-THE-THING rung 1 |
| B73 | pre-submission checklist | ten checkboxes ticking; devel slot clears | text card | a checklist is checkboxes; labels 1–3 words |
| B80 | four research domains | large library icons (LibraryIconRow) | FormBCard | four named things, each with a mark |
| B81 | HF TrainingArguments | **real code** | — | "one flag each" is the code |

## Tool beats and their SHOW-THE-THING rung

| Beat | Tool | Rung | Evidence |
|---|---|---|---|
| B20 | nvidia-smi | the workshop's own sample output, verbatim | source §2.1 |
| B23, B34 | nvitop, nsys | real commands, no output (no GPU session available to this build) | source §2.3, §3.4 |
| B72 | jobstats | 1, real output | `SESSION.md`: job 318592, read 2026-10-06 |
| B12 B32 B41 B43 B53 B56 B62 B81 | code | the source's own code, verbatim lines (comments shortened to fit the card) | source |
| scripts/0N_*.py demos | the workshop's demo scripts | NOT run (need a GPU node; job submission is outside this build's permissions) | named in narration only (B14) |
