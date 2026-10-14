# Running a Local LLM on Explorer

**What this is.** A film in the series *Research Computing on Explorer and AICR* (about 14 minutes) on running an open model on an Explorer GPU and pointing a coding agent such as Claude Code at it. **Status:** film built; not yet published.

**Watch the film:** not published yet.

**Want instructions you can paste to get started?** Go to [`skills/local-llm-on-explorer/GET-STARTED.md`](../../skills/local-llm-on-explorer/GET-STARTED.md): one file you hand to Claude Code, which guides you step by step and asks before every file it writes and every job it submits.

## Where it comes from

Written for this repository from a tutorial of ours, checked against Ollama, Claude Code and Northeastern Research Computing documentation, and from read-only sessions on the cluster. The film says plainly that the setup was documented, not run end to end. Every claim in it says what it rests on (`build/FACTCHECK.md`).

## What is in this folder

- `source/`: the tutorial the film teaches from. Every script line shown on screen is read from it.
- `build/`: how the film was made. `beat_sheet.json` is the heart (one entry per shot: narration, picture, timing). `make_sheet.py` regenerates it; `scenes.py` holds the Manim animations; `ACTS.md`, `SHOTLIST.md`, `FACTCHECK.md` and the other `.md` files are the plan and the record; `_research/` holds the three verification passes against primary documentation. Rendered video, audio and large images are not included (they are rebuilt, see below).

## Redo it

The films are built with the [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit (Manim and Remotion scenes, free Kokoro narration). Put `build/` where the toolkit expects a film folder, regenerate the audio and run its review and final steps. The narration was voiced with Liam, an AI voice (Kokoro `am_onyx`), speaking in for the author.
