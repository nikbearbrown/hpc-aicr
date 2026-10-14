# BUILD-LOG: Scientific Reproducibility II: Version Control

**What this is.** Rough cut with audio, 2026-10-13. **Result.** 1920x1080 review cut, 732.1 s (12:12), 52 beats: 20 Manim, 26 terminal (`CCPlainShell`), 6 bookends; no slates. Not staged, not published, `art final` not run. **Not verified.** Nobody has listened to the voice; GATE T (TYPECHECK), the 4K master and the bookend check were not run (they belong to `art final`).

Rough cut: <books>/brutalist.art/renders/rough/claude-liam-lecture-scientific-reproducibility-ii-version-control-rough.mp4 (same file as the reel's `-slate.mp4`; the review compiler names it that).

**Gates.** L, SHAPE, A, W, B (layout audit): pass. V: one remaining MAJOR, run with `ART_STRICT=0`: B44 midpoint frame `low-contrast` (ink/background separation 0.27 < 0.3; the ghost placeholder pills for the six message types). Earlier rounds fixed: B44 X mark on text, B75 log chip on the timeline (Gate B); underfill and low contrast on B15, B20, B77, B78, B85 (Gate V).

**New evidence.** The source's Git steps were run for real on a Mac in a throwaway folder (`captures/EVIDENCE.md`). New findings not in the written guide: the comment-after-pattern bug in the source's `.gitignore`; `*.log` above `!results/run.log` is NOT a problem once the folder is `results/*` (later `!` lines win); Mac Git names the first branch `master`; `wc -l` pads counts on a Mac.

**Traps met.** `make_sheet.py` `rl()` needs exact line prefixes from the recorded files. Title card needs three balanced lines of at most 28 characters ("Scientific" / "Reproducibility II:" / "Version Control"). X marks drawn over text trip Gate B. Detach a long `art run` (python Popen with start_new_session) or the tool kills it.

## 4K master, 2026-10-14
Deleted all 1080p clips and re-rendered everything at 2160 (BOPEN kept, already 3840 wide; make_sheet + assemble_scenes re-run, parts A-D). Master: exports/landscape/claude-liam-lecture-scientific-reproducibility-ii-version-control.mp4, 3840x2160, 732.1 s (beats sum 731.2 s). Gates: L, SHAPE, A, W, B pass; V pass (0 BLOCKER, 0 MAJOR, no ART_STRICT=0); T PASS; bookend_check PASS.
Changes forced by the checks:
- Gate V B44 low-contrast: the grey ghost pills/plaque (near the background luminance) replaced by dashed ink outlines (_scenes_partB.py).
- Gate T no-wordy-card (>12 words): shortened the terminal window titles of B61, B63, B74, B80, B81 in make_sheet.py (e.g. "tag the submission  ·  recorded on a Mac, push not run"); narration untouched. The "from the source, not run" caveat now lives in narration/comment lines only for B80/B81/B63.
- Nothing outside this reel changed. Art-final SKIN LINT notes BOPEN is not a ClaudeComposerAsk cold open (expected: lecture title card).
