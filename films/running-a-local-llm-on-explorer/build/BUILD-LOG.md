# BUILD-LOG: Running a Local LLM on Explorer

**What this is.** The Claude Code build of the lecture film from the pasted tutorial, 2026-10-13. **Result.** Master built: 3840x2160, 867.3 s (14:27), 57 beats (33 Manim, 18 terminal on `CCPlainShell`, 6 bookends), no slates. Gates F, A, B, W, V, T and the bookend check PASS. Not staged, not published. **Not verified.** Nobody has listened to the voice; the tutorial's setup was documented, not run end to end (the film says so in B95).

**Master:** <books>/brutalist.art/renders/claude-liam-lecture-running-a-local-llm-on-explorer.mp4

## How it was built
Whole tutorial read; three verification agents checked it against primary documentation (`_research/check-*.md`); sheet, narration (Kokoro `am_onyx`, measured), scenes by six parallel authors (parts A to F), paperwork (STORY, ACTS, SHOTLIST, FACTCHECK, CHECKS-REPORT, SOURCES, PROMPTS), then review cut and final.

## Act XI added (2026-10-13, at Bear's request)
Two beats after Act X: B110 (where to go: the hpc-aicr repository, skills/local-llm-on-explorer/GET-STARTED.md) and B111 (clone, start Claude Code, paste the prompt; three real commands read from the guide). Part G scene file; B110 shows dashed placeholder slots from the start so Gate V underfill passes at the midpoint. The guide itself was not run end to end; the film says so. The description needs the repository link, and the path must be live on GitHub before publishing.

## Changes forced by the checks (smallest unit each)
- **Wording from the fact-check:** B22 (bare host is the documented example, `/v1` doubles the path), B24 (small model for background tasks, a separate setting for subagents), B26 (a 1.5B model "cannot reliably drive" an agent loop, not "fails at tool calling"), B41/B42 (GLM-4.7-flash 19 GB download, about 23 GB of video memory at 64k), B53 (new: Anthropic does not support Claude Code against non-Claude models; hosted web search not fully supported), B81/B82 (new: the proxy module and Research Computing's own advice to unset the proxy variables), B92 (vLLM keys not to be relied on alone), B94 (develop and test on Explorer first).
- **Pronunciation (never heard):** `runtime/pronunciation/liam.json` gained Ollama to "Ohlama", Apptainer to "Aptayner", Qwen to "Kwen" (phonemes verified with `pronunciation.py --check`). The audio generator caches by text, so affected mp3s were moved to `_superseded/audio-before-pronunciation/` and regenerated.
- **assemble_scenes.py** defaulted to parts A to D; changed to A to F (the first review cut slated B80 onward).
- **Gate V underfill:** B95 and B101 got dashed placeholder slots so the layout is visible at the midpoint (B80 passed once its scene was included).
- **Gate T (10 beats):** nested ink outlines made grey or kraft (B11 bands and container, B23 laptop screen, B41 axis); terracotta ring pulses made transient so none is alive at the midpoint (B42, B43, B80 rows 1 to 3; B80 row 2's pulse timed after the midpoint); B90's job box drawn without terracotta tape; B54 stopwatch hub and hand enlarged (a horizontal hand read as a 36 px text run); B92 page scribbles amplitude 0.07 to 0.09; B82 title without an apostrophe; BIDEA's typed text ends "always running" (a trailing "on" read as a truncated string) and its narration was re-voiced.

## Open for Bear
1. Listen to the voice, especially Ollama, Apptainer, Qwen ("Kwen"; the maker says closer to "chwen") and the three-letter-heavy lines.
2. No logo exists for Aider or Droid (mono chips used).
3. `HPC.md` Section 10 calls the tutorial "Research Computing's local-LLM tutorial"; it is not RC's. Not edited.
4. Staging and publishing wait for Bear; internal playlist position is `chapter_number` 11 in Northeastern HPC and AICR.
