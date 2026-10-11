# BUILD-LOG — Optimizing GPU Usage on AICR (lecture)

**What this is.** Decisions and gate results for film 2 of the AICR lecture series. **Source.** `hpc/AICR-Optimizing-GPU-Usage/aicr-gpu-optimization.md`. **Channel.** claude-liam (@NikBearBrown), Liam in for Bear.

## 2026-10-06

- Bear (after film 1 was published): "Just keep on going. Go through the entire folder one by one, film by film … keep using the lecture skill … After making it, I'll watch it. If okay, then you publish it."
- Plan: eight acts, 38 body beats; measured audio 14 min 29 s. Lane histogram in CHECKS-REPORT.md.
- Real evidence: `jobstats 318592`, Bear's own 55-minute fine-tuning job on rtx-batch (read-only). It happens to be the textbook "high utilization, low memory" case (80% / 17%) and carries a real "request less time" note; B72 is built on it.
- Left out, following the source's own HTML comments: storage section 4.2 and the `$TMPDIR` advice. Stripped: the unsourced 2.5× cost claim, the Workshop 1/3 cross-references.
- B200 VRAM: the workshop says 192 GB (and its nvidia-smi sample shows 196608 MiB); the AICR hardware docs page says 180 GB. The film follows the workshop it is teaching; FACTCHECK row 4 records the discrepancy for Bear.
- Reuse: film 1's `_kit.py` (cast) copied unchanged; B16 reuses film 1's idle-cancel scene; B11 reuses its table builder. The workshop's demo scripts were not run (GPU allocation needed; job submission is outside this build's permissions).
- Manim scenes authored in four parallel parts (A–D) on the shared kit, assembled into `scenes.py`.

## 2026-10-06 — master cut

- First 4K run: Gate V flagged 13 underfill frames, all on drawn beats that build progressively (32–54% at the sampled midpoint). Declared the isometric lane's sparse waiver on those eleven beats (`PROGRESSIVE` in make_sheet.py: underfill and clustered only). Gate V then clean, 94 frames.
- GATE T round 1: B20 terracotta rings on the dark terminal read as accent text (§8.3) → rings recoloured pale (CARD); B50 and B60 the ink gauge needle inside the arc's bbox read as an overlapping text run (§8.6b) → needles grey (BAR1), B60's 60%/80% labels moved outside the gauge bbox. Round 2: §8.12 prose-in-code on B12/B12B (an #SBATCH header is all comments to the checker) → both shown in a plain terminal via `cat`, as film 1 does. Round 3: GATE T PASS.
- Also: ClaudeCodeBeat holds ~11 lines at the readable size, so the four long listings were split into two beats each (B12/B12B, B32/B32B, B41/B41B, B62/B62B); Kokoro's "nvidia-smi" and "Nsight" were respelled in narration only.
- Master: `exports/landscape/claude-liam-lecture-aicr-optimizing-gpu-usage.mp4`, 3840×2160, 893.2 s (14:53), 47 beats, bookend PASS. Not staged, not published. Waiting for Bear's verdict.

## 2026-10-07 — BOPEN opening card (lecture skill update)
- Prepended the 3 s series title card (template `lecture-title-slide-16x9`, video 2 of 13 in "Research Computing on Explorer and AICR", random square Professor Bear portrait seeded by the slug; portrait recorded in `opening/opening-fields.json`). Silent clock `mp3/BOPEN.wav`, `audio_policy: silence`.
- Recut: Gate V clean, GATE T PASS, bookend PASS. Master in `exports/landscape/` is 3 s longer than before. Not staged, not published.

## 2026-10-09 — BOPEN now narrated (lecture skill 2026-10-08 contract)
- The silent 3 s card is superseded: Liam speaks playlist → exact title → one-sentence summary over the card (`narration_contract: playlist-title-summary-v1`), card held 13.01 s to the measured audio; `audio_policy: silence` and the WAV clock removed. Recut: Gate V clean, GATE T PASS, bookend PASS. Not staged, not published.
