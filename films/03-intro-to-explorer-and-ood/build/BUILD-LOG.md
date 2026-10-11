# BUILD-LOG — Intro to Explorer and OOD (lecture)

**What this is.** Decisions and gate results for film 3 of the hpc lecture series. **Source.** `hpc/Intro-to-Explorer-OOD-2026/Intro_explorer_ood.md`. **Channel.** claude-liam (@NikBearBrown), Liam in for Bear.

## 2026-10-06

- Bear: go through the hpc folder film by film with the lecture skill; he watches each, then it publishes.
- Plan: nine acts, 29 body beats, about 9 min. The training's own screenshots are the captures (SHOW-THE-THING rung 1); no Explorer session was run (no account access from this build).
- Kokoro: "c a t", "s c p", "l e s s", "s e f f" came out garbled; narration now says cat, S C P, less, seff. Six beats re-voiced.
- Manim scenes in two parallel parts (A, B) on the series kit.

## 2026-10-06 — master cut

- Gate V: two progressive-drawing underfills (B62, B63) → drawn-lane waiver; then clean on 66 frames.
- GATE T rounds: (1) the training's screenshots carried the browser's own tab/address strip, whose grey-on-black text failed local contrast → every capture cropped to the page (`CROP` in make_sheet.py, originals in `captures/orig/`); rings that touched type merged into the text blob → rings padded and drawn in ink (`ringColor`); the red Cancel buttons on the jobs page read as accent text → those two beats frame to the left of them. (2) §8.9 read the hesitant-writer line ending "…run my code on" as truncated → reworded. GATE T PASS.
- Master: `exports/landscape/claude-liam-lecture-intro-to-explorer-ood.mp4`, 3840×2160, 551.9 s (9:12), 33 beats, bookend PASS. Not staged, not published. Waiting for Bear's verdict.

## 2026-10-07 — BOPEN opening card (lecture skill update)
- Prepended the 3 s series title card (template `lecture-title-slide-16x9`, video 3 of 13 in "Research Computing on Explorer and AICR", random square Professor Bear portrait seeded by the slug; portrait recorded in `opening/opening-fields.json`). Silent clock `mp3/BOPEN.wav`, `audio_policy: silence`.
- Recut: Gate V clean, GATE T PASS, bookend PASS. Master in `exports/landscape/` is 3 s longer than before. Not staged, not published.

## 2026-10-09 — BOPEN now narrated (lecture skill 2026-10-08 contract)
- The silent 3 s card is superseded: Liam speaks playlist → exact title → one-sentence summary over the card (`narration_contract: playlist-title-summary-v1`), card held 12.42 s to the measured audio; `audio_policy: silence` and the WAV clock removed. Recut: Gate V clean, GATE T PASS, bookend PASS. Not staged, not published.
