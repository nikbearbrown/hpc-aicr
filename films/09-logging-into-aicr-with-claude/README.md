# Logging into AICR with Claude

**What this is.** Video 9 of the series *Research Computing on Explorer and AICR*. **Status:** published.

**Watch the film:** https://youtu.be/QZibDBeMgec (unlisted).

## Where it comes from

Written for this repository, from Northeastern Research Computing's public documentation and from real, read-only sessions on the clusters. Every claim in it says what it rests on.

## What is in this folder

- `source/`: the material the film teaches from (ours: real session records and guides written for this repository).
- `build/`: how the film was made. `beat_sheet.json` is the heart (one entry per shot: narration, picture, timing). `make_sheet.py` regenerates it; `scenes.py` holds the Manim animations; `ACTS.md`, `SHOTLIST.md`, `FACTCHECK.md` and the other `.md` files are the plan and the record. Rendered video, audio and large images are not included (they are rebuilt, see below).

## Redo it

The films are built with the [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit (Manim and Remotion scenes, free Kokoro narration). Put `build/` where the toolkit expects a film folder, regenerate the audio and run its review and final steps. The narration was voiced with Liam, an AI voice (Kokoro `am_onyx`), speaking in for the author.

