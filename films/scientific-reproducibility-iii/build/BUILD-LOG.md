# BUILD-LOG: Scientific Reproducibility III: Containers

**What this is.** Build log of the rough cut, 2026-10-13. **Result.** See the final report; this file records traps and decisions as they happen. Not staged, not published.

## Decisions
- Title kept exactly as assigned, "Scientific Reproducibility III: Containers". The "III" may read as a film number; Bear's law is no numbers on films. Bear to decide (card text and BOUT narration say "Three").
- Apptainer had no logo in the library; created `brutalist.art/icons/logos/apptainer/apptainer-01.svg|png` from the project's public SVG (mark only). No existing toolkit file edited.
- Terminal lines are read from the sources by `g()`, `o()`, `blk()`, `cmd()` in `make_sheet.py`; a missing line stops the build. Two long source commands are shown on two lines with a shell line-continuation (B36, B39).
- Narration respellings written into the narration text (no pronunciation-dictionary edit): "Key dot I O" for Quay.io, "Sigh-labs" for Sylabs, "G A T K", "S I F", "N V".
- The guide says every pull example names a version; `library://lolcow` does not. The film says so (B61); the guide could be corrected.

## Traps met
- BSD sed needs `-i ''`; a failed `sed -i` in a chained command silently skipped the qstill scratch-path edit once (fixed with python).
- Scratch directory `scratchpad/qs` is shared with other films; qstill.py points at `scratchpad/repro3/qs`.
- Layout audit flags a label touching a line: chips shrinking into an open box, a chip sitting on a pipe, a label inside a dashed slot. Fixed by moving the chip off the pipe, fading the slot before the folder arrives, ShrinkToCenter for the chips.

## Rough cut (2026-10-13)
Review cut 1920x1080, 616.8 s, 44 beats (19 Manim, 19 terminal `CCPlainShell`, 6 bookends), no slates. Gates L, A, W, V pass (Gate V: 0 blockers, 0 major after fixes). SKIN LINT note on BOPEN (lecture's portrait card is not a composer cold open: expected). Gate T and the master (`art final`) not run, by instruction. Copy: <books>/brutalist.art/renders/rough/claude-liam-lecture-scientific-reproducibility-iii-containers-rough.mp4
- Gate V fixes: B23 steps white (kraft fill gave low contrast) with labels visible from the start; B56 had mostly ghost comments (now two real commands).
- Terminal font: the window holds about 1720/(0.6*fs) characters; lines over that are cut with an ellipsis (not verbatim). Sizes set per beat: 24 for the 104-character APPTAINER_BIND line (B42), 26 for B36, 30 for B39, 31 for B63, 36 for B41, 38 otherwise.
- Incident: I ran `pkill -f` on "art run", "remotion_scenes" and "manim" to stop my own render; that pattern can also have killed other agents' renders running at the same time. Anyone whose build died in that minute (about 22:05) should re-run it.

## 4K master (2026-10-14)
- Deleted all 1080p clips (manim/, clips/, media/*.mp4 except BOPEN which was already 3840 wide, partial_movie_files) and the 1080 slate; re-ran make_sheet.py, assemble_scenes.py (parts ABC cover every _scenes part), `art run --height 2160`: Gates L, A, W, V pass (0 blockers, 0 major, no ART_STRICT=0).
- Gate T first run: 3 FAIL. Fixes (smallest unit each, narration and story untouched): B23 step labels moved below the boxes (a label inside a short box fused with its outline), taller steps, library rack lifted clear of the box; B70 terminal title shortened to "VII · Cache off home · from the source, not run" (13 words > 12); B72 chips 38/34, labels 40, "=" 110, and the notes scribbles drawn with amplitude 0.11 (the short last line read as a 40 px text run). Gate T PASS. Advisories left: B30 and BVDT narration recites the card.
- Master: exports/landscape/claude-liam-lecture-scientific-reproducibility-iii-containers.mp4, 3840x2160, 616.79 s (beats sum 615.99 s). bookend_check PASS. SKIN LINT note on BOPEN as before (expected). B42 terminal text is small (24 pt, the 104-char verbatim line) but passes Gate T.
- No pkill used. Nothing staged or published.
