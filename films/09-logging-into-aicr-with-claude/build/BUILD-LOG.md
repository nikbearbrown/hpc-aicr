# BUILD-LOG — Logging into AICR with Claude (lecture)

**What this is.** The decisions, traps and gate results for the film built from `../source/README.md` with real evidence from `SESSION.md`. **Result.** Master built, all machine gates PASS, 2026-10-11. Not staged, not published.

## Decisions
- **Video number 9 of 13.** The eight published films carry `series_video_number` 1 to 8 in their make_sheet.py files (AICR Introduction 1, Optimizing GPU Usage on AICR 2, Intro to Explorer and OOD 3, Intro to GPUs on Explorer 4, Intro to Parallel Computing 5, Intro to Linux 6, Scientific Reproducibility 7, Installing Software 8), and the playlist note says 8 of 13 planned. The next free number is 9. `claude-liam-lecture-managing-projects` carries no number (built 2026-10-02, not in the playlist), so 9 does not collide with a numbered film; if Bear wants this film earlier in the series, the number is `series_video_number` in make_sheet.py plus a re-voiced BOPEN is not needed (the number is on the card only).
- Series fields as the siblings: `series_title` "Research Computing on Explorer and AICR", `series_video_count` 13, `series_entry_video` "Video 1 · AICR Introduction" (exact, from the entry film's sheet), `playlist` "Northeastern HPC and AICR", `chapter_number` 8. No course credit.
- Order change: the problem and fix of section 4 are told before section 3's config block (ACTS.md).
- Prompt on the Your Turn card is README step 6 verbatim; the spoken version says the sinfo output format and "s queue for my own user" aloud (FACTCHECK row 42).
- No `ssh` was run by the build. No key, certificate or passphrase file was read or printed. The three runs in SESSION.md are the only evidence.
- Claude Code surface: none drawn. The Bash tool-call row cannot hold the 90-column command at readable size; terminal beats use `CCPlainShell` ("Terminal · the command Claude Code ran") with the real text. The approval habit (B40) is a conceptual drawing.
- Two display changes of real output, both marked on screen: B32 shows the long command on two lines with `\`; B33 shows the recorder's `(squeue: header only, no jobs)` as a comment line.

## Built for this film (library changes, all backwards compatible)
- `CCPlainShell` (`brutalist.art/runtime/remotion/src/scenes/CCPlainShell.tsx`): optional `lineCues` (a frame per line; <= 0 = already on screen), `rings` (terracotta ring round chosen lines after their cue), `windowMargin`; `fontSize` minimum lowered 28 to 24 (long real lines).
- `ClaudeCodeBeat`: optional `lineCues`. (Not used in the end: GATE T 8.12 reads shell or config lines without code tokens as prose-in-code, and the "no file extension" title rule rejects `~/.ssh/config`; the five command and config beats moved to `CCPlainShell`.)
- Cast helpers in `_kit_cast.py`: key, padlock, certificate page, agent slab, vault, chip, plaque. `scenes.py` = `_kit_header.py` + measured word times (`_ASR`) + cast + parts A to D, assembled by `assemble_scenes.py`.
- No `scene-index` run was needed: no new composition was registered.

## Traps met (all fixed)
- Layout audit (Gate B) reads a strike-through X over a label as "label on a curve": X marks sit beside chips.
- Gate V: underfill on text-and-table beats (B11, B13, B14, B41, B53, B54) is waived with `sparse_by_design`; the B53 and B54 row marker is a thick ink bar (an outline round the row fused the row into one GATE T blob, a fill dragged Gate V contrast under 0.3).
- GATE T §8.3b: some Professor Bear portraits contain dark facial blobs that read as unreadable text near a label; B21, B38, B43, B46 got other seeds (B21x, B38y, B43q, B46y). Logged here because the seed rule is "slug-seeded".
- GATE T/Gate V sample the midpoint: terminal lines never start landing within 21 frames before or 7 frames after it (`clear_midpoint` in make_sheet.py). The ASR writes "user name" as "username", "principals" as "principles" and "600" as digits, so cue phrases carry `a|b` alternatives; a cue that is not found prints `[cue-fallback]`.
- Spoken order must match on-screen order: B16 was re-voiced so Valid is said before Principals (the output prints them in that order).
- B27 midpoint was an empty terminal (Gate V low contrast): the command now lands at "Type it there" and the key line at 4.9 s.
- `art final` runs Gate V again on the candidate master and prints only the command on failure; read `_qc/REPORT.md`.

## Gate results
- Gate F/L/A/W: clean. Gate B (layout audit): clean on all 23 Manim scenes. Gate V: 88 frames, 0 BLOCKER, 0 MAJOR. GATE T: PASS (`TYPECHECK.md`; BVDT 0.94 advisory only, same stock card as the siblings). bookend_check: PASS. `MASTERCHECK.md`: PASS.
- Master: `exports/landscape/claude-liam-lecture-logging-into-aicr-with-claude.mp4`, 3840x2160 h264/aac 24 fps, 518.875 s (sum of measured audio 518.05 s; the 0.8 s difference is per-beat frame rounding at 24 fps). Silent tail 1.63 s (BOUT pad 1.0 s plus rounding).
- Lane histogram (body, information only): drawing 15, Manim diagram/table/text transform 8, real capture 1, real terminal 9, real command or config listing 5 (rendered on CCPlainShell), card 0. Beats: 44 (38 body, 6 bookends).

## Not done
- No audible listening pass (ASR only). No staging, no publishing, no YouTube description upload; the draft is `claude-liam-lecture-logging-into-aicr-with-claude-youtube.md` (chapter times are within a second of the master).
