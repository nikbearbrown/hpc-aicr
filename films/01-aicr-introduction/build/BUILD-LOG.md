# BUILD-LOG — AICR Introduction (lecture)

**What this is.** The decisions and gate results for the first film made with the `lecture` skill. **Source.** `hpc/AICR-Introduction-2026/aicr-introduction.md`. **Channel.** claude-liam (@NikBearBrown), Liam in for Bear, Kokoro `am_onyx`.

## 2026-10-02

- Bear: "let's try a lecture, Liam persona, on the first folder there, AICR introduction; remove the dates, it should just say AICR introduction rather than AICR introduction 2026 … the AICR folder already has a bunch of films made, which you should use for these as well."
  - Title is "AICR Introduction", slug `claude-liam-lecture-aicr-introduction`. The source folder `hpc/AICR-Introduction-2026/` is a clone of the public repo and was NOT renamed (my reading: the date comes off the film, not off the upstream repo folder).
  - The eleven `aicr/youtube/aicr-*` films were used for their fact-checks against the AICR docs and for the cast ideas (storage ladder, partition table). Their bodies are mostly text cards, so no clip was re-used; this film redraws those ideas as pictures.
- Plan: six acts, 24 body beats, estimated 6 min 20 s. Lane histogram: isometric 10, Manim chart/diagram 6, real capture 2, real terminal 3, real code 2, icon row 1.
- Audio: 29 beats, 379 s measured. BOUT padded with a 1.0 s tail.
- Kokoro says "AICR" as "acre" (as in the earlier films). Kept; flagged in FACTCHECK.
- SHOW-THE-THING: real `sinfo` output from login.aicr.ai (read-only); real captures of the sign-in page and the Globus docs page. Submitting a test job to show real `sbatch`/`squeue` output was blocked by the session's safety rules, so B53/B54 show commands only.
- Not captured (sign-in walls): the proposal Google Form (B20) and the Open OnDemand app launcher (B55). Both beats are drawings that assert only what the source says. Upgrade available if Bear captures them signed in.
- MISS → built: no browser-capture scene and no large-icon scene in the library. Built `BrowserCapture` and `LibraryIconRow`, registered, re-indexed. `CCPlainShell` gained optional `durationSeconds`.
- Manim scenes authored in three parallel parts (`_scenes_partA/B/C.py`) on one shared kit (`_kit.py`), assembled into `scenes.py`.

## 2026-10-06 — master cut

- `art run --height 2160`: Gate L clean, Gate A 16/16 clean, Gate W 16/16 clean, layout audit clean, Gate V 58 frames 0 BLOCKER 0 MAJOR (after one fix: the icon row's empty tiles now sit on stage from frame one, so its midpoint frame fills).
- `art final`: GATE T PASS (29 beats, 0 FAILs). Master: `exports/landscape/claude-liam-lecture-aicr-introduction.mp4`, 3840×2160 H.264/AAC, 380.4 s, sha256 5ec7309105915b19…, `.verified.json` beside it.
- `bookend_check.py`: PASS (lecture cold open accepted).
- Known soft spots, not gate failures: the belt in B13 (Part A, dashed outline) and the belt in B55/B62 (Part C, solid kraft) are drawn differently; the recap card (`ClaudeVerdictArtifact`) is the stock size. B50's title reads "Three Ways to Work on AICR".
- Not staged, not published. Waiting for Bear's verdict.

## 2026-10-07 — BOPEN opening card (lecture skill update) + GATE T catch-up
- Prepended the 3 s series title card (video 1 of 13 in "Research Computing on Explorer and AICR"; "Start here · AICR Introduction"; portrait in `opening/opening-fields.json`). Silent clock `mp3/BOPEN.wav`, `audio_policy: silence`.
- GATE T §8.12 (added after this film was published) read the two `myjob.slurm` ClaudeCodeBeats as prose-in-code → shown as `$ head -11 myjob.slurm` / `$ tail -6 myjob.slurm` shell cards instead.
- Recut 383.4 s: Gate V clean, GATE T PASS, bookend PASS. The PUBLISHED version (youtu.be/h2248fkcuyU, 2026-10-06) has no card; replacing it on YouTube means a new upload, which is Bear's call.

## 2026-10-09 — BOPEN now narrated (lecture skill 2026-10-08 contract)
- The silent 3 s card is superseded: Liam speaks playlist → exact title → one-sentence summary over the card (`narration_contract: playlist-title-summary-v1`), card held 12.67 s to the measured audio; `audio_policy: silence` and the WAV clock removed. Recut: Gate V clean, GATE T PASS, bookend PASS. Not staged, not published.
