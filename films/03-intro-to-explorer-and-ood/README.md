# Intro to Explorer and OOD

**What this is.** Video 3 of the series *Research Computing on Explorer and AICR*. **Status:** published.

**Watch the film:** https://youtu.be/LIjhb1dokME (unlisted link). Playlist: https://www.youtube.com/playlist?list=PLX28mAL5_hLk

**Read the guide:** [`guide.md`](guide.md) is our written version of the lesson. It follows the film's structure, adds the exact commands the film cannot carry, and records what we tested ourselves and where the original is wrong or silent.

## Where it comes from

Based on Northeastern University Research Computing's training lesson, presented by Serena Caplins: https://github.com/northeastern-rc-training/Intro-to-Explorer-OOD-2026. **This repository does not reproduce that lesson.** The guide and the film are our own rewrite: the structure follows our film, the wording, examples and exercises are ours, and we added what we learned using it. The original remains the authority and belongs to its authors.

## What is in this folder

- `guide.md`: the written lesson (our own words), with the film link, the citation, exercises, and corrections.
- `images/`: our diagrams, each as SVG (editable source) and PNG (embedded in the guide).
- `build/`: how the film was made. `beat_sheet.json` is the heart (one entry per shot: narration, picture, timing). `make_sheet.py` regenerates it; `scenes.py` holds the Manim animations; `ACTS.md`, `SHOTLIST.md`, `FACTCHECK.md` and the other `.md` files are the plan and the record. Rendered video, audio and large images are not included (they are rebuilt, see below).

## Images we do not republish

The film's pictures include 8 screenshots from Research Computing's own lesson (`screenshot_OOD.png`, `screenshot_files1.png`, `screenshot_files2.png`, `screenshot_files3.png`, `screenshot_jobs.png`, `screenshot_jobs2.png`, `screenshot_rstudio.png`, `screenshot_rstudio3.png`). They belong to their authors and are not in this repository. To rebuild the film, download them from https://github.com/northeastern-rc-training/Intro-to-Explorer-OOD-2026/tree/main/images into `build/captures/`.

## Redo it

The films are built with the [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit (Manim and Remotion scenes, free Kokoro narration). Put `build/` where the toolkit expects a film folder, regenerate the audio and run its review and final steps. The narration was voiced with Liam, an AI voice (Kokoro `am_onyx`), speaking in for the author.

