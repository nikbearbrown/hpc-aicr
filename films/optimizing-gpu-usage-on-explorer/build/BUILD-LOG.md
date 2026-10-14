# BUILD-LOG: Optimizing GPU Usage on Explorer

**What this is.** The rough-cut build of this lecture film, 2026-10-13. **Result.** Review cut at 1080p, 903.8 s (15:04), 61 beats (26 terminal on `CCPlainShell`, 29 Manim, 6 bookends), all 61 slots filled, no slates. Gates L, A, B, W, V passed on the last strict run (`art run --height 1080`, no ART_STRICT override). Not staged, not published, no `art final`, so GATE T and the bookend check were not run. **Not verified.** Nobody has listened to the voice; nothing was run on a GPU node.

**Cut:** <books>/brutalist.art/renders/rough/claude-liam-lecture-optimizing-gpu-usage-on-explorer-rough.mp4

## Changes forced by the checks
- Pronunciation by respelling the narration text (no shared dictionary edit): "pre fetch" (Kokoro said "per-fetch"), "fif teen" (heard as fifty), "drop by half" (halve said as have), "narrow the search", "restart" (respawn), and B82 reworded so AICR starts a sentence.
- Gate A: stub widths made `stamp()` and `lab_l()` fail on B48 and B80; explicit widths and centred labels.
- Gate B: label-on-line errors in B22, B47, B48, B70, B71; out-of-safe-area in B11, B19, B55, B80; each fixed in the scene.
- Gate V: edge-bleed on terminal beats B43 and B65 (shorter lines, fs 24, margin 100); underfill on B15, B19, B23, B35, B44, B55 (dashed placeholder slots shown from the start, removed when the real item lands).
- Traps met: `art run` skips filled beats, so clips (`manim/`, `clips/`, `media/`) were removed before each re-render; a zsh `rm` with an unmatched glob aborts the whole command.

## 4K master, 2026-10-14
Clips deleted and re-rendered at 2160 (BOPEN kept, already 3840 wide). `art run --height 2160`: Gate V pass without ART_STRICT=0. GATE T first run failed on 8 beats; fixes (smallest unit each): B21/B31/B72 titles cut to 12 words or fewer ("not run by us", dropped "from the source"); B43/B46/B57/B64 terminal fontSize raised to 30 (sub-41 px text); B46 line cues moved earlier (one dim comment line was the only text at the clip midpoint); B83 left stamps got kraft outlines (ink outline merged with its label as one blob). Then GATE T PASS, `art final` to exports/landscape, bookend_check PASS. Master 3840x2160, 903.75 s (sum of beats 902.48 s). Narration unchanged. Not listened to; nothing run on a GPU node. Not staged or published.
