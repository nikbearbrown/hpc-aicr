# SHOTLIST — Optimizing GPU Usage on Explorer

**What this is.** One row per body beat: what the sentence is about, the lane picked, the runner-up, why. **Why.** BEST-BEAT LAW. **Result.** 26 terminal beats (`CCPlainShell`, text read verbatim from the source files or the recorded real output), 29 Manim beats, 6 bookends.

| beat | about | lane picked | runner-up | why this one wins |
|---|---|---|---|---|
| B10 | A kraft job box with a terracotta tape rolls into a finish gate and a check lands at the gate (job finished, n | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B11 | A horizontal bar chart on an hours ruler (0 to 24 h): 'sharing' 1 h, 'gpu-short' 2 h, 'gpu-interactive' 2 h, ' | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B12 | I · Partitions  ·  recorded on the login node, read-only | terminal (CCPlainShell), recorded real output | Manim code card | the evidence IS text; a terminal shows it as written |
| B13 | I · GPU types on partition gpu  ·  recorded, selected rows | terminal (CCPlainShell), recorded real output | Manim code card | the evidence IS text; a terminal shows it as written |
| B14 | I · The request  ·  a batch script header, as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B15 | Left half: a node with a RAM slot (kraft block, mono label '--mem=32G') and a separate GPU card block with its | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B16 | I · The environment  ·  from the setup script | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B17 | I · Login node  ·  recorded read-only | terminal (CCPlainShell), recorded real output | Manim code card | the evidence IS text; a terminal shows it as written |
| B18 | I · Verify at runtime  ·  01_gpu_verify.py, excerpts | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B19 | A mono tag 'CUDA_VISIBLE_DEVICES' at the top; below, three small states side by side: '0' with one GPU block l | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B20 | Two drawn gauges side by side (ink arcs with a needle): left 'GPU-Util' with the needle at 87 and a one-second | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B21 | II · Watching  ·  the commands, from the source, not run by us | terminal (CCPlainShell), not run by us | Manim code card | the evidence IS text; a terminal shows it as written |
| B22 | A drawn 2x2 grid: utilization across (low to high), memory up (low to high) | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B23 | Two horizontal scales stacked | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B24 | A GPU-utilisation line on a time axis that starts busy and then sinks to a flat low stretch; a watcher marker  | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B30 | A ladder of four rungs drawn bottom to top, light to heavy: 'live' (nvidia logo chip + mono 'nvidia-smi'), 'fr | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B31 | III · An interactive session  ·  from the source, not run by us | terminal (CCPlainShell), not run by us | Manim code card | the evidence IS text; a terminal shows it as written |
| B32 | III · PyTorch profiler  ·  04_pytorch_profiler_demo.py, excerpts | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B33 | A drawn horizontal bar pair per row (CPU total in grey, CUDA total in ink) for four rows: 'DataLoader | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B34 | III · A timeline  ·  from the source, not run by us | terminal (CCPlainShell), not run by us | Manim code card | the evidence IS text; a terminal shows it as written |
| B35 | A timeline drawing with two rows on a time axis: a 'GPU' row of short ink bursts with long empty gaps between  | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B40 | A single time bar of 60 units (tagged 'example'): the first 25 units filled ink 'GPU computes 25 ms', the rema | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B41 | IV · Stopwatch test one  ·  the loader alone | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B42 | IV · Stopwatch test two  ·  the compute alone | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B43 | IV · The four settings  ·  as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B44 | Four chips in a row, each with a mono name and a value tag: 'num_workers' -> 'cpus - 1'; 'pin_memory' -> 'True | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B45 | IV · The benchmark  ·  03_dataloader_benchmark.py, excerpts | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B46 | IV · One at a time, or batched  ·  02_naive_vs_batched.py, excerpts | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B47 | Three storage boxes in a row, each labelled in mono: '/home' (small, a cross on 'datasets'), '/scratch' (a che | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B48 | Three bar pairs left to right on a shared ruler (tagged 'illustration from the source, not our run'): utilizat | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B50 | A tall tank labelled 'VRAM' with a batch block of height 20% sitting in it; the block doubles (40%) and a thro | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B51 | V · Finding the largest batch  ·  as written, excerpts | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B52 | V · Mixed precision  ·  the change, as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B53 | Three rows of bit cells, drawn as segmented bars: 'FP32' = 1 sign + 8 exponent (range) + 23 mantissa (precisio | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B54 | V · Which format  ·  two scripts disagree | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B55 | A memory bar split into segments: 'activations', 'master weights', 'optimizer state' | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B56 | V · Last resort  ·  gradient checkpointing, as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B57 | V · Watching memory  ·  as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B60 | A utilization scale for one GPU 0 to 100 with a mark at 60 ('fix first') and at 80 ('more cards pay') | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B61 | Four GPU blocks in a row, each holding an identical small model block; four different batch cards A, B, C, D d | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B62 | VI · Is the code written for it?  ·  as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B63 | VI · The DDP rules  ·  as written, excerpts | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B64 | VI · The request  ·  ddp_multigpu.slurm, as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B65 | VI · A template trap  ·  both slurm templates, as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B66 | A drawn fraction: numerator block 'throughput on N cards', a bar; denominator 'N x one-card throughput' (N sma | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B70 | Seven numbered-free stations arranged on a ring, each a small drawn object with a 1-2 word label: 'baseline' ( | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B71 | A drawn decision tree: root 'utilization' splits into '< 50' -> box 'data pipeline first' (a mono chip 'num_wo | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B72 | VII · After the job  ·  from the source, not run by us | terminal (CCPlainShell), not run by us | Manim code card | the evidence IS text; a terminal shows it as written |
| B73 | Three small drawn line plots on a time axis, side by side, labelled 'flat and high' (healthy, check), 'bouncin | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B74 | A clipboard page with eight unnumbered rows, each a short label and an empty box that gets a check on its spok | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B80 | Four rows, each with a logo chip or mono chip and a short tag: pytorch + tensorflow logo chips -> 'every act'; | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B81 | VIII · Hugging Face  ·  as written | terminal (CCPlainShell), source text | Manim code card | the evidence IS text; a terminal shows it as written |
| B82 | Two columns with a divider: 'Explorer' (rack) and 'AICR' (bigger grid rack) | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B83 | Two columns of stamped items | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |
| B84 | Three chips land in a row under a small rack: a mail chip with the address 'rchelp@northeastern | Manim drawing | ShowTellCard / isometric | motion lands on the spoken words; a flat chart, scale or 2x2 reads best here |

## Tool beats (SHOW-THE-THING)

Tools named: nvidia-smi, nvitop, PyTorch, Nsight, Hugging Face, NVIDIA: logos shown by `logo_chip` (LOGO LAW). The commands themselves are shown in the plain terminal skin, as text, with no output unless recorded (B12, B13, B17). `gpu-logs`, `nvidia-smi` and the profilers were not run by us and the film says so (B21, B34, B45, B72, B83). No Aider-style missing logos here.
