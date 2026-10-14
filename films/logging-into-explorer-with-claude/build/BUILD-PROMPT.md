# BUILD-PROMPT — Logging into Explorer with Claude (lecture)

**What this is.** The handoff for the lower-effort build session (Claude Code, launched from `books/`). A Cowork session did the thinking: the story, the acts, the narration, the sheet (every terminal line read from the real Explorer session record at build time), the measured Kokoro audio, the fact-check, and the Manim scenes (parts A to C). What is left is mechanical: assemble, build the title card, look at stills, review cut, final master, gates.
**Why.** Bear's two-stage rule (2026-10-11): Cowork lays the film out; Claude Code renders and builds.
**Found.** Everything on screen traces to a real run. The paperwork is written (ACTS, SHOTLIST, FACTCHECK, CHECKS-REPORT, SOURCES, PROMPTS). Audio is generated and measured: 23 beats, about 328 s.
**Not verified.** No scene has been rendered at 4K yet; no gate (A, B, V, T, bookend) has run on the assembled film; nobody has listened to the voice.

Run everything from `<books>`. R = `<books>/hpc-aicr/youtube/claude-liam-lecture-logging-into-explorer-with-claude`.

## Read first
1. `<books>/brutalist.art/skills/make/lecture/SKILL.md` (governing skill; **videos are never numbered**, the card and the sheet carry no number or "start here").
2. `<books>/CLAUDE.md` (TOPOST-only publishing, GATE T, absolute paths).
3. `R/STORY.md`, `R/ACTS.md`, `R/SOURCES.md` (every edit to real text), `R/BUILD-LOG.md` if it exists. The real record the film is made from: `<books>/hpc-aicr/Logging-into-Explorer-with-Claude/SESSION.md`. Also `<books>/brutalist.art/CLAUDE.md` rule 11 (LOGO LAW: Claude is the logo, `logo_chip`).
4. The sibling film's `BUILD-PROMPT.md` and `BUILD-LOG.md` for the same pipeline already run end to end: `<books>/hpc-aicr/youtube/claude-liam-lecture-logging-into-aicr-with-claude/`.

## The commands, in order

```bash
R=hpc-aicr/youtube/claude-liam-lecture-logging-into-explorer-with-claude
# 0. all three scene parts exist?
ls $R/_scenes_part{A,B,C}.py
# 1. the sheet (keeps the measured audio); NEVER re-run it after `art final` (it wipes the build stamps)
python3 $R/make_sheet.py
# 2. scenes.py = _kit_header.py + measured word times + _kit_cast.py + parts A to C, then the midpoint guard
python3 $R/assemble_scenes.py
# 3. the title card (BOPEN): needs BOPEN's measured audio, which exists
python3 brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $PWD/$R/opening --sheet $PWD/$R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*s.mp4 $R/media/BOPEN.mp4      # use the file the builder printed
# 4. stills FIRST: python3 $R/qstill.py --scenes scenes.py <Class> ... for every Manim class; contact sheet; LOOK at them
# 5. review cut, then the clean master
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

## Gates that must PASS (fix the smallest unit, re-run only that, log it in BUILD-LOG.md)
Gate F (FACTCHECK.md present), PROOF GATE (CHECKS-REPORT.md), Gate A (static scene check), Gate B (layout audit), Gate V (frame check), GATE T (type), bookend_check. Look at frames and `qc-sheet.png`; do not trust the mp4 probe alone.

## Traps already met on this machine and in the cluster pilot
- **Never edit the beat sheet while a compiler runs.** `make_sheet.py` rewrites it and clears build stamps.
- Terminal beats were cued on word times in `R/_qc/asr.json` (faster-whisper). If you re-voice a beat (`generate_audio_kokoro.py $R --only <BID>`), run `python3 $R/pad_audio.py`, `python3 $R/whisper_check.py <BID>`, then `make_sheet.py`, `assemble_scenes.py` again.
- Heard in the voice check: "ssh keygen" and "E D twenty-five five-nineteen" should be checked by ear (the recogniser wrote "ED25 -519"). Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report both to Bear after he has listened.
- Terminal beats use `CCPlainShell`; every terminal line is read from the real session record by `sl()` in `make_sheet.py`; do not hand-edit lines.
- The Manim scenes use `professor_bear(...)` with literal seeds; the library lives only on this Mac (it is never shipped).
- Disk: check `df -h /` before the 4K render; stop and say so under about 15 GB free.

## Hard stops
- **Do NOT publish, stage (`art post`) or upload anything.** No paid generation. Free steps run straight through with no approval gate.
- Do not touch any cluster; this film needs no `ssh`.
- Do not change the narration, the scene design or the beat sheet. If a gate fails, fix the smallest unit and log it.

## Final report (to Bear, concise)
Absolute path of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), any slate, any mispronunciation, any gate that did not pass. Report every file by absolute path. Do not claim anything you did not verify by looking at frames.
