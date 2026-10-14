# BUILD-LOG — Logging into Explorer (HPC) with Claude

**What this is.** The Claude Code build of the lecture film laid out by Cowork. **Result.** Master built 2026-10-13, 330.0 s, 23 beats; Gates A, B, W, V, T and bookend PASS. Not staged, not published.
**Master:** <books>/brutalist.art/renders/claude-liam-lecture-logging-into-explorer-with-claude.mp4

## Changes made during the build
- **Retitled at Bear's request (2026-10-13):** "Logging into Explorer (HPC) with Claude". TITLE, the card title lines, and the BOPEN and BOUT narration (re-voiced with Kokoro am_onyx; Liam says "Explorer, H P C"; the speech check heard it right). The folder slug is unchanged.
- **GATE V edge-bleed, 20 frames:** terminal beats B21, B22, B31, B32, B33, B40, B41, B43 rendered the window at `windowMargin` 50, which crosses the title-safe edge; set to 100 in make_sheet.py. Manim beats B20 and B30: the Professor Bear portrait crossed the left safe edge; size 2.6 to 2.3 and x -5.2 to -5.05 in _scenes_partB.py.

## Not verified
- Nobody has listened to the voice. The recogniser wrote "ED25 -519" for the key type, so "ssh keygen" and "E D twenty-five five-nineteen" need an ear check; liam.json was not touched.
