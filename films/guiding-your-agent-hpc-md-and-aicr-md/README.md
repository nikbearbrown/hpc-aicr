# Guiding Your Agent: HPC.md and AICR.md

**What this is.** A film in the series *Research Computing on Explorer and AICR* (about 9 minutes) on why an agent on a shared cluster needs written rules, and a walk through the two rule files in this repository: [`HPC.md`](../../skills/hpc/HPC.md) and [`AICR.md`](../../skills/aicr/AICR.md). **Status:** published.

**Watch the film:** https://youtu.be/1OasVYsVVJw (unlisted).

## Where it comes from

The two rule files themselves: every file excerpt shown on screen is read from them when the film is built. The three real mistakes in the film come from a recorded working session on Explorer.

## What is in this folder

- `build/`: how the film was made. `beat_sheet.json` is the heart; `make_sheet.py` regenerates it; `scenes.py` holds the Manim animations; the `.md` files are the plan and the record. Rendered video, audio and large images are not included (they are rebuilt, see below).

## Redo it

The films are built with the [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit (Manim and Remotion scenes, free Kokoro narration). Put `build/` where the toolkit expects a film folder, regenerate the audio and run its review and final steps. The narration was voiced with Liam, an AI voice (Kokoro `am_onyx`), speaking in for the author.
