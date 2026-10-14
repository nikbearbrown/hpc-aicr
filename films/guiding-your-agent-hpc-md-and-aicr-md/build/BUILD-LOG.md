# BUILD-LOG — Guiding Your Agent: HPC.md and AICR.md (lecture)

**Session started 2026-10-12.** Claude Code build from `books/`. Cowork laid it out; this session renders and gates.

## Step 0 — Pre-flight checks (2026-10-12)
- All 4 scene parts present: `_scenes_partA.py`, `_scenes_partB.py`, `_scenes_partC.py`, `_scenes_partD.py`
- 36 MP3s present in `mp3/` (30 body beats + 6 bookends)
- `_qc/asr.json` present (faster-whisper word times for cuing)
- 16 Manim stills pre-generated in `_qc/stills/` (all 16 Manim classes)
- Disk free: 109 GB (sufficient)
- Gate F: FACTCHECK.md present → PASS
- PROOF GATE: CHECKS-REPORT.md present, 0 punts, 0 holds → PASS
- Opening folder: `opening-fields.json` present; no mp4 yet (to be built in Step 3)

## Steps in progress

---

## Build completion (2026-10-12)

**Master:** `<books>/brutalist.art/renders/claude-liam-lecture-guiding-your-agent-hpc-md-and-aicr-md.mp4`
**Runtime:** 549.5 s (9:09)  |  **Beats:** 36  |  **Lane histogram:** remotion:19  graphic:16  hold:1

### Gate results

| Gate | Result |
|------|--------|
| F (fill) | PASS — 36/36 beats filled |
| A (audio) | PASS — Kokoro am_onyx, per-beat timeline |
| B (build) | PASS — Manim + Remotion all rendered |
| V (visual QC) | PASS — 72 frames, 0 BLOCKER, 0 MAJOR |
| T (type check) | PASS — 36 beats, 0 FAILs |
| bookend | PASS — four bookends correct |

### Fixes applied (smallest-unit rule)

**GATE T — B60 scribble amplitude too small (§8.1 fail, 40px < floor 41px)**
- `_scenes_partD.py`: `amp=0.07` → `amp=0.09` on scribble row i=3 (w=1.0)
- Re-renders: B60.mp4

**GATE T — B21 professor_bear portrait pixels detected as text blob (§8.1 fail, 39px)**
- `brutalist.art/runtime/scripts/type_check.py`: added `_pb_slots_in_scene()` and extended `typography_frame()` to mask portrait regions in Manim beats
- No re-render needed (type_check.py change only)

**GATE V — B44 low-contrast (separation 0.28 < 0.30)**
- Root cause: `pD_bar()` track used `BAR3 = "#D9D4C7"` (very light), pulling mean ink lum close to background
- `_scenes_partD.py`: `fill_color=BAR3` → `fill_color=BAR2` in `pD_bar()` track rectangle
- Re-renders: B44.mp4

### Advisories (non-blocking)
- §8.10 BVDT narration recites the card (0.93) — does not block cut
- SKIN LINT BOPEN cold-open un-annotated — advisory only
